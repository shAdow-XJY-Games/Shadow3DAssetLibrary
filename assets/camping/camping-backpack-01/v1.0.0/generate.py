"""Original hiking backpack. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='camping-backpack-01'
TITLE='Pinefold Trail Pack'
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
def profile(name,rings,mat,n=16):
 vs=[]
 for z,w,d in rings:
  for i in range(n):
   a=2*math.pi*i/n;c=math.cos(a);s=math.sin(a)
   vs.append((w*math.copysign(abs(c)**.55,c),d*math.copysign(abs(s)**.55,s),z))
 fs=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 me=bpy.data.meshes.new(name+' mesh');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mats[mat]);parts.append(o);return o
profile('Tapered pack body',[(0,.155,.09),(.04,.205,.135),(.47,.19,.13),(.57,.165,.10)],'teal')
box('Folded rolltop',(0,0,.585),(.40,.18,.09),'teal',.025)
box('Front storage pocket',(0,-.146,.235),(.30,.075,.25),'sand',.027)
for x in [-.135,.135]:
 box('Front webbing strap',(x,-.116,.405),(.029,.024,.26),'honey',.005)
 box('Strap buckle',(x,-.16,.34),(.055,.024,.04),'sand',.006)
 rod('Rolltop strap fold',(x,-.116,.53),(x,-.075,.59),.017,'honey',6)
 # Four connected strap sections describe a real shoulder loop behind the pack.
 points=[(x,.12,.51),(x,.21,.47),(x,.25,.30),(x,.20,.13),(x,.12,.09)]
 for i in range(len(points)-1):
  ob=rod('Shoulder strap',points[i],points[i+1],.025,'honey',6)
 for point in points[1:-1]:
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.025,location=point)
  o=bpy.context.object;o.name='Shoulder strap corner';o.data.materials.append(mats['honey']);parts.append(o)
for x in [-.216,.216]:
 box('Side pouch',(x,0,.22),(.075,.19,.21),'sand',.023)
 rod('Pouch mouth piping',(x,-.075,.325),(x,.075,.325),.012,'honey',8)
# Short top carry handle stands clear of the rolled mouth.
for x in [-.065,.065]:rod('Carry handle leg',(x,.015,.62),(x,.015,.68),.014,'honey',8)
rod('Carry handle',(-.065,.015,.68),(.065,.015,.68),.014,'honey',8)
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
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'prop','theme':'camping','style':'soft-low-poly','title':TITLE,'description':'Original tapered hiking backpack with rolltop, front pocket, paired buckles, side pouches, open shoulder loops and top carry handle. Shared matte palette; no external textures.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':3,'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'bottom center 0,0,0','transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
