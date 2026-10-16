"""One complete fixed table-football asset, not separate player or rod products. All named parts are unit-scale editable, feet lie at local Z0. Rows along Y: A1, A2, B3, A5, B5, A3, B2, B1; A faces +Y with negative-X grips, B faces -Y with positive-X grips. Eight rods are fixed in one centered pose, supported via their actual sleeve/end-collar contact geometry. No animation or advertised travel. Field top Z.780, player soles Z.791: 11mm static gap. Side bearings have actual 23mm polygonal bores around 18mm rods. Goal openings lead only into modeled local pockets, with no complete return route. Full bounds include eight grips and pockets. Separate original Floor_Centre_2x2 use translates the whole unit by (.14,0,.08), avoiding original board seams at each foot; the 2m panel is only a display platform, not a certified playing area. No ball, floor, human QA proxy or fixtures are exported here. No child-safety/load/physical-function certification."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).parent;OUT.mkdir(exist_ok=True)
ASSET='entertainment-table-football-01'
DESCRIPTION='Original fixed indoor table-football assembly with four feet and legs, tied frame, supported recessed marked field, two real goal openings into local enclosed pockets, eight rods through sixteen bored side bearings, fixed locating collars, eight grips and twenty-two solid figures in opposed 1-2-5-3 team arrangements. Full reported dimensions include all grips and end pockets. Named editable static components at one centered pose only; no telescopic or continuous rod movement, playable ball physics, scoring, complete ball-return route, load or child-safety certification. Original floor selection and full actual foot support are verified separately.'
QA_FOCUS_Z=.48
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100
s.world.color=(.3,.3,.3);s.view_settings.view_transform='AgX'
def mat(n,v):
 m=bpy.data.materials.new(n);m.diffuse_color=(*([v]*3),1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*([v]*3),1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.78;return m
materials=[mat('Warm cabinet',.4),mat('Satin rods and frame',.4),mat('Fixed dark grips and bearing sleeves',.15),mat('Green playing field',.3),mat('Terracotta team A',.3),mat('Blue team B',.3),mat('Field marking bands',.7)]
for m,c,metal,rough in zip(materials,[(.36,.25,.16),(.27,.30,.30),(.055,.07,.065),(.10,.25,.16),(.47,.12,.075),(.075,.21,.42),(.70,.72,.63)],[0,.45,0,0,0,0,0],[.67,.45,.75,.70,.62,.62,.72]):
 n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=(*c,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough

parts=[]
def box(n,loc,size,m=0,bevel=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[m]);parts.append(o)
 if bevel:
  mod=o.modifiers.new('Designed edge','BEVEL');mod.width=bevel;mod.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o


KIND='fixed-table-football'
def meshpart(name,vs,fs,m=0):
 import bmesh
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);parts.append(o);me.materials.append(materials[m]);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def cyl(name,loc,r,depth,m=1,rot=None,n=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(materials[m]);parts.append(o)
 if rot:o.rotation_euler=rot;bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
 return o

# Fixed original cabinet, four feet and supported recessed field.
for x in [-.305,.305]:
 for y in [-.52,.52]:
  box('Grounded square foot',(x,y,.018),(.105,.105,.036),2,.006)
  box('Table leg',(x,y,.378),(.082,.082,.738),0,.006)
for y in [-.52,.52]:box('Lower transverse tie',(0,y,.23),(.65,.055,.065),1,.005)
box('Lower long tie',(0,0,.23),(.055,1.08,.050),1,.005)
box('Field supporting floor',(0,0,.735),(.76,1.40,.055),0,.005)
# Single closed field mesh with coplanar material-region topology, no overlapping decal skin.
xb=[-.364,-.338,-.333,.333,.338,.364];yb=[-.685,-.658,-.653,-.0025,.0025,.653,.658,.685];vs=[];fs=[];mids=[];ids={}
def fv(v):
 if v not in ids:ids[v]=len(vs);vs.append(v)
 return ids[v]
def ff(vs1,m):fs.append(tuple(fv(v) for v in vs1));mids.append(m)
for i in range(len(xb)-1):
 for j in range(len(yb)-1):
  x0,x1=xb[i:i+2];y0,y1=yb[j:j+2];z0,z1=.752,.780
  marked=(i in [1,3] and - .658<=y0 and y1<=.658) or (j in [1,3,5] and -.338<=x0 and x1<=.338)
  ff([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)],0);ff([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],int(marked))
  if i==0:ff([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],0)
  if i==len(xb)-2:ff([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],0)
  if j==0:ff([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],0)
  if j==len(yb)-2:ff([(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)],0)
field=meshpart('Recessed playing field',vs,fs,3);field.data.materials.append(materials[6])
for polygon,mi in zip(field.data.polygons,mids):polygon.material_index=mi

ys=[-.56,-.40,-.24,-.08,.08,.24,.40,.56]
for x in [-.387,.387]:
 wall=box('Side cabinet wall',(x,0,.827),(.052,1.42,.206),0,.005)
 for y in ys:
  bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.025,depth=.12,location=(x,y,.88),rotation=(0,math.pi/2,0));cut=bpy.context.object;bpy.context.view_layer.objects.active=wall;mod=wall.modifiers.new('True rod wall aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# True end goal opening, with a distinct closed pocket enclosure behind it.
for sign in [-1,1]:
 y=sign*.704
 for x in [-.245,.245]:box('Goal end cheek',(x,y,.827),(.27,.045,.198),0,.004)
 box('Goal opening lintel',(0,y,.914),(.24,.046,.032),0,.003)
 box('Goal pocket floor',(0,sign*.753,.756),(.236,.128,.028),1,.003)
 box('Goal pocket back',(0,sign*.808,.824),(.242,.026,.152),0,.003)
 for x in [-.122,.122]:box('Goal pocket side',(x,sign*.754,.824),(.022,.13,.145),0,.003)
 box('Goal pocket roof',(0,sign*.755,.899),(.245,.120,.022),0,.003)
# Actual bored bearing sleeve: ring axis X, embedded into wall. Fixed collars carry each rod.
def ring(name,x,y,z,outer,inner,length):
 n=16;vs=[]
 for xx,rr in [(x-length/2,outer),(x+length/2,outer),(x-length/2,inner),(x+length/2,inner)]:
  for k in range(n):
   t=2*math.pi*k/n;vs.append((xx,y+rr*math.cos(t),z+rr*math.sin(t)))
 fs=[]
 for k in range(n):
  j=(k+1)%n;fs.extend([(k,j,n+j,n+k),(2*n+k,3*n+k,3*n+j,2*n+j),(k,2*n+k,2*n+j,j),(n+k,n+j,3*n+j,3*n+k)])
 return meshpart(name,vs,fs,2)
rows=[('A',1),('A',2),('B',3),('A',5),('B',5),('A',3),('B',2),('B',1)]
for row,(y,(team,count)) in enumerate(zip(ys,rows)):
 for x in [-.387,.387]:ring(f'Bearing row{row} side{x}',x,y,.88,.031,.0115,.066)
 cyl(f'Rod row{row} team{team}',(0,y,.88),.009,1.24,1,(0,math.pi/2,0),12)
 # Coplanar opposed annular surfaces with bearing ends, no rod movement promise.
 for x in [-.428,.428]:cyl(f'Fixed rod collar row{row}',(x,y,.88),.021,.016,1,(0,math.pi/2,0),16)
 side=-1 if team=='A' else 1
 cyl(f'Grip row{row} team{team}',(side*.65,y,.88),.021,.15,2,(0,math.pi/2,0),12)
 # One continuous solid per player, with projecting toe/head direction, no tiny face marks.
 xs={1:[0],2:[-.18,.18],3:[-.23,0,.23],5:[-.28,-.14,0,.14,.28]}[count];facing=1 if team=='A' else -1
 for pi,x in enumerate(xs):
  vs=[]
  for z,hx,hy,dy in [(.791,.021,.023,.012),(.813,.014,.013,0),(.850,.018,.015,0),(.895,.027,.019,0),(.912,.011,.011,0),(.920,.018,.016,.003),(.951,.018,.016,.003),(.960,.011,.010,.003)]:
   yy=y+dy*facing;vs.extend([(x-hx,yy-hy,z),(x+hx,yy-hy,z),(x+hx,yy+hy,z),(x-hx,yy+hy,z)])
  fs=[(0,3,2,1),(28,29,30,31)]
  for k in range(7):
   for i in range(4):j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
  meshpart(f'Player team{team} row{row} index{pi} face{facing}',vs,fs,4 if team=='A' else 5)
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
candidate_geometry_gate(parts,None,0,OUT)
if '--geometry-only' in sys.argv:raise SystemExit(0)
focus=Vector((0,0,.48));scale=2.2
for name,loc,power,size in [('Key',(-3,-4,6),700,4),('Fill',(4,-1,3),350,3),('Rear fill',(-3,4,5),300,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;s.camera=cam;cam.data.type='ORTHO'
def render(name,loc,size=scale,res=512):
 if '--no-render' in sys.argv:return
 if '--wire-only' in sys.argv and name!='qa-wireframe':return
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 center=sum(points,Vector())/len(points)
 cam.location=Vector(loc);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 axes={'qa-front':(0,-3,0),'qa-side':(3,0,0),'qa-back':(0,3,0),'qa-top':(0,0,3)}
 if name in axes:
  cam.location=center+Vector(axes[name]);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
  if name=='qa-top':cam.rotation_euler=(0,0,0)
 q=cam.rotation_euler.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0))
 xs=[p.dot(right) for p in points];ys=[p.dot(up) for p in points]
 shift=right*((min(xs)+max(xs))/2-center.dot(right))+up*((min(ys)+max(ys))/2-center.dot(up));cam.location+=shift
 cam.data.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.28
 s.render.resolution_x=res;s.render.resolution_y=res;s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
def verify_foosball_interface():
 from mathutils.bvhtree import BVHTree
 original=bpy.context.window.scene;test=bpy.data.scenes.new('Actual table football proof');bpy.context.window.scene=test;bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));obs=[o for o in test.objects if o.type=='MESH']
 def tris(o):
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];return [[vs[i] for i in t.vertices] for t in o.data.loop_triangles]
 def tree(tt):return BVHTree.FromPolygons([v for t in tt for v in t],[(i*3,i*3+1,i*3+2) for i in range(len(tt))],all_triangles=True)
 players=[o for o in obs if o.name.startswith('Player team')];bearings=[o for o in obs if o.name.startswith('Bearing row')];assert len(players)==22 and len(bearings)==16
 field=next(o for o in obs if o.name.startswith('Recessed playing field'));ft=tris(field);top=max(v.z for t in ft for v in t);assert abs(top-.78)<1e-6;clearances=[]
 for o in players:
  tt=tris(o);z=min(v.z for t in tt for v in t);assert z-top>.010 and not tree(tt).overlap(tree(ft));clearances.append({'player':o.name,'clearance_m':z-top})
 ys=[-.56,-.40,-.24,-.08,.08,.24,.40,.56];rows=[('A',1),('A',2),('B',3),('A',5),('B',5),('A',3),('B',2),('B',1)];bores=[]
 for row,(y,(team,count)) in enumerate(zip(ys,rows)):
  po=[o for o in players if f'row{row} ' in o.name];assert len(po)==count and all(f'team{team}' in o.name for o in po)
  near=[o for o in bearings if o.name.startswith(f'Bearing row{row} ')];assert len(near)==2
  for o in near:
   tt=tris(o);vv=[v for t in tt for v in t];x=(min(v.x for v in vv)+max(v.x for v in vv))/2;bt=tree(tt)
   for dy,dz in [(0,0),(.0105,0),(-.0105,0),(0,.0105),(0,-.0105)]:assert bt.ray_cast(Vector((x-.1,y+dy,.88+dz)),Vector((1,0,0)),.2)[0] is None
   assert bt.ray_cast(Vector((x-.1,y+.020,.88)),Vector((1,0,0)),.2)[0] is not None;bores.append(o.name)
  rod=next(o for o in obs if o.name.startswith(f'Rod row{row} '));assert not tree(tris(rod)).overlap(tree([t for o in near for t in tris(o)]))
 whole=tree([t for o in obs for t in tris(o)]);goals=[]
 for sign in [-1,1]:
  for x in [-.065,0,.065]:
   for z in [.805,.835,.865]:
    h=whole.ray_cast(Vector((x,sign*.63,z)),Vector((0,sign,0)),.25)[0];assert h is not None and abs(h.y)>.78;goals.append(list(h))
 h=whole.ray_cast(Vector((.17,-.63,.835)),Vector((0,-1,0)),.25)[0];assert h is not None and abs(h.y)<.75
 rod=next(o for o in obs if o.name.startswith('Rod row0 '));bad=tree([[v+Vector((0,0,.017)) for v in t] for t in tris(rod)]);nh=bad.overlap(tree([t for o in bearings if o.name.startswith('Bearing row0 ') for t in tris(o)]));assert nh
 badp=tree([[v-Vector((0,0,.025)) for v in t] for t in tris(players[0])]);assert badp.overlap(tree(ft))
 result={'model_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'player_count':22,'row_teams_counts':rows,'actual_player_field_clearances':clearances,'actual_bored_bearings':bores,'bore_clear_rays_per_bearing':5,'actual_goal_pocket_back_hits':goals,'negative_offset_goal_ray_blocked':True,'negative_rod17mm_bearing_crossings':len(nh),'negative_lowered_player_hits_field':True,'scope':'Only one centered fixed rod state. Bore gap and local goal pocket geometry; no rod travel/rotation, ball return route, physics, scoring, load or child-safety claim.'}
 for o in list(test.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.window.scene=original;bpy.data.scenes.remove(test);return result
s.cycles.samples=512;render('thumbnail',(2.5,-3,2.5));s.cycles.samples=128
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=True)
roundtrip=validate_candidate_roundtrip(parts,None,OUT/'model.glb');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
interface=verify_foosball_interface();(OUT/'interface-check.json').write_text(json.dumps(interface,indent=2))
if '--no-render' in sys.argv:
 (OUT/'final-roundtrip.json').write_text(json.dumps(roundtrip,indent=2));print('FORMAL_REPRODUCTION_COMPLETE',ASSET);raise SystemExit(0)
for name,loc in [('qa-front',(0,-4,QA_FOCUS_Z)),('qa-side',(4,0,QA_FOCUS_Z)),('qa-back',(0,4,QA_FOCUS_Z)),('qa-top',(0,0,5))]:render(name,loc)
wiremat=mat('Actual edge diagnostic',.025);overlays=[]
for o in parts:
 curve=bpy.data.curves.new('Actual edge segments','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=.0012;curve.bevel_resolution=0
 for edge in o.data.edges:
  spline=curve.splines.new('POLY');spline.points.add(1)
  for point,vid in zip(spline.points,edge.vertices):point.co=(*tuple(o.matrix_world@o.data.vertices[vid].co),1)
 w=bpy.data.objects.new('QA actual edges '+o.name,curve);s.collection.objects.link(w);curve.materials.append(wiremat);overlays.append(w)
render('qa-wireframe',(2.5,-3,2.5))
for w in overlays:bpy.data.objects.remove(w,do_unlink=True)
triangles=sum(len(o.data.loop_triangles) for o in parts);vs=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
qa=json.loads((OUT/'technical-stage.json').read_text());qa.update({'asset':ASSET,'stage':'candidate','artPassed':False,'approved':False,'triangles':triangles,'bounds_m':bounds,'final_colored_glb_roundtrip':roundtrip,'mechanism_scope':'Static editable source and GLB components; no moving part or load simulation claim.','view_count':6,'samples':{'hero':512,'qa':128},'foosball_interface':interface});qa['door_motion']={'applicable':False,'scope':'Fixed static display, no door or motion promise'};(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2))
files={}
for key,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 b=(OUT/name).read_bytes();files[key]={'path':f'assets/entertainment/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'entertainment','style':'S01-clean-geometric','title':'Fixed Indoor Table Football','description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({o.data.materials[p.material_index].name for o in parts for p in o.data.polygons}),'files':files,'status':'review','license':'All rights reserved'};(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2));print('FORMAL_CANDIDATE_COMPLETE',ASSET,triangles)
