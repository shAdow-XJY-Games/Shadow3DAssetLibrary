"""Original empty two-tier V-cradle ball trolley. One complete fixed static prop."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-two-tier-cradle-ball-trolley-01';VERSION='1.0.0';TITLE='Two-Tier V-Cradle Ball Trolley'
DESCRIPTION=('One original empty two-tier ball-storage trolley, counted as one complete static prop. Each tier has two long thick inward-sloping cradle rails with a genuine full-length central opening, two finite V-profile end supports and two independent low end stops. Four continuous posts connect the two open tiers to a low open perimeter frame. One continuous raised U-shaped push handle is supported by two complete post-root faces. Four fixed wheel assemblies each contain an original twelve-sided thick wheel with a real through-bore, one continuous shouldered axle and one complete double-cheek U fork with true through-bores; every wheel has a complete finite flat ground facet. All intended joints are complete finite opposed faces, with positive noncontact gaps. No balls are included; original temporary faceted test balls are geometry evidence only and are not exported or separately counted. Metres, native Z up, front -Y, horizontally bounds-centred ground origin, five opaque unlinked constant PBR materials. Newly authored geometry: not a wheeled flat-shelf equipment rack, shortened delivery cage, cloth hamper or recolour. Fixed empty visual appearance only: no rolling, steering, brake, folding, usable ball fit, compatibility with existing balls, capacity, competition dimensions, human pushing fit, load, stability, anti-tip, pinch protection, material, manufacture, transport, installation, public-sports suitability or safety certification claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];RAILS=[];END_SUPPORTS=[];STOPS=[];POSTS=[];WHEEL_SETS=[];QA_BALLS={};QA_BALL_CONTACTS=[];NONCONTACT_SURFACES=[]
BODY='LowOpenPerimeterFrame';HANDLE='ContinuousSingleEndUHandle';SLOPE=.65;TIERS=[.43,.83];WHEEL_Z=.075*math.cos(math.pi/12)
PALETTE=[('DeepInkBlueFrame',(.045,.115,.155,1),.57,.12),('WarmOchreCradleRails',(.72,.31,.070,1),.62,.04),('PaleWarmEndStops',(.65,.65,.51,1),.65,.03),('DarkGraphiteWheels',(.038,.048,.050,1),.75,0),('DullAlloyAxles',(.34,.40,.40,1),.45,.58)]
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
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  if len(ids)==3:self.f.append(tuple(ids));self.fm.append(mat);self.tags.append(tag);return
  c=self.vertex(tuple(sum(p[k] for p in points)/len(points) for k in range(3)))
  for a,b in zip(ids,ids[1:]+ids[:1]):
   if a==b:continue
   self.f.append((a,b,c));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable surface'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected surface'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def rect(y0,y1,z0,z1):return [(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
def chamfer(y0,y1,z0,z1,c):return [(y0+c,z0),(y1-c,z0),(y1,z0+c),(y1,z1-c),(y1-c,z1),(y0+c,z1),(y0,z1-c),(y0,z0+c)]
def inside2(p,poly):
 y,z=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>z)!=(b[1]>z) and y<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def extrude_region(outer,holes,x0,x1,mat=0,role='closed finite prism'):
 # Exact horizontal decomposition of the polygon-with-holes. Every slab end
 # shares all boundary breakpoints; no T-junctions and no booleans or fake caps.
 outer=[tuple(round(c,9) for c in p) for p in outer];holes=[[tuple(round(c,9) for c in p) for p in h] for h in holes]
 loops=[outer]+holes;levels=sorted(set(round(p[1],9) for loop in loops for p in loop));m=Mesh()
 segs=[(a,b,k) for k,loop in enumerate(loops) for a,b in zip(loop,loop[1:]+loop[:1])]
 def hit(a,b,z):return a[0]+(b[0]-a[0])*(z-a[1])/(b[1]-a[1])
 cuts={}
 for z in levels:
  yy=[]
  for a,b,k in segs:
   if min(a[1],b[1])-1e-8<=z<=max(a[1],b[1])+1e-8:
    yy.extend([a[0],b[0]] if abs(a[1]-b[1])<1e-8 else [hit(a,b,z)])
  cuts[z]=sorted(set(round(y,9) for y in yy))
 for z0,z1 in zip(levels,levels[1:]):
  z=(z0+z1)/2;active=sorted([(hit(a,b,z),a,b) for a,b,k in segs if min(a[1],b[1])<z<max(a[1],b[1])],key=lambda r:r[0])
  for left,right in zip(active,active[1:]):
   p=((left[0]+right[0])/2,z)
   if not inside2(p,outer) or any(inside2(p,h) for h in holes):continue
   l0,l1=hit(left[1],left[2],z0),hit(left[1],left[2],z1);r0,r1=hit(right[1],right[2],z0),hit(right[1],right[2],z1)
   low=[(y,z0) for y in cuts[z0] if l0+1e-8<y<r0-1e-8];high=[(y,z1) for y in reversed(cuts[z1]) if l1+1e-8<y<r1-1e-8]
   poly=[(l0,z0)]+low+[(r0,z0),(r1,z1)]+high+[(l1,z1)];clean=[]
   for p in poly:
    if not clean or math.dist(clean[-1],p)>1e-8:clean.append(p)
   if math.dist(clean[0],clean[-1])<1e-8:clean.pop()
   for x in [x0,x1]:m.face([(x,*p) for p in clean],mat,'side_face')
 for a,b,k in segs:
  if abs(a[1]-b[1])<1e-8:
   z=round(a[1],9);ys=[a[0]]+[y for y in cuts[z] if min(a[0],b[0])+1e-8<y<max(a[0],b[0])-1e-8]+[b[0]];ys=sorted(ys);pp=[(y,z) for y in ys]
  else:
   zs=sorted([a[1]]+[z for z in levels if min(a[1],b[1])+1e-8<z<max(a[1],b[1])-1e-8]+[b[1]]);pp=[(hit(a,b,z),z) for z in zs]
  for p,q in zip(pp,pp[1:]):m.face([(x0,*p),(x1,*p),(x1,*q),(x0,*q)],mat,'outer_wall' if k==0 else 'hole_wall_'+str(k))
 return m.result(role,mat)
def box_geometry(lo,hi,mat=0,role='complete finite rectangular prism'):
 return extrude_region(rect(lo[1],hi[1],lo[2],hi[2]),[],lo[0],hi[0],mat,role)
def yz_prism(poly,x0,x1,mat=0,role=''):
 return prism(poly,x0,x1,mat,role,lambda p:(p[2],p[0],p[1]))
def railtop(y,z):return z+SLOPE*(abs(y)-.035)
# New low continuous perimeter with a whole open centre.
G[BODY]=grid([-.60,-.54,.54,.60],[-.31,-.25,.25,.31],[.22,.26],lambda x,y,z:abs(x)>.54 or abs(y)>.25,0,'One continuous thick low perimeter with completely open central underside; no flat deck.')
solid('CompleteLowFrameMaterial',grid([-.599,-.541,.541,.599],[-.309,-.251,.251,.309],[.221,.259],lambda x,y,z:abs(x)>.541 or abs(y)>.251),[BODY],'Complete connected finite inset perimeter material around the whole opening; 1 mm boundary inset.')
air('WholeLowFrameCentralOpening',box((-.539,-.249,.001),(.539,.249,.419)),'Whole low-frame central void from ground to below lower tier; finite complete volume and both frame mouths.')
for side,label in [(-1,'Left'),(1,'Right')]:
 x0,x1=sorted([side*.55,side*.59])
 for sign,frontback in [(-1,'Front'),(1,'Back')]:
  y0,y1=sorted([sign*.24,sign*.28]);n=f'FullPost_{label}_{frontback}';G[n]=box((x0,y0,.26),(x1,y1,1.04),0,'Continuous full-height post with complete finite base and two tier-support seats.');POSTS.append(n)
  contact(n+'_FrameSeat',BODY,n,(0,0,1),((x0+x1)/2,(y0+y1)/2,.26),.001599)
  solid(n+'_FullMaterial',box((x0+.001,y0+.001,.261),(x1-.001,y1-.001,1.039)),[n],'Complete full-height finite thick post core, 1 mm inset.')
for ti,z in enumerate(TIERS):
 tag=f'Tier_{ti+1}';tier=[]
 for sign,label in [(-1,'Front'),(1,'Back')]:
  y0,y1=sorted([sign*.035,sign*.24]);poly=[(y0,railtop(y0,z)-.028),(y1,railtop(y1,z)-.028),(y1,railtop(y1,z)),(y0,railtop(y0,z))]
  n=tag+'_'+label+'ContinuousInclinedRail';G[n]=yz_prism(poly,-.50,.50,1,'Original full-width inward-sloping 28 mm vertical-thick V cradle rail; complete finite end faces, no flat shelf.');RAILS.append(n);tier.append(n)
  a,b=y0+.001,y1-.001;sp=[(a,railtop(a,z)-.027),(b,railtop(b,z)-.027),(b,railtop(b,z)-.001),(a,railtop(a,z)-.001)]
  solid(n+'_FullMaterial',yz_prism(sp,-.499,.499),[n],'Whole finite thick long inclined rail material including both ends, 1 mm boundary inset.')
 for side,label in [(-1,'Left'),(1,'Right')]:
  x0,x1=sorted([side*.50,side*.55]);poly=[(-.28,z-.055),(.28,z-.055),(.28,railtop(.28,z)),(.035,z),(-.035,z),(-.28,railtop(-.28,z))]
  n=tag+'_'+label+'VProfileEndSupport';G[n]=yz_prism(poly,x0,x1,0,'One complete thick V-profile end support, with continuous valley web and two full post seats; closes only the short tier end.');END_SUPPORTS.append(n)
  for sign,frontback in [(-1,'Front'),(1,'Back')]:
   post='FullPost_'+label+'_'+frontback;p=(side*.55,sign*.26,z+.06);a,b=(post,n) if side<0 else (n,post);contact(n+'_'+frontback+'PostSeat',a,b,(1,0,0),p,.0076)
  for rail in tier:
   yy=-.13 if 'Front' in rail else .13;p=(side*.50,yy,railtop(yy,z)-.014);a,b=(n,rail) if side<0 else (rail,n);contact(rail+'_'+label+'FullEndSeat',a,b,(1,0,0),p,.005739)
  ppoly=[(-.279,z-.054),(.279,z-.054),(.279,railtop(.279,z)-.001),(.035,z-.001),(-.035,z-.001),(-.279,railtop(-.279,z)-.001)]
  solid(n+'_FullMaterial',yz_prism(ppoly,x0+.001,x1-.001),[n],'Whole V-profile finite end-support material, continuous lower web and inclined ends, 1 mm inset.')
  a,b=sorted([side*.55,side*.57]);stop=tag+'_'+label+'IndependentLowStop';G[stop]=box((a,-.23,z-.02),(b,.23,z+.18),2,'Independent low solid end stop with a broad finite inside root on the tier V end support; no tall cage.');STOPS.append(stop)
  aa,bb=(stop,n) if side<0 else (n,stop);contact(stop+'_FiniteRoot',aa,bb,(1,0,0),(side*.55,.15,z+.04),.029)
 # Whole tier air above both sloped faces, and the full open slot through their thickness.
 low=[(-.239,railtop(-.239,z)+.001),(-.035,z+.001),(.035,z+.001),(.239,railtop(.239,z)+.001)]
 if ti==0:
  up=[(.239,railtop(.239,TIERS[1])-.029),(.035,TIERS[1]-.029),(-.035,TIERS[1]-.029),(-.239,railtop(-.239,TIERS[1])-.029)]
 else:up=[(.239,1.119),(-.239,1.119)]
 air(tag+'_CompleteSlopingAccessSpace',yz_prism(low+up,-.499,.499),'Whole finite open cradle/access space above both inclined faces and along the full usable length; lower tier extends to the next tier underside. Complete sloped boundaries, not centre rays.')
 air(tag+'_WholeLongOpenVSlot',box((-.499,-.034,z-.029),(.499,.034,z+.25)),'Complete full-length central V-slot air through the entire rail thickness and into the open cradle above; 1 mm lateral inset.')
# One raised U on the right end, joined at two complete roots; the open handle is not a cage wall.
handle_boxes=[]
for sign in [-1,1]:
 y0,y1=sorted([sign*.24,sign*.28]);handle_boxes += [((.59,y0,.96),(.70,y1,1.00)),((.66,y0,1.00),(.70,y1,1.12))]
handle_boxes.append(((.66,-.28,1.12),(.70,.28,1.16)))
G[HANDLE]=union_boxes(handle_boxes,0,'One continuous raised U handle with two finite roots on the right posts and a genuine broad open grip space.')
for label,yy in [('Front',-.26),('Back',.26)]:contact(HANDLE+'_'+label+'Root','FullPost_Right_'+label,HANDLE,(1,0,0),(.59,yy,.98),.001599)
air('WholeRaisedUHandleOpening',box((.659,-.239,1.001),(.701,.239,1.119)),'Whole finite opening inside the raised handle, beyond both thickness faces.')
# Four new fixed fork/axle/bored-wheel groups. All axes run X and remain static.
for ix,cx in enumerate([-.54,.54]):
 for iy,cy in enumerate([-.265,.265]):
  tag=f'FixedWheelGroup_{ix+1}_{iy+1}';wheel=tag+'_TrueBoredThickWheel';fork=tag+'_ContinuousDoubleCheekBoredFork';axle=tag+'_ContinuousShoulderedAxle';zc=WHEEL_Z
  x0,x1=cx-.025,cx+.025
  outer=[(cy+.075*math.cos((i+.5)*math.tau/12),zc+.075*math.sin((i+.5)*math.tau/12)) for i in range(12)]
  G[wheel]=extrude_region(outer,[rect(cy-.017,cy+.017,zc-.012,zc+.017)],x0,x1,3,'One original thick twelve-sided wheel with a real square through-bore and full finite flat bottom facet; no rolling or swivel claim.');FEET.append(wheel)
  xs=[cx-.065,cx-.045,cx+.045,cx+.065];ys=[cy-.040,cy-.017,cy+.017,cy+.040];zs=[.035,zc-.017,zc+.012,.19,.22]
  G[fork]=grid(xs,ys,zs,lambda x,y,z: z>.19 or (abs(x-cx)>.045 and not(abs(y-cy)<.017 and zc-.017<z<zc+.012)),4,'One continuous fixed U fork: complete top bridge plus two thick cheeks, each with an actual transverse square through-bore; no swivel.')
  axle_boxes=[((cx-.079,cy-.012,zc-.012),(cx+.079,cy+.012,zc+.012))]
  for a,b,r in [(cx-.079,cx-.065,.026),(cx-.035,cx-.025,.023),(cx+.025,cx+.035,.023),(cx+.065,cx+.079,.026)]:axle_boxes.append(((a,cy-r,zc-r),(b,cy+r,zc+r)))
  G[axle]=union_boxes(axle_boxes,4,'One uninterrupted fixed square through-axle with two integral wheel-side collars and two finite outer fork end caps; all four are one continuous closed solid.')
  contact(wheel+'_BoreFloorSupportsAxle',wheel,axle,(0,0,1),(cx,cy,zc-.012),.001199)
  contact(fork+'_BothBoreCeilingsSupported',axle,fork,(0,0,1),(cx-.055,cy,zc+.012),.000959,points=[(cx-.055,cy,zc+.012),(cx+.055,cy,zc+.012)])
  for x,a,b,label in [(cx-.025,axle,wheel,'NegativeWheelSide'),(cx+.025,wheel,axle,'PositiveWheelSide'),(cx-.065,axle,fork,'NegativeForkEndCap'),(cx+.065,fork,axle,'PositiveForkEndCap')]:
   contact(tag+'_'+label,a,b,(1,0,0),(x,cy+.021,zc),.00112 if 'Wheel' in label else .00171)
  contact(fork+'_CompleteFrameSeat',fork,BODY,(0,0,1),(cx,cy,.22),.008374)
  # Isolated whole bores and complete remaining nonseat bore air.
  air(wheel+'_WholeIsolatedBore',box((x0-.001,cy-.016,zc-.011),(x1+.001,cy+.016,zc+.016)),'Entire real isolated wheel bore and both mouths, excluding only its intended axle for this isolated-hole check.',[wheel])
  p=[(cy-.016,zc-.011),(cy-.013,zc-.011),(cy-.013,zc+.013),(cy+.013,zc+.013),(cy+.013,zc-.011),(cy+.016,zc-.011),(cy+.016,zc+.016),(cy-.016,zc+.016)]
  air(wheel+'_CompleteNonseatBoreAir',yz_prism(p,x0+.001,x1-.001),'Complete connected inverted-U air along every nonbearing wheel bore side; excludes only the finite lower seat and end collars.')
  for side,label in [(-1,'Left'),(1,'Right')]:
   a,b=sorted([cx+side*.045,cx+side*.065]);air(fork+'_'+label+'WholeIsolatedBore',box((a-.001,cy-.016,zc-.016),(b+.001,cy+.016,zc+.011)),'Entire isolated fork cheek through-bore including both mouths.',[fork])
   p=[(cy-.016,zc-.016),(cy+.016,zc-.016),(cy+.016,zc+.011),(cy+.013,zc+.011),(cy+.013,zc-.013),(cy-.013,zc-.013),(cy-.013,zc+.011),(cy-.016,zc+.011)]
   air(fork+'_'+label+'CompleteNonseatBoreAir',yz_prism(p,a+.001,b-.001),'Complete connected U air over the full fork-cheek bore thickness, excluding only the finite supported ceiling.')
  # Whole side gaps: exact closed stepped volumes include all corners around collar and shaft.
  for sign,label in [(-1,'Left'),(1,'Right')]:
   a,b=sorted([cx+sign*.026,cx+sign*.044]);cut=[a,b,cx+sign*.034,cx+sign*.036];cut=sorted(x for x in set(cut) if a<=x<=b)
   def free(x,y,z):
    shaft=abs(y-cy)<.013 and abs(z-zc)<.013
    collar=abs(x-cx)<.036 and abs(y-cy)<.024 and abs(z-zc)<.024
    return not shaft and not collar
   g=grid(cut,[cy-.039,cy-.024,cy-.013,cy+.013,cy+.024,cy+.039],[.036,zc-.024,zc-.013,zc+.013,zc+.024,.189],free)
   air(tag+'_'+label+'WholeForkWheelSideGap',g,'Whole finite stepped fork-to-wheel side gap over the complete fork cheek face and wheel height; excludes only expanded actual axle/collar solids. Full corners and all thickness included.')
  solid(axle+'_FullContinuousCore',box((cx-.078,cy-.011,zc-.011),(cx+.078,cy+.011,zc+.011)),[axle],'Complete continuous finite core across both caps, both fork cheeks, two collars and wheel bore.')
  solid(fork+'_CompleteUpperBridge',box((cx-.064,cy-.039,.191),(cx+.064,cy+.039,.219)),[fork],'Whole finite thick upper fork bridge connecting both cheeks, with full support under frame.')
  WHEEL_SETS.append({'wheel':wheel,'fork':fork,'axle':axle,'cx':cx,'cy':cy,'zc':zc,'wheel_width_m':.05,'wheel_radius_m':.075,'wheel_bore_m':[.034,.029],'axle_width_m':.024})
# Whole frame aperture with the four actual fixed-wheel group envelopes excluded.
VOID_VOLUMES['WholeLowFrameCentralOpening']=dict(grid([-.539,-.460,.460,.539],[-.249,-.191,.191,.249],[.001,.221,.374],lambda x,y,z:not(abs(x)>.460 and abs(y)>.191 and z<.221)),targets=None,role='Whole central low-frame aperture through the frame thickness and to below the first tier; four conservative fixed-wheel envelopes are excluded explicitly. All remaining connected finite air is checked, not centre rays.')
# Exact original convex faceted QA-only ball, created from complete plane intersections.
# It is never added to G or exported. Bottom pair planes match both actual V rail faces.
def faceted_ball(z):
 normals=[]
 for q in itertools.product([-1,0,1],repeat=3):
  if q!=(0,0,0):normals.append(unit(q))
 normals += [unit((0,-SLOPE,-1)),unit((0,SLOPE,-1))];r=.135;centre=(0,0,z-SLOPE*.035+r*math.sqrt(1+SLOPE*SLOPE));verts=[]
 for a,b,c in itertools.combinations(normals,3):
  d=dot(a,cross(b,c))
  if abs(d)<1e-9:continue
  p=mul(add(add(cross(b,c),cross(c,a)),cross(a,b)),r/d)
  if all(dot(n,p)<=r+1e-8 for n in normals) and not any(math.dist(p,v)<1e-7 for v in verts):verts.append(p)
 faces=[]
 for n in normals:
  ids=[i for i,p in enumerate(verts) if abs(dot(n,p)-r)<1e-7]
  if len(ids)<3:continue
  u=unit(cross((1,0,0),n)) if abs(n[0])<.9 else unit(cross((0,1,0),n));v=cross(n,u);c=mul(tuple(sum(verts[i][k] for i in ids) for k in range(3)),1/len(ids));ids.sort(key=lambda i:math.atan2(dot(sub(verts[i],c),v),dot(sub(verts[i],c),u)));faces.append(tuple(ids))
 return mesh([add(p,centre) for p in verts],faces,2,'Original QA-only faceted ball of 135 mm inradius; neither exported nor counted, no real ball-size or compatibility claim.'),centre
for i,z in enumerate(TIERS):
 name=f'QAOnlyFacetedBall_Tier_{i+1}';g,centre=faceted_ball(z);QA_BALLS[name]=g
 for sign,label in [(-1,'Front'),(1,'Back')]:
  normal=unit((0,-sign*SLOPE,1));p=add(centre,mul(normal,-.135));rail=f'Tier_{i+1}_{label}ContinuousInclinedRail'
  contact(name+'_'+label+'WholeFacetSeat',rail,name,normal,p,.0007)
  QA_BALL_CONTACTS.append(CONTACTS.pop())
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
# Bounds-centre the sole exported prop without changing the ground datum.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,SOLID_VOLUMES,QA_BALLS]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS+QA_BALL_CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
CONTRACT={'single_prop_count':1,'empty_tiers':2,'continuous_inward_sloping_thick_rails':4,'open_long_V_slots':2,'finite_V_profile_end_supports':4,'independent_low_end_stops':4,'continuous_posts':4,'low_open_perimeter_frame':1,'continuous_U_handle':1,'fixed_true_bored_thick_wheels':4,'continuous_true_bored_double_cheek_forks':4,'continuous_shouldered_axles':4,'finite_ground_facets':4,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'exported_balls':0,'qa_only_original_faceted_test_balls':2,'usable_fit_or_load_or_rolling_claim':False}
def measure_trolley_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in RAILS:assert abs(max(p[0] for p in vertices[n])-min(p[0] for p in vertices[n])-1)<2e-7
 assert abs(max(p[2] for p in vertices[HANDLE])-1.16)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; whole void/material bodies, full opposed seats and all noncontact surfaces, temporary ball facets and real mutations are separate required gates')
INSIDE_TESTS=[(BODY,sub((.57,0,.24),SHIFT),sub((0,0,.24),SHIFT)),(FEET[0],sub((-.54,-.265,WHEEL_Z-.05),SHIFT),sub((-.54,-.265,WHEEL_Z),SHIFT))]
FOCUS=(0,0,.58);ORTHO=1.85
CAMERAS={'gray-front3q':(2.5,-4,2.8),'gray-back3q':(-2.5,4,2.8),'thumbnail':(2.5,-4,2.8),'qa-front':(0,-6,2.1),'qa-side':(6,0,2.1),'qa-top':(0,0,6),'qa-back':(0,6,2.1),'qa-wireframe':(2.5,-4,2.8),'silhouette-128-front':(0,-6,2.1),'silhouette-128-side':(6,0,2.1)}
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
root=bpy.data.objects.new('OneEmptyTwoTierBallTrolley',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-wheel ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_trolley_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'trolley_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/sports/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
