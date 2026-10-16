"""Original village-gathering-corner-01. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-gathering-corner-01'
TITLE='Meadow Gathering Corner'
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

box('Village lawn',(0,0,.09),(4.6,3.5,.18),'leaf',.07)
start=len(parts)

for x in [-.65,.65]:box('Board post',(x,0,.90),(.12,.14,1.80),'honey',.012)
box('Notice panel',(0,0,1.26),(1.25,.10,.88),'teal',.012)
for z in [.83,1.69]:box('Board frame',(0,-.025,z),(1.45,.12,.09),'sand',.012)
box('Weather cap',(0,0,1.81),(1.60,.42,.12),'honey',.018)
for i,(x,z,w,h) in enumerate([(-.31,1.34,.30,.40),(.15,1.39,.30,.28),(.31,1.08,.36,.23)]):
 box('Posted notice',(x,-.055,z),(w,.025,h),'stone-light',.006)
 cyl('Notice peg',(x,-.073,z+h/2-.04),.018,.025,'iron',8,(math.pi/2,0,0))

for o in parts[start:]:o.name='Board '+o.name;o.location+=Vector((-1.1, 0.95, 0.172))
start=len(parts)

for x in [-.65,.65]:
 for y in [-.25,.25]:box('Table leg',(x,y,.37),(.11,.11,.74),'honey',.012)
 box('Table bearer',(x,0,.70),(.13,.92,.12),'honey',.012)
 box('Bench bearer',(x,0,.345),(.13,1.78,.13),'honey',.012)
 for y in [-.73,.73]:box('Bench leg',(x,y,.19),(.12,.12,.38),'honey',.012)
for y in [-.36,-.18,0,.18,.36]:box('Table top plank',(0,y,.78),(1.80,.165,.10),'sand',.012)
for side in [-1,1]:
 for y in [.64,.82]:box('Seat plank',(0,side*y,.43),(1.88,.16,.09),'sand',.012)
box('Table longitudinal brace',(0,0,.31),(1.38,.12,.11),'honey',.012)

for o in parts[start:]:o.name='Table '+o.name;o.location+=Vector((0.45, -0.35, 0.172))

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
for a,b,n in [('Board Notice panel', 'Board Board post', 2), ('Board Board frame', 'Board Board post', 2), ('Board Weather cap', 'Board Board post', 2), ('Board Posted notice', 'Board Notice panel', 1), ('Board Notice peg', 'Board Posted notice', 1), ('Table Table top plank', 'Table Table bearer', 2), ('Table Table bearer', 'Table Table leg', 2), ('Table Bench bearer', 'Table Table leg', 2), ('Table Bench bearer', 'Table Bench leg', 2), ('Table Seat plank', 'Table Bench bearer', 2), ('Table Table longitudinal brace', 'Table Bench bearer', 2), ('Board Board post', 'Village lawn', 1), ('Table Table leg', 'Village lawn', 1), ('Table Bench leg', 'Village lawn', 1)]:contact_results+=link_roles(role(a),role(b),n)
roots=role('Village lawn')
ground_results=[check_ground_patch(o) for o in roots]
support_graph=validate_support_graph([o.name for o in parts],contact_results,[o.name for o in roots],{})

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
joined_bad=sum(not e.is_manifold for e in joined.edges);joined.free();assert joined_bad==0,('Joined candidate',joined_bad)
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
 report_dir=OUT.parent/'preflight';report_dir.mkdir(exist_ok=True)
 (report_dir/(ASSET+'.json')).write_text(json.dumps({'asset':ASSET,'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':ground_results,'joined_welded_nonmanifold_edges':joined_bad},indent=2)+'\n')
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
views={'thumbnail':(7,-9,7),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(7,-9,7)}
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
meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'village','style':'soft-low-poly','title':TITLE,'description':'Original compact village meeting scene with a picnic table, public noticeboard and rounded grass base. Separate editable source parts and a single self-contained export.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'ground centre 0,0,0', 'assembly':{'assembly': 'Standalone grounded asset; scene origin is grass-base underside centre.'},'contact_checks':contact_results,'support_graph':support_graph,'ground_patch_checks':ground_results,'transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
