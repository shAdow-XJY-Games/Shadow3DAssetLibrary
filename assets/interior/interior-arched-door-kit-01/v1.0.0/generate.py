"""Original S01 interior arched frame/leaf kit. No external assets or dependencies.
Blender: blender -b -t 4 --python-exit-code 1 --python generate.py [-- --geometry-only | --gray-only]
Coordinates are metres, Z up. Kit origin is the threshold top / jamb-foot centre.
Install at pinned dining arch-wall origin + (0,0,.05). Finite poses 0/-45/-90 only.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
START=time.time(); OUT=Path(__file__).resolve().parent
ASSET='interior-arched-door-kit-01'; VERSION='1.0.0'
TITLE='Seafoam Arched Interior Door Kit'
DESCRIPTION=('Original S01 independent frame and true arched leaf for the unchanged 1.4 m dining architecture family. '
 'Place kit jamb-foot origin at dining-archway-wall-01 origin +(0,0,0.05)m, or Z=0.095m above the bottom of dining-plank-floor-01. '
 'Frame outer/inner arch radii 0.412/0.386m, 0.232m deep, spring centre Z=1.60m; leaf radius0.372m, thickness0.036m, bottom clearance0.014m. '
 'DoorPivot (-0.380,-0.130,0)m is independently editable, opening towards -Y. Only discrete 0,-45,-90 degree Z poses are tested. '
 'No animation or continuous sweep claim. Keep old wall, maple reveals and threshold intact. Static central mounting shims deliberately engage the wall. '
 'One useful kit with editable frame, leaf, hinge and handle components; solid PBR materials, no textures. Functional origin is not the bounds centre.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[vl.cycles.use_denoising for vl in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
PALETTE={'maple':((.48,.255,.105,1),.72,0),'seafoam':((.19,.40,.35,1),.66,0),
 'cream':((.86,.75,.52,1),.74,0),'warm_metal':((.19,.15,.085,1),.35,.7)}
mats={}
for n,(c,r,m) in PALETTE.items():
 a=bpy.data.materials.new(n);a.diffuse_color=c;a.use_nodes=True
 p=a.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=m;mats[n]=a
parts=[];moving=[];static=[]
root=bpy.data.objects.new('InteriorDoorKit',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['placement_wall_offset_z_m']=.05;root['tested_degrees']='0,-45,-90'
root['native_render_contract']=json.dumps(render_config(),sort_keys=True)
pivot=bpy.data.objects.new('DoorPivot',None);scene.collection.objects.link(pivot);pivot.location=(-.380,-.130,0);pivot.parent=root
pivot.empty_display_type='PLAIN_AXES';pivot.empty_display_size=.13;pivot['finite_pose_degrees']='0,-45,-90';pivot['axis']='local Z';pivot['continuous_sweep_validated']=False
def register(o,mat,move=False):
 o.data.materials.append(mats[mat]);o['role']='leaf' if move else 'frame';parts.append(o);(moving if move else static).append(o);return o
def normals(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
def mesh(n,v,f,mat,move=False,bevel=0):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);scene.collection.objects.link(o);register(o,mat,move);normals(o)
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Small geometric edge','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 return o
def box(n,lo,hi,mat,move=False,bevel=.002):
 v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh(n,v,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],mat,move,bevel)
def outline(n,p,y0,y1,mat,move=False,bevel=0):
 N=len(p);q=[Vector((x,0,z)) for x,z in p];v=[(x,y,z) for y in [y0,y1] for x,z in p];f=[]
 for t in tessellate_polygon([q]):
  ids=tuple(i if isinstance(i,int) else min(range(N),key=lambda j:(q[j]-i).length_squared) for i in t);f += [ids,tuple(N+i for i in reversed(ids))]
 f += [(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 return mesh(n,v,f,mat,move,bevel)
def arched(r,bottom,cz=1.60):
 return [(-r,bottom),(-r,cz)]+[(r*math.cos(math.pi-i*math.pi/12),cz+r*math.sin(math.pi-i*math.pi/12)) for i in range(1,13)]+[(r,bottom)]
outer=arched(.412,0);inner=arched(.386,0)
outline('Frame_arched_liner',outer+list(reversed(inner)),-.116,.116,'maple')
for side in [-1,1]:
 for i,z in enumerate([.33,1.15]):
  x=sorted([side*.407,side*.454]);o=box('Frame_mount_shim_%s_%d'%('L' if side<0 else 'R',i+1),(x[0],-.034,z-.045),(x[1],.034,z+.045),'cream',False,.001);o['intentional_connection']='frame to frozen wall, central-depth bridge'
outline('Leaf_arched_solid',arched(.372,.014),-.130,-.094,'seafoam',True,.002)
outline('Leaf_upper_inset_front',arched(.295,.95),-.134,-.126,'cream',True,.002)
outline('Leaf_upper_inset_rear',arched(.295,.95),-.098,-.090,'cream',True,.002)
for face,y0,y1 in [('front',-.134,-.126),('rear',-.098,-.090)]:
 box('Leaf_lower_inset_'+face,(-.295,y0,.20),(.295,y1,.80),'cream',True,.003)
def cylinder(n,xyz,r,depth,mat,move=False,axis='Z',sides=12):
 bpy.ops.mesh.primitive_cylinder_add(vertices=sides,radius=r,depth=depth,end_fill_type='NGON',location=xyz)
 o=bpy.context.object;o.name=n
 if axis=='Y':o.rotation_euler.x=math.pi/2
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);return register(o,mat,move)
for i,z in enumerate([.38,1.32]):
 cylinder('Hinge_static_barrel_%d'%i,(-.380,-.130,z),.011,.090,'warm_metal')
 box('Hinge_static_socket_%d'%i,(-.414,-.136,z-.029),(-.377,-.097,z+.029),'warm_metal',False,.001)
 box('Hinge_leaf_plate_%d'%i,(-.374,-.135,z-.025),(-.337,-.123,z+.025),'warm_metal',True,.001)
for side,y0,y1 in [('front',-.164,-.127),('rear',-.097,-.060)]:
 cylinder('Handle_spindle_'+side,(.268,(y0+y1)/2,.90),.012,y1-y0,'warm_metal',True,'Y')
 end=y0 if side=='front' else y1
 box('Handle_lever_'+side,(.235,end-.005,.886),(.333,end+.010,.914),'warm_metal',True,.004)
# Keep all mesh origins identity relative to their functional parent; preserve true pivot.
bpy.context.view_layer.update()
for o in parts:
 if o in moving:
  for v in o.data.vertices:v.co-=pivot.location
  o.parent=pivot
 else:o.parent=root
 o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1)
 normals(o)
bpy.context.view_layer.update()
bad=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free();o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
assert not bad,bad
def coordinates():return [o.matrix_world@v.co for o in parts for v in o.data.vertices]
v=coordinates();lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert min(p.z for p in v)>=-1e-7
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root,pivot]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'functional_origin':'jamb-foot centre / threshold top, not bounding-box centre','pivot_m':list(pivot.location),'axis':'local Z',
 'allowed_discrete_degrees':[0,-45,-90],'continuous_sweep_validated':False,'nonmanifold_or_nonpositive_components':bad,
 'geometry_fingerprint_sha256':hashlib.sha256(json.dumps([(o.name,[list(o.matrix_world@v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest(),
 'source_compatibility_pin':'c4b39f3dbba04f299cf5da284a81253ed33a19b6','native_saved_render_config':render_config(),'status':'producer geometry only; independent interface/pose/visual/runtime gates required'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
if '--geometry-only' in sys.argv:print('GEOMETRY_READY',json.dumps(qa));sys.exit(0)
# Presentation geometry is intentionally added only after native source is saved.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.color=(.35,.35,.35);scene.view_settings.view_transform='AgX'
focus=Vector((0,-.03,1.0))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-3,-4,6),500,4),('Fill',(4,-1,3),220,3),('Rim',(1,4,5),340,3)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=2.65
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1);m.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=0
views={'gray-early':(3,-5,3)} if gray else {'thumbnail':(3,-5,3),'qa-front':(0,-5,1.0),'qa-side':(5,-.03,1),'qa-top':(0,-.03,6),'qa-back':(-3,5,3),'qa-wireframe':(3,-5,3)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
for n,p in views.items():
 if n=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.01,.02,.025,1)
  for o in parts:
   o.data.materials.append(wm);w=o.modifiers.new('Preview_wire','WIREFRAME');w.thickness=.0012;w.use_replace=False;w.offset=1;w.material_offset=len(o.data.materials)-1
 aim(cam,p);scene.render.filepath=str(OUT/(n+'.png'));render_configs[n]=render_config();t=time.time();bpy.ops.render.render(write_still=True);render_seconds[n]=round(time.time()-t,3)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent gates pending'})
if not gray:
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n;files[role]={'path':f'assets/interior/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'interior','style':'soft-low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
