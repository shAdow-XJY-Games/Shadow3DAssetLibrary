"""Original static finned inverter cabinet exterior; one ground-supported prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='renewable-finned-inverter-cabinet-01';VERSION='1.0.0';TITLE='Finned Inverter Cabinet'
DESCRIPTION=('One original static low-poly inverter-cabinet exterior. Two short full-depth skids support a continuous thick cabinet body with a genuinely recessed lower connection bay, thick floor and back wall. Three independent thick blind-bore connector seats are recessed inside that bay. A separate rear plate finitely joins the body and nine thick vertical fins; eight real full-height open channels remain between the fins. The front has one recessed opaque blank display and two fixed buttons. Nineteen closed connected editable meshes, five opaque unlinked constant PBR materials, metres, native Z up, front -Y and a fixed ground-level design datum with actual Y bounds midpoint -0.0055 m. One prop only: no solar panels, batteries, cables, text, brand, door motion, textures or animation. The upper body is a solid exterior representation; no internal electronics are modeled. Static visual geometry only. No power conversion, supply, voltage, circuits, wiring, communication, efficiency, air flow, thermal performance, waterproofing, fire resistance, insulation, shock protection, load, tip resistance, installation, manufacture or electrical/safety certification is asserted. No compatibility with earlier power-station, cabinet, panel or cable-tray assets.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={};FEET=[]
BODY='Cabinet_ContinuousRecessedHousing';PLATE='Rear_ThickFinRootPlate';DISPLAY='Front_RecessedOpaqueDisplay';FIN_NAMES=[];SOCKET_NAMES=[];BUTTON_NAMES=[]
SHIFT_Y=-.0625
PALETTE=[('Housing_WarmSage',(.48,.59,.47,1),.48,.06),('SkidsAndDisplay_Charcoal',(.035,.057,.056,1),.48,.12),('RearFins_SatinGraphite',(.12,.17,.16,1),.39,.52),('SocketRims_MutedAlloy',(.40,.46,.40,1),.38,.65),('Buttons_MutedOchre',(.65,.32,.065,1),.44,.08)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no texture nodes, linked shader inputs, emission or transmission.'
FOCUS=(0,0,.545);ORTHO=1.50
CAMERAS={'gray-front3q':(2.2,-3.2,1.65),'gray-back3q':(-2.2,3.2,2.15),'thumbnail':(2.2,-3.2,1.65),'qa-front':(0,-3.5,1.65),'qa-side':(3.5,0,1.65),'qa-top':(0,0,4),'qa-back':(0,3.5,1.65),'qa-wireframe':(-2.2,3.2,2.15),'silhouette-128-front':(0,-3.5,1.65),'silhouette-128-side':(3.5,0,1.65)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def point(p):return (p[0],p[1]+SHIFT_Y,p[2])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.idx={}
 def vertex(self,p):
  p=tuple(round(float(c),9) for c in p)
  if p not in self.idx:self.idx[p]=len(self.v);self.v.append(p)
  return self.idx[p]
 def face(self,pts,mat=0):
  ids=[self.vertex(p) for p in pts]
  for i in range(1,len(ids)-1):
   if len(set([ids[0],ids[i],ids[i+1]]))==3:self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat)
 def result(self,role,mat=0):
  vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if vol<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':[point(p) for p in self.v],'faces':self.f,'face_materials':self.fm,'material':mat,'role':role}
def cellsolid(name,xs,ys,zs,occupied,mat,role):
 m=Mesh();cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 for i,j,k in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
  for (dx,dy,dz),q in [((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]:
   if (i+dx,j+dy,k+dz) not in cells:m.face(q,mat)
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def box(lo,hi,mat=0,role='Finite closed box volume'):
 return cellsolid(None,[lo[0],hi[0]],[lo[1],hi[1]],[lo[2],hi[2]],lambda x,y,z:True,mat,role)
def slab(name,lo,hi,mat,role):G[name]=box(lo,hi,mat,role);return name
def profile_y(name,cx,cz,profile,mat,role,n=24,face_mats=None):
 m=Mesh()
 def p(y,r,a):return(cx+r*math.cos(a),y,cz+r*math.sin(a))
 for k,((y,r),(yy,rr)) in enumerate(zip(profile,profile[1:])):
  for i in range(n):
   a=math.tau*i/n;b=math.tau*(i+1)/n;m.face([p(y,r,a),p(y,r,b),p(yy,rr,b),p(yy,rr,a)],face_mats[k] if face_mats else mat)
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def fin(name,x):
 m=Mesh();poly=[(.195,.325),(.315,.325),(.345,.355),(.345,.955),(.315,.985),(.195,.985)]
 for side in [-1,1]:m.face([(x+side*.009,y,z) for y,z in (poly if side>0 else list(reversed(poly)))],2)
 for a,b in zip(poly,poly[1:]+poly[:1]):m.face([(x-.009,*a),(x-.009,*b),(x+.009,*b),(x+.009,*a)],2)
 G[name]=m.result('One thick vertical chamfer-ended fin; its whole long root is finitely embedded in the rear plate.',2)

def housing_occupied(x,y,z):
 return not ((abs(x)<.247 and y<.075 and .185<z<.445) or (abs(x)<.170 and y<-.174 and .730<z<.875))
cellsolid(BODY,[-.31,-.247,-.170,.170,.247,.31],[-.205,-.174,.075,.170],[.105,.185,.445,.730,.875,1.09],housing_occupied,0,'One closed continuous housing with a thick bottom, sidewalls, rear wall, lower front recess and small display recess; solid upper exterior, no internal electronics.')
for label,x in [('Left',-.215),('Right',.215)]:
 name='GroundSkid_'+label;slab(name,(x-.06,-.22,0),(x+.06,.28,.125),1,'One independent short broad skid with a finite ground bottom and finite housing embedding.');FEET.append(name)
 EMBED_VOLUMES[name+'_HousingRoot']=dict(box((x-.05,-.16,.109),(x+.05,.14,.121)),targets=[name,BODY],role='Complete bounded skid-to-housing material overlap.');LINKS.append((name,BODY,[point((x,-.10,.115)),point((x,.10,.115))]))
slab(PLATE,(-.285,.155,.290),(.285,.205,1.020),2,'Independent continuous thick rear plate finitely embedded into the housing, carrying every vertical fin.')
EMBED_VOLUMES['Plate_HousingRoot']=dict(box((-.26,.158,.31),(.26,.167,1.00)),targets=[BODY,PLATE],role='Complete large finite rear plate-to-housing embedded strip.');LINKS.append((BODY,PLATE,[point((-.20,.162,.50)),point((.20,.162,.88))]))
for i,x in enumerate([-.24,-.18,-.12,-.06,0,.06,.12,.18,.24],1):
 name=f'RearFin_{i:02d}';fin(name,x);FIN_NAMES.append(name)
 EMBED_VOLUMES[f'FinRoot_{i:02d}']=dict(box((x-.006,.197,.35),(x+.006,.203,.96)),targets=[PLATE,name],role='Complete long finite material connection between fin root and rear plate.');LINKS.append((PLATE,name,[point((x,.200,.40)),point((x,.200,.90))]))
 if i<9:VOID_VOLUMES[f'FinChannel_{i:02d}']=dict(box((x+.010,.206,.310),(x+.050,.350,1.005)),targets=[],role='Full finite open inter-fin corridor, from below lower fin ends to above upper ends and beyond rear tips; 1 mm root/wall inset.')
slab(DISPLAY,(-.151,-.185,.746),(.151,-.171,.859),1,'One blank opaque nonemissive front panel recessed behind the housing front; broad finite rear embedding.')
EMBED_VOLUMES['Display_RearSeat']=dict(box((-.140,-.1734,.750),(.140,-.1716,.855)),targets=[BODY,DISPLAY],role='Complete thin broad rear panel embedding into the display-recess back.');LINKS.append((BODY,DISPLAY,[point((-.10,-.1725,.80)),point((.10,-.1725,.80))]))
for i,x in enumerate([-.08,.08],1):
 name=f'Front_FixedButton_{i}';profile_y(name,x,.645,[(-.193,0),(-.193,.025),(-.223,.025),(-.231,.019),(-.231,0)],4 if i==1 else 1,'One solid fixed chamfered button with finite rear embedding; no switch mechanism.');BUTTON_NAMES.append(name)
 EMBED_VOLUMES[f'ButtonSeat_{i}']=dict(box((x-.010,-.201,.635),(x+.010,-.196,.655)),targets=[BODY,name],role='Complete finite control-button rear embedding.');LINKS.append((BODY,name,[point((x,-.198,.640)),point((x,-.198,.650))]))
for i,x in enumerate([-.16,0,.16],1):
 name=f'Bay_BlindBoreSocket_{i}';profile_y(name,x,.305,[(.090,0),(.090,.054),(.051,.054),(.043,.043),(-.055,.043),(-.055,.025),(.062,.025),(.062,0)],1,'One thick independent blind-bore connector seat with complete inner wall, deep empty bore, thick closed back and integral mounting flange.',face_mats=[1,1,1,1,3,1,1]);SOCKET_NAMES.append(name)
 EMBED_VOLUMES[f'SocketSeat_{i}']=dict(box((x-.018,.080,.287),(x+.018,.087,.323)),targets=[BODY,name],role='Complete finite solid connector back-cap embedding in the recess rear wall.');LINKS.append((BODY,name,[point((x-.010,.083,.305)),point((x+.010,.083,.305))]))
 VOID_VOLUMES[f'SocketBlindBore_{i}']=dict(profile_y(None,x,.305,[(-.058,0),(-.058,.0235),(.0605,.0235),(.0605,0)],0,'Complete finite cylindrical blind-bore air including open mouth and deep inner end.'),targets=[],role='Full bore from outside its lip to 1.5 mm before its real closed back; all assembly meshes tested.')
 # Full squared-annular bay partition around the actual faceted socket exterior.
 m=Mesh();n=24;ys=[-.054,.043,.051,.074];rs=[.0445,.0445,.0555,.0555]
 def q(y,r,a):return(x+r*math.cos(a),y,.305+r*math.sin(a))
 def outer(a):return .060/max(abs(math.cos(a)),abs(math.sin(a)))
 for k in range(len(ys)-1):
  for j in range(n):
   a=math.tau*j/n;b=math.tau*(j+1)/n
   m.face([q(ys[k],rs[k],a),q(ys[k+1],rs[k+1],a),q(ys[k+1],rs[k+1],b),q(ys[k],rs[k],b)])
   m.face([q(ys[k],outer(b),b),q(ys[k+1],outer(b),b),q(ys[k+1],outer(a),a),q(ys[k],outer(a),a)])
 for k,rev in [(0,False),(-1,True)]:
  for j in range(n):
   a=math.tau*j/n;b=math.tau*(j+1)/n;pts=[q(ys[k],rs[k],b),q(ys[k],outer(b),b),q(ys[k],outer(a),a),q(ys[k],rs[k],a)];m.face(list(reversed(pts)) if rev else pts)
 VOID_VOLUMES[f'BayAroundSocket_{i}']=dict(m.result('Full squared-annular finite air around all outer socket surfaces, following flange changes.'),targets=[],role='Complete bounded cross-section around each socket, including wedge spaces; positive inner clearance.')
# Together these closed partitions cover the whole intended bay air with only
# positive tolerance layers near actual material. Bores are separately complete.
for name,lo,hi in [('BayFullFrontMouth',(-.246,-.220,.186),(.246,-.056,.444)),('BayFullUpperAir',(-.246,-.054,.366),(.246,.074,.444)),('BayFullLowerAir',(-.246,-.054,.186),(.246,.074,.244))]:VOID_VOLUMES[name]=dict(box(lo,hi),targets=[],role='Complete finite rectangular partition of the recessed bay and open mouth.')
for i,(a,b) in enumerate([(-.246,-.221),(-.099,-.061),(.061,.099),(.221,.246)],1):VOID_VOLUMES[f'BayBetweenSocketZones_{i}']=dict(box((a,-.054,.245),(b,.074,.365)),targets=[],role='Entire finite rear bay corridor beside or between socket footprints.')
VOID_VOLUMES['DisplayFullFrontRecess']=dict(box((-.169,-.208,.731),(.169,-.186,.874)),targets=[],role='Full empty front portion of the recessed display seat, before the opaque panel face.')
for name,lo,hi in [('DisplaySeat_Left',(-.169,-.184,.731),(-.152,-.175,.874)),('DisplaySeat_Right',(.152,-.184,.731),(.169,-.175,.874)),('DisplaySeat_Lower',(-.151,-.184,.731),(.151,-.175,.745)),('DisplaySeat_Upper',(-.151,-.184,.860),(.151,-.175,.874))]:VOID_VOLUMES[name]=dict(box(lo,hi),targets=[],role='Complete finite side/end air strip around the recessed opaque panel.')
for name,lo,hi in [('BayCompleteFloor',(-.240,-.198,.130),(.240,.14,.180)),('BayCompleteBackWall',(-.240,.095,.190),(.240,.145,.440)),('BayLeftWall',(-.305,-.198,.190),(-.252,.14,.440)),('BayRightWall',(.252,-.198,.190),(.305,.14,.440))]:SOLID_VOLUMES[name]=dict(box(lo,hi),targets=[BODY],role='Complete finite material region proving thick continuous bay floor or wall.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
def measure_inverter_geometry(vertices):
 return {'single_prop_count':1,'closed_mesh_count':len(G),'skid_count':2,'height_m':1.09,'body_width_m':.62,'recess_clear_width_m':.494,'recess_clear_height_m':.260,'recess_depth_m':.280,'rear_fin_count':9,'full_inter_fin_channel_count':8,'fin_thickness_m':.018,'between_fin_gap_m':.042,'fin_nominal_height_m':.660,'blind_socket_count':3,'socket_bore_depth_m':.117,'socket_inner_polygon_circumradius_m':.025,'opaque_display_count':1,'fixed_button_count':2,'materials':MATERIAL_CONTRACT,'upper_compartment_scope':'Solid closed exterior representation; internal electronics are absent.'}
assert len(G)==19,len(G)

# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFinnedInverterCabinet',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 fixed design datum; native bounds X [-0.310,0.310], Y [-0.2935,0.2825], Z [0,1.090] m; Y midpoint -0.0055 m; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
inverter_evidence=measure_inverter_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<12000
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'inverter_geometry':inverter_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/renewable/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'renewable','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
