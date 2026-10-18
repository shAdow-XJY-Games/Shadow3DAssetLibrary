"""Original laboratory benchtop centrifuge, one fixed-open static visual prop.
Metres, native Z up, front -Y, ground origin (0,0,0). No external dependencies.
True thick blind chamber and eight true blind rotor wells; fixed open lid with
bored hinge supports. No spin, lid motion, tube-fit, diagnostic or safety claim.
Stages --geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
All views freshly import the exact exported GLB; Cycles128 FIXED4, no denoise.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-benchtop-centrifuge-01';VERSION='1.0.0';TITLE='Fixed-Open Laboratory Benchtop Centrifuge'
DESCRIPTION=('Original compact static benchtop centrifuge visual prop with a thick chamfered enclosure, '
 'genuine blind-bottom circular chamber, centrally supported eight-well rotor and eight real deep blind receiving cavities. '
 'Fixed open thick lid, inset seal ring, two bored hinge supports and a polygonal pin resting on actual finite bearing facets. '
 'Independent controls and four grounded feet. Five solid PBR materials; closed separately editable components. '
 'Metres, source Z up, front -Y, ground origin (0,0,0). No sample tubes or compatibility with the existing sample rack are claimed. '
 'No rotor or lid animation, continuous motion, laboratory procedure, diagnosis, speed, electrical, load, stability or safety certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('WarmIvory_Enclosure',(.74,.70,.60,1),.58,.05),
 ('MutedTeal_ControlAndSeal',(.085,.27,.26,1),.58,.12),('Graphite_RotorAndFeet',(.10,.13,.14,1),.49,.35),
 ('BrushedSteel_ChamberAndHinge',(.37,.43,.44,1),.40,.65),('Ochre_StaticControl',(.63,.38,.12,1),.56,.15)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('LaboratoryBenchtopCentrifuge',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_axis']='-Y';root['static_visual_only']=True
root['fixed_open_lid_degrees']=-103.0
root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Restrained manufactured chamfer','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def rod(name,a,b,r,material,role,n=12):
 a=Vector(a);b=Vector(b);d=(b-a).normalized();ref=Vector((0,1,0)) if abs(d.y)<.9 else Vector((1,0,0))
 u=d.cross(ref).normalized();v=d.cross(u).normalized()
 vs=[p+r*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,(a+b)/2)

def lathe(name,profile,material,role,n=48,center=(0,0,0)):
 c=Vector(center);vs=[c+Vector((r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z)) for r,z in profile for i in range(n)]
 fs=[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i) for k in range(len(profile)-1) for i in range(n)]
 for k,rev in [(0,True),(len(profile)-1,False)]:
  ci=len(vs);vs.append(c+Vector((0,0,profile[k][1])))
  fs += [(ci,k*n+(i+1)%n,k*n+i) if rev else (ci,k*n+i,k*n+(i+1)%n) for i in range(n)]
 return mesh(name,vs,fs,material,role,c)
def annulus(name,center,axis,length,outer,inner,material,role,n=24,phase=0):
 c=Vector(center);d=Vector(axis).normalized();u=Vector((0,1,0)) if abs(d.x)>.9 else Vector((1,0,0));v=d.cross(u).normalized()
 vs=[c+d*t+r*(u*math.cos(math.tau*i/n+phase)+v*math.sin(math.tau*i/n+phase)) for t,r in [(-length/2,outer),(length/2,outer),(length/2,inner),(-length/2,inner)] for i in range(n)]
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,material,role,c)
def polar_rect(hw,hd,chamfer,n=64):
 q=[]
 for i in range(n):
  a=math.tau*i/n;c=math.cos(a);s=math.sin(a);r=min(hw/max(abs(c),1e-12),hd/max(abs(s),1e-12),(hw+hd-chamfer)/(abs(c)+abs(s)))
  q.append((r*c,r*s))
 return q
# One closed thick housing with a real open chamber and blind floor at Z=.115.
n=64;loops=[]
for hw,hd,ch,z in [(.276,.296,.05,.055),(.29,.31,.055,.070),(.29,.31,.055,.282),(.282,.302,.05,.300)]:loops.append([(x,y,z) for x,y in polar_rect(hw,hd,ch,n)])
for r,z in [(.245,.300),(.239,.291),(.239,.115)]:loops.append([(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)])
vs=sum(loops,[]);fs=[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i) for k in range(len(loops)-1) for i in range(n)]
for k,rev in [(0,True),(len(loops)-1,False)]:
 ci=len(vs);vs.append((0,0,loops[k][0][2]));fs.extend([(ci,k*n+(i+1)%n,k*n+i) if rev else (ci,k*n+i,k*n+(i+1)%n) for i in range(n)])
housing=mesh('Housing_ThickBlindChamber',vs,fs,0,'one closed thick enclosure with open circular chamber and actual blind floor')
housing.data.materials.append(mats[3])
for f in housing.data.polygons:
 if 4*n<=f.index<6*n or f.index>=7*n:f.material_index=1
# Rotor underside is held by a solid central spindle; no shaft or rotation rig.
rod('Rotor_CentralSupport',(0,0,.106),(0,0,.169),.057,3,'central stationary support embedded in real chamber floor and rotor underside',n=24)
rotor=lathe('Rotor_EightBlindWells',[(.177,.150),(.195,.170),(.195,.245),(.185,.255)],2,'single closed rotor body with eight actual blind receiving wells',n=48)
well_centres=[]
for i in range(8):
 a=math.tau*i/8+math.pi/8;x=.126*math.cos(a);y=.126*math.sin(a);well_centres.append((x,y))
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.026,depth=.140,location=(x,y,.244));c=bpy.context.object
 mod=rotor.modifiers.new('Actual blind receiving well %02d'%(i+1),'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c
 bpy.context.view_layer.objects.active=rotor;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)
rod('Rotor_CentreCap',(0,0,.248),(0,0,.274),.038,4,'fixed central rotor fastener; no speed indicator',n=12)
# Four feet are distinct grounded solids with finite bottom faces.
feet=[]
for x,lx in [(-.22,'Left'),(.22,'Right')]:
 for y,ly in [(-.23,'Front'),(.23,'Rear')]:
  name='Foot_'+lx+ly;box(name,(x,y,.038),(.085,.085,.076),2,'closed foot with bottom at Z=0 and finite housing overlap',bevel=.005);feet.append((name,x,y))
# Compact front control plate and three static details, all actually attached.
box('Control_FrontPanel',(0,-.307,.199),(.42,.022,.105),1,'fixed front control fascia embedded into housing',bevel=.010)
box('Control_BlankDisplay',(-.070,-.322,.206),(.17,.016,.045),2,'blank opaque display; no operational readings or emission',bevel=.004)
rod('Control_FixedDial',(.112,-.312,.205),(.112,-.353,.205),.028,4,'fixed control knob with actual face overlap',n=12)
box('Control_FixedButton',(.174,-.325,.201),(.027,.020,.027),0,'small fixed rectangular control button',bevel=.003)
# Bored bearing supports and a pin resting on their horizontal bottom facets.
# Circular-polygon bore radius .016, pin radius .015, both phase pi/12.
# The pin centre is lowered by .001*cos(pi/12), creating genuine facet contact.
HINGE_Y=.279;HINGE_Z=.319;PHASE=math.pi/12;PIN_Z=HINGE_Z-.001*math.cos(PHASE)
for x,label in [(-.185,'Left'),(.185,'Right')]:
 annulus('Hinge_BoredSupport_'+label,(x,HINGE_Y,HINGE_Z),(1,0,0),.070,.036,.016,3,'real polygonal through bore; bottom facet supports hinge pin',n=12,phase=PHASE)
# Pin generated with identical polygon phase around X.
vs=[(x,HINGE_Y+.015*math.cos(math.tau*i/12+PHASE),PIN_Z+.015*math.sin(math.tau*i/12+PHASE)) for x in [-.245,.245] for i in range(12)]
fs=[tuple(reversed(range(12))),tuple(12+i for i in range(12))]+[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)]
mesh('Hinge_FixedPin',vs,fs,3,'fixed pin with finite bottom bearing-facet support',(0,HINGE_Y,PIN_Z))
# Fixed cover pose, -103 degrees about X; actual mesh vertices are transformed.
LID_ANGLE=math.radians(-103)
def lidpoint(p):
 x,y,z=p;y-=HINGE_Y;z-=PIN_Z
 return Vector((x,HINGE_Y+y*math.cos(LID_ANGLE)-z*math.sin(LID_ANGLE),PIN_Z+y*math.sin(LID_ANGLE)+z*math.cos(LID_ANGLE)))
def pose_lid(o):
 for v in o.data.vertices:v.co=lidpoint(o.matrix_world@v.co)-o.location
 return o
# The low-poly lid is a closed chamfered rectangle, with no external texture.
q=[(-.226,-.282),(.226,-.282),(.282,-.226),(.282,.226),(.226,.282),(-.226,.282),(-.282,.226),(-.282,-.226)]
vs=[lidpoint((x,y,z)) for z in [.310,.338] for x,y in q];fs=[tuple(reversed(range(8))),tuple(8+i for i in range(8))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
mesh('Lid_FixedOpenCover',vs,fs,0,'closed thick cover, fixed open at -103 degrees; no animated sweep')
seal=annulus('Lid_InsetSealRing',(0,0,.309),(0,0,1),.012,.244,.230,1,'thick nonfunctional seal ring partly embedded into lid',n=48)
bpy.context.view_layer.update();pose_lid(seal)
for x,label in [(-.145,'Left'),(.145,'Right')]:
 a=(x,HINGE_Y,PIN_Z);b=lidpoint((x,.225,.324))
 rod('Lid_HingeArm_'+label,a,b,.018,3,'fixed short connecting arm joining hinge pin to opened lid',n=12)
# Bake triangulation once, ensuring GLB/native/clean comparison is unambiguous.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces))
 if o.name=='Rotor_EightBlindWells':
  # Exact Boolean leaves zero-area sliver faces at coplanar intersections.
  # Remove only degenerate faces/edges within 0.1 micrometre, preserving wells.
  bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges))
  bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free()
 for f in o.data.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 votes=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  votes.append(bool(hits%2))
 return all(votes)
joints=[]
def joint(a,b,points):
 rows=[]
 for p in points:
  p=list(p);clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})

joint('Housing_ThickBlindChamber','Rotor_CentralSupport',[(x,0,.110) for x in [-.020,0,.020]])
joint('Rotor_CentralSupport','Rotor_EightBlindWells',[(x,0,.158) for x in [-.020,0,.020]])
joint('Rotor_EightBlindWells','Rotor_CentreCap',[(x,0,.252) for x in [-.012,0,.012]])
for name,x,y in feet:joint('Housing_ThickBlindChamber',name,[(x+dx,y+dy,.066) for dx,dy in [(-.015,0),(.015,0),(0,.015)]])
joint('Housing_ThickBlindChamber','Control_FrontPanel',[(x,-.301,.199) for x in [-.10,0,.10]])
joint('Control_FrontPanel','Control_BlankDisplay',[(x,-.316,.206) for x in [-.11,-.07,-.03]])
joint('Control_FrontPanel','Control_FixedDial',[(.112+dx,-.315,.205+dz) for dx,dz in [(-.008,0),(.008,0),(0,.008)]])
joint('Control_FrontPanel','Control_FixedButton',[(.174+dx,-.317,.201+dz) for dx,dz in [(-.005,0),(.005,0),(0,.005)]])
for x,label in [(-.185,'Left'),(.185,'Right')]:
 joint('Housing_ThickBlindChamber','Hinge_BoredSupport_'+label,[(x+dx,HINGE_Y,.289) for dx in [-.018,0,.018]])
for x,label in [(-.145,'Left'),(.145,'Right')]:
 a=Vector((x,HINGE_Y,PIN_Z));d=(lidpoint((x,.225,.324))-a).normalized()
 joint('Hinge_FixedPin','Lid_HingeArm_'+label,[a+d*.006+Vector((dx,0,0)) for dx in [-.005,0,.005]])
 joint('Lid_FixedOpenCover','Lid_HingeArm_'+label,[lidpoint((x+dx,.232,.324)) for dx in [-.005,0,.005]])
joint('Lid_FixedOpenCover','Lid_InsetSealRing',[lidpoint((x,y,.312)) for x,y in [(.237,0),(-.237,0),(0,-.237)]])
# Finite contact proof from actual loop triangles, evaluated in Python doubles.
# Avoid float32 BVH closest-point drift on a long thin pin facet. Geometry and
# plane tolerance are unchanged; compare actual planar triangle intersections.
def orient2(a,b,p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
def polygon_area(poly):return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2 if len(poly)>=3 else 0.0
def ccw(poly):return list(reversed(poly)) if orient2(poly[0],poly[1],poly[2])<0 else list(poly)
def clip_triangle(poly,triangle):
 poly=list(poly);triangle=ccw(triangle)
 for i in range(3):
  a,b=triangle[i],triangle[(i+1)%3];output=[]
  if not poly:break
  previous=poly[-1];dp=orient2(a,b,previous)
  for current in poly:
   dc=orient2(a,b,current)
   if (dc>=-1e-12)!=(dp>=-1e-12):
    t=dp/(dp-dc);output.append((previous[0]+t*(current[0]-previous[0]),previous[1]+t*(current[1]-previous[1])))
   if dc>=-1e-12:output.append(current)
   previous=current;dp=dc
  poly=output
 return poly
def horizontal_faces(name,z,normal_sign):
 o=byname[name];rows=[]
 for t in o.data.loop_triangles:
  vs=[tuple(float(c) for c in o.matrix_world@o.data.vertices[i].co) for i in t.vertices]
  nz=orient2(vs[0],vs[1],vs[2])
  if max(abs(v[2]-z) for v in vs)<1e-7 and nz*normal_sign>1e-12:
   rows.append({'triangle':t.index,'vertices_m':vs,'xy':ccw([(v[0],v[1]) for v in vs]),'normal_z_sign':normal_sign})
 assert rows,(name,'no horizontal contact faces');return rows
def covered_xy(point,rows):return any(all(orient2(r['xy'][i],r['xy'][(i+1)%3],point)>=-1e-12 for i in range(3)) for r in rows)
contact_z=HINGE_Z-.016*math.cos(PHASE);bearing_contacts=[]
for x,label in [(-.185,'Left'),(.185,'Right')]:
 a='Hinge_BoredSupport_'+label;b='Hinge_FixedPin';af=horizontal_faces(a,contact_z,1);bf=horizontal_faces(b,contact_z,-1);points=[]
 for dx,dy in [(-.020,-.0015),(-.020,.0015),(.020,-.0015),(.020,.0015),(0,0)]:
  p=(x+dx,HINGE_Y+dy,contact_z);assert covered_xy(p,af) and covered_xy(p,bf),(a,p,'finite planar coverage missing');points.append(p)
 intersections=[]
 for ta in af:
  for tb in bf:
   poly=clip_triangle(ta['xy'],tb['xy']);area=polygon_area(poly)
   if area>1e-12:intersections.append({'bearing_triangle':ta['triangle'],'pin_triangle':tb['triangle'],'xy_polygon_m':poly,'area_m2':area})
 area=sum(r['area_m2'] for r in intersections);assert area>=.00012,(a,area)
 bearing_contacts.append({'a':a,'b':b,'contact_plane_z_m':contact_z,'probed_finite_patch_m':points,'conservative_patch_area_m2':.00012,'actual_opposed_triangle_intersection_area_m2':area,'actual_triangle_intersections':intersections,'bearing_faces':af,'pin_faces':bf})
# Support graph includes overlap joints and actual bearing contact joints.
adj={o.name:set() for o in parts}
for j in joints+bearing_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={feet[0][0]};pending=list(seen)
while pending:
 for name in adj[pending.pop()]-seen:seen.add(name);pending.append(name)
assert seen==set(adj),'Unsupported components: '+repr(set(adj)-seen)
supports=[]
for name,_,_ in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.005,area;supports.append({'name':o.name,'area_m2':area,'triangles':patch})
# Chamber annulus rays reach the true floor without crossing housing or rotor.
chamber_rays=[]
for i in range(8):
 a=math.tau*i/8;x=.217*math.cos(a);y=.217*math.sin(a);p=Vector((x,y,.33));hit,normal,_,dist=trees['Housing_ThickBlindChamber'].ray_cast(p,Vector((0,0,-1)),1)
 assert hit is not None and abs(hit.z-.115)<1e-6,(i,hit)
 assert trees['Rotor_EightBlindWells'].ray_cast(p,Vector((0,0,-1)),1)[0] is None
 chamber_rays.append({'origin_m':list(p),'floor_hit_m':list(hit)})
well_rays=[]
for i,(x,y) in enumerate(well_centres):
 rows=[]
 for dx,dy in [(0,0),(.008,0),(-.008,0),(0,.008),(0,-.008)]:
  p=Vector((x+dx,y+dy,.28));hit,normal,_,dist=trees['Rotor_EightBlindWells'].ray_cast(p,Vector((0,0,-1)),1)
  assert hit is not None and abs(hit.z-.174)<1e-6,(i,hit)
  assert not inside(trees['Rotor_EightBlindWells'],(x+dx,y+dy,.215))
  rows.append({'origin_m':list(p),'blind_floor_hit_m':list(hit)})
 well_rays.append({'well':i+1,'centre_xy_m':[x,y],'depth_m':.081,'rays':rows})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'Solid-only PBR expected'
 assert not any(i.is_linked for i in p.inputs),'Linked Principled inputs are not solid PBR'
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
 'components':component_checks,'connection_interior_points':joints,'finite_ground_supports':supports,'all_components_support_connected':True,'finite_hinge_bearing_contacts':bearing_contacts,'chamber_floor_rays':chamber_rays,'rotor_well_rays':well_rays,'fixed_lid_angle_degrees':-103,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.03,.42));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.10;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-front-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(1.4,-2.2,1.65),'gray-back3q':(-1.4,2.2,1.65)} if gray else {
 'thumbnail':(1.5,-2.0,1.65),'qa-front':(0,-6,.42),'qa-side':(6,.03,.42),'qa-top':(0,.03,7),
 'qa-back':(0,6,.42),'qa-wireframe':(1.5,-2.0,1.65)}
if '--gray-front-only' in sys.argv:views={'gray-front3q':views['gray-front3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={}
def render(name,pos):
 cam.data.ortho_scale=1.22 if name in ['gray-front3q','thumbnail','qa-wireframe'] else 1.10
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00045;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-front-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-6,.42)),('silhouette-128-side',(6,.03,.42))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
