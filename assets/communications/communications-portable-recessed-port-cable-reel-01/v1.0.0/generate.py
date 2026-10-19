"""Original portable recessed-port cable reel. One fixed static visual prop."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-portable-recessed-port-cable-reel-01';VERSION='1.0.0';TITLE='Portable Recessed-Port Cable Reel'
DESCRIPTION=('One original static visual prop: one whole rear carry frame on two long ground shoes, one fixed short horizontal axle, one integral double-flange drum whose thick front body forms a real recessed face and three original nonstandard blind cavities, one connected capped cable winding four separated axial turns with its inner end fixed on a distinct drum seat, and one solid no-pin tail head parked by a complete flat base on an independently open side tray. Metres, native Z up, front -Y, ground origin at horizontal envelope centre. Five opaque constant unlinked Principled PBR materials. All numerical geometry newly authored; no old model or shape-generation code imported. No electrical, communication, power, signal, grounding, insulation, ingress, compatibility, rotating, winding, plugging, handling, strength, stability, manufacturing or safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
PALETTE=[('DeepTealCarryFrame',(.065,.235,.255,1),.63,.12),('OchreIvoryDrum',(.67,.49,.255,1),.65,.08),('GraphiteContinuousCable',(.045,.060,.062,1),.78,0),('TerracottaTail',(.48,.19,.095,1),.67,0),('PewterFixedAxle',(.27,.33,.34,1),.49,.35)]
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

# All numerical geometry and layered/sweep assembly below are original.
# Fixed comparison generators are read-only provenance, never runtime inputs.
def poly(cx,cz,r,n=24,phase=0):return [(cx+r*math.cos(phase+math.tau*i/n),cz+r*math.sin(phase+math.tau*i/n)) for i in range(n)]
def xz_region(outer,holes,y0,y1,mat=0,role=''):
 g=extrude_region(outer,holes,y0,y1,mat,role);g['vertices']=[(y,x,z) for x,y,z in g['vertices']];g['faces']=[tuple(reversed(f)) for f in g['faces']];return g

def layered_regions(layers,mat=1,role=''):
 # Original connected drum boundary. Recess, blind floors, core and both rims
 # share a conforming boundary arrangement; no stacked solid disks or booleans.
 outer=layers[0][2];bowl=layers[0][3][0];ports=layers[1][3];core=layers[3][2]
 loops=[outer,bowl,core]+ports;segs=[(a,b) for p in loops for a,b in zip(p,p[1:]+p[:1])]
 levels=sorted(set(round(p[1],9) for loop in loops for p in loop));m=Mesh()
 def hit(a,b,z):return a[0]+(b[0]-a[0])*(z-a[1])/(b[1]-a[1])
 cuts={}
 for z in levels:
  xx=[]
  for a,b in segs:
   if min(a[1],b[1])-1e-8<=z<=max(a[1],b[1])+1e-8:xx.extend([a[0],b[0]] if abs(a[1]-b[1])<1e-9 else [hit(a,b,z)])
  xx=sorted(set(round(x,9) for x in xx));cuts[z]=[x for i,x in enumerate(xx) if i==0 or x-xx[i-1]>1e-7]
 def surface(outer,holes,y):
  edges=[(a,b) for loop in [outer]+holes for a,b in zip(loop,loop[1:]+loop[:1])]
  for z0,z1 in zip(levels,levels[1:]):
   zm=(z0+z1)/2;active=sorted((hit(a,b,zm),a,b) for a,b in edges if min(a[1],b[1])<zm<max(a[1],b[1]))
   for left,right in zip(active,active[1:]):
    if not inside2(((left[0]+right[0])/2,zm),outer) or any(inside2(((left[0]+right[0])/2,zm),h) for h in holes):continue
    l0,l1=hit(left[1],left[2],z0),hit(left[1],left[2],z1);r0,r1=hit(right[1],right[2],z0),hit(right[1],right[2],z1)
    l0,r0=[min(cuts[z0],key=lambda x:abs(x-q)) for q in [l0,r0]];l1,r1=[min(cuts[z1],key=lambda x:abs(x-q)) for q in [l1,r1]]
    pp=[(l0,z0)]+[(x,z0) for x in cuts[z0] if l0+1e-8<x<r0-1e-8]+[(r0,z0),(r1,z1)]+[(x,z1) for x in reversed(cuts[z1]) if l1+1e-8<x<r1-1e-8]+[(l1,z1)]
    clean=[]
    for p in pp:
     if not clean or math.dist(p,clean[-1])>1e-8:clean.append(p)
    if math.dist(clean[0],clean[-1])<1e-8:clean.pop()
    m.face([(x,y,z) for x,z in clean],mat)
 def wall(loop,y0,y1):
  for a,b in zip(loop,loop[1:]+loop[:1]):
   if abs(a[1]-b[1])<1e-9:
    z=round(a[1],9);pp=[(x,z) for x in sorted([a[0],b[0]]+[x for x in cuts[z] if min(a[0],b[0])+1e-8<x<max(a[0],b[0])-1e-8])]
   else:
    zz=sorted([a[1],b[1]]+[z for z in levels if min(a[1],b[1])+1e-8<z<max(a[1],b[1])-1e-8]);pp=[(min(cuts[round(z,9)],key=lambda x:abs(x-hit(a,b,z))),z) for z in zz]
   for (x0,z0),(x1,z1) in zip(pp,pp[1:]):m.face([(x0,y0,z0),(x1,y0,z1),(x1,y1,z1),(x0,y1,z0)],mat)
 surface(outer,[bowl],-.25);surface(bowl,ports,-.215)
 for p in ports:surface(p,[],-.155);wall(p,-.215,-.155)
 surface(outer,[core],-.13);surface(outer,[core],.13);surface(outer,[],.17)
 wall(outer,-.25,-.13);wall(bowl,-.25,-.215);wall(core,-.13,.13);wall(outer,.13,.17)
 return m.result(role,mat)

def sweep(path,r,sides=10,mat=2,role=''):
 # Parallel frames use the outward radial guide for the helix and transport
 # it into the tail. Every ring shares vertices; only the two ends are capped.
 vv=[];ff=[];last=None
 for i,p in enumerate(path):
  tangent=unit(sub(path[min(i+1,len(path)-1)],path[max(i-1,0)]))
  guide=(1,0,0) if last is None else last
  u=sub(guide,mul(tangent,dot(guide,tangent)))
  if dot(u,u)<1e-8:u=cross(tangent,(0,1,0))
  u=unit(u);v=cross(tangent,u);last=u
  vv.extend(add(p,add(mul(u,r*math.cos(math.tau*j/sides)),mul(v,r*math.sin(math.tau*j/sides)))) for j in range(sides))
 for i in range(len(path)-1):
  for j in range(sides):
   k=(j+1)%sides;a=i*sides+j;b=i*sides+k;c=(i+1)*sides+k;d=(i+1)*sides+j;ff.extend([(a,b,c),(a,c,d)])
 ff.extend([tuple(reversed(range(sides))),tuple((len(path)-1)*sides+j for j in range(sides))])
 return mesh(vv,ff,mat,role)
def bezier(a,b,c,d,steps):
 return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in range(3)) for t in [i/steps for i in range(1,steps+1)]]

CZ=.63
FRAME_OUTER=[(-.47,.06),(.47,.06),(.47,1.06),(.39,1.22),(.32,1.29),(-.32,1.29),(-.39,1.22),(-.47,1.06)]
FRAME_LOWER=[(-.38,.16),(.38,.16),(.38,.56),(-.38,.56)]
FRAME_UPPER=[(-.38,.70),(.38,.70),(.38,1.04),(.32,1.16),(-.32,1.16),(-.38,1.04)]
FRAME='WholeContinuousCarryFrame';DRUM='IntegralRecessedThreePortDrum';CABLE='OneContinuousFourTurnCable';AXLE='FixedHorizontalAxle';SEAT='InnerCableEndSeat';TRAY='OpenSideTailTray';TAIL='SolidParkedTailHead'
G[FRAME]=xz_region(FRAME_OUTER,[FRAME_LOWER,FRAME_UPPER],.27,.35,0,'One continuous frame with integral lower tie, bearing crossbridge and upper carry bridge; both true apertures are full thickness.')
solid('Frame_CompleteMaterial',xz_region(offset_convex(FRAME_OUTER,.001),[offset_convex(p,-.001) for p in [FRAME_LOWER,FRAME_UPPER]],.271,.349),[FRAME],'Entire carry frame material with full feet roots, both stems, low tie, axle crossbridge and complete top carry bridge; uniform 1 mm surface margins.')
for label,x in [('Left',-.425),('Right',.425)]:
 name='LongGroundShoe_'+label;FEET.append(name);G[name]=box((x-.08,-.36,0),(x+.08,.36,.06),0,'One full long flat ground shoe and whole upper finite frame seat.')
 contact(name+'_FullFrameSeat',name,FRAME,(0,0,1),(x,.31,.06),.0100-1e-7)
 FOOT_CONTACTS.append({'name':name+'_WholeSole','mesh':name,'x':x,'y':0,'half_x':.08,'half_y':.36,'minimum_area_m2':.1152-1e-7})
 solid(name+'_CompleteMaterial',box((x-.079,-.359,.001),(x+.079,.359,.059)),[name],'Complete finite shoe material, uniformly inset 1 mm including both ends and all sole area.')
G[AXLE]=xz_region(poly(0,CZ,.048,12),[],.17,.27,4,'Complete fixed solid twelve-facet horizontal axle, finitely end-seated between one frame crossbridge and drum rear.')
contact('Axle_RearToFrame',AXLE,FRAME,(0,1,0),(0,.27,CZ),.006912-1e-7)
solid('Axle_CompleteMaterial',xz_region(poly(0,CZ,.0469,12),[],.171,.269),[AXLE],'Entire fixed axle including all twelve wall facets and both finite end sections.')
OUTER=poly(0,CZ,.36,24);BOWL=poly(0,CZ,.275,16);CORE=poly(0,CZ,.115,24)
PORTS=[[(x+.115,z+.718) for x,z in [(-.056,-.047),(.038,-.047),(.058,-.021),(.043,.048),(-.046,.048),(-.061,.015)]],[(x-.117,z+.713) for x,z in [(-.052,-.038),(.046,-.038),(.060,.013),(.027,.052),(-.034,.052),(-.057,.018)]],[(x,z+.510) for x,z in [(-.064,-.032),(.050,-.032),(.064,.015),(.041,.047),(-.048,.047),(-.066,.011)]]]
LAYERS=[(-.25,-.215,OUTER,[BOWL]),(-.215,-.155,OUTER,PORTS),(-.155,-.13,OUTER,[]),(-.13,.13,CORE,[]),(.13,.17,OUTER,[])]
G[DRUM]=layered_regions(LAYERS,1,'One complete connected double-flange drum; thick front flange contains one full face recess, three irregular blind cavities with actual back thickness, an integral winding core and rear flange. No overlay, separate dark caps or standard interfaces.')
contact('Drum_BackToAxle',DRUM,AXLE,(0,1,0),(0,.17,CZ),.006912-1e-7)
# Every complete slab and every material connection across slab seams is probed.
for i,(y0,y1,outer,holes) in enumerate(LAYERS):
 solid('Drum_WholeSlab_%d'%i,xz_region(offset_convex(outer,.001),[offset_convex(p,-.001) for p in holes],y0+.001,y1-.001),[DRUM],'Complete finite inward-offset material of layered drum slab %d, including all walls and full extent.'%i)
for i,(yy,outer,holes) in enumerate([(-.215,OUTER,[BOWL]),(-.155,OUTER,PORTS),(-.13,CORE,[]),(.13,CORE,[])]):
 solid('Drum_WholeLayerJoin_%d'%i,xz_region(offset_convex(outer,.001),[offset_convex(p,-.001) for p in holes],yy-.002,yy+.002),[DRUM],'Complete finite continuity material over this entire layer-to-layer join, including the actual complete stepped core roots.')
# A distinct full support seat fixes the inner cable cap to the front inner face.
G[SEAT]=box((.16,-.13,.575),(.22,-.07,.63),3,'Fixed original inner cable seat with a full rear face against the front flange and a complete top cable-end cap seat.')
contact('Seat_ToDrum',DRUM,SEAT,(0,1,0),(.19,-.13,.602),.0033-1e-7)
solid('Seat_CompleteMaterial',box((.161,-.129,.576),(.219,-.071,.629)),[SEAT],'Whole inner end seat including full front-drum root and flat upper end-cap seat.')
# Four turns wind axially between flanges; a slight increasing radius leaves
# the last end room to turn outward without crossing the previous turns.
TURNS=4;TURN_STEPS=40;CABLE_R=.017;PATH=[]
for i in range(TURNS*TURN_STEPS+1):
 t=i/(TURNS*TURN_STEPS);theta=math.tau*TURNS*t;r=.19+.028*(3*t*t-2*t*t*t);y=-.10+.20*t
 PATH.append((r*math.cos(theta),y,CZ+r*math.sin(theta)))
# Exactly vertical starting cap; adjust only the first forward station.
PATH[1]=(.19,-.10,CZ+.028)
# A tangent-led original tail exits between rims, then reaches the right tray.
a=PATH[-1];PATH+=bezier(a,(a[0],a[1],a[2]+.14),(.45,.10,.86),(.53,-.11,.72),20)
PATH+=bezier(PATH[-1],(.56,-.19,.69),(.56,-.19,.66),(.56,-.19,.62),8)
PATH +=[(.56,-.19,z) for z in [.60,.58,.56]]
G[CABLE]=sweep(PATH,CABLE_R,10,2,'One closed connected ten-sided continuous thick cable, exactly four complete axial turns, two and only two capped endpoints, and one smooth fixed parked tail.')
CABLE_INNER_PATH=list(PATH);CABLE_INNER_PATH[0]=add(PATH[0],(0,0,.001));CABLE_INNER_PATH[-1]=add(PATH[-1],(0,0,.001))
solid('Cable_WholeContinuousMaterial',sweep(CABLE_INNER_PATH,CABLE_R-.001,10),[CABLE],'Entire connected inward cable material over all four turns, every tail bend, and both fixed end sections; no selected loops or point-only test.')
contact('InnerCableCap_ToSeat',SEAT,CABLE,(0,0,1),PATH[0],5*CABLE_R*CABLE_R*math.sin(math.tau/10)-1e-7)
# One open-sided tray with a full side root to the frame and full bottom seat.
TRAY_BOXES=[((.47,.27,.43),(.64,.35,.46)),((.51,-.27,.43),(.64,.35,.46)),((.51,-.27,.46),(.525,-.125,.53)),((.61,-.27,.46),(.64,-.125,.53)),((.525,-.14,.46),(.61,-.125,.53))]
G[TRAY]=union_boxes(TRAY_BOXES,0,'One complete rooted side tray, continuous rear-to-front bottom shelf and two short side cheeks with a back lip; top/front opening remains real around parked tail.')
contact('Tray_WholeFrameRoot',FRAME,TRAY,(1,0,0),(.47,.31,.445),.0024-1e-7)
# Full tray body proved in all five material regions, including shared seams.
for i,(lo,hi) in enumerate(TRAY_BOXES):solid('Tray_WholeRegion_%d'%i,box(add(lo,(.001,.001,.001)),sub(hi,(.001,.001,.001))),[TRAY],'Complete inward-offset tray constituent material; full length/width/depth, no centre slice.')
for i,(lo,hi) in enumerate([((.511,.271,.431),(.639,.349,.459)),((.511,-.269,.458),(.524,-.141,.462)),((.611,-.269,.458),(.639,-.141,.462)),((.526,-.139,.458),(.609,-.126,.462))]):solid('Tray_FullJoin_%d'%i,box(lo,hi),[TRAY],'Whole finite material crossing a tray union boundary so no detached pieces can satisfy only slab checks.')
TAIL_POLY=[(.536,-.222),(.588,-.222),(.598,-.212),(.598,-.168),(.588,-.158),(.536,-.158),(.526,-.168),(.526,-.212)]
G[TAIL]=xy_region(TAIL_POLY,[],.46,.56,3,'Original solid chamfered parked cable-end head; no pins, no socket standard, no usable connector. Full flat bottom bears on the open tray.')
contact('Tail_FullBottomSeat',TRAY,TAIL,(0,0,1),(.56,-.19,.46),abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(TAIL_POLY,TAIL_POLY[1:]+TAIL_POLY[:1])))/2-1e-7)
contact('Tail_TopToCableCap',TAIL,CABLE,(0,0,1),(.56,-.19,.56),5*CABLE_R*CABLE_R*math.sin(math.tau/10)-1e-7)
solid('Tail_WholeMaterial',xy_region(offset_convex(TAIL_POLY,.001),[],.461,.559),[TAIL],'Entire solid no-pin tail head, including all chamfered corner facets and complete upper/lower capped faces.')
# Complete finite air domains: both frame apertures; hand opening through the
# full depth; entire drum recess/each blind cavity; all sides and winding bay.
air('Frame_WholeLowerAperture',xz_region(offset_convex(FRAME_LOWER,.001),[],.269,.351),'Entire through lower frame aperture with every edge and both open mouths.')
air('Frame_WholeUpperAperture',xz_region(offset_convex(FRAME_UPPER,.001),[],.269,.351),'Entire through upper frame aperture from axle crossbridge to underside of integral carry bridge.')
air('Carry_CompleteAboveRimHandAir',box((-.31,-.251,.992),(.31,.269,1.159)),'Whole finite hand passage between drum top and carry bridge across the complete front-to-rear depth.')
air('Drum_WholeFrontRecess',xz_region(offset_convex(BOWL,.001),[],-.35,-.216),'Entire sixteen-facet face recess and full forward mouth; the complete finite floor is independently material-probed.')
for i,p in enumerate(PORTS):air('Drum_WholeBlindCavity_%d'%i,xz_region(offset_convex(p,.001),[],-.214,-.156),'Complete original nonstandard blind cavity through all wall facets to 1 mm before its actual thick floor, not a centre ray.')
air('Drum_WholeRearSideAir',xz_region(offset_convex(OUTER,.001),[offset_convex(poly(0,CZ,.048,12),-.001)],.171,.269),'Complete annular side air between drum rear and carry frame, only actual axle is subtracted.')
air('Drum_WholeFrontSideAir',xz_region(offset_convex(OUTER,.001),[],-.359,-.251),'Complete forward slab before the full drum flange and recessed face.')
air('Drum_WholeUnderRimAir',box((-.359,-.249,.161),(.359,.269,.269)),'Complete finite under-drum air above low tie and shoes, across full flange/front/rear span.')
# Entire cable-neighbour clearances are certified separately by all tube strip
# pairs and the full triangle self relation. The empty winding air is a closed
# CSG-free cell complex: occupied cable is subtracted by a tube envelope proof.
# Here broad top/left/right perimeter air is explicitly bounded as full slabs.
for label,lo,hi in [('Left',(-.379,-.249,.271),(-.361,.269,.989)),('Top',(-.359,-.129,.991),(.359,.129,1.039))]:air('Drum_WholePerimeter_'+label,box(lo,hi),'Complete finite perimeter strip adjacent to the full drum and side frame; 1 mm physical margin.')
# Full open-front tray entrance and complete free side strips around the head.
air('Drum_WholeExternalPerimeter',xz_region(poly(0,CZ,.379,24),[offset_convex(OUTER,-.001)],-.249,.269),'Entire finite 360-degree exterior annular gap around the complete drum, across the whole drum/frame depth. Only the actual continuous exiting tail may occupy it; every other component must be absent and cable/drum full-surface separation is separately proved.',[n for n in G if n!=CABLE])
air('Tray_WholeFrontOpening',box((.526,-.34,.461),(.609,-.271,.529)),'Whole finite open front entrance to the side tray, before the parked head.')
air('Tray_WholeAssembledHeadAir',xy_region(rect(.52535,.60965,-.26965,-.14035),[offset_convex(TAIL_POLY,-.00035)],.46035,.52965),'Entire finite assembled tray opening around ALL head sides and chamfers, full depth from actual floor to cheek top; uniform 0.35 mm margins.')
air('Drum_WholeWindingEnvelope',xz_region(offset_convex(OUTER,.001),[offset_convex(CORE,-.001)],-.129,.129),'Entire annular winding bay across full circumference and depth, with ONLY actual cable and its explicit inner seat treated as occupied. All other solids must remain absent; full nonlocal cable strip clearance separately certifies every inter-turn region.',[n for n in G if n not in [CABLE,SEAT]])
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
# Centre the horizontal full envelope and consistently translate every domain.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for dd in [G,VOID_VOLUMES,SOLID_VOLUMES,ISOLATED_VOID_VOLUMES]:
 for g in dd.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['x']-=SHIFT[0];r['y']-=SHIFT[1]
PATH=[sub(p,SHIFT) for p in PATH]
BODY=DRUM
CONTRACT={'single_prop_count':1,'whole_continuous_carry_frames':1,'ground_shoes':2,'fixed_horizontal_axles':1,'integral_double_flange_drums':1,'real_front_face_recesses':1,'original_nonstandard_blind_cavities':3,'connected_cable_components':1,'complete_cable_turns':TURNS,'cable_capped_endpoints':2,'fixed_inner_seats':1,'open_tail_trays':1,'solid_parked_no_pin_heads':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'electrical_communication_mechanical_or_safety_claim':False}
def measure_cable_reel_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 vv=[p for values in vertices.values() for p in values]
 for k in [0,1]:assert abs(min(p[k] for p in vv)+max(p[k] for p in vv))<2e-7
 return dict(CONTRACT,geometry_scope='one original fixed visual prop; full surface/volume/negative proofs and independent actual exported GLB required')
INSIDE_TESTS=[(FRAME,sub((0,.31,1.25),SHIFT),sub((0,.31,1.12),SHIFT)),(DRUM,sub((0,-.145,.63),SHIFT),sub((0,-.235,.63),SHIFT))]
FOCUS=(0,0,.64);ORTHO=1.90
CAMERAS={'gray-front3q':(2.6,-3.6,2.2),'gray-back3q':(-2.6,3.6,2.2),'thumbnail':(2.6,-3.6,2.2),'qa-front':(0,-4,1.65),'qa-side':(4,0,1.65),'qa-top':(0,0,5),'qa-back':(0,4,1.65),'qa-wireframe':(2.6,-3.6,2.2),'silhouette-128-front':(0,-4,1.65),'silhouette-128-side':(4,0,1.65)}
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
root=bpy.data.objects.new('OnePortableCableReel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontal envelope centre on ground';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_cable_reel_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'cable_reel_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/communications/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'communications','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
