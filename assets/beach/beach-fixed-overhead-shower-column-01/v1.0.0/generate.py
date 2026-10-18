"""Original fixed beach shower exterior; no plumbing or water function is modelled."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beach-fixed-overhead-shower-column-01';VERSION='1.0.0';TITLE='Fixed Overhead Beach Shower Column'
DESCRIPTION=('One original static low-poly freestanding beach shower exterior. A thick grounded octagonal foot supports one continuous tall post, chamfered overhead arm and integral downturned terminal. A broad thick downward-facing head has one continuous closed shell surrounding a real recessed empty cavity, and one separate continuous thick faceplate with sixteen genuine square through-openings reaching that cavity. The faceplate is finitely seated into all four shell rims. One fixed side valve block and inset round push button complete the silhouette. Six named closed editable meshes, four opaque constant unlinked PBR materials, metres, source Z up, front -Y and origin on the post centreline at ground. One complete assembly counts as one prop. No water, person, sand, platform, drain, hose, foot tap, enclosure, texture, logo or animation. '
 'The head cavity and holes are visual geometric details only. There is no modelled supply route inside the post or base. No water supply or drainage, pressure, spray coverage, flow, temperature, hot/cold control, valve operation, hygiene, drinking-water suitability, human fit, wet-slip, corrosion resistance, strength, loads, stability, installation, manufacturing tolerance or public-facility safety certification is claimed. Not real plumbing, equipment design, installation or use guidance. No brand or compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=['Shower_GroundedFoot'];VOID_PROBES={};EMBED_PROBES=[];PAIR_REGIONS={}
PALETTE=[('SeaTeal_Column',(.045,.26,.245,1),.43,.45),('SatinSilver_HeadAndValve',(.55,.62,.63,1),.30,.78),('Graphite_FootAndFaceplate',(.055,.078,.080,1),.55,.40),('WarmBrass_FixedButton',(.58,.33,.085,1),.39,.60)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,-.25,1.29);ORTHO=3.20
CAMERAS={'gray-front3q':(4,-6,3.05),'gray-back3q':(-3,4,-1.0),'thumbnail':(4,-6,3.05),'qa-front':(0,-7,3.00),'qa-side':(7,-.25,3.00),'qa-top':(0,-.25,7),'qa-back':(0,7,3.00),'qa-wireframe':(4,-6,3.05),'silhouette-128-front':(0,-7,3.00),'silhouette-128-side':(7,-.25,3.00)}
TECHNICAL_UNDERSIDE_VIEWS={'gray-back3q'}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,p,mat=0,tag=''):
  ids=[self.vertex(q) for q in p]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def cuboid(name,lo,hi,mat,role):
 m=Mesh();v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 for f in [(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.face([v[i] for i in f],mat)
 G[name]=m.result(role,mat)
def grid_solid(name,xs,ys,zs,keep,mat,role):
 # Conforming cell-boundary union: internal faces disappear. No booleans, hidden
 # solid backing, black-dot perforations or intersecting bars substitute for holes.
 boundary={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    if not keep(i,j,k):continue
    v=[(xs[a],ys[b],zs[c]) for c in [k,k+1] for b in [j,j+1] for a in [i,i+1]]
    for f in [(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:
     q=[v[a] for a in f];key=tuple(sorted(q))
     if key in boundary:del boundary[key]
     else:boundary[key]=q
 m=Mesh()
 for q in boundary.values():m.face(q,mat)
 G[name]=m.result(role,mat)
def earclip2(poly):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 order=list(range(len(poly))) if area>0 else list(reversed(range(len(poly))));out=[]
 while len(order)>3:
  found=False
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-12:continue
   if any(all(cr(poly[x],poly[y],poly[q])>=-1e-12 for x,y in [(a,b),(b,c),(c,a)]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(k);found=True;break
  assert found
 out.append(tuple(order));return out
# Thick tapered octagonal grounding foot, with no exported ground slab.
outline=[(-.17,-.21),(.17,-.21),(.23,-.15),(.23,.15),(.17,.21),(-.17,.21),(-.23,.15),(-.23,-.15)]
lo=[(x,y,0) for x,y in outline];hi=[(x*.85,y*.85,.12) for x,y in outline];m=Mesh()
m.face(lo[::-1],2);m.face(hi,2)
for i in range(8):j=(i+1)%8;m.face([lo[i],lo[j],hi[j],hi[i]],2)
G['Shower_GroundedFoot']=m.result('One thick finite octagonal grounded foot. No waterway, anchors or slab.',2)
# Concave sagittal extrusion is one continuous closed column-and-arm body.
ARM_PROFILE=[(.075,.09),(.075,2.45),(-.015,2.54),(-.600,2.54),(-.655,2.485),(-.655,2.320),(-.545,2.320),(-.545,2.410),(-.110,2.410),(-.065,2.365),(-.065,.09)]
m=Mesh();aa=[(-.055,y,z) for y,z in ARM_PROFILE];bb=[(.055,y,z) for y,z in ARM_PROFILE]
for f in earclip2(ARM_PROFILE):m.face([aa[i] for i in f][::-1],0);m.face([bb[i] for i in f],0)
for i in range(len(aa)):j=(i+1)%len(aa);m.face([aa[i],aa[j],bb[j],bb[i]],0)
G['Shower_ContinuousPostArm']=m.result('One actual continuous tall post, chamfered cantilever arm and downward terminal. Solid visual exterior, no supply pipe.',0)
grid_solid('Shower_RecessedHeadShell',[-.175,-.153,.153,.175],[-.775,-.753,-.447,-.425],[2.245,2.310,2.332],lambda i,j,k:k==1 or i!=1 or j!=1,1,'One continuous thick downward open shell with a closed top and four real cavity walls; no solid cavity fill.')
HOLE_CENTRES=[(x,-.60+y) for y in [-.09,-.03,.03,.09] for x in [-.09,-.03,.03,.09]]
xs=sorted(set([-.162,.162]+[x+s for x in [-.09,-.03,.03,.09] for s in [-.012,.012]]));ys=[-.60+x for x in xs]
grid_solid('Shower_ThroughHoleFaceplate',xs,ys,[2.235,2.255],lambda i,j,k:not(i%2==1 and j%2==1),2,'One continuous 20 mm thick faceplate with sixteen genuine 24 mm square through-holes and a continuous thick perimeter, inserted into all four rim walls.')
cuboid('Shower_FixedValveBlock',[-.075,-.150,1.08],[.075,-.050,1.26],1,'One fixed side valve block finitely inset into front of the post, without working controls or pipe.')
m=Mesh();rings=[[(.043*math.cos(math.tau*i/12),y,1.17+.043*math.sin(math.tau*i/12)) for i in range(12)] for y in [-.210,-.128]]
m.face(rings[0],3);m.face(rings[1][::-1],3)
for i in range(12):j=(i+1)%12;m.face([rings[0][i],rings[1][i],rings[1][j],rings[0][j]],3)
G['Shower_FixedPushButton']=m.result('One thick stationary twelve-sided push-button form with finite valve-body insertion; no actuation or temperature function.',3)

def joint(a,b,regions,probes):
 PAIR_REGIONS[tuple(sorted([a,b]))]=regions
 points=[]
 for lo,hi in probes:
  EMBED_PROBES.append({'a':a,'b':b,'lo_m':lo,'hi_m':hi});points.append(tuple((x+y)/2 for x,y in zip(lo,hi)))
 LINKS.append((a,b,points))
joint('Shower_GroundedFoot','Shower_ContinuousPostArm',[{'lo_m':[-.056,-.066,.089],'hi_m':[.056,.076,.121]}],[([-.04,-.04,.095],[.04,.04,.115])])
joint('Shower_ContinuousPostArm','Shower_RecessedHeadShell',[{'lo_m':[-.056,-.656,2.319],'hi_m':[.056,-.544,2.333]}],[([-.04,-.64,2.322],[.04,-.56,2.330])])
rim_regions=[{'lo_m':[-.163,-.763,2.244],'hi_m':[-.152,-.437,2.256]},{'lo_m':[.152,-.763,2.244],'hi_m':[.163,-.437,2.256]},{'lo_m':[-.163,-.763,2.244],'hi_m':[.163,-.752,2.256]},{'lo_m':[-.163,-.448,2.244],'hi_m':[.163,-.437,2.256]}]
rim_probes=[([-.160,-.73,2.248],[-.155,-.47,2.252]),([.155,-.73,2.248],[.160,-.47,2.252]),([-.13,-.760,2.248],[.13,-.755,2.252]),([-.13,-.445,2.248],[.13,-.440,2.252])]
joint('Shower_RecessedHeadShell','Shower_ThroughHoleFaceplate',rim_regions,rim_probes)
joint('Shower_ContinuousPostArm','Shower_FixedValveBlock',[{'lo_m':[-.056,-.066,1.079],'hi_m':[.056,-.049,1.261]}],[([-.04,-.062,1.10],[.04,-.053,1.24])])
joint('Shower_FixedValveBlock','Shower_FixedPushButton',[{'lo_m':[-.044,-.151,1.126],'hi_m':[.044,-.127,1.214]}],[([-.020,-.146,1.15],[.020,-.132,1.19])])
VOID_PROBES['EntireInsetHeadCavity']={'type':'box','lo_m':[-.149,-.749,2.256],'hi_m':[.149,-.451,2.309],'targets':list(G),'role':'one complete finite cavity immediately above plate, below shell ceiling and inside all walls'}
for k,(x,y) in enumerate(HOLE_CENTRES):
 VOID_PROBES['FullHoleToCavity_%02d'%k]={'type':'box','lo_m':[x-.011,y-.011,2.230],'hi_m':[x+.011,y+.011,2.307],'targets':list(G),'role':'complete square bore volume, beyond underside through full plate thickness into actual common head cavity'}
 BORES.append({'mesh':'Shower_ThroughHoleFaceplate','origin_m':(x,y,2.230),'direction':(0,0,1),'length_m':.078,'role':'actual isolated full thickness square spray face opening'})
VOID_PROBES['WholeDownwardFreeSpace']={'type':'box','lo_m':[-.174,-.774,.005],'hi_m':[.174,-.426,2.234],'targets':list(G),'role':'entire below-head envelope down to ground, clear of foot, post, arm and control'}
def measure_shower_geometry(vertices):
 def bounds(v):return[(min(p[i] for p in v),max(p[i] for p in v)) for i in range(3)]
 return {'single_prop_count':1,'mesh_count':len(G),'faceplate_hole_count':len(HOLE_CENTRES),'head_cavity_clear_box_m':[.298,.298,.053],'faceplate_thickness_m':.020,'individual_hole_section_m':[.024,.024],'shell_wall_thickness_m':.022,'shell_ceiling_thickness_m':.022,'overall_height_m':max(p[2] for v in vertices.values() for p in v),'continuous_post_arm_actual_bounds_m':bounds(vertices['Shower_ContinuousPostArm']),'finite_embedded_interface_count':len(LINKS),'finite_embedded_probe_count':len(EMBED_PROBES),'materials':MATERIAL_CONTRACT,'functional_scope':'one static fixed shower exterior only; no waterway, water, hygiene or safety performance claim'}
# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFixedBeachShowerColumn',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X centreline, design Y=0 and ground Z=0; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]

# Geometry-only source checks are repeated on actual generated Blender triangles.
# Independent acceptance separately imports the final GLB and verifies the entire interface.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
shower_evidence=measure_shower_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
adj={name:set() for name in G}
for a,b,points in LINKS:
 samples=[]
 for p in points:
  margin=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3]);valid=actual_inside(a,p) and actual_inside(b,p) and margin>.0001;assert valid,(a,b,p,margin)
  samples.append({'point_m':p,'both_interiors':True,'nearest_boundary_margin_m':margin})
 joints.append({'a':a,'b':b,'samples':samples});adj[a].add(b);adj[b].add(a)
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m']);assert hit[0] is None,(r,hit)
 bore_checks.append(dict(r,actual_isolated_full_thickness_clear=True))
for r in CONTACTS:
 a,b=r['a'],r['b'];eps=r['interior_probe_offset_m']
 for p in r['points']:
  low=(p[0],p[1],p[2]-eps);high=(p[0],p[1],p[2]+eps)
  assert actual_inside(a,low) and actual_inside(b,high) and not actual_inside(a,high) and not actual_inside(b,low),(a,b,p)
 adj[a].add(b);adj[b].add(a);face_contacts.append(dict(r,actual_opposed_interior_side_probes=True,full_area_scope='pure source and independent actual GLB full-surface audit'))
todo=list(seen)
while todo:
 for name in adj[todo.pop()]-seen:seen.add(name);todo.append(name)
assert seen==set(G),seen
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<12000
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':1,'shower_geometry':shower_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'technical_underside_view':{'name':'gray-back3q','diagnostic_only':True,'asset_geometry_complete':True,'preview_ground_only_temporarily_hidden':True,'restoration':'finally block'},'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beach/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beach','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-front-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--gray-front-only' in sys.argv:views={'gray-front3q':views['gray-front3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();previous_ground_hidden=ground.hide_render
 if name in TECHNICAL_UNDERSIDE_VIEWS:ground.hide_render=True
 try:bpy.ops.render.render(write_still=True)
 finally:ground.hide_render=previous_ground_hidden
 seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-front-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
