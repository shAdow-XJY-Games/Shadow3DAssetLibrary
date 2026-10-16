"""Original Meadow Harvest Handcart. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-handcart-01'
TITLE='Meadow Harvest Handcart'
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

for y in [-.28,-.14,0,.14,.28]:box('Bed plank',(0,y,.60),(1.04,.13,.07),'sand',.012)
for y in [-.37,.37]:
 for z in [.73,.92]:box('Side slat',(0,y,z),(.97,.07,.15),'sand',.015)
for x in [-.52,.52]:
 for z in [.73,.92]:box('End slat',(x,0,z),(.07,.72,.15),'honey',.012)
 for y in [-.35,.35]:box('Corner upright',(x,y,.79),(.075,.075,.53),'honey',.012)
for y in [-.23,.23]:box('Axle bearer',(-.20,y,.49),(.16,.12,.20),'honey',.012)
cyl('Axle',(-.20,0,.36),.06,1.20,'iron',12,(math.pi/2,0,0))
for y in [-.55,.55]:
 # Each wheel is one closed annular solid; no coincident segmented end caps.
 verts=[];n=12
 for yy in [y-.0375,y+.0375]:
  for radius in [.2825,.3575]:
   verts.extend([(-.20+radius*math.sin(i*math.tau/n),yy,.36+radius*math.cos(i*math.tau/n)) for i in range(n)])
 faces=[]
 for i in range(n):
  j=(i+1)%n
  faces.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh=bpy.data.meshes.new('Continuous timber wheel rim');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Wheel rim',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(mats['honey']);parts.append(o)
 # Three full-diameter spokes replace six halves with coincident centre caps.
 for i in range(3):
  a=i*math.pi/3;dx=.29*math.sin(a);dz=.29*math.cos(a)
  beam('Wheel spoke',(-.20-dx,y,.36-dz),(-.20+dx,y,.36+dz),.045,'sand')
 cyl('Wheel hub',(-.20,y,.36),.08,.14,'iron',12,(math.pi/2,0,0))
for y in [-.25,.25]:beam('Long cart handle',(.15,y,.48),(1.48,y,.76),.075,'honey')
support=box('Standing prop',(.45,0,.30),(.075,.075,.60),'honey',.012)
# A sheared prism retains a genuinely flat bottom contact patch.
for v in support.data.vertices:v.co.x-=v.co.z/6
# Normalize minimum Z after leg splay so feet sit precisely on the ground.
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
wheel_low=min(v.co.z for o in parts if o.name.startswith('Wheel rim') for v in o.data.vertices)
support_low=min(v.co.z for v in support.data.vertices)
for v in support.data.vertices:v.co.z+=wheel_low-support_low
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
  hits+=1;origin=hit+direction*1e-7
 raise AssertionError('Ray classification did not terminate')

def validate_overlap_joint(record,objects):
 assert record['mode']=='overlap','Touch requires a separately implemented area/normal test.'
 margin=record.get('min_inside_clearance_m',.002)
 anchors=record['anchors_world_m']
 assert len(anchors)>=record.get('required_anchor_count',3),'Insufficient overlap anchors'
 if len(anchors)>1:assert max((Vector(a)-Vector(b)).length for a in anchors for b in anchors)>margin*2,'Anchors not spatially separated'
 result={'a':record['a'],'b':record['b'],'mode':'overlap','anchors_world_m':anchors,'tolerance_m':margin,'meshes':{},'passed':False}
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


# Scope is the repaired prop-to-bed joint and three ground contacts.
centre_bed=min([o for o in parts if o.name.startswith('Bed plank')],key=lambda o:abs(sum(v.co.y for v in o.data.vertices)/len(o.data.vertices)))
contact_results=[validate_overlap_joint({'a':support.name,'b':centre_bed.name,'mode':'overlap','anchors_world_m':[[.4033,-.012,.58],[.4033,0,.58],[.4033,.012,.58]],'min_inside_clearance_m':.002}, {o.name:o for o in parts})]
ground_contacts={}
for side in [-1,1]:
 wheels=[o for o in parts if o.name.startswith('Wheel rim') and sum(v.co.y for v in o.data.vertices)*side>0]
 ground_contacts['wheel_'+str(side)]=min(v.co.z for o in wheels for v in o.data.vertices)
ground_contacts['standing_prop']=min(v.co.z for v in support.data.vertices)
assert all(abs(z)<1e-6 for z in ground_contacts.values()),ground_contacts

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
joined_check=bmesh.new();joined_check.from_mesh(model.data)
bmesh.ops.remove_doubles(joined_check,verts=list(joined_check.verts),dist=1e-6)
joined_nonmanifold=sum(not e.is_manifold for e in joined_check.edges)
joined_check.free();assert joined_nonmanifold==0,('Joined export candidate nonmanifold edges',joined_nonmanifold)

bounds=[round(v,5) for v in model.dimensions]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(model,do_unlink=True)
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
 print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.world.color=(.32,.32,.32)
scene.view_settings.view_transform='AgX'
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(bounds)*1.65
focus=Vector((0,0,bounds[2]*.48))
def point(o,xyz):o.location=xyz;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),180,3),('Rim',(1,4,5),300,3)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;point(light,xyz)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview ground (not asset)'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
views={'thumbnail':(3,-4,2.8),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(3,-4,2.8)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 scene.cycles.samples=512 if name=='thumbnail' else 128
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  for o in parts:
   o.data.materials.append(wiremat)
   wire=o.modifiers.new('QA edge overlay','WIREFRAME');wire.thickness=.0025;wire.use_replace=False;wire.offset=1;wire.material_offset=1
 point(cam,xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/village/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'village','style':'soft-low-poly','title':TITLE,'description':'Original two-wheel harvest handcart with open plank bed, spoked timber wheels, metal tyres, handles and a standing support.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'ground centre 0,0,0', 'assembly':{},'joined_welded_nonmanifold_edges':joined_nonmanifold,'contact_check_scope':'repaired support joint and three ground contacts; other connections require independent review','contact_checks':contact_results,'ground_contacts_m':ground_contacts,'transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
