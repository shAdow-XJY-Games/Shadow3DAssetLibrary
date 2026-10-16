"""Original Meadow Well Courtyard. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='village-well-courtyard-01'
TITLE='Meadow Well Courtyard'
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
box('Meadow ground tile',(0,0,.09),(5,4.5,.18),'leaf',.12)

before=len(parts)

for x in [-1,1]:
 box('Square terminal post',(x,0,.55),(.14,.16,1.1),'honey',.015)
 bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.112,radius2=0,depth=.14,location=(x,0,1.17),rotation=(0,0,math.pi/4));o=bpy.context.object;o.name='Pyramid post cap';o.data.materials.append(mats['sand']);parts.append(o)
for z in [.35,.78]:box('Continuous rail',(0,.025,z),(2,.09,.13),'honey',.012)
for i in range(9):
 x=(i-4)*.2;h=.87+(.04 if i%2==0 else 0)
 box('Rounded-top picket',(x,-.035,h/2+.12),(.115,.075,h),'sand',.026)

for obj in parts[before:]:
 obj.location.x=obj.location.x*1+0;obj.location.y=obj.location.y*1+2.0;obj.location.z=obj.location.z*1+.18
 obj.scale*= 1

before=len(parts)

# Individual closed annular stone wedges create a genuinely open bore.
for layer in range(3):
 for k in range(12):
  a=(k+layer%2*.5)*math.tau/12+.015;b=a+math.tau/12-.03;z=.02+layer*.24
  verts=[(r*math.cos(t),r*math.sin(t),zz) for zz in [z,z+.23] for r,t in [(.46,a),(.72,a),(.72,b),(.46,b)]]
  mesh=bpy.data.meshes.new('Voussoir');mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.update();o=bpy.data.objects.new('Stone course block',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(mats['stone-light' if (k+layer)%3==0 else 'stone']);parts.append(o)

def ring_mesh(name,inner,outer,z0,z1,mat,segments=24):
 verts=[(r*math.cos(i*math.tau/segments),r*math.sin(i*math.tau/segments),z) for z in [z0,z1] for r in [inner,outer] for i in range(segments)]
 faces=[];n=segments
 for i in range(n):
  j=(i+1)%n
  faces.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(mats[mat]);parts.append(o);return o
ring_mesh('Recessed continuous mortar',.48,.695,.02,.735,'stone',24)

cyl('Deep water',(0,0,.09),.455,.035,'water',24)
for x in [-.88,.88]:box('Canopy post',(x,0,1.075),(.15,.17,2.15),'honey',.018)
cyl('Windlass spindle',(0,0,1.22),.065,1.95,'sand',12,(0,math.pi/2,0))
beam('Crank',(.99,0,1.22),(.99,0,.99),.06,'iron');cyl('Crank grip',(1.09,0,.99),.055,.22,'honey',10,(0,math.pi/2,0))
cyl('Hanging rope',(0,0,.99),.018,.46,'sand',8)
ring_mesh('Open bucket staves',.115,.15,.37,.61,'honey',12)
cyl('Bucket bottom',(0,0,.38),.13,.025,'honey',12)
for x in [-.14,.14]:beam('Bucket handle side',(x,0,.58),(x,0,.76),.025,'iron')
beam('Bucket handle',( -.14,0,.76),(.14,0,.76),.025,'iron')
for x in [-.88,.88]:
 beam('Roof rafter left',(x,-.76,1.74),(x,0,2.14),.09,'honey')
 beam('Roof rafter right',(x,0,2.14),(x,.76,1.74),.09,'honey')
box('Structural ridge beam',(0,0,2.10),(1.92,.10,.14),'honey',.012)
for side in [-1,1]:
 for j in range(6):
  y=side*(j+.5)*.13;z=2.17-abs(y)*.52
  o=box('Overlapping canopy board',(0,y,z),(2.22,.155,.075),'sand' if j%2 else 'honey',.012);o.rotation_euler.x=-side*math.atan(.52)
box('Roof ridge',(0,0,2.20),(2.30,.10,.12),'honey',.022)

for obj in parts[before:]:
 obj.location.x=obj.location.x*0.85+-1.1;obj.location.y=obj.location.y*0.85+0.3;obj.location.z=obj.location.z*0.85+.18
 obj.scale*= 0.85

before=len(parts)

cyl('Tapered trunk',(0,0,.75),.15,1.5,'honey',9)
for i in range(5):
 a=i*math.tau/5;beam('Surface root',(0,0,.13),(.42*math.cos(a),.42*math.sin(a),.035),.095,'honey')
for a,b in [((0,0,.9),(-.43,.02,1.65)),((0,0,1.13),(.41,.08,1.84)),((0,0,1.25),(.02,.3,2.03))]:beam('Forked branch',a,b,.13,'honey')
ico('Left crown',(-.43,0,1.95),(.64,.60,.66),'leaf')
ico('Right crown',(.40,.04,2.07),(.65,.58,.71),'leaf-light')
ico('High crown',(-.05,.17,2.48),(.66,.60,.68),'leaf')

for obj in parts[before:]:
 obj.location.x=obj.location.x*0.85+1.25;obj.location.y=obj.location.y*0.85+0.7;obj.location.z=obj.location.z*0.85+.18
 obj.scale*= 0.85

for i in range(5):
 o=cyl('Approach stone',(i*.09-.05,-1.8+i*.38,.225),.23,.09,'stone-light',7);o.scale=(1.3,.7,1)
for x,y in [(-1.8,-1.5),(1.8,-1.2),(1.8,1.8)]:
 for j in range(3):ico('Low meadow shrub',(x+(j-1)*.16,y,.32),(.21,.18,.18),'leaf-light')
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
if '--render-only' not in sys.argv:bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(model,do_unlink=True)
# Persist clean source before adding the non-exported presentation rig.
if '--render-only' not in sys.argv:bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
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
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False
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
views={'thumbnail':(7,-9,7),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(7,-9,7)}
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
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'scene','theme':'village','style':'soft-low-poly','title':TITLE,'description':'Original compact village vignette combining a hollow stone well, orchard tree, timber fence, stepping approach and meadow shrubs on a five-metre base. Reproducible standalone generator; editable component objects.','bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len({m.name for o in parts for m in o.data.materials if m and m.name!='QA dark edges'}),'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'ground centre 0,0,0', 'assembly':{'assembly': 'Complete 5m x 4.5m static scene with ground slab. Origin at underside centre. Props remain editable as separate source objects.'},'transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
