"""Original shallow honeycomb frame: one editable static wooden-frame prop.
Metres, Z up, ground-centre origin; wax-cell openings face +Z in a stable flat pose.
Real shared-wall hexagonal cavities, finite floors, continuous backed support.
Self-contained source. Fresh actual GLB renders with complete geometry/PBR guard.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-recessed-comb-frame-01';VERSION='1.0.0';TITLE='Recessed Honeycomb Wooden Frame'
DESCRIPTION=('One original static honeycomb-frame prop lying flat on finite timber-bar undersides. '
 'A long top bar has two short raised-underside hanging ears; two independently editable side rails and a lower bar capture a solid wax foundation. '
 'A single connected wax mesh contains 136 actual shallow hexagonal recesses in a 17 by 8 staggered field. Shared cell walls have finite thickness, each cavity has a real floor, and the integrated base overlaps the supported foundation. '
 'Four small seated timber pegs mark the rail joints. Ten named closed editable meshes and three solid PBR materials without textures, bees, honey fluid or external models. '
 'Metres, native Z up, ground-centre origin, cell openings +Z, long top bar toward +Y. Stylized cell spacing intentionally limits geometry cost. '
 'One standalone game/display prop, without hive or extractor insertion compatibility, species-specific cell dimensions, honey production, bee behaviour, fluid, animation, manufacture or beekeeping-safety guarantees.')
G={};LINKS=[];FEET=['Frame_TopBarWithEars','Frame_BottomBar'];BORES=[];GAPS=[];CELLS=[]
PALETTE=[('Timber_WarmMaple',(.49,.235,.075,1),.69,0),('Timber_DarkEndgrain',(.22,.085,.024,1),.78,0),('Wax_WarmGolden',(.80,.48,.105,1),.57,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def poly_y(name,outline,y0,y1,mat,role):
 k=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def box(name,c,size,mat,role):
 a,b,d=[x/2 for x in size];vs=[add(c,(sx*a,sy*b,sz*d)) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def pin(name,c,z0,z1,r,mat):
 n=16;vs=[(c[0]+r*math.cos(math.tau*i/n),c[1]+r*math.sin(math.tau*i/n),z) for z in [z0,z1] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,'small seated timber joint peg; actual volume in its supporting rail')
# The top bar includes short integral overhanging ears with raised undersides.
poly_y('Frame_TopBarWithEars',[(-.240,.014),(-.220,.014),(-.220,0),(.220,0),(.220,.014),(.240,.014),(.240,.028),(.238,.030),(-.238,.030),(-.240,.028)],.110,.138,0,'top bar with finite central underside, two short raised-underside hanging ears')
poly_y('Frame_BottomBar',[(-.220,0),(.220,0),(.220,.024),(.218,.026),(-.218,.026),(-.220,.024)],-.136,-.110,0,'lower timber bar with a broad finite underside at ground datum Z=0')
for s,label in [(-1,'Left'),(1,'Right')]:
 x=s*.208
 box('Frame_SideRail_'+label,(x,0,.01425),(.022,.236,.0265),0,'separate timber side strip with finite embedded joints to upper and lower bars')
 link('Frame_SideRail_'+label,'Frame_TopBarWithEars',(x,.114,.019),axis=(1,0,0),spread=.005)
 link('Frame_SideRail_'+label,'Frame_BottomBar',(x,-.114,.018),axis=(1,0,0),spread=.005)
# Foundation has genuine thickness and enters all four wooden rails.
box('Wax_CapturedFoundation',(0,0,.00975),(.412,.234,.0065),2,'solid wax foundation from Z=.0065 to .013, embedded into all four timber rails')
for s,label in [(-1,'Left'),(1,'Right')]:link('Wax_CapturedFoundation','Frame_SideRail_'+label,(s*.201,0,.010),axis=(0,1,0),spread=.070)
link('Wax_CapturedFoundation','Frame_TopBarWithEars',(0,.1135,.010),spread=.090)
link('Wax_CapturedFoundation','Frame_BottomBar',(0,-.1135,.010),spread=.090)
# Directly author the union of a 17 x 8 hex tile field: shared boundaries have
# no duplicate walls. Each cell has an annular rim, six inward walls and a floor.
# Only perimeter tile edges receive outside walls; shared vertices are welded.
R=.015;RI=.0130;H=math.sqrt(3)*R;Z_BASE=.0115;Z_FLOOR=.0155;Z_RIM=.0270
vs=[];fs=[];lookup={};edges=collections.defaultdict(list)
def vertex(p):
 key=tuple(round(float(c),7) for c in p)
 if key not in lookup:lookup[key]=len(vs);vs.append(key)
 return lookup[key]
for col in range(17):
 for row in range(8):
  cx=(col-8)*1.5*R;cy=(row-3.5)*H+(col%2-.5)*H/2
  outer=[(cx+R*math.cos(math.tau*i/6),cy+R*math.sin(math.tau*i/6)) for i in range(6)]
  inner=[(cx+RI*math.cos(math.tau*i/6),cy+RI*math.sin(math.tau*i/6)) for i in range(6)]
  ot=[vertex((x,y,Z_RIM)) for x,y in outer];ob=[vertex((x,y,Z_BASE)) for x,y in outer]
  it=[vertex((x,y,Z_RIM)) for x,y in inner];ib=[vertex((x,y,Z_FLOOR)) for x,y in inner]
  for i in range(6):
   j=(i+1)%6;fs.append((ot[i],ot[j],it[j],it[i]));fs.append((it[i],it[j],ib[j],ib[i]));edges[tuple(sorted([ot[i],ot[j]]))].append((ot[i],ot[j],ob[i],ob[j]))
  fs.append(tuple(ib));fs.append(tuple(reversed(ob)))
  CELLS.append({'column':col,'row':row,'centre_m':[round(cx,7),round(cy,7)],'inner_circumradius_m':RI,'floor_z_m':Z_FLOOR,'rim_z_m':Z_RIM,'recess_depth_m':round(Z_RIM-Z_FLOOR,7),'base_bottom_z_m':Z_BASE})
for key,items in edges.items():
 assert len(items) in [1,2]
 if len(items)==1:
  a,b,c,d=items[0];fs.append((a,c,d,b))
mesh('Wax_SharedWallRecessField',vs,fs,2,'one welded closed wax field with 136 true open-topped hexagonal blind cavities, solid floors and shared walls')
# Three widely separated physical base/foundation witnesses. These lie below floors.
link('Wax_SharedWallRecessField','Wax_CapturedFoundation',(0,-H/4,.0122),spread=.090)
# Real dark timber pins are embedded into bars, with heights different from rail tops.
for y,z1,label,bar in [(.1244,.0315,'Top','Frame_TopBarWithEars'),(-.1244,.0275,'Bottom','Frame_BottomBar')]:
 for s,side in [(-1,'Left'),(1,'Right')]:
  name='JointPeg_'+label+'_'+side;pin(name,(s*.208,y),z1-.006,z1,.0042,1)
  link(name,bar,(s*.208,y,z1-.003),axis=(1,0,0),spread=.0012)
# Cell tests distinguish a shallow blind cavity from a fake dark top or through hole.
# All 136 cell centres must have an unobstructed mouth corridor and hit a real floor.
for cell in CELLS:
 x,y=cell['centre_m'];GAPS.append({'label':'cell_mouth_%02d_%02d'%(cell['column'],cell['row']),'origin_m':[x,y,.035],'direction':[0,0,-1],'length_m':.0185})
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
root=bpy.data.objects.new('OneRecessedHoneycombFrame',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual floor and wall intersections measured on the generated closed field.
cell_evidence=[];field=trees['Wax_SharedWallRecessField']
for cell in CELLS:
 x,y=cell['centre_m'];p=Vector((x,y,.035));q,n,_,distance=field.ray_cast(p,Vector((0,0,-1)),.05)
 assert q is not None and abs(q.z-cell['floor_z_m'])<1.1e-6 and n.z>.99,('Missing actual cell floor',cell,q,n)
 walls=[]
 for i in range(6):
  a=math.tau*(i+.5)/6;d=Vector((math.cos(a),math.sin(a),0));q,normal,_,distance=field.ray_cast(Vector((x,y,.021)),d,.030)
  expected=RI*math.cos(math.pi/6)
  assert q is not None and abs(distance-expected)<1.2e-6,('Missing real cell wall',cell,i,q,distance)
  # Shared wall thickness spans two half-walls: outer tile apothem minus inner.
  walls.append({'side':i,'actual_inner_wall_distance_m':distance,'expected_inner_apothem_m':expected})
 cell_evidence.append(dict(cell,actual_floor_hit_z_m=float(cell['floor_z_m']),actual_floor_normal_up=True,wall_hits=walls))
comb_evidence={'cell_count':len(CELLS),'columns':17,'rows':8,'cell_openings_direction':'+Z','minimum_recess_depth_m':Z_RIM-Z_FLOOR,'integrated_floor_thickness_m':Z_FLOOR-Z_BASE,'shared_wall_thickness_m':2*(R-RI)*math.cos(math.pi/6),'all_actual_cell_checks':cell_evidence,'external_hive_or_extractor_fit_claim':False}
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
 'single_prop_count':1,'honeycomb_working_geometry':comb_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.014));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.565;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(2.8,-4.2,5.4),'gray-back3q':(-2.8,4.2,5.4)} if gray else {
 'thumbnail':(2.8,-4.2,5.4),'qa-front':(0,-7,.014),'qa-side':(7,0,.014),'qa-top':(0,0,8),
 'qa-back':(0,7,.014),'qa-wireframe':(2.8,-4.2,5.4)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.565
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00012;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.014)),('silhouette-128-side',(7,0,.014))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
