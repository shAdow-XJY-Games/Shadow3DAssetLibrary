"""One original deep floating-panel frame. One static form; plural family partial."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-recessed-floating-panel-frame-01';VERSION='1.0.0';TITLE='Deep Floating-panel Picture Frame'
DESCRIPTION=('One original horizontal deep floating-panel picture frame, one static prop and one form only; the original plural frame-form family remains partial. A continuous 90 mm deep closed rectangular annulus and full 18 mm rear board surround an unpatterned 12 mm display panel. Four complete 40 by 40 mm rear spacers hold the panel 50 mm before the rear board. Real uninterrupted 30 mm air gaps separate every panel edge from the frame, and the front face is recessed 28 mm. Original fixed rear strut, two full pierced cheeks, complete finite stop and one continuous headed square pin provide explicit finite desktop-ground contacts with the complete lower frame edge. Three actual square through-bores retain complete walls and nonbearing air corridors; all finite contacts and whole empty/material domains require actual-geometry acceptance. Metres, native Z up, horizontal bounds-centred ground origin. Four opaque unlinked constant Principled PBR colours, no texture nodes. Existing easel canvas, true mirror ring and comb frame are acknowledged, never imported or converted. No painting, design, glass, mirror, table, wall, extra variant or artwork. Visual static display only: no standard canvas or easel fit, conservation, moisture/light protection, folding, load, anti-tip, material, manufacture or safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];NONCONTACT_SURFACES=[]
PALETTE=[('DeepBlueFrame',(.045,.105,.14,1),.57,.06),('MutedWarmBacking',(.39,.27,.17,1),.72,0),('WarmBlankPanel',(.78,.72,.59,1),.82,0),('SatinBrassPin',(.50,.34,.12,1),.40,.38)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),12) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
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
  p=tuple(round(x,12) for x in p)
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
  p=tuple(round(float(x),12) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  if len(ids)==3:self.f.append(tuple(ids));self.fm.append(mat);self.tags.append(tag);return
  if len(ids)==4 and all(sum(q*q for q in cross(sub(points[j],points[i]),sub(points[k],points[i])))>1e-22 for i,j,k in [(0,1,2),(0,2,3)]):
   for f in [(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])]:self.f.append(f);self.fm.append(mat);self.tags.append(tag)
   return
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
 outer=[tuple(round(c,12) for c in p) for p in outer];holes=[[tuple(round(c,12) for c in p) for p in h] for h in holes]
 loops=[outer]+holes;levels=sorted(set(round(p[1],12) for loop in loops for p in loop));m=Mesh()
 segs=[(a,b,k) for k,loop in enumerate(loops) for a,b in zip(loop,loop[1:]+loop[:1])]
 def hit(a,b,z):return a[0]+(b[0]-a[0])*(z-a[1])/(b[1]-a[1])
 cuts={}
 for z in levels:
  yy=[]
  for a,b,k in segs:
   if min(a[1],b[1])-1e-8<=z<=max(a[1],b[1])+1e-8:
    yy.extend([a[0],b[0]] if abs(a[1]-b[1])<1e-8 else [hit(a,b,z)])
  cuts[z]=sorted(set(round(y,12) for y in yy))
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
   z=round(a[1],12);ys=[a[0]]+[y for y in cuts[z] if min(a[0],b[0])+1e-8<y<max(a[0],b[0])-1e-8]+[b[0]];ys=sorted(ys);pp=[(y,z) for y in ys]
  else:
   zs=sorted([a[1]]+[z for z in levels if min(a[1],b[1])+1e-8<z<max(a[1],b[1])-1e-8]+[b[1]]);pp=[(hit(a,b,z),z) for z in zs]
  for p,q in zip(pp,pp[1:]):m.face([(x0,*p),(x1,*p),(x1,*q),(x0,*q)],mat,'outer_wall' if k==0 else 'hole_wall_'+str(k))
 return m.result(role,mat)
def box_geometry(lo,hi,mat=0,role='complete finite rectangular prism'):
 return extrude_region(rect(lo[1],hi[1],lo[2],hi[2]),[],lo[0],hi[0],mat,role)
def yz_prism(poly,x0,x1,mat=0,role=''):
 return prism(poly,x0,x1,mat,role,lambda p:(p[2],p[0],p[1]))
def xy_region(outer,holes,z0,z1,mat=0,role=''):
 g=extrude_region(outer,holes,z0,z1,mat,role)
 g['vertices']=[(y,z,x) for x,y,z in g['vertices']]
 return g

def offset_convex(poly,amount):
 # CCW polygon offset inward by an exact distance from every finite side.
 rows=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length);rows.append((n,n[0]*a[0]+n[1]*a[1]+amount))
 out=[]
 for (a,da),(b,db) in zip(rows[-1:]+rows[:-1],rows):
  det=a[0]*b[1]-a[1]*b[0];out.append(((da*b[1]-a[1]*db)/det,(a[0]*db-da*b[0])/det))
 return out

def area2(poly):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2

def inset_polygon(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 out=[]
 for i,p in enumerate(poly):
  a=poly[i-1];b=poly[(i+1)%len(poly)];u=(p[0]-a[0],p[1]-a[1]);v=(b[0]-p[0],b[1]-p[1]);lu=math.hypot(*u);lv=math.hypot(*v);n1=(-u[1]/lu,u[0]/lu);n2=(-v[1]/lv,v[0]/lv);den=1+dot(n1,n2);assert den>.001
  out.append((p[0]+d*(n1[0]+n2[0])/den,p[1]+d*(n1[1]+n2[1])/den))
 return out

def octagon(x0,x1,y0,y1,c):return [(x0+c,y0),(x1-c,y0),(x1,y0+c),(x1,y1-c),(x1-c,y1),(x0+c,y1),(x0,y1-c),(x0,y0+c)]
# A fresh horizontal frame, not a reshaped old mirror. Coordinates below are
# design-space metres; the one final translation centers its ground bounds.
FRAME='ContinuousDeepFrame';BACK='CompleteRearBoard';PANEL='BlankFloatingDisplayPanel';LEG='PiercedFixedRearStrut';PIN='ContinuousHeadedSquarePin';STOP='FiniteRearStrutStop';BODY=FRAME
SHIFT=(0,.105,0)
def xz_region(outer,holes,y0,y1,mat=0,role=''):
 g=extrude_region(outer,holes,y0,y1,mat,role);g['vertices']=[(y,x,z) for x,y,z in g['vertices']];g['faces']=[tuple(reversed(f)) for f in g['faces']];return g
G[FRAME]=xz_region(rect(-.38,.38,0,.50),[rect(-.335,.335,.045,.455)],-.05,.04,0,'One closed connected full-depth rectangular annulus; four uninterrupted 45 mm walls, full 90 mm depth and continuous corners.')
G[BACK]=box_geometry((-.38,.04,0),(.38,.058,.50),1,'Complete 18 mm rear board; entire frame-back ring contact and full ground edge.')
G[PANEL]=box_geometry((-.305,-.022,.075),(.305,-.010,.425),2,'One unpatterned 12 mm display panel, front recessed 28 mm; all four edges separated from frame by 30 mm true air.')
contact('WholeFrameRearRingToBoard',FRAME,BACK,(0,1,0),(0,.04,.0225),.105299,points=[(-.357,.04,.25),(.357,.04,.25),(0,.04,.0225),(0,.04,.4775)])
SPACERS=[]
for x,labelx in [(-.24,'Left'),(.24,'Right')]:
 for z,labelz in [(.13,'Lower'),(.37,'Upper')]:
  n='FiniteRearSpacer'+labelx+labelz;SPACERS.append(n);G[n]=box_geometry((x-.02,-.010,z-.02),(x+.02,.04,z+.02),1,'Finite complete 40 by 40 mm spacer with 50 mm depth; full opposed seats on panel and rear board.')
  contact(n+'WholeRearSeat',n,BACK,(0,1,0),(x,.04,z),.001599)
  contact(n+'WholePanelSeat',PANEL,n,(0,1,0),(x,-.010,z),.001599)
  solid(n+'WholeMaterial',box_geometry((x-.019,-.009,z-.019),(x+.019,.039,z+.019)),[n],'Whole spacer material, 1 mm inward boundary margin.')
# Original fixed rear standing construction. Square bores are genuine full
# thickness openings. The fixed square pin is not a functional folding hinge.
HOLE=rect(.092,.112,.340,.360);CHEEKS=[]
for x0,x1,label in [(-.065,-.035,'Left'),(.035,.065,'Right')]:
 n='PiercedRearCheek'+label;CHEEKS.append(n);G[n]=extrude_region(rect(.058,.148,.30,.39),[HOLE],x0,x1,1,'Complete thick rear cheek with true 20 mm square through-hole, continuous four bore walls and full front root on rear board.')
 contact(n+'WholeBoardRoot',BACK,n,(0,1,0),((x0+x1)/2,.058,.345),.002699)
 solid(n+'WholePiercedMaterial',extrude_region(rect(.059,.147,.301,.389),[rect(.091,.113,.339,.361)],x0+.001,x1-.001),[n],'Entire connected pierced cheek material including all four bore walls, 1 mm margins.')
 ISOLATED_VOID_VOLUMES[n+'WholeTrueBore']=dict(extrude_region(rect(.093,.111,.341,.359),[],x0-.001,x1+.001),targets=[n],role='Whole finite isolated square bore including both mouth planes, 1 mm lateral margins; fixed pin is intentionally omitted only from this isolated-hole proof.')
STRUT_POLY=[(.20,0),(.26,0),(.138,.30),(.138,.39),(.078,.39),(.078,.30)]
G[LEG]=extrude_region(STRUT_POLY,[HOLE],-.03,.03,0,'One original continuous fixed inclined rear strut with wide finite horizontal foot and thick upper head pierced by a true square hole.')
G[STOP]=box_geometry((-.026,.058,.305),(.026,.078,.325),1,'Finite rear stop; complete front face on backboard and complete rear face against strut head.')
contact('RearStopWholeBoardRoot',BACK,STOP,(0,1,0),(0,.058,.315),.001039)
contact('RearStrutWholeFiniteStop',STOP,LEG,(0,1,0),(0,.078,.315),.001039)
G[PIN]=union_boxes([((-.075,.096,.340),(.065,.108,.352)),((.065,.086,.333),(.080,.118,.367))],3,'One closed headed square pin; complete shaft runs through all three actual square bores; lower bearing facets and finite head stop are real material.')
for n,x0,x1 in [(CHEEKS[0],-.065,-.035),(LEG,-.03,.03),(CHEEKS[1],.035,.065)]:
 contact(n+'WholePinFloorBearing',n,PIN,(0,0,1),((x0+x1)/2,.102,.340),((x1-x0)*.012)-.000001)
contact('PinHeadWholeRightCheekStop',CHEEKS[1],PIN,(1,0,0),(.065,.090,.350),.000687,points=[(.065,.090,.350),(.065,.116,.350),(.065,.102,.365)])
FEET=[FRAME,BACK,LEG]
FOOT_CONTACTS=[{'name':'WholeFrameLowerGroundEdge','mesh':FRAME,'x':0,'y':-.005,'fixture_lo':[-.381,-.051,-.02],'fixture_hi':[.381,.041,0],'minimum_area_m2':.068399},
 {'name':'WholeRearBoardGroundEdge','mesh':BACK,'x':0,'y':.049,'fixture_lo':[-.381,.039,-.02],'fixture_hi':[.381,.059,0],'minimum_area_m2':.013679},
 {'name':'WholeRearStrutFoot','mesh':LEG,'x':0,'y':.23,'fixture_lo':[-.031,.199,-.02],'fixture_hi':[.031,.261,0],'minimum_area_m2':.003599}]
# Whole closed finite empty domains, not darkness, center rays or AABBs.
air('WholeFourSideShadowGapAndAllCorners',xz_region(rect(-.334,.334,.046,.454),[rect(-.306,.306,.074,.426)],-.049,.039),'Complete four-sided shadow-gap volume and all four corners through full frame depth, with 1 mm boundary margins.',list(G))
seat_holes=[rect(x-.021,x+.021,z-.021,z+.021) for x in [-.24,.24] for z in [.13,.37]]
air('WholePanelToRearBoardAirExceptFourSeats',xz_region(rect(-.304,.304,.076,.424),seat_holes,-.009,.039),'Entire connected volume behind the thick display panel and before the rear board except four complete finite spacer volumes; 1 mm margins.',list(G))
air('WholeFrontRecessAir',box_geometry((-.304,-.049,.076),(.304,-.023,.424)),'Entire clear 28 mm front recess, 1 mm from actual front frame datum and display face.',list(G))
air('WholeLowerRearStrutAir',extrude_region([(.059,.001),(.1985,.001),(.0778,.298),(.059,.298)],[],-.029,.029),'Complete finite lower triangular rear air space between rear board and fixed strut; 1 mm boundary margins.',list(G))
for side,x0,x1 in [('Left',-.034,-.031),('Right',.031,.034)]:
 air(side+'WholeStrutCheekSideAir',extrude_region(rect(.059,.147,.301,.389),[rect(.095,.109,.339,.353)],x0,x1),'Whole 5 mm side separation between rear strut and cheek except the complete crossing pin shaft, with 1 mm insets.',list(G))
for name,lo,hi in [('Front',(-.064,.093,.341),(.064,.095,.359)),('Back',(-.064,.109,.341),(.064,.111,.359)),('Above',(-.064,.095,.353),(.064,.109,.359))]:
 air('WholeNonbearingPinAir'+name,box_geometry(lo,hi),'Full-length nonbearing bore air corridor around complete pin; bearing-floor/head edge boundaries deliberately excluded by 1 mm insets.',list(G))
ISOLATED_VOID_VOLUMES[LEG+'WholeTrueBore']=dict(extrude_region(rect(.093,.111,.341,.359),[],-.031,.031),targets=[LEG],role='Complete isolated square bore through fixed rear strut, including both mouth planes; pin intentionally omitted only from isolated-hole proof.')
solid('WholeDeepFrameMaterialAndCorners',xz_region(rect(-.379,.379,.001,.499),[rect(-.336,.336,.044,.456)],-.049,.039),[FRAME],'Whole continuous full-depth four-wall annular material and all complete corners, 1 mm inward margins.')
solid('WholeRearBoardMaterial',box_geometry((-.379,.041,.001),(.379,.057,.499)),[BACK],'Entire thick backboard material, 1 mm margins.')
solid('WholeBlankDisplayPanelMaterial',box_geometry((-.304,-.021,.076),(.304,-.011,.424)),[PANEL],'Entire thick unpatterned display panel, 1 mm margins.')
solid('WholePiercedStrutMaterial',extrude_region(inset_polygon(STRUT_POLY,.001),[rect(.091,.113,.339,.361)],-.029,.029),[LEG],'Entire continuous inclined strut, foot and all four bore walls, 1 mm inward material margins.')
solid('WholeRearStopMaterial',box_geometry((-.025,.059,.306),(.025,.077,.324)),[STOP],'Entire finite stop material, 1 mm margins.')
solid('WholeContinuousHeadedPinMaterial',union_boxes([((-.074,.097,.341),(.066,.107,.351)),((.066,.087,.334),(.079,.117,.366))]),[PIN],'Entire connected shaft and head material including full shaft-to-head root, 1 mm margins.')
# Center the exported prop's actual horizontal bounds without moving datum Z=0.
for group in [G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in group.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['plane_m']-=dot(r['axis'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['y']-=SHIFT[1];r['fixture_lo']=sub(r['fixture_lo'],SHIFT);r['fixture_hi']=sub(r['fixture_hi'],SHIFT)
CONTRACT={'single_prop_count':1,'frame_forms_completed':1,'original_plural_family_complete':False,'closed_meshes':len(G),'frame_wall_depth_m':.09,'frame_side_width_m':.045,'backboard_thickness_m':.018,'panel_thickness_m':.012,'four_side_gap_m':.03,'panel_front_recess_m':.028,'panel_rear_air_depth_m':.05,'full_finite_spacers':4,'rear_true_bore_count':3,'square_bore_size_m':.020,'pin_shaft_section_m':[.012,.012],'minimum_nonbearing_front_back_pin_clearance_m':.004,'top_pin_clearance_m':.008,'strut_cheek_side_clearance_m':.005,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'folding_load_or_safety_claim':False}
def measure_float_frame_geometry(vertices):
 assert set(vertices)==set(G)
 for name in G:
  for k in range(3):
   assert abs(min(p[k] for p in vertices[name])-min(p[k] for p in G[name]['vertices']))<2e-7 and abs(max(p[k] for p in vertices[name])-max(p[k] for p in G[name]['vertices']))<2e-7,(name,k)
 return dict(CONTRACT,geometry_scope='actual component extrema plus independent entire finite contact, whole empty/material and self-intersection predicates required')
INSIDE_TESTS=[(FRAME,sub((.36,0,.25),SHIFT),sub((0,0,.25),SHIFT)),(LEG,sub((0,.11,.375),SHIFT),sub((0,.102,.350),SHIFT))]
FOCUS=(0,-.06,.25);ORTHO=1.0
CAMERAS={'gray-front3q':(2.5,-4,2.4),'gray-back3q':(-2.5,4,2.4),'thumbnail':(2.5,-4,2.4),'qa-front':(0,-5,1.25),'qa-side':(5,0,1.5),'qa-top':(0,0,6),'qa-back':(0,5,1.25),'qa-wireframe':(2.5,-4,2.4),'silhouette-128-front':(0,-5,1.25),'silhouette-128-side':(5,0,1.5)}
WIRE_THICKNESS=ORTHO/1500
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
root=bpy.data.objects.new('OneDeepFloatingPanelFrame',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontal bounds centre at ground Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_float_frame_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'float_frame_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
