"""Original open-top static pinball machine, metre scale, Z up, player at -Y.
Real sloped playfield, separate launcher lane, fixed flippers and bumpers, four legs.
No playable physics, scores, input, electrical function, manufacture or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='arcade-open-playfield-pinball-01';VERSION='1.0.0';TITLE='Open-Playfield Pinball Machine'
DESCRIPTION=('Original single static low-poly pinball machine with an open-top inclined physical playfield. A deep tapered teal cabinet stands on four individually supported steel legs and dark foot pads. The right-side launch channel has its own raised divider, a seated faceted metal ball and a front fixed pull handle. The playing area contains two fixed tapered flipper paddles on real pivots, three stepped pop bumpers, two slingshot guides and three rear target blades, all joined to the sloped floor with actual support. A tall framed backbox carries a plain ivory face and raised original geometric medallion; it is an opaque solid sign with no image screen or runtime-display claim. '
 'Visible empty finite launch-lane, central-ball and lower drain-approach volumes distinguish the physical ball layout from a screen cabinet or flat tabletop. Cabinet rails, target brackets and coin-door relief are solid thickness, not texture overlays. Five fully opaque untextured constant PBR materials. Metres, source Z up, player at -Y, origin at the X centreline, design Y=0 datum and ground Z=0. '
 'One fixed stylized visual prop only: no playable pinball, ball simulation, scoring, input devices, electronics, moving parts, physics, mechanisms hidden under the playfield, fit, manufacture, load-bearing or amusement-equipment safety guarantee. No real branding, game imagery, fonts, textures, external dependencies or scene.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Cabinet_DeepTeal',(.025,.255,.27,1),.52,.08),('Playfield_WarmIvory',(.78,.69,.46,1),.62,0),('Mechanisms_Tangerine',(.82,.145,.025,1),.48,0),('Rubber_DeepGraphite',(.025,.037,.038,1),.68,0),('Fittings_BrushedSteel',(.41,.49,.48,1),.34,.75)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'image_or_runtime_screen':False,'geometry_only_mechanisms':True}
SLOPE=.115
# A local playfield height h is transformed by a shear into a real sloped surface.
def P(x,y,h=0):return (x,y,.94+SLOPE*(y+.72)+h)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def box(name,lo,hi,material,role):
 vs,fs=box_geometry(lo,hi);return mesh(name,vs,fs,material,role)
def slab(name,poly,low,high,material,role):
 n=len(poly);vs=[P(x,y,h) for h in [low,high] for x,y in poly];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role)
def rect(x0,x1,y0,y1):return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
def roundrect(x0,x1,y0,y1,r):return [(x0+r,y0),(x1-r,y0),(x1,y0+r),(x1,y1-r),(x1-r,y1),(x0+r,y1),(x0,y1-r),(x0,y0+r)]
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def joinfloor(name,x,y,h=-.003):link(name,'Playfield_SlopedFloor',P(x,y,h))
def profile(name,x,y,rings,material,role,sides=16):
 vs=[P(x+r*math.cos(2*math.pi*j/sides),y+r*math.sin(2*math.pi*j/sides),h) for h,r in rings for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+j for j in range(sides))]
 for i in range(len(rings)-1):
  for j in range(sides):k=(j+1)%sides;fs.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
 return mesh(name,vs,fs,material,role)
def bar(name,a,b,r,material,role,sides=12):
 d=[b[i]-a[i] for i in range(3)];length=math.sqrt(sum(x*x for x in d));n=[x/length for x in d];ref=(0,0,1) if abs(n[2])<.9 else (1,0,0)
 u=(n[1]*ref[2]-n[2]*ref[1],n[2]*ref[0]-n[0]*ref[2],n[0]*ref[1]-n[1]*ref[0]);ll=math.sqrt(sum(x*x for x in u));u=tuple(x/ll for x in u);v=(n[1]*u[2]-n[2]*u[1],n[2]*u[0]-n[0]*u[2],n[0]*u[1]-n[1]*u[0])
 vs=[add(c,add(mul(u,r*math.cos(2*math.pi*j/sides)),mul(v,r*math.sin(2*math.pi*j/sides)))) for c in [a,b] for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple(sides+j for j in range(sides))]+[(j,(j+1)%sides,(j+1)%sides+sides,j+sides) for j in range(sides)]
 return mesh(name,vs,fs,material,role)
def void(name,lo,hi,role,sloped=True):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':[P(*v) for v in vs] if sloped else vs,'faces':fs,'role':role}
# Grounded four-foot base; cabinet is a solid visual shell with no hidden mechanism claim.
slab('Cabinet_TaperedBody',roundrect(-.385,.385,-.735,.690,.045),-.235,-.020,0,'deep sloped continuous cabinet beneath the ball floor')
slab('Playfield_SlopedFloor',rect(-.355,.355,-.700,.640),-.035,0,1,'single solid sloped playing floor, no texture simulation')
link('Playfield_SlopedFloor','Cabinet_TaperedBody',P(0,0,-.027),spread=.15)
for label,x,y in [('FrontLeft',-.305,-.585),('FrontRight',.305,-.585),('RearLeft',-.305,.535),('RearRight',.305,.535)]:
 foot='Foot_'+label;leg='Leg_'+label;z=P(x,y,-.195)[2]
 box(foot,(x-.052,y-.050,0),(x+.052,y+.050,.045),3,'finite planar ground pad for one leg');FEET.append(foot)
 box(leg,(x-.031,y-.031,.027),(x+.031,y+.031,z),4,'independent solid steel leg embedded in cabinet underside')
 link(leg,foot,(x,y,.036),spread=.012);link(leg,'Cabinet_TaperedBody',(x,y,z-.018),spread=.012)
# Continuous perimeter trim plus a separately bounded right launch channel.
for label,x0,x1 in [('Left',-.373,-.339),('Right',.339,.373)]:
 name='SideRail_'+label;slab(name,rect(x0,x1,-.715,.665),-.0265,.055,3,'raised full-length perimeter rail with solid cabinet seating');link(name,'Cabinet_TaperedBody',P((x0+x1)/2,0,-.024))
slab('Front_Lockbar',roundrect(-.378,.378,-.746,-.655,.015),-.0285,.045,4,'rounded front crossbar physically joined to the cabinet')
link('Front_Lockbar','Cabinet_TaperedBody',P(0,-.69,-.024),spread=.22)
slab('Rear_Boundary',rect(-.360,.360,.619,.672),-.0305,.060,0,'back wall at head of the sloped ball track');link('Rear_Boundary','Cabinet_TaperedBody',P(0,.65,-.024),spread=.18)
slab('Launcher_Divider',rect(.245,.262,-.650,.500),-.008,.062,4,'raised separator makes a real right-hand ball launch channel');joinfloor('Launcher_Divider',.253,0)
# Upper guide has real thickness and joins the side channel to the playing field.
slab('Upper_ReturnGuide',[(.325,.485),(.325,.560),(.270,.614),(.170,.614),(.170,.596),(.261,.596),(.307,.550),(.307,.485)],-.008,.065,2,'bent solid guide at the open upper exit of the launch lane');joinfloor('Upper_ReturnGuide',.316,.52)
# One ball is intentionally seated a little into the sloped floor, a static display pose.
profile('Ball_SeatedStatic',.301,-.490,[(-.003,.008),(.003,.017),(.016,.023),(.029,.020),(.040,.012),(.043,.004)],4,'faceted metal ball fixed at the bottom of the launch channel')
link('Ball_SeatedStatic','Playfield_SlopedFloor',P(.301,-.490,-.0015),axis=(1,0,0),spread=.003)
# Fixed launcher shaft and thick handle. No spring or motion is implied.
bar('Launcher_Rod',P(.301,-.860,.018),P(.301,-.575,.018),.010,4,'fixed front pull shaft seated in the front crossbar')
link('Launcher_Rod','Front_Lockbar',P(.301,-.700,.018),axis=(0,1,SLOPE),spread=.012)
bar('Launcher_PullHandle',P(.301,-.900,.018),P(.301,-.840,.018),.033,3,'thick hand pull disc, fixed visual pose')
link('Launcher_PullHandle','Launcher_Rod',P(.301,-.850,.018),axis=(0,1,SLOPE),spread=.003)
# Paired fixed flippers. A real separate pivot joins each tapered paddle to the floor.
FLIPPERS=[]
for side,s in [('Left',-1),('Right',1)]:
 x=s*.185;y=-.400;post='FlipperPivot_'+side;paddle='FlipperPaddle_'+side
 profile(post,x,y,[(-.008,.021),(.049,.021)],4,'fixed flipper pivot anchored into the playing floor');joinfloor(post,x,y)
 poly=[(s*.208,-.388),(s*.202,-.420),(s*.059,-.500),(s*.041,-.493),(s*.043,-.472),(s*.169,-.381)]
 if s<0:poly.reverse()
 slab(paddle,poly,.014,.040,2,'tapered solid static flipper paddle attached to its real pivot')
 link(paddle,post,P(x,y,.027),spread=.004);FLIPPERS.append({'pivot':post,'paddle':paddle,'static':True})
 # Slingshot banks are thick triangular raised solids with clear inward ball faces.
 name='Slingshot_'+side;outer,upper,inner=(.301,.283,.182) if s<0 else (.225,.211,.146);poly=[(s*outer,-.365),(s*upper,-.125),(s*inner,-.286)]
 if s<0:poly.reverse()
 slab(name,poly,-.008,.047,3,'thick side slingshot bank sitting on the playing floor');joinfloor(name,s*(.266 if s<0 else .199),-.275)
# Three distinct stepped bumpers: each base supports a stem and broad orange cap.
BUMPERS=[]
for i,(x,y) in enumerate([(-.180,.155),(.145,.190),(-.035,.380)],1):
 base='BumperBase_%02d'%i;stem='BumperStem_%02d'%i;cap='BumperCap_%02d'%i
 profile(base,x,y,[(-.008,.047),(.017,.047),(.024,.039)],3,'wide fixed pop-bumper base seated into playfield');joinfloor(base,x,y)
 profile(stem,x,y,[(.010,.022),(.082,.022)],4,'solid bumper stem connecting base and cap');link(stem,base,P(x,y,.016),spread=.007)
 profile(cap,x,y,[(.068,.050),(.079,.058),(.101,.058),(.111,.049)],2,'broad closed top of a static pop bumper');link(cap,stem,P(x,y,.076),spread=.007)
 BUMPERS.append({'base':base,'stem':stem,'cap':cap})
# Three target blades in actual small sockets, comfortably clear of the ball return.
for i,x in enumerate([-.245,-.145,-.045],1):
 socket='TargetSocket_%02d'%i;blade='TargetBlade_%02d'%i
 slab(socket,rect(x-.030,x+.030,.510,.550),-.006,.016,3,'solid target bracket sitting in floor');joinfloor(socket,x,.530)
 slab(blade,rect(x-.020,x+.020,.522,.538),.008,.078,2,'short vertical fixed target blade, no scoring switch');link(blade,socket,P(x,.530,.012),spread=.008)
# Backbox is a supported opaque physical sign, not a simulated image screen.
box('Backbox_Riser',(-.280,.645,1.000),(.280,.710,1.250),0,'broad structural riser from cabinet into backbox')
link('Backbox_Riser','Cabinet_TaperedBody',P(0,.665,-.050),spread=.18)
box('Backbox_Housing',(-.425,.555,1.200),(.425,.720,1.825),0,'deep rectangular rear sign enclosure')
link('Backbox_Housing','Backbox_Riser',(0,.675,1.225),spread=.16)
box('Backbox_IvoryFace',(-.367,.538,1.260),(.367,.568,1.765),1,'plain opaque recessed-looking thick sign face without picture or screen')
link('Backbox_IvoryFace','Backbox_Housing',(0,.562,1.50),spread=.22)
# Raised original badge and three little geometric pips use closed mesh solids.
bar('Backbox_Medallion',(0,.523,1.545),(0,.545,1.545),.142,2,'orange 16-sided geometric emblem physically embedded into sign face',16)
link('Backbox_Medallion','Backbox_IvoryFace',(0,.542,1.545),axis=(1,0,0),spread=.035)
bar('Backbox_MedallionInset',(0,.511,1.545),(0,.528,1.545),.077,4,'solid raised inner medallion with finite attachment',12)
link('Backbox_MedallionInset','Backbox_Medallion',(0,.525,1.545),axis=(1,0,0),spread=.025)
for i,x in enumerate([-.235,0,.235],1):
 name='Backbox_Pip_%02d'%i;bar(name,(x,.522,1.333),(x,.546,1.333),.025,3,'small closed round decoration embedded in sign panel');link(name,'Backbox_IvoryFace',(x,.542,1.333),spread=.005)
# Front relief is a sealed visual coin door. No operable slot, cavity or access promise.
box('Front_CoinDoor',(-.112,-.749,.765),(.112,-.724,.902),3,'thick sealed coin-door relief on the front cabinet')
link('Front_CoinDoor','Cabinet_TaperedBody',(0,-.729,.830),spread=.050)
box('Front_CoinDoorLatch',(.062,-.760,.807),(.090,-.741,.845),4,'solid small latch block embedded in front relief')
link('Front_CoinDoorLatch','Front_CoinDoor',(.076,-.745,.826),axis=(0,0,1),spread=.006)
# Additional intentional finite seats at perimeter intersections.
for side,x in [('Left',-.347),('Right',.347)]:
 link('SideRail_'+side,'Playfield_SlopedFloor',P(x,0,-.012))
 link('SideRail_'+side,'Front_Lockbar',P(x,-.690,.020))
 link('SideRail_'+side,'Rear_Boundary',P(x,.640,.020))
link('Front_Lockbar','Playfield_SlopedFloor',P(0,-.680,-.012),spread=.18)
link('Rear_Boundary','Playfield_SlopedFloor',P(0,.630,-.012),spread=.18)
link('Backbox_Riser','Rear_Boundary',(0,.660,1.130),spread=.18)
# Actual finite sloped volumes, not a single hopeful centre ray, establish ball clearances.
void('LaunchLane_UpperClear',(.272,-.380,.008),(.333,.440,.070),'finite open volume above right launch-channel floor; wider than the displayed ball')
void('Central_BallApproach',(-.025,-.365,.008),(.025,.100,.075),'clear central approach between fixed lower mechanisms and bumper cluster')
void('Between_FlipperTips',(-.024,-.570,.008),(.024,-.455,.070),'finite space between flipper tips approaching the lower stop')
void('UnderCabinet_Clearance',(-.235,-.520,.080),(.235,.460,.650),'real empty space below the cabinet between four legs',False)
for name,x,ya,yb in [('launch_channel',.302,-.375,.435),('central_approach',0,-.360,.095)]:
 d=(0,1,SLOPE);ll=math.sqrt(1+SLOPE*SLOPE);GAPS.append({'label':name,'origin_m':list(P(x,ya,.035)),'direction':[v/ll for v in d],'length_m':(yb-ya)*ll})
PINBALL_CONTRACT={'single_prop_count':1,'legs':4,'playfield_slope_z_per_y':SLOPE,'open_top_no_transparency':True,'launch_channel_inner_width_m':.077,'ball_max_diameter_m':.046,'flippers':FLIPPERS,'bumpers':BUMPERS,'fixed_ball':'Ball_SeatedStatic','rear_sign_has_no_screen':True,'physics_or_score_logic':False}
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
root=bpy.data.objects.new('OpenPlayfieldPinballMachine',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X centreline, design Y=0 datum, ground Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
pinball_evidence=dict(PINBALL_CONTRACT,finite_ball_and_underbody_clearances=void_volume_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'pinball_geometry':pinball_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/arcade/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.04,.91));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.6;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3.5,-4.8,4.1),'gray-back3q':(-3.5,4.8,4.1)} if gray else {
 'thumbnail':(3.5,-4.8,4.1),'qa-front':(0,-5.5,1.75),'qa-side':(5.5,-.04,1.75),'qa-top':(0,-.04,6),
 'qa-back':(0,5.5,1.75),'qa-wireframe':(3.5,-4.8,4.1)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.6
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=2.6/640;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-5.5,1.75)),('silhouette-128-side',(5.5,-.04,1.75))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
