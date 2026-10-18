"""Original continuous-belt treadmill appearance. One static prop, metres/Z up/front -Y.
Original closed thick running loop, support deck, fixed end rollers and external frame.
No reused rowing seat or logistics roller-table geometry. No operating/safety claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fitness-continuous-belt-treadmill-01';VERSION='1.0.0';TITLE='Continuous Belt Treadmill'
DESCRIPTION=('One original static low-poly treadmill appearance with a real full-width closed thick belt. The single connected hollow belt solid has two long straight spans and two curved return ends, a distinct internal deck, two fixed end rollers, continuous axles and four external bearing blocks. '
 'Separate side frames, independent raised step strips, four finite ground feet, a front motor-style cover, two upright posts, two cantilever handrails and a tilted plain control console make a complete supported standing-machine silhouette. The console has a blank screen and three unmarked controls. '
 'All parts are named editable closed solids. Six constant opaque PBR materials, no image or procedural textures, logos, displayed speed, people, extra equipment or scene. Metres, native Z up, front -Y. Origin at the ground on the X midline halfway between the belt end-roller axes. '
 'Fixed stylized visual only: geometric contacts, clear volumes and one display pose do not establish walking/running motion, continuous transmission, motor or electrical operation, speed/incline control, exercise benefit, human fit, load capacity, manufacturing or fitness-equipment safety certification.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={};SEAM_PROBES=[]
PALETTE=[('Frame_Graphite',(.070,.092,.102,1),.40,.48),('Cover_DeepTeal',(.035,.27,.29,1),.38,.28),('Belt_Charcoal',(.028,.034,.036,1),.84,0),('Metal_Satin',(.46,.55,.58,1),.32,.70),('Control_Amber',(.91,.34,.055,1),.48,.08),('Screen_DarkSlate',(.035,.083,.11,1),.29,.05)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'operating_or_equipment_safety_claim':False}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 vs=[transform((a*size[0]/2,b*size[1]/2,d*size[2]/2),c,u,v,w) for d in [-1,1] for b in [-1,1] for a in [-1,1]]
 return mesh(name,vs,BOX_FACES,mat,role)
def chamfer_box(name,c,width,length,height,chamfer,mat,role):
 p=[(-width/2+chamfer,-length/2),(width/2-chamfer,-length/2),(width/2,-length/2+chamfer),(width/2,length/2-chamfer),(width/2-chamfer,length/2),(-width/2+chamfer,length/2),(-width/2,length/2-chamfer),(-width/2,-length/2+chamfer)]
 vs=[add(c,(x,y,z)) for z in [-height/2,height/2] for x,y in p]
 return mesh(name,vs,[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],mat,role)
def rod(name,a,b,r,mat,role,n=24):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1) if abs(w[2])<.9 else (1,0,0)));v=cross(w,u)
 vs=[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n)))) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,role)
def beam(name,a,b,width,depth,mat,role):
 v=unit(sub(b,a));u=(1,0,0);w=cross(u,v)
 return box(name,mul(add(a,b),.5),(width,math.sqrt(dot(sub(b,a),sub(b,a))),depth),mat,role,u,v,w)
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void(name,lo,hi,role):
 vs=[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
 VOID_VOLUMES[name]={'vertices':vs,'faces':BOX_FACES,'role':role}
# One swept annular capsule extrusion. Every segment owns outer, inner and both edge faces.
# The long straight portions belong to the same connected solid as the curved returns.
NARC=24;BELT_HALF_WIDTH=.285;BELT_AXIS_Y=.740;BELT_AXIS_Z=.180;BELT_INNER_R=.065;BELT_OUTER_R=.077
path=[(-BELT_AXIS_Y,math.pi/2+math.pi*i/NARC) for i in range(NARC+1)]+[(BELT_AXIS_Y,3*math.pi/2+math.pi*i/NARC) for i in range(NARC+1)]
N=len(path);vs=[]
for x,r in [(-BELT_HALF_WIDTH,BELT_OUTER_R),(BELT_HALF_WIDTH,BELT_OUTER_R),(-BELT_HALF_WIDTH,BELT_INNER_R),(BELT_HALF_WIDTH,BELT_INNER_R)]:
 vs.extend((x,cy+r*math.cos(a),BELT_AXIS_Z+r*math.sin(a)) for cy,a in path)
fs=[];BELT_SEGMENTS=[]
for i in range(N):
 j=(i+1)%N;k=len(fs)
 fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 BELT_SEGMENTS.append({'index':i,'faces':list(range(k,k+4))})
BELT=mesh('Belt_ContinuousThickClosedLoop',vs,fs,2,'one connected manifold thick running belt: two straight spans and both curved returns; genuine hollow interior')
# Four actual floor feet connect the pair of side frames to ground.
FRAMES=[];STEPS=[];POSTS=[];RAILS=[];ROLLERS=[];AXLES=[];BEARINGS=[]
for side,s in [('Left',-1),('Right',1)]:
 frame=box('Frame_'+side+'_LongSide',(s*.355,-.035,.160),(.100,1.900,.170),0,'long side frame outside the belt with real lateral clearance');FRAMES.append(frame)
 step=chamfer_box('Step_'+side+'_RaisedStrip',(s*.355,-.020,.257),.104,1.800,.032,.018,3,'independent finite raised side step with bevelled plan corners');STEPS.append(step)
 link(step,frame,(s*.355,0,.243),axis=(0,1,0),spread=.40)
 for label,y in [('Front',-.90),('Rear',.82)]:
  foot=chamfer_box('Foot_'+side+'_'+label,(s*.355,y,.040),.150,.150,.080,.015,2,'finite rubber floor foot with flat lower contact at Z=0');FEET.append(foot)
  link(foot,frame,(s*.355,y,.0775),axis=(0,1,0),spread=.025)
# The deck supports the upper band, with small deliberate finite static engagement.
DECK=box('Deck_InternalSupportPlate',(0,0,.22575),(.550,1.320,.0415),0,'actual internal support plate under upper running span; top Z=.2465, no filled box interior')
link(DECK,BELT,(0,0,.24575),axis=(0,1,0),spread=.55)
for label,y in [('Front',-.56),('Rear',.56)]:
 crossbar=box('Frame_DeckCrossbar_'+label,(0,y,.193),(.650,.070,.040),0,'crossbar below deck, clear of lower return span')
 link(crossbar,DECK,(0,y,.209),spread=.15)
 for side,s in [('Left',-1),('Right',1)]:link(crossbar,'Frame_'+side+'_LongSide',(s*.315,y,.193),axis=(0,1,0),spread=.01)
# Fixed end rollers engage the belt's inner return arcs; no dynamic rotation is claimed.
for label,y in [('Front',-.740),('Rear',.740)]:
 roller=rod('Roller_'+label+'_FixedEnd',(-.273,y,.180),(.273,y,.180),.0665,0,'fixed closed end roller: slight finite seating in inner belt return, no motion simulation',48);ROLLERS.append(roller)
 sign=-1 if label=='Front' else 1
 link(roller,BELT,(0,y+sign*.06575,.180),spread=.16)
 axle=rod('Axle_'+label+'_Continuous',(-.370,y,.180),(.370,y,.180),.012,3,'single transverse axle through roller and two external bearing blocks',20);AXLES.append(axle)
 link(axle,roller,(0,y,.180),spread=.18)
 for side,s in [('Left',-1),('Right',1)]:
  bearing=box('Bearing_'+label+'_'+side,(s*.325,y,.180),(.080,.056,.056),3,'finite external axle-bearing block extending into side frame, clear of belt shell');BEARINGS.append(bearing)
  link(bearing,axle,(s*.325,y,.180),axis=(0,1,0),spread=.004)
  link(bearing,'Frame_'+side+'_LongSide',(s*.325,y,.195),axis=(0,1,0),spread=.010)
  # Axle physically enters the same side frame beyond bearing; register that finite overlap too.
  link(axle,'Frame_'+side+'_LongSide',(s*.350,y,.180),axis=(0,1,0),spread=.004)
# The front cover remains outside the curved return, on a dedicated transverse base.
BASE=box('Frame_FrontCoverCrossbar',(0,-.970,.175),(.710,.100,.110),0,'transverse front bar entering both side frames')
for side,s in [('Left',-1),('Right',1)]:link(BASE,'Frame_'+side+'_LongSide',(s*.325,-.955,.175),axis=(0,0,1),spread=.025)
COVER=chamfer_box('Cover_FrontMotorStyle',(0,-1.005,.260),.590,.320,.130,.045,1,'simple chamfer-corner motor-style cover outside the belt; no motor or electrical specification')
link(COVER,BASE,(0,-.970,.215),spread=.20)
# Uprights and open handrails rise outside the running surface. One fixed pose only.
for side,s in [('Left',-1),('Right',1)]:
 post=beam('Post_'+side+'_Inclined',(s*.355,-.920,.205),(s*.355,-.760,1.165),.065,.070,1,'finite inclined upright rooted directly in corresponding side frame');POSTS.append(post)
 link(post,'Frame_'+side+'_LongSide',(s*.355,-.915,.225),axis=(1,0,0),spread=.013)
 link(post,BASE,(s*.340,-.935,.215),axis=(0,0,1),spread=.004)
 # Post overlaps its side step near its root, a registered finite contact.
 link(post,'Step_'+side+'_RaisedStrip',(s*.355,-.911,.257),axis=(1,0,0),spread=.013)
 rail=rod('Handrail_'+side+'_OpenCantilever',(s*.355,-.770,1.110),(s*.355,.240,1.025),.025,0,'continuous sloped handrail with finite front seat in upright and open unsupported free end',24);RAILS.append(rail)
 link(rail,post,(s*.355,-.766,1.110),axis=(1,0,0),spread=.010)
 grip=rod('Grip_'+side+'_RearSleeve',(s*.355,.030,1.04267),(s*.355,.242,1.02483),.030,2,'thick rear sleeve finitely covering cantilever handrail, separate editable solid',24)
 link(grip,rail,(s*.355,.150,1.0326),axis=(1,0,0),spread=.010)
CONSOLE_BAR=rod('Console_SupportCrossbar',(-.385,-.765,1.145),(.385,-.765,1.145),.029,0,'console support tube joining both upright heads',24)
for side,s in [('Left',-1),('Right',1)]:link(CONSOLE_BAR,'Post_'+side+'_Inclined',(s*.355,-.764,1.145),axis=(0,0,1),spread=.010)
U=(1,0,0);V=(0,math.cos(math.radians(18)),-math.sin(math.radians(18)));W=(0,math.sin(math.radians(18)),math.cos(math.radians(18)));C=(0,-.780,1.188)
CONSOLE=box('Console_TiltedBody',C,(.780,.255,.075),1,'plain inclined console body firmly seated on crossbar; no brand or live values',U,V,W)
link(CONSOLE,CONSOLE_BAR,(0,-.765,1.154),spread=.20)
for side,s in [('Left',-1),('Right',1)]:link(CONSOLE,'Post_'+side+'_Inclined',(s*.355,-.760,1.160),axis=(1,0,0),spread=.008)
for side,s in [('Left',-1),('Right',1)]:
 link('Handrail_'+side+'_OpenCantilever',CONSOLE_BAR,(s*.355,-.750,1.125),axis=(1,0,0),spread=.007)
 link('Handrail_'+side+'_OpenCantilever',CONSOLE,(s*.355,-.690,1.125),axis=(1,0,0),spread=.007)
SCREEN=box('Console_BlankScreen',transform((0,-.030,.040),C,U,V,W),(.325,.125,.010),5,'small blank dark screen seated into console, not a texture or readable value',U,V,W)
link(SCREEN,CONSOLE,transform((0,-.030,.036),C,U,V,W),spread=.10)
for i,x in enumerate([-.085,0,.085]):
 a=transform((x,.081,.032),C,U,V,W);b=transform((x,.081,.051),C,U,V,W)
 button=rod('Control_'+str(i+1)+'_Unmarked',a,b,.018,4,'plain small raised control without brand, label, value or function claim',20)
 link(button,CONSOLE,transform((x,.081,.035),C,U,V,W),axis=U,spread=.005)
# Actual finite empty spaces, not centreline rays alone.
void('AboveRunningSurface',(-.265,-.575,.280),(.265,.670,1.550),'finite unoccupied volume over exposed running span; no human-fit statement')
void('InsideLowerBeltReturn',(-.245,-.450,.123),(.245,.450,.168),'true internal air between lower return and deck supports; rejects a filled belt')
for side,s in [('Left',-1),('Right',1)]:
 xa,xb=sorted((s*.288,s*.301));void('BeltToFixedSide_'+side,(xa,-.680,.239),(xb,.680,.266),'finite lateral air beside upper running band')
 void('LowerBeltToFixedSide_'+side,(xa,-.680,.095),(xb,.680,.122),'finite lateral air beside lower return band')
void('FrontBeltToCover',(-.260,-.840,.130),(.260,-.821,.290),'finite end clearance between curved front belt and motor-style cover')
# Thickness probes start within hollow interior, hit shell inner then outer surface.
for label,p,d,thick in [('Upper',(0,0,.235),(0,0,1),.011),('Lower',(0,0,.125),(0,0,-1),.011),('Front',(0,-.740,.180),(0,-1,0),.011),('Rear',(0,.740,.180),(0,1,0),.011)]:
 WALL_PROBES.append({'mesh':BELT,'label':label,'origin_m':p,'direction':d,'length_m':.15,'minimum_wall_thickness_m':thick})
TREADMILL_CONTRACT={'single_prop_count':1,'belt_mesh':BELT,'belt_segments':BELT_SEGMENTS,'belt_contour_points':N,'belt_inner_radius_m':BELT_INNER_R,'belt_outer_radius_m':BELT_OUTER_R,'belt_half_width_m':BELT_HALF_WIDTH,'belt_axis_y_m':BELT_AXIS_Y,'belt_axis_z_m':BELT_AXIS_Z,'deck_mesh':DECK,'roller_meshes':ROLLERS,'axle_meshes':AXLES,'bearing_meshes':BEARINGS,'frame_meshes':FRAMES,'step_meshes':STEPS,'upright_meshes':POSTS,'handrail_meshes':RAILS,'console_mesh':CONSOLE,'ground_meshes':FEET,'static_pose_only':True,'motion_power_load_human_fit_or_safety_claim':False}
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
root=bpy.data.objects.new('OneOriginalContinuousBeltTreadmill',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground X midline halfway between belt end-roller axes';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
seam_checks=[]
for r in SEAM_PROBES:
 o=byname[r['mesh']];cx,cy=r['local_center_xy']
 def radius(k):p=o.data.vertices[k].co;return math.hypot(p.x-cx,p.y-cy)
 depth=(radius(r['left_bank_vertex'])+radius(r['right_bank_vertex']))/2-radius(r['centre_vertex'])
 assert depth>r['minimum_radial_indent_m'],('Actual seam is not recessed',r,depth)
 seam_checks.append(dict(r,actual_vertex_radial_indent_m=depth))
treadmill_evidence=dict(TREADMILL_CONTRACT,finite_empty_volume_checks=void_volume_checks,actual_shell_thickness_checks=wall_checks,material_contract=MATERIAL_CONTRACT,actual_recessed_seam_checks=seam_checks)
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
 'single_prop_count':1,'treadmill_geometry':treadmill_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fitness/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.105,.63));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-back-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3.6,4.7,3.0),'gray-back3q':(-3.6,-4.7,3.0)} if gray else {
 'thumbnail':(3.6,4.7,3.0),'qa-front':(0,-12,1.8),'qa-side':(12,-.105,1.8),'qa-top':(0,-.105,5),
 'qa-back':(0,12,1.8),'qa-wireframe':(3.6,4.7,3.0)}
if '--gray-back-only' in sys.argv:views={'gray-back3q':views['gray-back3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.65
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00414;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-back-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-12,1.8)),('silhouette-128-side',(12,-.105,1.8))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
