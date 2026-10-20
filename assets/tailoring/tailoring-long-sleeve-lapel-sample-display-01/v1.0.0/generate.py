"""Original long-sleeve hollow sample with open cuffs, V neck and thick returned lapels."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='tailoring-long-sleeve-lapel-sample-display-01';VERSION='1.0.0';TITLE='Long-Sleeve Lapel Sample Display'
DESCRIPTION=('One original complete static tailoring sample display with a continuous three-dimensional hollow torso and two long down-sloping sleeve chambers that communicate with the torso and terminate in genuinely open cuffs. The body has a narrowed waist, flared open hem, full inner surfaces and a deep V-shaped front neckline. Two thick outward-returned lapels and one standing rear collar give the neckline a distinct folded form. A newly authored narrow internal twin-pad yoke supports the complete shoulder undersides on finite seats, with a slender central post and one full grounded base; no mannequin fills the garment. All seven closed editable meshes together count as one prop and zero scenes. Four opaque constant untextured PBR materials; native Z up, front -Y, metres, base-centred ground origin. No existing garment, clothesline shirt, character clothing or hanger geometry is imported, stretched or recolored. Fixed visual appearance only: no wearable or body-size fit, dressing action, cloth simulation, sewing pattern, manufacturing, removal/assembly path, material strength, load/stability, safety certification or compatibility claim. No text, logo, texture, animation, rig, floor or background exported.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousHollowLongSleeveBody';YOKE='DedicatedInternalShoulderYoke';POST='NarrowDisplayPost';BASE='CompleteGroundBase';COLLAR='StandingRearCollar';LAPELS=['ReturnedLapelLeft','ReturnedLapelRight']
PALETTE=[('Sample_DeepPetrol',(.075,.23,.27,1),.87,0),('CollarAndCuffs_MutedBlue',(.18,.36,.39,1),.87,0),('Yoke_WarmAsh',(.52,.36,.20,1),.67,0),('Stand_Graphite',(.05,.068,.071,1),.48,.35)]
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
# Entirely new numeric construction; no prior garment vertices imported.
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
Z_KNOTS=[.62,.88,1.12,1.17,1.40]
W_SHAPE=[(.62,.300),(.88,.250),(1.12,.280),(1.40,.280)]
def interp(z,points):
 if z<=points[0][0]:return points[0][1]
 if z>=points[-1][0]:return points[-1][1]
 for (a,x),(b,y) in zip(points,points[1:]):
  if a<=z<=b:return x+(y-x)*(z-a)/(b-a)
def shaped(p):
 x,y,z=p;s=-1 if x<0 else 1;a=abs(x);w=interp(z,W_SHAPE);neck=interp(z,[(.62,.11),(1.17,.025),(1.40,.11)])
 if a<=.11:xx=a*neck/.11
 elif a<=.28:xx=neck+(a-.11)*(w-neck)/.17
 else:xx=w+a-.28
 return(s*xx,y,z-max(0,a-.28)*.58)
def stations(a,b,knots):return sorted(set([a,b]+[x for x in knots if a<x<b]))
def grid(xs,ys,zs,occupied,mat=0,role='',transform=lambda p:p,cuff=False):
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};m=Mesh()
 for i,j,k in sorted(cells):
  cell=[(x,y,z) for z in zs[k:k+2] for y in ys[j:j+2] for x in xs[i:i+2]]
  for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:
    pts=[cell[n] for n in face];material=1 if cuff and min(abs(p[0]) for p in pts)>.6599 else mat;m.quad(*[transform(p) for p in pts],material,'WholeWeldedBoundary')
 return m.result(role)
def shaped_grid(xs,ys,zs,occupied,mat=0,role='',cuff=False):
 xs=sorted(set(xs+[x for x in[-.28,-.11,.11,.28] if min(xs)<x<max(xs)]));zs=sorted(set(zs+[z for z in Z_KNOTS if min(zs)<z<max(zs)]))
 return grid(xs,ys,zs,occupied,mat,role,shaped,cuff)
def shaped_box(lo,hi,mat=0,role=''):
 return shaped_grid([lo[0],hi[0]],[lo[1],hi[1]],[lo[2],hi[2]],lambda x,y,z:True,mat,role)
def garment(e=0,role=''):
 xs=sorted(set([-v for v in [.73-e,.66,.28-e,.272+e,.11+e]]+[v for v in [.73-e,.66,.28-e,.272+e,.11+e]]))
 ys=sorted(set([-v for v in [.145-e,.137+e,.115-e,.107+e,.085+e]]+[v for v in [.145-e,.137+e,.115-e,.107+e,.085+e]]))
 zs=sorted(set([.62+e,1.12+e,1.128-e,1.17-e,1.362+e,1.37-e,1.392+e,1.40-e]))
 def occupied(x,y,z):
  outer=(abs(x)<.28-e and abs(y)<.145-e and .62+e<z<1.40-e) or (abs(x)<.73-e and abs(y)<.115-e and 1.12+e<z<1.37-e)
  inside=(abs(x)<.272+e and abs(y)<.137+e and z<1.392+e) or (abs(x)>.272-e and abs(y)<.107+e and 1.128-e<z<1.362+e)
  neck=abs(x)<.11+e and y<.085+e and z>1.17-e
  return outer and not inside and not neck
 return shaped_grid(xs,ys,zs,occupied,0,role,cuff=True)
def contact(name,a,b,axis,plane,area,points):
 axis=tuple(axis);u=(1,0,0) if abs(axis[2]) else (0,0,1);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':.0004})
def solid(name,g,target,role='Whole inset material'):
 SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
def air(name,g,targets=None,isolated=False):
 d=ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES;d[name]=dict(g,targets=targets if targets else list(G),role='Whole finite empty domain, complete boundary and containment tested')
G[BODY]=garment(0,'One continuous welded hollow body with two whole sleeve chambers, open cuffs, open hem and V-neckline; complete thick material rims and inner/outer surfaces.')
G[BASE]=box((-.19,-.16,0),(.19,.16,.035),3,'One complete ground base with whole finite underside.');FEET.append(BASE)
G[POST]=shaped_box((-.012,-.012,.035),(.012,.012,1.295),3,'Thin central post through open hem; no mannequin body.')
G[YOKE]=shaped_grid([-.22,-.15,.15,.22],[-.052,-.022,.022,.052],[1.295,1.327,1.392],lambda x,y,z:(abs(y)<.022 and z<1.327) or (abs(x)>.15 and z>=1.327),2,'One continuous narrow bridge and two broad finite shoulder pads.')
contact('WholePostBaseSeat',BASE,POST,(0,0,1),.035,.0005759,[(0,0,.035)])
contact('WholeYokePostSeat',POST,YOKE,(0,0,1),1.295,.000339,[(0,0,1.295)])
for sign,label in[(-1,'Left'),(1,'Right')]:contact(label+'WholeShoulderPad',YOKE,BODY,(0,0,1),1.392,.0072798,[(sign*.185,0,1.392)])
# Raised U collar wraps the neck sides and back; its front is truly open.
def rear_collar(e=0):
 return grid([-.134+e,-.118-e,.118+e,.134-e],[-.080+e,.087+e,.103-e],[1.40+e,1.482-e],lambda x,y,z:abs(x)>.118+e or y>.087+e,1,'Complete thick U-shaped standing collar with front mouth and full neck clearance.')
G[COLLAR]=rear_collar();contact('WholeCollarShoulderSeat',BODY,COLLAR,(0,0,1),1.40,.0093758,[(.126,0,1.40),(-.126,0,1.40),(0,.095,1.40)])
# The two fold-back lapels have distinct angled outer faces and closed thickness.
LAPEL_POLY=[(.028,1.175),(.205,1.245),(.168,1.398),(.113,1.398),(.086,1.327)]
def lapel(sign,e=0):
 poly=offset(LAPEL_POLY,e) if e else LAPEL_POLY;m=Mesh()
 def front(p):x,z=p;return -.145-(.014+.16*(z-1.175))+e
 def back(p):return -.145-e
 for side in[front,back]:
  for tri in earclip(poly):m.tri([(sign*poly[i][0],side(poly[i]),poly[i][1]) for i in tri],1,'WholeReturnedLapelFace')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad((sign*a[0],front(a),a[1]),(sign*b[0],front(b),b[1]),(sign*b[0],back(b),b[1]),(sign*a[0],back(a),a[1]),1,'WholeLapelFoldThickness')
 return m.result('Closed outward-thickening folded lapel with a finite back seat on the front body; no floating decal.')
for sign,name in zip([-1,1],LAPELS):
 G[name]=lapel(sign);contact(name+'WholeBodyFrontSeat',name,BODY,(0,1,0),-.145,.012,[(sign*.155,-.145,1.28)])
solid('WholeBodyIncludingBothSleevesAndAllOpenRims',garment(.0012),BODY)
solid('WholeBase',box((-.1888,-.1588,.0012),(.1888,.1588,.0338),3),BASE)
solid('WholePost',shaped_box((-.010,-.0108,.0362),(.010,.0108,1.2938),3),POST)
# Connected inset yoke explicitly preserves both pad roots and the whole bridge.
solid('WholeYokeAndPads',shaped_grid([-.2188,-.1512,.1512,.2188],[-.0508,-.0208,.0208,.0508],[1.2962,1.3258,1.3282,1.3908],lambda x,y,z:(abs(y)<.0208 and z<1.3258) or(abs(x)>.1512 and (abs(y)<.0208 or z>1.3282)),2),YOKE)
solid('WholeStandingCollar',rear_collar(.0012),COLLAR)
for sign,name in zip([-1,1],LAPELS):solid(name+'WholeMaterial',lapel(sign,.0012),name)
# Continuous isolated torso chamber includes the full shape, from open hem to shoulder undersides.
air('WholeIsolatedTorsoChamber',shaped_box((-.2708,-.1358,.618),(.2708,.1358,1.3908)),[BODY],True)
for sign,label in[(-1,'Left'),(1,'Right')]:
 lo,hi=sorted([sign*.2696,sign*.732]);air('Whole'+label+'SleeveChamberAndOpenCuff',shaped_box((lo,-.1058,1.1292),(hi,.1058,1.3608)),None)
# Complete V opening in front and the top portal, isolated from support by definition.
air('WholeVNeckAndTopPortal',shaped_grid([-.108,.108],[-.191,-.136,.0838],[1.1712,1.3908,1.484],lambda x,y,z:y<-.136 or z>1.3908),[BODY,COLLAR,*LAPELS])
EXCLUSIONS=[((-.014,-.0132,.617),(.014,.0132,1.2962)),((-.2212,-.0232,1.2938),(.2212,.0232,1.3282)),((-.2212,-.0532,1.3258),(-.1488,.0532,1.3932)),((.1488,-.0532,1.3258),(.2212,.0532,1.3932))]
def cavity_without_support(lo,hi):
 st=[stations(lo[k],hi[k],[p[k] for pair in EXCLUSIONS for p in pair]) for k in range(3)]
 # All support and exclusion surfaces use the same complete shape map.
 return shaped_grid(*st,lambda x,y,z:not any(all(a[k]<p<b[k] for k,p in enumerate([x,y,z])) for a,b in EXCLUSIONS))
air('WholeTorsoAirAroundDedicatedSupport',cavity_without_support((-.2708,-.1358,.6212),(.2708,.1358,1.3908)))
air('WholeOpenHemAroundThinPost',cavity_without_support((-.2708,-.1358,.618),(.2708,.1358,.6212)))
air('WholeStandingCollarMouth',box((-.1168,-.140,1.4012),(.1168,.0858,1.484)),[COLLAR])
# Both whole finite underarm gaps remain empty, distinct from the sleeve chambers.
for sign,label in[(-1,'Left'),(1,'Right')]:
 lo,hi=sorted([sign*.315,sign*.705]);air('Whole'+label+'UnderarmGap',shaped_box((lo,-.103,.68),(hi,.103,1.1188)))
SHIFT=(0,0,0)
INSIDE_TESTS=[(BODY,(.20,-.141,1.02),(0,0,1.02)),(COLLAR,(0,.095,1.44),(0,0,1.44)),(POST,(0,0,.70),(.035,0,.70))]
EXPECTED_EULER={BODY:-4,BASE:2,POST:2,YOKE:2,COLLAR:2,**{n:2 for n in LAPELS}}
CONTRACT={'single_prop_count':1,'new_scene_count':0,'closed_connected_material_meshes':7,'continuous_hollow_body_shells':1,'communicating_long_sleeve_chambers':2,'open_cuffs':2,'deep_V_neckline':1,'thick_returned_lapels':2,'standing_open_rear_collar':1,'dedicated_full_shoulder_seats':2,'finite_ground_bases':1,'whole_material_volumes':len(SOLID_VOLUMES),'whole_air_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'finite_opposed_contacts':len(CONTACTS),'old_geometry_imports':0,'nominal_main_material_thickness_m':.008,'wearable_or_cloth_simulation_claim':False}
def measure_garment_geometry(vertices):
 assert set(vertices)==set(G);v=vertices[BODY];assert max(p[0] for p in v)-min(p[0] for p in v)>1.45 and max(p[1] for p in v)-min(p[1] for p in v)>.28
 assert abs(min(p[2] for p in vertices[BASE]))<2e-7
 return dict(CONTRACT,scope='Complete actual finite source/export triangles; complete material/void/contact predicates separately required.')
FOCUS=(0,0,.741);ORTHO=1.95
CAMERAS={'gray-front3q':(3.0,-5.0,2.65),'gray-back3q':(-3.0,5.0,2.65),'thumbnail':(3.0,-5.0,2.65),'qa-front':(0,-7,2.45),'qa-side':(7,0,2.45),'qa-top':(0,0,8),'qa-back':(0,7,2.45),'qa-wireframe':(-3.0,5.0,2.65),'silhouette-128-front':(0,-7,2.45),'silhouette-128-side':(7,0,2.45)}
WIRE_THICKNESS=ORTHO/1600
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
root=bpy.data.objects.new('OneLongSleeveLapelSampleDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='one complete base sole at Z=0; continuous open-cuff long-sleeve body, folded lapels, open neckline and thin internal yoke';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_garment_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'collared_garment_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/tailoring/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'tailoring','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
