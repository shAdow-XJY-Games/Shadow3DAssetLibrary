"""Original fixed rope-stanchion barrier. Entire assembly is one static visual prop.
Metres; source Z up; front -Y; two true finite ground faces. No simulations.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='museum-rope-stanchion-barrier-kit-01';VERSION='1.0.0';TITLE='Fixed Rope Stanchion Barrier'
DESCRIPTION=('One original static stylized rope barrier with two broad finite circular-foot stanchions, integral narrow shafts and faceted heads, two fixed solid mounting studs, two solid rope-end ferrules and one continuous thick sagging rope. '
 'The complete assembly is one prop and seven closed editable meshes. The rope joins both ferrules, both studs join the heads, and the bases have true planar finite ground contact. The open space below the rope remains clear. '
 'Four constant solid PBR materials, metre scale, source Z up, front -Y and ground-centre origin. Generic exhibition and queue appearance suitable for reuse without duplicating themed recolours; no claim of specific modular or corner compatibility. '
 'Static visual geometry only: no rope physics, tension, motion, crowd control, barrier effectiveness, load capacity, stability, anti-tip, installation, accessibility, escape-route, manufacturing, real product dimensional compliance or public safety certification. No display plinths, people, floor or accessory set.')
G={};LINKS=[];FEET=['Stanchion_Left','Stanchion_Right'];BORES=[];GAPS=[];VOID_VOLUMES={};VOID_CENTRES={};WALL_PROBES=[]
PALETTE=[('Bronze_Satin',(.41,.275,.115,1),.34,.70),('Rope_DeepBurgundy',(.235,.025,.044,1),.79,0),('Ferrule_WarmGold',(.58,.38,.135,1),.30,.73),('Base_DarkFoot',(.035,.042,.043,1),.65,.12)]
N=12;R=.026

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name

def link(a,b,p,axis=(0,1,0),spread=.004):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size
 vs=[(x+a*w/2,y+b*d/2,z+c*h/2) for c in [-1,1] for b in [-1,1] for a in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def empty_box(name,c,size,role):
 temp='PROBE_'+name;box(temp,c,size,0,role);VOID_VOLUMES[name]=G.pop(temp);VOID_CENTRES[name]=c

def rod(name,a,b,r,mat,role,n=12):
 delta=[b[i]-a[i] for i in range(3)];L=math.sqrt(sum(t*t for t in delta));w=[t/L for t in delta];tmp=[0,0,1]
 u=[w[1]*tmp[2]-w[2]*tmp[1],w[2]*tmp[0]-w[0]*tmp[2],w[0]*tmp[1]-w[1]*tmp[0]];l=math.sqrt(sum(t*t for t in u));u=[t/l for t in u]
 v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[j]+r*(u[j]*math.cos(math.tau*i/n)+v[j]*math.sin(math.tau*i/n)) for j in range(3)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
# Each stanchion is a closed lathed body. Its polygonal bottom cap has finite
# area, rather than a tangent sphere, hidden plane or sharp point contact.
POST_PROFILE=[(0,.215),(.025,.215),(.058,.195),(.090,.112),(.118,.073),(.150,.047),(.830,.039),(.855,.050),(.875,.067),(.945,.067),(.970,.055),(.990,.030),(1.000,.016)]
def stanchion(name,x,n=20):
 vs=[(x+r*math.cos(math.tau*j/n),r*math.sin(math.tau*j/n),z) for z,r in POST_PROFILE for j in range(n)]
 fs=[tuple(reversed(range(n)))];fm=[3]
 for i in range(len(POST_PROFILE)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));fm.append(3 if i==0 else 0)
 fs.append(tuple((len(POST_PROFILE)-1)*n+j for j in range(n)));fm.append(0)
 mesh(name,vs,fs,0,'one-piece broad finite disk foot, tapered base shoulder, narrow upright shaft and integral faceted head');G[name]['face_materials']=fm
for side,sgn in [('Left',-1),('Right',1)]:
 stanchion('Stanchion_'+side,sgn*.940)
 rod('MountStud_'+side,(sgn*.924,0,.936),(sgn*.825,0,.919),.026,0,'closed solid fixed mounting stud; no claimed eye, aperture, clip or movable joint')
 link('Stanchion_'+side,'MountStud_'+side,(sgn*.902,0,.9322))
# Thick rope follows a broad low U-parabola. Every section is a genuine closed
# solid polygon; consecutive sections share complete ring edges.
ROPE_STATIONS=[]
for i in range(41):
 x=-.780+1.560*i/40;z=.580+.300*(x/.780)**2;slope=.600*x/(.780**2);L=math.sqrt(1+slope*slope)
 ROPE_STATIONS.append(((x,0,z),(-slope/L,0,1/L)))
vs=[];fs=[]
for c,u in ROPE_STATIONS:
 for j in range(N):
  a=math.tau*j/N+math.pi/N;vs.append((c[0]+R*u[0]*math.sin(a),R*math.cos(a),c[2]+R*u[2]*math.sin(a)))
fs.append(tuple(reversed(range(N))))
for i in range(len(ROPE_STATIONS)-1):
 for j in range(N):fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
fs.append(tuple((len(ROPE_STATIONS)-1)*N+j for j in range(N)))
mesh('Rope_ContinuousSag',vs,fs,1,'one continuous thick solid rope with forty axial cells, closed seated ends and fixed smooth sag; no curve bevel dependency')
FERRULE_AXES={}
for side,sgn in [('Left',-1),('Right',1)]:
 p=(sgn*.780,0,.880);t=(-sgn,0,-.600/.780);L=math.sqrt(sum(x*x for x in t));t=tuple(x/L for x in t)
 a=add(p,mul(t,-.070));b=add(p,mul(t,.040));FERRULE_AXES[side]={'a':a,'b':b,'radius':.037,'rope_endpoint':p}
 rod('Ferrule_'+side,a,b,.037,2,'solid fixed rope-end ferrule seated onto real rope and mounting stud; not an open eye or detachable hardware')
 link('MountStud_'+side,'Ferrule_'+side,(sgn*.836,0,.921))
 link('Ferrule_'+side,'Rope_ContinuousSag',add(p,mul(t,.019)),spread=.006)
# Finite volumes show actual open space under the sag and beside both shafts.
empty_box('UnderRope_Central',(0,0,.280),(1.360,.280,.500),'central finite clearance volume below the rope, above ground and between bases')
empty_box('UnderRope_Left',(-.800,0,.450),(.120,.120,.500),'finite open space between the left shaft and below the rising rope')
empty_box('UnderRope_Right',(.800,0,.450),(.120,.120,.500),'finite open space between the right shaft and below the rising rope')
for x,z in [(0,.28),(-.8,.45),(.8,.45),(0,.54)]:GAPS.append({'label':'under_rope_'+str((x,z)),'origin_m':[x,-.22,z],'direction':[0,1,0],'length_m':.44})
ROPE_SPEC={'stanchion_profile_z_radius_m':POST_PROFILE,'stanchion_centres_x_m':[-.940,.940],'stanchion_radial_sides':20,'rope_stations':ROPE_STATIONS,'rope_radial_sides':N,'rope_radius_m':R,'rope_cells':40,'ferrule_axes':FERRULE_AXES,'fixed_assembly_only':True,'single_prop_count':1,'public_safety_or_barrier_function_claim':False}
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
root=bpy.data.objects.new('OneFixedRopeBarrier',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual imported/generated triangle wall probes and source station evidence.
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);hits=[];travel=0.0
 for _ in range(4):
  q,_,_,dist=trees[r['mesh']].ray_cast(p,d,r['length_m']-travel)
  if q is None:break
  absolute=travel+dist;hits.append(absolute);p=q+d*1e-6;travel=absolute+1e-6
 assert len(hits)==2 and all(abs(hits[i]-r['expected_hits_m'][i])<2e-6 for i in range(2)),('wall thickness',r,hits)
 wall_checks.append(dict(r,actual_hits_m=hits,actual_thickness_m=hits[1]-hits[0]))
rope_evidence=dict(ROPE_SPEC,finite_void_volumes=VOID_VOLUMES,finite_volume_empty_checks=void_volume_checks)

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
 'single_prop_count':1,'rope_geometry':rope_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/museum/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.48));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.72;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3,-7,3.2),'gray-back3q':(-3,7,3.2)} if gray else {
 'thumbnail':(3,-7,3.2),'qa-front':(0,-7,1.7),'qa-side':(7,0,1.7),'qa-top':(0,0,8),
 'qa-back':(0,7,1.7),'qa-wireframe':(3,-7,3.2)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.72
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00425;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.48)),('silhouette-128-side',(7,0,.48))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
