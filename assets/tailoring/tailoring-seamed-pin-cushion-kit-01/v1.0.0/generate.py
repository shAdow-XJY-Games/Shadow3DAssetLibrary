"""Original static seamed pin cushion. No material or tool-safety claims.
Metres, Z up; finite flat cushion bottom at ground-centre origin. Original geometry.
Self-contained; every render uses a fresh actual GLB import and full solid-PBR guard.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='tailoring-seamed-pin-cushion-kit-01';VERSION='1.0.0';TITLE='Eight-Gore Seamed Pin Cushion'
DESCRIPTION=('One original low round pin cushion with eight visibly depressed radial gores, a tucked top centre and a recessed continuous waist seam. '
 'The cushion is a single closed bulging surface with a finite flat bottom. Its warm ivory waist is a material assignment on recessed geometry, never an overlay or texture. '
 'Five fixed slender steel-colour pins have matching faceted amber ball heads; each shaft has a short tapered lower end embedded well inside the cushion and an upper end embedded in its head. '
 'Eleven separately editable closed meshes, four solid PBR materials, no texture or external dependency. Metres, source Z up and ground-centre origin. '
 'The complete cushion-and-pins arrangement counts as one prop, not five pin assets. Only the pictured static pose is checked. '
 'No cloth, sewing, insertion, puncture or motion simulation; no real material, needle safety, puncture resistance, child suitability, manufacture or tool performance guarantee.')
G={};LINKS=[];FEET=['Cushion_SeamedBody'];BORES=[];GAPS=[]
PALETTE=[('Cushion_Mulberry',(.42,.065,.095,1),.84,0),('Seam_WarmIvory',(.68,.49,.29,1),.85,0),('Pin_BrushedSteel',(.44,.51,.54,1),.28,.72),('Head_Amber',(.88,.43,.055,1),.34,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
# z/r/radial-seam-depth/vertical-seam-depth. Eight radial gores visibly sculpt the body.
# Waist rings 4 and 5 are inset; the ivory seam lies on those surfaces, not atop them.
CUSHION_RINGS=[(0,.032,0,0),(.003,.041,.0003,0),(.008,.049,.001,.0003),(.012,.0518,.0018,.0005),(.013,.0502,.0018,.0005),(.0142,.0502,.0018,.0005),(.0152,.052,.0018,.0005),(.0235,.0495,.0023,.0012),(.0305,.0415,.0023,.0023),(.035,.027,.0015,.003),(.036,.0125,.0007,.0035),(.0325,.002,0,0)]
N=64;vs=[];fs=[];fm=[]
for z,r,rd,zd in CUSHION_RINGS:
 for i in range(N):
  a=math.tau*i/N;groove=((1+math.cos(8*a))/2)**4;rr=r-rd*groove;vs.append((rr*math.cos(a),rr*math.sin(a),z-zd*groove))
for j in range(len(CUSHION_RINGS)-1):
 for i in range(N):ii=(i+1)%N;fs.append((j*N+i,j*N+ii,(j+1)*N+ii,(j+1)*N+i));fm.append(1 if j==4 else 0)
fs += [tuple(reversed(range(N))),tuple((len(CUSHION_RINGS)-1)*N+i for i in range(N))];fm += [0,0]
mesh('Cushion_SeamedBody',vs,fs,0,'one continuous closed low bulging cushion; eight sculpted radial seam depressions; recessed waist hem; flat bottom')
G['Cushion_SeamedBody']['face_materials']=fm
PIN_SPECS=[('01',(-.024,-.020,.017),(-.033,-.028,.059)),('02',(-.022,.017,.017),(-.030,.023,.066)),('03',(.010,.027,.017),(.015,.036,.060)),('04',(.027,.001,.017),(.037,.002,.065)),('05',(.007,-.026,.017),(.011,-.037,.063))]
PIN_RADIUS=.0008;HEAD_RADIUS=.0036
# Matching radial profile for each actual static pin. The small lower cap remains deeply buried.
def pin(name,start,head):
 axis=unit(sub(head,start));length=math.sqrt(dot(sub(head,start),sub(head,start)));u=unit(cross(axis,(0,1,0)));v=cross(axis,u)
 profile=[(0,.00018),(.004,PIN_RADIUS),(length+.0008,PIN_RADIUS)];n=12;vs=[];fs=[]
 for along,r in profile:
  for i in range(n):a=math.tau*i/n;vs.append(add(add(start,mul(axis,along)),add(mul(u,r*math.cos(a)),mul(v,r*math.sin(a)))))
 for j in range(2):
  for i in range(n):ii=(i+1)%n;fs.append((j*n+i,j*n+ii,(j+1)*n+ii,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple(2*n+i for i in range(n))]
 shaft=mesh('Pin_'+name+'_Shaft',vs,fs,2,'fixed slender pin shaft with short tapered buried tip and upper end embedded in ball head')
 # Six latitude rings and two poles: closed faceted ball, not a flat disk or painted dot.
 vs=[add(head,(0,0,-HEAD_RADIUS))];fs=[];rings=7
 for j in range(1,rings):
  lat=-math.pi/2+math.pi*j/rings;z=HEAD_RADIUS*math.sin(lat);r=HEAD_RADIUS*math.cos(lat)
  for i in range(n):a=math.tau*i/n;vs.append(add(head,(r*math.cos(a),r*math.sin(a),z)))
 top=len(vs);vs.append(add(head,(0,0,HEAD_RADIUS)))
 for i in range(n):fs.append((0,1+(i+1)%n,1+i))
 for j in range(rings-2):
  for i in range(n):ii=(i+1)%n;fs.append((1+j*n+i,1+j*n+ii,1+(j+1)*n+ii,1+(j+1)*n+i))
 for i in range(n):fs.append((1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n,top))
 ball=mesh('Pin_'+name+'_BallHead',vs,fs,3,'matching faceted spherical ball head; shaft extends through a positive-volume interior region')
 link(shaft,'Cushion_SeamedBody',add(start,mul(axis,.007)),axis,.001)
 link(shaft,ball,add(head,mul(axis,-.0005)),axis,.0005)
for name,start,head in PIN_SPECS:pin(name,start,head)
def measure_pin_cushion_geometry(vertices):
 assert len(vertices)==11 and set(vertices)==set(G)
 body=sorted(set(tuple(round(float(c),7) for c in p) for p in vertices['Cushion_SeamedBody']));assert len(body)==N*len(CUSHION_RINGS)
 # Derive each angular column directly from coordinates. Radius increases then contracts.
 columns=[]
 for i in range(N):
  angle=math.tau*i/N;u=(math.cos(angle),math.sin(angle));col=[p for p in body if abs(p[0]*u[1]-p[1]*u[0])<1e-7 and p[0]*u[0]+p[1]*u[1]>0]
  assert len(col)==len(CUSHION_RINGS),(i,len(col));col.sort(key=lambda p:(p[2],math.hypot(p[0],p[1])))
  radii=[math.hypot(p[0],p[1]) for p in col];assert abs(min(p[2] for p in col))<1e-7 and .049<max(radii)<.0521
  columns.append({'angle_index':i,'vertices':len(col),'top_m':max(p[2] for p in col),'outer_radius_m':max(radii)})
 # Real crown gores must be lower than inter-gore lobes; actual waist points are recessed.
 indent=[]
 for sector in range(8):
  valley=columns[sector*8];lobe=columns[sector*8+4];depth=lobe['top_m']-valley['top_m'];assert .0029<depth<.0036;indent.append(depth)
 ground=[p for p in body if abs(p[2])<1e-7];assert len(ground)==64 and max(abs(math.hypot(p[0],p[1])-.032) for p in ground)<2e-7
 rows=[]
 for name,start,head in PIN_SPECS:
  shaft=sorted(set(tuple(float(c) for c in p) for p in vertices['Pin_'+name+'_Shaft']));ball=sorted(set(tuple(float(c) for c in p) for p in vertices['Pin_'+name+'_BallHead']));assert len(shaft)==36 and len(ball)==74
  axis=unit(sub(head,start));length=math.sqrt(dot(sub(head,start),sub(head,start)));along=[dot(sub(p,start),axis) for p in shaft];assert abs(min(along))<2e-7 and abs(max(along)-length-.0008)<2e-7
  assert min(p[2] for p in shaft)>.016 and max(p[2] for p in shaft)>.058
  rd=[math.sqrt(dot(sub(p,head),sub(p,head))) for p in ball];assert max(abs(r-HEAD_RADIUS) for r in rd)<2e-7
  rows.append({'pin':name,'actual_shaft_low_z_m':min(p[2] for p in shaft),'actual_shaft_high_z_m':max(p[2] for p in shaft),'actual_ball_radius_min_m':min(rd),'actual_ball_radius_max_m':max(rd),'actual_axis':axis,'actual_shaft_length_m':max(along)-min(along)})
 return {'actual_body_angular_columns':columns,'actual_crown_gore_depths_m':indent,'actual_flat_bottom_vertices':len(ground),'actual_pins':rows,'counted_props':1,'static_pose_only':True,'cloth_or_needle_insertion_simulated':False}
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
root=bpy.data.objects.new('OneStaticSeamedPinCushion',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
cushion_evidence=measure_pin_cushion_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'pin_cushion_geometry':cushion_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/tailoring/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'tailoring','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.036));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.145;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,4.5),'gray-back3q':(3,5,4.5)} if gray else {
 'thumbnail':(-3,-5,4.5),'qa-front':(0,-7,.036),'qa-side':(7,0,.036),'qa-top':(0,0,8),
 'qa-back':(0,7,.036),'qa-wireframe':(-3,-5,4.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.145
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00008;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.036)),('silhouette-128-side',(7,0,.036))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
