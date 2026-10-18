"""One original complete compact static acoustic drum kit; one prop.
Three truly hollow shells, thick heads, open bass port, shaped cymbal and fixed stands.
Metres, native Z up, front -Y. No sound, motion, performance, fit or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='music-compact-acoustic-drum-kit-01';VERSION='1.0.0';TITLE='Compact Acoustic Drum Kit'
DESCRIPTION=('One original static low-poly compact acoustic drum kit, counted as one prop: a horizontal bass drum with a genuinely perforated thick front head, a separate open-bottom snare drum, one open-bottom mounted tom, and one formed thick cymbal on an independent fixed tripod stand. Each drum has a real hollow thick shell, separate finite-thickness heads, two open hoops and restrained tension lugs. The snare has a fixed basket and tripod, the tom has an exterior fixed mount, and the bass has two short spurs plus a rear support foot. All components have documented finite fixed connections and ground paths. No solid cylinder substitutes for a drum cavity. Opaque constant PBR colours, no texture, animation, person, stool, stage, sticks, pedal or extra drums. Metres, native Z up, front -Y, ground-level origin. '
'Static visual geometry only. No sound, acoustic response, musical performance, tuning, membrane physics, striking, moving pedal, human fit, load capacity, stability, manufacture, installation compatibility, certification or safety claim. No compatibility with earlier music scenes is implied.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];DRUMS=[];FLOOR_PROBES=[];WALL_PROBES=[]
PALETTE=[('Shell_DeepTeal',(.025,.20,.22,1),.38,.2),('Hardware_SatinChrome',(.53,.60,.63,1),.29,.74),('Head_WarmIvory',(.81,.79,.67,1),.84,0),('Cymbal_BurnishedBrass',(.63,.36,.085,1),.33,.77),('FeetAndFelt_Charcoal',(.038,.047,.05,1),.86,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,mat,role):
 assert name not in G;G[name]={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':mat,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 return mesh(name,[transform((a*size[0]/2,b*size[1]/2,d*size[2]/2),c,u,v,w) for d in [-1,1] for b in [-1,1] for a in [-1,1]],BOX_FACES,mat,role)
def rod(name,a,b,r,mat,role,n=12):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1) if abs(w[2])<.9 else (1,0,0)));v=cross(w,u)
 vs=[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n)))) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,role)
def ring(name,c,u,v,w,rout,rin,low,high,mat,role,n=32,hole_offset=(0,0)):
 # Four actual polygon rings joined by walls and annular end faces. The hole is real.
 vs=[]
 for inner,z in [(False,low),(False,high),(True,low),(True,high)]:
  for i in range(n):
   a=math.tau*i/n;r=rin if inner else rout
   p=(r*math.cos(a)+(hole_offset[0] if inner else 0),r*math.sin(a)+(hole_offset[1] if inner else 0),z)
   vs.append(transform(p,c,u,v,w))
 fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,mat,role)
def disk(name,c,u,v,w,r,lo,hi,mat,role,n=32):return rod(name,add(c,mul(w,lo)),add(c,mul(w,hi)),r,mat,role,n)
def link(a,b,p,axis=(0,1,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def cylinder_void(name,c,u,v,w,r,lo,hi,role,n=32):
 vs=[transform((r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z),c,u,v,w) for z in [lo,hi] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def void_box(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],'faces':BOX_FACES,'role':role}
ZB=((1,0,0),(0,1,0),(0,0,1));YB=((1,0,0),(0,0,1),(0,-1,0))
# Bass axis local +Z is world -Y; local cross section X/Y is world X/Z.
BC=(0,0,.32);u,v,w=YB
bass=ring('Bass_HollowTealShell',BC,u,v,w,.284,.263,-.148,.190,0,'genuinely hollow 21 mm thick bass shell; axis -Y')
bfront=ring('Bass_ThickPortedFrontHead',BC,u,v,w,.278,.065,.195,.205,2,'10 mm thick front membrane with a real offset through-port',hole_offset=(.110,-.080))
brear=disk('Bass_ThickRearHead',BC,u,v,w,.278,-.153,-.140,2,'closed thick rear membrane')
bfh=ring('Bass_FrontOpenHoop',BC,u,v,w,.294,.269,.185,.220,1,'thick open front hoop')
brh=ring('Bass_RearOpenHoop',BC,u,v,w,.294,.269,-.175,-.135,1,'thick open rear hoop')
link(bass,bfh,(0,-.188,.596),axis=(1,0,0),spread=.003)
link(bass,brh,(0,.145,.596),axis=(1,0,0),spread=.003)
link(bfront,bfh,(0,-.200,.593),axis=(1,0,0),spread=.003)
link(brear,bass,(0,.145,.590),axis=(1,0,0),spread=.003)
link(brear,brh,(0,.145,.593),axis=(1,0,0),spread=.003)
# The front membrane reaches its hoop but is separated from the shell by 5 mm.
for k in range(6):
 a=math.tau*(k+.5)/6;r=(math.cos(a),0,math.sin(a));t=(-math.sin(a),0,math.cos(a))
 lug=box('Bass_TensionLug_%02d'%(k+1),add(add(BC,mul(r,.2945)),(0,-.025,0)),(.029,.350,.026),1,'fixed long bass tension lug; no adjustment mechanism',u=r,v=(0,1,0),w=t)
 link(lug,bass,add(BC,mul(r,.282)),axis=(0,1,0),spread=.005)
 for hoop,y in [(bfh,-.195),(brh,.145)]:link(lug,hoop,add(add(BC,mul(r,.286)),(0,y,0)),axis=t,spread=.002)
DRUMS.append({'name':'bass','shell':bass,'heads':[bfront,brear],'hoops':[bfh,brh],'axis':w,'centre_m':BC,'inner_radius_m':.263,'outer_radius_m':.284,'shell_axis_range_m':[-.148,.190],'front_port_mesh':bfront,'front_port_radius_m':.065,'front_port_offset_m':[.110,-.080]})
cylinder_void('Bass_CompleteInterior',BC,u,v,w,.257,-.136,.191,'finite complete inset bass cavity, not a ray or hollow-looking texture')
cylinder_void('Bass_ThroughFrontPort',(.110,0,.240),u,v,w,.060,.170,.235,'finite round through-port extends both sides of the entire front membrane')
BORES.append({'mesh':bfront,'origin_m':(.110,-.235,.240),'direction':(0,1,0),'length_m':.065})
GAPS.append({'label':'AssembledBassPort','origin_m':(.110,-.235,.240),'direction':(0,1,0),'length_m':.10})
for side,sgn in [('Left',-1),('Right',1)]:
 spur=rod('Bass_Spur_'+side,(sgn*.210,-.080,.140),(sgn*.350,-.135,.026),.017,1,'short fixed bass spur')
 foot=box('Bass_Foot_'+side,(sgn*.350,-.135,.018),(.085,.070,.036),4,'finite bass spur ground foot');FEET.append(foot)
 link(bass,spur,(sgn*.211,-.080,.138),axis=(0,1,0),spread=.003)
 link(spur,foot,(sgn*.345,-.133,.030),axis=(0,1,0),spread=.003)
rearfoot=box('Bass_RearGroundSupport',(0,.075,.025),(.120,.100,.050),4,'finite rear support touching lower shell');FEET.append(rearfoot)
link(bass,rearfoot,(0,.075,.043),axis=(1,0,0),spread=.018)
link('Bass_TensionLug_05',rearfoot,(0,.075,.030),axis=(0,1,0),spread=.010)
# Upright drums have a real thick top membrane and genuinely open bottom.
def upright(label,c,r,rin,zlo,zhi,mat,lugs):
 u,v,w=ZB;shell=ring(label+'_HollowShell',c,u,v,w,r,rin,zlo,zhi,mat,'real thick open-bottom drum shell')
 head=disk(label+'_ThickTopHead',c,u,v,w,r-.004,zhi-.004,zhi+.004,2,'8 mm finite thick top membrane')
 top=ring(label+'_TopOpenHoop',c,u,v,w,r+.010,r-.011,zhi-.009,zhi+.017,1,'genuinely open thick top hoop')
 bottom=ring(label+'_BottomOpenHoop',c,u,v,w,r+.010,r-.011,zlo-.010,zlo+.017,1,'genuinely open bottom hoop; no bottom fill')
 link(shell,head,add(c,(r-.010,0,zhi-.002)),axis=(0,1,0),spread=.002)
 link(shell,top,add(c,(r-.005,0,zhi-.006)),axis=(0,1,0),spread=.002)
 link(shell,bottom,add(c,(r-.005,0,zlo+.007)),axis=(0,1,0),spread=.002)
 link(head,top,add(c,(r-.007,0,zhi+.001)),axis=(0,1,0),spread=.002)
 for k in range(lugs):
  a=math.tau*(k+.5)/lugs;rdir=(math.cos(a),math.sin(a),0);tdir=(-math.sin(a),math.cos(a),0)
  lug=box(label+'_TensionLug_%02d'%(k+1),add(c,add(mul(rdir,r+.006),(0,0,(zlo+zhi)/2))),(.025,.022,zhi-zlo-.010),1,'restrained fixed lug joining shell and both hoops',u=rdir,v=tdir,w=(0,0,1))
  link(lug,shell,add(c,add(mul(rdir,r-.003),(0,0,(zlo+zhi)/2))),axis=tdir,spread=.001)
  link(lug,top,add(c,add(mul(rdir,r+.001),(0,0,zhi-.007))),axis=tdir,spread=.001)
  link(lug,bottom,add(c,add(mul(rdir,r+.001),(0,0,zlo+.012))),axis=tdir,spread=.001)
 DRUMS.append({'name':label.lower(),'shell':shell,'heads':[head],'hoops':[top,bottom],'axis':w,'centre_m':c,'inner_radius_m':rin,'outer_radius_m':r,'shell_axis_range_m':[zlo,zhi],'open_bottom':True})
 cylinder_void(label+'_CompleteInterior',c,u,v,w,rin-.006,zlo-.030,zhi-.009,'complete inset finite drum cavity, extending visibly through open bottom')
 BORES.append({'mesh':shell,'origin_m':add(c,(0,0,zlo-.035)),'direction':(0,0,1),'length_m':zhi-zlo+.07})
 return shell,head,top,bottom
snare,sh,sth,sbh=upright('Snare',(-.53,.12,0),.180,.163,.575,.705,1,4)
tom,th,tth,tbh=upright('Tom',(.12,.10,0),.155,.140,.790,1.010,0,4)
mount=rod('Tom_ExteriorRisingMount',(.156,.10,.551),(.320,.10,.800),.014,1,'fixed exterior tom mount rises from bass shell')
arm=rod('Tom_ExteriorShortBracket',(.334,.10,.800),(.265,.10,.800),.016,1,'short fixed bracket reaches tom lower wall without crossing its cavity')
link(bass,mount,(.157,.10,.5525),axis=(0,1,0),spread=.002)
link(mount,arm,(.316,.10,.794),axis=(0,1,0),spread=.002)
link(arm,tom,(.267,.10,.800),axis=(0,1,0),spread=.002)
link(arm,tbh,(.273,.10,.795),axis=(0,1,0),spread=.002)
# Three-legged fixed stands, with separate finite pads and an actual central post.
def tripod(label,c,top,rfoot,angle):
 x,y=c;post=rod(label+'_LowerPost',(x,y,.135),(x,y,top),.016,1,'fixed main support post')
 legs=[]
 for k in range(3):
  a=angle+math.tau*k/3;d=(math.cos(a),math.sin(a),0);base=(x+rfoot*d[0],y+rfoot*d[1],.027)
  leg=rod(label+'_Leg_%02d'%(k+1),(x,y,.205),base,.014,1,'fixed diagonal tripod leg');legs.append(leg)
  foot=box(label+'_Foot_%02d'%(k+1),(base[0],base[1],.018),(.070,.065,.036),4,'finite tripod ground foot');FEET.append(foot)
  # Legs start just outside a small central post interior, meeting by finite overlap.
  link(post,leg,(x+d[0]*.006,y+d[1]*.006,.200),axis=(-d[1],d[0],0),spread=.002)
  link(leg,foot,(base[0]-d[0]*.005,base[1]-d[1]*.005,.031),axis=(-d[1],d[0],0),spread=.002)
 # Their nearby root volumes intentionally overlap one another within the fixed hub.
 for i in range(3):
  for j in range(i+1,3):link(legs[i],legs[j],(x,y,.200),axis=(0,0,1),spread=.001)
 return post
spost=tripod('SnareStand',(-.53,.12),.493,.235,math.radians(30))
basket=[]
for k in range(3):
 a=math.tau*k/3;d=(math.cos(a),math.sin(a),0);x,y=-.53,.12
 arm=rod('SnareBasket_Arm_%02d'%(k+1),(x,y,.477),(x+.179*d[0],y+.179*d[1],.525),.013,1,'fixed lower basket arm stays below the open drum cavity');basket.append(arm)
 link(spost,arm,(x+d[0]*.005,y+d[1]*.005,.481),axis=(-d[1],d[0],0),spread=.002)
 upright=rod('SnareBasket_RimSupport_%02d'%(k+1),(x+.179*d[0],y+.179*d[1],.517),(x+.179*d[0],y+.179*d[1],.581),.013,1,'short outer basket support stays outside the entire drum cavity')
 link(arm,upright,(x+.175*d[0],y+.175*d[1],.523),axis=(-d[1],d[0],0),spread=.002)
 link(upright,sbh,(x+.176*d[0],y+.176*d[1],.579),axis=(-d[1],d[0],0),spread=.002)
 link(upright,snare,(x+.176*d[0],y+.176*d[1],.579),axis=(-d[1],d[0],0),spread=.002)
for i in range(3):
 for j in range(i+1,3):link(basket[i],basket[j],(-.53,.12,.483),axis=(0,0,1),spread=.001)
# The cymbal is a formed 8 mm thick annular profile, never a plane or flat disk.
cpost=tripod('CymbalStand',(.63,.12),.725,.250,math.radians(30))
cupper=rod('CymbalStand_UpperPost',(.63,.12,.690),(.63,.12,1.166),.0085,1,'fixed upper cymbal post passing through the cymbal center hole')
link(cpost,cupper,(.63,.12,.708),axis=(1,0,0),spread=.002)
profile=[(.013,1.155),(.045,1.150),(.095,1.110),(.255,1.075)]
vs=[];n=40
for lower in [False,True]:
 for r,z in profile:
  for i in range(n):
   a=math.tau*i/n;vs.append((.63+r*math.cos(a),.12+r*math.sin(a),z-(.008 if lower else 0)))
fs=[];rings=len(profile)
for layer in range(2):
 off=layer*rings*n
 for ringno in range(rings-1):
  for i in range(n):
   j=(i+1)%n;f=(off+ringno*n+i,off+(ringno+1)*n+i,off+(ringno+1)*n+j,off+ringno*n+j);fs.append(f if layer==0 else tuple(reversed(f)))
for ringno in [0,rings-1]:
 for i in range(n):
  j=(i+1)%n;a=ringno*n+i;b=ringno*n+j;f=(a,b,rings*n+b,rings*n+a);fs.append(tuple(reversed(f)) if ringno==0 else f)
cymbal=mesh('Cymbal_FormedThickBrass',vs,fs,3,'single continuous 8 mm thick shaped cymbal with raised bell and true small center bore')
felt=ring('Cymbal_LowerFeltCollar',(.63,.12,0),*ZB,.030,.007,1.140,1.150,4,'finite lower collar between stem and formed cymbal',n=24)
cap=rod('Cymbal_UpperFixedCap',(.63,.12,1.152),(.63,.12,1.170),.022,4,'fixed upper cymbal clamp cap',n=24)
link(cupper,felt,(.6377,.12,1.145),axis=(0,0,1),spread=.002)
link(cupper,cap,(.63,.12,1.160),axis=(1,0,0),spread=.002)
link(felt,cymbal,(.650,.12,1.148),axis=(0,1,0),spread=.002)
link(cap,cymbal,(.645,.12,1.1533),axis=(0,1,0),spread=.001)
# Broad non-contact clearances between drum shells, mount, cymbal and ground.
void_box('BetweenBassAndSnare',(-.332,-.025,.320),(-.317,.230,.490),'finite free space between the bass body and separate snare')
void_box('BetweenTomAndCymbal',(.330,.035,.850),(.353,.180,1.025),'finite free space between mounted tom and cymbal stand')
void_box('BelowCymbalOuterBow',(.720,.020,.935),(.800,.190,1.052),'finite clear volume beneath outer cymbal, away from central support')
DRUM_KIT_CONTRACT={'single_prop_count':1,'drums':DRUMS,'cymbal_mesh':cymbal,'cymbal_profile_radius_z_m':profile,'cymbal_vertical_thickness_m':.008,'cymbal_true_center_bore_radius_m':.013,'ground_meshes':FEET,'static_fixed_pose_only':True,'sound_motion_human_fit_load_or_safety_claim':False}
def measure_drum_kit_geometry(vertices):
 assert set(vertices)==set(G),'Changed complete kit mesh set'
 rows=[]
 for name,g in G.items():
  actual=sorted(set(tuple(float(c) for c in p) for p in vertices[name]));expected=sorted(set(g['vertices']))
  assert len(actual)==len(expected),('Changed unique surface vertex count',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(i)==1 for i in matches) and len({i[0] for i in matches})==len(expected),('Actual surface lacks bijective unique source match',name)
  rows.append({'mesh':name,'unique_vertices':len(actual),'maximum_position_error_m':max(math.dist(p,expected[i[0]]) for p,i in zip(actual,matches)),'unique_bijective_surface_match':True})
 return dict(DRUM_KIT_CONTRACT,actual_components=rows,full_finite_void_count=len(VOID_VOLUMES),material_contract=MATERIAL_CONTRACT)
FOCUS=(.075,0,.560);ORTHO=2.2
CAMERAS={'gray-front3q':(3,-4,3.10),'gray-back3q':(-3,4,3.10),'thumbnail':(3,-4,3.10),'qa-front':(.075,-6,2.20),'qa-side':(6,0,2.20),'qa-top':(.075,0,6),'qa-back':(.075,6,2.20),'qa-wireframe':(3,-4,3.10),'silhouette-128-front':(.075,-6,2.20),'silhouette-128-side':(6,0,2.20)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneCompleteCompactAcousticDrumKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Design ground datum X=0, Y=0, Z=0; not the whole-kit AABB centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
drum_evidence=measure_drum_kit_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'drum_kit_geometry':drum_evidence,'finite_empty_volumes':void_volume_checks,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/music/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
