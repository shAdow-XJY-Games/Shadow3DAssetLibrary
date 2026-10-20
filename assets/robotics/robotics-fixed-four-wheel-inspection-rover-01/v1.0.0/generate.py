"""Original four-wheel fixed inspection robot. One static visual prop.
All numerical shapes are authored here; no prior vehicle or camera mesh executes.
Native Z up, front -Y, origin centered between four ground soles.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='robotics-fixed-four-wheel-inspection-rover-01';VERSION='1.0.0';TITLE='Four-Wheel Mast Inspection Rover'
DESCRIPTION=('One original compact fixed inspection-robot visual prop. Four separate flat-facet polygonal wheels and four outer hub plates meet two continuous transverse axle bars below a chamfered low chassis. An independently editable continuous electronics housing has a broad lower shoulder and a tapered upper roof. A separate round mast seat, hexagonal upright and chamfered horizontal camera head form a clear elevated sensor silhouette. Two thick truly bored forward lens hoods surround separate fully backed recessed opaque lens discs. All nineteen meshes are closed, individually named and statically connected through complete finite opposed face patches. Five constant opaque unlinked PBR materials; no textures. Metres, native Z up, front -Y, ground origin centered between the wheel soles. Every profile and dimension is newly authored; no earlier vehicle, robot arm, trolley, camera, wheel or other geometry is imported, transformed or reused. One fixed static presentation only. No autonomy, operation, real sensing, optical imaging, communications, navigation, driving, steering, suspension, wheel motion, animation, rigging, power, controls, load capacity, stability, terrain suitability, manufacturing, safety or compatibility with prior mechanical assets is claimed.')
PALETTE=[('Housing_WarmIvory',(.72,.75,.68,1),.57,.12),('ChassisAndMast_DeepPetrol',(.035,.19,.20,1),.52,.32),('Wheels_Graphite',(.028,.037,.041,1),.84,0),('HubsAndHoods_SatinAlloy',(.39,.45,.46,1),.37,.68),('Lens_OpaqueSlateBlue',(.055,.135,.205,1),.30,.15)]
G={};CONTACTS=[];FEET=[];SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
FOCUS=(0,0,.55);ORTHO=1.72;WIRE_THICKNESS=.00085
CAMERAS={'gray-front3q':(3.5,-5,3.0),'gray-back3q':(-3.5,5,3.0),'thumbnail':(3.5,-5,3.0),'qa-front':(0,-6,1.55),'qa-side':(6,0,1.55),'qa-top':(0,0,6),'qa-back':(0,6,1.55),'qa-wireframe':(3.5,-5,3.0),'silhouette-128-front':(0,-6,1.55),'silhouette-128-side':(6,0,1.55)}
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
def rings_z(stations,mat,role):
 m=Mesh();rings=[[(x,y,z) for x,y in poly] for z,poly in stations]
 for k in [0,len(rings)-1]:
  for tri in earclip([(x,y) for x,y,z in rings[k]]):m.tri([rings[k][i] for i in tri])
 for a,b in zip(rings,rings[1:]):
  for i in range(len(a)):j=(i+1)%len(a);m.quad([a[i],a[j],b[j],b[i]])
 return m.result(mat,role)
def wheel(name,x,y,inset=0,hub=False):
 # A complete 16-sided horizontal bottom facet, not a point on the ground.
 r=(.18/math.cos(math.pi/16) if not hub else .086)-inset;cx=x;w=.14 if not hub else .024
 yz=circle((y,.18),r,16,math.pi/16)
 g=extrude(yz,cx-w/2+inset,cx+w/2-inset,'y',3 if hub else 2,'Complete flat-facet solid wheel' if not hub else 'Complete separate fixed outer hub disk')
 # extrude uses x/y local plane to form (Y,X,Z); swap first two axes.
 g['vertices']=[(p[1],p[0],p[2]) for p in g['vertices']];g['faces']=[tuple(reversed(f)) for f in g['faces']]
 return g

def hood(x,inset=0):
 n=16;outer=circle((x,1.02),.049-inset,n,math.pi/16);inner=circle((x,1.02),.037+inset,n,math.pi/16);y0=-.14+inset;y1=-.03-inset;m=Mesh()
 for y in [y0,y1]:
  for i in range(n):j=(i+1)%n;m.quad([(outer[i][0],y,outer[i][1]),(outer[j][0],y,outer[j][1]),(inner[j][0],y,inner[j][1]),(inner[i][0],y,inner[i][1])])
 for poly in [outer,inner]:
  for i in range(n):j=(i+1)%n;m.quad([(poly[i][0],y0,poly[i][1]),(poly[j][0],y0,poly[j][1]),(poly[j][0],y1,poly[j][1]),(poly[i][0],y1,poly[i][1])])
 return m.result(3,'Complete thick open camera hood with full through-bore and annular backing seat')

def contact(name,a,b,axis,plane,u,v,area):CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'plane_m':plane,'u':u,'v':v,'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.001,'points':[]})
POLYAREA=lambda r,n=16:n*r*r*math.sin(math.tau/n)/2
CHASSIS=chamfer(.31,.46,.065)
G['ChamferedLowChassis']=extrude(CHASSIS,.21,.29,'z',1,'One continuous low chamfered chassis with clear air below and outside wheels')
for label,y in [('Front',-.31),('Rear',.31)]:
 axle=label+'ContinuousAxle';G[axle]=boxg((-.34,y-.03,.15),(.34,y+.03,.21),3)
 contact(label+'AxleDeckFullSeat',axle,'ChamferedLowChassis',(0,0,1),.21,(1,0,0),(0,1,0),.62*.06)
 SOLID_VOLUMES[axle]=dict(boxg((-.338,y-.028,.152),(.338,y+.028,.208)),targets=[axle])
 for side,x in [('Left',-.41),('Right',.41)]:
  n=label+side+'Wheel';G[n]=wheel(n,x,y);FEET.append(n);SOLID_VOLUMES[n]=dict(wheel(n,x,y,.002),targets=[n])
  if x<0:contact(n+'AxleSeat',n,axle,(1,0,0),-.34,(0,1,0),(0,0,1),.06*.06)
  else:contact(n+'AxleSeat',axle,n,(1,0,0),.34,(0,1,0),(0,0,1),.06*.06)
  hn=label+side+'OuterHub';hx=-.492 if x<0 else .492;G[hn]=wheel(hn,hx,y,hub=True);SOLID_VOLUMES[hn]=dict(wheel(hn,hx,y,.001,True),targets=[hn])
  if x<0:contact(hn+'FullBack',hn,n,(1,0,0),-.48,(0,1,0),(0,0,1),POLYAREA(.086))
  else:contact(hn+'FullBack',n,hn,(1,0,0),.48,(0,1,0),(0,0,1),POLYAREA(.086))
BODY=[(.29,chamfer(.29,.425,.06)),(.43,chamfer(.29,.425,.06)),(.58,chamfer(.225,.345,.065))]
G['ContinuousSlopedElectronicsHousing']=rings_z(BODY,0,'One connected closed low electronics body with full chamfered plan, broad lower shoulder and tapered upper roof')
contact('HousingWholeBottom','ChamferedLowChassis','ContinuousSlopedElectronicsHousing',(0,0,1),.29,(1,0,0),(0,1,0),abs(area2(BODY[0][1])))
G['RoundMastSeat']=extrude(circle((0,.08),.085),.58,.64,'z',3,'Separate finite grounded-to-housing circular mast seat')
contact('MastSeatWholeBase','ContinuousSlopedElectronicsHousing','RoundMastSeat',(0,0,1),.58,(1,0,0),(0,1,0),POLYAREA(.085))
G['HexagonalSensorMast']=extrude(circle((0,.08),.033,6,math.pi/6),.64,.94,'z',1,'Separate continuous hexagonal short mast; static visual sensor mounting')
contact('HexMastWholeFoot','RoundMastSeat','HexagonalSensorMast',(0,0,1),.64,(1,0,0),(0,1,0),POLYAREA(.033,6))
HEAD=[(x,z+1.02) for x,z in chamfer(.18,.08,.025)]
G['ChamferedTwinCameraHead']=extrude(HEAD,-.03,.19,'y',0,'One complete horizontal camera housing with chamfered silhouette and independent mast interface')
contact('HexMastWholeHeadSeat','HexagonalSensorMast','ChamferedTwinCameraHead',(0,0,1),.94,(1,0,0),(0,1,0),POLYAREA(.033,6))
for side,x in [('Left',-.09),('Right',.09)]:
 hn=side+'OpenLensHood';ln=side+'RecessedOpaqueLens';G[hn]=hood(x);G[ln]=extrude(circle((x,1.02),.035,16,math.pi/16),-.055,-.03,'y',4,'Separate opaque lens-appearance solid with full rear support and real front recess; no optics')
 contact(hn+'WholeAnnularBack',hn,'ChamferedTwinCameraHead',(0,1,0),-.03,(1,0,0),(0,0,-1),POLYAREA(.049)-POLYAREA(.037))
 contact(ln+'WholeBack',ln,'ChamferedTwinCameraHead',(0,1,0),-.03,(1,0,0),(0,0,-1),POLYAREA(.035))
 SOLID_VOLUMES[hn]=dict(hood(x,.0015),targets=[hn]);SOLID_VOLUMES[ln]=dict(extrude(circle((x,1.02),.0335,16,math.pi/16),-.0535,-.0315,'y'),targets=[ln])
 VOID_VOLUMES[side+'WholeRecessAir']=dict(extrude(circle((x,1.02),.0355,16,math.pi/16),-.142,-.0565,'y'),targets=list(G))
 ISOLATED_VOID_VOLUMES[side+'CompleteHoodBore']=dict(extrude(circle((x,1.02),.0355,16,math.pi/16),-.142,-.028,'y'),targets=[hn])
# Every eye air domain is tested against the final complete assembly.
for g in VOID_VOLUMES.values():g['targets']=list(G)
SOLID_VOLUMES['ChamferedLowChassis']=dict(extrude(offset(CHASSIS,.002),.212,.288,'z'),targets=['ChamferedLowChassis'])
SOLID_VOLUMES['ContinuousSlopedElectronicsHousing']=dict(rings_z([(.292,offset(BODY[0][1],.003)),(.429,offset(BODY[1][1],.003)),(.578,offset(BODY[2][1],.003))],0,'whole inset sloped material volume'),targets=['ContinuousSlopedElectronicsHousing'])
SOLID_VOLUMES['RoundMastSeat']=dict(extrude(circle((0,.08),.083),.582,.638,'z'),targets=['RoundMastSeat'])
SOLID_VOLUMES['HexagonalSensorMast']=dict(extrude(circle((0,.08),.031,6,math.pi/6),.642,.938,'z'),targets=['HexagonalSensorMast'])
SOLID_VOLUMES['ChamferedTwinCameraHead']=dict(extrude(offset(HEAD,.002),-.028,.188,'y'),targets=['ChamferedTwinCameraHead'])
VOID_VOLUMES['WholeOpenUnderDeckCenter']=dict(boxg((-.308,-.278,.001),(.308,.278,.208)),targets=list(G))
for side,lo,hi in [('Left',-.338,-.312),('Right',.312,.338)]:
 for label,y in [('Front',-.31),('Rear',.31)]:
  VOID_VOLUMES[side+label+'WholeUpperWheelChassisClearance']=dict(boxg((lo,y-.12,.212),(hi,y+.12,.358)),targets=list(G))
GROUND_AREA=.14*2*(.18/math.cos(math.pi/16))*math.sin(math.pi/16)
def measurements():
 vv=[p for g in G.values() for p in g['vertices']];lo=[min(p[k] for p in vv) for k in range(3)];hi=[max(p[k] for p in vv) for k in range(3)]
 return {'bounds_min_m':lo,'bounds_max_m':hi,'bounds_m':[round(b-a,9) for a,b in zip(lo,hi)],'mesh_count':len(G),'triangles':sum(len(g['faces']) for g in G.values()),'materials':5,'single_prop_count':1,'ground_wheels':4,'complete_axles':2,'independent_chassis_and_body':True,'independent_mast_and_head':True,'genuine_open_camera_hoods':2,'opaque_recessed_lens_discs':2,'minimum_wheel_chassis_lateral_clearance_m':.03,'hood_wall_radial_thickness_m':.012,'lens_front_recess_m':.085,'per_wheel_ground_sole_area_m2':GROUND_AREA,'old_geometry_imports':0}
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
 root=bpy.data.objects.new('OneFixedInspectionRover',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['origin_datum']='wheelbase center at ground Z=0';root['front_direction']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
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
