"""Original tapered single-cavity tote with two opposed attached comb-edge lids; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='logistics-opposed-attached-lid-tote-01';VERSION='1.0.0';TITLE='Opposed Attached-Lid Tote'
DESCRIPTION=('One original static opposed attached-lid logistics tote form. A single continuous tapered thick shell has a complete bottom, real deep empty cavity, full rim and two genuine short-end handholes. Two complete thick half lids are fixed outward and upward at 62 degrees above the horizontal; their facing edges have alternating full-thickness comb teeth and actual open notches. Four three-knuckle assemblies have complete thick through-bored ears, continuous solid headed pins, finite lower pin-bearing faces and full nonbearing bore clearances. Eight broad body-ear pedestals and four independent fixed-angle wedge stops have finite full support patches from the rim to the ears and lids. Four full flat feet support the shell. Newly authored shell, opposed lids and support geometry; no reused produce-crate body, copied bait-box lid, deleted battery divider or recolored suitcase. One form only: the plural turnover-box family remains partial and the existing open produce crate remains reusable. Metres, native Z up, front -Y, horizontal bounds-centred ground origin. Constant opaque PBR only; no TEX_* nodes, linked Principled inputs, image/procedural textures, text, brand, animation or environment. Fixed visual geometry only: no opening/closing path, closing interlock, locking, stacking/nesting, load, transport suitability, food/hygiene, water/dust/air sealing, manufacturing/material, safety certification or old rack/pallet compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousTaperedDeepToteShell';LIDS=[];PINS=[];HINGES=[];STOPS=[];TEETH=[];NOTCHES=[]
PALETTE=[('MutedCobaltShell',(.075,.20,.30,1),.66,.02),('PaleBlueLids',(.22,.41,.49,1),.65,.02),('DarkBlueFeet',(.045,.085,.11,1),.73,.02),('WarmAlloyPins',(.49,.43,.31,1),.45,.48),('DeepBlueSupportWedges',(.08,.16,.20,1),.69,.02)]
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
# Original tapered single-cavity shell. Cartesian material boundary is mapped
# continuously to a shallow draft in both horizontal directions, keeping all
# faces planar and both complete short-end handholes genuinely through-open.
def transform_geometry(g,fn):return mesh([fn(p) for p in g['vertices']],g['faces'],g['material'],g['role'])
def draft(p):
 x,y,z=p;f=(z-.035)/.365;return(x*(.36+.06*f),y*(.23+.05*f),z)
def shell_geometry(inset=False):
 if inset:xs=[-.996,-.924,.924,.996];ys=[-.996,-.884,-.384,.384,.884,.996];zs=[.036,.072,.314,.354,.399];xi=.924;yi=.884;hh=.384;z0=.072;h0=.314;h1=.354
 else:xs=[-1,-.92,.92,1];ys=[-1,-.88,-.38,.38,.88,1];zs=[.035,.073,.315,.353,.40];xi=.92;yi=.88;hh=.38;z0=.073;h0=.315;h1=.353
 g=grid(xs,ys,zs,lambda x,y,z:z<z0 or abs(y)>yi or (abs(x)>xi and not(abs(y)<hh and h0<z<h1)),0,'One original continuous closed thick tapered material shell with complete floor, rim and real short-end handles.')
 return transform_geometry(g,draft)
G[BODY]=shell_geometry();solid('Shell_EntireContinuousThickMaterial',shell_geometry(True),[BODY],'Whole closed inset shell material, including complete bottom, all four tapered walls, continuous rim and the full material around both expanded handholes; at least 0.9 mm boundary inset.')
# Complete deep cavity continued vertically through its entire top mouth.
def cavity():
 rings=[(.074,.916*(.36+.06*(.074-.035)/.365),.876*(.23+.05*(.074-.035)/.365)),(.40,.916*.42,.876*.28),(.73,.916*.42,.876*.28)]
 vs=[(x*hx,y*hy,z) for z,hx,hy in rings for x,y in[(-1,-1),(1,-1),(1,1),(-1,1)]];fs=[(3,2,1,0),(8,9,10,11)]
 for k in range(2):
  for i in range(4):fs.append((4*k+i,4*k+(i+1)%4,4*(k+1)+(i+1)%4,4*(k+1)+i))
 return mesh(vs,fs)
air('Shell_WholeDeepCavityAndOpenMouth',cavity(),'Entire finite tapered inner cavity from 1 mm above the complete floor, through the whole rim mouth and above the two raised lids. Four walls inset by at least 0.9 mm; no sampled-ray substitute.')
for side in[-1,1]:
 lo,hi=(.916,1.006) if side>0 else(-1.006,-.916)
 air('Shell_WholeShortEndHandle_'+str(side),transform_geometry(box((lo,-.376,.316),(hi,.376,.352)),draft),'Whole finite handle air through and beyond the full tapered short-end wall, with complete long/short aperture edges and both mouths.')
for ix,x in enumerate([-.29,.29],1):
 for iy,y in enumerate([-.16,.16],1):
  n=f'CompleteFoot_{ix}_{iy}';G[n]=box((x-.04,y-.04,0),(x+.04,y+.04,.035),2,'Complete short finite flat foot beneath the full tote bottom.');FEET.append(n)
  contact(n+'_WholeShellSeat',n,BODY,(0,0,1),(x,y,.035),.006399)
  FOOT_CONTACTS.append({'mesh':n,'name':n+'_WholeGroundSole','x':x,'y':y,'half_x':.04,'half_y':.04,'minimum_area_m2':.006399})
  solid(n+'_EntireMaterial',inset_box((x-.04,y-.04,0),(x+.04,y+.04,.035)),[n],'Entire finite foot material from full ground sole through full shell seat, 1 mm inset.')
THETA=math.radians(62);C=math.cos(THETA);S=math.sin(THETA)
def frame(side,p):
 x,u,v=p;return(x,side*(.31+C*u-S*v),.47+S*u+C*v)
def direction(side,p):x,u,v=p;return(x,side*(C*u-S*v),S*u+C*v)
def posed(side,g):return transform_geometry(g,lambda p:frame(side,p))
def wedge(side,x0,x1,u0,u1,v,e=0):
 # This original wedge has its entire upper inclined face precisely
 # opposed to an ear or lid lower face, and a broad horizontal rim seat.
 p0=frame(1,(0,u0,v));p1=frame(1,(0,u1,v))
 poly=[(.25,.40),(p1[1],.40),(p1[1],p1[2]),(p0[1],p0[2])]
 if e:
  old=poly;poly=[]
  for i,p in enumerate(old):
   prev=old[i-1];nxt=old[(i+1)%len(old)];a=unit((-(p[1]-prev[1]),p[0]-prev[0]));b=unit((-(nxt[1]-p[1]),nxt[0]-p[0]));poly.append(add(p,mul(add(a,b),e/(1+dot(a,b)))))
  x0+=e;x1-=e
 return prism(poly,x0,x1,4,'Complete fixed wedge from a finite top-rim root to the full inclined bearing patch.',lambda p:(p[2],side*p[0],p[1]))
X=[round(-.41+.082*i,9) for i in range(11)]
for side,label in[(-1,'Front'),(1,'Rear')]:
 lid=label+'_CompleteCombHalfLid';LIDS.append(lid)
 bins=[i for i in range(10) if i%2==(0 if side<0 else 1)]
 def tooth(x):return any(X[i]<x<X[i+1] for i in bins)
 G[lid]=posed(side,grid(X,[.025,.23,.275],[-.012,.012],lambda x,u,v:u<.23 or tooth(x),1,'One complete original thick half lid with five integral full-thickness teeth and five real through-thickness notches. Fixed outward raised pose, no closure/interlock claim.'))
 # Connected complete inset slab with every tooth and its rooted bridge.
 boxes=[((-.409,.026,-.011),(.409,.229,.011))]+[((X[i]+.001,.228,-.011),(X[i+1]-.001,.274,.011)) for i in bins]
 solid(lid+'_WholeMaterialWithEveryTooth',posed(side,union_boxes(boxes)),[lid],'Whole finite inset half-lid material including its entire thick main slab and all five complete teeth with overlapping finite roots; 1 mm boundary inset.')
 for i in range(10):
  if i in bins:
   TEETH.append({'lid':lid,'side':side,'bin':i,'x0':X[i],'x1':X[i+1]})
  else:
   name=lid+'_WholeNotch_'+str(i);NOTCHES.append(name)
   air(name,posed(side,box((X[i]+.001,.231,-.014),(X[i+1]-.001,.277,.014))),'Entire genuine open notch through both lid faces and beyond the complete 45 mm tooth ends, 1 mm side/base inset.')
 for cx in[-.35,.35]:
  stop=label+'_FixedAngleStop_'+str(cx);G[stop]=wedge(side,cx-.022,cx+.022,.025,.06,-.012);STOPS.append({'mesh':stop,'lid':lid,'side':side,'x':cx})
  contact(stop+'_WholeRimRoot',BODY,stop,(0,0,1),(cx,side*.264,.4),.044*.03-.000001)
  contact(stop+'_WholeInclinedLidSeat',stop,lid,direction(side,(0,0,1)),frame(side,(cx,.0425,-.012)),.044*.035-.000001)
  solid(stop+'_EntireMaterial',wedge(side,cx-.022,cx+.022,.025,.06,-.012,.001),[stop],'Entire closed inset fixed-angle stop material across every finite root-to-seat section, exact 1 mm planar inward offsets.')
 # Full useful lower-panel clearance excludes only real independent stops.
 xx=sorted(set([-.409,.409]+[x+d for x in[-.35,.35] for d in[-.023,.023]]+X[1:-1]));uu=[.026,.061,.229,.274]
 below=grid(xx,uu,[-.034,-.013],lambda x,u,v:(u<.229 or tooth(x)) and not(any(abs(x-c)<.023 for c in[-.35,.35]) and u<.061))
 air(lid+'_EntireLowerFaceAir',posed(side,below),'Whole connected finite lower-lid clearance over the thick slab and teeth; only the two actual finite stop footprints plus 1 mm border are excluded. Explicit 1 mm underside inset.')
 air(lid+'_EntireUpperFaceAir',posed(side,grid(X,[.026,.229,.274],[.013,.035],lambda x,u,v:u<.229 or tooth(x))),'Whole connected finite upper-lid clearance over slab and comb teeth; 1 mm face inset, no overlap with hinges or opposing lid.')
 for hi,cx in enumerate([-.23,.23],1):
  pin=label+f'_Hinge_{hi}_ContinuousHeadedPin';PINS.append(pin);rings=[]
  pb=[((cx-.055,-.010,-.012),(cx+.055,.010,.008)),((cx-.064,-.016,-.018),(cx-.055,.016,.014)),((cx+.055,-.016,-.018),(cx+.064,.016,.014))]
  G[pin]=posed(side,union_boxes(pb,3,'One continuous full square pin with two integral thick end heads; fixed appearance, no rotation or retention-performance claim.'))
  for j,(lo,hi2) in enumerate(pb):solid(pin+'_WholeMaterial_'+str(j),posed(side,inset_box(lo,hi2)),[pin],'Entire finite shaft or end head material including the complete finite root to the shaft, 1 mm inset.')
  for part,a,b in [('Left',cx-.049,cx-.027),('Center',cx-.022,cx+.022),('Right',cx+.027,cx+.049)]:
   ring=label+f'_Hinge_{hi}_{part}TrueBoredEar';rings.append(ring);uo=.025 if part=='Center' else .022
   G[ring]=posed(side,grid([a,b],[-uo,-.012,.012,uo],[-.025,-.012,.012,.025],lambda x,u,v:not(abs(u)<.012 and abs(v)<.012),4,'Complete thick rectangular annular ear, genuine full 24 mm through-bore over the entire axial thickness.'))
   solid(ring+'_WholeAnnularMaterial',posed(side,grid([a+.001,b-.001],[-uo+.001,-.013,.013,uo-.001],[-.024,-.013,.013,.024],lambda x,u,v:not(abs(u)<.013 and abs(v)<.013))),[ring],'Whole inset closed annular ear material around all four bore walls and corners, 1 mm outer inset and expanded bore.')
   isolated(ring+'_WholeIsolatedBore',posed(side,box((a-.001,-.011,-.011),(b+.001,.011,.011))),[ring],'Whole isolated full-thickness ear bore extending beyond both mouths, 1 mm side inset.')
   contact(ring+'_WholeLowerPinBearing',ring,pin,direction(side,(0,0,1)),frame(side,((a+b)/2,0,-.012)),(b-a)*.020-.000001)
   if part=='Center':contact(ring+'_WholeLidRoot',ring,lid,direction(side,(0,1,0)),frame(side,(cx,.025,0)),(b-a)*.024-.000001)
   else:
    pedestal=ring+'_RimPedestal';G[pedestal]=wedge(side,a,b,-uo,uo,-.025)
    contact(pedestal+'_WholeRimRoot',BODY,pedestal,(0,0,1),((a+b)/2,side*.264,.4),(b-a)*.03-.000001)
    contact(pedestal+'_WholeEarUnderseat',pedestal,ring,direction(side,(0,0,1)),frame(side,((a+b)/2,0,-.025)),(b-a)*uo*2-.000001)
    solid(pedestal+'_WholeMaterial',wedge(side,a,b,-uo,uo,-.025,.001),[pedestal],'Whole finite inset pedestal material with complete top-ear and lower-rim root regions; exact 1 mm planar inward offsets.')
  # All nonbearing walls across all three bored ears, not only their centres.
  for lab,lo,hi2 in [('SideMinus',(cx-.050,-.0115,-.011),(cx+.050,-.0105,.011)),('SidePlus',(cx-.050,.0105,-.011),(cx+.050,.0115,.011)),('AbovePin',(cx-.050,-.010,.009),(cx+.050,.010,.011))]:
   air(pin+'_WholeNonbearingAir_'+lab,posed(side,box(lo,hi2)),'Complete finite nonbearing bore-wall corridor over all three ear thicknesses and both axial gaps; at least 0.5 mm to either actual boundary, intended lower bearing plane excluded.')
  for lab,a,b in [('LeftEnd',cx-.054,cx-.050),('GapLeft',cx-.026,cx-.023),('GapRight',cx+.023,cx+.026),('RightEnd',cx+.050,cx+.054)]:
   air(pin+'_WholeAxialClearance_'+lab,posed(side,grid([a,b],[-.024,-.011,.011,.024],[-.024,-.013,.009,.024],lambda x,u,v:not(abs(u)<.011 and -.013<v<.009))),'Complete finite axial gap around the continuous shaft between adjacent ears or between each end ear and its head. 1 mm axial/radial inset; no zero-area clearance substitute.')
  HINGES.append({'side':side,'rings':rings,'pin':pin,'lid':lid,'center_x':cx,'side_clearance_m':.002,'upper_clearance_m':.004,'axial_gap_m':.005})
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
SHIFT=(0,0,0)
CONTRACT={'single_prop_count':1,'tote_form_count':1,'plural_tote_family_complete':False,'continuous_tapered_single_cavity_shell':1,'complete_short_end_handholes':2,'complete_flat_feet':4,'fixed_outward_half_lids':2,'fixed_lid_inclination_degrees':62,'integral_comb_teeth':len(TEETH),'full_thickness_comb_notches':len(NOTCHES),'true_bored_ears':12,'continuous_headed_pins':4,'finite_angle_stops':4,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'motion_interlock_stacking_load_or_safety_claim':False}
def measure_attached_lid_tote_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-.4)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; complete finite empty/material domains, full bearing faces, self-intersection, all-pair separation and focused real negative gates required')
INSIDE_TESTS=[(BODY,(0,0,.05),(0,0,.20))]+[(n,frame(side,(0,.1,0)),frame(side,(0,.1,.03))) for side,n in zip([-1,1],LIDS)]
FOCUS=(0,0,.35);ORTHO=1.42
CAMERAS={'gray-front3q':(1.8,-2.8,2.4),'gray-back3q':(-1.8,2.8,2.4),'thumbnail':(1.8,-2.8,2.4),'qa-front':(0,-4,1.75),'qa-side':(4,0,1.75),'qa-top':(0,0,4),'qa-back':(0,4,1.75),'qa-wireframe':(1.8,-2.8,2.4),'silhouette-128-front':(0,-4,1.75),'silhouette-128-side':(4,0,1.75)}
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
root=bpy.data.objects.new('OneOpposedAttachedLidTote',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_attached_lid_tote_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'attached_lid_tote_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/logistics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'logistics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
