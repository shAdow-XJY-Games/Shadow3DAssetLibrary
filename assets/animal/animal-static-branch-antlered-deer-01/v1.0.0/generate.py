"""Original static branch-antlered deer. One full prop, fixed artistic pose.
No rig, animation, species precision, biological accuracy or real stability claim.
"""
import math,json,hashlib,sys,time,collections,itertools,copy
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='animal-static-branch-antlered-deer-01';VERSION='1.0.0';TITLE='Static Branch-Antlered Deer'
DESCRIPTION=('One original complete static stylized antlered deer: a long continuous tapered torso carried by four narrow joint-shaped legs with full flat dark hoof soles, an ascending long neck supporting a small cheeked head and tapered muzzle with integral nose, two outward pointed thick ears, a short tapered tail, and two complete thick branching antlers. Each antler is one continuous closed branched solid with a rising beam and three distinct offshoot tines. Eyes, inner ears, nose and hooves are integral face materials. Thirteen closed editable meshes meet at twelve complete finite planar joints. Four full ground soles, entire finite material domains, antler clefts, leg spaces and all noncontact pairs are tested against the exported geometry. Five opaque matte constant PBR colors. Metres, native Z up, front -Y, ground origin horizontally bounds centred. One prop, zero scenes or variants. Entire animal geometry is newly authored; no rabbit, tortoise, bird or carousel-horse geometry reused. No fur, textures, separate eyes, clothing, pedestal, vegetation, rig, skeleton or animation. Fixed artistic appearance only; no real species identification, anatomical or biological precision, ecology, animal behaviour, locomotion, physical stability, manufacturing, safety or old-asset compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='LongTaperedDeerTorso';NECK='AscendingSlenderNeck';HEAD='SmallCheekedHead_IntegralEyes';MUZZLE='TaperedMuzzle_IntegralNose';TAIL='ShortTaperedTail';LEGS=[];EARS=[];ANTLERS=[];RINGS={}
PALETTE=[('Fur_Chestnut',(.32,.155,.065,1),.90,0),('ThroatMuzzle_WarmCream',(.68,.51,.33,1),.92,0),('Antlers_WarmIvory',(.64,.52,.34,1),.88,0),('EyesNoseHooves_DeepBrown',(.025,.018,.012,1),.72,0),('InnerEars_MutedSienna',(.38,.22,.13,1),.94,0)]
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




BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,mat=0,role='whole finite closed prism'):
 m=Mesh();v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
 for f in BOX_FACES:m.quad(*[v[i] for i in f],mat,'WholeFiniteFace')
 return m.result(role)
def cap(m,p,mat,tag):
 c=tuple(sum(x[k] for x in p)/len(p) for k in range(3))
 for a,b in zip(p,p[1:]+p[:1]):m.tri([c,a,b],mat,tag)
def loft(rings,mat,role,eyes=False,ear=False,nose=False):
 m=Mesh();cap(m,rings[0],3 if nose else mat,'IntegralNoseFace' if nose else 'CompleteFirstEnd');cap(m,rings[-1],mat,'CompleteLastEnd')
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  for i in range(len(a)):
   j=(i+1)%len(a);p=[a[i],a[j],b[j],b[i]]
   if eyes and k==0 and i in[3,7]:
    c=tuple(sum(x[d] for x in p)/4 for d in range(3));q=[add(c,mul(sub(x,c),.30)) for x in p]
    for h in range(4):v=(h+1)%4;m.quad(p[h],p[v],q[v],q[h],mat,'IntegralEyeSurround')
    m.quad(*q,3,'IntegralDarkEye')
   else:m.quad(*p,4 if ear and i==5 and k<len(rings)-2 else mat,'IntegralInnerEarFace' if ear and i==5 and k<len(rings)-2 else 'WholeContinuousFacet')
 return m.result(role)
def xy(x,y,z,rx,ry):return [(x+rx*math.cos((i+.5)*math.tau/8)/math.cos(math.pi/8),y+ry*math.sin((i+.5)*math.tau/8)/math.cos(math.pi/8),z) for i in range(8)]
def xz(x,y,z,rx,rz):return [(x+rx*a,y,z+rz*b) for a,b in [(1,.4),(.65,1),(-.65,1),(-1,.4),(-1,-.4),(-.65,-1),(.65,-1),(1,-.4)]]
def yz(x,y,z,ry,rz):return [(x,y+ry*math.cos((i+.5)*math.tau/8)/math.cos(math.pi/8),z+rz*math.sin((i+.5)*math.tau/8)/math.cos(math.pi/8)) for i in range(8)]
def part(name,rr,mat,role,**kw):G[name]=loft(rr,mat,role,**kw);RINGS[name]=rr

def contact(name,a,b,axis,p,area):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else(1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'minimum_patch_area_m2':area-2e-7,'complete_interface_area_m2':area,'points':[p],'interior_probe_offset_m':.0004})
def polyarea(p,axis):return abs(sum(dot(cross(a,b),axis) for a,b in zip(p,p[1:]+p[:1])))/2
# All broad constant belly panels are at z=.91; four legs terminate there.
bodyrr=[xz(0,-.65,1.21,.20,.25),xz(0,-.48,1.21,.28,.30),xz(0,.44,1.21,.28,.30),xz(0,.64,1.22,.22,.25)]
part(BODY,bodyrr,0,'Whole long tapered deer torso, continuous belly and shoulder with four complete underside leg seats.')
neckrr=[xz(0,-.92,1.76,.09,.10),xz(0,-.80,1.54,.115,.25),xz(0,-.65,1.21,.15,.17)]
part(NECK,neckrr,1,'Whole ascending slender neck, complete chest joint and full small-head bearing, no floating head.')
contact('WholeTorsoNeckSeat',BODY,NECK,(0,-1,0),(0,-.65,1.21),polyarea(neckrr[-1],(0,-1,0)))
headrr=[xz(0,-1.23,1.79,.095,.075),xz(0,-1.12,1.80,.14,.14),xz(0,-.92,1.80,.14,.14)]
part(HEAD,headrr,0,'Whole elongated small head with integral dark side eyes, full neck seat, flat antler crown and two ear seats.',eyes=True)
contact('WholeNeckHeadSeat',NECK,HEAD,(0,-1,0),(0,-.92,1.76),polyarea(neckrr[0],(0,-1,0)))
muzzlerr=[xz(0,-1.49,1.755,.05,.048),xz(0,-1.38,1.765,.07,.058),xz(0,-1.23,1.79,.08,.06)]
part(MUZZLE,muzzlerr,1,'Whole tapered long muzzle with integral dark nose end and complete head attachment.',nose=True)
contact('WholeHeadMuzzleSeat',HEAD,MUZZLE,(0,-1,0),(0,-1.23,1.79),polyarea(muzzlerr[-1],(0,-1,0)))
for sx,side in[(-1,'Left'),(1,'Right')]:
 for yy,label in[(-.40,'Fore'),(.38,'Hind')]:
  leg=side+label+'ContinuousLegAndHoof';LEGS.append(leg);FEET.append(leg)
  rr=[xy(sx*.13,yy-.025,0,.055,.075),xy(sx*.13,yy-.025,.09,.055,.075),xy(sx*.13,yy,.16,.028,.035),xy(sx*.13,yy+(.025 if label=='Hind' else -.015),.43,.030,.032),xy(sx*.13,yy,.66,.035,.036),xy(sx*.13,yy,.91,.048,.055)]
  part(leg,rr,0,'Whole continuous narrow deer leg, shaped hock/knee and integral dark full-ground hoof.')
  g=G[leg];g['face_materials']=[3 if tag=='CompleteFirstEnd' or (i>=16 and i<32) else 0 for i,tag in enumerate(g['face_tags'])]
  contact(side+label+'WholeLegTorsoSeat',leg,BODY,(0,0,1),(sx*.13,yy,.91),polyarea(rr[-1],(0,0,1)))
 ear=side+'OutwardPointedThickEar';EARS.append(ear)
 rr=[yz(sx*.14,-1.02,1.80,.065,.033),yz(sx*.24,-1.01,1.88,.105,.055),yz(sx*.38,-.99,1.94,.035,.018),yz(sx*.405,-.99,1.95,.008,.006)]
 part(ear,rr,0,'Whole thick outward pointed ear with full head side joint and integral muted inner-face color.',ear=True)
 contact(side+'WholeHeadEarSeat',HEAD,ear,(sx,0,0),(sx*.14,-1.02,1.80),polyarea(rr[0],(sx,0,0)))
tailrr=[xz(0,.64,1.22,.06,.07),xz(0,.77,1.25,.055,.055),xz(0,.88,1.22,.025,.03)]
part(TAIL,tailrr,1,'Whole short tapered posterior tail with complete finite torso interface.')
contact('WholeTorsoTailSeat',BODY,TAIL,(0,1,0),(0,.64,1.22),polyarea(tailrr[0],(0,1,0)))
# One explicit complete branched outline per antler. The four endpoints
# are terminal beam plus three offshoots; no intersecting stacked cylinders.
ANTLER_POLYGON=[(.015,1.94),(.050,1.94),(.13,2.10),(.26,2.26),(.42,2.44),(.57,2.66),(.64,2.88),(.615,2.91),(.54,2.70),(.43,2.58),(.36,2.80),(.33,2.805),(.36,2.52),(.25,2.39),(.19,2.60),(.16,2.60),(.18,2.32),(.09,2.20),(.04,2.40),(.01,2.40),(.035,2.12),(.015,2.05)]
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def triangulate_polygon(poly):
 order=list(range(len(poly)));area=sum(cross2(a,b) for a,b in zip(poly,poly[1:]+poly[:1]));
 if area<0:order.reverse()
 out=[]
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a=order[j-1];c=order[(j+1)%len(order)]
   if cross2(sub(poly[b],poly[a]),sub(poly[c],poly[b]))<1e-12:continue
   def within(q):return all(cross2(sub(y,x),sub(q,x))>=-1e-12 for x,y in[(poly[a],poly[b]),(poly[b],poly[c]),(poly[c],poly[a])])
   if any(within(poly[q]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,'Cannot triangulate antler polygon'
 out.append(tuple(order));return out
ANTLER_FACES=triangulate_polygon(ANTLER_POLYGON)
def inset_polygon(p,d):
 # Intersect successive inward offset lines; exact boundary-corresponding inset.
 area=sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1]));sign=1 if area>0 else -1;out=[]
 for i,q in enumerate(p):
  prev=p[i-1];nxt=p[(i+1)%len(p)];a=unit(sub(q,prev));b=unit(sub(nxt,q));na=(-a[1]*sign,a[0]*sign);nb=(-b[1]*sign,b[0]*sign);v=add(q,mul(na,d));w=add(q,mul(nb,d));den=cross2(a,b)
  out.append(add(v,mul(a,cross2(sub(w,v),b)/den)))
 return out
def antler_mesh(poly,sx,depth,mat,role):
 m=Mesh()
 def v(p,side):
  x,z=p;return (sx*x,-1.02+.080*(z-1.94)+.10*(x-.0325)+side*depth/2,z)
 for i,j,k in triangulate_polygon(poly):
  m.tri([v(poly[t],-1) for t in[i,j,k]],mat,'CompleteBranchedFront');m.tri([v(poly[t],1) for t in[i,j,k]],mat,'CompleteBranchedBack')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad(v(a,-1),v(b,-1),v(b,1),v(a,1),mat,'WholeBranchedThickness')
 return m.result(role)
for sx,side in[(-1,'Left'),(1,'Right')]:
 name=side+'CompleteFourTipBranchedAntler';ANTLERS.append(name)
 G[name]=antler_mesh(ANTLER_POLYGON,sx,.050,2,'One complete thick branching antler: whole rising beam, three offshoots and four distinct terminal tips, continuous through every fork.')
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(antler_mesh(inset_polygon(ANTLER_POLYGON,.004),sx,.034,0,'Whole inward offset continuous antler material domain through all branch levels'),targets=[name])
 contact(side+'WholeCrownAntlerSeat',HEAD,name,(0,0,1),(sx*.0325,-1.02,1.94),.035*.050)
# Whole inset material domains retain every bend and every full cross-section.
for name,rings in RINGS.items():
 inset=[]
 for ring in rings:
  c=tuple(sum(p[k] for p in ring)/8 for k in range(3));inset.append([add(c,mul(sub(p,c),.80)) for p in ring])
 inset[0]=[add(a,mul(sub(b,a),.06)) for a,b in zip(inset[0],inset[1])];inset[-1]=[add(a,mul(sub(b,a),.06)) for a,b in zip(inset[-1],inset[-2])]
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(loft(inset,0,'Whole inset continuous loft material'),targets=[name])
VOID_VOLUMES['WholeUnderLongBellyAir']=dict(box((-.06,-.47,.02),(.06,.46,.85)),targets=None)
VOID_VOLUMES['WholeBetweenFrontHindLegsAir']=dict(box((-.24,-.27,.02),(.24,.25,.80)),targets=None)
VOID_VOLUMES['WholeBetweenAntlerCrownsAir']=dict(box((-.007,-1.04,1.98),(.007,-.94,2.80)),targets=None)
for sx,side in[(-1,'Left'),(1,'Right')]:
 for j,(x,z) in enumerate([(.09,2.32),(.25,2.50),(.42,2.68)]):
  lo,hi=sorted([sx*(x-.013),sx*(x+.013)]);VOID_VOLUMES[side+'AntlerBranchCleft'+str(j+1)]=dict(box((lo,-1.09,z-.015),(hi,-.87,z+.015)),targets=None)
SHIFT_Y=.305
for group in[G,SOLID_VOLUMES,VOID_VOLUMES]:
 for g in group.values():g['vertices']=[(p[0],p[1]+SHIFT_Y,p[2]) for p in g['vertices']]
for r in CONTACTS:r['plane_m']+=r['axis'][1]*SHIFT_Y;r['points']=[(p[0],p[1]+SHIFT_Y,p[2]) for p in r['points']]
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','closed_meshes':len(G),'materials':5,'continuous_long_torso':1,'ascending_long_neck':1,'small_cheeked_head':1,'tapered_muzzle':1,'continuous_slender_legs_and_hooves':4,'outward_thick_ears':2,'complete_branched_antlers':2,'offshoots_per_antler':3,'tips_per_antler':4,'short_tail':1,'finite_opposed_contacts':len(CONTACTS),'whole_material_volumes':len(SOLID_VOLUMES),'whole_air_volumes':len(VOID_VOLUMES),'full_ground_soles':len(FEET),'old_geometry_imports':0,'rig_animation_or_species_claim':False,'ordinary_opaque_PBR':True,'static_visual_only':True}
def measure_deer_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for v in vertices.values() for p in v];assert abs(min(p[2] for p in vv))<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],scope='Producer geometry only; separately decoded actual-GLB full finite predicates govern acceptance')
INSIDE_TESTS=[(BODY,(0,SHIFT_Y,1.21),(3,3,4)),(HEAD,(0,-1.05+SHIFT_Y,1.8),(3,3,4)),(TAIL,(0,.77+SHIFT_Y,1.25),(3,3,4))]
FOCUS=(0,0,1.42);ORTHO=3.90
CAMERAS={'gray-front3q':(4,-6,3.6),'gray-back3q':(-4,6,3.6),'thumbnail':(4,-6,3.6),'qa-front':(0,-6,2.8),'qa-side':(6,0,2.8),'qa-top':(0,0,7),'qa-back':(0,6,2.8),'qa-wireframe':(-4,6,3.6),'silhouette-128-front':(0,-6,2.8),'silhouette-128-side':(6,0,2.8)}
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
root=bpy.data.objects.new('OneStaticBranchAntleredDeer',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='four full deer hoof soles at Z0; horizontal bounds centred';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# and whole-surface nonpenetration remain separate maker-self-reviewed actual-GLB gates.
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
mount_evidence=measure_deer_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'static_deer_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/animal/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'animal','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)



# BEGIN AUTHORIZED TIERED RENDER V1; native has already been saved at128.
def tier_arg(flag,default=None):
 if flag not in sys.argv:return default
 i=sys.argv.index(flag);assert i+1<len(sys.argv);return sys.argv[i+1]
TIER_PROFILE=tier_arg('--render-profile')
TIER_ALLOWED={'simple-v1':(16,[16,32,64]),'complex-v1':(32,[32,64])}
TIER_SINGLE=tier_arg('--tier-single-view')
TIER_LIST=json.loads(tier_arg('--tier-view-list','[]'))
TIER_OVERRIDES=json.loads(tier_arg('--tier-sample-overrides','{}'))
TIER_STANDARD=['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']
if TIER_PROFILE:
 assert TIER_PROFILE in TIER_ALLOWED and '--gray-only' not in sys.argv and '--gray-obliques-only' not in sys.argv
 assert isinstance(TIER_OVERRIDES,dict)
 for k,v in TIER_OVERRIDES.items():assert k in CAMERAS and k!='thumbnail' and type(v) is int and v in TIER_ALLOWED[TIER_PROFILE][1]
 assert isinstance(TIER_LIST,list) and len(TIER_LIST)==len(set(TIER_LIST)) and not(TIER_LIST and TIER_SINGLE)
 assert all(n in TIER_STANDARD[1:] and n in CAMERAS for n in TIER_LIST)
 if TIER_SINGLE:assert TIER_SINGLE in CAMERAS and TIER_SINGLE not in ['gray-front3q','gray-back3q','silhouette-128-front','silhouette-128-side']
 qa['tiered_render']={'profile_id':TIER_PROFILE,'authorization_reference':'Sentinel_f2fcc66115e881918d02bc1ea780953c','native_samples':128,'resolution':[640,640],'gray_stage':'omitted_by_authorized_profile','samples_by_image':{}}
def tier_select_views(views):
 if not TIER_PROFILE:return views
 if TIER_SINGLE:return {TIER_SINGLE:CAMERAS[TIER_SINGLE]}
 if TIER_LIST:return {n:CAMERAS[n] for n in TIER_LIST}
 assert set(views)<=set(TIER_STANDARD)
 return views
def tier_before_view(name):
 if not TIER_PROFILE:return
 samples=128 if name=='thumbnail' else TIER_OVERRIDES.get(name,TIER_ALLOWED[TIER_PROFILE][0])
 assert samples==128 if name=='thumbnail' else samples in TIER_ALLOWED[TIER_PROFILE][1]
 scene.cycles.samples=samples
 EXPECTED['samples']=samples
 qa['tiered_render']['samples_by_image'][name+'.png']=samples
# END AUTHORIZED TIERED RENDER V1
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
 views=tier_select_views(views)
 seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
 def render(name,pos):
  tier_before_view(name)
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
