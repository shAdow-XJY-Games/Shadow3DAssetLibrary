"""Original single static fishing seatbox with continuous stepped underframe and front footplate."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fishing-fixed-footplate-seatbox-01';VERSION='1.0.0';TITLE='Fixed Footplate Fishing Seatbox'
DESCRIPTION=('One original fixed fishing seatbox appearance: a complete deep empty thick shell, one full thick lid with a complete cushion fixed at 100 degrees, two continuous stepped side bearers linking the elevated rear box and lower front footplate, three finite crossmembers and six short complete ground feet. Two true-bored three-ear hinges have continuous headed pins, full bearing faces and residual clearances; two complete fixed-angle stops carry the lid. All geometry is newly authored as one coherent static prop, not an old box placed on an old stool. Native Z up, front -Y, metres, horizontally bounds-centred ground origin. Five constant opaque unlinked PBR materials. No TEX_* nodes, texture, image, text, logo, animation, gear, scene or reused model. No seating, standing, load, stability, anti-tip, human fit, opening/closing path, hinge motion, locking, adjustability, waterproofing, food contact, fishing performance, manufacture or safety claim; no old equipment compatibility. One narrow seatbox form only, counted once.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];FOOT_CONTACTS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};BEAMS=[];CROSSMEMBERS=[];HINGES=[];STOPS=[]
BODY='WholeDeepSeatboxShell';LID='WholeFixed100DegreeLid';PAD='WholeThickSeatCushion';PLATE='WholeLowFrontFootplate'
PALETTE=[('MutedRiverTeal',(.08,.25,.25,1),.67,.02),('WarmStoneFrame',(.49,.48,.36,1),.67,.04),('DeepTealCushion',(.045,.10,.105,1),.8,0),('PaleSageLid',(.32,.44,.37,1),.66,.02),('WarmAlloyPins',(.44,.37,.23,1),.46,.48)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in p) for p in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 return {'vertices':vv,'faces':[tuple(reversed(f)) if volume<0 else tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def prism(poly,z0,z1,material=0,role='',transform=None):
 n=len(poly);vv=[(x,y,z) for z in [z0,z1] for x,y in poly];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv] if transform else vv,ff,material,role)
def grid(xs,ys,zs,occupied,material=0,role=''):
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};vv=[];ff=[];ids={}
 def vi(p):
  p=tuple(round(x,9) for x in p)
  if p not in ids:ids[p]=len(vv);vv.append(p)
  return ids[p]
 for i,j,k in sorted(cells):
  cell=[(x,y,z) for z in zs[k:k+2] for y in ys[j:j+2] for x in xs[i:i+2]]
  for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:ff.append(tuple(vi(cell[n]) for n in face))
 return mesh(vv,ff,material,role)
def union_boxes(boxes,material=0,role=''):
 stations=[sorted(set(p[k] for lo,hi in boxes for p in [lo,hi])) for k in range(3)]
 return grid(*stations,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes),material,role)
def transform_geometry(g,fn):return mesh([fn(p) for p in g['vertices']],g['faces'],g['material'],g['role'])
def inset_box(lo,hi,e=.001):return box(tuple(x+e for x in lo),tuple(x-e for x in hi))
def contact(name,a,b,axis,p,area,points=None,offset=.0004):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'points':points or [p],'minimum_patch_area_m2':area-.000001,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def solid(name,g,targets,role):SOLID_VOLUMES[name]=dict(g,targets=targets,role=role)
def isolated(name,g,targets,role):ISOLATED_VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def putbox(n,lo,hi,m,role):
 G[n]=box(lo,hi,m,role);solid(n+'_WholeMaterial',inset_box(lo,hi),[n],'Whole finite inward-offset material body; full end faces, all corners and complete thickness.');return n
# One original full shell. The inner rectangle and bottom are explicit material boundaries.
def shell(e=0,filled=False):
 return grid([-.30+e,-.265-e,.265+e,.30-e],[e,.035-e,.445+e,.48-e],[.18+e,.218-e,.61-e],lambda x,y,z:filled or z<.218-e or abs(x)>.265+e or y<.035-e or y>.445+e,0,'One complete deep shell, continuous 38 mm bottom and four 35 mm walls, full continuous rim; no scene objects inside.')
G[BODY]=shell();solid('WholeDeepShellMaterial',shell(.001),[BODY],'Entire continuous inset shell including complete bottom, four complete walls, all corners and every floor-wall root.')
air('WholeDeepCavityAndMouth',box((-.264,.036,.219),(.264,.444,1.21)),'Entire finite empty cavity from above complete floor through the full mouth and above the whole fixed lid; all inner corners included with 1 mm surface inset.')
# Stepped side beams are each one concave prism, not intersecting box bars.
STEP=[(-.50,.065),(-.50,.12),(-.14,.12),(-.14,.18),(.48,.18),(.48,.125),(-.04,.125),(-.04,.065)]
def stepbeam(cx,e=0):
 # Exact inward polygon for the orthogonal concave profile.
 poly=[(-.50+e,.065+e),(-.50+e,.12-e),(-.14+e,.12-e),(-.14+e,.18-e),(.48-e,.18-e),(.48-e,.125+e),(-.04-e,.125+e),(-.04-e,.065+e)]
 return prism(poly,cx-.028+e,cx+.028-e,1,'One unbroken stepped side bearer; full lower front run, solid riser/return and full higher rear run.',lambda p:(p[2],p[0],p[1]))
for side,label in[(-1,'Left'),(1,'Right')]:
 x=side*.27;n='ContinuousSteppedSideBeam_'+label;BEAMS.append(n);G[n]=stepbeam(x);solid(n+'_WholeMaterial',stepbeam(x,.001),[n],'Whole connected side-beam material covering both full runs and every complete concave/convex turn, exact 1 mm inward offset.')
 contact(n+'_WholeBoxUndersideSeat',n,BODY,(0,0,1),(x,.24,.18),.056*.48)
 for j,(y,z) in enumerate([(-.42,.065),(.065,.125),(.405,.125)],1):
  foot=f'CompleteShortFoot_{label}_{j}';putbox(foot,(x-.025,y-.045,0),(x+.025,y+.045,z),2,'One complete fixed short foot with full planar ground sole and finite entire head.');FEET.append(foot)
  contact(foot+'_WholeBeamHead',foot,n,(0,0,1),(x,y,z),.05*.09)
  FOOT_CONTACTS.append({'mesh':foot,'name':foot+'_WholeGroundSole','x':x,'y':y,'half_x':.025,'half_y':.045,'minimum_area_m2':.004499})
for j,(y,z,target) in enumerate([(-.42,.065,PLATE),(.065,.125,BODY),(.405,.125,BODY)],1):
 n='WholeCrossmember_'+str(j);CROSSMEMBERS.append(n);putbox(n,(-.242,y-.02,z),(.242,y+.02,z+.055),1,'Complete finite crossmember meeting the two continuous side beams at full cut ends.')
 for side,beam in zip([-1,1],BEAMS):contact(n+'_WholeEnd_'+str(side),n,beam,(side,0,0),(side*.242,y,z+.0275),.04*.055)
 contact(n+'_WholeUpperBearing',n,target,(0,0,1),(0,y,z+.055),.484*.04)
putbox(PLATE,(-.32,-.50,.12),(.32,-.18,.148),3,'One full 28 mm thick low front footplate supported by both stepped bearers and its crossmember; no slip-resistance or stepping claim.')
for side,beam in zip([-1,1],BEAMS):contact(beam+'_WholeFootplateSeat',beam,PLATE,(0,0,1),(side*.27,-.34,.12),.056*.32)
# Lid frame: u points from rear hinge toward the raised free edge, v is its outer face normal.
THETA=math.radians(100);C=math.cos(THETA);S=math.sin(THETA)
def frame(p):x,u,v=p;return(x,.515-C*u+S*v,.66+S*u+C*v)
def direction(p):x,u,v=p;return(x,-C*u+S*v,S*u+C*v)
def posed(g):return transform_geometry(g,frame)
G[LID]=posed(box((-.30,.026,-.018),(.30,.506,.018),3,'One complete 36 mm thick rectangular cover fixed rearward at 100 degrees; single static pose.'))
solid(LID+'_WholeMaterial',posed(inset_box((-.30,.026,-.018),(.30,.506,.018))),[LID],'Entire full lid material and thickness; no hollow second box or zero-thickness plane.')
G[PAD]=posed(box((-.275,.045,.018),(.275,.487,.055),2,'One complete thick cushion resting over its full inner face on the whole raised cover; visual only.'))
solid(PAD+'_WholeMaterial',posed(inset_box((-.275,.045,.018),(.275,.487,.055))),[PAD],'Entire closed inset cushion body including complete corners and full thickness.')
contact('WholeCushionToCoverFace',LID,PAD,direction((0,0,1)),frame((0,.266,.018)),.55*.442)
def wedge(x0,x1,u0,u1,v,e=0):
 p0=frame((0,u0,v));p1=frame((0,u1,v));poly=[(.452,.61),(.477,.61),(p0[1],p0[2]),(p1[1],p1[2])]
 if e:
  old=poly;poly=[]
  for i,p in enumerate(old):
   prev=old[i-1];nxt=old[(i+1)%len(old)];a=unit((-(p[1]-prev[1]),p[0]-prev[0]));b=unit((-(nxt[1]-p[1]),nxt[0]-p[0]));poly.append(add(p,mul(add(a,b),e/(1+dot(a,b)))))
  x0+=e;x1-=e
 return prism(poly,x0,x1,1,'Complete solid fixed bracket from full rear-rim root to entire inclined lid/ear seat.',lambda p:(p[2],p[0],p[1]))
for x in[-.09,.09]:
 n='WholeFixedAngleStop_'+str(x);G[n]=wedge(x-.018,x+.018,.028,.066,-.018);STOPS.append(n)
 solid(n+'_WholeMaterial',wedge(x-.018,x+.018,.028,.066,-.018,.001),[n],'Whole inward-offset stop including full horizontal root and full inclined lid seat.')
 contact(n+'_WholeRimRoot',BODY,n,(0,0,1),(x,.4675,.61),.036*.025)
 contact(n+'_WholeLidSeat',n,LID,direction((0,0,1)),frame((x,.047,-.018)),.036*.038)
for idx,cx in enumerate([-.20,.20],1):
 pin=f'Hinge_{idx}_ContinuousHeadedPin';boxes=[((cx-.058,-.011,-.014),(cx+.058,.011,.010)),((cx-.068,-.020,-.022),(cx-.058,.020,.018)),((cx+.058,-.020,-.022),(cx+.068,.020,.018))]
 G[pin]=posed(union_boxes(boxes,4,'One continuous solid square pin with integral two thick end heads. Fixed appearance, no moving joint claim.'))
 # One connected inset core and two inset head bodies, bridged across both roots.
 pb=[((cx-.067,-.019,-.021),(cx-.059,.019,.017)),((cx-.060,-.010,-.013),(cx+.060,.010,.009)),((cx+.059,-.019,-.021),(cx+.067,.019,.017))]
 solid(pin+'_WholeMaterial',posed(union_boxes(pb)),[pin],'Whole connected pin material including the entire shaft, both entire heads and both finite head/shaft roots.')
 rings=[]
 for label,a,b in [('Left',cx-.052,cx-.028),('Center',cx-.022,cx+.022),('Right',cx+.028,cx+.052)]:
  n=f'Hinge_{idx}_{label}TrueBoredEar';rings.append(n);uo=.026 if label=='Center' else .023
  G[n]=posed(grid([a,b],[-uo,-.014,.014,uo],[-.026,-.014,.014,.026],lambda x,u,v:not(abs(u)<.014 and abs(v)<.014),1,'Complete four-wall thick annular ear, full 28 mm square through-bore.'))
  solid(n+'_WholeMaterial',posed(grid([a+.001,b-.001],[-uo+.001,-.015,.015,uo-.001],[-.025,-.015,.015,.025],lambda x,u,v:not(abs(u)<.015 and abs(v)<.015))),[n],'Entire inward-offset annular material around all four true hole walls, full mouths and every corner.')
  isolated(n+'_WholeBore',posed(box((a-.001,-.013,-.013),(b+.001,.013,.013))),[n],'Entire isolated through-bore, extended beyond both full axial mouths and inset by 1 mm on every hole face.')
  contact(n+'_WholeLowerPinSeat',n,pin,direction((0,0,1)),frame(((a+b)/2,0,-.014)),(b-a)*.022)
  if label=='Center':contact(n+'_WholeLidRoot',n,LID,direction((0,1,0)),frame((cx,.026,0)),(b-a)*.036)
  else:
   bracket=n+'_CompleteRimBracket';G[bracket]=wedge(a,b,-uo,uo,-.026);solid(bracket+'_WholeMaterial',wedge(a,b,-uo,uo,-.026,.001),[bracket],'Whole closed inward-offset bracket joining full rim root and full inclined ear seat.')
   contact(bracket+'_WholeRimRoot',BODY,bracket,(0,0,1),((a+b)/2,.4675,.61),(b-a)*.025)
   contact(bracket+'_WholeEarSeat',bracket,n,direction((0,0,1)),frame(((a+b)/2,0,-.026)),(b-a)*uo*2)
 for label,lo,hi in [('SideMinus',(cx-.053,-.0135,-.013),(cx+.053,-.0115,.013)),('SidePlus',(cx-.053,.0115,-.013),(cx+.053,.0135,.013)),('AbovePin',(cx-.053,-.011,.0105),(cx+.053,.011,.0135))]:
  air(pin+'_WholeRemainingBoreAir_'+label,posed(box(lo,hi)),'Entire finite remaining bore corridor spanning all three ears and both inter-ear gaps; nonbearing walls have 0.5 mm inset, actual lower bearing plane explicitly excluded.')
 for label,a,b in [('LeftEnd',cx-.057,cx-.053),('LeftMiddle',cx-.027,cx-.023),('RightMiddle',cx+.023,cx+.027),('RightEnd',cx+.053,cx+.057)]:
  air(pin+'_WholeAxialAir_'+label,posed(grid([a,b],[-.025,-.012,.012,.025],[-.025,-.015,.011,.025],lambda x,u,v:not(abs(u)<.012 and -.015<v<.011))),'Whole finite axial space around the continuous shaft between each pair of ears or between an end ear and its head; 1 mm boundary inset.')
 HINGES.append({'pin':pin,'rings':rings,'center_x':cx,'side_clearance_m':.003,'upper_clearance_m':.004,'inter_ear_gap_m':.006,'head_gap_m':.006})
# Complete bounded empty domains in all underframe and front working openings.
def empty_partition(lo,hi,obstacles):
 cuts=[sorted(set([lo[k],hi[k]]+[max(lo[k],min(hi[k],p[k])) for a,b in obstacles for p in[a,b]])) for k in range(3)]
 return grid(*cuts,lambda x,y,z:not any(all(a[k]<p<b[k] for k,p in enumerate((x,y,z))) for a,b in obstacles))
def inflated(lo,hi,e=.001):return(tuple(x-e for x in lo),tuple(x+e for x in hi))
under_obstacles=[]
for s in[-1,1]:
 under_obstacles.append(inflated((s*.27-.028,0,.125),(s*.27+.028,.48,.18)))
 for y in[.065,.405]:under_obstacles.append(inflated((s*.27-.025,y-.045,0),(s*.27+.025,y+.045,.125)))
for y in[.065,.405]:under_obstacles.append(inflated((-.242,y-.02,.125),(.242,y+.02,.18)))
air('WholeUnderBoxRemainingAir',empty_partition((-.299,.001,.001),(.299,.479,.179),under_obstacles),'Whole bounded under-box air including both sides and every space around the real beams, crossmembers and feet; only actual full material plus 1 mm boundary inset excluded.')
front_obstacles=[inflated((s*.27-.028,-.50,.065),(s*.27+.028,-.18,.12)) for s in[-1,1]]+[inflated((s*.27-.025,-.465,0),(s*.27+.025,-.375,.065)) for s in[-1,1]]+[inflated((-.242,-.44,.065),(.242,-.40,.12))]
air('WholeUnderFrontFootplateAir',empty_partition((-.319,-.499,.001),(.319,-.181,.119),front_obstacles),'Entire bounded under-footplate opening around the real lower frame and its two short feet, all finite connected air included with 1 mm interface border.')
air('WholeBetweenSteppedSideBeamsAir',box((-.241,-.179,.001),(.241,-.001,.179)),'Entire open finite region between both step transitions, ground to box-bearing height, front-plate rear edge to box front.')
obstacles=[inflated((s*.27-.028,-.14,.125),(s*.27+.028,0,.18)) for s in[-1,1]]
air('WholeBoxFrontToFootplateUpperAir',empty_partition((-.319,-.499,.149),(.319,-.001,.609),obstacles),'Entire air above low front plate and in front of complete box front, full width/height/depth, excluding only the two actual stepped bearer upper returns plus 1 mm border.')
# Full below-lid face air, subtract only exact two stops; hinge roots end at u=.026.
ob=[((x-.019,.027,-.040),(x+.019,.067,-.018)) for x in[-.09,.09]]
air('WholeRaisedLidInnerFaceAir',posed(empty_partition((-.299,.027,-.040),(.299,.505,-.019),ob)),'Entire finite layer along full raised inner lid face, only two actual stop footprints plus 1 mm perimeter excluded.')
air('WholeCushionOuterFaceAir',posed(box((-.274,.046,.056),(.274,.486,.080))),'Entire bounded air over full outer cushion face; no extra object may overlap the pad.')
air('WholeRearRimToRaisedCoverAir',box((-.299,.036,.611),(.299,.444,1.16)),'Whole finite box-mouth-to-raised-cover inner clearance; bounded over all inner wall plan and full lid height, no centre-ray substitute.')
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
# Translate every vertex and every finite contact/probe datum by the actual horizontal envelope centre.
vv=[p for g in G.values() for p in g['vertices']];SHIFT=tuple(-(min(p[k] for p in vv)+max(p[k] for p in vv))/2 if k<2 else 0 for k in range(3))
for records in [G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in records.values():g['vertices']=[add(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['points']=[add(p,SHIFT) for p in r['points']];r['plane_m']+=dot(r['axis'],SHIFT)
for r in FOOT_CONTACTS:r['x']+=SHIFT[0];r['y']+=SHIFT[1]
CONTRACT={'single_prop_count':1,'deep_shell':1,'complete_thick_cover':1,'complete_thick_cushion':1,'fixed_cover_degrees':100,'continuous_stepped_side_beams':2,'whole_front_footplate':1,'crossmembers':3,'complete_ground_feet':6,'true_bored_ears':6,'headed_pins':2,'fixed_angle_stops':2,'finite_opposed_contacts':len(CONTACTS),'whole_empty_domains':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_domains':len(SOLID_VOLUMES),'load_motion_or_safety_claim':False}
def measure_seatbox_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-.61)<2e-7
 for n in BEAMS:assert max(p[1] for p in vertices[n])-min(p[1] for p in vertices[n])>.979
 tangent=unit(sub(vertices[LID][2],vertices[LID][0]));angle=math.degrees(math.acos(max(-1,min(1,dot(tangent,(0,-1,0))))));assert abs(angle-100)<.0001,angle
 return dict(CONTRACT,scope='actual full source/export coordinates; complete finite material/air, all interfaces, whole-surface separation, selfchecks and independent real negative gates remain required')
INSIDE_TESTS=[(BODY,add((0,.24,.20),SHIFT),add((0,.24,.30),SHIFT)),(LID,add(frame((0,.25,0)),SHIFT),add(frame((0,.25,-.06)),SHIFT))]
FOCUS=(0,0,.57);ORTHO=1.85
CAMERAS={'gray-front3q':(2.5,-3.5,2.5),'gray-back3q':(-2.5,3.5,2.5),'thumbnail':(2.5,-3.5,2.5),'qa-front':(0,-4,1.85),'qa-side':(4,0,1.85),'qa-top':(0,0,4),'qa-back':(0,4,1.85),'qa-wireframe':(2.5,-3.5,2.5),'silhouette-128-front':(0,-4,1.85),'silhouette-128-side':(4,0,1.85)}
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
root=bpy.data.objects.new('OneFixedFootplateSeatbox',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred six-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_seatbox_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'seatbox_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fishing/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
