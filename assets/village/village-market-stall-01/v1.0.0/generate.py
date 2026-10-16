"""Original Meadow Produce Stall. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-market-stall-01'
TITLE='Meadow Produce Stall'
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

for x in [-.9,.9]:
 for y in [-.5,.5]:box('Canopy upright',(x,y,1.05),(.105,.105,2.1),'honey',.015)
for y in [-.5,.5]:box('Roof crossbeam',(0,y,2.02),(1.98,.11,.14),'honey',.018)
for side in [-1,1]:
 for i in range(8):
  x=(i-3.5)*.25;o=box('Canopy stripe',(x,side*.34,2.19),( .245,.78,.07),'teal' if i%2 else 'stone-light',.012);o.rotation_euler.x=-side*.25
for x in [-.9,.9]:
 beam('Left canopy rafter',(x,-.72,2.04),(x,0,2.235),.08,'honey')
 beam('Right canopy rafter',(x,0,2.235),(x,.72,2.04),.08,'honey')
box('Ridge beam',(0,0,2.30),(2.12,.09,.10),'honey',.018)
box('Display counter',(0,-.25,.90),(1.85,.65,.10),'sand',.02)
for z in [.27,.46,.65]:box('Front fascia',(0,-.54,z),(1.85,.065,.16),'honey',.012)
for x in [-.46,.46]:
 box('Tray bottom',(x,-.25,.98),(.75,.48,.06),'honey',.01)
 for y in [-.49,-.01]:box('Tray rail',(x,y,1.05),(.715,.045,.12),'sand',.01)
 for xx in [x-.38,x+.38]:box('Tray end',(xx,-.25,1.05),(.045,.48,.12),'sand',.01)
 for j in range(3):
  for k in range(2):ico('Fresh produce',(x+(j-1)*.20,-.25+(k-.5)*.19,1.09),(.09,.08,.09),'leaf-light' if x<0 else 'sand')
# Normalize minimum Z after leg splay so feet sit precisely on the ground.
for o in parts:
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
low=min(v.co.z for o in parts for v in o.data.vertices)
for o in parts:
 for v in o.data.vertices:v.co.z-=low
# Normalize winding per closed component before export.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
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
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'village','style':'soft-low-poly','title':TITLE,'description':'Original open market stall with pitched striped timber canopy, front display counter and two divided produce trays. Walk-in access at rear.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'ground centre 0,0,0', 'assembly':{},'transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
