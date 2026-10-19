"""Original fictional fish skeleton and dedicated two-post museum mount.
One static visual prop. Metres, Z up, head/front -Y. No species or anatomy claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='museum-stylized-fish-skeleton-mount-01';VERSION='1.0.0';TITLE='Fictional Fish Skeleton Display Mount'
DESCRIPTION=('One original complete fictional fish-shaped skeleton on its dedicated two-post long base, counted together as one fixed static visual prop. A continuous thick backbone has six integrated vertebral bulges, twelve thick curved ribs with finite root faces, a broad thick skull with an actual full-through orbital aperture, a fixed lower jaw with real open mouth space, and a tapered three-ray tail. Two narrow fixed metal posts meet two finite saddles beneath the backbone; the continuous long base has an entire flat ground face. All bone and mount pieces have finite traceable material or face connections and closed thick boundaries. No real species, labels, lettering, glass cover, old plinth, fossil slab, room, people, animation or additional specimen. This is original geometry, not a recoloured fossil, thin old horse, reshaped bear or assembly of reused fragments. No biological, anatomical, paleontological, educational, age, restoration, bone-material, motion, load, stability, manufacture, installation or exhibit-safety accuracy or certification.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SECTIONS=[];RIBS=[];POSTS=[];SADDLES=[]
PALETTE=[('Bone_WarmIvory',(.79,.72,.57,1),.78,0),('Base_DeepPetrol',(.045,.125,.145,1),.66,.10),('Mount_DullBronze',(.29,.23,.14,1),.53,.55)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
def prism_geometry(x,width,yz):
 if area2(yz)<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 return vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
def prism_x(name,x,width,yz,mat,role):return mesh(name,*prism_geometry(x,width,yz),mat,role)
def prism_y(name,y,width,xz,mat,role):
 vs,fs=prism_geometry(y,width,xz);return mesh(name,[(x,yy,z) for yy,x,z in vs],[tuple(reversed(f)) for f in fs],mat,role)
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size;return prism_x(name,x,w,[(y-d/2,z-h/2),(y+d/2,z-h/2),(y+d/2,z+h/2),(y-d/2,z+h/2)],mat,role)
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);ref=(0,1,0) if abs(axis[0])>.9 else (1,0,0);u=unit(sub(ref,mul(axis,dot(ref,axis))));v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':points or [point],'scope':scope})
def void_x(name,x,w,yz,scope):
 vs,fs=prism_geometry(x,w,yz);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'targets':None,'role':scope}
def void_y(name,y,w,xz,scope):
 vs,fs=prism_geometry(y,w,xz);VOID_VOLUMES[name]={'vertices':[(x,yy,z) for yy,x,z in vs],'faces':[tuple(reversed(f)) for f in fs],'targets':None,'role':scope}
# Original single long chamfered rectangular base, full finite bottom on Z0.
basepoly=[(-.26,-1.18),(-.20,-1.25),(.20,-1.25),(.26,-1.18),(.26,1.18),(.20,1.25),(-.20,1.25),(-.26,1.18)]
vs=[(x,y,z) for z in[0,.12] for x,y in basepoly];fs=[tuple(reversed(range(8))),tuple(8+i for i in range(8))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
mesh('DedicatedLongBase',vs,fs,1,'one original low long base with eight-sided outline and entire finite flat bottom');FEET.append('DedicatedLongBase')
# One connected backbone boundary, with six bulges built into the same material.
RIB_Y=[-.40,-.16,.08,.32,.56,.80];SCALES=[1.,.98,.90,.80,.68,.52]
rings=[(-.64,.06,1.36)]
for y in RIB_Y:rings += [(y-.095,.045,1.35),(y-.045,.075,1.39),(y+.045,.075,1.39),(y+.095,.045,1.35)]
rings.append((1.04,.035,1.36))
vs=[(x,y,z) for y,w,top in rings for x,z in[(-w,1.26),(w,1.26),(w,top),(-w,top)]];fs=[(3,2,1,0)]
for j in range(len(rings)-1):
 for i in range(4):fs.append((j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i))
fs.append(tuple((len(rings)-1)*4+i for i in range(4)))
mesh('ContinuousVertebralBackbone',vs,fs,0,'continuous closed backbone including all six enlarged vertebral sections; no detached bead array')
# Each thin post and saddle touches through complete positive-area end patches.
for j,y in enumerate([-.40,.56]):
 post=box('FixedSupportPost_%d'%j,(0,y,.65),(.045,.05,1.06),2,'fixed dedicated display post with full bottom and upper end faces');POSTS.append(post)
 saddle=box('FiniteBackboneSaddle_%d'%j,(0,y,1.22),(.12,.05,.08),2,'finite rectangular saddle centered underneath an integrated vertebra, outside rib roots');SADDLES.append(saddle)
 contact('DedicatedLongBase',post,(0,0,1),(0,y,.12),.002249,'entire fixed post bottom on dedicated base')
 contact(post,saddle,(0,0,1),(0,y,1.18),.002249,'entire post top against saddle bottom')
 contact(saddle,'ContinuousVertebralBackbone',(0,0,1),(0,y,1.26),.005999,'entire 120 by 50 mm saddle top on backbone underside')
# Thick curved ribs: their only connected boundary is the complete root face.
ribpoly=[(.075,1.28),(.20,1.23),(.31,1.10),(.35,.96),(.31,.85),(.24,.80),(.28,.765),(.36,.81),(.41,.95),(.37,1.13),(.25,1.29),(.075,1.34)]
for j,(y,scale) in enumerate(zip(RIB_Y,SCALES)):
 poly=[(.075+(x-.075)*scale,1.31+(z-1.31)*scale) for x,z in ribpoly]
 for sign in[-1,1]:
  n=prism_y('CurvedRib_%d_%s'%(j,'L' if sign<0 else 'R'),y,.055,[(sign*x,z) for x,z in poly],0,'one continuous thick curved rib from finite root to closed tapered end');RIBS.append(n)
  contact('ContinuousVertebralBackbone',n,(sign,0,0),(sign*.075,y,1.31),.055*.06*scale-.000001,'complete rib root rectangle on vertebral side facet')
# Original thick skull annulus. The eye opening is real material topology.
outer=[(-.64,1.16),(-.64,1.45),(-.88,1.59),(-1.16,1.63),(-1.46,1.48),(-1.60,1.17),(-1.34,1.16),(-.83,1.16)]
center=(-1.12,1.38);eye=[(center[0]+.13*(y-center[0])/math.hypot(y-center[0],z-center[1]),center[1]+.13*(z-center[1])/math.hypot(y-center[0],z-center[1])) for y,z in outer]
vs=[(x,y,z) for x,poly in[(-.10,outer),(.10,outer),(.10,eye),(-.10,eye)] for y,z in poly]
fs=[(j*8+i,j*8+(i+1)%8,((j+1)%4)*8+(i+1)%8,((j+1)%4)*8+i) for j in range(4) for i in range(8)]
mesh('ThickOrbitalSkull',vs,fs,0,'broad continuous eight-sided skull ring with true thick fully through orbital hole')
contact('ThickOrbitalSkull','ContinuousVertebralBackbone',(0,1,0),(0,-.64,1.31),.011999,'entire anterior backbone end on skull rear facet')
jawpoly=[(-1.60,.96),(-1.49,.91),(-.78,.95),(-.66,1.09),(-.66,1.16),(-.80,1.16),(-.80,1.08),(-1.48,1.02),(-1.59,1.04)]
prism_x('FixedLowerJaw',0,.16,jawpoly,0,'one original fixed lower jaw with complete thick rear rise and open mouth gap above')
contact('FixedLowerJaw','ThickOrbitalSkull',(0,0,1),(0,-.73,1.16),.022399,'entire lower-jaw rear rise upper face on skull underside')
# One continuous forked three-ray tail with no detached bones or planar decals.
tailpoly=[(1.04,1.26),(1.16,1.26),(1.50,.86),(1.55,.90),(1.30,1.27),(1.58,1.27),(1.58,1.35),(1.30,1.35),(1.55,1.72),(1.50,1.76),(1.16,1.36),(1.04,1.36)]
prism_x('ContinuousThreeRayTail',0,.06,tailpoly,0,'one closed thick forked tail of three material-continuous tapered rays')
contact('ContinuousVertebralBackbone','ContinuousThreeRayTail',(0,1,0),(0,1.04,1.31),.005999,'entire tail-root end face on posterior backbone end')
# Complete finite air bodies, not sparse center rays. Eye body extends past both
# skull mouths. The jaw body covers the full designed mouth region through width.
eye_air=[(center[0]+(y-center[0])*.985,center[1]+(z-center[1])*.985) for y,z in eye]
void_x('WholeOrbitalAir',0,.204,eye_air,'complete through orbital aperture, 1.95 mm radial margin, beyond both external skull mouths')
void_x('WholeJawAir',0,.204,[(-1.579,1.045),(-1.48,1.024),(-.804,1.084),(-.804,1.157),(-1.34,1.157),(-1.579,1.167)],'complete designed jaw opening between actual snout/skull underside and lower-jaw upper outline, with 3 to 5 mm boundaries and through both side mouths')
for j,(a,b) in enumerate(zip(RIB_Y,RIB_Y[1:])):
 # Complete intercostal slab: all width and all height under the backbone,
 # extending through the open flanks; posts are inside rib planes, never this air.
 void_y('WholeInterRibAir_%d'%j,(a+b)/2,b-a-.057,[(-.412,.764),(.412,.764),(.412,1.259),(-.412,1.259)],'entire slab between adjacent left/right rib pairs below the spine; full flank width and height, 1 mm boundary margin')
# The complete transverse belly cavities at each rib plane complement the full
# inter-rib slabs. Exact convex half-plane partition removes only actual post and
# saddle occupants on the two supported planes; numerical margins are explicit.
def clip2(poly,axis,value,less=True):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  dp=(p[axis]-value)*(1 if less else -1);dq=(q[axis]-value)*(1 if less else -1)
  if dp<=0:out.append(p)
  if (dp<0<dq) or (dq<0<dp):out.append(tuple(p[k]+(q[k]-p[k])*dp/(dp-dq) for k in range(2)))
 return out
def inset_convex(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length);lines.append((n,n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for (a,aa),(b,bb) in zip(lines[-1:]+lines[:-1],lines):
  det=a[0]*b[1]-a[1]*b[0]
  assert abs(det)>1e-10
  out.append(((aa*b[1]-a[1]*bb)/det,(a[0]*bb-aa*b[0])/det))
 assert area2(out)>1e-10 and all(n[0]*p[0]+n[1]*p[1]>=q-1e-8 for n,q in lines for p in out)
 return out
BELLY_PARTITION=[]
for j,(y,scale) in enumerate(zip(RIB_Y,SCALES)):
 side=[(.075+(x-.075)*scale,1.31+(z-1.31)*scale) for x,z in reversed(ribpoly[:6])]
 nominal=[(-x,z) for x,z in reversed(side)]+side
 nominal=clip2(nominal,1,1.26)
 poly=inset_convex(nominal,.001)
 if j not in[0,4]:cells=[('All',poly)]
 else:
  cells=[]
  for sign,label in [(-1,'Left'),(1,'Right')]:
   lower=clip2(clip2(poly,1,1.179),0,sign*.0235,sign<0)
   upper=clip2(clip2(poly,1,1.181,False),0,sign*.061,sign<0)
   cells.extend([(label+'Lower',lower),(label+'Upper',upper)])
 for label,cell in cells:
  assert len(cell)>=3
  name='WholeBellyAir_%d_'%j+label
  void_y(name,y,.057,cell,'complete transverse inner belly cavity partition with 1 mm boundary margin; only actual post/saddle envelopes removed at their own two rib planes')
  BELLY_PARTITION.append({'name':name,'rib_index':j,'xz_polygon':cell,'y0':y-.0285,'y1':y+.0285,'actual_mount_occupants_excluded':j in[0,4]})

# Tail split slots are finite whole triangular prisms, open at the rear mouths.
void_x('WholeUpperTailSlot',0,.064,[(1.31,1.356),(1.57,1.356),(1.548,1.698)],'whole open upper tail-ray split with finite boundary margin')
void_x('WholeLowerTailSlot',0,.064,[(1.31,1.264),(1.548,.922),(1.57,1.264)],'whole open lower tail-ray split with finite boundary margin')
for g in VOID_VOLUMES.values():g['targets']=list(G)
FISH_CONTRACT={'single_prop_count':1,'fictional_species':True,'continuous_backbone':1,'integrated_vertebrae':6,'closed_curved_ribs':12,'thick_true_orbital_skull':1,'fixed_jaw':1,'continuous_three_ray_tail':1,'dedicated_base':1,'fixed_posts':2,'finite_saddles':2,'whole_empty_volumes':len(VOID_VOLUMES),'finite_opposed_contacts':len(CONTACTS)}
def measure_fish_geometry(vertices):
 assert set(vertices)==set(G)
 assert abs(min(p[2] for p in vertices['DedicatedLongBase']))<2e-7
 for n in POSTS:assert abs(min(p[2] for p in vertices[n])-.12)<2e-7 and abs(max(p[2] for p in vertices[n])-1.18)<2e-7
 return dict(FISH_CONTRACT,geometry_scope='actual complete source/exported coordinates; full contact, void, separation and actual negative gates remain required')
FOCUS=(0,0,.87);ORTHO=4.10
CAMERAS={'gray-front3q':(8,-5,4.1),'gray-back3q':(-8,5,4.1),'thumbnail':(8,-5,4.1),'qa-front':(0,-9,3.4),'qa-side':(9,0,3.3),'qa-top':(0,0,9),'qa-back':(0,9,3.4),'qa-wireframe':(8,-5,4.1),'silhouette-128-front':(0,-9,3.4),'silhouette-128-side':(9,0,3.3)}
WIRE_THICKNESS=ORTHO/850

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
root=bpy.data.objects.new('OneFictionalFishSkeletonMount',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='dedicated base centre ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in [('DedicatedLongBase',(0,0,.06),(0,0,.15)),('ThickOrbitalSkull',(0,-1.12,1.58),(0,-1.12,1.38))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate independent actual-GLB gates.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_fish_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'fish_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/museum/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
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
 for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
