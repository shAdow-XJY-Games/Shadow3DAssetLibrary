"""Original fixed-open twin-pan hard-shell travel case. One static visual prop, one structure only."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='baggage-open-clamshell-wheeled-case-01';VERSION='1.0.0';TITLE='Open Clamshell Wheeled Hard Case'
DESCRIPTION=('One original hard-shell wheeled travel case in one fixed flat-open pose, counted as one static prop and one structure only. Separate deep main pan and shallow lid pan have complete rounded thick walls, complete continuously ribbed backs, inner floors and continuous rims. Three shallow flat-bottom ribs on each exterior back are integral continuous thick shell surfaces. Both complete empty cavities remain unpartitioned. Two three-ear true-bored hinge groups have continuous fixed pins with complete finite lower bearings and real side/top clearance. Two true-bored fixed wheels have continuous axles, complete bored U forks and positive wheel-contour clearance. Two real through-bored short guides support a single original continuous stowed U pull handle on finite lower bearings and end shoulders; remaining guide air is empty. Every component has a complete finite contact path to the six complete finite rib landing bands. Original shell, wheel, guide and whole-case geometry, not a recolored soft holdall, enlarged solid astronomy case, bait-box divider deletion, camera-bag lid change or reused battery box. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. Opaque constant PBR colors; no textures, logo, baggage contents or scene. Only this fixed visual appearance: no closure fit, continuous opening, rolling, telescoping, capacity, airline dimensions, human grip, load, strength, impact, waterproofing, theft protection, material/manufacturing, durability or safety claim. Original plural hard-shell structure family remains partial and other forms unverified.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];HINGES=[];WHEELS=[];GUIDES=[]
BODY='DeepMainPan_ContinuousRibbedShell';LID='ShallowLidPan_ContinuousRibbedShell';HANDLE='OneContinuousStowedUPullHandle'
PALETTE=[('MutedAtlanticShell',(.055,.25,.31,1),.48,.12),('WarmPalePanInterior',(.51,.56,.52,1),.71,.02),('DarkEdgeAndTyre',(.035,.052,.060,1),.68,.02),('SatinAlloyHardware',(.35,.40,.42,1),.43,.57),('MutedCopperEndDetail',(.51,.26,.12,1),.51,.12)]
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
 boxes=[(tuple(round(v,9) for v in lo),tuple(round(v,9) for v in hi)) for lo,hi in boxes];stations=[sorted(set(p[k] for lo,hi in boxes for p in [lo,hi])) for k in range(3)]
 return grid(*stations,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes),material,role)
def contact(name,a,b,axis,p,area,points=None,offset=.0004):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'points':points or [p],'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def solid(name,g,targets,role):SOLID_VOLUMES[name]=dict(g,targets=targets,role=role)
# Original continuous exterior-back ribs. Each pan is one closed shell; three
# full flat finite landing bands are integral, while shallow valleys sit 6 mm up.
# All internal floor surfaces remain flat and the entire cavity is empty.
RIB_X=[-.21,-.175,-.150,-.105,-.085,-.045,-.025,.025,.045,.085,.105,.150,.175,.21]
RIB_Z=[.006,.006,0,0,.006,.006,0,0,.006,.006,0,0,.006,.006]
def bottom_z(x):
 for a,b,u,v in zip(RIB_X,RIB_X[1:],RIB_Z,RIB_Z[1:]):
  if a-1e-10<=x<=b+1e-10:return u+(v-u)*(x-a)/(b-a)
 return .006

def original_outline(cx):
 p=[]
 for ccx,ccy,a0 in [(.155,-.285,-90),(.155,.285,0),(-.155,.285,90),(-.155,-.285,180)]:
  for i in range(7):
   a=math.radians(a0+15*i);p.append((cx+ccx+.055*math.cos(a),ccy+.055*math.sin(a)))
 return p

def offset_poly(poly,d):
 out=[]
 for i,p in enumerate(poly):
  a=poly[i-1];b=poly[(i+1)%len(poly)];e=unit(sub(p,a));f=unit(sub(b,p));n=(-e[1],e[0]);m=(-f[1],f[0]);den=1+dot(n,m)
  out.append(add(p,mul(add(n,m),d/den)))
 return out

def outline(cx,inset=0):return offset_poly(original_outline(cx),inset)
def clip_x(poly,x,keep_above):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[0]-x)*(1 if keep_above else -1);db=(b[0]-x)*(1 if keep_above else -1);ia=da>=-1e-10;ib=db>=-1e-10
  if ia:out.append(a)
  if ia!=ib:out.append(add(a,mul(sub(b,a),da/(da-db))))
 clean=[]
 for p in out:
  p=tuple(round(v,9) for v in p)
  if not clean or p!=clean[-1]:clean.append(p)
 if clean and clean[0]==clean[-1]:clean.pop()
 return clean

def pan(cx,height,outward=0,inset=0):
 poly=outline(cx,inset);cuts=[cx+x for x in RIB_X if min(p[0] for p in poly)+1e-8<cx+x<max(p[0] for p in poly)-1e-8]
 perimeter=[];inner=[];innerpoly=outline(cx,.019-inset)
 for k,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
  ia,ib=innerpoly[k],innerpoly[(k+1)%len(innerpoly)];perimeter.append(a);inner.append(ia)
  if abs(b[0]-a[0])>1e-10:
   hits=sorted((x-a[0])/(b[0]-a[0]) for x in cuts if min(a[0],b[0])+1e-8<x<max(a[0],b[0])-1e-8)
   perimeter.extend(add(a,mul(sub(b,a),t)) for t in hits);inner.extend(add(ia,mul(sub(ib,ia),t)) for t in hits)
 perimeter=[tuple(round(v,8) for v in p) for p in perimeter];inner=[tuple(round(v,8) for v in p) for p in inner]
 rings=[[(x,y,bottom_z(x-cx)+inset) for x,y in perimeter],[(x,y,.016) for x,y in perimeter],[(x,y,height-inset) for x,y in perimeter],[(x,y,height-inset) for x,y in inner],[(x,y,.025-inset) for x,y in inner]]
 n=len(perimeter);vv=[tuple(round(c,8) for c in v) for ring in rings for v in ring];ff=[];fm=[];lookup={v:i for i,v in enumerate(vv)}
 def vid(p):
  p=tuple(round(c,8) for c in p)
  matches=[i for i,v in enumerate(vv[:n]) if abs(v[0]-p[0])<2e-8 and abs(v[1]-p[1])<2e-8]
  assert len(matches)==1,(p,matches)
  return matches[0]
 allcuts=[min(p[0] for p in poly)]+cuts+[max(p[0] for p in poly)]
 for a,b in zip(allcuts,allcuts[1:]):
  cell=clip_x(clip_x(poly,a,True),b,False)
  if len(cell)>2:ff.append(tuple(vid((x,y,bottom_z(x-cx)+inset)) for x,y in reversed(cell)));fm.append(0)
 for j in range(len(rings)-1):
  for i in range(n):ff.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));fm.append(0 if j<2 else 2 if j==2 else 1)
 ff.append(tuple(range(n*(len(rings)-1),n*len(rings))));fm.append(1)
 g=mesh(vv,ff,0,'One complete rounded thick pan shell, integral three shallow back ribs with finite full flat landing bands, full inner floor and continuous rim.');g['face_materials']=fm;return g
for name,cx,h,side in [(BODY,-.255,.165,-1),(LID,.255,.095,1)]:
 G[name]=pan(cx,h,side);FEET.append(name)
 air(name+'_CompleteUnpartitionedCavity',prism(outline(cx,.020),.026,h+.006),'Entire rounded inner cavity through the mouth, including every corner and the continuous rim opening, with 1 mm wall/floor inset.')
 solid(name+'_WholeInsetShellMaterial',pan(cx,h,side,.002),[name],'One complete connected finite material shell inset 2 mm from exterior, inner floor, inner walls and rim; includes full bottom, all roots/corners and integral back-rib material.')
# Long-edge connection: two independent three-ear assemblies, all original and fixed.
def tube_rect(axis,a,b,outer,inner,material=3,role=''):
 # Extrude an annulus in cross coordinates; axis chooses world placement.
 x0,x1,z0,z1=outer;u0,u1,v0,v1=inner;out=[(x0,z0),(x1,z0),(x1,z1),(x0,z1)];inn=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
 def tr(p):return (p[0],p[2],p[1]) if axis=='y' else (p[2],p[0],p[1])
 vv=[tr((x,z,y)) for y,poly in [(a,out),(b,out),(a,inn),(b,inn)] for x,z in poly];ff=[]
 for i in range(4):j=(i+1)%4;ff.extend([(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)])
 return mesh(vv,ff,material,role)
for j,c in enumerate([-.19,.19]):
 ears=[];pin=f'Hinge_{j+1}_ContinuousFixedPin'
 for label,a,b in [('LowerY',c-.039,c-.023),('Center',c-.017,c+.017),('UpperY',c+.023,c+.039)]:
  n=f'Hinge_{j+1}_{label}TrueBoredEar';G[n]=tube_rect('y',a,b,(-.024,.024,.050,.094),(-.010,.010,.061,.081),3,'One full thick annular ear with genuine rectangular through hole.');ears.append(n)
  air(n+'_WholeIsolatedBore',box((-.009,a-.001,.062),(.009,b+.001,.080)),'Entire finite ear through-bore extending past both mouths, isolated against the actual ear.',[n])
  contact(n+'_PinLowerBearing',n,pin,(0,0,1),(0,(a+b)/2,.061),(b-a)*.014-1e-8)
  if label!='Center':
   br=n+'_MainPanBridge';G[br]=box((-.045,a,.058),(-.024,b,.086),3,'Full finite end-to-end bridge between main pan and true-bored ear.')
   contact(br+'_ShellRoot',BODY,br,(1,0,0),(-.045,(a+b)/2,.072),(b-a)*.028-1e-8);contact(br+'_EarEnd',br,n,(1,0,0),(-.024,(a+b)/2,.072),(b-a)*.028-1e-8)
  else:
   br=f'Hinge_{j+1}_LidTongue';G[br]=box((.024,a,.059),(.045,b,.083),3,'Full finite tongue from central ear outer face to shallow lid wall.')
   contact(br+'_EarEnd',n,br,(1,0,0),(.024,c,.071),(b-a)*.024-1e-8);contact(br+'_LidRoot',br,LID,(1,0,0),(.045,c,.071),(b-a)*.024-1e-8)
 G[pin]=box((-.007,c-.047,.061),(.007,c+.047,.075),3,'One continuous square fixed through-pin with full lower finite bearing in all three true bores.')
 for sign,label in [(-1,'Low'),(1,'High')]:
  a,b=(c-.054,c-.047) if sign<0 else (c+.047,c+.054);cap=pin+'_'+label+'Cap';G[cap]=box((-.012,a,.058),(.012,b,.080),4,'Thick fixed end plate finitely attached to the entire pin end, separated from neighboring ear.')
  if sign<0:contact(cap+'_Pin',cap,pin,(0,1,0),(0,b,.068),.0001959)
  else:contact(cap+'_Pin',pin,cap,(0,1,0),(0,a,.068),.0001959)
 for label,lo,hi in [('Left',(-.009,c-.046,.062),(-.008,c+.046,.080)),('Right',(.008,c-.046,.062),(.009,c+.046,.080)),('Above',(-.007,c-.046,.076),(.007,c+.046,.080))]:air(f'Hinge_{j+1}_WholeRemainingBoreAir_'+label,box(lo,hi),'Complete continuous residual coaxial bore air through all ears and axial intervals, excluding the intended lower bearing.')
 HINGES.append({'ears':ears,'pin':pin,'center_y_m':c,'square_pin_side_m':.014,'bore_x_width_m':.020,'bore_height_m':.020,'lateral_clearance_m':.003,'upper_clearance_m':.006})
# Two wheel/fork units at the main short end. Every wheel is a solid annulus with
# an actual square bore; the outer tyre contour is 24-sided and closed.
def wheel(cx):
 n=24;outer=[];inner=[]
 for i in range(n):
  a=math.tau*i/n;u,v=math.cos(a),math.sin(a);outer.append((-.397+.043*u,.079+.043*v));s=.012/max(abs(u),abs(v));inner.append((-.397+s*u,.079+s*v))
 vv=[(x,y,z) for x,poly in [(cx-.016,outer),(cx+.016,outer),(cx-.016,inner),(cx+.016,inner)] for y,z in poly];ff=[];fm=[]
 for i in range(n):
  j=(i+1)%n;ff.extend([(i,j,j+n,i+n),(i+2*n,i+3*n,j+3*n,j+2*n),(i,i+2*n,j+2*n,j),(i+n,j+n,j+3*n,i+3*n)]);fm.extend([2,3,2,2])
 g=mesh(vv,ff,2,'One complete closed fixed wheel with real square through-axle hole and full faceted tyre contour.');g['face_materials']=fm;return g
for j,cx in enumerate([-.365,-.145]):
 fork=f'Wheel_{j+1}_ContinuousBoredUFork';w=f'Wheel_{j+1}_TrueBoredTyre';ax=f'Wheel_{j+1}_ContinuousAxle'
 xs=[cx-.035,cx-.023,cx+.023,cx+.035];ys=[-.429,-.408,-.386,-.350,-.340];zs=[.049,.067,.091,.112]
 G[fork]=grid(xs,ys,zs,lambda x,y,z:(abs(x-cx)>.023 or y>-.350) and not(abs(x-cx)>.023 and -.408<y<-.386 and .067<z<.091),3,'One continuous U fork, full rear shell root, two thick side cheeks and two real coaxial square axle bores.')
 contact(fork+'_WholeShellRoot',fork,BODY,(0,1,0),(cx,-.340,.080),.070*.063-1e-8)
 G[w]=wheel(cx);G[ax]=box((cx-.040,-.406,.067),(cx+.040,-.388,.085),3,'One continuous square axle through both fork cheeks and fixed wheel; entire lower finite bearing in all three holes.')
 contact(w+'_AxleLowerBearing',w,ax,(0,0,1),(cx,-.397,.067),.032*.018-1e-8)
 contact(fork+'_TwoAxleBearings',fork,ax,(0,0,1),(cx-.029,-.397,.067),.024*.018-1e-8,points=[(cx-.029,-.397,.067),(cx+.029,-.397,.067)])
 for sign,label in [(-1,'Left'),(1,'Right')]:
  a,b=(cx-.047,cx-.040) if sign<0 else (cx+.040,cx+.047);cap=ax+'_'+label+'Head';G[cap]=box((a,-.412,.061),(b,-.382,.091),4,'Thick fixed axle head, full finite pin-end seat and positive cheek clearance.')
  if sign<0:contact(cap+'_Axle',cap,ax,(1,0,0),(b,-.397,.076),.0003239)
  else:contact(cap+'_Axle',ax,cap,(1,0,0),(a,-.397,.076),.0003239)
 air(w+'_WholeIsolatedBore',box((cx-.017,-.408,.068),(cx+.017,-.386,.090)),'Full finite wheel bore reaching past both side mouths; checked against the complete wheel only.',[w])
 for side in [-1,1]:
  a,b=(cx-.036,cx-.022) if side<0 else(cx+.022,cx+.036)
  air(fork+f'_IsolatedCheekBore_{side}',box((a,-.407,.068),(b,-.387,.090)),'Entire finite true fork-cheek bore extending through both mouths.',[fork])
 for label,lo,hi in [('Front',(cx-.039,-.407,.068),(cx+.039,-.4065,.090)),('Rear',(cx-.039,-.3875,.068),(cx+.039,-.387,.090)),('Above',(cx-.039,-.405,.086),(cx+.039,-.389,.090))]:air(ax+'_WholeResidualBoreAir_'+label,box(lo,hi),'Entire finite assembled axle-to-bore residual air through wheel and both fork cheeks; intended lower bearing excluded.')
 WHEELS.append({'wheel':w,'fork':fork,'axle':ax,'center_x_m':cx,'wheel_radius_m':.043,'wheel_width_m':.032,'side_clearance_to_cheek_m':.007,'minimum_back_contour_clearance_m':.004})
# Two through guides and one continuous fixed stowed U handle. The complete air
# bodies include the unoccupied blind end at the pan and every side/top recess.
handleboxes=[]
for j,cx in enumerate([-.365,-.145]):
 n=f'PullGuide_{j+1}_TrueThroughSleeve';G[n]=tube_rect('y',.340,.420,(cx-.016,cx+.016,.078,.112),(cx-.008,cx+.008,.085,.105),3,'One short thick guide sleeve with complete rectangular through-bore; full annular rear root on main pan.')
 contact(n+'_WholePanRoot',BODY,n,(0,1,0),(cx,-0+.340,.095),.032*.034-.016*.020-1e-8,points=[(cx-.012,.340,.095)])
 contact(n+'_HandleLowerBearing',n,HANDLE,(0,0,1),(cx,.390,.085),.012*.065-1e-8)
 contact(n+'_HandleStopShoulder',n,HANDLE,(0,1,0),(cx-.011,.420,.094),.026*.028-.016*.020-1e-8)
 handleboxes.extend([((cx-.006,.355,.085),(cx+.006,.466,.097)),((cx-.013,.420,.080),(cx+.013,.432,.108))])
 air(n+'_WholeIsolatedBore',box((cx-.007,.339,.086),(cx+.007,.421,.104)),'Full finite guide bore through both mouths, isolated against its sleeve.',[n])
 # Exact conforming connected remaining guide air, subtraction of the intended
 # rail expanded by 1 mm. The lower seated rail face has no falsely claimed gap.
 xs=[cx-.007,cx-.006-0.001,cx+.006+.001,cx+.007]
 # Left/right full side strips have only 2 mm nominal clearance: use 0.5 mm insets.
 for label,lo,hi in [('Left',(cx-.0075,.341,.0855),(cx-.0065,.4195,.1045)),('Right',(cx+.0065,.341,.0855),(cx+.0075,.4195,.1045)),('Above',(cx-.006,.341,.098),(cx+.006,.4195,.104)),('BlindEnd',(cx-.006,.341,.086),(cx+.006,.354,.098))]:air(n+'_WholeRemainingAir_'+label,box(lo,hi),'Complete partition of finite guide residual air including both narrow sides, full top and closed-end interval; 0.5–1 mm boundary inset.')
 GUIDES.append({'sleeve':n,'center_x_m':cx,'bore_width_m':.016,'bore_height_m':.020,'rail_width_m':.012,'rail_height_m':.012,'side_clearance_m':.002,'upper_clearance_m':.008})
handleboxes.append(((-.371,.466,.085),(-.139,.482,.105)))
G[HANDLE]=union_boxes(handleboxes,2,'One original continuous fixed U handle: both square rails, two integral finite guide-stop shoulders and the complete transverse grip; no separate floating bars.')
air('WholeUPullHandleOpening',box((-.358,.433,.086),(-.152,.465,.104)),'Entire finite opening inside the stowed U grip between both rails and the crossbar, inset 1 mm; not a decorative dark strip.')
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,SOLID_VOLUMES]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
GROUND_BANDS=[{'mesh':n,'x_min_m':cx+a-SHIFT[0],'x_max_m':cx+b-SHIFT[0],'y_min_m':-.34-SHIFT[1],'y_max_m':.34-SHIFT[1],'z_m':0,'expected_area_m2':(b-a)*.68} for n,cx in [(BODY,-.255),(LID,.255)] for a,b in [(-.150,-.105),(-.025,.025),(.105,.150)]]
CONTRACT={'single_prop_count':1,'one_fixed_flat_open_structure_only':True,'original_plural_family_remains_partial':True,'deep_main_pan':1,'shallow_lid_pan':1,'full_unpartitioned_empty_cavities':2,'complete_ground_back_rib_bands':6,'integral_exterior_back_ribs':6,'three_ear_hinges':2,'true_hinge_bores':6,'fixed_continuous_hinge_pins':2,'true_bored_fixed_wheels':2,'continuous_bored_U_forks':2,'continuous_axles':2,'true_through_guides':2,'one_continuous_stowed_U_handle':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'motion_load_or_safety_claim':False}
def measure_suitcase_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-.165)<2e-7 and abs(max(p[2] for p in vertices[LID])-.095)<2e-7
 return dict(CONTRACT,geometry_scope='actual source/export coordinates; complete cavity/material, finite contact, full clearance and real negative gates remain required')
INSIDE_TESTS=[(BODY,sub((-.255,0,.012),SHIFT),sub((-.255,0,.07),SHIFT)),(LID,sub((.255,0,.012),SHIFT),sub((.255,0,.06),SHIFT))]
FOCUS=(0,0,.045);ORTHO=1.38
CAMERAS={'gray-front3q':(1.25,-1.70,2.15),'gray-back3q':(-1.25,1.70,2.15),'thumbnail':(1.25,-1.70,2.15),'qa-front':(0,-2.4,1.45),'qa-side':(2.4,0,1.45),'qa-top':(0,0,3),'qa-back':(0,2.4,1.45),'qa-wireframe':(1.25,-1.70,2.15),'silhouette-128-front':(0,-2.4,1.45),'silhouette-128-side':(2.4,0,1.45)}
WIRE_THICKNESS=ORTHO/1400

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
root=bpy.data.objects.new('OneFixedOpenClamshellWheeledCase',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred six finite back-rib landing-band datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_suitcase_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'suitcase_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/baggage/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'baggage','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
