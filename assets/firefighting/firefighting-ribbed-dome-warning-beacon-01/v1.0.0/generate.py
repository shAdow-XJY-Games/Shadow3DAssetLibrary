"""Original low three-hole mounting disc, annular collar and integral ribbed blind shell; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='firefighting-ribbed-dome-warning-beacon-01';VERSION='1.0.0';TITLE='Ribbed Dome Warning Beacon'
DESCRIPTION=('One original low fixed beacon appearance, counted as one static visual prop. A broad closed installation disc has three genuine full-thickness mounting holes and a complete planar underside. A thick open annular collar rests on the disc and supports the entire lower rim of a single integral closed-top dome shell. Twelve modeled longitudinal ridges are continuously part of its shared-vertex outer skin; an actual thick blind interior cavity remains inside, hidden after the base closes the assembly. Three closed editable component meshes, three opaque constant PBR materials, metre units, source Z up, front -Y, horizontal centre and mounting underside Z=0. No interior rotor, lens insert, glass, emission, textures, separate intersecting rib strips, imported old lamp, cables, vehicle, attachment bolts or scene. Static unlit illustrative geometry only: no rotating/flashing operation, brightness, optical coverage, warning or firefighting standard, electrical function, sealing, ingress protection, mounting compatibility, vehicle fit, material/manufacturing or public-safety performance claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[]
BODY='ThreeHoleLowMountingDisc';COLLAR='CompleteAnnularRimSeat';SHELL='IntegralTwelveRidgeThickBlindDome'
PALETTE=[('MountingDiscDeepSlate',(.065,.105,.12,1),.57,.32),('CollarWarmBrushedAlloy',(.34,.29,.22,1),.42,.52),('OpaqueUnlitVermilionDome',(.64,.105,.035,1),.39,.06)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def within(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(within(p[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);break
  else:raise AssertionError(('untriangulable planar cell',p,order))
 out.append(tuple(order));return out

def perforated(outline,holes,t0,t1,material=0,role='',transform=lambda p:p):
 # Exact conforming scanline triangulation. Front and back both contain the
 # complete genuine holes; every remaining boundary gets a full-depth side.
 stations=sorted(set(round(x,9) for p in [outline]+holes for x,y in p))
 def interval(poly,x):
  if x<min(a for a,b in poly)-1e-9 or x>max(a for a,b in poly)+1e-9:return None
  yy=[]
  for (a,u),(b,v) in zip(poly,poly[1:]+poly[:1]):
   if abs(b-a)<1e-11:
    if abs(x-a)<1e-9:yy.extend([u,v])
   elif min(a,b)-1e-9<=x<=max(a,b)+1e-9:yy.append(u+(v-u)*(x-a)/(b-a))
  return (min(yy),max(yy)) if yy else None
 pp=[];tt=[];lk={}
 def vid(p):
  p=tuple(round(c,9) for c in p)
  if p not in lk:lk[p]=len(pp);pp.append(p)
  return lk[p]
 def cell(a,b,al,bl,ah,bh):
  right=sorted(set(y for poly in holes for q in [interval(poly,b)] if q for y in q if bl+1e-9<y<bh-1e-9));left=sorted(set(y for poly in holes for q in [interval(poly,a)] if q for y in q if al+1e-9<y<ah-1e-9),reverse=True)
  p=[(a,al),(b,bl)]+[(b,y) for y in right]+[(b,bh),(a,ah)]+[(a,y) for y in left];q=[]
  for r in p:
   r=tuple(round(c,9) for c in r)
   if not q or q[-1]!=r:q.append(r)
  if q[0]==q[-1]:q.pop()
  if len(q)<3:return
  ids=[vid(p) for p in q];tt.extend(tuple(ids[j] for j in tri) for tri in earclip2(q))
 for a,b in zip(stations,stations[1:]):
  aa=interval(outline,a);bb=interval(outline,b);active=sorted((p for p in holes if min(x for x,y in p)<(a+b)/2<max(x for x,y in p)),key=lambda p:interval(p,(a+b)/2)[0]);al,bl=aa[0],bb[0]
  for p in active:
   lo,hi=interval(p,a);ll,hh=interval(p,b);cell(a,b,al,bl,lo,ll);al,bl=hi,hh
  cell(a,b,al,bl,aa[1],bb[1])
 n=len(pp);vv=[(x,y,z) for z in [t0,t1] for x,y in pp];ff=[tuple(reversed(t)) for t in tt]+[tuple(i+n for i in t) for t in tt]
 counts=collections.Counter(tuple(sorted((a,b))) for t in tt for a,b in zip(t,t[1:]+t[:1]))
 for t in tt:
  for a,b in zip(t,t[1:]+t[:1]):
   if counts[tuple(sorted((a,b)))]==1:ff.append((a,b,b+n,a+n))
 return mesh([transform(p) for p in vv],ff,material,role)
def prism(poly,t0,t1,material=0,role='',transform=lambda p:p):
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for z in [t0,t1] for x,y in poly];tris=earclip2(poly)
 ff=[tuple(reversed(t)) for t in tris]+[tuple(i+n for i in t) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv],ff,material,role)
def octrect(x0,x1,y0,y1,ch):return [(x0+ch,y0),(x1-ch,y0),(x1,y0+ch),(x1,y1-ch),(x1-ch,y1),(x0+ch,y1),(x0,y1-ch),(x0,y0+ch)]
def contact(name,a,b,origin,axis,plane,points,area,offset=.0005):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':origin,'u':u,'v':v,'axis':axis,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=list(G) if targets is None else targets,role=role)
def axial(p):return(p[2],p[0],p[1])
def backmap(p):return(p[0],p[2],p[1])

# The following dimensions and radial/axial topology are original to this prop.
N=48
ANGLES=[math.tau*j/N for j in range(N)]
def circle(r,n=N,cx=0,cy=0):return [(round(cx+r*math.cos(math.tau*j/n),9),round(cy+r*math.sin(math.tau*j/n),9)) for j in range(n)]
def ring(z,r,amplitude=0):return [((r+amplitude*(1 if j%4 in (1,2) else 0))*math.cos(a),(r+amplitude*(1 if j%4 in (1,2) else 0))*math.sin(a),z) for j,a in enumerate(ANGLES)]
def profile(rings,material=0,role='',caps=True,cycle=False):
 n=len(rings[0]);assert all(len(q)==n for q in rings);vv=[p for q in rings for p in q];ff=[]
 for k in range(len(rings) if cycle else len(rings)-1):
  l=(k+1)%len(rings)
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=l*n+(j+1)%n;d=l*n+j
   # Explicit triangles also specify the surface on nonplanar rib-shoulder quads.
   ff.extend([(a,b,c),(a,c,d)])
 if caps:ff += [tuple(reversed(range(n))),tuple(range((len(rings)-1)*n,len(rings)*n))]
 return mesh(vv,ff,material,role)
def lathe(p,material=0,role=''):return profile([ring(z,r) for z,r in p],material,role)
def annulus(ri,ro,z0,z1,material=0,role=''):
 return profile([ring(z0,ro),ring(z1,ro),ring(z1,ri),ring(z0,ri)],material,role,caps=False,cycle=True)
def shell_geometry(outer,inner,material=2,role=''):
 # Outer upward wall + outer closed cap; inner downward wall + inner closed cap;
 # a complete bottom annulus joins the two into one watertight material boundary.
 rr=[ring(*r) for r in outer]+[ring(z,r) for z,r in reversed(inner)];n=N;m=len(outer);vv=[p for q in rr for p in q];ff=[]
 for k in list(range(m-1))+list(range(m,len(rr)-1)):
  for j in range(n):
   a=k*n+j;b=k*n+(j+1)%n;c=(k+1)*n+(j+1)%n;d=(k+1)*n+j;ff.extend([(a,b,c),(a,c,d)])
 ff += [tuple(range((m-1)*n,m*n)),tuple(reversed(range(m*n,(m+1)*n)))]
 for j in range(n):ff.extend([(j,(len(rr)-1)*n+j,(len(rr)-1)*n+(j+1)%n),(j,(len(rr)-1)*n+(j+1)%n,(j+1)%n)])
 return mesh(vv,ff,material,role)
BASE_RADIUS=.240;BASE_TOP=.035;MOUNT_CENTRES=[(.200*math.cos(a),.200*math.sin(a)) for a in [-math.pi/2,math.pi/6,5*math.pi/6]]
MOUNT_HOLES=[circle(.015,12,x,y) for x,y in MOUNT_CENTRES]
G[BODY]=perforated(circle(BASE_RADIUS,48),MOUNT_HOLES,0,BASE_TOP,0,'One original broad low disc with three complete twelve-sided through holes; continuous finite upper and lower faces, complete thickness and bore side walls.')
G[COLLAR]=annulus(.122,.155,.035,.061,1,'One continuous thick annular collar with an actual open centre; full lower base seat and full upper shell-rim seat.')
OUTER=[(.061,.153,0),(.076,.153,0),(.084,.146,.009),(.190,.131,.009),(.222,.110,.006),(.245,.075,.003),(.264,.040,0)]
INNER=[(.061,.128),(.078,.128),(.184,.112),(.214,.093),(.237,.061),(.244,.038)]
G[SHELL]=shell_geometry(OUTER,INNER,2,'One original shared-vertex twelve-ridge thick dome shell, complete closed top and bottom annulus; real blind cavity opens down in the isolated shell and is occluded by the assembled base. All ridges are continuous wall geometry.')
FEET=[BODY];SUPPORT_ROOTS=FEET
contact('CollarFullLowerAnnularSeat',BODY,COLLAR,(0,0,0),(0,0,1),.035,[(.139*math.cos(a),.139*math.sin(a),.035) for a in ANGLES[::4]],.0285)
contact('DomeFullLowerRimOnCollar',COLLAR,SHELL,(0,0,0),(0,0,1),.061,[(.140*math.cos(a),.140*math.sin(a),.061) for a in ANGLES[::4]],.0219)
for i,(x,y) in enumerate(MOUNT_CENTRES,1):
 air(f'MountingHole{i}CompleteThroughAir',prism(circle(.0135,12,x,y),-.0015,.0365),'Complete finite twelve-sided hole volume, full installation-disc thickness and both mouths; every actual bore is unoccupied.')
 BORES.append({'mesh':BODY,'origin_m':(x,y,-.0015),'direction':(0,0,1),'length_m':.038})
# Entire assembled blind cavity. Inset 1.5 mm at the complete floor, stepped
# collar mouth, side/shoulder facets and closed inner ceiling; no rotor/solid fill.
CAVITY_PROFILE=[(.0365,.1205),(.0625,.1205),(.0625,.1265),(.078,.1265),(.184,.1105),(.214,.0915),(.237,.0595),(.2425,.0365)]
air('WholeInstalledBlindCavity',lathe(CAVITY_PROFILE),'Whole closed finite installed blind cavity, including the lower collar passage, full ring ledge transition and upper shoulder/cap region. The base occludes visual access; no hollow-glass or optical claim.')
ISOLATED_VOID_VOLUMES['IsolatedDomeFullDownOpenBlindCavity']=dict(lathe([(.0595,.1265),(.078,.1265),(.184,.1105),(.214,.0915),(.237,.0595),(.2425,.0365)]),targets=[SHELL],role='Complete finite isolated dome cavity through its lower open mouth and all the way to the closed inner ceiling; base and collar excluded only for this isolated-shell proof.')
air('WholePeripheralRadialAir',annulus(.158,.182,.0365,.2655),'Complete finite circumferential radial noncontact corridor outside the collar and every dome rib, above the base and below/above the complete dome height.')
air('WholeBaseToDomeLowerPeripheralAir',annulus(.157,.237,.0365,.0595),'Complete finite under-rim peripheral clearance above the disc and outside the collar; all circumferential positions, full positive axial depth.')
# Complete finite material bodies cover the full base, collar, shell top/rim and
# every integral ridge, rather than a few sampled solid points.
SOLID_VOLUMES['CompleteDiscMaterialCore']=dict(perforated(circle(.238,48),[circle(.017,12,x,y) for x,y in MOUNT_CENTRES],.002,.033),targets=[BODY],role='Full finite inset perforated installation-disc material core, including all bridges around the three holes and centre.')
SOLID_VOLUMES['CompleteCollarMaterialCore']=dict(annulus(.124,.153,.037,.059),targets=[COLLAR],role='Whole continuous finite annular support material core, all 360 degrees and full substantial depth.')
SO=[(z+(.002 if i==0 else -.002 if i==len(OUTER)-1 else 0),r-.002,a) for i,(z,r,a) in enumerate(OUTER)]
SI=[(z+(.002 if i==0 else .002 if i==len(INNER)-1 else 0),r+.002) for i,(z,r) in enumerate(INNER)]
SOLID_VOLUMES['CompleteRibbedShellMaterialCore']=dict(shell_geometry(SO,SI),targets=[SHELL],role='One complete inset thick shell material volume, including entire circumferential lower annulus, all twelve ridge bodies, every shoulder and closed top; not a collection of sample witnesses.')
MOUNT={'plane_m':0.,'plate_lo':[-.26,-.26,-.018],'plate_hi':[.26,.26,0.],'minimum_patch_area_m2':.178}
MOUNT_CONTACT={'name':'CompleteBottomInstallationFace','a':'TemporaryQA_SupportPlate_NotAsset','b':BODY,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':0.,'minimum_patch_area_m2':.178,'interior_probe_offset_m':.0005,'points':[(0,0,0),(.10,0,0),(-.10,0,0),(0,.10,0)]}
CONTRACT={'single_prop_count':1,'closed_components':3,'mounting_through_holes':3,'integral_outer_ridges':12,'dome_shell_meshes':1,'closed_top':True,'true_blind_cavity':True,'finite_annular_contacts':2,'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'mounting_plane_z_m':0,'temporary_support_exported':False,'opaque_nonemitting_static_only':True}
def measure_beacon_geometry(vertices):
 assert set(vertices)==set(G)
 assert abs(min(p[2] for p in vertices[BODY]))<2e-7 and abs(max(p[2] for p in vertices[BODY])-.035)<2e-7
 assert abs(min(p[2] for p in vertices[SHELL])-.061)<2e-7 and abs(max(p[2] for p in vertices[SHELL])-.264)<2e-7
 return dict(CONTRACT,geometry_scope='actual source/exported coordinates; complete shell/ridge material and cavity/hole volumes, whole opposed mounting and independent actual negatives remain required')
INSIDE_TESTS=[(BODY,(0,0,.02),(0,-.20,.02)),(COLLAR,(.140,0,.048),(0,0,.048)),(SHELL,(.139,0,.09),(0,0,.15))]
FOCUS=(0,0,.123);ORTHO=.66
CAMERAS={'gray-front3q':(.72,-1.45,.91),'gray-back3q':(-.72,1.45,.91),'thumbnail':(.72,-1.45,.91),'qa-front':(0,-1.5,.75),'qa-side':(1.5,0,.75),'qa-top':(0,0,1.8),'qa-back':(0,1.5,.75),'qa-wireframe':(.72,-1.45,.91),'silhouette-128-front':(0,-1.5,.75),'silhouette-128-side':(1.5,0,.75)}
WIRE_THICKNESS=ORTHO/1500

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
root=bpy.data.objects.new('OneRibbedDomeWarningBeacon',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally centred complete installation underside, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in INSIDE_TESTS:
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_beacon_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'beacon_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/firefighting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'firefighting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
