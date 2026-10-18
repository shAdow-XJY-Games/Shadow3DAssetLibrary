"""Original side-resting deep-bag landing net. Metres; native Z up.
One static prop: a long shaft, genuinely open oval frame and a gathered rope bag.
Every net strand is closed solid geometry. No textures, borrowed models or animation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fishing-deep-bag-landing-net-01';VERSION='1.0.0';TITLE='Side-Resting Deep-Bag Landing Net'
DESCRIPTION=('Original static low-poly landing net with a long straight wooden shaft, solid teal grip and sleeve, and a thick genuinely open oval frame. '
 'Twelve closed solid longitudinal cords and four closed cross-loop cords form a three-dimensional sparse mesh bag that narrows into one grounded gathering knot. '
 'The frame, shaft and grip lie in one tilted vertical plane in a fixed side-resting storage pose; the bag sags sideways to its gathered low end. '
 'Finite frame, grip and knot ground patches and measured volumetric joints connect every named component. Actual empty mouth and net windows are geometry, without transparent net textures. '
 'One editable prop, four constant solid PBR materials, metre scale, native Z up and ground-centre origin; no external dependencies. '
 'No fishing, catch retention, flexible-net behavior, loads, material stiffness, human fit, manufacture, regulation, animation or safety certification.')
G={};LINKS=[];FEET=['Frame_OpenOval','Grip_FlatRestingButt','Bag_GatheredBottomKnot'];BORES=[];GAPS=[];WINDOWS=[];CAVITY=[];BOTTOM_PROBES=[];NET_NAMES=[]
PALETTE=[('Shaft_Maple',(.54,.32,.14,1),.77,0),('Frame_Ochre',(.64,.34,.12,1),.44,.38),('Grip_Petrol',(.045,.18,.19,1),.87,0),('Net_SandFiber',(.67,.59,.40,1),.94,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def tube(name,points,r,mat,role,closed=False,n=8):
 vs=[];count=len(points)
 for i,p in enumerate(points):
  tangent=unit(sub(points[(i+1)%count],points[(i-1)%count])) if closed or 0<i<count-1 else unit(sub(points[min(i+1,count-1)],points[max(0,i-1)]))
  ref=(0,0,1) if abs(tangent[2])<.9 else (0,1,0);u=unit(cross(tangent,ref));v=cross(tangent,u)
  vs.extend(add(p,add(mul(u,r*math.cos(math.tau*j/n)),mul(v,r*math.sin(math.tau*j/n)))) for j in range(n))
 fs=[]
 for i in range(count if closed else count-1):
  q=(i+1)%count
  for j in range(n):k=(j+1)%n;fs.append((i*n+j,i*n+k,q*n+k,q*n+j))
 if not closed:fs += [tuple(reversed(range(n))),tuple((count-1)*n+j for j in range(n))]
 return mesh(name,vs,fs,mat,role)
def poly_x(name,outline,x0,x1,mat,role):
 k=len(outline);vs=[(x,y,z) for x in [x0,x1] for y,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def clip_ground(poly):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[1]>=0;ib=b[1]>=0
  if ia:out.append(a)
  if ia!=ib:
   t=-a[1]/(b[1]-a[1]);out.append((a[0]+t*(b[0]-a[0]),0))
 return out
TH=math.radians(9);E=(0,math.cos(TH),math.sin(TH));U=(0,-math.sin(TH),math.cos(TH))
A=.350;B=.250;N=32;T0=math.atan2(-B*math.cos(TH),-A*math.sin(TH));ANGLES=[T0+math.pi/N+math.tau*i/N for i in range(N)]
ZC=-min((A*math.cos(t)*E[2]+B*math.sin(t)*U[2]) for t in ANGLES)
C=(0,0,ZC)
def ellipse(t,a,b,c=C):return add(c,add(mul(E,a*math.cos(t)),mul(U,b*math.sin(t))))
# Annular solid extrusion. Two lowest outer vertices make a true flat ground facet.
vs=[]
for x,a,b in [(-.016,A,B),(.016,A,B),(-.016,A-.029,B-.029),(.016,A-.029,B-.029)]:
 vs += [(x,*ellipse(t,a,b)[1:]) for t in ANGLES]
fs=[]
for i in range(N):j=(i+1)%N;fs += [(i,j,N+j,N+i),(2*N+j,2*N+i,3*N+i,3*N+j),(j,i,2*N+i,2*N+j),(N+i,N+j,3*N+j,3*N+i)]
mesh('Frame_OpenOval',vs,fs,1,'closed 32 mm thick annular frame with a genuinely empty oval aperture and finite side-resting bottom facet')
# The shaft follows the major axis. The sleeve physically surrounds it and overlaps the near frame tip.
def axispoint(t):return add(C,mul(E,t))
tube('Handle_LongShaft',[axispoint(-1.455),axispoint(-.347)],.018,0,'long continuous solid eight-sided maple shaft, tangent to the hoop plane',n=12)
tube('Sleeve_FrameSocket',[axispoint(-.455),axispoint(-.325)],.030,2,'solid neck sleeve with true interior overlap into both shaft and oval frame',n=12)
link('Sleeve_FrameSocket','Handle_LongShaft',axispoint(-.390),axis=E,spread=.020)
link('Sleeve_FrameSocket','Frame_OpenOval',ellipse(math.pi,A-.0145,B-.0145),axis=(1,0,0),spread=.005)
# A clipped solid grip has a finite ground facet at its remote end, not point contact.
p0=axispoint(-1.565);p1=axispoint(-1.325);outline=[]
for p,d in [(p0,-.028),(p1,-.028),(p1,.028),(p0,.028)]:
 q=add(p,mul(U,d));outline.append((q[1],q[2]))
poly_x('Grip_FlatRestingButt',clip_ground(outline),-.025,.025,2,'thick rectangular soft grip with a real clipped flat resting facet, no separate stand')
link('Grip_FlatRestingButt','Handle_LongShaft',axispoint(-1.410),axis=(1,0,0),spread=.006)
# Sideways, sagged net bag. Each cross-loop remains above the ground; the bottom
# gathers into a small finite solid knot on the floor, rather than a second mouth.
R=.0038;M=12;T=[math.tau*i/M for i in range(M)]
LAYERS=[(0,1.0),(.075,.86),(.150,.66),(.220,.44),(.275,.22)]
CENTRES=[];RINGS=[]
for j,(x,s) in enumerate(LAYERS):
 a=(A-.0145)*s;b=(B-.0145)*s
 if j==0:c=(x,0,ZC)
 else:
  low=min(a*math.cos(t)*E[2]+b*math.sin(t)*U[2] for t in [math.tau*i/24 for i in range(24)])
  c=(x,.012*j,-low+.010)
 CENTRES.append(c);RINGS.append([ellipse(t,a,b,c) for t in T])
KNOT=(.330,.061,.018)
# Faceted knot has a flat underside. All 12 terminals end inside its closed volume.
outline=[(.039,0),(.079,0),(.087,.010),(.087,.025),(.078,.036),(.042,.036),(.033,.025),(.033,.010)]
poly_x('Bag_GatheredBottomKnot',outline,.312,.348,3,'single solid gathered cord knot with finite flat underside; not a plug on an open bag tube')
for i,t in enumerate(T):
 name=f'Bag_Longitudinal_{i:02d}';pts=[ring[i] for ring in RINGS]+[KNOT]
 tube(name,pts,R,3,'one continuous closed solid cord from the real hoop to the common gathered bottom',n=8);NET_NAMES.append(name)
 # The first knot lies just inside the near frame, before the cord exits toward the bag.
 link(name,'Frame_OpenOval',add(pts[0],mul(unit(sub(pts[1],pts[0])),.0025)),axis=(0,1,0),spread=.0006)
 link(name,'Bag_GatheredBottomKnot',add(KNOT,mul(unit(sub(pts[-2],KNOT)),.006)),axis=(0,1,0),spread=.0005)
for j in range(1,len(LAYERS)):
 x,s=LAYERS[j];c=CENTRES[j];points=[ellipse(math.tau*i/24,(A-.0145)*s,(B-.0145)*s,c) for i in range(24)]
 name=f'Bag_CrossLoop_{j:02d}';tube(name,points,R,3,'closed solid cross-loop; all twelve crossings overlap volumetrically with longitudinal cords',closed=True,n=8);NET_NAMES.append(name)
 for i in range(M):link(name,f'Bag_Longitudinal_{i:02d}',RINGS[j][i],axis=(1,0,0),spread=.0006)
# Empty mouth: finite shallow volume rays through the actual assembled hoop.
for y in [-.18,-.09,0,.09,.18]:
 for z in [ZC-.10,ZC,ZC+.10]:
  GAPS.append({'label':'open_oval_mouth','origin_m':[-.080,y,z],'direction':[1,0,0],'length_m':.100})
# 48 five-ray net-window probes between rings. The last triangular gathering
# region is intentionally excluded from the finite-window size claim.
for j in range(4):
 for i in range(M):
  ii=(i+1)%M;p00=RINGS[j][i];p01=RINGS[j][ii];p10=RINGS[j+1][i];p11=RINGS[j+1][ii]
  centre=mul(add(add(p00,p01),add(p10,p11)),.25);u=unit(sub(add(p01,p11),add(p00,p10)));v=unit(sub(add(p10,p11),add(p00,p01)));n=unit(cross(u,v));rays=[]
  for du,dv in [(0,0),(-.003,-.003),(-.003,.003),(.003,-.003),(.003,.003)]:
   p=add(centre,add(mul(u,du),mul(v,dv)));r={'label':f'bag_window_{j:02d}_{i:02d}','origin_m':add(p,mul(n,-.014)),'direction':n,'length_m':.028};GAPS.append(r);rays.append(r)
  WINDOWS.append({'layer':j,'segment':i,'five_ray_span_m':.006,'continuous_window_prism_verified':False,'centre_m':centre,'rays':rays})
# True open interior reaches toward the gathered endpoint with no false surface.
for a,b in zip(CENTRES,CENTRES[1:]):
 d=sub(b,a);length=math.sqrt(dot(d,d));r={'label':'bag_open_centreline','origin_m':a,'direction':unit(d),'length_m':length};GAPS.append(r);CAVITY.append(r)
BOTTOM_PROBES.append({'label':'gathered_closed_end','mesh':'Bag_GatheredBottomKnot','origin_m':(.295,.061,.018),'direction':(1,0,0),'length_m':.070})
# Ground-centre origin (from actual generated extents); coordinates stay baked.
allv=[v for g in G.values() for v in g['vertices']];SHIFT=((min(v[0] for v in allv)+max(v[0] for v in allv))/2,(min(v[1] for v in allv)+max(v[1] for v in allv))/2,0)
for g in G.values():g['vertices']=[tuple(round(c,7) for c in sub(v,SHIFT)) for v in g['vertices']]
LINKS=[(a,b,[sub(p,SHIFT) for p in ps]) for a,b,ps in LINKS]
for r in GAPS+BOTTOM_PROBES:r['origin_m']=sub(r['origin_m'],SHIFT)
for w in WINDOWS:w['centre_m']=sub(w['centre_m'],SHIFT)
CENTRES=[sub(c,SHIFT) for c in CENTRES];KNOT=sub(KNOT,SHIFT)
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
root=bpy.data.objects.new('OneSideRestingLandingNet',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# The gathered endpoint is finite solid geometry; sparse net pores remain open.
bottom_checks=[]
for r in BOTTOM_PROBES:
 q,_,_,distance=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])
 assert q is not None and .005<distance<.04,('Gathered bag bottom absent',r)
 bottom_checks.append(dict(r,actual_first_hit_m=list(q),distance_m=distance))
# Geometric support footprint includes three actual finite contact facets.
def hull(points):
 points=sorted(set(tuple(p) for p in points))
 def cr(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for p in points:
  while len(lower)>=2 and cr(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 for p in reversed(points):
  while len(upper)>=2 and cr(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 return lower[:-1]+upper[:-1]
footprint=hull([v[:2] for patch in supports for tri in patch['triangles'] for v in tri['vertices_m']])
volume_sum=0;centroid_sum=Vector((0,0,0))
for o in parts:
 for tri in o.data.loop_triangles:
  a,b,c=[o.matrix_world@o.data.vertices[i].co for i in tri.vertices];vv=a.dot(b.cross(c))/6
  volume_sum+=vv;centroid_sum+=(a+b+c)*(vv/4)
centroid=centroid_sum/volume_sum
margins=[(b[0]-a[0])*(centroid.y-a[1])-(b[1]-a[1])*(centroid.x-a[0]) for a,b in zip(footprint,footprint[1:]+footprint[:1])]
assert min(margins)>0,('Geometric centroid outside finite support footprint',list(centroid),footprint)
net_evidence={'longitudinal_cord_count':12,'closed_cross_loop_count':4,'five_ray_window_probes':WINDOWS,'net_meshes':NET_NAMES,'mouth_axis':'X','mouth_centreline_points_m':CENTRES,'gathered_bottom_hit_probes':bottom_checks,'gathered_bottom_point_m':KNOT,'side_resting_pose':True,'support_hull_xy_m':footprint,'uniform_volume_centroid_m':list(centroid),'centroid_projection_inside_geometric_support_hull':True,'physics_or_load_or_catch_retention_claim':False}
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
 'single_prop_count':1,'landing_net_working_geometry':net_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fishing/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.200));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.950;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-5,-3,4),'gray-back3q':(5,3,4)} if gray else {
 'thumbnail':(5,3,4),'qa-front':(0,-7,.200),'qa-side':(-7,0,.200),'qa-top':(0,0,8),
 'qa-back':(0,7,.200),'qa-wireframe':(5,3,4)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
if '--top-only' in sys.argv:views={'qa-top':views['qa-top']}
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.145 if name=='qa-top' else 1.950
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00040;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.200)),('silhouette-128-side',(-7,0,.200))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
