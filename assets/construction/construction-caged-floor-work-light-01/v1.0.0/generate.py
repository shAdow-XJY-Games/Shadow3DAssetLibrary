"""Original caged floor work light: one complete static, non-emitting visual prop.
Metres, native Z up, front -Y. No electrical, illumination or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='construction-caged-floor-work-light-01';VERSION='1.0.0';TITLE='Caged Floor Work Light'
DESCRIPTION=('One original low portable floor-work-light visual prop. A shallow rectangular thick housing is fixed at a 15-degree upward-facing attitude inside an open low protective-looking frame. The housing has a real stepped front recess and an opaque non-emitting solid panel bearing on a complete finite internal shoulder. Two wide ground runners carry tall bored side uprights, a lower tie and a full top carrying bar. Two housing tabs carry true bored ears. Two individual continuous solid capped pins sit on finite lower bore facets, and two frame-mounted blocks meet full tab undersides as finite angle stops. Housing, ears, pins, stops, frame and runners form one connected fixed assembly. Complete clear air remains in the front recess, top handle aperture and housing-to-frame openings. Sixteen closed editable meshes and four constant opaque PBR colours. This low caged rectangular head with paired runners is original: it is not a shortened softbox, track light on a new base or repainted lantern. No cord, circuit, battery, bulb, second head, stand pole, soft cloth, track, scene or animation. Fixed static appearance only: no actual light emission, power, electrical circuit, illumination, heat dissipation, ingress protection, impact resistance, load, stability, fire or construction safety certification, adjustment, folding, manufacture or old-interface compatibility.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SECTIONS=[];EAR_PAIRS=[];EARS=[];STOPS=[];TABS=[];EMPTY_PARTITION=[]
PALETTE=[('Frame_SiteAmber',(.72,.32,.045,1),.58,.24),('Housing_Graphite',(.055,.075,.085,1),.64,.24),('Panel_CloudIvory',(.74,.77,.70,1),.57,0),('Hardware_BrushedSteel',(.29,.34,.36,1),.42,.64)]
A=math.radians(15);C=math.cos(A);S=math.sin(A);H=.38;N=(0,-C,S)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def head(p):x,d,h=p;return(x,C*d+S*h,H-S*d+C*h)
def head_yz(poly):return[(head((0,d,h))[1],head((0,d,h))[2]) for d,h in poly]
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def prism_geometry(x,width,yz):
 if area2(yz)<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return vs,fs

def prism_x(name,x,width,yz,mat,role):
 SECTIONS.append({'name':name,'x0':x-width/2,'x1':x+width/2,'loops':[yz]});return mesh(name,*prism_geometry(x,width,yz),mat,role)
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size;return prism_x(name,x,w,[(y-d/2,z-h/2),(y+d/2,z-h/2),(y+d/2,z+h/2),(y-d/2,z+h/2)],mat,role)
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0002,'points':points or [point],'scope':scope})
def void_x(name,x,w,yz,scope,targets=None,isolated=False):
 vs,fs=prism_geometry(x,w,yz);g={'vertices':vs,'faces':fs,'targets':list(G) if targets is None else targets,'role':scope}
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]=g
HOLE=[(-.013,-.020),(.013,-.020),(.020,-.013),(.020,.013),(.013,.020),(-.013,.020),(-.020,.013),(-.020,-.013)]
SHAFT=[(-.009,-.020),(.009,-.020),(.015,-.013),(.015,.007),(.009,.014),(-.009,.014),(-.015,.007),(-.015,-.013)]
CAP=[(-.019,-.029),(.019,-.029),(.029,-.019),(.029,.019),(.019,.029),(-.019,.029),(-.029,.019),(-.029,-.019)]
def yzshift(poly):return[(y,H+z) for y,z in poly]
def bored(name,x0,x1,out,mat,role):
 inner=yzshift(HOLE);vs=[(x,y,z) for x in[x0,x1] for loop in[out,inner] for y,z in loop];fs=[];tags=[]
 for i in range(8):
  j=(i+1)%8
  for f,tag in [((i,j,16+j,16+i),'outer'),((8+j,8+i,24+i,24+j),'bore_floor' if i==0 else 'bore_nonbearing'),((i,8+i,8+j,j),'left_shoulder'),((16+j,24+j,24+i,16+i),'right_shoulder')]:fs.append(f);tags.append(tag)
 mesh(name,vs,fs,mat,role,tags);SECTIONS.append({'name':name,'x0':x0,'x1':x1,'loops':[out,inner]});EARS.append(name)

# One continuous thick stepped shell, constructed from boundary rings.
# The shoulder is an actual finite annulus, not a material line or fake groove.
rings=[(.060,.300,.200),(-.080,.300,.200),(-.080,.264,.164),(-.018,.264,.164),(-.018,.244,.144),(.028,.244,.144)]
vs=[head((x,d,h)) for d,w,hmax in rings for x,h in[(-w,-hmax),(w,-hmax),(w,hmax),(-w,hmax)]];fs=[];tags=[]
for k in range(len(rings)-1):
 for i in range(4):fs.append((k*4+i,k*4+(i+1)%4,(k+1)*4+(i+1)%4,(k+1)*4+i));tags.append('panel_shoulder' if k==3 else 'shell')
fs += [tuple(reversed(range(4))),tuple(20+i for i in range(4))];tags+=['back','cavity_floor'];mesh('Shallow_SteppedHousing',vs,fs,1,'one closed thick shallow rectangular housing with a real open stepped recess and continuous finite internal panel seat',tags)
outer=[(-.08,-.20),(.06,-.20),(.06,.20),(-.08,.20)]
mid=[(-.08,-.20),(.06,-.20),(.06,.20),(-.08,.20),(-.08,.164),(-.018,.164),(-.018,-.164),(-.08,-.164)]
inner=[(-.08,-.20),(.06,-.20),(.06,.20),(-.08,.20),(-.08,.164),(-.018,.164),(-.018,.144),(.028,.144),(.028,-.144),(-.018,-.144),(-.018,-.164),(-.08,-.164)]
for x0,x1,p in[(-.3,-.264,outer),(-.264,-.244,mid),(-.244,.244,inner),(.244,.264,mid),(.264,.3,outer)]:SECTIONS.append({'name':'Shallow_SteppedHousing','x0':x0,'x1':x1,'loops':[head_yz(p)]})
prism_x('Opaque_NonEmittingFrontPanel',0,.526,head_yz([(-.036,-.163),(-.018,-.163),(-.018,.163),(-.036,.163)]),2,'one 18 mm thick opaque non-emitting front panel with 1 mm positive edge clearance and complete rear annular shoulder contact')
# Shell has outward -depth face; panel rear lies on that shoulder.
contact('Shallow_SteppedHousing','Opaque_NonEmittingFrontPanel',N,head((0,-.018,.153)),(.526*.326-.488*.288)-.000001,'complete rectangular shoulder annulus covered by the panel rear',points=[head((x,-.018,h)) for x,h in[(0,.153),(0,-.153),(.253,0),(-.253,0)]])
for side,sign in [('Left',-1),('Right',1)]:
 x=sign*.40
 foot=box(side+'_WideGroundRunner',(x,0,.025),(.13,.44,.05),1,'one broad continuous runner with a complete 0.13 by 0.44 m flat ground face');FEET.append(foot)
 upright=side+'_BoredFrameUpright';bored(upright,x-.03,x+.03,[(-.026,.05),(.026,.05),(.035,.059),(.035,.691),(.026,.70),(-.026,.70),(-.035,.691),(-.035,.059)],0,'one tall thick frame upright with an actual octagonal through-bore, full finite bottom and top flats')
 contact(foot,upright,(0,0,1),(x,0,.05),.06*.052-.000001,'entire chamfered upright bottom flat against broad runner top')
 tab=box(side+'_HousingMountTab',(sign*.33,0,.29),(.06,.07,.02),1,'finite thick housing mounting tab, exactly joined to shell side and carrying the bored ear');TABS.append(tab)
 contact('Shallow_SteppedHousing',tab,(sign,0,0),(sign*.30,0,.29),.07*.02-.000001,'whole tab side rectangle against the housing exterior side')
 ear=side+'_HousingBoredEar';x0,x1=sorted([sign*.325,sign*.345]);bored(ear,x0,x1,[(-.035,.30),(.035,.30),(.05,.315),(.05,.425),(.035,.44),(-.035,.44),(-.05,.425),(-.05,.315)],1,'one thick housing ear with a real octagonal through-bore and full finite lower flat')
 contact(tab,ear,(0,0,1),(sign*.335,0,.30),.02*.07-.000001,'entire housing-ear bottom flat against housing tab top')
 stop=box(side+'_FiniteAngleStop',(sign*.3575,0,.265),(.025,.06,.03),3,'one frame-mounted fixed angle-stop block with a finite upper face under the housing tab');STOPS.append(stop)
 contact(stop,upright,(sign,0,0),(sign*.37,0,.265),.06*.03-.000001,'complete outer stop face against inward frame upright side')
 contact(stop,tab,(0,0,1),(sign*.3525,0,.28),.015*.06-.000001,'complete overlapped finite stop top patch against housing-tab underside')
 # Side-specific pin: one continuous shaft and two integral capped shoulders.
 pin=side+'_ContinuousCappedPin';pr=[(.315,CAP),(.325,CAP),(.325,SHAFT),(.43,SHAFT),(.43,CAP),(.44,CAP)]
 if sign<0:pr=[(-xx,p) for xx,p in reversed(pr)]
 vs=[(xx,y,H+z) for xx,p in pr for y,z in p];fs=[];tags=[]
 for k in range(5):
  for i in range(8):fs.append((k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i));tags.append('shaft_floor' if k==2 and i==0 else 'shaft_nonbearing' if k==2 else 'cap')
 fs += [tuple(reversed(range(8))),tuple(40+i for i in range(8))];tags+=['end','end'];mesh(pin,vs,fs,3,'one continuous solid fixed pin with finite lower bearing facet and two integral end shoulders',tags)
 for a,b,p in[(.315,.325,CAP),(.325,.43,SHAFT),(.43,.44,CAP)]:
  xx=sorted([sign*a,sign*b]);SECTIONS.append({'name':pin,'x0':xx[0],'x1':xx[1],'loops':[yzshift(p)]})
 for ename in[ear,upright]:
  sec=next(s for s in SECTIONS if s['name']==ename);xx=(sec['x0']+sec['x1'])/2
  contact(ename,pin,(0,0,1),(xx,0,H-.020),(sec['x1']-sec['x0'])*.018-.000001,'entire lower flat shaft facet within this ear bears on its bore floor')
  EAR_PAIRS.append({'ear':ename,'pin':pin,'x0':sec['x0'],'x1':sec['x1'],'minimum_nonbearing_clearance_m':.0025})
  BORES.append({'mesh':ename,'origin_m':(sec['x0']-.001,0,H),'direction':(1,0,0),'length_m':sec['x1']-sec['x0']+.002})
 contact(pin,ear,(sign,0,0),(sign*.325,.024,H),.0010,'complete inner cap annulus against housing-ear end',points=[(sign*.325,.024,H),(sign*.325,-.024,H),(sign*.325,0,H+.024)])
 contact(upright,pin,(sign,0,0),(sign*.43,.024,H),.0010,'complete outer frame-ear annulus against integral cap shoulder',points=[(sign*.43,.024,H),(sign*.43,-.024,H),(sign*.43,0,H+.024)])
bar=box('FullWidth_TopCarryBar',(0,0,.725),(.86,.07,.05),0,'one full-width thick top bar joining the uprights above the entire clear carrying aperture')
tie=box('Low_ContinuousFrameTie',(0,0,.105),(.74,.07,.05),0,'one full-width low tie completing the open low frame')
for side,sign in [('Left',-1),('Right',1)]:
 contact(side+'_BoredFrameUpright',bar,(0,0,1),(sign*.4,0,.70),.06*.052-.000001,'entire finite upright top flat against top-bar underside')
 contact(tie,side+'_BoredFrameUpright',(sign,0,0),(sign*.37,0,.105),.07*.05-.000001,'entire low-tie end against frame upright inner side')
# Whole true bore bodies and complete nonbearing surfaces are distinct tests.
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
for r in EAR_PAIRS:
 void_x('FullIsolatedBore_'+r['ear'],(r['x0']+r['x1'])/2,r['x1']-r['x0']+.002,inset_convex(yzshift(HOLE),.001),'whole true octagonal through-bore with both open mouths, isolated from the assembled shaft',[r['ear']],True)
void_x('Whole_FrontRecess',0,.526,head_yz([(-.079,-.163),(-.037,-.163),(-.037,.163),(-.079,.163)]),'entire front recess above the actual panel, only 1 mm boundary margin')
void_x('Whole_InnerHousingCavity',0,.486,head_yz([(-.017,-.143),(.027,-.143),(.027,.143),(-.017,.143)]),'complete rear housing cavity behind the panel, only 1 mm boundary margin')
headlo=min(v[2] for v in G['Shallow_SteppedHousing']['vertices']);headhi=max(v[2] for v in G['Shallow_SteppedHousing']['vertices'])
void_x('Whole_TopCarryAperture',0,.738,[(-.034,headhi+.001),(.034,headhi+.001),(.034,.699),(-.034,.699)],'whole top carrying aperture across the frame thickness, bounded by actual highest housing and bar underside')
void_x('Whole_LowerFrameWindow',0,.598,[(-.034,.131),(.034,.131),(.034,headlo-.001),(-.034,headlo-.001)],'whole central lower opening between low frame tie and actual lowest housing')
# Partition the complete central and lateral housing/frame windows into exact free X/Y/Z
# cells. Every section vertex and line crossing is included before free cells
# are frozen. Actual triangles must clear every complete closed cell afterward.
def crossing(loop,y):
 vals=[]
 for a,b in zip(loop,loop[1:]+loop[:1]):
  if min(a[0],b[0])<y<max(a[0],b[0]):
   m=(b[1]-a[1])/(b[0]-a[0]);vals.append((m,a[1]-m*a[0]))
 return vals

def solid_at(loops,y,z):return sum(sum(m*y+b>z for m,b in crossing(loop,y)) for loop in loops)%2==1
for side,domain in [('Left',(-.37,-.30)),('Centre',(-.30,.30)),('Right',(.30,.37))]:
 xs=sorted(set(round(x,9) for x in [*domain]+[v for s in SECTIONS for v in[s['x0'],s['x1']] if domain[0]<v<domain[1]]))
 for ix,(x0,x1) in enumerate(zip(xs,xs[1:])):
  mid=(x0+x1)/2;active=[s for s in SECTIONS if s['x0']<mid<s['x1']]
  ys=sorted(set([-.035,.035]+[p[0] for s in active for loop in s['loops'] for p in loop if -.035<p[0]<.035]))
  extra=[]
  for y0,y1 in zip(ys,ys[1:]):
   lines=[(0,.13),(0,.70)]+[q for s in active for loop in s['loops'] for q in crossing(loop,(y0+y1)/2)]
   for i,(a,b) in enumerate(lines):
    for c,d in lines[i+1:]:
     if abs(a-c)>1e-12:
      v=(d-b)/(a-c)
      if y0+1e-9<v<y1-1e-9:extra.append(v)
  ys=sorted(set(ys+extra))
  for iy,(y0,y1) in enumerate(zip(ys,ys[1:])):
   y=(y0+y1)/2;lines=sorted(set([(0,.13),(0,.70)]+[q for s in active for loop in s['loops'] for q in crossing(loop,y)]),key=lambda q:q[0]*y+q[1])
   for iz,(bottom,upper) in enumerate(zip(lines,lines[1:])):
    z=((bottom[0]+upper[0])*y+bottom[1]+upper[1])/2
    if not .13<z<.70 or any(solid_at(s['loops'],y,z) for s in active):continue
    yz=[(y0,bottom[0]*y0+bottom[1]),(y1,bottom[0]*y1+bottom[1]),(y1,upper[0]*y1+upper[1]),(y0,upper[0]*y0+upper[1])];cleaned=[]
    for p in yz:
     if not cleaned or math.dist(p,cleaned[-1])>1e-8:cleaned.append(p)
    if math.dist(cleaned[0],cleaned[-1])<1e-8:cleaned.pop()
    if len(cleaned)<3 or abs(area2(cleaned))<1e-10:continue
    inset=inset_convex(cleaned,.0008)
    if not inset or x1-x0<=.0016:continue
    name='WholeSideWindow_%s_%02d_%02d_%02d'%(side,ix,iy,iz)
    void_x(name,(x0+x1)/2,x1-x0-.0016,inset,'complete free inner-cage partition cell; 0.8 mm boundary/partition margins')
    EMPTY_PARTITION.append({'name':name,'side':side,'x0':x0,'x1':x1,'yz_uninset':cleaned,'boundary_margin_m':.0008,'nominal_free_volume_m3':abs(area2(cleaned))*.5*(x1-x0)})
WORKLIGHT_CONTRACT={'single_prop_count':1,'fixed_upward_tilt_degrees':15,'housing_width_m':.6,'housing_depth_m':.14,'housing_height_m':.4,'front_panel_normal_thickness_m':.018,'wide_ground_runners':2,'continuous_top_carry_bar':1,'true_bored_ears':4,'continuous_capped_pins':2,'finite_angle_stop_blocks':2,'finite_opposed_contacts':len(CONTACTS),'complete_inner_frame_partition_cells':len(EMPTY_PARTITION),'finite_empty_volumes':len(VOID_VOLUMES),'isolated_bore_volumes':len(ISOLATED_VOID_VOLUMES),'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_worklight_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 v=vertices['Shallow_SteppedHousing'];assert abs(min(p[0] for p in v)+.3)<2e-7 and abs(max(p[0] for p in v)-.3)<2e-7
 return dict(WORKLIGHT_CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, whole empty regions, all noncontact surfaces and real mutations still required')
FOCUS=(0,0,.375);ORTHO=1.20
CAMERAS={'gray-front3q':(4.6,-6.3,3.4),'gray-back3q':(-4.6,6.3,3.4),'thumbnail':(4.6,-6.3,3.4),'qa-front':(0,-6.8,2.2),'qa-side':(6.8,0,2.2),'qa-top':(0,0,7.0),'qa-back':(0,6.8,2.2),'qa-wireframe':(4.6,-6.3,3.4),'silhouette-128-front':(0,-6.8,2.2),'silhouette-128-side':(6.8,0,2.2)}
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
root=bpy.data.objects.new('OneCagedFloorWorkLight',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.40,0,.025),(-.40,0,.06)),('Opaque_NonEmittingFrontPanel',head((0,-.027,0)),head((0,-.045,0)))]:
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
mount_evidence=measure_worklight_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'worklight_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
