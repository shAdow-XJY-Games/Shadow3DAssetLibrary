"""Original static frame-supported laundry hamper cart, one complete prop.
Real empty thick fabric shell and folded cuff seated on a continuous frame.
Metres, Z up, front -Y, four finite grounded caster treads. No simulation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laundry-frame-hamper-cart-01';VERSION='1.0.0';TITLE='Frame-Supported Linen Hamper Cart'
DESCRIPTION=('One original static laundry hamper cart with an empty thick tapered fabric basket, gently folded faceted walls, a continuous thick floor and a broad turned-over top cuff. '
 'The cuff is genuinely seated into a separate complete metal top rim. Four slim posts, lower side rails and end crossbars connect to four separate fixed caster assemblies with real fork-side gaps and finite flat tread contacts. '
 'The open chamber and the space under the suspended basket remain visible; no laundry, solid filler, lid, floor platform or surrounding scene is included. '
 'Named closed editable components, five constant solid PBR materials, metres, source Z up, front -Y and ground-centre origin. One cart including basket, frame and four wheels counts as one prop. '
 'Independently authored fabric-hamper construction, not a harvest basket or produce crate with wheels or a recolored logistics cage. '
 'Static game-art only: no cloth deformation, folding, rolling, steering, carrying capacity, load, hygiene, ergonomics, washing-appliance compatibility, manufacture or safety certification.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];CLEARANCE_PAIRS=[];VOID_VOLUMES={}
PALETTE=[('Fabric_WarmLinen',(.57,.45,.28,1),.90,0),('Fold_PaleCanvas',(.83,.75,.54,1),.89,0),('Frame_MutedTeal',(.055,.26,.27,1),.53,.40),('Tread_Charcoal',(.028,.037,.043,1),.88,0),('Axle_SatinMetal',(.48,.55,.56,1),.42,.65)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
FBOX=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box_data(c,s):
 x,y,z=c;a,b,d=[q/2 for q in s];return {'vertices':[(x-a,y-b,z-d),(x+a,y-b,z-d),(x+a,y+b,z-d),(x-a,y+b,z-d),(x-a,y-b,z+d),(x+a,y-b,z+d),(x+a,y+b,z+d),(x-a,y+b,z+d)],'faces':FBOX}
def box(name,c,s,mat,role):
 d=box_data(c,s);return mesh(name,d['vertices'],d['faces'],mat,role)
def link(a,b,p,axis=(1,0,0),spread=.004):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
PERIM=[(-.8,-1),(-.4,-1),(0,-1),(.4,-1),(.8,-1),(1,-.8),(1,-.4),(1,0),(1,.4),(1,.8),(.8,1),(.4,1),(0,1),(-.4,1),(-.8,1),(-1,.8),(-1,.4),(-1,0),(-1,-.4),(-1,-.8)]
N=len(PERIM)
def outline(hx,hy,z,fold=0):
 # Small alternating side displacements are modeled folds, not a texture.
 return [(a*hx+(fold*(1 if i%2 else -1) if abs(a)==1 and abs(b)<.9 else 0),b*hy+(fold*(1 if i%2 else -1) if abs(b)==1 and abs(a)<.9 else 0),z) for i,(a,b) in enumerate(PERIM)]
# Continuous material solid: underside -> outer draping walls -> underfold ->
# broad turned cuff -> inner wall -> true sealed interior floor. It is not a box
# with an opaque dark lid. The mouth and full central chamber stay empty.
SECTIONS=[(.270,.170,.305,0),(.290,.190,.350,.003),(.325,.225,.550,.008),(.343,.243,.790,.004),(.349,.249,.838,0),(.387,.287,.838,0),(.390,.290,.861,0),(.326,.226,.861,0),(.326,.226,.815,0),(.308,.208,.550,.008),(.273,.173,.350,.003),(.255,.155,.329,0)]
vs=[v for row in SECTIONS for v in outline(*row)];fs=[];fm=[]
for j in range(len(SECTIONS)-1):
 for i in range(N):fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i));fm.append(1 if 3<=j<=7 else 0)
fs += [tuple(reversed(range(N))),tuple((len(SECTIONS)-1)*N+i for i in range(N))];fm += [0,0]
mesh('Hamper_ContinuousThickFabric',vs,fs,0,'one continuously closed thick fabric shell with real inner floor, tapered folded walls and a continuous broad support cuff');G['Hamper_ContinuousThickFabric']['face_materials']=fm
# Separate complete upper support frame, with a real open centre.
rows=[(.382,.282,.797,0),(.382,.282,.843,0),(.346,.246,.843,0),(.346,.246,.797,0)]
rv=[v for r in rows for v in outline(*r)];rf=[]
for j in range(4):
 for i in range(N):rf.append((j*N+i,j*N+(i+1)%N,((j+1)%4)*N+(i+1)%N,((j+1)%4)*N+i))
mesh('Frame_ContinuousUpperRim',rv,rf,2,'separate closed annular frame with empty centre; broad cuff underside overlaps the finite upper rim by 5 mm')
for x,y,axis in [(-.368,0,(0,1,0)),(.368,0,(0,1,0)),(0,-.268,(1,0,0)),(0,.268,(1,0,0))]:link('Hamper_ContinuousThickFabric','Frame_ContinuousUpperRim',(x,y,.8405),axis,.025)
# Four narrow posts avoid the chamfered bag corners. No cargo deck.
for si,x in [('L',-.330),('R',.330)]:
 rail=box('Chassis_SideRail_'+si,(x,0,.255),(.040,.550,.046),2,'low longitudinal chassis rail, without a solid platform')
 for ei,y in [('Front',-.250),('Rear',.250)]:
  tag=si+'_'+ei;post=box('Frame_Post_'+tag,(x,y,.510),(.034,.032,.610),2,'slim continuous corner post supports the rim and seats into caster bridge')
  link(post,'Frame_ContinuousUpperRim',(x,y,.806),axis=(0,0,1),spread=.004)
  link(post,rail,(x,y,.255),axis=(0,0,1),spread=.010)
for ei,y in [('Front',-.250),('Rear',.250)]:
 bar=box('Chassis_EndCrossbar_'+ei,(0,y,.275),(.680,.036,.042),2,'lower transverse frame member; open centre and suspended basket remain clear')
 for si,x in [('L',-.330),('R',.330)]:
  link(bar,'Frame_Post_'+si+'_'+ei,(x,y,.272),axis=(0,0,1),spread=.008)
  link(bar,'Chassis_SideRail_'+si,(x,y,.266),axis=(1,0,0),spread=.006)
# Original fixed caster set. Flat polygon facets yield finite tread contact.
C=math.cos(math.pi/16)
def cylinder_x(name,x0,x1,y,z,r,mat,role):
 n=16;pts=[(r*math.cos(math.pi/16+math.tau*i/n),r*math.sin(math.pi/16+math.tau*i/n)) for i in range(n)];vs=[(x,y+yy,z+zz) for x in [x0,x1] for yy,zz in pts]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
for si,x in [('L',-.330),('R',.330)]:
 for ei,y in [('Front',-.250),('Rear',.250)]:
  tag=si+'_'+ei;wheel=cylinder_x('Caster_Tread_'+tag,x-.021,x+.021,y,.080,.080/C,3,'fixed 16-sided solid wheel with finite flat bottom tread at ground Z zero');FEET.append(wheel)
  axle=cylinder_x('Caster_Axle_'+tag,x-.047,x+.047,y,.080,.011,4,'solid visible axle seats inside tire and both fork sides')
  link(wheel,axle,(x,y,.080),axis=(1,0,0),spread=.010)
  bridge=box('Caster_Bridge_'+tag,(x,y,.200),(.094,.065,.035),4,'top bridge joins both fork plates to the continuous frame post')
  link(bridge,'Frame_Post_'+tag,(x,y,.211),axis=(1,0,0),spread=.006)
  for side in [-1,1]:
   fork=box('Caster_Fork_'+tag+('_Inner' if side==-1 else '_Outer'),(x+side*.037,y,.1315),(.012,.046,.133),4,'fixed fork plate with 10 mm genuine axial clearance to wheel side')
   link(fork,axle,(x+side*.037,y,.080),axis=(1,0,0),spread=.003)
   link(fork,bridge,(x+side*.037,y,.190),axis=(0,1,0),spread=.008)
   CLEARANCE_PAIRS.append({'a':wheel,'b':fork,'axis':0,'minimum_m':.0099,'role':'actual wheel side to fork plate axial clearance'})
# Empty finite central chamber and air beneath the bottom. These probes are
# mathematical QA volumes only and never become asset meshes.
VOID_VOLUMES['Hamper_EmptyCentralChamber']=box_data((0,0,.595),(.470,.270,.510))
VOID_VOLUMES['SuspendedBottom_AirClearance']=box_data((0,0,.230),(.440,.240,.140))
for x in [-.20,0,.20]:
 for y in [-.10,0,.10]:
  FLOOR_PROBES.append({'mesh':'Hamper_ContinuousThickFabric','origin_m':(x,y,.880),'direction':(0,0,-1),'length_m':.700,'expected_hits_m':[.551,.575]})
  GAPS.append({'label':'empty_chamber_above_actual_floor','origin_m':(x,y,.850),'direction':(0,0,-1),'length_m':.505})
for p,d in [((0,0,.55),(1,0,0)),((0,0,.55),(-1,0,0)),((0,0,.55),(0,1,0)),((0,0,.55),(0,-1,0))]:
 WALL_PROBES.append({'mesh':'Hamper_ContinuousThickFabric','origin_m':p,'direction':d,'length_m':.45,'minimum_thickness_m':.0169,'maximum_thickness_m':.0171})
# Finite whole-box clipping catches any triangle entering the central chamber;
# model vertices and box corners supply enclosed-solid containment checks in
# independent QA. Diagnostic rays alone are never the cavity acceptance gate.
def triangle_box_intersects(triangle,lo,hi):
 polygon=[tuple(v) for v in triangle]
 for axis in range(3):
  for limit,sign in [(lo[axis],1),(hi[axis],-1)]:
   old=polygon;polygon=[]
   if not old:return False
   for start,end in zip(old,old[1:]+old[:1]):
    ds=(start[axis]-limit)*sign;de=(end[axis]-limit)*sign;si=ds>=-1e-10;ei=de>=-1e-10
    if si!=ei:polygon.append(add(start,mul(sub(end,start),ds/(ds-de))))
    if ei:polygon.append(end)
 return bool(polygon)
def measure_hamper_geometry(vertices,triangles):
 checks=[]
 for label,box in VOID_VOLUMES.items():
  lo=[min(v[i] for v in box['vertices']) for i in range(3)];hi=[max(v[i] for v in box['vertices']) for i in range(3)]
  blockers=[n for n,tt in triangles.items() if any(triangle_box_intersects(t,lo,hi) for t in tt)]
  assert not blockers,('Finite empty volume is blocked',label,blockers)
  checks.append({'name':label,'lo_m':lo,'hi_m':hi,'actual_surface_box_intersections':0})
 clear=[]
 for r in CLEARANCE_PAIRS:
  a=[v[r['axis']] for v in vertices[r['a']]];b=[v[r['axis']] for v in vertices[r['b']]];gap=max(min(a)-max(b),min(b)-max(a));assert gap>r['minimum_m'],(r,gap)
  clear.append(dict(r,actual_separation_m=gap))
 return {'finite_empty_volume_surface_checks':checks,'wheel_fork_clearances':clear,'floor_thickness_m':.024,'folded_cuff_rim_overlap_m':.005,'suspended_bottom_ground_height_m':.305,'fixed_four_wheel_pose':True,'counted_props':1,'simulation_tested':False}
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
root=bpy.data.objects.new('OneFrameSupportedLaundryCart',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.001,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
def actual_ray_distances(r):
 origin=Vector(r['origin_m']);direction=Vector(r['direction']).normalized();current=origin.copy();distances=[]
 for _ in range(8):
  q,_,_,_=trees[r['mesh']].ray_cast(current,direction,r['length_m'])
  if q is None:break
  distance=(q-origin).length
  if distance>r['length_m']:break
  distances.append(float(distance));current=q+direction*1e-5
 return distances
floor_checks=[];wall_checks=[]
for r in FLOOR_PROBES:
 distances=actual_ray_distances(r);assert len(distances)==2 and all(abs(distances[i]-r['expected_hits_m'][i])<2e-6 for i in range(2)),('Actual thick floor missing',r,distances)
 floor_checks.append(dict(r,actual_hit_distances_m=distances,actual_floor_thickness_m=distances[1]-distances[0]))
for r in WALL_PROBES:
 distances=actual_ray_distances(r);assert len(distances)==2 and r['minimum_thickness_m']<distances[1]-distances[0]<r['maximum_thickness_m'],('Actual thick wall missing',r,distances)
 wall_checks.append(dict(r,actual_hit_distances_m=distances,actual_wall_thickness_m=distances[1]-distances[0]))
hamper_evidence=measure_hamper_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts},{o.name:[[o.matrix_world@o.data.vertices[i].co for i in t.vertices] for t in o.data.loop_triangles] for o in parts})
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
 'single_prop_count':1,'hamper_geometry':dict(hamper_evidence,actual_floor_probes=floor_checks,actual_wall_probes=wall_checks),'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laundry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laundry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.435));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.22;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,3.8),'gray-back3q':(3,5,3.8)} if gray else {
 'thumbnail':(-3,-5,3.8),'qa-front':(0,-7,.435),'qa-side':(7,0,.435),'qa-top':(0,0,8),
 'qa-back':(0,7,.435),'qa-wireframe':(-3,-5,3.8)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.22
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0011;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.435)),('silhouette-128-side',(7,0,.435))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
