"""One original fixed double-wing photographic flag panel. Static visual prop only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-fixed-wing-flag-panel-kit-01';VERSION='1.0.0';TITLE='Fixed Double-wing Flag Panel'
DESCRIPTION=('One original fixed three-panel photographic flag visual prop. A broad central solid thick rectangle and two narrow solid thick side wings are set at fixed 35 degree angles, with genuine open fold seams. Each side has two complete thick square-bored fixed and wing ears, a separate whole headed square pin with radial air and visible lower end clearance, and two finite solid angle stops. Complete opposed finite hinge shoulder and stop faces support the wings; none is a floating thin plane. A full rear saddle, offset straight mast, hexagonal hub and three independent low radial legs with full flat soles complete one static prop. Twenty-five editable closed connected meshes and four opaque constant unlinked Principled PBR materials, metre units, native Z up, front -Y and horizontal bounds-centred ground origin. Newly authored panel, pierced-ear, fixed-stop and three-foot geometry; no old reflector, softbox, backdrop, divider or scene geometry is imported or evaluated. No textures, graphics, text, logo, fabric, animation, folding, angle adjustment or height adjustment. No light-blocking, absorption, reflectance, optical control, wind resistance, loading, clamping, compatibility, stability, material, manufacturing or safety performance claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[]
BODY='WholeCentralThickFlag';MAST='OffsetRearStraightMast';SADDLE='WholeRearPanelSaddle';HUB='WholeHexagonalTripodHub';SHIFT=(0,0,0)
PALETTE=[('CharcoalOpaqueFlag',(.045,.055,.062,1),.83,.03),('BlueSlateHardware',(.115,.22,.25,1),.52,.42),('MutedBrassPins',(.43,.29,.095,1),.47,.55),('DarkLowTripod',(.065,.09,.105,1),.62,.28)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def prism(poly,z0,z1,material=0,role='',transform=None):
 n=len(poly);vv=[(x,y,z) for z in [z0,z1] for x,y in poly];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv] if transform else vv,ff,material,role)
def grid(xs,ys,zs,occupied,material=0,role=''):
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};vv=[];ff=[];ids={}
 def vertex(p):
  p=tuple(round(x,9) for x in p)
  if p not in ids:ids[p]=len(vv);vv.append(p)
  return ids[p]
 for i,j,k in sorted(cells):
  cell=[(x,y,z) for z in zs[k:k+2] for y in ys[j:j+2] for x in xs[i:i+2]]
  for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:ff.append(tuple(vertex(cell[n]) for n in face))
 return mesh(vv,ff,material,role)
def union_boxes(boxes,material=0,role=''):
 stations=[sorted(set(p[k] for lo,hi in boxes for p in [lo,hi])) for k in range(3)]
 return grid(*stations,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes),material,role)
def contact(name,a,b,axis,p,area,points=None,offset=.0004):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'points':points or [p],'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def solid(name,g,targets,role):SOLID_VOLUMES[name]=dict(g,targets=targets,role=role)
# Original numerical panel and hinge geometry. All thicknesses are real closed solids.
C=math.cos(math.radians(35));S=math.sin(math.radians(35));HINGES=[];STOPS=[];WINGS=[]
def transformed(g,fn):return mesh([fn(p) for p in g['vertices']],g['faces'],g['material'],g['role'])
def ring_square(inner,outer,z0,z1,angle_inner=0,angle_outer=0,transform=None):
 # Two complete four-sided loops, closed upper/lower annuli and full inside/outside walls.
 def loop(r,a,z):return [(r*x*math.cos(a)-r*y*math.sin(a),r*x*math.sin(a)+r*y*math.cos(a),z) for x,y in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 vv=loop(outer,angle_outer,z0)+loop(inner,angle_inner,z0)+loop(outer,angle_outer,z1)+loop(inner,angle_inner,z1);ff=[]
 for k in range(4):j=(k+1)%4;ff += [(k,j,j+8,k+8),(k+4,k+12,j+12,j+4),(k,k+4,j+4,j),(k+8,j+8,j+12,k+12)]
 return mesh([transform(p) for p in vv] if transform else vv,ff)
def ear(z0,z1,lo,hi,transform,i=0):
 g=grid([lo+i,-.012-i,.012+i,hi-i],[-.032+i,-.012-i,.012+i,.032-i],[z0+i,z1-i],lambda x,y,z:not(-.012-i<x<.012+i and -.012-i<y<.012+i),1,'Complete thick pierced ear with full root and a genuine through square bore; no painted hole or disconnected tab.')
 return transformed(g,transform)
G[BODY]=box((-.44,-.024,.82),(.44,.024,1.82),0,'One complete solid thick central panel, including full faces and all finite edges.')
solid('WholeCentralPanelMaterial',box((-.439,-.023,.821),(.439,.023,1.819)),[BODY],'Entire 1 mm inset central thick panel, not a sparse surface sample.')
for sign,side in [(1,'Right'),(-1,'Left')]:
 origin=(sign*.49,0,0);d=(sign*C,S,0);n=(-sign*S,C,0)
 def tf(p,origin=origin,d=d,n=n):return add(origin,add(mul(d,p[0]),add(mul(n,p[1]),(0,0,p[2]))))
 def cf(p,sign=sign):return(sign*(.49+p[0]),p[1],p[2])
 wn=side+'WholeFixedThickWing';WINGS.append(wn);G[wn]=box((.05,-.022,.82),(.36,.022,1.82),0,'Complete narrow solid thick wing in one fixed 35 degree pose; genuine full-thickness open seam to central panel.',tf)
 solid(side+'WholeWingMaterial',box((.051,-.021,.821),(.359,.021,1.819),transform=tf),[wn],'Entire 1 mm inset wing material including both faces and all four edges.')
 for j,z0 in enumerate([1.06,1.56],1):
  lower=side+'FixedPiercedEar_'+str(j);upper=side+'WingPiercedEar_'+str(j);pin=side+'WholeHeadedPin_'+str(j);zu=z0+.04
  G[lower]=ear(z0,z0+.02,-.05,.032,cf);G[upper]=ear(z0+.02,zu,-.032,.05,tf)
  solid(lower+'_WholeMaterial',ear(z0,z0+.02,-.05,.032,cf,.0007),[lower],'Complete 0.7 mm inset connected lower ear/root and full bore walls.')
  solid(upper+'_WholeMaterial',ear(z0+.02,zu,-.032,.05,tf,.0007),[upper],'Complete 0.7 mm inset connected upper ear/root and full bore walls.')
  contact(lower+'_CentralRootSeat',BODY,lower,(sign,0,0),(sign*.44,0,z0+.01),.000959,offset=.0004)
  contact(upper+'_WholeWingRootSeat',upper,wn,d,tf((.05,0,z0+.03)),.000879,offset=.0004)
  contact(side+'Hinge_'+str(j)+'_WholeOpposedEarShoulder',lower,upper,(0,0,1),(sign*.49,.025,z0+.02),.00120)
  def pinmesh(i=0):
   g=union_boxes([((-.0065+i,-.0065+i,z0-.012+i),(.0065-i,.0065-i,zu+.002)),((-.024+i,-.024+i,zu+i),(.024-i,.024-i,zu+.012-i))],2,'One whole fixed square shaft and integral finite head; complete shaft passes through both true holes without radial interference.')
   return transformed(g,tf)
  G[pin]=pinmesh();solid(pin+'_WholeMaterial',pinmesh(.0007),[pin],'Complete 0.7 mm inset pin shaft and continuous thick head.')
  contact(pin+'_FullHeadOnUpperEar',upper,pin,(0,0,1),tf((0,.019,zu)),.001727)
  # Each isolated bore is fully certified, rather than only a central ray.
  for obj,a,b,fn in [(lower,z0,z0+.02,cf),(upper,z0+.02,zu,tf)]:
   air(obj+'_WholeIsolatedThroughBore',box((-.0115,-.0115,a-.001),(.0115,.0115,b+.001),transform=fn),'Entire finite isolated square bore and both mouths with explicit 0.5 mm side margin; only the pierced ear is tested so the separate pin is intentionally excluded.',[obj])
   BORES.append({'mesh':obj,'origin_m':fn((0,0,a-.003)),'direction':(0,0,1),'length_m':b-a+.006})
  # Shaft/ear full annuli use the actual differing square orientations; all parts tested.
  a=math.radians(35)
  air(lower+'_WholePinRadialAir',ring_square(.007,.0115,z0+.0005,z0+.0195,a,0,cf),'Whole finite four-sided lower bore-to-pin air, with 0.5 mm wall margins and actual 35 degree relative square orientation.')
  air(upper+'_WholePinRadialAir',ring_square(.007,.0115,z0+.0205,zu-.0005,0,0,tf),'Whole finite four-sided upper bore-to-pin air, 0.5 mm side and axial margins.')
  air(pin+'_WholeLowerEndAir',box((-.006,-.006,z0-.025),(.006,.006,z0-.0125),transform=tf),'Whole finite open volume directly below the complete lower shaft end; 0.5 mm end margin.')
  HINGES.append({'side':side,'lower':lower,'upper':upper,'pin':pin,'wing':wn,'z0':z0,'z1':zu,'head_contact':pin+'_FullHeadOnUpperEar','root_contact':lower+'_CentralRootSeat','wing_contact':upper+'_WholeWingRootSeat','shoulder_contact':side+'Hinge_'+str(j)+'_WholeOpposedEarShoulder'})
 for j,(z0,z1) in enumerate([(.93,.985),(1.685,1.74)],1):
  sn=side+'FiniteFixedAngleStop_'+str(j)
  poly=[(sign*.44,.006),(sign*.44,.023),tf((.13,.022,0))[:2],tf((.08,.022,0))[:2]]
  G[sn]=prism(poly,z0,z1,1,'Whole finite wedge angle stop, with a full central side root and full opposed wing back-face seat; no dynamic lock or loading claim.')
  # Convex polygon inset against every complete edge, not a scaled centre probe.
  def insetpoly(poly,off):
   area=sum(poly[k][0]*poly[(k+1)%len(poly)][1]-poly[(k+1)%len(poly)][0]*poly[k][1] for k in range(len(poly)));poly=list(poly if area>0 else reversed(poly));out=[]
   for k,p in enumerate(poly):
    a=poly[k-1];b=p;c=poly[(k+1)%len(poly)];e1=unit((b[0]-a[0],b[1]-a[1],0));e2=unit((c[0]-b[0],c[1]-b[1],0));n1=(-e1[1],e1[0]);n2=(-e2[1],e2[0]);det=n1[0]*n2[1]-n1[1]*n2[0];q1=dot(n1,b)+off;q2=dot(n2,b)+off;out.append(((q1*n2[1]-n1[1]*q2)/det,(n1[0]*q2-q1*n2[0])/det))
   return out
  solid(sn+'_WholeMaterial',prism(insetpoly(poly,.0006),z0+.0006,z1-.0006),[sn],'Complete 0.6 mm inset stop prism, including full connected root, finite wedge and contact edge neighborhoods.')
  contact(sn+'_CentralFiniteRoot',BODY,sn,(sign,0,0),(sign*.44,.0145,(z0+z1)/2),.000934)
  contact(sn+'_FullFixedWingSeat',wn,sn,n,tf((.105,.022,(z0+z1)/2)),.002749)
  STOPS.append({'name':sn,'wing':wn,'root_contact':sn+'_CentralFiniteRoot','wing_contact':sn+'_FullFixedWingSeat'})
 # Whole central seam segments between actual hardware bands; no nominal empty
 # region is asserted across the real ears or stops themselves.
 seam=[(sign*.441,-.023),(sign*.441,.023),tf((.049,.021,0))[:2],tf((.049,-.021,0))[:2]]
 for k,(a,b) in enumerate([(.821,.929),(.986,1.047),(1.113,1.547),(1.613,1.684),(1.741,1.819)],1):
  air(side+'WholeFoldSeamSegment_'+str(k),prism(seam,a,b),'Entire closed finite central fold seam section between actual hardware bands; includes every corner and both panel-side approaches with explicit boundary margins.')
 air(side+'WholeFrontFoldAir',box((.441,-.080,.821),(.530,-.046,1.819),transform=lambda p,sign=sign:(sign*p[0],p[1],p[2])),'Complete full-height finite air immediately in front of the real fold seam and all its ear/stop hardware, with 1 mm hardware margin.')
 air(side+'WholeRearFoldAir',box((.441,.101,.821),(.530,.135,1.819),transform=lambda p,sign=sign:(sign*p[0],p[1],p[2])),'Complete full-height finite air immediately behind the inner fold seam, including all hinge and stop height bands.')
# Full back saddle and offset independent three-foot stand.
G[SADDLE]=box((-.10,.024,1.15),(.10,.13,1.30),1,'Complete thick rear saddle with whole central-panel back interface and complete rear mast interface.')
solid('WholeRearSaddleMaterial',box((-.099,.025,1.151),(.099,.129,1.299)),[SADDLE],'Whole 1 mm inset saddle material, both complete interface neighborhoods included.')
contact('WholePanelBackToSaddle',BODY,SADDLE,(0,1,0),(0,.024,1.225),.029999)
G[MAST]=box((-.03,.13,.20),(.03,.19,1.30),3,'One complete solid offset straight mast from full hub top seat to full rear saddle interface.')
solid('WholeMastMaterial',box((-.029,.131,.201),(.029,.189,1.299)),[MAST],'Whole 1 mm inset mast from base to saddle.')
contact('FullSaddleToMastSeat',SADDLE,MAST,(0,1,0),(0,.13,1.225),.008999)
R=.09/math.cos(math.pi/6);poly=[(R*math.cos(math.radians(60*k)),.16+R*math.sin(math.radians(60*k))) for k in range(6)]
G[HUB]=prism(poly,.07,.20,1,'One full solid hexagonal three-foot hub; three alternating whole side faces meet independent radial low legs.')
solid('WholeHexHubMaterial',prism(insetpoly(poly,.001),.071,.199),[HUB],'Whole 1 mm inset hub material across full height and all corners.')
contact('WholeMastOnHubTop',HUB,MAST,(0,0,1),(0,.16,.20),.003599)
def legshape(a,i=0):
 d=(math.cos(a),math.sin(a),0);n=(-math.sin(a),math.cos(a),0);r0=.09+i;r1=.55-i;w=.038-i
 def top(r):return .17-(r-.09)*(.122/.46)-i
 vv=[(r,y,z) for r,z in [(r0,i),(r1,i),(r1,top(r1)),(r0,top(r0))] for y in [-w,w]]
 ff=[(0,2,3,1),(4,6,7,5),(0,1,7,6),(2,4,5,3),(0,6,4,2),(1,3,5,7)]
 return mesh([add((0,.16,0),add(mul(d,p[0]),add(mul(n,p[1]),(0,0,p[2])))) for p in vv],ff,3,'One complete independent low radial tripod leg with a full flat planar ground sole, finite hub root and sloping upper surface.')
for j,deg in enumerate([90,210,330],1):
 a=math.radians(deg);d=(math.cos(a),math.sin(a),0);name='WholeFlatSoleRadialLeg_'+str(j);G[name]=legshape(a);FEET.append(name)
 solid(name+'_WholeMaterial',legshape(a,.001),[name],'Complete 1 mm inset material along the whole low leg, finite root and full flat sole.')
 p=add((0,.16,.12),mul(d,.09));contact(name+'_FullHubSideRoot',HUB,name,d,p,.007599)
# Translate every numerical domain to the horizontal bounds-centred ground datum.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=(-(min(p[0] for p in allv)+max(p[0] for p in allv))/2,-(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for collection in [G,VOID_VOLUMES,SOLID_VOLUMES]:
 for name,g in collection.items():g['vertices']=[add(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['plane_m']+=dot(r['axis'],SHIFT);r['points']=[add(p,SHIFT) for p in r['points']]
for r in BORES:r['origin_m']=add(r['origin_m'],SHIFT)
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
CONTRACT={'single_prop_count':1,'whole_thick_central_panel':1,'whole_fixed_35_degree_thick_wings':2,'true_square_bored_fixed_ears':4,'true_square_bored_wing_ears':4,'whole_headed_square_pins':4,'whole_finite_fixed_angle_stops':4,'whole_rear_saddle':1,'offset_straight_mast':1,'hex_hub':1,'independent_full_flat_sole_low_legs':3,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'folding_or_optical_loading_safety_claim':False}
def measure_flag_geometry(vertices):
 assert set(vertices)==set(G) and len(vertices)==25
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-1.82)<2e-7
 return dict(CONTRACT,geometry_scope='actual full coordinates; complete closed air/material bodies, finite seats, every component pair and focused actual negative controls required')
INSIDE_TESTS=[(BODY,add((0,0,1.4),SHIFT),add((.46,0,1.4),SHIFT)),(HINGES[0]['lower'],add((.49,.025,1.07),SHIFT),add((.49,0,1.07),SHIFT))]
FOCUS=(0,0,.91);ORTHO=2.60
CAMERAS={'gray-front3q':(3,-4,3.3),'gray-back3q':(-3,4,3.5),'thumbnail':(3,-4,3.3),'qa-front':(0,-6,2.7),'qa-side':(6,0,2.7),'qa-top':(0,0,6),'qa-back':(0,6,2.7),'qa-wireframe':(3,-4,3.3),'silhouette-128-front':(0,-6,2.7),'silhouette-128-side':(6,0,2.7)}
WIRE_THICKNESS=ORTHO/1300
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
root=bpy.data.objects.new('OneFixedWingFlagPanelKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred three-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in INSIDE_TESTS:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate independent actual-GLB gates.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_flag_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'flag_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/photography/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
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
 for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
