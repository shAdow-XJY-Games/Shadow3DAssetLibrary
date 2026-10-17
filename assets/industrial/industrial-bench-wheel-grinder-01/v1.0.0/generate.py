"""Original compact static twin-wheel bench grinder; S01 clean geometric limited palette review.
Blender 4.3.2, metres, authoring Z up, front -Y, planar base underside Z=0.
Self-contained, no source asset, library, network, texture or add-on dependency.
Run: blender -b -t 2 --python generate.py -- [--out DIRECTORY] [--render]
This is a fixed-pose game prop. No operation, material removal, anchoring, load,
manufacturability or safety certification is claimed. References set scale only.
The separate QA script imports an unchanged old worktable for context.
"""
import bpy,bmesh,math,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
ASSET='industrial-bench-wheel-grinder-01';VERSION='1.0.0'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(n,d):return ARGS[ARGS.index(n)+1] if n in ARGS else d
OUT=Path(arg('--out',str(Path(__file__).resolve().parent))).resolve();OUT.mkdir(parents=True,exist_ok=True)
if Path(__file__).resolve()!=OUT/'generate.py':(OUT/'generate.py').write_bytes(Path(__file__).resolve().read_bytes())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.context.preferences.filepaths.save_version=0
S=bpy.context.scene;S.name=ASSET+' editable limited palette source';S.unit_settings.system='METRIC';S.unit_settings.scale_length=1
S.render.engine='CYCLES';S.cycles.samples=128;S.cycles.use_denoising=False;S.render.threads_mode='FIXED';S.render.threads=4
S.render.resolution_x=896;S.render.resolution_y=896;S.render.resolution_percentage=100;S.view_settings.view_transform='AgX'
S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.24,.27,1);S.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
# Four restrained PBR materials only, no textures or external resources.
def material(n,c,metal,rough):
 m=bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=(*c,1)
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
MATS=[material('Muted teal cast body',(.18,.28,.29),.25,.70),material('Plain machined steel',(.38,.40,.40),.70,.48),material('Dark charcoal control',(.035,.040,.045),0,.80),material('Rough gray abrasive wheel',(.26,.27,.28),0,.94)]
def component_material(n):
 if 'abrasive wheel with through bore' in n:return MATS[3]
 if n=='Unlabelled recessed rocker':return MATS[2]
 if n in ('Complete planar cast base','Motor pedestal','Horizontal faceted motor housing') or any(x in n for x in ('motor end bell','inner guard web','thick C-shaped guard rim','outer guard cover')):return MATS[0]
 return MATS[1]
PARTS=[]
def fix(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();return o
def reg(o,n):
 o.name=n;o.data.name=n+' mesh';o.data.materials.append(component_material(n));o['asset_id']=ASSET;o['component_role']=n;o['fixed_display_pose']=True;PARTS.append(o);return fix(o)
def mesh(n,v,f):
 me=bpy.data.meshes.new(n+' mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);S.collection.objects.link(o);return reg(o,n)
def box(n,loc,size,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('One-segment edge chamfer','BEVEL');mod.width=bevel;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 return reg(o,n)
def cx(n,xlo,xhi,r,y=.015,z=.145,N=32):
 vs=[(x,y+r*math.cos(2*math.pi*i/N),z+r*math.sin(2*math.pi*i/N)) for x in (xlo,xhi) for i in range(N)]
 fs=[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,N+(i+1)%N,N+i) for i in range(N)]
 return mesh(n,vs,fs)
def ringx(n,xlo,xhi,ro,ri,y=.015,z=.145,N=32,deg0=0,deg1=360):
 full=abs(deg1-deg0-360)<1e-8;count=N if full else N+1
 aa=[math.radians(deg0+(deg1-deg0)*i/N) for i in range(count)]
 vs=[(x,y+r*math.cos(a),z+r*math.sin(a)) for x,r in ((xlo,ro),(xhi,ro),(xlo,ri),(xhi,ri)) for a in aa]
 fs=[]
 for i in range(N):
  j=(i+1)%count;fs.extend([(i,j,count+j,count+i),(2*count+i,3*count+i,3*count+j,2*count+j),(i,2*count+i,2*count+j,j),(count+i,count+j,3*count+j,3*count+i)])
 if not full:
  fs.extend([(0,count,3*count,2*count),(N,2*count+N,3*count+N,count+N)])
 return mesh(n,vs,fs)
def sidebox(n,sgn,xlo,xhi,ylo,yhi,zlo,zhi,bevel=0):
 return box(n,(sgn*(xlo+xhi)/2,(ylo+yhi)/2,(zlo+zhi)/2),(xhi-xlo,yhi-ylo,zhi-zlo),bevel)
def sidecx(n,sgn,xlo,xhi,r,y=.015,z=.145,N=32):return cx(n,*sorted((sgn*xlo,sgn*xhi)),r,y,z,N)
def sidering(n,sgn,xlo,xhi,ro,ri,**kw):return ringx(n,*sorted((sgn*xlo,sgn*xhi)),ro,ri,**kw)
box('Complete planar cast base',(0,.005,.013),(.240,.160,.026),.004)
box('Motor pedestal',(0,.015,.061),(.126,.090,.074),.004)
cx('Horizontal faceted motor housing',-.085,.085,.0575,N=24)
cx('Continuous coaxial spindle',-.170,.170,.00635)
for s,side in [(-1,'Left'),(1,'Right')]:
 sidecx(side+' motor end bell',s,.083,.102,.060,N=24)
 sidecx(side+' bearing neck',s,.099,.130,.017)
 # Thick side webs and 270-degree rim have the same real 90-degree front opening.
 sidering(side+' inner guard web',s,.115,.119,.086,.017,N=24,deg0=225,deg1=495)
 sidering(side+' thick C-shaped guard rim',s,.119,.174,.086,.081,N=24,deg0=225,deg1=495)
 sidering(side+' outer guard cover',s,.174,.178,.086,.012,N=24,deg0=225,deg1=495)
 # Wheel bore and continuous spindle share aligned 32-sided actual surfaces.
 sidering(side+' abrasive wheel with through bore',s,.133,.153,.075,.00635,N=32)
 sidecx(side+' inner wheel flange',s,.126,.133,.024)
 sidecx(side+' outer wheel flange',s,.153,.160,.024)
 sidecx(side+' spindle retaining nut',s,.160,.167,.010,N=6)
 # Inboard tab touches the real inner guard face below the wheel opening.
 sidebox(side+' tool-rest mounting tab',s,.109,.115,-.034,-.006,.074,.102)
 sidebox(side+' forward tool-rest bracket',s,.108,.121,-.099,-.020,.080,.090)
 sidebox(side+' tool-rest riser',s,.114,.125,-.097,-.085,.089,.115)
 sidebox(side+' horizontal tool-rest plate',s,.113,.173,-.112,-.061,.114,.120)
 # One shank crosses both mount and guard web; two raised heads are visibly seated.
 sidecx(side+' bracket fastening shank',s,.105,.123,.0035,y=-.020,z=.090,N=12)
 sidecx(side+' bracket bolt head',s,.103,.109,.007,y=-.020,z=.090,N=6)
 sidecx(side+' bracket captive nut',s,.119,.124,.0065,y=-.020,z=.090,N=6)
 # Separate upper deflector with its own seated guard tab, fixed display only.
 sidebox(side+' upper deflector mounting tab',s,.109,.115,-.027,-.011,.202,.223)
 sidebox(side+' upper deflector lip',s,.108,.164,-.050,-.014,.219,.224)
 sidecx(side+' upper deflector bolt',s,.105,.122,.003,y=-.018,z=.213,N=12)
 sidecx(side+' upper deflector bolt head',s,.103,.109,.006,y=-.018,z=.213,N=6)
 # Three outer cover fasteners at rear/lower/upper locations, no brand emblems.
 for j,ang in enumerate((0,90,270),1):
  a=math.radians(ang);sidecx(side+' outer cover screw '+str(j),s,.172,.182,.0035,y=.015+.072*math.cos(a),z=.145+.072*math.sin(a),N=8)
box('Front switch enclosure',(0,-.039,.063),(.042,.018,.039),.002)
box('Unlabelled recessed rocker',(0,-.052,.063),(.025,.008,.022),.001)
# All source components are separate, editable meshes. No reference meshes enter export.
asset=bpy.data.collections.new('Original asset parts');S.collection.children.link(asset)
for o in PARTS:
 for c in list(o.users_collection):c.objects.unlink(o)
 asset.objects.link(o)
bpy.context.view_layer.update();bpy.ops.object.select_all(action='DESELECT')
for o in PARTS:o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_materials='EXPORT')
S['review_stage']='limited palette review; final independent QA pending';S['static_asset_only']=True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Derive published counts from a real GLB import, never source assumptions.
R=bpy.data.scenes.new('Temporary actual GLB statistics');bpy.context.window.scene=R
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
rparts=[o for o in R.objects if o.type=='MESH'];vv=[o.matrix_world@v.co for o in rparts for v in o.data.vertices]
tri=0
for o in rparts:o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles)
bounds={k:float(max(v[i] for v in vv)-min(v[i] for v in vv)) for i,k in enumerate(('x','y','z'))};bounds['unit']='m'
mc=len({m.name for o in rparts for m in o.data.materials});bpy.context.window.scene=S
meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':'Original Compact Twin-Wheel Bench Grinder','description':'Original static compact horizontal twin-wheel bench grinder in a limited S01 palette. Separate planar base, pedestal, horizontal motor, coaxial spindle, bored wheels, flanges, thick open-front guards, bolted tool-rest brackets, upper deflectors and front rocker. Four restrained teal, steel, charcoal and rough gray wheel PBR materials. No movement, grinding performance, anchoring, load capacity, manufacturability, or safety certification is claimed.','bounds':bounds,'triangles':tri,'materials':mc,'status':'review','license':'All rights reserved','files':{}}
def finfo(p):return {'path':'assets/industrial/'+ASSET+'/v'+VERSION+'/'+p.name,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save_meta():
 meta['files']={k:finfo(OUT/f) for k,f in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')] if (OUT/f).exists()}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_meta()
print('BUILT',json.dumps({'parts':len(PARTS),'actual_glb_triangles':tri,'actual_glb_materials':mc,'bounds':bounds}),flush=True)
if '--render' in ARGS:
 def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0005));floor=bpy.context.object;floor.name='Render only ground'
 fm=bpy.data.materials.new('Render only charcoal ground');fm.diffuse_color=(.07,.085,.10,1);floor.data.materials.append(fm)
 for n,loc,en,size in [('Key',(.55,-.65,.90),12,.70),('Fill',(-.65,-.25,.55),7,.65),('Rim',(.25,.55,.75),14,.50)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=en;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,.12))
 bpy.ops.object.camera_add(location=(.65,-.85,.56));cam=bpy.context.object;cam.data.type='ORTHO';aim(cam,(0,0,.115));S.camera=cam
 bpy.context.view_layer.update();pp=[cam.matrix_world.inverted()@(o.matrix_world@v.co) for o in PARTS for v in o.data.vertices];lo=[min(v[i] for v in pp) for i in (0,1)];hi=[max(v[i] for v in pp) for i in (0,1)];cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*1.18;cam.location+=cam.matrix_world.to_3x3()@Vector(((hi[0]+lo[0])/2,(hi[1]+lo[1])/2,0))
 S.render.filepath=str(OUT/'thumbnail.png');bpy.ops.render.render(write_still=True);save_meta()
