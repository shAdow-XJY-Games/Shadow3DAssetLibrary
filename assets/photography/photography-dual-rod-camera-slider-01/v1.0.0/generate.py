"""Original empty dual-rod photography slider, fixed static pose only.
Two parallel polygonal rods support four genuinely bored sleeves through finite
opposed top facets. Bore-wall clearance is positive elsewhere. No motion or fit claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-dual-rod-camera-slider-01';VERSION='1.0.0';TITLE='Dual Rod Camera Slider'
DESCRIPTION=('One original static low-poly empty photography slider with two parallel circular-section rods, four genuine thick through-bored guide sleeves, one chamfered mounting platform with a true open elongated slot, two transverse end supports and four finite feet. Each guide sleeve is geometrically seated on a finite top facet of its rod, with positive clearance around the remainder of the hole. The end supports also form physical end stops. '
 'One fixed empty pose. Thirteen named editable closed meshes and four opaque constant PBR materials. No camera, tripod, head, motor, belt, labels, textures, people or surrounding scene. Metres, native Z up, front -Y; origin at ground level under the center between the rods. '
 'Geometry checks do not establish actual sliding, travel, friction, locks, precision, load capacity, strength, photographic stability, camera or head compatibility, standard mounting dimensions, manufacture or safety performance.')
G={};LINKS=[];CONTACTS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={};SEAM_PROBES=[]
PALETTE=[('Rails_SatinSilver',(.53,.59,.61,1),.32,.72),('Platform_DeepPetrol',(.035,.16,.20,1),.40,.4),('Sleeves_WarmGraphite',(.12,.14,.15,1),.48,.28),('Feet_CharcoalRubber',(.055,.064,.067,1),.85,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'motion_camera_fit_load_or_safety_claim':False}
CAMERA_FOCUS=(0,0,.081);ORTHO_SCALE=1.44
VIEWS={'gray-front3q':(2.5,-3.5,2.4),'gray-back3q':(-2.5,3.5,1.55),'thumbnail':(2.5,-3.5,2.4),'qa-front':(0,-8,1.00),'qa-side':(8,0,1.00),'qa-top':(0,0,5),'qa-back':(0,8,1.00),'qa-wireframe':(2.5,-3.5,2.4),'silhouette-128-front':(0,-8,1.00),'silhouette-128-side':(8,0,1.00)}
WIRE_THICKNESS=ORTHO_SCALE/640
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
# Every vertex below is original. Frozen earlier generators are audit-only inputs.
N=24;ROD_RADIUS=.022;BORE_RADIUS=.025;ROD_Z=.100
BORE_Z=ROD_Z-(BORE_RADIUS-ROD_RADIUS)*math.cos(math.pi/N)
CONTACT_Z=round(ROD_Z+ROD_RADIUS*math.cos(math.pi/N),7)
RODS=[];SLEEVES=[];END_BLOCKS=[];GUIDE_CONTRACTS=[]
def axis_rod(name,y):
 vs=[(x,y+ROD_RADIUS*math.cos(math.tau*i/N+math.pi/N),ROD_Z+ROD_RADIUS*math.sin(math.tau*i/N+math.pi/N)) for x in [-.530,.530] for i in range(N)]
 return mesh(name,vs,[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],0,'one continuous capped 24-sided circular-section guide rod along X')
def sleeve(name,x,y):
 # Four rings of actual points: outer-left, outer-right, inner-left, inner-right.
 # Outer body is rectangular; inner loop is a full real 24-sided circular hole.
 vs=[]
 for inner,xx in [(False,x-.036),(False,x+.036),(True,x-.036),(True,x+.036)]:
  for i in range(N):
   a=math.tau*i/N+math.pi/N;dy=math.cos(a);dz=math.sin(a)
   r=BORE_RADIUS if inner else min(.038/abs(dy),(.145-BORE_Z)/dz if dz>0 else (.059-BORE_Z)/dz)
   vs.append((xx,y+r*dy,BORE_Z+r*dz))
 fs=[]
 for i in range(N):
  j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 return mesh(name,vs,fs,2,'thick rectangular guide body with genuine through hole; top internal flat rests on finite top rod facet with no rod penetration')
def mounting_plate():
 # One closed ring-shaped chamfered plate. Hole is a 32-sided elongated oval.
 n=32;vs=[];half_x=.16;half_y=.155;ch=.018
 for inner,z in [(False,.141),(False,.163),(True,.141),(True,.163)]:
  for i in range(n):
   a=math.tau*i/n;dx=math.cos(a);dy=math.sin(a)
   if inner:x=.095*dx;y=.018*dy
   else:
    r=min(half_x/max(abs(dx),1e-12),half_y/max(abs(dy),1e-12),(half_x+half_y-ch)/max(abs(dx)+abs(dy),1e-12));x=r*dx;y=r*dy
   vs.append((x-.06,y,z))
 fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh('Platform_ChamferedEmptySlottedPlate',vs,fs,1,'single closed thick chamfered platform with genuinely open elongated mounting slot; no standard hardware compatibility claim')
for side,y in [('Front',-.11),('Back',.11)]:
 rail=axis_rod('GuideRod_'+side,y);RODS.append(rail)
 for label,x in [('Left',-.17),('Right',.05)]:
  ring=sleeve('GuideSleeve_'+side+'_'+label,x,y);SLEEVES.append(ring)
  points=[(x+dx,y+dy,CONTACT_Z) for dx in [-.025,0,.025] for dy in [-.0015,0,.0015]]
  contact={'a':rail,'b':ring,'axis':'Z','plane_m':CONTACT_Z,'patch_lo_m':[x-.036,y-ROD_RADIUS*math.sin(math.pi/N),CONTACT_Z],'patch_hi_m':[x+.036,y+ROD_RADIUS*math.sin(math.pi/N),CONTACT_Z],'minimum_patch_area_m2':.00040,'points':points,'lower_mesh':rail,'upper_mesh':ring,'normal':(0,0,1),'interior_probe_offset_m':.00005}
  CONTACTS.append(contact)
  BORES.append({'mesh':ring,'origin_m':(x-.041,y,BORE_Z),'direction':(1,0,0),'length_m':.082})
  # Finite positive bottom radial clearance extends through the whole guide body.
  lo=(x-.034,y-.001,BORE_Z-BORE_RADIUS*math.cos(math.pi/N)+.0006)
  hi=(x+.034,y+.001,ROD_Z-ROD_RADIUS*math.cos(math.pi/N)-.0006)
  void('GuideBottomClearance_'+side+'_'+label,lo,hi,'finite actual assembled radial bore clearance below rod, throughout this guide sleeve')
  GUIDE_CONTRACTS.append({'rod':rail,'sleeve':ring,'sleeve_x_center_m':x,'rod_y_center_m':y,'rod_z_center_m':ROD_Z,'bore_z_center_m':BORE_Z,'rod_radius_m':ROD_RADIUS,'bore_radius_m':BORE_RADIUS,'cross_section_sides':N,'cross_section_angle_offset_rad':math.pi/N,'contact':contact,'radial_clearance_test_x_m':x,'open_axis':'X'})
PLATFORM=mounting_plate()
for ring in SLEEVES:
 v=G[ring]['vertices'];x=sum(p[0] for p in v)/len(v);y=sum(p[1] for p in v)/len(v)
 link(ring,PLATFORM,(x,y,.143),axis=(1,0,0),spread=.020)
BORES.append({'mesh':PLATFORM,'origin_m':(-.06,0,.135),'direction':(0,0,1),'length_m':.035})
for x in [-.12,-.06,0]:GAPS.append({'label':'OpenMountingSlot_'+str(x),'origin_m':(x,0,.130),'direction':(0,0,1),'length_m':.045})
void('ClearMountingSlot',(-.125,-.010,.130),(.005,.010,.175),'finite completely open central platform slot through and beyond both faces')
for label,x in [('Left',-.55),('Right',.55)]:
 end=chamfer_box('EndSupport_Stop_'+label,(x,0,.092),.090,.350,.116,.008,1,'transverse capped support block and physical end stop; rods enter the fixed body by 25 mm');END_BLOCKS.append(end)
 for rail,y in zip(RODS,[-.11,.11]):link(end,rail,(x+(.030 if x<0 else -.030),y,ROD_Z),axis=(0,1,0),spread=.005)
 for side,y in [('Front',-.125),('Back',.125)]:
  foot=chamfer_box('Foot_'+label+'_'+side,(x,y,.019),.110,.090,.038,.010,3,'one finite chamfered grounded rubber-style foot');FEET.append(foot)
  link(foot,end,(x,y,.036),axis=(1,0,0),spread=.012)
# The center remains empty between the rods, away from the actual plate and ends.
for label,x in [('Left',-.36),('Right',.31)]:void('OpenRailBay_'+label,(x-.07,-.07,.045),(x+.07,.07,.175),'finite empty bay between both rods and away from the fixed platform and end supports')
for ring in SLEEVES:
 v=G[ring]['vertices'];x=sum(p[0] for p in v)/len(v);y=sum(p[1] for p in v)/len(v)
 WALL_PROBES.append({'mesh':ring,'label':'UpperSleeveWall_'+ring,'origin_m':(x,y,BORE_Z),'direction':(0,0,1),'length_m':.060,'minimum_wall_thickness_m':.020})
SLIDER_CONTRACT={'single_prop_count':1,'two_parallel_rod_meshes':RODS,'four_true_bored_sleeves':SLEEVES,'platform':PLATFORM,'end_support_stop_meshes':END_BLOCKS,'ground_meshes':FEET,'guide_contracts':GUIDE_CONTRACTS,'contact_plane_z_m':CONTACT_Z,'rod_cross_section_sides':N,'fixed_empty_pose_only':True,'sliding_travel_friction_clamp_camera_fit_load_or_safety_claim':False}
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
root=bpy.data.objects.new('OneOriginalDualRodPhotographySlider',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground level at center between rods';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
# Python floats use double precision over the actual Blender world-space loop triangles.
# Blender 4.3.2 BVH nearest-point results are retained below as diagnostic comparisons.
def triangle_surface_distance(vertices,point):
 a,b,c=vertices;p=tuple(float(x) for x in point);n=unit(cross(sub(b,a),sub(c,a)));signed=dot(sub(p,a),n);projected=sub(p,mul(n,signed))
 sides=[dot(cross(sub(y,x),sub(projected,x)),n) for x,y in [(a,b),(b,c),(c,a)]]
 best=abs(signed) if min(sides)>=-1e-15 or max(sides)<=1e-15 else float('inf')
 for x,y in [(a,b),(b,c),(c,a)]:
  edge=sub(y,x);u=max(0.,min(1.,dot(sub(p,x),edge)/dot(edge,edge)));delta=sub(p,add(x,mul(edge,u)));best=min(best,math.sqrt(dot(delta,delta)))
 return best
def actual_loop_triangles(name):
 o=byname[name];o.data.calc_loop_triangles();v=[tuple(float(c) for c in o.matrix_world@p.co) for p in o.data.vertices]
 return [tuple(v[i] for i in t.vertices) for t in o.data.loop_triangles]
def actual_surface_distance(name,point):return min(triangle_surface_distance(t,point) for t in actual_loop_triangles(name))
def finite_face_distance_controls():
 rows=[]
 for name in RODS:
  actual=actual_loop_triangles(name);top=[t for t in actual if max(abs(v[2]-CONTACT_Z) for v in t)<1e-6];assert len(top)==2
  for i,triangle in enumerate(top):
   centroid=mul(add(add(triangle[0],triangle[1]),triangle[2]),1/3)
   for delta in [-.000050,-.000010,0,.000010,.000050]:
    p=add(centroid,(0,0,delta));actual_distance=actual_surface_distance(name,p);expected=abs(delta)
    assert abs(actual_distance-expected)<1e-9 and (actual_distance<1e-6)==(delta==0),('Near-face distance control failed',name,i,delta,actual_distance)
    rows.append({'rod':name,'case':'actual_triangle_centroid_normal_offset','triangle':i,'point_m':p,'offset_m':delta,'expected_distance_m':expected,'actual_distance_m':actual_distance,'contact_predicate':actual_distance<1e-6})
  shared=sorted(set(top[0])&set(top[1]));assert len(shared)==2;mid=mul(add(shared[0],shared[1]),.5)
  for i,triangle in enumerate(top):
   d=triangle_surface_distance(triangle,mid);assert d<1e-9
   rows.append({'rod':name,'case':'actual_common_edge_midpoint','triangle':i,'point_m':mid,'expected_distance_m':0.,'actual_distance_m':d,'contact_predicate':d<1e-6})
   vertex=next(v for v in triangle if v not in shared);edge=unit(sub(shared[1],shared[0]));toward=sub(vertex,mid);perp=unit(sub(toward,mul(edge,dot(toward,edge))));p=sub(mid,mul(perp,.000020));d=triangle_surface_distance(triangle,p)
   assert abs(d-.000020)<1e-9 and d>=1e-6,('Outside-edge distance control failed',name,i,d)
   rows.append({'rod':name,'case':'outside_actual_triangle_common_edge_in_plane','triangle':i,'point_m':p,'expected_distance_m':.000020,'actual_distance_m':d,'contact_predicate':d<1e-6,'scope':'individual actual triangle; adjacent triangle is excluded for this control'})
 return rows
nearest_controls=finite_face_distance_controls()
face_contacts=[]
for r in CONTACTS:
 points=[]
 for p in r['points']:
  point=Vector(p);eps=r['interior_probe_offset_m'];up=Vector(r['normal']);ta=trees[r['lower_mesh']];tb=trees[r['upper_mesh']]
  da=actual_surface_distance(r['lower_mesh'],point);db=actual_surface_distance(r['upper_mesh'],point);bvh_da=ta.find_nearest(point)[3];bvh_db=tb.find_nearest(point)[3]
  valid=da<1e-6 and db<1e-6 and inside(ta,point-up*eps) and inside(tb,point+up*eps) and not inside(ta,point+up*eps) and not inside(tb,point-up*eps)
  assert valid,('True face contact failed',r['a'],r['b'],p,da,db)
  points.append({'point_m':list(p),'lower_surface_distance_m':da,'upper_surface_distance_m':db,'distance_method':'all_actual_loop_triangles_float64','bvh_lower_surface_distance_m':bvh_da,'bvh_upper_surface_distance_m':bvh_db,'opposed_interior_sides_verified':True})
 face_contacts.append(dict(r,actual_surface_point_checks=points))
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
slider_evidence=dict(SLIDER_CONTRACT,finite_empty_volume_checks=void_volume_checks,actual_shell_thickness_checks=wall_checks,material_contract=MATERIAL_CONTRACT,actual_recessed_seam_checks=seam_checks)
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
 'single_prop_count':1,'slider_geometry':slider_evidence,'finite_opposed_face_contacts':face_contacts,'actual_triangle_nearest_distance_controls':nearest_controls,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
focus=Vector(CAMERA_FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO_SCALE;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-back-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={name:VIEWS[name] for name in ['gray-front3q','gray-back3q']} if gray else {name:VIEWS[name] for name in ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe']}
if '--gray-back-only' in sys.argv:views={'gray-back3q':views['gray-back3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO_SCALE
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-back-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name in ['silhouette-128-front','silhouette-128-side']:render(name,VIEWS[name])
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
