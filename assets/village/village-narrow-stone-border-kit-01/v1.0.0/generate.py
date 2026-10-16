"""
S03 narrow stone border family: one kit, two selectable nodes.

All dimensions and installation coordinates are Blender Z-up metres. GLB uses
standard glTF Y-up. Scale stays (1,1,1). Each member has its own true local
bottom-centre origin; replace its default display translation when installing.

Border_Straight_2m: 2 x 0.16 x 0.12 m; local X is the long axis. Default display
translation (-0.2,0,0). The +Y upper outside edge has a 20 mm arris. Full end
profiles remain at local X=-1 and X=+1.
Border_Corner_0p16: 0.16 x 0.16 x 0.12 m; default display translation (1.2,0,0).
Its northeast external corner is clipped. The west and south ends fit the
straight section. Rotate this one corner for other orientations. Its compact
outer-corner footprint avoids overlapping two long straight bars.

The separated 2.48 x 0.16 m display envelope is for node selection, not one
installed border. Duplicate only the needed member. Do not scale the whole
kit or place both default display positions as an assembly.

Validated example around two 2 m paving cores (existing separate asset):
- Paving core centres: (0,0,0) and (2.002,0,0), no rotation.
- North straight centres: (0,1.082,0) and (2.002,1.082,0), no rotation.
- Northeast corner centre: (3.084,1.082,0), no rotation.
- East straight centre: (3.084,0,0), Z rotation -90 degrees.
The paving outer edge is Y=1 or X=3.002; border inner edges are Y=1.002 or
X=3.004. Actual end-to-end and paving-side gaps are 2 mm. Boundary top Z0.12
stands 60 mm above the paving top Z0.06. South/west approaches stay open.
Both nodes have real flat ground-bearing faces at Z0. A shifted corner can
intersect the long stone; preserve the validated offsets and orientations.

This is a low visual planting-side boundary. It is not a certified barrier,
accessible route, drainage design or load-bearing engineering component.
The two selectable members count as one asset. Paving cores and multiple
instances are reuse, not included new scenery.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-narrow-stone-border-kit-01'
TITLE='Village Narrow Stone Border Kit'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(.36,.19,.085,1),'sand':(.66,.43,.22,1),'teal':(.12,.28,.22,1),'stone':(.42,.47,.45,1),'stone-light':(.58,.61,.55,1),'leaf':(.25,.44,.18,1),'leaf-light':(.40,.57,.25,1),'water':(.075,.20,.24,1),'iron':(.16,.20,.21,1),'soil':(.16,.095,.045,1),'earth':(.30,.36,.18,1),'frame':(.55,.60,.60,1),'steel':(.24,.30,.32,1),'panel':(.055,.15,.23,1),'cream':(.72,.71,.60,1),'fungus-coral':(.50,.24,.14,1),'fungus-cream':(.73,.64,.43,1)}
mats={}
for name,col in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.83
 mats[name]=m
mats['water'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.23
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



def prism_y(name,section,y0,y1,mat):
 n=len(section);verts=[(x,y,z) for y in [y0,y1] for x,z in section]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats[mat]);parts.append(o);return o
# Two selectable boundary members, one family: no whole-pavement duplication.
PRESETS={'straight':(2.,.16,False),'corner':(.16,.16,False)}
LAYOUT={'straight':(-.2,0,0),'corner':(1.2,0,0)}
NODE_NAMES={'straight':'Border_Straight_2m','corner':'Border_Corner_0p16'}
profile_groups={}
def closed_mesh(name,verts,faces,profile):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats['stone']);parts.append(o);profile_groups[profile]=[o];o.location=Vector(LAYOUT[profile]);return o
section=[(-.08,0),(.08,0),(.08,.10),(.06,.12),(-.08,.12)]
n=len(section);verts=[(x,y,z) for x in [-1,1] for y,z in section]
faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
closed_mesh('Straight boundary stone',verts,faces,'straight')
p=[(-.08,-.08),(.08,-.08),(.08,.055),(.055,.08),(-.08,.08)]
top=[(-.08,-.08),(.06,-.08),(.06,.045),(.045,.06),(-.08,.06)]
verts=[(x,y,z) for z in [0,.10] for x,y in p]+[(x,y,.12) for x,y in top];n=len(p)
faces=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]
for ring in [0,1]:
 for i in range(n):j=(i+1)%n;faces.append((ring*n+i,ring*n+j,(ring+1)*n+j,(ring+1)*n+i))
closed_mesh('Clipped outer corner stone',verts,faces,'corner')
for name in ['stone']:
 mats[name].diffuse_color=(.48,.49,.48,1);mats[name].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.48,.49,.48,1)
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Restrained stone value groups by actual face orientation.
for name,col in [('stone',(.34,.33,.29,1)),('stone-light',(.43,.40,.34,1)),('earth',(.39,.37,.32,1))]:
 mats[name].diffuse_color=col;mats[name].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=col
for o in parts:
 o.data.materials.clear()
 for name in ['stone','stone-light','earth']:o.data.materials.append(mats[name])
 for f in o.data.polygons:f.material_index=1 if f.normal.z>.95 else (2 if f.normal.z>.1 else 0)
"""Strict mesh-anchor joint validator, for embedding in future generators.
Run after modifiers and applied transforms, before export/render.
No check is passed until explicit assembly records are supplied and executed.
"""
import bpy,hashlib,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
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
def validate_bearing_face(child,parent,tolerance=1e-5,min_area=1e-4):
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
  if na.z>=-.1:continue # Child underside must face downward for bearing.
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
 return {'a':child.name,'b':parent.name,'mode':'actual opposite-face gravity-bearing contact','passed':True,'area_m2':area,'minimum_area_m2':min_area,'plane_tolerance_m':tolerance,'child_mesh_sha256':afp,'parent_mesh_sha256':bfp,'patches':patches,'scope':'one-sided solid bearing patches only; not rigid-body stability or load capacity'}


role=lambda name:[o for o in parts if o.name.startswith(name)]
contact_results=[]
roots=parts[:]
ground_results=[check_ground_patch(o) for o in roots]
support_graph=validate_support_graph([o.name for o in parts],contact_results,[o.name for o in roots],{})
support_graph['root_semantics']='Each selectable closed boundary module has its own actual flat bottom on Z0.'

# Conservative same-facing exposed-skin gate; all transforms/modifiers already applied.
objs=parts
cache={}
for o in objs:
 o.data.calc_loop_triangles()
 vv=[o.matrix_world@v.co for v in o.data.vertices]
 tree,fingerprint=evaluated_joint_mesh(o)
 cache[o.name]=(tree,Vector([min(v[k] for v in vv) for k in range(3)]),Vector([max(v[k] for v in vv) for k in range(3)]))
inside=lambda tree,point:all(classify_inside(tree,point,d) for d in _DIRECTIONS)
connection_report={'evaluated_fingerprints':{o.name:evaluated_joint_mesh(o)[1] for o in objs}}
connection_report['gate_template_sha256']='70e82ffb4c4d63d5c4a25dfd3e6773a899a004f4e9e28924b28d96be5343cc4c'
kit_profiles=[]
for profile,group in profile_groups.items():
 offset=Vector(LAYOUT[profile]);local=[o.matrix_world@v.co-offset for o in group for v in o.data.vertices]
 actual=[max(v[k] for v in local)-min(v[k] for v in local) for k in range(3)]
 expected=[PRESETS[profile][0],PRESETS[profile][1],.12]
 assert max(abs(a-b) for a,b in zip(actual,expected))<1e-5
 kit_profiles.append({'profile':profile,'node':NODE_NAMES[profile],'actual_dimensions_m':actual,'local_origin_m':[0,0,0],'origin_semantics':'Bottom-centre mounting plane of this selectable profile','default_display_translation_m':list(offset),'new_asset_count_for_this_profile':0})
actual_ports={}
for profile,group in profile_groups.items():
 offset=Vector(LAYOUT[profile]);v=[o.matrix_world@p.co-offset for o in group for p in o.data.vertices]
 for label,axis,value,other in ([('west',0,-1,1),('east',0,1,1)] if profile=='straight' else [('west',0,-.08,1),('south',1,-.08,0)]):
  actual=sorted({(round(p[other],6),round(p.z,6)) for p in v if abs(p[axis]-value)<1e-6})
  actual_ports[profile+'_'+label]=actual
connection_report['module_interface']={'family':'S03 narrow stone boundary family','counted_asset_count':1,'selectable_profiles':kit_profiles,'actual_end_vertices_y_or_x_z_m':actual_ports,'top_m':.12,'paving_top_m':.06,'scope':'Grounded planting-side boundary; leave road entry open. No navigation or engineered barrier claims.'}
connection_report['bearing_face_contacts']=contact_results

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

# All mesh origins at the common bottom-center; keep parts separate for editing.
scene.cursor.location=(0,0,0)
for o in parts:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
# Join only for export to reduce runtime draw calls; restore editable components afterwards.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.duplicate();export_parts=list(bpy.context.selected_objects);bpy.ops.object.join();model=bpy.context.object;model.name=ASSET
model.data.calc_loop_triangles();triangles=len(model.data.loop_triangles)
joined=bmesh.new();joined.from_mesh(model.data);bmesh.ops.remove_doubles(joined,verts=list(joined.verts),dist=1e-6)
joined_bad=sum(not e.is_manifold for e in joined.edges);joined.free() # Cross-component coincident contacts are diagnostic; provenance gate below validates each source shell.
bounds=[round(v,5) for v in model.dimensions]
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
connection_report['joined_global_weld_diagnostic']=global_weld_diagnostic(model)
export_fingerprint=evaluated_triangle_fingerprint(model)

export_nodes=[]
for profile,group in profile_groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in group:o.select_set(True)
 bpy.context.view_layer.objects.active=group[0];bpy.ops.object.duplicate();bpy.ops.object.join();node=bpy.context.object;node.name=NODE_NAMES[profile]
 offset=Vector(LAYOUT[profile])
 for v in node.data.vertices:v.co-=offset
 node.location=offset;export_nodes.append(node)
bpy.context.view_layer.update()
def aggregate_fingerprint(objects):return hashlib.sha256(json.dumps(sorted(k for o in objects for k,v in world_triangle_records(o)),separators=(',',':')).encode()).hexdigest()
assert aggregate_fingerprint(export_nodes)==export_fingerprint,'Node partition changed source world triangles'
bpy.ops.object.select_all(action='DESELECT')
for node in export_nodes:node.select_set(True)
bpy.context.view_layer.objects.active=export_nodes[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
for node in export_nodes:bpy.data.objects.remove(node,do_unlink=True)
bpy.data.objects.remove(model,do_unlink=True)
# Reimport actual GLB and reconstruct source-part triangle groups, never globally weld distinct parts into one shell.
original_scene=bpy.context.window.scene;roundtrip_scene=bpy.data.scenes.new('Temporary GLB verification')
old_meshes=set(bpy.data.meshes);old_materials=set(bpy.data.materials)
bpy.context.window.scene=roundtrip_scene
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
imported=[o for o in roundtrip_scene.objects if o.type=='MESH'];assert len(imported)==2, 'Expected two selectable paving nodes'
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
for profile,name in NODE_NAMES.items():
 node=next(o for o in imported if o.name==name)
 assert (node.matrix_world.translation-Vector(LAYOUT[profile])).length<1e-5,(name,'pivot drift')
 assert max(abs(v-1) for v in node.matrix_world.to_scale())<1e-5,(name,'scale drift')
 local=[node.matrix_world@v.co-node.matrix_world.translation for v in node.data.vertices]
 dims=[max(v[k] for v in local)-min(v[k] for v in local) for k in range(3)]
 assert max(abs(a-b) for a,b in zip(dims,[PRESETS[profile][0],PRESETS[profile][1],.12]))<1e-5
 node_checks.append({'node':name,'profile':profile,'actual_bottom_centre_pivot_world_m':list(node.matrix_world.translation),'actual_dimensions_m':dims,'unit_scale':True})
connection_report['glb_profile_nodes']=node_checks
for o in list(roundtrip_scene.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.context.window.scene=original_scene;bpy.data.scenes.remove(roundtrip_scene)
for mesh in set(bpy.data.meshes)-old_meshes:
 if mesh.users==0:bpy.data.meshes.remove(mesh)
for material in set(bpy.data.materials)-old_materials:
 if material.users==0:bpy.data.materials.remove(material)


# Actual re-import verifies GLB units, bounds and each original surface vertex.
source_vertices=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
existing=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
imported=[o for o in bpy.data.objects if o not in existing and o.type=='MESH']
assert imported,'GLB import produced no geometry'
import_vertices=[o.matrix_world@v.co for o in imported for v in o.data.vertices]
from mathutils.kdtree import KDTree
kd=KDTree(len(import_vertices))
for i,v in enumerate(import_vertices):kd.insert(v,i)
kd.balance();max_vertex_error=max(kd.find(v)[2] for v in source_vertices)
assert max_vertex_error<1e-5,('GLB geometry mismatch',max_vertex_error)
import_bounds=[max(v[i] for v in import_vertices)-min(v[i] for v in import_vertices) for i in range(3)]
assert max(abs(a-b) for a,b in zip(import_bounds,bounds))<1e-4
import_triangle_count=0
for o in imported:o.data.calc_loop_triangles();import_triangle_count+=len(o.data.loop_triangles)
assert import_triangle_count==triangles
closed_components=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 assert all(e.is_manifold for e in bm.edges),o.name
 assert all(f.calc_area()>1e-10 for f in bm.faces),o.name
 vol=bm.calc_volume(signed=True);assert vol>1e-10,(o.name,vol)
 closed_components.append({'part':o.name,'positive_volume_m3':vol,'closed':True});bm.free()
glb_import_check={'passed':True,'max_vertex_error_m':max_vertex_error,'import_bounds_m':import_bounds,'triangles':import_triangle_count,'all_source_joint_regions_survive':True}
for o in list(bpy.data.objects):
 if o not in existing:bpy.data.objects.remove(o,do_unlink=True)

# Persist clean source before adding the non-exported presentation rig.
# Preserve the same two true selectable origins in editable Blender source.
for profile,group in profile_groups.items():
 root=bpy.data.objects.new(NODE_NAMES[profile],None);scene.collection.objects.link(root);offset=Vector(LAYOUT[profile]);root.location=offset;root['profile']=profile;root['installation_origin']='Bottom centre, Z=0 mounting plane'
 for o in group:
  for v in o.data.vertices:v.co-=offset
  o.parent=root
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Geometry and format QA. Components closed; deliberate plank overlaps are allowed.
import bmesh
bad=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges):bad.append(o.name)
 bm.free()
assert not bad,bad
assert 4<=triangles<=10000,triangles # Simple functional modules need no artificial minimum triangle count.
assert bounds[2]>0 and min(v.co.z for o in parts for v in o.data.vertices)>-1e-5
assert (OUT/'model.glb').stat().st_size<500000
if '--geometry-only' in sys.argv:
 report_dir=OUT.parent/'preflight';report_dir.mkdir(exist_ok=True)
 (report_dir/(ASSET+'.json')).write_text(json.dumps({'asset':ASSET,'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':ground_results,'joined_welded_nonmanifold_edges':joined_bad,'exposed_skin_check':connection_report,'glb_import_check':glb_import_check,'closed_components':closed_components},indent=2)+'\n')
 print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.world.color=(.32,.32,.32)
scene.view_settings.view_transform='AgX'
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(bounds)*1.65
focus=Vector((0,0,bounds[2]*.48))
def point(o,xyz):o.location=xyz;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power,size in [('Key',(-6,-8,12),1800,8),('Fill',(8,-2,6),720,6),('Rim',(2,8,10),1200,6),('Underside fill',(2,-4,-6),500,6)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;point(light,xyz)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview ground (not asset)'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
views={'thumbnail':(7,-9,7),'qa-front':(0,-5,focus.z),'qa-back':(0,5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(7,-9,7),'qa-underside':(6,-7,-5)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 if '--silhouette-only' in sys.argv:continue
 if '--underside-only' in sys.argv and name!='qa-underside':continue
 ground.hide_render=(name=='qa-underside')
 for overlay in scene.objects:
  if overlay.name.startswith('QA topology '):overlay.hide_render=(name!='qa-wireframe')
 if '--diagnostic' in sys.argv and name not in ['thumbnail','qa-top']:continue
 scene.cycles.samples=512 if name=='thumbnail' else 128
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  # True edge curves avoid acute-fan miter spikes from a wireframe modifier.
  for o in parts:
   cu=bpy.data.curves.new('Actual topology curves','CURVE');cu.dimensions='3D';cu.bevel_depth=.0018;cu.bevel_resolution=0;cu.resolution_u=1
   for edge in o.data.edges:
    # The view is above the opaque paving: do not overlay its hidden bottom fan.
    if all(abs((o.matrix_world@o.data.vertices[vi].co).z)<1e-6 for vi in edge.vertices):continue
    sp=cu.splines.new('POLY');sp.points.add(1)
    for i,vi in enumerate(edge.vertices):
     v=o.matrix_world@o.data.vertices[vi].co;sp.points[i].co=(*v,1)
   overlay=bpy.data.objects.new('QA topology '+o.name,cu);scene.collection.objects.link(overlay);cu.materials.append(wiremat)
 point(cam,xyz)
 basis=cam.rotation_euler.to_matrix();right=basis@Vector((1,0,0));up=basis@Vector((0,1,0));world=[o.matrix_world@v.co for o in parts for v in o.data.vertices];xx=[v.dot(right) for v in world];yy=[v.dot(up) for v in world]
 cam.location+=right*((min(xx)+max(xx))/2-focus.dot(right))+up*((min(yy)+max(yy))/2-focus.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.22
 scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
# Review-only scale/concept/silhouette evidence; never exported or saved into clean source.
if '--no-render' not in sys.argv and '--wire-only' not in sys.argv and '--diagnostic' not in sys.argv:
 ground.hide_render=False
 for o in scene.objects:
  if o.name.startswith('QA topology '):o.hide_render=True
 scene.cycles.samples=128
 marker=bpy.data.materials.new('Reference charcoal');marker.diffuse_color=(.14,.14,.14,1)
 preview=[]
 def reference_cube(name,xyz,size):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz);o=bpy.context.object;o.name=name;o.dimensions=size;o.data.materials.append(marker);preview.append(o);return o
 # 1.75 m neutral scale figure, exactly ground to top of head.
 refx=max((o.matrix_world@v.co).x for o in parts for v in o.data.vertices)+.45
 for dx in [-.075,.075]:reference_cube('Scale leg',(refx+dx,.5,.40),(.10,.13,.80))
 reference_cube('Scale torso',(refx,.5,1.12),(.34,.18,.64))
 reference_cube('Scale neck',(refx,.5,1.49),(.10,.10,.12))
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.10,location=(refx,.5,1.65));o=bpy.context.object;o.name='Scale head 1.75m';o.data.materials.append(marker);preview.append(o)
 old_scale=cam.data.ortho_scale;old_focus=focus.copy();focus=Vector((.3,0,.9));cam.data.ortho_scale=max(bounds)*1.8;point(cam,(7,-9,7));scene.render.filepath=str(OUT/'blockout-scale-1p75m.png')
 if '--silhouette-only' not in sys.argv:bpy.ops.render.render(write_still=True)
 focus=old_focus;point(cam,(7,-9,7))
 for o in preview:o.hide_render=True
 cam.data.ortho_scale=old_scale
 saved_slots={o.name:list(o.data.materials) for o in parts}
 black=bpy.data.materials.new('Silhouette black');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);em.inputs['Strength'].default_value=1;black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128;scene.cycles.samples=32
 for name,xyz in [('silhouette-128-3q',(7,-9,7)),('silhouette-128-front',(0,-7,focus.z)),('silhouette-128-side',(7,0,focus.z))]:
  point(cam,xyz)
  basis=cam.rotation_euler.to_matrix();right=basis@Vector((1,0,0));up=basis@Vector((0,1,0));world=[o.matrix_world@v.co for o in parts for v in o.data.vertices];xx=[v.dot(right) for v in world];yy=[v.dot(up) for v in world]
  cam.location+=right*((min(xx)+max(xx))/2-focus.dot(right))+up*((min(yy)+max(yy))/2-focus.dot(up));cam.data.ortho_scale=max(max(xx)-min(xx),max(yy)-min(yy))*1.22
  scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
 for o in parts:
  o.data.materials.clear()
  for material in saved_slots[o.name]:o.data.materials.append(material)

files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'architecture','assetKind':'modular','theme':'village','style':'warm-handcrafted-village','title':TITLE,'description':'S03 narrow planting-side stone boundary family with two selectable bottom-centre nodes: a 2 x 0.16 x 0.12 m straight and a 0.16 m clipped external corner. Unit-scale defaults are a separated selection layout. Full node selection, orientation and actual 2 mm interface installation table are in the opening documentation of generate.py. Boundary rises 60 mm above the matching public paving; keep entrances open. One family, without engineering or accessibility guarantees.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'stage':'formal candidate','artPassed':False,'concept_images':[],'scale_reference_m':1.75,'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'exposed_skin_check':connection_report,'glb_import_check':glb_import_check,'closed_components':closed_components,'nonmanifold_components':bad,'origin':'Each named profile node has its own bottom-centre mounting origin; kit layout is display only', 'assembly':{'assembly': 'One narrow boundary family; straight and clipped corner with actual external-paving use evidence.'},'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':ground_results,'transforms':'Two unit-scale profile nodes with true bottom-centre pivots; separated display translations are intentional','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
qa['wireframe_scope']='Actual visible upper and vertical mesh edges shown as curves; hidden Z0 bottom edges omitted from the above view. Full closed topology is checked separately.'
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
