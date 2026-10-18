"""Original static single-seat playground swing, metre scale, source Z up.
Single pose only. Four feet, end A-frames, top beam, fixed collars, real rope
suspension with split bridles and a thick seat. Every render uses a fresh GLB.
Modes: --geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
No animation, people, rope physics, load, anchoring or child-safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='playground-a-frame-swing-01';VERSION='1.0.0';TITLE='Meadow Single-seat A-frame Swing'
DESCRIPTION=('Original static low-poly single-seat swing with two sage A-shaped end frames, four finite ground shoes, '
 'an ivory crossbeam, side ties and four diagonal knee braces. Two fixed metal beam collars and downward rope ferrules '
 'support long sand-coloured ropes; each divides through a lower ferrule into two short bridle ropes attached to four '
 'physical seat brackets on a single coral seat plank. The complete support route is real closed geometry and every '
 'named part connects to the four ground shoes. The seated central space, seat-to-frame and under-seat clearances '
 'are checked on actual triangles in this one rest pose. Five solid PBR materials; metre units, native Z up, front -Y '
 'and ground-centre origin. One independently reusable playground prop, distinct from the earlier pivoted seesaw, '
 'slide, picnic bench, clothesline and rigid footbridge. No person, extra scenery, textures or external dependencies. '
 'Fixed stylized game visual only: no swinging, rope dynamics, animation, load rating, anchoring, tipping resistance, '
 'fall-zone or entrapment compliance, engineering, playground or child-safety certification.')
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
for name,color,rough,metal in [('SagePowdercoat_Frame',(.23,.40,.32,1),.76,.12),
 ('WarmIvory_Crossbeam',(.79,.73,.54,1),.74,.10),('SandFiber_Ropes',(.58,.39,.18,1),.94,0),
 ('Graphite_Fittings',(.072,.10,.09,1),.49,.48),('MutedCoral_Seat',(.62,.22,.105,1),.82,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('MeadowSingleSeatSwing',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True
root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[];spines={};rope_names=[]
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

# GEOMETRY_BEGIN: original fixed assembly; ropes and fittings are closed meshes.
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
def end_link(name,target,end):
 a,b=spines[name];start=a if end==0 else b;direction=((b-a) if end==0 else (a-b)).normalized()
 joint(name,target,[start+direction*d for d in [.006,.010,.014]])
def rope(name,a,b,support_a,support_b):
 rod(name,a,b,.013,2,'closed fixed suspension rope with physically embedded ends',12);rope_names.append(name)
 end_link(name,support_a,0);end_link(name,support_b,1)
def collar(name,x,ri,ro,z,width):
 n=24;vs=[(xx,r*math.sin(math.tau*i/n),z+r*math.cos(math.tau*i/n)) for xx in [x-width/2,x+width/2] for r in [ri,ro] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,3,'thick closed annular fixed clamp fitted around the beam')
feet=[];FX=1.18;FY=.76;ZT=2.15;LZ=.045
for x,side in [(-FX,'Left'),(FX,'Right')]:
 for y,end in [(-FY,'Front'),(FY,'Back')]:
  foot='Foot_'+side+'_'+end;box(foot,(x,y,.05),(.23,.27,.10),3,'finite flat grounded shoe',.007);feet.append(foot)
  leg='Leg_'+side+'_'+end;rod(leg,(x,y,LZ),(x,0,ZT),.061,0,'splayed A-frame end leg',16)
  end_link(leg,foot,0)
 # End tie lies between the two actual leg centres at its height.
 tie_z=.96;tie_y=FY*(ZT-tie_z)/(ZT-LZ)
 tie='SideTie_'+side;rod(tie,(x,-tie_y,tie_z),(x,tie_y,tie_z),.035,0,'end-frame horizontal tie',12)
 end_link(tie,'Leg_'+side+'_Front',0);end_link(tie,'Leg_'+side+'_Back',1)
rod('Crossbeam',(-1.37,0,ZT),(1.37,0,ZT),.078,1,'one continuous upper crossbeam',24)
for x,side in [(-FX,'Left'),(FX,'Right')]:
 for end in ['Front','Back']:end_link('Leg_'+side+'_'+end,'Crossbeam',1)
 sign=-1 if side=='Left' else 1
 for y,end in [(-1,'Front'),(1,'Back')]:
  z=1.77;ly=y*FY*(ZT-z)/(ZT-LZ);n='KneeBrace_'+side+'_'+end
  rod(n,(sign*.83,0,ZT),(x,ly,z),.029,0,'diagonal crossbeam-to-leg knee brace',12)
  end_link(n,'Crossbeam',0);end_link(n,'Leg_'+side+'_'+end,1)
box('Seat_Plank',(0,0,.49),(.70,.32,.065),4,'single thick gently bevelled seat plank',.018)
for x,side in [(-.29,'Left'),(.29,'Right')]:
 clamp='BeamCollar_'+side;collar(clamp,x,.060,.101,ZT,.052)
 joint(clamp,'Crossbeam',[(x+d,0,ZT+.068) for d in [-.012,0,.012]])
 upper='UpperFerrule_'+side;rod(upper,(x,0,1.996),(x,0,2.076),.026,3,'fixed lower beam-collar rope ferrule',16)
 joint(upper,clamp,[(x+d,0,2.065) for d in [-.009,0,.009]])
 lower='BridleFerrule_'+side;rod(lower,(x,0,.724),(x,0,.794),.025,3,'lower splitting ferrule physically holding three rope ends',16)
 rope('SuspensionRope_'+side,(x,0,.762),(x,0,2.035),lower,upper)
 for y,end in [(-.13,'Front'),(.13,'Back')]:
  bracket='SeatBracket_'+side+'_'+end;box(bracket,(x,y,.525),(.055,.050,.050),3,'fixed metal seat attachment block',.003)
  joint(bracket,'Seat_Plank',[(x+d,y,.512) for d in [-.012,0,.012]])
  rope('BridleRope_'+side+'_'+end,(x,0,.758),(x,y,.530),lower,bracket)
# GEOMETRY_END
# Real source-mesh checks, never solely dimensions or declared roles.
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-10 and deg==0,(o.name,bad,vol,deg)
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
assert all(sum(j['a']==n for j in joints)==2 for n in rope_names)
supports=[]
for name in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.03;supports.append({'name':name,'area_m2':area,'triangles':patch})

# Geometric empty volume tests. These are visual rest-pose clearances, not user safety dimensions.
def tri_box(vs,lo,hi):
 c=(lo+hi)*.5;h=(hi-lo)*.5;q=[v-c for v in vs];edges=[q[1]-q[0],q[2]-q[1],q[0]-q[2]]
 axes=[Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)),edges[0].cross(edges[1])]
 axes.extend(e.cross(a) for e in edges for a in [Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))])
 for a in axes:
  if a.length_squared<1e-20:continue
  pp=[a.dot(v) for v in q];r=sum(abs(a[k])*h[k] for k in range(3))
  if min(pp)>r or max(pp)<-r:return False
 return True
clearances=[]
for label,lower,upper in [('central_seat_space',(-.23,-.32,.565),(.23,.32,1.98)),
 ('under_seat',(-.35,-.16,.05),(.35,.16,.43)),
 ('left_seat_to_frame',(-1.02,-.25,.42),(-.40,.25,.72)),
 ('right_seat_to_frame',(.40,-.25,.42),(1.02,.25,.72))]:
 lower,upper=Vector(lower),Vector(upper);rows=[]
 for o in parts:
  intersections=sum(tri_box([o.matrix_world@o.data.vertices[k].co for k in t.vertices],lower,upper) for t in o.data.loop_triangles)
  contained=inside(trees[o.name],(lower+upper)*.5)
  assert intersections==0 and not contained,('Blocked static clearance',label,o.name,intersections,contained)
  rows.append({'name':o.name,'triangle_box_intersections':intersections,'box_centre_inside_component':contained})
 clearances.append({'name':label,'minimum_m':list(lower),'maximum_m':list(upper),'per_component':rows})
# Real moved-geometry negative: pull one long rope out of both fixed ferrules.
o=byname['SuspensionRope_Left'];delta=Vector((.20,0,0));neg_tree=BVHTree.FromPolygons([o.matrix_world@v.co+delta for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
negative=[]
for j in joints:
 if j['a']!=o.name:continue
 failures=sum(not inside(neg_tree,p['world_point_m']) for p in j['interior_overlap_points']);assert failures==3
 negative.append({'displaced_mesh':o.name,'translation_m':list(delta),'support':j['b'],'failed_anchor_count':failures})
assert len(negative)==2
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
 'suspension_rope_count':len(rope_names),'every_rope_has_two_supported_ends':True,'static_empty_clearance_volumes':clearances,
 'displaced_suspension_rope_negative':negative,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/playground/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,1.10));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.40;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.7,-7.5,3.75),'gray-back3q':(-4.7,7.5,3.75)} if gray else {
 'thumbnail':(4.7,-7.5,3.75),'qa-front':(0,-7,1.1),'qa-side':(7,0,1.1),'qa-top':(0,0,8),
 'qa-back':(0,7,1.1),'qa-wireframe':(4.7,-7.5,3.75)}
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
 for name,pos in [('silhouette-128-front',(0,-7,1.1)),('silhouette-128-side',(7,0,1.1))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
