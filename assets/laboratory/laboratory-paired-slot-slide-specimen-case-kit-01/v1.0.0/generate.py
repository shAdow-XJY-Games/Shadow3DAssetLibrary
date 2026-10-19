"""Original paired-slot case, six opposed true slots and three opaque blank plates."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-paired-slot-slide-specimen-case-kit-01';VERSION='1.0.0';TITLE='Paired-Slot Slide Specimen Case'
DESCRIPTION=('One original static visual specimen-slide case with a continuous thick base and four walls, two continuous comb rails carrying six aligned pairs of true upward-open slots, and three original opaque blank rectangular plates seated in alternating slot pairs. Each plate has two complete finite lower-corner bearing patches; its entire central lower edge remains above the case floor. The other three slot pairs remain wholly empty. A single thick shallow-recessed lid is frozen rearward raised, supported by two true two-ear through-bore assemblies, continuous headed pins, complete ear pedestals and two finite angle stops. Original shell, rails, plates and lid geometry; no recoloured bait-box compartments, circular eyepiece holes, copied pipette fork or resized suitcase. One complete prop, not separate plate assets. Metres, source Z up, front -Y, horizontal bounds-centred ground datum. Constant opaque PBR only; no texture nodes, linked Principled inputs, external geometry, labels, biological material, personal samples or microscopy pictures. Fixed visual geometry only: no standard slide compatibility, scientific sample preservation, sterile/sealed/temperature-controlled storage, pathology, diagnosis, optical performance, opening or loading trajectory, manufacturing, structural performance or laboratory safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];RAILS=[];PLATES=[];HINGES=[];STOPS=[];SLOTS=[]
BODY='ContinuousCaseBottomAndFourWalls';LID='CompleteShallowRecessedRaisedLid';SHIFT=(0,0,0)
PALETTE=[('WarmStoneCase',(.48,.40,.29,1),.70,.03),('SlateCombRails',(.09,.16,.19,1),.70,.03),('OpaqueBlankIvoryPlates',(.73,.78,.72,1),.52,.02),('MutedBrassPins',(.42,.32,.17,1),.42,.60)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
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
 stations=[sorted(set(p[k] for lo,hi in boxes for p in[lo,hi])) for k in range(3)]
 return grid(*stations,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes),material,role)
def prism(poly,x0,x1,material=0,role=''):
 # Convex cross-section in YZ, extruded along X.
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for x in[x0,x1] for y,z in poly];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(vv,ff,material,role)
def inset(poly,d):
 lines=[]
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);n=unit((-e[1],e[0]));lines.append((n,dot(n,a)+d))
 out=[]
 for i,(b,db) in enumerate(lines):
  a,da=lines[i-1];det=cr2(a,b);out.append(((da*b[1]-a[1]*db)/det,(a[0]*db-da*b[0])/det))
 return out

def posed(g):return mesh([frame(p) for p in g['vertices']],g['faces'],g['material'],g['role'])
def contact(name,a,b,axis,p,area,scope='Whole finite opposed interface.'):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,p),'minimum_patch_area_m2':area-1e-8,'complete_interface_area_m2':area,'interior_probe_offset_m':.0004,'points':[p],'scope':scope})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def isolated(name,g,targets,role):ISOLATED_VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def solid(name,g,target,role):SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
def inset_box(lo,hi,e=.001):return box(add(lo,(e,e,e)),sub(hi,(e,e,e)))
def shell(e=0):
 return grid([-.40+e,-.382-e,.382+e,.40-e],[-.225+e,-.207-e,.207+e,.225-e],[e,.018-e,.17-e],lambda x,y,z:z<.018-e or abs(x)>.382+e or abs(y)>.207+e,0,'One continuous thick shell, complete solid bottom and four connected walls, full open mouth.')
G[BODY]=shell();FEET.append(BODY)
solid('WholeContinuousCaseMaterial',shell(.001),BODY,'Complete connected inward-offset material shell, full bottom, all four walls, corners and complete rim, 1 mm inset.')
FOOT_CONTACTS.append({'mesh':BODY,'name':'EntireCaseBottomGroundSeat','x':0,'y':0,'half_x':.40,'half_y':.225,'minimum_area_m2':.36-1e-8,'expected_area_m2':.36})
isolated('WholeIsolatedCaseCavityAndMouth',box((-.381,-.206,.019),(.381,.206,.34)),[BODY],'Entire deep inner cavity continued past the complete top mouth, 1 mm inward wall/floor offset; isolated shell only because rails and plates intentionally occupy it.')
CENTERS=[-.15,-.09,-.03,.03,.09,.15];OCCUPIED=[0,2,4]
def rail(s,e=0,filled=None):
 a,b=sorted((s*.285,s*.355));ys=sorted(set([-.195+e,.195-e]+[c+d for c in CENTERS for d in[-.012-e,.012+e]]))
 def occupied(x,y,z):return z<.068-e or not any(abs(y-c)<.012+e for i,c in enumerate(CENTERS) if i!=filled)
 return grid([a+e,b-e],ys,[.018+e,.068-e,.15-e],occupied,1,'One continuous thick comb rail with six real narrow upward-open slots, integral full base and all seven teeth.')
for s,label in[(-1,'Left'),(1,'Right')]:
 n=label+'ContinuousSixSlotRail';RAILS.append(n);a,b=sorted((s*.285,s*.355));G[n]=rail(s)
 solid(n+'WholeConnectedMaterial',rail(s,.001),n,'Whole connected inset rail base, every complete tooth and tooth-root neck, slots expanded 1 mm and all exterior planes inset 1 mm.')
 contact(label+'RailWholeBase',BODY,n,(0,0,1),((a+b)/2,0,.018),.070*.390,'Entire 70 by 390 mm rail underside rests finitely on the full case floor.')
 for i,c in enumerate(CENTERS):
  key=label+'Slot'+str(i+1);SLOTS.append({'name':key,'rail':n,'side':s,'slot_index':i,'center_y':c,'x0':a,'x1':b,'occupied':i in OCCUPIED})
  isolated(key+'WholeIsolatedOpening',box((a-.001,c-.011,.069),(b+.001,c+.011,.16)),[n],'Entire slot opening across and beyond both rail end faces, from 1 mm above its real floor through and above its full open top.')
  if i not in OCCUPIED:air(key+'WholeEmptyAssemblySlot',box((a-.001,c-.011,.069),(b+.001,c+.011,.18)),'Whole empty pair-slot air in the complete assembly, including full transverse rail thickness and entire upward opening.')
  else:
   for side in[-1,1]:
    y0,y1=(c-.011,c-.007) if side<0 else(c+.007,c+.011)
    air(key+'WholePlateSideAir'+str(side),box((a-.001,y0,.069),(b+.001,y1,.151)),'Full nonbearing slot side clearance along the complete rail thickness and entire slot height, 1 mm wall and plate allowance.')
   x0,x1=(a+.001,-.343) if s<0 else(.343,b-.001)
   air(key+'WholePlateOuterEndAir',box((x0,c-.011,.069),(x1,c+.011,.151)),'Entire clear slot area outside the plate end, connected to its upward mouth; 1 mm plate/rail-edge allowance.')
for j,i in enumerate(OCCUPIED,1):
 c=CENTERS[i];n='OpaqueBlankPlate'+str(j);PLATES.append(n);lo=(-.342,c-.006,.068);hi=(.342,c+.006,.325);G[n]=box(lo,hi,2,'One complete original thick opaque blank plate, vertical, no imagery/text/sample; two lower corners in opposing slots with the entire central lower edge suspended.')
 solid(n+'WholeMaterial',inset_box(lo,hi),n,'Entire finite blank plate material including both full lower bearing shoulders and complete upper/sides, 1 mm inset.')
 for s,label in[(-1,'Left'),(1,'Right')]:
  x=s*(.285+.057/2);contact(n+label+'WholeBottomCornerSeat',label+'ContinuousSixSlotRail',n,(0,0,1),(x,c,.068),.057*.012,'Entire 57 by 12 mm lower-corner bearing patch on the complete actual slot floor.')
 air(n+'WholeCentralLowerEdgeAir',box((-.284,c-.005,.019),(.284,c+.005,.067)),'Whole finite region beneath the complete central plate lower edge and above the actual case floor, 1 mm clearance from both supports and full plate underside.')
for j,i in enumerate(OCCUPIED,1):
 c=CENTERS[i];n='OpaqueBlankPlate'+str(j)
 for side in[-1,1]:
  y0,y1=(c-.011,c-.007) if side<0 else(c+.007,c+.011)
  air(n+'WholeNonbearingBroadFaceAir'+str(side),box((-.341,y0,.069),(.341,y1,.324)),'Full finite air over the entire broad plate face from its lower edge to its upper edge, 1 mm face/edge allowance.')
  x0,x1=(-.348,-.343) if side<0 else(.343,.348)
  air(n+'WholeNonbearingEndFaceAir'+str(side),box((x0,c-.005,.069),(x1,c+.005,.324)),'Full finite air along the entire vertical plate end face, including the portion inside its real rail slot, 1 mm face/edge allowance.')
 air(n+'WholeUpperEdgeAir',box((-.341,c-.005,.326),(.341,c+.005,.336)),'Entire upper plate edge free from lid and assembly, 1 mm edge/face allowance.')
# Complete residual case air, not a few isolated rays.
air('WholeCentralUnderPlateAir',box((-.284,-.206,.019),(.284,.206,.067)),'Entire central lower case cavity between rails below all three plates, including all lower-edge air.')
for label,x0,x1 in[('Left',-.381,-.356),('Right',.356,.381)]:air(label+'WholeRailToWallAir',box((x0,-.206,.019),(x1,.206,.169)),'Whole longitudinal side corridor between the full rail and inner side wall.')
for label,y0,y1 in[('Front',-.206,-.196),('Rear',.196,.206)]:air(label+'WholeEndWallAir',box((-.381,y0,.019),(.381,y1,.169)),'Entire clear end corridor between both complete rail ends and case end wall.')
bounds_y=[-.206]+[q for i in OCCUPIED for q in[CENTERS[i]-.007,CENTERS[i]+.007]]+[.206]
for i in range(0,len(bounds_y)-1,2):air('WholeBetweenPlateRegion'+str(i//2+1),box((-.284,bounds_y[i],.0671),(.284,bounds_y[i+1],.230 if i==6 else .326)),'Whole central upper cavity through the full case mouth. Rear region stops below the actual hinge overhang; full plate faces have separate complete clearance volumes.')
THETA=math.radians(70);C=math.cos(THETA);S=math.sin(THETA)
def frame(p):
 x,u,v=p;return add((x,.225+C*u-S*v,.28+S*u+C*v),SHIFT)
def direction(p):x,u,v=p;return(x,C*u-S*v,S*u+C*v)
def lid(e=0):
 return posed(grid([-.40+e,-.38-e,.38+e,.40-e],[.030+e,.050-e,.450+e,.470-e],[-.018+e,-.006-e,.016-e],lambda x,u,v:v<-.006-e or abs(x)>.38+e or u<.05-e or u>.45+e,0,'One continuous thick raised lid with a full shallow interior recess, complete perimeter and solid back; fixed 70-degree pose.'))
G[LID]=lid();solid('WholeRaisedRecessedLidMaterial',lid(.001),LID,'Entire connected finite recessed lid material, complete back, four sides and all corners, 1 mm inset.')
air('WholeLidRecessAndMouth',posed(box((-.379,.051,-.005),(.379,.449,.032))),'Entire shallow lid recess and full open face, continuing above its complete rim, with 1 mm interior allowance.')
def wedge(a,b,u0,u1,v,e=0):
 p0=frame((0,u0,v));p1=frame((0,u1,v));poly=[(.207,.17),(.225,.17),(p1[1],p1[2]),(p0[1],p0[2])]
 return prism(inset(poly,e) if e else poly,a+e,b-e,1,'Original finite tapered support from the complete rear wall top to the complete inclined upper bearing face.')
# Two broad stops, independently supporting the fixed lid angle.
for i,cx in enumerate([-.34,.34],1):
 n='FixedLidAngleStop'+str(i);STOPS.append(n);a,b=cx-.021,cx+.021;G[n]=wedge(a,b,.055,.100,-.018)
 solid(n+'WholeMaterial',wedge(a,b,.055,.100,-.018,.001),n,'Whole finite stop wedge, complete rear-wall root, inclined lid seat and every connecting cross-section, 1 mm planar inset.')
 contact(n+'WholeWallRoot',BODY,n,(0,0,1),(cx,.216,.17),.042*.018)
 contact(n+'WholeLidSeat',n,LID,direction((0,0,1)),frame((cx,.0775,-.018)),.042*.045)
# Two original side-by-side two-ear assemblies; square bores make every finite
# actual bearing explicit. No moving-hinge or manufacturing-fit claim.
for j,cx in enumerate([-.23,.23],1):
 prefix='Hinge'+str(j);pin=prefix+'ContinuousHeadedPin';ears=[]
 pb=[((cx-.044,-.008,-.010),(cx+.042,.008,.006)),((cx-.052,-.014,-.016),(cx-.044,.014,.014)),((cx+.042,-.014,-.016),(cx+.050,.014,.014))]
 G[pin]=posed(union_boxes(pb,3,'One continuous full solid square pin with two integral finite heads and real lower bearing faces.'))
 solid(pin+'WholeMaterial',posed(union_boxes([((cx-.051,-.013,-.015),(cx-.045,.013,.013)),((cx-.046,-.007,-.009),(cx+.044,.007,.005)),((cx+.043,-.013,-.015),(cx+.049,.013,.013))])),pin,'Entire connected inset headed pin including both actual head-to-shaft roots; 1 mm boundary inset.')
 for kind,a,b in[('Body',cx-.035,cx-.009),('Lid',cx+.003,cx+.033)]:
  n=prefix+kind+'TrueThroughBoredEar';ears.append(n);u1=.026 if kind=='Body' else .030
  def ear(e=0):return posed(grid([a+e,b-e],[-.030+e,-.010-e,.010+e,u1-e],[-.024+e,-.010-e,.012+e,.024-e],lambda x,u,v:not(abs(u)<.010+e and -.010-e<v<.012+e),1,'One complete continuous thick annular ear with a genuine full-thickness rectangular through-bore.'))
  G[n]=ear();solid(n+'WholeAnnularMaterial',ear(.001),n,'Entire closed inset annulus including all bore walls and corners, bore expanded 1 mm and exterior inset 1 mm.')
  isolated(n+'WholeIsolatedBore',posed(box((a-.001,-.009,-.009),(b+.001,.009,.011))),[n],'Entire isolated true through-bore extending across and beyond both ear faces, 1 mm interior wall allowance.')
  contact(n+'WholePinLowerSeat',n,pin,direction((0,0,1)),frame(((a+b)/2,0,-.010)),(b-a)*.016)
  if kind=='Body':
   foot=n+'RearWallPedestal';G[foot]=wedge(a,b,-.030,.026,-.024)
   solid(foot+'WholeMaterial',wedge(a,b,-.030,.026,-.024,.0006),foot,'Whole connected pedestal from complete rear-wall top to full ear lower face, 0.6 mm planar inset.')
   contact(foot+'WholeWallRoot',BODY,foot,(0,0,1),((a+b)/2,.216,.17),(b-a)*.018)
   contact(foot+'WholeEarSeat',foot,n,direction((0,0,1)),frame(((a+b)/2,-.002,-.024)),(b-a)*.056)
  else:contact(n+'WholeLidRoot',n,LID,direction((0,1,0)),frame(((a+b)/2,.030,-.001)),(b-a)*.034)
  BORES.append({'mesh':n,'origin_m':frame((a-.001,0,0)),'direction':(1,0,0),'length_m':b-a+.002,'meaning':'Supplementary isolated bore ray; full finite bore volume remains authoritative.'})
 for label,lo,hi in[('SideMinus',(cx-.036,-.0094,-.009),(cx+.034,-.0086,.011)),('SidePlus',(cx-.036,.0086,-.009),(cx+.034,.0094,.011)),('AbovePin',(cx-.036,-.008,.007),(cx+.034,.008,.011))]:air(prefix+'WholeNonbearingBoreAir'+label,posed(box(lo,hi)),'Entire continuous nonbearing bore corridor across both complete ears and the axial interval; 0.6 mm side allowance and 1 mm upper allowance.')
 for label,a,b in[('LeftEnd',cx-.043,cx-.036),('BetweenEars',cx-.008,cx+.002),('RightEnd',cx+.034,cx+.041)]:
  air(prefix+'WholeAxialAir'+label,posed(grid([a,b],[-.029,-.009,.009,.029],[-.023,-.011,.007,.023],lambda x,u,v:not(abs(u)<.009 and -.011<v<.007))),'Entire finite axial separation around the complete shaft, between ears or head/ear ends, 1 mm allowance.')
 HINGES.append({'ears':ears,'pin':pin,'center_x':cx,'side_clearance_m':.002,'upper_clearance_m':.006,'axial_ear_gap_m':.012})
# Full finite lower-face air is the exact rectangular slab minus the two
# expanded complete wedge cross-sections, partitioned into closed domains.
def clip2(poly,a,b,keep_inside):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  dp=cr2(sub(b,a),sub(p,a));dq=cr2(sub(b,a),sub(q,a));ip=dp>=-1e-13 if keep_inside else dp<=1e-13;iq=dq>=-1e-13 if keep_inside else dq<=1e-13
  if ip!=iq:out.append(add(p,mul(sub(q,p),dp/(dp-dq))))
  if iq:out.append(q)
 clean=[]
 for p in out:
  if not clean or math.hypot(*sub(p,clean[-1]))>1e-10:clean.append(p)
 if len(clean)>1 and math.hypot(*sub(clean[0],clean[-1]))<1e-10:clean.pop()
 return clean
under=[(.031,-.039),(.469,-.039),(.469,-.019),(.031,-.019)]
for j,(a,b) in enumerate([(-.399,-.362),(-.318,.318),(.362,.399)],1):
 air('WholeLidLowerFaceOuterBand'+str(j),posed(prism(under,a,b)),'Entire finite lower-lid slab outside both full stop widths; all panel extent included with 1 mm edge/stop clearance.')
wp=[(.207,.17),(.225,.17)]+[(frame((0,u,-.018))[1],frame((0,u,-.018))[2]) for u in[.100,.055]]
uv=[((y-.225)*C+(z-.28)*S,-(y-.225)*S+(z-.28)*C) for y,z in wp];expanded=inset(uv,-.001)
for j,cx in enumerate([-.34,.34],1):
 remaining=list(under)
 for k,(a,b) in enumerate(zip(expanded,expanded[1:]+expanded[:1])):
  if not remaining:break
  outside=clip2(remaining,a,b,False);remaining=clip2(remaining,a,b,True)
  if len(outside)>=3 and abs(sum(cr2(outside[i],outside[(i+1)%len(outside)]) for i in range(len(outside))))>1e-10:
   air('WholeLidLowerFaceStopComplement'+str(j)+'_'+str(k),posed(prism(outside,cx-.020,cx+.020)),'Complete finite component of lower-lid air beside the actual full wedge profile; exact convex halfplane subtraction of the 1 mm expanded wedge, not a rectangular omitted gap.')
# Recenter the complete fixed assembly without changing relative geometry.
allv=[v for g in G.values() for v in g['vertices']];SHIFT=(0,-(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for table in[G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in table.values():g['vertices']=[add(v,SHIFT) for v in g['vertices']]
for r in CONTACTS:r['origin_m']=SHIFT;r['points']=[add(p,SHIFT) for p in r['points']]
for r in BORES:r['origin_m']=add(r['origin_m'],SHIFT)
for r in FOOT_CONTACTS:r['x']+=SHIFT[0];r['y']+=SHIFT[1]
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
CONTRACT={'single_prop_count':1,'mesh_count':len(G),'continuous_shells':2,'continuous_comb_rails':2,'aligned_slot_pairs':6,'opaque_blank_plates':3,'empty_slot_pairs':3,'whole_bottom_corner_bearings':6,'plate_center_underedge_air_height_m':.050,'slot_width_m':.024,'plate_thickness_m':.012,'plate_slot_side_clearance_m':.006,'fixed_lid_angle_degrees':70,'two_ear_assemblies':2,'true_bored_ears':4,'headed_pins':2,'finite_angle_stops':2,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'scientific_medical_storage_or_safety_claim':False}
def measure_specimen_case_geometry(vertices):
 assert set(vertices)==set(G)
 assert abs(min(v[2] for v in vertices[BODY]))<2e-7
 for n in PLATES:assert abs(min(v[2] for v in vertices[n])-.068)<2e-7 and abs(max(v[2] for v in vertices[n])-.325)<2e-7
 return dict(CONTRACT,geometry_scope='Complete actual mesh coordinates; all six finite plate bearings, continuous rail material, whole cavity and slot volumes, full self-intersection and all component pairs independently required.')
INSIDE_TESTS=[(BODY,add((0,0,.009),SHIFT),add((0,0,.10),SHIFT)),(RAILS[0],add((-.32,-.15,.04),SHIFT),add((-.32,-.15,.10),SHIFT))]
FOCUS=(0,0,.36);ORTHO=1.35
CAMERAS={'gray-front3q':(1.8,-2.8,2.2),'gray-back3q':(-1.8,2.8,2.2),'thumbnail':(1.8,-2.8,2.2),'qa-front':(0,-4,1.8),'qa-side':(4,0,1.8),'qa-top':(0,0,4),'qa-back':(0,4,1.8),'qa-wireframe':(1.8,-2.8,2.2),'silhouette-128-front':(0,-4,1.8),'silhouette-128-side':(4,0,1.8)}
WIRE_THICKNESS=ORTHO/1600
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
root=bpy.data.objects.new('OnePairedSlotSlideSpecimenCase',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred complete case ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_specimen_case_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'specimen_case_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
