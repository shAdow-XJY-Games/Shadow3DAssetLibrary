"""One original fixed sleeve volleyball-post pair, compact display spacing, no net.
Metres, Z up, front -Y. Fixed static visual geometry, not sports equipment.
"""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-sleeve-volleyball-post-kit-01';VERSION='1.0.0';TITLE='Fixed Sleeve Volleyball Post Kit'
DESCRIPTION=('One original static visual volleyball-post kit: two independently grounded posts count together as one prop. Each broad base supports a genuinely hollow thick outer sleeve and a narrower inner post with a continuous integral finite height shoulder. A single solid transverse pin passes through real opposed sleeve holes and the real inner-post hole, with finite lower and upper bearing patches. The remaining sleeve air is preserved. Each post has a top twin-ear bracket, a genuinely grooved bored guide wheel and one continuous capped fixed axle. The main post carries an original compact double-ear bracket, bored empty spool, fixed axle and short attached crank grip; the secondary post carries a thick pierced tie eye. The two posts are positioned close together for display, not at competition installation spacing. No net, cable, tension route, court, animation, simulated rotation, adjustment, winding, ratchet mechanism or operational sports function. No competition dimensions, compatibility with an old net, tensile strength, structural stability, anti-tip performance, safety, installation or manufacturing certification is claimed. Every visible colour is constant opaque PBR; no procedural or image textures.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};EAR_PAIRS=[];EMPTY_PARTITION=[];PIN_SUPPORTS=[];SHOULDERS=[];BRACKET_ATTACH=[];HANDLE_ATTACH=[];SLEEVE_NAMES=[];INNER_NAMES=[];GROOVE_NAMES=[]
PALETTE=[('Sleeve_CourtTeal',(.035,.29,.32,1),.57,.22),('Post_CloudIvory',(.78,.81,.73,1),.56,.18),('Hardware_Graphite',(.055,.072,.077,1),.56,.35),('Wheel_SignalAmber',(.84,.39,.055,1),.46,.34)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def prism_geometry(x,width,yz):
 if area2(yz)<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return vs,fs

def prism_x(name,x,width,yz,mat,role):return mesh(name,*prism_geometry(x,width,yz),mat,role)
def box(name,lo,hi,mat,role):return mesh(name,cuboid(lo,hi),BOX_FACES,mat,role)
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0002,'points':points or [point],'scope':scope})
 return len(CONTACTS)-1

def void_box(name,lo,hi,scope,targets=None,isolated=False):
 g={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'targets':list(G) if targets is None else targets,'role':scope}
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]=g

def void_x(name,x,w,yz,scope,targets=None,isolated=False):
 vs,fs=prism_geometry(x,w,yz);g={'vertices':vs,'faces':fs,'targets':list(G) if targets is None else targets,'role':scope}
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]=g

def cell_mesh(name,xs,ys,zs,solid,offset,mat,role):
 occupied={(i,j,k) for i,j,k in itertools.product(range(len(xs)-1),range(len(ys)-1),range(len(zs)-1)) if solid((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 verts=[];lookup={};faces=[]
 def vertex(p):
  p=tuple(round(p[i]+offset[i],9) for i in range(3))
  if p not in lookup:lookup[p]=len(verts);verts.append(p)
  return lookup[p]
 sides=[((0,0,-1),(0,2,3,1)),((0,0,1),(4,5,7,6)),((0,-1,0),(0,1,5,4)),((0,1,0),(2,6,7,3)),((-1,0,0),(0,4,6,2)),((1,0,0),(1,3,7,5))]
 for i,j,k in sorted(occupied):
  vv=cuboid((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1]))
  for d,f in sides:
   if (i+d[0],j+d[1],k+d[2]) not in occupied:faces.append(tuple(vertex(vv[q]) for q in f))
 return mesh(name,verts,faces,mat,role)

HOLE=[(-.012,-.018),(.012,-.018),(.018,-.012),(.018,.012),(.012,.018),(-.012,.018),(-.018,.012),(-.018,-.012)]
SHAFT=[(-.008,-.018),(.008,-.018),(.011,-.011),(.011,.011),(.008,.018),(-.008,.018),(-.011,.011),(-.011,-.011)]
CAP=[(-.020,-.028),(.020,-.028),(.028,-.020),(.028,.020),(.020,.028),(-.020,.028),(-.028,.020),(-.028,-.020)]
def shifted(poly,y,z):return[(y+a,z+b) for a,b in poly]
def inset(poly,d):
 if area2(poly)<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  dy,dz=b[0]-a[0],b[1]-a[1];ln=math.hypot(dy,dz);n=(-dz/ln,dy/ln);lines.append((n[0],n[1],n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for i,(a,b,c) in enumerate(lines):
  d1,e,f=lines[i-1];det=a*e-b*d1
  if abs(det)<1e-12:continue
  out.append(((c*e-b*f)/det,(a*f-c*d1)/det))
 return out

def bored(name,x0,x1,out,y,z,mat,role):
 inner=shifted(HOLE,y,z);vs=[(x,yy,zz) for x in[x0,x1] for loop in[out,inner] for yy,zz in loop];fs=[];tags=[]
 for i in range(8):
  j=(i+1)%8
  for f,tag in [((i,j,16+j,16+i),'outer'),((8+j,8+i,24+i,24+j),'bore_floor' if i==0 else 'bore_ceiling' if i==4 else 'bore_nonbearing'),((i,8+i,8+j,j),'left'),((16+j,24+j,24+i,16+i),'right')]:fs.append(f);tags.append(tag)
 mesh(name,vs,fs,mat,role,tags)
 return {'name':name,'x0':x0,'x1':x1,'y':y,'z':z}

def axle(name,x0,x1,y,z,mat=2):
 rings=[(x0-.012,CAP),(x0,CAP),(x0,SHAFT),(x1,SHAFT),(x1,CAP),(x1+.012,CAP)];vs=[(x,yy,zz) for x,p in rings for yy,zz in shifted(p,y,z)];fs=[];tags=[]
 for k in range(5):
  for i in range(8):fs.append((k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i));tags.append('shaft_floor' if k==2 and i==0 else 'shaft_ceiling' if k==2 and i==4 else 'shaft_nonbearing' if k==2 else 'cap')
 fs += [tuple(reversed(range(8))),tuple(40+i for i in range(8))];tags+=['end','end'];mesh(name,vs,fs,mat,'one continuous solid fixed shaft with integral terminal shoulders, finite upper and lower flats and positive nonbearing side gaps',tags)
 return name

def wheel(name,cx,y,z,rings,mat,role):
 n=16
 inner=[p for i in range(8) for p in [HOLE[i],tuple((HOLE[i][j]+HOLE[(i+1)%8][j])/2 for j in range(2))]]
 # Two edges per octant have a regular circular exterior and an exact bored interior.
 outer=[(math.cos(-3*math.pi/4+math.tau*i/n),math.sin(-3*math.pi/4+math.tau*i/n)) for i in range(n)]
 vs=[(cx+x,y+r*a,z+r*b) for x,r in rings for a,b in outer]+[(cx+x,y+a,z+b) for x in[rings[-1][0],rings[0][0]] for a,b in inner];fs=[];tags=[];nr=len(rings)
 for k in range(nr-1):
  for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i));tags.append('groove' if 0<k<nr-2 else 'outer')
 for i in range(n):
  j=(i+1)%n
  fs.append(((nr-1)*n+i,(nr-1)*n+j,nr*n+j,nr*n+i));tags.append('end')
  fs.append((nr*n+i,nr*n+j,(nr+1)*n+j,(nr+1)*n+i));tags.append('bore_floor' if i in[0,1] else 'bore_ceiling' if i in[8,9] else 'bore_nonbearing')
  fs.append(((nr+1)*n+i,(nr+1)*n+j,j,i));tags.append('end')
 mesh(name,vs,fs,mat,role,tags)
 return {'name':name,'x0':cx+rings[0][0],'x1':cx+rings[-1][0],'y':y,'z':z}

def shaft_contacts(r,pin):
 name=r['name'];cx=(r['x0']+r['x1'])/2;y,z=r['y'],r['z'];area=(r['x1']-r['x0'])*.016-.0000001
 contact(name,pin,(0,0,1),(cx,y,z-.018),area,'complete finite lower shaft facet against the actual bore floor')
 contact(pin,name,(0,0,1),(cx,y,z+.018),area,'complete finite upper shaft facet against the actual bore ceiling')
 EAR_PAIRS.append({'ear':name,'pin':pin,'x0':r['x0'],'x1':r['x1'],'minimum_nonbearing_clearance_m':.003})
 BORES.append({'mesh':name,'origin_m':(r['x0']-.001,y,z),'direction':(1,0,0),'length_m':r['x1']-r['x0']+.002})
 void_x('FullIsolatedBore_'+name,cx,r['x1']-r['x0']+.002,inset(shifted(HOLE,y,z),.0008),'complete isolated true octagonal through-hole including both open mouths',[name],True)
 # Complete left and right bore-minus-shaft bodies, each connected and closed.
 for side,outer_indices,shaft_indices in [('Left',[0,7,6,5],[5,6,7,0]),('Right',[1,2,3,4],[4,3,2,1])]:
  poly=[(y+HOLE[i][0],z+HOLE[i][1]) for i in outer_indices]+[(y+SHAFT[i][0],z+SHAFT[i][1]) for i in shaft_indices]
  void_x('AssembledBoreGap_'+name+'_'+side,cx,r['x1']-r['x0']-.0012,inset(poly,.0006),'complete connected side crescent of bore minus shaft; uniform 0.6 mm boundary margin',[name,pin])

def channel_void(name,cx,y,z,profile,targets,role):
 profile=inset(profile,.0008);n=16;vs=[(cx+x,y+r*math.cos(-3*math.pi/4+math.tau*i/n),z+r*math.sin(-3*math.pi/4+math.tau*i/n)) for x,r in profile for i in range(n)];fs=[]
 for k in range(len(profile)):
  for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,((k+1)%len(profile))*n+(i+1)%n,((k+1)%len(profile))*n+i))
 VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'targets':targets,'role':role}

POSTS=[('Main',-.63,0),('Secondary',.63,.18)]
for prefix,cx,cy in POSTS:
 def p(x,y,z):return(cx+x,cy+y,z)
 foot=box(prefix+'_WideGroundBase',p(-.27,-.25,0),p(.27,.25,.08),2,'one broad finite flat ground base for this independent post');FEET.append(foot)
 sleeve=cell_mesh(prefix+'_ThickHollowSleeve',[-.08,-.063,.063,.08],[-.09,-.068,-.018,.018,.068,.09],[.08,1.26,1.284,1.30,1.50],lambda x,y,z:(abs(x)>.063 or abs(y)>.068) and not(abs(y)<.018 and 1.26<z<1.30),(cx,cy,0),0,'continuous thick open-ended sleeve with complete interior cavity and true aligned transverse pin openings');SLEEVE_NAMES.append(sleeve)
 contact(foot,sleeve,(0,0,1),p(.072,0,.08),.011663,'whole sleeve lower rim supported by the flat base',points=[p(.072,0,.08),p(-.072,0,.08),p(0,.079,.08),p(0,-.079,.08)])
 inner=cell_mesh(prefix+'_InnerPostWithShoulder',[-.082,-.055,.055,.082],[-.092,-.06,-.016,.016,.06,.092],[.70,1.25,1.26,1.284,1.50,1.54,2.30],lambda x,y,z:((abs(x)<.055 and abs(y)<.06) and not(abs(y)<.016 and 1.25<z<1.284)) or 1.50<z<1.54,(cx,cy,0),1,'one continuous narrower inner post with real transverse hole and integral full finite shoulder at its one fixed height');INNER_NAMES.append(inner)
 SHOULDERS.append(contact(sleeve,inner,(0,0,1),p(.072,0,1.5),.011663,'whole sleeve upper rim against the continuous inner-post shoulder underside',points=[p(.072,0,1.5),p(-.072,0,1.5),p(0,.079,1.5),p(0,-.079,1.5)]))
 pin=box(prefix+'_ContinuousHeightPin',p(-.10,-.012,1.26),p(.10,.012,1.284),3,'single unbroken solid transverse fixed pin through the two sleeve walls and real inner-post opening')
 for sx in[-1,1]:PIN_SUPPORTS.append(contact(sleeve,pin,(0,0,1),p(sx*.0715,0,1.26),.017*.024-.0000001,'complete pin lower facet borne by this sleeve-wall hole floor'))
 PIN_SUPPORTS.append(contact(pin,inner,(0,0,1),p(0,0,1.284),.11*.024-.0000001,'full upper transverse pin facet supports the true inner-post hole ceiling'))
 void_box('IsolatedCavity_'+prefix,p(-.0622,-.0672,.081),p(.0622,.0672,1.501),'entire isolated sleeve cavity open through both ends',[sleeve],True)
 void_box('IsolatedSleevePinHole_'+prefix,p(-.081,-.0172,1.2608),p(.081,.0172,1.2992),'whole opposed true sleeve pin hole, including the intervening cavity',[sleeve],True)
 void_box('IsolatedInnerPinHole_'+prefix,p(-.056,-.0152,1.2508),p(.056,.0152,1.2832),'whole actual inner-post transverse hole',[inner],True)
 for label,sx in[('Left',-1),('Right',1)]:
  yz=[(cy+y,z) for y,z in[(-.018,1.26),(-.012,1.26),(-.012,1.284),(.012,1.284),(.012,1.26),(.018,1.26),(.018,1.30),(-.018,1.30)]]
  void_x('AssembledSleevePinHoleAir_'+prefix+'_'+label,cx+sx*.0715,.0158,inset(yz,.0006),'entire remaining U-shaped side-wall pin opening, full hole-minus-solid-pin cross-section',[sleeve,pin,inner])

 # Complete actual remaining sleeve chamber, partitioned only at solid boundaries.
 xs=[-.063,-.055,.055,.063];ys=[-.068,-.06,-.016,-.012,.012,.016,.06,.068];zs=[.08,.70,1.25,1.26,1.284,1.50]
 free=set()
 for i,j,k in itertools.product(range(3),range(7),range(5)):
  x,y,z=(xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2
  inside_inner=abs(x)<.055 and abs(y)<.06 and z>.70 and not(abs(y)<.016 and 1.25<z<1.284)
  inside_pin=abs(y)<.012 and 1.26<z<1.284
  if not inside_inner and not inside_pin:free.add((i,j,k))
 count=0
 while free:
  i,j,k=min(free);ii,jj,kk=i+1,j+1,k+1
  while (ii,j,k) in free:ii+=1
  while all((a,jj,k) in free for a in range(i,ii)):jj+=1
  while all((a,b,kk) in free for a in range(i,ii) for b in range(j,jj)):kk+=1
  free-=set(itertools.product(range(i,ii),range(j,jj),range(k,kk)))
  name='SleeveAir_'+prefix+'_%02d'%count;count+=1
  lo=p(xs[i]+.0006,ys[j]+.0006,zs[k]+.0006);hi=p(xs[ii]-.0006,ys[jj]-.0006,zs[kk]-.0006)
  void_box(name,lo,hi,'complete merged rectangular free cell of sleeve chamber; 0.6 mm boundary and partition margin',[sleeve,inner,pin,foot]);EMPTY_PARTITION.append({'name':name,'nominal_box':(p(xs[i],ys[j],zs[k]),p(xs[ii],ys[jj],zs[kk])),'boundary_margin_m':.0006})
 top=box(prefix+'_TopBridge',p(-.08,-.08,2.30),p(.08,.08,2.34),0,'thick transverse top bridge connects the actual post top to both guide-wheel ears')
 contact(inner,top,(0,0,1),p(0,0,2.30),.11*.12-.0000001,'whole inner-post top against underside of top bridge')
 ears=[]
 for label,sx in[('Left',-1),('Right',1)]:
  x=cx+sx*.060;out=shifted([(-.050,-.130),(.050,-.130),(.065,-.115),(.065,.050),(.050,.065),(-.050,.065),(-.065,.050),(-.065,-.115)],cy,2.47)
  r=bored(prefix+'_Top'+label+'Ear',x-.010,x+.010,out,cy,2.47,0,'one thick guide bracket ear with a true through-hole and a finite complete lower attachment');ears.append(r)
  contact(top,r['name'],(0,0,1),(x,cy,2.34),.02*.10-.0000001,'whole ear bottom against top bridge')
 w=wheel(prefix+'_GroovedGuideWheel',cx,cy,2.47,[(-.04,.105),(-.028,.105),(-.02,.075),(.02,.075),(.028,.105),(.04,.105)],3,'one real polygonal annular guide wheel with complete recessed circumferential channel and an actual bored hub')
 ax=axle(prefix+'_FixedTopAxle',cx-.07,cx+.07,cy,2.47)
 for r in ears+[w]:shaft_contacts(r,ax)
 for r,sx in[(ears[0],-1),(ears[1],1)]:
  contact(ax,r['name'],(1,0,0),(cx-.07,cy+.024,2.47),.0010,'full left cap annular shoulder against guide-ear outer face',points=[(cx-.07,cy+.024,2.47),(cx-.07,cy-.024,2.47)]) if sx<0 else contact(r['name'],ax,(1,0,0),(cx+.07,cy+.024,2.47),.0010,'full right guide-ear face against cap shoulder',points=[(cx+.07,cy+.024,2.47),(cx+.07,cy-.024,2.47)])
 # One connected closed full annular groove body includes both sloping flanks.
 name='WholeGuideChannel_'+prefix
 channel_void(name,cx,cy,2.47,[(-.028,.105),(-.020,.075),(.020,.075),(.028,.105)],[w['name'],ax]+[r['name'] for r in ears],'entire circumferential guide channel including both sloped shoulders, uniformly inset 0.8 mm from actual profile')
 GROOVE_NAMES.append(name)

# Original compact post-hung empty spool, not a miniature ground ratchet winch.
cx,cy=-.63,0;back=box('Main_SpoolBackplate',(cx-.10,-.12,.85),(cx+.10,-.09,1.07),2,'thick compact post-hung backplate at the main sleeve front')
BRACKET_ATTACH.append(contact('Main_ThickHollowSleeve',back,(0,-1,0),(cx,-.09,.96),.16*.22-.0000001,'whole plate middle strip against solid front sleeve wall'))
ears=[]
for label,sx in[('Left',-1),('Right',1)]:
 x=cx+sx*.08;out=[(-.335,.88),(-.135,.88),(-.12,.895),(-.12,1.025),(-.135,1.04),(-.335,1.04),(-.35,1.025),(-.35,.895)]
 r=bored('Main_Spool'+label+'Ear',x-.01,x+.01,out,-.25,.96,2,'one original forward-pointing thick spool bracket ear with a real octagonal shaft hole');ears.append(r)
 contact(back,r['name'],(0,-1,0),(x,-.12,.96),.02*.13-.0000001,'entire rear ear flat connects to the compact backplate')
w=wheel('Main_EmptyBoredSpool',cx,-.25,.96,[(-.05,.075),(-.04,.075),(-.035,.042),(.035,.042),(.04,.075),(.05,.075)],1,'one empty bored polygonal spool with two flanges and a genuinely recessed full winding region; no rope or winding claim')
ax=axle('Main_FixedSpoolAxle',cx-.09,cx+.09,-.25,.96)
for r in ears+[w]:shaft_contacts(r,ax)
contact(ax,ears[0]['name'],(1,0,0),(cx-.09,-.226,.96),.0010,'complete left spool-axle cap shoulder against outer bracket ear',points=[(cx-.09,-.226,.96),(cx-.09,-.274,.96)])
contact(ears[1]['name'],ax,(1,0,0),(cx+.09,-.226,.96),.0010,'complete right bracket ear against spool-axle cap shoulder',points=[(cx+.09,-.226,.96),(cx+.09,-.274,.96)])
arm=box('Main_FixedShortCrankArm',(cx+.102,-.262,.947),(cx+.122,-.238,1.095),3,'short thick static crank arm attaches to the finite outer end of the continuous spool axle')
HANDLE_ATTACH.append(contact(ax,arm,(1,0,0),(cx+.102,-.25,.971),.0009,'finite axle-cap end against lower crank-arm side'))
grip=box('Main_CrankEndGrip',(cx+.122,-.264,1.070),(cx+.205,-.236,1.095),2,'compact thick fixed grip attached over a full finite patch at the upper arm end')
HANDLE_ATTACH.append(contact(arm,grip,(1,0,0),(cx+.122,-.25,1.082),.024*.025-.0000001,'whole overlap of grip end and crank arm face'))
channel_void('WholeEmptySpoolWindingRegion',cx,-.25,.96,[(-.04,.075),(-.035,.042),(.035,.042),(.04,.075)],[w['name'],ax]+[r['name'] for r in ears],'entire empty circumferential spool winding region including both sloped flange roots; uniform 0.8 mm actual-profile inset')
# Secondary thick pierced tie eye and its finite attachment tab.
cx,cy=.63,.18;tab=box('Secondary_TieEyeTab',(cx-.045,cy-.13,.96),(cx+.045,cy-.09,1.04),0,'one compact thick tie-eye tab meeting the secondary sleeve front over a finite face')
contact('Secondary_ThickHollowSleeve',tab,(0,-1,0),(cx,cy-.09,1.0),.09*.08-.0000001,'entire tab back face against secondary sleeve front')
out=shifted([(-.04,-.05),(.04,-.05),(.055,-.035),(.055,.035),(.04,.05),(-.04,.05),(-.055,.035),(-.055,-.035)],cy-.185,1.0)
eye=bored('Secondary_TruePiercedTieEye',cx-.0175,cx+.0175,out,cy-.185,1.0,3,'one genuine thick pierced tie eye with an open octagonal through-hole')
contact(tab,eye['name'],(0,-1,0),(cx,cy-.13,1.0),.035*.07-.0000001,'whole finite rear eye flat connects to front of mounting tab')
void_x('FullTieEyeOpening',cx,.037,inset(shifted(HOLE,cy-.185,1.0),.0008),'complete real tie-eye opening, including both mouths',list(G))
BORES.append({'mesh':eye['name'],'origin_m':(cx-.019,cy-.185,1.0),'direction':(1,0,0),'length_m':.038})
VOLLEYBALL_CONTRACT={'single_prop_count':1,'independent_posts':2,'display_only_spacing_m':1.26,'wide_ground_bases':2,'genuine_hollow_sleeves':2,'continuous_inner_posts_with_integral_shoulders':2,'continuous_height_pins':2,'genuine_top_guide_wheels':2,'compact_empty_post_spool':1,'short_crank_grip':1,'true_pierced_tie_eye':1,'finite_opposed_contacts':len(CONTACTS),'complete_sleeve_air_partition_cells':len(EMPTY_PARTITION),'finite_empty_volumes':len(VOID_VOLUMES),'isolated_hole_volumes':len(ISOLATED_VOID_VOLUMES),'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_volleyball_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in SLEEVE_NAMES:assert abs(max(p[2] for p in vertices[n])-1.5)<2e-7
 return dict(VOLLEYBALL_CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, whole empty regions, all noncontact surfaces and real mutations required')
FOCUS=(0,.05,1.29);ORTHO=3.50
CAMERAS={'gray-front3q':(4.8,-7,4.1),'gray-back3q':(-4.8,7,4.1),'thumbnail':(4.8,-7,4.1),'qa-front':(0,-7.5,3.3),'qa-side':(7.5,-.6,3.3),'qa-top':(0,.05,8.0),'qa-back':(0,7.5,3.3),'qa-wireframe':(4.8,-7,4.1),'silhouette-128-front':(0,-7.5,3.3),'silhouette-128-side':(7.5,-.6,3.3)}
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
root=bpy.data.objects.new('OneFixedVolleyballPostPair',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='design ground datum (0,0,0); actual AABB (-0.90,-0.35,0) to (0.90,0.43,2.575) m; Y bounds midpoint 0.04 m';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.63,0,.04),(-.63,0,.10)),('Main_ThickHollowSleeve',(-.558,0,.5),(-.63,0,.5))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Finite support and true openings are checked against actual generated mesh triangles.
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
mount_evidence=measure_volleyball_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'volleyball_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
