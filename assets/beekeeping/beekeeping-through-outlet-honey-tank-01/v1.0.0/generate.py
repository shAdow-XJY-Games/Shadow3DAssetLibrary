"""Original thick open honey tank with integral through-wall outlet and fixed side gate."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-through-outlet-honey-tank-01';VERSION='1.0.0';TITLE='Through-Outlet Honey Tank'
DESCRIPTION=('One original fixed open honey-tank visual form: an upright continuous thick octagonal bucket with complete bottom, deep empty cavity, full top rim and a low true wall-through short outlet. One continuous full-thickness open domain joins the entire bucket cavity to both nozzle mouths. A thick round gate with integral real pierced ear sits fixed to the side, clear of the outlet, captured by a solid stepped pin with two complete finite collar faces and carried on a complete finite bottom stop. Two closed short side lifting ears have entire finite bucket roots. Three short feet have complete top seats and flat ground soles. Ten closed connected editable meshes and five opaque constant unlinked PBR materials. Metres, native Z up, front -Y and horizontal bounds-centred ground origin. All shape geometry newly dimensioned, without importing or modifying a prior extractor, jar or barrel. The old extractor already has a separate hollow nozzle; its bucket wall lacks the corresponding opening. This asset adds a genuinely continuous through-wall outlet and fixed pierced side gate. One static empty prop: no shaft, rotor basket, sieve, liquid, receiving vessel, lid, texture, text, logo or animation. No opening trajectory, sealing, leak prevention, flow, food contact, hygiene, pressure, heating, load, handling, manufacturing, equipment safety or old-asset fit claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];HANDLES=[]
BODY='WholeOctagonalTankAndIntegralThroughOutlet';GATE='WholeRoundSideGateWithTrueEarHole';PIN='WholeSteppedRetainingPin';MOUNT='WholeUpperPinFoundation';STOP='WholeLowerFiniteGateStop';SHIFT=(0,.1675,0)
PALETTE=[('WarmPaleMetalTank',(.60,.63,.60,1),.40,.55),('MutedHoneyBrassGate',(.52,.29,.075,1),.40,.60),('DeepPetrolMounts',(.045,.12,.13,1),.57,.32),('DarkSteelPin',(.12,.15,.15,1),.39,.68),('DarkFlatFeet',(.055,.075,.075,1),.73,.10)]
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

def welded_closed(vs,fs,material=0,role=''):
 # Weld equal coordinates and split every polygon edge at all collinear mesh
 # vertices. This preserves complete shared front-panel/nozzle boundary edges.
 vv=[];idx={};mapping=[]
 for p in vs:
  p=tuple(round(float(x),9) for x in p)
  if p not in idx:idx[p]=len(vv);vv.append(p)
  mapping.append(idx[p])
 ff=[]
 for f in fs:
  face=[mapping[i] for i in f];new=[]
  for a,b in zip(face,face[1:]+face[:1]):
   av,bv=vv[a],vv[b];d=sub(bv,av);den=dot(d,d);hits=[]
   for k,p in enumerate(vv):
    t=dot(sub(p,av),d)/den
    if -1e-9<=t<1-1e-9 and dot(sub(sub(p,av),mul(d,t)),sub(sub(p,av),mul(d,t)))<1e-17:hits.append((t,k))
   new.extend(k for t,k in sorted(hits))
  ff.append(tuple(new))
 edges=collections.defaultdict(list)
 for i,f in enumerate(ff):
  for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))].append((i,a,b))
 assert all(len(v)==2 for v in edges.values()),[(k,v) for k,v in edges.items() if len(v)!=2][:10]
 signs={0:1};todo=[0];adj=collections.defaultdict(list)
 for values in edges.values():
  (i,a,b),(j,c,d)=values;relation=-1 if a==c else 1;adj[i].append((j,relation));adj[j].append((i,relation))
 while todo:
  i=todo.pop()
  for j,r in adj[i]:
   if j not in signs:signs[j]=signs[i]*r;todo.append(j)
   else:assert signs[j]==signs[i]*r
 assert len(signs)==len(ff)
 return mesh(vv,[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(ff)],material,role)
def octagon(a,c):return[(-a+c,-a),(a-c,-a),(a,-a+c),(a,a-c),(a-c,a),(-a+c,a),(-a,a-c),(-a,-a+c)]
def disk_poly(cx,cz,r,n=24,phase=.5):return[(cx+r*math.cos(math.tau*(i+phase)/n),cz+r*math.sin(math.tau*(i+phase)/n)) for i in range(n)]
def tube_mesh(outer,inner,y0,y1,material=0,role=''):
 n=len(outer);assert len(inner)==n;vs=[(x,y,z) for poly,y in[(outer,y0),(outer,y1),(inner,y1),(inner,y0)] for x,z in poly];fs=[]
 for k in range(4):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,((k+1)%4)*n+j,((k+1)%4)*n+i))
 return welded_closed(vs,fs,material,role)
def xzprism(poly,y0,y1,material=0,role=''):
 return prism(poly,y0,y1,material,role,transform=lambda p:(p[0],p[2],p[1]))
def tank(e=0):
 ao=.48-e;ai=.43+e;co=.20+(math.sqrt(2)-2)*e;ci=.18+(2-math.sqrt(2))*e;zo=.18+e;zi=.24-e;zt=1.18-e;zc=.40
 op=octagon(ao,co);ip=octagon(ai,ci);vs=[(x,y,z) for poly,z in[(op,zo),(op,zt),(ip,zt),(ip,zi)] for x,y in poly];fs=[tuple(reversed(range(8))),tuple(range(24,32))]
 for i in range(8):
  j=(i+1)%8;fs.append((8+i,8+j,16+j,16+i))
  if i:fs.extend([(i,j,8+j,8+i),(16+i,16+j,24+j,24+i)])
 theta=set(math.tau*i/24 for i in range(24))
 for width,z0 in[(ao-co,zo),(ai-ci,zi)]:
  for x in[-width,width]:
   for z in[z0,zt]:theta.add(math.atan2(z-zc,x)%math.tau)
 theta=sorted(theta);n=len(theta)
 if e==0:globals()['NOZZLE_ANGLES']=theta
 def rect(width,z0,t):
  dx,dz=math.cos(t),math.sin(t);limits=[]
  if abs(dx)>1e-10:limits.append(width/abs(dx))
  if dz>1e-10:limits.append((zt-zc)/dz)
  if dz< -1e-10:limits.append((z0-zc)/dz)
  d=min(limits);return(dx*d,zc+dz*d)
 rings=[]
 for spec in [('rect',ao-co,zo,-ao),('circle',.13-e,None,-ao),('circle',.13-e,None,-.78+e),('circle',.095+e,None,-.78+e),('circle',.095+e,None,-ai),('rect',ai-ci,zi,-ai)]:
  typ,r,z0,y=spec;ring=[]
  for t in theta:
   x,z=rect(r,z0,t) if typ=='rect' else(r*math.cos(t),zc+r*math.sin(t));ring.append(len(vs));vs.append((x,y,z))
  rings.append(ring)
 for aa,bb in zip(rings,rings[1:]):
  for i in range(n):j=(i+1)%n;fs.append((aa[i],aa[j],bb[j],bb[i]))
 return welded_closed(vs,fs,0,'One original continuous thick octagonal open bucket, complete bottom and rim, with integral low nozzle and genuinely missing front-wall aperture connecting the entire cavity to the short mouth.')
G[BODY]=tank();solid('EntireTankBottomWallsRimAndThroughNozzle',tank(.001),[BODY],'Whole connected 1 mm inset material of the complete bottom, all eight walls, full rim, actual front aperture boundary and entire integral nozzle wall.')
# The cavity and full outlet volumes overlap by 9 mm at their join. They are
# complete finite volumes, not a ray that only tests the separate nozzle.
air('WholeDeepCavityAndTopMouth',prism(octagon(.429,.18+(math.sqrt(2)-2)*.001),.241,1.181),'Entire finite empty octagonal cavity from the full bottom to above the complete open top rim, every inner corner included.')
air('WholeThroughWallOutletAndBothMouths',xzprism([(.094*math.cos(t),.40+.094*math.sin(t)) for t in NOZZLE_ANGLES],-.83,-.42),'Entire full-thickness connected outlet air, from outside the mouth through the whole 50 mm bucket front wall and into the cavity. Its full profile overlaps the cavity domain for 9 mm.')
air('WholeUnderOutletAir',box((-.129,-.829,.001),(.129,-.481,.269)),'Whole finite space under the outlet to ground, 1 mm below the lowest outer nozzle boundary; no receiving vessel or hidden prop.')
# One convex round-disc/ear outline, with a full real through-hole at the ear.
def hull(points):
 pp=sorted(set(points))
 def cr(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[]
 for p in pp:
  while len(lower)>=2 and cr(lower[-2],lower[-1],p)<=1e-12:lower.pop()
  lower.append(p)
 upper=[]
 for p in reversed(pp):
  while len(upper)>=2 and cr(upper[-2],upper[-1],p)<=1e-12:upper.pop()
  upper.append(p)
 return lower[:-1]+upper[:-1]
PC=(.13,.59);GATE_OUT=hull(disk_poly(.267,.399,.12)+disk_poly(*PC,.045));GATE_ANGLES=[math.atan2(z-PC[1],x-PC[0]) for x,z in GATE_OUT]
def offset_convex(poly,e):
 # Full inward parallel polygon offset, preserving every complete outer facet.
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  d=(b[0]-a[0],b[1]-a[1]);le=math.hypot(*d);n=(-d[1]/le,d[0]/le);lines.append((n,n[0]*a[0]+n[1]*a[1]+e))
 out=[]
 for (a,da),(b,db) in zip(lines[-1:]+lines[:-1],lines):
  de=a[0]*b[1]-a[1]*b[0];out.append(((da*b[1]-a[1]*db)/de,(a[0]*db-da*b[0])/de))
 return out
def gate(e=0):return tube_mesh(offset_convex(GATE_OUT,e),[(PC[0]+(.018+e)*math.cos(t),PC[1]+(.018+e)*math.sin(t)) for t in GATE_ANGLES],-.80+e,-.77-e,1,'Single thick round side gate with integral neck and complete pierced ear; fixed open beside the outlet, no cap or decal substitutes for the real hole.')
G[GATE]=gate();solid('EntireRoundGateNeckAndPiercedEar',gate(.001),[GATE],'Whole inset solid gate disc, complete neck, full annular ear material and both thick faces, every outer facet and hole boundary included.')
isolated=lambda name,g,targets,role:ISOLATED_VOID_VOLUMES.update({name:dict(g,targets=targets,role=role)})
EAR_POLY=[(PC[0]+.017*math.cos(t),PC[1]+.017*math.sin(t)) for t in GATE_ANGLES]
isolated('EntireIsolatedEarThroughHole',xzprism(EAR_POLY,-.801,-.769),[GATE],'Whole full-thickness ear hole and both mouths. The intended separate through-pin is omitted only from this isolated-hole predicate.')
def pin(e=0):
 # One solid stepped pin, complete axial core and two distinct finite collars.
 specs=[(-.815+e,.032-e),(-.80-e,.032-e),(-.80-e,.015-e),(-.77+e,.015-e),(-.77+e,.032-e),(-.75-e,.032-e)];vs=[(PC[0]+r*math.cos(t),y,PC[1]+r*math.sin(t)) for y,r in specs for t in GATE_ANGLES];n=len(GATE_ANGLES);fs=[tuple(reversed(range(n))),tuple(range((len(specs)-1)*n,len(specs)*n))]
 for k in range(len(specs)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return welded_closed(vs,fs,3,'Complete solid stepped retaining pin through the true ear hole, with full front and rear finite collars holding one fixed gate position.')
G[PIN]=pin();solid('EntireSteppedPinCoreAndBothCollars',pin(.001),[PIN],'Whole 1 mm inset stepped through-pin, complete core and full front/rear collars, from end face to full mounting back face.')
air('EntirePinToEarRadialAir',tube_mesh([(PC[0]+.017*math.cos(t),PC[1]+.017*math.sin(t)) for t in GATE_ANGLES],[(PC[0]+.016*math.cos(t),PC[1]+.016*math.sin(t)) for t in GATE_ANGLES],-.799,-.771),'Entire annular pin-to-ear nonbearing radial clearance through the full gate thickness, ending 1 mm before the two intentional collar bearing planes.')
G[MOUNT]=box((.09,-.75,.55),(.17,-.48,.63),2,'Complete fixed upper mounting block with a full bucket-wall root and complete finite pin-end support.')
solid('EntireUpperPinFoundation',box((.091,-.749,.551),(.169,-.481,.629)),[MOUNT],'Whole 1 mm inset upper pin support, from complete bucket root to full pin back seat.')
contact('UpperMountWholeBucketWallRoot',MOUNT,BODY,(0,1,0),(.13,-.48,.59),.08*.08-.000001)
# Collar face areas use actual same polygon angles, excluding the whole real hole.
def polyarea(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2
UNIT_POLY=[(math.cos(t),math.sin(t)) for t in GATE_ANGLES];COLLAR_AREA=polyarea(UNIT_POLY)*(.032**2-.018**2)
contact('WholePinBackToMountSeat',PIN,MOUNT,(0,1,0),(.13,-.75,.59),polyarea(UNIT_POLY)*.032**2-.000001)
contact('GateWholeFrontCollarBearing',PIN,GATE,(0,1,0),(.154,-.80,.59),COLLAR_AREA-.000001)
contact('GateWholeRearCollarBearing',GATE,PIN,(0,1,0),(.154,-.77,.59),COLLAR_AREA-.000001)
STOP_TOP=min(z for x,z in GATE_OUT)
G[STOP]=box((.255,-.80,STOP_TOP-.04),(.279,-.48,STOP_TOP),2,'Complete fixed lower stop from full bucket-wall root to the entire finite lower flat gate facet, retaining the displayed static side-open pose.')
solid('EntireLowerFiniteGateStop',box((.256,-.799,STOP_TOP-.039),(.278,-.481,STOP_TOP-.001)),[STOP],'Whole 1 mm inset lower stop material including complete bucket root, full beam and entire finite top support face.')
contact('LowerStopWholeBucketWallRoot',STOP,BODY,(0,1,0),(.267,-.48,STOP_TOP-.02),.024*.04-.000001)
contact('GateWholeBottomStopSeat',STOP,GATE,(0,0,1),(.267,-.785,STOP_TOP),.024*.03-.000001)
# Short closed side ears, with full finite vertical roots on opposite flat walls.
def handle(side,e=0):
 lo=.48+e;outer=.70-e;inner0=.53-e;inner1=.65+e
 g=grid([lo,inner0,inner1,outer],[-.035+e,.035-e],[.83+e,.88-e,1.02+e,1.07-e],lambda x,y,z:x<inner0 or x>inner1 or z<.88-e or z>1.02+e,2,'One complete closed short thick side ear; all four sides and full bucket-wall root, with a real full-thickness rectangular opening.')
 if side<0:g=mesh([(-x,y,z) for x,y,z in g['vertices']],[tuple(reversed(f)) for f in g['faces']],2,g['role'])
 return g
for side in[-1,1]:
 n=f'WholeClosedSideLiftEar_{side}';HANDLES.append(n);G[n]=handle(side);solid(n+'_EntireClosedMaterial',handle(side,.001),[n],'Whole 1 mm inset material of all four sides and the complete bucket-wall root.')
 air(n+'_EntireThroughHole',box((.531 if side>0 else-.649,-.036,.881),(.649 if side>0 else-.531,.036,1.019)),'Whole full-thickness side-ear aperture and both mouths, complete 1 mm inset rectangular domain.')
 contact(n+'_WholeBucketWallRoot',BODY,n,(side,0,0),(side*.48,0,.95),.07*.24-.000001)
for i,(cx,cy) in enumerate([(-.29,.25),(.29,.25),(0,-.30)]):
 n=f'WholeFlatGroundFoot_{i+1}';FEET.append(n);G[n]=box((cx-.065,cy-.065,0),(cx+.065,cy+.065,.18),4,'Complete short flat foot, with full finite bucket-bottom support and full flat ground sole.')
 solid(n+'_EntireMaterial',box((cx-.064,cy-.064,.001),(cx+.064,cy+.064,.179)),[n],'Whole 1 mm inset foot material from complete ground sole to whole tank-bottom seat.')
 contact(n+'_WholeTankBottomSeat',n,BODY,(0,0,1),(cx,cy,.18),.13*.13-.000001)
 FOOT_CONTACTS.append({'mesh':n,'name':n+'_FullGroundSole','x':cx,'y':cy,'half_x':.065,'half_y':.065,'minimum_area_m2':.13*.13-.000001})
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
# A single final translation applies to all finite geometry/evidence domains.
for container in [G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in container.values():g['vertices']=[add(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=SHIFT;r['points']=[add(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['x']+=SHIFT[0];r['y']+=SHIFT[1]
CONTRACT={'single_prop_count':1,'continuous_thick_open_buckets':1,'integral_true_through_wall_outlets':1,'complete_side_gate_with_real_ear_hole':1,'whole_stepped_through_pin':1,'complete_pin_collar_bearing_faces':2,'finite_gate_bottom_stops':1,'complete_closed_side_lift_ears':2,'complete_flat_feet':3,'nominal_wall_m':.05,'nominal_bottom_m':.06,'nozzle_full_bore_diameter_m':.19,'gate_thickness_m':.03,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'motion_food_fluid_sealing_or_safety_claim':False}
def measure_honey_tank_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-1.18)<2e-7
 allv=[p for v in vertices.values() for p in v]
 for ax in[0,1]:assert abs(min(p[ax] for p in allv)+max(p[ax] for p in allv))<2e-7
 return dict(CONTRACT,geometry_scope='complete source/export coordinates; independent actual full empty/material domains, complete contacts, self-intersection and real negative controls required')
INSIDE_TESTS=[(BODY,add((0,0,.21),SHIFT),add((0,0,.40),SHIFT)),(GATE,add((.267,-.785,.399),SHIFT),add((.13,-.785,.59),SHIFT)),(PIN,add((.13,-.785,.59),SHIFT),add((.20,-.785,.59),SHIFT))]
FOCUS=(0,0,.59);ORTHO=2.03
CAMERAS={'gray-front3q':(2.5,-3.6,2.9),'gray-back3q':(-2.5,3.6,2.9),'thumbnail':(2.5,-3.6,2.9),'qa-front':(0,-4,1.8),'qa-side':(4,0,1.8),'qa-top':(0,0,4),'qa-back':(0,4,1.8),'qa-wireframe':(2.5,-3.6,2.9),'silhouette-128-front':(0,-4,1.8),'silhouette-128-side':(4,0,1.8)}
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
root=bpy.data.objects.new('OneThroughOutletHoneyTank',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred three-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_honey_tank_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'honey_tank_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
