"""Original single-bay empty glass greenhouse, one static architectural model."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='farming-single-bay-glass-greenhouse-01';VERSION='1.0.0';TITLE='Single-bay Glass Greenhouse'
DESCRIPTION=('One original freestanding empty 2.4 by 3 metre gabled greenhouse shell: a whole open-centre low footing, four original continuous inverted-U portal frames, finite longitudinal eave and ridge members, eighteen individually closed 6 mm true-glass panes across both side walls, both roof pitches, both end gables and one distinct fixed closed front door. The planting interior is entirely empty, including the roof volume, side recesses, end gable recesses and inner entrance approach. One static architectural model, native metres/Z up/front -Y, centred horizontal envelope and full ground datum Z=0. Constant near-clear transmission glass with alpha one, matching IOR and physical-volume thickness; no textures or linked inputs. No shelves, crops, soil contents, lights, labels, branding, animation, window operation, ventilation, climate control, door travel, practical passage, growing performance, structural/weather/glass safety, manufacturing or old-building interface claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BASE='WholeOpenCentreGroundFooting';BODY=BASE;DOOR='ContinuousFixedEntranceDoorFrame';GLASS=[];PORTALS=[];EAVES=[];RIDGES=[];GLASS_NORMALS={};GLASS_SPECS={}
PALETTE=[('DeepSageFrame',(.075,.135,.105,1),.38,.45),('WarmMineralFooting',(.36,.33,.27,1),.72,.0),('PaleSageEntranceFrame',(.22,.29,.20,1),.4,.25),('TrueClearThickGlass',(.94,.985,.98,1),.035,0.),('SatinBrassDoorPull',(.45,.30,.10,1),.32,.7)]
GLASS_INDEX=3;GLASS_TRANSMISSION=1.;GLASS_IOR=1.45;GLASS_THICKNESS=.006
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

def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def polyarea(p):return sum(cross2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2

def ear2(poly):
 order=list(range(len(poly)))
 if polyarea(poly)<0:order.reverse()
 out=[]
 while len(order)>3:
  found=False
  for ii,b in enumerate(order):
   a=order[ii-1];c=order[(ii+1)%len(order)]
   if cross2(sub(poly[b],poly[a]),sub(poly[c],poly[b]))<=1e-13:continue
   def within(q):return all(cross2(sub(y,x),sub(q,x))>=-1e-13 for x,y in [(poly[a],poly[b]),(poly[b],poly[c]),(poly[c],poly[a])])
   if any(within(poly[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(ii);found=True;break
  assert found,('Invalid polygon',poly,order)
 out.append(tuple(order));return out

def xzprism(poly,y0,y1,material=0,role=''):
 # Every cap is triangulated correctly; side quads retain their true finite boundary.
 if polyarea(poly)<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for y in [y0,y1] for x,z in poly]
 ff=[tuple(reversed(t)) for t in ear2(poly)]+[tuple(k+n for k in t) for t in ear2(poly)]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(vv,ff,material,role)

def inset_poly(poly,e=.0006):
 if polyarea(poly)<0:poly=list(reversed(poly))
 out=[]
 for i,p in enumerate(poly):
  before=poly[i-1];after=poly[(i+1)%len(poly)];a=unit(sub(p,before));b=unit(sub(after,p));na=(-a[1],a[0]);nb=(-b[1],b[0]);q=add(p,mul(na,e));r=add(p,mul(nb,e));den=cross2(a,b)
  if abs(den)<1e-12:out.append(q)
  else:out.append(add(q,mul(a,cross2(sub(r,q),b)/den)))
 return out

def part_xz(name,poly,y0,y1,material,role):
 G[name]=xzprism(poly,y0,y1,material,role);solid(name+'_WholeMaterial',xzprism(inset_poly(poly),y0+.0006,y1-.0006),[name],'Entire connected polygonal material body, all edges and cap boundaries offset inward 0.6 mm. '+role)

def pane(name,g,normal,role):
 g['material']=GLASS_INDEX;g['role']=role;G[name]=g;GLASS.append(name);GLASS_NORMALS[name]=normal
 proj=[dot(p,normal) for p in g['vertices']];GLASS_SPECS[name]={'normal':normal,'plane_min_m':min(proj),'plane_max_m':max(proj),'thickness_m':GLASS_THICKNESS}
 assert abs(max(proj)-min(proj)-GLASS_THICKNESS)<2e-8,(name,min(proj),max(proj))

# One genuine perimeter footing. No broad exhibit plinth or floor fills its planting area.
def footing(e=0):return grid([-1.2+e,-1.14-e,1.14+e,1.2-e],[-1.5+e,-1.44-e,1.44+e,1.5-e],[e,.1-e],lambda x,y,z:abs(x)>1.14+e or abs(y)>1.44+e,1,'Whole continuous open-centre low ground footing; full perimeter sole at Z=0.')
G[BASE]=footing();FEET=[BASE];solid(BASE+'_WholeMaterial',footing(.0006),[BASE],'Entire connected open-centre footing material, outer inset and inner outset 0.6 mm.')
for side,x in [('Left',-1.17),('Right',1.17)]:FOOT_CONTACTS.append({'mesh':BASE,'name':side+'WholeLongGroundSole','x':x,'y':0,'half_x':.03,'half_y':1.5,'minimum_area_m2':.179999})
for end,y in [('Front',-1.47),('Rear',1.47)]:FOOT_CONTACTS.append({'mesh':BASE,'name':end+'WholeEndGroundSole','x':0,'y':y,'half_x':1.14,'half_y':.03,'minimum_area_m2':.136799})
# Four new continuous five-sided inverted-U portals. Their lower ends are real sole seats.
K=.65/1.2;PITCH_NORMAL=unit((K,0,1));PORTAL_Y=[(-1.5,-1.44),(-.53,-.47),(.47,.53),(1.44,1.5)]
portal_poly=[(-1.2,.1),(-1.2,1.9),(0,2.55),(1.2,1.9),(1.2,.1),(1.14,.1),(1.14,2.48-K*1.14),(0,2.48),(-1.14,2.48-K*1.14),(-1.14,.1)]
for i,(a,b) in enumerate(PORTAL_Y):
 n=f'Portal{i+1}_ContinuousGabledFrame';PORTALS.append(n);part_xz(n,portal_poly,a,b,0,'One continuous full-size gabled inverted-U frame, two real vertical wall posts and both pitched rafters joined at its ridge; no crossing disconnected bars.')
BAYS=[(-1.44,-.53),(-.47,.47),(.53,1.44)]
for bay,(a,b) in enumerate(BAYS,1):
 for sign,label in [(-1,'Left'),(1,'Right')]:
  poly=[(sign*x,z) for x,z in [(1.14,1.84),(1.2,1.84),(1.2,1.9),(1.14,1.9325)]]
  n=f'{label}Bay{bay}_SlopedTopEaveBeam';EAVES.append(n);part_xz(n,poly,a,b,0,'Whole longitudinal eave beam with actual sloping outer top and four finite end/side bearing surfaces.')
  n=f'{label}Bay{bay}_FullSideGlass';cx=sign*1.17;lo=(cx-.003,a,.1);hi=(cx+.003,b,1.84)
  pane(n,box(lo,hi), (1,0,0),'Complete 6 mm closed wall pane, finite bottom/top/two portal-edge seats, full front/back and four edge faces.')
  solid(n+'_WholeMaterial',inset_box(lo,hi,.0006),[n],'Whole wall glass material including both broad faces and every edge inset 0.6 mm.')
  # True thickness is perpendicular to the sloped broad faces, not a vertical 6 mm approximation.
  dz=GLASS_THICKNESS*math.sqrt(1+K*K)
  poly=[(sign*x,z) for x,z in [(.03,2.52-K*.03),(1.14,2.52-K*1.14),(1.14,2.52-K*1.14+dz),(.03,2.52-K*.03+dz)]]
  n=f'{label}Bay{bay}_FullPitchedRoofGlass';normal=unit((sign*K,0,1));pane(n,xzprism(poly,a,b),normal,'Complete 6 mm perpendicular-thickness pitched roof pane between parallel physical planes; full four-edge real frame bearing.')
  solid(n+'_WholeMaterial',xzprism(inset_poly(poly),a+.0006,b-.0006),[n],'Entire sloped glass solid inset 0.6 mm perpendicular to every physical edge and broad face.')
 n=f'Bay{bay}_ContinuousGabledRidgeBeam';RIDGES.append(n);part_xz(n,[(-.03,2.45),(.03,2.45),(.03,2.53375),(0,2.55),(-.03,2.53375)],a,b,0,'Whole continuous longitudinal ridge with two actual roof-edge seats and two end portal seats.')
# Both gables are enclosed, the front has a visually distinct fixed entrance.
for label,(a,b) in [('Front',PORTAL_Y[0]),('Rear',PORTAL_Y[-1])]:
 n=label+'WholeTransomBeam';add_solid(n,(-1.14,a+.002,1.78),(1.14,b-.002,1.84),0,'Whole horizontal end-wall transom, butt seated at both real portal inner walls.')
 centre=(a+b)/2;poly=[(-1.14,1.84),(1.14,1.84),(1.14,2.48-K*1.14),(0,2.48),(-1.14,2.48-K*1.14)]
 n=label+'FullGableGlass';pane(n,xzprism(poly,centre-.003,centre+.003),(0,1,0),'Complete closed 6 mm end-gable pane bounded by actual transom and both sloped inner rafter faces.')
 solid(n+'_WholeMaterial',xzprism(inset_poly(poly),centre-.0024,centre+.0024),[n],'Entire pentagonal end-gable glass domain, all outer boundaries inset 0.6 mm.')
 if label=='Rear':
  n='RearFullLowerWallGlass';lo=(-1.14,centre-.003,.1);hi=(1.14,centre+.003,1.78);pane(n,box(lo,hi),(0,1,0),'Complete closed 6 mm rear wall pane, surrounded by full-width base, transom and portal seats.');solid(n+'_WholeMaterial',inset_box(lo,hi,.0006),[n],'Whole rear lower glass slab with 0.6 mm boundary inset.')
 else:
  for side,xa,xb in [('Left',-.46,-.4),('Right',.4,.46)]:add_solid('Front'+side+'EntranceJamb',(xa,a,.1),(xb,b,1.78),0,'Continuous original doorway jamb, grounded on the footing and bearing against the transom.')
  for side,xa,xb in [('Left',-1.14,-.46),('Right',.46,1.14)]:
   n='Front'+side+'FullSidelightGlass';lo=(xa,centre-.003,.1);hi=(xb,centre+.003,1.78);pane(n,box(lo,hi),(0,1,0),'Complete closed 6 mm front sidelight, all four finite surrounding frame edge seats.');solid(n+'_WholeMaterial',inset_box(lo,hi,.0006),[n],'Whole sidelight glass material with 0.6 mm boundary inset.')
# One separate closed-position door frame and one glass pane. No hinges or travel mechanism promised.
def door(e=0):return grid([-.4+e,-.36-e,.36+e,.4-e],[-1.49+e,-1.45-e],[.1+e,.14-e,1.74+e,1.78-e],lambda x,y,z:abs(x)>.36+e or z<.14-e or z>1.74+e,2,'One continuous fixed closed entrance frame with real hollow central glazing seat.')
G[DOOR]=door();solid(DOOR+'_WholeMaterial',door(.0006),[DOOR],'Entire connected fixed door ring material, 0.6 mm inset outer and outset inner boundaries.')
n='FrontDoorFullGlass';lo=(-.36,-1.473,.14);hi=(.36,-1.467,1.74);pane(n,box(lo,hi),(0,1,0),'Complete closed 6 mm glass door infill, seated on all four inner frame faces.');solid(n+'_WholeMaterial',inset_box(lo,hi,.0006),[n],'Entire door glazing slab with 0.6 mm full-boundary inset.')
add_solid('InsetFixedDoorPull',(.366,-1.5,.88),(.394,-1.49,1.02),4,'A shallow fixed brass pull attached across its whole rear face to the real right door stile, within the building envelope.')
# Whole finite empty cultivation domain reaches the ground and both roof pitches.
# Recesses are separately complete, overlapping the main volume without pretending frame/glass is absent.
mainpoly=[(-1.1394,.0006),(1.1394,.0006),(1.1394,2.4792-K*1.1394),((2.4792-2.4494)/K,2.4494),(-(2.4792-2.4494)/K,2.4494),(-1.1394,2.4792-K*1.1394)]
air('WholeCultivationInterior',xzprism(mainpoly,-1.4394,1.4394),'Entire continuous ground-to-gable finite interior, including the empty planting floor and full upper air under all four true portal undersides. No central-only ray proxy.')
for bay,(a,b) in enumerate(BAYS,1):
 for sign,label in [(-1,'Left'),(1,'Right')]:
  xa,xb=sorted([sign*1.1388,sign*1.1664]);air(f'{label}Bay{bay}_WholeSideWallRecess',box((xa,a+.0006,.1006),(xb,b-.0006,1.8394)),'Full peripheral wall-glass recess from overlapping main interior to actual pane inner face, bounded by real portal faces.')
  # Includes the full between-portal attic under each roof pane; ridge/eave members excluded.
  poly=[(sign*x,z) for x,z in [(.0306,2.42-K*.0306),(1.1394,2.42-K*1.1394),(1.1394,2.5192-K*1.1394),(.0306,2.5192-K*.0306)]]
  air(f'{label}Bay{bay}_WholePitchedRoofRecess',xzprism(poly,a+.0006,b-.0006),'Complete between-portal roof-glass recess up to the physical sloped pane underside, down into overlapping whole main roof air; excludes real ridge and eave material.')
for i,(a,b) in enumerate(PORTAL_Y[1:3],2):
 poly=[(-.056,2.44),(.056,2.44),(.056,2.4792-K*.056),(0,2.4792),(-.056,2.4792-K*.056)]
 air(f'Portal{i}_WholeUnderRidgeApex',xzprism(poly,a+.0006,b-.0006),'Whole under-portal apex interval between overlapping main room and actual portal inner ridge, absent only where real longitudinal ridge material exists.')
for label,ya,yb in [('Front',-1.4664,-1.4388),('Rear',1.4388,1.4664)]:
 poly=inset_poly([(-1.14,1.84),(1.14,1.84),(1.14,2.48-K*1.14),(0,2.48),(-1.14,2.48-K*1.14)],.0006)
 air(label+'WholeGableGlassRecess',xzprism(poly,ya,-1.4406) if label=='Front' else xzprism(poly,1.4406,yb),'Entire finite end-gable recess up to real glass inner face; complete sloped frame boundary inset.')
 bridge=[(-1.1394,1.8406),(1.1394,1.8406),(1.1394,2.4792-K*1.1394),((2.4792-2.4494)/K,2.4494),(-(2.4792-2.4494)/K,2.4494),(-1.1394,2.4792-K*1.1394)]
 air(label+'WholeGableRecessBridge',xzprism(bridge,-1.4412,-1.4388) if label=='Front' else xzprism(bridge,1.4388,1.4412),'Complete low-apex end-recess transition to overlapping whole interior, excludes actual ridge end material.')
 if label=='Rear':air('RearWholeWallGlassRecess',box((-1.1394,ya,.1006),(1.1394,yb,1.7794)),'Entire rear lower pane recess to actual glass inner face, overlapping main room air.')
 else:
  for side,xa,xb in [('Left',-1.1394,-.4606),('Right',.4606,1.1394)]:air('Front'+side+'WholeSidelightRecess',box((xa,ya,.1006),(xb,yb,1.7794)),'Whole front sidelight recess between complete portal, jamb and glass boundaries.')
  air('WholeInnerDoorGlazingRecess',box((-.3594,ya,.1406),(.3594,yb,1.7394)),'Full fixed-door inner glazing recess; not a claim of an open or traversable entrance.')
  air('WholeInnerEntranceApproach',box((-.3994,-1.4394,.1006),(.3994,-.90,1.7794)),'Whole actual clear inner entrance approach up to closed door frame; overlaps complete cultivation interior and makes no opening or fit claim.')
for v in VOID_VOLUMES.values():v['targets']=list(G)
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

def canonical_patch(poly):
 out=[]
 for p in poly:
  if not out or math.dist(p,out[-1])>1e-10:out.append(p)
 if len(out)>1 and math.dist(out[0],out[-1])<1e-10:out.pop()
 changed=True
 while changed and len(out)>3:
  changed=False
  for i,p in enumerate(out):
   if abs(patch_cross(sub(p,out[i-1]),sub(out[(i+1)%len(out)],p)))<1e-12:
    out.pop(i);changed=True;break
 return out

def source_triangles(g):return [[g['vertices'][j] for j in [f[0],f[i],f[i+1]]] for f in g['faces'] for i in range(1,len(f)-1)]
# The author declares only real positive-area opposed boundary contacts. All
# remaining pairs must pass positive separation; independent QA rechecks full finite patches.
for an,bn in itertools.combinations(G,2):
 aa=source_triangles(G[an]);bb=source_triangles(G[bn]);planes={}
 for a in aa:
  normal=unit(cross(sub(a[1],a[0]),sub(a[2],a[0])));plane=dot(normal,a[0]);key=tuple(round(x,8) for x in normal)+(round(plane,8),)
  if key in planes:continue
  u=unit(cross((0,1,0),normal)) if abs(normal[1])<.9 else (1,0,0);v=cross(normal,u)
  r={'a':an,'b':bn,'origin_m':(0,0,0),'u':u,'v':v,'axis':normal,'plane_m':plane}
  at=patch_triangles(an,r,1);bt=patch_triangles(bn,r,-1);polys=[]
  for at0 in at:
   for bt0 in bt:
    poly=canonical_patch(patch_clip(at0,bt0))
    if patch_area(poly)>1e-11:polys.append(poly)
  if not polys:continue
  area=sum(patch_area(p) for p in polys);largest=max(polys,key=patch_area);centre=tuple(sum(p[k] for p in largest)/len(largest) for k in range(2));point=add(add(mul(u,centre[0]),mul(v,centre[1])),mul(normal,plane))
  r.update(name=an+'__to__'+bn+'__'+str(len(planes)),points=[point],minimum_patch_area_m2=area-2e-8,interior_probe_offset_m=.0004,declared_patch_polygons_uv_m=polys,declared_patch_area_m2=area)
  planes[key]=r
 CONTACTS.extend(planes.values())


# Quantized source domains are immutable numerical construction evidence.
# Authored geometry remains exact; every quantized vertex stays within 2e-7 m.
import struct
def f32(x):return struct.unpack('<f',struct.pack('<f',float(x)))[0]
QVERTS={name:[tuple(f32(c) for c in p) for p in g['vertices']] for name,g in G.items()}
for name,v in QVERTS.items():assert all(math.dist(a,b)<=2e-7 for a,b in zip(v,G[name]['vertices']))
def triangles_with_vertices(name,vertices):return [[vertices[j] for j in [f[0],f[i],f[i+1]]] for f in G[name]['faces'] for i in range(1,len(f)-1)]
def finite_domains(a,b,r):
 def project(tris,sign):
  out=[]
  for t in tris:
   if max(abs(dot(sub(p,r['origin_m']),r['axis'])-r['plane_m']) for p in t)>2e-7:continue
   if dot(cross(sub(t[1],t[0]),sub(t[2],t[0])),r['axis'])*sign<=0:continue
   out.append([(dot(sub(p,r['origin_m']),r['u']),dot(sub(p,r['origin_m']),r['v'])) for p in t])
  return out
 out=[]
 for aa in project(a,1):
  for bb in project(b,-1):
   p=canonical_patch(patch_clip(aa,bb))
   if patch_area(p)>1e-11:out.append(p)
 return out

def finite_segment_in_union(a,b,polys,eps=2e-7):
 d=sub(b,a);intervals=[]
 for poly in polys:
  p=list(poly)
  if patch_cross(sub(p[1],p[0]),sub(p[2],p[0]))<0:p.reverse()
  low,high=0.,1.
  for u,v in zip(p,p[1:]+p[:1]):
   edge=sub(v,u);length=math.hypot(*edge)
   if length<1e-12:continue
   value=patch_cross(edge,sub(a,u))/length;slope=patch_cross(edge,d)/length
   if abs(slope)<1e-12:
    if value < -eps:low,high=1.,0.;break
   elif slope>0:low=max(low,(-eps-value)/slope)
   else:high=min(high,(-eps-value)/slope)
  if low<=high:intervals.append((max(0.,low),min(1.,high)))
 end=0.
 for low,high in sorted(intervals):
  if low>end+1e-8:break
  end=max(end,high)
 return end>=1.-1e-8

def full_boundary_in(a,b,eps=2e-7):return all(finite_segment_in_union(p,p,b,eps) and finite_segment_in_union(p,poly[(i+1)%len(poly)],b,eps) for poly in a for i,p in enumerate(poly))
for r in CONTACTS:
 qp=finite_domains(triangles_with_vertices(r['a'],QVERTS[r['a']]),triangles_with_vertices(r['b'],QVERTS[r['b']]),r);original=r['declared_patch_polygons_uv_m'];qa=sum(patch_area(p) for p in qp)
 assert qp and full_boundary_in(qp,original) and full_boundary_in(original,qp) and abs(qa-r['declared_patch_area_m2'])<=2e-7,r['name']
 r['expected_float32_patch_polygons_uv_m']=qp;r['expected_float32_patch_area_m2']=qa

CONTRACT={'single_prop_count':1,'kind':'modular','whole_open_centre_footing':1,'continuous_gabled_portals':4,'longitudinal_eave_members':6,'longitudinal_ridge_members':3,'complete_side_glass_panes':6,'complete_pitched_roof_glass_panes':6,'complete_end_wall_gable_door_glass_panes':6,'separate_fixed_entrance_door':1,'whole_empty_cultivation_interior':1,'glass_meshes':GLASS,'glass_thickness_m':{n:GLASS_THICKNESS for n in GLASS},'glass_normal_specs':GLASS_SPECS,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'shelves_crops_opening_climate_or_safety_claim':False}
assert len(GLASS)==18

def measure_greenhouse_geometry(vertices):
 assert set(vertices)==set(G)
 allv=[p for v in vertices.values() for p in v];lo=[min(p[k] for p in allv) for k in range(3)];hi=[max(p[k] for p in allv) for k in range(3)]
 assert all(abs(a-b)<2e-7 for a,b in zip(lo,[-1.2,-1.5,0])) and all(abs(a-b)<2e-7 for a,b in zip(hi,[1.2,1.5,2.55]))
 measured={}
 for n in GLASS:
  normal=GLASS_NORMALS[n];proj=[dot(p,normal) for p in vertices[n]];th=max(proj)-min(proj);assert abs(th-GLASS_THICKNESS)<2e-7,(n,th)
  assert abs(min(proj)-GLASS_SPECS[n]['plane_min_m'])<2e-7 and abs(max(proj)-GLASS_SPECS[n]['plane_max_m'])<2e-7
  measured[n]={'normal_thickness_m':th,'complete_parallel_boundary_planes_m':[min(proj),max(proj)]}
 return dict(CONTRACT,measured_glass=measured,geometry_scope='Actual complete vertices; full finite material/air domains, contacts, topology, orientation and nonpenetration remain separately required.')
INSIDE_TESTS=[(BASE,(1.17,0,.05),(0,0,.05)),(DOOR,(.38,-1.47,.5),(0,-1.47,.5)),('RightBay2_FullSideGlass',(1.17,0,.6),(1.16,0,.6))]
FOCUS=(0,0,1.24);ORTHO=4.6
CAMERAS={'gray-front3q':(6,-8,5.2),'gray-back3q':(-6,8,5.2),'thumbnail':(6,-8,5.2),'qa-front':(0,-9,3.7),'qa-side':(9,0,3.7),'qa-top':(0,0,9),'qa-back':(0,9,3.7),'qa-wireframe':(6,-8,5.2),'silhouette-128-front':(0,-9,3.7),'silhouette-128-side':(9,0,3.7)}
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
  group=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree');group.interface.new_socket(name='Occlusion',in_out='INPUT',socket_type='NodeSocketFloat');th=group.interface.new_socket(name='Thickness',in_out='INPUT',socket_type='NodeSocketFloat');th.default_value=GLASS_THICKNESS;group.nodes.new('NodeGroupInput');group.nodes.new('NodeGroupOutput');settings=m.node_tree.nodes.new('ShaderNodeGroup');settings.node_tree=group;settings.inputs['Thickness'].default_value=GLASS_THICKNESS
  assert not any(q.is_linked for q in settings.inputs)
 mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneSingleBayGlassGreenhouse',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred whole perimeter footing ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
face_contacts=[]
actual_quantization=[]
for name,o in byname.items():
 observed=[tuple(float(c) for c in (o.matrix_world@v.co)) for v in o.data.vertices]
 assert len(observed)==len(QVERTS[name]),('Actual vertex count changed',name)
 delta=max(math.dist(a,b) for a,b in zip(observed,G[name]['vertices']));qdelta=max(math.dist(a,b) for a,b in zip(observed,QVERTS[name]))
 assert delta<=2e-7 and qdelta<=1e-12,('Actual whole vertex quantization changed',name,delta,qdelta)
 actual_quantization.append({'mesh':name,'all_vertex_count':len(observed),'max_original_vertex_euclidean_error_m':delta,'max_expected_float32_vertex_error_m':qdelta})
for r in CONTACTS:
 def actual_triangles_for(name):
  o=byname[name];return [[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
 domains=finite_domains(actual_triangles_for(r['a']),actual_triangles_for(r['b']),r);area=sum(patch_area(p) for p in domains);original=r['declared_patch_polygons_uv_m'];expected=r['expected_float32_patch_polygons_uv_m']
 assert domains and full_boundary_in(domains,original) and full_boundary_in(original,domains),('Actual complete boundary escaped original 2e-7 m domain',r['name'])
 assert abs(area-r['declared_patch_area_m2'])<=2e-7,('Actual whole nominal-area difference',r['name'],area)
 assert full_boundary_in(domains,expected,1e-9) and full_boundary_in(expected,domains,1e-9) and abs(area-r['expected_float32_patch_area_m2'])<=1e-10,('Actual domain disagrees with fixed float32 construction',r['name'],area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area,actual_complete_boundary_in_original_domain=True,original_complete_boundary_in_actual_domain=True,actual_complete_boundary_matches_fixed_float32_domain=True,actual_nominal_area_difference_m2=abs(area-r['declared_patch_area_m2'])))

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
mount_evidence=measure_greenhouse_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
  assert abs(thickness-GLASS_THICKNESS)<2e-7 and abs(float(p.inputs['IOR'].default_value)-1.45)<2e-7 and p.inputs['Alpha'].default_value==1.
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
  vol=ext['KHR_materials_volume'];assert near(vol['thicknessFactor'],GLASS_THICKNESS) and vol.get('attenuationColor',[1,1,1])==[1,1,1] and 'attenuationDistance' not in vol
  actual_glass_materials.append({'mesh':me['name'],'material':primitive['material'],'extensions':ext,'pbr':pbrj})
assert {r['mesh'] for r in actual_glass_materials}==set(GLASS)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'actual_whole_vertex_float32_checks':actual_quantization,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'glass_material_actual_export':actual_glass_materials,'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'greenhouse_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_transmission_volume_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/farming/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'architecture','assetKind':'modular','theme':'farming','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-5,7),850,5),('Fill',(5,-2,5),550,4),('Rim',(2,5,6),700,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
original_material_inputs={m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_socket_counts={m:len(m.node_tree.nodes.get('Principled BSDF').inputs) for m in asset_mats}
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
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF');assert len(p.inputs)==original_material_socket_counts[m],'Diagnostic socket count changed'
  assert len(inputs)==len(p.inputs),'Every original Principled socket must retain an explicitly captured value'
  for index,identifier,socket_type,value in inputs:
   socket=p.inputs[index];actual=tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value
   assert socket.identifier==identifier and socket.bl_idname==socket_type and actual==value,('Diagnostic exact socket readback mismatch',m.name,index,identifier)
 for o,(slots,indices) in original_slots.items():
  assert list(o.data.materials)==slots,'Diagnostic material-slot ordering/count mismatch'
  assert len(o.data.polygons)==len(indices),'Diagnostic face count mismatch'
  assert [f.material_index for f in o.data.polygons]==indices,'Diagnostic complete face material-index mismatch'
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
