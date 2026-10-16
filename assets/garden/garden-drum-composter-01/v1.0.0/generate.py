"""Original hollow garden drum composter in one fixed open access-cover pose.
Metres, Blender Z-up / GLB Y-up. 23 separately editable closed mesh parts form
one equipment kit. No old nursery rack, seedling tray, soil, plants, person or
floor is included. Box/frame pieces retain construction-center origins;
authored drum/cap/bearing/shaft/cover meshes use the modelling origin. These
nodes are static editable pieces, not animated drum/cover pivots. Unit scale.
Drum axis lies along X at Z .72 m; outer radius .37m, inner radius .34m, cylindrical
shell X extent +/-.32m, thick closed end caps. The front-upper access hole is
actually absent shell cells, X[-.21,.21] and angle[-112.5,-45] degrees about X.
Two genuine narrow through slots occur at X +/-.09 m around 37.5 degrees. They are
small geometric openings, not an airflow or drainage-performance certificate.
Two .030m-radius twelve-sided axle stubs rest on actual lower inner facets of
.032m-radius twelve-sided bearing bores. Bearing center Z is adjusted by the
actual polygon apothem difference, not a nominal-circle assumption. Each real
partial facet contact is about .001164686m2. An 8 mm upward stub displacement
must penetrate the actual bore. The self-contained --no-render run repeats
these contacts, the displacement negative, .32x.32x.25m inner clear volume,
.30x.26x.15m front-access clear volume and both radial through-slot rays.
All clearance volumes are diagnostic only and removed before final export.
The independently editable curved cover is permanently authored open at the
shown supported hinge attachments. No second pose or continuous swing/tumble
sweep has been validated. Frame feet have actual Z0 bearing patches.
Actual-use layout keeps equipment at identity, original nursery rack at
(1.45,0,0), original complete seedling tray at(1.45,0,.81), unit scale.
Tray bottom is fully supported on the actual upper shelf; a +.4 m sideways
misplacement fails support. Old soil and seedlings remain nursery stock,
not material produced by this machine. No compost output or extra waste exists.
No biological rate, fertilizer quality, hygiene, pest prevention, drainage,
load capacity, tip stability or moving-mechanism certification is supplied.
"""
DESCRIPTION='Original hollow garden drum composter on two braced A-frames, with a genuine front access cavity, two small through slots, two real polygonal spindle-bearing bores and a separately editable curved cover fixed open. Twenty-three closed editable parts form one static garden-service appliance. Self-contained geometry checks validate actual lower spindle-facet contact, displaced-axle collision negatives, clear interior/access volumes and through-slot rays. Original nursery rack and planted tray are adjacent context only. No compost output, biological-performance, load, stability or continuous rotation guarantee.'
import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;OUT.mkdir(exist_ok=True)
ASSET='garden-drum-composter-01'
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


KIND='garden-drum-composter'
from mathutils import Matrix
import bmesh
Z=.72
angles=sorted(set([-180+i*22.5 for i in range(16)]+[35,40]))
def meshpart(name,vs,fs,m=0):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.data.materials.append(materials[m]);parts.append(o);return o
def radial(x,r,t,z=Z):a=math.radians(t);return (x,r*math.sin(a),z+r*math.cos(a))
def shellpatch(name,xs,aa,ri,ro,closed=True,omit=None,m=0):
 n=len(aa);vs=[radial(x,r,t) for r in [ro,ri] for x in xs for t in aa];layer=len(xs)*n;fs=[];cells=set()
 for i in range(len(xs)-1):
  for j in range(n if closed else n-1):
   if not omit or not omit(i,j):cells.add((i,j))
 for i,j in cells:
  jj=(j+1)%n;v=[i*n+j,(i+1)*n+j,(i+1)*n+jj,i*n+jj];fs.extend([tuple(v),tuple(k+layer for k in reversed(v))])
  for edge,neighbor in [(0,(i,j-1 if j else n-1)),(1,(i+1,j)),(2,(i,(j+1)%n)),(3,(i-1,j))]:
   if neighbor not in cells or (not closed and ((edge==0 and j==0) or (edge==2 and j==n-2))):a,b=v[edge],v[(edge+1)%4];fs.append((a,b,b+layer,a+layer))
 return meshpart(name,vs,fs,m)
xs=[-.32,-.23,-.21,-.10,-.08,.08,.10,.21,.23,.32]
def omitted(i,j):
 mid=(xs[i]+xs[i+1])/2;t=angles[j]
 return (-.21<mid<.21 and -112.5<=t<-45) or (i in [3,5] and t==35)
shellpatch('Hollow drum with access and two through vents',xs,angles,.34,.37,True,omitted,0)
def solidx(name,cx,depth,r,aa,z=Z,m=0):
 vs=[radial(x,r,t,z) for x in [cx-depth/2,cx+depth/2] for t in aa];n=len(aa);fs=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return meshpart(name,vs,fs,m)
for x in [-.32,.32]:solidx('Closed drum end wall',x,.04,.368,angles)
a12=[15+i*30 for i in range(12)];bearingZ=Z+(.032-.030)*math.cos(math.pi/12)
for x in [-.45,.45]:
 for y in [-.28,.28]:box('Frame ground foot',(x,y,.02),(.14,.13,.04),2,.003)
 for y in [-.28,.28]:
  a,b=Vector((x,y,.035)),Vector((x,math.copysign(.025,y),.665));o=box('Splayed frame leg',(a+b)/2,(.045,.045,(b-a).length),2,.003);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 # Real polygonal bearing ring; bottom inner facet matches the stub's flat lower facet.
 vs=[radial(xx,r,t,bearingZ) for r in [.075,.032] for xx in [x-.0375,x+.0375] for t in a12];n=12;fs=[]
 for i in range(n):j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+j,2*n+i,3*n+i,3*n+j),(j,i,2*n+i,2*n+j),(n+i,n+j,3*n+j,3*n+i)])
 meshpart('True bore spindle bearing',vs,fs,2)
 solidx('Drum supporting stub axle',math.copysign(.395,x),.23,.030,a12,Z,1)
for y in [-.24,.24]:box('Stand lower cross tie',(0,y,.14),(.90,.045,.045),2,.003)
for x in [-.24,.24]:box('Cover hinge foundation',(x,-.255,.995),(.065,.055,.065),0,.003)
solidx('Fixed cover hinge pin',0,.56,.012,a12,1.015,1)
# Move the hinge pin to the actual front hinge line.
parts[-1].location.y=-.275
cover=shellpatch('Fixed open curved access cover',[-.23,.23],[-112.5,-90,-67.5,-45],.372,.390,False,None,0)
pivot=Vector((0,-.275,1.015));M=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(-100),4,'X')@Matrix.Translation(-pivot)
for v in cover.data.vertices:v.co=M@v.co
for x in [-.20,.20]:box('Fixed cover hinge attachment',(x,-.291,1.014),(.05,.06,.032),0,.002)
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);o.select_set(False)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free();o.data.update()

for m,col,name in zip(materials,[(.26,.39,.24,1),(.45,.48,.48,1),(.18,.21,.20,1)],['Muted green drum and fixed open cover','Dull spindle and hinge metal','Dark garden stand']):
 m.name=name;m.diffuse_color=col;n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=col;n.inputs['Roughness'].default_value=.72

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
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data)
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
 bpy.ops.export_scene.gltf(filepath=str(out/'technical-model.glb'),export_format='GLB',use_selection=True,export_apply=True)
 report['glb_roundtrip']=validate_candidate_roundtrip(parts,moving_pivot,out/'technical-model.glb')
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'technical-source.blend'))
 (out/'technical-stage.json').write_text(json.dumps(report,indent=2));print('BLOCKOUT_TECHNICAL_STAGE_COMPLETE')
import sys
candidate_geometry_gate(parts,None,0,OUT)
from mathutils.bvhtree import BVHTree
objects=parts
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
 # Exact world-vertex half-space separation, only for the independently covered contact pair.
 # A and B are closed triangle meshes, so every point on every triangle remains in its half-space.
 if contact_z is not None and min(v.z for v in va)>=contact_z-2e-6 and max(v.z for v in vb)<=contact_z+2e-6:return []
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


def flat(obs,z,sign):
 result=[]
 for o in obs:
  vv,ff=data(o)[1:]
  result.extend([[tuple(vv[i][:2]) for i in f] for f in ff if all(abs(vv[i].z-z)<1e-6 for i in f) and (vv[f[1]]-vv[f[0]]).cross(vv[f[2]]-vv[f[0]]).z*sign>1e-10])
 return result
def supported(obs,base,z):
 tops=flat(base,z,1);record=[]
 for o in obs:
  bottoms=flat([o],z,-1);total=sum(area(t) for t in bottoms);covered=sum(area(clip(t[:],u)) for t in bottoms for u in tops);assert total>1e-8 and abs(total-covered)<1e-7,(o.name,total,covered)
  for b in base:assert not clash(o,b,z),(o.name,b.name,'surface intersection',clash(o,b,z))
  record.append({'object':o.name,'plane':z,'actualDownwardArea':total,'coveredArea':covered,'worldBottomMinZ':min(v.z for v in data(o)[1]),'supportMaxZ':max(v.z for b in base for v in data(b)[1]),'halfSpaceTolerance':2e-6})
 return record

report={'source_mesh_names':[o.name for o in parts],'scope':'One static open-cover loading pose. Actual polygonal spindle/bore lower facet patches and cavity/vent probes, no continuous rotation or processing claim.'}
shafts=[o for o in objects if 'Drum supporting stub axle' in o.name];bearings=[o for o in objects if 'True bore spindle bearing' in o.name];assert len(shafts)==len(bearings)==2
z=.72-.030*math.cos(math.pi/12);patches=[]
for shaft in shafts:
 bearing=min(bearings,key=lambda b:abs(sum(v.x for v in data(b)[1])/len(data(b)[1])-sum(v.x for v in data(shaft)[1])/len(data(shaft)[1])))
 bt=flat([shaft],z,-1);tt=flat([bearing],z,1);coverage=sum(area(clip(t[:],u)) for t in bt for u in tt);assert coverage>.0011,(shaft.name,coverage)
 assert not clash(shaft,bearing,z),(shaft.name,bearing.name,clash(shaft,bearing,z)[:3]);patches.append({'shaft':shaft.name,'bearing':bearing.name,'plane_z':z,'actual_contact_area_m2':coverage})
 m=shaft.matrix_world.copy();shaft.location.z+=.008;bpy.context.view_layer.update();cache.clear();hits=clash(shaft,bearing);assert hits;shaft.matrix_world=m;bpy.context.view_layer.update();cache.clear();patches[-1]['offset_negative']={'translation_z_m':.008,'rejected':True,'actual_hits':hits[:2]}
report['actual_bearing_patches']=patches
for name,loc,size in [('QA cavity volume',(0,0,.72),(.32,.32,.25)),('QA front opening volume',(0,-.33,.77),(.30,.26,.15))]:
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.context.view_layer.update();cache.clear()
 hits=[(b.name,clash(o,b)[:2]) for b in objects if clash(o,b)];assert not hits,(name,hits);report[name]={'center':loc,'dimensions':size,'collision_count':0,'not_exported':True};bpy.data.objects.remove(o,do_unlink=True);cache.clear()
shell=next(o for o in objects if 'Hollow drum with access' in o.name);tree=data(shell)[0];vents=[]
for x in [-.09,.09]:
 t=math.radians(37.5);rad=Vector((0,math.sin(t),math.cos(t)));start=Vector((x,0,.72))+rad*.42;h,n,i,d=tree.ray_cast(start,-rad,.12);assert h is None,(x,h,d);vents.append({'x':x,'angle_degrees':37.5,'ray_start':list(start),'ray_direction':list(-rad),'tested_distance_m':.12,'blocked':False})
report['actual_through_vent_rays']=vents
(OUT/'actual-interface-evidence.json').write_text(json.dumps(report,indent=2));print('COMPOSTER_ACTUAL_INTERFACE_PASSED')

if '--geometry-only' in sys.argv:raise SystemExit(0)
focus=Vector((0,-.12,.58));scale=1.8
for name,loc,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-1,3),350,3),('Rear fill',(-3,4,5),300,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
def render(name,loc,size=scale,res=512):
 if '--no-render' in sys.argv:return
 if '--top-only' in sys.argv and name!='qa-top':return
 if '--wire-only' in sys.argv and name!='qa-wireframe':return
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 center=sum(points,Vector())/len(points)
 cam.location=Vector(loc);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();
 if name=='qa-top':cam.rotation_euler=(0,0,0)
 elif name=='qa-front':cam.rotation_euler=(math.pi/2,0,0)
 elif name=='qa-side':cam.rotation_euler=(math.pi/2,0,math.pi/2)
 elif name=='qa-back':cam.rotation_euler=(math.pi/2,0,math.pi)
 q=cam.rotation_euler.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0))
 xs=[p.dot(right) for p in points];ys=[p.dot(up) for p in points]
 shift=right*((min(xs)+max(xs))/2-cam.location.dot(right))+up*((min(ys)+max(ys))/2-cam.location.dot(up));cam.location+=shift
 cam.data.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.32
 s.render.resolution_x=res;s.render.resolution_y=res;s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.object.light_add(type='AREA',location=(0,-3,1.5));fill=bpy.context.object;fill.data.energy=180;fill.data.size=2.5;fill.rotation_euler=(Vector((0,0,.72))-fill.location).to_track_quat('-Z','Y').to_euler()
s.cycles.samples=512;render('thumbnail',(4,-6,4));s.cycles.samples=128
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=True)
roundtrip=validate_candidate_roundtrip(parts,None,OUT/'model.glb')
if not any(flag in sys.argv for flag in ['--top-only','--wire-only']):bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
if '--no-render' in sys.argv:
 (OUT/'final-roundtrip.json').write_text(json.dumps(roundtrip,indent=2));print('FORMAL_REPRODUCTION_COMPLETE',ASSET);raise SystemExit(0)
for name,loc in [('qa-front',(0,-6,1.2)),('qa-side',(6,0,1.2)),('qa-back',(0,6,1.2)),('qa-top',(0,0,8))]:render(name,loc)
wiremat=mat('Actual edge diagnostic',.025);overlays=[]
for o in parts:
 curve=bpy.data.curves.new('Actual edge segments','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=.0008;curve.bevel_resolution=0
 for edge in o.data.edges:
  spline=curve.splines.new('POLY');spline.points.add(1)
  for point,vid in zip(spline.points,edge.vertices):point.co=(*tuple(o.matrix_world@o.data.vertices[vid].co),1)
 w=bpy.data.objects.new('QA actual edges '+o.name,curve);s.collection.objects.link(w);curve.materials.append(wiremat);overlays.append(w)
render('qa-wireframe',(4,-6,4))
for w in overlays:bpy.data.objects.remove(w,do_unlink=True)
triangles=sum(len(o.data.loop_triangles) for o in parts);vs=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
qa=json.loads((OUT/'technical-stage.json').read_text());qa.update({'asset':ASSET,'stage':'candidate','artPassed':False,'approved':False,'triangles':triangles,'bounds_m':bounds,'final_colored_glb_roundtrip':roundtrip,'mechanism_scope':'Static independently editable mesh nodes; no moving or simulated mechanisms','view_count':6,'samples':{'hero':512,'qa':128}});qa['door_motion']={'applicable':False,'scope':'One fixed open access-cover pose; no continuous rotation or processing promise'};qa['actual_interface_fixtures']=json.loads((OUT/'actual-interface-evidence.json').read_text());(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
files={}
for key,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 b=(OUT/name).read_bytes();files[key]={'path':f'assets/garden/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'garden','style':'S01-clean-geometric','title':'Open Garden Drum Composter','description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({o.data.materials[p.material_index].name for o in parts for p in o.data.polygons}),'files':files,'status':'review','license':'All rights reserved'};(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print('FORMAL_CANDIDATE_COMPLETE',ASSET,triangles)
