"""Original single full-height changing locker: long chamber, real rod and fixed open louver door. One static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-vented-full-height-changing-locker-01';VERSION='1.0.0';TITLE='Full-Height Vented Changing Locker'
DESCRIPTION=('One original single-column full-height changing locker, counted as one static prop. A thick continuous shell has a complete back, floor, two sides, roof and one integral upper hat shelf, leaving a long empty hanging chamber below. A fixed square-section hanging rod has two finite end supports and two original thick J-shaped fixed hooks. A separate full-height thick door is fixed open at 90 degrees, with two real through-windows and six outward-sloping thick louvers supported at both finite ends; all eight remaining louver openings are truly empty through the whole door thickness. Two original three-ear true-through-bored vertical hinge assemblies have continuous square pins with integral finite support shoulders, complete lateral air clearance and two fixed finite angle stops. Four complete flat feet support the shell; one thick open grip has two finite door roots. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. All geometry is original, opaque constant PBR; no textures, clothing, person, bench, scenery, multi-column cabinet array, old pantry shelf deletion, old postal-bay merging or recoloring. Static visual appearance only: no practical hanging capacity, load, stability, anti-tip, door motion/closing path, lock/security, airflow/ventilation, human enclosure or changing suitability, public-facility, material, manufacture, installation, hygiene or safety/certification claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];HINGES=[];LOUVERS=[];HOOKS=[];STOPS=[];OBSTACLES=[]
BODY='ContinuousFullHeightLongChamberShell';DOOR='FixedOpenThickLouverDoor';ROD='FullWidthFixedHangingRod'
PALETTE=[('MutedMarineBlue',(.10,.23,.29,1),.56,.10),('LouverBlue',(.16,.32,.37,1),.55,.10),('WarmPaleInterior',(.54,.58,.51,1),.67,.04),('DullAlloyHardware',(.33,.38,.37,1),.48,.52),('GraphiteFootAndGrip',(.045,.060,.060,1),.70,.03)]
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
# One conforming continuous closed shell with integral upper shelf. No old cabinet geometry.
G[BODY]=grid([-.32,-.295,.295,.32],[-.28,.255,.28],[.08,.112,1.62,1.645,1.895,1.92],lambda x,y,z:abs(x)>.295 or y>.255 or z<.112 or z>1.895 or 1.62<z<1.645,0,'Continuous full back, floor, side walls, roof and one integral hat shelf; uninterrupted lower long hanging chamber.')
# Pale constant material on actual inward-facing shell/shelf surfaces only.
G[BODY]['face_materials']=[]
for f in G[BODY]['faces']:
 pts=[G[BODY]['vertices'][i] for i in f]
 interior=any(all(abs(p[k]-level)<1e-8 for p in pts) for k,level in [(0,-.295),(0,.295),(1,.255),(2,.112),(2,1.62),(2,1.645),(2,1.895)])
 G[BODY]['face_materials'].append(2 if interior else 0)
for ix,x in enumerate([-.255,.255]):
 for iy,y in enumerate([-.205,.205]):
  n=f'FullFlatFoot_{ix+1}_{iy+1}';G[n]=box((x-.045,y-.045,0),(x+.045,y+.045,.08),4,'One complete flat ground foot, full 90 mm square finite upper shell seat.');FEET.append(n);contact(n+'_ShellSeat',n,BODY,(0,0,1),(x,y,.08),.008099)
for label,lo,hi in [('Floor',(-.319,-.279,.081),(.319,.279,.111)),('Back',(-.319,.256,.081),(.319,.279,1.919)),('Left',(-.319,-.279,.081),(-.296,.254,1.919)),('Right',(.296,-.279,.081),(.319,.254,1.919)),('Roof',(-.319,-.279,1.896),(.319,.279,1.919)),('IntegralHatShelf',(-.294,-.279,1.621),(.294,.254,1.644))]:solid('CompleteShellMaterial_'+label,box(lo,hi),[BODY],'Whole finite material slab of '+label+', 1 mm boundary inset; all internal thickness and corner connections included.')
# Two short solid side pads and complete end faces support one actual long rod.
for side,label in [(-1,'Left'),(1,'Right')]:
 x0,x1=(-.295,-.26) if side<0 else (.26,.295);n='RodEndSupport_'+label;lo=(x0,-.078,1.465);hi=(x1,-.002,1.531);G[n]=box(lo,hi,3,'Finite side-wall pad ending at complete hanging-rod end plane.');OBSTACLES.append((lo,hi))
 contact(n+'_Wall',BODY,n,(-side,0,0),(side*.295,-.04,1.498),.005015)
 if side<0:contact('RodLeftFullEnd',n,ROD,(1,0,0),(-.26,-.04,1.498),.000783)
 else:contact('RodRightFullEnd',ROD,n,(1,0,0),(.26,-.04,1.498),.000783)
lo=(-.26,-.054,1.484);hi=(.26,-.026,1.512);G[ROD]=box(lo,hi,3,'Single original square-section hanging rod with two full finite end bearings.');OBSTACLES.append((lo,hi))
for i,cx in enumerate([-.12,.12]):
 boxes=[((cx-.012,-.052,1.414),(cx+.012,-.028,1.484)),((cx-.012,-.104,1.414),(cx+.012,-.052,1.434)),((cx-.012,-.104,1.434),(cx+.012,-.084,1.459))]
 n=f'FixedJHook_{i+1}';G[n]=union_boxes(boxes,3,'One original continuous thick J hook with a complete upper face finitely seated under the rod and a real open throat.');HOOKS.append(n);OBSTACLES.extend(boxes)
 contact(n+'_RodSeat',n,ROD,(0,0,1),(cx,-.04,1.484),.000575)
# Full useful long cavity including all of the area around rod/pads/hooks: one
# conforming inset air-body union, subtracting exact expanded component boxes.
airlo=(-.294,-.279,.113);airhi=(.294,.254,1.619);expanded=[(tuple(x-.001 for x in lo),tuple(x+.001 for x in hi)) for lo,hi in OBSTACLES]
stations=[sorted(set([airlo[k],airhi[k]]+[p[k] for lo,hi in expanded for p in [lo,hi] if airlo[k]<p[k]<airhi[k]])) for k in range(3)]
air('CompleteLongHangingChamber',grid(*stations,lambda x,y,z:not any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in expanded)),'One entire connected finite long-chamber air body, including all recesses beside and below each J hook and around both rod ends; 1 mm inset at actual surfaces.')
air('CompleteUpperHatCubby',box((-.294,-.279,1.646),(.294,.254,1.894)),'Whole full-width upper hat-cubby empty finite volume; complete side, floor, roof and back coverage with 1 mm inset.')
# Door perpendicular to cabinet front. The two windows are actual omitted cells.
WINDOWS=[(.27,.52),(1.34,1.59)]
G[DOOR]=grid([-.38,-.35],[-.92,-.84,-.38,-.30],[.112,.27,.52,1.34,1.59,1.895],lambda x,y,z:not(-.84<y<-.38 and any(a<z<b for a,b in WINDOWS)),1,'One full-height thick closed door panel with two genuine through-windows, fixed open at 90 degrees.')
for label,lo,hi in [('LeftRail',(-.379,-.919,.113),(-.351,-.841,1.894)),('RightRail',(-.379,-.379,.113),(-.351,-.301,1.894)),('Bottom',(-.379,-.839,.113),(-.351,-.381,.269)),('Middle',(-.379,-.839,.521),(-.351,-.381,1.339)),('Top',(-.379,-.839,1.591),(-.351,-.381,1.894))]:solid('CompleteDoorMaterial_'+label,box(lo,hi),[DOOR],'Entire finite thick door '+label+' material region around the full window edges.')
def blade_z(x,c):return c-.45*(x+.375)
def xz_prism(poly,y0,y1,mat=1,role=''):return prism(poly,y0,y1,mat,role,lambda p:(p[0],p[2],p[1]))
for wi,(z0,z1) in enumerate(WINDOWS):
 centres=[z0+.055,z0+.125,z0+.195]
 for i,c in enumerate(centres):
  poly=[(-.403,blade_z(-.403,c)-.008),(-.347,blade_z(-.347,c)-.008),(-.347,blade_z(-.347,c)+.008),(-.403,blade_z(-.403,c)+.008)]
  n=f'Window_{wi+1}_OutwardSlopedLouver_{i+1}';G[n]=xz_prism(poly,-.84,-.38,1,'One complete thick outward-sloped louver with full finite contacts at both window edges, projecting beyond both door faces.');LOUVERS.append(n)
  contact(n+'_OuterEnd',DOOR,n,(0,1,0),(-.365,-.84,blade_z(-.365,c)),.000479)
  contact(n+'_InnerEnd',n,DOOR,(0,1,0),(-.365,-.38,blade_z(-.365,c)),.000479)
 for i in range(4):
  x0,x1=-.405,-.345
  low=lambda x: z0+.001 if i==0 else blade_z(x,centres[i-1])+.009
  high=lambda x: z1-.001 if i==3 else blade_z(x,centres[i])-.009
  poly=[(x0,low(x0)),(x1,low(x1)),(x1,high(x1)),(x0,high(x0))]
  air(f'Window_{wi+1}_WholeThroughSlit_{i+1}',xz_prism(poly,-.839,-.381),'Entire finite sloping empty strip between neighboring louvers or full window edge; spans beyond both door faces and the full width with 1 mm inset.')
# Grip is one thick continuous C, with two finite roots on exterior door face.
handle_boxes=[((-.425,-.887,.83),(-.38,-.861,.86)),((-.425,-.887,.98),(-.38,-.861,1.01)),((-.445,-.887,.83),(-.425,-.861,1.01))]
G['FullOpenDoorGrip']=union_boxes(handle_boxes,4,'One thick continuous open grip; both standoff end faces finitely touch the door exterior.')
contact('GripTwoFullDoorRoots',DOOR,'FullOpenDoorGrip',(-1,0,0),(-.38,-.874,.845),.001559,points=[(-.38,-.874,.845),(-.38,-.874,.995)])
air('CompleteGripOpening',box((-.424,-.886,.861),(-.381,-.862,.979)),'Entire finite grip opening between both roots, full thickness and reach, 1 mm inset.')
# Two original coaxial three-ear hinges. Every ear has a true square through bore.
def ear(z0,z1):
 outer=[(-.398,-.283),(-.332,-.283),(-.332,-.217),(-.398,-.217)];inner=[(-.381,-.266),(-.349,-.266),(-.349,-.234),(-.381,-.234)];vv=[(x,y,z) for z,poly in [(z0,outer),(z1,outer),(z0,inner),(z1,inner)] for x,y in poly];ff=[]
 for i in range(4):j=(i+1)%4;ff.extend([(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)])
 return mesh(vv,ff,3,'One complete closed thick ear with a full vertical square through-bore; all annular material and both end faces are real.')
for j,c in enumerate([.40,1.53]):
 names=[]
 for label,a,b in [('Lower',c-.068,c-.042),('Center',c-.033,c+.033),('Upper',c+.042,c+.068)]:
  n=f'Hinge_{j+1}_{label}TrueBoredEar';G[n]=ear(a,b);names.append(n)
  air(n+'_WholeIsolatedBore',box((-.380,-.265,a-.001),(-.350,-.235,b+.001)),'Full finite true ear bore extending beyond both end mouths, checked against the complete isolated ear.',[n])
  if label!='Center':
   br=n+'_BodyBridge';G[br]=box((-.332,-.263,a+.003),(-.32,-.237,b-.003),3,'Finite bridge between complete ear outer side and cabinet side wall.')
   contact(br+'_Ear',n,br,(1,0,0),(-.332,-.25,(a+b)/2),.026*(b-a-.006)-1e-8);contact(br+'_Wall',br,BODY,(1,0,0),(-.32,-.25,(a+b)/2),.026*(b-a-.006)-1e-8)
  else:
   tongue=f'Hinge_{j+1}_DoorTongue';G[tongue]=box((-.38,-.30,c-.018),(-.35,-.283,c+.018),3,'Finite complete tongue between door hinge edge and central true-bored ear.')
   contact(tongue+'_Door',DOOR,tongue,(0,1,0),(-.365,-.30,c),.001079);contact(tongue+'_Ear',tongue,n,(0,1,0),(-.365,-.283,c),.001079)
 pin=f'Hinge_{j+1}_ContinuousShoulderedPin';pinboxes=[((-.377,-.262,c-.074),(-.353,-.238,c+.080)),((-.390,-.275,c-.042),(-.340,-.225,c-.033)),((-.390,-.275,c+.068),(-.340,-.225,c+.080))];G[pin]=union_boxes(pinboxes,3,'One continuous square through-pin with integral lower support shoulder and upper head; positive full lateral bore clearance.')
 # Complete square annular overlap is 0.05^2 - 0.032^2.
 contact(pin+'_LowerEarSeat',names[0],pin,(0,0,1),(-.386,-.25,c-.042),.001475)
 contact(pin+'_CenterEarSupport',pin,names[1],(0,0,1),(-.386,-.25,c-.033),.001475)
 contact(pin+'_UpperEarHead',names[2],pin,(0,0,1),(-.386,-.25,c+.068),.001475)
 for label,lo,hi in [('Left',(-.380,-.265,c-.073),(-.378,-.235,c+.067)),('Right',(-.352,-.265,c-.073),(-.350,-.235,c+.067)),('Front',(-.377,-.265,c-.073),(-.353,-.263,c+.067)),('Back',(-.377,-.237,c-.073),(-.353,-.235,c+.067))]:
  # The integral shoulder deliberately occupies the inter-ear support interval.
  for k,(a,b) in enumerate([(c-.073,c-.043),(c-.032,c+.067)]):
   lo=list(lo);hi=list(hi);lo[2]=a;hi[2]=b;air(f'Hinge_{j+1}_CompleteLateralBoreAir_{label}_{k+1}',box(lo,hi),'Entire finite lateral pin-to-bore air partition; integral axial shoulder interval excluded as the intended finite bearing.')
 HINGES.append({'ears':names,'pin':pin,'center_z_m':c,'through_bore_size_m':.032,'square_pin_width_m':.024,'lateral_clearance_m':.004,'whole_finite_annular_seat_area_m2':.001476})
for j,z in enumerate([.18,1.78]):
 n=f'FixedDoorAngleStop_{j+1}';G[n]=box((-.35,-.34,z),(-.32,-.22,z+.03),3,'One complete finite fixed-angle stop with a cabinet-side root and a finite door inside-face contact; unique static pose only.');STOPS.append(n)
 contact(n+'_Wall',n,BODY,(1,0,0),(-.32,-.25,z+.015),.001799)
 contact(n+'_Door',DOOR,n,(1,0,0),(-.35,-.32,z+.015),.001199)
# Include every completed assembly mesh in whole-assembly void certificates.
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
# Recenter entire asset in XY without altering its exact ground datum.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,SOLID_VOLUMES]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in BORES:r['origin_m']=sub(r['origin_m'],SHIFT)
CONTRACT={'single_prop_count':1,'continuous_full_height_shell':1,'integral_upper_hat_shelf':1,'long_main_hanging_chamber':1,'full_width_rod':1,'rod_end_supports':2,'fixed_J_hooks':2,'fixed_open_full_height_door':1,'real_through_windows':2,'sloped_thick_louvers':6,'whole_through_slit_air_bodies':8,'vertical_three_ear_hinges':2,'true_through_bored_ears':6,'continuous_shouldered_pins':2,'finite_fixed_angle_stops':2,'flat_ground_feet':4,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'safety_or_airflow_claim':False}
def measure_locker_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-1.92)<2e-7
 assert abs(min(p[2] for p in vertices[DOOR])-.112)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; whole void/material volumes, full contacts, positive nonseat separation and real negative gates remain required')
INSIDE_TESTS=[(BODY,sub((-.307,0,1),SHIFT),sub((0,0,1),SHIFT)),(DOOR,sub((-.365,-.6,.8),SHIFT),sub((-.365,-.6,.295),SHIFT))]
FOCUS=(0,0,.96);ORTHO=2.70
CAMERAS={'gray-front3q':(3,-5,3.7),'gray-back3q':(-3,5,3.7),'thumbnail':(3,-5,3.7),'qa-front':(0,-6,2.5),'qa-side':(6,0,2.5),'qa-top':(0,0,6),'qa-back':(0,6,2.5),'qa-wireframe':(3,-5,3.7),'silhouette-128-front':(0,-6,2.5),'silhouette-128-side':(6,0,2.5)}
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
root=bpy.data.objects.new('OneFullHeightVentedChangingLocker',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_locker_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'locker_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
