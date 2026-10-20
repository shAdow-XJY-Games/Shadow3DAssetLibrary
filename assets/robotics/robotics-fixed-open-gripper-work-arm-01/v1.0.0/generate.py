"""Original fixed open-gripper work robot arm. One static visual prop.
All shapes are newly authored numerical meshes. No old asset geometry executes.
Ground origin is the base axis, native Z up, the arm extends toward +X.
Shoulder, elbow and wrist are bored lap joints held by complete finite collars.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='robotics-fixed-open-gripper-work-arm-01';VERSION='1.0.0';TITLE='Fixed Open-Gripper Work Robot Arm'
DESCRIPTION=('One original single static work robot arm with a broad round grounded base, a separate round turntable seat, a bored shoulder pedestal, two continuous thick bored arm links, a bored wrist carrier, three continuous collared pins, a palm block and two separate thick inward-stepped fingers with a genuinely open empty jaw. Each complete finite annular collar face is seated against its corresponding joint face; the smaller shafts have full circumferential clearance inside the true bores. Twelve independently editable closed meshes, four opaque constant unlinked PBR materials, metres, native Z up, origin at the base axis on ground, arm toward +X. All dimensions and shapes are original author design values. No old excavator, clamp, grabber, linkage, industrial scene or other geometry is imported or transformed. Only this fixed display pose is supplied. No rotation, motion range, animation, rigging, controls, programming, dynamics, grip force, torque, arbitrary-object compatibility, holding, lifting, loading, stability, anchoring, manufacturing, installation or industrial-equipment safety certification is claimed. The empty opening is visual geometry, not a certified gripper specification.')
PALETTE=[('Body_DeepPetrol',(.035,.17,.185,1),.48,.32),('Links_WarmOrange',(.73,.255,.055,1),.48,.30),('Pins_SatinSteel',(.40,.47,.50,1),.32,.72),('BaseAndPalm_Graphite',(.055,.073,.080,1),.62,.22)]
G={};CONTACTS=[];FEET=['RoundGroundBase'];SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
FOCUS=(.28,0,.66);ORTHO=1.9;WIRE_THICKNESS=.0010
CAMERAS={'gray-front3q':(3.5,-5.0,3.2),'gray-back3q':(-3.5,5.0,3.2),'thumbnail':(3.5,-5.0,3.2),'qa-front':(.28,-7,1.75),'qa-side':(7,0,1.75),'qa-top':(.28,0,7),'qa-back':(.28,7,1.75),'qa-wireframe':(3.5,-5.0,3.2),'silhouette-128-front':(.28,-7,1.75),'silhouette-128-side':(7,0,1.75)}
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
N=16;ANGLES=[math.tau*i/N for i in range(N)]
def ringplate(outer,inner,y0,y1,mat=0,role='complete bored plate'):
 m=Mesh()
 for y in [y0,y1]:
  for i in range(N):j=(i+1)%N;m.quad([(outer[i][0],y,outer[i][1]),(outer[j][0],y,outer[j][1]),(inner[j][0],y,inner[j][1]),(inner[i][0],y,inner[i][1])])
 for poly in [outer,inner]:
  for i in range(N):j=(i+1)%N;m.quad([(poly[i][0],y0,poly[i][1]),(poly[j][0],y0,poly[j][1]),(poly[j][0],y1,poly[j][1]),(poly[i][0],y1,poly[i][1])])
 return m.result(mat,role)
def circ(c,r):return [(c[0]+r*math.cos(t),c[1]+r*math.sin(t)) for t in ANGLES]
def standplate(c,bottom,y0,y1,R=.14,r=.05,inset=0,mat=0):
 x,z=c;poly=[(x+R*math.cos(t),z+R*math.sin(t)) for t in ANGLES[:9]]+[(x-R,bottom),(x-R/2,bottom),(x,bottom),(x+R/2,bottom),(x+R,bottom),(x+R,bottom+(z-bottom)/3),(x+R,bottom+2*(z-bottom)/3)]
 if inset:poly=offset(poly,inset)
 return ringplate(poly,circ(c,r+inset),y0+inset,y1-inset,mat,'Continuous upright with true complete bore and full flat lower seat')
def linkplate(a,b,y0,y1,R=.13,r=.05,inset=0,mat=1):
 m=Mesh();dx,dz=sub(b,a);L=math.hypot(dx,dz);d=(dx/L,dz/L);e=(-d[1],d[0]);R-=inset;r+=inset
 for c,sign in [(a,1),(b,-1)]:
  outer=[];inner=[]
  for t in ANGLES:
   co=math.cos(t);si=math.sin(t)
   # Two convex end cells share one complete subdivided midline; its
   # internal walls are omitted so the final link is one connected solid.
   ox=L/2 if co>=-1e-8 else R*co
   oz=R*si
   outer.append(add(c,add(mul(d,sign*ox),mul(e,sign*oz))))
   inner.append(add(c,add(mul(d,sign*r*co),mul(e,sign*r*si))))
  for y in [y0+inset,y1-inset]:
   for i in range(N):j=(i+1)%N;m.quad([(outer[i][0],y,outer[i][1]),(outer[j][0],y,outer[j][1]),(inner[j][0],y,inner[j][1]),(inner[i][0],y,inner[i][1])])
  for i in range(N):
   j=(i+1)%N
   if not(math.cos(ANGLES[i])>=-1e-8 and math.cos(ANGLES[j])>=-1e-8):m.quad([(outer[i][0],y0+inset,outer[i][1]),(outer[j][0],y0+inset,outer[j][1]),(outer[j][0],y1-inset,outer[j][1]),(outer[i][0],y1-inset,outer[i][1])])
   m.quad([(inner[i][0],y0+inset,inner[i][1]),(inner[j][0],y0+inset,inner[j][1]),(inner[j][0],y1-inset,inner[j][1]),(inner[i][0],y1-inset,inner[i][1])])
 return m.result(mat,'One complete continuous thick two-bore arm link, both holes have real full walls')
def profile_y(c,stations,mat=2):
 m=Mesh();rings=[[(c[0]+r*math.cos(t),y,c[1]+r*math.sin(t)) for t in ANGLES] for y,r in stations]
 for k in [0,len(rings)-1]:
  for tri in earclip([(x,z) for x,y,z in rings[k]]):m.tri([rings[k][i] for i in tri])
 for a,b in zip(rings,rings[1:]):
  for i in range(N):j=(i+1)%N;m.quad([a[i],a[j],b[j],b[i]])
 return m.result(mat,'One continuous closed shaft with three integral collars and four full bearing shoulder faces')
def jointpin(c,inset=0):
 a=.042-inset;b=.092-inset
 stations=[(-.19+inset,b),(-.15-inset,b),(-.15-inset,a),(0+inset,a),(0+inset,b),(.025-inset,b),(.025-inset,a),(.175+inset,a),(.175+inset,b),(.215-inset,b)]
 return profile_y(c,stations)
def cylinder_z(r,z0,z1,mat=0):return extrude(circ((0,0),r),z0,z1,'z',mat,'Complete round faceted disk with full flat upper and lower surfaces')
def boxg(lo,hi,mat=0):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z',mat)
A=(0,.55);B=(.24,1.18);C=(.85,1.08)
G['RoundGroundBase']=cylinder_z(.43,0,.12,3)
G['RoundTurntableSeat']=cylinder_z(.28,.12,.20,0)
G['BoredShoulderPedestal']=standplate(A,.20,-.15,0)
G['ContinuousUpperArm']=linkplate(A,B,.025,.175)
G['ContinuousForearm']=linkplate(B,C,-.15,0)
G['BoredWristCarrier']=standplate(C,.82,.025,.175,R=.12,mat=0)
for label,c in [('Shoulder',A),('Elbow',B),('Wrist',C)]:G[label+'CollaredPin']=jointpin(c)
G['ThickGripperPalm']=boxg((.71,-.06,.74),(.99,.235,.82),3)
LEFT=[(.71,.74),(.77,.74),(.77,.54),(.81,.52),(.81,.46),(.71,.46)]
RIGHT=[(1.70-x,z) for x,z in LEFT]
for n,poly in [('LeftOpenFinger',LEFT),('RightOpenFinger',RIGHT)]:G[n]=extrude(poly,-.025,.20,'y',2,'One complete thick inward-stepped finger; genuine empty opening to the opposite finger, fixed pose')
def contact(name,a,b,axis,plane,u,v,area):CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'plane_m':plane,'u':u,'v':v,'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.001,'points':[]})
POLYAREA=lambda r:N*r*r*math.sin(math.tau/N)/2
contact('TurntableFullSole','RoundGroundBase','RoundTurntableSeat',(0,0,1),.12,(1,0,0),(0,1,0),POLYAREA(.28))
contact('ShoulderFullFoot','RoundTurntableSeat','BoredShoulderPedestal',(0,0,1),.20,(1,0,0),(0,1,0),.28*.15)
for label,low,high in [('Shoulder','BoredShoulderPedestal','ContinuousUpperArm'),('Elbow','ContinuousForearm','ContinuousUpperArm'),('Wrist','ContinuousForearm','BoredWristCarrier')]:
 pin=label+'CollaredPin';ar=POLYAREA(.092)-POLYAREA(.05)
 # Basis u=X, v=-Z gives axis +Y. Interfaces are complete annular areas.
 contact(label+'OuterLow',pin,low,(0,1,0),-.15,(1,0,0),(0,0,-1),ar)
 contact(label+'InnerLow',low,pin,(0,1,0),0,(1,0,0),(0,0,-1),ar)
 contact(label+'InnerHigh',pin,high,(0,1,0),.025,(1,0,0),(0,0,-1),ar)
 contact(label+'OuterHigh',high,pin,(0,1,0),.175,(1,0,0),(0,0,-1),ar)
contact('WristPalmFullSeat','ThickGripperPalm','BoredWristCarrier',(0,0,1),.82,(1,0,0),(0,1,0),.24*.15)
for n in ['LeftOpenFinger','RightOpenFinger']:contact(n+'FullRoot',n,'ThickGripperPalm',(0,0,1),.74,(1,0,0),(0,1,0),.06*.225)
SOLID_VOLUMES['RoundGroundBase']=dict(cylinder_z(.428,.002,.118),targets=['RoundGroundBase'])
SOLID_VOLUMES['RoundTurntableSeat']=dict(cylinder_z(.278,.122,.198),targets=['RoundTurntableSeat'])
SOLID_VOLUMES['BoredShoulderPedestal']=dict(standplate(A,.20,-.15,0,inset=.002),targets=['BoredShoulderPedestal'])
SOLID_VOLUMES['ContinuousUpperArm']=dict(linkplate(A,B,.025,.175,inset=.002),targets=['ContinuousUpperArm'])
SOLID_VOLUMES['ContinuousForearm']=dict(linkplate(B,C,-.15,0,inset=.002),targets=['ContinuousForearm'])
SOLID_VOLUMES['BoredWristCarrier']=dict(standplate(C,.82,.025,.175,R=.12,inset=.002),targets=['BoredWristCarrier'])
for label,c in [('Shoulder',A),('Elbow',B),('Wrist',C)]:SOLID_VOLUMES[label+'CollaredPin']=dict(jointpin(c,.001),targets=[label+'CollaredPin'])
SOLID_VOLUMES['ThickGripperPalm']=dict(boxg((.712,-.058,.742),(.988,.233,.818)),targets=['ThickGripperPalm'])
for n,poly in [('LeftOpenFinger',LEFT),('RightOpenFinger',RIGHT)]:SOLID_VOLUMES[n]=dict(extrude(offset(poly,.002),-.023,.198,'y'),targets=[n])
for label,c,low,high in [('Shoulder',A,'BoredShoulderPedestal','ContinuousUpperArm'),('Elbow',B,'ContinuousForearm','ContinuousUpperArm'),('Wrist',C,'ContinuousForearm','BoredWristCarrier')]:
 for suffix,y0,y1,target in [('Low',-.15,0,low),('High',.025,.175,high)]:
  VOID_VOLUMES[label+suffix+'FullShaftRadialAir']=dict(ringplate(circ(c,.0485),circ(c,.0435),y0+.002,y1-.002),targets=list(G))
  ISOLATED_VOID_VOLUMES[label+suffix+'CompleteBore']=dict(extrude(circ(c,.0485),y0-.002,y1+.002,'y'),targets=[target])
VOID_VOLUMES['CompleteCentralOpenJaw']=dict(boxg((.812,-.027,.45),(.888,.202,.738)),targets=list(G))
VOID_VOLUMES['OpenLeftFingerUpperRecess']=dict(boxg((.772,-.027,.543),(.812,.202,.738)),targets=list(G))
VOID_VOLUMES['OpenRightFingerUpperRecess']=dict(boxg((.888,-.027,.543),(.928,.202,.738)),targets=list(G))
GROUND_AREA=POLYAREA(.43)
def measurements():
 vv=[p for g in G.values() for p in g['vertices']];lo=[min(p[k] for p in vv) for k in range(3)];hi=[max(p[k] for p in vv) for k in range(3)]
 return {'bounds_min_m':lo,'bounds_max_m':hi,'bounds_m':[round(b-a,9) for a,b in zip(lo,hi)],'mesh_count':len(G),'triangles':sum(len(g['faces']) for g in G.values()),'materials':4,'single_prop_count':1,'ground_base_radius_m':.43,'joint_count':3,'joint_through_bores':6,'full_finite_bearing_faces':12,'shaft_radius_m':.042,'bore_radius_m':.05,'nominal_radial_gap_m':.008,'open_finger_tip_gap_m':.08,'minimum_finger_thickness_m':.06,'base_sole_area_m2':GROUND_AREA,'old_geometry_imports':0}
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
 root=bpy.data.objects.new('OneStaticOpenGripperRobotArm',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['origin_datum']='base axis at ground Z=0';root['front_direction']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 qa={'asset':ASSET,'review_basis':'maker-self-reviewed','blender':bpy.app.version_string,'triangles':measurements()['triangles'],'materials':4,'mesh_objects':len(G),'bounds_m':measurements()['bounds_m'],'measurements':measurements(),'components':checks,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),'status':'geometry produced; full gates pending'}
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
 ms=measurements();d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'robotics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],ms['bounds_m']),unit='m'),'triangles':ms['triangles'],'materials':4,'files':files,'status':'review','license':'All rights reserved'}
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
