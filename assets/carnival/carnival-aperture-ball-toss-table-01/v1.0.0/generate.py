"""One original aperture ball toss table, four real through-holes, one prop.
Metres, source Z up, front -Y. Static visual geometry only.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carnival-aperture-ball-toss-table-01';VERSION='1.0.0';TITLE='Aperture Ball Toss Table'
DESCRIPTION=('One complete static carnival ball toss table, counted as one prop. A 25-degree inclined 65 mm thick connected target board has four real polygonal circular through-holes, each with continuous visible inner walls and a flush ochre material rim. The holes are geometry, not black discs. Two separate side rails and sloped side cheeks carry the board over a collection cavity with a solid floor, side and rear walls and an open front retrieval side above a low lip. Four separate upright legs, two side stretchers and two cross stretchers connect the assembly to four finite floor-contact patches. The below-board cavity and all four target passages are genuinely empty. Editable closed meshes, opaque constant PBR colours, metres, source Z up, front -Y and ground-centre origin. No textures, labels, characters, loose balls, ring posts, basketball hoop, pinball mechanisms or surrounding scene. '
'Static visual geometry only. No throwing trajectory, ball motion, bounce, hole-entry probability, automatic ball return, scoring, payment, game rules, gameplay completeness, human fit, load capacity, anti-tip performance, operation, amusement-facility or child safety certification. No legacy ball or scene compatibility claim. Dimensions define visual geometry only.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];APERTURES=[]
PALETTE=[('Target_CarnivalCoral',(.63,.105,.055,1),.62,0),('TargetRims_GoldenOchre',(.86,.52,.085,1),.57,0),('Frame_DeepTeal',(.025,.25,.265,1),.63,0),('Collection_WarmLinen',(.66,.53,.34,1),.72,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
ANGLE=math.radians(25);C=math.cos(ANGLE);S=math.sin(ANGLE);BOARD_Z=1.15;THICK=.065;RADIUS=.18
CELL_X=.72;CELL_Y=.64;CENTERS=[(-.36,-.32),(.36,-.32),(-.36,.32),(.36,.32)]
BOX_FACES=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def polygon_area(p):return abs(sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1])))/2

def panel_point(x,v,w):return (x,C*v-S*w,BOARD_Z+S*v+C*w)
def panel_local(p):return (p[0],C*p[1]+S*(p[2]-BOARD_Z),-S*p[1]+C*(p[2]-BOARD_Z))
def mesh(name,vs,fs,mat,role):
 assert name not in G
 G[name]={'vertices':[tuple(0. if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':mat,'role':role};return name

def box_geometry(lo,hi,transform=lambda x:x):
 x,y,z=lo;X,Y,Z=hi
 return {'vertices':[transform(p) for p in [(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]],'faces':BOX_FACES}
def box(name,lo,hi,mat,role,transform=lambda x:x):
 g=box_geometry(lo,hi,transform);return mesh(name,g['vertices'],g['faces'],mat,role)
def link(a,b,p):LINKS.append((a,b,[p]))
def voidbox(name,lo,hi,role,transform=lambda x:x):
 g=box_geometry(lo,hi,transform);g.update({'role':role,'enclosed_fill_center_m':tuple(sum(p[i] for p in g['vertices'])/8 for i in range(3))});VOID_VOLUMES[name]=g
# Four rectangular tiles share all seam subdivisions. Top and bottom surfaces
# merge into one connected thick plate; only true hole walls and outer walls remain.
a0=math.atan2(CELL_Y/2,CELL_X/2)
angles={round((math.tau*i/24)%math.tau,12) for i in range(24)}
angles.update(round(a%math.tau,12) for a in [a0,math.pi-a0,math.pi+a0,math.tau-a0]);ANGLES=sorted(angles)
vs=[];fs=[];fm=[];lookup={}
def vertex(p):
 p=tuple(0. if abs(x)<1e-9 else round(float(x),7) for x in p)
 if p not in lookup:lookup[p]=len(vs);vs.append(p)
 return lookup[p]
def face(f,m):fs.append(tuple(f));fm.append(m)
for ci,(cx,cy) in enumerate(CENTERS):
 loops=[]
 for w in [-THICK/2,THICK/2]:
  rings=[]
  for kind in ['outer','rim','inner']:
   ids=[]
   for a in ANGLES:
    d=(math.cos(a),math.sin(a));r=min(CELL_X/2/max(abs(d[0]),1e-15),CELL_Y/2/max(abs(d[1]),1e-15)) if kind=='outer' else (.22 if kind=='rim' else RADIUS)
    ids.append(vertex((cx+d[0]*r,cy+d[1]*r,w)))
   rings.append(ids)
  loops.append(rings)
 n=len(ANGLES)
 for j in range(n):
  k=(j+1)%n
  for upper in [0,1]:
   for ri in [0,1]:
    a,b=loops[upper][ri:ri+2];f=(a[j],a[k],b[k],b[j]);face(f if upper else tuple(reversed(f)),1 if upper and ri==1 else (0 if upper else 3))
  low=loops[0][2];high=loops[1][2];face((high[j],high[k],low[k],low[j]),3)
 APERTURES.append({'index':ci,'centre_local_xy_m':(cx,cy),'radius_m':RADIUS,'inner_top_indices':loops[1][2],'inner_bottom_indices':loops[0][2]})
# Boundary edges occur only on outer perimeter, because the internal seams
# and the true hole walls already have two adjacent faces.
edges=collections.Counter(tuple(sorted((a,b))) for f in fs for a,b in zip(f,f[1:]+f[:1]));boundary=[]
for f in fs:
 for a,b in zip(f,f[1:]+f[:1]):
  if edges[tuple(sorted((a,b)))]==1 and vs[a][2]>0 and vs[b][2]>0:boundary.append((a,b))
for a,b in boundary:
 pa,pb=vs[a],vs[b];aa=vertex((pa[0],pa[1],-THICK/2));bb=vertex((pb[0],pb[1],-THICK/2));face((b,a,aa,bb),0)
BOARD=mesh('TargetBoard_FourTrueThroughHoles',[panel_point(*p) for p in vs],fs,0,'one connected inclined thick board; four genuine full-depth bores; flush coloured rim regions are same continuous surface');G[BOARD]['face_materials']=fm
for ci,(cx,cy) in enumerate(CENTERS):
 # Complete finite polygonal cylinder covers hole and 167.5 mm air beneath it.
 radius=RADIUS-.003;v=[panel_point(cx+radius*math.cos(a),cy+radius*math.sin(a),w) for w in [-.20,.045] for a in ANGLES];n=len(ANGLES)
 f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 VOID_VOLUMES[f'ThroughHole_{ci+1}_FullPassage']={'vertices':v,'faces':f,'role':'whole finite through-hole including continuous inner-wall clearance and open below-board region','enclosed_fill_center_m':panel_point(cx,cy,-.075)}
 for dx,dy in [(0,0),(.12,0),(-.12,0),(0,.12),(0,-.12)]:
  r={'label':f'Hole_{ci+1}_{dx}_{dy}','origin_m':panel_point(cx+dx,cy+dy,.05),'direction':(0,S,-C),'length_m':.255};GAPS.append(r);BORES.append(dict(r,mesh=BOARD))
# Side rails overlap only the actual solid edge bands, never any aperture.
for side,sgn in [('Left',-1),('Right',1)]:
 x=sgn*.735;rail=box('InclinedRail_'+side,(x-.04,-.665,-.105),(x+.04,.665,-.015),2,'separate inclined edge rail supporting the panel',lambda p:panel_point(*p))
 link(BOARD,rail,panel_point(sgn*.707,0,-.024))
 # An actual sloped-top closed prism; top and bottom are not an AABB proxy.
 lo,hi=x-.03,x+.03;y0,y1=-.64,.70;z0=.460
 top=lambda y:BOARD_Z+y*math.tan(ANGLE)-.060/C
 v=[(lo,y0,z0),(hi,y0,z0),(hi,y1,z0),(lo,y1,z0),(lo,y0,top(y0)),(hi,y0,top(y0)),(hi,y1,top(y1)),(lo,y1,top(y1))]
 wall=mesh('CollectionSideCheek_'+side,v,BOX_FACES,3,'thick sloped side wall with real inner face and solid bottom connection')
 link(rail,wall,panel_point(x,0,-.080))
FLOOR=box('CollectionFloor_ContinuousSolid',(-.775,-.75,.425),(.775,.75,.475),3,'continuous 50 mm solid collection floor with visible open front')
BACK=box('CollectionRearWall',(-.755,.65,.455),(.755,.72,.99),3,'real 70 mm rear wall closing collection cavity at the back')
LIP=box('CollectionFrontLowLip',(-.760,-.743,.455),(.760,-.69,.555),0,'low front retaining lip; open retrieval space above')
link(FLOOR,BACK,(0,.68,.465));link(FLOOR,LIP,(0,-.72,.465))
for side,sgn in [('Left',-1),('Right',1)]:
 wall='CollectionSideCheek_'+side;link(FLOOR,wall,(sgn*.735,0,.465));link(BACK,wall,(sgn*.735,.68,.60))
 for end,y in [('Front',-.55),('Back',.55)]:
  leg=box('Leg_'+side+'_'+end,(sgn*.68-.0475,y-.0475,0),(sgn*.68+.0475,y+.0475,.455),2,'separate upright leg with finite flat ground patch');FEET.append(leg);link(FLOOR,leg,(sgn*.68,y,.440))
 brace=box('SideStretcher_'+side,(sgn*.68-.035,-.55,.245),(sgn*.68+.035,.55,.315),2,'lower side frame stretcher joining independent front and rear legs')
 for end,y in [('Front',-.55),('Back',.55)]:link(brace,'Leg_'+side+'_'+end,(sgn*.68,y+(.018 if y<0 else -.018),.28))
for end,y in [('Front',-.55),('Back',.55)]:
 brace=box('CrossStretcher_'+end,(-.68,y-.032,.15),(.68,y+.032,.214),2,'cross stretcher connecting left and right leg frames')
 for side,sgn in [('Left',-1),('Right',1)]:link(brace,'Leg_'+side+'_'+end,(sgn*.662,y,.18))
# Full collection volume is a sloped-top prism, following actual underside.
x0,x1=-.69,.69;y0,y1=-.68,.64;z0=.480;top=lambda y:BOARD_Z+y*math.tan(ANGLE)-.041/C
v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,top(y0)),(x1,y0,top(y0)),(x1,y1,top(y1)),(x0,y1,top(y1))]
VOID_VOLUMES['CollectionCavity_FullSlopedVolume']={'vertices':v,'faces':BOX_FACES,'role':'entire below-board collection cavity, including rear, floor-adjacent and side-adjacent hidden air','enclosed_fill_center_m':(0,0,.75)}
voidbox('FrontRetrievalOpening_FullFinite',(-.69,-.77,.565),(.69,-.635,.78),'full finite open retrieval entrance above front lip')
for x in [-.6,0,.6]:GAPS.append({'label':'FrontRetrieval_'+str(x),'origin_m':(x,-.78,.67),'direction':(0,1,0),'length_m':1.41})

def unique(points):return sorted(set(tuple(round(float(c),6) for c in p) for p in points))
def measure_table_geometry(vertices,triangles=None):
 assert set(vertices)==set(G),'Changed component set'
 local=[panel_local(p) for p in unique(vertices[BOARD])];ww=[p[2] for p in local]
 assert abs(min(ww)+THICK/2)<2e-6 and abs(max(ww)-THICK/2)<2e-6,'Actual full board thickness missing'
 assert all(abs(abs(w)-THICK/2)<2e-6 for w in ww),'Actual board surfaces changed'
 rows=[];expected_top_area=4*CELL_X*CELL_Y
 for ci,(cx,cy) in enumerate(CENTERS):
  ring=[]
  for side,w in [('top',THICK/2),('bottom',-THICK/2)]:
   v=unique([(p[0]-cx,p[1]-cy) for p in local if abs(p[2]-w)<2e-6 and abs(math.hypot(p[0]-cx,p[1]-cy)-RADIUS)<2e-6])
   assert len(v)==len(ANGLES),('Actual complete aperture rim missing',ci,side,len(v))
   v.sort(key=lambda p:math.atan2(p[1],p[0]));ring.append(v)
  assert all(min(math.dist(p,q) for q in ring[1])<3e-6 for p in ring[0]),'Through-wall top/bottom mismatch'
  area=polygon_area(ring[0]);perimeter=sum(math.dist(a,b) for a,b in zip(ring[0],ring[0][1:]+ring[0][:1]));expected_top_area-=area
  wall_area=None
  if triangles is not None:
   wall=[]
   for tri in triangles[BOARD]:
    p=[panel_local(q) for q in tri]
    if all(abs(math.hypot(q[0]-cx,q[1]-cy)-RADIUS)<2e-6 for q in p) and max(q[2] for q in p)-min(q[2] for q in p)>.06:wall.append(p)
   def ar(t):
    a,b=sub(t[1],t[0]),sub(t[2],t[0]);return math.sqrt(sum(c*c for c in (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])))/2
   wall_area=sum(ar(t) for t in wall);assert abs(wall_area-perimeter*THICK)<3e-6,('Incomplete actual through-wall triangles',ci,wall_area,perimeter*THICK)
  rows.append({'index':ci+1,'actual_top_and_bottom_polygon_vertices':len(ring[0]),'actual_aperture_area_m2':area,'actual_inner_wall_area_m2':wall_area,'actual_wall_depth_m':max(ww)-min(ww),'true_through_geometry':True})
 for name,lo,hi in [(FLOOR,.425,.475),(BACK,.455,.99),(LIP,.455,.555)]:
  z=[p[2] for p in vertices[name]];assert abs(min(z)-lo)<2e-6 and abs(max(z)-hi)<2e-6,('Actual collection wall/floor changed',name)
 for side in ['Left','Right']:
  name='CollectionSideCheek_'+side;v=vertices[name];span=max(p[0] for p in v)-min(p[0] for p in v);assert abs(span-.060)<2e-6,('Actual collection side thickness changed',name,span)
 support=[]
 for name in FEET:
  v=vertices[name];base=unique([p for p in v if abs(p[2])<1e-6]);assert len(base)==4,('Actual finite ground base missing',name)
  bc=(sum(q[0] for q in base)/4,sum(q[1] for q in base)/4);base.sort(key=lambda p:math.atan2(p[1]-bc[1],p[0]-bc[0]));area=polygon_area([(p[0],p[1]) for p in base]);assert abs(area-.095**2)<2e-6
  support.append({'leg':name,'actual_base_area_m2':area})
 return {'single_prop_count':1,'incline_degrees':25,'actual_normal_board_thickness_m':max(ww)-min(ww),'apertures':rows,'actual_expected_perforated_surface_area_m2':expected_top_area,'actual_edge_ligament_min_m':.14,'actual_hole_to_hole_ligament_min_m':.28,'solid_collection_floor_thickness_m':.05,'side_wall_thickness_m':.06,'finite_ground_support':support,'no_ball_motion_or_gameplay_claim':True}
FOCUS=(0,0,.74);ORTHO=2.55
CAMERAS={'gray-front3q':(3.4,-5.3,4.2),'gray-back3q':(-3.4,5.3,4.2),'thumbnail':(3.4,-5.3,4.2),'qa-front':(0,-5,2.6),'qa-side':(5,0,2.7),'qa-top':(0,0,5),'qa-back':(0,5,2.6),'qa-wireframe':(3.4,-5.3,4.2),'silhouette-128-front':(0,-5,2.6),'silhouette-128-side':(5,0,2.7)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneApertureBallTossTable',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
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
adj={o.name:set() for o in parts}
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
table_evidence=dict(measure_table_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts},{o.name:[[tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices] for t in o.data.loop_triangles] for o in parts}),material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'table_geometry':table_evidence,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carnival/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
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
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
