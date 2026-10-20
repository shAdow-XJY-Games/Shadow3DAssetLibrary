"""One original fixed H-frame studio easel. Source geometry is plain Python."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-fixed-h-frame-studio-easel-01';VERSION='1.0.0';TITLE='Fixed H-frame Studio Easel'
DESCRIPTION=('One original fixed H-frame studio easel with two complete long ground runners, two parallel thick upright guide rails with integral fixed shoulders, lower and upper full cross ties, one continuous twin-through-slot carriage with integral lower board ledge and stop lip, and one upper fixed cap/back-support head bearing a newly authored thick blank board. The complete slots have real closed walls and full-length rail clearance. All geometry is newly authored; no old A-frame easel, blackboard, mirror or sheet rack components are imported. One static prop only; one fixed vertical pose. Metres, native Z up, front -Y, full horizontal bounds centred on its ground datum Z=0. Constant opaque PBR, alpha 1, no texture or linked Principled inputs. No sliding, adjustment, clamping operation, tilt, folding, assembly, arbitrary board compatibility, structural load, stability, anti-tip, manufacturing or safety claim. Original easel structure family and tilt/fold motion remain partial.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousTwinSlotCarriageWithLedgeLip';BOARD='OriginalThickBlankBoard';CAP='ContinuousUpperFixedCapAndBackPad';RAILS=[]
PALETTE=[('WarmMapleStructure',(.43,.24,.105,1),.58,.0),('DarkWalnutFixedCarriage',(.14,.065,.025,1),.48,.0),('WarmBlankBoard',(.76,.70,.57,1),.77,.0)]
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

def erode_boxes(boxes,e):return [(tuple(q+e for q in a),tuple(q-e for q in b)) for a,b in boxes]
def member(name,lo,hi,mat,role):
 add_solid(name,lo,hi,mat,role)
def combo(name,boxes,mat,role):
 G[name]=union_boxes(boxes,mat,role);solid(name+'_WholeConnectedMaterial',union_boxes(erode_boxes(boxes,.0006)),[name],'Whole connected finite material; each complete construction volume eroded 0.6 mm, overlapping union junctions retained. '+role)
for x,label in [(-.23,'Left'),(.23,'Right')]:
 foot=label+'CompleteGroundRunner';rail=label+'ParallelGuideRailWithIntegralShoulder';FEET.append(foot);RAILS.append(rail)
 member(foot,(x-.06,-.36,0),(x+.06,.36,.075),0,'Complete 720 mm long ground runner with uninterrupted 120 by 720 mm bottom sole.')
 FOOT_CONTACTS.append({'mesh':foot,'name':foot+'_WholeGroundSole','x':x,'y':0,'half_x':.06,'half_y':.36,'minimum_area_m2':.0863999})
 combo(rail,[((x-.03,.025,.075),(x+.03,.095,1.82)),((x-.055,.012,.57),(x+.055,.108,.60))],0,'One continuous parallel vertical thick guide rail with an integral full finite four-sided fixed shoulder. No moving/height-adjustable mechanism.')
 contact(label+'_WholeRailBottomOnRunner',foot,rail,(0,0,1),(x,.06,.075),.0041999)
 contact(label+'_WholeFixedShoulderToCarriage',rail,BODY,(0,0,1),(x-.045,.06,.60),.0055439)
for name,z0,z1 in [('LowerFullCrossTie',.075,.14),('UpperFullCrossTie',1.75,1.82)]:
 member(name,(-.20,.025,z0),(.20,.095,z1),0,'Complete transverse member between both parallel rails, with full finite square-ended contact to each upright.')
 contact(name+'_WholeLeftEnd',RAILS[0],name,(1,0,0),(-.20,.06,(z0+z1)/2),(.07*(z1-z0))-.0000001)
 contact(name+'_WholeRightEnd',name,RAILS[1],(1,0,0),(.20,.06,(z0+z1)/2),(.07*(z1-z0))-.0000001)
for x,label in[(-.185,'Left'),(.185,'Right')]:contact(label+'_WholeLowerTieOnRunner',label+'CompleteGroundRunner','LowerFullCrossTie',(0,0,1),(x,.06,.075),.0020999)
# Two real whole-thickness holes in ONE coherent carriage. The shelf, lip and
# lower rear pads are integral material, with no internal overlapping surfaces.
CARRIAGE_BOXES=[((-.29,-.015,.60),(.29,.125,.72)),((-.38,-.12,.69),(.38,.005,.72)),((-.38,-.12,.70),(.38,-.09,.765))]
for x in [-.23,.23]:CARRIAGE_BOXES.append(((x-.035,-.045,.70),(x+.035,.005,.79)))
def carriage(e=0):
 boxes=erode_boxes(CARRIAGE_BOXES,e);holes=[((x-.033-e,.022-e),(x+.033+e,.098+e)) for x in[-.23,.23]]
 axes=[sorted(set([p[k] for a,b in boxes for p in[a,b]]+[p[k] for a,b in holes for p in[a,b]])) if k<2 else sorted(set(p[k] for a,b in boxes for p in[a,b])) for k in range(3)]
 return grid(*axes,lambda x,y,z:any(all(a[k]<p<b[k] for k,p in enumerate([x,y,z])) for a,b in boxes) and not any(a[0]<x<b[0] and a[1]<y<b[1] for a,b in holes),1,'One connected twin-through-slot carriage, full four walls and central root bridge, integral whole lower ledge, full stop lip and two full rear board-bearing pads.')
G[BODY]=carriage();solid(BODY+'_WholeTwinSlotBridgeLedgeLipPadsMaterial',carriage(.0006),[BODY],'Complete connected material around both enlarged through slots, all outer walls, central root bridge, ledge/lip and both board pads, 0.6 mm boundary allowance.')
for x,label in[(-.23,'Left'),(.23,'Right')]:
 isolated(label+'_WholeCarriageSlotThroughBothMouths',box((x-.0324,.0226,.5994),(x+.0324,.0974,.7206)),[BODY],'Complete isolated actual slot section and 120 mm length extended past both mouths; 0.6 mm wall inset. The rail is omitted only for this isolated bore proof.')
 air(label+'_WholeAssembledSlotRailClearance',grid([x-.0324,x-.0306,x+.0306,x+.0324],[.0226,.0244,.0956,.0974],[.6006,.7194],lambda xx,y,z:abs(xx-x)>.0306 or y<.0244 or y>.0956),'Complete finite rectangular annular air surrounding the full four-sided rail over the entire carriage length; 0.6 mm boundary insets. Original nominal clearance is 3 mm; intended bottom shoulder bearing excluded.')
# One entirely new blank thick board, supported at its whole lower edge,
# two lower rear pads, full upper finite cap and an upper rear pad.
member(BOARD,(-.32,-.075,.72),(.32,-.045,1.52),2,'One complete blank 30 mm thick board; unpainted opaque constant PBR, full six-sided closed material.')
contact('WholeBoardLowerEdgeOnLedge',BODY,BOARD,(0,0,1),(0,-.06,.72),.0191999)
contact('BothWholeBoardLowerRearPads',BOARD,BODY,(0,1,0),(-.23,-.045,.755),.0097999,points=[(-.23,-.045,.755),(.23,-.045,.755)])
CAP_BOXES=[((-.28,-.005,1.56),(.28,.025,1.63)),((-.09,-.045,1.52),(.09,.025,1.60)),((-.10,-.09,1.52),(.10,.025,1.56)),((-.08,-.045,1.47),(.08,-.005,1.54))]
combo(CAP,CAP_BOXES,1,'One connected fixed upper head: complete rear transverse rail-root bridge, finite top cap and rear board-support pad. No screw, clamp pressure, sliding or motion claim.')
for x,label in[(-.23,'Left'),(.23,'Right')]:contact(label+'_WholeUpperHeadRailRoot',CAP,label+'ParallelGuideRailWithIntegralShoulder',(0,1,0),(x,.025,1.595),.0041999)
contact('WholeBoardUpperEdgeAgainstFixedCap',BOARD,CAP,(0,0,1),(0,-.06,1.52),.0059999)
contact('WholeBoardUpperRearSupport',BOARD,CAP,(0,1,0),(0,-.045,1.495),.0079999)
# Full bounded nonbearing board-air domains, including lip clearance and
# rear gap corridors. Air domains are complete closed volumes, never rays.
air('WholeLowerLipToBoardFrontGap',box((-.3194,-.0894,.7206),(.3194,-.0756,.7644)),'Complete full-width board-to-lower-lip nonbearing gap, 0.6 mm boundary allowance.')
air('WholeBoardRearToRailsCentralAir',box((-.1994,-.0444,.7906),(.1994,.0244,1.4694)),'Whole central board-back to rail-plane air, full height between lower pads and upper fixed head; 0.6 mm boundary allowance.')
for x,label in[(-.23,'Left'),(.23,'Right')]:air(label+'_WholeBoardRearRailAir',box((x-.0294,-.0444,.7906),(x+.0294,.0244,1.5594)),'Whole finite rail-front to board-rear air above lower pads and below upper bridge; only intended fixed head and pad contacts excluded.')
air('WholeLowerBoardRearCentralAir',box((-.1944,-.0444,.7206),(.1944,-.0156,.7900)),'Whole lower central board-back air between both actual rear pads.')
air('WholeOpenUpperHBay',box((-.1994,.0256,1.6306),(.1994,.0944,1.7494)),'Complete open H-frame top bay between full parallel rails and top tie, above fixed upper head.')
air('WholeOpenLowerHBay',grid([-.1994,-.1744,.1744,.1994],[.0256,.0944],[.1406,.5694,.5994],lambda x,y,z:z<.5694 or abs(x)<.1744),'Complete stepped open lower H-frame bay between rails and lower tie, reaching the full carriage underside through the central gap between both integral shoulders; 0.6 mm boundaries.')
for label,y0,y1 in[('Front',-.3594,.0244),('Rear',.0956,.3594)]:air(label+'_WholeBetweenGroundRunnersAir',box((-.1694,y0,.0006),(.1694,y1,.0744)),'Whole finite floor-level gap between the two uninterrupted long ground runners; 0.6 mm ground/member allowance.')
# One complete board-rear nonbearing domain additionally covers all side,
# top and bottom corridors, with only actual expanded support bodies excluded.
back_lo=(-.3194,-.0444,.7206);back_hi=(.3194,.0244,1.5194)
obstacles=[(tuple(q-.0006 for q in a),tuple(q+.0006 for q in b)) for a,b in CARRIAGE_BOXES+CAP_BOXES]
back_axes=[sorted(set([back_lo[k],back_hi[k]]+[max(back_lo[k],min(back_hi[k],p[k])) for a,b in obstacles for p in[a,b]])) for k in range(3)]
air('WholeBoardRearAllNonbearingAir',grid(*back_axes,lambda x,y,z:not any(all(a[k]<p<b[k] for k,p in enumerate([x,y,z])) for a,b in obstacles)),'Entire bounded board-back to rail-front air over full board width and height, with only expanded actual carriage/head supports excluded; all peripheral, interpad, upper side and lower corridors included. 0.6 mm boundary allowance.')
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
# Freeze every declared support as the complete finite opposed source patch.
# This is numerical construction evidence, never inferred from a mutated export.
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
def patch_clean(poly):
 # Eliminate exact/roundoff duplicate and collinear vertices before freezing.
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
 if len(out)>=3 and sum(patch_cross(out[i],out[(i+1)%len(out)]) for i in range(len(out)))<0:out.reverse()
 return out

def patch_triangles(name,r,sign):
 g=G[name];out=[]
 for face in g['faces']:
  for i in range(1,len(face)-1):
   tri=[g['vertices'][j] for j in [face[0],face[i],face[i+1]]]
   if max(abs(dot(sub(p,r['origin_m']),r['axis'])-r['plane_m']) for p in tri)>1e-8:continue
   if dot(cross(sub(tri[1],tri[0]),sub(tri[2],tri[0])),r['axis'])*sign<=0:continue
   out.append([(dot(sub(p,r['origin_m']),r['u']),dot(sub(p,r['origin_m']),r['v'])) for p in tri])
 return out
for r in CONTACTS:
 aa=patch_triangles(r['a'],r,1);bb=patch_triangles(r['b'],r,-1);polys=[]
 for a in aa:
  for b in bb:
   poly=patch_clean(patch_clip(a,b))
   if patch_area(poly)>1e-12:polys.append(poly)
 r['declared_patch_polygons_uv_m']=polys;r['declared_patch_area_m2']=sum(patch_area(p) for p in polys)
 assert r['declared_patch_area_m2']>=r['minimum_patch_area_m2'],r['name']


SHIFT=(0,0,0)
CONTRACT={'single_prop_count':1,'complete_ground_runners':2,'parallel_full_height_guide_rails':2,'integral_finite_fixed_shoulders':2,'complete_transverse_ties':2,'continuous_twin_slot_carriage':1,'true_full_section_through_slots':2,'integral_lower_ledge_stop_lip':1,'integral_lower_board_back_pads':2,'complete_upper_fixed_cap_and_back_pad':1,'original_thick_blank_board':1,'board_thickness_m':.030,'full_slot_length_m':.120,'nominal_four_side_rail_slot_clearance_m':.003,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'motion_tilt_fold_family_completion_or_load_safety_claim':False}
def measure_easel_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in RAILS:assert abs(max(p[2] for p in vertices[n])-1.82)<2e-7
 lo=[min(p[k] for p in vertices[BOARD]) for k in range(3)];hi=[max(p[k] for p in vertices[BOARD]) for k in range(3)]
 assert all(abs(a-b)<2e-7 for a,b in zip([hi[k]-lo[k] for k in range(3)],[.64,.03,.80]))
 return dict(CONTRACT,geometry_scope='Complete source/export coordinates; full finite air/material bodies, immutable opposed patch domains and all-component-pair nonpenetration required.')
INSIDE_TESTS=[(BODY,(0,.05,.65),(-.23,.06,.65)),(BOARD,(0,-.06,1.),(0,0,1.)),(RAILS[0],(-.23,.06,1.),(0,.06,1.))]
FOCUS=(0,0,.91);ORTHO=2.34
CAMERAS={'gray-front3q':(3,-5,3.1),'gray-back3q':(-3,5,3.1),'thumbnail':(3,-5,3.1),'qa-front':(0,-6,2.2),'qa-side':(6,0,2.2),'qa-top':(0,0,6),'qa-back':(0,6,2.2),'qa-wireframe':(3,-5,3.1),'silhouette-128-front':(0,-6,2.2),'silhouette-128-side':(6,0,2.2)}
WIRE_THICKNESS=ORTHO/1500

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
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneFixedHFrameStudioEasel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete horizontal envelope centred, both complete runner ground soles Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_easel_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=2500
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
import struct
raw=(OUT/'model.glb').read_bytes();json_length,kind=struct.unpack_from('<II',raw,12);assert kind==0x4E4F534A
gltf=json.loads(raw[20:20+json_length]);assert not gltf.get('textures') and not gltf.get('images') and len(raw)<=512000
assert mesh_count<=12 and len(mats)==3 and len(Path(__file__).read_bytes())<=49152
for material in gltf['materials']:
 p=material['pbrMetallicRoughness'];assert p.get('baseColorFactor',[1,1,1,1])[3]==1 and material.get('alphaMode','OPAQUE')=='OPAQUE'
 assert material.get('extensions',{}).get('KHR_materials_transmission',{}).get('transmissionFactor',0)==0 and not any(material.get('emissiveFactor',[0,0,0]))
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'easel_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/painting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'painting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
original_material_inputs={m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
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
  assert len(o.data.polygons)==len(indices),'Diagnostic restoration face count changed before zip'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,expected in inputs:
   assert index<len(p.inputs),'Restored socket index missing'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Restored socket identity/type mismatch'
   actual=tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value
   assert actual==expected,('Restored socket exact value mismatch',m.name,index,identifier,actual,expected)
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Restored face count mismatch'
  assert len(o.data.materials)==len(slots) and list(o.data.materials)==slots,'Restored material slot order mismatch'
  assert [f.material_index for f in o.data.polygons]==indices,'Restored full face material indices mismatch'
 assert records(parts)==source_records,'Diagnostic restoration changed complete geometry/opaque PBR signature'
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
