"""Original static railway maintenance wagon, metres, source Z up, rail axis Y.
Fixed rear workbench, two genuinely open-front storage compartments, solid
toolboard with fixed supported tools, and an unobstructed forward work deck.
Root is the flange-bottom datum; tread bottoms Z=.04. Place at world Z=.16 on
original straight-track heads Z=.20. Wheel centres X=+/- .54 and Y=+/- .76.
No external files. --geometry-only / --no-render / --gray-only / --preview-only /
--extra-views. All images use a fresh import of the exact exported GLB.
No animation, operating tools, material physics, dynamic coupling, running,
load, stability, railway operation, engineering or safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='railway-maintenance-wagon-01';VERSION='1.0.0';TITLE='Railway Maintenance Workbench Wagon'
DESCRIPTION=('Original static railway maintenance wagon with a fixed rear workbench attached through four legs to a broad deck. '
 'Two genuinely open-front storage compartments have a solid shelf, side walls, divider and back. A rear toolboard '
 'holds a recognisable fixed hammer, open-jaw spanner and screwdriver on solid mounts; the forward deck remains '
 'visibly open as a work area. The tabletop is clear and every component has a physical static support path. '
 'Metres, source Z up, long axis Y; flange-bottom origin. Four tread centres X plus/minus .54 m, Y plus/minus .76 m; '
 'local tread bottom Z=.04 m. Place at Z=.16 m on the original 1.00 m clear-gauge track with head top Z=.20 m. '
 'Four solid PBR materials, named editable components, no external source dependency. This work station is '
 'different from the existing hand-push toolbox trolley and empty freight flatbed. Static visual prop only; '
 'no driving, braking, lifting, animated wheels, tool operation, dynamic coupling, human occupancy, load capacity, '
 'physics, engineering, railway safety or regulatory certification.')
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
for name,color,rough,metal in [('WarmTimber_WorkSurfaces',(.43,.29,.16,1),.79,0),
 ('MutedOchre_UtilityFrame',(.43,.28,.09,1),.72,.12),('RestrainedSteel_RunningGearAndTools',(.30,.35,.36,1),.58,.45),
 ('DeepTeal_ToolStorage',(.10,.25,.24,1),.70,.10)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('RailwayMaintenanceWorkbenchWagon',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['longitudinal_axis']='Y';root['static_fixed_workstation_visual_only']=True
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
# Underframe, wheel positions and facet-based rail datum follow the existing railway family.
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Chassis_'+label,(side*.37,0,.53),(.10,2.00,.14),1,'long chassis supporting deck',bevel=.004)
for y,end in [(-.90,'Front'),(0,'Middle'),(.90,'Rear')]:
 box('Crossmember_'+end,(0,y,.54),(1.10,.12,.10),1,'deck support across the chassis',bevel=.004)
for y,end in [(-.76,'Front'),(.76,'Rear')]:
 railwheel('Axle_'+end,(0,y,.24),.035,1.16,2,'fixed axle along X')
 for side,label in [(-1,'Left'),(1,'Right')]:
  suffix=label+'_'+end
  railwheel('Tread_'+suffix,(side*.54,y,.24),.20,.10,2,'flat steel tread with finite bottom facet')
  railwheel('Flange_'+suffix,(side*.48,y,.24),.24,.035,2,'inner flange with .0025 m nominal rail-head side clearance')
  railwheel('Hub_'+suffix,(side*.596,y,.24),.065,.04,2,'fixed outer hub')
  box('AxleHanger_'+suffix,(side*.37,y,.37),(.09,.12,.28),1,'hanger joining axle to chassis',bevel=.004)
for sign,end in [(-1,'Front'),(1,'Rear')]:
 box('CouplingShank_'+end,(0,sign*1.10,.53),(.14,.34,.07),2,'fixed coupling shank; no dynamic compatibility claim',bevel=.003)
 box('CouplingFace_'+end,(0,sign*1.26,.53),(.28,.065,.13),2,'static coupling face',bevel=.004)
box('Deck_WorkArea',(0,0,.61),(1.24,2.10,.08),0,'solid broad forward work deck',bevel=.008)
# Four fixed legs mount the rear workbench directly into the deck.
for x,side in [(-.48,'Left'),(.48,'Right')]:
 for y,end in [(.46,'Front'),(.90,'Rear')]:
  box('BenchLeg_'+side+'_'+end,(x,y,1.04),(.07,.07,.84),3,'fixed workbench leg with actual deck and worktop overlap',bevel=.004)
box('Bench_Worktop',(0,.68,1.47),(1.14,.60,.09),0,'fixed clear tabletop at .865 m above the deck',bevel=.008)
# Actual open-front compartments, with different outer extents to avoid coincident skins.
box('Storage_Shelf',(0,.68,.88),(1.016,.50,.05),3,'solid bottom shelf spanning between bench legs',bevel=.003)
for x,side in [(-.49,'Left'),(.49,'Right')]:
 box('Storage_Side_'+side,(x,.69,1.07),(.04,.46,.38),3,'real compartment side wall',bevel=.002)
box('Storage_Back',(0,.905,1.07),(.98,.04,.36),3,'real rear wall giving the open compartments visible depth',bevel=.002)
box('Storage_Divider',(0,.69,1.055),(.035,.45,.35),3,'physical divider of two open front storage compartments',bevel=.002)
# Uprights sit behind the board and overlap the worktop; no unsupported floating panel.
for x,side in [(-.48,'Left'),(.48,'Right')]:
 box('ToolboardUpright_'+side,(x,.99,1.72),(.06,.05,.70),3,'rear upright supporting toolboard and fixed into tabletop',bevel=.003)
box('Toolboard',(0,.96,1.80),(1.08,.055,.62),3,'solid tool panel behind bench, with separate supported tool mounts',bevel=.006)
# Three restrained fixed tools, each with a real support mount back to the board.
box('Hammer_Handle',(-.30,.889,1.77),(.035,.035,.30),0,'fixed timber hammer handle',bevel=.005)
box('Hammer_Head',(-.30,.889,1.94),(.22,.055,.07),2,'fixed steel hammer head',bevel=.010)
# Extruded concave outline creates a genuine open jaw, not a painted slot.
profile=[(-.025,-.18),(.025,-.18),(.025,.08),(.07,.12),(.07,.205),(.027,.205),(.027,.142),(-.027,.142),(-.027,.205),(-.07,.205),(-.07,.12),(-.025,.08)]
vs=[(.06+x,y,1.76+z) for y in [.873,.905] for x,z in profile];n=len(profile)
fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
mesh('Spanner_OpenJaw',vs,fs,2,'fixed steel spanner with true open jaw',origin=(.06,.889,1.76))
box('Screwdriver_Handle',(.34,.889,1.69),(.055,.05,.16),1,'fixed broad screwdriver grip',bevel=.008)
box('Screwdriver_Shaft',(.34,.889,1.87),(.016,.020,.23),2,'fixed screwdriver shaft attached into grip',bevel=.001)
for label,x,z in [('Hammer_Lower',-.30,1.67),('Hammer_Upper',-.30,1.85),('Spanner_Lower',.06,1.64),('Spanner_Upper',.06,1.80),('Screwdriver',.34,1.69)]:
 box('ToolMount_'+label,(x,.919,z),(.043,.080,.035),2,'solid fixed mount joining tool to board',bevel=.002)
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
 joint('Deck_WorkArea','Chassis_'+label,[(side*x,y,.585) for x,y in [(.35,-.40),(.39,0),(.37,.40)]])
 for y,end in [(-.90,'Front'),(0,'Middle'),(.90,'Rear')]:
  joint('Chassis_'+label,'Crossmember_'+end,[(side*x,y+dy,.54) for x,dy in [(.35,-.02),(.39,-.02),(.37,.02)]])
 for y,end in [(-.76,'Front'),(.76,'Rear')]:
  suffix=label+'_'+end
  joint('Chassis_'+label,'AxleHanger_'+suffix,[(side*x,y+dy,.49) for x,dy in [(.35,-.02),(.39,-.02),(.37,.02)]])
  joint('AxleHanger_'+suffix,'Axle_'+end,[(side*x,y+dy,.25) for x,dy in [(.35,-.005),(.39,-.005),(.37,.005)]])
  joint('Axle_'+end,'Tread_'+suffix,[(side*x,y+dy,.24) for x,dy in [(.52,-.005),(.56,-.005),(.54,.005)]])
  joint('Tread_'+suffix,'Flange_'+suffix,[(side*.494,y+dy,z) for dy,z in [(-.01,.12),(.01,.12),(0,.36)]])
  joint('Tread_'+suffix,'Hub_'+suffix,[(side*.585,y+dy,z) for dy,z in [(-.01,.23),(.01,.23),(0,.26)]])
for sign,end in [(-1,'Front'),(1,'Rear')]:
 joint('Crossmember_'+end,'CouplingShank_'+end,[(x,sign*y,.53) for x,y in [(-.025,.94),(.025,.94),(0,.95)]])
 joint('CouplingShank_'+end,'CouplingFace_'+end,[(x,sign*y,.53) for x,y in [(-.025,1.25),(.025,1.25),(0,1.26)]])
for x,side in [(-.48,'Left'),(.48,'Right')]:
 for y,end in [(.46,'Front'),(.90,'Rear')]:
  leg='BenchLeg_'+side+'_'+end
  joint('Deck_WorkArea',leg,[(x+dx,y+dy,.635) for dx,dy in [(-.01,-.01),(.01,-.01),(0,.01)]])
  joint('Bench_Worktop',leg,[(x+dx,y+dy,1.44) for dx,dy in [(-.01,-.01),(.01,-.01),(0,.01)]])
  joint('Storage_Shelf',leg,[(x+dx,y+dy,.88) for dx,dy in [(-.01,-.005),(.01,-.005),(0,.005)]])
 joint('Storage_Shelf','Storage_Side_'+side,[(x+dx,y,.895) for dx,y in [(-.005,.55),(.005,.55),(0,.80)]])
 joint('Storage_Back','Storage_Side_'+side,[(x+dx,.900,z) for dx,z in [(-.005,1.00),(.005,1.00),(0,1.15)]])
 joint('Bench_Worktop','ToolboardUpright_'+side,[(x+dx,.972,1.46+dz) for dx,dz in [(-.01,0),(.01,0),(0,.025)]])
 joint('Toolboard','ToolboardUpright_'+side,[(x+dx,.977,z) for dx,z in [(-.01,1.65),(.01,1.65),(0,1.95)]])
joint('Storage_Shelf','Storage_Back',[(x,.905,.895) for x in [-.3,0,.3]])
joint('Storage_Shelf','Storage_Divider',[(0,y,.895) for y in [.52,.68,.83]])
joint('Storage_Back','Storage_Divider',[(x,.905,z) for x,z in [(-.005,1.00),(.005,1.00),(0,1.15)]])
joint('Hammer_Handle','Hammer_Head',[(-.30+dx,.889+dy,1.912) for dx,dy in [(-.008,-.006),(.008,-.006),(0,.006)]])
joint('Screwdriver_Handle','Screwdriver_Shaft',[(.34+dx,.889+dy,1.762) for dx,dy in [(-.003,-.004),(.003,-.004),(0,.004)]])
for label,x,z,tool in [('Hammer_Lower',-.30,1.67,'Hammer_Handle'),('Hammer_Upper',-.30,1.85,'Hammer_Handle'),('Spanner_Lower',.06,1.64,'Spanner_OpenJaw'),('Spanner_Upper',.06,1.80,'Spanner_OpenJaw'),('Screwdriver',.34,1.69,'Screwdriver_Handle')]:
 mount='ToolMount_'+label
 joint(mount,'Toolboard',[(x+dx,.945,z+dz) for dx,dz in [(-.008,-.006),(.008,-.006),(0,.006)]])
 joint(mount,tool,[(x+dx,.895,z+dz) for dx,dz in [(-.008,-.006),(.008,-.006),(0,.006)]])
# Every mesh must have a genuine support path to the deck, not just name/bounds adjacency.
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={'Deck_WorkArea'};todo=list(seen)
while todo:
 for other in adj[todo.pop()]-seen:seen.add(other);todo.append(other)
assert seen==set(adj),('Unsupported components',set(adj)-seen)
def first_ray(origin,direction,distance):
 hits=[]
 for name,tree in trees.items():
  p,n,_,d=tree.ray_cast(Vector(origin),Vector(direction),distance)
  if p is not None:hits.append((d,name,p,n))
 return min(hits,key=lambda h:h[0]) if hits else None
# Full assembly rays establish open-front compartment mouths and their actual depth.
storage_rays=[]
for x in [-.34,-.20,.20,.34]:
 for z in [.98,1.10,1.18]:
  h=first_ray((x,-1.20,z),(0,1,0),2.5)
  assert h and h[1]=='Storage_Back' and abs(h[2].y-.885)<1e-6,(x,z,h)
  storage_rays.append({'origin_m':[x,-1.20,z],'first_hit':h[1],'point_m':list(h[2])})
work_rays=[]
for x in [-.45,0,.45]:
 for y in [-.85,-.45,0,.25]:
  h=first_ray((x,y,2.50),(0,0,-1),3)
  assert h and h[1]=='Deck_WorkArea' and abs(h[2].z-.65)<1e-6,(x,y,h)
  work_rays.append({'xy_m':[x,y],'top_z_m':h[2].z})
top_rays=[]
for x in [-.4,0,.4]:
 for y in [.48,.65,.82]:
  h=first_ray((x,y,2.5),(0,0,-1),3)
  assert h and h[1]=='Bench_Worktop' and abs(h[2].z-1.515)<1e-6,(x,y,h)
  top_rays.append({'xy_m':[x,y],'top_z_m':h[2].z})
# The open spanner jaw is genuine geometry; the board remains behind it.
sp=trees['Spanner_OpenJaw'];assert sp.ray_cast(Vector((.06,.7,1.94)),Vector((0,1,0)),.3)[0] is None
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_deck':sorted(seen),
 'open_storage_full_assembly_first_hit_rays':storage_rays,'unobstructed_forward_work_deck_down_rays':work_rays,
 'clear_fixed_worktop_down_rays':top_rays,'open_spanner_jaw_real_void':True,'finite_tread_supports':supports,
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
 d={'id':ASSET,'version':VERSION,'category':'vehicles','assetKind':'prop','theme':'railway','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,1.03));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.50;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-6,4.5),'gray-back3q':(-4,5,4.5)} if gray else {
 'thumbnail':(4,-6,4.5),'qa-front':(0,-6,1.03),'qa-side':(6,0,1.03),'qa-top':(0,0,7),
 'qa-back':(0,6,1.03),'qa-wireframe':(4,-6,4.5)}
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
 for name,pos in [('silhouette-128-front',(0,-6,1.03)),('silhouette-128-side',(6,0,1.03))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
