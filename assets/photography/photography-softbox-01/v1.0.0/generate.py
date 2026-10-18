"""Original deep rectangular photography softbox, fixed static visual prop.
Metres, native Z up, front is -Y, ground origin (0,0,0); mast axis is Y=.19 m.
No external files, textures or fonts. No illumination power, optical simulation,
electrical equipment, operation, animation, load/stability or safety claims.
Stages --geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
All views freshly import the exact exported GLB; Cycles128 FIXED4, no denoise.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-softbox-01';VERSION='1.0.0';TITLE='Deep Rectangular Photography Softbox'
DESCRIPTION=('Original static photography softbox with a genuinely deep tapered hollow rectangular hood, '
 'closed inset front diffusion panel, rear lamp-head housing and a fixed U-shaped mounting yoke. '
 'The head has a real continuous support path through its pivot, yoke, mast, hub and three grounded feet. '
 'Five restrained solid PBR materials and separately named closed editable components; no external source dependencies. '
 'Metres, source Z up, front -Y, ground origin (0,0,0), mast axis Y=.19 m. Distinct from the existing thin octagonal reflector. '
 'One reusable static prop only; no emitted light, optical or electrical simulation, physical light power, '
 'animated tilt or folding, engineering, load-bearing, balance, stability or safety certification.')
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
for name,color,rough,metal in [('Graphite_HoodFabric',(.105,.12,.13,1),.86,0),
 ('Ivory_FrontDiffuser',(.80,.76,.65,1),.88,0),('RestrainedSteel_Stand',(.20,.24,.25,1),.55,.50),
 ('MutedTeal_LampHousing',(.12,.30,.28,1),.67,.18),('Ochre_FixedLocks',(.55,.32,.10,1),.65,.08)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('PhotographyDeepSoftbox',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_axis']='-Y';root['static_visual_only']=True
root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Restrained manufactured chamfer','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def rod(name,a,b,r,material,role,n=12):
 a=Vector(a);b=Vector(b);d=(b-a).normalized();ref=Vector((0,1,0)) if abs(d.y)<.9 else Vector((1,0,0))
 u=d.cross(ref).normalized();v=d.cross(u).normalized()
 vs=[p+r*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,(a+b)/2)
def outline(w,h,c):return [(-w+c,-h),(w-c,-h),(w,-h+c),(w,h-c),(w-c,h),(-w+c,h),(-w,h-c),(-w,-h+c)]
def slab(name,front,back,w,h,c,material,role,zc=1.65):
 q=outline(w,h,c);vs=[(x,y,zc+z) for y in [front,back] for x,z in q];n=len(q)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,(0,(front+back)/2,zc))
def hood_ring(name,loops,material,role):
 vs=[(x,y,1.65+z) for y,w,h,c in loops for x,z in outline(w,h,c)];n=8
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,material,role,(0,0,1.65))
# One continuous watertight thick hood wall, with a large real central cavity.
hood_ring('Softbox_DeepHood',[(-.42,.52,.40,.085),(.065,.16,.145,.040),(.065,.125,.110,.028),(-.42,.49,.37,.070)],0,
 'closed tapered hollow shell, actual .485 m front-to-rear depth; not a flat reflector')
slab('Softbox_FrontDiffuser',-.425,-.409,.505,.385,.077,1,
 'closed thick ivory diffusion panel attached with finite overlap into the hood front lip; no emission')
hood_ring('Softbox_RearCollar',[(.04,.182,.167,.043),(.12,.182,.167,.043),(.12,.125,.110,.028),(.04,.125,.110,.028)],2,
 'solid annular collar joining the deep hood to the lamp housing')
slab('LampHead_Housing',.035,.35,.147,.132,.025,3,'closed rear lamp housing carried by actual transverse pivot')
box('LampHead_RearControlPanel',(0,.352,1.65),(.18,.030,.11),0,'fixed rear controls panel embedded into lamp head',bevel=.007)
for x,label in [(-.047,'Left'),(.047,'Right')]:
 rod('LampHead_FixedControl_'+label,(x,.36,1.65),(x,.391,1.65),.021,4,'small fixed dial supported by rear panel',n=12)
# U-shaped yoke: side arms and bottom bridge physically meet; axle crosses head.
box('Yoke_BottomBridge',(0,.19,1.41),(.40,.13,.08),2,'solid bottom U-yoke bridge supported by mast',bevel=.008)
for sign,label in [(-1,'Left'),(1,'Right')]:
 box('Yoke_Arm_'+label,(sign*.173,.19,1.533),(.055,.105,.276),2,'upright U-yoke arm with bridge and pivot overlap',bevel=.006)
rod('Yoke_TransversePivot',(-.25,.19,1.65),(.25,.19,1.65),.036,2,'fixed through-head pivot joining both yoke arms',n=16)
for sign,label in [(-1,'Left'),(1,'Right')]:
 rod('Yoke_FixedTiltLock_'+label,(sign*.217,.19,1.65),(sign*.270,.19,1.65),.061,4,'fixed tilt-lock knob with actual axle overlap',n=10)
# Continuous grounded tripod support. No collapsible mechanism or dynamic pose.
rod('Stand_Mast',(0,.19,.145),(0,.19,1.439),.033,2,'continuous fixed mast from tripod hub to yoke bridge',n=16)
rod('Stand_HeightCollar',(0,.19,.91),(0,.19,.98),.052,3,'fixed mast collar; visual height hardware',n=16)
rod('Stand_FixedHeightLock',(.033,.19,.945),(.09,.19,.945),.022,4,'fixed mast-collar lock',n=10)
rod('Stand_TripodHub',(0,.19,.205),(0,.19,.43),.069,3,'solid tripod hub overlapped by mast and three legs',n=16)
feet=[]
for deg,label in [(90,'Rear'),(210,'LeftFront'),(330,'RightFront')]:
 a=math.radians(deg);end=Vector((.50*math.cos(a),.19+.50*math.sin(a),.045));start=Vector((0,.19,.355))
 rod('Stand_Leg_'+label,start,end,.027,2,'fixed splayed support leg meeting hub and foot',n=8)
 box('Stand_Foot_'+label,tuple(end+Vector((0,0,-.015))),(.115,.115,.060),0,'flat grounded rubber-like foot; bottom Z=0',bevel=.008)
 feet.append((label,start,end))
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 votes=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  votes.append(bool(hits%2))
 return all(votes)
joints=[]
def joint(a,b,points):
 rows=[]
 for p in points:
  p=list(p);clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
joint('Softbox_DeepHood','Softbox_FrontDiffuser',[(.497,-.413,1.65+z) for z in [-.12,0,.12]])
joint('Softbox_DeepHood','Softbox_RearCollar',[(.15,.055,1.65+z) for z in [-.045,0,.045]])
joint('Softbox_RearCollar','LampHead_Housing',[(.136,.085,1.65+z) for z in [-.04,0,.04]])
joint('LampHead_Housing','LampHead_RearControlPanel',[(x,.343,1.65) for x in [-.05,0,.05]])
for x,label in [(-.047,'Left'),(.047,'Right')]:
 joint('LampHead_RearControlPanel','LampHead_FixedControl_'+label,[(x+dx,.363,1.65+dz) for dx,dz in [(-.005,0),(.005,0),(0,.006)]])
joint('LampHead_Housing','Yoke_TransversePivot',[(x,.19,1.65) for x in [-.10,0,.10]])
for sign,label in [(-1,'Left'),(1,'Right')]:
 joint('Yoke_TransversePivot','Yoke_Arm_'+label,[(sign*.173,.19+dy,1.65+dz) for dy,dz in [(-.012,0),(.012,0),(0,-.01)]])
 joint('Yoke_Arm_'+label,'Yoke_BottomBridge',[(sign*.173,.19+dy,1.425+dz) for dy,dz in [(-.014,0),(.014,0),(0,.008)]])
 joint('Yoke_TransversePivot','Yoke_FixedTiltLock_'+label,[(sign*.235,.19+dy,1.65+dz) for dy,dz in [(-.01,0),(.01,0),(0,.01)]])
joint('Yoke_BottomBridge','Stand_Mast',[(x,.19+dy,1.414) for x,dy in [(-.01,0),(.01,0),(0,.01)]])
joint('Stand_Mast','Stand_HeightCollar',[(x,.19+dy,.945) for x,dy in [(-.01,0),(.01,0),(0,.01)]])
joint('Stand_HeightCollar','Stand_FixedHeightLock',[(.043,.19+dy,.945+dz) for dy,dz in [(-.004,0),(.004,0),(0,.005)]])
joint('Stand_Mast','Stand_TripodHub',[(x,.19+dy,.30) for x,dy in [(-.01,0),(.01,0),(0,.01)]])
for label,start,end in feet:
 d=(end-start).normalized()
 joint('Stand_TripodHub','Stand_Leg_'+label,[start+d*s for s in [.014,.027,.040]])
 joint('Stand_Leg_'+label,'Stand_Foot_'+label,[end-d*s for s in [.002,.007,.012]])
# Connectivity includes every component, grounded through a real finite-area foot patch.
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={'Stand_TripodHub'};pending=list(seen)
while pending:
 for name in adj[pending.pop()]-seen:seen.add(name);pending.append(name)
assert seen==set(adj),'Unsupported components: '+repr(set(adj)-seen)
supports=[]
for label,_,_ in feet:
 o=byname['Stand_Foot_'+label];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.008,area;supports.append({'name':o.name,'area_m2':area,'triangles':patch})
# Real empty cavity probes and visible silhouette depth; separate from diffuser thickness.
hood=byname['Softbox_DeepHood'];hv=[hood.matrix_world@v.co for v in hood.data.vertices]
hood_depth=max(v.y for v in hv)-min(v.y for v in hv);assert abs(hood_depth-.485)<1e-6
cavity=[(0,y,1.65) for y in [-.36,-.20,-.04]]
assert all(not inside(trees['Softbox_DeepHood'],p) for p in cavity),'Hood cavity is filled'
diffuser=byname['Softbox_FrontDiffuser'];dv=[diffuser.matrix_world@v.co for v in diffuser.data.vertices]
assert abs(max(v.y for v in dv)-min(v.y for v in dv)-.016)<1e-6
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'Solid-only PBR expected'
 assert not any(i.is_linked for i in p.inputs),'Linked Principled inputs are not solid PBR'
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
 'components':component_checks,'connection_interior_points':joints,'finite_ground_supports':supports,'all_components_support_connected':True,'hood_depth_m':hood_depth,'hood_cavity_empty_points_m':cavity,'diffuser_thickness_m':.016,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/photography/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.06,1.04));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.45;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3.0,-5.5,2.8),'gray-back3q':(-3.0,5.5,2.8)} if gray else {
 'thumbnail':(4.8,-4.8,2.8),'qa-front':(0,-6,1.04),'qa-side':(6,.06,1.04),'qa-top':(0,.06,7),
 'qa-back':(0,6,1.04),'qa-wireframe':(4.8,-4.8,2.8)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0009;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-6,1.04)),('silhouette-128-side',(6,.06,1.04))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
