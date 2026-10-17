"""Original compact static two-wheel bench band saw, S01-clean-geometric.
Metres, Z-up, front -Y, four foot undersides at Z=0; Blender 4.3.2.
Self-contained: no asset library, network, textures, optional add-ons or data files.
CLI (five published files): blender -b -t 4 --python-exit-code 1 --python generate.py -- --out DIRECTORY --threads 4
Six actual views: append --views QA_DIRECTORY (hero thumbnail + front/back/left/right/top).
No render / geometry only: append --no-render (alias --geometry-only), optionally --gray;
only generate.py/model.glb/source.blend are written, no metadata is fabricated.
No-render cannot be combined with --views. CPU 2 or 4, 128 samples, no denoising.
Optional --expect-glb-sha256 DIGEST checks exact exported GLB bytes before any image.
With --views, the external QA directory also receives a six-view camera/hash report.
All author-selected dimensions are design values, not a branded model replica.
Primary scale/structure references, read 2026-10-17:
https://cdn0.grizzly.com/specsheets/g0803z_ds.pdf (pp1-2 product vs carton)
https://support.grizzly.com/hc/en-us/articles/35116279826199-FAQ-G0803Z-Benchtop-Bandsaw
https://cdn0.grizzly.com/manuals/g0803z_m.pdf (pp15-17 table, pp53-56 parts)
https://rikontools.com/wp-content/uploads/manuals/10-3061/10-3061M4-English.pdf
(Rikon p7 structure, pp10-12 table/trunnions, pp24-27 exploded parts).
Author design table: tire diameter .235m, parallel Y wheel shafts vertically
separated .430m, band .0065m wide / .00065m thick; table .300x.300m,
table top .350m, base .410x.302m, four pads .062x.050m. Ideal tire-loop
2*.430+pi*.235=1.598274m; band centerline is slightly longer. This deliberately
differs from the reference 62-inch blade and is not a Grizzly/Rikon replica.
Lower housing author roof .319m, true rear trunnion service mouth, two .011m
rear guide-bolt apertures and an open right guide notch. All wheel/guide/table
poses stay fixed; these are geometric display clearances only.
Fixed display only. No motion, cutting, loading, anchoring, manufacture or safety
rating is represented. Reference research and independent tests are separate QA.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
ASSET='industrial-bench-band-saw-01'; VERSION='1.0.0'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def arg(n,d): return ARGS[ARGS.index(n)+1] if n in ARGS else d
OUT=Path(arg('--out',str(Path(__file__).resolve().parent))).resolve(); OUT.mkdir(parents=True,exist_ok=True)
if Path(__file__).resolve()!=OUT/'generate.py': (OUT/'generate.py').write_bytes(Path(__file__).resolve().read_bytes())
GRAY='--gray' in ARGS; GEO_ONLY='--geometry-only' in ARGS or '--no-render' in ARGS
THREADS=int(arg('--threads','4'));assert THREADS in (2,4), '--threads must be 2 or 4'
assert not (GEO_ONLY and '--views' in ARGS), 'no-render and --views are mutually exclusive'
N=64; CX=-.060; LO=.195; HI=.625; WR=.1175; BT=.00065; BW=.0065; BR=WR+BT/2; BX=CX+BR
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
bpy.context.preferences.filepaths.save_version=0
S=bpy.context.scene; S.name=ASSET+' editable static source'; S.unit_settings.system='METRIC';S.unit_settings.scale_length=1
S.render.engine='CYCLES';S.cycles.samples=128;S.cycles.use_adaptive_sampling=False;S.cycles.use_denoising=False;S.render.threads_mode='FIXED';S.render.threads=THREADS
S.render.resolution_x=896;S.render.resolution_y=896;S.render.resolution_percentage=100;S.view_settings.view_transform='AgX'
S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.24,.27,1);S.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
PARTS=[]; ROLES={}
def material(n,c,metal,rough):
 m=bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=(*c,1)
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
PALETTE=[('Muted teal cast body',(.18,.28,.29),.25,.70),('Plain machined steel',(.38,.40,.40),.70,.48),('Dark charcoal controls and tires',(.035,.040,.045),0,.80)]
MATS=[material('Gray geometry' if GRAY else n,(.42,.43,.44) if GRAY else c,0 if GRAY else m,.72 if GRAY else r) for n,c,m,r in PALETTE]
def fix(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();return o
def reg(o,n,slot=0,role=None):
 o.name=n;o.data.name=n+' mesh';o.data.materials.append(MATS[slot]);o['asset_id']=ASSET;o['component_role']=role or n;o['fixed_display_pose']=True;PARTS.append(o);ROLES[n]=role or n;return fix(o)
def mesh(n,vs,fs,slot=0,role=None):
 me=bpy.data.meshes.new(n+' mesh');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);S.collection.objects.link(o);return reg(o,n,slot,role)
def box(n,loc,size,slot=0,bevel=0,role=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('One-segment chamfer','BEVEL');mod.width=bevel;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 return reg(o,n,slot,role)
def cyl(n,loc,r,depth,slot=1,axis='Z',sides=24,role=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=sides,radius=r,depth=depth,location=loc);o=bpy.context.object
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 if axis=='X':o.rotation_euler[1]=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return reg(o,n,slot,role)
def ring_y(n,x,z,ro,ri,y0,y1,slot=1,count=N,a0=0,a1=2*math.pi,role=None):
 full=abs(a1-a0-2*math.pi)<1e-8;K=count if full else count+1
 aa=[a0+(a1-a0)*i/count for i in range(K)]
 vs=[(x+r*math.cos(a),y,z+r*math.sin(a)) for y,r in ((y0,ro),(y1,ro),(y0,ri),(y1,ri)) for a in aa];fs=[]
 for i in range(count):
  j=(i+1)%K;fs.extend([(i,j,K+j,K+i),(2*K+i,3*K+i,3*K+j,2*K+j),(i,2*K+i,2*K+j,j),(K+i,K+j,3*K+j,3*K+i)])
 if not full:fs.extend([(0,K,3*K,2*K),(K-1,2*K-1,4*K-1,3*K-1)])
 return mesh(n,vs,fs,slot,role)
def poly_y(n,pts,y0,y1,slot=0,role=None):
 k=len(pts);vs=[(x,y,z) for y in (y0,y1) for x,z in pts];fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,k+(i+1)%k,k+i) for i in range(k)]
 return mesh(n,vs,fs,slot,role)
def boolean_box(o,n,loc,size):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);c=bpy.context.object;c.name=n;c.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new(n,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True);fix(o)
def boolean_cylinder(o,n,loc,r,depth,axis='Z'):
 c=cyl(n,loc,r,depth,1,axis,32);PARTS.remove(c);ROLES.pop(n,None)
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new(n,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True);fix(o)
def rod(n,a,b,r,slot=1,sides=12):
 a,b=Vector(a),Vector(b);o=cyl(n,(a+b)/2,r,(b-a).length,slot,sides=sides);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o

# Real support pads: these four complete horizontal rectangles alone touch Z=0.
for i,(x,y) in enumerate([(-.155,-.105),(.155,-.105),(-.155,.105),(.155,.105)],1):
 box('Ground contact foot '+str(i),(x,y,.006),(.062,.050,.012),2,role='ground_contact')
base=box('Chamfered cast base',(0,0,.027),(.410,.302,.030),0,.006,role='base')
for x in (-.155,.155):
 for y in (-.105,.105):cyl('Base seated bolt '+str(x)+' '+str(y),(x,y,.046),.006,.008,1,sides=6)
# C-shaped cast load path lives behind the blade plane; this is geometry, not a load claim.
box('C frame upright',(-.181,.067,.389),(.044,.052,.666),0,.005,role='frame')
box('C frame lower bridge',(-.109,.067,.132),(.175,.052,.095),0,.004,role='frame')
box('C frame upper bridge',(-.109,.067,.627),(.175,.052,.100),0,.005,role='frame')
# Rear support clears the complete band and lower wheel plane; static seating only.
box('Lower frame foot',(-.142,.075,.071),(.119,.111,.064),0,.005,role='frame')
for label,z in [('Lower',LO),('Upper',HI)]:
 # A bored bearing block and the actual horizontal axle intersect the frame bridge.
 block=box(label+' axle bearing block',(CX,.058,z),(.054,.062,.054),0,.003,role='wheel_mount')
 boolean_cylinder(block,label+' axle bore cutter',(CX,.058,z),.0081,.080,'Y')
 cyl(label+' horizontal axle',(CX,.034,z),.008,.126,1,'Y',24,role='wheel_axle')
 ring_y(label+' rear bearing sleeve',CX,z,.019,.0081,.033,.081,1,32,role='wheel_mount')
 ring_y(label+' bored wheel hub',CX,z,.027,.0081,-.013,.013,1,32,role='wheel')
 ring_y(label+' wheel metal rim',CX,z,.110,.093,-.008,.008,1,N,role='wheel')
 ring_y(label+' faceted tire',CX,z,WR,.110,-.008,.008,2,N,role='tire')
 for i in range(6):
  a=2*math.pi*i/6;u=(math.cos(a),math.sin(a));v=(-u[1],u[0]);w=.010
  pts=[(CX+r*u[0]+s*v[0],z+r*u[1]+s*v[1]) for r,s in [(.023,-w/2),(.097,-w/2),(.097,w/2),(.023,w/2)]]
  poly_y(label+' wheel spoke '+str(i+1),pts,-.007,.007,1,role='wheel')
 nut=cyl(label+' axle retaining nut',(CX,-.024,z),.012,.009,1,'Y',6)
 boolean_cylinder(nut,label+' nut through bore',(CX,-.024,z),.0081,.025,'Y')
# One manifold closed band. Its wheel contact facets share exactly the tire's angular tessellation.
path=[]
for i in range(N//2+1):
 a=math.pi*i/(N//2);path.append((CX+BR*math.cos(a),HI+BR*math.sin(a),math.cos(a),math.sin(a)))
for i in range(1,22):path.append((CX-BR,HI+(LO-HI)*i/22,-1,0))
for i in range(N//2+1):
 a=math.pi+math.pi*i/(N//2);path.append((CX+BR*math.cos(a),LO+BR*math.sin(a),math.cos(a),math.sin(a)))
for i in range(1,22):path.append((CX+BR,LO+(HI-LO)*i/22,1,0))
vs=[]
for x,z,nx,nz in path:
 for sign,y in [(-1,-BW/2),(-1,BW/2),(1,BW/2),(1,-BW/2)]:vs.append((x+sign*BT/2*nx,y,z+sign*BT/2*nz))
fs=[];K=len(path)
for i in range(K):
 for j in range(4):fs.append((i*4+j,i*4+(j+1)%4,((i+1)%K)*4+(j+1)%4,((i+1)%K)*4+j))
blade=mesh('Single continuous closed blade band',vs,fs,1,role='blade_loop');blade['path_segment_count']=K;blade['width_m']=BW;blade['thickness_m']=BT
# Restrained fine teeth on the front edge of the continuous band; every root overlaps it.
for side,x in [('Working',CX+BR),('Return',CX-BR)]:
 tv=[];tf=[]
 for i in range(94):
  z=LO+.004+i*(HI-LO-.008)/94;k=len(tv)
  tv +=[(x+s*BT/2,y,zz) for s in (-1,1) for y,zz in [(-BW/2+.0001,z),(-BW/2-.0011,z+.0015),(-BW/2+.0001,z+.0034)]]
  tf.extend([(k,k+2,k+1),(k+3,k+4,k+5),(k,k+1,k+4,k+3),(k+1,k+2,k+5,k+4),(k+2,k,k+3,k+5)])
 mesh(side+' fine blade teeth',tv,tf,1,role='blade_teeth')
# Closed front/rear doors and fixed outer shells. Two real bottom/top exits in each shell
# accommodate the work and return band. Doors never occupy the central wheel plane.
for label,z,sgn in [('Upper',HI,1),('Lower',LO,-1)]:
 cap=.1375;end=.470 if sgn==1 else .319
 pts=[(CX-cap,end),(CX+cap,end),(CX+cap,z)] if sgn==1 else [(CX-cap,end),(CX-cap,z)]
 if sgn==1:pts +=[(CX+cap*math.cos(math.pi*i/32),z+cap*math.sin(math.pi*i/32)) for i in range(1,33)]
 else:pts +=[(CX+cap*math.cos(math.pi+math.pi*i/32),z+cap*math.sin(math.pi+math.pi*i/32)) for i in range(1,33)]+[(CX+cap,end)]
 poly_y(label+' closed front door',pts,-.049,-.043,0,role='front_cover')
 rear=poly_y(label+' fixed rear cover',pts,.043,.049,0,role='rear_cover');boolean_cylinder(rear,label+' shaft rear aperture',(CX,.046,z),.020,.020,'Y')
 if sgn==-1:
  # Real rear trunnion service mouth; unchanged ear and clamp stud stay outside metal.
  boolean_box(rear,'Lower rear trunnion service mouth',(-.018,.0455,.3025),(.102,.013,.045))
  for x in (.0511,.06455):
   boolean_cylinder(rear,'Lower side-guide bolt access '+str(x),(x,.046,.312),.0055,.014,'Y')
 ring_y(label+' curved outer shell',CX,z,cap,cap-.007,-.043,.043,0,32,0 if sgn==1 else math.pi,math.pi if sgn==1 else 2*math.pi,role='shell')
 for x in (CX-cap+.0035,CX+cap-.0035):
  wall=box(label+' shell side '+str(x),(x,0,(end+z)/2),(.007,.086,abs(end-z)),0,role='shell')
  if sgn==-1 and x>CX:
   boolean_box(wall,'Lower right guide service notch',(.074,.017,.314),(.026,.042,.022))
 # Lower cover is continuous to the new roof; all functional openings are real.
 # Author roof .319: web [.316,.322], tire gap .0035, shoe gap .002m.
 work_left,work_right=(CX+BR-.005,CX+BR+.005) if sgn==1 else (.0375,.073825)
 edges=[CX-cap,CX-BR-.005,CX-BR+.005,work_left,work_right,CX+cap]
 for j,(a,b) in enumerate(zip(edges[::2],edges[1::2])):
  web=box(label+' slotted exit web '+str(j),((a+b)/2,0,end),(b-a,.086,.006),0,role='shell_exit')
  if sgn==-1 and j==1:
   boolean_box(web,'Lower top trunnion service mouth',(-.018,.0455,.3025),(.102,.013,.045))
  if sgn==-1 and j==2:
   boolean_box(web,'Lower right roof guide service notch',(.074,.017,.314),(.026,.042,.022))
 for i,hz in enumerate([z-.055,z+.055]):
  if hz<.06 or hz>.76:continue
  box(label+' door hinge '+str(i),(CX-cap-.002,-.045,hz),(.012,.018,.024),1,.001)
 cyl(label+' seated door latch',(CX+.106,-.055,z+.015),.008,.012,2,'Y',12)
# Rectangular return tunnel, hollow throughout, bridges the two housings.
RX=CX-BR
box('Return guard left wall',(RX-.010,0,.380),(.006,.036,.214),0)
box('Return guard right wall',(RX+.010,0,.380),(.006,.036,.214),0)
box('Return guard front wall',(RX,-.015,.380),(.014,.006,.214),0)
box('Return guard rear wall',(RX,.015,.380),(.014,.006,.214),0)
# The upper guide post is seated into the upper casting and its clamp; work blade remains visible.
box('Upper guide sliding post',(.092,.030,.516),(.016,.018,.220),1,.001,role='guide_post')
box('Upper guide post clamp',(.086,.036,.485),(.038,.034,.034),0,.002,role='guide_mount')
cyl('Upper post lock shaft',(.110,.028,.485),.004,.032,1,'X',16)
cyl('Upper post lock knob',(.129,.028,.485),.012,.010,2,'X',12)
# Upper/lower side bearing axes are Y, rear thrust axis X. The .0045m-wide
# side races occupy Y[-.0015,.0030], 1.75mm behind the tooth-root line
# Y=-.00325. This original static geometry is not an operating adjustment.
def guide(label,z):
 box(label+' guide rear bridge',(.066,.029,z),(.053,.014,.014),0,.001,role='guide_bracket')
 box(label+' guide right cheek',(.087,.018,z),(.011,.031,.022),0,.001,role='guide_bracket')
 for sign,side in [(-1,'left'),(1,'right')]:
  x=BX+sign*(.006+BT/2+.0004)
  cyl(label+' '+side+' side guide axle',(x,.013,z),.0018,.032,1,'Y',16,role='guide_axle')
  ring_y(label+' '+side+' side bearing',x,z,.006,.0019,-.0015,.0030,1,24,role='side_guide')
  cyl(label+' '+side+' side axle bolt',(x,.040,z),.004,.009,1,'Y',6)
 thrust=cyl(label+' thrust bearing',(BX,.0113,z+.009),.0075,.012,1,'X',24,role='thrust_guide')
 boolean_cylinder(thrust,label+' thrust bearing real bore',(BX,.0113,z+.009),.0021,.026,'X')
 cyl(label+' thrust axle',(.073,.0113,z+.009),.002,.037,1,'X',16,role='guide_axle')
guide('Upper',.434);guide('Lower',.312)
box('Lower guide seated mount',(.088,.034,.294),(.024,.033,.034),0,.002,role='guide_mount')
# Split front blade guard is a hollow channel, not a solid block through the band.
for x in (BX-.006,BX+.006):box('Upper blade guard side '+str(x),(x,.001,.453),(.003,.014,.034),2,role='blade_guard')
box('Upper blade guard rear',(BX,.0095,.453),(.015,.003,.034),2,role='blade_guard')
# A genuine front insertion slit ends at a through insert pocket in the table.
TABLE_TOP=.350;TABLE_BOT=.332
work=box('Working table with real slit and insert pocket',(.075,-.070,.341),(.300,.300,.018),1,.002,role='table')
boolean_box(work,'Actual insert through pocket',(BX,0,.341),(.020,.020,.050))
boolean_box(work,'Actual front insertion slit',(BX,-.115,.341),(.0032,.230,.050))
insert=box('Removable slotted table insert',(BX,0,.3485),(.0188,.0188,.003),2,role='table_insert')
boolean_box(insert,'Insert blade through clearance',(BX,0,.349),(.0032,.009,.020))
boolean_box(insert,'Insert insertion slit',(BX,-.0065,.349),(.0032,.008,.020))
# Genuine dual curved trunnion ears with a through clamping stud under the back of table.
for y in (.045,.072):
 ear=ring_y('Table trunnion curved ear '+str(y),-.018,.331,.048,.032,y-.004,y+.004,0,16,math.pi,2*math.pi,role='table_trunnion')
 boolean_cylinder(ear,'Real trunnion clamp bore '+str(y),(-.018,y,.291),.00615,.030,'Y')
 box('Table trunnion top shoe '+str(y),(-.018,y,.328),(.096,.012,.008),0,role='table_mount')
box('Table support casting',(-.102,.062,.288),(.140,.036,.038),0,.003,role='table_support')
riser=box('Trunnion seated riser',(-.018,.062,.300),(.034,.040,.048),0,.002,role='table_support')
boolean_cylinder(riser,'Real riser clamp bore',(-.018,.062,.291),.00615,.065,'Y')
cyl('Table trunnion through clamping stud',(-.018,.059,.291),.006,.080,1,'Y',24,role='table_axle')
cyl('Table tilt lock knob',(-.018,.105,.291),.018,.018,2,'Y',12)
# Coaxial rear lower motor and a real hollow exhaust connection.
cyl('Rear direct motor housing',(CX,.134,LO),.051,.110,0,'Y',24,role='motor')
cyl('Rear motor end cap',(CX,.193,LO),.053,.014,1,'Y',24)
for i in range(5):box('Rear motor cooling rib '+str(i),(CX,.205,LO-.030+i*.015),(.062,.008,.003),2)
# Dust neck points +Y from lower cover, away from working blade.
ring_y('Hollow dust collection port',.014,.112,.027,.023,.042,.117,0,32,role='dust_port')
ring_y('Dust port outer lip',.014,.112,.029,.023,.109,.121,2,32,role='dust_port')
# The rear cover actually opens into the neck, not a capped decorative cylinder.
lower_rear=bpy.data.objects['Lower fixed rear cover'];boolean_cylinder(lower_rear,'Dust rear cover aperture',(.014,.046,.112),.023,.030,'Y')
# Fixed tension screw and unlabelled control; seated in the upper bridge/casting.
box('Tension screw top boss',(CX,.015,.762),(.047,.050,.018),0,.002)
cyl('Fixed upper tension screw',(CX,.015,.774),.005,.044,1,'Z',16)
cyl('Fixed tension hand knob',(CX,.015,.797),.021,.015,2,'Z',12)
box('Front switch enclosure',(-.178,-.032,.341),(.040,.028,.063),2,.003)
box('Unlabelled recessed rocker',(-.178,-.050,.341),(.024,.010,.035),1,.001)
# Source grouping preserves every independently editable named piece, no render props.
asset_col=bpy.data.collections.new('Asset geometry: '+ASSET);S.collection.children.link(asset_col)
for o in PARTS:
 fix(o)
 for c in list(o.users_collection):c.objects.unlink(o)
 asset_col.objects.link(o)
bpy.context.view_layer.update()
S['asset_id']=ASSET;S['stage']='gray geometry' if GRAY else 'limited palette review';S['static_asset_only']=True
S['author_design_values_m']=json.dumps({'wheel_diameter':WR*2,'wheel_center_spacing':HI-LO,'blade_width':BW,'blade_thickness':BT,'table_size':[.300,.300],'table_top':TABLE_TOP,'foot_underside':0})
bpy.ops.object.select_all(action='DESELECT')
for o in PARTS:o.select_set(True)
bpy.context.view_layer.objects.active=PARTS[0]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_apply=False,export_yup=True,export_extras=True,export_materials='EXPORT',export_animations=False)
expected_glb=arg('--expect-glb-sha256','')
if expected_glb:
 actual_glb=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest();assert actual_glb==expected_glb, 'Export differs from reviewed PBR bytes before rendering: '+actual_glb
 print('REVIEWED_PBR_GLB_BYTES_LOCKED',actual_glb,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
world=[o.matrix_world@v.co for o in PARTS for v in o.data.vertices]
bounds={k:float(max(v[i] for v in world)-min(v[i] for v in world)) for i,k in enumerate(('x','y','z'))};bounds['unit']='m'
triangles=0
for o in PARTS:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
print('BUILT',json.dumps({'id':ASSET,'parts':len(PARTS),'triangles':triangles,'bounds':bounds,'gray':GRAY,'geometryOnly':GEO_ONLY}),flush=True)

def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def render_setup():
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));floor=bpy.context.object;floor.name='Render only backdrop';floor.data.materials.append(material('Render backdrop',(.10,.12,.15),0,.9))
 for name,loc,energy,size in [('Key',(.8,-1.2,1.5),45,1.1),('Fill',(-.9,-.3,.9),25,1.0),('Rim',(.4,.9,1.3),48,.8)]:
  bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.name=name;light.data.energy=energy;light.data.shape='DISK';light.data.size=size;aim(light,(0,0,.4))
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';S.camera=cam;return cam

VIEW_REPORT=[]
def view(cam,loc,path,margin=1.16):
 assert S.cycles.samples==128 and S.cycles.use_adaptive_sampling is False and S.cycles.use_denoising is False and S.render.threads_mode=='FIXED' and S.render.threads==4 and S.use_nodes is False, 'Actual fixed-128/no-adaptive/no-denoise/four-thread/no-compositor contract violated before image render'
 cam.location=loc;aim(cam,(0,0,.4));bpy.context.view_layer.update();v=[cam.matrix_world.inverted()@(o.matrix_world@p.co) for o in PARTS for p in o.data.vertices];lo=[min(p[i] for p in v) for i in (0,1)];hi=[max(p[i] for p in v) for i in (0,1)];cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*margin;cam.location+=cam.matrix_world.to_3x3()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0));S.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 bpy.context.view_layer.update();pv=[cam.matrix_world.inverted()@(o.matrix_world@p.co) for o in PARTS for p in o.data.vertices];half=cam.data.ortho_scale/2;margins={axis:min(min(p[i] for p in pv)+half,half-max(p[i] for p in pv)) for i,axis in enumerate(('horizontal','vertical'))};assert min(margins.values())>1e-5
 VIEW_REPORT.append({'view':Path(path).stem,'path':str(path),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'samples':S.cycles.samples,'threads':S.render.threads,'denoise':S.cycles.use_denoising,'adaptiveSampling':S.cycles.use_adaptive_sampling,'compositor':S.use_nodes,'threadsMode':S.render.threads_mode,'resolution':[S.render.resolution_x,S.render.resolution_y],'orthoScale_m':cam.data.ortho_scale,'cameraWorldLocation':list(cam.location),'cameraRotationEuler':list(cam.rotation_euler),'allActualWorldVertexMargins_m':margins})
 print('FORMAL_VIEW_READY',Path(path).stem,'samples',S.cycles.samples,'threads',S.render.threads,flush=True)
if not GEO_ONLY or '--views' in ARGS:
 cam=render_setup()
 if not GEO_ONLY:view(cam,(1.12,-1.55,1.07),OUT/'thumbnail.png')
 if '--views' in ARGS:
  vd=Path(arg('--views',''));vd.mkdir(parents=True,exist_ok=True)
  for name,loc in [('front',(0,-2,.4)),('back',(0,2,.4)),('left',(-2,0,.4)),('right',(2,0,.4)),('top',(0,0,2))]:view(cam,loc,vd/(name+'.png'))
  (vd/'six-formal-view-report.json').write_text(json.dumps({'modelGlbSha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'generatorSha256':hashlib.sha256((OUT/'generate.py').read_bytes()).hexdigest(),'sourceBlendSha256':hashlib.sha256((OUT/'source.blend').read_bytes()).hexdigest(),'actualViews':VIEW_REPORT,'selfContainedGeneratorRenderedAllSix':len(VIEW_REPORT)==6},indent=2)+'\n')
if not GEO_ONLY:
 def info(name):
  p=OUT/name;return {'path':'assets/industrial/'+ASSET+'/v'+VERSION+'/'+name,'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'industrial','style':'S01-clean-geometric','title':'Original Compact Two-Wheel Bench Band Saw','description':'Original fixed-pose compact workshop band saw with four planar feet, C-shaped rear frame, horizontal upper and lower axles, bored spoked wheels, one continuous closed toothed blade, closed wheel housings with actual band exits, correctly oriented upper and lower three-bearing guides, slotted table and insert, supported curved trunnion ears, direct rear motor, tension knob, front switch and hollow dust port. Limited teal, steel and charcoal PBR palette. All dimensions are author design values. Independent editable mesh components. No motion, cutting, anchoring, loading, manufacturability or safety certification is claimed.','bounds':bounds,'triangles':triangles,'materials':len(MATS),'status':'review','license':'All rights reserved','files':{k:info(n) for k,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]}}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
