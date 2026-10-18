"""Original single-fin surfboard, one fixed deck-down rest pose.
Broad closed curved board plus a genuinely thick swept fin. No external assets.
Metres, Z up; nose -Y. All render geometry is freshly imported from actual GLB.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beach-single-fin-surfboard-01';VERSION='1.0.0';TITLE='Wide-Rail Single-Fin Surfboard'
DESCRIPTION=('One original static single-fin surfboard with a broad continuous closed board, rounded faceted rails, a curved deck and bottom, tapered rounded nose and tucked tail. '
 'The board is 2.17 m long, 0.65 m wide and up to 0.08 m thick. A separately editable solid swept-back fin has a tapered finite thickness and is seated into the bottom with real interior overlap. '
 'One fixed deck-down rest pose places finite nose and tail deck patches on the ground, with the centre deck raised and the fin pointing upward. This preserves the normal board rocker when inverted; it does not imply buoyancy. '
 'Two closed editable meshes, four constant solid PBR materials, original face-assigned cream centre line and coral nose color; no overlays, textures, stand, people, water, straps or external assets. '
 'Metres, source Z up, nose -Y and ground-centre origin. One complete surfboard counts as one prop. '
 'No flotation, wave or fluid simulation, handling, motion, human fit, carrying capacity, manufacturing, sport-safety guarantee or compatibility with skis, bindings, boats or paddles.')
G={};LINKS=[];FEET=['Board_ContinuousWideBody'];BORES=[];GAPS=[]
PALETTE=[('Body_OceanTeal',(.025,.36,.38,1),.39,0),('Stripe_WarmIvory',(.86,.80,.59,1),.43,0),('Nose_SoftCoral',(.66,.16,.085,1),.42,0),('Fin_DeepNavy',(.025,.075,.11,1),.47,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.015):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
# These stations are entirely newly authored, with no geometry imported from skis.
# Tuple = Y, half width, displayed deck underside Z, thickness.
STATIONS=[(-1.10,.026,.010,.021),(-1.075,.065,.003,.026),(-1.03,.120,0,.032),(-.96,.180,0,.040),
 (-.83,.245,.023,.050),(-.63,.290,.050,.065),(-.38,.317,.067,.075),(0,.325,.072,.080),
 (.34,.305,.060,.074),(.61,.270,.038,.064),(.80,.218,.013,.052),(.94,.155,0,.044),
 (1.03,.110,0,.038),(1.07,.068,.003,.030)]
# Fourteen perimeter points follow a rounded physical rail; there is no zero-thickness sheet.
# The lower central panel is the deck in this upside-down rest pose.
RING=[(-.65,0),(.65,0),(.88,.09),(1,.38),(.98,.62),(.88,.80),(.60,.94),(.18,1),(-.18,1),(-.60,.94),(-.88,.80),(-.98,.62),(-1,.38),(-.88,.09)]
NORMAL_DISPLAY_DATUM=.20
# Normal surfboard coordinates have deck upward, nose -Y and bottom down.
# Display = rotation Y 180 degrees, then translation Z +.20 m.
def normal_to_display(p):return (-p[0],p[1],NORMAL_DISPLAY_DATUM-p[2])
def displayed_section(y,w,z,t):
 normal=[(-a*w,y,NORMAL_DISPLAY_DATUM-z-b*t) for a,b in RING]
 return [normal_to_display(v) for v in normal]
vs=[p for station in STATIONS for p in displayed_section(*station)];fs=[];fm=[];n=len(RING)
for j in range(len(STATIONS)-1):
 for i in range(n):
  fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
  # Teal rails and deck, ivory single centre line on the visible bottom; coral near nose.
  fm.append(1 if i==7 else (2 if j in [2,3] and i in [5,6,8,9] else 0))
fs += [tuple(reversed(range(n))),tuple((len(STATIONS)-1)*n+i for i in range(n))];fm += [0,0]
fs=[tuple(reversed(f)) for f in fs]  # Outward winding in displayed world coordinates.
mesh('Board_ContinuousWideBody',vs,fs,0,'one closed continuous wide surfboard; genuine rounded rail, thick deck/bottom and two finite deck-down ground patches')
G['Board_ContinuousWideBody']['face_materials']=fm
# One solid swept fin, with a curved polygonal leading/trailing outline and tapered thickness.
# The lower edge is embedded into the actual curved board bottom rather than merely touching it.
FIN_OUTLINE=[(.38,.116),(.92,.039),(.92,.063),(.85,.108),(.79,.160),(.755,.220),(.760,.265),
 (.800,.325),(.835,.365),(.820,.382),(.790,.382),(.730,.354),(.640,.300),(.540,.227),(.460,.158)]
k=len(FIN_OUTLINE);fv=[(s*(.014-.018*z),y,z) for s in [-1,1] for y,z in FIN_OUTLINE]
ff=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
mesh('Fin_ThickSweptSingle',fv,ff,3,'single closed thick swept-back bottom fin, tapered from a broad root to finite tip; turned upward only by the rest pose')
for y,z in [(.44,.112),(.60,.091),(.80,.061)]:link('Fin_ThickSweptSingle','Board_ContinuousWideBody',(0,y,z),spread=.008)
# An actual finite empty envelope under the central deck, not an inferred AABB gap.
CLEAR_BOXES=[{'label':'central_deck_ground_clearance','lo':(-.12,-.30,.002),'hi':(.12,.25,.051)}]
for x in [-.11,0,.11]:
 for y in [-.29,0,.24]:GAPS.append({'label':'central_deck_ground_clearance','origin_m':[x,y,.002],'direction':[0,0,1],'length_m':.049})
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
def measure_rest_contacts(triangles):
 result={}
 for label,sign in [('nose',-1),('tail',1)]:
  patch=[t for t in triangles['Board_ContinuousWideBody'] if max(abs(v[2]) for v in t)<1.1e-6 and all(v[1]*sign>.90 for v in t)]
  area=sum(math.sqrt(sum(c*c for c in cross(sub(t[1],t[0]),sub(t[2],t[0]))))/2 for t in patch)
  assert area>.01,(label,'insufficient finite rest surface',area)
  result[label]={'actual_ground_triangle_area_m2':area,'actual_triangle_count':len(patch)}
 checks=[]
 for box in CLEAR_BOXES:
  blockers=[name for name,tt in triangles.items() if any(triangle_box_intersects(t,box['lo'],box['hi']) for t in tt)]
  assert not blockers,('actual central deck clearance blocked',box,blockers)
  checks.append(dict(box,actual_triangle_box_intersections=0))
 return {'finite_rest_patches':result,'whole_triangle_clear_volume_checks':checks,'no_dynamic_stability_claim':True}
def measure_surfboard_geometry(vertices):
 assert set(vertices)=={'Board_ContinuousWideBody','Fin_ThickSweptSingle'},('unexpected meshes',set(vertices))
 board=sorted(set(tuple(round(float(c),7) for c in v) for v in vertices['Board_ContinuousWideBody']));fin=sorted(set(tuple(round(float(c),7) for c in v) for v in vertices['Fin_ThickSweptSingle']));rows=[]
 for y,w,z,t in STATIONS:
  ring=[v for v in board if abs(v[1]-y)<1e-6];assert len(ring)==len(RING),('missing continuous section',y,len(ring))
  width=max(v[0] for v in ring)-min(v[0] for v in ring);low=min(v[2] for v in ring);high=max(v[2] for v in ring)
  assert abs(width-2*w)<2e-6 and abs(low-z)<2e-6 and abs(high-low-t)<2e-6,(y,width,low,high)
  rows.append({'actual_y_m':y,'actual_width_m':width,'actual_deck_rest_z_m':low,'actual_bottom_rest_z_m':high,'actual_thickness_m':high-low,'normal_bottom_z_m':NORMAL_DISPLAY_DATUM-high})
 assert len(board)==len(STATIONS)*len(RING) and len(fin)==2*len(FIN_OUTLINE)
 assert rows[7]['actual_width_m']>.64 and rows[7]['actual_thickness_m']>.079
 assert rows[2]['normal_bottom_z_m']-rows[7]['normal_bottom_z_m']>.119
 assert rows[-2]['normal_bottom_z_m']-rows[7]['normal_bottom_z_m']>.113
 for v in fin:
  assert any(abs(v[1]-y)<1e-6 and abs(v[2]-z)<1e-6 and abs(abs(v[0])-(.014-.018*z))<1e-6 for y,z in FIN_OUTLINE),('fin outline mismatch',v)
 assert min(p[2] for p in fin)>.038 and max(p[2] for p in fin)>.381
 return {'actual_board_sections':rows,'actual_full_width_length_ratio':rows[7]['actual_width_m']/(STATIONS[-1][0]-STATIONS[0][0]),'actual_central_deck_z_m':rows[7]['actual_deck_rest_z_m'],
 'actual_fin_min_z_m':min(p[2] for p in fin),'actual_fin_max_z_m':max(p[2] for p in fin),'actual_fin_tip_thickness_m':2*(.014-.018*max(p[2] for p in fin)),
 'normal_to_rest_transform':'rotation Y 180 degrees then translation Z +0.20 m; nose remains -Y','rest_pose':'deck-down, finite nose and tail deck patches; fin points upward','counted_props':1,'performance_tested':False}
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
root=bpy.data.objects.new('OneWideSingleFinSurfboard',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.02,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
surfboard_evidence=measure_surfboard_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
surfboard_evidence.update(measure_rest_contacts({o.name:[[o.matrix_world@o.data.vertices[i].co for i in t.vertices] for t in o.data.loop_triangles] for o in parts}))
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
 'single_prop_count':1,'surfboard_geometry':surfboard_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beach/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beach','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.015,.16));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.65;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,4.6),'gray-back3q':(3,5,4.6)} if gray else {
 'thumbnail':(-3,-5,4.6),'qa-front':(0,-7,.16),'qa-side':(7,0,.16),'qa-top':(0,0,8),
 'qa-back':(0,7,.16),'qa-wireframe':(-3,-5,4.6)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.65
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0023;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.16)),('silhouette-128-side',(7,0,.16))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
