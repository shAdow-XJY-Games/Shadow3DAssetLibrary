"""Select named playing halves, net, mounts and frame/leg parts independently at unit scale; keep the supplied fixed installation for the validated geometry. Surface height is .76m above the four original foot bottoms. All 36 net holes are real geometry with opaque materials. Playing lines are material assignments on coplanar shared-vertex top faces, not separate overlays. No folding or ball behavior is provided. Dimensions reference the official technical table at https://play-style.cornilleau.com/en/ping-pong-tables/3362-classic-outdoor-ping-pong-table-white.html (274 x 152.5 x 76cm, read 2026-10-16); original design, no vendor model or engineering certification. Example installation uses six unchanged Paving_Core_2x2 nodes for a 6x4m display area, not a regulation/safe play area."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;OUT.mkdir(exist_ok=True)
ASSET='sports-outdoor-table-tennis-table-01'
DESCRIPTION='Original fixed outdoor table-tennis asset with two complete planar playing halves, a small center joint, actual painted face partitions, four foot pads and legs, perimeter and transverse frames, two-ended knee braces, and a continuous closed net mesh with 36 true openings attached to two real post/arm mounts. Playing surface dimensions 2.74 x 1.525 metres, height .76m, are proportion references only. Editable assembled static geometry; no folding, ball physics, bounce, weather/load rating, competition or safety certification. Reused paving display is only a measured installation example, not a regulation activity area.'
QA_FOCUS_Z=.46
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100
s.world.color=(.3,.3,.3);s.view_settings.view_transform='AgX'
def mat(n,v):
 m=bpy.data.materials.new(n);m.diffuse_color=(*([v]*3),1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*([v]*3),1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.78;return m
def surface(name,c,metal=0,rough=.65):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
materials=[surface('S01 muted blue playing surface',(.035,.18,.24)),surface('S01 outdoor frame',(.18,.23,.24),.35,.55),surface('S01 dark net and foot pads',(.055,.07,.075)),surface('S01 pale playing marks and tape',(.72,.76,.70))]

parts=[]
def box(n,loc,size,m=0,bevel=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[m]);parts.append(o)
 if bevel:
  mod=o.modifiers.new('Designed edge','BEVEL');mod.width=bevel;mod.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o


KIND='fixed-outdoor-table-tennis'
def meshpart(name,vs,fs,mi=0,indices=None):
 import bmesh
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);parts.append(o)
 for m in materials:me.materials.append(m)
 for i,p in enumerate(me.polygons):p.material_index=indices[i] if indices else mi
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def half(name,x0,x1):
 xs=[x0,x0+.02,x1-.02,x1];ys=[-.7625,-.7425,-.0015,.0015,.7425,.7625];nx=len(xs);ny=len(ys);vs=[(x,y,.76) for y in ys for x in xs];fs=[];mi=[]
 for j in range(ny-1):
  for i in range(nx-1):
   v=j*nx+i;fs.append((v,v+1,v+1+nx,v+nx));mi.append(0)
 boundary=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range((ny-1)*nx+nx-2,(ny-1)*nx-1,-1))+[j*nx for j in range(ny-2,0,-1)]
 bottom=[]
 for k in boundary:bottom.append(len(vs));vs.append((vs[k][0],vs[k][1],.728))
 fs.append(tuple(reversed(bottom)));mi.append(0)
 for i in range(len(boundary)):fs.append((boundary[i],bottom[i],bottom[(i+1)%len(bottom)],boundary[(i+1)%len(boundary)]));mi.append(0)
 return meshpart(name,vs,fs,indices=mi)
half('Playing half left',-1.37,-.002);half('Playing half right',.002,1.37)
for y in [-.65,.65]:box('Long side frame',(0,y,.705),(2.62,.055,.055),1,.004)
for x in [-.9,.9]:
 box('Transverse underframe',(x,0,.695),(.075,1.34,.06),1,.004)
 for y in [-.55,.55]:
  box('Grounded foot pad',(x,y,.02),(.14,.14,.04),2,.006)
  box('Fixed upright leg',(x,y,.37),(.065,.065,.67),1,.004)
  # Triangular knee strut runs up and in along length, joining leg and frame.
  A=Vector((x,y,.44));B=Vector((x-math.copysign(.28,x),y+math.copysign(.10,y),.705));d=B-A
  o=box('Knee brace',(A+B)/2,(.042,.042,d.length+.02),1,.002);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
# Low longitudinal pair provides a visible continuous understructure, not folding hardware.
for y in [-.55,.55]:box('Lower longitudinal tie',(0,y,.29),(1.84,.04,.05),1,.003)
for y in [-.765,.765]:box('Net side mounting arm',(0,y,.695),(.10,.28,.06),1,.004)
for y in [-.865,.865]:box('Fixed net support post',(0,y,.805),(.035,.035,.22),1,.003)
# Single continuous, closed, genuinely perforated net grid. No alpha texture or opaque wall.
yb=[-.86]
for k in range(13):
 c=-.854+k*(1.708/12)
 yb.extend([c-.003,c+.003])
yb=sorted(set([-.86,.86]+[max(-.86,min(.86,y)) for y in yb]))
zb=[.766,.772,.811,.815,.854,.858,.9025,.9085]
occupied=set()
for j in range(len(zb)-1):
 for i in range(len(yb)-1):
  mid=(yb[i]+yb[i+1])/2
  if j in [0,2,4,6] or any(abs(mid-(-.854+k*(1.708/12)))<.00301 for k in range(13)):occupied.add((i,j))
verts=[];faces=[];vid={}
def vi(v):
 if v not in vid:vid[v]=len(verts);verts.append(v)
 return vid[v]
def face(q):faces.append(tuple(vi(v) for v in q))
for i,j in occupied:
 y0,y1=yb[i:i+2];z0,z1=zb[j:j+2];x0,x1=-.003,.003
 face([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]);face([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)])
 if (i-1,j) not in occupied:face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)])
 if (i+1,j) not in occupied:face([(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)])
 if (i,j-1) not in occupied:face([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)])
 if (i,j+1) not in occupied:face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
meshpart('Continuous real-open net grid',verts,faces,2)
box('Net top tape',(0,0,.9095),(.011,1.70,.006),0,0)
bpy.context.view_layer.update()
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
   if len(anchors)<3:
    for src,other in [(a,tb),(b,ta)]:
     for tri in world_triangles(src):
      normal=(tri[1]-tri[0]).cross(tri[2]-tri[0]).normalized()
      for weights in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6),(.8,.1,.1),(.1,.8,.1),(.1,.1,.8)]:
       pt=sum((v*w for v,w in zip(tri,weights)),Vector())-normal*.0005
       if not all(lo[k]<=pt[k]<=hi[k] for k in range(3)):continue
       da=ta.find_nearest(pt)[3];db=tb.find_nearest(pt)[3]
       if min(da,db)>=.0002 and inside(ta,pt) and inside(tb,pt):anchors.append({'world_m':list(pt),'clearance_a_m':da,'clearance_b_m':db})
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
for o in parts:
 if o.name.startswith('Playing half'):
  for p in o.data.polygons:
   center=sum((o.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
   if p.normal.z>.99 and (abs(center.x)>1.349 or abs(center.y)>.741 or abs(center.y)<.0016):p.material_index=3
 if o.name=='Net top tape':o.data.materials.clear();o.data.materials.append(materials[3])
candidate_geometry_gate(parts,None,0,OUT)
if '--geometry-only' in sys.argv:raise SystemExit(0)
focus=Vector((0,0,.46));scale=3.8
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
 shift=right*((min(xs)+max(xs))/2-center.dot(right))+up*((min(ys)+max(ys))/2-center.dot(up));cam.location+=shift
 cam.data.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.28
 s.render.resolution_x=res;s.render.resolution_y=res;s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)

def verify_actual_table_net():
 from mathutils.bvhtree import BVHTree
 source_scene=bpy.context.window.scene;test=bpy.data.scenes.new('Actual table net proof');bpy.context.window.scene=test;bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));obs=[o for o in test.objects if o.type=='MESH']
 def tris(o):
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];return [[vs[i] for i in t.vertices] for t in o.data.loop_triangles]
 def tree(tt):return BVHTree.FromPolygons([v for t in tt for v in t],[(i*3,i*3+1,i*3+2) for i in range(len(tt))],all_triangles=True)
 net=next(o for o in obs if o.name.startswith('Continuous real-open net grid'));nt=tree(tris(net));openings=[]
 for i in range(12):
  y=-.854+(i+.5)*(1.708/12)
  for z in [.7915,.8345,.88025]:
   assert nt.ray_cast(Vector((-.1,y,z)),Vector((1,0,0)),.2)[0] is None;openings.append([y,z])
 for z in [.769,.813,.856,.905]:assert nt.ray_cast(Vector((-.1,0,z)),Vector((1,0,0)),.2)[0] is not None
 halves=[o for o in obs if o.name.startswith('Playing half')];assert len(halves)==2;allv=[];surfaces=[]
 for o in halves:
  tt=tris(o);top=[t for t in tt if (t[1]-t[0]).cross(t[2]-t[0]).normalized().z>.999];vv=[v for t in top for v in t];assert max(abs(v.z-.76) for v in vv)<1e-6;allv+=vv;surfaces.append({'half':o.name,'flat_top_z':.76,'area_m2':sum((t[1]-t[0]).cross(t[2]-t[0]).length/2 for t in top)})
 dims=[max(v[k] for v in allv)-min(v[k] for v in allv) for k in [0,1]];assert abs(dims[0]-2.74)<1e-6 and abs(dims[1]-1.525)<1e-6
 posts=[o for o in obs if o.name.startswith('Fixed net support post')];assert len(posts)==2;contacts=[len(nt.overlap(tree(tris(o)))) for o in posts];assert all(n>0 for n in contacts)
 shifted=tree([[v+Vector((.12,0,0)) for v in t] for t in tris(net)]);negative=[len(shifted.overlap(tree(tris(o)))) for o in posts];assert not any(negative)
 report={'model_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'mesh_count':len(obs),'actual_open_hole_rays':openings,'actual_solid_band_rays':4,'flat_playing_halves':surfaces,'playing_dimensions_m':dims,'actual_net_post_intersections':contacts,'net_x_120mm_detachment_negative':{'rejected':True,'remaining_post_contacts':negative},'scope':'Fixed low-poly installation and actual mesh interfaces; no folding, ball physics, rating or play-area certification.'}
 for o in list(test.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.window.scene=source_scene;bpy.data.scenes.remove(test);return report
s.cycles.samples=512;render('thumbnail',(3,-4,2.6));s.cycles.samples=128
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=True)
roundtrip=validate_candidate_roundtrip(parts,None,OUT/'model.glb');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
interface=verify_actual_table_net();(OUT/'interface-check.json').write_text(json.dumps(interface,indent=2))
if '--no-render' in sys.argv:
 (OUT/'final-roundtrip.json').write_text(json.dumps(roundtrip,indent=2));print('FORMAL_REPRODUCTION_COMPLETE',ASSET);raise SystemExit(0)
for name,loc in [('qa-front',(0,-4,QA_FOCUS_Z)),('qa-side',(4,0,QA_FOCUS_Z)),('qa-back',(0,4,QA_FOCUS_Z)),('qa-top',(0,0,5))]:render(name,loc)
wiremat=mat('Actual edge diagnostic',.025);overlays=[]
for o in parts:
 curve=bpy.data.curves.new('Actual edge segments','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=.0035;curve.bevel_resolution=0
 for edge in o.data.edges:
  spline=curve.splines.new('POLY');spline.points.add(1)
  for point,vid in zip(spline.points,edge.vertices):point.co=(*tuple(o.matrix_world@o.data.vertices[vid].co),1)
 w=bpy.data.objects.new('QA actual edges '+o.name,curve);s.collection.objects.link(w);curve.materials.append(wiremat);overlays.append(w)
render('qa-wireframe',(3,-4,2.6))
for w in overlays:bpy.data.objects.remove(w,do_unlink=True)
triangles=sum(len(o.data.loop_triangles) for o in parts);vs=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
qa=json.loads((OUT/'technical-stage.json').read_text());qa.update({'asset':ASSET,'stage':'candidate','artPassed':False,'approved':False,'triangles':triangles,'bounds_m':bounds,'final_colored_glb_roundtrip':roundtrip,'mechanism_scope':'Static editable source and GLB components; no moving part or load simulation claim.','view_count':6,'samples':{'hero':512,'qa':128},'table_net_interface':interface});qa['door_motion']={'applicable':False,'scope':'Fixed static display, no door or motion promise'};(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
files={}
for key,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 b=(OUT/name).read_bytes();files[key]={'path':f'assets/sports/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':'Fixed Outdoor Table Tennis Table','description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({o.data.materials[p.material_index].name for o in parts for p in o.data.polygons}),'files':files,'status':'review','license':'All rights reserved'};(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print('FORMAL_CANDIDATE_COMPLETE',ASSET,triangles)
