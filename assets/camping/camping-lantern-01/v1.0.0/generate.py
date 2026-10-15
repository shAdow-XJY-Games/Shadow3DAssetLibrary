"""Original portable camping lantern. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='camping-lantern-01'
TITLE='Pinefold Carry Lantern'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(0.48,0.255,0.105,1),'sand':(0.68,0.43,0.22,1),'teal':(0.055,0.19,0.20,1)}
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
# Original A-frame geometry with genuine open entrance and closed individual panels.
def prism(name, polygon, thickness, mat):
 # Polygon is planar in any orientation; extrusion vector explicit.
 verts=list(polygon)+[tuple(Vector(v)+Vector(thickness)) for v in polygon]
 n=len(polygon);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
 faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
 me=bpy.data.meshes.new(name+' mesh');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mats[mat]);parts.append(o)
 return o
def rod(name,a,b,r,mat='sand',verts=10):
 delta=Vector(b)-Vector(a)
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=delta.length,location=(Vector(a)+Vector(b))/2)
 o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(mats[mat]);parts.append(o);return o
# Squat octagonal portable form, separate from tall harbor dock lamp.
def disc(name,radius,depth,z,mat):
 bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=radius,depth=depth,location=(0,0,z))
 o=bpy.context.object;o.name=name;o.data.materials.append(mats[mat]);parts.append(o);return o
disc('Weighted base',.145,.055,.0275,'teal')
disc('Base shoulder',.126,.035,.0725,'teal')
disc('Opaque luminous chamber',.098,.165,.1675,'sand')
disc('Top collar',.126,.028,.264,'teal')
disc('Vent shoulder',.108,.028,.292,'teal')
disc('Top cap',.077,.026,.319,'honey')
for i in range(4):
 a=math.pi/4+i*math.pi/2
 rod('Protective cage upright',(.112*math.cos(a),.112*math.sin(a),.08),(.112*math.cos(a),.112*math.sin(a),.27),.012,'honey',8)
# Carry hoop is an open arch of actual rods with rounded polygonal outline.
points=[(.13*math.cos(math.pi*i/12),0,.31+.16*math.sin(math.pi*i/12)) for i in range(13)]
for i in range(12):rod('Carry hoop segment',points[i],points[i+1],.012,'honey',6)
for x in [-.13,.13]:rod('Handle hinge',(x,-.018,.31),(x,.018,.31),.025,'sand',8)
rod('Control knob',(0,-.123,.071),(0,-.155,.071),.029,'honey',10)
# Small cap vents are dark solid inset strips, no external texture.
for i in range(4):
 a=i*math.pi/2
 box('Cap vent',(.077*math.cos(a),.077*math.sin(a),.310),(.042,.015,.010),'teal',.002,rot=a+math.pi/2)
# Recalculate outward normals consistently on closed hand-authored panels.
import bmesh
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
assert 300<=triangles<=10000,triangles
assert bounds[2]>0 and min(v.co.z for o in parts for v in o.data.vertices)>-1e-5
assert (OUT/'model.glb').stat().st_size<500000
# Geometry-only mode lets other producers finish serial render work first.
if '--geometry-only' in __import__('sys').argv:
 print('GEOMETRY_READY', triangles, bounds); raise SystemExit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False
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
for name,xyz in views.items():
 if name=='qa-wireframe':
  wiremat=bpy.data.materials.new('QA charcoal edges');wiremat.diffuse_color=(.008,.012,.015,1)
  for o in parts:
   o.data.materials.append(wiremat)
   wire=o.modifiers.new('QA edge overlay','WIREFRAME');wire.thickness=max(bounds)*.002;wire.use_replace=False;wire.offset=1;wire.material_offset=1
 point(cam,xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/camping/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'camping','style':'soft-low-poly','title':TITLE,'description':'Original squat portable camping lantern with protective cage, opaque warm chamber, cap vents, rotary knob and polygonal carry hoop. Shared matte palette; no external textures.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':3,'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'bottom center 0,0,0','transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
