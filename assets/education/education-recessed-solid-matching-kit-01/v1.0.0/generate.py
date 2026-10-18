"""One original recessed solid matching set. Four closed meshes, one prop.
Metres, source Z up, front -Y. Fixed seated display only; no use or safety claim.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='education-recessed-solid-matching-kit-01';VERSION='1.0.0';TITLE='Recessed Solid Matching Kit'
DESCRIPTION=('One complete static geometric matching set, counted as one prop: one connected thick rectangular board has three real blind cavities with circular, triangular and square profiles, holding a circular cylinder, a triangular prism and a square pyramid. Each separate closed solid has its complete flat base seated on the cavity floor, positive side clearance around its full perimeter and its distinctive upper shape exposed. The board has continuous outer walls, actual inward cavity walls and 24 mm of material below the cavity floors. Cavities are actual geometry, never dark overlays. Four editable closed meshes, four opaque constant PBR materials, metres, source Z up, front -Y and ground-centre origin. No textures, words, characters, table or surrounding scene. '
'Static visual geometry only. No teaching or cognitive outcome, age suitability, human fit, child or toy safety, swallowing safety, material feel, insertion path, manipulation, interactive control, animation, dynamic assembly, manufacturing tolerance, strength, loading or safety certification. Dimensions define visual geometry only.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];CAVITIES=[]
PALETTE=[('Board_WarmMaple',(.58,.365,.17,1),.72,0),('Cylinder_Terracotta',(.63,.125,.065,1),.57,0),('Prism_DeepTeal',(.035,.32,.31,1),.57,0),('Pyramid_GoldenOchre',(.79,.48,.055,1),.57,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
FLOOR=.024;TOP=.085;CELL=.32;DEPTH=.40;CENTERS=[-.32,0,.32]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def polygon_area(p):return abs(sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1])))/2

def mesh(name,vs,fs,mat,role):
 assert name not in G
 G[name]={'vertices':[tuple(0. if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':mat,'role':role};return name

def ngon(n,r,angle=0):return [(r*math.cos(angle+math.tau*i/n),r*math.sin(angle+math.tau*i/n)) for i in range(n)]
PROFILES=[ngon(24,.112),ngon(3,.142,math.pi/2),[(-.117,-.117),(.117,-.117),(.117,.117),(-.117,.117)]]
SOLID_PROFILES=[ngon(24,.092),ngon(3,.106,math.pi/2),[(-.09,-.09),(.09,-.09),(.09,.09),(-.09,.09)]]
HEIGHTS=[.220,.225,.270];SHAPE_NAMES=['Cylinder_CircularSection','Prism_TriangularSection','Pyramid_SquareBase']
# Every tile uses the same mirror-symmetric outer subdivisions, so merging
# the tile rims produces one true watertight board without internal faces.
a0=math.atan2(DEPTH/2,CELL/2)
angles={round((math.tau*i/24)%(math.tau),12) for i in range(24)}
angles.update(round(a%math.tau,12) for a in [a0,math.pi-a0,math.pi+a0,math.tau-a0])
ANGLES=sorted(angles)
def ray_polygon(poly,d):
 limits=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);den=cross2(e,d)
  if den< -1e-10:limits.append(cross2(e,a)/den)
 return mul(d,min(t for t in limits if t>0))
vs=[];fs=[];lookup={}
def vertex(p):
 p=tuple(0. if abs(x)<1e-9 else round(x,7) for x in p)
 if p not in lookup:lookup[p]=len(vs);vs.append(p)
 return lookup[p]
for ci,(cx,profile) in enumerate(zip(CENTERS,PROFILES)):
 outer=[];inner=[];floor=[]
 for a in ANGLES:
  d=(math.cos(a),math.sin(a));r=min(CELL/2/max(abs(d[0]),1e-15),DEPTH/2/max(abs(d[1]),1e-15));q=ray_polygon(profile,d)
  outer.append(vertex((cx+d[0]*r,d[1]*r,TOP)));inner.append(vertex((cx+q[0],q[1],TOP)));floor.append(vertex((cx+q[0],q[1],FLOOR)))
 center=vertex((cx,0,FLOOR));n=len(outer)
 for j in range(n):
  k=(j+1)%n
  fs.append((outer[j],outer[k],inner[k],inner[j]))
  fs.append((inner[j],inner[k],floor[k],floor[j]))
  fs.append((center,floor[j],floor[k]))
 CAVITIES.append({'index':ci,'centre_xy_m':(cx,0),'profile':profile,'wall_top_indices':inner,'wall_floor_indices':floor,'solid':SHAPE_NAMES[ci]})
# The only one-use edges after the top/floor shells are the external perimeter.
edges=collections.Counter(tuple(sorted((a,b))) for f in fs for a,b in zip(f,f[1:]+f[:1]));boundary=[]
for f in fs:
 for a,b in zip(f,f[1:]+f[:1]):
  if edges[tuple(sorted((a,b)))]==1:boundary.append((a,b))
bottom_center=vertex((0,0,0))
for a,b in boundary:
 pa,pb=vs[a],vs[b];assert abs(pa[2]-TOP)<1e-7 and abs(pb[2]-TOP)<1e-7
 aa=vertex((pa[0],pa[1],0));bb=vertex((pb[0],pb[1],0));fs.append((b,a,aa,bb));fs.append((bottom_center,bb,aa))
BOARD=mesh('Board_ThreeTrueBlindCavities',vs,fs,0,'one connected closed board with three real differently shaped blind cavities, continuous thick walls and 24 mm material below each floor');FEET.append(BOARD)
for ci,(cx,poly,height,name) in enumerate(zip(CENTERS,SOLID_PROFILES,HEIGHTS,SHAPE_NAMES)):
 n=len(poly);v=[(cx+x,y,FLOOR) for x,y in poly];f=[tuple(reversed(range(n)))]
 if ci<2:
  v += [(cx+x,y,FLOOR+height) for x,y in poly];f.append(tuple(n+j for j in range(n)));f += [(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 else:
  v.append((cx,0,FLOOR+height));f += [(j,(j+1)%n,n) for j in range(n)]
 mesh(name,v,f,ci+1,['genuine circular cylinder with 24-sided circular section and two parallel end faces','genuine triangular prism with two parallel triangular end faces','genuine square-based pyramid with four sloped triangular sides meeting at one apex'][ci])
 CONTACTS.append({'a':BOARD,'b':name,'plane_z_m':FLOOR,'expected_contact_area_m2':polygon_area(poly),'nature':'whole opposing base/floor finite contact, no solid penetration'})
 # Whole-annulus clearance is evaluated using every cavity plane against
 # every actual solid vertex. These rays additionally expose the true floor.
 for j,(a,b) in enumerate(zip(PROFILES[ci],PROFILES[ci][1:]+PROFILES[ci][:1])):
  mid=mul(add(a,b),.5);outer=add((cx,0),mul(mid,.94));GAPS.append({'label':f'VisibleSideGap_{ci+1}_{j+1}','origin_m':(outer[0],outer[1],TOP+.015),'direction':(0,0,-1),'length_m':TOP-FLOOR+.014})
# Finite closed annular wedges collectively cover every cavity side gap,
# inset 1 mm from physical surfaces to keep a strict empty-volume predicate.
for ci,(cx,hole,base) in enumerate(zip(CENTERS,PROFILES,SOLID_PROFILES)):
 n=len(hole)
 for j in range(n):
  k=(j+1)%n
  inner=[mul(base[t],1.025) for t in [j,k]];outer=[mul(hole[t],.985) for t in [j,k]]
  poly=[inner[0],outer[0],outer[1],inner[1]]
  vv=[(cx+x,y,z) for z in [FLOOR+.001,TOP-.001] for x,y in poly]
  ff=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
  centre=tuple(sum(p[t] for p in vv)/8 for t in range(3))
  VOID_VOLUMES[f'WholeSideGap_{ci+1}_Sector{j+1}']={'vertices':vv,'faces':ff,'role':'complete finite side-gap wedge, including hidden rear and floor-adjacent air; all wedges form one full annular gap','enclosed_fill_center_m':centre}
def convex_hull(points):
 pts=sorted(set((round(float(p[0]),7),round(float(p[1]),7)) for p in points))
 def half(pp):
  out=[]
  for p in pp:
   while len(out)>=2 and cross2(sub(out[-1],out[-2]),sub(p,out[-1]))<=1e-8:out.pop()
   out.append(p)
  return out
 return half(pts)[:-1]+half(pts[::-1])[:-1]
def clip_polygon(poly,clip):
 out=list(poly)
 for a,b in zip(clip,clip[1:]+clip[:1]):
  old=out;out=[];edge=sub(b,a)
  if not old:break
  for p,q in zip(old,old[1:]+old[:1]):
   dp=cross2(edge,sub(p,a));dq=cross2(edge,sub(q,a));ip=dp>=-1e-9;iq=dq>=-1e-9
   if ip!=iq:out.append(add(p,mul(sub(q,p),dp/(dp-dq))))
   if iq:out.append(q)
 return out

def measure_matching_geometry(vertices,triangles=None):
 assert set(vertices)==set(G),'Changed component set'
 board=vertices[BOARD];assert abs(min(p[2] for p in board))<1e-6 and abs(max(p[2] for p in board)-TOP)<1e-6
 rows=[]
 for ci,(cx,name) in enumerate(zip(CENTERS,SHAPE_NAMES)):
  vv=vertices[name];bottom=min(p[2] for p in vv);highest=max(p[2] for p in vv)
  assert abs(bottom-FLOOR)<1e-6,('Actual solid detached from cavity floor',name,bottom)
  assert abs(highest-FLOOR-HEIGHTS[ci])<1e-6,('Actual height changed',name,highest)
  boundary=convex_hull([p for p in board if abs(p[2]-FLOOR)<1e-6 and abs(p[0]-cx)<CELL/2-1e-6]);base=convex_hull([p for p in vv if abs(p[2]-bottom)<1e-6])
  assert len(boundary)==[24,3,4][ci] and len(base)==[24,3,4][ci],('Changed actual section',name,len(boundary),len(base))
  clearances=[]
  for a,b in zip(boundary,boundary[1:]+boundary[:1]):
   edge=sub(b,a);length=math.hypot(*edge);ds=[cross2(edge,sub((p[0],p[1]),a))/length for p in vv]
   clearances.append(min(ds))
  assert min(clearances)>.0179,('Actual full-perimeter side clearance missing',name,min(clearances))
  expected=[.020*math.cos(math.pi/24),.018,.027][ci]
  assert abs(min(clearances)-expected)<2e-6,('Changed full side gap',name,min(clearances),expected)
  base_area=polygon_area(base);assert abs(base_area-CONTACTS[ci]['expected_contact_area_m2'])<2e-7
  top=[p for p in vv if abs(p[2]-highest)<1e-6];assert len(set(tuple(round(float(c),7) for c in p) for p in top))==[24,3,1][ci],('Wrong upper topology',name)
  floor_overlap=base_area;floor_triangle_count=None
  if triangles is not None:
   floor_tris=[t for t in triangles[BOARD] if max(abs(p[2]-FLOOR) for p in t)<1e-6 and all(abs(p[0]-cx)<CELL/2-1e-6 for p in t)]
   floor_overlap=sum(polygon_area(clip_polygon([(float(p[0]),float(p[1])) for p in t],base)) for t in floor_tris)
   floor_triangle_count=len(floor_tris)
   assert abs(floor_overlap-base_area)<2e-7,('Actual complete finite floor support missing',name,floor_overlap,base_area)
  rows.append({'solid':name,'actual_cavity_polygon_xy_m':boundary,'actual_base_polygon_xy_m':base,'actual_minimum_all_wall_planes_to_all_solid_vertices_m':min(clearances),'actual_bottom_z_m':bottom,'actual_top_z_m':highest,'actual_whole_base_area_m2':base_area,'actual_floor_support_overlap_m2':floor_overlap,'actual_floor_triangles':floor_triangle_count,'upper_above_board_m':highest-TOP})
 return {'single_prop_count':1,'closed_mesh_count':4,'actual_floor_thickness_m':FLOOR,'actual_cavity_depth_m':TOP-FLOOR,'matching_pairs':rows,'fixed_seated_state_only':True,'interactive_or_dynamic_claim':False}
FOCUS=(0,0,.142);ORTHO=1.22
CAMERAS={'gray-front3q':(1.1,-2.5,2.6),'gray-back3q':(-1.1,2.5,2.6),'thumbnail':(1.1,-2.5,2.6),'qa-front':(0,-3,1.25),'qa-side':(3,0,1.5),'qa-top':(0,0,4),'qa-back':(0,3,1.25),'qa-wireframe':(1.1,-2.5,2.6),'silhouette-128-front':(0,-3,1.25),'silhouette-128-side':(3,0,1.5)}
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
root=bpy.data.objects.new('OneRecessedSolidMatchingKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
matching_evidence=dict(measure_matching_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts},{o.name:[[tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices] for t in o.data.loop_triangles] for o in parts}),material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'matching_geometry':matching_evidence,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/education/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'education','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
