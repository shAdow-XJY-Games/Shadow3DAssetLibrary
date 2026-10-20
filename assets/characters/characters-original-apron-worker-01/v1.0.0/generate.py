"""Original generic adult worker. One static low-poly character prop; no rig or IP."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='characters-original-apron-worker-01';VERSION='1.0.0';TITLE='Original Apron Workshop Worker'
DESCRIPTION=('One original generic adult worker in a fixed relaxed standing pose, wearing a plain short-sleeve shirt, long work trousers, a thick continuous bib apron and complete low work shoes. A faceted shaped head has an integral angular nose, readable eyes and mouth formed by material regions on the same closed surface, cropped hair and a complete neck. Both full arms terminate in thumb-shaped closed hands; both separated full legs terminate in independent flat grounded shoes. All body joints meet on finite opposed surfaces without penetrating ellipsoids. The apron has a continuous full-width waist and low hem with two integrated front shoulder-strap color regions on the shirt. All clothing is fixed visual geometry, with no hidden body or replaceable garment system. Native Z up, front -Y, metres as game-space scale and origin between the two soles. Entire geometry newly authored, not an existing toy, tabletop player, mannequin, real person or established character. One prop, zero scenes. Six opaque untextured constant PBR materials. No rig, bones, skinning, animation, locomotion, behavior, dressing or interchangeable outfit, demographic likeness, anatomical/ergonomic accuracy, physical stability, manufacturability or safety certification is claimed. No tools, held objects, logo, text, textures, floor or background are exported.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='FullShirtTorso';HEAD='ShapedAdultHead';NECK='CompleteNeck';PELVIS='TrouserHipBridge';APRON='ContinuousThickBibApron';LEGS=[];ARMS=[];HANDS=[]
PALETTE=[('Skin_WarmOchre',(.49,.285,.16,1),.83,0),('Shirt_UnbleachedIvory',(.72,.68,.55,1),.87,0),('Trousers_DeepOlive',(.105,.15,.12,1),.84,0),('Apron_MutedCopper',(.43,.20,.075,1),.88,0),('HairAndFace_Espresso',(.035,.024,.018,1),.86,0),('Shoes_CharcoalLeather',(.055,.070,.065,1),.68,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
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



def area2(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2

def offset(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);L=math.hypot(*e);lines.append(((a[0]-d*e[1]/L,a[1]+d*e[0]/L),e))
 out=[]
 for i,(q,v) in enumerate(lines):
  p,u=lines[i-1];den=u[0]*v[1]-u[1]*v[0]
  if abs(den)<1e-14:out.append(q);continue
  t=((q[0]-p[0])*v[1]-(q[1]-p[1])*v[0])/den;out.append((p[0]+t*u[0],p[1]+t*u[1]))
 return out

def earclip(p):
 order=list(range(len(p))) if area2(p)>0 else list(reversed(range(len(p))));out=[]
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(p[a],p[b],p[c])<1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)]) for k in order if k not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('untriangulable',p,order)
 out.append(tuple(order));return out

def extrude_x(poly,x0,x1,mat=0,role='Complete closed extruded material'):
 m=Mesh()
 for x in [x0,x1]:
  for tri in earclip(poly):m.tri([(x,*poly[i]) for i in tri],mat,'CompleteEndSection')
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad((x0,*p),(x0,*q),(x1,*q),(x1,*p),mat,'CompleteExtrusionWall')
 return m.result(role)
def box(lo,hi,mat=1,role='Complete rectangular closed solid'):
 m=Mesh();v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
 for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.quad(*[v[i] for i in f],mat,'CompleteBoxFace')
 return m.result(role)

def contact(name,a,b,axis,plane,area,points):
 axis=tuple(axis);u=(1,0,0) if abs(axis[2]) else (0,0,1);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':plane,'points':points,'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.0004})
def section(cx,cy,rx,ry,z):
 return[(cx-rx*.72,cy-ry,z),(cx+rx*.72,cy-ry,z),(cx+rx,cy-ry*.60,z),(cx+rx,cy+ry*.60,z),(cx+rx*.72,cy+ry,z),(cx-rx*.72,cy+ry,z),(cx-rx,cy+ry*.60,z),(cx-rx,cy-ry*.60,z)]
def loft(rings,mat,role):
 m=Mesh();n=len(rings[0]);assert all(len(r)==n for r in rings)
 for ring in [rings[0],rings[-1]]:
  center=tuple(sum(p[k] for p in ring)/n for k in range(3))
  for p,q in zip(ring,ring[1:]+ring[:1]):m.tri([center,p,q],mat,'WholeClosedEnd')
 for j,(ra,rb) in enumerate(zip(rings,rings[1:])):
  for i in range(n):k=(i+1)%n;m.quad(ra[i],ra[k],rb[k],rb[i],mat,'WholeSurface_'+str(j)+'_'+str(i))
 return m.result(role)
def mirror(g,sign):
 if sign<0:g=dict(g,vertices=[(-p[0],p[1],p[2]) for p in g['vertices']],faces=[tuple(reversed(f)) for f in g['faces']])
 return g
def add_part(name,g,center=None,shrink=.975):
 G[name]=g
 if center is None:center=tuple(sum(p[k] for p in g['vertices'])/len(g['vertices']) for k in range(3))
 q=dict(g,vertices=[tuple(center[k]+(p[k]-center[k])*shrink for k in range(3)) for p in g['vertices']],targets=[name])
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=q
# Adult proportions: 1.78m full height, 0.30m head, 0.43m shoulders and two long legs.
def shirt_section(rx,z):
 front=[(rx*f,-.13,z) for f in[-.72,-.58,-.37,.37,.58,.72]]
 return front+[(rx,-.078,z),(rx,.078,z),(rx*.72,.13,z),(-rx*.72,.13,z),(-rx,.078,z),(-rx,-.078,z)]
torso=[shirt_section(.173,1.05),shirt_section(.190,1.20),shirt_section(.204583333,1.27),shirt_section(.215,1.32),shirt_section(.215,1.40)]
add_part(BODY,loft(torso,1,'Complete closed shaped shirt torso; flat finite shoulder sides, full waist seat and neck seat.'))
add_part(PELVIS,loft([section(0,0,.185,.119,.86),section(0,0,.182,.125,.96),section(0,0,.173,.13,1.05)],2,'Complete continuous trouser hip bridge joins both separately bounded legs and full shirt waist.'))
contact('WholeWaistSeat',PELVIS,BODY,(0,0,1),1.05,.08492224,[(0,0,1.05)])
add_part(NECK,loft([section(0,0,.055,.052,1.40),section(0,0,.055,.052,1.48)],0,'Whole complete neck, full upper and lower horizontal anatomical joins.'))
contact('WholeNeckBase',BODY,NECK,(0,0,1),1.40,.01079936,[(0,0,1.40)])
# The front head surface is a non-overlaid sculpted grid; nose and facial regions belong to it.
HEAD_ROWS=[(1.48,.070,.065),(1.52,.086,.078),(1.555,.102,.094),(1.570,.106,.096),(1.579,.107,.097),(1.600,.108,.100),(1.620,.110,.100),(1.638,.110,.100),(1.653,.110,.100),(1.672,.109,.102),(1.700,.105,.100),(1.745,.091,.085),(1.780,.066,.063)]
XF=[-.72,-.56,-.33,-.18,0,.18,.33,.56,.72]
rings=[]
for z,rx,ry in HEAD_ROWS:
 front=[]
 for f in XF:
  nose=max(0,1-abs(f)/.33)*max(0,1-abs(z-1.620)/.045)*.037
  front.append((rx*f,-ry-nose,z))
 rings.append(front+[(rx,-ry*.55,z),(rx,ry*.50,z),(rx*.70,ry,z),(-rx*.70,ry,z),(-rx,ry*.50,z),(-rx,-ry*.55,z)])
g=loft(rings,0,'Complete faceted adult head; jaw, cheeks, continuous projecting nose and cropped scalp. Face uses continuous material-region topology.')
for i,f in enumerate(g['faces']):
 pts=[g['vertices'][j] for j in f];c=tuple(sum(p[k] for p in pts)/3 for k in range(3));x,y,z=c
 if z>=1.70-1e-9 or (y>.035 and z>1.57) or (abs(x)>.09 and z>1.67):g['face_materials'][i]=4
 # Two readable eyes and a short neutral mouth are actual face regions, not discs.
 if y<-.091 and 1.638<z<1.653 and .033<abs(x)<.063:g['face_materials'][i]=4
 if y<-.09 and 1.570<z<1.579 and abs(x)<.019:g['face_materials'][i]=4
add_part(HEAD,g,center=(0,0,1.63),shrink=.96)
contact('WholeNeckHeadSeat',NECK,HEAD,(0,0,1),1.48,.01079936,[(0,0,1.48)])
# Integral front shoulder-strap regions: no extra coincident surfaces or separate garment system.
for i,f in enumerate(G[BODY]['faces']):
 pts=[G[BODY]['vertices'][j] for j in f];c=tuple(sum(p[k] for p in pts)/3 for k in range(3))
 # Face tessellation is intentionally coarse; a complete dark warm shoulder band continues over shoulders.
 if c[2]>1.27 and c[1]<-.12 and .07<abs(c[0])<.13:G[BODY]['face_materials'][i]=3
# A continuous thick apron sheet with tapered bib, shaped waist and a visibly hanging hem.
APRON_ROWS=[(.70,.155,-.157),(.83,.164,-.146),(.96,.165,-.134),(1.05,.155,-.134),(1.06,.152863636,-.130),(1.27,.108,-.130)]
loops=[]
for z,rx,back in APRON_ROWS:loops.append([(-rx,back-.008,z),(rx,back-.008,z),(rx,back,z),(-rx,back,z)])
G[APRON]=loft(loops,3,'One closed 8mm thick bib apron, full connected hanging hem, tapered bib and finite upper torso seat.')
inset=[]
for i,(zz,rr,bb) in enumerate(APRON_ROWS):
 z=zz+(.0012 if i==0 else -.0012 if i==len(APRON_ROWS)-1 else 0)
 if i==0:other=APRON_ROWS[1]
 elif i==len(APRON_ROWS)-1:other=APRON_ROWS[-2]
 else:other=(zz+1,rr,bb)
 t=(z-zz)/(other[0]-zz);rx=rr+t*(other[1]-rr)-.0015;back=bb+t*(other[2]-bb)
 inset.append([(-rx,back-.0065,z),(rx,back-.0065,z),(rx,back-.0015,z),(-rx,back-.0015,z)])
SOLID_VOLUMES[APRON+'_WholeInsetMaterial']=dict(loft(inset,3,'Complete inset apron material'),targets=[APRON])
contact('FullBibTorsoSeat',APRON,BODY,(0,1,0),-.130,.052222159375,[(0,-.130,1.15)])
# Full arms have planar cut joints and separated hand silhouettes.
for sign,label in[(-1,'Left'),(1,'Right')]:
 sleeve='ShortSleeve_'+label;fore='FullForearm_'+label;hand='ThumbedHand_'+label
 g=loft([section(.310,0,.055,.070,1.17),section(.280,0,.065,.078,1.32),section(.280,0,.065,.078,1.40)],1,'Complete tapered shirt sleeve, full shoulder-side join and complete cuff seat.')
 add_part(sleeve,mirror(g,sign));ARMS.append(sleeve)
 contact(label+'FullShoulderSide',BODY,sleeve,(sign,0,0),.215,.08*.0936,[(sign*.215,0,1.36)])
 g=loft([section(.3475,-.012,.0325,.033,.97),section(.339,-.005,.044,.046,1.075),section(.310,0,.050,.060,1.17)],0,'Whole faceted forearm from sleeve cuff to complete wrist, no elbow/skin overlap.')
 add_part(fore,mirror(g,sign));ARMS.append(fore)
 contact(label+'WholeSleeveCuff',fore,sleeve,(0,0,1),1.17,.011328,[(sign*.31,0,1.17)])
 poly=[(.315,.97),(.380,.97),(.397,.925),(.400,.845),(.385,.820),(.333,.825),(.320,.870),(.292,.860),(.282,.884),(.298,.920),(.315,.930)]
 # extrude_x uses a YZ profile; remap its axis to the hand thickness Y.
 q=extrude_x(poly,-.045,.021,0,'Whole closed palm and integral broad thumb; fingers are a single stylized block, no articulated fingers.')
 q=dict(q,vertices=[(p[1],p[0],p[2]) for p in q['vertices']],faces=[tuple(reversed(f)) for f in q['faces']]);q=mirror(q,sign)
 G[hand]=q;HANDS.append(hand)
 qq=extrude_x(offset(poly,.0012),-.0438,.0198,0,'Whole inset palm and thumb material')
 qq=dict(qq,vertices=[(p[1],p[0],p[2]) for p in qq['vertices']],faces=[tuple(reversed(f)) for f in qq['faces']]);SOLID_VOLUMES[hand+'_WholeInsetMaterial']=dict(mirror(qq,sign),targets=[hand])
 contact(label+'WholeWrist',hand,fore,(0,0,1),.97,.00404976,[(sign*.3475,-.012,.97)])
 leg='FullTrouserLeg_'+label;shoe='CompleteGroundShoe_'+label;LEGS.append(leg);FEET.append(shoe)
 g=loft([section(.108,0,.056,.060,.16),section(.112,.003,.060,.065,.38),section(.108,0,.067,.072,.58),section(.108,0,.075,.095,.86)],2,'Whole separated trouser leg, tapered ankle and knee, full hip and ankle joins.')
 add_part(leg,mirror(g,sign));contact(label+'WholeHipLeg',leg,PELVIS,(0,0,1),.86,.026890566528,[(sign*.108,0,.86)])
 g=loft([section(.108,-.044,.072,.151,0),section(.108,-.044,.072,.151,.035),section(.108,-.043,.073,.148,.070),section(.108,-.012,.066,.108,.115),section(.108,0,.062,.069,.16)],5,'Complete flat-soled low work shoe with projecting toe, shaped instep and full ankle seat; no hollow unworn boot.')
 for i,f in enumerate(g['faces']):
  if max(g['vertices'][j][2] for j in f)<=.035+1e-9:g['face_materials'][i]=4
 add_part(shoe,mirror(g,sign));contact(label+'WholeAnkleShoe',shoe,leg,(0,0,1),.16,.01268736,[(sign*.108,0,.16)])
# The actual gap is a complete finite box from ground to the crotch, inset from both legs/shoes.
VOID_VOLUMES['WholeBetweenLegsAndShoes']=dict(box((-.030,-.115,.002),(.030,.095,.858)),targets=None)
for sign,label in[(-1,'Left'),(1,'Right')]:
 lo,hi=sorted([sign*.188,sign*.252]);VOID_VOLUMES[label+'WholeLowerArmTorsoGap']=dict(box((lo,-.035,.83),(hi,.035,1.16)),targets=None)
INSIDE_TESTS=[(BODY,(0,0,1.2),(3,3,3)),(HEAD,(0,0,1.63),(3,3,3)),(NECK,(0,0,1.44),(3,3,3)),(PELVIS,(0,0,.96),(3,3,3))]
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','origin':'midpoint between two ground shoe soles','closed_meshes':len(G),'materials':6,'complete_adult_heads':1,'complete_necks':1,'complete_torso_and_pelvis':1,'complete_arms_and_hands':2,'separated_full_legs':2,'complete_flat_ground_shoes':2,'continuous_thick_bib_aprons':1,'full_finite_contacts':len(CONTACTS),'whole_material_domains':len(SOLID_VOLUMES),'whole_gap_domains':len(VOID_VOLUMES),'old_geometry_imports':0,'rigs_animations_behaviors':0,'fixed_visual_only':True}
def measure_worker_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for vs in vertices.values() for p in vs];assert abs(min(p[2] for p in vv))<2e-7
 assert abs(max(p[2] for p in vv)-1.78)<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],scope='Producer shape only. Complete actual-GLB geometry/PBR and raw-image character recognition govern acceptance; no rig or motion.')
FOCUS=(0,-.02,.89);ORTHO=2.18
CAMERAS={'gray-front3q':(3.5,-6,2.7),'gray-back3q':(-3.5,6,2.7),'thumbnail':(3.5,-6,2.7),'qa-front':(0,-7,2.35),'qa-side':(7,0,2.35),'qa-top':(0,0,8),'qa-back':(0,7,2.35),'qa-wireframe':(-3.5,6,2.7),'silhouette-128-front':(0,-7,2.35),'silhouette-128-side':(7,0,2.35)}
WIRE_THICKNESS=ORTHO/1800
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
root=bpy.data.objects.new('OneOriginalAdultApronWorker',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='two complete shoe soles at Z=0, front -Y, fixed original adult character';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# and whole-surface nonpenetration remain separate maker actual-GLB gates.
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
mount_evidence=measure_worker_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=4000
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'original_worker_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/characters/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'characters','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker visual/native/clean gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
