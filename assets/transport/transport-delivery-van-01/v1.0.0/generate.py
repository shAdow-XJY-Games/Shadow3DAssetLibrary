import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;OUT.mkdir(exist_ok=True)
ASSET='transport-delivery-van-01'
THEME='transport'
TITLE='S01 Small Delivery Van'
DESCRIPTION='Original stylized small delivery vehicle with sloped cab, inset glazing, cargo cavity, real wheel arches and flat tire contact patches. Separate rear hinge node and source components; finite door poses verified. No driving, steering or continuous physics simulation.'
HERO_CAMERA=(4, -6, 3.2)
QA_CAMERAS={'qa-front': (0, -6, 0.9), 'qa-side': (6, 0, 0.9), 'qa-back': (0, 6, 0.9), 'qa-top': (0, 0, 7)}
QA_SCALE=4.3
WIRE_WIDTH=0.003
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
def mesh(n,vs,fs,m=0):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);s.collection.objects.link(o);o.data.materials.append(materials[m]);parts.append(o);return o
def arch_cut(o,y):
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.351,depth=2.0,location=(0,y,.28),rotation=(0,math.pi/2,0));cut=bpy.context.object
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Real wheel opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
box('Chassis',(0,0,.43),(1.18,3.0,.10),2,.012)
for y in [-.9,-.3]:box('Cab body mounting bearer',(0,y,.515),(1.10,.12,.10),2,.006)
for y in [.1,1.25]:box('Cargo mounting bearer',(0,y,.555),(1.10,.13,.17),2,.006)
for x in [-.48,.48]:
 for y in [-1.05,1.05]:box('Fixed axle support',(x,y,.35),(.10,.10,.16),2,.006)

outline=[(-1.64,.55),(-1.64,.86),(-1.30,.94),(-.90,1.64),(-.10,1.64),(-.10,.55)]
n=len(outline);v=[(x,y,z) for x in [-.67,.67] for y,z in outline];f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
cab=mesh('Sloped cab',v,f);arch_cut(cab,-1.05)
# Closed recessed pane inside a real closed frame, not a coplanar color sheet.
def framed_window(name,corners,normal):
 normal=Vector(normal).normalized();front=name.startswith('Front');offset=.009 if front else .018;inset=.94 if front else .87;depth=.006 if front else .012
 outer=[Vector(v)+normal*offset for v in corners];center=sum(outer,Vector())/4;inner=[center+(v-center)*inset for v in outer]
 vs=[v+normal*d for poly,d in [(outer,depth),(outer,-offset-.012),(inner,-offset-.012),(inner,depth)] for v in poly]
 fs=[(j*4+i,j*4+(i+1)%4,((j+1)%4)*4+(i+1)%4,((j+1)%4)*4+i) for j in range(4) for i in range(4)]
 mesh(name+' frame',vs,fs,0)
 vs=[v+normal*d for d in [-.008,.002] for v in inner];fs=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
 mesh(name+' glazing',vs,fs,2)
for sign in [-1,1]:
 framed_window('Cab side',[(sign*.67,y,z) for y,z in [(-1.23,1.01),(-.86,1.57),(-.19,1.57),(-.19,1.01)]],(sign,0,0))
framed_window('Front windshield',[(-.58,-1.267,1.01),(.58,-1.267,1.01),(.58,-.932,1.58),(-.58,-.932,1.58)],(0,-.868,.496))
bpy.context.view_layer.objects.active=cab;mod=cab.modifiers.new('Cab edge scale','BEVEL');mod.width=.009;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
box('Cargo floor',(0,.72,.65),(1.40,1.76,.08),0,.008)
box('Cargo front',(0,-.16,1.23),(1.40,.06,1.10),0,.008)
for x in [-.68,.68]:
 o=box('Cargo side',(x,.72,1.16),(.06,1.80,1.20),0,.01);arch_cut(o,1.05)
box('Cargo roof',(0,.72,1.77),(1.44,1.84,.06),1,.012)
door=box('Rear cargo door',(0,1.645,1.22),(1.28,.05,1.02),0,.009)
pivot=bpy.data.objects.new('Rear hinge pivot',None);s.collection.objects.link(pivot);pivot.location=(-.66,1.675,1.22);bpy.context.view_layer.update();mw=door.matrix_world.copy();door.parent=pivot;door.matrix_world=mw
leaves=[pivot]
for y in [-1.05,1.05]:
 box('Axle',(0,y,.28),(1.43,.065,.065),2,.005)
 for x in [-.70,.70]:
  N=16;rr=.28/math.cos(math.pi/N);vs=[(xx,y+rr*math.sin(i*math.tau/N+math.pi/N),.28+rr*math.cos(i*math.tau/N+math.pi/N)) for xx in [x-.085,x+.085] for i in range(N)]
  fs=[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];mesh('Tire',vs,fs,2)
  sign=1 if x>0 else -1;N=12;vs=[]
  for xx,rad in [(x+sign*.094,.135),(x+sign*.074,.135),(x+sign*.074,.092),(x+sign*.094,.092)]:
   vs.extend([(xx,y+rad*math.cos(i*math.tau/N),.28+rad*math.sin(i*math.tau/N)) for i in range(N)])
  fs=[(j*N+i,j*N+(i+1)%N,((j+1)%4)*N+(i+1)%N,((j+1)%4)*N+i) for j in range(4) for i in range(N)];mesh('Wheel hub rim',vs,fs,1)
  for rad,dx,depth,name in [(.093,.075,.012,'Wheel hub recess'),(.032,.086,.018,'Wheel hub center')]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=rad,depth=depth,location=(x+sign*dx,y,.28),rotation=(0,math.pi/2,0));o=bpy.context.object;o.name=name;o.data.materials.append(materials[1 if rad<.05 else 2]);parts.append(o)
for x in [-.45,.45]:box('Rear bumper mounting bracket',(x,1.55,.43),(.09,.26,.09),2,.006)
for y in [-1.67,1.67]:box('Bumper',(0,y,.45),(1.47,.12,.15),2,.018)
for x in [-.5,.5]:box('Front lamp',(x,-1.65,.78),(.23,.025,.13),1,.009)
for x in [-.69,.69]:box('Side step',(x,-.40,.56),(.18,.48,.055),2,.009)
# Secondary functional shapes for silhouette refinement, still blockout.
for sign in [-1,1]:
 x=sign*.685
 # Lower door panel follows the front wheel opening rather than cutting into the tire.
 outline=[(-.83,.89),(-.70,.60),(-.18,.60),(-.18,.99),(-.83,.99)]
 n=len(outline);vs=[(xx,y,z) for xx in [x-sign*.008,x+sign*.008] for y,z in outline]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh('Cab door lower skin',vs,fs)
 box('Cab door handle',(sign*.711,-.27,.93),(.043,.14,.028),2,.005)
 box('Mirror arm',(sign*.75,-1.20,1.025),(.20,.035,.035),2,.005)
 box('Mirror housing',(sign*.86,-1.20,1.09),(.065,.16,.18),2,.012)
 box('Mirror inset surface',(sign*.86,-1.117,1.09),(.044,.012,.136),2,.003)
 for y in [-1.05,1.05]:
  N=11;vs=[]
  for xx,r in [(sign*.66,.345),(sign*.79,.345),(sign*.79,.39),(sign*.66,.39)]:
   for i in range(N):
    a=i*math.pi/(N-1);vs.append((xx,y+r*math.cos(a),.28+r*math.sin(a)))
  fs=[(j*N+i,j*N+i+1,((j+1)%4)*N+i+1,((j+1)%4)*N+i) for j in range(4) for i in range(N-1)]
  fs.extend([(0,N,2*N,3*N),(N-1,4*N-1,3*N-1,2*N-1)])
  mesh('Wheel arch rolled lip',vs,fs,0)
# Narrow transition shoulders link the lower cab roof to the tall cargo volume.
for x in [-.63,.63]:box('Cab rear transition',(x,-.105,1.43),(.09,.14,.44),0,.016)
box('Front grille recess',(0,-1.65,.685),(.61,.04,.14),2,.004)
for z in [.65,.70,.74]:box('Grille bar',(0,-1.67,z),(.55,.015,.012),1,.002)
box('Bumper upper step',(0,-1.66,.54),(1.31,.15,.04),1,.006)
for x in [-.68,.68]:box('Rear tail lamp',(x,1.63,.85),(.04,.04,.20),2,.006)
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
 raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+size]);nodes=gltf['nodes'];pn=next(n for n in nodes if n.get('name')==pivot.name)
 expected={o.name for o in parts if o.parent==pivot};actual={nodes[i]['name'] for i in pn.get('children',[])};assert expected<=actual,('Lost hinge child nodes',expected,actual)
 original=bpy.context.window.scene;test=bpy.data.scenes.new('Candidate actual GLB import');bpy.context.window.scene=test;bpy.ops.import_scene.gltf(filepath=str(path));imported=[o for o in test.objects if o.type=='MESH'];triangles={n:[] for n in source_checks}
 for o in imported:
  for key,xyz in world_triangle_records(o):
   assert key in owners and owners[key],('GLB world oriented triangle/PBR mismatch',o.name,key)
   triangles[owners[key].pop()].append(xyz)
 assert not any(owners.values()),'GLB lost source triangles'
 checks={}
 for n,tris in triangles.items():
  vs=[v for t in tris for v in t];fs=[(i,i+1,i+2) for i in range(0,len(vs),3)];me=bpy.data.meshes.new('Provenance temp');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Provenance temp',me);checks[n]=verify_joined_closed_mesh(o);bpy.data.objects.remove(o);bpy.data.meshes.remove(me)
 for o in list(test.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.window.scene=original;bpy.data.scenes.remove(test)
 return {'source_component_count':len(parts),'imported_mesh_node_count':len(imported),'world_oriented_triangle_and_pbr_sha256':source_hash,'per_source_roundtrip':checks,'hinge_node':pivot.name,'hinge_children':sorted(actual),'pivot_gltf_translation':pn.get('translation'),'all_source_triangles_matched':True}

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
 bpy.context.view_layer.update();moving=[o for o in parts if o.parent==moving_pivot];static=[o for o in parts if o not in moving];cache={o.name:tree(o) for o in static}
 assert moving_pivot.parent is None and abs(moving_pivot.rotation_euler.x)<1e-9 and abs(moving_pivot.rotation_euler.y)<1e-9 and all(abs(v-1)<1e-9 for v in moving_pivot.scale), 'Expected unparented unscaled world-Z hinge'
 report['door_motion']['assumptions']={'axis':'world Z','pivot_unparented':True,'pivot_scale':[float(v) for v in moving_pivot.scale],'floating_distance_margin_m':2e-6,'precision':'Blender float geometry; numerical certificate with stated margin, not symbolic exact arithmetic'}
 step=20 if '--fixture-between' in __import__('sys').argv else 1
 angles=sorted(set(list(range(0,abs(angle_degrees)+1,step))+[abs(angle_degrees)]))
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
   if len(anchors)<3:
    for src,other in [(a,tb),(b,ta)]:
     for tri in world_triangles(src):
      normal=(tri[1]-tri[0]).cross(tri[2]-tri[0]).normalized()
      for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
       pt=sum((v*w for v,w in zip(tri,weights)),Vector())-normal*.0005
       if not all(lo[k]<=pt[k]<=hi[k] for k in range(3)):continue
       da=ta.find_nearest(pt)[3];db=tb.find_nearest(pt)[3]
       if min(da,db)>=.0002 and inside(ta,pt) and inside(tb,pt):anchors.append({'world_m':list(pt),'clearance_a_m':da,'clearance_b_m':db})
   if len(anchors)>=3:
    first=anchors[0];p0=Vector(first['world_m']);second=max(anchors,key=lambda q:(Vector(q['world_m'])-p0).length);v1=Vector(second['world_m'])-p0;third=max(anchors,key=lambda q:v1.cross(Vector(q['world_m'])-p0).length)
    if v1.cross(Vector(third['world_m'])-p0).length>1e-10:add_edge(a,b,'interior-overlap',[first,second,third]);continue
   contacts=[]
   for tri in world_triangles(a):
    na=(tri[1]-tri[0]).cross(tri[2]-tri[0]).normalized()
    for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
     pt=sum((v*w for v,w in zip(tri,weights)),Vector());hit,nb,idx,d=tb.find_nearest(pt)
     if d is not None and d<1e-5 and na.dot(nb)<-.95:contacts.append({'world_m':list(pt),'distance_m':d,'normal_dot':na.dot(nb)})
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
 if '--continuous-experiment' in __import__('sys').argv:
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
 
 moving_pivot.rotation_euler.z=0;bpy.context.view_layer.update();report['door_motion']['sampled_pass']=True
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
 moving_pivot.select_set(True)
 bpy.ops.export_scene.gltf(filepath=str(out/'technical-model.glb'),export_format='GLB',use_selection=True,export_apply=True)
 report['glb_roundtrip']=validate_candidate_roundtrip(parts,moving_pivot,out/'technical-model.glb')
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'technical-source.blend'))
 (out/'technical-stage.json').write_text(json.dumps(report,indent=2));print('BLOCKOUT_TECHNICAL_STAGE_COMPLETE')

import sys
candidate_geometry_gate(parts,leaves[0],105,OUT)
if '--geometry-only' in sys.argv:raise SystemExit(0)
# Lighting rig kept out of model parts.
for n,loc,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-1,3),350,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.90))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
def render(n,xyz,scale=4.3,res=512):
 if '--no-render' in sys.argv:return
 cam.location=Vector(xyz);cam.rotation_euler=(Vector((0,0,.90))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;s.render.resolution_x=res;s.render.resolution_y=res;s.render.filepath=str(OUT/(n+'.png'));bpy.ops.render.render(write_still=True)
render('gray-closed',(4,-6,3.2));render('gray-front',(0,-6,.9));render('gray-side',(6,0,.9))
leaves[0].rotation_euler.z=math.radians(105)
render('gray-open',(-4,6,3.2),4.8);leaves[0].rotation_euler.z=0
start=len(parts)
box('1.75m scale reference',(2.5,0,.875),(.025,.025,1.75),2,.001)
for z in [0,.5,1,1.5,1.75]:box('Scale tick',(2.5,0,z),(.12,.03,.012),2,.001)
render('scale-reference',(4,-6,3.2),6.2)
for o in parts[start:]:o.hide_render=True
def color_mat(n,rgb,rough):
 m=mat(n,.5);m.diffuse_color=(*rgb,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Roughness'].default_value=rough;return m
paint=color_mat('S01 ochre paint',(.64,.31,.08),.66);glass=color_mat('S01 opaque glazing',(.055,.10,.13),.46);rubber=color_mat('S01 tire',(.025,.032,.035),.9);metal=color_mat('S01 metal',(.20,.23,.25),.52);light=color_mat('S01 lamp',(.90,.74,.42),.4)
glass.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=.22
cargo=color_mat('S01 warm light cargo shell',(.67,.65,.57),.74)
for o in parts:
 n=o.name
 if n.startswith('Cargo') or n.startswith('Rear cargo'):m=cargo
 elif n.startswith('Tire'):m=rubber
 elif 'Front windshield frame' in n:m=rubber
 elif 'glazing' in n or 'Mirror inset' in n:m=glass
 elif 'hub recess' in n:m=rubber
 elif any(w in n for w in ['hub','Axle','Chassis','mounting bearer','axle support','Grille','grille','handle','Bumper','Bumper','Mirror','step']):m=metal
 elif 'lamp' in n:m=light
 else:m=paint
 o.data.materials.clear();o.data.materials.append(m)
s.cycles.samples=512
render('material-A',(4,-6,3.2));s.cycles.samples=128;leaves[0].rotation_euler.z=math.radians(105);render('material-A-open',(-4,6,3.2),4.8);leaves[0].rotation_euler.z=0


# Formal candidate package, still awaiting independent art and technical approval.
import shutil,datetime
for o in list(parts):
 if 'scale reference' in o.name or 'Scale tick' in o.name:
  parts.remove(o);bpy.data.objects.remove(o,do_unlink=True)
leaves[0].rotation_euler.z=0;bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
leaves[0].select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=True)
final_roundtrip=validate_candidate_roundtrip(parts,leaves[0],OUT/'model.glb')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
if '--no-render' in sys.argv:
 (OUT/'final-roundtrip.json').write_text(json.dumps(final_roundtrip,indent=2));print('FORMAL_REPRODUCTION_COMPLETE',ASSET);raise SystemExit(0)
shutil.copyfile(OUT/'material-A.png',OUT/'thumbnail.png')
s.cycles.samples=128
for name,xyz in QA_CAMERAS.items():render(name,xyz,QA_SCALE)
# Actual mesh-edge overlay; excludes presentation geometry and lights.
wiremat=mat('Diagnostic edge',.025)
overlays=[]
for o in parts:
 w=o.copy();w.data=o.data.copy();s.collection.objects.link(w);w.name='QA edges '+o.name;w.data.materials.clear();w.data.materials.append(wiremat)
 mod=w.modifiers.new('Actual editable mesh edges','WIREFRAME');mod.thickness=WIRE_WIDTH;mod.use_replace=True;mod.offset=1
 overlays.append(w)
render('qa-wireframe',HERO_CAMERA,QA_SCALE)
for o in overlays:bpy.data.objects.remove(o,do_unlink=True)
triangles=sum(len(o.data.loop_triangles) for o in parts);vertices=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[max(v[k] for v in vertices)-min(v[k] for v in vertices) for k in range(3)]
qa=json.loads((OUT/'technical-stage.json').read_text());qa.update({'asset':ASSET,'stage':'candidate','artPassed':False,'approved':False,'triangles':triangles,'bounds_m':bounds,'final_colored_glb_roundtrip':final_roundtrip,'view_count':6,'samples':{'hero':512,'qa':128},'mechanism_scope':'Independent editable hinge node and the finite tested poses recorded in door_motion; no animation, continuous-motion, load or physics claim.'})
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
files={}
for key,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 data=(OUT/name).read_bytes();files[key]={'path':f'assets/{THEME}/{ASSET}/v1.0.0/{name}','size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':THEME,'style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION+' '+qa['mechanism_scope'],'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print('FORMAL_CANDIDATE_COMPLETE',ASSET,triangles)

# True opaque black silhouette material; no lighting influence.
black=bpy.data.materials.new('Silhouette black');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs[0]);s.view_layers[0].material_override=black;s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(1,1,1,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=1
render('silhouette-front-128',(0,-6,.9),4.0,128);render('silhouette-side-128',(6,0,.9),4.0,128)
s.view_layers[0].material_override=None
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'graybox.blend'))
(OUT/'stage.json').write_text(json.dumps({'stage':'blockout','artPassed':False,'formal_asset':False,'style':'S01','prior_asset':None,'counts_as':'new-functional-model','dimensions_m':[1.5,3.3,1.8],'mechanism':'Rear cargo door pivot demonstration only; final swept-clearance/GLB independent-node gate not yet run','images':['gray-closed','gray-front','gray-side','gray-open','silhouette-front-128','silhouette-side-128']},indent=2))
print('GRAYBOX_COMPLETE')
