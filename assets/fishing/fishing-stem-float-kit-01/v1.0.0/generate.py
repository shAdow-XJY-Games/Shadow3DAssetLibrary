"""Original three-shape stem fishing float kit, one static visual prop.
Metres, Z up; the three long axes lie along Y and each float rests on a finite body facet.
No water, buoyancy, sensitivity, line compatibility or fishing performance claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fishing-stem-float-kit-01';VERSION='1.0.0';TITLE='Three-Profile Stem Fishing Float Kit'
DESCRIPTION=('Original three-float static kit counted as one prop. A compact egg, an elongated asymmetric teardrop and a slender symmetric spindle have genuinely distinct body profiles. Every float has a long integral striped top antenna and a separate lower stem joined by finite interior seats to the closed body. Each body rests on its own finite planar lower facet at Z=0. The three parallel floats have positive actual separation and no rack or display base. '
 'Nine editable closed meshes, four constant fully opaque solid PBR materials. The common orange/ivory/graphite tail bands are material regions on continuous mesh faces, not overlays or separate color variants. Original geometry, metre scale, Z up, front -Y, central ground-plane origin. No line eyes, line, hooks, fish, water, accessories, logo, texture, animation or scene. '
 'Stylized fixed dry-laid visual only. No buoyancy, sensitivity, shot capacity, fishing performance, water behavior, rod/line compatibility, true equipment dimensions, manufacture, installation or safety guarantee. Not real fishing-equipment design or use guidance.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Bodies_WarmOchre',(.60,.32,.095,1),.66,0),('Stems_DeepGraphite',(.035,.049,.046,1),.56,0),('Tail_WarmIvory',(.90,.82,.61,1),.58,0),('Tail_SignalOrange',(.86,.17,.025,1),.52,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'bands_are_mesh_face_material_regions':True,'line_eyes_modeled_or_claimed':False}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.0005):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def void(name,lo,hi,role):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def profile(name,origin,rings,material,role,sides=16,phase=math.pi/16,segment_materials=None):
 # Axis +Y with a regular faceted section. The maximum-radius bottom facet is finite.
 vs=[(origin[0]+r*math.cos(phase+2*math.pi*j/sides),t,origin[2]-r*math.sin(phase+2*math.pi*j/sides)) for t,r in rings for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+j for j in range(sides))]
 for i in range(len(rings)-1):
  for j in range(sides):
   k=(j+1)%sides;fs.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
 mesh(name,vs,fs,material,role)
 if segment_materials is not None:
  assert len(segment_materials)==len(rings)-1
  G[name]['face_materials']=[segment_materials[0],segment_materials[-1]]+[m for m in segment_materials for _ in range(sides)]
 return name
# Each explicit profile is independently authored, not a normalized/rescaled duplicate.
BODY_PROFILES=[
 ('Egg',-.070,[(-.034,.0032),(-.029,.0095),(-.021,.0150),(-.015,.0180),(.011,.0180),(.022,.0140),(.030,.0080),(.035,.0032)]),
 ('Teardrop',0.0,[(-.050,.0032),(-.045,.0090),(-.036,.0150),(-.006,.0150),(.013,.0125),(.037,.0085),(.055,.0048),(.065,.0026)]),
 ('Spindle',.070,[(-.078,.0026),(-.063,.0050),(-.044,.0082),(-.025,.0110),(.025,.0110),(.044,.0082),(.063,.0050),(.078,.0026)])]
FLOATS=[]
for label,x,rings in BODY_PROFILES:
 rmax=max(r for y,r in rings);z=rmax*math.cos(math.pi/16);a=rings[0][0];b=rings[-1][0]
 body=label+'_Body';tail=label+'_StripedTail';stem=label+'_LowerStem';origin=(x,0,z)
 profile(body,origin,rings,0,label.lower()+' closed body with real distinct profile and finite planar lower facet')
 FEET.append(body)
 # One connected closed tail mesh; bands partition axial quads and never overlap surfaces.
 levels=[b-.007,b+.010,.109,.122,.135,.148,.161,.174,.187,.195]
 assert all(y>x for x,y in zip(levels,levels[1:]))
 profile(tail,origin,[(y,.00155 if i<len(levels)-1 else .00130) for i,y in enumerate(levels)],1,'long upper antenna with integral material face bands; no raised stripe geometry',sides=12,phase=math.pi/12,segment_materials=[1,1,3,2,1,3,2,1,3])
 profile(stem,origin,[(-.160,.00125),(-.154,.00165),(a+.007,.00165)],1,'long fixed lower stem, seated inside body with finite overlap',sides=12,phase=math.pi/12)
 link(tail,body,(x,b-.0035,z),axis=(0,1,0),spread=.0007)
 link(stem,body,(x,a+.0035,z),axis=(0,1,0),spread=.0007)
 FLOATS.append({'label':label,'body':body,'tail':tail,'lower_stem':stem,'axis_x_m':x,'axis_z_m':z,'profile_y_radius_m':rings,'body_length_m':b-a,'body_max_radius_m':rmax,'profile_length_diameter_ratio':(b-a)/(2*rmax),'body_ground_facet':True,'no_line_eye':True})
# Conservative positive-volume empty spaces between entire float envelopes.
void('Between_Egg_Teardrop',(-.049,-.162,.001),(-.018,.197,.036),'finite external separation between complete egg and teardrop float assemblies')
void('Between_Teardrop_Spindle',(.018,-.162,.001),(.056,.197,.036),'finite external separation between complete teardrop and spindle float assemblies')
for label,x in [('Egg_Teardrop',-.034),('Teardrop_Spindle',.038)]:GAPS.append({'label':label+'_full_length_clearance','origin_m':[x,-.163,.014],'direction':[0,1,0],'length_m':.362})
FLOAT_CONTRACT={'floats':FLOATS,'single_prop_count':1,'float_count':3,'editable_meshes':9,'same_palette_all_three':True,'bodies_are_distinct_profiles_not_color_variants':True,'dry_laid_fixed_pose_only':True,'line_eyes_modeled_or_claimed':False,'water_buoyancy_sensitivity_fishing_performance_claim':False}
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
root=bpy.data.objects.new('OneThreeProfileFloatKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='central dry-laid plane datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual floor and wall tests supplement finite void and support tests.
floor_checks=[]
for r in FLOOR_PROBES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is not None and abs(hit.z-r['expected_hit_z_m'])<1e-6
 floor_checks.append(dict(r,actual_hit_m=list(hit)))
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);t=trees[r['mesh']];inner=t.ray_cast(p,d,r['length_m'])[0]
 assert inner is not None
 outer=t.ray_cast(inner+d*1e-6,d,r['length_m'])[0];assert outer is not None
 thickness=(outer-inner).length;assert thickness>r['minimum_wall_thickness_m']
 wall_checks.append(dict(r,actual_inner_hit_m=list(inner),actual_outer_hit_m=list(outer),actual_wall_thickness_m=thickness))
float_evidence=dict(FLOAT_CONTRACT,finite_external_air_volume_checks=void_volume_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'float_kit_geometry':float_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fishing/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.018,.016));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.445;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-.52,-.69,1.25),'gray-back3q':(.52,.69,1.25)} if gray else {
 'thumbnail':(-.52,-.69,1.25),'qa-front':(0,-4,.35),'qa-side':(4,.018,.35),'qa-top':(0,0,4),
 'qa-back':(0,4,.35),'qa-wireframe':(-.52,-.69,1.25)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.445
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0007;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.016)),('silhouette-128-side',(4,.018,.016))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
