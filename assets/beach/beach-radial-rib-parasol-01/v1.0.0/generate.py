"""Original thick radial-rib beach parasol. One static prop, metres/Z up/front -Y.
One connected thick closed canopy, eight true curved ribs and eight actual stretchers.
A fixed runner and upper hub have true axial bores; no opening animation or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beach-radial-rib-parasol-01';VERSION='1.0.0';TITLE='Radial Rib Beach Parasol'
DESCRIPTION=('One original static low-poly opened beach parasol with one connected closed thick eight-panel domed canopy, eight continuous curved radial ribs beneath it and eight diagonal fixed stretchers. A genuinely bored upper hub and fixed runner join the ribs and stretchers to one central pole. A bored lower socket and one finite bevelled ballast-style base complete the supported prop. '
 'The cream and aqua sectors are material assignments within the same physical thick shell, not separate assets. Twenty-two named editable closed meshes. Five constant opaque PBR materials; no image or procedural textures, logos, people, beach surface or scene. Metres, native Z up, front -Y. Origin is at ground level on the pole axis. '
 'One fixed open visual only: geometric support and clear-volume tests do not establish folding or opening motion, kinematics, ultraviolet or sun protection, rain protection, wind resistance, heat comfort, human fit, load capacity, tip resistance, installation or public-space safety performance.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={};SEAM_PROBES=[]
PALETTE=[('Canopy_WarmCream',(.89,.80,.59,1),.82,0),('Canopy_SeaAqua',(.045,.46,.46,1),.78,0),('Frame_SatinAluminum',(.52,.59,.59,1),.36,.65),('Fittings_DeepTeal',(.025,.14,.16,1),.42,.28),('Base_WarmGraphite',(.12,.125,.115,1),.88,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'operating_or_sun_wind_safety_claim':False}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 vs=[transform((a*size[0]/2,b*size[1]/2,d*size[2]/2),c,u,v,w) for d in [-1,1] for b in [-1,1] for a in [-1,1]]
 return mesh(name,vs,BOX_FACES,mat,role)
def chamfer_box(name,c,width,length,height,chamfer,mat,role):
 p=[(-width/2+chamfer,-length/2),(width/2-chamfer,-length/2),(width/2,-length/2+chamfer),(width/2,length/2-chamfer),(width/2-chamfer,length/2),(-width/2+chamfer,length/2),(-width/2,length/2-chamfer),(-width/2,-length/2+chamfer)]
 vs=[add(c,(x,y,z)) for z in [-height/2,height/2] for x,y in p]
 return mesh(name,vs,[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],mat,role)
def rod(name,a,b,r,mat,role,n=24):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1) if abs(w[2])<.9 else (1,0,0)));v=cross(w,u)
 vs=[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n)))) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,role)
def beam(name,a,b,width,depth,mat,role):
 v=unit(sub(b,a));u=(1,0,0);w=cross(u,v)
 return box(name,mul(add(a,b),.5),(width,math.sqrt(dot(sub(b,a),sub(b,a))),depth),mat,role,u,v,w)
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void(name,lo,hi,role):
 vs=[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
 VOID_VOLUMES[name]={'vertices':vs,'faces':BOX_FACES,'role':role}
# All geometry below is original. Historical sources are audit-only, never imported.
def revolved(name,profile,mat,role,n=32):
 vs=[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for r,z in profile for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 fs += [(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i) for k in range(len(profile)-1) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def annulus(name,outer,inner,z0,z1,mat,role,n=32):
 vs=[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for r,z in [(outer,z0),(outer,z1),(inner,z0),(inner,z1)] for i in range(n)]
 fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,mat,role)
def radial(r,z,a):return (r*math.cos(a),r*math.sin(a),z)
def sweep_rib(name,profile,a,radius,mat,role,n=8):
 vs=[]
 for k,(r,z) in enumerate(profile):
  p=radial(r,z,a);p0=radial(*profile[max(0,k-1)],a);p1=radial(*profile[min(len(profile)-1,k+1)],a)
  tangent=unit(sub(p1,p0));u=(-math.sin(a),math.cos(a),0);v=cross(tangent,u)
  vs.extend(add(p,add(mul(u,radius*math.cos(math.tau*i/n)),mul(v,radius*math.sin(math.tau*i/n)))) for i in range(n))
 fs=[tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 fs += [(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i) for k in range(len(profile)-1) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
CANOPY_PROFILE=[(0,2.515),(.10,2.500),(.40,2.455),(.80,2.325),(1.25,2.080)]
CANOPY_THICKNESS=.018;RIB_RADIUS=.017;RIB_UNDERSIDE_OFFSET=.011
CANOPY_SECTORS=8;ANGULAR_STEPS=4;N=CANOPY_SECTORS*ANGULAR_STEPS
# At each radial rib the true lower canopy surface is seated on the rib crown.
# Between ribs the edge is slightly scalloped inward and the fabric is gently sagged.
vs=[]
for top in [False,True]:
 vs.append((0,0,CANOPY_PROFILE[0][1]+(CANOPY_THICKNESS if top else 0)))
 for r,z in CANOPY_PROFILE[1:]:
  for i in range(N):
   a=math.tau*i/N;f=(i%ANGULAR_STEPS)/ANGULAR_STEPS;sag=math.sin(math.pi*f);rr=r*(1-.036*sag*(r/1.25)**2)
   vs.append(radial(rr,z-.024*sag*(r/1.25)**1.6+(CANOPY_THICKNESS if top else 0),a))
L=1+(len(CANOPY_PROFILE)-1)*N;fs=[];fm=[]
for level in [0,1]:
 off=level*L
 for i in range(N):
  j=(i+1)%N;face=(off,off+1+i,off+1+j);fs.append(tuple(reversed(face)) if level==0 else face);fm.append((i//ANGULAR_STEPS)%2)
 for k in range(len(CANOPY_PROFILE)-2):
  for i in range(N):
   j=(i+1)%N;a=off+1+k*N+i;b=off+1+k*N+j;c=off+1+(k+1)*N+j;d=off+1+(k+1)*N+i
   # Explicit planar triangles avoid non-planar n-gon triangulation ambiguity.
   for face in [(a,d,c),(a,c,b)]:fs.append(tuple(reversed(face)) if level==0 else face);fm.append((i//ANGULAR_STEPS)%2)
for i in range(N):
 j=(i+1)%N;a=1+3*N+i;b=1+3*N+j;fs.append((a,b,L+b,L+a));fm.append((i//ANGULAR_STEPS)%2)
CANOPY=mesh('Canopy_OneClosedThickEightPanelShell',vs,fs,0,'one connected finite thick radial dome with a slightly scalloped edge; the eight colored sectors are the same physical shell',fm)
BASE=revolved('Base_FiniteBevelledBallast',[(.270,0),(.300,.025),(.300,.100),(.250,.130)],4,'single finite bevelled ballast-style base with flat bottom; visual support only',32);FEET.append(BASE)
POLE=rod('Pole_OneContinuousCentralMast',(0,0,.100),(0,0,2.521),.032,2,'single continuous center pole from base into crown shell',24)
SOCKET=annulus('Socket_BoredLowerSupport',.080,.029,.095,.285,3,'true-bored lower support sleeve; small finite pole interference is intentional',32)
UPPER=annulus('Hub_BoredUpperRibCarrier',.095,.029,2.465,2.506,3,'true-bored upper hub; eight radially spaced ribs enter its outer portion',32)
RUNNER=annulus('Runner_BoredFixedSleeve',.073,.029,1.875,1.965,3,'fixed true-bored runner with eight spatially separated stretcher roots; no moving mechanism',32)
link(BASE,POLE,(0,0,.115),axis=(1,0,0),spread=.010)
link(BASE,SOCKET,(.052,0,.112),axis=(0,1,0),spread=.010)
for sleeve,z in [(SOCKET,.200),(UPPER,2.485),(RUNNER,1.920)]:
 link(sleeve,POLE,(.0305,0,z),axis=(0,0,1),spread=.008)
link(POLE,CANOPY,(.010,0,2.517),axis=(0,1,0),spread=.008)
link(UPPER,CANOPY,(.083,0,2.504),axis=(0,1,0),spread=.003)
for name,z0,z1 in [(SOCKET,.095,.285),(UPPER,2.465,2.506),(RUNNER,1.875,1.965)]:
 BORES.append({'mesh':name,'origin_m':(0,0,z0-.01),'direction':(0,0,1),'length_m':z1-z0+.02})
RIBS=[];STRETCHERS=[];RIB_CONTRACTS=[]
RIB_PROFILE=[(.075,2.50375-RIB_UNDERSIDE_OFFSET)]+[(r,z-RIB_UNDERSIDE_OFFSET) for r,z in CANOPY_PROFILE[1:]]
for i in range(8):
 a=math.tau*i/8;u=(-math.sin(a),math.cos(a),0)
 rib=sweep_rib('Rib_%02d_ContinuousCurvedRadial'%(i+1),RIB_PROFILE,a,RIB_RADIUS,2,'one actual continuous curved radial rib, tucked under the thick shell with full capped end',8);RIBS.append(rib)
 link(rib,UPPER,radial(.084,2.4914,a),axis=u,spread=.003)
 # Three distinct radial zones witness real shell support, including the complete tip.
 for r,z in [(.25,2.4775),(.58,2.3965),(1.230,2.0908889)]:
  link(rib,CANOPY,radial(r,z+.0015,a),axis=u,spread=.0006)
 end=radial(.680,2.364-RIB_UNDERSIDE_OFFSET,a);start=radial(.054,1.932,a)
 st=rod('Stretcher_%02d_FixedDiagonal'%(i+1),start,end,.013,2,'one diagonal fixed support linking runner to its matching rib; no motion or latch claim',12);STRETCHERS.append(st)
 link(st,RUNNER,radial(.063,1.938053,a),axis=u,spread=.003)
 link(st,rib,radial(.677,2.3509808,a),axis=u,spread=.003)
 # A finite patch below the fabric and between adjacent rib planes is a real open air wedge.
 ac=a+math.pi/8;center=radial(.970,1.80,ac);void('UnderCanopySector_%02d'%(i+1),sub(center,(.045,.045,.12)),add(center,(.045,.045,.12)),'finite unobstructed air under the canopy between neighboring radial supports; no human-fit claim')
 RIB_CONTRACTS.append({'rib':rib,'stretcher':st,'angle_rad':a,'profile':RIB_PROFILE,'canopy_contact_radial_positions_m':[.25,.58,1.23]})
# Finite side air near the long pole, above the socket and below the fixed runner.
for side,s in [('Left',-1),('Right',1)]:
 center=(s*.20,0,1.05);void('PoleSideAir_'+side,sub(center,(.08,.08,.65)),add(center,(.08,.08,.65)),'finite empty volume on each side of central pole')
for i,(r,a,z) in enumerate([(.25,math.pi/8,2.470),(.62,math.pi/8,2.374),(.98,math.pi/8,2.210)]):
 WALL_PROBES.append({'mesh':CANOPY,'label':'FabricRadialZone_'+str(i+1),'origin_m':radial(r,z-.045,a),'direction':(0,0,1),'length_m':.15,'minimum_wall_thickness_m':.017})
PARASOL_CONTRACT={'single_prop_count':1,'canopy_mesh':CANOPY,'canopy_sectors':8,'canopy_thickness_m':CANOPY_THICKNESS,'canopy_profile':CANOPY_PROFILE,'rib_meshes':RIBS,'stretcher_meshes':STRETCHERS,'rib_support_contracts':RIB_CONTRACTS,'upper_hub_mesh':UPPER,'fixed_runner_mesh':RUNNER,'central_pole_mesh':POLE,'lower_socket_mesh':SOCKET,'ground_meshes':FEET,'static_open_pose_only':True,'opening_animation_uv_rain_wind_load_human_fit_or_safety_claim':False}
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
root=bpy.data.objects.new('OneOriginalRadialRibBeachParasol',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground level on central pole axis';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
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
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
# Actual floor and wall tests supplement finite void and support tests.
floor_checks=[]
for r in FLOOR_PROBES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is not None and abs(hit.z-r['expected_hit_z_m'])<1e-6
 floor_checks.append(dict(r,actual_hit_m=list(hit)))
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);t=trees[r['mesh']];inner=t.ray_cast(p,d,r['length_m'])[0]
 assert inner is not None
 outer=t.ray_cast(inner+d*1e-6,d,r['length_m'])[0];assert outer is not None
 thickness=(outer-inner).length;assert thickness>r['minimum_wall_thickness_m']
 wall_checks.append(dict(r,actual_inner_hit_m=list(inner),actual_outer_hit_m=list(outer),actual_wall_thickness_m=thickness))
seam_checks=[]
for r in SEAM_PROBES:
 o=byname[r['mesh']];cx,cy=r['local_center_xy']
 def radius(k):p=o.data.vertices[k].co;return math.hypot(p.x-cx,p.y-cy)
 depth=(radius(r['left_bank_vertex'])+radius(r['right_bank_vertex']))/2-radius(r['centre_vertex'])
 assert depth>r['minimum_radial_indent_m'],('Actual seam is not recessed',r,depth)
 seam_checks.append(dict(r,actual_vertex_radial_indent_m=depth))
parasol_evidence=dict(PARASOL_CONTRACT,finite_empty_volume_checks=void_volume_checks,actual_shell_thickness_checks=wall_checks,material_contract=MATERIAL_CONTRACT,actual_recessed_seam_checks=seam_checks)
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
 'single_prop_count':1,'parasol_geometry':parasol_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beach/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beach','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,1.26));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.30;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-back-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.5,-6.0,3.15),'gray-back3q':(-4.5,6.0,-3.0)} if gray else {
 'thumbnail':(4.5,-6.0,3.15),'qa-front':(0,-12,2.05),'qa-side':(12,0,2.05),'qa-top':(0,0,7),
 'qa-back':(0,12,2.05),'qa-wireframe':(4.5,-6.0,3.15)}
if '--gray-back-only' in sys.argv:views={'gray-back3q':views['gray-back3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=3.30
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00515625;w.use_replace=True;w.use_even_offset=False;w.offset=1
 # Only this technical underside gray omits the non-asset preview floor.
 if name=='gray-back3q':
  previous_ground_hide=ground.hide_render;ground.hide_render=True
  qa['technical_gray_back_view']={'camera_position_m':list(pos),'upward_underside_diagnostic':True,'preview_ground_hidden':True,'all_asset_meshes_visible':True,'ground_support_evidence':'original gray-front3q, silhouettes and actual ground geometry'}
  try:render(name,pos)
  finally:ground.hide_render=previous_ground_hide
 else:render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-back-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-12,2.05)),('silhouette-128-side',(12,0,2.05))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
