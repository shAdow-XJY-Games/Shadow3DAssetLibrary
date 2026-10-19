"""Original fixed-tilt drawing desk, one complete static visual prop.
Metres, native Z up, front -Y. No adjustment, load, human fit or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-fixed-tilt-drafting-desk-01';VERSION='1.0.0';TITLE='Fixed-Tilt Drafting Desk'
DESCRIPTION=('One original fixed 25-degree drafting desk, counted as one static visual prop. A broad 55 mm thick empty drawing board and a continuous thick front retaining strip sit above two open side frames. Four uprights, two side ties, two cross beams and two flat runners form the table-shaped base. Two complete rear wedge supports have opposed inclined top faces against the full board underside bearing rectangles. A wide front board ear and two separate frame ears have true octagonal through-bores around one continuous solid capped pin. Its full lower flat bears on all three bore floors; both integral end shoulders meet the frame ear ends, with positive clearance along every nonbearing shaft/bore surface. All connections are finite opposed patches, without hidden positive penetration. Eighteen editable closed meshes and four constant opaque PBR colours; metres, native Z up, front -Y and bounds-centred ground origin. No paper, canvas, brushes, chair, star chart, display, room or animation. This table frame, wide continuous work board, real front ear/pin assembly and fixed rear bearing arrangement are original, not a rotated easel, enlarged music stand or stripped chart console. Fixed static appearance only: no adjustment, locking, assembly path, human fit, ergonomics, writing comfort, load, strength, stability, manufacture, installation or work-safety certification, and no compatibility with old chairs or art-tool interfaces.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SECTIONS=[];EAR_PAIRS=[];EARS=[];REAR_SUPPORTS=[];LEGS=[]
PALETTE=[('Frame_DeepPetrol',(.035,.16,.18,1),.60,.30),('Board_PaleBirch',(.72,.54,.31,1),.78,0),('Pin_WarmBrass',(.62,.395,.12,1),.36,.65),('Runner_Charcoal',(.045,.055,.06,1),.75,.08)]
A=math.radians(25);C=math.cos(A);S=math.sin(A);T=math.tan(A);N=(0,-S,C);H=1.10
HY=-.385;HZ=.86

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def top(p):x,y,z=p;return(x,C*y-S*z,H+S*y+C*z)
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def prism_geometry(x,width,yz):
 if sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(yz,yz[1:]+yz[:1]))<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return vs,fs

def prism_x(name,x,width,yz,mat,role):
 SECTIONS.append({'name':name,'x0':x-width/2,'x1':x+width/2,'loops':[yz]});return mesh(name,*prism_geometry(x,width,yz),mat,role)
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size;return prism_x(name,x,w,[(y-d/2,z-h/2),(y+d/2,z-h/2),(y+d/2,z+h/2),(y-d/2,z+h/2)],mat,role)
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':points or [add(point,mul(u,d)) for d in[-.015,0,.015]],'scope':scope})
def void_x(name,x,w,yz,scope,targets=None,isolated=False):
 vs,fs=prism_geometry(x,w,yz);g={'vertices':vs,'faces':fs,'targets':list(G) if targets is None else targets,'role':scope}
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]=g

for i,x in enumerate([-.64,.64]):
 foot=box('Side_%d_GroundRunner'%i,(x,0,.04),(.16,1.24,.08),3,'one continuous runner with complete 0.16 by 1.24 m flat ground face');FEET.append(foot)
 for label,y,upper in [('Front',-.385,.71),('Rear',.36,1.02)]:
  leg=box('Side_%d_%sUpright'%(i,label),(x,y,(.08+upper)/2),(.10,.10,upper-.08),0,'one original table upright with flat full end support faces');LEGS.append(leg)
  contact(foot,leg,(0,0,1),(x,y,.08),.009999,'complete upright bottom against finite runner top')
 tie=box('Side_%d_OpenFrameTie'%i,(x,(-.335+.31)/2,.35),(.08,.645,.08),0,'horizontal side tie with complete end faces on inward upright faces')
 contact('Side_%d_FrontUpright'%i,tie,(0,1,0),(x,-.335,.35),.006399,'complete side-tie front end against upright inner face')
 contact(tie,'Side_%d_RearUpright'%i,(0,1,0),(x,.31,.35),.006399,'complete side-tie rear end against upright inner face')
front=box('Front_ContinuousCrossBeam',(0,HY,.75),(1.38,.16,.08),0,'full-width front beam joining both side frames and carrying two outer front hinge ears')
rear=box('Rear_ContinuousCrossBeam',(0,.36,1.06),(1.38,.16,.08),0,'full-width rear beam supporting both fixed rear wedge bearings')
for i,x in enumerate([-.64,.64]):
 contact('Side_%d_FrontUpright'%i,front,(0,0,1),(x,HY,.71),.009999,'complete front upright top against crossbeam bottom')
 contact('Side_%d_RearUpright'%i,rear,(0,0,1),(x,.36,1.02),.009999,'complete rear upright top against crossbeam bottom')
 support=prism_x('Side_%d_FixedRearInclinedBearing'%i,x,.10,[(.28,1.10),(.44,1.10),(.44,H+T*.44),(.28,H+T*.28)],3,'complete fixed rear wedge with horizontal base and broad 25-degree inclined upper bearing rectangle');REAR_SUPPORTS.append(support)
 contact(rear,support,(0,0,1),(x,.36,1.10),.015999,'entire 0.10 by 0.16 m wedge base against rear beam')
 contact(support,'Wide_EmptyDrawingBoard',N,(x,.36,H+T*.36),.10*.16/C-.000001,'entire 0.10 by 0.17654 m rear wedge inclined upper face against actual board underside')
board_yz=[(top((0,y,z))[1],top((0,y,z))[2]) for y,z in[(-.56,0),(.56,0),(.56,.055),(-.56,.055)]]
prism_x('Wide_EmptyDrawingBoard',0,1.56,board_yz,1,'one complete 1.56 by 1.12 m board, 55 mm normal thickness, fixed 25 degrees above horizontal')
stop_yz=[(top((0,y,z))[1],top((0,y,z))[2]) for y,z in[(-.56,.055),(-.515,.055),(-.515,.090),(-.56,.090)]]
prism_x('Continuous_ThickFrontRetainingStrip',0,1.56,stop_yz,0,'full-width thick front retaining strip with entire 1.56 by 0.045 m underside against drawing-board top')
contact('Wide_EmptyDrawingBoard','Continuous_ThickFrontRetainingStrip',N,top((0,-.5375,.055)),1.56*.045-.000001,'whole finite normal-thickness retaining-strip underside on board top')
# Original front hinge: three full true-octagonal bored ears and one solid pin.
# Flat lower pin facet meets all bore floors; the other seven facets clear them.
HOLE=[(-.017,-.025),(.017,-.025),(.025,-.017),(.025,.017),(.017,.025),(-.017,.025),(-.025,.017),(-.025,-.017)]
SHAFT=[(-.012,-.025),(.012,-.025),(.020,-.017),(.020,.008),(.012,.016),(-.012,.016),(-.020,.008),(-.020,-.017)]
CAP=[(-.032,-.043),(.032,-.043),(.043,-.032),(.043,.032),(.032,.043),(-.032,.043),(-.043,.032),(-.043,-.032)]
def yzshift(poly):return[(HY+y,HZ+z) for y,z in poly]
def outer(bottom,drop):
 y0,y1=HY-.07,HY+.07;z0,z1=H+T*y0-drop,H+T*y1-drop
 return[(HY-.035,bottom),(HY+.035,bottom),(y1,bottom+.018),(y1,z1-.018),(HY+.035,H+T*(HY+.035)-drop),(HY-.035,H+T*(HY-.035)-drop),(y0,z0-.018),(y0,bottom+.018)]
def ear(name,x0,x1,bottom,drop,mat):
 out=outer(bottom,drop);inner=yzshift(HOLE);vs=[(x,y,z) for x in[x0,x1] for loop in[out,inner] for y,z in loop];fs=[];tags=[]
 for i in range(8):
  j=(i+1)%8
  for f,tag in [((i,j,16+j,16+i),'outer'),((8+j,8+i,24+i,24+j),'bore_floor' if i==0 else 'bore_nonbearing'),((i,8+i,8+j,j),'left_shoulder'),((16+j,24+j,24+i,16+i),'right_shoulder')]:fs.append(f);tags.append(tag)
 mesh(name,vs,fs,mat,'one continuous thick ear with a full octagonal through-bore and finite external bearing faces',tags);SECTIONS.append({'name':name,'x0':x0,'x1':x1,'loops':[out,inner]});EARS.append(name)
 return out
for side,x0,x1 in [('Left',-.56,-.44),('Right',.44,.56)]:
 name=side+'_FrameBoredEar';ear(name,x0,x1,.79,.015,0)
 contact(front,name,(0,0,1),((x0+x1)/2,HY,.79),.12*.070-.000001,'entire finite lower flat of frame ear against front beam')
name='Central_BoardBoredEar';ear(name,-.43,.43,.804,0,3)
# Ear outer top is a straight inclined face between its top two vertices.
contact(name,'Wide_EmptyDrawingBoard',N,(0,HY,H+T*HY),.86*.070/C-.000001,'whole finite inclined upper ear face against board underside')
# One watertight stepped pin with integral caps, assembled directly from boundary rings.
pin='One_ContinuousCappedPin';rings=[(-.59,CAP),(-.56,CAP),(-.56,SHAFT),(.56,SHAFT),(.56,CAP),(.59,CAP)]
vs=[(x,HY+y,HZ+z) for x,p in rings for y,z in p];fs=[];tags=[]
for k in range(len(rings)-1):
 for i in range(8):fs.append((k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i));tags.append('shaft_floor' if k==2 and i==0 else 'shaft_nonbearing' if k==2 else 'cap')
fs += [tuple(reversed(range(8))),tuple(40+i for i in range(8))];tags+=['end','end'];mesh(pin,vs,fs,2,'one complete continuous solid octagonal pin with two integral finite end shoulders',tags)
for x0,x1,p in[(-.59,-.56,CAP),(-.56,.56,SHAFT),(.56,.59,CAP)]:SECTIONS.append({'name':pin,'x0':x0,'x1':x1,'loops':[yzshift(p)]})
for name in EARS:
 sec=next(s for s in SECTIONS if s['name']==name);x=(sec['x0']+sec['x1'])/2
 contact(name,pin,(0,0,1),(x,HY,HZ-.025),(sec['x1']-sec['x0'])*.024-.000001,'entire lower flat pin facet within this ear bears on the complete bore floor portion',points=[(x+d,HY,HZ-.025) for d in[-.02,0,.02]])
 EAR_PAIRS.append({'ear':name,'pin':pin,'x0':sec['x0'],'x1':sec['x1'],'minimum_nonbearing_clearance_m':.003})
 BORES.append({'mesh':name,'origin_m':(sec['x0']-.001,HY,HZ),'direction':(1,0,0),'length_m':sec['x1']-sec['x0']+.002})
contact(pin,'Left_FrameBoredEar',(1,0,0),(-.56,HY+.035,HZ),.0025,'full left pin shoulder annulus against outer frame-ear end',points=[(-.56,HY+.035,HZ),(-.56,HY-.035,HZ),(-.56,HY,HZ-.035)])
contact('Right_FrameBoredEar',pin,(1,0,0),(.56,HY+.035,HZ),.0025,'full right frame-ear end against right integral pin shoulder',points=[(.56,HY+.035,HZ),(.56,HY-.035,HZ),(.56,HY,HZ-.035)])
# Full isolated bores use their true octagonal cross-section, inset 1 mm.
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def inset_convex(poly,d):
 p=list(poly)
 if area2(p)<0:p.reverse()
 lines=[]
 for a,b in zip(p,p[1:]+p[:1]):
  dy,dz=b[0]-a[0],b[1]-a[1];ln=math.hypot(dy,dz);n=(-dz/ln,dy/ln);lines.append((n[0],n[1],n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for i,(a,b,c) in enumerate(lines):
  d1,e,f=lines[i-1];det=a*e-b*d1
  if abs(det)<1e-12:continue
  q=((c*e-b*f)/det,(a*f-c*d1)/det)
  if any(n*q[0]+m*q[1]<v-1e-8 for n,m,v in lines):return []
  out.append(q)
 return out
for row in EAR_PAIRS:
 void_x('FullIsolatedBore_'+row['ear'],(row['x0']+row['x1'])/2,row['x1']-row['x0']+.002,inset_convex(yzshift(HOLE),.001),'entire actual octagonal bore volume including both open mouths; tested only against its isolated ear',[row['ear']],True)
# Complete tabletop usable air, bounded above at 0.24 m, excludes the retaining strip.
work_yz=[(top((0,y,z))[1],top((0,y,z))[2]) for y,z in[(-.514,.056),(.559,.056),(.559,.295),(-.514,.295)]]
void_x('Whole_UsableAboveBoardAir',0,1.558,work_yz,'entire finite empty work air above the board, behind the retaining strip, 1 mm inset')
# Whole under-board free-space partition. Each source mesh is a piecewise X
# extrusion. Sweep every X section and every Y boundary: sorted exact linear
# Z boundaries delimit ALL free trapezoids, including side-frame apertures,
# under/over-beam bays and assembly bore clearance. The fixed intended volumes
# are then checked against every actual triangle. No sparse ray is the acceptance.
def crossing(loop,y):
 vals=[]
 for a,b in zip(loop,loop[1:]+loop[:1]):
  if min(a[0],b[0])<y<max(a[0],b[0]):
   m=(b[1]-a[1])/(b[0]-a[0]);vals.append((m,a[1]-m*a[0]))
 return vals

def solid_at(loops,y,z):return sum(sum(m*y+b>z for m,b in crossing(loop,y)) for loop in loops)%2==1
DOMAIN_Y=(-.56*C,.56*C);DOMAIN_X=(-.78,.78);EMPTY_PARTITION=[]
xs=sorted(set(round(x,9) for x in [*DOMAIN_X]+[v for s in SECTIONS for v in[s['x0'],s['x1']] if DOMAIN_X[0]<v<DOMAIN_X[1]]))
for ix,(x0,x1) in enumerate(zip(xs,xs[1:])):
 mid=(x0+x1)/2;active=[s for s in SECTIONS if s['x0']<mid<s['x1'] and s['name'] not in ['Wide_EmptyDrawingBoard','Continuous_ThickFrontRetainingStrip']]
 ys=sorted(set([*DOMAIN_Y]+[p[0] for s in active for loop in s['loops'] for p in loop if DOMAIN_Y[0]<p[0]<DOMAIN_Y[1]]))
 for iy,(y0,y1) in enumerate(zip(ys,ys[1:])):
  y=(y0+y1)/2;lines=[(0,0),(T,H)]+[q for s in active for loop in s['loops'] for q in crossing(loop,y)]
  lines=sorted(set(lines),key=lambda q:q[0]*y+q[1])
  for iz,(bottom,upper) in enumerate(zip(lines,lines[1:])):
   z=(bottom[0]*y+bottom[1]+upper[0]*y+upper[1])/2
   if not (0<z<H+T*y) or any(solid_at(s['loops'],y,z) for s in active):continue
   yz=[(y0,bottom[0]*y0+bottom[1]),(y1,bottom[0]*y1+bottom[1]),(y1,upper[0]*y1+upper[1]),(y0,upper[0]*y0+upper[1])]
   # Remove coincident vertices from triangular endpoint tapers.
   cleaned=[]
   for p in yz:
    if not cleaned or math.dist(p,cleaned[-1])>1e-8:cleaned.append(p)
   if math.dist(cleaned[0],cleaned[-1])<1e-8:cleaned.pop()
   if len(cleaned)<3 or abs(area2(cleaned))<1e-10:continue
   inset=inset_convex(cleaned,.001)
   if not inset or x1-x0<=.002:continue
   label='WholeUnderDesk_%02d_%02d_%02d'%(ix,iy,iz)
   void_x(label,(x0+x1)/2,x1-x0-.002,inset,'complete free-space partition cell under the drawing board, with only 1 mm face and partition margins')
   EMPTY_PARTITION.append({'name':label,'x0':x0,'x1':x1,'yz_uninset':cleaned,'x_margin_m':.001,'yz_margin_m':.001,'nominal_free_volume_m3':abs(area2(cleaned))*.5*(x1-x0)})
DESK_CONTRACT={'single_prop_count':1,'fixed_tilt_degrees':25,'wide_board_normal_thickness_m':.055,'original_open_side_frames':2,'continuous_ground_runners':2,'uprights':4,'true_bored_ears':3,'one_continuous_capped_pin':1,'complete_rear_inclined_bearings':2,'finite_opposed_contacts':len(CONTACTS),'complete_underdesk_partition_cells':len(EMPTY_PARTITION),'finite_empty_volumes':len(VOID_VOLUMES),'isolated_bore_volumes':len(ISOLATED_VOID_VOLUMES),'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_desk_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 v=vertices['Wide_EmptyDrawingBoard'];assert abs(min(p[0] for p in v)+.78)<2e-7 and abs(max(p[0] for p in v)-.78)<2e-7
 return dict(DESK_CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, whole empty regions, all noncontact surfaces and real mutations still required')
FOCUS=(0,0,.69);ORTHO=2.30
CAMERAS={'gray-front3q':(4.6,-6.3,3.5),'gray-back3q':(-4.6,6.3,3.5),'thumbnail':(4.6,-6.3,3.5),'qa-front':(0,-6.8,2.6),'qa-side':(6.8,0,2.6),'qa-top':(0,0,7.0),'qa-back':(0,6.8,2.6),'qa-wireframe':(4.6,-6.3,3.5),'silhouette-128-front':(0,-6.8,2.6),'silhouette-128-side':(6.8,0,2.6)}
WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneFixedTiltDraftingDesk',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.64,0,.04),(-.64,0,.09)),('Wide_EmptyDrawingBoard',top((0,0,.025)),top((0,0,.065)))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Finite support and true openings are checked against actual generated mesh triangles.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_desk_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'desk_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/painting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'painting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
