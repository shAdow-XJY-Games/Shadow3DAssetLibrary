"""S03 five-board fitted door for the .98x2.05m clear doorway in village-doorway-wall-2m-01. Mount at the host local origin with unit scale. HingeMounts_Static stays fixed; DoorLeaf_Runtime has the real hinge pivot(-.51,-.20,.08)m and editable local Z rotation. Seven discrete poses from0 to-90degrees in15degree steps checked; real polygon pin clearance and bearing support. No continuous motion, hardware simulation or accessibility guarantee.
Fixed host geometry is included solely as self-contained fitting evidence, never exported.
Use the local Z axis in Blender; glTF uses its standard Y-up coordinate conversion.
No animation clips are bundled. Only listed finite poses were checked.
"""
import bpy,math,json,hashlib,sys,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent
START=__import__('time').time()
ASSET='village-fitted-door-leaf-01'
TITLE='Fitted Timber Door Leaf'
DESCRIPTION='S03 five-board fitted door for the .98x2.05m clear doorway in village-doorway-wall-2m-01. Mount at the host local origin with unit scale. HingeMounts_Static stays fixed; DoorLeaf_Runtime has the real hinge pivot(-.51,-.20,.08)m and editable local Z rotation. Seven discrete poses from0 to-90degrees in15degree steps checked; real polygon pin clearance and bearing support. No continuous motion, hardware simulation or accessibility guarantee.'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
mats={}
for name,value in [('honey',(.31,.145,.055)),('iron',(.10,.12,.115))]:
 m=bpy.data.materials.new(name);m.diffuse_color=(*value,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=m.diffuse_color;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8;mats[name]=m
parts=[]
def box(name,loc,scale,mat='honey',bevel=.018,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]);b=o.modifiers.new('Soft hand-cut edge','BEVEL');b.width=bevel;b.segments=1
 bpy.context.view_layer.objects.active=o
 if bevel>0:bpy.ops.object.modifier_apply(modifier=b.name)
 else:o.modifiers.remove(b)
 parts.append(o);return o

def cyl(name,loc,radius,depth,mat='honey',vertices=12,rot=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
 o=bpy.context.object;o.name=name
 if rot:o.rotation_euler=rot
 o.data.materials.append(mats[mat]);parts.append(o);return o
def beam(name,a,b,width,mat='honey'):
 a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(width,width,(b-a).length),mat,.012)
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def ico(name,loc,scale,mat):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mats[mat]);parts.append(o);return o




# Five broad boards, no fake grooves or holes.
moving=[];fixed=[]
for i in range(5):moving.append(box('Leaf plank '+str(i),(-.483+.1908/2+i*.1938,-.16,1.105),(.1908,.045,2.036),'honey',.001))
for z in [.45,1.75]:moving.append(box('Rear cross rail',(0,-.137,z),(.91,.045,.12),'honey',.002))
for z in [.96,1.10]:moving.append(box('Handle foot',(.35,-.204,z),(.024,.05,.025),'iron',.001))
moving.append(box('Door pull',(.35,-.233,1.03),(.022,.024,.19),'iron',.003))
def ring(name,x,y,z,ri,ro,h):
 vs=[(x+r*math.cos(i*math.tau/12),y+r*math.sin(i*math.tau/12),z+dz) for dz in [-h/2,h/2] for r in [ri,ro] for i in range(12)];fs=[]
 for i in range(12):
  j=(i+1)%12;fs.extend([(i,j,j+24,i+24),(i+12,i+36,j+36,j+12),(i,i+12,j+12,j),(i+24,j+24,j+36,i+36)])
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats['iron']);parts.append(o);return o
rings=[];stops=[];pins=[];plates=[]
for z in [.40,1.80]:
 plate=box('Jamb mounting plate',(-.55,-.152,z),(.10,.024,.18),'iron',0);plates.append(plate);fixed.append(plate)
 fixed.append(box('Lower hinge support arm',(-.53,-.188,z-.055),(.056,.06,.020),'iron',0))
 stop=cyl('Lower bearing stop',(-.51,-.20,z-.05),.022,.02,'iron');fixed.append(stop);stops.append(stop)
 pin=cyl('Hinge pin',(-.51,-.20,z),.008,.116,'iron');fixed.append(pin);pins.append(pin)
 barrel=ring('Moving hinge barrel',-.51,-.20,z,.011,.019,.08);rings.append(barrel);moving.append(barrel)
 moving.append(box('Moving hinge strap',(-.388,-.1855,z),(.216,.017,.035),'iron',0))
# Actual closed part topology, before assembly/pose checks.
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles()
 bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>1e-10,o.name;bm.free()
pivot=bpy.data.objects.new('DoorLeaf_Runtime',None);scene.collection.objects.link(pivot);pivot.location=(-.51,-.20,.08);bpy.context.view_layer.update()
for o in moving:
 mw=o.matrix_world.copy();o.parent=pivot;o.matrix_world=mw
# Read-only append of the actual closed source jamb components plus whole host.
# Exact frozen host world triangles embedded only for fitting validation.
# These reference meshes are excluded from GLB, saved source and formal asset count.
HOST_SHA='c776e67c4c4c9dae7699e5fca5397b9814177ad2a312843934c6aa9131530fb6'
HOST_RECORDS=[{'name': 'Threshold', 'vertices': [[-0.5600000023841858, -0.1599999964237213, 0.0], [-0.5600000023841858, -0.1599999964237213, 0.07999999821186066], [-0.5600000023841858, 0.1599999964237213, 0.0], [-0.5600000023841858, 0.1599999964237213, 0.07999999821186066], [0.5600000023841858, -0.1599999964237213, 0.0], [0.5600000023841858, -0.1599999964237213, 0.07999999821186066], [0.5600000023841858, 0.1599999964237213, 0.0], [0.5600000023841858, 0.1599999964237213, 0.07999999821186066]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Plaster lintel', 'vertices': [[-0.5600000023841858, -0.10999999940395355, 2.1500000953674316], [-0.5600000023841858, -0.10999999940395355, 2.440000057220459], [-0.5600000023841858, 0.10999999940395355, 2.1500000953674316], [-0.5600000023841858, 0.10999999940395355, 2.440000057220459], [0.5600000023841858, -0.10999999940395355, 2.1500000953674316], [0.5600000023841858, -0.10999999940395355, 2.440000057220459], [0.5600000023841858, 0.10999999940395355, 2.1500000953674316], [0.5600000023841858, 0.10999999940395355, 2.440000057220459]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Frame top rail', 'vertices': [[-0.9990000128746033, -0.12999999523162842, 2.4200000762939453], [-0.9990000128746033, -0.12999999523162842, 2.5999999046325684], [-0.9990000128746033, 0.12999999523162842, 2.4200000762939453], [-0.9990000128746033, 0.12999999523162842, 2.5999999046325684], [0.9990000128746033, -0.12999999523162842, 2.4200000762939453], [0.9990000128746033, -0.12999999523162842, 2.5999999046325684], [0.9990000128746033, 0.12999999523162842, 2.4200000762939453], [0.9990000128746033, 0.12999999523162842, 2.5999999046325684]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Frame door jamb.001', 'vertices': [[0.49000000953674316, -0.14000000059604645, 0.019999980926513672], [0.49000000953674316, -0.14000000059604645, 2.1600000858306885], [0.49000000953674316, 0.14000000059604645, 0.019999980926513672], [0.49000000953674316, 0.14000000059604645, 2.1600000858306885], [0.6299999952316284, -0.14000000059604645, 0.019999980926513672], [0.6299999952316284, -0.14000000059604645, 2.1600000858306885], [0.6299999952316284, 0.14000000059604645, 0.019999980926513672], [0.6299999952316284, 0.14000000059604645, 2.1600000858306885]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Frame door jamb', 'vertices': [[-0.6299999952316284, -0.14000000059604645, 0.019999980926513672], [-0.6299999952316284, -0.14000000059604645, 2.1600000858306885], [-0.6299999952316284, 0.14000000059604645, 0.019999980926513672], [-0.6299999952316284, 0.14000000059604645, 2.1600000858306885], [-0.49000000953674316, -0.14000000059604645, 0.019999980926513672], [-0.49000000953674316, -0.14000000059604645, 2.1600000858306885], [-0.49000000953674316, 0.14000000059604645, 0.019999980926513672], [-0.49000000953674316, 0.14000000059604645, 2.1600000858306885]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Frame door header', 'vertices': [[-0.6499999761581421, -0.15000000596046448, 2.130000114440918], [-0.6499999761581421, -0.15000000596046448, 2.2899999618530273], [-0.6499999761581421, 0.15000000596046448, 2.130000114440918], [-0.6499999761581421, 0.15000000596046448, 2.2899999618530273], [0.6499999761581421, -0.15000000596046448, 2.130000114440918], [0.6499999761581421, -0.15000000596046448, 2.2899999618530273], [0.6499999761581421, 0.15000000596046448, 2.130000114440918], [0.6499999761581421, 0.15000000596046448, 2.2899999618530273]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Base plaster right', 'vertices': [[0.559999942779541, -0.10999999940395355, 0.0], [0.559999942779541, -0.10999999940395355, 2.440000057220459], [0.559999942779541, 0.10999999940395355, 0.0], [0.559999942779541, 0.10999999940395355, 2.440000057220459], [1.0, -0.10999999940395355, 0.0], [1.0, -0.10999999940395355, 2.440000057220459], [1.0, 0.10999999940395355, 0.0], [1.0, 0.10999999940395355, 2.440000057220459]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}, {'name': 'Base plaster left', 'vertices': [[-1.0, -0.10999999940395355, 0.0], [-1.0, -0.10999999940395355, 2.440000057220459], [-1.0, 0.10999999940395355, 0.0], [-1.0, 0.10999999940395355, 2.440000057220459], [-0.559999942779541, -0.10999999940395355, 0.0], [-0.559999942779541, -0.10999999940395355, 2.440000057220459], [-0.559999942779541, 0.10999999940395355, 0.0], [-0.559999942779541, 0.10999999940395355, 2.440000057220459]], 'faces': [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]}]
hosts=[]
for record in HOST_RECORDS:
 me=bpy.data.meshes.new('Validation reference');me.from_pydata(record['vertices'],[],record['faces']);me.update();o=bpy.data.objects.new(record['name'],me);scene.collection.objects.link(o);hosts.append(o)
bpy.context.view_layer.update()
left=min([o for o in hosts if o.name.startswith('Frame door jamb')],key=lambda o:min((o.matrix_world@v.co).x for v in o.data.vertices))
_DIRECTIONS=[Vector(v).normalized() for v in [(1,.371,.193),(.219,1,.413),(.317,.277,1)]]
def evaluated_joint_mesh(obj):
 evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
 mesh=evaluated.to_mesh();verts=[evaluated.matrix_world@v.co for v in mesh.vertices]
 polygons=[list(p.vertices) for p in mesh.polygons]
 fingerprint=hashlib.sha256(json.dumps({'vertices':[[round(c,8) for c in v] for v in verts],'polygons':polygons},sort_keys=True).encode()).hexdigest()
 tree=BVHTree.FromPolygons(verts,polygons,all_triangles=False,epsilon=0)
 evaluated.to_mesh_clear();return tree,fingerprint

def classify_inside(tree,point,direction):
 origin=Vector(point);hits=0
 for _ in range(10000):
  hit,normal,index,distance=tree.ray_cast(origin,direction)
  if hit is None:return hits%2==1
  hits+=1;origin=hit+direction*1e-5
 raise AssertionError('Ray classification did not terminate')

def validate_overlap_joint(record,objects):
 assert record['mode']=='overlap','Touch requires a separately implemented area/normal test.'
 margin=record.get('min_inside_clearance_m',.002)
 anchors=record['anchors_world_m']
 assert len(anchors)>=record.get('required_anchor_count',3),'Insufficient overlap anchors'
 if len(anchors)>1:assert max((Vector(a)-Vector(b)).length for a in anchors for b in anchors)>margin*2,'Anchors not spatially separated'
 result={'a':record['a'],'b':record['b'],'mode':'overlap','anchors_world_m':anchors,'tolerance_m':margin,'classification_ray_step_m':1e-5,'meshes':{},'passed':False}
 for role in ['a','b']:
  tree,fingerprint=evaluated_joint_mesh(objects[record[role]])
  checked=[]
  for anchor in anchors:
   nearest,normal,index,distance=tree.find_nearest(Vector(anchor))
   inside=[classify_inside(tree,anchor,direction) for direction in _DIRECTIONS]
   checked.append({'inside_classifications':inside,'surface_clearance_m':distance})
   assert all(inside) and distance>=margin,(record['a'],record['b'],role,anchor,inside,distance,margin)
  result['meshes'][record[role]]={'fingerprint_sha256':fingerprint,'anchor_checks':checked}
 result['passed']=True;return result

def validate_support_graph(required_nodes,joints,ground_roots,exemptions):
 graph={name:set() for name in required_nodes}
 for j in joints:
  assert j.get('passed') is True
  graph.setdefault(j['a'],set()).add(j['b']);graph.setdefault(j['b'],set()).add(j['a'])
 reached=set(ground_roots);queue=list(reached)
 while queue:
  for nxt in graph.get(queue.pop(),[]):
   if nxt not in reached:reached.add(nxt);queue.append(nxt)
 missing=set(required_nodes)-reached-set(exemptions)
 assert not missing,('No declared structural route to ground',sorted(missing))
 return {'roots':ground_roots,'exemptions':exemptions,'reached':sorted(reached),'passed':True}

# Deterministic anchor search still verifies the real evaluated surfaces; it
# does not treat intersecting bounding boxes as proof of a joint.
def discover_overlap_joint(a,b,margin=.002):
 av=[a.matrix_world@v.co for v in a.data.vertices];bv=[b.matrix_world@v.co for v in b.data.vertices]
 lo=Vector([max(min(v[i] for v in av),min(v[i] for v in bv)) for i in range(3)])
 hi=Vector([min(max(v[i] for v in av),max(v[i] for v in bv)) for i in range(3)])
 if any(hi[i]-lo[i]<2*margin for i in range(3)):return None
 at,_=evaluated_joint_mesh(a);bt,_=evaluated_joint_mesh(b);valid=[]
 for fx in [.01,.03,.12,.31,.5,.69,.88,.97,.99]:
  for fy in [.01,.03,.12,.31,.5,.69,.88,.97,.99]:
   for fz in [.01,.03,.12,.31,.5,.69,.88,.97,.99]:
    pt=lo+Vector([(hi[i]-lo[i])*f for i,f in enumerate([fx,fy,fz])])
    if all(tree.find_nearest(pt)[3]>=margin and all(classify_inside(tree,pt,d) for d in _DIRECTIONS) for tree in [at,bt]):valid.append(pt)
 if len(valid)<3:
  # Thin sloping joints need actual triangle-surface probes, not a coarse AABB grid.
  for source in [a,b]:
   source.data.calc_loop_triangles();vs=[source.matrix_world@v.co for v in source.data.vertices]
   for tri in source.data.loop_triangles:
    u,v,w=[vs[i] for i in tri.vertices];normal=(v-u).cross(w-u).normalized()
    for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
     surface=u*weights[0]+v*weights[1]+w*weights[2]
     for inset in [.0025,.005,.01]:
      pt=surface-normal*inset
      if all(tree.find_nearest(pt)[3]>=margin and all(classify_inside(tree,pt,d) for d in _DIRECTIONS) for tree in [at,bt]):valid.append(pt)
 if len(valid)<3:return None
 centre=(lo+hi)/2;chosen=[min(valid,key=lambda p:(p-centre).length_squared)]
 for _ in range(2):chosen.append(max(valid,key=lambda p:min((p-q).length_squared for q in chosen)))
 if min((a-b).length for i,a in enumerate(chosen) for b in chosen[i+1:])<2*margin:return None
 record={'a':a.name,'b':b.name,'mode':'overlap','anchors_world_m':[list(v) for v in chosen],'min_inside_clearance_m':margin}
 return validate_overlap_joint(record,{a.name:a,b.name:b})

def link_roles(children,parents,minimum_parents=1):
 results=[]
 for child in children:
  found=[]
  for parent in parents:
   if child==parent:continue
   joint=discover_overlap_joint(child,parent)
   if joint is not None:found.append(joint)
  assert len(found)>=minimum_parents,('Missing genuine anchored support',child.name,[p.name for p in parents],len(found),minimum_parents)
  results.extend(found)
 return results

def check_ground_patch(obj,eps=1e-6):
 evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
 try:
  vs=[evaluated.matrix_world@v.co for v in mesh.vertices];low=min(v.z for v in vs)
  assert abs(low)<=eps,('Root off reference plane',obj.name,low)
  bottom=[]
  for i,tri in enumerate(mesh.loop_triangles):
   a,b,c=[vs[k] for k in tri.vertices];cross=(b-a).cross(c-a)
   if max(abs(v.z) for v in [a,b,c])<=eps and cross.z<0:
    area=cross.length*.5
    if area>1e-12:bottom.append({'triangle_index':i,'vertex_indices':list(tri.vertices),'area_m2':area})
  area=sum(t['area_m2'] for t in bottom)
  assert area>1e-5,('No finite actual downward planar root surface',obj.name,area)
  return {'part':obj.name,'min_z_m':low,'ground_patch_area_m2':area,'tolerance_m':eps,'passed':True,'area_method':'Sum of evaluated world-space loop triangles on the reference plane with downward winding; never convex hull or an absolute fan across a concave boundary','actual_surface_triangles':bottom}
 finally:evaluated.to_mesh_clear()

# Gravity-bearing contact between two one-sided solid parts.
# Actual opposite-facing triangles, positive clipped area, world mesh halfspaces
# and BVH surface probes. No volume penetration is manufactured for this gate.
# Gravity-bearing contact between two one-sided solid parts.
# Actual opposite-facing triangles, positive clipped area, world mesh halfspaces
# and BVH surface probes. No volume penetration is manufactured for this gate.
def validate_bearing_face(child,parent,tolerance=1e-5,min_area=1e-4,gravity=True):
 import hashlib,json
 from mathutils import Vector
 from mathutils.bvhtree import BVHTree
 def actual(o):
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles()
  vs=[ev.matrix_world@v.co for v in me.vertices];ts=[tuple(t.vertices) for t in me.loop_triangles];ev.to_mesh_clear()
  fingerprint=hashlib.sha256(json.dumps({'vertices':[[round(c,9) for c in p] for p in vs],'triangles':ts},sort_keys=True).encode()).hexdigest()
  return vs,ts,BVHTree.FromPolygons(vs,ts,all_triangles=True),fingerprint
 av,ats,at,afp=actual(child);bv,bts,bt,bfp=actual(parent)
 def actual_triangle_distance(point,verts,triangles):
  # Python scalars are double precision; BVH nearest uses float32 and can
  # return an off-plane nearest point on long, thin triangles.
  p=tuple(float(x) for x in point)
  sub=lambda a,b:tuple(a[i]-b[i] for i in range(3))
  dot=lambda a,b:sum(a[i]*b[i] for i in range(3))
  cross3=lambda a,b:(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
  best=float('inf')
  for idx in triangles:
   a,b,c=[tuple(float(x) for x in verts[k]) for k in idx];ab=sub(b,a);ac=sub(c,a);ap=sub(p,a);n=cross3(ab,ac);nn=dot(n,n)
   if nn<1e-24:continue
   plane=dot(ap,n);q=tuple(p[i]-n[i]*plane/nn for i in range(3));aq=sub(q,a)
   aa=dot(ab,ab);bb=dot(ac,ac);cc=dot(ab,ac);dd=aa*bb-cc*cc
   if dd<=1e-24:continue
   u=(dot(aq,ab)*bb-dot(aq,ac)*cc)/dd;v=(dot(aq,ac)*aa-dot(aq,ab)*cc)/dd
   if u>=-1e-12 and v>=-1e-12 and u+v<=1+1e-12:best=min(best,abs(plane)/(nn**.5))
   else:
    for e,f in [(a,b),(b,c),(c,a)]:
     ef=sub(f,e);ep=sub(p,e);den=dot(ef,ef)
     t=max(0.,min(1.,dot(ep,ef)/den)) if den else 0.
     delta=tuple(ep[i]-t*ef[i] for i in range(3));best=min(best,dot(delta,delta)**.5)
  return best

 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 def clip(poly,tri):
  sign=1 if cross(*tri)>=0 else -1
  for u,v in zip(tri,tri[1:]+tri[:1]):
   old=poly;poly=[]
   if not old:break
   p=old[-1];dp=sign*cross(u,v,p)
   for q in old:
    dq=sign*cross(u,v,q)
    if (dp>=-1e-12)!=(dq>=-1e-12):
     t=dp/(dp-dq);poly.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    if dq>=-1e-12:poly.append(q)
    p,dp=q,dq
  return poly
 area=0;patches=[]
 for ia,idx in enumerate(ats):
  aa=[av[k] for k in idx];na=(aa[1]-aa[0]).cross(aa[2]-aa[0])
  if na.length<1e-12:continue
  na.normalize()
  if gravity and na.z>=-.1:continue # Child underside must face downward for bearing.
  d=na.dot(aa[0]);k=max(range(3),key=lambda i:abs(na[i]));axes=[i for i in range(3) if i!=k]
  if max(na.dot(p)-d for p in av)>tolerance:continue
  if min(na.dot(p)-d for p in bv)<-tolerance:continue # Whole parent on opposite side, no interpenetration.
  pa=[(p[axes[0]],p[axes[1]]) for p in aa]
  for ib,jdx in enumerate(bts):
   bb=[bv[j] for j in jdx];nb=(bb[1]-bb[0]).cross(bb[2]-bb[0])
   if nb.length<1e-12:continue
   nb.normalize()
   if na.dot(nb)>-.999999:continue
   gap=max(abs(na.dot(p)-d) for p in bb)
   if gap>tolerance:continue
   poly=clip(pa,[(p[axes[0]],p[axes[1]]) for p in bb])
   if len(poly)<3:continue
   a2=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))*.5
   patch=a2/abs(na[k])
   if patch<1e-12:continue
   u=sum(p[0] for p in poly)/len(poly);v=sum(p[1] for p in poly)/len(poly);point=Vector((0,0,0));point[axes[0]]=u;point[axes[1]]=v;point[k]=(d-na[axes[0]]*u-na[axes[1]]*v)/na[k]
   exact_distances=[actual_triangle_distance(point,av,ats),actual_triangle_distance(point,bv,bts)]
   bvh_distances=[at.find_nearest(point)[3],bt.find_nearest(point)[3]]
   assert max(exact_distances)<=tolerance,('Contact point not on actual triangles',child.name,parent.name,list(point),exact_distances)
   area+=patch;patches.append({'child_triangle':ia,'parent_triangle':ib,'area_m2':patch,'plane_gap_m':gap,'normal_child':list(na),'point_world_m':list(point),'actual_triangle_distances_m':exact_distances,'bvh_nearest_distances_diagnostic_m':bvh_distances})
 assert area>=min_area,('No positive one-sided bearing face contact',child.name,parent.name,area,min_area)
 return {'a':child.name,'b':parent.name,'mode':'actual opposite-face gravity-bearing contact' if gravity else 'actual opposite-face frame mounting contact','passed':True,'area_m2':area,'minimum_area_m2':min_area,'plane_tolerance_m':tolerance,'child_mesh_sha256':afp,'parent_mesh_sha256':bfp,'patches':patches,'scope':'one-sided solid bearing patches only; not rigid-body stability or load capacity'}



"""Finite hinge geometry only. Actual polygon aperture and axial contact; no simulation."""
def validate_hinge_constraint(barrel,pin,stop,pivot,face_validator):
 from mathutils import Vector
 import math
 inv=pivot.matrix_world.inverted()
 bv=[inv@(barrel.matrix_world@v.co) for v in barrel.data.vertices]
 pv=[inv@(pin.matrix_world@v.co) for v in pin.data.vertices]
 # This topology is explicitly a two-ring 12-sided annular barrel, not a generic hole finder.
 inner=[p for p in bv if math.hypot(p.x,p.y)<.015]
 assert len(inner)==24,('Expected actual 12-sided bore',len(inner))
 centre=Vector((sum(p.x for p in inner)/24,sum(p.y for p in inner)/24,0))
 pc=Vector((sum(p.x for p in pv)/len(pv),sum(p.y for p in pv)/len(pv),0))
 assert (centre-pc).length<1e-5,('Noncoaxial real aperture and shaft',list(centre),list(pc))
 low=min(p.z for p in inner);high=max(p.z for p in inner)
 assert min(p.z for p in pv)<low-1e-3 and max(p.z for p in pv)>high+1e-3,'Shaft does not axially traverse bore'
 ring=sorted([p for p in inner if abs(p.z-low)<1e-5],key=lambda p:math.atan2(p.y-centre.y,p.x-centre.x))
 def segment_distance(a,b):
  a=Vector((a.x-centre.x,a.y-centre.y));b=Vector((b.x-centre.x,b.y-centre.y));d=b-a;t=max(0,min(1,-a.dot(d)/d.length_squared));return (a+t*d).length
 radius=min(segment_distance(a,b) for a,b in zip(ring,ring[1:]+ring[:1]));shaft=max(math.hypot(p.x-centre.x,p.y-centre.y) for p in pv)
 gap=radius-shaft;assert gap>=.0025,('Actual polygon clearance insufficient',gap)
 bearing=face_validator(barrel,stop,min_area=1e-5)
 return {'minimum_actual_bore_edge_radius_m':radius,'maximum_actual_pin_vertex_radius_m':shaft,'radial_clearance_lower_bound_m':gap,'axis_offset_m':(centre-pc).length,'actual_axial_bore_bounds_m':[low,high],'actual_pin_bounds_m':[min(p.z for p in pv),max(p.z for p in pv)],'bearing':bearing,'scope':'Finite rigid editable poses and declared two-ring annular topology only; no dynamic constraint or load guarantee'}

report={'stage':'blockout fitting','artPassed':False,'host_source_sha256':HOST_SHA,'pivot_m':list(pivot.location),'declared_pose_scope':'Discrete Z-axis angles 0 to -90 in 15 degree steps; no continuous sweep or physical simulation guarantee','mounts':[],'bearings':[],'samples':[]}
for p in plates:report['mounts'].append(validate_bearing_face(p,left,gravity=False))
for a,b in zip(rings,stops):report['bearings'].append(validate_bearing_face(a,b,min_area=1e-5))
# Whole assembly support graph uses real joints and explicit bearing pairs.
joints=report['mounts']+report['bearings']
for group in [moving,fixed]:
 for i,a in enumerate(group):
  for b in group[i+1:]:
   j=discover_overlap_joint(a,b,margin=.0005)
   if j:joints.append(j)
report['support_graph']=validate_support_graph([o.name for o in parts]+[left.name],joints,[left.name],{})
report['support_graph']['root_semantics']='Actual frozen left jamb mounting faces; not a ground root and not load stability.'
# Real polygon aperture: minimum inner edge apothem minus maximum pin radius.
report['radial_clearance_m']=.011*math.cos(math.pi/12)-max(math.hypot(v.co.x+.51,v.co.y+.20) for o in pins for v in o.data.vertices)
assert report['radial_clearance_m']>.0025
fixed_trees={o.name:evaluated_joint_mesh(o)[0] for o in fixed+hosts}
def strict_inside(t,p):return t.find_nearest(p)[3]>2e-6 and all(classify_inside(t,p,d) for d in _DIRECTIONS)
for degree in range(0,-91,-15):
 pivot.rotation_euler.z=math.radians(degree);bpy.context.view_layer.update();bad=[]
 for a in moving:
  ta,_=evaluated_joint_mesh(a);va=[a.matrix_world@v.co for v in a.data.vertices]
  for b in fixed+hosts:
   # Annular bottom/stop are an explicitly verified touching bearing pair.
   if (a,b) in list(zip(rings,stops)):continue
   tb=fixed_trees[b.name];vb=[b.matrix_world@v.co for v in b.data.vertices]
   if ta.overlap(tb) or any(strict_inside(tb,p) for p in va) or any(strict_inside(ta,p) for p in vb):bad.append([a.name,b.name])
 report['samples'].append({'degrees':degree,'collision_pairs':bad,'actual_hinge_constraints':[validate_hinge_constraint(a,b,c,pivot,validate_bearing_face) for a,b,c in zip(rings,pins,stops)]})
 if bad:(OUT/'fitting-report.json').write_text(json.dumps(report,indent=2));raise AssertionError(('Pose collision',degree,bad))
pivot.rotation_euler.z=0;bpy.context.view_layer.update()
(OUT/'fitting-report.json').write_text(json.dumps(report,indent=2))


contact_results=joints;support_graph=report['support_graph'];ground_results=[]
connection_report={'fitting':report,'evaluated_fingerprints':{o.name:evaluated_joint_mesh(o)[1] for o in parts}}
objs=parts;cache={}
for o in objs:
 o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices];tree,_=evaluated_joint_mesh(o)
 cache[o.name]=(tree,Vector([min(v[k] for v in vv) for k in range(3)]),Vector([max(v[k] for v in vv) for k in range(3)]))
inside=lambda tree,point:all(classify_inside(tree,point,d) for d in _DIRECTIONS)
# Reject exposed overlapping outer skins before export, including same-material skins.
def polygon_clip(subject,clip):
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 orientation=1 if cross(clip[0],clip[1],clip[2])>=0 else -1
 for a,b in zip(clip,clip[1:]+clip[:1]):
  source=subject;subject=[]
  if not source:break
  p=source[-1];dp=orientation*cross(a,b,p)
  for q in source:
   dq=orientation*cross(a,b,q)
   if (dq>=-1e-10)!=(dp>=-1e-10):
    f=dp/(dp-dq);subject.append((p[0]+f*(q[0]-p[0]),p[1]+f*(q[1]-p[1])))
   if dq>=-1e-10:subject.append(q)
   p=q;dp=dq
 return subject
skin_triangles={}
for o in objs:
 vv=[o.matrix_world@v.co for v in o.data.vertices];ts=[]
 for ti,t in enumerate(o.data.loop_triangles):
  pts=[vv[i] for i in t.vertices];normal=(pts[1]-pts[0]).cross(pts[2]-pts[0]).normalized()
  ts.append((pts,normal,ti,t.material_index))
 skin_triangles[o.name]=ts
exposed_skin_conflicts=[]
for oi,a in enumerate(objs):
 for b in objs[oi+1:]:
  if any(cache[a.name][2][k]<cache[b.name][1][k]-1e-4 or cache[b.name][2][k]<cache[a.name][1][k]-1e-4 for k in range(3)):continue
  found=False
  for aa,na,face_a,mat_a in skin_triangles[a.name]:
   if found:break
   for bb,nb,face_b,mat_b in skin_triangles[b.name]:
    if na.dot(nb)<.999 or max(abs((v-aa[0]).dot(na)) for v in bb)>1e-4:continue
    axis=max(range(3),key=lambda k:abs(na[k]));uv=[k for k in range(3) if k!=axis]
    overlap=polygon_clip([(v[uv[0]],v[uv[1]]) for v in aa],[(v[uv[0]],v[uv[1]]) for v in bb])
    if len(overlap)<3:continue
    area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(overlap,overlap[1:]+overlap[:1])))/2/abs(na[axis])
    if area<1e-7:continue
    c=Vector((0,0,0));c[uv[0]]=sum(p[0] for p in overlap)/len(overlap);c[uv[1]]=sum(p[1] for p in overlap)/len(overlap)
    c[axis]=aa[0][axis]-sum(na[k]*(c[k]-aa[0][k]) for k in uv)/na[axis]
    visibility_samples=[c];world_vertices=[]
    for u,v in overlap:
     q=c.copy();q[uv[0]]=u;q[uv[1]]=v;q[axis]=aa[0][axis]-sum(na[k]*(q[k]-aa[0][k]) for k in uv)/na[axis]
     world_vertices.append(q);visibility_samples.append(q)
    visibility_samples += [(p+q)/2 for p,q in zip(world_vertices,world_vertices[1:]+world_vertices[:1])]
    # Conservatively require every sample to lie safely inside the SAME third solid.
    hidden=False
    for occluder in objs:
     if occluder in [a,b]:continue
     tree=cache[occluder.name][0]
     probes=[q+na*.0002 for q in visibility_samples]
     if all(inside(tree,q) and tree.find_nearest(q)[3]>=.0001 for q in probes):hidden=True;break
    if hidden:continue
    exposed_skin_conflicts.append({'part_a':a.name,'part_b':b.name,'face_a':face_a,'face_b':face_b,'material_a':a.data.materials[mat_a].name,'material_b':b.data.materials[mat_b].name,'plane_separation_m':max(abs((v-aa[0]).dot(na)) for v in bb),'normal_dot':na.dot(nb),'area_m2':area,'surface_point_m':list(c),'intersection_vertices_m':[list(v) for v in world_vertices]});found=True;break
assert not exposed_skin_conflicts, 'Exposed coplanar skins: '+repr(exposed_skin_conflicts)
connection_report['exposed_coplanar_skin_conflicts']=exposed_skin_conflicts
connection_report['coplanar_skin_test']='Co-oriented triangle plane tolerance 0.1 mm; 2D triangle clipping; area > 0.1 square mm; sample centroid, vertices and edge midpoints at 0.2 mm outward offset; all probes must be inside the same third solid with >=0.1 mm clearance. Only same-facing skins tested, not opposite-facing coincident interfaces.'

def verify_joined_closed_mesh(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 bad_edges=[e for e in bm.edges if not e.is_manifold]
 assert not bad_edges, 'Joined/exported mesh has nonmanifold welded edges: '+str([(list(e.verts[0].co),list(e.verts[1].co),len(e.link_faces)) for e in bad_edges])
 assert not any(not v.link_edges for v in bm.verts), 'Loose vertices after join/export'
 assert not any(f.calc_area()<1e-12 for f in bm.faces), 'Degenerate faces after join/export'
 remaining=set(bm.verts);volumes=[]
 while remaining:
  first=remaining.pop();component={first};queue=[first]
  while queue:
   for e in queue.pop().link_edges:
    for v in e.verts:
     if v in remaining:remaining.remove(v);component.add(v);queue.append(v)
  faces=set(f for v in component for f in v.link_faces);island=bmesh.new();mapping={v:island.verts.new(v.co) for v in component}
  for f in faces:island.faces.new([mapping[v] for v in f.verts])
  volume=island.calc_volume(signed=True);island.free();assert volume>1e-12, 'Nonpositive closed component volume';volumes.append(volume)
 result={'weld_tolerance_m':1e-6,'nonmanifold_edges':0,'loose_vertices':0,'degenerate_faces':0,'closed_components':len(volumes),'component_signed_volumes_m3':volumes}
 bm.free();return result
def pbr_signature(material):
 node=material.node_tree.nodes.get('Principled BSDF') if material.use_nodes else None
 assert node is not None, 'Expected solid Principled PBR material'
 return tuple(round(float(v),6) for v in node.inputs['Base Color'].default_value)+(round(float(node.inputs['Roughness'].default_value),6),round(float(node.inputs['Metallic'].default_value),6))
def world_triangle_records(o):
 o.data.calc_loop_triangles();coords=[o.matrix_world@v.co for v in o.data.vertices]
 for t in o.data.loop_triangles:
  xyz=[coords[i].copy() for i in t.vertices];rounded=[tuple(round(float(c),6) for c in v) for v in xyz]
  key=(min(tuple(rounded[i:]+rounded[:i]) for i in range(3)),pbr_signature(o.data.materials[t.material_index]))
  yield key,xyz
def evaluated_triangle_fingerprint(o):
 return hashlib.sha256(json.dumps(sorted(k for k,v in world_triangle_records(o)),separators=(',',':')).encode()).hexdigest()
def global_weld_diagnostic(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 bad=[{'endpoints_m':[list(v.co) for v in e.verts],'linked_faces':len(e.link_faces)} for e in bm.edges if not e.is_manifold];bm.free()
 return {'nonmanifold_edges_after_global_weld':len(bad),'edges':bad,'scope':'Diagnostic only: global positional welding may merge distinct, independently closed components at intended contacts. Per-source-component GLB roundtrip validation remains a hard gate.'}

source_component_owners={};source_component_checks={}
for part in parts:
 source_component_checks[part.name]=verify_joined_closed_mesh(part)
 for key,xyz in world_triangle_records(part):source_component_owners.setdefault(key,[]).append(part.name)
connection_report['source_component_topology']=source_component_checks
closed_components=sum(v['closed_components'] for v in source_component_checks.values())
def aggregate_fingerprint(objects):return hashlib.sha256(json.dumps(sorted(k for o in objects for k,v in world_triangle_records(o)),separators=(',',':')).encode()).hexdigest()
export_fingerprint=aggregate_fingerprint(parts)
world=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
bounds=[round(max(v[k] for v in world)-min(v[k] for v in world),6) for k in range(3)]
triangles=sum(len(o.data.loop_triangles) for o in parts)
pivot.name='DoorLeaf_EditPivot'
EXPORT_GROUPS=[('HingeMounts_Static',fixed,Vector((0,0,0))),('DoorLeaf_Runtime',moving,pivot.location.copy())]

export_nodes=[]
for name,group,origin in EXPORT_GROUPS:
 bpy.ops.object.select_all(action='DESELECT');copies=[]
 for o in group:
  me=o.data.copy()
  for v in me.vertices:v.co=o.matrix_world@v.co-origin
  c=bpy.data.objects.new('Export temporary',me);scene.collection.objects.link(c);c.location=origin;c.select_set(True);copies.append(c)
 bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();node=bpy.context.object;node.name=name;export_nodes.append(node)
bpy.context.view_layer.update();assert aggregate_fingerprint(export_nodes)==export_fingerprint,'Partition/pivot altered world geometry'
bpy.ops.object.select_all(action='DESELECT')
for o in export_nodes:o.select_set(True)
bpy.context.view_layer.objects.active=export_nodes[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
for o in export_nodes:bpy.data.objects.remove(o,do_unlink=True)
# Reimport actual GLB and reconstruct source-part triangle groups, never globally weld distinct parts into one shell.
original_scene=bpy.context.window.scene;roundtrip_scene=bpy.data.scenes.new('Temporary GLB verification')
old_meshes=set(bpy.data.meshes);old_materials=set(bpy.data.materials)
bpy.context.window.scene=roundtrip_scene
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
imported=[o for o in roundtrip_scene.objects if o.type=='MESH'];assert len(imported)==len(EXPORT_GROUPS), 'Expected fixed hardware plus independent leaf nodes'
roundtrip_fingerprint=aggregate_fingerprint(imported);assert roundtrip_fingerprint==export_fingerprint,'GLB oriented world triangles or PBR materials changed during export/import'
owners={k:list(v) for k,v in source_component_owners.items()};component_triangles={name:[] for name in source_component_checks}
for key,xyz in (item for obj in imported for item in world_triangle_records(obj)):
 assert key in owners and owners[key], 'Unmatched exported triangle or material'
 component_triangles[owners[key].pop()].append(xyz)
assert not any(owners.values()), 'Source triangles lost in export'
component_roundtrip={}
for name,triangles_for_part in component_triangles.items():
 vertices=[v for tri in triangles_for_part for v in tri];faces=[tuple(range(i,i+3)) for i in range(0,len(vertices),3)]
 temp_mesh=bpy.data.meshes.new('QA provenance component');temp_mesh.from_pydata(vertices,[],faces);temp_mesh.update()
 temp_object=bpy.data.objects.new('QA provenance object',temp_mesh)
 component_roundtrip[name]=verify_joined_closed_mesh(temp_object)
 bpy.data.objects.remove(temp_object);bpy.data.meshes.remove(temp_mesh)
connection_report['glb_roundtrip']={'world_oriented_triangle_and_pbr_sha256':roundtrip_fingerprint,'source_component_count':len(component_roundtrip),'all_source_triangles_matched':True,'components':component_roundtrip,'per_node_global_weld_diagnostic':{o.name:global_weld_diagnostic(o) for o in imported}}

node_checks=[]
for name,group,origin in EXPORT_GROUPS:
 node=next(o for o in imported if o.name==name)
 assert (node.matrix_world.translation-origin).length<1e-5,('Runtime pivot drift',name)
 assert max(abs(v-1) for v in node.matrix_world.to_scale())<1e-5
 node_checks.append({'node':name,'pivot_world_m':list(origin),'unit_scale':True})
connection_report['runtime_nodes']=node_checks
for o in list(roundtrip_scene.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.context.window.scene=original_scene;bpy.data.scenes.remove(roundtrip_scene)
for mesh in set(bpy.data.meshes)-old_meshes:
 if mesh.users==0:bpy.data.meshes.remove(mesh)
for material in set(bpy.data.materials)-old_materials:
 if material.users==0:bpy.data.materials.remove(material)
# Keep only editable delivered parts, not read-only validation reference walls.
for o in hosts:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'stage':'formal candidate','artPassed':False,'triangles':triangles,'bounds_m':bounds,'closed_components':closed_components,'nonmanifold_components':0,'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':[],'exposed_skin_check':connection_report,'origin':'Host local coordinate system; fixed hardware origin0, moving leaves use actual hinge Z axes','assembly':{'root_semantics':'Frame-mounted fitted leaf assembly. Embedded frozen host triangles used only for fitting gates, excluded from deliverables.'},'render_evidence':'Real Blender Cycles,512px hero and QA','review_status':'awaiting independent review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles,flush=True);sys.exit(0)
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.world.color=(.32,.32,.32);scene.view_settings.view_transform='AgX'
focus=Vector([sum(v[k] for v in world)/len(world) for k in range(3)])
def point(o,xyz):o.location=xyz;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power,size in [('Key',(-6,-8,12),1800,8),('Fill',(8,-2,6),720,6),('Rim',(2,8,10),1200,6)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);l=bpy.context.object;l.name=name;l.data.energy=power;l.data.size=size;point(l,xyz)
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO'
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,min(v.z for v in world)-.015));ground=bpy.context.object;ground.name='Presentation ground only'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in {'thumbnail':(4,-7,3),'qa-front':(0,-5,focus.z),'qa-back':(0,5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(4,-7,3)}.items():
 if name=='qa-wireframe':
  for o in parts:
   overlay=o.copy();overlay.data=o.data.copy();scene.collection.objects.link(overlay);overlay.data.materials.clear();overlay.data.materials.append(wiremat)
   for p in overlay.data.polygons:p.material_index=0
   w=overlay.modifiers.new('Actual mesh edges','WIREFRAME');w.thickness=0.003;w.use_replace=True;w.use_even_offset=False;w.offset=1
 point(cam,xyz);basis=cam.rotation_euler.to_matrix();right=basis@Vector((1,0,0));up=basis@Vector((0,1,0));xx=[v.dot(right) for v in world];yy=[v.dot(up) for v in world]
 cam.location+=right*((min(xx)+max(xx))/2-focus.dot(right))+up*((min(yy)+max(yy))/2-focus.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.22
 scene.cycles.samples=512 if name=='thumbnail' else 128
 scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'village','style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':2,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print('ASSET_COMPLETE',ASSET,triangles,flush=True)
