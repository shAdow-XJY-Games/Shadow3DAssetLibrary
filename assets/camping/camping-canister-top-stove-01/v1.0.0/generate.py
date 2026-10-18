"""Original fixed single-burner canister-top camping stove visual prop.
Metres, Z up, front -Y; ground-centre origin. One static unlit pose.
No fuel contents, gas, pressure, heat, ignition, cookware, textures or operation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='camping-canister-top-stove-01';VERSION='1.0.0';TITLE='Single-Burner Canister-Top Camping Stove'
DESCRIPTION=('Original single unlit canister-top camping stove visual prop: a low faceted canister exterior with broad flat bottom, a separate narrowed neck and collar, a genuinely open thick concave burner cup, and three separately editable bent radial support arms. '
 'The arms share three finite coplanar raised support surfaces; their embedded roots have complete static geometric support routes through the collar to the canister bottom. A short front control stem seats an independent faceted knob. '
 'The cup has a real inner floor and walls, with an unobstructed finite mouth volume and actual gaps to the raised arms. Eight closed named editable meshes, four constant solid PBR materials, metre scale, source Z up, front -Y and ground-centre origin. '
 'One original reusable prop, no flame, cookware, fuel contents, hose, texture, text, logo or external dependencies. Source design is independent of the old campfire, lantern and kitchen two-burner stove. '
 'Static stylized visual only: no gas, pressure-vessel structure, ignition, combustion, heat, folding, cooking, cookware fit, carrying load, real operation, manufacture or outdoor/gas safety or performance guarantee.')
G={};LINKS=[];FEET=['Canister_FlatBottom'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Canister_MutedSage',(.20,.33,.27,1),.70,.05),('Neck_DarkSlate',(.055,.075,.080,1),.58,.35),('Burner_WarmSteel',(.36,.35,.31,1),.50,.62),('Control_Clay',(.38,.16,.09,1),.72,.02)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def ring_geometry(profile,n=24):
 vs=[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for z,r in profile for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 for k in range(len(profile)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return vs,fs
def lathe(name,profile,mat,role,n=24):
 vs,fs=ring_geometry(profile,n);return mesh(name,vs,fs,mat,role)
# The canister is a closed exterior visual solid, not a vessel-wall design.
# Its broad lower disk supplies finite ground contact, without a pointed base.
lathe('Canister_FlatBottom',[(0,.046),(.004,.052),(.011,.055),(.061,.055),(.072,.051),(.081,.035),(.084,.016)],0,'original squat canister exterior with real flat circular bottom; closed visual solid, no fuel or pressure-vessel structure')
lathe('Neck_SeatedCollar',[(.080,.014),(.087,.014),(.087,.019),(.104,.019),(.108,.012),(.119,.012)],1,'independent neck seated within canister shoulder; broad collar embeds all three arm roots and narrows into burner underside')
link('Neck_SeatedCollar','Canister_FlatBottom',(0,0,.082),axis=(1,0,0),spread=.005)
# One continuous closed thick cup. Its profile crosses the lip then descends
# the inner wall to a raised inner floor; the top is a real open aperture.
CUP_PROFILE=[(.114,.020),(.119,.026),(.136,.035),(.142,.035),(.142,.029),(.137,.029),(.125,.021),(.121,.020)]
lathe('Burner_TrueConcaveCup',CUP_PROFILE,2,'continuous thick open burner cup with outer bottom, finite inner floor and actual inner/outer walls; no gas holes or combustion simulation')
link('Burner_TrueConcaveCup','Neck_SeatedCollar',(0,0,.116),axis=(1,0,0),spread=.005)
# Three independent solid radial bent arms. The concave side profile is
# extruded through a finite tangent width, leaving a real gap around the cup.
ARM_PROFILE=[(.008,.095),(.025,.095),(.052,.114),(.052,.149),(.084,.149),(.084,.157),(.044,.157),(.044,.119),(.008,.103)]
ARM_ANGLES=[90,210,330]
for i,degrees in enumerate(ARM_ANGLES,1):
 a=math.radians(degrees);rad=(math.cos(a),math.sin(a),0);tan=(-math.sin(a),math.cos(a),0)
 vs=[(r*rad[0]+t*tan[0],r*rad[1]+t*tan[1],z) for t in [-.005,.005] for r,z in ARM_PROFILE];n=len(ARM_PROFILE)
 fs=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 name=f'Arm_{i}_RaisedSupport';mesh(name,vs,fs,2,'one fixed bent radial support arm; embedded collar root, open cup-side clearance and finite horizontal top surface at Z=0.157 m')
 link(name,'Neck_SeatedCollar',(.013*rad[0],.013*rad[1],.099),axis=tan,spread=.002)
# Front-facing control is static geometry only; the stem and knob are separate.
vs,fs=ring_geometry([(-.014,.003),(-.037,.003)],12)
vs=[(x,ypos,.093+y) for x,y,ypos in vs]
mesh('Control_EmbeddedStem',vs,fs,1,'short closed front control stem embedded into the neck and knob; no operative valve or gas path')
link('Control_EmbeddedStem','Neck_SeatedCollar',(0,-.017,.093),axis=(1,0,0),spread=.001)
vs,fs=ring_geometry([(-.033,.007),(-.036,.010),(-.043,.010),(-.046,.007)],12)
vs=[(x,ypos,.093+y) for x,y,ypos in vs]
mesh('Control_FacetedKnob',vs,fs,3,'separate closed faceted control knob physically seated around the stem, fixed pose only')
link('Control_FacetedKnob','Control_EmbeddedStem',(0,-.035,.093),axis=(1,0,0),spread=.001)
# A complete conservative finite open chamber extends from just above the real
# floor through the cup mouth and beyond the arm bearing plane. No probe exports.
vs,fs=ring_geometry([(.1225,.018),(.135,.026),(.165,.026)],24)
VOID_VOLUMES['Burner_OpenChamber']={'vertices':vs,'faces':fs,'role':'finite empty chamber and open upward mouth, not a few sparse opening rays'}
for x,y in [(0,0),(.012,0),(-.012,0),(0,.012),(0,-.012)]:
 GAPS.append({'label':'cup_upward_open_mouth','origin_m':[x,y,.1225],'direction':[0,0,1],'length_m':.045})
for i,degrees in enumerate(ARM_ANGLES,1):
 a=math.radians(degrees);r=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0)
 # A finite eight-millimetre tangential gap next to each standing arm.
 def xy(rad,tan,z):return [rad*r[0]+tan*t[0],rad*r[1]+tan*t[1],z]
 vs=[xy(rad,tan,z) for z in [.129,.144] for tan in [-.004,.004] for rad in [.0365,.0425]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 VOID_VOLUMES[f'Arm_{i}_CupSideGap']={'vertices':vs,'faces':fs,'role':'complete finite geometric clearance from cup exterior to raised support arm; no thermal or safe-operation claim'}
 FLOOR_PROBES.append({'mesh':'Burner_TrueConcaveCup','origin_m':[.006*r[0],.006*r[1],.130],'direction':[0,0,-1],'length_m':.020,'expected_hit_z_m':.121})
 WALL_PROBES.append({'mesh':'Burner_TrueConcaveCup','origin_m':[0,0,.139],'direction':[r[0],r[1],0],'length_m':.040,'minimum_wall_thickness_m':.0045})
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
root=bpy.data.objects.new('OneUnlitCanisterTopStove',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual horizontal bearing patches, inner-floor depth and wall thickness.
arm_patches=[]
for i in range(1,4):
 name=f'Arm_{i}_RaisedSupport';patch=horizontal_triangles(name,.157,1);area=sum(t['area_m2'] for t in patch)
 assert area>.00035,(name,area)
 arm_patches.append({'mesh':name,'plane_z_m':.157,'actual_bearing_area_m2':area,'triangles':patch})
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
stove_evidence={'single_burner_cup_count':1,'radial_support_arm_count':3,'arm_bearing_patches':arm_patches,'finite_void_volumes':VOID_VOLUMES,'finite_volume_empty_checks':void_volume_checks,'actual_inner_floor_checks':floor_checks,'actual_wall_thickness_checks':wall_checks,'static_unlit_visual_only':True,'gas_pressure_ignition_cooking_load_safety_claim':False}
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
 'single_prop_count':1,'stove_working_geometry':stove_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/camping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'camping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.0785));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.225;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-.30,-.50,.35),'gray-back3q':(.30,.50,.35)} if gray else {
 'thumbnail':(-.30,-.50,.35),'qa-front':(0,-.7,.0785),'qa-side':(.7,0,.0785),'qa-top':(0,0,.8),
 'qa-back':(0,.7,.0785),'qa-wireframe':(-.30,-.50,.35)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.225
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00028;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-.7,.0785)),('silhouette-128-side',(.7,0,.0785))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
