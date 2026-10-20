"""Original fixed inclined grizzly ore screen. One static, independently editable prop.
Seven longitudinal solid bars, six full-length slots, a continuous thick open
collector and an open low-end lip. No old asset geometry imports or reuse.
Pure modelling data precede BLENDER PHASE. Geometry and render modes are separate.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='cave-mine-inclined-grizzly-screen-01';VERSION='1.0.0';TITLE='Inclined Grizzly Ore Screen'
DESCRIPTION=('One original static low-poly inclined ore-screen prop: seven solid longitudinal grizzly bars and six genuine long slots, a separate continuous thick-walled open collector with a through discharge neck, and a low-end open U-shaped coarse-material lip. Four flat feet and finite grounded support chains. Three opaque constant PBR materials; no textures. Metres, source Z up, low end -Y, horizontal bounds-centred origin at ground. One complete prop, no scene or separately counted components. A fixed stylised visual design only: no real screening, particle size, throughput, granular flow, vibration, powered drive, motion, rigging, physics, collision, load, stability, manufacturing, equipment compatibility or safety certification.')
PALETTE=[('DeepTeal_SupportFrame',(.055,.18,.18,1),.68,.20),('MutedOchre_Collector',(.48,.275,.075,1),.68,.16),('QuietSteel_GrizzlyBars',(.36,.43,.44,1),.56,.48)]
G={};JOINTS=[];FEET=[];VOIDS={};CLEARANCE_PAIRS=[]
SLOPE=.30;Y_SHIFT=.12
FOCUS=(0,0,.76);ORTHO=2.65
CAMERAS={'gray-front3q':(3.2,-4.8,3.5),'gray-back3q':(-3.2,4.8,3.5),'thumbnail':(3.2,-4.8,3.5),'qa-front':(0,-5,.76),'qa-side':(5,0,.76),'qa-top':(0,0,6),'qa-back':(0,5,.76),'qa-wireframe':(3.2,-4.8,3.5),'silhouette-128-front':(0,-5,.76),'silhouette-128-side':(5,0,.76)}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def world(p):x,y,w=p;return (x,y+Y_SHIFT,w+SLOPE*y)
def raw_world(p):x,y,z=p;return(x,y+Y_SHIFT,z)
def triangulate_polygon(points):
 if len(points)==3:return [(0,1,2)]
 normal=[0.,0.,0.]
 for p,q in zip(points,points[1:]+points[:1]):normal=add(normal,cross(p,q))
 drop=max(range(3),key=lambda i:abs(normal[i]));v=[tuple(p[i] for i in range(3) if i!=drop) for p in points]
 cr=lambda a,b:a[0]*b[1]-a[1]*b[0];area=sum(cr(p,q) for p,q in zip(v,v[1:]+v[:1]));order=list(range(len(v)));out=[]
 if area<0:order.reverse()
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(sub(v[b],v[a]),sub(v[c],v[b]))<1e-13:continue
   if any(all(cr(sub(v[y],v[x]),sub(v[k],v[x]))>=-1e-13 for x,y in [(a,b),(b,c),(c,a)]) for k in order if k not in (a,b,c)):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('bad polygon',points,order)
 out.append(tuple(order));return out if area>0 else [tuple(reversed(t)) for t in out]
def geom(v,f,role,mat=0):
 v=[tuple(round(float(c),9) for c in p) for p in v];tri=[]
 for face in f:tri.extend(tuple(face[k] for k in t) for t in triangulate_polygon([v[k] for k in face]))
 edges={}
 for i,face in enumerate(tri):
  for a,b in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
 assert all(len(e)==2 for e in edges.values()),role
 signs={0:1};todo=[0]
 while todo:
  i=todo.pop()
  for a,b in zip(tri[i],tri[i][1:]+tri[i][:1]):
   for j,c,d in edges[tuple(sorted((a,b)))]:
    if i==j:continue
    want=signs[i]*(-1 if (a,b)==(c,d) else 1)
    if j in signs:assert signs[j]==want
    else:signs[j]=want;todo.append(j)
 assert len(signs)==len(tri)
 tri=[t if signs[i]>0 else tuple(reversed(t)) for i,t in enumerate(tri)]
 volume=sum(dot(v[t[0]],cross(v[t[1]],v[t[2]])) for t in tri)/6
 if volume<0:tri=[tuple(reversed(t)) for t in tri]
 return {'vertices':v,'faces':tri,'material':mat,'face_materials':[mat]*len(tri),'role':role}
def put(name,g):assert name not in G;G[name]=g;return name
BOXF=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def boxg(lo,hi,shear=True,role='finite closed box',mat=0):
 v=[(lo[0],lo[1],lo[2]),(hi[0],lo[1],lo[2]),(hi[0],hi[1],lo[2]),(lo[0],hi[1],lo[2]),(lo[0],lo[1],hi[2]),(hi[0],lo[1],hi[2]),(hi[0],hi[1],hi[2]),(lo[0],hi[1],hi[2])]
 return geom([(world if shear else raw_world)(p) for p in v],BOXF,role,mat)
def box(name,lo,hi,mat,role,shear=True):return put(name,boxg(lo,hi,shear,role,mat))
def extrude(name,polygon,y0,y1,mat,role):
 n=len(polygon);v=[world((x,y,w)) for y in (y0,y1) for x,w in polygon];f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return put(name,geom(v,f,role,mat))
def chamfer_xw(name,x0,x1,w0,w1,y0,y1,b,mat,role):
 p=[(x0+b,w0),(x1-b,w0),(x1,w0+b),(x1,w1-b),(x1-b,w1),(x0+b,w1),(x0,w1-b),(x0,w0+b)]
 return extrude(name,p,y0,y1,mat,role)
def joint(a,b,lo,hi,shear=True,role='complete finite embedded connection core'):
 JOINTS.append({'a':a,'b':b,'geometry':boxg(lo,hi,shear,role),'role':role})
BARS=[]
for i,x in enumerate([-.48,-.32,-.16,0,.16,.32,.48],1):
 n=chamfer_xw('GrizzlyBar_%02d'%i,x-.035,x+.035,1.095,1.18,-.85,.85,.004,2,'One of seven solid longitudinal grizzly bars, with full thickness and chamfered long edges');BARS.append(n)
for side,x in [('L',-.665),('R',.665)]:
 beam=chamfer_xw('SideBeam_'+side,x-.04,x+.04,1.0,1.245,-.88,.88,.005,0,'Fixed inclined outer side beam and side guard, clear of all six internal slots')
 for end,y in [('Low',-.76),('High',.76)]:
  foot=box('Foot_'+side+'_'+end,(x-.09,y-.095,0),(x+.09,y+.095,.05),0,'Flat finite ground pad',False);FEET.append(foot)
  leg=box('Leg_'+side+'_'+end,(x-.0425,y-.045,.038),(x+.0425,y+.045,1.045+.30*y),0,'Full vertical leg from foot to side beam',False)
  joint(foot,leg,(x-.03,y-.03,.041),(x+.03,y+.03,.047),False)
  joint(beam,leg,(x-.026,y-.025,1.008),(x+.026,y+.025,1.021),True)
 tie=box('LowerSideTie_'+side,(x-.028,-.775,.27),(x+.028,.775,.325),0,'External lower side tie; does not obstruct throat or central unloading domain',False)
 for end,y in [('Low',-.76),('High',.76)]:joint(tie,'Leg_'+side+'_'+end,(x-.02,y-.01,.28),(x+.02,y+.01,.315),False)
 # Solid side diagonal confined to the outer side-frame plane.
 p0=(x,-.68,.31);p1=(x,.68,1.02+.30*.68);dy=p1[1]-p0[1];dz=p1[2]-p0[2];le=math.sqrt(dy*dy+dz*dz);oy=-dz/le*.028;oz=dy/le*.028
 v=[raw_world((xx,y+sy*oy,z+sy*oz)) for xx in (x-.026,x+.026) for y,z,sy in [(p0[1],p0[2],-1),(p1[1],p1[2],-1),(p1[1],p1[2],1),(p0[1],p0[2],1)]]
 brace=put('DiagonalBrace_'+side,geom(v,BOXF,'Finite rigid diagonal side brace',0))
 joint(brace,tie,(x-.015,-.669,.317),(x+.015,-.663,.321),False)
 joint(brace,beam,(x-.015,.661,1.005),(x+.015,.667,1.012),True)
for end,y in [('Low',-.8175),('High',.8175)]:
 beam=box('CrossSupport_'+end,(-.685,y-(.0365 if end=='Low' else .0325),1.065),(.685,y+(.0365 if end=='High' else .0325),1.11),0,'End-only transverse support band, leaving the complete central long-slot lengths open')
 for side,x in [('L',-.665),('R',.665)]:joint(beam,'SideBeam_'+side,(x-.018,y-.020,1.075),(x+.018,y+.020,1.100))
 for i,x in enumerate([-.48,-.32,-.16,0,.16,.32,.48],1):joint(BARS[i-1],beam,(x-.034,y-.0315,1.100),(x+.034,y+.0315,1.109),role='Entire inset bar-end overlap across full usable support width and end-band length')
# Single continuous annular material shell. No face caps either aperture.
profile=[(.19,.25,.32),(.19,.25,.45),(.59,.82,1.025),(.605,.835,1.025),(.605,.835,1.055),(.56,.79,1.055),(.16,.22,.45),(.16,.22,.32)]
def rectangle(a,b,w):return [(-a,-b,w),(a,-b,w),(a,b,w),(-a,b,w)]
v=[world(p) for a,b,w in profile for p in rectangle(a,b,w)];f=[(4*k+i,4*k+(i+1)%4,4*((k+1)%len(profile))+(i+1)%4,4*((k+1)%len(profile))+i) for k in range(len(profile)) for i in range(4)]
FUNNEL=put('Collector_ContinuousThickOpenShell',geom(v,f,'One connected thick tapering collector with genuine top mouth and rectangular open discharge neck',1))
for side,x in [('L',-.6275),('R',.6275)]:
 for end,y in [('Low',-.42),('High',.42)]:
  # Inner edge stops outside the actual cavity; includes shell overlap only.
  bracket=box('CollectorBracket_'+side+'_'+end,(x-.0625,y-.045,.98),(x+.0625,y+.045,1.04),0,'External thick collector bracket, kept wholly outside inner cavity')
  sx=-1 if side=='L' else 1
  joint(bracket,'SideBeam_'+side,(sx*.660-.012,y-.027,1.010),(sx*.660+.012,y+.027,1.030))
  joint(bracket,FUNNEL,(sx*.570-.002,y-.025,1.005),(sx*.570+.002,y+.025,1.018))
LIP=extrude('LowEnd_OpenULip',[(-.60,1.13),(.60,1.13),(.60,1.28),(.55,1.28),(.55,1.177),(-.55,1.177),(-.55,1.28),(-.60,1.28)],-1.12,-.83,1,'Thick continuous U-shaped low-end lip, no exit cap; 3mm fixed downward visual step from bar tops')
for i,x in enumerate([-.48,-.32,-.16,0,.16,.32,.48],1):joint(LIP,BARS[i-1],(x-.025,-.847,1.138),(x+.025,-.834,1.169),role='Complete finite lip attachment overlap at grizzly low end')
for i in range(6):
 x0=-.48+i*.16+.035+.002;x1=x0+.086
 VOIDS['LongSlot_%02d'%(i+1)]={'geometry':boxg((x0,-.783,1.090),(x1,.783,1.186)), 'scope':'Entire long-slot prism, 2mm side inset and 2mm endpoint gap beyond support inner edge, through full 85mm bar thickness plus 5mm below/6mm above'}
def solid_rings(rings,role):
 v=[world(p) for a,b,w in rings for p in rectangle(a,b,w)];f=[(3,2,1,0),tuple(range(4*(len(rings)-1),4*len(rings)))]+[(4*k+i,4*k+(i+1)%4,4*(k+1)+(i+1)%4,4*(k+1)+i) for k in range(len(rings)-1) for i in range(4)]
 return geom(v,f,role)
VOIDS['FullCollectorCavity']={'geometry':solid_rings([(.157,.217,.307),(.157,.217,.449),(.557,.787,1.057)],'Complete finite rectangular neck plus tapered cavity; all walls/corners and height rings included'), 'scope':'Continuous full lower mouth, full throat and full taper, 3mm coordinate inset from independent inner dimensions; exact minimum distances checked separately'}
VOIDS['FullThroat']={'geometry':boxg((-.157,-.217,.307),(.157,.217,.455)),'scope':'Entire throat width/depth, complete neck length and 13mm below/5mm above'}
VOIDS['FiniteGroundClearance']={'geometry':boxg((-.153,-.213,.001),(.153,.213,.385),False),'scope':'Only this explicitly bounded central box from Z=.001 to .385; no claim for all space under the machine'}
VOIDS['FullCoarseLipOpenDomain']={'geometry':boxg((-.547,-1.13,1.1805),(.547,-.832,1.33)),'scope':'Whole open U interior and both side-adjacent outlet corners, from 3.5mm above bottom and 0.5mm above attachment bars to above walls, from attachment edge through 10mm past exit'}
for a,b in zip(BARS,BARS[1:]):CLEARANCE_PAIRS.append({'a':a,'b':b,'minimum_m':.0899,'role':'entire neighbouring grizzly bar surfaces'})
for a in BARS:CLEARANCE_PAIRS.append({'a':a,'b':FUNNEL,'minimum_m':.0382,'role':'entire grizzly underside and collector upper rim remain separate'})
for side in ['L','R']:CLEARANCE_PAIRS.append({'a':'SideBeam_'+side,'b':FUNNEL,'minimum_m':.0199,'role':'collector entire shell from unconnected inclined side beam'})
for end in ['Low','High']:
 for side in ['L','R']:CLEARANCE_PAIRS.append({'a':'Leg_'+side+'_'+end,'b':FUNNEL,'minimum_m':.015,'role':'entire leg from collector and throat'})

def measurements():
 vv=[v for g in G.values() for v in g['vertices']];lo=[min(v[k] for v in vv) for k in range(3)];hi=[max(v[k] for v in vv) for k in range(3)]
 return {'bounds_min_m':lo,'bounds_max_m':hi,'bounds_m':[round(b-a,9) for a,b in zip(lo,hi)],'bar_count':7,'slot_count':6,'slot_clear_width_m':.09,'slot_evidence_length_m':1.566,'bar_vertical_thickness_m':.085,'slope':.30,'angle_degrees':math.degrees(math.atan(.30)),'lip_visual_downstep_m':.003,'lip_overlap_length_m':.020,'bar_bottom_to_rim_vertical_gap_m':.040,'coordinate_transform':{'x': 'unchanged','y':'design_y + 0.12','z':'w + 0.30 * design_y; raw-world legs/feet use literal z'},'mesh_count':len(G),'triangles':sum(len(g['faces']) for g in G.values()),'single_prop_count':1,'new_scene_count':0}
# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
scene=bpy.context.scene
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
bpy.context.preferences.filepaths.save_version=0
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p and not any(n.type.startswith('TEX_') for n in m.node_tree.nodes) and not any(s.is_linked for s in p.inputs)
 values={}
 for n in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  v=p.inputs[n].default_value;values[n]=[round(float(x),6) for x in v] if hasattr(v,'__len__') else round(float(v),6)
 assert values['Alpha']==1 and values['Transmission Weight']==0 and values['Emission Strength']==0
 values['double_sided']=not m.use_backface_culling;return values

def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices];rows.append((o.name,min(tuple(q[i:]+q[:i]) for i in range(3)),json.dumps(pbr(o.data.materials[t.material_index]),sort_keys=True)))
 return sorted(rows)
def fingerprint(objects):return hashlib.sha256(json.dumps(records(objects),separators=(',',':')).encode()).hexdigest()
if '--render-only' not in sys.argv:
 mats=[]
 for name,color,rough,metal in PALETTE:
  m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
  p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
 root=bpy.data.objects.new('OneInclinedGrizzlyOreScreen',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['origin_datum']='horizontal bounds centre at ground Z=0';root['front_direction']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
 parts=[];checks=[]
 for name,g in G.items():
  me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o['component_role']=g['role'];parts.append(o)
  for m in mats:me.materials.append(m)
  for face in me.polygons:face.material_index=g['material'];face.use_smooth=False
  bm=bmesh.new();bm.from_mesh(me);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();me.calc_loop_triangles();deg=sum(t.area<1e-12 for t in me.loop_triangles);assert not bad and not deg and volume>0
  checks.append({'name':name,'nonmanifold_edges':bad,'signed_volume_m3':volume,'degenerate_triangles':deg,'triangles':len(me.loop_triangles)})
 bpy.context.view_layer.update();source_fp=fingerprint(parts)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts+[root]:o.select_set(True)
 bpy.context.view_layer.objects.active=root
 bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
 guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
 qa={'asset':ASSET,'review_basis':'maker-self-reviewed','blender':bpy.app.version_string,'measurements':measurements(),'components':checks,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'geometry produced; full gates pending'}
else:qa=json.loads((OUT/'qa-report.json').read_text());source_fp=qa['world_oriented_triangle_full_solid_pbr_sha256']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];assert fingerprint(parts)==source_fp
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_constant_pbr_and_names_match':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'mesh_count':len(parts)}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/cave-mine/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 ms=measurements();d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'cave-mine','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],ms['bounds_m']),unit='m'),'triangles':ms['triangles'],'materials':3,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
saveqa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,measurements());sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset';m=bpy.data.materials.new('Preview_slate');m.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(m)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for face in dup.data.polygons:face.material_index=0
   wire=dup.modifiers.new('Preview_actual_edges','WIREFRAME');wire.thickness=.0025;wire.use_replace=True;wire.use_even_offset=False;wire.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for face in o.data.polygons:face.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name in ['silhouette-128-front','silhouette-128-side']:render(name,CAMERAS[name])
qa.setdefault('render_seconds',{}).update(seconds);qa.setdefault('render_configs',{}).update(configs);qa['status']='maker-self-reviewed render data produced; visual and full geometry acceptance separate';saveqa()
if not gray:metadata()
print('ASSET_RENDER_COMPLETE',ASSET,seconds)
