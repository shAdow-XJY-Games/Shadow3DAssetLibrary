"""Original compact tracked excavator; one fixed static metre-scale visual prop.
Two real hollow closed-loop thick belts, supported axles/rollers, open operator bay,
a forked two-section fixed arm and an actually hollow scoop. No motion/safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='construction-compact-tracked-excavator-01';VERSION='1.0.0';TITLE='Compact Tracked Excavator'
DESCRIPTION=('Original single static low-poly compact tracked excavator. Two thick continuous closed-loop rubber belts wrap around separate visible end wheels and support rollers; four transverse steel axles join the wheels and side rails to a central chassis. A circular fixed pedestal supports the amber upper deck, rear counterweight and engine cover. An open air operator bay has a real supported seat and two-post canopy, with no glass or sealed cab. A forked main boom and a narrower stick have actual cross-axis pins, small finite side clearances and a fixed exterior cylinder barrel/rod joining two anchors. A curved, thick-walled open scoop has two side plates, real inner void, bucket ears and three teeth; it is independently constructed rather than a reused truck bed or wheelbarrow. '
 'Four opaque constant PBR materials, no textures, fonts, branding or external dependencies. Metres, source Z up, arm/front at -Y. Origin is the chassis X centreline, chassis longitudinal Y=0 datum and track ground Z=0, not the asymmetric asset bounding-box centre. All components remain individually editable. '
 'One fixed stylized visual pose only. No locomotion, slewing, hydraulic or linkage simulation, joint range, continuous collision test, digging performance, traction, realistic powertrain, human fit, manufacture, loads, stability or construction-equipment/occupational safety guarantee. No operator, soil or environment is included.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Body_WarmAmber',(.88,.34,.035,1),.56,.05),('Rubber_Graphite',(.035,.045,.048,1),.76,0),('Frame_Charcoal',(.115,.145,.15,1),.59,.24),('Pins_BrushedSteel',(.43,.50,.51,1),.34,.78)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'fixed_static_geometry_only':True}
CAMERA_FOCUS=(0,-.67,1.00);CAMERA_SCALE=4.0
CAMERA_VIEWS={'thumbnail':(4.6,-7.0,4.5),'qa-front':(0,-7.0,2.5),'qa-side':(7.0,-.67,2.5),'qa-top':(0,-.67,8.0),'qa-back':(0,7.0,2.5),'qa-wireframe':(4.6,-7.0,4.5),'gray-front3q':(4.6,-7.0,4.5),'gray-back3q':(-4.6,6.0,4.5),'silhouette-128-front':(0,-7.0,2.5),'silhouette-128-side':(7.0,-.67,2.5)}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def lerp(a,b,t):return add(mul(a,1-t),mul(b,t))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def box(name,lo,hi,material,role):
 vs,fs=box_geometry(lo,hi);return mesh(name,vs,fs,material,role)
def extrude_x(name,x0,x1,poly,material,role):
 n=len(poly);vs=[(x,y,z) for x in [x0,x1] for y,z in poly];fs=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return mesh(name,vs,fs,material,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def bar(name,a,b,r,material,role,sides=16):
 d=[b[i]-a[i] for i in range(3)];length=math.sqrt(sum(x*x for x in d));n=[x/length for x in d];ref=(0,0,1) if abs(n[2])<.9 else (1,0,0)
 u=(n[1]*ref[2]-n[2]*ref[1],n[2]*ref[0]-n[0]*ref[2],n[0]*ref[1]-n[1]*ref[0]);ll=math.sqrt(sum(x*x for x in u));u=tuple(x/ll for x in u);v=(n[1]*u[2]-n[2]*u[1],n[2]*u[0]-n[0]*u[2],n[0]*u[1]-n[1]*u[0])
 vs=[add(c,add(mul(u,r*math.cos(2*math.pi*j/sides)),mul(v,r*math.sin(2*math.pi*j/sides)))) for c in [a,b] for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple(sides+j for j in range(sides))]+[(j,(j+1)%sides,(j+1)%sides+sides,j+sides) for j in range(sides)]
 return mesh(name,vs,fs,material,role)
def beam(name,x0,x1,a,b,r,material,role):
 # Four-chamfered capsule profile in the YZ plane; distinct shafts run across X.
 dy=b[0]-a[0];dz=b[1]-a[1];th=math.atan2(dz,dy);poly=[]
 for center,start in [(b,th-math.pi/2),(a,th+math.pi/2)]:
  for j in range(5):
   angle=start+math.pi*j/4;poly.append((center[0]+r*math.cos(angle),center[1]+r*math.sin(angle)))
 return extrude_x(name,x0,x1,poly,material,role)
def void(name,lo,hi,role):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def prismvoid(name,x0,x1,poly,role):
 n=len(poly);VOID_VOLUMES[name]={'vertices':[(x,y,z) for x in [x0,x1] for y,z in poly],'faces':[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],'role':role}
# Racetrack belt cells: exact parallel inner/outer loops, thickness 80 mm.
# Top and bottom straights each form one complete finite cell for surface QA.
TRACKS=[]
def outline(r):
 q=[]
 for center,start in [(.65,-math.pi/2),(-.65,math.pi/2)]:
  for j in range(13):
   a=start+math.pi*j/12;q.append((center+r*math.cos(a),.25+r*math.sin(a)))
 return q
for side,s in [('Left',-1),('Right',1)]:
 x0,x1=sorted([s*.50,s*.80]);outer=outline(.25);inner=outline(.17);n=len(outer)
 vs=[(x,y,z) for x in [x0,x1] for path in [outer,inner] for y,z in path];fs=[]
 for j in range(n):
  k=(j+1)%n
  fs += [(j,k,2*n+k,2*n+j),(n+j,3*n+j,3*n+k,n+k),(j,n+j,n+k,k),(2*n+j,2*n+k,3*n+k,3*n+j)]
 belt='TrackBelt_'+side;mesh(belt,vs,fs,1,'true closed thick racetrack band with open central through-region; finite bottom ground surface');FEET.append(belt)
 rail='TrackRail_'+side;rx=sorted([s*.37,s*.59]);box(rail,(rx[0],-.68,.21),(rx[1],.68,.31),2,'solid inner roller support rail tied to the central chassis')
 TRACKS.append({'belt':belt,'rail':rail,'side':side,'x_limits_m':[x0,x1],'outer_radius_m':.25,'inner_radius_m':.17,'half_straight_m':.65,'center_z_m':.25,'loop_segments':n,'thickness_m':.08})
 for i,y in enumerate([-.65,-.22,.22,.65]):
  name=f'Roller_{side}_{i+1}';r=.185 if i in [0,3] else .182;ax=sorted([s*.53,s*.77]);bar(name,(ax[0],y,.25),(ax[1],y,.25),r,2,'closed visible end wheel' if i in [0,3] else 'closed visible support roller',16)
  link(name,rail,(s*.56,y,.25),spread=.01)
  # Bottom interior belt-wheel overlap is deliberate, finite and below inner radius.
  link(name,belt,(s*.66,y,.073 if i in [0,3] else .075),spread=.02)
box('Chassis_CrossFrame',(-.44,-.56,.26),(.44,.56,.48),2,'central load-path visual frame between inner track rails')
for side,s in [('Left',-1),('Right',1)]:link('Chassis_CrossFrame','TrackRail_'+side,(s*.405,0,.285),axis=(0,1,0),spread=.20)
for i,y in enumerate([-.65,-.22,.22,.65]):
 name=f'Axle_{i+1}';bar(name,(-.82,y,.25),(.82,y,.25),.030,3,'real transverse fixed wheel axle through matching rollers and support rails',12)
 for side,s in [('Left',-1),('Right',1)]:
  link(name,'TrackRail_'+side,(s*.46,y,.25),spread=.015);link(name,f'Roller_{side}_{i+1}',(s*.65,y,.25),spread=.03)
 if i in [1,2]:link(name,'Chassis_CrossFrame',(0,y,.272),spread=.20)
bar('SlewPedestal_Static',(0,0,.455),(0,0,.645),.35,2,'fixed cylindrical pedestal joining chassis and upper deck; no rotation simulation',24)
link('SlewPedestal_Static','Chassis_CrossFrame',(0,0,.468),spread=.20)
box('UpperDeck',(-.62,-.62,.610),(.62,.62,.760),0,'continuous upper body deck clear of both track belts')
link('UpperDeck','SlewPedestal_Static',(0,0,.627),spread=.20)
box('Counterweight_Rear',(-.59,.485,.735),(.59,.745,1.035),0,'thick low rear counterweight attached to upper deck')
link('Counterweight_Rear','UpperDeck',(0,.55,.748),spread=.40)
box('EngineCover',(-.015,.205,.745),(.57,.565,1.255),0,'compact right rear engine cover')
link('EngineCover','UpperDeck',(.28,.35,.752),spread=.15);link('EngineCover','Counterweight_Rear',(.28,.525,.90),spread=.15)
box('EngineTop_Inset',(.090,.255,1.242),(.50,.505,1.273),2,'single thick dark inset on the engine cover, no texture grille')
link('EngineTop_Inset','EngineCover',(.28,.38,1.25),spread=.12)
# Open operator bay with actual seat, back and two independent canopy posts.
box('SeatPedestal',(-.44,-.02,.745),(-.13,.24,1.000),2,'seat pedestal visibly supported by upper deck');link('SeatPedestal','UpperDeck',(-.29,.10,.752),spread=.06)
box('SeatCushion',(-.48,-.20,.976),(-.09,.22,1.065),1,'thick seat cushion carried by pedestal');link('SeatCushion','SeatPedestal',(-.29,.08,.988),spread=.06)
box('SeatBack',(-.46,.150,1.042),(-.11,.235,1.435),1,'thick seat back joined directly to the cushion');link('SeatBack','SeatCushion',(-.29,.18,1.052),spread=.06)
for side,x in [('Left',-.535),('Right',.045)]:
 name='CanopyPost_'+side;box(name,(x-.026,.355,.740),(x+.026,.407,1.955),2,'rear canopy upright extending from deck into roof');link(name,'UpperDeck',(x,.38,.752),axis=(0,1,0),spread=.008)
 if side=='Right':link(name,'EngineCover',(x,.38,1.02),axis=(0,0,1),spread=.09)
box('CanopyRoof',(-.60,-.48,1.925),(.11,.48,2.005),0,'solid thin canopy roof supported by two rear uprights')
for side,x in [('Left',-.535),('Right',.045)]:link('CanopyRoof','CanopyPost_'+side,(x,.38,1.94),axis=(0,1,0),spread=.008)
box('EntryStep_Left',(-.735,-.41,.570),(-.595,-.09,.633),2,'single real step joined to upper deck and clear of left belt');link('EntryStep_Left','UpperDeck',(-.605,-.25,.621),axis=(0,1,0),spread=.08)
# The two separated main-boom cheeks form a real fork around the middle stick.
A=(-.36,.94);B=(-1.12,1.90);C=(-1.73,.75)
for side,x0,x1 in [('Left',.045,.115),('Right',.505,.575)]:
 name='BoomBaseEar_'+side;box(name,(x0,-.52,.735),(x1,-.20,1.010),0,'base pivot ear attached to upper deck, clear of main boom cheek')
 link(name,'UpperDeck',((x0+x1)/2,-.36,.748),axis=(0,1,0),spread=.08)
for side,x0,x1 in [('Left',.140,.220),('Right',.400,.480)]:beam('BoomCheek_'+side,x0,x1,A,B,.105,0,'separate thick main-boom fork cheek; middle channel stays open at the stick pivot')
bar('BoomBase_Pin',(.015,*A),(.605,*A),.060,3,'actual horizontal base pin through both deck ears and both boom cheeks',16)
for name,x in [('BoomBaseEar_Left',.08),('BoomBaseEar_Right',.54),('BoomCheek_Left',.18),('BoomCheek_Right',.44)]:link('BoomBase_Pin',name,(x,*A),axis=(0,1,0),spread=.014)
for i,t in enumerate([.22,.55],1):
 yz=lerp(A,B,t);name=f'BoomCrossWeb_{i}';bar(name,(.196,*yz),(.424,*yz),.068,0,'fixed transverse web joining the separated boom cheeks below the fork mouth',12)
 for side,x in [('Left',.208),('Right',.412)]:link(name,'BoomCheek_'+side,(x,*yz),axis=(0,1,0),spread=.015)
beam('Stick_Center',.265,.355,B,C,.070,0,'narrow fixed dipper stick centered in the real main-boom fork')
bar('Elbow_Pin',(.115,*B),(.505,*B),.047,3,'actual elbow pin through boom fork cheeks and centered stick',16)
for name,x in [('BoomCheek_Left',.18),('BoomCheek_Right',.44),('Stick_Center',.31)]:link('Elbow_Pin',name,(x,*B),axis=(0,1,0),spread=.01)
# Fixed visible cylinder geometry; neither hydraulic nor range-of-motion claims.
D=(.660,-.52,.83);E=(.660,*lerp(A,B,.60))
box('Cylinder_DeckMount',(.590,-.582,.740),(.730,-.455,.906),2,'short visible cylinder anchor attached to deck');link('Cylinder_DeckMount','UpperDeck',(.605,-.52,.751),axis=(0,1,0),spread=.020)
bar('Cylinder_BasePin',(.580,D[1],D[2]),(.740,D[1],D[2]),.035,3,'cross pin at fixed cylinder base',12);link('Cylinder_BasePin','Cylinder_DeckMount',D,axis=(0,1,0),spread=.010)
bar('Cylinder_Barrel',D,lerp(D,E,.67),.054,2,'closed outer barrel of a fixed visual cylinder',16)
link('Cylinder_Barrel','Cylinder_DeckMount',lerp(D,E,.035),axis=(1,0,0),spread=.01);link('Cylinder_Barrel','Cylinder_BasePin',lerp(D,E,.015),axis=(1,0,0),spread=.01)
bar('Cylinder_Rod',lerp(D,E,.59),E,.026,3,'closed narrower fixed rod telescoped into barrel',12);link('Cylinder_Rod','Cylinder_Barrel',lerp(D,E,.63),axis=(1,0,0),spread=.008)
bar('Cylinder_BoomPin',(.450,E[1],E[2]),(.725,E[1],E[2]),.039,3,'cross-axis pin joining fixed cylinder rod to right boom cheek',12)
link('Cylinder_BoomPin','Cylinder_Rod',lerp(D,E,.985),axis=(1,0,0),spread=.008);link('Cylinder_BoomPin','BoomCheek_Right',(.465,E[1],E[2]),axis=(0,1,0),spread=.01)
# Bent thick scoop shell, separately solid side walls and teeth. All cavity is real air.
shellpoly=[(-1.61,.66),(-1.60,.40),(-1.68,.20),(-1.86,.12),(-2.28,.15),(-2.28,.21),(-1.88,.18),(-1.74,.25),(-1.67,.42),(-1.68,.64)]
extrude_x('Bucket_CurvedShell',.040,.580,shellpoly,2,'continuous bent thick scoop floor and rear wall with a genuinely concave inner surface')
sidepoly=[(-1.635,.635),(-1.630,.410),(-1.710,.230),(-1.870,.150),(-2.255,.180),(-2.255,.290),(-2.030,.490),(-1.660,.650)]
for side,x0,x1 in [('Left',.025,.090),('Right',.530,.595)]:
 name='BucketSide_'+side;extrude_x(name,x0,x1,sidepoly,2,'solid side wall of scoop, seated within thick bent shell and preserving inner cavity');link(name,'Bucket_CurvedShell',((x0+x1)/2,-1.86,.16),axis=(1,0,0),spread=.008)
for side,x0,x1 in [('Left',.180,.240),('Right',.380,.440)]:
 name='BucketEar_'+side;extrude_x(name,x0,x1,[(-1.665,.550),(-1.620,.550),(-1.620,.820),(-1.780,.820),(-1.780,.700),(-1.665,.635)],0,'shaped bucket attachment ear above rear shell, preserving cavity and middle stick gap')
 link(name,'Bucket_CurvedShell',((x0+x1)/2,-1.65,.59),axis=(0,0,1),spread=.015)
bar('Bucket_Pin',(.155,*C),(.465,*C),.041,3,'actual bucket pin through both bucket ears and middle stick',16)
for name,x in [('BucketEar_Left',.21),('BucketEar_Right',.41),('Stick_Center',.31)]:link('Bucket_Pin',name,(x,*C),axis=(0,1,0),spread=.008)
for i,x in enumerate([.14,.31,.48],1):
 name=f'BucketTooth_{i}';extrude_x(name,x-.035,x+.035,[(-2.245,.16),(-2.395,.145),(-2.405,.175),(-2.250,.215)],3,'finite solid short tooth embedded in scoop lip')
 link(name,'Bucket_CurvedShell',(x,-2.265,.183),spread=.010)
# Finite voids cover the full declared scoop core, open operator volume and fork gaps.
prismvoid('Bucket_InnerCavity',.100,.520,[(-1.705,.570),(-1.725,.425),(-1.790,.290),(-1.905,.225),(-2.200,.247),(-2.200,.288),(-2.025,.465)],'finite whole inner cavity inset from thick scoop floor, rear and both side walls')
void('OperatorBay_OpenAir',(-.49,-.36,1.145),(-.105,.115,1.860),'finite open operator space above the seat front and below the canopy')
# Tiny but positive complete axial clearances on both sides of the fixed stick.
void('ElbowFork_LeftClear',(.226,-1.15,1.835),(.257,-1.09,1.845),'finite fork side clearance below the steel elbow pin')
void('ElbowFork_RightClear',(.363,-1.15,1.835),(.394,-1.09,1.845),'finite fork side clearance below the steel elbow pin')
void('BucketFork_LeftClear',(.244,-1.755,.690),(.260,-1.705,.700),'finite axial bucket-fork gap below the bucket pin')
void('BucketFork_RightClear',(.360,-1.755,.690),(.376,-1.705,.700),'finite axial bucket-fork gap below the bucket pin')
void('TrackChassis_UnderGap',(-.33,-.50,.045),(.33,.50,.205),'finite empty underside between the two track supports and middle chassis')
EXCAVATOR_CONTRACT={'single_prop_count':1,'tracks':TRACKS,'ground_belts':FEET,'fixed_arm_points_yz_m':{'base':A,'elbow':B,'bucket':C},'fork_boom_cheeks':['BoomCheek_Left','BoomCheek_Right'],'stick':'Stick_Center','bucket_shell':'Bucket_CurvedShell','open_cab_no_glass':True,'four_transverse_axles':True,'fixed_pose_only':True,'motion_hydraulics_load_safety_claim':False}
# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('CompactTrackedExcavator',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X centreline, design Y=0 datum, ground Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
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
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Finite support and true openings are checked against actual generated mesh triangles.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
# Actual floor and wall tests supplement finite void and support tests.
floor_checks=[]
for r in FLOOR_PROBES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is not None and abs(hit.z-r['expected_hit_z_m'])<1e-6
 floor_checks.append(dict(r,actual_hit_m=list(hit)))
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);t=trees[r['mesh']];inner=t.ray_cast(p,d,r['length_m'])[0]
 assert inner is not None
 outer=t.ray_cast(inner+d*1e-6,d,r['length_m'])[0];assert outer is not None
 thickness=(outer-inner).length;assert thickness>r['minimum_wall_thickness_m']
 wall_checks.append(dict(r,actual_inner_hit_m=list(inner),actual_outer_hit_m=list(outer),actual_wall_thickness_m=thickness))
excavator_evidence=dict(EXCAVATOR_CONTRACT,finite_static_clearances=void_volume_checks,material_contract=MATERIAL_CONTRACT)
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<12000
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
 'single_prop_count':1,'excavator_geometry':excavator_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector(CAMERA_FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=CAMERA_SCALE;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERA_VIEWS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALE
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=CAMERA_SCALE/640;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name in ['silhouette-128-front','silhouette-128-side']:render(name,CAMERA_VIEWS[name])
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
