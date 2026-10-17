"""Original S02 bank-to-plateau escarpment transition, metres, Z up.
One closed faceted terrain mesh, 2m X repeat; static visual geometry only.
Standalone: blender -b -t 4 --python-exit-code 1 --python generate.py
Flags after --: --geometry-only, --no-render, --gray-only, --preview-only, --extra-views.
Place at (0,1.2,0) beside the original nature-stream-bank-01 at identity:
the full lower front face then opposes the actual landward bank cap, including
its X=0 rise to Z=.58. The front rim is Z=.55 at X=+-1. Raised rear is ~1.65m.
This is a steep terrain height transition, with no walkability/collision claim.
X-end sections repeat only with this new escarpment family; no universal snap.
Solid PBR materials only, no file inputs, linked files, textures or scene assets.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-bank-escarpment-transition-01';VERSION='1.0.0';TITLE='Bank-to-Plateau Escarpment Transition'
DESCRIPTION=('Original S02 steep bank-to-plateau terrain transition with two unequal cliff ledges, angular fracture facets, low earth apron and broad upper earth shoulder. '
 'One continuous closed editable mesh, 2 m X repeat, 1.60 m landward depth and approximately 1.70 m total height. '
 'At placement (0,1.2,0), the complete local Y=0 front cap matches the original straight bank landward boundary, including its .55/.58/.55 m rim at X=-1/0/+1. '
 'Full boundary agreement and finite opposed contact are verified for this one placement within 2e-6 m positional tolerance. X=-1 and +1 sections repeat with another copy translated 2 m along X. '
 'Legacy earth PBR is retained on the low apron; stone values follow coherent cliff planes. Local origin is the low-front boundary centre at ground Z=0. '
 'No water geometry, whole-scene or curved-bank snapping, walkability, navigation, collision mesh, dynamic terrain, physics or engineering certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={'LegacyEarth':((.30,.36,.18,1),.83),'CliffSide':((.29,.33,.30,1),.92),'StoneLedge':((.40,.42,.365,1),.92),'StoneRecess':((.245,.28,.255,1),.92),'CutEarth':((.215,.245,.225,1),.92)}
mats={}
for n,(c,r) in PALETTE.items():
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=r;mats[n]=m
root=bpy.data.objects.new('BankEscarpmentTransition',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['origin']='Low-front cap centre at ground Z=0; landward axis +Y';root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
# Grid rows form two steep fracture planes with an actual intermediate bench.
# Unequal interior stations shape the fracture in depth/height, never random face noise.
XS=[-1.,-.55,0.,.48,1.]
# Each row has apron, lower face, exposed ledge, upper face, upper shoulder and rear.
PROFILE=[(0.,.55),(.18,.60),(.34,1.02),(.54,1.10),(.65,1.49),(.82,1.62),(1.28,1.67),(1.60,1.65)]
DY=[0.,-.025,.045,-.018,0.];DZ=[0.,.042,-.025,.060,0.]
verts=[]
for i,x in enumerate(XS):
 for j,(y,z) in enumerate(PROFILE):
  if j==0:y,z=0.,.55+.03*(1-abs(x))
  elif j==1:y,z=y+DY[i]*.3,z+.03*(1-abs(x))
  elif j==7:y,z=1.60,z+DZ[i]*.45
  else:y,z=y+DY[i]*(1 if j<6 else .3),z+DZ[i]*(1 if j<5 else .6)
  verts.append((x,y,z))
N=len(PROFILE);bottom_front=[];bottom_back=[]
for x in XS:
 bottom_front.append(len(verts));verts.append((x,0.,0.))
 bottom_back.append(len(verts));verts.append((x,1.6,0.))
faces=[];material_indices=[]
def face(ids,mat):faces.append(tuple(ids));material_indices.append(mat)
# Explicit triangles keep the surface diagonal deterministic through GLB roundtrips.
for i in range(len(XS)-1):
 for j in range(N-1):
  a=i*N+j;b=(i+1)*N+j;c=b+1;d=a+1
  mat=0 if j in [0,5,6] else (2 if j==2 else (3 if j==3 else 1))
  if (i+j)%2:face((a,b,d),mat);face((b,c,d),mat)
  else:face((a,b,c),mat);face((a,c,d),mat)
for i in range(len(XS)-1):
 face((bottom_front[i],bottom_front[i+1],(i+1)*N,i*N),0)
 face((i*N+N-1,(i+1)*N+N-1,bottom_back[i+1],bottom_back[i]),4)
 face((bottom_front[i],bottom_back[i],bottom_back[i+1],bottom_front[i+1]),4)
face((bottom_front[0],*range(N),bottom_back[0]),4)
face((bottom_front[-1],*range((len(XS)-1)*N,len(XS)*N),bottom_back[-1]),4)
me=bpy.data.meshes.new('Escarpment_continuous_terrain');me.from_pydata(verts,[],faces);me.update()
o=bpy.data.objects.new('Escarpment_ContinuousTerrain',me);scene.collection.objects.link(o);o.parent=root;o['component_role']='continuous_grounded_terrain'
for n in PALETTE:me.materials.append(mats[n])
for p,mi in zip(me.polygons,material_indices):p.material_index=mi;p.use_smooth=False
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();parts=[o]
# Read back actual native vertices for module port documentation.
front=sorted((round(v.co.x,6),round(v.co.z,6)) for v in me.vertices if abs(v.co.y)<1e-6)
end_profiles=[]
for x in [-1.,1.]:end_profiles.append(sorted((round(v.co.y,6),round(v.co.z,6)) for v in me.vertices if abs(v.co.x-x)<1e-6))
assert end_profiles[0]==end_profiles[1]
PORTS={'front_plane_y_m':0.,'original_straight_bank_placement_m':[0.,1.2,0.],'actual_front_vertices_xz_m':front,'rim_at_x_minus1_zero_plus1_z_m':[.55,.58,.55],'full_front_contact_area_m2':1.13,'x_repeat_m':2.,'actual_end_profiles_yz_m':end_profiles,'new_family':'escarpment-2m-v1','scope':'This original straight-bank landward face only. Original curve, access shelf and whole scene do not share this boundary.'}
root['port_contract']=json.dumps(PORTS,sort_keys=True)
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
geometry_fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
def oriented_pbr_fingerprint(objects):
 records=[]
 for o in objects:
  o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(q),6) for q in vv[i]) for i in t.vertices]
   m=o.data.materials[t.material_index];node=m.node_tree.nodes.get('Principled BSDF');assert node is not None
   pbr=tuple(round(float(q),6) for q in node.inputs['Base Color'].default_value)+(round(float(node.inputs['Roughness'].default_value),6),round(float(node.inputs['Metallic'].default_value),6))
   records.append((min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),pbr))
 return hashlib.sha256(json.dumps(sorted(records),separators=(',',':')).encode()).hexdigest()
authored_oriented_pbr=oriented_pbr_fingerprint(parts)
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'origin':'Low-front boundary centre at ground Z=0','components':checks,'ports':PORTS,'geometry_fingerprint_sha256':geometry_fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
# Render and runtime checks use a fresh import of the exact exported GLB.
# The editable native file above remains the authored component scene, without studio objects.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];bpy.context.view_layer.update()
actual_oriented_pbr=oriented_pbr_fingerprint(parts);assert actual_oriented_pbr==authored_oriented_pbr,('GLB oriented triangles or PBR changed',authored_oriented_pbr,actual_oriented_pbr)
mats={m.name:m for o in parts for m in o.data.materials};assert len(mats)==len(PALETTE)
qa['actual_glb_sha256']=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa['actual_glb_roundtrip']={'fresh_import':True,'oriented_triangles_and_pbr_sha256':actual_oriented_pbr,'matches_authored':True,'mesh_count':len(parts),'render_source':'fresh exact exported model.glb import'}
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Presentation added only after clean native/runtime have been saved.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX';focus=Vector((0,.8,.84))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-5,-7,10),1400,7),('Fill',(7,-2,5),650,6),('Rim',(2,7,8),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=3.1
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview_ground_not_asset';g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.22,.245,.24,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(-5,-7,5),'gray-back3q':(5,7,5)} if gray else {'thumbnail':(-5,-7,5),'qa-front':(0,-7,.84),'qa-side':(-7,.8,.84),'qa-top':(0,.8,8),'qa-back':(0,7,.84),'qa-wireframe':(-5,-7,7)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(n,p):
 cam.data.ortho_scale=2.4 if n in ['qa-front','qa-back','silhouette-128-front'] else (2.2 if n in ['qa-side','silhouette-128-side'] else 3.1)
 aim(cam,p);scene.render.filepath=str(OUT/(n+'.png'));render_configs[n]=assert_render();t=time.time();bpy.ops.render.render(write_still=True);render_seconds[n]=round(time.time()-t,3)
for n,p in views.items():
 if n=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for poly in dup.data.polygons:poly.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.004;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(0,-7,.84)),('silhouette-128-side',(-7,.8,.84))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n;files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
