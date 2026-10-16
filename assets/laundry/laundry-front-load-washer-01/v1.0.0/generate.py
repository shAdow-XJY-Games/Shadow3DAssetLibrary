"""Static editable washer kit. Select the named 'Washer door pivot' EMPTY and its seven child meshes for door edits. Runtime GLB imports may use quaternion rotation: switch the pivot rotation_mode to XYZ before setting rotation_euler.z to 0 or radians(-100). Only these two fixed poses are validated. The hinge axis is (-.285,-.375,0) metres; preserve unit scale and all child transforms. Control face, detergent face and inner drum are independently editable fixed parts, with no operating or sliding promise. The recessed dark disc is opaque stylized material, not glass transmission. Existing flat hanging clothes are reused only on the original clothesline, never claimed to have fitted this drum."""
"""Original static front-loading washing appliance with true drum cavity, dark recessed door disc and bored editable hinge. Two fixed door poses only; no washing, drum rotation, fluid, electrical or safety simulation."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;OUT.mkdir(exist_ok=True)
ASSET='laundry-front-load-washer-01'
DESCRIPTION='Original static front-loading washing appliance with a continuous closed housing, real circular opening, thick inner drum cup and blind rear bottom, three fixed drum lifters, four grounded feet, independent control and detergent faces, and an editable seven-part door on a named vertical hinge pivot. Thick annular door surrounds an opaque recessed dark inspection disc. Actual imported GLB verifies closed 0 and open -100 degree poses, positive-area bored hinge seating, pin clearance, a wrong-placement collision negative and nine rays reaching the real rear bottom. No continuous door sweep, washing, drum rotation, detergent drawer travel, optical transparency, textile loading, plumbing, electrical, load or safety certification.'
QA_FOCUS_Z=.44
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100
s.world.color=(.3,.3,.3);s.view_settings.view_transform='AgX'
def mat(n,v):
 m=bpy.data.materials.new(n);m.diffuse_color=(*([v]*3),1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*([v]*3),1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.78;return m
materials=[mat('Primary gray',.53),mat('Countertop gray',.70),mat('Handle gray',.22)]
parts=[]
def box(n,loc,size,m=0,bevel=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[m]);parts.append(o)
 if bevel:
  mod=o.modifiers.new('Designed edge','BEVEL');mod.width=bevel;mod.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o


KIND='front-loading-washing-machine'
def meshpart(name,vs,fs,m=0):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.data.materials.append(materials[m]);parts.append(o);return o
N=32;CZ=.43
# A closed appliance housing with a genuine circular opening and continuous blind cylindrical cavity.
outer=[];inner=[]
for i in range(N):
 t=math.tau*i/N;dx=math.cos(t);dz=math.sin(t);limx=.325/max(abs(dx),1e-9);limz=((.86-CZ) if dz>=0 else (CZ-.055))/max(abs(dz),1e-9);scale=min(limx,limz)
 outer.append((dx*scale,CZ+dz*scale));inner.append((.225*dx,CZ+.225*dz))
vs=[(x,y,z) for ring,y in [(outer,-.32),(outer,.32),(inner,-.32),(inner,.265)] for x,z in ring];fs=[]
for i in range(N):
 j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j)])
fs.extend([tuple(N+i for i in range(N)),tuple(3*N+i for i in reversed(range(N)))])
meshpart('Continuous washer housing and real circular cavity',vs,fs)
for x in [-.25,.25]:
 for y in [-.25,.25]:box('Washer grounded foot %.2f %.2f'%(x,y),(x,y,.035),(.065,.065,.07),2,.004)
box('Upper overhanging appliance cap',(0,0,.865),(.656,.652,.03),0,.004)
# Thick metallic inner drum cup, embedded in the shell by 2 mm; inner opening and rear bottom remain real.
def cup(name,outer_r,inner_r,yfront,yback,yinner,m):
 vs=[(rr*math.cos(i*math.tau/N),yy,CZ+rr*math.sin(i*math.tau/N)) for rr,yy in [(outer_r,yfront),(outer_r,yback),(inner_r,yfront),(inner_r,yinner)] for i in range(N)];fs=[]
 for i in range(N):
  j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j)])
 fs.extend([tuple(N+i for i in range(N)),tuple(3*N+i for i in reversed(range(N)))]);return meshpart(name,vs,fs,m)
cup('Fixed thick inner drum and blind rear bottom',.227,.213,-.299,.274,.253,1)
# Three broad interior lifters join the actual drum wall, with no rotation or washing claim.
for i in range(3):
 t=math.tau*i/3+.3;c=(.209*math.cos(t),-.012,CZ+.209*math.sin(t));o=box('Fixed drum lifter '+str(i+1),c,(.024,.40,.025),1,.003);o.rotation_euler.y=-t
# Fixed controls, independently editable but not promised to slide or operate.
box('Detergent drawer fixed face',(-.16,-.328,.78),(.22,.026,.082),1,.004)
box('Drawer recessed pull',(-.16,-.343,.77),(.10,.013,.019),2,.003)
box('Unlit control display',(.095,-.327,.79),(.17,.024,.055),2,.003)
bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.027,depth=.034,location=(.248,-.329,.79),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='Static selector dial';o.data.materials.append(materials[1]);parts.append(o)
# A real bored hinge has a fixed pin, horizontal bearing seat and moving knuckle.
pivot=bpy.data.objects.new('Washer door pivot',None);s.collection.objects.link(pivot);pivot.location=(-.285,-.375,0);bpy.context.view_layer.update()
def attach(o):
 bpy.context.view_layer.update();M=o.matrix_world.copy();o.parent=pivot;o.matrix_world=M;return o
def sleeve(name,z):
 n=16;vs=[(-.285+rr*math.cos(i*math.tau/n),-.375+rr*math.sin(i*math.tau/n),zz) for zz,rr in [(z,.018),(z+.034,.018),(z+.034,.010),(z,.010)] for i in range(n)];fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)];return meshpart(name,vs,fs,2)
for i,z in enumerate([.285,.575]):
 box('Fixed door hinge seat '+str(i+1),(-.285,-.34,z-.009),(.058,.12,.018),2,0)
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.008,depth=.052,location=(-.285,-.375,z+.018));o=bpy.context.object;o.name='Fixed door hinge pin '+str(i+1);o.data.materials.append(materials[2]);parts.append(o)
 attach(sleeve('Door bored hinge sleeve '+str(i+1),z));attach(box('Door hinge arm '+str(i+1),(-.231,-.357,z+.017),(.082,.036,.025),2,.002))
# Four annular rings define a closed thick door rim rather than a disc painted to resemble an opening.
vs=[(rr*math.cos(i*math.tau/N),yy,CZ+rr*math.sin(i*math.tau/N)) for yy,rr in [(-.39,.258),(-.328,.258),(-.328,.193),(-.39,.193)] for i in range(N)];fs=[(k*N+i,k*N+(i+1)%N,((k+1)%4)*N+(i+1)%N,((k+1)%4)*N+i) for k in range(4) for i in range(N)];attach(meshpart('Door thick annular rim',vs,fs,0))
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.197,depth=.017,location=(0,-.351,CZ),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='Door recessed dark inspection disc';o.data.materials.append(materials[2]);parts.append(o);attach(o)
attach(box('Door side pull grip',(.24,-.405,CZ),(.038,.047,.13),2,.007))
bpy.context.view_layer.update()
# Bake authored mesh rotations before export; preserve world geometry and the explicit parent pivot.
for ob in parts:
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.context.view_layer.update()

# Restrained appliance materials; the recessed viewing disc is deliberately opaque.
def pbr(n,c,rough=.62,metal=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
shellmat=pbr('Warm neutral appliance enamel',(.62,.65,.62),.48)
steelmat=pbr('Satin inner drum steel',(.31,.35,.37),.36,.55)
darkmat=pbr('Graphite grips feet and unlit face',(.055,.065,.070),.60)
rimmat=pbr('Muted blue grey door rim',(.18,.26,.28),.43,.15)
for ob in parts:
 name=ob.name
 target=steelmat if name.startswith(('Fixed thick inner drum','Fixed drum lifter','Fixed door hinge pin','Static selector')) else darkmat if name.startswith(('Washer grounded foot','Drawer recessed','Unlit control','Door recessed','Door side pull','Door bored hinge','Door hinge arm','Fixed door hinge seat')) else rimmat if name=='Door thick annular rim' else shellmat
 ob.data.materials.clear();ob.data.materials.append(target)
import bmesh,hashlib
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

def validate_candidate_roundtrip(parts,pivot,path):
 from collections import Counter
 import struct
 owners={};source_checks={}
 for o in parts:
  source_checks[o.name]=verify_joined_closed_mesh(o)
  for key,xyz in world_triangle_records(o):owners.setdefault(key,[]).append(o.name)
 source_hash=hashlib.sha256(json.dumps(sorted(k for k,rows in owners.items() for _ in rows),separators=(',',':')).encode()).hexdigest()
 raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+size]);nodes=gltf['nodes'];pn=next(n for n in nodes if n.get('name')==pivot.name) if pivot is not None else {}
 expected={o.name for o in parts if o.parent==pivot} if pivot is not None else set();actual={nodes[i]['name'] for i in pn.get('children',[])};assert expected<=actual,('Lost hinge child nodes',expected,actual)
 original=bpy.context.window.scene;test=bpy.data.scenes.new('Candidate actual GLB import');bpy.context.window.scene=test;bpy.ops.import_scene.gltf(filepath=str(path));imported=[o for o in test.objects if o.type=='MESH'];triangles={n:[] for n in source_checks}
 for o in imported:
  for key,xyz in world_triangle_records(o):
   assert key in owners and owners[key],('GLB world oriented triangle/PBR mismatch',o.name,key)
   triangles[owners[key].pop()].append(xyz)
 assert not any(owners.values()),'GLB lost source triangles'
 checks={}
 for n,tris in triangles.items():
  vs=[v for t in tris for v in t];fs=[(i,i+1,i+2) for i in range(0,len(vs),3)];me=bpy.data.meshes.new('Provenance temp');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Provenance temp',me);print('CHECK_PROVENANCE',n,flush=True);checks[n]=verify_joined_closed_mesh(o);bpy.data.objects.remove(o);bpy.data.meshes.remove(me)
 for o in list(test.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.window.scene=original;bpy.data.scenes.remove(test)
 return {'source_component_count':len(parts),'imported_mesh_node_count':len(imported),'world_oriented_triangle_and_pbr_sha256':source_hash,'per_source_roundtrip':checks,'hinge_node':pivot.name if pivot is not None else None,'hinge_children':sorted(actual),'pivot_gltf_translation':pn.get('translation'),'all_source_triangles_matched':True}

def candidate_geometry_gate(parts,moving_pivot,angle_degrees,out):
 import bmesh,hashlib,json
 from mathutils.bvhtree import BVHTree
 report={'stage':'blockout','artPassed':False,'formal_approved':False,'topology':{},'door_motion':{'method':'Actual world-space evaluated triangle intersections at declared sample increments; bidirectional containment parity checked','continuous_clearance_certified':False,'required_final_gate':'No continuous-motion claim by default; finite tested poses only. Physical hinge/independent imported node evidence pending.','samples':[]}}
 for o in parts:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data)
  bad=sum(not e.is_manifold for e in bm.edges);loose=sum(not v.link_faces for v in bm.verts);vol=bm.calc_volume(signed=True)
  report['topology'][o.name]={'nonmanifold_edges':bad,'loose_vertices':loose,'signed_volume_m3':vol};bm.free()
  assert bad==0 and loose==0 and vol>1e-10,('Topology',o.name,bad,loose,vol)
 def tree(o):
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];tris=[tuple(t.vertices) for t in o.data.loop_triangles];return BVHTree.FromPolygons(vs,tris,all_triangles=True),vs
 def inside(t,p):
  votes=[]
  for raw in [(.811,.337,.479),(.257,.887,.383),(.419,.293,.861)]:
   direction=Vector(raw).normalized();pos=p.copy();hits=0
   for _ in range(256):
    hit,normal,index,distance=t.ray_cast(pos,direction,100)
    if hit is None:break
    hits+=1;pos=hit+direction*1e-5
   votes.append(hits%2==1)
  return sum(votes)>=2
 def in_bounds(p,vertices):return all(min(v[k] for v in vertices)-1e-7<=p[k]<=max(v[k] for v in vertices)+1e-7 for k in range(3))
 bpy.context.view_layer.update();moving=[o for o in parts if moving_pivot is not None and o.parent==moving_pivot];static=[o for o in parts if o not in moving];cache={o.name:tree(o) for o in static}
 if moving_pivot is not None:assert moving_pivot.parent is None and abs(moving_pivot.rotation_euler.x)<1e-9 and abs(moving_pivot.rotation_euler.y)<1e-9 and all(abs(v-1)<1e-9 for v in moving_pivot.scale), 'Expected unparented unscaled world-Z hinge'
 if moving_pivot is not None:report['door_motion']['assumptions']={'axis':'world Z','pivot_unparented':True,'pivot_scale':[float(v) for v in moving_pivot.scale],'floating_distance_margin_m':2e-6,'precision':'Blender float geometry; numerical certificate with stated margin, not symbolic exact arithmetic'}
 step=20 if '--fixture-between' in __import__('sys').argv else 1
 angles=sorted(set(list(range(0,abs(angle_degrees)+1,step))+[abs(angle_degrees)])) if moving_pivot is not None else []
 # Real assembly paths: sampled interior overlap or opposed shared surface patches.
 acache={o.name:tree(o) for o in parts};edges=[];adj={o.name:set() for o in parts}
 def add_edge(a,b,mode,anchors):
  edges.append({'a':a.name,'b':b.name,'mode':mode,'anchors':anchors,'minimum_inside_clearance_m':.0002 if mode=='interior-overlap' else None});adj[a.name].add(b.name);adj[b.name].add(a.name)
 def world_triangles(o):
  o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices]
  return [tuple(vv[i] for i in t.vertices) for t in o.data.loop_triangles]
 for ai,a in enumerate(parts):
  ta,va=acache[a.name]
  for b in parts[ai+1:]:
   tb,vb=acache[b.name];lo=Vector(tuple(max(min(v[k] for v in va),min(v[k] for v in vb)) for k in range(3)));hi=Vector(tuple(min(max(v[k] for v in va),max(v[k] for v in vb)) for k in range(3)))
   if any(hi[k]<lo[k]-1e-5 for k in range(3)):continue
   anchors=[]
   if all(hi[k]-lo[k]>=.0008 for k in range(3)):
    for u in [.25,.5,.75]:
     for v in [.25,.5,.75]:
      for w in [.25,.5,.75]:
       pt=Vector(tuple(lo[k]+(hi[k]-lo[k])*f for k,f in enumerate([u,v,w])));da=ta.find_nearest(pt)[3];db=tb.find_nearest(pt)[3]
       if min(da,db)>=.0002 and inside(ta,pt) and inside(tb,pt):anchors.append({'world_m':list(pt),'clearance_a_m':da,'clearance_b_m':db})
   # Thin oblique interfaces may miss axis-aligned box-grid points.
   initial_anchor_count=len(anchors)
   def anchor_span(records):
    if len(records)<3:return 0.0
    p0=Vector(records[0]['world_m']);v=max((Vector(q['world_m'])-p0 for q in records),key=lambda x:x.length)
    return max(v.cross(Vector(q['world_m'])-p0).length for q in records)
   initial_span=anchor_span(anchors)
   if initial_anchor_count<3 or initial_span<=1e-10:
    for src,other in [(a,tb),(b,ta)]:
     for tri in world_triangles(src):
      normal=(tri[1]-tri[0]).cross(tri[2]-tri[0]).normalized()
      for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6),(.8,.1,.1),(.1,.8,.1),(.1,.1,.8)]:
       pt=sum((v*w for v,w in zip(tri,weights)),Vector())-normal*.0005
       if not all(lo[k]<=pt[k]<=hi[k] for k in range(3)):continue
       da=ta.find_nearest(pt)[3];db=tb.find_nearest(pt)[3]
       if min(da,db)>=.0002 and inside(ta,pt) and inside(tb,pt):anchors.append({'world_m':list(pt),'clearance_a_m':da,'clearance_b_m':db})
   if initial_anchor_count>=3 and initial_span<=1e-10:report.setdefault('collinear_probe_recovery',[]).append({'parts':[a.name,b.name],'initial_count':initial_anchor_count,'initial_cross_span_m2':initial_span,'expanded_count':len(anchors),'expanded_cross_span_m2':anchor_span(anchors),'actual_triangle_inset_m':.0005,'clearance_m':.0002})
   if len(anchors)>=3:
    first=anchors[0];p0=Vector(first['world_m']);second=max(anchors,key=lambda q:(Vector(q['world_m'])-p0).length);v1=Vector(second['world_m'])-p0;third=max(anchors,key=lambda q:v1.cross(Vector(q['world_m'])-p0).length)
    if v1.cross(Vector(third['world_m'])-p0).length>1e-10:add_edge(a,b,'interior-overlap',[first,second,third]);continue
   contacts=[]
   for src,dest in [(a,tb),(b,ta)]:
    for tri in world_triangles(src):
     na=(tri[1]-tri[0]).cross(tri[2]-tri[0]).normalized()
     for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
      pt=sum((v*w for v,w in zip(tri,weights)),Vector());hit,nb,idx,d=dest.find_nearest(pt)
      if d is not None and d<1e-5 and na.dot(nb)<-.95:contacts.append({'world_m':list(pt),'distance_m':d,'normal_dot':na.dot(nb),'sampled_surface':src.name})
   if len(contacts)>=3:
    pts=[Vector(c['world_m']) for c in contacts];noncollinear=any((pts[i]-pts[0]).cross(pts[j]-pts[0]).length>1e-8 for i in range(1,len(pts)) for j in range(i+1,len(pts)))
    if noncollinear:add_edge(a,b,'opposed-surface-contact',contacts[:12])
 for o in parts:
  target='Continuous front frame' if o.name in ['Left door','Right door'] else ('Cargo side' if o.name=='Rear cargo door' else None)
  if target:
   b=next(p for p in parts if p.name==target);pivot=o.parent
   assert pivot is not None and pivot.type=='EMPTY',('Missing editable hinge parent',o.name)
   assert pivot.parent is None and all(abs(v-1)<1e-8 for v in pivot.scale),('Hinge scale/parent',pivot.name)
   axis=(pivot.matrix_world.to_3x3()@Vector((0,0,1))).normalized();assert axis.dot(Vector((0,0,1)))>1-1e-7
   origin=pivot.matrix_world.translation.copy();to,vo=acache[o.name];tf,vf=acache[b.name]
   low=min(v.z for v in vo);high=max(v.z for v in vo)
   side_offset=min(abs(origin.x-min(v.x for v in vo)),abs(origin.x-max(v.x for v in vo)))
   leaf_limit=.025 if o.name=='Rear cargo door' else .006
   frame_limit=.065 if o.name=='Rear cargo door' else .015
   assert side_offset<=leaf_limit,('Hinge axis not at leaf side',o.name,side_offset)
   stations=[]
   for fraction in [.2,.8]:
    point=Vector((origin.x,origin.y,low+(high-low)*fraction));lh,ln,li,ld=to.find_nearest(point);fh,fn,fi,fd=tf.find_nearest(point)
    assert min(v.z for v in vf)<=point.z<=max(v.z for v in vf),('Hinge lacks frame height coverage',o.name)
    assert ld<=leaf_limit and fd<=frame_limit,('Hinge support distance',o.name,ld,fd)
    stations.append({'axis_point_world_m':list(point),'leaf_surface_world_m':list(lh),'frame_surface_world_m':list(fh),'leaf_distance_m':ld,'frame_distance_m':fd,'leaf_limit_m':leaf_limit,'frame_limit_m':frame_limit})
   add_edge(o,b,'geometrically-checked-editable-hinge-constraint',stations)
   edges[-1].update({'pivot_node':pivot.name,'world_axis':list(axis),'axis_side_offset_m':side_offset,'scope':'finite poses tested' if pivot==moving_pivot else 'fixed display pose only; no motion claim'})
 ground=[]
 for o in parts:
  area=sum((t[1]-t[0]).cross(t[2]-t[0]).length/2 for t in world_triangles(o) if max(abs(p.z) for p in t)<1e-6 and (t[1]-t[0]).cross(t[2]-t[0]).z<0)
  if area>1e-6:ground.append({'name':o.name,'actual_ground_face_area_m2':area})
 assert ground,'No real ground patches'
 seen={x['name'] for x in ground};stack=list(seen)
 while stack:
  for name in adj[stack.pop()]-seen:seen.add(name);stack.append(name)
 required=set(adj)-{n for n in adj if 'negative fixture' in n}
 report['assembly']={'edges':edges,'ground':ground,'unconnected':sorted(required-seen),'minimum_overlap_anchor_clearance_m':.0002,'scope':'Static support/attachment paths plus explicitly declared editable hinge constraints. Not a load/physics simulation.'}
 if required-seen:(out/'assembly-failure.json').write_text(json.dumps(report['assembly'],indent=2))
 assert required<=seen,('Unconnected actual geometry',sorted(required-seen))

 for degree in angles:
  moving_pivot.rotation_euler.z=math.radians(degree*(1 if angle_degrees>=0 else -1));bpy.context.view_layer.update();collisions=[]
  for a in moving:
   ta,va=tree(a)
   for b in static:
    tb,vb=cache[b.name]
    if ta.overlap(tb):collisions.append([a.name,b.name,'triangle-intersection'])
    elif any(in_bounds(p,vb) and inside(tb,p) and tb.find_nearest(p)[3]>1e-6 for p in va):collisions.append([a.name,b.name,'moving-vertex-inside'])
    elif any(in_bounds(p,va) and inside(ta,p) and ta.find_nearest(p)[3]>1e-6 for p in vb):collisions.append([a.name,b.name,'static-vertex-inside-moving'])
  report['door_motion']['samples'].append({'angle_degrees':degree*(1 if angle_degrees>=0 else -1),'collisions':collisions})
  if collisions:
   (out/'technical-stage.json').write_text(json.dumps(report,indent=2));raise AssertionError(('Door sampled collision',degree,collisions))
 if moving_pivot is not None and '--continuous-experiment' in __import__('sys').argv:
  # Continuous certificate: exact triangle distance at interval midpoint minus a rigid-rotation Lipschitz bound.
  from mathutils.geometry import closest_point_on_tri
  def tri_data(o):
   o.data.calc_loop_triangles();v=[o.matrix_world@q.co for q in o.data.vertices]
   return [tuple(v[i] for i in t.vertices) for t in o.data.loop_triangles]
  static_tris=[t for o in static for t in tri_data(o)]
  def bounds(t):return tuple(min(v[k] for v in t) for k in range(3)),tuple(max(v[k] for v in t) for k in range(3))
  static_boxes=[bounds(t) for t in static_tris]
  def boxdist2(a,b):return sum(max(a[0][k]-b[1][k],b[0][k]-a[1][k],0)**2 for k in range(3))
  def segdist2(p1,q1,p2,q2):
   d1=q1-p1;d2=q2-p2;r=p1-p2;a=d1.dot(d1);e=d2.dot(d2);f=d2.dot(r)
   if a<=1e-24 and e<=1e-24:return r.length_squared
   if a<=1e-24:ss=0;tt=max(0,min(1,f/e))
   else:
    c=d1.dot(r)
    if e<=1e-24:tt=0;ss=max(0,min(1,-c/a))
    else:
     b=d1.dot(d2);den=a*e-b*b;ss=max(0,min(1,(b*f-c*e)/den)) if den>1e-24 else 0;tt=(b*ss+f)/e
     if tt<0:tt=0;ss=max(0,min(1,-c/a))
     elif tt>1:tt=1;ss=max(0,min(1,(b-c)/a))
   return ((p1+d1*ss)-(p2+d2*tt)).length_squared
  def tridist2(a,b):
   best=min([(v-closest_point_on_tri(v,*b)).length_squared for v in a]+[(v-closest_point_on_tri(v,*a)).length_squared for v in b])
   for i in range(3):
    for j in range(3):best=min(best,segdist2(a[i],a[(i+1)%3],b[j],b[(j+1)%3]))
   return best
  pivot_world=moving_pivot.matrix_world.translation.copy();moving_pivot.rotation_euler.z=0;bpy.context.view_layer.update()
  rmax=max(((o.matrix_world@v.co)-pivot_world).xy.length for o in moving for v in o.data.vertices)
  samples={};cert=[]
  def min_distance(deg):
   if deg in samples:return samples[deg]
   moving_pivot.rotation_euler.z=math.radians(deg);bpy.context.view_layer.update();best=1e30
   for a in moving:
    ta,va=tree(a)
    for b in static:
     tb,vb=cache[b.name]
     if ta.overlap(tb):samples[deg]=0.0;return 0.0
     best=min(best,min(tb.find_nearest(v)[3]**2 for v in va),min(ta.find_nearest(v)[3]**2 for v in vb))
    for t in tri_data(a):
     bt=bounds(t)
     for u,bu in zip(static_tris,static_boxes):
      if boxdist2(bt,bu)<best:best=min(best,tridist2(t,u))
   samples[deg]=math.sqrt(best);return samples[deg]
  def certify(lo,hi,depth=0):
   mid=(lo+hi)/2;d=min_distance(mid);bound=2*rmax*math.sin(math.radians(abs(hi-lo))/4)
   if d>bound+2e-6:cert.append({'lo_degrees':lo,'hi_degrees':hi,'midpoint_triangle_distance_m':d,'maximum_point_motion_m':bound,'certified_separation_lower_bound_m':d-bound});return
   assert depth<18 and d>2e-6,('Uncertified swept clearance',lo,hi,d,bound)
   certify(lo,mid,depth+1);certify(mid,hi,depth+1)
  try:certify(min(0,angle_degrees),max(0,angle_degrees))
  except AssertionError:
   report['door_motion']['continuous_clearance_certified']=False;report['door_motion']['failed_continuous_intervals']=cert;(out/'technical-stage.json').write_text(json.dumps(report,indent=2));raise
  report['door_motion']['continuous_clearance_certified']=True
  report['door_motion']['continuous_method']='Numerically evaluated vertex-triangle and edge-edge triangle distance at adaptive interval midpoints; bound 2*rmax*sin(interval_angle/4); all static meshes fixed, moving assembly rigid about declared Z pivot.'
  report['door_motion']['maximum_rotation_radius_m']=rmax;report['door_motion']['certified_intervals']=cert;report['door_motion']['distance_samples']=len(samples)
  report['door_motion']['required_final_gate']='Physical hinge support/constraint, independent imported GLB pivot and source provenance remain pending.'
 
 if moving_pivot is not None:moving_pivot.rotation_euler.z=0;bpy.context.view_layer.update();report['door_motion']['sampled_pass']=True
 else:report.pop('door_motion');report['static_scope']='Independent editable parts in fixed display pose; no sliding or movement claim.'
 objs=parts;skin_cache={}
 for obj in objs:
  obj.data.calc_loop_triangles();bt,vv=tree(obj);skin_cache[obj.name]=(bt,Vector(tuple(min(v[k] for v in vv) for k in range(3))),Vector(tuple(max(v[k] for v in vv) for k in range(3))))
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
   if any(skin_cache[a.name][2][k]<skin_cache[b.name][1][k]-1e-4 or skin_cache[b.name][2][k]<skin_cache[a.name][1][k]-1e-4 for k in range(3)):continue
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
      tree=skin_cache[occluder.name][0]
      probes=[q+na*.0002 for q in visibility_samples]
      if all(inside(tree,q) and tree.find_nearest(q)[3]>=.0001 for q in probes):hidden=True;break
     if hidden:continue
     exposed_skin_conflicts.append({'part_a':a.name,'part_b':b.name,'face_a':face_a,'face_b':face_b,'material_a':a.data.materials[mat_a].name,'material_b':b.data.materials[mat_b].name,'plane_separation_m':max(abs((v-aa[0]).dot(na)) for v in bb),'normal_dot':na.dot(nb),'area_m2':area,'surface_point_m':list(c),'intersection_vertices_m':[list(v) for v in world_vertices]});found=True;break
 if exposed_skin_conflicts:(out/'skin-conflicts.json').write_text(json.dumps(exposed_skin_conflicts,indent=2))
 assert not exposed_skin_conflicts, 'Exposed coplanar skins: '+repr(exposed_skin_conflicts)
 report['exposed_coplanar_skin_conflicts']=exposed_skin_conflicts
 report['coplanar_skin_test']='Co-oriented triangle plane tolerance 0.1 mm; 2D triangle clipping; area > 0.1 square mm; sample centroid, vertices and edge midpoints at 0.2 mm outward offset; all probes must be inside the same third solid with >=0.1 mm clearance. Only same-facing skins tested, not opposite-facing coincident interfaces.'
 

 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 if moving_pivot is not None:moving_pivot.select_set(True)
 if 'pivot' in globals():globals()['pivot'].select_set(True)
 bpy.ops.export_scene.gltf(filepath=str(out/'technical-model.glb'),export_format='GLB',use_selection=True,export_apply=True)
 report['glb_roundtrip']=validate_candidate_roundtrip(parts,moving_pivot,out/'technical-model.glb')
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'technical-source.blend'))
 (out/'technical-stage.json').write_text(json.dumps(report,indent=2));print('BLOCKOUT_TECHNICAL_STAGE_COMPLETE')
import sys
candidate_geometry_gate(parts,None,0,OUT)
if '--geometry-only' in sys.argv:raise SystemExit(0)
focus=Vector((0,0,.44));scale=1.4
for name,loc,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-1,3),350,3),('Rear fill',(-3,4,5),300,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
def render(name,loc,size=scale,res=512):
 if '--no-render' in sys.argv:return
 if '--wire-only' in sys.argv and name!='qa-wireframe':return
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 center=sum(points,Vector())/len(points)
 cam.location=Vector(loc);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 axes={'qa-front':(0,-4,0),'qa-side':(4,0,0),'qa-back':(0,4,0),'qa-top':(0,0,4)}
 if name in axes:
  cam.location=center+Vector(axes[name]);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
  if name=='qa-top':cam.rotation_euler=(0,0,0)
 q=cam.rotation_euler.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0))
 xs=[p.dot(right) for p in points];ys=[p.dot(up) for p in points]
 shift=right*((min(xs)+max(xs))/2-cam.location.dot(right))+up*((min(ys)+max(ys))/2-cam.location.dot(up));cam.location+=shift
 cam.data.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.28
 s.render.resolution_x=res;s.render.resolution_y=res;s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)

def verify_actual_washer_interface():
 import bpy,json,hashlib,math,sys
 from pathlib import Path
 from mathutils import Vector,Matrix
 from mathutils.bvhtree import BVHTree
 s=bpy.data.scenes.new('Actual washer finite-pose validation');source_scene=bpy.context.window.scene;bpy.context.window.scene=s
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 p=OUT/'model.glb';bpy.ops.import_scene.gltf(filepath=str(p));parts=[o for o in s.objects if o.type=='MESH'];pivot=next(ob for ob in s.objects if ob.type=='EMPTY' and ob.name.startswith('Washer door pivot'));moving=[o for o in parts if o.parent==pivot];fixed=[o for o in parts if o not in moving];assert len(moving)==7
 original={o.name:o.matrix_world.copy() for o in moving};axis=Vector((-.285,-.375,0))
 original_mode=pivot.rotation_mode;pivot.rotation_mode='XYZ';bpy.context.view_layer.update();before={o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts};pivot_records=[]
 for deg in [0,-100]:
  pivot.rotation_euler.z=math.radians(deg);bpy.context.view_layer.update();M=Matrix.Translation(axis)@Matrix.Rotation(math.radians(deg),4,'Z')@Matrix.Translation(-axis);err=0;zerr=0;fixederr=0
  for ob in moving:
   for v,old in zip(ob.data.vertices,before[ob.name]):
    actual=ob.matrix_world@v.co;err=max(err,(actual-M@old).length);zerr=max(zerr,abs(actual.z-old.z))
  for ob in fixed:
   fixederr=max(fixederr,max((ob.matrix_world@v.co-old).length for v,old in zip(ob.data.vertices,before[ob.name])))
  assert err<1e-6 and zerr<1e-6 and fixederr<1e-7,(err,zerr,fixederr)
  pivot_records.append({'degrees':deg,'max_world_vertex_rotation_error_m':err,'max_z_change_m':zerr,'fixed_max_change_m':fixederr})
 pivot.rotation_euler.z=0;bpy.context.view_layer.update()
 
 cache={}
 def data(o):
  if o.name not in cache:
   o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];tt=[tuple(t.vertices) for t in o.data.loop_triangles];cache[o.name]=(BVHTree.FromPolygons(vs,tt,all_triangles=True),vs,tt)
  return cache[o.name]
 def verts(role):return [v for o in roles[role] for v in data(o)[1]]
 def inside(tree,p):
  votes=[]
  for raw in [(.811,.337,.479),(.257,.887,.383),(.419,.293,.861)]:
   d=Vector(raw).normalized();q=p.copy();count=0
   for _ in range(256):
    h,n,i,dist=tree.ray_cast(q,d)
    if h is None:break
    count+=1;q=h+d*1e-6
   votes.append(count%2)
  return sum(votes)>=2
 
 def clash(a,b,contact_z=None):
  ta,va,fa=data(a);tb,vb,fb=data(b)
  if any(min(max(v[k] for v in va),max(v[k] for v in vb))<max(min(v[k] for v in va),min(v[k] for v in vb))-2e-6 for k in range(3)):return []
  failures=[]
  for ia,ib in ta.overlap(tb):
   at=[va[q] for q in fa[ia]];bt=[vb[q] for q in fb[ib]]
   if contact_z is not None and min(v.z for v in at)>=contact_z-2e-6 and max(v.z for v in bt)<=contact_z+2e-6:continue
   failures.append(['triangles',ia,ib])
  for role,vv,t in [('a-inside-b',va,tb),('b-inside-a',vb,ta)]:
   for v in vv:
    if t.find_nearest(v)[3]>2e-6 and inside(t,v):failures.append([role,list(v)]);break
  return failures
 def clip(subject,edge):
  def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  sign=1 if cross(*edge)>0 else -1
  for a,b in zip(edge,edge[1:]+edge[:1]):
   old=subject;subject=[]
   if not old:break
   for p,q in zip(old,old[1:]+old[:1]):
    dp=sign*cross(a,b,p);dq=sign*cross(a,b,q)
    if dp>=-1e-12:subject.append(p)
    if (dp>=0)!=(dq>=0):
     t=dp/(dp-dq);subject.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return subject
 def area(poly):return abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))/2 if len(poly)>2 else 0
 
 def door(deg):
  trans=Matrix.Translation(axis)@Matrix.Rotation(math.radians(-deg),4,'Z')@Matrix.Translation(-axis)
  for o in moving:o.matrix_world=trans@original[o.name]
  bpy.context.view_layer.update();cache.clear()
 def planar_contact(a,b,z,sign=-1):
  surfaces=[]
  for ob,normal in [(a,sign),(b,-sign)]:
   vv,ff=data(ob)[1:];surfaces.append([[tuple(vv[i][:2]) for i in f] for f in ff if all(abs(vv[i].z-z)<1e-6 for i in f) and (vv[f[1]]-vv[f[0]]).cross(vv[f[2]]-vv[f[0]]).z*normal>1e-10])
  total=sum(area(t) for t in surfaces[0]);covered=sum(area(clip(t[:],u)) for t in surfaces[0] for u in surfaces[1]);assert total>0 and abs(total-covered)<1e-7,(a.name,b.name,total,covered)
  return {'a':a.name,'b':b.name,'z':z,'sourceArea':total,'coveredArea':covered}
 report={'source_glb_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fixed_door_poses':[],'bearing_seats':[],'scope':'Two fixed door poses only. No continuous sweep, load, washing, drum rotation, or textile loading guarantee.'}
 for deg in [0,100]:
  door(deg);bad=[]
  for a in moving:
   for b in fixed:
    contact=.285 if a.name.startswith('Door bored hinge sleeve 1') and b.name.startswith('Fixed door hinge seat 1') else (.575 if a.name.startswith('Door bored hinge sleeve 2') and b.name.startswith('Fixed door hinge seat 2') else None)
    hits=clash(a,b,contact)
    if hits:bad.append([a.name,b.name,hits[:2]])
  assert not bad,(deg,bad)
  report['fixed_door_poses'].append({'rotation_degrees':-deg,'noncontact_collisions':bad})
  for i,z in enumerate([.285,.575],1):
   c=planar_contact(next(o for o in moving if o.name.startswith('Door bored hinge sleeve '+str(i))),next(o for o in fixed if o.name.startswith('Fixed door hinge seat '+str(i))),z);c['rotation_degrees']=-deg;report['bearing_seats'].append(c)
 # The original door rigidly shifted backward is a real failing fixture.
 door(0)
 for o in moving:o.matrix_world=Matrix.Translation((0,.06,0))@o.matrix_world
 bpy.context.view_layer.update();cache.clear();bad=[(a.name,b.name) for a in moving for b in fixed if clash(a,b)];assert bad;report['door_backward_60mm_negative']={'rejected':True,'collisions':bad}
 door(100)
 # Nine front-to-back probes enter the actual mouth, reach the drum rear bottom, and do not hit a front face.
 probes=[]
 allverts=[];allfaces=[]
 for o in fixed:
  vv,ff=data(o)[1:];n=len(allverts);allverts+=vv;allfaces += [tuple(n+i for i in f) for f in ff]
 tree=BVHTree.FromPolygons(allverts,allfaces,all_triangles=True)
 for x in [-.11,0,.11]:
  for z in [.32,.43,.54]:
   hit,normal,idx,dist=tree.ray_cast(Vector((x,-.6,z)),Vector((0,1,0)),1)
   assert hit is not None and abs(hit.y-.253)<1e-5,(x,z,hit)
   probes.append({'ray_origin_m':[x,-.6,z],'rear_bottom_hit_m':list(hit),'distance_m':dist})
 report['actual_open_mouth_nine_rays']=probes
 # Axis hole clearance has actual sampled polygonal sleeve boundary, not an AABB assertion.
 clearances=[]
 for i in [1,2]:
  ob=next(o for o in moving if o.name.startswith('Door bored hinge sleeve '+str(i)));radial=sorted({round(math.hypot(v.x-axis.x,v.y-axis.y),7) for v in data(ob)[1]});assert abs(radial[0]-.010)<1e-6
  clearances.append({'sleeve':ob.name,'inner_vertex_radius_m':radial[0],'actual_polygon_inradius_m':radial[0]*math.cos(math.pi/16),'pin_max_radius_m':.008,'minimum_radial_clearance_m':radial[0]*math.cos(math.pi/16)-.008})
 report['bored_hinge_clearances']=clearances
 report['actual_imported_pivot']={'name':pivot.name,'origin_m':list(axis),'imported_rotation_mode':original_mode,'test_rotation_mode':'XYZ','moving_meshes':[o.name for o in moving],'fixed_mesh_count':len(fixed),'vertex_tests':pivot_records}
 for ob in list(s.objects):bpy.data.objects.remove(ob,do_unlink=True)
 bpy.context.window.scene=source_scene;bpy.data.scenes.remove(s)
 return report

s.cycles.samples=512;render('thumbnail',(2,-4,2));s.cycles.samples=128
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
pivot.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=True)
roundtrip=validate_candidate_roundtrip(parts,pivot,OUT/'model.glb');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
interface=verify_actual_washer_interface();(OUT/'interface-check.json').write_text(json.dumps(interface,indent=2))
if '--no-render' in sys.argv:
 (OUT/'final-roundtrip.json').write_text(json.dumps(roundtrip,indent=2));print('FORMAL_REPRODUCTION_COMPLETE',ASSET);raise SystemExit(0)
for name,loc in [('qa-front',(0,-4,QA_FOCUS_Z)),('qa-side',(4,0,QA_FOCUS_Z)),('qa-back',(0,4,QA_FOCUS_Z)),('qa-top',(0,0,5))]:render(name,loc)
wiremat=mat('Actual edge diagnostic',.025);overlays=[]
for o in parts:
 curve=bpy.data.curves.new('Actual edge segments','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=.001;curve.bevel_resolution=0
 for edge in o.data.edges:
  spline=curve.splines.new('POLY');spline.points.add(1)
  for point,vid in zip(spline.points,edge.vertices):point.co=(*tuple(o.matrix_world@o.data.vertices[vid].co),1)
 w=bpy.data.objects.new('QA actual edges '+o.name,curve);s.collection.objects.link(w);curve.materials.append(wiremat);overlays.append(w)
render('qa-wireframe',(2,-4,2))
for w in overlays:bpy.data.objects.remove(w,do_unlink=True)
triangles=sum(len(o.data.loop_triangles) for o in parts);vs=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
qa=json.loads((OUT/'technical-stage.json').read_text());qa.update({'asset':ASSET,'stage':'candidate','artPassed':False,'approved':False,'triangles':triangles,'bounds_m':bounds,'final_colored_glb_roundtrip':roundtrip,'mechanism_scope':'Editable door pivot tested only in two fixed poses; no continuous motion or appliance function simulation.','view_count':6,'samples':{'hero':512,'qa':128},'washer_fixed_pose_interface':interface});qa['door_motion']={'applicable':True,'finite_poses_degrees':[0,-100],'continuous_clearance_certified':False,'scope':'Two fixed imported-node poses and actual geometry only'};(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
files={}
for key,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 b=(OUT/name).read_bytes();files[key]={'path':f'assets/laundry/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'laundry','style':'S01-clean-geometric','title':'Static Front-Loading Washing Appliance','description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({o.data.materials[p.material_index].name for o in parts for p in o.data.polygons}),'files':files,'status':'review','license':'All rights reserved'};(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print('FORMAL_CANDIDATE_COMPLETE',ASSET,triangles)
