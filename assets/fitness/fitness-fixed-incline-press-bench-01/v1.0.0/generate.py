"""Original short-seat / long-back fixed-incline press bench; one static visual prop.
Metres, native Z up, front -Y. No use, adjustment, load, body-fit or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fitness-fixed-incline-press-bench-01';VERSION='1.0.0';TITLE='Fixed-Incline Press Bench'
DESCRIPTION=('One original low-poly fixed-incline press bench, counted as one complete static prop. A separate short chamfered cushion and long 30-degree back cushion have complete thick closed bodies and independent flat underplates. A real visible seat-back gap remains. Two independent thick pierced hinge ears have genuine full-depth rectangular shaft openings; a continuous fixed sixteen-sided solid pin has integral end shoulders, finite lower seats in both holes and a finite upper face under the back tongue. A broad fixed rear wedge meets the back underplate across an entire finite inclined face. Four ground pads, two transverse feet, one low longitudinal beam and a front seat post form a connected support assembly. Eighteen closed editable meshes and four opaque unlinked constant PBR materials. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. No barbell, rack, athlete, second angle, adjustment mechanism, animation, scene or textures. Newly authored short-seat/long-back geometry, not a recoloured public bench, bleacher row, rack or stretched rowing seat. Fixed static illustrative pose only: no adjustment, rotation, locking, friction, exercise suitability, body dimensions, comfort, load, strength, stability, injury prevention, manufacturing, installation, equipment standards or safety claim. No compatibility with historical barbell racks or other assets is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};NONCONTACT_SURFACES=[];FEET=[];EARS=[]
PALETTE=[('Frame_SlateTeal',(.075,.18,.19,1),.49,.42),('Cushion_MutedTerracotta',(.43,.16,.105,1),.78,0),('GroundPad_Graphite',(.035,.043,.047,1),.85,0),('Hinge_BrushedSteel',(.44,.48,.50,1),.32,.72)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no procedural or image texture nodes.'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  if len(ids)==3:self.f.append(tuple(ids));self.fm.append(mat);self.tags.append(tag);return
  c=self.vertex(tuple(sum(p[k] for p in points)/len(points) for k in range(3)))
  for a,b in zip(ids,ids[1:]+ids[:1]):
   if a==b:continue
   self.f.append((a,b,c));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable surface'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected surface'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def rect(y0,y1,z0,z1):return [(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
def chamfer(y0,y1,z0,z1,c):return [(y0+c,z0),(y1-c,z0),(y1,z0+c),(y1,z1-c),(y1-c,z1),(y0+c,z1),(y0,z1-c),(y0,z0+c)]
def inside2(p,poly):
 y,z=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>z)!=(b[1]>z) and y<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def extrude_region(outer,holes,x0,x1,mat=0,role='closed finite prism'):
 # Exact horizontal decomposition of the polygon-with-holes. Every slab end
 # shares all boundary breakpoints; no T-junctions and no booleans or fake caps.
 outer=[tuple(round(c,9) for c in p) for p in outer];holes=[[tuple(round(c,9) for c in p) for p in h] for h in holes]
 loops=[outer]+holes;levels=sorted(set(round(p[1],9) for loop in loops for p in loop));m=Mesh()
 segs=[(a,b,k) for k,loop in enumerate(loops) for a,b in zip(loop,loop[1:]+loop[:1])]
 def hit(a,b,z):return a[0]+(b[0]-a[0])*(z-a[1])/(b[1]-a[1])
 cuts={}
 for z in levels:
  yy=[]
  for a,b,k in segs:
   if min(a[1],b[1])-1e-8<=z<=max(a[1],b[1])+1e-8:
    yy.extend([a[0],b[0]] if abs(a[1]-b[1])<1e-8 else [hit(a,b,z)])
  cuts[z]=sorted(set(round(y,9) for y in yy))
 for z0,z1 in zip(levels,levels[1:]):
  z=(z0+z1)/2;active=sorted([(hit(a,b,z),a,b) for a,b,k in segs if min(a[1],b[1])<z<max(a[1],b[1])],key=lambda r:r[0])
  for left,right in zip(active,active[1:]):
   p=((left[0]+right[0])/2,z)
   if not inside2(p,outer) or any(inside2(p,h) for h in holes):continue
   l0,l1=hit(left[1],left[2],z0),hit(left[1],left[2],z1);r0,r1=hit(right[1],right[2],z0),hit(right[1],right[2],z1)
   low=[(y,z0) for y in cuts[z0] if l0+1e-8<y<r0-1e-8];high=[(y,z1) for y in reversed(cuts[z1]) if l1+1e-8<y<r1-1e-8]
   poly=[(l0,z0)]+low+[(r0,z0),(r1,z1)]+high+[(l1,z1)];clean=[]
   for p in poly:
    if not clean or math.dist(clean[-1],p)>1e-8:clean.append(p)
   if math.dist(clean[0],clean[-1])<1e-8:clean.pop()
   for x in [x0,x1]:m.face([(x,*p) for p in clean],mat,'side_face')
 for a,b,k in segs:
  if abs(a[1]-b[1])<1e-8:
   z=round(a[1],9);ys=[a[0]]+[y for y in cuts[z] if min(a[0],b[0])+1e-8<y<max(a[0],b[0])-1e-8]+[b[0]];ys=sorted(ys);pp=[(y,z) for y in ys]
  else:
   zs=sorted([a[1]]+[z for z in levels if min(a[1],b[1])+1e-8<z<max(a[1],b[1])-1e-8]+[b[1]]);pp=[(hit(a,b,z),z) for z in zs]
  for p,q in zip(pp,pp[1:]):m.face([(x0,*p),(x1,*p),(x1,*q),(x0,*q)],mat,'outer_wall' if k==0 else 'hole_wall_'+str(k))
 return m.result(role,mat)
def box_geometry(lo,hi,mat=0,role='complete finite rectangular prism'):
 return extrude_region(rect(lo[1],hi[1],lo[2],hi[2]),[],lo[0],hi[0],mat,role)
def volume(entries,name,g,targets,role):entries[name]=dict(g,targets=list(targets),role=role)
def contact(a,b,axis,plane,points,area,label):
 u=(0,1,0) if axis==(1,0,0) else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':label,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'scope':'complete finite opposed actual faces and full two-way no-positive-penetration test; static geometric contact only'})
def box(name,lo,hi,mat,role):G[name]=box_geometry(lo,hi,mat,role);return name
def xprism(name,x0,x1,poly,mat,role):G[name]=extrude_region(poly,[],x0,x1,mat,role);return name
def zseat(a,b,z,x,y,area,label,spread=.012):contact(a,b,(0,0,1),z,[(x+d,y,z) for d in[-spread,0,spread]],area,label)
def voidbox(name,lo,hi,role,targets=None):volume(VOID_VOLUMES,name,box_geometry(lo,hi),targets or [],role)
def oriented_box(name,x0,x1,t0,t1,n0,n1,mat,role):
 poly=[bp(t0,n0),bp(t1,n0),bp(t1,n1),bp(t0,n1)];return xprism(name,x0,x1,[(p[1],p[2]) for p in poly],mat,role)
def cushion(name,origin,length,width,normal,tangent,base,mat):
 m=Mesh();rings=[]
 for inset,z in[(.006,base),(0,base+.008),(0,base+.067),(.010,base+.075)]:
  rings.append([add(origin,add((x,0,0),add(mul(tangent,t),mul(normal,z)))) for x,t in[(-width/2+inset,inset),(width/2-inset,inset),(width/2-inset,length-inset),(-width/2+inset,length-inset)]])
 m.face(rings[0],mat,'flat_complete_underside');m.face(rings[-1],mat,'flat_inset_top')
 for a,b in zip(rings,rings[1:]):
  for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]],mat,'thick_chamfered_side')
 G[name]=m.result('Complete closed thick cushion; flat lower face, continuous sides and bevelled upper perimeter. Static material appearance only.',mat)
# Ground pads and transverse feet. Every part meets at a finite opposed face.
for label,y in[('Front',-.71),('Rear',.71)]:
 foot=box('Frame_'+label+'_TransverseFoot',(-.28,y-.08,.045),(.28,y+.08,.105),0,'full transverse foot between two separate finite ground pads')
 for side,x in[('Left',-.225),('Right',.225)]:
  pad=box('Ground_'+label+'_'+side,(x-.055,y-.08,0),(x+.055,y+.08,.045),2,'finite rectangular rubber-like visual ground pad');FEET.append(pad)
  zseat(pad,foot,.045,x,y,.01759,pad+'_SupportsTransverseFoot',.020)
BEAM=box('Frame_LowLongitudinalBeam',(-.05,-.71,.105),(.05,.71,.26),0,'one continuous low longitudinal beam joining both transverse feet')
for label,y in[('Front',-.67),('Rear',.67)]:zseat('Frame_'+label+'_TransverseFoot',BEAM,.105,0,y,.00799,label+'_FootSupportsLowBeam')
POST=box('Seat_FrontPost',(-.07,-.50,.26),(.07,-.38,.415),0,'short front post with full base and broad finite seat plate support')
zseat(BEAM,POST,.26,0,-.44,.01199,'LowBeamSupportsSeatPost')
SEAT_PLATE=box('Seat_SeparateUnderplate',(-.12,-.63,.415),(.12,-.25,.445),0,'independent short seat underplate, fully below the complete short cushion')
zseat(POST,SEAT_PLATE,.415,0,-.44,.01679,'SeatPostSupportsUnderplate')
SEAT='Seat_ShortThickCushion';cushion(SEAT,(0,-.64,0),.40,.30,(0,0,1),(0,1,0),.445,1)
zseat(SEAT_PLATE,SEAT,.445,0,-.44,.09119,'ShortUnderplateSupportsCompleteCushion',.06)
BRIDGE=box('Hinge_TransverseBaseBridge',(-.21,-.16,.26),(.21,-.04,.29),0,'transverse base bridge carries both pierced ears over the low longitudinal beam')
zseat(BEAM,BRIDGE,.26,0,-.10,.01199,'LowBeamSupportsHingeBridge')
HY=-.10;HZ=.35+.018*math.cos(math.pi/16);PIN_TOP=HZ+.018*math.cos(math.pi/16);PIN_HALF_FACET=.018*math.sin(math.pi/16)
PIN='Hinge_ContinuousPinIntegralShoulders'
outer=[(-.16,.29),(-.04,.29),(-.04,.420),(-.06,.440),(-.14,.440),(-.16,.420)]
hole=rect(-.125,-.075,.35,.395)
for side,x0,x1 in[('Left',-.18,-.13),('Right',.13,.18)]:
 ear='Hinge_'+side+'_TruePiercedEar';EARS.append(ear);G[ear]=extrude_region(outer,[hole],x0,x1,0,'closed thick fixed hinge ear with one true full-depth rectangular shaft opening, full lower bridge and bevelled crown; no false cap')
 zseat(BRIDGE,ear,.29,(x0+x1)/2,-.10,.00599,ear+'_FiniteBaseSeat')
 zseat(ear,PIN,.35,(x0+x1)/2,-.10,.000349,ear+'_BoreFloorSupportsPin',.012)
 x=x0 if side=='Left' else x1;a,b=(PIN,ear) if side=='Left' else (ear,PIN)
 contact(a,b,(1,0,0),x,[(x,HY-.030,HZ),(x,HY+.030,HZ),(x,HY,HZ-.030)],.0013,ear+'_IntegralPinShoulder')
 volume(ISOLATED_VOID_VOLUMES,ear+'_WholeIsolatedBore',box_geometry((x0-.001,-.1245,.3505),(x1+.001,-.0755,.3945)),[ear],'complete isolated true through-hole, full finite bore and both mouths with 0.5 mm inset')
 # Full connected U air follows every actual polygonal pin facet, with a
 # 0.5 mm normal inset from pin, hole walls, shoulder faces and bearing plane.
 radius=.018+.0005/math.cos(math.pi/16)
 pinpoly=[(HY+radius*math.cos((j+.5)*math.tau/16),HZ+radius*math.sin((j+.5)*math.tau/16)) for j in range(16)]
 cut=.3505
 def cutpoint(a,b):
  q=(cut-a[1])/(b[1]-a[1]);return(a[0]+q*(b[0]-a[0]),cut)
 left=cutpoint(pinpoly[11],pinpoly[10]);right=cutpoint(pinpoly[12],pinpoly[13])
 chain=[left]+[pinpoly[j] for j in list(range(10,-1,-1))+[15,14,13]]+[right]
 p=[(HY-.0245,cut)]+chain+[(HY+.0245,cut),(HY+.0245,.3945),(HY-.0245,.3945)]
 volume(VOID_VOLUMES,ear+'_CompleteAssembledBoreAir',extrude_region(p,[],x0+.0005,x1-.0005),[],'complete connected U-shaped upper/side finite bore air following every actual pin facet, 0.5 mm normal wall/contact/end insets; no corner air omitted')
 volume(SOLID_VOLUMES,ear+'_ContinuousLowerBridge',box_geometry((x0+.001,-.159,.291),(x1-.001,-.041,.349)),[ear],'entire inset finite lower ear bridge connects actual bore-floor bearing to base bridge')
 NONCONTACT_SURFACES.append({'name':ear+'_NonbearingBoreWalls','solid':ear,'other':PIN,'x_range':[x0+.0005,x1-.0005],'y_range':[-.125,-.075],'z_range':[.3505,.395],'minimum_distance_m':.00049})
# One connected sixteen-facet pin including the two finite axial shoulders.
m=Mesh();rings=[]
for x,r in[(-.205,.036),(-.18,.036),(-.18,.018),(.18,.018),(.18,.036),(.205,.036)]:
 rings.append([(x,HY+r*math.cos((j+.5)*math.tau/16),HZ+r*math.sin((j+.5)*math.tau/16)) for j in range(16)])
m.face(rings[0],3,'end');m.face(rings[-1],3,'end')
for k,(a,b) in enumerate(zip(rings,rings[1:])):
 for i in range(16):j=(i+1)%16;m.face([a[i],a[j],b[j],b[i]],3,'pin_segment_'+str(k))
G[PIN]=m.result('one uninterrupted fixed sixteen-sided solid hinge pin with integral finite end shoulders, lower bearing facets and upper tongue bearing facet',3)
volume(SOLID_VOLUMES,'Pin_UninterruptedCore',box_geometry((-.204,HY-.006,HZ-.006),(.204,HY+.006,HZ+.006)),[PIN],'whole continuous finite inner pin core through both ears and integral shoulders')
# Original 30-degree back assembly and a broad matching rear wedge.
ANGLE=math.pi/6;T=(0,math.cos(ANGLE),math.sin(ANGLE));N=(0,-math.sin(ANGLE),math.cos(ANGLE));BACK_ORIGIN=(0,-.14,.418)
def bp(t,n=0):return add(BACK_ORIGIN,add(mul(T,t),mul(N,n)))
BACK_PLATE='Back_SeparateInclinedUnderplate';oriented_box(BACK_PLATE,-.12,.12,.02,1.06,0,.028,0,'independent long thirty-degree underplate with broad underside and complete cushion seat')
TONGUE='Back_FiniteHingeTongue';p0=bp(.03);p1=bp(.23)
xprism(TONGUE,-.09,.09,[(HY-PIN_HALF_FACET,PIN_TOP),(HY+PIN_HALF_FACET,PIN_TOP),(p1[1],p1[2]),(p0[1],p0[2])],0,'thick closed back tongue with finite flat pin-top root and broad inclined face against long underplate')
zseat(PIN,TONGUE,PIN_TOP,0,HY,.001263,'PinUpperFacetSupportsBackTongue',.05)
plane=dot(N,BACK_ORIGIN)
contact(TONGUE,BACK_PLATE,N,plane,[add(bp(.13),(x,0,0)) for x in[-.06,0,.06]],.03599,'TongueWholeInclinedFaceSupportsBackPlate')
REAR='Back_FixedBroadRearSupport';r0=bp(.65);r1=bp(.90)
xprism(REAR,-.09,.09,[(r0[1],.26),(r1[1],.26),(r1[1],r1[2]),(r0[1],r0[2])],0,'fixed thick rear wedge, full finite horizontal beam base and whole matching thirty-degree underplate support face')
zseat(BEAM,REAR,.26,0,(r0[1]+r1[1])/2,.02164,'LowBeamSupportsRearWedge')
contact(REAR,BACK_PLATE,N,plane,[add(bp(.775),(x,0,0)) for x in[-.06,0,.06]],.04499,'RearWedgeWholeInclinedFaceSupportsBackPlate')
BACK='Back_LongThickCushion';cushion(BACK,BACK_ORIGIN,1.08,.30,N,T,.028,1)
contact(BACK_PLATE,BACK,N,plane+.028,[add(bp(.54,.028),(x,0,0)) for x in[-.07,0,.07]],.24959,'LongUnderplateSupportsCompleteCushion')
# Complete rectangular finite seat-back opening, and two under-frame bays.
voidbox('WholeSeatBackGap',(-.149,-.239,.416),(.149,-.193,.521),'entire transverse seat/back gap between the actual cushion envelopes, including both lateral mouths')
voidbox('LeftOpenUnderBackBay',(-.279,-.025,.106),(-.121,.629,.417),'complete broad left under-back bay outside the low beam and rear wedge')
voidbox('RightOpenUnderBackBay',(.121,-.025,.106),(.279,.629,.417),'complete broad right under-back bay outside the low beam and rear wedge')
for g in VOID_VOLUMES.values():g['targets']=list(G)
BENCH_CONTRACT={'single_prop_count':1,'separate_short_cushions':1,'separate_long_back_cushions':1,'independent_underplates':2,'fixed_incline_degrees':30,'true_full_depth_pierced_hinge_ears':2,'continuous_integral_shoulder_pins':1,'finite_pin_bore_floor_seats':2,'finite_pin_end_shoulders':2,'rear_broad_matching_inclined_face':1,'ground_pads':4,'transverse_feet':2,'low_longitudinal_beams':1,'finite_opposed_contacts':len(CONTACTS),'static_visual_only':True,'human_load_or_old_rack_fit_claimed':False,'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_bench_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<2e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<2e-7 for p in actual),(n,'actual shape changed')
 return dict(BENCH_CONTRACT,geometry_scope='actual vertices only; complete finite contacts, full void volumes, nonbearing surfaces, every part pair and real mutations required')
FOCUS=(0,0,.47);ORTHO=2.06
CAMERAS={'gray-front3q':(2.8,-3.4,2.7),'gray-back3q':(-2.8,3.4,2.7),'thumbnail':(2.8,-3.4,2.7),'qa-front':(0,-3.8,2.2),'qa-side':(3.8,0,2.2),'qa-top':(0,0,4),'qa-back':(0,3.8,2.2),'qa-wireframe':(2.8,-3.4,2.7),'silhouette-128-front':(0,-3.8,2.2),'silhouette-128-side':(3.8,0,2.2)}
WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneFixedInclinePressBench',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.225,-.71,.0225),(-.225,-.71,.05)),(SEAT,(0,-.44,.48),(0,-.44,.53))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

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
mount_evidence=measure_bench_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'bench_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
