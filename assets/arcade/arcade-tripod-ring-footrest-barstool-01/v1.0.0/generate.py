"""Original three-legged high barstool with genuine annulus and open three-spoke cradle."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='arcade-tripod-ring-footrest-barstool-01';VERSION='1.0.0';TITLE='Tripod Ring-Footrest Barstool'
DESCRIPTION=('One original static backless arcade barstool, counted as one prop. Three thick outward-splayed legs have actual complete flat feet and integral short inward lugs. All three lugs meet a complete thick dodecagonal footrest annulus on separate finite planar interfaces; the whole ring centre is truly open. A single thick three-spoke under-seat cradle has a real central through aperture and full open inter-spoke spaces. Three full leg tops bear on the cradle, and the complete cradle top bears against the separate thick bevelled round cushion. Seat top is author-designed at 0.75 metres as visual scale only. Six closed editable meshes, constant opaque unlinked PBR colours, source Z up, front -Y and exact ground-level bounds-centre origin. No textures, fonts, external meshes, scene, characters, stools taken from game machines, text, animation or mechanism. No sitting suitability, comfort, ergonomic fit, rotation, height adjustment, folding, load capacity, centre-of-mass stability, tip resistance, durability, manufacturing, installation, public-space safety or compatibility with existing arcade controls is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('Frame_DeepPetrol',(.038,.16,.18,1),.53,.16),('Footring_WarmBrass',(.61,.33,.095,1),.49,.35),('Cushion_Berry',(.47,.065,.18,1),.80,0),('Cushion_DeepBerryBase',(.17,.025,.075,1),.77,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled colours; no TEX_* nodes or linked inputs.'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,p,mat=0,tag=''):
  ids=[self.vertex(q) for q in p]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def earclip(poly):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 order=list(range(len(poly))) if area>0 else list(reversed(range(len(poly))));out=[]
 while len(order)>3:
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-12:continue
   if any(all(cr(poly[x],poly[y],poly[q])>=-1e-12 for x,y in[(a,b),(b,c),(c,a)]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(k);break
  else:raise AssertionError('non-simple or degenerate polygon')
 out.append(tuple(order));return out

def radial(a,p):x,y,z=p;return(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z)
def transform(g,a):q=dict(g);q['vertices']=[radial(a,p) for p in g['vertices']];return q
def extrude_xy(poly,z0,z1,mat=0):
 if sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))<0:poly=list(reversed(poly))
 m=Mesh();rings=[[(x,y,z) for x,y in poly] for z in[z0,z1]]
 for f in earclip(poly):m.face([rings[0][i] for i in f][::-1],mat);m.face([rings[1][i] for i in f],mat)
 for i in range(len(poly)):j=(i+1)%len(poly);m.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]],mat)
 return m.result('one complete closed polygonal prism')
def extrude_xz(poly,y0,y1,mat=0):
 g=extrude_xy(poly,-y1,-y0,mat);g['vertices']=[(x,-z,y) for x,y,z in g['vertices']];return g

def box_geometry(lo,hi,mat=0):return extrude_xy([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],mat)
def volume(table,name,g,targets,role):table[name]=dict(g,targets=list(targets),role=role,asset_member=False)
def regular(n,apothem,phase=0):return[(apothem/math.cos(math.pi/n)*math.cos(phase+(i+.5)*math.tau/n),apothem/math.cos(math.pi/n)*math.sin(phase+(i+.5)*math.tau/n)) for i in range(n)]
def annulus(ri,ro,z0,z1,n=12,phase=-math.pi/2,mat=1):
 m=Mesh();rr=[[(x,y,z) for x,y in regular(n,r,phase)] for z,r in[(z0,ri),(z0,ro),(z1,ri),(z1,ro)]]
 for i in range(n):
  j=(i+1)%n
  for inds in[((0,j),(1,j),(1,i),(0,i)),((2,i),(3,i),(3,j),(2,j)),((0,j),(0,i),(2,i),(2,j)),((1,i),(1,j),(3,j),(3,i))]:m.face([rr[a][b] for a,b in inds],mat)
 return m.result('one closed full annulus with true inner and outer walls')
ANGLES=[-math.pi/2,math.pi/6,5*math.pi/6];LEGS=[];RING='Footrest_CompleteDodecagonalAnnulus';CRADLE='SeatCradle_OpenCentreThreeSpokes';CUSHION='Cushion_ThickBevelledRound'
def centre(z):return .295-.12*z/.66
def leg_profile(z0=0,z1=.66,half=.035,lug=True):
 p=[(centre(z0)-half,z0),(centre(z0)+half,z0),(centre(z1)+half,z1),(centre(z1)-half,z1)]
 if lug:p += [(centre(.305)-half,.305),(.200,.305),(.200,.255),(centre(.255)-half,.255)]
 return p
for i,a in enumerate(ANGLES):
 name='Leg_%d_ContinuousSplayAndRingLug'%(i+1);LEGS.append(name);G[name]=transform(extrude_xz(leg_profile(),-.035,.035),a);G[name]['role']='One continuous splayed thick leg, complete 70mm-square flat foot, complete flat head and integral short inward ring lug; no disconnected blocks'
FEET=list(LEGS);G[RING]=annulus(.165,.200,.255,.305)
# Nine-vertex original cradle outline: broad tip, concave valley, broad next tip.
OUTER=[]
for a in ANGLES:
 OUTER += [radial(a,(.225,-.045,0))[:2],radial(a,(.225,.045,0))[:2],(.095*math.cos(a+math.pi/3),.095*math.sin(a+math.pi/3))]
def ray_outline(poly,a):
 d=(math.cos(a),math.sin(a));cr=lambda x,y:x[0]*y[1]-x[1]*y[0];hits=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  e=sub(q,p);det=cr(d,e)
  if abs(det)<1e-10:continue
  t=cr(p,e)/det;u=cr(p,d)/det
  if t>0 and -1e-8<=u<=1+1e-8:hits.append(t)
 assert hits,(poly,a);return min(hits)
A=sorted(set(round(math.atan2(y,x)%math.tau,12) for x,y in OUTER)|set(round(i*math.tau/36,12) for i in range(36)))
def cradle(z0=.66,z1=.69,inner=.045,radial_min=None):
 m=Mesh();rings=[]
 for z,kind in[(z0,'in'),(z0,'out'),(z1,'in'),(z1,'out')]:
  rings.append([((inner if kind=='in' else ray_outline(OUTER,a))*math.cos(a),(inner if kind=='in' else ray_outline(OUTER,a))*math.sin(a),z) for a in A])
 for i in range(len(A)):
  j=(i+1)%len(A)
  for inds in[((0,j),(1,j),(1,i),(0,i)),((2,i),(3,i),(3,j),(2,j)),((0,j),(0,i),(2,i),(2,j)),((1,i),(1,j),(3,j),(3,i))]:m.face([rings[a][b] for a,b in inds],0)
 return m.result('One continuous thick three-spoke cradle with a full central through hole and three deep open exterior bays')
G[CRADLE]=cradle()
def disk_loft(levels,mats,n=48):
 m=Mesh();rr=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for z,r in levels]
 for i in range(n):j=(i+1)%n;m.face([(0,0,levels[0][0]),rr[0][j],rr[0][i]],mats[0]);m.face([(0,0,levels[-1][0]),rr[-1][i],rr[-1][j]],mats[-1])
 for k,(lo,hi) in enumerate(zip(rr,rr[1:])):
  for i in range(n):j=(i+1)%n;m.face([lo[i],lo[j],hi[j],hi[i]],mats[k])
 return m.result('one complete thick bevelled circular cushion with integral lower material band')
G[CUSHION]=disk_loft([(.69,.233),(.698,.233),(.707,.242),(.735,.242),(.75,.227)],[3,3,2,2])
def seat(name,a,b,axis,u,v,plane,points,minarea,offset=.001,coverage='smaller_complete_interface'):
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':plane,'points':points,'interior_probe_offset_m':offset,'minimum_patch_area_m2':minarea,'coverage':coverage,'role':'finite opposed whole-area bearing; no interpenetration'})
for i,(a,leg) in enumerate(zip(ANGLES,LEGS)):
 axis=(math.cos(a),math.sin(a),0);u=(-math.sin(a),math.cos(a),0)
 seat('RingToIntegralLug_%d'%i,RING,leg,axis,u,(0,0,1),.200,[radial(a,(.200,0,.28))],.00349)
 seat('WholeLegHeadToSpoke_%d'%i,leg,CRADLE,(0,0,1),(1,0,0),(0,1,0),.66,[radial(a,(centre(.66),0,.66))],.00489)
seat('WholeCradleTopToCushion',CRADLE,CUSHION,(0,0,1),(1,0,0),(0,1,0),.69,[radial(ANGLES[0],(.14,0,.69))],.073)
# Whole finite QA-only air/material bodies. They are never exported.
def triangle_air(z0,z1):
 m=Mesh();rr=[]
 for z in[z0,z1]:
  r=2*(centre(z)-.038);rr.append([(r*math.cos(a+math.pi/3),r*math.sin(a+math.pi/3),z) for a in ANGLES])
 m.face(rr[0][::-1]);m.face(rr[1])
 for i in range(3):j=(i+1)%3;m.face([rr[0][i],rr[0][j],rr[1][j],rr[1][i]])
 return m.result('complete finite triangular inter-leg air following all three inward splayed leg planes')
volume(VOID_VOLUMES,'FullInterLegOpeningBelowRing',triangle_air(.004,.251),list(G),'whole finite inter-leg opening from near ground to footring underside, including full three outward triangular corners')
volume(VOID_VOLUMES,'FullInterLegOpeningAboveRing',triangle_air(.309,.656),list(G),'whole finite inter-leg opening above footring and below seat cradle, following every inward splayed leg plane')
volume(VOID_VOLUMES,'WholeFootringAperture',extrude_xy(regular(12,.162,-math.pi/2),.251,.309),list(G),'complete dodecagonal ring aperture extended through both mouths; central air is actual volume')
volume(VOID_VOLUMES,'WholeCradleCentralAperture',disk_loft([(.656,.042),(.688,.042)],[0],36),list(G),'complete central cradle through aperture to just below the supported cushion; not claimed as a hole through the cushion')
for i,a in enumerate(ANGLES):
 # One complete inset exterior bay, bounded by both adjacent spokes and the outer radial mouth.
 p=[(.222,.050),(.095*math.cos(math.pi/3),.095*math.sin(math.pi/3)+.005),radial(2*math.pi/3,(.222,-.050,0))[:2]]
 p += [(.26*math.cos(t),.26*math.sin(t)) for t in [2*math.pi/3-.22,math.pi/2,math.pi/3,math.pi/6,.22]]
 # Ensure a single oriented simple outline before triangulating.
 g=transform(extrude_xy(p,.663,.687),a)
 volume(VOID_VOLUMES,'FullInterSpokeBay_%d'%i,g,list(G),'complete finite open cradle bay from left boundary around its concave root to right boundary and outer mouth')
 volume(SOLID_VOLUMES,'ContinuousLegMaterial_%d'%i,transform(extrude_xz(leg_profile(.004,.656,.030,False),-.030,.030),a),[LEGS[i]],'whole inset splayed leg body from finite foot region to whole head; excludes only exterior bevel-free boundary')
 volume(SOLID_VOLUMES,'IntegralLugRoot_%d'%i,transform(box_geometry((.208,-.030,.260),(.250,.030,.300)),a),[LEGS[i]],'whole finite lug root crosses into the continuous leg material')
 volume(SOLID_VOLUMES,'WholeSpokeCore_%d'%i,transform(box_geometry((.060,-.022,.664),(.211,.022,.686)),a),[CRADLE],'whole finite spoke root and arm material from central annular region to outer leg-bearing head')
volume(SOLID_VOLUMES,'CompleteFootringMaterial',annulus(.168,.197,.258,.302),[RING],'whole inward-offset complete annular ring material, never isolated samples')
volume(SOLID_VOLUMES,'WholeCushionCore',disk_loft([(.694,.221),(.746,.221)],[0]),[CUSHION],'complete finite thick central cushion core, including material over centre and all three spokes')
# Common X/Y translation puts exact ground-level bounds centre at zero.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=tuple(-(min(p[i] for p in allv)+max(p[i] for p in allv))/2 if i<2 else 0 for i in range(3))
def shifted(p):return add(p,SHIFT)
for table in[G,VOID_VOLUMES,SOLID_VOLUMES]:
 for g in table.values():g['vertices']=[shifted(p) for p in g['vertices']]
for r in CONTACTS:r['points']=[shifted(p) for p in r['points']];r['plane_m']+=dot(SHIFT,r['axis'])
BARSTOOL_CONTRACT={'single_prop_count':1,'editable_meshes':len(G),'splayed_legs':3,'complete_ground_patches':3,'integral_ring_lugs':3,'continuous_ring':1,'central_ring_aperture':1,'three_spoke_cradle':1,'central_cradle_aperture':1,'separate_thick_cushion':1,'seat_top_m':.75,'ground_level_m':0,'origin':'ground-level exact bounds centre','no_load_or_ergonomic_claim':True}
def measure_barstool_geometry(vertices):
 assert set(vertices)==set(G)
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<6e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<6e-7 for p in actual),(n,'actual shape changed')
 return dict(BARSTOOL_CONTRACT,whole_void_groups=len(VOID_VOLUMES),finite_material_volume_groups=len(SOLID_VOLUMES),materials=MATERIAL_CONTRACT)
FOCUS=(0,0,.375);ORTHO=1.08
CAMERAS={'gray-front3q':(1.4,-2.4,1.15),'gray-back3q':(-1.4,2.4,-1.5),'thumbnail':(1.4,-2.4,1.15),'qa-front':(0,-3,.65),'qa-side':(3,0,.65),'qa-top':(0,0,3),'qa-back':(0,3,.65),'qa-wireframe':(1.4,-2.4,1.15),'silhouette-128-front':(0,-3,.65),'silhouette-128-side':(3,0,.65)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/1100

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
root=bpy.data.objects.new('OneTripodRingFootrestBarstool',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground-level exact bounds centre (0,0,0), source Z up and front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(LEGS[0],shifted(radial(ANGLES[0],(.295-.12*.12/.66,0,.12))),shifted((0,0,.12))),(RING,shifted(radial(ANGLES[0],(.182,0,.28))),shifted((0,0,.28)))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Producer Blender checks below cover actual closed mesh topology, ground and
# opposed contact triangle areas plus auxiliary interior-side probes only.
# Complete void/material bodies, full-interface nonpenetration and all-pair
# boundary acceptance remain independent actual-GLB gates; no full void claim here.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0048,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_barstool_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'barstool_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'producer_check_scope':'Actual closed mesh topology, degeneracy, finite ground triangles, opposed contact triangle area and auxiliary interior-side probes, oriented GLB/PBR readback only. Whole void/material volumes, complete interface nonpenetration and all-pair boundary acceptance remain independent actual-GLB gates.',
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-6,-8,11),1800,7),('Fill',(7,-3,7),1100,6),('Rim',(3,8,9),1500,5)]:
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
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True
 old_ground_visibility=ground.hide_render
 try:
  if name=='gray-back3q':ground.hide_render=True
  t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 finally:ground.hide_render=old_ground_visibility
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
