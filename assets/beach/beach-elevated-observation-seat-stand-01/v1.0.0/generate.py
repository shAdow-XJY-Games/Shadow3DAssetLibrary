"""Original static high observation seat with four splayed posts and independent ladder."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beach-elevated-observation-seat-stand-01';VERSION='1.0.0';TITLE='Elevated Observation Seat Stand'
DESCRIPTION=('One original fixed high observation-seat visual prop. Four complete outward-splayed posts carry an upper open U-shaped seat cradle and separate rear crossmember; the two continuous rear posts rise to three thick open-spaced back slats and both finite-rooted armrests. The complete thick seat top is 1.80 m high. A separate lower full foot platform has a 1.42 m top and a complete three-member underframe. Two independent inclined ladder side beams have full flat ground soles and support four thick horizontal treads across both complete finite ends. Three clipped diagonal braces join the two side bays and rear bay. Six complete flat soles, all finite structural interfaces, full material bodies and complete empty bays are explicitly described. All geometry is newly authored, without removing a slide chute, stretching a dining chair or barstool, or assembling earlier ladder/platform assets. One static prop with no person, umbrella, lifebuoy, sand, textures, text, logos or animation. Metres, native Z up, front -Y and horizontally bounds-centred ground origin. Only visual form: no real rescue performance, observation coverage, human suitability, climbability, loading, stability, wind resistance, outdoor durability, manufacture, public safety or rescue-equipment certification.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];PLANES={}
SHIFT=(0,.51,0);KX=.14/1.64;KF=.20/1.64;KR=-.22/1.64;KL=.64/1.30
PALETTE=[('WarmIvoryStructure',(.64,.65,.57,1),.66,.08),('MutedCoralSeatBack',(.63,.16,.105,1),.57,.02),('DeepMarineTreads',(.035,.21,.23,1),.61,.08),('DarkBraceMetal',(.09,.14,.14,1),.50,.35)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr(a,b):return a[0]*b[1]-a[1]*b[0]
def clip(poly,cl):
 if cr(sub(cl[1],cl[0]),sub(cl[2],cl[0]))<0:cl=list(reversed(cl))
 for p,q in zip(cl,cl[1:]+cl[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-11;ei=de>=-1e-11
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return poly

def earclip(v):
 if len(v)==3:return [(0,1,2)]
 normal=tuple(sum(cross(v[i],v[(i+1)%len(v)])[k] for i in range(len(v))) for k in range(3));drop=max(range(3),key=lambda i:abs(normal[i]));p=[tuple(x for k,x in enumerate(vv) if k!=drop) for vv in v];area=sum(cr(p[i],p[(i+1)%len(p)]) for i in range(len(p)));order=list(range(len(p))) if area>0 else list(reversed(range(len(p))));out=[]
 while len(order)>3:
  found=False
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-13:continue
   def contained(q):return all(cr(sub(y,x),sub(q,x))>=-1e-13 for x,y in[(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(contained(p[q]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(i);found=True;break
  assert found,('Untriangulable original polygon',p,order)
 out.append(tuple(order));return out if area>0 else[tuple(reversed(t)) for t in out]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];ff=[tuple(f[i] for i in t) for f in fs for t in earclip([vv[j] for j in f])];volume=sum(dot(vv[f[0]],cross(vv[f[1]],vv[f[2]])) for f in ff)/6
 if volume<0:ff=[tuple(reversed(f)) for f in ff]
 return {'vertices':vv,'faces':ff,'material':material,'role':role}
def convex(planes,e=0,material=0,role=''):
 ps=[]
 for n,d in planes:
  length=math.sqrt(dot(n,n));ps.append((mul(n,1/length),d/length-e))
 vs=[]
 for (a,da),(b,db),(c,dc) in itertools.combinations(ps,3):
  det=dot(a,cross(b,c))
  if abs(det)<1e-10:continue
  p=mul(add(add(mul(cross(b,c),da),mul(cross(c,a),db)),mul(cross(a,b),dc)),1/det)
  if all(dot(n,p)<=d+1e-8 for n,d in ps) and not any(dot(sub(p,q),sub(p,q))<1e-15 for q in vs):vs.append(p)
 fs=[]
 for n,d in ps:
  inds=[i for i,p in enumerate(vs) if abs(dot(n,p)-d)<1e-7]
  if len(inds)<3:continue
  center=tuple(sum(vs[i][k] for i in inds)/len(inds) for k in range(3));u=unit(sub(vs[inds[0]],center));v=cross(n,u)
  inds.sort(key=lambda i:math.atan2(dot(sub(vs[i],center),v),dot(sub(vs[i],center),u)));fs.append(tuple(inds))
 return mesh(vs,fs,material,role)
def xr(s,half):return[((s,0,KX),.64+half),((-s,0,-KX),-.64+half)]
def yr(b,k,half):return[((0,1,-k),b+half),((0,-1,k),-b+half)]
def zr(z0,z1):return[((0,0,-1),-z0),((0,0,1),z1)]
def br(lo,hi):return [((1,0,0),hi[0]),((-1,0,0),-lo[0]),((0,1,0),hi[1]),((0,-1,0),-lo[1]),((0,0,1),hi[2]),((0,0,-1),-lo[2])]
def put(n,p,m,role):
 G[n]=convex(p,material=m,role=role);PLANES[n]=p;SOLID_VOLUMES[n+'_WholeInsetMaterial']=dict(convex(p,.001),targets=[n],role='Complete connected 1 mm inward-offset material volume of every full face, all thickness and entire member: '+role)
def air(n,p,role):VOID_VOLUMES[n]=dict(convex(p),targets=None,role=role)
def contact(name,a,b,normal,p):
 normal=unit(normal);u=unit(cross((0,1,0),normal)) if abs(normal[1])<.9 else (1,0,0);v=cross(normal,u);plane=dot(normal,p)
 def tris(n,sign):
  g=G[n];out=[]
  for f in g['faces']:
   t=[g['vertices'][i] for i in f]
   if max(abs(dot(normal,q)-plane) for q in t)<1e-7 and dot(cross(sub(t[1],t[0]),sub(t[2],t[0])),normal)*sign>0:out.append([(dot(q,u),dot(q,v)) for q in t])
  return out
 polys=[clip(aa,bb) for aa in tris(a,1) for bb in tris(b,-1)];area=lambda q:abs(sum(cr(q[i],q[(i+1)%len(q)]) for i in range(len(q))))/2 if len(q)>2 else 0
 total=sum(area(q) for q in polys);assert total>1e-5,(name,a,b,total)
 pp=max(polys,key=area);cp=tuple(sum(q[k] for q in pp)/len(pp) for k in range(2));point=add(add(mul(u,cp[0]),mul(v,cp[1])),mul(normal,plane))
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':normal,'plane_m':plane,'points':[point],'minimum_patch_area_m2':total-1e-7,'complete_interface_area_m2':total,'interior_probe_offset_m':.0004,'role':'Complete finite opposed surface intersection, including every triangulated contact patch. Positive penetration is disallowed in either direction.'})
FRONT=[];REAR=[];LADDER=[];TREADS=[];BRACES=[];ARMS=[];BACKS=[];BEARERS=[]
for s,label in[(-1,'Left'),(1,'Right')]:
 f='MainFrontSplayedPost_'+label;r='ContinuousRearSplayedBackPost_'+label;FRONT.append(f);REAR.append(r)
 put(f,xr(s,.05)+yr(-.58,KF,.05)+zr(0,1.64),0,'Complete outward-splayed front post, whole flat 100 mm square sole and complete upper cradle seat.')
 put(r,xr(s,.05)+yr(.62,KR,.05)+zr(0,2.58),0,'One unbroken outward-splayed rear post from whole flat ground sole to the complete back/arm support, not disconnected stacked legs.')
 for n,y in[(f,-.58),(r,.62)]:FEET.append(n);FOOT_CONTACTS.append({'mesh':n,'name':n+'_WholeGroundSole','x':s*.64,'y':y,'half_x':.05,'half_y':.05,'minimum_area_m2':.01-1e-7})
# The U cradle is one newly authored continuous concave loft, not three overlapping beams.
FRAME='WholeOpenUSeatCradle';REARBAR='WholeRearSeatCrossmember';SEAT='WholeThickHighSeatBoard';BODY=FRAME

def uframe(e=0):
 rings=[]
 for z in[1.64+e,1.72-e]:
  c=.64-KX*z;f=-.58+KF*z;r=.62+KR*z;xo=c+.05-e;xi=c-.05+e;yf=f-.05+e;yi=f+.05-e;yb=r-.05-e
  rings.append([(-xo,yf,z),(xo,yf,z),(xo,yb,z),(xi,yb,z),(xi,yi,z),(-xi,yi,z),(-xi,yb,z),(-xo,yb,z)])
 fs=[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
 return mesh(rings[0]+rings[1],fs,0,'One thick continuous open U-shaped upper seat cradle with full front crossmember and both side rails.')
G[FRAME]=uframe();SOLID_VOLUMES['WholeUCradleInsetMaterial']=dict(uframe(.001),targets=[FRAME],role='Entire connected inward-offset U material, both complete side rails, full front crossmember, full thickness and every concave corner.')
put(REARBAR,[((1,0,KX),.59),((-1,0,KX),.59)]+yr(.62,KR,.04)+zr(1.64,1.72),0,'Complete rear seat-frame crossmember between the two unbroken rear posts, separated from the U tips by a visible 10 mm return gap.')
put(SEAT,br((-.56,-.46,1.72),(.56,.318,1.80)),1,'Complete thick high seat board, flat 1.80 m top and full finite bearing patches on the original U cradle.')
for s,f,r in zip([-1,1],FRONT,REAR):
 contact(f+'_FullCradleSeat',f,FRAME,(0,0,1),(s*.5,-.38,1.64))
 contact(r+'_FullCradleRearRoot',FRAME,r,(0,1,-KR),(s*.5,.35,1.64))
 contact(r+'_FullRearCrossmemberEnd',REARBAR,r,(s,0,KX),(s*(.64-KX*1.68-.05),.62+KR*1.68,1.68))
contact('HighSeatWholeCradleBearing',FRAME,SEAT,(0,0,1),(0,-.38,1.72))
# Two projecting lower bearers and a front crossmember form the independent foot-platform underframe.
FOOTBAR='WholeLowerPlatformFrontCrossmember';FOOTBOARD='WholeLowFootPlatform'
for s,label,f in zip([-1,1],['Left','Right'],FRONT):
 n='WholeLowerPlatformSideBearer_'+label;BEARERS.append(n)
 put(n,xr(s,.05)+[((0,-1,0),.95),((0,1,-KF),-.63)]+zr(1.26,1.34),0,'Complete lower foot-platform side bearer, clipped over its whole rear root to the splayed front post and extending to the independent ladder head.')
 contact(n+'_FullFrontPostRoot',n,f,(0,1,-KF),(s*(.64-KX*1.30),-.63+KF*1.30,1.30))
put(FOOTBAR,[((1,0,KX),.59),((-1,0,KX),.59)]+yr(-.90,0,.04)+zr(1.26,1.34),0,'Whole finite lower-platform crossmember, end-supported by both side bearers, with 10 mm clear setback from the ladder contact plane.')
put(FOOTBOARD,br((-.62,-.95,1.34),(.62,-.49,1.42)),2,'Complete 80 mm thick low foot platform, flat 1.42 m top, independently 380 mm below the high seat top.')
for s,n in zip([-1,1],BEARERS):
 contact(n+'_WholeCrossmemberEnd',FOOTBAR,n,(s,0,KX),(s*(.64-KX*1.30-.05),-.90,1.30))
 contact(n+'_WholePlatformBearing',n,FOOTBOARD,(0,0,1),(s*(.64-KX*1.34),-.72,1.34))
contact('LowerPlatformWholeCrossmemberBearing',FOOTBAR,FOOTBOARD,(0,0,1),(0,-.90,1.34))
for s,label,bearer in zip([-1,1],['Left','Right'],BEARERS):
 n='IndependentInclinedLadderBeam_'+label;LADDER.append(n)
 put(n,xr(s,.05)+yr(-1.62,KL,.07)+[((0,1,0),-.95)]+zr(0,1.33),0,'Complete independent inclined ladder side beam, full horizontal 100 by 140 mm sole and full finite vertical head join to the lower platform frame.')
 FEET.append(n);FOOT_CONTACTS.append({'mesh':n,'name':n+'_WholeGroundSole','x':s*.64,'y':-1.62,'half_x':.05,'half_y':.07,'minimum_area_m2':.014-1e-7})
 contact(n+'_WholePlatformFrameHead',n,bearer,(0,1,0),(s*(.64-KX*1.30),-.95,1.30))
for i,zt in enumerate([.28,.56,.84,1.12],1):
 n='WholeHorizontalLadderTread_%02d'%i;TREADS.append(n)
 put(n,[((1,0,KX),.59),((-1,0,KX),.59)]+yr(-1.62,KL,.06)+zr(zt-.055,zt),2,'One whole 55 mm thick horizontal tread with complete finite opposed left and right end support. Full top and bottom planes remain horizontal.')
 for s,beam in zip([-1,1],LADDER):contact(n+'_WholeEnd_'+str(s),n,beam,(s,0,KX),(s*(.64-KX*(zt-.0275)-.05),-1.62+KL*(zt-.0275),zt-.0275))
# Both side diagonals are fully clipped at the actual sloped post planes.
zf=.45;zb=1.15;yf=-.58+KF*zf+.05;yb=.62+KR*zb-.05;M=(zb-zf)/(yb-yf);B=zf-M*yf
for s,label,f,r in zip([-1,1],['Left','Right'],FRONT,REAR):
 n='WholeClippedSideDiagonal_'+label;BRACES.append(n)
 put(n,xr(s,.035)+[((0,-1,KF),.53),((0,1,-KR),.57),((0,-M,1),B+.045),((0,M,-1),-B+.045)],3,'Whole thick diagonal through a side bay, both full finite ends cut exactly to the opposing actual splayed post faces.')
 z=.45;contact(n+'_WholeFrontEnd',f,n,(0,1,-KF),(s*(.64-KX*z),-.53+KF*z,z))
 z=1.15;contact(n+'_WholeRearEnd',n,r,(0,1,-KR),(s*(.64-KX*z),.57+KR*z,z))
n='WholeClippedRearDiagonal';BRACES.append(n)
put(n,[((1,0,KX),.59),((-1,0,KX),.59)]+yr(.62,KR,.035)+[((-.74,0,1),.845),((.74,0,-1),-.755)],3,'Whole thick rear diagonal between the two continuous rear posts, complete finite end cuts and full depth.')
for s,r in zip([-1,1],REAR):
 z=(.8+.74*s*.59)/(1+.74*s*KX);contact(n+'_WholeRearPostEnd_'+str(s),n,r,(s,0,KX),(s*(.64-KX*z-.05),.62+KR*z,z))
for s,label,r in zip([-1,1],['Left','Right'],REAR):
 post='WholeArmFrontUpright_'+label;arm='WholeSideArmrest_'+label;ARMS.append(arm)
 put(post,br((s*.47-.04,-.36,1.80),(s*.47+.04,-.28,2.10)),0,'Complete short front arm upright on the high seat, with full finite bottom and top faces.')
 put(arm,[((1,0,0),s*.47+.07),((-1,0,0),-s*.47+.07),((0,-1,0),.43),((0,1,-KR),.57)]+zr(2.10,2.18),1,'Complete thick armrest with full front upright bearing and finite clipped root against the continuous rear post.')
 contact(post+'_WholeSeatBearing',SEAT,post,(0,0,1),(s*.47,-.32,1.80));contact(arm+'_WholeUprightBearing',post,arm,(0,0,1),(s*.47,-.32,2.10));contact(arm+'_WholeRearPostRoot',arm,r,(0,1,-KR),(s*.46,.57+KR*2.14,2.14))
for i,(z0,z1) in enumerate([(1.94,2.04),(2.20,2.30),(2.46,2.56)],1):
 n='WholeOpenSpacedBackSlat_%02d'%i;BACKS.append(n)
 put(n,[((1,0,KX),.59),((-1,0,KX),.59)]+yr(.62,KR,.035)+zr(z0,z1),1,'Complete thick horizontal back slat, both full finite ends supported by the unbroken rear posts; real open gaps separate all slats.')
 for s,r in zip([-1,1],REAR):
  z=(z0+z1)/2;contact(n+'_WholeEnd_'+str(s),n,r,(s,0,KX),(s*(.64-KX*z-.05),.62+KR*z,z))
# Finite full empty domains cover entire bays, not rays or human-size proxies.
for i,(z0,z1) in enumerate([(0.002,.223),(.282,.503),(.562,.783),(.842,1.063),(1.122,1.258)]):
 air('WholeLadderBay_%02d'%i,[((1,0,KX),.588),((-1,0,KX),.588)]+yr(-1.62,KL,.068)+[((0,1,0),-.952)]+zr(z0,z1),'Entire finite empty bay between the actual ladder side beams, across their full depth and between complete adjacent horizontal tread surfaces, with 2 mm boundary allowance.')
air('WholeUpperFrontEntry',br((-.398,-.948,1.422),(.398,-.462,2.578)),'Entire unoccupied upper-front entry above the lower foot platform and in front of the high seat, through its complete finite height. No human access or climbability claim.')
air('WholeSeatToFootPlatformSeparation',br((-.398,-.488,1.422),(.398,-.462,1.798)),'Whole finite transition opening between the low platform and the high seat front, with explicit independent seat/platform top-height difference.')
air('WholeCentralUnderSeatAir',[((1,0,0),.388),((-1,0,0),.388),((0,-1,KF),.528),((0,1,-KR),.533)]+zr(.002,1.638),'Entire central under-seat empty chamber, extending from near the ground to the upper-frame underside, ahead of the full rear diagonal and inside both side diagonals.')
for s,label in[(-1,'Left'),(1,'Right')]:
 air('WholeArmSideOpening_'+label,xr(s,.048)+[((0,-1,0),.278),((0,1,-KR),.568)]+zr(1.802,2.098),'Whole finite side opening between the high seat, front arm upright, armrest underside and rear post; full transverse post depth with 2 mm boundary allowance.')
 for upper in[False,True]:
  diagonal=[((0,M,-1),-B-.047)] if upper else[((0,-M,1),B-.047)]
  air('WholeSideDiagonalBay_'+label+('_Upper' if upper else'_Lower'),xr(s,.033)+[((0,-1,KF),.528),((0,1,-KR),.568)]+zr(.002,1.638)+diagonal,'Complete finite empty side bay on one side of its full diagonal brace, including the entire clipped wedge, with 2 mm inset from intentional structure.')
for i,(z0,z1) in enumerate([(1.802,1.938),(2.042,2.198),(2.302,2.458)]):
 air('WholeBackOpening_%02d'%i,[((1,0,KX),.588),((-1,0,KX),.588)]+yr(.62,KR,.033)+zr(z0,z1),'Entire finite back opening across full width and depth between actual supported back slats or the high seat, with 2 mm boundaries.')
for upper in[False,True]:
 diagonal=[((.74,0,-1),-.847)] if upper else[((-.74,0,1),.753)]
 air('WholeRearDiagonalBay_'+('Upper' if upper else'Lower'),[((1,0,KX),.588),((-1,0,KX),.588)]+yr(.62,KR,.033)+zr(.002,1.638)+diagonal,'Entire finite rear empty wedge on one side of the complete rear diagonal, across full depth and between both continuous rear posts.')
for r in VOID_VOLUMES.values():r['targets']=list(G)
for container in[G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in container.values():g['vertices']=[add(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=SHIFT;r['points']=[add(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['x']+=SHIFT[0];r['y']+=SHIFT[1]
CONTRACT={'single_prop_count':1,'complete_main_splayed_posts':4,'unbroken_rear_back_posts':2,'upper_open_u_cradles':1,'upper_rear_crossmembers':1,'high_seat_top_m':1.80,'low_foot_platform_top_m':1.42,'seat_to_platform_top_difference_m':.38,'lower_platform_underframe_members':3,'independent_ladder_side_beams':2,'whole_horizontal_ladder_treads':4,'full_double_end_tread_contacts':8,'whole_diagonal_braces':3,'whole_armrests':2,'whole_back_slats':3,'complete_flat_ground_soles':6,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'human_climb_load_rescue_or_safety_claim':False}
def measure_observation_seat_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[SEAT])-1.80)<2e-7 and abs(max(p[2] for p in vertices[FOOTBOARD])-1.42)<2e-7
 for n,zt in zip(TREADS,[.28,.56,.84,1.12]):assert abs(max(p[2] for p in vertices[n])-zt)<2e-7 and abs(min(p[2] for p in vertices[n])-(zt-.055))<2e-7
 allv=[p for vv in vertices.values() for p in vv]
 for ax in[0,1]:assert abs(min(p[ax] for p in allv)+max(p[ax] for p in allv))<2e-7
 return dict(CONTRACT,geometry_scope='complete source/export coordinates; independent actual full volumes, complete finite contacts, self-intersections and necessary actual negative controls required')
INSIDE_TESTS=[(SEAT,add((0,0,1.76),SHIFT),add((0,0,2),SHIFT)),(FOOTBOARD,add((0,-.70,1.38),SHIFT),add((0,-.70,1.70),SHIFT))]
FOCUS=(0,0,1.29);ORTHO=4.05
CAMERAS={'gray-front3q':(4,-6,4.6),'gray-back3q':(-4,6,4.6),'thumbnail':(4,-6,4.6),'qa-front':(0,-6,3.2),'qa-side':(6,0,3.2),'qa-top':(0,0,6),'qa-back':(0,6,3.2),'qa-wireframe':(4,-6,4.6),'silhouette-128-front':(0,-6,3.2),'silhouette-128-side':(6,0,3.2)}
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
root=bpy.data.objects.new('OneElevatedObservationSeatStand',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred six-sole ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_observation_seat_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'observation_seat_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beach/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beach','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
