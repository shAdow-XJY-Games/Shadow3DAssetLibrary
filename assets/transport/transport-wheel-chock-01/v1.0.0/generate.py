"""Original single S01/S06 static wheel chock, metres, source Z up.
One ochre closed wedge with a true X-through gripping aperture, one dark treaded sole.
Origin is X=Y=Z=0 on the bearing plane and centred across width;
sole limits X +/-0.116, Y -0.170..+0.160. Axis +Y rises toward the rear grip.
Standalone generator: no external inputs. --no-render / --geometry-only / --gray-only /
--preview-only / --extra-views. All images render a fresh exact exported GLB.
No brake, friction, load, carrying ergonomics or vehicle-fit certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='transport-wheel-chock-01';VERSION='1.0.0';TITLE='Ochre Single Wedge Wheel Chock'
DESCRIPTION=('Original S01/S06 static single wheel-chock prop: an ochre rising wedge has a real transverse X-through '
 'gripping aperture in its thick rear section; a separate dark continuous sole has seven shallow underside channels '
 'and eight finite flat bearing strips. Two named editable closed meshes, solid PBR materials, metre scale and '
 'source Z-up. Origin X=Y=Z=0 lies on the ground, centred across width; sole Y extents -0.170 to +0.160 m. '
 'Low tip faces -Y, rising wedge and grip face +Y. One reusable model; repeated placements do not add models. '
 'Existing delivery-van wheel dimensions are a separate fixed-size visual comparison only. No vehicle-fit, '
 'braking, anti-roll, friction, load, carrying ergonomics, physics or safety certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough in [('Warm_Ochre_MouldedBody',(.67,.365,.060,1),.72),('Charcoal_TreadedSole',(.045,.052,.055,1),.87)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0
 mats.append(m)
root=bpy.data.objects.new('WheelChock',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_low_tip_axis']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[]
def mesh(name,vs,fs,material,role):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o.parent=root;o['component_role']=role;parts.append(o)
 for f in me.polygons:f.use_smooth=False
 return o
# Closed extruded ring: both side walls, the wedge outer wall and the true aperture wall.
# The clear octagonal hole is 86 mm long by 76 mm high before its 2 mm edge chamfer.
outer=[(-.160,.018),(.010,.188),(.020,.194),(.140,.194),(.150,.184),(.150,.020),(.140,.010),(-.152,.010)]
inner=[(.040,.083),(.040,.135),(.052,.147),(.114,.147),(.126,.135),(.126,.083),(.114,.071),(.052,.071)]
vs=[(x,y,z) for x in [-.110,.110] for loop in [outer,inner] for y,z in loop];fs=[]
for i in range(8):
 j=(i+1)%8
 fs.extend([(i,j,j+8,i+8),(i+16,i+24,j+24,j+16),(i,i+16,j+16,j),(i+8,j+8,j+24,i+24)])
body=mesh('Chock_Wedge_ThroughGrip',vs,fs,0,'closed rising wedge with true X-through grip aperture')
bpy.context.view_layer.objects.active=body;body.select_set(True)
b=body.modifiers.new('Small moulded edge chamfer','BEVEL');b.width=.002;b.segments=1;b.affect='EDGES';bpy.ops.object.modifier_apply(modifier=b.name)
# Continuous solid sole, with actual broad ground strips separated by shallow underside channels.
grooves=[(-.145+i*.045,-.133+i*.045) for i in range(7)]
profile=[(-.170,.014),(.160,.014),(.160,0)]
for a,z in reversed(grooves):profile.extend([(z,0),(z,.003),(a,.003),(a,0)])
profile.append((-.170,0));n=len(profile)
vs=[(x,y,z) for x in [-.116,.116] for y,z in profile]
fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
sole=mesh('Chock_Continuous_ChannelledSole',vs,fs,1,'closed dark sole with seven shallow channels and finite ground strips')
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
deps=bpy.context.evaluated_depsgraph_get();bt=BVHTree.FromObject(body,deps);st=BVHTree.FromObject(sole,deps)
aperture=[]
for y,z in [(.083,.109),(.050,.109),(.116,.109),(.083,.081),(.083,.137)]:
 assert bt.ray_cast(Vector((-.2,y,z)),Vector((1,0,0)),.4)[0] is None,(y,z)
 aperture.append([y,z])
def inside(t,p):
 p=Vector(p);d=Vector((.37,.59,.73)).normalized();hits=0
 for _ in range(32):
  q,_,_,_=t.ray_cast(p,d,2)
  if q is None:break
  hits+=1;p=q+d*1e-6
 return bool(hits%2)
join_points=[(-.06,-.08,.012),(.06,-.08,.012),(0,.10,.012)]
for p in join_points:assert inside(bt,p) and inside(st,p),p
support=[]
for t in sole.data.loop_triangles:
 v=[sole.matrix_world@sole.data.vertices[i].co for i in t.vertices]
 if max(abs(p.z) for p in v)<1e-7 and (v[1]-v[0]).cross(v[2]-v[0]).z<0:
  support.append({'vertices_m':[list(p) for p in v],'area_m2':(v[1]-v[0]).cross(v[2]-v[0]).length/2})
assert len(support)==16
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
# Every oriented triangle is bound to its complete supported solid PBR signature.
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes),'Solid-only PBR expected'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling))
 return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':len(parts),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':checks,'through_grip_clear_x_rays_yz_m':aperture,'body_sole_join_interior_points_m':join_points,
 'actual_ground_triangles':support,'actual_ground_area_m2':sum(t['area_m2'] for t in support),'groove_count':7,'groove_depth_m':.003,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'transport','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# The exact saved GLB is imported into a clean empty scene for roundtrip and every rendered view.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==2 and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((0,-.005,.090));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-1.2,-1.5,2),90,1.4),('Fill',(1.3,-.2,1),44,1.0),('Rim',(.3,1.4,1.8),55,1.2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.46;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.8,-1,.65),'gray-back3q':(-.8,1,.65)} if gray else {
 'thumbnail':(.8,-1,.65),'qa-front':(0,-1,.09),'qa-side':(1,-.005,.09),'qa-top':(0,-.005,1),
 'qa-back':(0,1,.09),'qa-wireframe':(.8,-1,.65)}
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
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00045;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-1,.09)),('silhouette-128-side',(1,-.005,.09))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
