"""Original mobile single-stage workshop dust collector, S01-clean-geometric.
Blender 4.3.2. Metres, author Z-up, front -Y. Self-contained: no downloaded
model, source asset, texture, network, add-on or external Python dependency.
Default: blender -b -t 2 --python generate.py -- --out DIRECTORY
The default clean single-file entry produces all five core files with one
thumbnail. --final --views DIR adds five orthographic views (six total).
--geometry-only (alias --no-render) writes PBR GLB/native source only, with
no PNG or metadata, and never claims the full five-file package was rebuilt.
--gray --geometry-only explicitly selects gray build, with no complete metadata.
--preview DIRECTORY renders one limited-PBR image without final thumbnail/meta.
--view NAME --view-out DIRECTORY renders any one of isometric/front/back/left/
right/top directly from this file, with GLB/native source but no final metadata.
No external helper is needed to reproduce the six approved camera directions.
Optional --expected-glb-sha HASH halts before any image if the actual fresh
export differs from the caller's pinned reviewed geometry/material binary.
All images use fixed 128 Cycles samples, no adaptive sampling or denoising.
Official exact-model scale/structure references, read 2026-10-17:
https://www.grizzly.com/products/grizzly-1-hp-canister-dust-collector/g0583z
https://cdn0.grizzly.com/specsheets/g0583z_ds.pdf (Model G0583Z, 2026-10-04)
https://cdn0.grizzly.com/manuals/g0583z_m.pdf (G0583Z since 9/11; 9/12 update)
https://www.grizzly.com/products/g0583z/parts
References inform scale and assembly class only. Original authored arrangement,
proportions, panel pattern and muted S01 palette; no logo or branded replica.
Author dimensions (m): base .640 x .360 x .022 at Z=.105-.127; caster wheel
OD=.070 / width=.024 / axle OD=.012; collector center X=-.130 Y=0, plenum
OD=.348 / ID=.328 / Z=.724-.830; filter visual OD=.340 / body H=.506;
independent opaque bag max OD about .322 / Z=.226-.700; blower radial shell
OD=.256 / Y=-.062..+.062, center X=.205 Z=.755; motor Y=.062..+.200.
Bare intake end center (.205,-.205,.755), outward axis (0,-1,0). The authored
64-sided bore vertex-circle diameter is .1016m; its actual across-flat clear
diameter is about .10147756m (101.47756mm), not a circular .1016m bore.
straight barrel OD=.1116, unobstructed axial barrel length=.143, barrel Y=-.205
..-.062, rolled outer lip OD=.118 for Y=-.205..-.196. These are authored mesh
parameters, not manufacturer connector dimensions; no hose/adapter fit certified.
The constant-OD exterior land is Y=-.196..-.068 (.128m), excluding the rolled
lip and front-cover insertion; .143m is barrel depth, not certified engagement.
Transfer-throat author center Z=.770m, a 15mm offset above the blower axis.
Hollow chamber path is visible geometry: bare inlet -> hollow blower casing ->
short hollow rectangular side throat -> open top/bottom collector plenum ->
upper hollow pleated filter / separate open-top, closed-bottom opaque bag.
The internal rotor, motor internals, filter pores and bag contents are deliberately
omitted; static exterior prop only. No airflow, collection, filtration, health,
explosion protection, load, operation, manufacturing or safety claim is made.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
ASSET='industrial-workshop-dust-collector-01'; VERSION='1.0.0'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(n,d): return ARGS[ARGS.index(n)+1] if n in ARGS else d
OUT=Path(arg('--out',str(Path(__file__).resolve().parent))).resolve();OUT.mkdir(parents=True,exist_ok=True)
if Path(__file__).resolve()!=OUT/'generate.py':(OUT/'generate.py').write_bytes(Path(__file__).resolve().read_bytes())
GRAY='--gray' in ARGS; SINGLE_VIEW=arg('--view',''); FINAL='--final' in ARGS or not any(x in ARGS for x in ('--gray','--geometry-only','--no-render','--preview','--view'))
VIEW_SPECS={'isometric':(2.8,-4,2.5),'front':(0,-4,.70),'back':(0,4,.70),'left':(-4,0,.70),'right':(4,0,.70),'top':(0,-.01,4)}
if '--final' in ARGS and any(x in ARGS for x in ('--no-render','--geometry-only')):raise SystemExit('Choose --final or no-render mode, not both.')
if SINGLE_VIEW and SINGLE_VIEW not in VIEW_SPECS:raise SystemExit('--view must be one of '+', '.join(VIEW_SPECS))
RENDER_RECORDS=[]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.context.preferences.filepaths.save_version=0
S=bpy.context.scene;S.name=ASSET+' editable static source';S.unit_settings.system='METRIC';S.unit_settings.scale_length=1
S.render.engine='CYCLES';S.cycles.samples=128;S.cycles.use_denoising=False;S.cycles.use_adaptive_sampling=False;S.use_nodes=False;S.render.use_compositing=False;S.render.use_sequencer=False;S.render.image_settings.file_format='PNG';S.render.threads_mode='FIXED';S.render.threads=4
S.render.resolution_x=896;S.render.resolution_y=896;S.render.resolution_percentage=100;S.view_settings.view_transform='AgX'
S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.24,.27,1);S.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
PALETTE=[('Muted teal coated steel',(.18,.28,.29),.25,.70),('Plain satin steel',(.38,.40,.40),.70,.48),('Charcoal tire and grip',(.035,.040,.045),0,.80),('Warm pale filter and opaque bag',(.59,.57,.50),0,.90)]
MATS=[]
for n,c,m,r in PALETTE:
 mat=bpy.data.materials.new('Gray geometry' if GRAY else n);mat.use_nodes=True;mat.diffuse_color=(*((.42,.43,.44) if GRAY else c),1)
 p=mat.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=mat.diffuse_color;p.inputs['Metallic'].default_value=0 if GRAY else m;p.inputs['Roughness'].default_value=.72 if GRAY else r;MATS.append(mat)
PARTS=[]
def fix(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();return o
def reg(o,n,slot=0,role=None):
 o.name=n;o.data.name=n+' mesh';o.data.materials.append(MATS[slot]);o['asset_id']=ASSET;o['component_role']=role or n;o['static_display_pose']=True;PARTS.append(o);return fix(o)
def mesh(n,v,f,slot=0,role=None):
 me=bpy.data.meshes.new(n+' mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);S.collection.objects.link(o);return reg(o,n,slot,role)
def box(n,loc,size,slot=0,bevel=0,role=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Small single chamfer','BEVEL');mod.width=bevel;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 return reg(o,n,slot,role)
def cyl(n,loc,r,depth,slot=1,axis='Z',N=32,role=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=N,radius=r,depth=depth,location=loc);o=bpy.context.object
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 if axis=='X':o.rotation_euler[1]=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return reg(o,n,slot,role)
def axispoint(axis,t,u,v,c):
 if axis=='Z':return(c[0]+u,c[1]+v,t)
 if axis=='Y':return(c[0]+u,t,c[2]+v)
 return(t,c[1]+u,c[2]+v)
def ring(n,axis,c,t0,t1,ro,ri,slot=1,N=64,role=None):
 v=[axispoint(axis,t,r*math.cos(2*math.pi*i/N),r*math.sin(2*math.pi*i/N),c) for t,r in ((t0,ro),(t1,ro),(t0,ri),(t1,ri)) for i in range(N)];f=[]
 for i in range(N):
  j=(i+1)%N;f.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 return mesh(n,v,f,slot,role)
def rod(n,a,b,r,slot=1,N=16,role=None):
 a,b=Vector(a),Vector(b);o=cyl(n,(a+b)/2,r,(b-a).length,slot,N=N,role=role);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o
def cutbox(o,n,loc,size):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);c=bpy.context.object;c.name=n;c.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new(n,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True);fix(o)
def cutcylinder(o,n,loc,r,depth,axis='X'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc);c=bpy.context.object;c.name=n
 if axis=='X':c.rotation_euler[1]=math.pi/2
 if axis=='Y':c.rotation_euler[0]=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new(n,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True);fix(o)
def rectangular_throat(n,x0,x1,yo,zo,yi,zi,zcenter):
 loops=[[(x,-y,zcenter-z),(x,y,zcenter-z),(x,y,zcenter+z),(x,-y,zcenter+z)] for x,y,z in ((x0,yo,zo),(x1,yo,zo),(x0,yi,zi),(x1,yi,zi))];v=sum(loops,[]);f=[]
 for i in range(4):
  j=(i+1)%4;f.extend([(i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)])
 return mesh(n,v,f,0,'open_transfer_throat')
# Fixed polygonal axle/bore surfaces have zero-gap contact at aligned vertices;
# this is not a dynamic rolling or manufacturing-clearance representation.
# Four identical fixed-pose swivel casters. Circular mesh tangent edges at Z=0
# are line contacts, not positive-area floor pads or a stability certification.
for k,(x,y) in enumerate([(-.267,-.140),(.267,-.140),(-.267,.140),(.267,.140)],1):
 root='Caster '+str(k)+' '
 ring(root+'bored tire','X',(0,y,.035),x-.012,x+.012,.035,.006,2,32,'ground_wheel')
 cyl(root+'continuous axle',(x,y,.035),.006,.048,1,'X',16,'caster_axle')
 for sign,label in [(-1,'left'),(1,'right')]:
  fork=box(root+label+' fork plate',(x+sign*.018,y,.0535),(.006,.030,.059),1,role='caster_fork')
  cutcylinder(fork,root+label+' true axle bore',(x+sign*.018,y,.035),.0061,.018)
  cyl(root+label+' seated axle head',(x+sign*.0235,y,.035),.008,.005,1,'X',6,'caster_axle_head')
 box(root+'fork bridge',(x,y,.080),(.042,.030,.010),1,role='caster_fork')
 cyl(root+'swivel stem',(x,y,.094),.010,.026,1,N=24,role='caster_stem')
 cyl(root+'swivel mounting plate',(x,y,.103),.023,.010,1,N=24,role='caster_mount')
 cyl(root+'base fastening shank',(x,y,.117),.004,.038,1,N=12,role='caster_base_fastener')
 cyl(root+'base fastening head',(x,y,.130),.008,.006,1,N=6,role='caster_base_fastener')
base=box('Chamfered mobile steel base',(0,0,.116),(.640,.360,.022),0,.010,'base')
for y,side in [(-.140,'Front'),(.140,'Rear')]:
 box(side+' steel collector support',(-.294,y,.423),(.025,.025,.604),0,role='collector_support')
 box(side+' collector rim mounting tab',(-.2665,y,.730),(.080,.034,.024),1,role='collector_mount')
 cyl(side+' collector mount bolt',(-.294,y,.746),.006,.008,1,N=6,role='collector_mount')
 cyl(side+' collector mount shank',(-.294,y,.731),.0035,.028,1,N=16,role='collector_mount')
box('Blower support upright',(.238,.112,.372),(.028,.028,.502),0,role='blower_support')
box('Motor transverse saddle',(.238,.113,.633),(.128,.070,.026),1,role='blower_mount')
for y in (.080,.150):box('Motor saddle riser '+str(y),(.205,y,.674),(.060,.022,.074),1,role='blower_mount')
plenum=ring('Open top bottom collector plenum','Z',(-.130,0,0),.724,.830,.174,.164,0,64,'collector_plenum')
cutbox(plenum,'Real collector side throat opening',(.074,0,.770),(.120,.078,.054))
blower=ring('Hollow blower radial shell','Y',(.205,0,.755),-.062,.062,.128,.118,0,64,'blower_shell')
cutbox(blower,'Real blower radial throat opening',(.070,0,.770),(.110,.078,.054))
ring('Blower front annular cover','Y',(.205,0,.755),-.068,-.058,.128,.0508,0,64,'blower_front')
cyl('Blower closed rear cover',(.205,.063,.755),.128,.012,0,'Y',64,'blower_rear')
rectangular_throat('Hollow side transfer throat',.024,.116,.046,.035,.039,.027,.770)
ring('Bare inlet straight tube','Y',(.205,0,.755),-.205,-.062,.0558,.0508,1,64,'inlet_tube')
ring('Inlet rolled outer lip','Y',(.205,0,.755),-.205,-.196,.059,.0556,1,64,'inlet_lip')
for a in (45,135,225,315):
 t=math.radians(a);cyl('Blower cover seated screw '+str(a),(.205+.114*math.cos(t),-.073,.755+.114*math.sin(t)),.0035,.012,1,'Y',8,'blower_fastener')
cyl('Motor bearing end bell',(.205,.080,.755),.074,.034,0,'Y',32,'motor')
cyl('Faceted motor sealed housing',(.205,.138,.755),.065,.116,0,'Y',24,'motor')
cyl('Motor rear cap',(.205,.194,.755),.068,.012,0,'Y',24,'motor')
for a in (0,45,90,135,180,225,315):
 t=math.radians(a);rod('Motor longitudinal cooling rib '+str(a),(.205+.065*math.cos(t),.093,.755+.065*math.sin(t)),(.205+.065*math.cos(t),.181,.755+.065*math.sin(t)),.0035,1,8,'motor_detail')
box('Motor plain control enclosure',(.278,.116,.800),(.042,.054,.053),0,.003,'control')
box('Unlabelled rocker',(.3025,.116,.800),(.009,.030,.032),2,.001,'control')
# Independent opaque hollow bag, true open top and thin closed rounded bottom.
N=64;profile=[(.226,.045),(.238,.112),(.260,.145),(.300,.157),(.390,.161),(.510,.158),(.610,.161),(.664,.158),(.700,.160)]
vs=[]
for inner in (False,True):
 for j,(z,r) in enumerate(profile):
  for i in range(N):
   a=2*math.pi*i/N;fold=(.0018*math.cos(8*a)+.0008*math.sin(5*a))*(0 if j in (0,len(profile)-1) else 1)
   rr=r+fold-(.003 if inner else 0);zz=z+(.003 if inner and j==0 else 0);vs.append((-.130+rr*math.cos(a),rr*math.sin(a),zz))
fs=[];L=len(profile);K=N*L
for j in range(L-1):
 for i in range(N):
  q=(i+1)%N;a=j*N+i;b=j*N+q;c=(j+1)*N+q;d=(j+1)*N+i;fs.extend([(a,b,c,d),(K+a,K+d,K+c,K+b)])
fs.extend([tuple(reversed(range(N))),tuple(K+i for i in range(N))])
for i in range(N):q=(i+1)%N;a=(L-1)*N+i;b=(L-1)*N+q;fs.append((a,b,K+b,K+a))
mesh('Independent open top opaque collection bag',vs,fs,3,'collection_bag')
# A short original stepped hollow neck exposes the bag clamp below the plenum.
profile=[(.672,.157,.151),(.704,.157,.151),(.715,.174,.164),(.724,.174,.164)];N=64;vs=[]
for inner in (False,True):
 for z,ro,ri in profile:
  for i in range(N):
   a=2*math.pi*i/N;r=ri if inner else ro;vs.append((-.130+r*math.cos(a),r*math.sin(a),z))
fs=[];K=len(profile)*N
for j in range(len(profile)-1):
 for i in range(N):
  q=(i+1)%N;a=j*N+i;b=j*N+q;c=(j+1)*N+q;d=(j+1)*N+i;fs.extend([(a,b,c,d),(K+a,K+d,K+c,K+b)])
for i in range(N):
 q=(i+1)%N;fs.extend([(i,K+i,K+q,q),((len(profile)-1)*N+i,(len(profile)-1)*N+q,K+(len(profile)-1)*N+q,K+(len(profile)-1)*N+i)])
mesh('Lower bag connecting collar',vs,fs,0,'bag_collar')
ring('Lower bag retaining clamp','Z',(-.130,0,0),.686,.704,.169,.1598,1,64,'bag_clamp')
ring('Upper filter connecting collar','Z',(-.130,0,0),.830,.852,.174,.157,0,64,'filter_collar')
ring('Upper filter retaining clamp','Z',(-.130,0,0),.826,.846,.183,.1738,1,64,'filter_clamp')
for z,label,clamp_ro in [(.695,'Lower bag',.169),(.836,'Upper filter',.183)]:
 box(label+' clamp latch seat',(-.130,-clamp_ro-.007,z),(.040,.018,.019),1,.002,'clamp_latch')
 rod(label+' clamp toggle bar',(-.145,-clamp_ro-.020,z),(-.112,-clamp_ro-.020,z),.004,1,12,'clamp_latch')
 for x in (-.145,-.112):rod(label+' clamp latch hinge '+str(x),(x,-clamp_ro-.018,z),(x,-clamp_ro+.001,z),.003,1,12,'clamp_latch')
N=96;vs=[]
for z,inner in ((.848,False),(1.354,False),(.848,True),(1.354,True)):
 for i in range(N):
  a=2*math.pi*i/N;r=(.170 if i%2==0 else .162)-(.004 if inner else 0);vs.append((-.130+r*math.cos(a),r*math.sin(a),z))
fs=[]
for i in range(N):
 j=(i+1)%N;fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
mesh('Hollow pleated upper filter',vs,fs,3,'filter_wall')
ring('Filter upper retaining rim','Z',(-.130,0,0),1.344,1.365,.176,.157,1,64,'filter_rim')
cyl('Filter sealed top cap',(-.130,0,1.362),.177,.012,0,N=64,role='filter_cap')
for x in (-.175,-.085):cyl('Top cap grip standoff '+str(x),(x,0,1.374),.006,.018,1,N=16,role='top_handle')
rod('Top cap short grip',(-.185,0,1.385),(-.075,0,1.385),.008,2,16,'top_handle')
for x in (-.240,-.020):
 rod('Push handle rearward mount '+str(x),(x,.125,.809),(x,.208,.809),.010,1,16,'push_handle_mount')
 rod('Push handle upright '+str(x),(x,.208,.803),(x,.208,.986),.010,1,16,'push_handle')
rod('Rear push handle grip',(-.250,.208,.986),(-.010,.208,.986),.012,2,16,'push_handle')
asset=bpy.data.collections.new('Original collector asset parts');S.collection.children.link(asset)
for o in PARTS:
 for c in list(o.users_collection):c.objects.unlink(o)
 asset.objects.link(o)
bpy.context.view_layer.update();bpy.ops.object.select_all(action='DESELECT')
for o in PARTS:o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_materials='EXPORT')
if '--expected-glb-sha' in ARGS and hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()!=arg('--expected-glb-sha',''):raise SystemExit('Actual exported GLB differs from requested reviewed binary pin; no images rendered.')
S['review_stage']='gray geometry' if GRAY else ('final limited palette geometry' if FINAL else 'limited PBR review');S['static_asset_only']=True
S['interface_scope']='Bare inlet only; no connected hose or validated mating fit.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
R=bpy.data.scenes.new('Temporary actual GLB measurements');bpy.context.window.scene=R
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));rparts=[o for o in R.objects if o.type=='MESH'];vv=[o.matrix_world@v.co for o in rparts for v in o.data.vertices]
tri=0
for o in rparts:o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles)
bounds={k:float(max(v[i] for v in vv)-min(v[i] for v in vv)) for i,k in enumerate(('x','y','z'))};bounds['unit']='m';mc=len({m.name for o in rparts for m in o.data.materials});bpy.context.window.scene=S
for o in list(R.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.data.scenes.remove(R)
print('BUILT',json.dumps({'parts':len(PARTS),'actual_glb_triangles':tri,'actual_glb_materials':mc,'bounds':bounds}),flush=True)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
def stage_render():
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0005));floor=bpy.context.object;floor.name='Render only ground';fm=bpy.data.materials.new('Render only charcoal ground');fm.use_nodes=True;p=fm.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(.07,.085,.10,1);p.inputs['Roughness'].default_value=.82;floor.data.materials.append(fm)
 for n,loc,en,size in [('Key',(2,-3,4),180,3),('Fill',(-3,-1,2.5),120,2.5),('Rim',(1,3,3.5),210,2)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name='Render only '+n;o.data.energy=en;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,.7))
 bpy.ops.object.camera_add(location=(2.8,-4,2.6));cam=bpy.context.object;cam.name='Render only fitted camera';cam.data.type='ORTHO';S.camera=cam;return cam
def render(cam,name,loc,path):
 cam.location=loc;aim(cam,(0,0,.70));bpy.context.view_layer.update();pp=[cam.matrix_world.inverted()@(o.matrix_world@v.co) for o in PARTS for v in o.data.vertices];lo=[min(v[i] for v in pp) for i in (0,1)];hi=[max(v[i] for v in pp) for i in (0,1)];cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*1.18;cam.location+=cam.matrix_world.to_3x3()@Vector(((hi[0]+lo[0])/2,(hi[1]+lo[1])/2,0));S.render.filepath=str(path);start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start;bpy.context.view_layer.update();pp=[cam.matrix_world.inverted()@(o.matrix_world@v.co)for o in PARTS for v in o.data.vertices];norm=[(v.x/cam.data.ortho_scale+.5,v.y/cam.data.ortho_scale+.5)for v in pp];mins=[min(v[i]for v in norm)for i in(0,1)];maxs=[max(v[i]for v in norm)for i in(0,1)];assert min(mins)>.06 and max(maxs)<.94;RENDER_RECORDS.append({'view':name,'file':str(path),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'bytes':Path(path).stat().st_size,'resolution':[896,896],'cycles_samples':S.cycles.samples,'adaptive_sampling':S.cycles.use_adaptive_sampling,'denoising':S.cycles.use_denoising,'compositor':S.use_nodes,'threads':S.render.threads,'elapsed_seconds':elapsed,'camera_location_m':list(cam.location),'ortho_scale_m':cam.data.ortho_scale,'all_part_projection_min':mins,'all_part_projection_max':maxs,'not_cropped':True});print('RENDERED',name,str(path),'SECONDS',elapsed,flush=True)
if '--gray-views' in ARGS:
 d=Path(arg('--gray-views',str(OUT))).resolve();d.mkdir(parents=True,exist_ok=True);cam=stage_render();render(cam,'gray-isometric',(2.8,-4,2.5),d/'gray-isometric.png');render(cam,'gray-rear-structure',(3.4,3,1.8),d/'gray-rear-structure.png')
elif '--preview' in ARGS:
 d=Path(arg('--preview',str(OUT))).resolve();d.mkdir(parents=True,exist_ok=True);cam=stage_render();render(cam,'limited-pbr',(2.8,-4,2.5),d/'limited-pbr.png')
elif SINGLE_VIEW:
 d=Path(arg('--view-out',str(OUT))).resolve();d.mkdir(parents=True,exist_ok=True);cam=stage_render();render(cam,SINGLE_VIEW,VIEW_SPECS[SINGLE_VIEW],d/('qa-'+SINGLE_VIEW+'.png'))
elif FINAL:
 cam=stage_render();render(cam,'isometric',VIEW_SPECS['isometric'],OUT/'thumbnail.png')
 if '--views' in ARGS:
  d=Path(arg('--views',str(OUT))).resolve();d.mkdir(parents=True,exist_ok=True)
  for n in ('front','back','left','right','top'):render(cam,n,VIEW_SPECS[n],d/('qa-'+n+'.png'))
if FINAL and all((OUT/n).is_file() for n in ('model.glb','source.blend','generate.py','thumbnail.png')):
 def finfo(n):
  p=OUT/n;return{'path':'assets/industrial/'+ASSET+'/v'+VERSION+'/'+n,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':'Original Mobile Canister Workshop Dust Collector','description':'Original static mobile single-stage workshop dust collector: hollow pleated upper canister, open collector plenum, separate opaque lower collection bag, side blower and motor, bare open inlet, retaining clamps, rear push handle, steel supports and four bored caster wheels. Limited teal, satin steel, charcoal and warm pale PBR palette. No connected hose, validated mating fit, motion, collection or filtration performance, health protection, explosion protection, load rating, operation, manufacture or safety certification is claimed.','bounds':bounds,'triangles':tri,'materials':mc,'status':'review','license':'All rights reserved','files':{k:finfo(n)for k,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]}}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n');print('COMPLETE_CORE',flush=True)

if '--views' in ARGS and RENDER_RECORDS:
 d=Path(arg('--views',str(OUT))).resolve();d.mkdir(parents=True,exist_ok=True);(d/'render-manifest.json').write_text(json.dumps({'self_contained_generator':True,'renderer':'Cycles fixed 128 samples','external_helpers_required':False,'views':RENDER_RECORDS},indent=2)+'\n')
