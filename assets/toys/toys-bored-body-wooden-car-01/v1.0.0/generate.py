"""Original thick bored wooden toy car, one static prop with four thick wood wheels."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='toys-bored-body-wooden-car-01';VERSION='1.0.0';TITLE='Bored Body Wooden Toy Car'
DESCRIPTION=('One original static low-poly wooden toy car, counted as one prop. An uninterrupted thick maple-coloured body has a short blunt nose, a high chamfer-corner roof and one genuinely open side-to-side grip window with a complete thick frame. Two independent real transverse rectangular axle bores pass through the full body. Two continuous fixed wooden axles have integral shoulders and end caps. Four thick twelve-sided wooden wheels each have a true rectangular centre bore and a finite flat ground face. Complete opposed faces connect wheel bore floors to axle undersides, axle tops to body bore ceilings, and both wheel side faces to their integral axle shoulders and caps. The remaining bore air is explicitly open finite geometry; the body bottom stays clear of the ground. Seven closed connected mesh components, three constant opaque PBR materials, metres, native Z up, bounds-centred ground origin and front -Y. No glass, cabin, tyre, cargo bed, push handle, pull cord, track, figure, scene, spare wheel, animation or texture. Newly authored toy geometry, not a scaled van, recoloured railway trolley or trimmed handcart. Static illustrative geometry only: no rolling, steering, propulsion, pulling, child age suitability, bite or material safety, swallowing or pinch protection, human grip fit, durability, load, manufacture, toy safety certification or old-asset compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};NONCONTACT_SURFACES=[]
BODY='Body_ContinuousThreeThroughBores';AXLES=[];WHEELS=[];FEET=[]
ZC=.060*math.cos(math.pi/12);AXLE_Y=[-.118,.118]
PALETTE=[('HoneyMaple_ThickBody',(.62,.365,.145,1),.64,0),('ChestnutWood_ThickWheels',(.245,.091,.028,1),.68,0),('DarkEndGrain_FixedAxles',(.100,.048,.020,1),.72,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no procedural or image texture nodes.'
FOCUS=(0,0,.105);ORTHO=.54
CAMERAS={'gray-front3q':(.75,-.85,.62),'gray-back3q':(-.75,.85,.62),'thumbnail':(.75,-.85,.62),'qa-front':(0,-1.2,.55),'qa-side':(1.2,0,.55),'qa-top':(0,0,1.3),'qa-back':(0,1.2,.55),'qa-wireframe':(.75,-.85,.62),'silhouette-128-front':(0,-1.2,.55),'silhouette-128-side':(1.2,0,.55)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
 u,v=((0,1,0),(0,0,1)) if axis==(1,0,0) else ((1,0,0),(0,1,0))
 CONTACTS.append({'name':label,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':.0006,'scope':'complete finite opposed actual faces and complete no-positive-penetration test; static geometric support only'})
OUTER=[(-.175,.030),(.175,.030),(.195,.050),(.195,.105),(.170,.130),(.130,.140),(.100,.200),(.075,.220),(-.065,.220),(-.095,.195),(-.120,.125),(-.175,.125),(-.195,.105),(-.195,.050)]
WINDOW=chamfer(-.065,.090,.142,.192,.012)
BODY_HOLES=[WINDOW]+[rect(y-.013,y+.013,ZC-.013,ZC+.008) for y in AXLE_Y]
G[BODY]=extrude_region(OUTER,BODY_HOLES,-.055,.055,0,'One continuous original thick car body; genuine full-thickness grip window and two independent real axle through-bores. Closed genus-three solid with thick complete window frame.')
def axle_geometry(y):
 core=[(-.008,-.008),(0,-.008),(.008,-.008),(.008,0),(.008,.008),(0,.008),(-.008,.008),(-.008,0)]
 end=[(.025*math.cos(-3*math.pi/4+math.tau*i/8),.025*math.sin(-3*math.pi/4+math.tau*i/8)) for i in range(8)]
 layout=[(-.118,end),(-.104,end),(-.104,core),(-.070,core),(-.070,end),(-.061,end),(-.061,core),(.061,core),(.061,end),(.070,end),(.070,core),(.104,core),(.104,end),(.118,end)]
 rr=[[(x,y+yy,ZC+zz) for yy,zz in p] for x,p in layout];m=Mesh();m.face(rr[0],2,'cap');m.face(rr[-1],2,'cap')
 for k,(a,b) in enumerate(zip(rr,rr[1:])):
  for i in range(8):j=(i+1)%8;m.face([a[i],a[j],b[j],b[i]],2,'shaft_or_shoulder_'+str(k))
 return m.result('One continuous fixed square wooden axle with integral inner shoulders and two outer thick end caps; true finite opposed wheel restraints, no detached cap or hidden embedded overlap.',2)
for ai,y in enumerate(AXLE_Y):
 axle='Axle_'+('Front' if ai==0 else 'Rear')+'_IntegralShouldersAndCaps';AXLES.append(axle);G[axle]=axle_geometry(y)
 contact(axle,BODY,(0,0,1),ZC+.008,[(x,y,ZC+.008) for x in [-.035,0,.035]],.00175,axle+'_TopSupportsBodyBoreCeiling')
 for sign,label in [(-1,'Left'),(1,'Right')]:
  w='Wheel_'+('Front' if ai==0 else 'Rear')+'_'+label;WHEELS.append(w);FEET.append(w)
  x0,x1=sorted([sign*.070,sign*.104]);outer=[(y+.060*math.cos((i+.5)*math.tau/12),ZC+.060*math.sin((i+.5)*math.tau/12)) for i in range(12)]
  G[w]=extrude_region(outer,[rect(y-.013,y+.013,ZC-.008,ZC+.013)],x0,x1,1,'One thick twelve-sided wooden wheel with a genuine rectangular centre through-bore and a finite flat ground face; fixed static pose, no tyre or rolling claim.')
  contact(w,axle,(0,0,1),ZC-.008,[(x,y,ZC-.008) for x in [x0+.006,(x0+x1)/2,x1-.006]],.00054,w+'_BoreFloorSupportsAxleBottom')
  for x,a,b,suffix in [(x0,axle,w,'NegativeSideShoulder'),(x1,w,axle,'PositiveSideShoulder')]:
   contact(a,b,(1,0,0),x,[(x,y-.019,ZC),(x,y+.019,ZC),(x,y,ZC+.019)],.00115,w+'_'+suffix)
  volume(ISOLATED_VOID_VOLUMES,w+'_WholeIsolatedBore',box_geometry((x0-.001,y-.0125,ZC-.0075),(x1+.001,y+.0125,ZC+.0125)),[w],'Entire inset through-hole from beyond one wheel face to beyond the other, tested on the isolated closed wheel.')
  # Complete connected inverted-U remaining air, all three noncontact bore sides.
  p=[(y-.0125,ZC-.0075),(y-.0085,ZC-.0075),(y-.0085,ZC+.0085),(y+.0085,ZC+.0085),(y+.0085,ZC-.0075),(y+.0125,ZC-.0075),(y+.0125,ZC+.0125),(y-.0125,ZC+.0125)]
  volume(VOID_VOLUMES,w+'_CompleteAssembledBoreAir',extrude_region(p,[],x0+.0005,x1-.0005),[], 'Complete connected inverted-U finite bore air between actual shoulder planes; 0.5 mm inset from axial end faces and all noncontact boundaries. Bottom is the intentional finite support contact.')
 volume(ISOLATED_VOID_VOLUMES,axle+'_WholeIsolatedBodyBore',box_geometry((-.060,y-.0125,ZC-.0125),(.060,y+.0125,ZC+.0075)),[BODY],'Entire inset body through-bore, beyond both side mouths, tested against isolated complete body.')
 p=[(y-.0125,ZC-.0125),(y+.0125,ZC-.0125),(y+.0125,ZC+.0075),(y+.0085,ZC+.0075),(y+.0085,ZC-.0085),(y-.0085,ZC-.0085),(y-.0085,ZC+.0075),(y-.0125,ZC+.0075)]
 volume(VOID_VOLUMES,axle+'_CompleteAssembledBodyBoreAir',extrude_region(p,[],-.060,.060),[],'Complete connected U-shaped finite side and bottom bore air through the entire body and both mouths; intentional top contact is excluded with 0.5 mm inset.')
# Complete grip aperture, including both exposed mouths; no false glass/black panel.
volume(VOID_VOLUMES,'WholeGripWindowAndBothMouths',extrude_region(chamfer(-.064,.089,.143,.191,.012),[],-.061,.061),[], 'Entire chamfered grip-window air volume through all body thickness and beyond both mouths, one millimetre inset from the complete opening boundary.')
volume(VOID_VOLUMES,'CompleteUnderBodyGroundGap',box_geometry((-.054,-.173,.001),(.054,.173,.029)),[], 'Complete broad finite air space below the body lower face, between ground and car body. Wheels are outside this prism.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
# Complete finite material across all four window-frame sides and both lower
# axle-bearing bridges. Each probe is a closed volume inside the continuous body.
for n,lo,hi in [('Roof',(-.053,-.060,.197),(.053,.070,.215)),('WindowFront',(-.053,-.082,.145),(.053,-.068,.187)),('WindowRear',(-.053,.094,.145),(.053,.102,.186)),('WindowSill',(-.053,-.060,.110),(.053,.085,.137)),('LowerContinuousBody',(-.053,-.168,.033),(.053,.168,.041))]:
 volume(SOLID_VOLUMES,'BodyMaterial_'+n,box_geometry(lo,hi),[BODY],'Complete inset finite body material supporting the continuous '+n+' region, not isolated interior points.')
for ai,y in enumerate(AXLE_Y):
 volume(SOLID_VOLUMES,'BodyBoreCeiling_'+str(ai),box_geometry((-.053,y-.011,ZC+.009),(.053,y+.011,.105)),[BODY],'Full-thickness finite solid bridge above the actual axle-bore ceiling, connecting bore support to body.')
 volume(SOLID_VOLUMES,'AxleContinuousCore_'+str(ai),box_geometry((-.116,y-.0065,ZC-.0065),(.116,y+.0065,ZC+.0065)),[AXLES[ai]],'Full uninterrupted finite core from one end cap through both wheels and complete body to the opposite end cap.')
# Actual-contact-pair surface domains: complete body bore walls except the
# supporting ceiling; complete wheel bore walls except the supporting floor.
# All three noncontact faces are used, including their full axial extent. The
# incident boundaries at contact facets have zero limiting gap, so these domains
# are trimmed by 0.5 mm from the intentional contact plane only.
for ai,y in enumerate(AXLE_Y):
 NONCONTACT_SURFACES.append({'name':'BodyBore_'+str(ai),'solid':BODY,'other':AXLES[ai],'x_range':[-.055,.055],'y_range':[y-.013,y+.013],'z_range':[ZC-.013,ZC+.0075],'bore':True,'minimum_distance_m':.00049})
 for w in WHEELS[ai*2:ai*2+2]:
  vv=G[w]['vertices'];xs=[p[0] for p in vv]
  NONCONTACT_SURFACES.append({'name':w+'_Bore','solid':w,'other':AXLES[ai],'x_range':[min(xs)+.0005,max(xs)-.0005],'y_range':[y-.013,y+.013],'z_range':[ZC-.0075,ZC+.013],'bore':True,'minimum_distance_m':.00049})
def measure_wood_car_geometry(vertices):
 assert set(vertices)==set(G),'Unexpected mesh set'
 for n,g in G.items():
  actual={tuple(round(float(c),6) for c in p) for p in vertices[n]};expected={tuple(round(float(c),6) for c in p) for p in g['vertices']};assert actual==expected,(n,'actual shape changed')
 return {'single_prop_count':1,'closed_body_meshes':1,'body_true_through_bores':3,'grip_windows':1,'axle_bores':2,'continuous_fixed_axles':2,'thick_bored_wheels':4,'body_width_m':.110,'body_length_m':.390,'body_height_m':.190,'body_ground_gap_m':.030,'wheel_thickness_m':.034,'wheel_outer_sides':12,'wheel_radius_m':.060,'axle_centres_y_m':AXLE_Y,'axle_height_m':ZC,'finite_opposed_contacts':len(CONTACTS),'material_contract':MATERIAL_CONTRACT,'static_pose_only':True,'child_safety_or_rolling_claim':False}
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
root=bpy.data.objects.new('OneStaticBoredWoodenToyCar',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0008,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
wood_car_evidence=measure_wood_car_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'wood_car_geometry':wood_car_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/toys/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
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
