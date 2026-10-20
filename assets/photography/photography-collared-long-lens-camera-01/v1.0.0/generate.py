"""Original continuous grip/shoulder camera, stepped barrel and integral bored collar-foot.
One fixed opaque visual prop. Generic export/check scaffolding only is shared.
No previous asset's visible geometry is imported or reconstructed.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-collared-long-lens-camera-01';VERSION='1.0.0';TITLE='Collared Long-Lens Camera'
DESCRIPTION=('One original fixed long-barrel camera visual prop. A continuous stepped-shoulder body includes its forward projecting right grip and complete ground sole. A finite rear mount supports one continuous multi-stage long barrel, a genuinely deep thick open hood and a full-backed recessed opaque optical-appearance disc. One continuous bored collar, narrow lower neck and broad integral foot has a real finite lower barrel bearing, complete upper/side bore clearances and its own full sole at Z=0. All numerical profiles are original, not an elongated old box camera, copied telescope or assembled earlier parts. Five constant opaque unlinked PBR materials, no textures, transmission or real optical glass. Metres, native Z up, front -Y, entire horizontal envelope centred. One fixed static form only, no tripod, rail, bag, strap, scene or text. No focal length, optical path, imaging, focus, zoom, motion, brand, interchangeable mount, compatibility, load, stability, safety, manufacturing or physical performance claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FOOT_CONTACTS=[]
BODY='ContinuousShoulderGripBody';MOUNT='FiniteRearLensMount';BARREL='ContinuousSteppedLongBarrel';HOOD='ThickDeepOpenHood';DISC='RecessedOpaqueOpticalAppearance';COLLAR='ContinuousBoredCollarNeckFoot';FEET=[BODY,COLLAR]
PALETTE=[('WarmGraphiteBody',(.062,.073,.078,1),.67,0),('DarkGripAndHood',(.029,.036,.040,1),.82,0),('WarmIvoryBarrel',(.58,.59,.52,1),.62,0),('BrushedDarkMount',(.19,.22,.23,1),.42,.30),('OpaqueDeepTealOpticalAppearance',(.025,.075,.081,1),.26,.12)]
SHIFT=(-.01,.4175,0.);CX=-.06;CZ=.28;N=24
BODY_STATIONS=[(-.34,-.10,.38),(-.29,-.10,.415),(-.19,-.10,.415),(-.15,-.10,.49),(.045,-.10,.49),(.09,-.10,.415),(.17,-.10,.415),(.205,-.22,.425),(.32,-.22,.425),(.36,-.18,.38)]
BARREL_STATIONS=[(-.15,.106),(-.21,.106),(-.245,.130),(-.565,.130),(-.59,.145),(-.685,.145),(-.71,.160),(-.745,.174)]
COLLAR_Y=(-.49,-.36);HOOD_Y=(-1.015,-.745);DISC_Y=(-.765,-.745)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(poly):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2
def world(p):return add(p,SHIFT)
def point(p,y):return world((p[0],y,p[1]))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat,tag):self.f.append(tuple(self.vertex(x) for x in p));self.fm.append(mat);self.tags.append(tag)
 def quad(self,a,b,c,d,mat,tag):self.tri([a,b,c],mat,tag);self.tri([a,c,d],mat,tag)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),('not closed',[(k,v) for k,v in edges.items() if len(v)!=2][:8])
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}
def earclip2(poly):
 order=list(range(len(poly))) if area2(poly)>0 else list(reversed(range(len(poly))));out=[]
 def cr(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  ok=False
  for j,b in enumerate(order):
   a=order[j-1];c=order[(j+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-13:continue
   if any(all(cr(poly[u],poly[v],poly[q])>=-1e-13 for u,v in [(a,b),(b,c),(c,a)]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);ok=True;break
  assert ok,('untriangulable polygon',poly,order)
 out.append(tuple(order));return out

def circle(r):return [(CX+r*math.cos(-math.pi/2+math.pi/N+2*math.pi*i/N),CZ+r*math.sin(-math.pi/2+math.pi/N+2*math.pi*i/N)) for i in range(N)]
def offset(poly,d):
 # Positive offsets move a CCW contour inward. The same finite line
 # intersections also offset concave neck/foot corners; no smoothing proxy.
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=(b[0]-a[0],b[1]-a[1]);l=math.hypot(*e);n=(-e[1]/l,e[0]/l);lines.append(((a[0]+d*n[0],a[1]+d*n[1]),e))
 out=[]
 for i,(q,v) in enumerate(lines):
  p,u=lines[i-1];den=u[0]*v[1]-u[1]*v[0];assert abs(den)>1e-12
  t=((q[0]-p[0])*v[1]-(q[1]-p[1])*v[0])/den;out.append((p[0]+t*u[0],p[1]+t*u[1]))
 return out

def solid_loft(loops,ys,role,mat=0):
 m=Mesh();n=len(loops[0]);assert all(len(q)==n for q in loops)
 for k in [0,len(ys)-1]:
  for tri in earclip2(loops[k]):m.tri([point(loops[k][i],ys[k]) for i in tri],mat,'End_'+str(k))
 for k in range(len(ys)-1):
  for i in range(n):
   q=(i+1)%n;m.quad(point(loops[k][i],ys[k]),point(loops[k][q],ys[k]),point(loops[k+1][q],ys[k+1]),point(loops[k+1][i],ys[k+1]),mat,'Wall_Layer_'+str(k)+'_Sector_'+str(i))
 return m.result(role)
def tube(stations,role,mat):return solid_loft([circle(r) for y,r in stations],[y for y,r in stations],role,mat)
def annulus(outer,inner,ys,role,mat=1):
 m=Mesh();n=len(inner[0]);assert all(len(q)==n for q in outer+inner)
 for k in [0,len(ys)-1]:
  for i in range(n):
   q=(i+1)%n;m.quad(point(outer[k][i],ys[k]),point(outer[k][q],ys[k]),point(inner[k][q],ys[k]),point(inner[k][i],ys[k]),mat,'AnnularEnd_'+str(k)+'_Sector_'+str(i))
 for k in range(len(ys)-1):
  for label,loops in [('OuterWall',outer),('InnerWall',inner)]:
   for i in range(n):
    q=(i+1)%n;m.quad(point(loops[k][i],ys[k]),point(loops[k][q],ys[k]),point(loops[k+1][q],ys[k+1]),point(loops[k+1][i],ys[k+1]),mat,label+'_Layer_'+str(k)+'_Sector_'+str(i))
 return m.result(role)
def body(stations,inset=0):
 m=Mesh();loops=[]
 for x,front,h in stations:
  back=.18;b=.018
  loops.append([(front+inset,inset),(back-inset,inset),(back-inset,h-b-inset),(back-b-inset,h-inset),(front+b+inset,h-inset),(front+inset,h-b-inset)])
 for k in [0,len(stations)-1]:
  for tri in earclip2(loops[k]):m.tri([world((stations[k][0],*loops[k][i])) for i in tri],0,'BodyEnd_'+str(k))
 for k in range(len(stations)-1):
  for i in range(6):
   q=(i+1)%6;mat=1 if k>=6 and i in [4,5] else 0
   m.quad(world((stations[k][0],*loops[k][i])),world((stations[k][0],*loops[k][q])),world((stations[k+1][0],*loops[k+1][q])),world((stations[k+1][0],*loops[k+1][i])),mat,'BodyStrip_'+str(k)+'_Sector_'+str(i))
 return m.result('One continuous lofted shoulder and forward grip body, complete connected bottom sole; no overlapping box grip.')
BORE=circle(.150);BEARING_Z=CZ-.130*math.cos(math.pi/N)
for i in [0,N-1]:BORE[i]=(BORE[i][0],BEARING_Z)
RING_OUTER=circle(.180)
# The lower outer ring edge is replaced by a finite neck and wide sole.
# It is one continuous boundary, not a ring plus touching detached blocks.
EXTENSION=[(CX-.0235,.055),(CX-.110,.035),(CX-.110,0),(CX+.110,0),(CX+.110,.035),(CX+.0235,.055)]
COLLAR_OUTER=RING_OUTER+EXTENSION

def collar(outer,inner,ys,role):
 m=Mesh();n=len(inner);assert len(outer)>=n+2
 for k,y in enumerate(ys):
  for i in range(n-1):m.quad(point(outer[i],y),point(outer[i+1],y),point(inner[i+1],y),point(inner[i],y),2,'CollarAnnularFace_'+str(k)+'_'+str(i))
  poly=[outer[n-1],*outer[n:],outer[0],inner[0],inner[n-1]]
  for tri in earclip2(poly):m.tri([point(poly[i],y) for i in tri],2,'IntegralNeckFootFace_'+str(k))
 for label,loop in [('CompleteOuterRingNeckFoot',outer),('CompleteBoreWall',inner)]:
  for i in range(len(loop)):
   q=(i+1)%len(loop);m.quad(point(loop[i],ys[0]),point(loop[q],ys[0]),point(loop[q],ys[1]),point(loop[i],ys[1]),2,label+'_Sector_'+str(i))
 return m.result(role)
G[BODY]=body(BODY_STATIONS)
G[MOUNT]=tube([(-.10,.100),(-.15,.100)],'Finite full-face mount between body and rear barrel.',3)
G[BARREL]=tube(BARREL_STATIONS,'One continuous multi-radius long barrel, original shoulder sequence and finite flat lower bearing facet.',2)
G[HOOD]=annulus([circle(.185),circle(.174)],[circle(.165),circle(.145)],list(HOOD_Y),'Independent genuinely through-open thick hood; complete front/back annuli and full inner/outer wall.',1)
G[DISC]=tube([(DISC_Y[0],.140),(DISC_Y[1],.140)],'Thick opaque optical-appearance disc, recessed .25 m behind the lip and completely backed by barrel; no real glass or imaging claim.',4)
G[COLLAR]=collar(COLLAR_OUTER,BORE,list(COLLAR_Y),'One continuous genus-one collar, lower neck and wide foot, real isolated bore and full flat sole.')
# Full finite material interiors for every continuous component.
bs=[(x+( .002 if i==0 else -.002 if i==len(BODY_STATIONS)-1 else 0),front,h) for i,(x,front,h) in enumerate(BODY_STATIONS)]
SOLID_VOLUMES['CompleteBodyShoulderGripInterior']=dict(body(bs,.002),targets=[BODY])
SOLID_VOLUMES['CompleteMountInterior']=dict(tube([(-.102,.098),(-.148,.098)],'Whole inset mount material',3),targets=[MOUNT])
SOLID_VOLUMES['CompleteSteppedBarrelInterior']=dict(tube([(y+(-.002 if i==0 else .002 if i==len(BARREL_STATIONS)-1 else 0),r-.002) for i,(y,r) in enumerate(BARREL_STATIONS)],'Whole inset multi-stage barrel material',2),targets=[BARREL])
SOLID_VOLUMES['CompleteHoodMaterial']=dict(annulus([circle(.18292),circle(.17208)],[circle(.16685),circle(.14715)],[-1.013,-.747],'Whole inset thick hood material, all radial and axial walls'),targets=[HOOD])
SOLID_VOLUMES['CompleteDiscMaterial']=dict(tube([(-.763,.138),(-.747,.138)],'Whole inset opaque disc material',4),targets=[DISC])
SOLID_VOLUMES['CompleteCollarNeckFootMaterial']=dict(collar(offset(COLLAR_OUTER,.0015),offset(BORE,-.0015),[-.4885,-.3615],'Whole inset continuous collar/neck/foot material, preserves complete genus-one boundary'),targets=[COLLAR])
# Full deep mouth interior from the entire recessed-disc plane to beyond the lip.
# The annular moat separately covers the entire peripheral gap beside the disc.
def hood_inner_at(y):return .145+(-.745-y)/.270*.020
VOID_VOLUMES['WholeDeepMouthAndForwardEgress']=dict(solid_loft([circle(.163),circle(.163),circle(hood_inner_at(-.767)-.002)],[-1.070,-1.015,-.767],'Entire front mouth cross-section, every depth interval and outside egress, 2mm positive boundary inset'),targets=list(G))
VOID_VOLUMES['WholeDiscPeripheralMoat']=dict(annulus([circle(hood_inner_at(-.763)-.001),circle(hood_inner_at(-.747)-.001)],[circle(.141),circle(.141)],[-.763,-.747],'Entire circumferential recessed-disc clearance, not a few sampled rays'),targets=list(G))
ISOLATED_VOID_VOLUMES['IsolatedCollarCompleteBore']=dict(solid_loft([offset(BORE,.001)]*2,[-.51,-.34],'Complete isolated collar bore with egress at both ends'),targets=[COLLAR])
ISOLATED_VOID_VOLUMES['IsolatedHoodCompleteBore']=dict(solid_loft([circle(.163),circle(.163),circle(.143),circle(.143)],[-1.035,-1.015,-.745,-.725],'Complete isolated hood bore including both end planes'),targets=[HOOD])
# Complete connected U-shaped remaining bore area. The lower coincident
# bearing chord is subtracted; both narrowing side wedges remain represented.
# All finite sides/end planes are physically inset 0.4mm, and complete
# oriented-surface correspondence covers the untested inset boundary margin.
RESIDUAL_OUTLINE=BORE+list(reversed(circle(.130)))
VOID_VOLUMES['WholeCollarRemainingBore']=dict(solid_loft([offset(RESIDUAL_OUTLINE,.0004)]*2,[-.488,-.362],'Whole connected upper/side residual collar air including both narrow lower-side wedges; exactly excludes only the finite lower bearing.'),targets=list(G))
# Every assembly joint is an exactly opposed finite patch; zero intentional
# interpenetration anywhere. No clearance or whole-surface exception for color.
def contact(name,a,b,axis,plane,point_,area):
 u=(1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':SHIFT,'u':u,'v':v,'axis':axis,'plane_m':plane,'points':[world(point_)],'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.0004})
POLY_AREA=lambda r:N*r*r*math.sin(2*math.pi/N)/2
contact('BodyFullRearMountSeat',BODY,MOUNT,(0,-1,0),.10,(CX,-.10,CZ),POLY_AREA(.100))
contact('MountFullRearBarrelSeat',MOUNT,BARREL,(0,-1,0),.15,(CX,-.15,CZ),POLY_AREA(.100))
contact('BarrelFullHoodRearAnnulus',BARREL,HOOD,(0,-1,0),.745,(CX+.152,-.745,CZ),POLY_AREA(.174)-POLY_AREA(.145))
contact('BarrelFullOpaqueDiscBack',BARREL,DISC,(0,-1,0),.745,(CX,-.745,CZ),POLY_AREA(.140))
contact('CollarCompleteLowerBarrelBearing',COLLAR,BARREL,(0,0,1),BEARING_Z,(CX,-.425,BEARING_Z),(.49-.36)*2*.130*math.sin(math.pi/N))
INSIDE_TESTS=[(BODY,world((0,0,.20)),world((.45,0,.20))),(COLLAR,world((CX, -.425,.025)),world((CX,-.425,CZ))),(HOOD,world((CX+.175,-.99,CZ)),world((CX,-.99,CZ)))]
CONTRACT={'single_prop_count':1,'original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','horizontal_shift_m':SHIFT,'body_stations_x_front_y_top_z_m':BODY_STATIONS,'barrel_stations_y_radius_m':BARREL_STATIONS,'barrel_axis_x_z_m':[CX,CZ],'hood_lip_y_m':-1.015,'disc_front_y_m':-.765,'complete_recess_depth_m':.25,'disc_thickness_m':.020,'collar_y_m':COLLAR_Y,'bearing_z_m':BEARING_Z,'bearing_width_m':2*.130*math.sin(math.pi/N),'body_and_collar_full_soles_at_z_m':0,'closed_meshes':6,'materials':5,'old_geometry_imports':0,'fixed_opaque_visual_only':True}
def measure_camera_geometry(vertices):
 assert set(vertices)==set(G)
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<2e-7
 vv=[p for vs in vertices.values() for p in vs]
 for i in [0,1]:assert abs(min(p[i] for p in vv)+max(p[i] for p in vv))<2e-7
 return dict(CONTRACT,scope='Pure source/producer geometry only; independent actual GLB gates still required')
FOCUS=(0.,0.,.245);ORTHO=1.68
CAMERAS={'gray-front3q':(2.,-3.0,1.7),'gray-back3q':(-2.,3.,1.7),'thumbnail':(2.,-3.,1.7),'qa-front':(0,-3.,1.05),'qa-side':(-3.,0.,1.1),'qa-top':(0,0,3.5),'qa-back':(0,3.,1.05),'qa-wireframe':(-2.,3.,1.7),'silhouette-128-front':(0,-3.,1.05),'silhouette-128-side':(-3.,0.,1.1)}
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
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneCollaredLongLensCamera',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete horizontal envelope centred, two complete ground soles Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_camera_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=3000
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'long_lens_camera_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/photography/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
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
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
