"""Original low slotted desktop transceiver, side U cradle, fixed handmic and one continuous coiled lead; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-desktop-handmic-transceiver-kit-01';VERSION='1.0.0';TITLE='Desktop Handmic Transceiver'
DESCRIPTION=('One original static desktop communications appearance, counted as one prop. A low wide closed thick hollow teal shell has a sloping front, six true through-wall top slots and a distinct internal thick baffle separated from every slot by a complete air chamber. A recessed dark screen, large faceted tuning-style knob and five finite controls rest on the front. Four separate finite feet support the main body. A thick side U-shaped open cradle supports one upright flattened handmic on a finite lower face, with real shallow open sound slots and a fixed side pad; the remaining cradle clearance is empty. A single closed thick short lead connects the front socket to the mic underside with three separated turns and continuous curved strain-relief ends. Every component is fixed and the complete assembly is one prop. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. No textures, antenna, table, person, extra wiring scene, old portable-radio widening, extracted microphone or old console conversion. Static visual geometry only: no transmit/receive, audio, power, band, protocol, signal/electrical continuity, ventilation, plugging, microphone or control operation, cable elasticity, ergonomics, manufacturing, material suitability, electrical/RF/install safety or certification claim. No compatibility claim with old antennas, handhelds or cradles.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[]
BODY='LowHollowSlottedChassis';MIC='FixedSlottedHandmic';CRADLE='SideOpenUCradle';CABLE='OneContinuousShortCoiledLead';BACK='SeparatedInternalBaffle'
PALETTE=[('DeepPetrolShell',(.044,.195,.204,1),.46,.18),('CharcoalTrim',(.026,.034,.039,1),.57,.05),('SlateHandmic',(.10,.13,.14,1),.57,0),('WarmIvoryControls',(.73,.68,.51,1),.43,.08),('MutedTerracottaPad',(.47,.16,.071,1),.58,0),('DarkInsetScreen',(.012,.044,.047,1),.28,.02)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def within(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(within(p[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);break
  else:raise AssertionError(('untriangulable planar cell',p,order))
 out.append(tuple(order));return out

def prism(poly,z0,z1,material=0,role='',transform=None):
 n=len(poly);vv=[(x,y,z) for z in [z0,z1] for x,y in poly];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv] if transform else vv,ff,material,role)
def contact(name,a,b,origin,axis,plane,points,area,offset=.0005):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':origin,'u':u,'v':v,'axis':axis,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=list(G) if targets is None else targets,role=role)

# A conforming occupied-cell boundary makes one true closed hollow shell.
# No internal duplicate faces, booleans, black strips or imported geometry.
Z0=.028;Z1=.175;SLOPE=.044/(Z1-Z0)
def shell_map(p):
 x,y,z=p;return(x,y+SLOPE*(z-Z0)*(.145-y)/.295,z)
SLOT_CENTERS=[-.195,-.145,-.095,-.045,.005,.055]
xs=sorted(set([-.25,-.239,.139,.15]+[x+d for x in SLOT_CENTERS for d in [-.007,.007]]));ys=[-.15,-.139,0,.105,.134,.145];zs=[Z0,.039,.164,Z1]
occupied=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   shell=i in [0,len(xs)-2] or j in [0,len(ys)-2] or k in [0,len(zs)-2]
   vent=k==len(zs)-2 and j==2 and any(abs((xs[i]+xs[i+1])/2-c)<.0069 for c in SLOT_CENTERS)
   if shell and not vent:occupied.add((i,j,k))
v=[];f=[];lookup={}
def vertex(p):
 p=tuple(round(x,9) for x in p)
 if p not in lookup:lookup[p]=len(v);v.append(p)
 return lookup[p]
for i,j,k in sorted(occupied):
 cell=[shell_map((x,y,z)) for z in [zs[k],zs[k+1]] for y in [ys[j],ys[j+1]] for x in [xs[i],xs[i+1]]]
 for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
  if (i+delta[0],j+delta[1],k+delta[2]) not in occupied:f.append(tuple(vertex(cell[n]) for n in face))
G[BODY]=mesh(v,f,0,'One manifold low hollow thick shell with sloped front, six actual top slots and an inner chamber; shell walls and floor are continuous.')
for ix,x in enumerate([-.197,.097]):
 for iy,y in enumerate([-.091,.092]):
  name=f'FiniteFoot_{ix+1}_{iy+1}';G[name]=box((x-.026,y-.023,0),(x+.026,y+.023,Z0),1,'Finite full flat ground foot and finite full top support.');FEET.append(name)
  contact(name+'_BodySeat',name,BODY,(0,0,0),(0,0,1),Z0,[(x,y,Z0)],.0023)
for ix,x in enumerate([-.215,.075]):
 name=f'InternalBafflePedestal_{ix+1}';G[name]=box((x-.009,.048,.039),(x+.009,.094,.146),1,'Internal finite pedestal from chassis floor to baffle underside.')
 contact(name+'_Floor',BODY,name,(0,0,0),(0,0,1),.039,[(x,.07,.039)],.00080)
G[BACK]=box((-.228,.010,.146),(.088,.126,.152),1,'Distinct real thick baffle beneath all six slots, with a complete air chamber between baffle and top wall.')
for ix,x in enumerate([-.215,.075]):contact(f'BaffleSeat_{ix+1}',f'InternalBafflePedestal_{ix+1}',BACK,(0,0,0),(0,0,1),.146,[(x,.07,.146)],.00080)

# All front controls have a real finite face on the sloping shell.
THETA=math.atan(SLOPE);U=(1,0,0);V=(0,math.sin(THETA),math.cos(THETA));N=(0,-math.cos(THETA),math.sin(THETA));PANEL=(0,-.15,Z0)
def front(p):return add(PANEL,add(mul(U,p[0]),add(mul(V,p[1]),mul(N,p[2]))))
def front_contact(name,point,area):contact(name+'_PanelSeat',BODY,name,PANEL,N,0,[front((point[0],point[1],0))],area)
def ringrect(x0,x1,y0,y1,w,z0,z1,material,role,transform):
 outer=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)];inner=[(x0+w,y0+w),(x1-w,y0+w),(x1-w,y1-w),(x0+w,y1-w)];vv=[(x,y,z) for z in [z0,z1] for poly in [outer,inner] for x,y in poly];ff=[]
 for i in range(4):j=(i+1)%4;ff.extend([(i,j,8+j,8+i),(4+j,4+i,12+i,12+j),(j,i,4+i,4+j),(8+i,8+j,12+j,12+i)])
 return mesh([transform(p) for p in vv],ff,material,role)
G['RecessedScreenFrame']=ringrect(-.211,-.055,.062,.123,.008,0,.010,1,'True thick open screen rim with finite shell seat; screen face is recessed below rim.',front);front_contact('RecessedScreenFrame',(-.207,.092),.0031)
G['InsetDarkScreen']=box((-.202,.071,0),(-.064,.114,.004),5,'Solid dark inset plate, seated on shell, below open frame lip with full perimeter air gap.',front);front_contact('InsetDarkScreen',(-.13,.092),.0058)
def radial_profile(cx,cy,levels,material,role,transform,sides=24):
 vv=[(cx+r*math.cos(math.tau*i/sides),cy+r*math.sin(math.tau*i/sides),z) for r,z in levels for i in range(sides)];ff=[tuple(reversed(range(sides))),tuple(range(sides*(len(levels)-1),sides*len(levels)))]
 for j in range(len(levels)-1):
  for i in range(sides):k=(i+1)%sides;ff.append((j*sides+i,j*sides+k,(j+1)*sides+k,(j+1)*sides+i))
 return mesh([transform(p) for p in vv],ff,material,role)
G['LargeFacetedTuningKnob']=radial_profile(.007,.088,[(.024,0),(.031,.005),(.031,.021),(.027,.028)],3,'Large fixed faceted knob with full finite rear mounting face.',front);front_contact('LargeFacetedTuningKnob',(.007,.088),.00175)
G['KnobInsetFace']=radial_profile(.007,.088,[(.019,.028),(.019,.030)],1,'Fixed smaller knob-face disc on full finite cap.',front);contact('KnobFaceSeat','LargeFacetedTuningKnob','KnobInsetFace',PANEL,N,.028,[front((.007,.088,.028))],.0010)
for i,x in enumerate([-.19,-.141,-.092]):
 name=f'LowerKey_{i+1}';G[name]=box((x-.016,.020,0),(x+.016,.038,.009),3,'One fixed finite rectangular control.',front);front_contact(name,(x,.029),.00055)
for i,h in enumerate([.086,.115]):
 name=f'RightKey_{i+1}';G[name]=box((.080,h-.009,0),(.112,h+.009,.008),4 if i==1 else 1,'One fixed finite rectangular control.',front);front_contact(name,(.096,h),.00055)
G['FrontLeadSocket']=radial_profile(.102,.033,[(.014,0),(.014,.018)],1,'Solid closed fixed visual connector with finite rear face and finite cable end seat.',front,sides=16);front_contact('FrontLeadSocket',(.102,.033),.00058)

# U cradle is one thick connected open concave solid, attached at the chassis side.
uoutline=[(.15,.065),(.284,.065),(.284,.153),(.272,.153),(.272,.075),(.174,.075),(.174,.153),(.15,.153)]
def cradle_map(p):return(p[0],p[2],p[1])
G[CRADLE]=prism(uoutline,.024,.050,0,'One thick side U cradle, open at top/front, with actual bottom shelf and two separated side limbs.',cradle_map)
contact('CradleFullSideMount',BODY,CRADLE,(0,0,0),(1,0,0),.15,[(.15,.037,.11)],.0022)

# Blind sound slots in a solid bevel-cornered handmic, produced as exact planar
# boundary cells. This makes one connected closed shell with genuine pocket walls.
def octagon(x,y,a,b,ch):return [(x-a+ch,y-b),(x+a-ch,y-b),(x+a,y-b+ch),(x+a,y+b-ch),(x+a-ch,y+b),(x-a+ch,y+b),(x-a,y+b-ch),(x-a,y-b+ch)]
def pocketed_extrusion(outline,pockets,depth0,depth1,floor,transform,material,role):
 stations=sorted(set(round(x,9) for p in [outline]+pockets for x,y in p))
 def interval(poly,x):
  if x<min(a for a,b in poly)-1e-9 or x>max(a for a,b in poly)+1e-9:return None
  yy=[]
  for (a,u),(b,v) in zip(poly,poly[1:]+poly[:1]):
   if abs(b-a)<1e-11:
    if abs(x-a)<1e-9:yy.extend([u,v])
   elif min(a,b)-1e-9<=x<=max(a,b)+1e-9:yy.append(u+(v-u)*(x-a)/(b-a))
  return (min(yy),max(yy)) if yy else None
 def sheet(holes):
  pp=[];tt=[];lk={}
  def vid(p):
   p=tuple(round(c,9) for c in p)
   if p not in lk:lk[p]=len(pp);pp.append(p)
   return lk[p]
  def cell(a,b,al,bl,ah,bh):
   right=sorted(set(y for poly in holes for q in [interval(poly,b)] if q for y in q if bl+1e-9<y<bh-1e-9));left=sorted(set(y for poly in holes for q in [interval(poly,a)] if q for y in q if al+1e-9<y<ah-1e-9),reverse=True)
   p=[(a,al),(b,bl)]+[(b,y) for y in right]+[(b,bh),(a,ah)]+[(a,y) for y in left];q=[]
   for r in p:
    r=tuple(round(c,9) for c in r)
    if not q or q[-1]!=r:q.append(r)
   if q[0]==q[-1]:q.pop()
   if len(q)<3:return
   ids=[vid(p) for p in q];tt.extend(tuple(ids[j] for j in tri) for tri in earclip2(q))
  for a,b in zip(stations,stations[1:]):
   aa=interval(outline,a);bb=interval(outline,b);active=sorted((p for p in holes if min(x for x,y in p)<(a+b)/2<max(x for x,y in p)),key=lambda p:interval(p,(a+b)/2)[0]);al,bl=aa[0],bb[0]
   for p in active:
    lo,hi=interval(p,a);ll,hh=interval(p,b);cell(a,b,al,bl,lo,ll);al,bl=hi,hh
   cell(a,b,al,bl,aa[1],bb[1])
  return pp,tt
 vv=[];ff=[];lk={}
 def vf(p):
  p=tuple(round(c,9) for c in p)
  if p not in lk:lk[p]=len(vv);vv.append(p)
  return lk[p]
 def face(pp):ff.append(tuple(vf(p) for p in pp))
 pp,tt=sheet(pockets)
 for t in tt:face([(pp[i][0],pp[i][1],depth0) for i in reversed(t)])
 bp,bt=sheet([])
 for t in bt:face([(bp[i][0],bp[i][1],depth1) for i in t])
 counts=collections.Counter(tuple(sorted((a,b))) for t in tt for a,b in zip(t,t[1:]+t[:1]));edges=[(pp[a],pp[b]) for t in tt for a,b in zip(t,t[1:]+t[:1]) if counts[tuple(sorted((a,b)))]==1];pe={i:[] for i in range(len(pockets))}
 def on(p,a,b):return abs(cr2(sub(b,a),sub(p,a)))<1e-11 and min(a[0],b[0])-1e-9<=p[0]<=max(a[0],b[0])+1e-9 and min(a[1],b[1])-1e-9<=p[1]<=max(a[1],b[1])+1e-9
 for a,b in edges:
  mid=mul(add(a,b),.5);owner=next((i for i,p in enumerate(pockets) if any(on(mid,q,r) for q,r in zip(p,p[1:]+p[:1]))),None);end=depth1 if owner is None else floor
  face([(a[0],a[1],depth0),(b[0],b[1],depth0),(b[0],b[1],end),(a[0],a[1],end)])
  if owner is not None:pe[owner].append((a,b))
 for i,p in enumerate(pockets):
  centre=mul(tuple(map(sum,zip(*p))),1/len(p))
  for a,b in pe[i]:face([(centre[0],centre[1],floor),(a[0],a[1],floor),(b[0],b[1],floor)])
 return mesh([transform(p) for p in vv],ff,material,role)
mic_outline=octagon(.223,.145,.035,.070,.008);sound_z=[.149,.165,.181];sound_slots=[[(.201,z-.004),(.245,z-.004),(.245,z+.004),(.201,z+.004)] for z in sound_z]
def mic_map(p):return(p[0],p[2],p[1])
G[MIC]=pocketed_extrusion(mic_outline,sound_slots,-.023,.038,-.013,mic_map,2,'One flattened fixed handmic with three true finite blind sound slots, chamfered outline and full finite bottom cradle seat.')
contact('MicFiniteBottomShelf',CRADLE,MIC,(0,0,0),(0,0,1),.075,[(.223,.031,.075)],.00072)
G['FixedMicSidePad']=box((.258,-.009,.108),(.265,.023,.137),4,'Fixed side press-style pad; finite side face on the mic, no functional operation.')
contact('MicSidePadSeat',MIC,'FixedMicSidePad',(0,0,0),(1,0,0),.258,[(.258,.008,.122)],.00090)

# One swept closed cable, with exact endpoint cap normals and no disconnected
# segment. Three helical turns use original spacing and a continuous curved exit.
def bezier(a,b,c,d,n):return [add(add(mul(a,(1-t)**3),mul(b,3*(1-t)**2*t)),add(mul(c,3*(1-t)*t*t),mul(d,t**3))) for t in [i/n for i in range(n+1)]]
CABLE_RADIUS=.0045;pitch=.027;coil_r=.013;COIL_START=.130;COIL_END=.211;coil_y=-.203;coil_z=.046
start=front((.102,.033,.018));hs=(COIL_START,coil_y,coil_z-coil_r);he=(COIL_END,coil_y,coil_z-coil_r);end=(.223,-.006,.075);helix_tangent=unit((pitch/math.tau,-coil_r,0))
entry=bezier(start,add(start,mul(N,.022)),sub(hs,mul(helix_tangent,.018)),hs,14)
helix=[(COIL_START+pitch*t/math.tau,coil_y-coil_r*math.sin(t),coil_z-coil_r*math.cos(t)) for t in [math.tau*3*i/90 for i in range(91)]]
mid=(.252,-.19,.040)
exit_points=bezier(he,add(he,mul(helix_tangent,.042)),(.252,-.230,.040),mid,18)+bezier(mid,(.252,-.130,.040),sub(end,(0,0,.036)),end,24)[1:]
CABLE_PATH=entry+helix[1:]+exit_points[1:];CABLE_HELIX_RANGE=[len(entry)-1,len(entry)-1+90];sides=10;vv=[];ff=[];tangents=[];basis=[]
for i,p in enumerate(CABLE_PATH):
 tangent=N if i==0 else (0,0,1) if i==len(CABLE_PATH)-1 else unit(sub(CABLE_PATH[min(i+1,len(CABLE_PATH)-1)],CABLE_PATH[max(i-1,0)]));tangents.append(tangent)
 if i==0:r=(1,0,0)
 else:r=unit(sub(basis[-1][0],mul(tangent,dot(basis[-1][0],tangent))))
 s=cross(tangent,r);basis.append((r,s))
 for j in range(sides):a=math.tau*j/sides;vv.append(add(p,add(mul(r,CABLE_RADIUS*math.cos(a)),mul(s,CABLE_RADIUS*math.sin(a)))))
for i in range(len(CABLE_PATH)-1):
 for j in range(sides):k=(j+1)%sides;ff.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
ff.extend([tuple(reversed(range(sides))),tuple(range(sides*(len(CABLE_PATH)-1),sides*len(CABLE_PATH)))])
G[CABLE]=mesh(vv,ff,1,'One continuous closed thick short cable, three separated helical turns and continuously curved ends; full finite endpoint contacts.')
contact('LeadStartFiniteCap','FrontLeadSocket',CABLE,PANEL,N,.018,[start],.000058,.0003)
contact('LeadEndFiniteCap',CABLE,MIC,(0,0,0),(0,0,1),.075,[end],.000058,.0003)

# Complete finite air bodies: every top slot through its entire thickness, the
# full baffle-to-slot chamber, full sound pockets, screen rim and complete U gaps.
for i,c in enumerate(SLOT_CENTERS):
 air(f'TopSlotWholeAir_{i+1}',box((c-.0062,.001,.1632),(c+.0062,.104,.179),transform=shell_map),'Complete finite top-slot passage through the full thick wall and beyond both mouths; inset 0.8 mm from edges.')
 BORES.append({'mesh':BODY,'origin_m':shell_map((c,.05,.162)),'direction':unit(sub(shell_map((c,.05,.18)),shell_map((c,.05,.162)))),'length_m':.019})
air('WholeBaffleToSlotChamber',box((-.224,.024,.1528),(.084,.109,.1632)),'Complete broad finite air chamber above the full baffle and below all six through-slot mouths; no contact with backing plate or top wall.')
air('WholeLowerFrontHollowChamber',box((-.230,-.080,.040),(.130,.000,.162)),'Complete full-width lower front interior chamber, through its entire height, behind the sloped front and in front of baffle supports.')
for i,z in enumerate(sound_z):air(f'MicSoundPocketWholeAir_{i+1}',box((.2018,-.025,z-.0032),(.2442,-.0138,z+.0032)),'Entire finite blind sound pocket from outside the front mouth to 0.8 mm before its true floor; all corner/end walls included.')
air('CradleLeftWholeSideAir',box((.1748,.0248,.0758),(.1872,.0492,.1522)),'Entire left U opening side corridor over full support height, beyond mic rear and forward-facing U mouth, excluding only finite seat.')
air('CradleRightWholeSideAir',box((.2658,.0248,.0758),(.2712,.0492,.1522)),'Entire right U opening side corridor including fixed side pad envelope, all shelf-to-limb height.')
# Ring probe between actual screen edge and actual frame inner wall.
air('ScreenWholePerimeterAir',ringrect(-.2026,-.0634,.0704,.1146,.0002,.0008,.0088,0,'',front),'Continuous full screen perimeter gap; ring crosses screen height and reaches below rim with 0.4 mm component margin.')
SOLID_VOLUMES['ChassisFloorContinuousBridge']=dict(box((-.229,-.115,.029),(.129,.119,.038)),targets=[BODY],role='Whole thick chassis floor material connecting the four foot seats and internal support bases.')
SOLID_VOLUMES['CradleBottomContinuousBridge']=dict(box((.151,.025,.066),(.283,.049,.074)),targets=[CRADLE],role='Whole solid U bottom bridge connecting chassis-side limb to outer limb and full mic seat.')
SOLID_VOLUMES['MicSolidBehindSoundPocketFloors']=dict(box((.200,-.012,.143),(.246,.036,.187)),targets=[MIC],role='Whole substantial handmic body behind every actual shallow sound-slot floor.')

# Recenter the entire complete assembly in XY, retaining the real ground datum.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,SOLID_VOLUMES]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in BORES:r['origin_m']=sub(r['origin_m'],SHIFT)
CABLE_PATH=[sub(p,SHIFT) for p in CABLE_PATH]
CONTRACT={'single_prop_count':1,'true_thick_hollow_chassis':1,'through_top_slots':6,'distinct_separated_internal_baffle':1,'finite_ground_feet':4,'one_open_U_cradle':1,'fixed_handmic':1,'true_blind_sound_slots':3,'one_continuous_closed_short_lead':1,'separated_helical_turns':3,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES)}
def measure_transceiver_geometry(vertices):
 assert set(vertices)==set(G)
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<2e-7
 assert abs(min(p[2] for p in vertices[MIC])-.075)<2e-7
 assert min(p[2] for p in vertices[CABLE])>.025
 return dict(CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, air/material bodies, separation and independent actual negatives remain required')
INSIDE_TESTS=[(BODY,sub((-.245,0,.10),SHIFT),sub((-.12,-.03,.10),SHIFT)),(MIC,sub((.223,.012,.16),SHIFT),sub((.223,-.018,.165),SHIFT))]
FOCUS=(0,0,.103);ORTHO=.665
CAMERAS={'gray-front3q':(.65,-1,.62),'gray-back3q':(-.65,1,.68),'thumbnail':(.65,-1,.62),'qa-front':(0,-1,.43),'qa-side':(1,0,.43),'qa-top':(0,0,1),'qa-back':(0,1,.43),'qa-wireframe':(.65,-1,.62),'silhouette-128-front':(0,-1,.43),'silhouette-128-side':(1,0,.43)}
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
root=bpy.data.objects.new('OneDesktopTransceiverWithFixedHandmic',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_transceiver_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'transceiver_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
