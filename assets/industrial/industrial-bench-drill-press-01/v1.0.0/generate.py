"""Original medium static workshop bench drill press, S01-clean-geometric.
Blender 4.3.2. Metres, Z-up authoring, ground datum is the planar base underside.
Self-contained asset generation: no old asset, library, network or add-on dependency.
Use: blender -b -t 2 --python generate.py -- [--out DIRECTORY] [--render]
Limited colors were approved after gray review; final QA is still pending. This is a static game prop;
no motion, drill performance, clamp suitability, force or safety rating is claimed.
External old worktable/vise are only imported by the separate QA scene script.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
ASSET='industrial-bench-drill-press-01'
VERSION='1.0.0'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(name, default):
 return ARGS[ARGS.index(name)+1] if name in ARGS else default
OUT=Path(arg('--out', str(Path(__file__).resolve().parent))).resolve()
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for datablock in list(bpy.data.materials): bpy.data.materials.remove(datablock)
bpy.context.preferences.filepaths.save_version=0
SCENE=bpy.context.scene
SCENE.name=ASSET+' source'
SCENE.unit_settings.system='METRIC';SCENE.unit_settings.scale_length=1.0
SCENE.render.engine='CYCLES';SCENE.cycles.samples=96
SCENE.cycles.use_denoising=False;SCENE.render.threads_mode='FIXED';SCENE.render.threads=2
SCENE.render.resolution_x=768;SCENE.render.resolution_y=768;SCENE.render.resolution_percentage=100
SCENE.world.use_nodes=True;SCENE.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.20,.22,.25,1);SCENE.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;SCENE.view_settings.view_transform='AgX'
PARTS=[]
def material(name, color, metal, rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1)
 n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough
 return m
# Limited palette approved after parent and independent gray visual review.
MATS=[material('Muted teal cast body',(.18,.28,.29),.25,.70),material('Plain machined steel',(.38,.40,.40),.70,.48),material('Dark charcoal controls',(.035,.040,.045),0,.80)]
def register(o,name,slot):
 o.name=name;o.data.name=name+' mesh';o.data.materials.append(MATS[slot]);PARTS.append(o);return o

def repair(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();return o

def mesh(name, verts, faces, slot=0):
 me=bpy.data.meshes.new(name+' mesh');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);SCENE.collection.objects.link(o);register(o,name,slot);return repair(o)

def box(name,loc,size,slot=0,bevel=.003):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Single chamfer', 'BEVEL');mod.width=bevel;mod.segments=1
  bpy.ops.object.modifier_apply(modifier=mod.name)
 return repair(register(o,name,slot))

def cylinder(name,loc,r,depth,slot=1,axis='Z',n=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=depth,location=loc)
 o=bpy.context.object
 if axis=='X':o.rotation_euler[1]=math.pi/2
 elif axis=='Y':o.rotation_euler[0]=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 return repair(register(o,name,slot))

def ring(name,xy,ro,ri,zlo,zhi,slot=0,n=16):
 angles=[2*math.pi*i/n for i in range(n)]
 rings=[[(xy[0]+r*math.cos(a),xy[1]+r*math.sin(a),z) for a in angles] for z,r in [(zlo,ro),(zhi,ro),(zlo,ri),(zhi,ri)]]
 vs=sum(rings,[]);fs=[]
 for i in range(n):
  j=(i+1)%n
  fs += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(n+i,n+j,3*n+j,3*n+i),(i,2*n+i,2*n+j,j)]
 return mesh(name,vs,fs,slot)

def tapered(name,xy,sections,slot=1,n=16):
 vs=[(xy[0]+r*math.cos(2*math.pi*i/n),xy[1]+r*math.sin(2*math.pi*i/n),z) for z,r in sections for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((len(sections)-1)*n+i for i in range(n))]
 for k in range(len(sections)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return mesh(name,vs,fs,slot)

def rod(name,a,b,r,slot=1,n=10):
 a,b=Vector(a),Vector(b);delta=b-a;o=cylinder(name,(a+b)/2,r,delta.length,slot,n=n)
 o.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
 bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o

def table_with_bore():
 # A complete extruded chamfered rectangular ring, with an actual open-through center.
 outline=[(-.095,-.100),(-.105,-.090),(-.105,-.035),(-.105,.035),(-.105,.090),(-.095,.100),(-.035,.100),(.035,.100),(.095,.100),(.105,.090),(.105,.035),(.105,-.035),(.105,-.090),(.095,-.100),(.035,-.100),(-.035,-.100)]
 outline.sort(key=lambda p:math.atan2(p[1],p[0]));n=len(outline);xy=(0,-.082)
 inner=[(.014*math.cos(math.atan2(y,x)),.014*math.sin(math.atan2(y,x))) for x,y in outline]
 vs=[(x+xy[0],y+xy[1],z) for z,pts in [(.309,outline),(.334,outline),(.309,inner),(.334,inner)] for x,y in pts];fs=[]
 for i in range(n):
  j=(i+1)%n;fs += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(n+i,n+j,3*n+j,3*n+i),(i,2*n+i,2*n+j,j)]
 return mesh('Working table with through bore',vs,fs,1)

box('Planar cast base',(0,-.015,.019),(.250,.350,.038),0,.006)
cylinder('Column foot socket',(0,.100,.053),.045,.040,0)
cylinder('Rear steel column',(0,.100,.350),.026,.592,1)
ring('Height collar sleeve',(0,.100),.043,.026,.284,.344,0)
box('Table support arm',(0,.0075,.300),(.068,.125,.026),0,.003)
table_with_bore()
# Side lock lever on the sleeve, connected but static, with no kinematic claim.
cylinder('Table lock screw',( .050,.100,.314),.009,.030,1,'X',12)
rod('Table lock lever',(.063,.100,.314),(.063,.132,.266),.006,2)
cylinder('Table tilt pivot cap',(0,-.015,.298),.016,.078,0,'X',12)
ring('Head column sleeve',(0,.100),.043,.026,.580,.650,0)
box('Main head casting',(0,-.0385,.620),(.140,.217,.108),0,.007)
box('Closed belt cover',(0,.040,.698),(.158,.414,.054),0,.009)
box('Rear motor mounting bridge',(0,.157,.611),(.058,.056,.055),0,.003)
cylinder('Faceted rear motor',(0,.192,.599),.047,.150,0)
cylinder('Motor lower end cap',(0,.192,.528),.049,.014,1)
cylinder('Motor upper end cap',(0,.192,.675),.049,.018,1)
# Quill bearing is visibly seated in the head, not floating under it.
cylinder('Lower quill bearing',(0,-.082,.570),.026,.052,0)
cylinder('Exposed quill',(0,-.082,.530),.016,.072,1)
cylinder('Chuck upper collar',(0,-.082,.499),.024,.020,1)
tapered('Faceted chuck body',(0,-.082),[(.459,.018),(.470,.028),(.492,.028)],1,16)
cylinder('Chuck lower jaw collar',(0,-.082,.460),.018,.012,2)
# Single closed low-poly two-flute fixed bit. Flutes are geometry, not a texture.
N=12;zs=[.414,.424,.434,.444,.454,.469];vs=[(0,-.082,.405)];fs=[]
for z in zs:
 twist=(z-.414)/.040*math.pi*1.5
 for i in range(N):
  a=2*math.pi*i/N;rad=(.0045 if i%6 in (0,1,2) else .0027) if z<.454 else .0045
  vs.append((rad*math.cos(a+twist),-.082+rad*math.sin(a+twist),z))
for i in range(N):fs.append((0,1+(i+1)%N,1+i))
for k in range(len(zs)-1):
 for i in range(N):j=(i+1)%N;fs.append((1+k*N+i,1+k*N+j,1+(k+1)*N+j,1+(k+1)*N+i))
fs.append(tuple(1+(len(zs)-1)*N+i for i in range(N)))
mesh('Fixed fluted drill bit',vs,fs,1)
# Three-radial-spoke manual feed handle at the right of the head.
hub=(.095,-.065,.610)
cylinder('Feed handle hub',hub,.025,.056,1,'X',12)
for index,degrees in enumerate((-35,85,205),1):
 a=math.radians(degrees);start=(.116,hub[1]+.017*math.sin(a),hub[2]+.017*math.cos(a));end=(.116,hub[1]+.105*math.sin(a),hub[2]+.105*math.cos(a))
 rod('Feed spoke '+str(index),start,end,.0055,1)
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.017,location=end)
 register(bpy.context.object,'Feed grip '+str(index),2)
box('Switch enclosure',(-.035,-.151,.620),(.042,.018,.047),2,.003)
box('Single unlabelled rocker',(-.035,-.162,.620),(.024,.010,.025),1,.002)

# All meshes remain independent and editable. No hidden diagnostic objects.
for o in PARTS:
 repair(o);o['asset_id']=ASSET;o['component_role']=o.name;o['static_pose']=True
bpy.context.view_layer.update()
asset_collection=bpy.data.collections.new('Asset geometry: '+ASSET);SCENE.collection.children.link(asset_collection)
for o in PARTS:
 for c in list(o.users_collection):c.objects.unlink(o)
 asset_collection.objects.link(o)
bpy.ops.object.select_all(action='DESELECT')
for o in PARTS:o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=False,export_yup=True,export_extras=True,export_materials='EXPORT',export_animations=False)
SCENE['asset_id']=ASSET;SCENE['review_stage']='limited palette review; final QA pending';SCENE['static_asset_only']=True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))

def fileinfo(path,key):
 return {'path':'assets/industrial/'+ASSET+'/v'+VERSION+'/'+path.name,'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
world=[o.matrix_world@v.co for o in PARTS for v in o.data.vertices]
bounds={key:float(max(v[i] for v in world)-min(v[i] for v in world)) for i,key in enumerate(('x','y','z'))};bounds['unit']='m'
triangles=0
for o in PARTS:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':'Original Medium Bench Drill Press','description':'Original static workshop bench drill press with a planar cast base, rear steel column, bored adjustable-height table, separate support arm and sleeves, quill and chuck, fixed fluted bit, enclosed belt cover, rear motor, and three-spoke feed handle. Limited teal, steel and charcoal palette. Independent closed editable parts in one fixed pose. No anchoring system has been supplied or certified. No motion, drilling performance, load capacity, workholding suitability, or safety certification is claimed.','bounds':bounds,'triangles':triangles,'materials':len(MATS),'components':len(PARTS),'status':'review','review':{'gray_geometry':'pending independent review','artPassed':False,'formal_approved':False,'paletteApplied':False},'license':'All rights reserved','authoring':{'unit':'m','upAxis':'Z','exportUpAxis':'Y','origin':'centered X=0, base underside Z=0; front is -Y','staticPose':True,'dimensionsAreOriginal':True},'installation':{'reference':'Unscaled interior-open-worktable-01/v1.0.0','translation_m':[.24,.02,.90],'rotation_degrees':[0,0,0],'scale':[1,1,1],'adjacentViseTranslation_m':[-.28,-.30,.74],'note':'Vise is an adjacent reused tool only. It is not mounted to the drill table and no safe drilling grip is claimed.'},'files':{}}
for fname,key in [('model.glb','glb'),('source.blend','blend'),('generate.py','generator'),('thumbnail.png','render')]:
 path=OUT/fname
 if path.exists():meta['files'][key]=fileinfo(path,key)
for key in ('components','review','authoring','installation'):meta.pop(key,None)
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print('BUILT',json.dumps({'id':ASSET,'parts':len(PARTS),'triangles':triangles,'bounds':bounds,'out':str(OUT)}),flush=True)

if '--render' in ARGS:
 def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));floor=bpy.context.object;floor.name='Render only backdrop';floor.data.materials.append(material('Backdrop',(.10,.12,.15),0,.9))
 for name,loc,energy,size in [('Key',(.8,-1.2,1.5),35,1.1),('Fill',(-.9,-.3,.9),20,1.0),('Rim',(.4,.9,1.3),40,.8)]:
  bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.name=name;light.data.energy=energy;light.data.shape='DISK';light.data.size=size;aim(light,(0,0,.4))
 bpy.ops.object.camera_add(location=(1.08,-1.48,1.02));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=.93;aim(cam,(0,.015,.375));SCENE.camera=cam
 bpy.context.view_layer.update();projected=[cam.matrix_world.inverted()@(o.matrix_world@v.co) for o in PARTS for v in o.data.vertices];lo=[min(v[i] for v in projected) for i in (0,1)];hi=[max(v[i] for v in projected) for i in (0,1)];cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*1.16;cam.location+=cam.matrix_world.to_3x3()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0))
 SCENE.render.filepath=str(OUT/'thumbnail.png');bpy.ops.render.render(write_still=True)
 meta['files']['render']=fileinfo(OUT/'thumbnail.png','render');(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
