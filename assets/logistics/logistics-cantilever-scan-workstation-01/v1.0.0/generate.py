"""One original static cantilever scan workstation. Unpowered visual prop only."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='logistics-cantilever-scan-workstation-01';VERSION='1.0.0';TITLE='Cantilever Scan Workstation'
DESCRIPTION=('One original static unpowered scan-workstation visual prop. A wide thick worktop has a real stepped through-opening and an independent shallow thick tray whose full flange rests on a finite perimeter shoulder. Four complete flat-footed legs and a three-member low H brace support the top. An offset rear column and one continuous L-shaped horizontal cantilever carry a thick downward-opening blind head shell. A separate dark opaque unlit inner plate rests on a full integral internal ledge, with real open cavity below and complete free chamber and perimeter air above. A small fixed side display has a finite mount and a flat dark unlit face, not an operational screen. The entire head-to-tray working space remains empty. Fifteen editable closed connected meshes, five opaque unlinked constant PBR materials, metre units, native Z up, front -Y, horizontal bounds-centred ground origin. No parcel, barcode, text, logo, cable, button interaction, computer operation or imported prior geometry. This newly authored stepped opening, tray, support frame and suspended downward head layout do not rename or recolour a scale, star-chart console, generic table or logistics scene. No barcode recognition, optical imaging, laser, reading distance, weighing, computing, networking, automation, parcel fit, loading, ergonomics, stability, material suitability, manufacture, installation, electrical/laser/workplace safety or functional certification claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[]
BODY='WholeSteppedApertureWorktop';TRAY='WholeInsetFlangedShallowTray';MAST='OffsetRearColumn';ARM='WholeLCantilever';HEAD='DownwardBlindHeadShell';PLATE='OpaqueUnlitInsetHeadPlate';DISPLAY='FixedSideDisplayBody';MOUNT='FixedSideDisplayMount';SHIFT=(0,0,0)
PALETTE=[('DeepPetrolFrame',(.035,.19,.21,1),.51,.32),('WarmIvoryShell',(.64,.66,.61,1),.66,.10),('SlateInsetTray',(.22,.29,.30,1),.60,.28),('DarkOpaqueUnlitFace',(.018,.033,.038,1),.59,0),('MutedAmberAccent',(.63,.31,.075,1),.57,.08)]
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
# All component unions are newly dimensioned original, conforming closed grids.
def tabletop(i=0):
 xs=[-.68+i,-.28-i,-.26-i,.42+i,.44+i,.68-i];ys=[-.42+i,-.30-i,-.28-i,.22+i,.24+i,.42-i];zs=[.82+i,.872-i,.89-i]
 return grid(xs,ys,zs,lambda x,y,z:not((- .26-i<x<.42+i and -.28-i<y<.22+i) if z<.872-i else (-.28-i<x<.44+i and -.30-i<y<.24+i)),1,'Continuous full thick worktop and stepped true opening; complete finite perimeter tray shoulder, no dark fake inset.')
def tray(i=0):
 xs=[-.278+i,-.255+i,-.232-i,.392+i,.415-i,.438-i];ys=[-.298+i,-.275+i,-.252-i,.192+i,.215-i,.238-i];zs=[.835+i,.85-i,.872+i,.89-i]
 return grid(xs,ys,zs,lambda x,y,z:(z>.872+i or (-.255+i<x<.415-i and -.275+i<y<.215-i)) and not(z>.85-i and -.232-i<x<.392+i and -.252-i<y<.192+i),2,'Whole shallow tray: real thick floor, full walls and integral continuous upper flange with finite table-shoulder support.')
G[BODY]=tabletop();G[TRAY]=tray()
contact('WholeTrayFlangeOnCompleteWorktopShoulder',BODY,TRAY,(0,0,1),(-.269,0,.872),.035,points=[(-.269,-.02,.872),(.429,-.02,.872),(.08,-.289,.872),(.08,.229,.872)])
solid('WholeWorktopAndSteppedOpeningMaterial',tabletop(.001),[BODY],'Complete 1 mm inset material follows the entire table perimeter, full lower ring and stepped aperture shoulder.')
solid('WholeTrayFloorWallAndFlangeMaterial',tray(.001),[TRAY],'Complete connected 1 mm inset tray material includes all of the floor, walls and integral peripheral flange.')
air('WholeIsolatedTableThroughOpening',box((-.259,-.279,.819),(.419,.219,.891)),'Entire lower through-opening and both mouths, excluding only 1 mm boundary margin; tray intentionally omitted only for this isolated aperture predicate.',[BODY])
air('WholeOpenTrayAndHeadWorkingVolume',box((-.231,-.251,.851),(.391,.191,1.379)),'Entire positive-volume tray interior and whole corresponding head-to-tray work volume through the actual top opening; every interior corner included.')
air('WholeAboveFlangeWorkingEnvelope',box((-.277,-.297,.891),(.437,.237,1.379)),'Entire widened work envelope directly above the full tray flange up to 1 mm below the head mouth.')
# Full tray-to-worktop side gap, around all four complete lower walls.
xs=[-.259,-.256,.416,.419];ys=[-.279,-.276,.216,.219];zs=[.836,.871]
air('WholeLowerTrayPerimeterAir',grid(xs,ys,zs,lambda x,y,z:not(-.256<x<.416 and -.276<y<.216)),'Whole continuous four-sided lower tray clearance from floor side to shoulder minus explicit 1 mm contact boundary margins.')
xs=[-.2795,-.2785,.4385,.4395];ys=[-.2995,-.2985,.2385,.2395];zs=[.8725,.8895]
air('WholeFlangePerimeterAir',grid(xs,ys,zs,lambda x,y,z:not(-.2785<x<.4385 and -.2985<y<.2385)),'Complete four-sided finite 2 mm flange-to-opening clearance with 0.5 mm wall margins; no side-wall interference.')
for ix,cx in enumerate([-.56,.56]):
 for iy,cy in enumerate([-.32,.32]):
  n=f'WholeFlatFootLeg_{ix+1}_{iy+1}';FEET.append(n)
  G[n]=box((cx-.0325,cy-.0325,0),(cx+.0325,cy+.0325,.82),0,'Complete solid square leg, full planar ground foot and finite worktop underside seat.')
  solid(n+'_WholeMaterial',box((cx-.0315,cy-.0315,.001),(cx+.0315,cy+.0315,.819)),[n],'Whole 1 mm inset leg material from finite foot to full upper seat.')
  contact(n+'_FullTopSeat',n,BODY,(0,0,1),(cx,cy,.82),.004224)
for iy,cy in enumerate([-.32,.32]):
 n='LowLongBrace_'+str(iy+1);G[n]=box((-.5275,cy-.025,.20),(.5275,cy+.025,.25),0,'One whole low cross-member joining the two complete end leg side faces.')
 solid(n+'_WholeMaterial',box((-.5265,cy-.024,.201),(.5265,cy+.024,.249)),[n],'Entire low brace material with explicit finite ends.')
 contact(n+'_LeftLegSeat',f'WholeFlatFootLeg_1_{iy+1}',n,(1,0,0),(-.5275,cy,.225),.002499)
 contact(n+'_RightLegSeat',n,f'WholeFlatFootLeg_2_{iy+1}',(1,0,0),(.5275,cy,.225),.002499)
n='LowCentralHBrace';G[n]=box((-.025,-.295,.20),(.025,.295,.25),0,'Whole low central H member, finite end faces on both low long braces.')
solid(n+'_WholeMaterial',box((-.024,-.294,.201),(.024,.294,.249)),[n],'Whole continuous central H material.')
contact('CentralH_FrontBraceSeat','LowLongBrace_1',n,(0,1,0),(0,-.295,.225),.002499)
contact('CentralH_BackBraceSeat',n,'LowLongBrace_2',(0,1,0),(0,.295,.225),.002499)
G[MAST]=box((-.50,.27,.89),(-.42,.35,1.63),0,'Whole offset rear solid column with a complete table foot and full cantilever end interface.')
solid('WholeOffsetColumnMaterial',box((-.499,.271,.891),(-.421,.349,1.629)),[MAST],'Full column material from tabletop through its complete upper arm interface.')
contact('ColumnOnFullWorktopSeat',BODY,MAST,(0,0,1),(-.46,.31,.89),.006399)
def cantilever(i=0):
 return union_boxes([((-.42+i,.27+i,1.55+i),(.12-i,.35-i,1.63-i)),((.04+i,-.02+i,1.55+i),(.12-i,.30,1.63-i))],0,'Whole connected L-shaped cantilever with complete elbow, horizontal column end and downward head seat.')
G[ARM]=cantilever();solid('WholeLCantileverAndElbowMaterial',cantilever(.001),[ARM],'Entire connected 1 mm inset L arm and elbow; full span and both end neighborhoods included.')
contact('FullColumnToCantileverSeat',MAST,ARM,(1,0,0),(-.42,.31,1.59),.006399)
def head_shell(i=0):
 xs=[-.09+i,-.065-i,-.055-i,.215+i,.225+i,.25-i];ys=[-.18+i,-.155-i,-.145-i,.105+i,.115+i,.14-i];zs=[1.38+i,1.485+i,1.495-i,1.52+i,1.55-i]
 def occupied(x,y,z):
  if z>1.52+i:return True
  hole=(-.055-i<x<.215+i and -.145-i<y<.105+i) if 1.485+i<z<1.495-i else (-.065-i<x<.225+i and -.155-i<y<.115+i)
  return not hole
 return grid(xs,ys,zs,occupied,1,'One full downward-opening blind shell with thick entire mouth rim, all walls, solid roof and integral continuous recessed inner ledge.')
G[HEAD]=head_shell();solid('WholeBlindHeadRoofWallsRimAndLedgeMaterial',head_shell(.001),[HEAD],'Complete connected inset material over all four walls, whole mouth rim, integral seat ledge and full blind roof.')
contact('CompleteCantileverToHeadRoofSeat',HEAD,ARM,(0,0,1),(.08,.06,1.55),.012799)
G[PLATE]=box((-.063,-.153,1.495),(.223,.113,1.505),3,'Separate complete thick opaque unlit inner plate on the full continuous recessed shelf. No lens, emission, scan or electrical function.')
solid('WholeOpaquePlateMaterial',box((-.062,-.152,1.496),(.222,.112,1.504)),[PLATE],'Whole inner plate 1 mm inset solid; opaque material, no external texture or optical claim.')
contact('InnerPlateOnWholeIntegralLedge',HEAD,PLATE,(0,0,1),(-.059,-.02,1.495),.00850,points=[(-.059,-.02,1.495),(.219,-.02,1.495),(.08,-.149,1.495),(.08,.109,1.495)])
xs=[-.064,-.054,.214,.224];ys=[-.154,-.144,.104,.114];zs=[1.379,1.484,1.494]
air('WholeDownwardBlindCavityAndOpenMouth',grid(xs,ys,zs,lambda x,y,z:z<1.484 or (-.054<x<.214 and -.144<y<.104)),'Whole downward cavity below the unlit plate, through the complete mouth and across all inner rim/wall/ledge corners, with 1 mm boundary margins.')
xs=[-.0645,-.0635,.2235,.2245];ys=[-.1545,-.1535,.1135,.1145];zs=[1.4955,1.5055,1.519]
air('WholeUpperChamberAndPlatePerimeterAir',grid(xs,ys,zs,lambda x,y,z:z>1.5055 or not(-.0635<x<.2235 and -.1535<y<.1135)),'Whole finite upper blind chamber and continuous four-sided plate-wall air with 0.5 mm side-seat boundary margins; true roof closure remains material.')
G[MOUNT]=box((-.42,.28,1.15),(-.39,.33,1.20),4,'One short thick lateral fixed-display mount with complete opposed end seats.')
solid('WholeSideDisplayMountMaterial',box((-.419,.281,1.151),(-.391,.329,1.199)),[MOUNT],'Whole finite lateral mount material.')
contact('SideDisplayMountOnColumn',MAST,MOUNT,(1,0,0),(-.42,.305,1.175),.002499)
G[DISPLAY]=grid([-.39,-.37,-.18,-.16],[.25,.34],[1.10,1.12,1.23,1.25],lambda x,y,z:True,1,'Whole thick fixed side display body, with one flat non-emissive dark face tessellated into its own front surface, not a false cavity.')
G[DISPLAY]['face_materials']=[3 if all(abs(G[DISPLAY]['vertices'][j][1]-.25)<1e-9 for j in f) and all(-.370001<=G[DISPLAY]['vertices'][j][0]<=-.179999 and 1.119999<=G[DISPLAY]['vertices'][j][2]<=1.230001 for j in f) else 1 for f in G[DISPLAY]['faces']]
solid('WholeFixedSideDisplayMaterial',box((-.389,.251,1.101),(-.161,.339,1.249)),[DISPLAY],'Whole fixed display body material behind the unlit planar face.')
contact('SideDisplayFullMountSeat',MOUNT,DISPLAY,(1,0,0),(-.39,.305,1.175),.002499)
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
CONTRACT={'single_prop_count':1,'whole_tabletop_true_stepped_aperture':1,'whole_shallow_flanged_inset_tray':1,'flat_ground_legs':4,'low_H_brace_members':3,'offset_column':1,'whole_L_cantilever':1,'whole_downward_blind_head_shell':1,'opaque_unlit_inner_plate_on_finite_ledge':1,'fixed_side_display_and_mount':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'included_parcels_barcodes_or_computers':0,'scanning_optical_electrical_or_safety_claim':False}
def measure_scan_table_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert len(vertices)==15
 assert abs(max(p[2] for p in vertices[MAST])-1.63)<2e-7
 return dict(CONTRACT,geometry_scope='actual full coordinates; entire air/material domains, all finite seats, all component pairs and focused actual mutations are required independent gates')
INSIDE_TESTS=[(BODY,(-.5,0,.85),(.08,-.02,.86)),(TRAY,(.08,-.02,.842),(.08,-.02,.875)),(HEAD,(.08,-.02,1.535),(.08,-.02,1.43))]
FOCUS=(0,0,.815);ORTHO=2.35
CAMERAS={'gray-front3q':(3,-4,3.3),'gray-back3q':(2,-5,-2.9),'thumbnail':(3,-4,3.3),'qa-front':(0,-6,2.7),'qa-side':(6,0,2.7),'qa-top':(0,0,6),'qa-back':(0,6,2.7),'qa-wireframe':(3,-4,3.3),'silhouette-128-front':(0,-6,2.7),'silhouette-128-side':(6,0,2.7)}
GRAY_UNDERSIDE_EXCEPTION={'view':'gray-back3q','purpose':'diagnostic lower view of true downward head cavity; only this early image replaces usual back three-quarter','hide_preview_ground':True,'all_vertex_minimum_margin_fraction':.06,'formal_views_unchanged':True,'permission_source':'parent instruction 2026-10-19 08:13 UTC'}
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
root=bpy.data.objects.new('OneUnpoweredCantileverScanWorkstation',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_scan_table_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'scan_table_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 if gray and name==GRAY_UNDERSIDE_EXCEPTION['view']:
  old_hidden=ground.hide_render
  try:
   ground.hide_render=True;render(name,pos)
  finally:ground.hide_render=old_hidden
 else:render(name,pos)
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
