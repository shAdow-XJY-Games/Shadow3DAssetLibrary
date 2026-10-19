"""Original freestanding four-face fixed glass vitrine, one static empty prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='museum-four-face-fixed-glass-vitrine-01';VERSION='1.0.0';TITLE='Four-face Fixed Glass Vitrine'
DESCRIPTION=('One original freestanding square empty museum vitrine: a complete stepped ground plinth and bearing floor, four continuous grooved corner posts between complete lower and upper rings, three vertical thick glass panes, a full-height fixed closed grooved glass-frame door, a thick glass lid and one thick glass shelf on four actual finite corner brackets. Two entire display chambers remain empty. Two original bored fixed hinge pairs with continuous headed pins and a finite closing stop connect the closed door; no moving state is claimed. All geometry is newly authored, never imported from an old hood, plinth or opaque cabinet. One static prop in metres, native Z up, front -Y, horizontal bounds centred at its complete ground datum Z=0. Constant PBR materials only; one physical transmission glass, alpha 1, no TEX nodes or linked Principled inputs. No exhibits, labels, lights, text, brands, scene or animation. No opening/insertion/manufacturing behavior, optical accuracy, load, glass safety, stability, security, dust/climate control, museum standard or compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BASE='CompleteSteppedGroundPlinth';BODY=BASE;LOWER='CompleteLowerBearingRing';UPPER='CompleteUpperLidRing';DOOR='ContinuousGroovedFixedDoorFrame';SHELF='ThickGlassDisplayShelf';LID='ThickGlassTopLid';STOP='FullHeightFiniteClosingStop'
POSTS=[];GLASS=[];BRACKETS=[];HINGES=[];PINS=[]
PALETTE=[('DeepBronzeFrame',(.115,.100,.075,1),.33,.62),('PaleStonePlinth',(.32,.30,.25,1),.67,.05),('SatinBrassFixedHardware',(.37,.27,.11,1),.35,.72),('TrueClearThickGlass',(.94,.985,.98,1),.035,0.)]
GLASS_INDEX=3;GLASS_TRANSMISSION=1.;GLASS_IOR=1.45
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

def add_solid(name,lo,hi,material,role):
 G[name]=box(lo,hi,material,role);solid(name+'_WholeMaterial',inset_box(lo,hi,.0006),[name],'Whole finite material with 0.6 mm boundary inset. '+role)
def ring(name,z0,z1,material=0,e=0):
 return grid([-.403+e,-.327-e,.327+e,.403-e],[-.33+e,-.255-e,.255+e,.33-e],[z0+e,z1-e],lambda x,y,z:abs(x)>.327+e or abs(y)>.255+e,material,'Complete continuous rectangular ring, not four crossing bars.')
# The plinth is one connected original stepped ground solid, not an old exhibit pedestal.
base_boxes=[((-.45,-.38,0),(.45,.38,.055)),((-.418,-.348,.055),(.418,.348,.135)),((-.45,-.38,.135),(.45,.38,.17))]
G[BASE]=union_boxes(base_boxes,1,'One complete low stepped plinth with whole ground sole, recessed waist and broad integral bearing floor.');FEET.append(BASE)
for i,(lo,hi) in enumerate(base_boxes):solid(BASE+'_EntireStep_'+str(i),inset_box(lo,hi),[BASE],'Complete finite lower, waist or top slab; 1 mm boundary inset.')
FOOT_CONTACTS.append({'mesh':BASE,'name':'WholePlinthGroundSole','x':0,'y':0,'half_x':.45,'half_y':.38,'minimum_area_m2':.683999})
# Two tiny integral bottom pads support the closed door above its perimeter gap.
lower_boxes=[((-.403,-.33,.17),(.403,-.255,.22)),((-.403,.255,.17),(.403,.33,.22)),((-.403,-.255,.17),(-.327,.255,.22)),((.327,-.255,.17),(.403,.255,.22))]
for x in [-.305,.305]:lower_boxes.append(((x-.014,-.33,.22),(x+.014,-.302,.224)))
G[LOWER]=union_boxes(lower_boxes,0,'Continuous lower ring with two integral full rectangular closed-door underseats.');G[UPPER]=ring(UPPER,1.74,1.79)
solid(LOWER+'_WholeRingMaterial',ring(LOWER,.17,.22,e=.001),[LOWER],'Entire connected lower ring material, outer and inner boundaries inset 1 mm.')
solid(UPPER+'_WholeRingMaterial',ring(UPPER,1.74,1.79,e=.001),[UPPER],'Entire connected upper ring material, outer and inner boundaries inset 1 mm.')
for i,(lo,hi) in enumerate(lower_boxes[4:]):solid(LOWER+'_WholeDoorPad_'+str(i),inset_box(lo,hi,.0006),[LOWER],'Whole integral finite door bottom pad.')
contact('WholeLowerRingOnFloor',BASE,LOWER,(0,0,1),(0,-.29,.17),.198419)
# Whole-height channels in the four narrow posts have a real end-stop and
# one-millimetre lateral air. No glass/metal interiors interpenetrate.
def post(side,rear,e=0):
 xa,xb=(.327+e,.403-e) if side>0 else (-.403+e,-.327-e)
 ya,yb=(.255+e,.33-e) if rear else (-.33+e,-.255-e)
 sx=sorted([side*.345-e,side*.355+e]) if side>0 else [-.355-e,-.345+e]
 # Explicit symmetric global slot bounds avoid handedness ambiguity.
 sx=[.345-e,.355+e] if side>0 else [-.355-e,-.345+e]
 sy=[.255,.27+e] if rear else [-.27-e,-.255]
 holes=[((sx[0],sy[0]),(sx[1],sy[1]))]
 if rear:
  hx=(.327,.355+e) if side>0 else (-.355-e,-.327)
  holes.append(((hx[0],.285-e),(hx[1],.295+e)))
 xs=sorted(set([xa,xb]+[max(xa,min(xb,p[0])) for h in holes for p in h]));ys=sorted(set([ya,yb]+[max(ya,min(yb,p[1])) for h in holes for p in h]))
 return grid(xs,ys,[.22+e,1.74-e],lambda x,y,z:not any(lo[0]<x<hi[0] and lo[1]<y<hi[1] for lo,hi in holes),0,'One full-height corner post with actual finite glazing stop channels; complete material remains around each channel.')
for side,label in [(-1,'Left'),(1,'Right')]:
 for rear,loc in [(False,'Front'),(True,'Rear')]:
  n=label+loc+'ContinuousGroovedPost';POSTS.append(n);G[n]=post(side,rear);solid(n+'_WholeChannelPostMaterial',post(side,rear,.0006),[n],'Entire connected grooved post material, 0.6 mm inward outer and outward channel boundary offsets.')
  contact(n+'_LowerEnd',LOWER,n,(0,0,1),(side*.38,.315 if rear else -.315,.22),.004)
  contact(n+'_UpperEnd',n,UPPER,(0,0,1),(side*.38,.315 if rear else -.315,1.74),.004)
 # Side glass ends at the actual channel end-stop; its lateral edges remain visible.
 n=label+'FullThickSideGlass';GLASS.append(n);cx=side*.35
 add_solid(n,(cx-.004,-.27,.22),(cx+.004,.27,1.74),3,'One closed 8 mm thick vertical side pane with all six faces and positive volume.')
 contact(n+'_BottomFullEdge',LOWER,n,(0,0,1),(cx,0,.22),.004319)
 contact(n+'_TopFullEdge',n,UPPER,(0,0,1),(cx,0,1.74),.004319)
 contact(n+'_FrontFullEdge',label+'FrontContinuousGroovedPost',n,(0,1,0),(cx,-.27,.6),.012159)
 contact(n+'_RearFullEdge',n,label+'RearContinuousGroovedPost',(0,1,0),(cx,.27,.6),.012159)
 for end,(ya,yb) in enumerate([(-.2694,-.2556),(.2556,.2694)]):
  for dx,lo,hi in [('Inside',cx-.00465,cx-.00435),('Outside',cx+.00435,cx+.00465)]:air(n+'_CompleteSlotAir_'+str(end)+dx,box((lo,ya,.2206),(hi,yb,1.7394)),'Full finite lateral slot-wall air, 0.35 mm from actual glass and metal walls. No positive clearance claimed at intended end/bottom/top bearing edges.')
n='RearFullThickGlass';GLASS.append(n);add_solid(n,(-.355,.286,.22),(.355,.294,1.74),3,'One complete closed 8 mm thick vertical rear pane.')
contact(n+'_BottomFullEdge',LOWER,n,(0,0,1),(0,.29,.22),.005679);contact(n+'_TopFullEdge',n,UPPER,(0,0,1),(0,.29,1.74),.005679)
contact(n+'_LeftFullEdge','LeftRearContinuousGroovedPost',n,(1,0,0),(-.355,.29,.6),.012159);contact(n+'_RightFullEdge',n,'RightRearContinuousGroovedPost',(1,0,0),(.355,.29,.6),.012159)
for side,label in [(-1,'Left'),(1,'Right')]:
 xa,xb=(.3276,.3544) if side>0 else (-.3544,-.3276)
 for loc,ya,yb in [('Front',.28535,.28565),('Back',.29435,.29465)]:air(n+'_'+label+'SlotAir'+loc,box((xa,ya,.2206),(xb,yb,1.7394)),'Whole finite rear-glass lateral channel air; intended edge seat excluded.')
# A new full-height continuous frame with a recessed true glass groove.
def door(e=0):
 xs=[-.325+e,-.295-e,-.285-e,.285+e,.295+e,.325-e];ys=[-.33+e,-.315-e,-.305+e,-.302-e];zs=[.224+e,.256-e,.266-e,1.694+e,1.704+e,1.736-e]
 return grid(xs,ys,zs,lambda x,y,z:(abs(x)>.285+e or z<.266-e or z>1.694+e) and not(abs(x)<.295+e and .256-e<z<1.704+e and -.315-e<y<-.305+e),0,'One continuous full-height grooved fixed door frame, with real upper/lower/stile frame material around one complete glass pane.')
G[DOOR]=door();solid(DOOR+'_WholeGroovedFrameMaterial',door(.0006),[DOOR],'Complete connected inset door-frame material around the whole glass groove.')
for x in [0]:contact(DOOR+'_BothWholeBottomPads',LOWER,DOOR,(0,0,1),(-.305,-.32,.224),.001567,points=[(-.305,-.32,.224),(.305,-.32,.224)])
n='FrontDoorFullThickGlass';GLASS.append(n);add_solid(n,(-.295,-.314,.256),(.295,-.306,1.704),3,'One closed 8 mm thick full-height fixed door pane, four real edge seats and full front/back surfaces.')
contact(n+'_BottomFullEdge',DOOR,n,(0,0,1),(0,-.31,.256),.004719);contact(n+'_TopFullEdge',n,DOOR,(0,0,1),(0,-.31,1.704),.004719)
contact(n+'_LeftFullEdge',DOOR,n,(1,0,0),(-.295,-.31,1.),.011583);contact(n+'_RightFullEdge',n,DOOR,(1,0,0),(.295,-.31,1.),.011583)
for face,ya,yb in [('Front',-.31465,-.31435),('Rear',-.30565,-.30535)]:
 for side,xa,xb in [('Left',-.2944,-.2856),('Right',.2856,.2944)]:air(n+'_WholeGrooveAir_'+face+side,box((xa,ya,.2566),(xb,yb,1.7034)),'Complete finite door side-groove air over full pane edge length, excluding intended edge seat boundaries.')
 for end,za,zb in [('Lower',.2566,.2654),('Upper',1.6946,1.7034)]:air(n+'_WholeGrooveAir_'+face+end,box((-.2844,ya,za),(.2844,yb,zb)),'Complete finite door horizontal-groove air excluding intended glass end seat.')
add_solid(STOP,(.312,-.302,.24),(.327,-.282,1.72),2,'One long finite stop attached to the front right post and touching the fixed closed door back face.')
contact('ClosingStopToRightPost',STOP,'RightFrontContinuousGroovedPost',(1,0,0),(.327,-.29,.7),.029599)
contact('ClosedDoorToWholeStop',DOOR,STOP,(0,1,0),(.319,-.302,.7),.019239)
# One complete thick lid, with a finite full perimeter ring bearing.
GLASS.append(LID);add_solid(LID,(-.37,-.30,1.79),(.37,.30,1.798),3,'One closed 8 mm thick glass top lid, borne by the whole upper ring.')
contact('LidToWholeUpperRing',UPPER,LID,(0,0,1),(0,.28,1.79),.110459)
# The one thick shelf is borne by four finite corner brackets; both chambers are empty.
for side,label in [(-1,'Left'),(1,'Right')]:
 for rear,loc,ya,yb in [(False,'Front',-.279,-.23),(True,'Rear',.23,.279)]:
  n=label+loc+'FiniteShelfBracket';BRACKETS.append(n);xa,xb=(.305,.327) if side>0 else (-.327,-.305);add_solid(n,(xa,ya,.95),(xb,yb,.97),2,'One whole finite shelf bearing bracket rooted by its complete lateral patch into an actual corner post.')
  p=label+loc+'ContinuousGroovedPost'
  if side>0:contact(n+'_WholePostRoot',n,p,(1,0,0),(.327,.265 if rear else -.265,.96),.000479)
  else:contact(n+'_WholePostRoot',p,n,(1,0,0),(-.327,.265 if rear else -.265,.96),.000479)
  contact(n+'_WholeShelfBearing',n,SHELF,(0,0,1),(side*.314,.25 if rear else -.238,.97),.000781 if rear else .000271)
GLASS.append(SHELF);add_solid(SHELF,(-.322,-.246,.97),(.322,.276,.978),3,'One closed 8 mm thick glass shelf, with four finite underside bracket contacts; no hidden support or filler.')
# Two simple original square-bored fixed hinge pairs. These are closed-pose
# geometric supports, not a motion mechanism or an assembly claim.
for i,z in enumerate([.45,1.49],1):
 fixed=f'FixedHinge{i}_PostLeafAndBoredKnuckle';moving=f'FixedHinge{i}_DoorLeafAndBoredKnuckle';pin=f'FixedHinge{i}_ContinuousHeadedPin';HINGES.extend([fixed,moving]);PINS.append({'mesh':pin,'fixed':fixed,'door_leaf':moving,'z':z})
 def leaf(isdoor,e=0):
  za,zb=(z-.004,z+.028) if isdoor else (z-.04,z-.008)
  boxes=[((-.319 if isdoor else -.38,-.36,za),(-.272 if isdoor else -.333,-.33,zb)),((-.339,-.38,za),(-.313,-.354,zb))]
  xx=sorted(set([p[0] for b in boxes for p in b]+[-.331-e,-.321+e]));yy=sorted(set([p[1] for b in boxes for p in b]+[-.372-e,-.362+e]));zz=[za+e,zb-e]
  if e:
   # Erode the complete union by all six directions, retaining connected root and knuckle.
   def inside0(x,y):return any(lo[0]<x<hi[0] and lo[1]<y<hi[1] for lo,hi in boxes)
   xx=sorted(set([v+d for v in xx for d in [-e,0,e]]));yy=sorted(set([v+d for v in yy for d in [-e,0,e]]))
   occ=lambda x,y,z:all(inside0(x+dx,y+dy) for dx,dy in [(e,0),(-e,0),(0,e),(0,-e),(e,e),(e,-e),(-e,e),(-e,-e)]) and not(-.331-e<x<-.321+e and -.372-e<y<-.362+e)
  else:occ=lambda x,y,z:any(lo[0]<x<hi[0] and lo[1]<y<hi[1] for lo,hi in boxes) and not(-.331<x<-.321 and -.372<y<-.362)
  return grid(xx,yy,zz,occ,2,'One connected thick fixed hinge leaf with integral true square-bored knuckle.')
 G[fixed]=leaf(False);G[moving]=leaf(True)
 for n,isdoor in [(fixed,False),(moving,True)]:solid(n+'_WholeBoredLeafMaterial',leaf(isdoor,.0006),[n],'Complete connected inset material around the real knuckle bore and through its leaf root.')
 contact(fixed+'_WholePostRoot',fixed,'LeftFrontContinuousGroovedPost',(0,1,0),(-.36,-.33,z-.024),.001503)
 contact(moving+'_WholeDoorRoot',moving,DOOR,(0,1,0),(-.305,-.33,z+.012),.001087)
 pb=[((-.331,-.371,z-.042),(-.323,-.363,z+.028)),((-.335,-.376,z+.028),(-.317,-.358,z+.04))];G[pin]=union_boxes(pb,2,'One continuous fixed headed square pin with genuine bores, full left-wall bearing on both knuckles and full head underside seat.')
 for k,(lo,hi) in enumerate(pb):solid(pin+'_WholeMaterial_'+str(k),inset_box(lo,hi,.0006),[pin],'Whole pin shaft or integral head finite material.')
 for n,za,zb in [(fixed,z-.04,z-.008),(moving,z-.004,z+.028)]:
  contact(pin+'_WholeLeftBearing_'+n,n,pin,(1,0,0),(-.331,-.367,(za+zb)/2),.000255)
  isolated(n+'_CompleteBore',box((-.3304,-.3714,za-.0006),(-.3216,-.3626,zb+.0006)),[n],'Entire isolated real square knuckle bore, through both mouths, 0.6 mm wall inset.')
  for label,lo,hi in [('Right',(-.32265,-.3704,za+.0006),(-.32135,-.3636,zb-.0006)),('Front',(-.3304,-.37165,za+.0006),(-.3236,-.37135,zb-.0006)),('Back',(-.3304,-.36265,za+.0006),(-.3236,-.36235,zb-.0006))]:air(n+'_WholeNonbearingAir_'+label,box(lo,hi),'Whole nonbearing bore-wall air over the knuckle length; intended left bearing edge excluded.')
 contact(pin+'_WholeHeadUnderside',moving,pin,(0,0,1),(-.326,-.374,z+.028),.000223)
 air(f'FixedHinge{i}_WholeInterknuckleGap',box((-.3384,-.3794,z-.0074),(-.3136,-.3546,z-.0046)),'Complete finite interknuckle interval excluding the actual pin material.',targets=[fixed,moving])
# Whole bounded display air is assembled as stepped cross-sections so it reaches
# each real inside glass face and includes the clear glass edge corridors.
# Separate strip domains supplement the central volume around corner fittings.
for label,z0,z1 in [('Lower',.2206,.9494),('Upper',.9786,1.7394)]:
 air('Whole'+label+'DisplayChamber',box((-.3264,-.3014,z0),(.3114,.2854,z1)),'Entire central finite '+label.lower()+' empty display domain bounded 0.6 mm from actual inner floor/frame/door/back/shelf surfaces; full peripheral strips separately certified.')
 for side,xa,xb in [('Left',-.3454,-.3258),('Right',.3108,.3454)]:air(label+'WholeSideGlassCorridor'+side,box((xa,-.2544,z0),(xb,.2544,z1)),'Complete finite peripheral strip up to side glass inner face, excluding whole corner-post material.')
 air(label+'WholeRightDoorStopCorridor',box((.3126,-.2814,z0),(.3264,.2854,z1)),'Complete right-side air beyond the finite closing stop to the corner-frame boundary.')
air('LowerWholeFloorWell',box((-.3264,-.2544,.1706),(.3264,.2544,.2212)),'Entire inset open lower-ring floor well down to the real continuous plinth top, overlapping lower chamber union.')
air('UpperWholeLidWell',box((-.3264,-.2544,1.7388),(.3264,.2544,1.7894)),'Entire inset upper-ring well to the actual glass lid underside, overlapping upper chamber union.')
air('LowerWholeTopCentralRegion',box((-.3044,-.2454,.9488),(.3044,.2754,.9694)),'Complete central lower chamber interval above bracket undersides to actual shelf underside; overlapping full chamber and perimeter domains.')
# Entire shelf perimeter and chamber transition are certified independently.
air('WholeShelfFrontGap',box((-.3044,-.3014,.9506),(.3044,-.2466,.9794)),'Full finite shelf-to-door interval, excluding corner brackets and stop.')
air('WholeShelfRearGap',box((-.3044,.2766,.9506),(.3044,.2854,.9794)),'Whole finite shelf-to-rear-pane gap.')
for side,xa,xb in [('Left',-.3454,-.3276),('Right',.3276,.3454)]:air('WholeShelfSideGap'+side,box((xa,-.2294,.9506),(xb,.2294,.9794)),'Whole finite shelf-side glazing gap, actual corner bracket intervals separately excluded.')
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
# Freeze every declared support as the complete finite opposed source patch.
# This is numerical construction evidence, never inferred from a mutated export.
def patch_cross(a,b):return a[0]*b[1]-a[1]*b[0]
def patch_area(poly):return abs(sum(patch_cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0.
def patch_clip(subject,clip,eps=1e-12):
 if patch_cross(sub(clip[1],clip[0]),sub(clip[2],clip[0]))<0:clip=list(reversed(clip))
 poly=list(subject)
 for a,b in zip(clip,clip[1:]+clip[:1]):
  old=poly;poly=[]
  if not old:break
  for p,q in zip(old,old[1:]+old[:1]):
   dp=patch_cross(sub(b,a),sub(p,a));dq=patch_cross(sub(b,a),sub(q,a));ip=dp>=-eps;iq=dq>=-eps
   if ip!=iq:poly.append(add(p,mul(sub(q,p),dp/(dp-dq))))
   if iq:poly.append(q)
 return poly
def patch_triangles(name,r,sign):
 g=G[name];out=[]
 for face in g['faces']:
  for i in range(1,len(face)-1):
   tri=[g['vertices'][j] for j in [face[0],face[i],face[i+1]]]
   if max(abs(dot(sub(p,r['origin_m']),r['axis'])-r['plane_m']) for p in tri)>1e-8:continue
   if dot(cross(sub(tri[1],tri[0]),sub(tri[2],tri[0])),r['axis'])*sign<=0:continue
   out.append([(dot(sub(p,r['origin_m']),r['u']),dot(sub(p,r['origin_m']),r['v'])) for p in tri])
 return out
for r in CONTACTS:
 aa=patch_triangles(r['a'],r,1);bb=patch_triangles(r['b'],r,-1);polys=[]
 for a in aa:
  for b in bb:
   poly=patch_clip(a,b)
   if patch_area(poly)>1e-12:polys.append(poly)
 r['declared_patch_polygons_uv_m']=polys;r['declared_patch_area_m2']=sum(patch_area(p) for p in polys)
 assert r['declared_patch_area_m2']>=r['minimum_patch_area_m2'],r['name']

SHIFT=(0,0,0)
CONTRACT={'single_prop_count':1,'complete_ground_plinth':1,'full_height_grooved_posts':4,'whole_lower_upper_rings':2,'full_vertical_glass_panes':4,'full_height_grooved_fixed_door':1,'thick_glass_lid':1,'thick_glass_shelf':1,'finite_shelf_brackets':4,'fixed_bored_hinge_pairs':2,'continuous_headed_hinge_pins':2,'finite_closing_stop':1,'whole_empty_display_chambers':2,'glass_meshes':GLASS,'glass_thickness_m':{n:.008 for n in GLASS},'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'door_motion_or_load_or_safety_claim':False}
def measure_vitrine_geometry(vertices):
 assert set(vertices)==set(G)
 assert abs(min(p[2] for p in vertices[BASE]))<2e-7
 assert abs(max(p[2] for p in vertices[LID])-1.798)<2e-7
 for n in GLASS:
  lo=[min(p[k] for p in vertices[n]) for k in range(3)];hi=[max(p[k] for p in vertices[n]) for k in range(3)];assert abs(min(hi[k]-lo[k] for k in range(3))-CONTRACT['glass_thickness_m'][n])<2e-7
 return dict(CONTRACT,geometry_scope='Complete actual source/export coordinates; all finite empty/material domains, full opposed patches and all-pair nonpenetration remain required.')
INSIDE_TESTS=[(BASE,(0,0,.15),(0,0,.5)),(DOOR,(-.31,-.32,.5),(0,-.31,.5)),('RightFullThickSideGlass',(.35,0,.6),(.34,0,.6))]
FOCUS=(0,0,.90);ORTHO=2.40
CAMERAS={'gray-front3q':(3,-5,3.1),'gray-back3q':(-3,5,3.1),'thumbnail':(3,-5,3.1),'qa-front':(0,-6,2.2),'qa-side':(6,0,2.2),'qa-top':(0,0,6),'qa-back':(0,6,2.2),'qa-wireframe':(3,-5,3.1),'silhouette-128-front':(0,-6,2.2),'silhouette-128-side':(6,0,2.2)}
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
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;m.use_backface_culling=True
 if name=='TrueClearThickGlass':
  p.inputs['Transmission Weight'].default_value=GLASS_TRANSMISSION;p.inputs['IOR'].default_value=GLASS_IOR;p.inputs['Alpha'].default_value=1.
  group=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree');group.interface.new_socket(name='Occlusion',in_out='INPUT',socket_type='NodeSocketFloat');th=group.interface.new_socket(name='Thickness',in_out='INPUT',socket_type='NodeSocketFloat');th.default_value=.008;group.nodes.new('NodeGroupInput');group.nodes.new('NodeGroupOutput');settings=m.node_tree.nodes.new('ShaderNodeGroup');settings.node_tree=group;settings.inputs['Thickness'].default_value=.008
  assert not any(q.is_linked for q in settings.inputs)
 mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFourFaceFixedGlassVitrine',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred whole plinth ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_vitrine_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 settings=[n for n in m.node_tree.nodes if n.type=='GROUP' and n.node_tree and n.node_tree.name.startswith('glTF Material Output')]
 thickness=0.
 if settings:
  assert len(settings)==1 and not any(q.is_linked for q in settings[0].inputs);thickness=float(settings[0].inputs['Thickness'].default_value)
 values.append(('volume_thickness',round(thickness,6)))
 if float(p.inputs['Transmission Weight'].default_value)>0:
  assert abs(thickness-.008)<2e-7 and abs(float(p.inputs['IOR'].default_value)-1.45)<2e-7 and p.inputs['Alpha'].default_value==1.
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
# Candidate-specific actual exported material contract, independent of Blender node claims.
import struct
raw=(OUT/'model.glb').read_bytes();json_length,kind=struct.unpack_from('<II',raw,12);assert kind==0x4E4F534A
gltf=json.loads(raw[20:20+json_length]);assert not gltf.get('textures') and not gltf.get('images')
actual_glass_materials=[]
for me in gltf['meshes']:
 if me['name'] not in GLASS:continue
 for primitive in me['primitives']:
  material=gltf['materials'][primitive['material']];pbrj=material['pbrMetallicRoughness'];ext=material.get('extensions',{})
  def near(a,b):return abs(float(a)-float(b))<2e-7
  assert all(near(a,b) for a,b in zip(pbrj['baseColorFactor'],PALETTE[GLASS_INDEX][1]))
  assert near(pbrj.get('metallicFactor',1),0) and near(pbrj.get('roughnessFactor',1),.035)
  assert material.get('alphaMode','OPAQUE')=='OPAQUE' and not material.get('doubleSided',False)
  assert near(ext['KHR_materials_transmission']['transmissionFactor'],1) and near(ext['KHR_materials_ior']['ior'],1.45)
  vol=ext['KHR_materials_volume'];assert near(vol['thicknessFactor'],.008) and vol.get('attenuationColor',[1,1,1])==[1,1,1] and 'attenuationDistance' not in vol
  actual_glass_materials.append({'mesh':me['name'],'material':primitive['material'],'extensions':ext,'pbr':pbrj})
assert {r['mesh'] for r in actual_glass_materials}==set(GLASS)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'glass_material_actual_export':actual_glass_materials,'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'vitrine_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_transmission_volume_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/museum/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / transmission-volume PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_transmission_volume_pbr_match':True,'mesh_count':len(parts)};saveqa()
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
 assert records(parts)==source_records,'Diagnostic restoration changed complete geometry/transmission/volume PBR signature'
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
 if gray:
  for m in asset_mats:
   p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.50,.50,.50,1);p.inputs['Transmission Weight'].default_value=0.;p.inputs['Metallic'].default_value=0.;p.inputs['Roughness'].default_value=.65
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
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
