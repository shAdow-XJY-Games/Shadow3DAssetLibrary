"""Original independent static football training goal, metres, source Z up.
Open front frame, grounded return rails and a real four-surface net pocket.
Every image renders a fresh import of the exact GLB. No external dependencies.
--geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
No animation, ball collision, flexible-net simulation, regulation or safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-training-football-goal-01';VERSION='1.0.0';TITLE='Open Pocket Training Football Goal'
DESCRIPTION=('Original static low-poly freestanding football training goal with two warm ivory front posts and a real open crossbar mouth. '
 'A muted teal return base, side shoulders, diagonal back stays and rear cross-members form a deep grounded frame. '
 'A sparse sand-coloured solid-rope net wraps the roof, sloped back and both trapezoidal sides, leaving the whole front open. '
 'Every rope has two physically joined support ends and every named component connects to four finite flat foot pads. '
 'The net openings and front-mouth clearance are real empty geometry. Approximate 3 m wide by 2 m high visual proportions, '
 'metres, source Z up, front faces -Y and ground-centre origin; four solid PBR materials, editable parts and no external dependencies. '
 'Distinct independent ground goal, not a scaled table-football pocket or a single flat divider net. Static game visual only; '
 'no regulation dimensions, net dynamics, playable ball collision, anchoring, tipping resistance, wind loading or safety certification.')
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
for name,color,rough,metal in [('IvoryPowdercoat_Front',(.83,.78,.62,1),.75,.10),
 ('MutedTeal_RearFrame',(.19,.40,.35,1),.79,.08),('SandFiber_Net',(.69,.58,.36,1),.92,0),
 ('DarkRubber_Feet',(.075,.12,.115,1),.96,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('OpenPocketTrainingGoal',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True
root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[];spines={};net_names=[]
def mesh(name,vs,fs,material,role,bevel=0):
 # Shared ground-centre origin and 1 micrometre lattice avoid export-transform drift.
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Soft cut edge','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
  for v in me.vertices:v.co=Vector(tuple(round(float(c),6) for c in v.co))
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.004):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,bevel)
def rod(name,a,b,radius,material,role,n=12):
 a,b=Vector(a),Vector(b);axis=(b-a).normalized();ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0));u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
 vs=[p+radius*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 spines[name]=(a,b);return mesh(name,vs,fs,material,role)
def end_link(name,target,end):
 a,b=spines[name];start=a if end==0 else b;direction=((b-a) if end==0 else (a-b)).normalized()
 links.append((name,target,[start+direction*d for d in [.006,.010,.014]]))
def rope(name,a,b,support_a,support_b):
 rod(name,a,b,.0075,2,'closed solid rope with two supported ends',8);net_names.append(name)
 end_link(name,support_a,0);end_link(name,support_b,1)
# Four independent flat foot pads. Front opening has no bottom crossbar.
W=1.50;FY=-.65;SY=-.15;RY=.70;Z0=.08;ZT=2.0
feet=[]
for x,side in [(-W,'Left'),(W,'Right')]:
 for y,end in [(FY,'Front'),(RY,'Rear')]:
  name='Foot_'+side+'_'+end;box(name,(x,y,.035),(.18,.22,.07),3,'finite flat grounded rubber pad',.005);feet.append(name)
 rod('FrontPost_'+side,(x,FY,.035),(x,FY,ZT+.025),.060,0,'vertical front goal post',16)
 end_link('FrontPost_'+side,'Foot_'+side+'_Front',0)
 rod('GroundReturn_'+side,(x,FY,Z0),(x,RY+.025,Z0),.036,1,'longitudinal grounded return rail',12)
 end_link('GroundReturn_'+side,'FrontPost_'+side,0)
 links.append(('GroundReturn_'+side,'Foot_'+side+'_Rear',[Vector((x,RY-d,.055)) for d in [.006,.010,.014]]))
 rod('RoofShoulder_'+side,(x,FY,ZT),(x,SY+.025,ZT),.036,1,'upper rearward net shoulder',12)
 end_link('RoofShoulder_'+side,'FrontPost_'+side,0)
 rod('RearStay_'+side,(x,SY,ZT),(x,RY,Z0),.036,1,'diagonal rear net frame stay',12)
 end_link('RearStay_'+side,'RoofShoulder_'+side,0);end_link('RearStay_'+side,'GroundReturn_'+side,1)
rod('FrontCrossbar',(-W,FY,ZT),(W,FY,ZT),.060,0,'open-front goal crossbar',16)
for end,side in [(0,'Left'),(1,'Right')]:end_link('FrontCrossbar','FrontPost_'+side,end)
rod('RearUpperCrossbar',(-W,SY,ZT),(W,SY,ZT),.032,1,'upper back net cross-member',12)
rod('RearGroundCrossbar',(-W,RY,Z0),(W,RY,Z0),.036,1,'rear ground net cross-member',12)
for end,side in [(0,'Left'),(1,'Right')]:
 end_link('RearUpperCrossbar','RoofShoulder_'+side,end);end_link('RearGroundCrossbar','GroundReturn_'+side,end)
# Back mesh: 15 columns x 10 rows, sloping away from the open front mouth.
# Roof mesh: 15 columns x 3 rows. Side nets: 4 columns x 10 rows.
for i in range(1,15):
 x=-W+2*W*i/15
 rope(f'Net_Back_V_{i:02d}',(x,SY,ZT),(x,RY,Z0),'RearUpperCrossbar','RearGroundCrossbar')
 rope(f'Net_Roof_V_{i:02d}',(x,FY,ZT),(x,SY,ZT),'FrontCrossbar','RearUpperCrossbar')
for j in range(1,10):
 t=j/10;y=RY+(SY-RY)*t;z=Z0+(ZT-Z0)*t
 rope(f'Net_Back_H_{j:02d}',(-W,y,z),(W,y,z),'RearStay_Left','RearStay_Right')
for j in range(1,3):
 y=FY+(SY-FY)*j/3
 rope(f'Net_Roof_H_{j:02d}',(-W,y,ZT),(W,y,ZT),'RoofShoulder_Left','RoofShoulder_Right')
for x,side in [(-W,'Left'),(W,'Right')]:
 for j in range(1,10):
  t=j/10;y=RY+(SY-RY)*t;z=Z0+(ZT-Z0)*t
  rope(f'Net_{side}_H_{j:02d}',(x,FY,z),(x,y,z),'FrontPost_'+side,'RearStay_'+side)
 for i in range(1,4):
  u=i/4
  rope(f'Net_{side}_V_{i:02d}',(x,FY+(RY-FY)*u,Z0),(x,FY+(SY-FY)*u,ZT),'GroundReturn_'+side,'RoofShoulder_'+side)
# Real source-mesh checks, never solely dimensions or declared roles.
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in links:
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3])
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(feet);todo=list(feet)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
assert all(sum(j['a']==n for j in joints)==2 for n in net_names)
supports=[]
for name in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.03;supports.append({'name':name,'area_m2':area,'triangles':patch})
# 275 finite local apertures across all four net surfaces, five rays each.
# Each 25 mm square is centred in a true grid cell; rays cross 80 mm of depth.
apertures=[]
def window(panel,centre,u,v):
 centre,u,v=Vector(centre),Vector(u).normalized(),Vector(v).normalized();normal=u.cross(v).normalized();rays=[]
 for du,dv in [(0,0),(-.0125,-.0125),(-.0125,.0125),(.0125,-.0125),(.0125,.0125)]:
  p=centre+u*du+v*dv;start=p-normal*.04;hits=[]
  for name,tree in trees.items():
   q,_,_,_=tree.ray_cast(start,normal,.08)
   if q is not None:hits.append(name)
  assert not hits,('Net aperture obstruction',panel,list(p),hits)
  rays.append({'start_m':list(start),'direction':list(normal),'length_m':.08})
 apertures.append({'panel':panel,'centre_m':list(centre),'square_size_m':.025,'rays':rays})
for i in range(15):
 x=-W+2*W*(i+.5)/15
 for j in range(10):
  t=(j+.5)/10;window('back',(x,RY+(SY-RY)*t,Z0+(ZT-Z0)*t),(1,0,0),(0,SY-RY,ZT-Z0))
 for j in range(3):window('roof',(x,FY+(SY-FY)*(j+.5)/3,ZT),(1,0,0),(0,1,0))
for x,side in [(-W,'left'),(W,'right')]:
 for i in range(4):
  u=(i+.5)/4
  for j in range(10):
   t=(j+.5)/10;y=FY+((RY-FY)+(SY-RY)*t)*u+(.020 if i==0 else 0);z=Z0+(ZT-Z0)*t
   window(side,(x,y,z),(0,1,0),(0,0,1))
# Entire shallow mouth volume is disjoint from every actual triangle and solid.
# Convex sample lattice plus triangle-box overlap catches crossing thin ropes.
from mathutils.geometry import intersect_ray_tri
mouth_lo=Vector((-1.40,-.85,.12));mouth_hi=Vector((1.40,-.49,1.88))
# Separating axis theorem for each triangle against axis-aligned mouth box.
def tri_box(vs,lo,hi):
 c=(lo+hi)*.5;h=(hi-lo)*.5;q=[v-c for v in vs];edges=[q[1]-q[0],q[2]-q[1],q[0]-q[2]]
 axes=[Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)),edges[0].cross(edges[1])]
 axes.extend(e.cross(a) for e in edges for a in [Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))])
 for a in axes:
  if a.length_squared<1e-20:continue
  pp=[a.dot(v) for v in q];r=sum(abs(a[k])*h[k] for k in range(3))
  if min(pp)>r or max(pp)<-r:return False
 return True
mouth_checks=[]
for o in parts:
 intersections=sum(tri_box([o.matrix_world@o.data.vertices[k].co for k in t.vertices],mouth_lo,mouth_hi) for t in o.data.loop_triangles)
 contained=inside(trees[o.name],(mouth_lo+mouth_hi)*.5)
 assert intersections==0 and not contained,('Blocked front mouth',o.name,intersections,contained)
 mouth_checks.append({'name':o.name,'triangle_box_intersections':intersections,'mouth_centre_inside_component':contained})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<10000
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
 'net_rope_count':len(net_names),'every_net_rope_has_two_supported_ends':True,'net_aperture_windows':apertures,
 'front_mouth_empty_box':{'minimum_m':list(mouth_lo),'maximum_m':list(mouth_hi),'per_component':mouth_checks},
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/sports/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.015,1.00));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.88;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.7,-7.5,4.2),'gray-back3q':(-4.7,7.5,4.2)} if gray else {
 'thumbnail':(4.7,-7.5,4.2),'qa-front':(0,-7,1),'qa-side':(7,.015,1),'qa-top':(0,.015,8),
 'qa-back':(0,7,1),'qa-wireframe':(4.7,-7.5,4.2)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0007;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,1)),('silhouette-128-side',(7,.015,1))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
