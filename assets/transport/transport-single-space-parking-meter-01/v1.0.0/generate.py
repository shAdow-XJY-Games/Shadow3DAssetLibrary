"""Original S01 single-space parking-meter static visual prop. Metres, source Z up.
Root at ground under the post; front/operator face -Y. One grounded base and post,
faceted arch-top timer head with genuine recessed display and deep coin pocket,
fixed analog gauge marks/pointer, and a fixed winding-handle visual. No animation,
countdown, coin acceptance, payment, billing, security, stability or engineering claim.
Separate named closed components; five solid PBR materials; no external inputs.
--no-render / --geometry-only / --gray-only / --preview-only / --extra-views.
All views use fresh exact exported GLB; Cycles 128, FIXED4, no adaptive or denoise.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='transport-single-space-parking-meter-01';VERSION='1.0.0';TITLE='Single-space Parking Meter'
DESCRIPTION=('Original S01 static single-space parking-meter prop with a faceted arch-top head, a genuinely recessed '
 'analog-display pocket with fixed gauge marks and pointer, a deep closed-back coin-slot recess, and a fixed winding '
 'handle. The continuous post sits inside a socket on a flat ground plate with four static bolt heads. Metre scale, '
 'source Z up, operator face -Y, root at the ground under the post. Five solid PBR materials, no textures. '
 'Independent editable closed components. Existing cycle-service post and bus-stop information pole contain no '
 'parking timer; this is an original transport-expansion prop. No operating timer, animation, coin handling, '
 'payment, billing, parking enforcement, security, stability, engineering or infrastructure certification.')
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
for name,color,rough,metal in [('MutedTeal_MeterHousing',(.16,.34,.32,1),.55,.25),
 ('WarmGrey_PostAndControl',(.38,.41,.40,1),.47,.55),('Charcoal_MarksAndSlot',(.028,.038,.037,1),.78,0),
 ('WarmIvory_Dial',(.76,.73,.61,1),.75,0),('MutedOrange_StaticPointer',(.59,.18,.065,1),.60,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('SingleSpaceParkingMeter',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['operator_face']='-Y';root['static_visual_only']=True
root['ground_origin']='under continuous post';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Restrained manufactured chamfer','BEVEL');b.width=bevel;b.segments=1
  bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def cylinder(name,center,radius,depth,material,role,axis='Z',n=16):
 x,y,z=center;vs=[]
 for d in [-depth/2,depth/2]:
  for i in range(n):
   a=i*math.tau/n;u=radius*math.cos(a);v=radius*math.sin(a)
   vs.append((x+u,y+d,z+v) if axis=='Y' else (x+u,y+v,z+d))
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def extrude_xz(name,outline,y0,y1,material,role,bevel=0):
 n=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 origin=(sum(p[0] for p in outline)/n,(y0+y1)/2,sum(p[1] for p in outline)/n)
 return mesh(name,vs,fs,material,role,origin,bevel)
def pocket(body,name,outline,back):
 cutter=extrude_xz(name,outline,-.18,back,0,'temporary pocket cutter')
 bpy.context.view_layer.objects.active=body;mod=body.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);parts.remove(cutter);del byname[name];bpy.data.objects.remove(cutter,do_unlink=True)
 bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
def clipped_rect(x0,x1,z0,z1,c):
 return [(x0+c,z0),(x1-c,z0),(x1,z0+c),(x1,z1-c),(x1-c,z1),(x0+c,z1),(x0,z1-c),(x0,z0+c)]
def radial_bar(name,a,b,width,depth,material,role,y=-.061):
 a,b=Vector((a[0],y,a[1])),Vector((b[0],y,b[1]));t=(b-a).normalized();n=Vector((-t.z,0,t.x));vs=[]
 for p in [a,b]:
  for d in [-depth/2,depth/2]:
   for s in [-1,1]:vs.append(p+n*s*width/2+Vector((0,d,0)))
 fs=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
 return mesh(name,vs,fs,material,role,(a+b)/2)
# The head is a genuine closed solid with two carved cavities, not flat overlays.
head=extrude_xz('MeterHead_RecessedClosedHousing',[(-.12,1.04),(.12,1.04),(.155,1.075),(.155,1.42),(.105,1.50),(-.105,1.50),(-.155,1.42),(-.155,1.075)],-.105,.095,0,'closed arch-top housing with true display and coin pockets',.005)
pocket(head,'CUT_Display',clipped_rect(-.115,.115,1.275,1.425,.012),-.055)
pocket(head,'CUT_CoinSlot',[(-.041,1.217),(.041,1.217),(.041,1.233),(-.041,1.233)],-.027)
# The opaque display is inset by 45mm; gauge and pointer are fixed solid relief.
box('Display_InsetDial',(0,-.055,1.35),(.218,.010,.138),3,'fixed opaque dial plate seated into pocket floor',bevel=.002)
for i in range(7):
 a=math.radians(20+i*140/6);ri=.079 if i%3==0 else .085;ro=.096
 radial_bar('Display_FixedTick_%02d'%i,(ri*math.cos(a),1.293+ri*math.sin(a)),(ro*math.cos(a),1.293+ro*math.sin(a)),.005,.004,2,'fixed analog gauge graduation; no time calculation')
a=math.radians(58)
radial_bar('Display_FixedPointer',(-.009*math.cos(a),1.303-.009*math.sin(a)),(.073*math.cos(a),1.303+.073*math.sin(a)),.006,.004,4,'fixed orange indicator; not an operating timer')
cylinder('Display_PointerBoss',(0,-.064,1.303),.009,.012,2,'static boss joining pointer and dial',axis='Y',n=12)
box('CoinSlot_DeepBackstop',(0,-.027,1.225),(.078,.006,.014),2,'dark closed-back slot floor recessed 75mm behind front',bevel=0)
cylinder('Control_FixedMount',(0,-.110,1.123),.032,.035,1,'fixed control mount seated into housing',axis='Y',n=12)
box('Control_FixedTurnBar',(0,-.135,1.123),(.088,.026,.021),1,'fixed transverse winding-bar visual; no rotation',bevel=.003)
# Continuous support chain from the arch head through post/socket to finite ground plate.
cylinder('Post_Continuous',(0,0,.588),.038,.994,1,'continuous upright post penetrating socket and head',n=16)
cylinder('Post_FootSocket',(0,0,.098),.064,.13,0,'fixed mounting socket joining pole and plate',n=16)
box('Base_GroundPlate',(0,0,.024),(.27,.23,.048),1,'flat finite grounded mounting plate',bevel=.006)
for x,labelx in [(-.099,'L'),(.099,'R')]:
 for y,labely in [(-.079,'F'),(.079,'B')]:
  cylinder('Base_Bolt_'+labelx+labely,(x,y,.050),.013,.014,2,'fixed bolt-head visual embedded in mounting plate',n=6)
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
  clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
joint('MeterHead_RecessedClosedHousing','Post_Continuous',[(0,0,z) for z in [1.050,1.060,1.070]])
joint('Post_Continuous','Post_FootSocket',[(0,0,z) for z in [.105,.125,.145]])
joint('Post_FootSocket','Base_GroundPlate',[(x,0,.040) for x in [-.02,0,.02]])
for x,labelx in [(-.099,'L'),(.099,'R')]:
 for y,labely in [(-.079,'F'),(.079,'B')]:joint('Base_Bolt_'+labelx+labely,'Base_GroundPlate',[(x,y,.045)])
joint('Display_InsetDial','MeterHead_RecessedClosedHousing',[(x,-.052,1.35) for x in [-.08,0,.08]])
for i in range(7):
 a=math.radians(20+i*140/6);r=.090
 joint('Display_FixedTick_%02d'%i,'Display_InsetDial',[(r*math.cos(a),-.0595,1.293+r*math.sin(a))])
joint('Display_FixedPointer','Display_InsetDial',[(r*math.cos(math.radians(58)),-.0595,1.303+r*math.sin(math.radians(58))) for r in [.02,.04,.06]])
joint('Display_PointerBoss','Display_InsetDial',[(0,-.059,1.303)])
joint('CoinSlot_DeepBackstop','MeterHead_RecessedClosedHousing',[(x,-.025,1.225) for x in [-.02,0,.02]])
joint('Control_FixedMount','MeterHead_RecessedClosedHousing',[(x,-.100,1.123) for x in [-.01,0,.01]])
joint('Control_FixedTurnBar','Control_FixedMount',[(x,-.125,1.123) for x in [-.01,0,.01]])
# Ray depths use actual complete assembly triangles and test visible cavity floors.
pocket_rays=[]
for kind,points,expected_y in [('display',[(-.09,1.40),(0,1.40),(.09,1.40)],-.060),('coin',[(-.025,1.225),(0,1.225),(.025,1.225)],-.030)]:
 for x,z in points:
  hits=[]
  for name,tree in trees.items():
   p,n,_,d=tree.ray_cast(Vector((x,-.20,z)),Vector((0,1,0)),.40)
   if p is not None:hits.append((d,name,p))
  hit=min(hits,key=lambda h:h[0]);assert abs(hit[2].y-expected_y)<1e-6,(kind,x,z,hit)
  pocket_rays.append({'pocket':kind,'ray_origin_m':[x,-.20,z],'first_surface_name':hit[1],'first_surface_y_m':hit[2].y,'recess_from_front_m':hit[2].y+.105})
supports=[]
o=byname['Base_GroundPlate'];patch=[]
for t in o.data.loop_triangles:
 v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
 if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
area=sum(t['area_m2'] for t in patch);assert area>.04,area
supports.append({'name':o.name,'area_m2':area,'triangles':patch})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes),'Solid-only PBR expected'
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
 'components':component_checks,'connection_interior_points':joints,'actual_recess_first_surface_rays':pocket_rays,'finite_ground_supports':supports,
 'placement_example':{'external_asset':'transport-curb-straight-01','meter_translation_source_m':[0,0,.15],'scope':'translation reference on original level pavement; ground is not exported, no snapping or pedestrian-clearance guarantee'},
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
focus=Vector((0,0,.75));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.80;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(2.4,-5,2.3),'gray-back3q':(-2.8,5,2.5)} if gray else {
 'thumbnail':(2.4,-5,2.3),'qa-front':(0,-6,.75),'qa-side':(6,0,.75),'qa-top':(0,0,7),
 'qa-back':(0,6,.75),'qa-wireframe':(2.4,-5,2.3)}
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
 for name,pos in [('silhouette-128-front',(0,-6,.75)),('silhouette-128-side',(6,0,.75))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
