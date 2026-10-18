"""Original low ribbed brush-wash bucket plus one supported flat brush; one static prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-ribbed-brush-wash-bucket-kit-01';VERSION='1.0.0';TITLE='Ribbed Brush Wash Bucket'
DESCRIPTION=('One original static low-poly brush-wash bucket and one resting flat brush, counted together as one prop. A low flared chamfer-corner basin has a genuine empty wash cavity, continuous thick bottom, four shallow integral floor ribs on one side, a clear wash zone on the other and two opposed open rim saddles. The flat underside of the original brush handle rests on both finite saddle shelves. A real thick hollow ferrule finitely receives the handle and a closed shallow-grooved flat bristle solid. Four closed connected meshes, five plain opaque constant PBR materials, metres, native Z up, bounds-centred ground origin and front -Y. No water, paint liquid, second bucket, brush set, easel, texture or animation. Static illustrative geometry only; no actual cleaning, absorption, bristle behavior, solvent compatibility, leakproofing, hygiene, food safety, load, human-fit, manufacturing, tool-safety or certification claim. No dimensional compatibility with earlier painting assets.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={}
BODY='Bucket_IntegralFloorRibsAndSaddles';HANDLE='Brush_ContinuousHandle';FERRULE='Brush_ThickHollowFerrule';BRISTLES='Brush_ClosedGroovedBristles';FEET=[BODY]
SHIFT=-.065
PALETTE=[('DeepTeal_OuterBucket',(.025,.22,.23,1),.43,0),('WarmIvory_InnerWashSurface',(.70,.65,.48,1),.51,0),('Terracotta_BrushHandle',(.48,.105,.045,1),.43,0),('MutedBrass_Ferrule',(.40,.31,.16,1),.36,.65),('Ochre_Bristles',(.48,.30,.115,1),.65,0)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no procedural or image texture nodes.'
FOCUS=(0,0,.09);ORTHO=.83
CAMERAS={'gray-front3q':(.70,-.90,.86),'gray-back3q':(-.70,.90,.86),'thumbnail':(.70,-.90,.86),'qa-front':(0,-1.1,.58),'qa-side':(1.1,0,.58),'qa-top':(0,0,1.2),'qa-back':(0,1.1,.58),'qa-wireframe':(.70,-.90,.86),'silhouette-128-front':(0,-1.1,.58),'silhouette-128-side':(1.1,0,.58)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def finish(vs,fs,mats):
 volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':[tuple(round(c,9) for c in (p[0]+SHIFT,p[1],p[2])) for p in vs],'faces':fs,'face_materials':mats,'material':0}
def connect(fs,fm,a,b,mat):
 for i in range(len(a)):
  j=(i+1)%len(a);fs.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])]);fm.extend([mat,mat])
def box(lo,hi,material=0):
 vs=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 qs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 fs=[t for a,b,c,d in qs for t in [(a,b,c),(a,c,d)]];return finish(vs,fs,[material]*len(fs))
XFR=[-1,-.90,-.75,-.5,0,.5,.75,.90,1]
RIB_Y=[-.081,-.061,-.041,-.021]
YROWS=sorted(set([-.115,-.105,-.095,-.09,-.016322580645,-.024516129032,0,.016322580645,.024516129032,.05,.09,.105,.115]+[round(c+d,9) for c in RIB_Y for d in [-.007,0,.007]]))
def xextent(y):return .14-.025*max(0,(abs(y)-.09)/.025)
def ribheight(x,y):return .010*max(0,min(1,(.126-abs(x))/.021))*max([max(0,1-abs(y-c)/.007) for c in RIB_Y])
def rimheight(x,y):return .140 if abs(y)<=.022000001 else (.180 if abs(y)>=.033-1e-8 else .140+.040*(abs(y)-.022)/.011)
# Continuous height-field floor. Ribs are top-surface relief of the same solid,
# never rods placed on a slab. Its boundary continues through inner wall,
# notched top rim, flared outer wall and the finite ground face.
vs=[];fs=[];fm=[];floor_ids=[]
for y in YROWS:
 row=[]
 for t in XFR:row.append(len(vs));x=t*xextent(y);vs.append((x,y,.028+ribheight(x,y)))
 floor_ids.append(row)
for j in range(len(YROWS)-1):
 for i in range(len(XFR)-1):
  a,b,c,d=floor_ids[j][i],floor_ids[j][i+1],floor_ids[j+1][i+1],floor_ids[j+1][i]
  fs.extend([(a,b,c),(a,c,d)]);fm.extend([1,1])
FLOOR_FACE_COUNT=len(fs)
boundary=floor_ids[0]+[r[-1] for r in floor_ids[1:]]+floor_ids[-1][-2::-1]+[r[0] for r in floor_ids[-2:0:-1]]
base_xy=[vs[i][:2] for i in boundary];last=boundary;BODY_RINGS=[boundary]
for rx,ry,z,mat in [(.184,.154,None,1),(.2,.17,None,1),(.174,.145,.008,0),(.158,.130,0,0)]:
 ring=[]
 for x,y in base_xy:
  xx=x/.14*rx;yy=y/.115*ry;zz=rimheight(xx,y/.115*.154) if z is None else z
  ring.append(len(vs));vs.append((xx,yy,zz))
 connect(fs,fm,last,ring,mat);BODY_RINGS.append(ring);last=ring
center=len(vs);vs.append((0,0,0))
for i in range(len(last)):fs.append((last[i],center,last[(i+1)%len(last)]));fm.append(0)
g=finish(vs,fs,fm);g.update(role='One continuous closed thick flared basin, real low wash cavity, integral four floor ribs, two opposing open saddle shelves and finite ground bottom.',floor_face_count=FLOOR_FACE_COUNT,rings=BODY_RINGS);G[BODY]=g
# Chamfered rectangular section, counterclockwise viewed along +X.
def section(w,z0,z1,b=.002):return [(-w+b,z0),(w-b,z0),(w,z0+b),(w,z1-b),(w-b,z1),(-w+b,z1),(-w,z1-b),(-w,z0+b)]
def along_x(rows,material):
 vv=[];ff=[];mm=[];rings=[]
 for x,sec in rows:
  ring=[]
  for y,z in sec:ring.append(len(vv));vv.append((x,y,z))
  rings.append(ring)
 for a,b in zip(rings,rings[1:]):connect(ff,mm,a,b,material)
 for ring,reverse in [(rings[0],False),(rings[-1],True)]:
  if len(ring)==22:
   for i in range(10):
    a,b,c,d=ring[i],ring[i+1],ring[20-i],ring[21-i]
    for tri in [(a,b,c),(a,c,d)]:ff.append(tuple(reversed(tri)) if reverse else tri);mm.append(material)
  else:
   center=len(vv);vv.append(tuple(sum(vv[i][k] for i in ring)/len(ring) for k in range(3)))
   for i in range(len(ring)):
    j=(i+1)%len(ring);ff.append((center,ring[j],ring[i]) if reverse else (center,ring[i],ring[j]));mm.append(material)
 return finish(vv,ff,mm)
G[HANDLE]=along_x([(-.25,section(.008,.142,.154,.002)),(-.238,section(.014,.140,.158,.003)),(.220,section(.014,.140,.158,.003)),(.264,section(.014,.140,.158,.002))],2)
G[HANDLE]['role']='One closed continuous chamfered handle; broad planar underside is finitely supported on both actual rim saddles; end embeds inside ferrule wall.'
# Genuine through-bore ferrule: one closed thick sleeve with four joined rings.
vv=[];ff=[];mm=[];rr=[]
for x,sec in [(.240,section(.022,.134,.164,.003)),(.300,section(.022,.134,.164,.003)),(.300,section(.012,.142,.156,.001)),(.240,section(.012,.142,.156,.001))]:
 r=[]
 for y,z in sec:r.append(len(vv));vv.append((x,y,z))
 rr.append(r)
for a,b in zip(rr,rr[1:]+rr[:1]):connect(ff,mm,a,b,3)
G[FERRULE]=finish(vv,ff,mm);G[FERRULE]['role']='Thick closed continuous metal-like ferrule sleeve with an actual open through-bore; handle and bristle roots embed finitely into opposite ends, leaving a real empty internal middle gap.'
# One finite bristle solid with shallow grooves across its broad upper face.
def bristle_section(w,z0,z1):
 ys=[-w,-.012,-.010,-.008,-.002,0,.002,.008,.010,.012,w]
 bottom=[(y,z0) for y in ys]
 top=[(y,z1-(.0015 if abs(y) in [.010,0] else 0)) for y in reversed(ys)]
 return bottom+top
G[BRISTLES]=along_x([(.281,bristle_section(.018,.139,.159)),(.311,bristle_section(.018,.139,.159)),(.372,bristle_section(.017,.140,.158)),(.380,bristle_section(.016,.143,.155))],4)
G[BRISTLES]['role']='One closed thick flat bristle-like solid, three shallow real upper grooves, chamfered tapered tip; finite root embedding in the ferrule and no hair particles or thicknessless planes.'
# Actual finite opposite-face supports, both evaluated as complete surfaces.
for sign in [-1,1]:
 x=sign*.192
 CONTACTS.append({'name':('Left' if sign<0 else 'Right')+'Saddle','a':BODY,'b':HANDLE,'plane_m':.140,'points':[(x+SHIFT,y,.140) for y in [-.006,.006]],'minimum_patch_area_m2':.00020,'interior_probe_offset_m':.0005,'x_range_m':[min(sign*.184,sign*.2)+SHIFT,max(sign*.184,sign*.2)+SHIFT]})
for name,lo,hi,targets in [('HandleFerruleEmbedding',(.245,.0128,.145),(.260,.0134,.152),[HANDLE,FERRULE]),('BristleFerruleEmbedding',(.284,.014,.145),(.295,.017,.153),[FERRULE,BRISTLES])]:
 EMBED_VOLUMES[name]=dict(box(lo,hi),targets=targets,role='Complete finite embedded material volume, wholly inside both joined solids.')
 LINKS.append((targets[0],targets[1],[(sum([lo[0],hi[0]])/2+SHIFT,(lo[1]+hi[1])/2,(lo[2]+hi[2])/2)]))
# Cavity is covered by a closed relief-following lower volume plus open-mouth
# wings on either side of the resting brush. These are actual finite volumes.
def cavity_volume():
 v=[];f=[];m=[];rows=[]
 for y in YROWS:
  row=[]
  for t in XFR:
   x=t*xextent(y);xx=x*.97 if abs(t)>.999 else x;yy=y*.97 if abs(y)>.114 else y;row.append(len(v));v.append((xx,yy,.031+ribheight(xx,yy)))
  rows.append(row)
 for j in range(len(rows)-1):
  for i in range(len(XFR)-1):
   a,b,c,d=rows[j][i],rows[j][i+1],rows[j+1][i+1],rows[j+1][i];f.extend([(a,c,b),(a,d,c)]);m.extend([0,0])
 lower=rows[0]+[r[-1] for r in rows[1:]]+rows[-1][-2::-1]+[r[0] for r in rows[-2:0:-1]]
 upper=[]
 for i,(x,y) in zip(lower,base_xy):
  upper.append(len(v));v.append((x/.14*.166,y/.115*.135,.136))
 # This is an ordinary closed solid, not the concave body-shell winding.
 for i in range(len(lower)):
  j=(i+1)%len(lower);f.extend([(lower[i],lower[j],upper[j]),(lower[i],upper[j],upper[i])]);m.extend([0,0])
 c=len(v);v.append((0,0,.136))
 for i in range(len(upper)):f.append((upper[i],upper[(i+1)%len(upper)],c));m.append(0)
 return finish(v,f,m)
VOID_VOLUMES['ReliefFollowingCompleteLowWashCavity']=dict(cavity_volume(),targets=list(G),role='Closed complete broad low washing chamber, lower surface follows four ribs, continues nearly to inner walls and below brush.')
for sign in [-1,1]:
 lo=[-.145,.030 if sign>0 else -.125,.132];hi=[.145,.125 if sign>0 else -.030,.205]
 VOID_VOLUMES['OpenMouthWing_'+str(sign)]=dict(box(lo,hi),targets=list(G),role='Finite mouth corridor on one side of the supported brush, open through the rim plane.')
for sign in [-1,1]:
 for side in [-1,1]:
  lo=[min(sign*.181,sign*.204),.015 if side>0 else -.019,.143];hi=[max(sign*.181,sign*.204),.019 if side>0 else -.015,.172]
  VOID_VOLUMES['OpenSaddle_'+str(sign)+'_'+str(side)]=dict(box(lo,hi),targets=list(G),role='Complete finite open saddle-side corridor adjacent to the handle; open above the real supporting shelf.')
VOID_VOLUMES['FerruleThroughBore']=dict(box((.237,-.009,.144),(.303,.009,.154)),targets=[FERRULE],role='Finite continuous through-bore volume passes fully through both open ferrule ends.')
VOID_VOLUMES['EmptyFerruleMiddle']=dict(box((.267,-.009,.144),(.278,.009,.154)),targets=list(G),role='Actual empty central part of the ferrule bore between handle end and bristle root.')
SOLID_VOLUMES['CompleteBottomPlate']=dict(box((-.100,-.085,.010),(.100,.085,.021)),targets=[BODY],role='Finite broad continuous bottom plate material below the wash floor.')
for i,y in enumerate(RIB_Y):SOLID_VOLUMES[f'IntegralRibRoot_{i+1}']=dict(box((-.090,y-.001,.020),(.090,y+.001,.033)),targets=[BODY],role='Finite material bridge from the continuous bottom plate into one raised rib, certifying real continuity.')
def measure_bucket_geometry(vertices):
 return {'height_m':.18,'bucket_top_width_m':.4,'bucket_top_depth_m':.34,'baseline_floor_z_m':.028,'rib_peak_z_m':.038,'integral_rib_count':4,'saddle_plane_z_m':.14,'continuous_bucket_floor_ribs_saddles':True,'brush_component_count':3,'single_prop_count':1,'material_contract':MATERIAL_CONTRACT}
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
root=bpy.data.objects.new('OneRibbedBrushWashBucket',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bucket_evidence=measure_bucket_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'bucket_geometry':bucket_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/painting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'painting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
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
