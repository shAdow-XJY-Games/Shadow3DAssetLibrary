"""Original fixed half-open irrigation sluice. One static architectural module.
Complete U waterway, open guide channels, thick gate, visible helical spindle,
through-bored crosshead and four-aperture handwheel. No flow or moving parts.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-fixed-half-open-sluice-gate-01';VERSION='1.0.0';TITLE='Fixed Half-Open Irrigation Sluice Gate'
DESCRIPTION=('One original static irrigation sluice architectural module with one continuous grounded U-shaped concrete-look channel, two true inward-open C-section guide rails, a thick fixed half-open gate, a vertical visibly helical spindle, a through-bored crosshead and one four-aperture handwheel. The complete under-gate passage is genuinely empty; no water surface is included. Seven independently editable closed meshes, four opaque constant PBR materials, metres, native Z up, front -Y and horizontal envelope centred at ground. Half-open describes this fixed displayed pose only. One modular asset with its own finite channel ends, no compatibility with older modules asserted. No flow, water retention, seal, hydrology, thread mating, motion, rigging, collision, physics, load, stability, civil engineering, manufacture, installation, operation or waterworks safety guarantee. No irrigation network, terrain scene, variants or separately counted components.')
PALETTE=[('WarmCastConcreteAppearance',(.42,.415,.35,1),.88,0),('DeepTealGateAndGuides',(.045,.19,.18,1),.59,.38),('SatinSpindleSteel',(.33,.38,.39,1),.42,.7),('OchreHandwheel',(.50,.285,.07,1),.54,.45)]
G={};CONTACTS=[];FEET=['ContinuousUChannel'];SOLID_VOLUMES={};VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
FOCUS=(0,0,.98);ORTHO=2.95;WIRE_THICKNESS=.0013
CAMERAS={'gray-front3q':(3.4,-5.1,3.3),'gray-back3q':(-3.4,5.1,3.3),'thumbnail':(3.4,-5.1,3.3),'qa-front':(0,-7,1.8),'qa-side':(7,0,1.8),'qa-top':(0,0,7),'qa-back':(0,7,1.8),'qa-wireframe':(3.4,-5.1,3.3),'silhouette-128-front':(0,-7,1.8),'silhouette-128-side':(7,0,1.8)}
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
  p,u=lines[i-1];den=u[0]*v[1]-u[1]*v[0];t=((q[0]-p[0])*v[1]-(q[1]-p[1])*v[0])/den;out.append((p[0]+t*u[0],p[1]+t*u[1]))
 return out
CHANNEL=[(-.75,0),(.75,0),(.75,.82),(.57,.82),(.57,.14),(-.57,.14),(-.57,.82),(-.75,.82)]
LEFT=[(-.57,-.09),(-.47,-.09),(-.47,-.052),(-.53,-.052),(-.53,.052),(-.47,.052),(-.47,.09),(-.57,.09)]
GATE=[(-.515,.48),(.515,.48),(.515,1.26),(.495,1.28),(-.495,1.28),(-.515,1.26)]
G['ContinuousUChannel']=extrude(CHANNEL,-.65,.65,'y',0,'One continuous thick U channel; real ground sole, bottom and opposed walls; both longitudinal ends remain open')
G['OpenCGuide_Left']=extrude(LEFT,.14,1.70,'z',1,'Continuous inward-open C guide, true 60mm deep by 104mm broad groove')
G['OpenCGuide_Right']=extrude([(-x,y) for x,y in LEFT],.14,1.70,'z',1,'Mirrored inward-open C guide with genuine groove')
G['ThickHalfOpenGate']=extrude(GATE,-.043,.043,'y',1,'One complete 86mm thick plate in a fixed raised pose, .34m clear above channel floor')
N=16
ANGLES=[math.tau*i/N for i in range(N)]
def ring_rectangle(z0,z1,hx,hy,r,mat=1):
 m=Mesh();outer=[(hx,0),(hx,hy/2),(hx,hy),(hx/2,hy),(0,hy),(-hx/2,hy),(-hx,hy),(-hx,hy/2),(-hx,0),(-hx,-hy/2),(-hx,-hy),(-hx/2,-hy),(0,-hy),(hx/2,-hy),(hx,-hy),(hx,-hy/2)];inner=[(r*math.cos(t),r*math.sin(t)) for t in ANGLES]
 for z in [z0,z1]:
  for i in range(N):j=(i+1)%N;m.quad([(*outer[i],z),(*outer[j],z),(*inner[j],z),(*inner[i],z)])
 for poly in [outer,inner]:
  for i in range(N):j=(i+1)%N;m.quad([(*poly[i],z0),(*poly[j],z0),(*poly[j],z1),(*poly[i],z1)])
 return m.result(mat,'One thick crosshead with real sixteen-sided through hole, complete outer and inner walls')
G['BoredCrosshead']=ring_rectangle(1.70,1.82,.65,.12,.027)
def spindle(inset=0):
 m=Mesh();rings=[]
 stations=[(1.28+inset,.019-inset,'round')]
 for j in range(33):stations.append((1.30+j*.38/32,.019-inset,'thread'))
 stations += [(1.70,.019-inset,'round'),(1.82+inset,.019-inset,'round'),(1.82+inset,.052-inset,'round'),(1.865-inset,.052-inset,'round'),(1.865-inset,.024-inset,'round'),(1.94-inset,.024-inset,'round')]
 for z,r,mode in stations:
  rings.append([( (r+(0.004*max(0.,1-abs(((t/math.tau-(z-1.30)/.0475+.5)%1)-.5)*4) if mode=='thread' else 0))*math.cos(t),(r+(0.004*max(0.,1-abs(((t/math.tau-(z-1.30)/.0475+.5)%1)-.5)*4) if mode=='thread' else 0))*math.sin(t),z) for t in ANGLES])
 for k in [0,len(rings)-1]:
  for tri in earclip([(x,y) for x,y,z in rings[k]]):m.tri([rings[k][i] for i in tri])
 for a,b in zip(rings,rings[1:]):
  for i in range(N):j=(i+1)%N;m.quad([a[i],a[j],b[j],b[i]])
 return m.result(2,'One closed vertical spindle with eight visible helical ridge turns, smooth guide-neck, integral bearing shoulder and top wheel seat; no threaded fit or operation claim')
G['HelicalSpindleAndCollar']=spindle()
def wheel(inset=0):
 m=Mesh();n=32;zs=[1.94+inset,1.99-inset];radii=[0,.05-inset,.16+inset,.20-inset]
 # Adjacent polar cells have shared complete faces; only the boundary is emitted.
 ang=[-math.pi/16+math.tau*i/n + (inset/.16 if i%8==0 else -inset/.16 if i%8==2 else 0) for i in range(n)]
 p=lambda k,i,z:(radii[k]*math.cos(ang[i%n]),radii[k]*math.sin(ang[i%n]),z)
 occupied={(k,i) for k in range(3) for i in range(n) if k in [0,2] or i%8 in [0,1]}
 for k,i in occupied:
  j=(i+1)%n
  for z in zs:
   if k==0:m.tri([p(0,i,z),p(1,i,z),p(1,j,z)])
   else:m.quad([p(k,i,z),p(k+1,i,z),p(k+1,j,z),p(k,j,z)])
  if k>0 and (k-1,i) not in occupied:m.quad([p(k,i,zs[0]),p(k,j,zs[0]),p(k,j,zs[1]),p(k,i,zs[1])])
  if (k+1,i) not in occupied:m.quad([p(k+1,i,zs[0]),p(k+1,j,zs[0]),p(k+1,j,zs[1]),p(k+1,i,zs[1])])
  if (k,(i-1)%n) not in occupied:m.quad([p(k,i,zs[0]),p(k+1,i,zs[0]),p(k+1,i,zs[1]),p(k,i,zs[1])])
  if (k,j) not in occupied:m.quad([p(k,j,zs[0]),p(k+1,j,zs[0]),p(k+1,j,zs[1]),p(k,j,zs[1])])
 return m.result(3,'One continuous four-spoke annular handwheel, four true through apertures and finite hub underside seat')
G['FourApertureHandwheel']=wheel()

def contact(name,a,b,axis,plane,u,v,area):
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'plane_m':plane,'u':u,'v':v,'minimum_patch_area_m2':area-2e-7,'interior_probe_offset_m':.001,'points':[]})
C_AREA=.1*.18-.06*.104
for side in ['Left','Right']:
 n='OpenCGuide_'+side
 contact('GuideFloorSeat_'+side,'ContinuousUChannel',n,(0,0,1),.14,(1,0,0),(0,1,0),C_AREA)
 contact('CrossheadSeat_'+side,n,'BoredCrosshead',(0,0,1),1.70,(1,0,0),(0,1,0),C_AREA)
 # Whole side-wall finite face contact; open inner channel and thickness remain explicit.
 sign=1 if side=='Left' else -1
 contact('GuideWallSeat_'+side,'ContinuousUChannel',n,(sign,0,0),-.57,(0,1,0),(0,0,sign),.18*.68)
contact('GateSpindleSeat','ThickHalfOpenGate','HelicalSpindleAndCollar',(0,0,1),1.28,(1,0,0),(0,1,0),N*.019*.019*math.sin(math.tau/N)/2)
contact('SpindleShoulderSeat','BoredCrosshead','HelicalSpindleAndCollar',(0,0,1),1.82,(1,0,0),(0,1,0),N*(.052**2-.027**2)*math.sin(math.tau/N)/2)
contact('WheelHubSeat','HelicalSpindleAndCollar','FourApertureHandwheel',(0,0,1),1.94,(1,0,0),(0,1,0),N*.024*.024*math.sin(math.tau/N)/2)
for name,poly,a,b,axis in [('ContinuousUChannel',CHANNEL,-.65,.65,'y'),('OpenCGuide_Left',LEFT,.14,1.70,'z'),('OpenCGuide_Right',[(-x,y) for x,y in LEFT],.14,1.70,'z'),('ThickHalfOpenGate',GATE,-.043,.043,'y')]:SOLID_VOLUMES[name]=dict(extrude(offset(poly,.002),a+.002,b-.002,axis),targets=[name])
SOLID_VOLUMES['BoredCrosshead']=dict(ring_rectangle(1.702,1.818,.648,.118,.029),targets=['BoredCrosshead'])
SOLID_VOLUMES['HelicalSpindleAndCollar']=dict(spindle(.0004),targets=['HelicalSpindleAndCollar'])
SOLID_VOLUMES['FourApertureHandwheel']=dict(wheel(.001),targets=['FourApertureHandwheel'])
def boxg(lo,hi):return extrude([(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],'z')
for label,y0,y1,x in [('Front',-.67,-.093,.567),('Centre',-.093,.093,.467),('Rear',.093,.67,.567)]:VOID_VOLUMES['WholeUnderGatePassage_'+label]=dict(boxg((-x,y0,.143),(x,y1,.477)),targets=list(G))
for label,y0,y1 in [('Front',-.67,-.093),('Rear',.093,.67)]:VOID_VOLUMES['WholeUpperChannelAir_'+label]=dict(boxg((-.567,y0,.477),(.567,y1,.817)),targets=list(G))
for side in ['Left','Right']:
 sx=-1 if side=='Left' else 1;poly=LEFT if sx<0 else [(-x,y) for x,y in LEFT]
 x0,x1=sorted([sx*.527,sx*.518]);VOID_VOLUMES['WholeGateRearGrooveClearance_'+side]=dict(boxg((x0,-.049,.143),(x1,.049,1.697)),targets=list(G))
 x0,x1=sorted([sx*.527,sx*.467]);ISOLATED_VOID_VOLUMES['WholeIsolatedGuideGroove_'+side]=dict(boxg((x0,-.049,.13),(x1,.049,1.71)),targets=['OpenCGuide_'+side])
def annulus_wedge(r0,r1,t0,t1,z0,z1,n=8):
 angles=[t0+(t1-t0)*i/n for i in range(n+1)];poly=[(r1*math.cos(t),r1*math.sin(t)) for t in angles]+[(r0*math.cos(t),r0*math.sin(t)) for t in reversed(angles)];return extrude(poly,z0,z1,'z')
for i in range(4):VOID_VOLUMES['WholeWheelAperture_'+str(i+1)]=dict(annulus_wedge(.053,.156,math.radians(13)+i*math.pi/2,math.radians(77)+i*math.pi/2,1.935,1.995),targets=list(G))
# True crosshead bore: full isolated hole, plus assembled residual annular clearance.
poly=[(.026*math.cos(t),.026*math.sin(t)) for t in ANGLES]
ISOLATED_VOID_VOLUMES['WholeIsolatedCrossheadBore']=dict(extrude(poly,1.69,1.83,'z'),targets=['BoredCrosshead'])
def annulus(r0,r1,z0,z1):
 m=Mesh();circles=[[(r*math.cos(t),r*math.sin(t)) for t in ANGLES] for r in [r0,r1]]
 for z in [z0,z1]:
  for i in range(N):j=(i+1)%N;m.quad([(*circles[0][i],z),(*circles[1][i],z),(*circles[1][j],z),(*circles[0][j],z)])
 for poly in circles:
  for i in range(N):j=(i+1)%N;m.quad([(*poly[i],z0),(*poly[j],z0),(*poly[j],z1),(*poly[i],z1)])
 return m.result(0,'Complete closed annular finite volume')
VOID_VOLUMES['WholeAssembledCrossheadNeckClearance']=dict(annulus(.0205,.025,1.702,1.818),targets=list(G))
def measurements():
 vv=[p for g in G.values() for p in g['vertices']];lo=[min(p[k] for p in vv) for k in range(3)];hi=[max(p[k] for p in vv) for k in range(3)]
 return {'bounds_min_m':lo,'bounds_max_m':hi,'bounds_m':[round(b-a,9) for a,b in zip(lo,hi)],'mesh_count':len(G),'triangles':sum(len(g['faces']) for g in G.values()),'materials':4,'single_modular_count':1,'channel_internal_width_m':1.14,'channel_floor_z_m':.14,'fixed_gate_bottom_z_m':.48,'fixed_under_gate_height_m':.34,'gate_thickness_m':.086,'minimum_guided_throat_width_m':.94,'guide_groove_width_m':.104,'guide_groove_depth_m':.06,'spindle_helix_turns':8,'handwheel_opening_count':4,'old_geometry_imports':0}

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
 root=bpy.data.objects.new('OneFixedIrrigationSluice',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['origin_datum']='horizontal bounds centre at ground Z=0';root['front_direction']='-Y';root['static_visual_only']=True;root['render_contract']=json.dumps(guard(),sort_keys=True)
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
  files[role]={'path':f'assets/farming/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 ms=measurements();d={'id':ASSET,'version':VERSION,'category':'architecture','assetKind':'modular','theme':'farming','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],ms['bounds_m']),unit='m'),'triangles':ms['triangles'],'materials':4,'files':files,'status':'review','license':'All rights reserved'}
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
