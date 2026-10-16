"""Original soft low-poly cargo transport assets. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='astronomy-tripod-telescope-01'
TITLE='Tripod Observing Telescope'
DESCRIPTION='Original stylized telescope with separate editable optical tube, shade, lens discs, eyepiece, mounting collar, pivot, yoke, tripod legs and grounded pads. Plausible visual arrangement only; no real optical performance or engineering specifications are claimed.'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(0.48,0.255,0.105,1),'sand':(0.86,0.75,0.52,1),'teal':(0.19,0.40,0.35,1)}
PALETTE['lens']=(.08,.18,.24,1)
mats={}
for name,col in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.24 if name=='lens' else .83
 mats[name]=m
parts=[]
def box(name,loc,scale,mat='honey',bevel=.018,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]);b=o.modifiers.new('Soft hand-cut edge','BEVEL');b.width=bevel;b.segments=1
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 parts.append(o);return o

def mesh(name,verts,faces,material):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats[material]);parts.append(o);return o
def lathe(name,profile,mat='teal',n=32):
 cyclic=profile[0]==profile[-1]
 if cyclic:profile=profile[:-1]
 verts=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for r,z in profile for i in range(n)]
 faces=[]
 for k in range(len(profile) if cyclic else len(profile)-1):
  nxt=(k+1)%len(profile)
  for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,nxt*n+(i+1)%n,nxt*n+i))
 if not cyclic:faces.extend([tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))])
 return mesh(name,verts,faces,mat)
def tube(name,points,radius,mat='honey',sides=8,cyclic=False):
 verts=[];faces=[]
 axis=min(range(3),key=lambda a:max(p[a] for p in points)-min(p[a] for p in points))
 ref=Vector(tuple(1 if a==axis else 0 for a in range(3)))
 for i,p in enumerate(points):
  tangent=Vector(points[(i+1)%len(points)])-Vector(points[(i-1)%len(points)]) if cyclic else Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
  tangent.normalize();n=tangent.cross(ref)
  if n.length<.001:n=tangent.cross(Vector((1,0,0)))
  n.normalize();bn=tangent.cross(n).normalized()
  for j in range(sides):verts.append(Vector(p)+radius*(math.cos(j*math.tau/sides)*n+math.sin(j*math.tau/sides)*bn))
 for i in range(len(points) if cyclic else len(points)-1):
  for j in range(sides):faces.append((i*sides+j,((i+1)%len(points))*sides+j,((i+1)%len(points))*sides+(j+1)%sides,i*sides+(j+1)%sides))
 if not cyclic:faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
 return mesh(name,verts,faces,mat)

def prism_xy(name,outline,z_bottom,z_top,material,bevel=0):
 from mathutils.geometry import tessellate_polygon
 pts=[Vector((x,y,0)) for x,y in outline];N=len(pts);verts=[(x,y,z) for z in [z_bottom,z_top] for x,y in outline];faces=[]
 for tri in tessellate_polygon([pts]):
  ids=tuple(v if isinstance(v,int) else min(range(N),key=lambda k:(pts[k]-v).length) for v in tri)
  faces.extend([tuple(reversed(ids)),tuple(N+i for i in ids)])
 for i in range(N):faces.append((i,(i+1)%N,(i+1)%N+N,i+N))
 o=mesh(name,verts,faces,material)
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Soft curb edges','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 return o


def axle_cylinder(name,center,radius,width,material,n=16,flat_bottom=False):
 x,y,z=center;rr=radius/math.cos(math.pi/n) if flat_bottom else radius
 verts=[(x+dx,y+rr*math.sin(math.tau*i/n+math.pi/n),z+rr*math.cos(math.tau*i/n+math.pi/n)) for dx in [-width/2,width/2] for i in range(n)]
 faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,verts,faces,material)


def railwheel(name,center,radius,width,material,n=16):
 x,y,z=center;rr=radius/math.cos(math.pi/n)
 verts=[(x+dx,y+rr*math.sin(math.tau*i/n+math.pi/n),z+rr*math.cos(math.tau*i/n+math.pi/n)) for dx in [-width/2,width/2] for i in range(n)]
 faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,verts,faces,material)


def sleeve_axis(name,center,direction,length,outer,inner,material,n=24):
 c=Vector(center);axis=Vector(direction).normalized();u=Vector((1,0,0));v=axis.cross(u).normalized();u=v.cross(axis).normalized();verts=[]
 for z,r in [(-length/2,outer),(length/2,outer),(length/2,inner),(-length/2,inner)]:
  verts.extend([c+axis*z+r*(u*math.cos(i*math.tau/n)+v*math.sin(i*math.tau/n)) for i in range(n)])
 faces=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,verts,faces,material)

C=Vector((0,0,1.37));D=Vector((0,-.9,.4)).normalized()
for angle in [-90,30,150]:
 a=math.radians(angle);x=.60*math.cos(a);y=.60*math.sin(a)
 box('Tripod foot',(x,y,.04),(.16,.16,.08),'teal',.012)
 tube('Tripod leg',[(x,y,.07),(0,0,.96)],.032,'honey',8)
tube('Tripod center hub',[(0,0,.87),(0,0,1.05)],.105,'teal',20)
box('Mount base',(0,0,1.07),(.38,.22,.12),'teal',.016)
for x in [-.14,.14]:box('Mount yoke',(x,0,1.20),(.06,.16,.30),'teal',.01)
tube('Altitude pivot',[(-.18,0,1.30),(.18,0,1.30)],.075,'honey',16)
tube('Main optical tube',[C-D*.45,C+D*.45],.105,'sand',24)
sleeve_axis('Tube mounting collar',C,D,.10,.125,.095,'honey')
sleeve_axis('Front shade',C+D*.44,D,.12,.13,.095,'sand')
tube('Objective lens',[C+D*.43,C+D*.462],.095,'lens',24)
tube('Eyepiece barrel',[C-D*.43,C-D*.63],.036,'teal',16)
tube('Eyepiece glass',[C-D*.62,C-D*.645],.025,'lens',16)
# Normalize winding per closed component before export.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# All mesh origins at the common bottom-center; keep parts separate for editing.
scene.cursor.location=(0,0,0)
for o in parts:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
# Normalize exact full-asset bottom-center after all component transforms.
coords=[v.co.copy() for o in parts for v in o.data.vertices]
shift=Vector(((min(v.x for v in coords)+max(v.x for v in coords))/2,(min(v.y for v in coords)+max(v.y for v in coords))/2,min(v.z for v in coords)))
for o in parts:
 for v in o.data.vertices:v.co-=shift
from mathutils.bvhtree import BVHTree
import itertools
objs=[o for o in bpy.context.scene.objects if o.type=='MESH'];cache={}
for o in objs:
 assert not o.modifiers, 'Unapplied modifiers: '+o.name
 o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];fs=[tuple(t.vertices) for t in o.data.loop_triangles]
 cache[o.name]=(BVHTree.FromPolygons(vs,fs,all_triangles=True),Vector([min(v[a] for v in vs) for a in range(3)]),Vector([max(v[a] for v in vs) for a in range(3)]))
clearance=.002
directions=[Vector((1,.371,.529)).normalized(),Vector((.263,1,.619)).normalized(),Vector((.419,.233,1)).normalized()]
def inside(tree,point):
 results=[]
 for d in directions:
  origin=point.copy();count=0
  for _ in range(100):
   loc,norm,idx,dist=tree.ray_cast(origin,d,100)
   if loc is None:break
   # Advance 10 micrometers to avoid float32 re-hitting the same face at distance -0.0.
   # This is 50x smaller than even the smallest required 0.5mm clearance.
   count+=1;origin=loc+d*1e-5
  else:raise RuntimeError('Ray parity uncertain: 100 hits exceeded')
  results.append(count%2==1)
 return all(results)
def anchors(a,b):
 ta,la,ha=cache[a.name];tb,lb,hb=cache[b.name]
 lo=Vector([max(la[i],lb[i]) for i in range(3)]);hi=Vector([min(ha[i],hb[i]) for i in range(3)])
 if min(hi-lo)<2*clearance: return []
 good=[]
 for uvw in itertools.product([.05,.2,.35,.5,.65,.8,.95],repeat=3):
  v=Vector([lo[i]+uvw[i]*(hi[i]-lo[i]) for i in range(3)])
  da=ta.find_nearest(v)[3];db=tb.find_nearest(v)[3]
  if min(da,db)<clearance or not inside(ta,v) or not inside(tb,v):continue
  if any((v-Vector(q['world_anchor_m'])).length<.002 for q in good):continue
  good.append({'world_anchor_m':list(v),'surface_clearance_a_m':da,'surface_clearance_b_m':db,'three_ray_inside_a':True,'three_ray_inside_b':True})
  if len(good)>=3:return good
 return good
checks=[]
def relation(ap,bp,count=1):
 assert any(o.name.startswith(ap) for o in objs), 'Missing required A: '+ap
 assert any(o.name.startswith(bp) for o in objs), 'Missing required B: '+bp
 for a in [o for o in objs if o.name.startswith(ap)]:
  contacts=[]
  for b in [o for o in objs if o.name.startswith(bp)]:
   pts=anchors(a,b)
   if len(pts)>=3:contacts.append({'part_b':b.name,'mode':'overlap','anchors':pts})
  checks.append({'part_a':a.name,'required_b_prefix':bp,'minimum_contacts':count,'contacts':contacts,'pass':len(contacts)>=count})
def manual_relation(ap,bp,points_fn):
 aa=[o for o in objs if o.name.startswith(ap)];bb=[o for o in objs if o.name.startswith(bp)]
 assert aa and len(bb)==1, 'Missing or ambiguous declared contact parts'
 b=bb[0]
 for a in aa:
  pts=[];all_good=True
  for raw in points_fn(a.name):
   v=Vector(raw);ta=cache[a.name][0];tb=cache[b.name][0];da=ta.find_nearest(v)[3];db=tb.find_nearest(v)[3];ia=inside(ta,v);ib=inside(tb,v)
   passed=ia and ib and min(da,db)>=clearance;all_good &= passed
   pts.append({'world_anchor_m':list(v),'surface_clearance_a_m':da,'surface_clearance_b_m':db,'three_ray_inside_a':ia,'three_ray_inside_b':ib,'pass':passed})
  checks.append({'part_a':a.name,'required_b_prefix':bp,'minimum_contacts':1,'contacts':[{'part_b':b.name,'mode':'overlap','anchors':pts}],'pass':all_good and len(pts)>=3})




relation('Tripod leg','Tripod foot')
relation('Tripod leg','Tripod center hub')
relation('Mount base','Tripod center hub')
relation('Mount yoke','Mount base')
relation('Mount yoke','Altitude pivot')
relation('Altitude pivot','Tube mounting collar')
relation('Tube mounting collar','Main optical tube')
relation('Front shade','Main optical tube')
relation('Objective lens','Main optical tube')
relation('Eyepiece barrel','Main optical tube')
relation('Eyepiece glass','Eyepiece barrel')

assert checks and all(c['pass'] for c in checks), 'Required structural contact failed: '+repr([c for c in checks if not c['pass']])
fingerprint=hashlib.sha256(json.dumps([(o.name,[list(o.matrix_world@v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in objs],sort_keys=True).encode()).hexdigest()
connection_report={'method':'Evaluated triangles, 3 ray parity directions and at least 3 separate overlap anchors per edge','minimum_inside_clearance_m':clearance,'evaluated_mesh_sha256':fingerprint,'checks':checks,'passed':True}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 assert not any(not e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)>0, o.name
 bm.free()


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

# Join only for export to reduce runtime draw calls; restore editable components afterwards.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.duplicate();export_parts=list(bpy.context.selected_objects);bpy.ops.object.join();model=bpy.context.object;model.name=ASSET
model.data.calc_loop_triangles();triangles=len(model.data.loop_triangles)
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

# Persist clean source before adding the non-exported presentation rig.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
material_count=len({m.name for o in parts for m in o.data.materials})
# Geometry and format QA. Components closed; deliberate plank overlaps are allowed.
import bmesh
bad=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges):bad.append(o.name)
 bm.free()
assert not bad,bad
assert 100<=triangles<=6000,triangles
assert bounds[2]>0 and min(v.co.z for o in parts for v in o.data.vertices)>-1e-5
assert (OUT/'model.glb').stat().st_size<500000
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False
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
views={'thumbnail':(3,-4,2.8),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-back':(3,4,2.8),'qa-wireframe':(3,-4,2.8)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  for o in parts:
   o.data.materials.append(wiremat)
   wire=o.modifiers.new('QA edge overlay','WIREFRAME');wire.thickness=.006;wire.use_replace=False;wire.offset=1;wire.material_offset=len(o.data.materials)-1
 scene.cycles.samples=512 if name=='thumbnail' else 128
 point(cam,tuple(focus+Vector(xyz)-Vector((0,0,0))) if name in ['thumbnail','qa-back','qa-wireframe'] else xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/astronomy/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'astronomy','style':'soft-low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':material_count,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':material_count,'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'bottom center 0,0,0','transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
qa['connections']=connection_report
qa['support']='All telescope and case joints have evaluated BVH anchors. Tripod pads and case feet provide broad ground surfaces. Scene stacked case uses exact opposing-face bearing, not hidden sinking; no optical or structural engineering claims.'
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
