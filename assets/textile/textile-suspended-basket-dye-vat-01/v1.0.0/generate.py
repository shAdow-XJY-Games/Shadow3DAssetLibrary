"""Original suspended full perforated basket in a thick deep long vat; one static prop."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='textile-suspended-basket-dye-vat-01';VERSION='1.0.0';TITLE='Suspended Basket Dye Vat'
DESCRIPTION=('One original fixed empty textile dye-vat visual form. A long chamfer-corner thick deep outer shell has a complete bottom and rests on a closed low support frame and four short full flat feet. One independently editable thick basket has all four perforated walls, ten real floor holes, twenty-eight true wall windows, a continuous top rim and two integral outward end ears. The ears rest on the full finite end shoulders of the outer rim; the entire basket bottom and all four sides have positive space from the outer shell. Two complete closed thick lifting rings have full finite roots on the basket rim. Nine closed connected editable meshes and five opaque unlinked constant PBR materials. Metres, native Z up, front -Y and horizontally bounds-centred four-foot ground datum. All shape geometry newly dimensioned: no old sieve copied into a shell, recoloured laundry basin, modified pet-wash grate or extractor with its spindle removed. One static empty prop, no liquid plane, cloth, dye, flame, extra container, texture, text, logo or animation. No take-out/lift path, dyeing, filtering, drainage, chemical/material compatibility, heating, capacity/loading, hygiene, manufacture, human/process/equipment safety or old-asset compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='WholeChamferedDeepOuterVat';BASKET='WholeFourWallPerforatedBasketWithEndEars';FRAME='WholeLowClosedSupportFrame';HANDLES=[];FLOOR_HOLES=[];SIDE_WINDOWS=[];SHIFT=(0,0,0)
PALETTE=[('SoftBlueEnamelVat',(.19,.36,.40,1),.55,.08),('PaleIvoryBasket',(.65,.67,.58,1),.50,.25),('DeepTealSupportFrame',(.045,.095,.11,1),.64,.25),('MutedBrassLiftRings',(.45,.34,.16,1),.45,.48),('DarkGrayFlatFeet',(.075,.09,.095,1),.75,.06)]
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
# Original octagonal long shell: full bottom and all connected thick walls.
def octagon(a,b,c):return[(-a+c,-b),(a-c,-b),(a,-b+c),(a,b-c),(a-c,b),(-a+c,b),(-a,b-c),(-a,-b+c)]
def shell(e=0):
 outer=octagon(.84-e,.45-e,.07+(math.sqrt(2)-2)*e);inner=octagon(.77+e,.38+e,.035+(2-math.sqrt(2))*e)
 vs=[(x,y,z) for poly,z in[(outer,.19+e),(outer,1.08-e),(inner,1.08-e),(inner,.25-e)] for x,y in poly];fs=[tuple(reversed(range(8))),tuple(range(24,32))]
 for i in range(8):
  j=(i+1)%8;fs.extend([(i,j,8+j,8+i),(8+i,8+j,16+j,16+i),(16+i,16+j,24+j,24+i)])
 return mesh(vs,fs,0,'One complete closed thick outer vat with long chamfered profile, full 60 mm bottom, all four walls and complete top shoulder.')
G[BODY]=shell();solid('OuterVat_EntireBottomWallsAndRim',shell(.001),[BODY],'Whole 1 mm planar-inset connected shell material: complete bottom, inner and outer chamfer corners, all walls and the entire top rim.')
def isolated(name,g,targets,role):ISOLATED_VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
inside_poly=octagon(.769,.379,.035+(2-math.sqrt(2))*.001)
isolated('OuterVat_WholeIsolatedDeepCavity',prism(inside_poly,.251,1.081),[BODY],'Entire finite chamfered vat cavity and rim mouth, 1 mm boundary inset. Basket is omitted only for this isolated cavity predicate.')
# Cartesian closed perforated material is built from its own original full grid,
# retaining shared material boundaries around every true hole and every corner.
XC=[-.48,-.24,0,.24,.48];YC=[-.125,.125];ZH=[(.51,.70),(.77,.98)]
def basket(e=0):
 xo=.67-e;xi=.642+e;yo=.28-e;yi=.252+e;xh=.075+e;yh=.065+e
 xs=sorted(set([- .835+e,-xo,-xi,xi,xo,.835-e]+[c+d for c in XC for d in[-xh,xh]]))
 ys=sorted(set([-yo,-yi,-.12+e,.12-e,yi,yo]+[c+d for c in YC for d in[-yh,yh]]))
 zs=sorted(set([.4+e,.43-e,1.08+e,1.115-e]+[q for a,b in ZH for q in[a-e,b+e]]))
 def occupied(x,y,z):
  xhole=any(abs(x-c)<xh for c in XC);yhole=any(abs(y-c)<yh for c in YC);window=any(a-e<z<b+e for a,b in ZH)
  floor=abs(x)<xo and abs(y)<yo and z<.43-e and not(xhole and yhole)
  walls=abs(x)<xo and abs(y)<yo and ((abs(y)>yi and not(xhole and window)) or (abs(x)>xi and not(yhole and window)))
  ears=xi<abs(x)<.835-e and abs(y)<.12-e and z>1.08+e
  return floor or walls or ears
 return grid(xs,ys,zs,occupied,1,'One complete connected thick basket: ten floor through-holes, twenty-eight four-wall windows, continuous top rim and both integral full-thickness end ears.')
G[BASKET]=basket();solid('Basket_EntireFourWallsFloorRimAndEars',basket(.001),[BASKET],'Whole connected 1 mm inset basket material, with every hole enlarged by 1 mm and every outer surface inset; includes all four walls, all floor grid bars, every corner, full rim and two rooted end ears.')
contact('BothCompleteEndEarShoulderSeats',BODY,BASKET,(0,0,1),(.8025,0,1.08),2*.065*.24-.000001,points=[(-.8025,0,1.08),(.8025,0,1.08)])
air('Basket_WholeWorkingCavityAndMouth',box((-.641,-.251,.431),(.641,.251,1.31)),'Entire inner basket working cavity from full floor to above the entire rim mouth, 1 mm boundary inset; no liquid or solid fill.')
air('WholeUnderBasketVoid',prism(inside_poly,.251,.399),'Entire outer-vat footprint below the basket, including all inner chamfered corners. A full 150 mm bottom gap with 1 mm top/bottom and wall insets.')
def annulus(outer,inner,z0,z1):
 n=len(outer);assert n==len(inner);vs=[(x,y,z) for poly,z in[(outer,z0),(outer,z1),(inner,z1),(inner,z0)] for x,y in poly];fs=[]
 for k in range(4):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,((k+1)%4)*n+j,((k+1)%4)*n+i))
 return mesh(vs,fs)
# Eight distinct collinear-capable inner stations form a true rectangular hole.
# This is one closed annular volume covering all four gaps plus every corner.
a=.671;b=.281;inner_rect=[(-a/2,-b),(a/2,-b),(a,-b),(a,b),(a/2,b),(-a/2,b),(-a,b),(-a,-b)]
air('WholeFourSideBasketToVatAir',annulus(inside_poly,inner_rect,.399,1.079),'Whole finite continuous four-sided annular air corridor around the basket, including all outer chamfer corners; 1 mm basket and vat insets, terminates 1 mm beneath the two intentional end-ear bearing faces.')
for ix,x in enumerate(XC):
 for iy,y in enumerate(YC):
  n=f'FloorThroughHole_{ix+1}_{iy+1}';FLOOR_HOLES.append(n)
  air(n,box((x-.074,y-.064,.399),(x+.074,y+.064,.431)),'Entire full-thickness floor hole and both mouths, 1 mm aperture-side inset; actual assembly must remain clear.')
for side in[-1,1]:
 for ix,x in enumerate(XC):
  for iz,(a,b) in enumerate(ZH):
   n=f'LongWallWindow_{side}_{ix+1}_{iz+1}';SIDE_WINDOWS.append(n);y0,y1=(.251,.281) if side>0 else(-.281,-.251)
   air(n,box((x-.074,y0,a+.001),(x+.074,y1,b-.001)),'Entire full-thickness long-wall window and both mouths, including complete finite height and width, 1 mm edge inset.')
 for iy,y in enumerate(YC):
  for iz,(a,b) in enumerate(ZH):
   n=f'EndWallWindow_{side}_{iy+1}_{iz+1}';SIDE_WINDOWS.append(n);x0,x1=(.641,.671) if side>0 else(-.671,-.641)
   air(n,box((x0,y-.064,a+.001),(x1,y+.064,b-.001)),'Entire full-thickness short-end wall window and both mouths, 1 mm aperture-side inset.')
# Two separate closed thick rectangular lifting rings, all four sides present.
def ring(cx,e=0):
 return grid([cx-.012+e,cx+.012-e],[-.19+e,-.15-e,.15+e,.19-e],[1.115+e,1.155-e,1.295+e,1.335-e],lambda x,y,z:abs(y)>.15+e or z<1.155-e or z>1.295+e,3,'Complete closed thick lifting ring with true full-thickness inner hole and full bottom-rim finite root.')
for side in[-1,1]:
 cx=side*.656;n=f'CompleteEndLiftRing_{side}';HANDLES.append(n);G[n]=ring(cx)
 contact(n+'_WholeRimRoot',BASKET,n,(0,0,1),(cx,0,1.115),.024*.38-.000001)
 solid(n+'_EntireFourSideMaterial',ring(cx,.001),[n],'Whole 1 mm inset material around all four sides of the true ring opening, including its full bottom finite root.')
 air(n+'_WholeThroughHole',box((cx-.013,-.149,1.156),(cx+.013,.149,1.294)),'Whole finite through-ring air across the full ring thickness and both mouths, 1 mm aperture-side inset.')
# Complete original lower closed frame, whose full top is opposed to vat floor.
def frame(e=0):return grid([-.72+e,-.60-e,.60+e,.72-e],[-.34+e,-.22-e,.22+e,.34-e],[.12+e,.19-e],lambda x,y,z:abs(x)>.60+e or abs(y)>.22+e,2,'One continuous closed rectangular underframe with broad complete outer-vat underside support and open central space.')
G[FRAME]=frame();solid('Underframe_EntireConnectedMaterial',frame(.001),[FRAME],'Whole 1 mm inset four-sided underframe material, every corner and the full footprint between all four feet and vat bottom.')
contact('WholeFrameToVatUnderside',FRAME,BODY,(0,0,1),(0,-.28,.19),1.44*.68-1.20*.44-.000001,points=[(0,-.28,.19),(0,.28,.19),(-.66,0,.19),(.66,0,.19)])
air('WholeOpenUnderframeCenter',box((-.599,-.219,.001),(.599,.219,.189)),'Complete finite central underframe opening from 1 mm above ground to 1 mm below the vat floor, all four corners included.')
for ix,cx in enumerate([-.66,.66]):
 for iy,cy in enumerate([-.28,.28]):
  n=f'WholeFlatFoot_{ix+1}_{iy+1}';FEET.append(n);lo=(cx-.06,cy-.05,0);hi=(cx+.06,cy+.05,.12)
  G[n]=box(lo,hi,4,'Complete thick short foot with full finite flat ground sole and complete underframe top seat.')
  solid(n+'_WholeMaterial',box((cx-.059,cy-.049,.001),(cx+.059,cy+.049,.119)),[n],'Whole 1 mm inset foot material from complete ground sole to upper support face.')
  contact(n+'_WholeUnderframeSeat',n,FRAME,(0,0,1),(cx,cy,.12),.12*.10-.000001)
  FOOT_CONTACTS.append({'mesh':n,'name':n+'_FullGroundSole','x':cx,'y':cy,'half_x':.06,'half_y':.05,'minimum_area_m2':.12*.10-.000001})
for r in VOID_VOLUMES.values():
 if r['targets'] is None:r['targets']=list(G)
CONTRACT={'single_prop_count':1,'continuous_deep_outer_vats':1,'complete_four_wall_baskets':1,'integral_finite_end_ears':2,'closed_lifting_rings':2,'complete_floor_holes':len(FLOOR_HOLES),'complete_four_wall_windows':len(SIDE_WINDOWS),'complete_flat_feet':4,'bottom_clearance_m':.15,'long_side_clearance_m':.10,'short_end_clearance_m':.10,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'motion_dyeing_fluid_chemical_material_or_safety_claim':False}
def measure_dye_vat_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 assert abs(min(p[2] for p in vertices[BASKET])-.4)<2e-7
 assert abs(max(p[2] for p in vertices[BODY])-1.08)<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; full empty/material volumes, complete bearing faces, self-intersections, all-pair separation and necessary real negative controls required')
INSIDE_TESTS=[(BODY,(0,0,.22),(0,0,.30)),(BASKET,(.63,0,.415),(0,0,.60)),(FRAME,(.66,0,.155),(0,0,.155))]
FOCUS=(0,0,.64);ORTHO=2.25
CAMERAS={'gray-front3q':(2.5,-3.6,3.4),'gray-back3q':(-2.5,3.6,3.4),'thumbnail':(2.5,-3.6,3.4),'qa-front':(0,-4,1.9),'qa-side':(4,0,1.9),'qa-top':(0,0,4),'qa-back':(0,4,1.9),'qa-wireframe':(2.5,-3.6,3.4),'silhouette-128-front':(0,-4,1.9),'silhouette-128-side':(4,0,1.9)}
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
root=bpy.data.objects.new('OneSuspendedBasketDyeVat',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_dye_vat_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'dye_vat_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
