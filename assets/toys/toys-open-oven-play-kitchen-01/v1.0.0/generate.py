"""Original one-piece play-kitchen assembly with true oven, pierced fixed door and independent basin; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='toys-open-oven-play-kitchen-01';VERSION='1.0.0';TITLE='Open Oven Play Kitchen'
DESCRIPTION=('One original static play-kitchen visual assembly: a continuous shared cabinet and rear upstand on four complete feet, one pierced continuous counter, a true deep independently rim-seated basin, two fixed annular countertop marks, an empty oven with a finite supported shelf, and an open storage bay with its own shelf. A thick 90-degree side-open door has a genuine through-window and integral full-bore ears. Two complete headed square pins pass through the aligned body and door ears; complete ear underseats, head seats and two integral fixed stops support the single pose. An original short solid-ended spout is decorative and blind. All geometry newly authored as one prop, no old stove/sink scaling or furniture assembly. Metres, native Z up, front -Y, horizontal bounds-centred ground origin. Constant opaque PBR only: no TEX_* nodes, linked Principled inputs, texture, text, branding, transparency or animation. Static visual appearance only. No heating, water supply/drainage, electricity, cooking, door/knob interaction, child scale/age suitability, pinch or swallowing protection, food/material safety, load/anti-tip, manufacturing, toy/child safety certification or old-asset compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousSharedCabinet';COUNTER='PiercedContinuousCounter';BASIN='IndependentThickBasin';DOOR='FixedOpenWindowDoor';OVEN_SHELF='FiniteOvenShelf';STORAGE_SHELF='FiniteStorageShelf';PINS=[]
PALETTE=[('SoftLagoonCabinet',(.10,.37,.36,1),.69,.0),('WarmCreamCounterAndBasin',(.76,.68,.48,1),.63,.0),('ClayDoorAndRingMarks',(.67,.27,.14,1),.67,.0),('WarmDarkFeetAndShelves',(.25,.17,.10,1),.72,.0),('PaleMetalHardware',(.44,.46,.42,1),.46,.45)]
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

def isolated(name,g,targets,role):ISOLATED_VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def inset_box(lo,hi,e=.001):return box(tuple(x+e for x in lo),tuple(x-e for x in hi))
# One continuous closed material boundary, including floor, sides, partition,
# rear upstand, finite shelf ledges, holed body ears and fixed stops.
BB=[((-.60,-.26,.12),(.60,.26,.16)),((-.60,-.26,.16),(-.565,.225,.76)),((.565,-.26,.16),(.60,.225,.76)),((-.035,-.26,.16),(.035,.225,.76)),((-.60,.225,.16),(.60,.26,.94))]
for lo,hi in [((-.565,-.22,.365),(-.52,.215,.39)),((-.08,-.22,.365),(-.035,.215,.39)),((.035,-.22,.355),(.08,.215,.38)),((.52,-.22,.355),(.565,.215,.38))]:BB.append((lo,hi))
for z in [.20,.55]:BB.append(((-.64,-.34,z),(-.565,-.24,z+.035)))
for z in [.30,.65]:BB.append(((-.64,-.34,z),(-.565,-.24,z+.035)))
xs=sorted(set([-.628,-.612]+[p[0] for q in BB for p in q]));ys=sorted(set([-.328,-.312]+[p[1] for q in BB for p in q]));zs=sorted(set(p[2] for q in BB for p in q))
def in_boxes(x,y,z,boxes):return any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes)
def body_bore(x,y,z,e=0):return -.628-e<x<-.612+e and -.328-e<y<-.312+e and any(a-e<z<a+.035+e for a in [.20,.55])
G[BODY]=grid(xs,ys,zs,lambda x,y,z:in_boxes(x,y,z,BB) and not body_bore(x,y,z),0,'Original continuous shared cabinet with real oven and storage bays, integrated thick back upstand, full shelf ledges, two pierced body ears and two fixed stops.')
for i,(lo,hi) in enumerate(BB[:9],1):solid('SharedCabinetWholeSlab_'+str(i),inset_box(lo,hi),[BODY],'Complete finite original body slab or shelf ledge including its full integral root, 1 mm boundary inset.')
for j,z in enumerate([.20,.55],1):
 solid('BodyEar_'+str(j)+'_WholeRingAndRoot',grid([-.639,-.629,-.611,-.566],[-.339,-.329,-.311,-.241],[z+.001,z+.034],lambda x,y,z:not(-.629<x<-.611 and -.329<y<-.311)),[BODY],'Entire body ear material and root with full expanded bore ring, 1 mm inset; not point witnesses.')
 isolated('BodyEar_'+str(j)+'_WholeBore',box((-.627,-.327,z-.001),(-.613,-.313,z+.036)),[BODY],'Entire isolated body-ear through-bore over its full thickness and both mouths, 1 mm lateral inset.')
for j,z in enumerate([.30,.65],1):solid('Stop_'+str(j)+'_WholeMaterial',inset_box((-.64,-.34,z),(-.565,-.24,z+.035)),[BODY],'Whole integral stop including its finite root into the cabinet side.')
for ix,x in enumerate([-.51,.51],1):
 for iy,y in enumerate([-.17,.17],1):
  n=f'CompleteFoot_{ix}_{iy}';G[n]=box((x-.04,y-.04,0),(x+.04,y+.04,.12),3,'Complete finite square foot under common cabinet floor.');FEET.append(n)
  contact(n+'_WholeFloorSeat',n,BODY,(0,0,1),(x,y,.12),.006399)
  FOOT_CONTACTS.append({'mesh':n,'name':n+'_WholeGroundSole','x':x,'y':y,'half_x':.04,'half_y':.04,'minimum_area_m2':.006399})
  solid(n+'_CompleteMaterial',inset_box((x-.04,y-.04,0),(x+.04,y+.04,.12)),[n],'Entire finite foot material from ground sole through full top seat, 1 mm boundary inset.')
G[COUNTER]=grid([-.62,.11,.53,.62],[-.27,-.16,.16,.225],[.76,.805],lambda x,y,z:not(.11<x<.53 and -.16<y<.16),1,'One continuous full-thickness countertop with a genuine basin aperture and finite support on both outer panels and central partition.')
contact('Counter_WholeCabinetTopSupports',BODY,COUNTER,(0,0,1),(-.58,0,.76),.067899,points=[(-.58,0,.76),(0,0,.76),(.58,0,.76)])
contact('Counter_WholeRearUpstandFace',COUNTER,BODY,(0,1,0),(0,.225,.78),.053999)
solid('Counter_CompletePiercedMaterial',grid([-.619,.109,.531,.619],[-.269,-.161,.161,.224],[.761,.804],lambda x,y,z:not(.109<x<.531 and -.161<y<.161)),[COUNTER],'Entire counter material around its one expanded hole, including all four broad strips and corners; 1 mm inset.')
isolated('Counter_WholeBasinAperture',box((.111,-.159,.759),(.529,.159,.806)),[COUNTER],'Whole finite true countertop cutout through the 45 mm top, independently of the inserted basin.')
# Independent bowl: complete floor/walls with a thicker continuous flange.
G[BASIN]=grid([.085,.117,.14,.50,.523,.555],[-.185,-.153,-.13,.13,.153,.185],[.60,.625,.805,.83],lambda x,y,z:((.117<x<.523 and -.153<y<.153) and (z<.625 or x<.14 or x>.50 or abs(y)>.13)) or (z>.805 and not(.14<x<.50 and abs(y)<.13)),1,'Independent true 205 mm-deep open basin with 25 mm floor, 23 mm walls and integral thick continuous rim resting on the counter; no pipe or drain promise.')
contact('Basin_WholeRimCounterSeat',COUNTER,BASIN,(0,0,1),(.10,0,.805),.039499,points=[(.10,0,.805),(.54,0,.805),(.32,-.175,.805),(.32,.175,.805)])
for label,lo,hi in [('Floor',(.117,-.153,.60),(.523,.153,.625)),('Left',(.117,-.153,.60),(.14,.153,.83)),('Right',(.50,-.153,.60),(.523,.153,.83)),('Front',(.117,-.153,.60),(.523,-.13,.83)),('Back',(.117,.13,.60),(.523,.153,.83))]:solid('Basin_WholeMaterial_'+label,inset_box(lo,hi),[BASIN],'Complete finite basin '+label+' slab including continuous floor/wall/rim root, 1 mm boundary inset.')
solid('Basin_WholeRimMaterial',grid([.086,.139,.501,.554],[-.184,-.131,.131,.184],[.806,.829],lambda x,y,z:not(.139<x<.501 and abs(y)<.131)),[BASIN],'Complete thick basin rim domain around all four sides and corners, expanded inner hole and 1 mm outer inset.')
air('Basin_EntireCavityAndMouth',box((.141,-.129,.626),(.499,.129,.85)),'Whole basin inner air from just above the actual floor through and above the entire rim mouth, 1 mm lateral clearance.')
for label,lo,hi in [('Left',(.111,-.152,.761),(.116,.152,.804)),('Right',(.524,-.152,.761),(.529,.152,.804)),('Front',(.111,-.159,.761),(.529,-.154,.804)),('Back',(.111,.154,.761),(.529,.159,.804))]:air('Basin_WholeCounterClearance_'+label,box(lo,hi),'Complete nonbearing basin/counter aperture wall corridor; full 45 mm counter thickness with 1 mm boundary inset.')
# Separate shelves bear on the complete top patches of integral cabinet ledges.
for n,x0,x1,z,seat0,seat1 in [(OVEN_SHELF,-.55,-.05,.39,-.535,-.065),(STORAGE_SHELF,.05,.55,.38,.065,.535)]:
 G[n]=box((x0,-.215,z),(x1,.21,z+.025),3,'Whole thick shelf supported by two complete finite cabinet ledge patches; all other boundaries positively separated.')
 contact(n+'_BothCompleteLedgeSeats',BODY,n,(0,0,1),(seat0,0,z),.025499,points=[(seat0,0,z),(seat1,0,z)])
 solid(n+'_WholeMaterial',inset_box((x0,-.215,z),(x1,.21,z+.025)),[n],'Entire 25 mm shelf solid including both finite bearing strips, 1 mm boundary inset.')
# Oven and storage free space partitioned around their actual supported shelf.
for name,lo,hi in [('OvenLowerFullChamber',(-.564,-.259,.161),(-.036,.224,.364)),('OvenUpperFullChamber',(-.564,-.259,.416),(-.036,.224,.759)),('OvenLedgeHeightCentralAir',(-.519,-.259,.364),(-.081,.224,.389)),('StorageLowerFullBay',(.036,-.259,.161),(.564,.224,.354)),('StorageAboveShelfBelowBasin',(.036,-.259,.406),(.564,.224,.599)),('StorageLedgeHeightCentralAir',(.081,-.259,.354),(.519,.224,.379))]:air(name,box(lo,hi),'Complete finite '+name+' domain, including the full front-to-rear opening, bounded by real walls/shelf/ledge/basin. 1 mm inset at actual surfaces.')
# Supplement narrow full-surface corridors beside shelves and under basin.
for n,x0,x1,z in [(OVEN_SHELF,-.55,-.05,.39),(STORAGE_SHELF,.05,.55,.38)]:
 for label,lo,hi in [('Front',(x0-.014,-.259,z+.001),(x1+.014,-.216,z+.024)),('Back',(x0-.014,.211,z+.001),(x1+.014,.224,z+.024)),('Left',(x0-.014,-.214,z+.001),(x0-.001,.209,z+.024)),('Right',(x1+.001,-.214,z+.001),(x1+.014,.209,z+.024))]:air(n+'_FullNonbearingAir_'+label,box(lo,hi),'Entire finite nonbearing '+label+' shelf-side corridor with 1 mm boundary inset; intended lower ledge seats excluded.')
air('Storage_CompleteBasinOuterAir',grid([.036,.116,.524,.564],[-.259,-.154,.154,.224],[.60,.759],lambda x,y,z:not(.116<x<.524 and abs(y)<.154)),'Entire connected finite storage air around the dropped basin on all four sides from its floor to just below the counter; every outer cup surface is covered, 1 mm inset.')
# A single connected finite whole-oven air body additionally covers all the
# side/front/back corridors around both ledges and the shelf, at every height.
ob=[((-.566,-.221,.364),(-.519,.216,.391)),((-.081,-.221,.364),(-.034,.216,.391)),((-.551,-.216,.389),(-.049,.211,.416))]
ox=sorted(set([-.564,-.036]+[max(-.564,min(-.036,p[0])) for q in ob for p in q]));oy=sorted(set([-.259,.224]+[p[1] for q in ob for p in q]));oz=sorted(set([.161,.759]+[p[2] for q in ob for p in q]))
air('Oven_EntireConnectedAirAroundShelf',grid(ox,oy,oz,lambda x,y,z:not in_boxes(x,y,z,ob)),'Complete connected finite oven void from its whole front opening to the back wall, floor to counter and side to partition, subtracting only the actual shelf and ledges with explicit 1 mm boundary insets. Includes every corridor around the shelf and support ledges.')
sbair=[((.034,-.221,.354),(.081,.216,.381)),((.519,-.221,.354),(.566,.216,.381)),((.049,-.216,.379),(.551,.211,.406)),((.116,-.154,.599),(.524,.154,.760))]
sx=sorted(set([.036,.564]+[max(.036,min(.564,p[0])) for q in sbair for p in q]));sy=sorted(set([-.259,.224]+[p[1] for q in sbair for p in q]));sz=sorted(set([.161,.759]+[max(.161,min(.759,p[2])) for q in sbair for p in q]))
air('Storage_EntireConnectedAirAroundShelfAndBasin',grid(sx,sy,sz,lambda x,y,z:not in_boxes(x,y,z,sbair)),'Complete connected finite storage void from the full front opening to the back, floor to counter and side to partition, subtracting only shelf, ledges and dropped basin with explicit 1 mm boundary insets.')
# Original thick fixed side-open door, rotated 90 degrees into an axis-aligned
# plane. Two integral pierced ears and the window belong to one closed solid.
DB=[((-.64,-.84,.18),(-.61,-.34,.27)),((-.64,-.84,.60),(-.61,-.34,.71)),((-.64,-.84,.27),(-.61,-.77,.60)),((-.64,-.40,.27),(-.61,-.34,.60))]
for z in [.235,.585]:DB.append(((-.64,-.34,z),(-.60,-.29,z+.035)))
dx=sorted(set([-.628,-.612]+[p[0] for q in DB for p in q]));dy=sorted(set([-.328,-.312]+[p[1] for q in DB for p in q]));dz=sorted(set(p[2] for q in DB for p in q))
def door_bore(x,y,z,e=0):return -.628-e<x<-.612+e and -.328-e<y<-.312+e and any(a-e<z<a+.035+e for a in [.235,.585])
G[DOOR]=grid(dx,dy,dz,lambda x,y,z:in_boxes(x,y,z,DB) and not door_bore(x,y,z),2,'One thick 90-degree open door boundary with actual through-window and two integral fully bored ears; no transparent glass or dark window plane.')
for i,(lo,hi) in enumerate(DB[:4],1):solid('Door_FullFrameMaterial_'+str(i),inset_box(lo,hi),[DOOR],'Entire finite door rail or stile; complete thick frame and window edge material.')
for j,z in enumerate([.235,.585],1):
 solid('DoorEar_'+str(j)+'_WholeRingAndRoot',grid([-.639,-.629,-.611,-.601],[-.339,-.329,-.311,-.291],[z+.001,z+.034],lambda x,y,z:not(-.629<x<-.611 and -.329<y<-.311)),[DOOR],'Whole integral pierced door ear material and ring, with complete finite root at the rear door stile.')
 isolated('DoorEar_'+str(j)+'_WholeBore',box((-.627,-.327,z-.001),(-.613,-.313,z+.036)),[DOOR],'Whole isolated ear bore through and beyond both full ear faces.')
 contact('DoorEar_'+str(j)+'_WholeUnderseat',BODY,DOOR,(0,0,1),(-.635,-.305,z),.001743)
 pin='ContinuousHeadedHingePin_'+str(j);PINS.append(pin)
 pb=[((-.626,-.326,z-.042),(-.614,-.314,z+.035)),((-.638,-.338,z+.035),(-.602,-.302,z+.05))]
 G[pin]=union_boxes(pb,4,'One continuous 12 mm square fixed pin and thick head; full shaft crosses both aligned 16 mm ear bores with finite wall clearance.')
 contact(pin+'_WholeHeadSeat',DOOR,pin,(0,0,1),(-.634,-.32,z+.035),.001039)
 for k,(lo,hi) in enumerate(pb):solid(pin+'_CompleteMaterial_'+str(k),inset_box(lo,hi),[pin],'Complete fixed pin shaft or head material, including the whole continuous root, 1 mm inset.')
 for label,lo,hi in [('Left',(-.627,-.327,z-.034),(-.6265,-.313,z+.034)),('Right',(-.6135,-.327,z-.034),(-.613,-.313,z+.034)),('Front',(-.6255,-.327,z-.034),(-.6145,-.3265,z+.034)),('Back',(-.6255,-.3135,z-.034),(-.6145,-.313,z+.034))]:air(pin+'_WholeNonbearingAir_'+label,box(lo,hi),'Full finite nonbearing '+label+' ear/pin gap over both complete ears; 0.5 mm corridor with >=0.5 mm actual wall/shaft clearances, ending 1 mm short of head seat.')
for j,z in enumerate([.30,.65],1):contact('FixedDoorStop_'+str(j)+'_CompleteFace',DOOR,BODY,(0,1,0),(-.625,-.34,z+.0175),.001049)
air('Door_EntireThroughWindow',box((-.655,-.769,.271),(-.595,-.401,.599)),'Entire finite actual window air through the full 30 mm door and beyond both faces; 1 mm window-edge inset.')
# Real noncontact corridor between the door/ear assembly and the cabinet front.
air('Door_WholeNonbearingCabinetFrontGap',box((-.599,-.339,.18),(-.566,-.261,.71)),'Whole vertical door/body corridor outside integrated ear/stop root intervals, split separately below.',targets=[])
# Remove the unsplit provisional volume; ear/stop contacts are not claimed clear.
del VOID_VOLUMES['Door_WholeNonbearingCabinetFrontGap']
for label,z0,z1 in [('Bottom',.181,.192),('Low',.286,.299),('Middle',.336,.542),('Upper',.636,.649),('Top',.686,.709)]:air('DoorBodyFullFreeCorridor_'+label,box((-.639,-.339,z0),(-.566,-.261,z1)),'Entire finite noncontact door/body front corridor in this uninterrupted vertical interval; genuine integral ear and stop bands excluded.')
HANDLE='ContinuousOpenDoorHandle';hb=[((-.68,-.77,.64),(-.64,-.74,.665)),((-.68,-.46,.64),(-.64,-.43,.665)),((-.705,-.77,.64),(-.68,-.43,.665))]
G[HANDLE]=union_boxes(hb,4,'One original continuous short thick horizontal door handle with two full finite roots and a true opening.')
contact('Handle_BothCompleteDoorRoots',HANDLE,DOOR,(1,0,0),(-.64,-.755,.6525),.001499,points=[(-.64,-.755,.6525),(-.64,-.445,.6525)])
air('Handle_WholeOpening',box((-.679,-.739,.641),(-.641,-.461,.664)),'Whole finite open handle void between roots, bridge and actual door face.')
for j,(lo,hi) in enumerate(hb):solid('Handle_CompleteMaterial_'+str(j),inset_box(lo,hi),[HANDLE],'Complete handle root or bridge material, 1 mm boundary inset.')
def ring(cx,cy,ro,ri,z0,z1,n=16,material=2):
 vv=[(cx+r*math.cos(i*math.tau/n),cy+r*math.sin(i*math.tau/n),z) for z,r in [(z0,ro),(z0,ri),(z1,ro),(z1,ri)] for i in range(n)];ff=[]
 for i in range(n):
  j=(i+1)%n;ff.extend([(i,j,j+2*n,i+2*n),(i+n,i+3*n,j+3*n,j+n),(i,i+n,j+n,j),(i+2*n,j+2*n,j+3*n,i+3*n)])
 return mesh(vv,ff,material,'Full closed annular countertop marking; fixed visual geometry only, no heating function.')
for i,cx in enumerate([-.43,-.17],1):
 n='FixedAnnularCounterMark_'+str(i);G[n]=ring(cx,.015,.095,.066,.805,.823)
 area=16*math.sin(math.tau/16)/2*(.095**2-.066**2);contact(n+'_WholeAnnularSeat',COUNTER,n,(0,0,1),(cx+.08,.015,.805),area-.000001)
 solid(n+'_CompleteRingMaterial',ring(cx,.015,.093,.068,.806,.822),[n],'Complete inset annular material over all facets and full height.')
 # Ring interior ends at the actual countertop; no false through-counter claim.
 air(n+'_WholeInnerAir',prism([(cx+.064*math.cos(k*math.tau/16),.015+.064*math.sin(k*math.tau/16)) for k in range(16)],.806,.825),'Complete finite polygonal ring interior above the real solid counter, not a through hole.')
SPOUT='SolidBlindDecorativeSpout';sb=[((.42,.195,.805),(.46,.225,.97)),((.42,.075,.94),(.46,.195,.97))]
G[SPOUT]=union_boxes(sb,4,'Original short continuous L spout with a fully solid blind end. Static appearance; no flow path or water outlet function.')
contact('Spout_CompleteCounterBase',COUNTER,SPOUT,(0,0,1),(.44,.21,.805),.001199)
contact('Spout_CompleteRearUpstandFace',SPOUT,BODY,(0,1,0),(.44,.225,.87),.005399)
for i,(lo,hi) in enumerate(sb):solid('Spout_EntireMaterial_'+str(i),inset_box(lo,hi),[SPOUT],'Complete solid spout stem or blind-ended arm, 1 mm boundary inset.')
air('Spout_EntireBelowArmClearance',box((.421,.076,.831),(.459,.194,.939)),'Complete finite air below the short blind spout and above the basin rim, 1 mm boundary inset.')
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['x']-=SHIFT[0];r['y']-=SHIFT[1]
CONTRACT={'single_prop_count':1,'continuous_shared_cabinet':1,'flat_ground_feet':4,'true_empty_oven':1,'finite_oven_shelf':1,'open_storage_shelf':1,'independent_true_basin':1,'fixed_thick_window_door':1,'full_thickness_ear_bores':4,'complete_headed_pins':2,'integral_fixed_stops':2,'fixed_annular_counter_marks':2,'blind_solid_decorative_spout':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'child_safety_or_function_claim':False}
def measure_play_kitchen_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-.94)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; complete finite air/material domains, contacts, self-intersection, all-pair separation and real negative gates required')
INSIDE_TESTS=[(BODY,sub((-.58,0,.50),SHIFT),sub((-.30,0,.50),SHIFT)),(BASIN,sub((.32,0,.61),SHIFT),sub((.32,0,.70),SHIFT)),(DOOR,sub((-.625,-.80,.40),SHIFT),sub((-.625,-.55,.40),SHIFT))]
FOCUS=(0,0,.48);ORTHO=1.90
CAMERAS={'gray-front3q':(-3,-5,2.7),'gray-back3q':(3,5,2.7),'thumbnail':(-3,-5,2.7),'qa-front':(0,-6,1.65),'qa-side':(-6,0,1.65),'qa-top':(0,0,6),'qa-back':(0,6,1.65),'qa-wireframe':(-3,-5,2.7),'silhouette-128-front':(0,-6,1.65),'silhouette-128-side':(-6,0,1.65)}
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
root=bpy.data.objects.new('OneOpenOvenPlayKitchen',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_play_kitchen_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'play_kitchen_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/toys/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
