"""Original compact saddle-tank truck exterior. One static visual prop.
Metres, native Z up, front -Y. Tank is an intentionally solid exterior shape.
No contained liquid, refuelling, driving, ground-service suitability or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='aviation-compact-saddle-tank-truck-01';VERSION='1.0.0';TITLE='Compact Saddle-Tank Truck Exterior'
DESCRIPTION=('One original compact aviation-themed ground vehicle exterior, counted as one static visual prop. A new short five-sided cab with genuinely recessed thick framed panes sits on two continuous chassis rails and four cross ties. Four flat-bottom polygonal wheels meet two fixed axles, four hangers and the rails through finite face patches. Four real open wheel arches remain clear of the tyres. The long solid exterior tank has a continuous elliptical section and original multi-ring rounded closed ends, supported by the complete curved upper surfaces of two independent saddles. A thick side service cabinet has a real open recess and two separate fixed blind sockets; these are disconnected visual shapes without fluid or working connections. Every mesh has a finite support path. No tank interior, airplane, hose, fuel, person, apron, animation, logos, hazard or official markings. This is not a copied van cab with a barrel, old pickup cargo bed, composter drum, minibus or three-wheeler. No fuel containment, pressure, sealing, pumping, dispensing, measurement, steering, wheel motion, speed, load, fire performance, aviation suitability, manufacture, installation, human fit or safety certification.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SECTIONS=[];SADDLES=[];ARCHES=[];WHEELS=[];HANGERS=[];AXLES=[];BLIND_SOCKETS=[];SERVICE_PARTITION=[]
PALETTE=[('Cab_MutedPetrol',(.045,.235,.255,1),.60,.15),('Tank_WarmIvory',(.78,.79,.69,1),.55,.30),('Chassis_Charcoal',(.055,.067,.073,1),.78,.15),('Details_DullAlloy',(.36,.40,.41,1),.45,.55),('Pane_SlateBlue',(.065,.12,.17,1),.38,.05),('Lamp_WarmPale',(.92,.66,.25,1),.56,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
def prism_geometry(x,width,yz):
 if area2(yz)<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 return vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
def prism_x(name,x,width,yz,mat,role,section=True):
 if section:SECTIONS.append({'name':name,'x0':x-width/2,'x1':x+width/2,'loops':[yz]})
 return mesh(name,*prism_geometry(x,width,yz),mat,role)
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size;return prism_x(name,x,w,[(y-d/2,z-h/2),(y+d/2,z-h/2),(y+d/2,z+h/2),(y-d/2,z+h/2)],mat,role)
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);ref=(0,1,0) if abs(axis[0])>.9 else (1,0,0);u=unit(sub(ref,mul(axis,dot(ref,axis))));v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':points or [point],'scope':scope})
def void_x(name,x,w,yz,scope,targets=None,isolated=False):
 vs,fs=prism_geometry(x,w,yz);g={'vertices':vs,'faces':fs,'targets':list(G) if targets is None else targets,'role':scope}
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]=g
def inset_convex(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length);lines.append((n,n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for (a,aa),(b,bb) in zip(lines[-1:]+lines[:-1],lines):
  det=a[0]*b[1]-a[1]*b[0]
  if abs(det)<1e-10:return None
  out.append(((aa*b[1]-a[1]*bb)/det,(a[0]*bb-aa*b[0])/det))
 return out if area2(out)>1e-10 and all(n[0]*p[0]+n[1]*p[1]>=q-1e-8 for n,q in lines for p in out) else None

# The original open chassis contains no old pickup tray or hidden van shell.
for i,x in enumerate([-.40,.40]):box('Rail_%d'%i,(x,0,.72),(.16,3.84,.14),2,'one continuous longitudinal chassis rail')
for i,y in enumerate([-1.82,-.72,.60,1.82]):
 n=box('CrossTie_%d'%i,(0,y,.72),(.64,.14,.14),2,'full chassis cross-tie with both finite end faces on rails')
 contact('Rail_0',n,(1,0,0),(-.32,y,.72),.019599,'whole left cross-tie end')
 contact(n,'Rail_1',(1,0,0),(.32,y,.72),.019599,'whole right cross-tie end')
WZ=.32*math.cos(math.pi/12)
wheelpoly=[(.32*math.cos(math.radians(15+i*30)),WZ+.32*math.sin(math.radians(15+i*30))) for i in range(12)]
for j,y in enumerate([-1.40,1.40]):
 axle=box('FixedAxle_%d'%j,(0,y,WZ),(1.20,.10,.10),3,'one continuous rectangular fixed axle, no wheel or axle movement');AXLES.append(axle)
 for i,x in enumerate([-.69,.69]):
  n=prism_x('Wheel_%d_%d'%(j,i),x,.18,[(y+yy,z) for yy,z in wheelpoly],2,'closed twelve-sided tyre exterior with an entire flat bottom patch at Z0');WHEELS.append(n);FEET.append(n)
  if i==0:contact(n,axle,(1,0,0),(-.60,y,WZ),.009999,'complete axle end against wheel inner side')
  else:contact(axle,n,(1,0,0),(.60,y,WZ),.009999,'complete axle end against wheel inner side')
  hub=prism_x('Hub_%d_%d'%(j,i),(-.795 if i==0 else .795),.03,[(y+.12*math.cos(math.radians(22.5+k*45)),WZ+.12*math.sin(math.radians(22.5+k*45))) for k in range(8)],3,'fixed solid hub cap with full inner end on tyre side')
  contact(hub,n,(1,0,0),(-.78,y,WZ),.040,'complete left hub disk on wheel' ) if i==0 else contact(n,hub,(1,0,0),(.78,y,WZ),.040,'complete right hub disk on wheel')
  hanger=box('Hanger_%d_%d'%(j,i),(-.4 if i==0 else .4,y,(WZ+.05+.65)/2),(.12,.10,.65-WZ-.05),2,'full fixed axle hanger from axle upper face to rail underside');HANGERS.append(hanger)
  contact(axle,hanger,(0,0,1),(-.4 if i==0 else .4,y,WZ+.05),.011999,'complete hanger bottom on axle')
  contact(hanger,'Rail_%d'%i,(0,0,1),(-.4 if i==0 else .4,y,.65),.011999,'complete hanger top against rail bottom')

# Four independently extruded true wheel-arch solids, never a dark painted patch.
archinner=[(-.37,.29),(-.37,WZ)]+[(.37*math.cos(math.radians(a)),WZ+.37*math.sin(math.radians(a))) for a in range(165,0,-15)]+[(.37,WZ),(.37,.29)]
for j,y in enumerate([-1.40,1.40]):
 for i,x in enumerate([-.68,.68]):
  yz=[(y-.43,.29)]+[(y+yy,z) for yy,z in archinner]+[(y+.43,.29),(y+.43,.79),(y-.43,.79)]
  arch=prism_x('Arch_%d_%d'%(j,i),x,.22,yz,0,'closed thick fender with an entirely open lower half-disc wheel arch');ARCHES.append(arch)
  # Arch rests at its inner top side against a bracket carried by the rail.
  bracket=box('ArchBracket_%d_%d'%(j,i),(-.525 if i==0 else .525,y,.755),(.09,.30,.07),2,'short lateral finite connector between chassis rail and arch inward face')
  if i==0:
   contact(arch,bracket,(1,0,0),(-.57,y,.755),.020999,'complete bracket outer end on fender inside')
   contact(bracket,'Rail_0',(1,0,0),(-.48,y,.755),.020999,'complete bracket inner end on rail outside')
  else:
   contact('Rail_1',bracket,(1,0,0),(.48,y,.755),.020999,'complete bracket inner end on rail outside')
   contact(bracket,arch,(1,0,0),(.57,y,.755),.020999,'complete bracket outer end on fender inside')
  # Full isolated arch opening includes the lower mouth and extends past both side faces.
  hole=[(y-.369,.289),(y+.369,.289),(y+.369,WZ)]+[(y+.369*math.cos(math.radians(a)),WZ+.369*math.sin(math.radians(a))) for a in range(15,181,15)]
  void_x('WholeIsolatedArch_'+arch,x,.222,hole,'entire isolated wheel-arch air, 1 mm radial margin and extending beyond both side mouths',[arch],True)

contact('CrossTie_0','OriginalShortCab',(0,0,1),(0,-1.82,.79),.089599,'complete front cross-tie top additionally bears the cab')
for i,x in enumerate([-.515,.515]):
 contact('ArchBracket_0_%d'%i,'OriginalShortCab',(0,0,1),(x,-1.40,.79),.020999,'complete overlap of front fender bracket top and cab bottom')
 contact('ArchBracket_1_%d'%i,'CurvedSaddle_1',(0,0,1),(x,1.33,.79),.013,'complete overlap of rear fender bracket top and rear saddle bottom')

# A genuinely new short five-sided front cab, held above the front wheel arches.
cabpoly=[(-2.04,.79),(-.82,.79),(-.82,1.75),(-1.69,1.75),(-2.04,1.17)]
cab=prism_x('OriginalShortCab',0,1.10,cabpoly,0,'one original solid short front shell, no internal driving compartment')
for i,x in enumerate([-.40,.40]):contact('Rail_%d'%i,cab,(0,0,1),(x,-1.35,.79),.16*1.10-.000001,'complete cab bearing strip on each rail')
WINDOWS=[]
def framed_pane(label,corners,normal):
 n=unit(normal);center=mul(tuple(map(sum,zip(*corners))),1/len(corners));inner=[add(center,mul(sub(p,center),.82)) for p in corners];pane=[add(center,mul(sub(p,center),.96)) for p in inner];k=len(corners)
 vs=[add(p,mul(n,d)) for d,poly in[(0,corners),(.042,corners),(.042,inner),(0,inner)] for p in poly]
 fs=[(r*k+i,r*k+(i+1)%k,((r+1)%4)*k+(i+1)%k,((r+1)%4)*k+i) for r in range(4) for i in range(k)]
 frame=mesh(label+'_ThickFrame',vs,fs,3,'true thick closed window frame with open inward recess')
 vs=[add(p,mul(n,d)) for d in[0,.012] for p in pane];fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 glass=mesh(label+'_RecessedPane',vs,fs,4,'12 mm thick opaque pane at the back of the real framed recess')
 mid=mul(add(mul(add(corners[0],corners[1]),.5),mul(add(inner[0],inner[1]),.5)),.5)
 contact(cab,frame,n,mid,.02,'whole window-frame back annulus against original cab face')
 contact(cab,glass,n,center,.05,'whole thick pane back against original cab face')
 # Complete recess free space: front prism plus all polygonal perimeter cells beside the pane.
 def probe(name,poly,d0,d1):
  vv=[add(p,mul(n,d)) for d in[d0,d1] for p in poly];kk=len(poly);ff=[tuple(reversed(range(kk))),tuple(kk+i for i in range(kk))]+[(i,(i+1)%kk,(i+1)%kk+kk,i+kk) for i in range(kk)]
  VOID_VOLUMES[name]={'vertices':vv,'faces':ff,'targets':None,'role':'complete framed-window recess free prism, with 1 mm boundary margin'}
 # Slight centroid scaling is an explicit finite frame margin; all outer free cells follow.
 u=unit(sub(corners[1],corners[0]));v=cross(n,u)
 def inset3(poly):
  pp=[(dot(sub(p,center),u),dot(sub(p,center),v)) for p in poly];q=inset_convex(pp,.001);assert q
  return [add(center,add(mul(u,a),mul(v,b))) for a,b in q]
 air=inset3(inner);probe(label+'_EntireFrontRecessAir',air,.013,.043)
 for i in range(k):
  poly=inset3([pane[i],pane[(i+1)%k],inner[(i+1)%k],inner[i]]);probe(label+'_SideAir_%d'%i,poly,.001,.011)
 WINDOWS.append({'frame':frame,'pane':glass})
for sign in[-1,1]:
 framed_pane(('Left' if sign<0 else 'Right')+'CabWindow',[(sign*.55,y,z) for y,z in[(-1.79,1.20),(-.94,1.20),(-.94,1.62),(-1.63,1.62),(-1.79,1.35)]],(sign,0,0))
# Windshield rests on the actual sloped forward cab plane.
frontn=unit((0,-.58,.35))
framed_pane('FrontWindshield',[(x,-2.04+.35*t,1.17+.58*t) for x,t in[(-.45,.14),(.45,.14),(.45,.87),(-.45,.87)]],frontn)
bumper=box('FrontBumper',(0,-2.08,.87),(1.22,.08,.13),3,'finite front bumper directly attached to cab vertical lower front')
contact(bumper,cab,(0,1,0),(0,-2.04,.87),.14,'whole bumper back against cab front')
for i,x in enumerate([-.40,.40]):
 lamp=box('FrontLamp_%d'%i,(x,-2.055,1.08),(.16,.03,.09),5,'fixed nonemissive lamp-shaped solid with its back on the cab')
 contact(lamp,cab,(0,1,0),(x,-2.04,1.08),.014399,'complete lamp back on cab front')

# Continuous original solid exterior tank: no interior capacity is supplied.
TCZ=1.44;RX=.68;RZ=.55;ANGLES=[math.radians(11.25+i*22.5) for i in range(16)]
section=[(RX*math.cos(a),TCZ+RZ*math.sin(a)) for a in ANGLES]
rings=[(-.64+.34*(1-math.cos(a)),math.sin(a)) for a in[math.pi/8,math.pi/4,3*math.pi/8,math.pi/2]]
rings += [(1.55,1.)]+[(1.55+.34*math.sin(a),math.cos(a)) for a in[math.pi/8,math.pi/4,3*math.pi/8]]
vs=[(0,-.64,TCZ)]+[(RX*fac*math.cos(a),y,TCZ+RZ*fac*math.sin(a)) for y,fac in rings for a in ANGLES]+[(0,1.89,TCZ)];fs=[];tags=[]
for i in range(16):fs.append((0,1+(i+1)%16,1+i));tags.append('front_closed_arc')
for k in range(len(rings)-1):
 for i in range(16):fs.append((1+k*16+i,1+k*16+(i+1)%16,1+(k+1)*16+(i+1)%16,1+(k+1)*16+i));tags.append('straight_shell' if k==3 else 'closed_arc')
end=len(vs)-1
for i in range(16):fs.append((end,1+(len(rings)-1)*16+i,1+(len(rings)-1)*16+(i+1)%16));tags.append('rear_closed_arc')
tank=mesh('ContinuousRoundedEndTank',vs,fs,1,'continuous solid elliptical exterior with multi-ring rounded front and rear ends; not a hollow working tank',tags)
# Both complete upper saddle polygons are the exact tank lower facets, not giant boxes penetrating it.
lower=sorted([section[i] for i in range(9,15)],key=lambda p:p[0])
for j,y in enumerate([-.05,1.30]):
 xz=[(lower[0][0],.79),(lower[-1][0],.79)]+list(reversed(lower));n=len(xz);vs=[(x,yy,z) for yy in[y-.11,y+.11] for x,z in xz];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 saddle=mesh('CurvedSaddle_%d'%j,vs,fs,3,'one continuous saddle whose entire five-facet concave upper surface exactly bears the tank lower curve');SADDLES.append(saddle)
 for i,x in enumerate([-.4,.4]):contact('Rail_%d'%i,saddle,(0,0,1),(x,y,.79),.16*.22-.000001,'complete finite saddle/rail bottom bearing rectangle')
 for k,(a,b) in enumerate(zip(lower,lower[1:])):
  dx,dz=b[0]-a[0],b[1]-a[1];normal=unit((-dz,0,dx));p=((a[0]+b[0])/2,y,(a[1]+b[1])/2)
  contact(saddle,tank,normal,p,.22*math.hypot(dx,dz)-.000001,'entire curved saddle upper facet %d, complete 0.22 m width'%k,points=[add(p,(0,d,0)) for d in[-.07,0,.07]])
topz=TCZ+RZ*math.cos(math.pi/16)
cap=box('FixedTopClosure',(0,.50,topz+.035),(.22,.24,.07),3,'one short fixed solid top closure with full lower face on the tank upper flat')
contact(tank,cap,(0,0,1),(0,.50,topz),.052799,'complete top-closure bottom on the full upper tank facet')

# True side cabinet: continuous thick back, floor, roof and side walls, open +X.
for j,y in enumerate([.38,.88]):
 b=box('CabinetBracket_%d'%j,(.485,y,.815),(.33,.10,.05),3,'finite cantilever-shaped connector visually linking the side cabinet to the rail')
 contact('Rail_1',b,(0,0,1),(.40,y,.79),.015999,'complete bracket base portion on rail')
 contact(b,'RecessedServiceCabinet',(0,0,1),(.625,y,.84),.004999,'whole cabinet bottom bracket tip bearing')
outer=[(.28,.84),(.98,.84),(.98,1.16),(.28,1.16)];inner=[(.33,.89),(.93,.89),(.93,1.11),(.33,1.11)]
vs=[(x,y,z) for x,poly in[(.60,outer),(.98,outer),(.98,inner),(.65,inner)] for y,z in poly];fs=[(3,2,1,0),(12,13,14,15)]
for k in range(3):
 for i in range(4):fs.append((4*k+i,4*k+(i+1)%4,4*(k+1)+(i+1)%4,4*(k+1)+i))
mesh('RecessedServiceCabinet',vs,fs,0,'continuous closed material shell with 50 mm back/floor/side/roof walls and a full 330 mm deep open service recess')
for j,y in enumerate([.45,.80]):
 outer=[(y+.047*math.cos(math.radians(22.5+i*45)),1+.047*math.sin(math.radians(22.5+i*45))) for i in range(8)];inner=[(y+.027*math.cos(math.radians(22.5+i*45)),1+.027*math.sin(math.radians(22.5+i*45))) for i in range(8)]
 vs=[(x,yy,z) for x,poly in[(.65,outer),(.755,outer),(.755,inner),(.685,inner)] for yy,z in poly];fs=[tuple(reversed(range(8))),tuple(24+i for i in range(8))]
 for k in range(3):
  for i in range(8):fs.append((k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i))
 n=mesh('BlindVisualSocket_%d'%j,vs,fs,3,'fixed octagonal blind-end visual socket, no fluid or working connection');BLIND_SOCKETS.append(n)
 contact('RecessedServiceCabinet',n,(1,0,0),(.65,y,1),.006,'complete blind socket rear disk on cabinet back wall')
 SECTIONS.extend([{'name':n,'x0':.65,'x1':.685,'loops':[outer]},{'name':n,'x0':.685,'x1':.755,'loops':[outer,inner]}])
 void_x('WholeBlindSocketAir_%d'%j,(.686+.756)/2,.070,inset_convex(inner,.001),'entire isolated finite blind socket hole beyond its mouth, with full closed bottom',[n],True)

# Exact complete service-cavity section sweep. It includes both socket bores and
# all air around them, not sparse witness boxes. The explicit intended cavity is
# X .65..98, Y .33..93, Z .89..1.11; all cells use 1 mm numerical boundary margins.
def crossing(loop,y):
 vals=[]
 for a,b in zip(loop,loop[1:]+loop[:1]):
  if min(a[0],b[0])<y<max(a[0],b[0]):m=(b[1]-a[1])/(b[0]-a[0]);vals.append((m,a[1]-m*a[0]))
 return vals
def solid_at(loops,y,z):return sum(sum(m*y+b>z for m,b in crossing(loop,y)) for loop in loops)%2==1
for ix,(x0,x1) in enumerate(zip([.65,.685,.755],[.685,.755,.981])):
 active=[s for s in SECTIONS if s['name'] in BLIND_SOCKETS and s['x0']<(x0+x1)/2<s['x1']]
 ys=sorted(set([.33,.93]+[p[0] for s in active for loop in s['loops'] for p in loop]))
 for iy,(y0,y1) in enumerate(zip(ys,ys[1:])):
  y=(y0+y1)/2;lines=sorted(set([(0,.89),(0,1.11)]+[q for s in active for loop in s['loops'] for q in crossing(loop,y)]),key=lambda q:q[0]*y+q[1])
  for iz,(bot,up) in enumerate(zip(lines,lines[1:])):
   z=((bot[0]+up[0])*y+bot[1]+up[1])/2
   if not .89<z<1.11 or any(solid_at(s['loops'],y,z) for s in active):continue
   poly=[(y0,bot[0]*y0+bot[1]),(y1,bot[0]*y1+bot[1]),(y1,up[0]*y1+up[1]),(y0,up[0]*y0+up[1])];clean=[]
   for p in poly:
    if not clean or math.dist(p,clean[-1])>1e-8:clean.append(p)
   if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-8:clean.pop()
   if len(clean)<3:continue
   poly=inset_convex(clean,.001)
   if not poly:continue
   name='WholeServiceCavity_%d_%02d_%d'%(ix,iy,iz);void_x(name,(x0+x1)/2,x1-x0-.002,poly,'complete service cabinet free-space partition cell including the blind socket interiors')
   SERVICE_PARTITION.append({'name':name,'x0':x0,'x1':x1,'yz_uninset':clean,'margin_m':.001,'nominal_free_volume_m3':abs(area2(clean))*.5*(x1-x0)})
for g in VOID_VOLUMES.values():g['targets']=list(G)
for j in range(2):
 for i in range(2):
  g=ISOLATED_VOID_VOLUMES['WholeIsolatedArch_Arch_%d_%d'%(j,i)]
  g['targets']=[n for n in G if n not in ['Wheel_%d_%d'%(j,i),'Hub_%d_%d'%(j,i),'FixedAxle_%d'%j]]
  g['role']='entire fixed wheel-arch aperture tested against every component except its three explicitly intended wheel, hub and axle occupants; their full fender separation is independently required'
TANKER_CONTRACT={'single_prop_count':1,'solid_exterior_tank_no_internal_cavity':True,'original_short_cab':1,'continuous_chassis_rails':2,'cross_ties':4,'fixed_axles':2,'ground_wheels':4,'real_wheel_arches':4,'whole_curved_saddles':2,'whole_saddle_facets':10,'recessed_service_cabinet':1,'fixed_blind_sockets':2,'whole_service_partition_cells':len(SERVICE_PARTITION),'whole_empty_volumes':len(VOID_VOLUMES),'isolated_arch_and_blind_volumes':len(ISOLATED_VOID_VOLUMES),'finite_opposed_contacts':len(CONTACTS)}
def measure_tanker_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 v=vertices['ContinuousRoundedEndTank'];assert abs(min(p[1] for p in v)+.64)<2e-7 and abs(max(p[1] for p in v)-1.89)<2e-7
 return dict(TANKER_CONTRACT,geometry_scope='actual complete source/exported coordinates; full contact, void, separation and real negative gates remain required')
FOCUS=(0,0,.95);ORTHO=5.30
CAMERAS={'gray-front3q':(6.8,-8.3,5.0),'gray-back3q':(-6.8,8.3,5.0),'thumbnail':(6.8,-8.3,5.0),'qa-front':(0,-9,3.7),'qa-side':(9,0,3.7),'qa-top':(0,0,9),'qa-back':(0,9,3.7),'qa-wireframe':(6.8,-8.3,5.0),'silhouette-128-front':(0,-9,3.7),'silhouette-128-side':(9,0,3.7)}
WIRE_THICKNESS=ORTHO/640


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
root=bpy.data.objects.new('OneCompactSaddleTankTruck',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='chassis centre ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.69,-1.4,WZ),(-.69,-1.4,.7)),('OriginalShortCab',(0,-1.2,1.3),(0,-1.2,1.8))]:
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_tanker_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'tanker_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/aviation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'aviation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
