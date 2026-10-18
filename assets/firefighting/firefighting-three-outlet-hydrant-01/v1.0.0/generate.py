"""Original three-outlet closed-cap hydrant static visual prop.
Metres, Z up, front -Y. All outlet necks, caps and nuts are fixed closed solids.
No unseen pipe, water flow, pressure, operation or safety performance claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='firefighting-three-outlet-hydrant-01';VERSION='1.0.0';TITLE='Three-Outlet Closed-Cap Fire Hydrant'
DESCRIPTION=('Original standalone three-outlet fire-hydrant static exterior visual. A broad chamfered base flange supports a stout stepped upright body, faceted domed bonnet and fixed pentagonal top nut. Two opposing smaller side outlet necks and one larger lower front neck each carry a separate thick shouldered closed cap with a fixed polygonal boss. Four small fixed base fastener heads are seated in the flange. '
 'Seventeen editable closed meshes have finite actual overlap seats and a connected support path to the flat base flange. Three constant fully opaque solid PBR materials. One original prop, metre scale, Z up, front -Y, base-centre origin. No textures, logos, chain, hose, pipe network, ground, scene, people, animation or reused geometry. '
 'Every outlet stays capped. The necks and body are solid visual volumes; no hidden hollow interior or continuous working water passage is modeled or claimed. Static stylized exterior only: no water flow, pressure, fire suppression, operation, installation, pipe or hose compatibility, structural load, manufacturing, fire-code or safety certification. Not real firefighting equipment design or use guidance.')
G={};LINKS=[];FEET=['Base_FlangedFoot'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Body_OxideRed',(.57,.075,.045,1),.64,.10),('Caps_DeepGraphite',(.085,.12,.135,1),.55,.35),('Fasteners_SatinSteel',(.42,.49,.49,1),.43,.72)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'closed_caps':True,'unseen_inner_flow_path_modeled_or_claimed':False}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def void(name,lo,hi,role):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def profile(name,origin,axis,u,v,rings,material,role,sides=24,phase=0):
 # Closed radial solid profile. No fake bore or implied hidden working passage.
 vs=[add(add(add(origin,mul(axis,t)),mul(u,r*math.cos(phase+2*math.pi*j/sides))),mul(v,r*math.sin(phase+2*math.pi*j/sides))) for t,r in rings for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+j for j in range(sides))]
 for i in range(len(rings)-1):
  for j in range(sides):
   k=(j+1)%sides;fs.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
 return mesh(name,vs,fs,material,role)
zaxis=(0,0,1);ux=(1,0,0);uy=(0,1,0)
profile('Base_FlangedFoot',(0,0,0),zaxis,ux,uy,[(0,.30),(.015,.33),(.075,.33),(.09,.31)],0,'broad chamfered closed foot flange with finite planar ground patch; no anchored installation claim')
profile('Body_StoutColumn',(0,0,0),zaxis,ux,uy,[(.070,.235),(.14,.235),(.17,.22),(.81,.22),(.85,.245),(.885,.245)],0,'thick stepped upright visual body solid; no modeled hidden bore')
link('Body_StoutColumn','Base_FlangedFoot',(0,0,.08),axis=(1,0,0),spread=.05)
profile('Bonnet_FacetedDome',(0,0,0),zaxis,ux,uy,[(.875,.265),(.905,.265),(.96,.24),(1.02,.19),(1.065,.115),(1.085,.065)],0,'faceted domed top cap with finite overlap seat on body')
link('Bonnet_FacetedDome','Body_StoutColumn',(0,0,.880),axis=(1,0,0),spread=.08)
profile('Bonnet_FixedPentagonalNut',(0,0,0),zaxis,ux,uy,[(1.072,.049),(1.136,.049),(1.145,.041)],2,'fixed closed five-sided top nut seated into bonnet; no operation',sides=5,phase=math.pi/2)
link('Bonnet_FixedPentagonalNut','Bonnet_FacetedDome',(0,0,1.078),axis=(1,0,0),spread=.012)
for j in range(4):
 a=math.pi/4+j*math.pi/2;x=.28*math.cos(a);y=.28*math.sin(a);name='Base_FixedBolt_'+str(j+1)
 profile(name,(x,y,0),zaxis,ux,uy,[(.068,.026),(.108,.026),(.115,.021)],2,'small fixed hexagonal fastener head embedded in flange, clear of stout body',sides=6,phase=a)
 link(name,'Base_FlangedFoot',(x,y,.080),axis=(1,0,0),spread=.006)
OUTLETS=[]
for label,axis,u,v,z in [('Left',(-1,0,0),(0,-1,0),(0,0,1),.72),('Right',(1,0,0),(0,1,0),(0,0,1),.72),('Front',(0,-1,0),(1,0,0),(0,0,1),.50)]:
 front=label=='Front';origin=(0,0,z)
 neck_rings=[(.16,.13),(.27,.145),(.36,.145),(.385,.155)] if front else [(.165,.09),(.24,.105),(.33,.105),(.35,.115),(.375,.115)]
 cap_rings=[(.37,.17),(.39,.185),(.44,.185),(.465,.155)] if front else [(.36,.125),(.382,.14),(.42,.14),(.445,.12)]
 boss_rings=[(.452,.055),(.505,.055),(.515,.047)] if front else [(.435,.043),(.479,.043),(.488,.037)]
 neck='Outlet_'+label+'_Neck';cap='Outlet_'+label+'_ClosedCap';boss='Outlet_'+label+'_FixedBoss'
 profile(neck,origin,axis,u,v,neck_rings,0,'solid exterior neck of the '+label.lower()+' closed outlet, rooted in actual body volume; no inner passage claim')
 profile(cap,origin,axis,u,v,cap_rings,1,'separate thick shouldered solid closed cap on '+label.lower()+' neck; fixed closed state')
 profile(boss,origin,axis,u,v,boss_rings,2,'fixed polygonal boss seated in closed cap; no handle movement or uncapping',sides=6,phase=math.pi/6)
 link(neck,'Body_StoutColumn',add(origin,mul(axis,.19)),axis=u,spread=.025)
 link(cap,neck,add(origin,mul(axis,.378 if front else .367)),axis=u,spread=.025)
 link(boss,cap,add(origin,mul(axis,.458 if front else .440)),axis=u,spread=.010)
 WALL_PROBES.append({'mesh':cap,'origin_m':list(add(origin,mul(axis,.25))),'direction':list(axis),'length_m':.35,'minimum_wall_thickness_m':.09 if front else .08})
 OUTLETS.append({'label':label,'axis':axis,'height_m':z,'neck_mesh':neck,'closed_cap_mesh':cap,'fixed_boss_mesh':boss,'neck_outer_radius_m':.155 if front else .115,'cap_outer_radius_m':.185 if front else .14,'cap_solid_axial_depth_m':.095 if front else .085,'fixed_closed':True})
# Finite conservative external air spaces only, never hidden functional pipe probes.
for side,sgn in [('Left',-1),('Right',1)]:
 lo,hi=sorted([sgn*.26,sgn*.33]);void('Clearance_'+side+'_FrontToSide',(lo,-.32,.60),(hi,-.16,.80),'real external clearance between front cap and side outlet; no bore claim')
 void('Clearance_'+side+'_BelowSideCap',tuple(min(a,b) for a,b in zip((sgn*.36,-.10,.18),(sgn*.44,.10,.56))),tuple(max(a,b) for a,b in zip((sgn*.36,-.10,.18),(sgn*.44,.10,.56))),'open external space beneath side closed cap and above ground')
 GAPS.append({'label':side+'_side_to_front_external_gap','origin_m':[sgn*.29,-.33,.70],'direction':[0,1,0],'length_m':.16})
HYDRANT_CONTRACT={'outlets':OUTLETS,'single_prop_count':1,'base_bolts':4,'fixed_top_nut':True,'closed_cap_count':3,'front_outlet_larger_than_side_outlets':True,'water_flow_pressure_firefighting_safety_claim':False,'inner_flow_path_modeled_or_claimed':False}
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
root=bpy.data.objects.new('OneThreeOutletClosedHydrant',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
hydrant_evidence=dict(HYDRANT_CONTRACT,finite_external_air_volume_checks=void_volume_checks,actual_solid_cap_depth_checks=wall_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'hydrant_closed_exterior_geometry':hydrant_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/firefighting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'firefighting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.08,.58));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.63;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-2.4,-3.8,2.55),'gray-back3q':(2.4,3.8,2.55)} if gray else {
 'thumbnail':(-2.4,-3.8,2.55),'qa-front':(0,-4,.58),'qa-side':(4,-.08,.58),'qa-top':(0,0,4),
 'qa-back':(0,4,.58),'qa-wireframe':(-2.4,-3.8,2.55)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.63
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0025;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.58)),('silhouette-128-side',(4,-.08,.58))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
