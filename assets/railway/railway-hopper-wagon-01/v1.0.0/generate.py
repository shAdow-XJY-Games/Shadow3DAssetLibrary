"""Original static railway hopper wagon, metres, source Z up, rail axis Y.
One continuous thick annular hopper wall with an open mouth and actual lower
throat, a fixed partially withdrawn gate, open underframe and four steel wheels.
Root is the flange-bottom datum; tread bottoms Z=.04. Place at world Z=.16 on
original straight-track heads Z=.20. Wheel centres X=+/- .54 and Y=+/- .76.
No external files. --geometry-only / --no-render / --gray-only / --preview-only /
--extra-views. All images use a fresh import of the exact exported GLB.
No animation, operating gate, bulk-material physics, dynamic coupling, running,
load, stability, railway operation, engineering or safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='railway-hopper-wagon-01';VERSION='1.0.0';TITLE='Compact Railway Hopper Wagon'
DESCRIPTION=('Original static railway hopper wagon with one continuous thick open shell: a wide upper mouth, four '
 'inward-sloping interior walls and a true bottom-discharge throat. One fixed partly withdrawn steel gate leaves '
 'a visible clear opening; two guide rails and four slope-matched brackets attach it to an open underframe. '
 'Four independently editable flat steel treads, inner flanges and hubs use two fixed transverse axles. '
 'Metres, source Z up, long axis Y; flange-bottom origin. Tread centres X plus/minus .54 m, Y plus/minus .76 m, '
 'local tread bottom Z=.04 m. Place at Z=.16 m on the original 1.00 m clear-gauge straight track with head top '
 'Z=.20 m. The body is newly authored, not a reskinned flatbed. Three solid PBR materials and editable static '
 'components. No moving gate, bulk-material unloading, animation, continuous wheel motion, dynamic coupling, '
 'load, stability, physics, railway operations, engineering or safety certification.')
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
for name,color,rough,metal in [('OxideOrange_HopperShell',(.40,.18,.075,1),.71,.08),
 ('DeepTeal_SupportFrame',(.13,.27,.24,1),.70,.12),('RestrainedSteel_RunningGear',(.39,.44,.42,1),.58,.42)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('CompactRailwayHopperWagon',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['longitudinal_axis']='Y';root['static_fixed_gate_visual_only']=True
root['origin_datum']='flange bottom; tread bottom .04 m above origin; original rail placement Z=.16 m'
root['render_contract']=json.dumps(guard(),sort_keys=True)
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
def railwheel(name,center,radius,width,material,role,n=16):
 x,y,z=center;rr=radius/math.cos(math.pi/n)
 vs=[(x+dx,y+rr*math.sin(math.tau*i/n+math.pi/n),z+rr*math.cos(math.tau*i/n+math.pi/n)) for dx in [-width/2,width/2] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def clipped(x,y,c):return [(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c),(-x,-y+c)]
# A single watertight annular wall solid: no cap covers either actual aperture.
profiles=[(.25,.37,.03,.47),(.25,.37,.03,.57),(.65,1.03,.08,1.05),(.65,1.03,.08,1.46),
 (.675,1.055,.08,1.46),(.675,1.055,.08,1.51),(.61,.99,.06,1.51),(.61,.99,.06,1.07),
 (.21,.33,.02,.59),(.21,.33,.02,.47)]
vs=[(x,y,z) for a,b,c,z in profiles for x,y in clipped(a,b,c)]
fs=[(k*8+i,k*8+(i+1)%8,((k+1)%len(profiles))*8+(i+1)%8,((k+1)%len(profiles))*8+i) for k in range(len(profiles)) for i in range(8)]
mesh('Hopper_ContinuousThickOpenShell',vs,fs,0,'continuous thick sloping hopper with genuine top and bottom apertures',origin=(0,0,.99))
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Chassis_'+label,(side*.37,0,.55),(.10,1.95,.14),1,'long supporting frame clear of central discharge aperture',bevel=.004)
 for y,end in [(-.48,'Front'),(.48,'Rear')]:
  # The four bracket tips follow the outer hopper slope, not an arbitrary tall post.
  profile=[(.33,.55),(.50,.55),(.50,.882),(.33,.678)]
  vv=[(side*x,yy,z) for yy in [y-.06,y+.06] for x,z in profile]
  ff=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
  mesh('HopperBracket_'+label+'_'+end,vv,ff,1,'slope-matched solid support below shell; no cavity intrusion',origin=(side*.41,y,.70))
 # Fixed slides attach directly to neck, with enough rail material below the gate.
 box('GateGuide_'+label,(side*.255,.25,.445),(.06,1.18,.06),2,'fixed neck-mounted gate guide',bevel=.002)
box('Gate_FixedPartlyWithdrawn',(0,.495,.455),(.49,.75,.025),2,'fixed static plate; front portion of real throat remains open',bevel=.002)
for y,end in [(-.90,'Front'),(.90,'Rear')]:
 box('Crossmember_'+end,(0,y,.55),(1.03,.14,.12),1,'fixed end crossmember; central discharge throat is unobstructed',bevel=.004)
for y,end in [(-.76,'Front'),(.76,'Rear')]:
 railwheel('Axle_'+end,(0,y,.24),.035,1.16,2,'fixed axle along X')
 for side,label in [(-1,'Left'),(1,'Right')]:
  suffix=label+'_'+end
  railwheel('Tread_'+suffix,(side*.54,y,.24),.20,.10,2,'fixed flanged steel tread with finite bottom facet')
  railwheel('Flange_'+suffix,(side*.48,y,.24),.24,.035,2,'inner flange with .0025 m nominal rail-head side clearance')
  railwheel('Hub_'+suffix,(side*.596,y,.24),.065,.04,2,'fixed outer wheel hub')
  box('AxleHanger_'+suffix,(side*.37,y,.37),(.09,.12,.28),1,'fixed hanger linking axle and chassis',bevel=.004)
for sign,end in [(-1,'Front'),(1,'Rear')]:
 box('CouplingShank_'+end,(0,sign*1.10,.55),(.14,.34,.08),2,'fixed coupling shank; no dynamic compatibility claim',bevel=.003)
 box('CouplingFace_'+end,(0,sign*1.26,.55),(.28,.065,.13),2,'static restrained coupling face',bevel=.004)
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
for side,label in [(-1,'Left'),(1,'Right')]:
 for y,end in [(-.48,'Front'),(.48,'Rear')]:
  bracket='HopperBracket_'+label+'_'+end
  joint(bracket,'Chassis_'+label,[(side*x,y,.59) for x in [.35,.37,.39]])
  joint(bracket,'Hopper_ContinuousThickOpenShell',[(side*x,y,.57+(x-.25)*1.2+.006) for x in [.35,.40,.45]])
 joint('GateGuide_'+label,'Hopper_ContinuousThickOpenShell',[(side*.24,y,.472) for y in [-.25,0,.25]])
 joint('GateGuide_'+label,'Gate_FixedPartlyWithdrawn',[(side*.235,y,.455) for y in [.2,.45,.70]])
 for y,end in [(-.90,'Front'),(.90,'Rear')]:
  joint('Chassis_'+label,'Crossmember_'+end,[(side*x,y,.55) for x in [.35,.37,.39]])
 for y,end in [(-.76,'Front'),(.76,'Rear')]:
  suffix=label+'_'+end
  joint('Chassis_'+label,'AxleHanger_'+suffix,[(side*x,y,.495) for x in [.35,.37,.39]])
  joint('AxleHanger_'+suffix,'Axle_'+end,[(side*x,y,.25) for x in [.35,.37,.39]])
  joint('Axle_'+end,'Tread_'+suffix,[(side*x,y,.24) for x in [.52,.54,.56]])
  joint('Tread_'+suffix,'Flange_'+suffix,[(side*.494,y,z) for z in [.12,.24,.36]])
  joint('Tread_'+suffix,'Hub_'+suffix,[(side*.585,y,z) for z in [.22,.24,.26]])
for sign,end in [(-1,'Front'),(1,'Rear')]:
 joint('Crossmember_'+end,'CouplingShank_'+end,[(x,sign*.95,.55) for x in [-.025,0,.025]])
 joint('CouplingShank_'+end,'CouplingFace_'+end,[(x,sign*1.25,.55) for x in [-.025,0,.025]])
# True through aperture, tested against every assembled mesh, not a black inset.
clear_rays=[]
for x,y in [(0,-.15),(-.10,-.15),(.10,-.15),(0,0),(-.10,0),(.10,0)]:
 for name,tree in trees.items():
  assert tree.ray_cast(Vector((x,y,1.7)),Vector((0,0,-1)),1.9)[0] is None,('Blocked bottom throat',name,x,y)
 clear_rays.append([x,y])
slopes=[]
for x,y,z in [(.40,0,.818),(-.40,0,.818),(0,.60,.59+.27*.48/.66),(0,-.60,.59+.27*.48/.66)]:
 hits=[]
 for name,tree in trees.items():
  p,n,_,d=tree.ray_cast(Vector((x,y,1.7)),Vector((0,0,-1)),1.4)
  if p is not None:hits.append((d,name,p,n))
 hit=min(hits,key=lambda row:row[0]);assert hit[1]=='Hopper_ContinuousThickOpenShell' and abs(hit[2].z-z)<1e-6 and hit[3].z>.4,(x,y,hit,z)
 slopes.append({'xy_m':[x,y],'first_inner_surface_z_m':hit[2].z,'normal':list(hit[3])})
p,normal,_,_=trees['Gate_FixedPartlyWithdrawn'].ray_cast(Vector((0,.22,1.7)),Vector((0,0,-1)),1.4)
assert p is not None and abs(p.z-.4675)<1e-6,'Fixed gate cover absent'
supports=[]
for name in sorted(n for n in byname if n.startswith('Tread_')):
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z-.04) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.007,(name,area)
 supports.append({'name':name,'local_tread_bottom_z_m':.04,'area_m2':area,'triangles':patch})
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
 'components':component_checks,'connection_interior_points':joints,'assembly_clear_throat_z_rays_xy_m':clear_rays,
 'actual_four_interior_slope_rays':slopes,'fixed_gate_cover_top_z_m':p.z,'finite_tread_supports':supports,
 'rail_interface':{'wheel_x_m':[-.54,.54],'axle_y_m':[-.76,.76],'tread_bottom_local_z_m':.04,'flange_bottom_local_z_m':0,'original_track_placement_z_m':.16,
 'status':'actual original-track GLB contact and negative placements require independent QA'},
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/railway/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'railway','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.20;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-6,4.5),'gray-back3q':(-4,5,4.5)} if gray else {
 'thumbnail':(4,-6,4.5),'qa-front':(0,-6,.75),'qa-side':(6,0,.75),'qa-top':(0,0,7),
 'qa-back':(0,6,.75),'qa-wireframe':(4,-6,4.5)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0017;w.use_replace=True;w.use_even_offset=False;w.offset=1
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
