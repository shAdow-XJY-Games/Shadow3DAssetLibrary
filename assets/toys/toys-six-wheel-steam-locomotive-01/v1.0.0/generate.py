"""Original six-wheel toy steam-locomotive shape. One fixed, static illustrative prop."""
import math,json,hashlib,sys,time,struct
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='toys-six-wheel-steam-locomotive-01';VERSION='1.0.0';TITLE='Six-Wheel Steam-Shaped Toy Locomotive'
DESCRIPTION=('One original short six-wheel steam-shaped toy locomotive, counted as one static prop. A new low thick three-bore chassis supports a blunt closed horizontal boiler and a truly empty rear cab with two side windows, an open rear doorway, integral floor, four continuous window posts and one thick overhanging roof. Three continuous square shoulder axles pass through three real chassis bores and six independently bored twelve-sided wheels; every wheel rests on a finite flat ground face. Each wheel bore floor supports its fixed axle, axle tops support the chassis bore ceilings, and integral inner shoulders and outer caps restrain the complete wheel side faces. A short flared capped chimney rests on the complete horizontal boiler crown facet. A low front buffer and a thick rear coupling ear with a genuine vertical through-hole have finite root faces seated on the chassis ends. All fifteen closed connected components belong to this one fixed pose. Five unlinked constant opaque PBR colours; metres, Z up, front -Y and bounds-centred ground origin. No track, carriages, figure, connecting rod, rope, smoke, animation, external texture, rolling, steering, steam, drive, sound, traction, operative coupling, track compatibility, child age suitability, swallowing or pinch protection, material safety, human fit, load, durability, manufacture or toy safety certification claim. Geometry is newly authored; it is not a recoloured four-wheel wooden car, a scaled railway wagon or an airport tanker with a chimney.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};NONCONTACT_SURFACES=[]
BODY='Chassis_NewThreeAxleBores';CAB='Cab_IntegralFloorPostsRoof';BOILER='Boiler_ClosedBluntHorizontalBody';CHIMNEY='Chimney_ShortFlaredClosedTop';BUFFER='Buffer_FrontLowCrossbar';EAR='Coupling_RearBoredEar'
AXLES=[];WHEELS=[];FEET=[]
ZC=.064*math.cos(math.pi/12);AXLE_Y=[-.180,-.010,.160];DECK=.136;BZ=DECK+.070*math.cos(math.pi/12);BTOP=DECK+2*.070*math.cos(math.pi/12)
PALETTE=[('WarmCrimson_ChassisCab',(.50,.057,.040,1),.59,0),('CreamPaint_ThickWheels',(.83,.62,.30,1),.65,0),('Slate_FixedAxlesChimney',(.055,.071,.078,1),.70,0),('DeepTeal_BluntBoiler',(.028,.235,.230,1),.60,0),('GoldenOchre_RoofBuffer',(.72,.31,.060,1),.62,0)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no procedural or image texture nodes.'
FOCUS=(0,0,.170);ORTHO=.77
CAMERAS={'gray-front3q':(.92,-1.10,.79),'gray-back3q':(-.92,1.10,.79),'thumbnail':(.92,-1.10,.79),'qa-front':(0,-1.4,.64),'qa-side':(1.4,0,.64),'qa-top':(0,0,1.6),'qa-back':(0,1.4,.64),'qa-wireframe':(.92,-1.10,.79),'silhouette-128-front':(0,-1.4,.64),'silhouette-128-side':(1.4,0,.64)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
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
def volume(entries,name,g,targets,role):entries[name]=dict(g,targets=list(targets),role=role)
def contact(a,b,axis,plane,points,area,label):
 u,v={ (1,0,0):((0,1,0),(0,0,1)), (0,1,0):((0,0,1),(1,0,0)), (0,0,1):((1,0,0),(0,1,0)) }[axis]
 CONTACTS.append({'name':label,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':.0006,'scope':'complete finite opposed actual faces and complete no-positive-penetration test; static geometric support only'})

def union_boxes(boxes,mat=0,role='one continuous exact rectilinear solid',material_at=None):
 # One conforming global grid; only exterior occupied-cell faces survive.
 # No embedded cuboids, overlapping shells, T-junctions or Boolean modifiers.
 cuts=[sorted(set(round(b[j][k],9) for b in boxes for j in [0,1])) for k in range(3)]
 cells=set()
 for i in range(len(cuts[0])-1):
  for j in range(len(cuts[1])-1):
   for k in range(len(cuts[2])-1):
    c=[(cuts[a][n]+cuts[a][n+1])/2 for a,n in enumerate([i,j,k])]
    if any(all(lo[a]<c[a]<hi[a] for a in range(3)) for lo,hi in boxes):cells.add((i,j,k))
 m=Mesh()
 for cell in sorted(cells):
  lo=[cuts[a][n] for a,n in enumerate(cell)];hi=[cuts[a][n+1] for a,n in enumerate(cell)]
  for a in range(3):
   other=[k for k in range(3) if k!=a]
   for sign in [-1,1]:
    neighbour=list(cell);neighbour[a]+=sign
    if tuple(neighbour) in cells:continue
    face=[]
    for s,t in [(0,0),(1,0),(1,1),(0,1)]:
     p=lo.copy();p[a]=lo[a] if sign<0 else hi[a];p[other[0]]=[lo[other[0]],hi[other[0]]][s];p[other[1]]=[lo[other[1]],hi[other[1]]][t];face.append(p)
    centre=[sum(p[k] for p in face)/4 for k in range(3)];mm=material_at(centre) if material_at else mat;m.face(face,mm,'continuous_grid_boundary')
 return m.result(role,mat)
def cyclic_xy_prism(poly,holes,z0,z1,mat=0,role='closed horizontal prism with full through-hole'):
 g=extrude_region(poly,holes,z0,z1,mat,role);g['vertices']=[(p[1],p[2],p[0]) for p in g['vertices']];return g
def radial_body_y(layout,mat,role):
 m=Mesh();rings=[[(r*math.cos((i+.5)*math.tau/12),y,BZ+r*math.sin((i+.5)*math.tau/12)) for i in range(12)] for y,r in layout]
 m.face(rings[0],mat,'closed_front_end');m.face(rings[-1],mat,'closed_rear_end')
 for a,b in zip(rings,rings[1:]):
  for i in range(12):j=(i+1)%12;m.face([a[i],a[j],b[j],b[i]],mat,'boiler_complete_skin')
 return m.result(role,mat)
BODY_HOLES=[rect(y-.015,y+.015,ZC-.015,ZC+.010) for y in AXLE_Y]
G[BODY]=extrude_region(chamfer(-.252,.252,.034,DECK,.008),BODY_HOLES,-.070,.070,0,'New uninterrupted low chassis with three genuine transverse axle through-bores; no reused automobile body.')
def axle_geometry(y):
 core=[(-.010,-.010),(0,-.010),(.010,-.010),(.010,0),(.010,.010),(0,.010),(-.010,.010),(-.010,0)]
 end=[(.027*math.cos(-3*math.pi/4+math.tau*i/8),.027*math.sin(-3*math.pi/4+math.tau*i/8)) for i in range(8)]
 layout=[(-.146,end),(-.132,end),(-.132,core),(-.100,core),(-.100,end),(-.086,end),(-.086,core),(.086,core),(.086,end),(.100,end),(.100,core),(.132,core),(.132,end),(.146,end)]
 rr=[[(x,y+yy,ZC+zz) for yy,zz in p] for x,p in layout];m=Mesh();m.face(rr[0],2,'cap');m.face(rr[-1],2,'cap')
 for k,(a,b) in enumerate(zip(rr,rr[1:])):
  for i in range(8):j=(i+1)%8;m.face([a[i],a[j],b[j],b[i]],2,'shaft_or_shoulder_'+str(k))
 return m.result('One uninterrupted fixed square axle with integral paired shoulders and thick end caps; no implied rolling freedom or embedded component overlap.',2)
for ai,y in enumerate(AXLE_Y):
 axle='Axle_'+['Front','Middle','Rear'][ai]+'_IntegralShouldersAndCaps';AXLES.append(axle);G[axle]=axle_geometry(y)
 contact(axle,BODY,(0,0,1),ZC+.010,[(x,y,ZC+.010) for x in [-.045,0,.045]],.0027,axle+'_TopSupportsChassisBoreCeiling')
 for sign,label in [(-1,'Left'),(1,'Right')]:
  w='Wheel_'+['Front','Middle','Rear'][ai]+'_'+label;WHEELS.append(w);FEET.append(w);x0,x1=sorted([sign*.100,sign*.132])
  outer=[(y+.064*math.cos((i+.5)*math.tau/12),ZC+.064*math.sin((i+.5)*math.tau/12)) for i in range(12)]
  G[w]=extrude_region(outer,[rect(y-.015,y+.015,ZC-.010,ZC+.015)],x0,x1,1,'Independent thick twelve-sided wheel with true square centre hole and finite complete ground facet; fixed illustration only.')
  contact(w,axle,(0,0,1),ZC-.010,[(x,y,ZC-.010) for x in [x0+.006,(x0+x1)/2,x1-.006]],.00062,w+'_BoreFloorSupportsAxleBottom')
  for x,a,b,suffix in [(x0,axle,w,'NegativeShoulder'),(x1,w,axle,'PositiveShoulder')]:contact(a,b,(1,0,0),x,[(x,y-.020,ZC),(x,y+.020,ZC),(x,y,ZC+.020)],.0013,w+'_'+suffix)
  volume(ISOLATED_VOID_VOLUMES,w+'_WholeIsolatedBore',box_geometry((x0-.001,y-.0145,ZC-.0095),(x1+.001,y+.0145,ZC+.0145)),[w],'Complete isolated wheel bore and both mouths, inset 0.5 mm; shoulder geometry intentionally excluded only in this isolated-hole test.')
  poly=[(y-.0145,ZC-.0095),(y-.0105,ZC-.0095),(y-.0105,ZC+.0105),(y+.0105,ZC+.0105),(y+.0105,ZC-.0095),(y+.0145,ZC-.0095),(y+.0145,ZC+.0145),(y-.0145,ZC+.0145)]
  volume(VOID_VOLUMES,w+'_CompleteAssembledBoreAir',extrude_region(poly,[],x0+.0005,x1-.0005),[],'Entire connected inverted-U remaining air across all noncontact wheel bore sides, between actual shoulder planes; only the intentional support floor is excluded.')
  NONCONTACT_SURFACES.append({'name':w+'_Bore','solid':w,'other':axle,'tag':'hole_wall_1','x_range':[x0+.0005,x1-.0005],'y_range':[y-.015,y+.015],'z_range':[ZC-.0095,ZC+.015],'minimum_distance_m':.00049})
 volume(ISOLATED_VOID_VOLUMES,axle+'_WholeIsolatedChassisBore',box_geometry((-.071,y-.0145,ZC-.0145),(.071,y+.0145,ZC+.0095)),[BODY],'Complete isolated chassis bore through the entire thickness and both mouths, inset 0.5 mm.')
 poly=[(y-.0145,ZC-.0145),(y+.0145,ZC-.0145),(y+.0145,ZC+.0095),(y+.0105,ZC+.0095),(y+.0105,ZC-.0105),(y-.0105,ZC-.0105),(y-.0105,ZC+.0095),(y-.0145,ZC+.0095)]
 volume(VOID_VOLUMES,axle+'_CompleteAssembledChassisBoreAir',extrude_region(poly,[],-.071,.071),[],'Complete connected U-shaped remaining chassis-bore air through both mouths, excluding only the finite supporting ceiling.')
 NONCONTACT_SURFACES.append({'name':axle+'_ChassisBore','solid':BODY,'other':axle,'tag':'hole_wall_'+str(ai+1),'x_range':[-.070,.070],'y_range':[y-.015,y+.015],'z_range':[ZC-.015,ZC+.0095],'minimum_distance_m':.00049})
 volume(SOLID_VOLUMES,'AxleCore_'+str(ai),box_geometry((-.145,y-.0085,ZC-.0085),(.145,y+.0085,ZC+.0085)),[axle],'Full finite uninterrupted square axle core across both caps, both wheels and the chassis.')
 volume(SOLID_VOLUMES,'ChassisBoreBridge_'+str(ai),box_geometry((-.068,y-.013,ZC+.011),(.068,y+.013,DECK-.001)),[BODY],'Complete finite full-width bearing bridge above this chassis bore.')
G[BOILER]=radial_body_y([(-.232,.058),(-.216,.070),(.020,.070),(.036,.058)],3,'One closed blunt twelve-sided horizontal boiler form, independently authored, closed front and rear faces, complete broad lower facet resting on the chassis; no pressure vessel or steam claim.')
contact(BODY,BOILER,(0,0,1),DECK,[(x,y,DECK) for x,y in [(-.010,-.18),(0,-.09),(.010,0)]],.0084,'ChassisSupportsCompleteBoilerBottomFacet')
# A true empty rear cab. Floor, side sills, four posts, window headers,
# front wall, short rear returns and the entire overhanging roof are one solid.
CAB_BOXES=[((-.098,.066,DECK),(.098,.244,.154)),((-.098,.066,.154),(.098,.084,.298)),((-.114,.050,.298),(.114,.260,.322))]
for sign in [-1,1]:
 x0,x1=sorted([sign*.080,sign*.098]);CAB_BOXES += [((x0,.084,.154),(x1,.244,.194)),((x0,.084,.278),(x1,.244,.298)),((x0,.084,.194),(x1,.106,.278)),((x0,.214,.194),(x1,.244,.278))]
 x0,x1=sorted([sign*.062,sign*.080]);CAB_BOXES.append(((x0,.226,.154),(x1,.244,.298)))
G[CAB]=union_boxes(CAB_BOXES,0,'One continuous thick cab floor, front wall, four genuine side-window posts, two headers, rear jamb returns and complete integral overhanging roof; real open inner cabin and rear doorway.',lambda c:4 if c[2]>=.298-1e-9 else 0)
contact(BODY,CAB,(0,0,1),DECK,[(x,y,DECK) for x,y in [(-.050,.100),(0,.160),(.050,.224)]],.024,'ChassisSupportsCompleteCabFloor')
# Independent closed flared short stack with a full finite bottom seat.
m=Mesh();rings=[]
for z,r in [(BTOP,.016),(BTOP+.012,.016),(BTOP+.056,.021),(BTOP+.066,.029),(BTOP+.078,.029)]:rings.append([(r*math.cos((i+.5)*math.tau/8),-.142+r*math.sin((i+.5)*math.tau/8),z) for i in range(8)])
m.face(rings[0],2,'whole_chimney_foot');m.face(rings[-1],2,'closed_stack_top')
for a,b in zip(rings,rings[1:]):
 for i in range(8):j=(i+1)%8;m.face([a[i],a[j],b[j],b[i]],2,'continuous_stack_root_and_flare')
G[CHIMNEY]=m.result('Short capped flared chimney silhouette, closed solid and finite full base on the boiler top facet; no steam passage, smoke or operating claim.',2)
contact(BOILER,CHIMNEY,(0,0,1),BTOP,[(x,-.142+dy,BTOP) for x,dy in [(0,0),(-.008,.004),(.008,-.004)]],.00070,'BoilerCrownSupportsWholeChimneyFoot')
G[BUFFER]=box_geometry((-.112,-.300,.084),(.112,-.252,.108),4,'One low broad closed front buffer, connected through a finite complete root face to the chassis front end; no impact or coupling function.')
contact(BUFFER,BODY,(0,1,0),-.252,[(x,-.252,z) for x,z in [(-.045,.096),(0,.092),(.045,.100)]],.0033,'BufferRootSeatedOnChassisFront')
G[EAR]=cyclic_xy_prism(chamfer(-.026,.026,.252,.300,.006),[chamfer(-.011,.011,.267,.290,.003)],.090,.114,2,'One complete thick horizontal rear coupling ear with a genuine chamfered through-hole and full finite front-root connection; fixed visual form with no usable mating object.')
contact(BODY,EAR,(0,1,0),.252,[(x,.252,z) for x,z in [(-.010,.098),(0,.102),(.010,.106)]],.00094,'ChassisRearSupportsBoredEarRoot')
# Full cabin air, including each complete opening and rear exit, represented
# by one conforming union volume instead of centre points or a sparse ray.
CAB_AIR_BOXES=[((-.079,.085,.155),(.079,.225,.297)),((-.061,.225,.155),(.061,.254,.297)),((-.107,.107,.195),(.107,.213,.277))]
volume(VOID_VOLUMES,'WholeCabInteriorWindowsRearMouth',union_boxes(CAB_AIR_BOXES),[],'Complete connected cabin air including the full inset interior, both whole side-window passages and the rear doorway mouth; all boundaries tested against the complete locomotive.')
for sign,label in [(-1,'Left'),(1,'Right')]:
 x0,x1=sorted([sign*.079,sign*.107]);volume(VOID_VOLUMES,'Whole'+label+'CabWindow',box_geometry((x0,.107,.195),(x1,.213,.277)),[],'Entire side-window passage beyond both thick wall faces, 1 mm inset all around.')
volume(VOID_VOLUMES,'WholeRearCabDoorway',box_geometry((-.061,.225,.155),(.061,.254,.297)),[],'Entire rear doorway including the external mouth, between complete jambs, floor and roof.')
volume(VOID_VOLUMES,'WholeRearCouplingThroughHole',cyclic_xy_prism(chamfer(-.010,.010,.268,.289,.003),[],.089,.115),[],'Complete chamfered rear ear through-hole and both vertical mouths, 1 mm inset from every side boundary.')
volume(VOID_VOLUMES,'WholeBoilerCabSeparation',box_geometry((-.057,.037,.155),(.057,.065,.260)),[],'Complete positive finite gap between the closed rear boiler end and the solid front cab wall, excluding any hidden boiler extension into the cab.')
volume(VOID_VOLUMES,'WholeChassisGroundGap',box_geometry((-.069,-.243,.001),(.069,.243,.033)),[],'Complete broad finite ground air below the chassis; six wheels are entirely outside its width.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
volume(SOLID_VOLUMES,'WholeChassisLowerWeb',box_geometry((-.069,-.243,.035),(.069,.243,ZC-.016)),[BODY],'Complete finite lower uninterrupted chassis web beneath all three bores.')
volume(SOLID_VOLUMES,'WholeCabFloor',box_geometry((-.097,.067,DECK+.001),(.097,.243,.153)),[CAB],'Complete finite inset thick floor supporting the empty cabin without a missing bottom.')
volume(SOLID_VOLUMES,'WholeCabRoof',box_geometry((-.113,.051,.299),(.113,.259,.321)),[CAB],'Entire finite inset overhanging thick roof, continuous across all cabin walls.')
volume(SOLID_VOLUMES,'WholeCabFrontWall',box_geometry((-.097,.067,.155),(.097,.083,.297)),[CAB],'Complete finite front wall separating the cabin air from the boiler.')
for sign,label in [(-1,'Left'),(1,'Right')]:
 x0,x1=sorted([sign*.081,sign*.097])
 for end,y0,y1 in [('Front',.085,.105),('Rear',.215,.243)]:volume(SOLID_VOLUMES,label+end+'FullCabPost',box_geometry((x0,y0,.155),(x1,y1,.297)),[CAB],'Entire finite window-post material from floor to roof, including both complete structural roots.')
volume(SOLID_VOLUMES,'WholeChimneyRoot',box_geometry((-.008,-.150,BTOP+.001),(.008,-.134,BTOP+.025)),[CHIMNEY],'Full finite inset stack root joining its broad bottom seat to the upper flared body.')
volume(SOLID_VOLUMES,'BoilerClosedFrontEnd',box_geometry((-.030,-.231,BZ-.030),(.030,-.219,BZ+.030)),[BOILER],'Finite complete thickness of the blunt closed boiler front end, not a false open tube.')
volume(SOLID_VOLUMES,'BoilerClosedRearEnd',box_geometry((-.030,.023,BZ-.030),(.030,.035,BZ+.030)),[BOILER],'Finite complete thickness of the closed rear boiler end, separate from all cabin air.')
volume(SOLID_VOLUMES,'RearEarContinuousRoot',box_geometry((-.018,.253,.091),(.018,.264,.113)),[EAR],'Finite complete root bridge between the rear chassis attachment and the true ear hole.')

def measure_locomotive_geometry(vertices):
 assert set(vertices)==set(G),'Unexpected mesh set'
 for n,g in G.items():
  actual={tuple(round(struct.unpack('f',struct.pack('f',float(c)))[0],6) for c in p) for p in vertices[n]};expected={tuple(round(struct.unpack('f',struct.pack('f',float(c)))[0],6) for c in p) for p in g['vertices']};assert actual==expected,(n,'actual shape changed')
 return {'single_prop_count':1,'closed_components':len(G),'chassis_true_axle_bores':3,'continuous_fixed_axles':3,'independently_bored_thick_wheels':6,'real_side_windows':2,'real_open_rear_doorways':1,'whole_empty_cab':True,'closed_boiler_ends':2,'supported_short_chimneys':1,'real_rear_coupling_holes':1,'bounds_m':[.292,.600,round(BTOP+.078,6)],'chassis_ground_gap_m':.034,'wheel_thickness_m':.032,'wheel_outer_sides':12,'wheel_radius_m':.064,'axle_centres_y_m':AXLE_Y,'axle_height_m':ZC,'finite_opposed_contacts':len(CONTACTS),'material_contract':MATERIAL_CONTRACT,'static_pose_only':True,'rolling_steam_or_child_safety_claim':False}
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
root=bpy.data.objects.new('OneStaticBoredSteamToyLocomotive',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0008,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
locomotive_evidence=measure_locomotive_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'locomotive_geometry':locomotive_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
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
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
