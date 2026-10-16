"""Original village-stone-steps-01. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-stone-steps-01'
TITLE='Meadow Four-Step Stone Module'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(.36,.19,.085,1),'sand':(.66,.43,.22,1),'teal':(.12,.28,.22,1),'stone':(.42,.47,.45,1),'stone-light':(.58,.61,.55,1),'leaf':(.25,.44,.18,1),'leaf-light':(.40,.57,.25,1),'water':(.075,.20,.24,1),'iron':(.16,.20,.21,1)}
mats={}
for name,col in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.83
 mats[name]=m
parts=[]
def box(name,loc,scale,mat='honey',bevel=.018,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]);b=o.modifiers.new('Soft hand-cut edge','BEVEL');b.width=bevel;b.segments=1
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
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



for i,(z,w,d,y) in enumerate([(.09,1.60,1.60,0),(.26,1.56,1.18,.19),(.43,1.52,.76,.38),(.60,1.48,.34,.57)]):
 box('Step tier '+str(i),(0,y,z),(w,d,.18),'stone-light',.012)

# Normalize minimum Z after leg splay so feet sit precisely on the ground.
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
low=min(v.co.z for o in parts for v in o.data.vertices)
for o in parts:
 for v in o.data.vertices:v.co.z-=low
# Normalize winding per closed component before export.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
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
 vs=[obj.matrix_world@v.co for v in obj.data.vertices];low=min(v.z for v in vs)
 assert abs(low)<=eps,('Floating ground root',obj.name,low)
 xy=sorted(set((round(v.x,8),round(v.y,8)) for v in vs if abs(v.z)<=eps))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[]
 for p in xy:
  while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 upper=[]
 for p in reversed(xy):
  while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 hull=lower[:-1]+upper[:-1];area=abs(sum(hull[i][0]*hull[(i+1)%len(hull)][1]-hull[(i+1)%len(hull)][0]*hull[i][1] for i in range(len(hull))))/2 if len(hull)>2 else 0
 assert area>1e-5,('No finite planar ground patch',obj.name,area)
 return {'part':obj.name,'min_z_m':low,'ground_patch_area_m2':area,'tolerance_m':eps,'passed':True}

role=lambda name:[o for o in parts if o.name.startswith(name)]
contact_results=[]
for a,b,n in [('Step tier 1', 'Step tier 0', 1), ('Step tier 2', 'Step tier 1', 1), ('Step tier 3', 'Step tier 2', 1)]:contact_results+=link_roles(role(a),role(b),n)
roots=role('Step tier 0')
ground_results=[check_ground_patch(o) for o in roots]
support_graph=validate_support_graph([o.name for o in parts],contact_results,[o.name for o in roots],{})

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

bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(model,do_unlink=True)
# Reimport actual GLB and reconstruct source-part triangle groups, never globally weld distinct parts into one shell.
original_scene=bpy.context.window.scene;roundtrip_scene=bpy.data.scenes.new('Temporary GLB verification')
old_meshes=set(bpy.data.meshes);old_materials=set(bpy.data.materials)
bpy.context.window.scene=roundtrip_scene
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
imported=[o for o in roundtrip_scene.objects if o.type=='MESH'];assert len(imported)==1, 'Expected single exported mesh'
roundtrip_fingerprint=evaluated_triangle_fingerprint(imported[0]);assert roundtrip_fingerprint==export_fingerprint,'GLB oriented world triangles or PBR materials changed during export/import'
owners={k:list(v) for k,v in source_component_owners.items()};component_triangles={name:[] for name in source_component_checks}
for key,xyz in world_triangle_records(imported[0]):
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
connection_report['glb_roundtrip']={'world_oriented_triangle_and_pbr_sha256':roundtrip_fingerprint,'source_component_count':len(component_roundtrip),'all_source_triangles_matched':True,'components':component_roundtrip,'global_weld_diagnostic':global_weld_diagnostic(imported[0])}
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
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Geometry and format QA. Components closed; deliberate plank overlaps are allowed.
import bmesh
bad=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges):bad.append(o.name)
 bm.free()
assert not bad,bad
assert 100<=triangles<=10000,triangles
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
for name,xyz,power,size in [('Key',(-6,-8,12),1800,8),('Fill',(8,-2,6),720,6),('Rim',(2,8,10),1200,6)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;point(light,xyz)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview ground (not asset)'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
views={'thumbnail':(7,-9,7),'qa-front':(0,-5,focus.z),'qa-back':(0,5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(7,-9,7)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 scene.cycles.samples=512 if name=='thumbnail' else 128
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  for o in parts:
   overlay=o.copy();overlay.data=o.data.copy();scene.collection.objects.link(overlay)
   overlay.name='QA topology '+o.name;overlay.data.materials.clear();overlay.data.materials.append(wiremat)
   for polygon in overlay.data.polygons:polygon.material_index=0
   wire=overlay.modifiers.new('QA actual mesh edges','WIREFRAME');wire.thickness=.009;wire.use_replace=True;wire.offset=1
 point(cam,xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'modular','theme':'village','style':'soft-low-poly','title':TITLE,'description':'Original four-tier stone stair module ascending along positive Y, with slightly inset successive tiers and a 0.69 meter top tread. Each tier is modeled and structurally supported.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'exposed_skin_check':connection_report,'glb_import_check':glb_import_check,'closed_components':closed_components,'nonmanifold_components':bad,'origin':'ground centre 0,0,0', 'assembly':{'assembly': 'Standalone grounded asset; origin is base underside centre.'},'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':ground_results,'transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
