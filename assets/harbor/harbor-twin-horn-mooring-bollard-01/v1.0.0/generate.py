"""Original fixed twin-horn harbor mooring bollard. One static visual prop only.
Metres, Z up, front -Y, horns along X; flat ground-centre origin.
No rope, vessel, dock, mounting substrate, textures, logos or external assets.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='harbor-twin-horn-mooring-bollard-01';VERSION='1.0.0';TITLE='Fixed Twin-Horn Mooring Bollard'
DESCRIPTION=('One original static low harbor bollard with a broad chamfered flat-bottom foot, a tapered post with a flared shoulder, and two independently editable thick upturned horns. '
 'The mirrored horns have broad embedded roots and gently rising faceted ends; complete finite open volumes beneath both horns preserve the real rope-retaining silhouette. '
 'Four seated capped fastener details are part of the prop, with no substrate or installation claim. Eight closed named editable meshes, three constant solid PBR materials, metre scale, source Z up, horns along X, front -Y and ground-centre origin. '
 'No ropes, boat, dock, new ground, text, textures or external dependencies. All components have finite support paths to the flat foot. '
 'One fixed visual pose only: no rope tying or mooring operation, pull strength, anchorage, ship matching, dock installation compatibility, load rating, corrosion resistance, manufacture or maritime/equipment safety certification.')
G={};LINKS=[];FEET=['Base_FlatChamferedFoot'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Foot_DeepSlate',(.065,.095,.105,1),.64,.28),('Casting_MutedTeal',(.095,.245,.225,1),.56,.33),('Fastener_WarmSteel',(.28,.275,.245,1),.48,.56)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.005):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def clipped_rect(rx,ry,c):
 return [(-rx+c,-ry),(rx-c,-ry),(rx,-ry+c),(rx,ry-c),(rx-c,ry),(-rx+c,ry),(-rx,ry-c),(-rx,-ry+c)]
def loft_z(name,levels,mat,role):
 vs=[(x,y,z) for z,rx,ry,c in levels for x,y in clipped_rect(rx,ry,c)];n=8
 fs=[tuple(reversed(range(n))),tuple((len(levels)-1)*n+i for i in range(n))]
 for k in range(len(levels)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return mesh(name,vs,fs,mat,role)
# A wide cast foot with a genuinely flat underside, shallow lower bevel and
# a broad upper seating plane. No mounting substrate or anchors below Z=0.
loft_z('Base_FlatChamferedFoot',[(0,.304,.214,.040),(.012,.320,.230,.046),(.053,.320,.230,.046),(.070,.302,.212,.040)],0,'closed broad chamfered foot with finite planar underside at Z=0; isolated placement datum, not dock mounting compatibility')
# The post is newly authored as a low waisted shoulder, not a reused signpost.
loft_z('Post_FlaredShoulder',[(.055,.145,.130,.030),(.090,.145,.130,.030),(.140,.112,.100,.025),(.285,.110,.098,.024),(.330,.152,.128,.032),(.375,.152,.128,.032),(.389,.139,.115,.028)],1,'solid tapered low post with flared shoulder and embedded finite base seat; both horns root into this shoulder')
link('Post_FlaredShoulder','Base_FlatChamferedFoot',(0,0,.062),axis=(1,0,0),spread=.070)
# Two separate thick eight-sided horn solids. Each cross-section is a clipped
# rectangle, not a chain of disconnected primitive cylinders. Rising end
# centres create an actual upturned lower/upper silhouette in the mesh.
HORN_SECTIONS=[(.065,.346,.078,.055,.020),(.170,.343,.077,.051,.020),(.290,.362,.069,.048,.018),(.390,.403,.061,.043,.016),(.445,.457,.050,.035,.013),(.470,.470,.036,.025,.010)]
for side,label in [(-1,'Left'),(1,'Right')]:
 vs=[(side*x,y,z+dz) for x,z,ry,rz,c in HORN_SECTIONS for y,dz in clipped_rect(ry,rz,c)];n=8
 fs=[tuple(reversed(range(n))),tuple((len(HORN_SECTIONS)-1)*n+i for i in range(n))]
 for k in range(len(HORN_SECTIONS)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 horn='Horn_'+label+'Upturned';mesh(horn,vs,fs,1,'independent closed faceted horn with thick shoulder-embedded root, rising end and genuine under-horn retention clearance')
 link(horn,'Post_FlaredShoulder',(side*.112,0,.347),spread=.027)
# Four fixed, capped head details sit into the foot. No concealed anchor rods,
# nut operation, foundation attachment or load-bearing installation is implied.
for x,xlabel in [(-.235,'Left'),(.235,'Right')]:
 for y,ylabel in [(-.143,'Front'),(.143,'Back')]:
  name='Fastener_'+ylabel+xlabel;profile=[(.057,.013),(.073,.013),(.073,.023),(.087,.023),(.092,.018)]
  vs=[(x+r*math.cos(math.tau*i/8+math.pi/8),y+r*math.sin(math.tau*i/8+math.pi/8),z) for z,r in profile for i in range(8)];fs=[tuple(reversed(range(8))),tuple(32+i for i in range(8))]
  for k in range(4):
   for i in range(8):j=(i+1)%8;fs.append((8*k+i,8*k+j,8*(k+1)+j,8*(k+1)+i))
  mesh(name,vs,fs,2,'capped fastener head and short stem seated in the prop foot; static detail only, no foundation anchoring')
  link(name,'Base_FlatChamferedFoot',(x,y,.063),axis=(1,0,0),spread=.004)
# Full closed conservative clearance volumes, separate from renderable G.
# They extend through depth, from above the capped head details to beneath the horn
# underside, and cover each continuous lateral throat. They are never exported.
for side,label in [(-1,'Left'),(1,'Right')]:
 outline=[(.170,.105),(.420,.105),(.420,.375),(.390,.345),(.290,.302),(.170,.280)]
 k=len(outline);vs=[(side*x,y,z) for y in [-.145,.145] for x,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 VOID_VOLUMES['Throat_'+label+'_FiniteClearance']={'vertices':vs,'faces':fs,'role':'complete conservative empty under-horn lateral throat from front to rear; no rope size or vessel compatibility claim'}
 for x,z in [(.185,.160),(.255,.220),(.335,.270),(.400,.325)]:
  GAPS.append({'label':label+'_continuous_underhorn_clearance','origin_m':[side*x,-.18,z],'direction':[0,1,0],'length_m':.36})
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
root=bpy.data.objects.new('OneFixedTwinHornMooringBollard',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Horn shape and geometry-only balance evidence are read from actual meshes.
horn_checks=[]
for label in ['Left','Right']:
 o=byname['Horn_'+label+'Upturned'];v=[o.matrix_world@p.co for p in o.data.vertices]
 root_vertices=[p for p in v if abs(abs(p.x)-.065)<1e-6];tip_vertices=[p for p in v if abs(abs(p.x)-.470)<1e-6]
 root_bottom=min(p.z for p in root_vertices);tip_bottom=min(p.z for p in tip_vertices)
 assert len(root_vertices)==len(tip_vertices)==8 and tip_bottom-root_bottom>.15
 horn_checks.append({'mesh':o.name,'actual_root_min_z_m':root_bottom,'actual_tip_min_z_m':tip_bottom,'actual_lower_edge_upturn_m':tip_bottom-root_bottom,'root_vertex_count':len(root_vertices),'tip_vertex_count':len(tip_vertices)})
volume_sum=0;centroid_sum=Vector((0,0,0))
for o in parts:
 for tri in o.data.loop_triangles:
  a,b,c=[o.matrix_world@o.data.vertices[i].co for i in tri.vertices];vv=a.dot(b.cross(c))/6
  volume_sum+=vv;centroid_sum+=(a+b+c)*(vv/4)
centroid=centroid_sum/volume_sum;assert abs(centroid.x)<.20 and abs(centroid.y)<.14
bollard_evidence={'independent_horn_count':2,'fixed_fastener_detail_count':4,'horn_actual_upturn':horn_checks,'finite_void_volumes':VOID_VOLUMES,'finite_volume_empty_checks':void_volume_checks,'uniform_volume_centroid_m':list(centroid),'centroid_projection_within_finite_base':True,'static_display_only':True,'mooring_operation_or_load_or_installation_claim':False}
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
 'single_prop_count':1,'bollard_working_geometry':bollard_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/harbor/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.245));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.20;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,3.5),'gray-back3q':(3,5,3.5)} if gray else {
 'thumbnail':(-3,-5,3.5),'qa-front':(0,-7,.245),'qa-side':(7,0,.245),'qa-top':(0,0,8),
 'qa-back':(0,7,.245),'qa-wireframe':(-3,-5,3.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.20
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0015;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.245)),('silhouette-128-side',(7,0,.245))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
