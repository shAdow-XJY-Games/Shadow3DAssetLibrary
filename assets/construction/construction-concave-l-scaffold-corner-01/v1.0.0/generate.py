"""Original continuous concave-L scaffold corner. One static modular visual asset."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='construction-concave-l-scaffold-corner-01';VERSION='1.0.0';TITLE='Concave-L Scaffold Corner'
DESCRIPTION=('One newly authored continuous concave-L thick deck, complete L open underframe, six finite flat feet and posts, two fully cut-end diagonal braces and a separate original outer L railing. One static modular visual asset, metres and native Z up, ground corner origin (0,0,0). The 60 mm continuous L deck has two orthogonal 0.90 m ports at X=1.39 and Y=1.39, and a 1.02 m top. All internal support/root joints are full finite opposed faces, never hidden penetration. Three opaque unlinked constant Principled PBR materials. The only neighboring placements in scope use the untouched pinned construction-scaffold-01 at centres (2.095,0.45,0), rotation 0, and (0.45,2.095,0), rotation 90 degrees, simultaneously, with a nominal 10 mm deck joint. Every original old end guard, post, brace and foot remains; those guards obstruct passage. These are separated independently railed units in a corner arrangement, never a connected walkway or seamless platform. Old copies exist only for QA and are not exported. Neither two overlapping straight decks nor rotated/coloured copies of an old stage. No connected passage, pedestrian route, scaffold installation standard, load, stability, tipping resistance, fall protection, construction use, human suitability, manufacture, navigation, collision or safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];POSTS=[];FOOT_CONTACTS=[]
BODY='ContinuousConcaveLOpenUnderframe';DECK='ContinuousConcaveLThickDeck';BRACES=[];RAILPOSTS=[]
PALETTE=[('WarmTimberDeck',(.52,.31,.13,1),.78,0),('IndustrialTealFrame',(.12,.25,.24,1),.63,.18),('GraphiteFlatFeet',(.065,.084,.084,1),.77,.10)]
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

# All numerical shape work below is original. Generic mesh/output helpers only
# are reused. No fixed generator is executed or imported by this asset.
def lshape(lo,hi,inner):return [(lo,lo),(hi,lo),(hi,inner),(inner,inner),(inner,hi),(lo,hi)]
def sq(x,y,h):return rect(x-h,x+h,y-h,y+h)
def addbox(name,lo,hi,mat,role):
 G[name]=box(lo,hi,mat,role);solid(name+'_CompleteMaterial',box(tuple(v+.001 for v in lo),tuple(v-.001 for v in hi)),[name],'Whole finite box material, every face and full height/length; 1 mm inset.')
OUTLINE=lshape(0.,1.39,.90);FRAME_OUTER=lshape(.06,1.33,.84);FRAME_INNER=lshape(.14,1.25,.76)
G[DECK]=xy_region(OUTLINE,[],.96,1.02,0,'One continuous closed 60 mm concave-L deck, full inner corner and two complete orthogonal planar ports. No overlapping panels.')
G[BODY]=xy_region(FRAME_OUTER,[FRAME_INNER],.88,.96,1,'One original connected 80 mm-thick L-perimeter ring with complete L aperture and all six corners; finite full ring top seat.')
solid('WholeContinuousLDeckMaterial',xy_region(lshape(.001,1.389,.899),[],.961,1.019),[DECK],'Whole connected thick concave-L solid including its entire inner bridge, both arms and both end faces, 1 mm inset.')
solid('WholeContinuousLFrameMaterial',xy_region(lshape(.061,1.329,.839),[lshape(.139,1.251,.761)],.881,.959),[BODY],'Complete connected ring material around every outer/inner L facet and corner; 1 mm inset.')
FRAME_AREA=(1.27*1.27-.49*.49)-(1.11*1.11-.49*.49)
contact('WholeLFrameTopSeat',BODY,DECK,(0,0,1),(.10,.45,.96),FRAME_AREA-1e-7,points=[(.10,.45,.96),(.45,.10,.96),(.80,1.05,.96),(1.05,.80,.96)])
CENTRES=[(.10,.10),(1.29,.10),(1.29,.80),(.80,.80),(.80,1.29),(.10,1.29)]
for i,(x,y) in enumerate(CENTRES,1):
 foot=f'FlatGroundFoot_{i}';post=f'CompleteSupportPost_{i}'
 addbox(foot,(x-.06,y-.06,0),(x+.06,y+.06,.06),2,'Complete 120 mm square finite flat foot, 60 mm thick, full top post seat and full ground sole.');FEET.append(foot)
 addbox(post,(x-.03,y-.03,.06),(x+.03,y+.03,.88),1,'Complete square 60 mm upright between exact finite foot/frame seats.');POSTS.append(post)
 contact(foot+'_WholePostSeat',foot,post,(0,0,1),(x,y,.06),.0035999)
 contact(post+'_WholeFrameSeat',post,BODY,(0,0,1),(x,y,.88),.0035999)
 FOOT_CONTACTS.append({'name':foot+'_WholeGroundSole','mesh':foot,'x':x,'y':y,'half_x':.06,'half_y':.06,'minimum_area_m2':.0143999})
# Vertical cut ends remain whole finite rectangles. The pair of braces is on
# orthogonal outside faces, not crossing or penetrating the inner aperture.
SLOPE=.51/1.13
def brace_low(x):return .19+(x-.13)*SLOPE
BRACE_PROFILE=[(.13,.19),(1.26,.70),(1.26,.76),(.13,.25)]
for axis in [0,1]:
 name='OrthogonalCutEndBrace_'+str(axis+1);transform=(lambda p:(p[0],p[2],p[1])) if axis==0 else (lambda p:(p[2],p[0],p[1]))
 G[name]=prism(BRACE_PROFILE,.075,.125,1,'Full solid diagonal with exact vertical-cut finite ends seated against two complete posts.',transform);BRACES.append(name)
 inner=[(.131,brace_low(.131)+.0012),(1.259,brace_low(1.259)+.0012),(1.259,brace_low(1.259)+.0588),(.131,brace_low(.131)+.0588)]
 solid(name+'_CompleteMaterial',prism(inner,.076,.124,transform=transform),[name],'Entire diagonal body inset along both slopes, both cut ends and both side faces.')
 vec=(1,0,0) if axis==0 else (0,1,0);a=(.13,.10,.22) if axis==0 else (.10,.13,.22);b=(1.26,.10,.73) if axis==0 else (.10,1.26,.73);far=POSTS[1] if axis==0 else POSTS[5]
 contact(name+'_WholeNearCutEnd',POSTS[0],name,vec,a,.0029999)
 contact(name+'_WholeFarCutEnd',name,far,vec,b,.0029999)
for i,(x,y) in enumerate([CENTRES[0],CENTRES[1],CENTRES[5]],1):
 name='OuterRailStanchion_'+str(i);addbox(name,(x-.03,y-.03,1.02),(x+.03,y+.03,1.78),1,'Whole original outer rail post, finite full base on deck and top below L cap.');RAILPOSTS.append(name)
 contact(name+'_WholeDeckSeat',DECK,name,(0,0,1),(x,y,1.02),.0035999)
CAP='ContinuousOuterLRailCap';CAP_OUTLINE=lshape(.07,1.32,.13)
G[CAP]=xy_region(CAP_OUTLINE,[],1.78,1.83,1,'One continuous original outer L top rail with a true corner and three whole finite post seats.')
solid('WholeContinuousLRailCapMaterial',xy_region(lshape(.071,1.319,.129),[],1.781,1.829),[CAP],'Whole L top rail material including continuous corner, all ends and full thickness.')
for i,(x,y) in enumerate([CENTRES[0],CENTRES[1],CENTRES[5]]):contact(RAILPOSTS[i]+'_WholeCapSeat',RAILPOSTS[i],CAP,(0,0,1),(x,y,1.78),.0035999)
for axis in [0,1]:
 name='OuterMiddleRail_'+str(axis+1)
 lo=(.13,.075,1.43) if axis==0 else (.075,.13,1.43);hi=(1.26,.125,1.48) if axis==0 else (.125,1.26,1.48)
 addbox(name,lo,hi,1,'Complete finite straight intermediate rail between separate stanchions; exactly cut at both post side faces.')
 vec=(1,0,0) if axis==0 else (0,1,0);a=(.13,.10,1.455) if axis==0 else (.10,.13,1.455);b=(1.26,.10,1.455) if axis==0 else (.10,1.26,1.455)
 contact(name+'_WholeNearEnd',RAILPOSTS[0],name,vec,a,.0024999)
 contact(name+'_WholeFarEnd',name,RAILPOSTS[axis+1],vec,b,.0024999)
# Complete functional air, partitioned only at actual material change heights
# and brace strip boundaries. Adjacent partitions meet at common artificial
# faces; 1 mm exclusions occur only at physical boundaries/change heights.
INSET=lshape(.001,1.389,.899)
air('WholeLConcaveNotch',box((.901,.901,.001),(1.389,1.389,1.829)),'Entire concave notch across full model height, no hidden corner filling.')
air('WholeFootLevelAir',xy_region(INSET,[sq(x,y,.061) for x,y in CENTRES],.001,.059),'Complete L footprint at foot level around all six entire expanded foot boundaries.')
air('WholeCentralUnderdeckAir',xy_region([(.131,.131),(1.389,.131),(1.389,.899),(.899,.899),(.899,1.389),(.131,1.389)],[sq(x,y,.031) for x,y in CENTRES[2:5]],.061,.879),'Entire central L underdeck volume, including far arms and full three internal upright exclusions.')
air('WholeOuterXStripUnderdeckAir',box((.001,.001,.061),(.069,1.389,.879)),'Complete outside strip alongside the whole X=0 side.')
air('WholeOuterYStripUnderdeckAir',box((.069,.001,.061),(1.389,.069,.879)),'Complete outside strip alongside Y=0, joined exactly to X strip.')
air('WholeFarXTipUnderdeckAir',box((1.321,.069,.061),(1.389,.131,.879)),'Complete air beyond far X-end post, before the deck port.')
air('WholeFarYTipUnderdeckAir',box((.069,1.321,.061),(.131,1.389,.879)),'Complete air beyond far Y-end post, before the deck port.')
for axis in [0,1]:
 transform=(lambda p:(p[0],p[2],p[1])) if axis==0 else (lambda p:(p[2],p[0],p[1]))
 low=[(.131,.061),(1.259,.061),(1.259,brace_low(1.259)-.0012),(.131,brace_low(.131)-.0012)]
 high=[(.131,brace_low(.131)+.0612),(1.259,brace_low(1.259)+.0612),(1.259,.879),(.131,.879)]
 for y0,y1,label in [(.069,.074,'OutsideSide'),(.126,.131,'InsideSide')]:
  air('Whole'+label+'Diagonal'+str(axis+1),prism([(.131,.061),(1.259,.061),(1.259,.879),(.131,.879)],y0,y1,transform=transform),'Whole finite side gap alongside the entire brace strip; joins the outside/central domains and overlaps the above/below domains.')
 for label,poly in [('Below',low),('Above',high)]:air('Whole'+label+'Diagonal'+str(axis+1),prism(poly,.069,.131,transform=transform),'Entire orthogonal brace-strip free volume '+label.lower()+' the full inclined facet, including both cut-end directions, 1 mm physical margin.')
air('WholeLFrameAperture',xy_region(lshape(.141,1.249,.759),[],.881,.959),'Entire real L underframe aperture through full frame thickness.')
air('WholeOuterFrameLevelAir',xy_region(INSET,[lshape(.059,1.331,.841)],.881,.959),'Entire outer underframe overhang air, including full concave elbow and both terminal mouths.')
for label,z0,z1 in [('BelowMiddleRails',1.021,1.429),('AboveMiddleRails',1.481,1.779)]:
 air('WholeAboveDeck'+label,xy_region(INSET,[sq(x,y,.031) for x,y in [CENTRES[0],CENTRES[1],CENTRES[5]]],z0,z1),'Entire above-deck L free region around all three posts, '+label+', with every outer/inner boundary.')
MIDDLE_ENVELOPE=[(.069,.069),(.131,.069),(.131,.074),(1.259,.074),(1.259,.069),(1.321,.069),(1.321,.131),(1.259,.131),(1.259,.126),(.131,.126),(.131,.131),(.126,.131),(.126,1.259),(.131,1.259),(.131,1.321),(.069,1.321),(.069,1.259),(.074,1.259),(.074,.131),(.069,.131)]
for label,z0,z1 in [('MiddleRailLevel',1.431,1.479),('TopRailLevel',1.781,1.829)]:
 air('WholeAboveDeck'+label,xy_region(INSET,[MIDDLE_ENVELOPE if label=='MiddleRailLevel' else lshape(.069,1.321,.131)],z0,z1),'Entire L above-deck free region outside continuous rail-level material envelope; complete L rail corner and both ends.')
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
CONTRACT={'single_modular_count':1,'deck_outline_xy_m':OUTLINE,'orthogonal_port_lengths_m':[.9,.9],'deck_thickness_m':.06,'deck_top_m':1.02,'underframe_thickness_m':.08,'continuous_frame_apertures':1,'support_posts':6,'flat_ground_feet':6,'outer_stanchions':3,'whole_diagonal_braces':2,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'nominal_old_deck_end_gap_m':.01,'qa_only_old_scaffold_placements':[{'centre_m':[2.095,.45,0],'rotation_z_degrees':0},{'centre_m':[.45,2.095,0],'rotation_z_degrees':90}],'exported_neighbor_count':0,'old_end_guards_retained':True,'connected_passage_or_load_or_safety_claim':False}
def measure_scaffold_corner_geometry(vertices):
 assert set(vertices)==set(G)
 vv=vertices[DECK]
 assert abs(max(p[2] for p in vv)-1.02)<2e-7 and abs(min(p[2] for p in vv)-.96)<2e-7
 for axis in [0,1]:assert abs(min(p[axis] for p in vv))<2e-7 and abs(max(p[axis] for p in vv)-1.39)<2e-7
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 return dict(CONTRACT,geometry_scope='one original exported concave-L scaffold corner; actual full triangles, full domains, complete faces and fixed old units require separate independent acceptance')
INSIDE_TESTS=[(DECK,(.6,.6,.99),(1.1,1.1,.99)),(BODY,(.10,.45,.92),(.45,.45,.92))]
FOCUS=(.695,.695,.915);ORTHO=2.8
CAMERAS={'gray-front3q':(3.9,4.6,3.1),'gray-back3q':(-3.5,-4.2,3.1),'thumbnail':(3.9,4.6,3.1),'qa-front':(.695,-5,2.2),'qa-side':(5,.695,2.2),'qa-top':(.695,.695,6),'qa-back':(.695,5,2.2),'qa-wireframe':(3.9,4.6,3.1),'silhouette-128-front':(.695,-5,2.2),'silhouette-128-side':(5,.695,2.2)}
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
root=bpy.data.objects.new('OneConcaveLScaffoldCorner',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='outer ground corner; deck ports at X=1.39 and Y=1.39';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_scaffold_corner_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'scaffold_corner_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
