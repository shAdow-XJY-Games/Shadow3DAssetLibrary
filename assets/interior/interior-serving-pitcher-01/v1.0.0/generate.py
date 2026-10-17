"""Original S01 Open Serving Pitcher. Metres, Z-up; static visual prop.
Self-contained geometry; spout +X, handle -X, body-base centre origin at Z=0.
Flags: --geometry-only / --gray-only / --preview-only / --extra-views.
All images use a fresh import of the exact exported GLB. Cycles 128/no adaptive/no denoise/FIXED4.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='interior-serving-pitcher-01';VERSION='1.0.0';TITLE='Open Seafoam Serving Pitcher'
DESCRIPTION=('Original S01 table-scale serving pitcher with a generous faceted belly, narrowed neck, large open refill mouth '
 'and an elongated integrated pouring lip. One continuous closed thick shell includes the flat base, real inner floor, '
 'inner walls and visible ivory rim. One separate solid C-profile rear handle has a large real aperture and two roots '
 'inserted into the body wall. Two named editable meshes, solid PBR materials, metre scale and body-base-centre origin '
 'at Z=0; spout +X, handle -X. Static game visual only; no liquid, pouring animation, capacity, load, grip ergonomics '
 'or food-contact certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c==EXPECTED,c;return c
PALETTE={'Seafoam_Ceramic':(.19,.40,.35,1),'Ivory_Ceramic':(.86,.78,.60,1)};mats={}
for name,color in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.53;mats[name]=m
root=bpy.data.objects.new('ServingPitcher',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['spout_axis']='+X';root['ground_z_m']=0.;root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def mesh(name,verts,faces,role):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for material in mats.values():me.materials.append(material)
 for f in me.polygons:f.use_smooth=False
 o.parent=root;o['component_role']=role;parts.append(o);return o
# Rings run continuously from the outer ground rim up over the lip, down inside to the real floor.
# Identical lip displacement on inner and outer rim makes an open pouring channel, not a blind spout.
N=32
PROFILE=[(.059,0,0),(.065,.006,0),(.079,.032,0),(.089,.085,0),(.087,.145,0),
 (.077,.205,.12),(.079,.236,.80),(.081,.245,1),(.075,.2445,1),(.073,.235,.80),
 (.071,.205,.12),(.081,.145,0),(.083,.085,0),(.073,.034,0),(.057,.014,0)]
verts=[]
for radius,z,lip in PROFILE:
 for k in range(N):
  a=2*math.pi*k/N;strength=max(0.,math.cos(a))**10
  # Forward centre of the lip projects 47 mm, shoulder arcs retain a wide open throat.
  verts.append((radius*math.cos(a)+.047*lip*strength,radius*math.sin(a),z-.008*lip*strength))
faces=[tuple(range(N-1,-1,-1))]
for ring in range(len(PROFILE)-1):
 for k in range(N):j=(k+1)%N;faces.append((ring*N+k,ring*N+j,(ring+1)*N+j,(ring+1)*N+k))
faces.append(tuple(range((len(PROFILE)-1)*N,len(PROFILE)*N)))
body=mesh('Pitcher_ThickBody_IntegratedLip',verts,faces,'continuous_thick_open_vessel')
for i,f in enumerate(body.data.polygons):
 # Outer body through shoulder is seafoam; top bevel/rim and actual inner surface are ivory.
 f.material_index=1 if i>=1+6*N else 0
# Two original cubic arcs make a broad C-profile loop, with solid roots entering the body wall.
def bezier(points,t):
 return points[0]*(1-t)**3+points[1]*(3*t*(1-t)**2)+points[2]*(3*t*t*(1-t))+points[3]*t**3
upper=[Vector((x,0,z)) for x,z in [(-.075,.199),(-.116,.199),(-.157,.201),(-.157,.158)]]
lower=[Vector((x,0,z)) for x,z in [(-.157,.158),(-.160,.111),(-.129,.074),(-.084,.074)]]
centres=[bezier(upper,i/12) for i in range(13)]+[bezier(lower,i/12) for i in range(1,13)]
sides=8;hv=[]
for i,c in enumerate(centres):
 tangent=(centres[min(i+1,len(centres)-1)]-centres[max(0,i-1)]).normalized()
 normal=Vector((-tangent.z,0,tangent.x));lateral=Vector((0,1,0))
 for j in range(sides):a=2*math.pi*j/sides;hv.append(tuple(c+normal*(.011*math.cos(a))+lateral*(.010*math.sin(a))))
hf=[tuple(range(sides-1,-1,-1)),tuple(range((len(centres)-1)*sides,len(centres)*sides))]
for i in range(len(centres)-1):
 for j in range(sides):k=(j+1)%sides;hf.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
handle=mesh('Pitcher_OpenGripHandle',hv,hf,'solid_c_profile_grip')
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();degenerate=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and volume>1e-9 and degenerate==0,(o.name,bad,volume,degenerate)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':volume,'nonmanifold_edges':bad,'degenerate_triangles':degenerate})
deps=bpy.context.evaluated_depsgraph_get();body_bvh=BVHTree.FromObject(body,deps);handle_bvh=BVHTree.FromObject(handle,deps)
def inside(bvh,point):
 p=Vector(point);direction=Vector((.381,.729,.568)).normalized();hits=[]
 for _ in range(30):
  loc,normal,index,distance=bvh.ray_cast(p,direction,2)
  if loc is None:break
  hits.append(tuple(loc));p=loc+direction*1e-6
 return bool(len(hits)%2),len(hits)
root_tests=[]
for name,c in [('upper',centres[0]),('lower',centres[-1])]:
 ok,hits=inside(body_bvh,c);assert ok,(name,tuple(c),hits)
 root_tests.append({'root':name,'point_m':list(c),'inside_actual_shell':ok,'parity_hits':hits})
root_cap_tests=[]
for name,points in [('upper',hv[:sides]),('lower',hv[-sides:])]:
 flags=[inside(body_bvh,p)[0] for p in points];assert all(flags),(name,flags)
 root_cap_tests.append({'root':name,'cap_vertices':len(points),'all_inside_actual_shell':all(flags)})
assert not inside(body_bvh,(0,0,.12))[0]
floor_hit=body_bvh.ray_cast(Vector((0,0,.30)),Vector((0,0,-1)),1)
assert floor_hit[0] is not None and abs(floor_hit[0].z-.014)<1e-6
radial_hits=[]
for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]:
 hit=body_bvh.ray_cast(Vector((0,0,.145)),Vector(d),1);assert hit[0] is not None and abs(hit[3]-.081)<1e-6
 radial_hits.append({'direction':d,'distance_m':hit[3]})
# A real aperture through Y: rays traverse the visible grip opening without touching either part.
aperture=[]
for x,z in [(-.120,.145),(-.120,.175),(-.120,.110)]:
 for bvh in [body_bvh,handle_bvh]:assert bvh.ray_cast(Vector((x,-.10,z)),Vector((0,1,0)),.20)[0] is None,(x,z)
 aperture.append([x,z])
# The pouring throat remains open from above well ahead of the ordinary circular mouth.
channel_hit=body_bvh.ray_cast(Vector((.106,0,.30)),Vector((0,0,-1)),1)
assert channel_hit[0] is not None and channel_hit[0].z<.231,channel_hit
allv=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
lo=[min(v[i] for v in allv) for i in range(3)];hi=[max(v[i] for v in allv) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7
base_area=.5*N*.059**2*math.sin(2*math.pi/N)
geometry_fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(f.vertices) for f in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':len(parts),'bounds_m':bounds,
 'bounds_min_m':lo,'bounds_max_m':hi,'origin':'body base centre, Z=0; not asymmetric bounds centre','components':checks,
 'handle_root_checks':root_tests,'handle_root_cap_checks':root_cap_tests,'cavity_floor_z_m':floor_hit[0].z,'cavity_radial_rays':radial_hits,
 'grip_aperture_clear_through_y_samples_xz_m':aperture,'pour_channel_vertical_hit_z_m':channel_hit[0].z,
 'ground_contact_polygon':{'vertices':N,'radius_m':.059,'area_m2':base_area,'z_m':0},
 'structure_scope':'Geometry and static empty spaces only; no liquid, capacity, grip ergonomics or performance claim.',
 'geometry_fingerprint_sha256':geometry_fingerprint,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def write_metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/interior/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric',
  'title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,
  'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 write_metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Render only the freshly imported exported GLB; native source remains clean.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
parts=[o for o in scene.objects if o.type=='MESH'];asset_mats={m for o in parts for m in o.data.materials};assert len(parts)==2
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX';focus=Vector((-.018,0,.122))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,energy,size in [('Key',(-1.1,-1.4,2.0),85,1.4),('Fill',(1.2,-.3,.8),32,1.0),('Rim',(.6,1.2,1.5),50,1.2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.37;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.54,-1,.66),'gray-back3q':(-.54,1,.66)} if gray else {
 'thumbnail':(.54,-1,.66),'qa-front':(-.018,-1,.122),'qa-side':(1,0,.122),'qa-top':(-.018,0,1),
 'qa-back':(-.018,1,.122),'qa-wireframe':(.54,-1,.66)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));render_configs[name]=assert_render();t=time.time()
 bpy.ops.render.render(write_still=True);render_seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for poly in dup.data.polygons:poly.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00040;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(-.018,-1,.122)),('silhouette-128-side',(1,0,.122))]:render(name,pos)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:write_metadata()
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
