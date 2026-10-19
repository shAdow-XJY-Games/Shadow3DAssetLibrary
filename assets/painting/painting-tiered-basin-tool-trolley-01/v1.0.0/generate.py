"""One original empty two-basin painting tool cart with a separate three-slot holder. Static prop."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-tiered-basin-tool-trolley-01';VERSION='1.0.0';TITLE='Two-Basin Painting Tool Cart'
DESCRIPTION=('One original empty painting tool trolley, counted as one static prop. Two horizontal continuous thick-shell basins have complete bottoms, four integral walls and different clear depths. Four uprights and four full horizontal transverse bearing rails support both basins. A separate thick three-through-slot tool holder rests on its own whole U-shaped side bracket. Every slot is genuinely open through the full holder thickness and the complete air below remains empty. One whole thick U-plan push handle meets two uprights. Four fixed twelve-facet wheels, each with a real bore, a whole twin-cheek bored fork and a shouldered solid axle, end on finite flat ground facets. All 25 closed editable components have full finite opposed-face connections, full material and empty domains, and explicit all-pair relations. Metres, native Z up, front -Y and horizontally bounds-centred ground origin. Five opaque constant unlinked Principled PBR materials, no textures, logo, text, tools, paint, cargo or scene. Original basin shells, independent pierced holder, side bracket, post frame and wheel layout are authored directly. No inclined book shelf, single laundry hamper, luggage deck, brush-wash bucket or old object is loaded or repurposed. Fixed empty visual appearance only: no rolling, steering, braking, brush-size compatibility, old-asset fit, load, stability, anti-tip, ergonomics, manufacture or safety-performance claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];WHEEL_SETS=[];BASINS=[];POSTS=[];BEAMS=[]
BODY='LowerDeepContinuousBasin';HOLDER='IndependentThreeSlotToolHolder';BRACKET='WholeIndependentSideSupportBracket';HANDLE='WholeContinuousPushHandle'
PALETTE=[('MutedSageBasin',(.24,.39,.30,1),.69,0),('WarmIvoryFrame',(.67,.64,.52,1),.57,.22),('OchreToolHolder',(.64,.34,.09,1),.66,0),('GraphiteFixedTyres',(.028,.032,.030,1),.82,0),('SatinSteelAxlesAndForks',(.24,.28,.27,1),.48,.55)]
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
def outline(hx,hy,c):return [(-hx+c,-hy),(hx-c,-hy),(hx,-hy+c),(hx,hy-c),(hx-c,hy),(-hx+c,hy),(-hx,hy-c),(-hx,-hy+c)]
def basin(z0,top,inset=0,mat=0):
 return grid([-.35+inset,-.325-inset,.325+inset,.35-inset],[-.235+inset,-.210-inset,.210+inset,.235-inset],[z0+inset,z0+.025-inset,top-inset],lambda x,y,z:z<z0+.025-inset or abs(x)>.325+inset or abs(y)>.210+inset,mat,'One continuous closed thick horizontal basin shell with complete bottom and four integral walls, no separate strips or floating rim.')
for label,z0,top in [('LowerDeep',.35,.52),('UpperShallow',.82,.925)]:
 n=label+'ContinuousBasin';BASINS.append(n);G[n]=basin(z0,top)
 solid(n+'_EntireConnectedFloorWallsRoots',basin(z0,top,.001),[n],'Entire connected inset material of full bottom, four whole walls, all four wall corners and complete floor-to-wall roots.')
 air(n+'_EntireEmptyCavity',box((-.324,-.209,z0+.026),(.324,.209,top+.001)),'Entire finite cavity including every inner corner, full clear height and open mouth, 1 mm off solid boundaries.')
 for side,cy in [('Front',-.265),('Back',.265)]:
  rail=label+'FullBearingRail_'+side;BEAMS.append(rail);ya,yb=(-.285,-.215) if cy<0 else (.215,.285)
  G[rail]=box((-.37,ya,z0-.04),(.37,yb,z0),1,'Complete transverse solid under-basin rail; both full cut ends meet posts and full inboard top strip meets the basin underside.')
  solid(rail+'_WholeMaterial',box((-.369,ya+.001,z0-.039),(.369,yb-.001,z0-.001)),[rail],'Whole finite inset rail material, full length and complete rectangular section.')
  contact(rail+'_EntireBasinBearingStrip',rail,n,(0,0,1),(0,(-.225 if cy<0 else .225),z0),.013999)
for ix,cx in enumerate([-.39,.39]):
 for iy,cy in enumerate([-.265,.265]):
  n=f'FullHeightUpright_{ix+1}_{iy+1}';POSTS.append(n);G[n]=box((cx-.02,cy-.02,.20),(cx+.02,cy+.02,.985),1,'One whole outside upright, continuously joins fork top, both rail ends, and the corresponding handle or side bracket.')
  solid(n+'_WholeMaterial',box((cx-.019,cy-.019,.201),(cx+.019,cy+.019,.984)),[n],'Whole finite full-height upright material including all connection elevations.')
  for level,z0 in [('LowerDeep',.35),('UpperShallow',.82)]:
   rail=level+'FullBearingRail_'+('Front' if cy<0 else 'Back');left=cx<0
   contact(rail+'_PostEnd_'+str(ix+1),n if left else rail,rail if left else n,(1,0,0),(-.37 if left else .37,cy,z0-.02),.001599)
# One thick continuous U-plan push handle on the left, supported on both post faces.
def handle(inset=0):
 return grid([-.51+inset,-.47-inset,-.41-inset],[-.285+inset,-.245-inset,.245+inset,.285-inset],[.945+inset,.985-inset],lambda x,y,z:x<-.47-inset or abs(y)>.245+inset,1,'One whole U-plan thick push handle with two full post-end roots; its central opening stays empty.')
G[HANDLE]=handle();solid(HANDLE+'_WholeConnectedMaterial',handle(.001),[HANDLE],'Complete connected finite inset handle material through both full end roots, both corners and full handrail.')
for iy,cy in enumerate([-.265,.265]):contact(HANDLE+'_FullPostRoot_'+str(iy+1),HANDLE,POSTS[iy],(1,0,0),(-.41,cy,.965),.001599)
air(HANDLE+'_EntireCentralOpening',box((-.469,-.244,.944),(-.411,.244,.986)),'Whole through-thickness central handle opening and both vertical mouths; no ergonomics claim.')
# Independent right-side U-shaped bracket has two complete post-face roots.
def bracket(inset=0):
 return grid([.41+inset,.505+inset,.545-inset],[-.285+inset,-.245-inset,.245+inset,.285-inset],[.845+inset,.885-inset],lambda x,y,z:x>.505+inset or abs(y)>.245+inset,1,'One whole U-plan side bracket with two complete post roots, continuous outer rail and an open middle below all tool slots.')
G[BRACKET]=bracket();solid(BRACKET+'_WholeConnectedMaterial',bracket(.001),[BRACKET],'Complete connected bracket material, both cantilever roots, both corners and whole outer bearing rail.')
for iy,cy in enumerate([-.265,.265]):contact(BRACKET+'_FullPostRoot_'+str(iy+1),POSTS[2+iy],BRACKET,(1,0,0),(.41,cy,.865),.001599)
SLOT_CENTRES=[-.14,0,.14]
def holder(inset=0):
 ys=sorted([-.20+inset,.20-inset]+[cy+d for cy in SLOT_CENTRES for d in [-.025-inset,.025+inset]])
 return grid([.425+inset,.445-inset,.485+inset,.545-inset],ys,[.885+inset,.935-inset],lambda x,y,z:not(.445-inset<x<.485+inset and any(abs(y-cy)<.025+inset for cy in SLOT_CENTRES)),2,'One continuous thick separate rectangular holder with three genuine full-thickness vertical slots, full end bridges and full side rails.')
G[HOLDER]=holder();solid(HOLDER+'_AllRailsBridgesAndSlotWalls',holder(.001),[HOLDER],'Entire connected inset material around all three slots, both end bridges, both inter-slot bridges and both full side rails.')
contact(HOLDER+'_EntireOuterRailBearing',BRACKET,HOLDER,(0,0,1),(.525,0,.885),.015999)
for i,cy in enumerate(SLOT_CENTRES):
 air('ToolSlot_'+str(i+1)+'_EntireThroughHoleAndAirBelow',box((.446,cy-.024,.525),(.484,cy+.024,.946)),'Whole vertical tool-slot cross section through both holder faces and its entire empty column below, including every corner; no fitted brush is included.')
air('EntireOpenUnderHolder',box((.426,-.199,.525),(.504,.199,.884)),'Complete finite empty under-holder region up to the bracket inner side and across full holder length, not just a centre ray.')
air('LowerBasin_WholeAboveCavityAccess',box((-.324,-.209,.521),(.324,.209,.779)),'Entire central air between lower rim and upper support-rail underside, all corners.')
for sign,label in [(-1,'Front'),(1,'Back')]:
 lo,hi=sorted([sign*.211,sign*.33]);air('LowerBasin_'+label+'EntireSideAccess',box((-.324,lo,.521),(.324,hi,.779)),'Complete front/back horizontal access from outside the cart into the clear inter-basin space.')
# Four independently dimensioned 12-facet fixed wheel assemblies. Generic closed
# polygon extrusion is shared with other assets, while every dimension is new.
WHEEL_Z=.065*math.cos(math.pi/12)
for ix,cx in enumerate([-.39,.39]):
 for iy,cy in enumerate([-.265,.265]):
  tag=f'FixedWheelGroup_{ix+1}_{iy+1}';wheel=tag+'_TwelveFacetBoredTyre';fork=tag+'_WholeBoredFork';axle=tag+'_ShoulderedAxle';zc=WHEEL_Z
  x0,x1=cx-.020,cx+.020
  outer=[(cy+.065*math.cos((i+.5)*math.tau/12),zc+.065*math.sin((i+.5)*math.tau/12)) for i in range(12)]
  G[wheel]=extrude_region(outer,[rect(cy-.012,cy+.012,zc-.008,zc+.013)],x0,x1,3,'One original thick twelve-facet wheel with a true full-thickness rectangular axle bore, complete sidewalls and finite flat bottom facet.');FEET.append(wheel)
  G[fork]=grid([cx-.052,cx-.034,cx+.034,cx+.052],[cy-.033,cy-.012,cy+.012,cy+.033],[.026,zc-.013,zc+.008,.155,.20],lambda x,y,z:z>.155 or (abs(x-cx)>.034 and not(abs(y-cy)<.012 and zc-.013<z<zc+.008)),4,'One whole thick fork bridge and two complete pierced cheeks; no detached cap or painted fake hole.')
  ab=[((cx-.064,cy-.008,zc-.008),(cx+.064,cy+.008,zc+.008))]
  shoulders=[(cx-.064,cx-.052,.020),(cx-.026,cx-.020,.018),(cx+.020,cx+.026,.018),(cx+.052,cx+.064,.020)]
  for a,b,r in shoulders:ab.append(((a,cy-r,zc-r),(b,cy+r,zc+r)))
  G[axle]=union_boxes(ab,4,'One continuous square axle with integral finite twin wheel collars and twin outer fork caps; fixed illustrative assembly.')
  contact(wheel+'_CompleteLowerBoreSeat',wheel,axle,(0,0,1),(cx,cy,zc-.008),.000639)
  contact(fork+'_BothCompleteBoreCeilings',axle,fork,(0,0,1),(cx-.043,cy,zc+.008),.000575,points=[(cx-.043,cy,zc+.008),(cx+.043,cy,zc+.008)])
  # Areas subtract the complete hole: wheel collar .036^2-.024*.021;
  # fork cap .040^2-.024*.021. They are actual full opposed finite annuli.
  for x,a,b,label in [(cx-.020,axle,wheel,'LeftWheelCollar'),(cx+.020,wheel,axle,'RightWheelCollar'),(cx-.052,axle,fork,'LeftForkCap'),(cx+.052,fork,axle,'RightForkCap')]:contact(tag+'_'+label,a,b,(1,0,0),(x,cy+.017 if 'Wheel' in label else cy+.019,zc),.000791 if 'Wheel' in label else .001095)
  contact(fork+'_FullUprightSeat',fork,POSTS[ix*2+iy],(0,0,1),(cx,cy,.20),.001599)
  air(wheel+'_WholeIsolatedBore',box((x0-.001,cy-.011,zc-.007),(x1+.001,cy+.011,zc+.012)),'Entire isolated wheel bore including both open mouths, full thickness and all corners, checked against this wheel.',[wheel])
  p=[(cy-.011,zc-.007),(cy-.009,zc-.007),(cy-.009,zc+.009),(cy+.009,zc+.009),(cy+.009,zc-.007),(cy+.011,zc-.007),(cy+.011,zc+.012),(cy-.011,zc+.012)]
  air(wheel+'_CompleteNonseatBoreAir',yz_prism(p,x0+.001,x1-.001),'Whole inverted-U nonbearing bore air beside both shaft sides and above the shaft, complete free length.')
  for sign,label in [(-1,'Left'),(1,'Right')]:
   a,b=sorted([cx+sign*.034,cx+sign*.052]);air(fork+'_'+label+'WholeIsolatedBore',box((a-.001,cy-.011,zc-.012),(b+.001,cy+.011,zc+.007)),'Entire isolated fork-cheek bore including both open mouths and all corners.',[fork])
   p=[(cy-.011,zc-.012),(cy+.011,zc-.012),(cy+.011,zc+.007),(cy+.009,zc+.007),(cy+.009,zc-.009),(cy-.009,zc-.009),(cy-.009,zc+.007),(cy-.011,zc+.007)]
   air(fork+'_'+label+'CompleteNonseatBoreAir',yz_prism(p,a+.001,b-.001),'Whole connected U-shaped free air around the shaft and below it, across complete fork-cheek depth.')
   a,b=sorted([cx+sign*.021,cx+sign*.033]);cut=sorted(set([a,b,cx+sign*.025,cx+sign*.027]))
   free=lambda x,y,z:not(abs(y-cy)<.009 and abs(z-zc)<.009) and not(abs(x-cx)<.027 and abs(y-cy)<.019 and abs(z-zc)<.019)
   air(tag+'_'+label+'WholeWheelForkSideAir',grid(cut,[cy-.032,cy-.019,cy-.009,cy+.009,cy+.019,cy+.032],[.027,zc-.019,zc-.009,zc+.009,zc+.019,.154],free),'Complete stepped free volume between wheel side and fork cheek over full cheek width and height, excluding only expanded true axle and collar material.')
  tyre_core=[(cy+.064*math.cos((i+.5)*math.tau/12),zc+.064*math.sin((i+.5)*math.tau/12)) for i in range(12)]
  solid(wheel+'_EntireAnnularMaterial',extrude_region(tyre_core,[rect(cy-.013,cy+.013,zc-.009,zc+.014)],x0+.001,x1-.001),[wheel],'Whole finite annular wheel material, all twelve outside facets, both full sidewalls and every bore wall.')
  innerfork=grid([cx-.051,cx-.035,cx+.035,cx+.051],[cy-.032,cy-.013,cy+.013,cy+.032],[.027,zc-.014,zc+.009,.156,.199],lambda x,y,z:z>.156 or(abs(x-cx)>.035 and not(abs(y-cy)<.013 and zc-.014<z<zc+.009)))
  solid(fork+'_EntireConnectedMaterial',innerfork,[fork],'Complete connected inset fork material: both full pierced cheek bodies, all hole walls and whole bridge.')
  core=[((cx-.063,cy-.007,zc-.007),(cx+.063,cy+.007,zc+.007))]
  for a,b,r in shoulders:core.append(((a+.001,cy-r+.001,zc-r+.001),(b-.001,cy+r-.001,zc+r-.001)))
  solid(axle+'_EntireConnectedMaterial',union_boxes(core),[axle],'Complete connected finite inset axle core and all four integral shoulders, including every collar and cap.')
  WHEEL_SETS.append({'wheel':wheel,'fork':fork,'axle':axle,'cx':cx,'cy':cy,'zc':zc,'wheel_width_m':.040,'wheel_radius_m':.065,'wheel_bore_m':[.024,.021],'axle_width_m':.016})
# Centre actual full horizontal bounds while retaining Z=0 ground datum.
SHIFT=(.0175,0,0)
for group in [G,VOID_VOLUMES,SOLID_VOLUMES]:
 for g in group.values():g['vertices']=[sub(v,SHIFT) for v in g['vertices']]
for r in CONTACTS:r['points']=[sub(p,SHIFT) for p in r['points']];r['plane_m']-=dot(r['axis'],SHIFT)
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
for w in WHEEL_SETS:w['cx']-=SHIFT[0]
SHIFT=(0,0,0)
CONTRACT={'single_prop_count':1,'empty_static_prop':True,'continuous_horizontal_basins':2,'different_clear_basin_depths_m':[.145,.080],'full_uprights':4,'complete_transverse_bearing_rails':4,'separate_three_slot_holder':1,'real_vertical_slots':3,'whole_side_bracket':1,'whole_push_handle':1,'fixed_true_bored_twelve_facet_wheels':4,'continuous_bored_forks':4,'continuous_shouldered_axles':4,'finite_flat_ground_facets':4,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'included_tools_or_cargo':0,'fit_load_rolling_or_safety_claim':False}
def measure_trolley_geometry(vertices):
 assert set(vertices)==set(G) and len(vertices)==25
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in POSTS:assert abs(max(p[2] for p in vertices[n])-.985)<2e-7
 return dict(CONTRACT,geometry_scope='whole coordinates; independent complete air/material, finite opposed seats, all pairs and actual mutations remain required')
INSIDE_TESTS=[(BODY,(-.0175,0,.36),(-.0175,0,.40)),(HOLDER,(.51,0,.91),(.4475,0,.91)),(FEET[0],(-.4075,-.265,WHEEL_Z-.04),(-.4075,-.265,WHEEL_Z))]
FOCUS=(0,0,.49);ORTHO=1.65
CAMERAS={'gray-front3q':(3,-4,3.3),'gray-back3q':(-3,4,3.3),'thumbnail':(3,-4,3.3),'qa-front':(0,-6,2.4),'qa-side':(6,0,2.4),'qa-top':(0,0,6),'qa-back':(0,6,2.4),'qa-wireframe':(3,-4,3.3),'silhouette-128-front':(0,-6,2.4),'silhouette-128-side':(6,0,2.4)}
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
root=bpy.data.objects.new('OneEmptyTwoBasinPaintingToolCart',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-wheel ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
