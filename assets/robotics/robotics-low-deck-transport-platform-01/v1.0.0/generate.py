"""Original low-deck transport robot platform. One empty fixed static visual prop.
Numerical assembly and proportions are newly authored; no old asset mesh executes.
Native Z up, front -Y, origin centered between four complete ground facets.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='robotics-low-deck-transport-platform-01';VERSION='1.0.0';TITLE='Low-Deck Transport Robot Platform'
DESCRIPTION=('One original empty low transport-robot platform. A broad independently editable chamfered loading deck rests on four short complete pedestals above a closed low electronics chassis. Four newly dimensioned twelve-facet wheels, four thin outer hubs and two complete transverse axle bars form a fixed wheelbase. Four separate thick external guard strips define the lower chassis boundary; two low side stops and one rear stop border the broad open-front loading deck. A fully backed front plaque is an opaque visual panel. Twenty-four closed independently named meshes, five constant opaque unlinked PBR materials, no textures. Metres, native Z up, front -Y, ground origin centered between all four wheel soles. All numerical profiles, dimensions and component layout are newly authored. No old inspection rover, handcart, pallet jack, railway wagon or other geometry is imported, removed, transformed, recoloured or reused. One empty fixed static visual prop only. No real load capacity, autonomy, navigation, sensing, charging, powered operation, driving, steering, wheel motion, suspension, controls, animation, rigging, stability, collision protection, manufacture, transport suitability, safety certification or compatibility with old cargo assets is claimed.')
PALETTE=[('Housing_Ochre',(.64,.31,.075,1),.59,.12),('Deck_WarmIvory',(.72,.73,.65,1),.65,.08),('Guard_DeepPetrol',(.035,.17,.19,1),.62,.24),('Treads_Graphite',(.026,.034,.038,1),.86,0),('Axles_SatinAlloy',(.40,.46,.47,1),.40,.65)]
G={};CONTACTS=[];FEET=[];SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
FOCUS=(0,0,.27);ORTHO=2.70;WIRE_THICKNESS=.00125
CAMERAS={'gray-front3q':(4,-6,3.8),'gray-back3q':(-4,6,3.8),'thumbnail':(4,-6,3.8),'qa-front':(0,-6,1.8),'qa-side':(6,0,1.8),'qa-top':(0,0,6),'qa-back':(0,6,1.8),'qa-wireframe':(4,-6,3.8),'silhouette-128-front':(0,-6,1.8),'silhouette-128-side':(6,0,1.8)}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def area2(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2

def earclip(p):
 order=list(range(len(p))) if area2(p)>0 else list(reversed(range(len(p))));out=[]
 cr=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  found=False
  for j,b in enumerate(order):
   a,c=order[j-1],order[(j+1)%len(order)]
   if cr(p[a],p[b],p[c])<1e-14:continue
   if any(all(cr(p[u],p[v],p[k])>=-1e-14 for u,v in [(a,b),(b,c),(c,a)]) for k in order if k not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);found=True;break
  assert found,('untriangulable',p,order)
 out.append(tuple(order));return out
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.ix={}
 def vert(self,p):
  p=tuple(round(float(c),9) for c in p)
  if p not in self.ix:self.ix[p]=len(self.v);self.v.append(p)
  return self.ix[p]
 def tri(self,p):self.f.append(tuple(self.vert(q) for q in p))
 def quad(self,p):self.tri(p[:3]);self.tri([p[0],p[2],p[3]])
 def result(self,mat,role):
  e={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):e.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(q)==2 for q in e.values()),('open mesh',role,[(k,q) for k,q in e.items() if len(q)!=2][:5])
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in e[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),('disconnected',role)
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if vol<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'material':mat,'face_materials':[mat]*len(self.f),'role':role}
def extrude(poly,a,b,axis,mat=0,role='complete finite extruded solid'):
 m=Mesh();point=lambda q,t:((q[0],q[1],t) if axis=='z' else (q[0],t,q[1]))
 for t in [a,b]:
  for tri in earclip(poly):m.tri([point(poly[i],t) for i in tri])
 for p,q in zip(poly,poly[1:]+poly[:1]):m.quad([point(p,a),point(q,a),point(q,b),point(p,b)])
 return m.result(mat,role)
def offset(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);L=math.hypot(*e);lines.append(((a[0]-d*e[1]/L,a[1]+d*e[0]/L),e))
 out=[]
 for i,(q,v) in enumerate(lines):
  p,u=lines[i-1];den=u[0]*v[1]-u[1]*v[0]
  if abs(den)<1e-14:out.append(q);continue
  t=((q[0]-p[0])*v[1]-(q[1]-p[1])*v[0])/den;out.append((p[0]+t*u[0],p[1]+t*u[1]))
 return out
def boxg(lo,hi,mat=0):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z',mat)
def circle(c,r,n=16,phase=0):return [(c[0]+r*math.cos(phase+math.tau*i/n),c[1]+r*math.sin(phase+math.tau*i/n)) for i in range(n)]
def chamfer(x,y,c):return [(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c),(-x,-y+c)]

def contact(name,a,b,axis,plane,u,v,area):CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'plane_m':plane,'u':u,'v':v,'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.001,'points':[]})
def seat(name,a,b,z,area):contact(name,a,b,(0,0,1),z,(1,0,0),(0,1,0),area)
def block(name,lo,hi,mat,role):
 G[name]=boxg(lo,hi,mat);G[name]['role']=role;SOLID_VOLUMES[name]=dict(boxg(tuple(v+.001 for v in lo),tuple(v-.001 for v in hi)),targets=[name])
def disk_x(x,y,r,width,mat,inset=0):
 # Original twelve-sided low wheel proportions; the lower complete facet is horizontal.
 poly=circle((y,.12),r-inset,12,math.pi/12)
 g=extrude(poly,x-width/2+inset,x+width/2-inset,'y',mat,'Complete twelve-facet fixed transverse disk with flat finite sole')
 g['vertices']=[(p[1],p[0],p[2]) for p in g['vertices']];g['faces']=[tuple(reversed(f)) for f in g['faces']];return g
WHEEL_R=.12/math.cos(math.pi/12);HUB_R=.059
POLYAREA=lambda r:12*r*r*math.sin(math.tau/12)/2
CHASSIS=chamfer(.50,.69,.065)
G['ClosedLowElectronicsChassis']=extrude(CHASSIS,.16,.34,'z',0,'Complete closed chamfered low robot electronics housing; no internal equipment claims')
SOLID_VOLUMES['ClosedLowElectronicsChassis']=dict(extrude(offset(CHASSIS,.002),.162,.338,'z'),targets=['ClosedLowElectronicsChassis'])
for tag,y in [('Forward',-.47),('Aft',.47)]:
 axle=tag+'FullAxle';block(axle,(-.55,y-.03,.10),(.55,y+.03,.16),4,'Whole continuous transverse static axle bar under chassis')
 seat(tag+'AxleWholeChassisSeat',axle,'ClosedLowElectronicsChassis',.16,1.0*.06)
 for side,x in [('Left',-.62),('Right',.62)]:
  n=tag+side+'Wheel';G[n]=disk_x(x,y,WHEEL_R,.14,3);FEET.append(n);SOLID_VOLUMES[n]=dict(disk_x(x,y,WHEEL_R,.14,3,.0015),targets=[n])
  a,b=(n,axle) if x<0 else (axle,n);contact(n+'WholeAxleEnd',a,b,(1,0,0),-.55 if x<0 else .55,(0,1,0),(0,0,1),.06*.06)
  hn=tag+side+'Hub';hx=-.701 if x<0 else .701;G[hn]=disk_x(hx,y,HUB_R,.022,4);SOLID_VOLUMES[hn]=dict(disk_x(hx,y,HUB_R,.022,4,.001),targets=[hn])
  a,b=(hn,n) if x<0 else (n,hn);contact(hn+'WholeBack',a,b,(1,0,0),-.69 if x<0 else .69,(0,1,0),(0,0,1),POLYAREA(HUB_R))
for x,side in [(-.36,'Left'),(.36,'Right')]:
 for y,end in [(-.47,'Forward'),(.47,'Aft')]:
  n=end+side+'DeckPedestal';block(n,(x-.05,y-.06,.34),(x+.05,y+.06,.41),2,'Whole short deck pedestal; visibly separates broad loading deck from low housing')
  seat(n+'WholeLowerSeat','ClosedLowElectronicsChassis',n,.34,.10*.12)
  seat(n+'WholeUpperSeat',n,'IndependentWideLoadingDeck',.41,.10*.12)
DECK=chamfer(.72,.90,.10)
G['IndependentWideLoadingDeck']=extrude(DECK,.41,.47,'z',1,'Single continuous broad empty octagonal loading deck with open front, no cargo')
SOLID_VOLUMES['IndependentWideLoadingDeck']=dict(extrude(offset(DECK,.002),.412,.468,'z'),targets=['IndependentWideLoadingDeck'])
for tag,y0,y1 in [('Front',-.78,-.69),('Rear',.69,.78)]:
 n=tag+'ExternalGuard';block(n,(-.42,y0,.20),(.42,y1,.32),2,'Separate thick protective-looking lower exterior guard; no protection certification')
 a,b=(n,'ClosedLowElectronicsChassis') if tag=='Front' else ('ClosedLowElectronicsChassis',n);contact(n+'FullInnerBack',a,b,(0,1,0),-.69 if tag=='Front' else .69,(1,0,0),(0,0,-1),.84*.12)
for side,x0,x1 in [('Left',-.56,-.50),('Right',.50,.56)]:
 n=side+'ExternalGuard';block(n,(x0,-.29,.20),(x1,.29,.32),2,'Separate thick side guard with full back seat and positive wheel clearance')
 a,b=(n,'ClosedLowElectronicsChassis') if side=='Left' else ('ClosedLowElectronicsChassis',n);contact(n+'FullInnerBack',a,b,(1,0,0),-.50 if side=='Left' else .50,(0,1,0),(0,0,1),.58*.12)
for side,x in [('Left',-.675),('Right',.675)]:
 n=side+'LowDeckEdgeStop';block(n,(x-.025,-.70,.47),(x+.025,.70,.53),0,'Low fixed deck-edge stop along one long side; full ground-to-deck support')
 seat(n+'WholeFoot','IndependentWideLoadingDeck',n,.47,.05*1.40)
block('RearLowDeckEdgeStop',(-.52,.83,.47),(.52,.88,.53),0,'Low rear end stop with full finite loading-deck seat')
seat('RearStopWholeFoot','IndependentWideLoadingDeck','RearLowDeckEdgeStop',.47,1.04*.05)
block('OpaqueFrontIdentificationPanel',(-.16,-.794,.238),(.16,-.78,.288),4,'Fully backed front plaque appearance; no display, sensor or controls claim')
contact('FrontPanelWholeBack','OpaqueFrontIdentificationPanel','FrontExternalGuard',(0,1,0),-.78,(1,0,0),(0,0,-1),.32*.05)
# Full finite empty domains for visually meaningful negative spaces.
VOID_VOLUMES['BroadEmptyLoadingSpace']=dict(boxg((-.64,-.899,.472),(.64,.828,.75)),targets=list(G))
VOID_VOLUMES['UnderDeckCentralAir']=dict(boxg((-.498,-.408,.342),(.498,.408,.408)),targets=list(G))
VOID_VOLUMES['UnderHousingCenterAir']=dict(boxg((-.498,-.438,.001),(.498,.438,.158)),targets=list(G))
for side,lo,hi in [('Left',-.548,-.502),('Right',.502,.548)]:
 for tag,y in [('Forward',-.47),('Aft',.47)]:
  VOID_VOLUMES[side+tag+'WholeWheelBodyGap']=dict(boxg((lo,y-.12,.162),(hi,y+.12,.238)),targets=list(G))
GROUND_AREA=.14*2*WHEEL_R*math.sin(math.pi/12)
def measurements():
 vv=[p for g in G.values() for p in g['vertices']];lo=[min(p[k] for p in vv) for k in range(3)];hi=[max(p[k] for p in vv) for k in range(3)]
 return {'bounds_min_m':lo,'bounds_max_m':hi,'bounds_m':[round(b-a,9) for a,b in zip(lo,hi)],'mesh_count':len(G),'triangles':sum(len(g['faces']) for g in G.values()),'materials':5,'single_prop_count':1,'ground_wheels':4,'complete_axles':2,'independent_wide_deck':True,'complete_deck_pedestals':4,'separate_exterior_guards':4,'low_deck_edge_stops':3,'wheel_body_lateral_gap_m':.05,'deck_separation_height_m':.07,'per_wheel_ground_sole_area_m2':GROUND_AREA,'old_geometry_imports':0}
# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
scene=bpy.context.scene
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
bpy.context.preferences.filepaths.save_version=0
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p and not any(n.type.startswith('TEX_') for n in m.node_tree.nodes) and not any(s.is_linked for s in p.inputs)
 values={}
 for n in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  v=p.inputs[n].default_value;values[n]=[round(float(x),6) for x in v] if hasattr(v,'__len__') else round(float(v),6)
 assert values['Alpha']==1 and values['Transmission Weight']==0 and values['Emission Strength']==0
 values['double_sided']=not m.use_backface_culling;return values

def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices];rows.append((o.name,min(tuple(q[i:]+q[:i]) for i in range(3)),json.dumps(pbr(o.data.materials[t.material_index]),sort_keys=True)))
 return sorted(rows)
def fingerprint(objects):return hashlib.sha256(json.dumps(records(objects),separators=(',',':')).encode()).hexdigest()
if not any(flag in sys.argv for flag in ['--render-only','--gray-only','--preview-only','--extra-views']):
 mats=[]
 for name,color,rough,metal in PALETTE:
  m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
  p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
 root=bpy.data.objects.new('OneLowDeckTransportPlatform',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['origin_datum']='wheelbase center at ground Z=0';root['front_direction']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
 parts=[];checks=[]
 for name,g in G.items():
  me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o['component_role']=g['role'];parts.append(o)
  for m in mats:me.materials.append(m)
  for face in me.polygons:face.material_index=g['material'];face.use_smooth=False
  bm=bmesh.new();bm.from_mesh(me);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();me.calc_loop_triangles();deg=sum(t.area<1e-12 for t in me.loop_triangles);assert not bad and not deg and volume>0
  checks.append({'name':name,'nonmanifold_edges':bad,'signed_volume_m3':volume,'degenerate_triangles':deg,'triangles':len(me.loop_triangles)})
 bpy.context.view_layer.update();source_fp=fingerprint(parts)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts+[root]:o.select_set(True)
 bpy.context.view_layer.objects.active=root
 bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
 guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
 qa={'asset':ASSET,'review_basis':'maker-self-reviewed','blender':bpy.app.version_string,'triangles':measurements()['triangles'],'materials':5,'mesh_objects':len(G),'bounds_m':measurements()['bounds_m'],'measurements':measurements(),'components':checks,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'geometry produced; full gates pending'}
else:qa=json.loads((OUT/'qa-report.json').read_text());source_fp=qa['world_oriented_triangle_full_solid_pbr_sha256']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];assert fingerprint(parts)==source_fp
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'oriented_geometry_and_full_constant_pbr_and_names_match':True,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'mesh_count':len(parts)}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/robotics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 ms=measurements();d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'robotics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],ms['bounds_m']),unit='m'),'triangles':ms['triangles'],'materials':5,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
saveqa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,measurements());sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset';m=bpy.data.materials.new('Preview_slate');m.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(m)
original_material_inputs={m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
 assert fingerprint(parts)==source_fp,'Diagnostic restoration changed complete geometry and constant PBR signature'
try:
 gray='--gray-only' in sys.argv
 if gray:
  for m in asset_mats:m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1)
 views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
 if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
 if '--extra-views' in sys.argv:views.pop('thumbnail',None)
 seconds={};configs={}
 def render(name,pos):
  aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
 for name,pos in views.items():
  if name=='qa-wireframe':
   wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
   for o in parts:
    dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
    for face in dup.data.polygons:face.material_index=0
    wire=dup.modifiers.new('Preview_actual_edges','WIREFRAME');wire.thickness=WIRE_THICKNESS;wire.use_replace=True;wire.use_even_offset=False;wire.offset=1
  render(name,pos)
 if gray:
  black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
  for o in parts:
   o.data.materials.clear();o.data.materials.append(black)
   for face in o.data.polygons:face.material_index=0
  ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
  for name in ['silhouette-128-front','silhouette-128-side']:render(name,CAMERAS[name])
finally:
 restore_diagnostic_materials()
 qa['diagnostic_exact_restoration']={'full_oriented_geometry_and_pbr_records_match':True,'all_original_slots_and_face_assignments_restored':True}
qa.setdefault('render_seconds',{}).update(seconds);qa.setdefault('render_configs',{}).update(configs);qa['status']='maker-self-reviewed render data produced; visual and full geometry acceptance separate';saveqa()
if not gray:metadata()
print('ASSET_RENDER_COMPLETE',ASSET,seconds)
