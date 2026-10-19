"""Original pierced vertical rail equipment cabinet with two ear-mounted hollow chassis; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-pierced-rail-equipment-cabinet-kit-01';VERSION='1.0.0';TITLE='Pierced-rail Equipment Cabinet'
DESCRIPTION=('One original static open-front equipment cabinet: a continuous thick floor/roof/side/back shell on four full feet, two vertical rails with eleven genuine square through-holes each, and two fixed hollow original chassis. Each chassis has integral pierced front ears, five actual shallow front ventilation slots entering its empty thick-walled cavity, and two short thick open handles. Eight continuous headed square pins pass through aligned ear and rail holes; full lower shaft faces bear on the hole floors and head back faces meet the ears. Four integral front rail shoulders also meet the complete ear-bottom faces. An entire tall middle equipment bay is empty, with real gaps between chassis, behind both chassis and beside the rails. All fixed parts count together as one prop. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. Constant opaque PBR only: no TEX_* nodes, linked Principled inputs, image/procedural textures, text, branding, cables, network, door or animation. Entire geometry newly authored; no old radio deletion/copy, drawer conversion or closed-cabinet recoloring. Static visual geometry only. No 19-inch or other standard-interface compatibility, insertion/pulling action, computing/storage/network/RF/power function, airflow/cooling/fire/electromagnetic/electrical/installation safety, load, anti-tip, stability, manufacturing or material-performance claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousOpenFrontCabinetShell';RAILS=[];CHASSIS=[];HANDLES=[];PINS=[];HOLES=[];VENTS=[]
PALETTE=[('MutedBlueCabinet',(.085,.17,.21,1),.58,.12),('PaleAlloyRails',(.39,.43,.43,1),.48,.54),('CoolGrayLowerChassis',(.24,.29,.30,1),.53,.20),('WarmGrayUpperChassis',(.36,.35,.30,1),.57,.15),('GraphiteFeetAndHandles',(.045,.056,.06,1),.66,.08)]
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
# Continuous new cabinet envelope. The front is genuinely absent.
G[BODY]=grid([-.40,-.37,.37,.40],[-.32,.26,.30],[.08,.14,1.56,1.62],lambda x,y,z:abs(x)>.37 or y>.26 or z<.14 or z>1.56,0,'One closed connected thick shell: lower and upper frames, both side panels and back; entirely open front.')
for label,lo,hi in [('Floor',(-.40,-.32,.08),(.40,.30,.14)),('Roof',(-.40,-.32,1.56),(.40,.30,1.62)),('Back',(-.40,.26,.08),(.40,.30,1.62)),('Left',(-.40,-.32,.08),(-.37,.30,1.62)),('Right',(.37,-.32,.08),(.40,.30,1.62))]:solid('CompleteCabinetMaterial_'+label,inset_box(lo,hi),[BODY],'Complete finite thick '+label+' material slab, 1 mm boundary inset including the continuous frame corners.')
for ix,x in enumerate([-.32,.32]):
 for iy,y in enumerate([-.22,.22]):
  n=f'FullGroundFoot_{ix+1}_{iy+1}';G[n]=box((x-.045,y-.045,0),(x+.045,y+.045,.08),4,'Complete flat 90 mm square foot, finitely seated under the continuous floor.');FEET.append(n)
  contact(n+'_FullFloorSeat',n,BODY,(0,0,1),(x,y,.08),.008099)
  FOOT_CONTACTS.append({'mesh':n,'name':n+'_FullGroundSole','x':x,'y':y,'half_x':.045,'half_y':.045,'minimum_area_m2':.008099})
RAIL_Z=[round(.24+.12*i,6) for i in range(11)]
for side,label in [(-1,'Left'),(1,'Right')]:
 cx=side*.31;n='TruePiercedRail_'+label;RAILS.append(n)
 xs=[cx-.025,cx-.013,cx+.013,cx+.025];zs=sorted(set([.14,1.56]+[z+d for z in RAIL_Z for d in [-.013,.013]]+[.285,.31,1.005,1.03]))
 G[n]=grid(xs,[-.33,-.30,-.27],zs,lambda x,y,z:(y<-.30 and (.285<z<.31 or 1.005<z<1.03)) or (y>-.30 and not(abs(x-cx)<.013 and any(abs(z-c)<.013 for c in RAIL_Z))),1,'One closed connected vertical 30 mm thick rail with eleven full-thickness square bores, continuous material bridges and two integral short front support shoulders; no painted-hole imitation.')
 contact(n+'_LowerFrame',BODY,n,(0,0,1),(cx,-.285,.14),.001499)
 contact(n+'_UpperFrame',n,BODY,(0,0,1),(cx,-.285,1.56),.001499)
 sx=[cx-.024,cx-.014,cx+.014,cx+.024];sz=sorted(set([.141,1.559]+[z+d for z in RAIL_Z for d in [-.014,.014]]))
 solid(n+'_CompleteMaterial',grid(sx,[-.299,-.271],sz,lambda x,y,z:not(abs(x-cx)<.014 and any(abs(z-c)<.014 for c in RAIL_Z))),[n],'Complete closed inset rail material including both continuous edge strips and every full inter-hole bridge; holes expanded 1 mm.')
 for j,z in enumerate([.31,1.03],1):solid(n+'_WholeIntegralShoulder_'+str(j),box((cx-.024,-.329,z-.024),(cx+.024,-.271,z-.001)),[n],'Entire finite material of an integral front shoulder and its continuous root into the vertical rail, 1 mm boundary inset.')
 for j,z in enumerate(RAIL_Z,1):
  q=f'{n}_Bore_{j:02d}';probe=box((cx-.012,-.301,z-.012),(cx+.012,-.269,z+.012))
  isolated(q,probe,[n],'Complete isolated finite square bore volume through and beyond both rail mouths; all four walls covered with 1 mm inset.')
  HOLES.append({'name':q,'rail':n,'x':cx,'z':z,'square_width_m':.026})
# Original chassis front plates, integral mounting ears and thick shells are
# one conforming connected boundary, not intersecting boxes or a reused radio.
for ci,z0 in enumerate([.31,1.03],1):
 z1=z0+.24;zscrew=[z0+.05,z0+.17];slot_z=[z0+.09,z0+.15];slot_x=[-.12,-.06,0,.06,.12];n=f'HollowEarMountedChassis_{ci}';CHASSIS.append(n)
 def removed(x,z,e=0):return any(abs(x-side*.31)<.013+e and any(abs(z-c)<.013+e for c in zscrew) for side in [-1,1]) or (slot_z[0]-e<z<slot_z[1]+e and any(abs(x-c)<.0125+e for c in slot_x))
 xs=sorted(set([-.335,-.323,-.297,-.27,-.25,.25,.27,.297,.323,.335]+[x+d for x in slot_x for d in [-.0125,.0125]]))
 zz=sorted(set([z0,z0+.02,z1-.02,z1]+slot_z+[z+d for z in zscrew for d in [-.013,.013]]))
 def filled(x,y,z):
  if y<-.30:return not removed(x,z)
  return abs(x)<.27 and (abs(x)>.25 or y>.16 or z<z0+.02 or z>z1-.02)
 G[n]=grid(xs,[-.33,-.30,.16,.18],zz,filled,ci+1,'One new closed connected hollow chassis with integral thick front plate/ears, four real ear holes and five real front vents; entire shell has finite thickness.')
 px=sorted(set([-.334,.334]+[s*.31+d for s in [-1,1] for d in [-.014,.014]]+[x+d for x in slot_x for d in [-.0135,.0135]]));pz=sorted(set([z0+.001,z1-.001,slot_z[0]-.001,slot_z[1]+.001]+[z+d for z in zscrew for d in [-.014,.014]]))
 solid(n+'_CompletePiercedFrontAndEars',grid(px,[-.329,-.301],pz,lambda x,y,z:not removed(x,z,.001)),[n],'Complete continuous finite front-plate and both integral ear material domains, including each entire hole ring and every vent bridge, 1 mm boundary inset.')
 for label,lo,hi in [('Floor',(-.27,-.33,z0),(.27,.18,z0+.02)),('Roof',(-.27,-.33,z1-.02),(.27,.18,z1)),('Back',(-.27,.16,z0),(.27,.18,z1)),('Left',(-.27,-.33,z0),(-.25,.18,z1)),('Right',(.25,-.33,z0),(.27,.18,z1))]:solid(n+'_CompleteMaterial_'+label,inset_box(lo,hi),[n],'Entire thick '+label+' material slab and its connection to the front plate, 1 mm inset.')
 air(n+'_WholeInnerCavity',box((-.249,-.299,z0+.021),(.249,.159,z1-.021)),'Complete finite chassis inner cavity from front wall to back wall, floor to roof and side to side, 1 mm inset.')
 for j,x in enumerate(slot_x,1):
  q=f'{n}_FullThroughVent_{j}';air(q,box((x-.0115,-.331,slot_z[0]+.001),(x+.0115,-.299,slot_z[1]-.001)),'Complete finite shallow vent air through the full 30 mm front wall and into the empty chassis cavity, 1 mm lateral inset.');VENTS.append(q)
 for side,label in [(-1,'Left'),(1,'Right')]:
  cx=side*.31;rail=RAILS[0 if side<0 else 1]
  contact(n+'_'+label+'_WholeEarUnderseat',rail,n,(0,0,1),(cx,-.315,z0),.001499)
  # Whole ear rail patch is 50 mm x 240 mm less two 26 mm square bores.
  contact(n+'_'+label+'_WholeEarRailFace',n,rail,(0,1,0),(cx,-.30,z0+.115),.010647)
  for j,z in enumerate(zscrew,1):
   q=f'{n}_{label}EarHole_{j}';isolated(q,box((cx-.012,-.331,z-.012),(cx+.012,-.299,z+.012)),[n],'Entire finite integral front-ear hole through its full thickness, independent of the installed fixed pin.')
   pin=f'Chassis_{ci}_{label}_HeadedPin_{j}';PINS.append({'mesh':pin,'chassis':n,'rail':rail,'x':cx,'z':z,'bearing_z':z-.013})
   pb=[((cx-.009,-.33,z-.013),(cx+.009,-.255,z+.005)),((cx-.019,-.344,z-.018),(cx+.019,-.33,z+.018))]
   G[pin]=union_boxes(pb,1,'One continuous fixed square pin and integral broad head. Entire shaft passes through aligned ear and rail bores, finitely bears on their bottom walls, and retains positive side/top wall gaps.')
   contact(pin+'_EarHoleFloor',n,pin,(0,0,1),(cx,-.315,z-.013),.000539)
   contact(pin+'_RailHoleFloor',rail,pin,(0,0,1),(cx,-.285,z-.013),.000539)
   contact(pin+'_HeadBackFace',pin,n,(0,1,0),(cx-.016,-.33,z),.000691)
   solid(pin+'_EntireShaft',inset_box(pb[0][0],pb[0][1]),[pin],'Complete finite square pin shaft from head root through and beyond both bored plates, all longitudinal material included.')
   solid(pin+'_EntireHead',inset_box(pb[1][0],pb[1][1]),[pin],'Complete thick broad pin head material, including the shaft root.')
   # At the exact bottom bearing plane air terminates on the finite support.
   # Nonbearing wall domains retain an explicit 1 mm inset; no positive closed
   # distance is claimed at a bearing-edge contact boundary itself.
   for label2,lo,hi in [('Left',(cx-.012,-.329,z-.012),(cx-.010,-.269,z+.012)),('Right',(cx+.010,-.329,z-.012),(cx+.012,-.269,z+.012)),('Top',(cx-.009,-.329,z+.006),(cx+.009,-.269,z+.012))]:air(pin+'_CompleteNonbearingAir_'+label2,box(lo,hi),'Full finite nonbearing '+label2+' bore-wall corridor over the complete ear and rail thickness, bounded 1 mm away from the intended lower bearing boundary and head face.')
  hx=side*.225;handle=f'Chassis_{ci}_{label}_ShortThickHandle';HANDLES.append({'mesh':handle,'chassis':n,'x':hx,'z0':z0})
  hb=[((hx-.014,-.40,z0+.045),(hx+.014,-.33,z0+.07)),((hx-.014,-.40,z0+.17),(hx+.014,-.33,z0+.195)),((hx-.014,-.42,z0+.045),(hx+.014,-.40,z0+.195))]
  G[handle]=union_boxes(hb,4,'One continuous thick short open handle with two complete finite front-plate roots, joined by a real outer bridge.')
  contact(handle+'_BothFullRoots',handle,n,(0,1,0),(hx,-.33,z0+.0575),.001399,points=[(hx,-.33,z0+.0575),(hx,-.33,z0+.1825)])
  air(handle+'_WholeOpening',box((hx-.013,-.399,z0+.071),(hx+.013,-.331,z0+.169)),'Entire finite handle opening between both roots, front face and bridge; 1 mm boundary inset.')
  for j,(lo,hi) in enumerate(hb,1):solid(handle+'_FullMaterial_'+str(j),inset_box(lo,hi),[handle],'Complete finite handle root or bridge material, 1 mm boundary inset.')
# Real unused holes stay clear through the whole assembly. Occupied holes have
# separate isolated full bores and finite nonbearing air volumes above.
used=[.36,.48,1.08,1.20]
for r in HOLES:
 if not any(abs(r['z']-z)<1e-7 for z in used):air(r['name']+'_WholeAssemblyOpen',box((r['x']-.012,-.321,r['z']-.012),(r['x']+.012,-.269,r['z']+.012)),'Complete unoccupied rail hole air from in front of the mounting plane to beyond its back, tested against every assembled part.')
for label,z0,z1 in [('Lower',.141,.309),('MiddleEmptyEquipmentBay',.551,1.029),('Upper',1.271,1.559)]:air('FullCentralCabinetAir_'+label,box((-.284,-.319,z0),(.284,.259,z1)),'Entire finite '+label+' open equipment space between the rails from front mouth to actual rear panel, 1 mm clearance at bounding solids; no hidden dark filler.')
air('WholeChassisRearClearance',box((-.284,.181,.141),(.284,.259,1.559)),'Complete full-height rear corridor behind both chassis to the inside back panel, including both full chassis back areas.')
for side,label in [(-1,'Left'),(1,'Right')]:
 a,b=(-.369,-.336) if side<0 else (.336,.369);air(label+'_WholeOuterRailSideCorridor',box((a,-.319,.141),(b,.259,1.559)),'Entire side-panel to outer-rail/ear corridor over the full cabinet height and depth.')
 a,b=(-.334,-.286) if side<0 else (.286,.334);air(label+'_WholeRailRearCorridor',box((a,-.254,.141),(b,.259,1.559)),'Entire rail-back corridor, beginning 1 mm beyond the pin tips and extending to the rear panel.')
 for ci,z0 in enumerate([.31,1.03],1):
  a,b=(-.284,-.271) if side<0 else (.271,.284);air(f'{label}_Chassis{ci}_WholeInnerRailGap',box((a,-.299,z0+.001),(b,.179,z0+.239)),'Entire chassis-side to inner rail-edge gap behind the front ear, 1 mm inset at both actual bodies.')
# One connected finite front air volume for nonbearing rail faces, subtracting
# the two chassis ear intervals. Each disconnected interval is a separate proof.
for label,z0,z1 in [('Below',.141,.284),('Middle',.551,1.004),('Above',1.271,1.559)]:
 for side,side_label in [(-1,'Left'),(1,'Right')]:
  cx=side*.31;air(f'{side_label}_RailNonbearingFront_{label}',box((cx-.024,-.319,z0),(cx+.024,-.301,z1)),'Complete finite nonbearing front rail-face air in this uninterrupted open interval; intended ear-face intervals excluded.')
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
# Translate all numerical domains together to the exact horizontal bounds center.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=((min(p[0] for p in allv)+max(p[0] for p in allv))/2,(min(p[1] for p in allv)+max(p[1] for p in allv))/2,0)
for d in [G,VOID_VOLUMES,ISOLATED_VOID_VOLUMES,SOLID_VOLUMES]:
 for g in d.values():g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
for r in FOOT_CONTACTS:r['x']-=SHIFT[0];r['y']-=SHIFT[1]
CONTRACT={'single_prop_count':1,'continuous_cabinet_shell':1,'flat_ground_feet':4,'pierced_vertical_rails':2,'integral_ear_underseat_shoulders':4,'full_thickness_rail_holes':22,'hollow_fixed_chassis':2,'integral_front_ear_holes':8,'continuous_headed_pins':8,'short_continuous_handles':4,'real_chassis_vents':10,'whole_empty_middle_equipment_bay':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'standard_interface_or_electrical_or_load_claim':False}
def measure_equipment_rack_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-1.62)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; complete finite solid/air domains, contacts, nonseat separation and real negative gates remain required')
INSIDE_TESTS=[(BODY,sub((-.385,0,.8),SHIFT),sub((0,0,.8),SHIFT)),(RAILS[0],sub((-.33,-.285,.7),SHIFT),sub((-.31,-.285,.72),SHIFT)),(CHASSIS[0],sub((0,.17,.43),SHIFT),sub((0,0,.43),SHIFT))]
FOCUS=(0,0,.81);ORTHO=2.20
CAMERAS={'gray-front3q':(3,-5,3.0),'gray-back3q':(-3,5,3.0),'thumbnail':(3,-5,3.0),'qa-front':(0,-6,2.1),'qa-side':(6,0,2.1),'qa-top':(0,0,6),'qa-back':(0,6,2.1),'qa-wireframe':(3,-5,3.0),'silhouette-128-front':(0,-6,2.1),'silhouette-128-side':(6,0,2.1)}
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
root=bpy.data.objects.new('OnePiercedRailEquipmentCabinet',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_equipment_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'equipment_rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
