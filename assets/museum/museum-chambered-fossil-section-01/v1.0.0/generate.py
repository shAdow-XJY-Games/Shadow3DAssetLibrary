"""Original stylized chambered fossil section, metres, source Z up, face toward -Y.
A thick hand-cut rock slice, a solid continuous expanding spiral shell wall,
22 thick radial-curved septa, actual recessed chambers and a closed central knot.
The cut face is deliberately stylized; no species identification or anatomical,
geological, palaeontological, load or museum conservation accuracy is claimed.
Self-contained. --geometry-only / --no-render / --gray-only / --preview-only /
--extra-views. Every image imports the exact exported GLB into an emptied scene.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='museum-chambered-fossil-section-01';VERSION='1.0.0';TITLE='Chambered Fossil Section'
DESCRIPTION=('Original stylized spiral-shell fossil section with a thick irregular stone matrix and broad directly grounded cut bottom. '
 'A continuous expanding solid shell wall and 22 separate thick curved septa bound a sequence of genuinely recessed chambers. '
 'The pale planar shell faces, darker chamber floors and rough faceted outer rind are actual closed meshes with solid PBR materials; '
 'no image, procedural texture or painted fossil pattern is used. The shell walls project 0.15 m above the recessed stone floor '
 'and are embedded into the matrix. Metres, Z-up native source, front facing -Y. Named editable parts and self-contained generator. '
 'This single specimen differs from the existing five-prism crystal cluster and unsectioned raw minerals. '
 'Static artistic collection prop; no real species identification, scientific anatomical reconstruction, dating, geological '
 'accuracy, physical conservation, load, stability or safety certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough in [('FacetedStoneRind',(.24,.25,.22,1),.87),('WarmCutLimestone',(.43,.36,.26,1),.84),
 ('PaleCalcifiedShell',(.72,.59,.39,1),.75),('RecessedChamberStone',(.30,.25,.18,1),.88)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0
 mats.append(m)
root=bpy.data.objects.new('ChamberedFossilSection',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_axis']='-Y';root['static_stylized_specimen_only']=True
root['origin_datum']='direct matrix flat-bottom ground plane Z=0'
root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,face_materials=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 for m in mats:me.materials.append(m)
 for i,p in enumerate(me.polygons):p.material_index=material if face_materials is None else face_materials[i]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o['component_role']=role;parts.append(o);byname[name]=o
 for p in me.polygons:p.use_smooth=False
 return o
CZ=.61;TAU=math.tau;TMAX=2.25*TAU;THETA0=-1.0
# A closed sculpted slab. The circular cavity has a real .13 m wall and a
# .16 m stone floor-to-back thickness; the outer rind is faceted and irregular.
N=40;verts=[]
def outline(i,scale):
 a=TAU*i/N;r=(.622+.016*math.sin(3*a+.6)+.013*math.cos(7*a-.2))*scale
 x=r*math.cos(a);z=CZ+r*math.sin(a)
 return (x,0 if z<.075 else z)
for y,scale in [(-.09,1.0),(.035,1.025),(.20,.96)]:
 for i in range(N):x,z=outline(i,scale);verts.append((x,y,z))
for y,r in [(-.09,.480),(.04,.474)]:
 for i in range(N):a=TAU*i/N;verts.append((r*math.cos(a),y,CZ+r*math.sin(a)))
frontcenter=len(verts);verts.append((0,.04,CZ));backcenter=len(verts);verts.append((0,.20,CZ))
faces=[];fm=[]
def face(indices,material):faces.append(indices);fm.append(material)
for i in range(N):
 j=(i+1)%N
 face((i,j,N+j,N+i),0);face((N+i,N+j,2*N+j,2*N+i),0)
 face((i,3*N+i,3*N+j,j),1);face((3*N+i,4*N+i,4*N+j,3*N+j),1)
 face((4*N+i,frontcenter,4*N+j),3);face((2*N+i,2*N+j,backcenter),0)
mesh('Matrix_ThickCutStone',verts,faces,0,'closed thick stone slice with recessed chamber floor, rough outer rind and flat ground face',fm)
def radius(t):return .052*math.exp(.153*t)
def spiralpoint(t):
 a=THETA0+t;r=radius(t);return (r*math.cos(a),CZ+r*math.sin(a))
def ribbon(name,path,widths,front,back,role):
 vs=[]
 for i,(x,z) in enumerate(path):
  before=Vector(path[max(i-1,0)]);after=Vector(path[min(i+1,len(path)-1)])
  tang=(after-before).normalized();normal=Vector((-tang.y,tang.x));w=widths[i]/2
  for y,sign in [(front,-1),(front,1),(back,1),(back,-1)]:vs.append((x+sign*w*normal.x,y,z+sign*w*normal.y))
 fs=[(3,2,1,0)]
 for i in range(len(path)-1):
  a=4*i;b=a+4
  for j in range(4):fs.append((a+j,a+(j+1)%4,b+(j+1)%4,b+j))
 a=4*(len(path)-1);fs.append((a,a+1,a+2,a+3))
 return mesh(name,vs,fs,2,role)
SPIRAL_TS=[TMAX*i/220 for i in range(221)]
ribbon('Shell_ContinuousSpiral',[spiralpoint(t) for t in SPIRAL_TS],[.010+.006*t/TMAX for t in SPIRAL_TS],-.11,.065,
 'real continuous 2.25-turn expanding shell wall; .15 m exposed depth and solid matrix embedment')
# The central knot meets the beginning of the shell; no disconnected floating detail.
vs=[(.055*math.cos(TAU*i/20),y,CZ+.055*math.sin(TAU*i/20)) for y in [-.104,.064] for i in range(20)]
fs=[tuple(range(19,-1,-1)),tuple(range(20,40))]+[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)]
mesh('Shell_CentralKnot',vs,fs,2,'closed small central knot embedded into the matrix and overlapping the spiral start')
SEPTA_TS=[2.8,3.5,4.2,4.9,5.6,6.3,6.85,7.4,7.95,8.5,9.05,9.6,10.15,10.7,11.25,11.75,12.2,12.65,13.05,13.45,13.8,TMAX]
septa_paths={}
def septum_point(t,u):
 ri=radius(t-TAU) if t>=TAU else .049
 ro=radius(t);r=ri+(ro-ri)*u;a=THETA0+t+.075*math.sin(math.pi*u)
 return (r*math.cos(a),CZ+r*math.sin(a))
for i,t in enumerate(SEPTA_TS):
 name='Septum_%02d'%(i+1);path=[septum_point(t,u/10) for u in range(11)];septa_paths[name]=path
 ribbon(name,path,[.009+.004*u/10 for u in range(11)],-.106,.063,
  'solid curved transverse chamber partition embedded into floor, with shell end overlap; terminal cap' if i==len(SEPTA_TS)-1 else
  'solid curved transverse chamber partition embedded into floor and overlapping shell at its outer end')
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 votes=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  votes.append(bool(hits%2))
 return all(votes)
joints=[]
def joint(a,b,points):
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
for name in septa_paths:
 pts=[septa_paths[name][i] for i in [2,5,8]]
 joint('Matrix_ThickCutStone',name,[(x,.052,z) for x,z in pts])
joint('Matrix_ThickCutStone','Shell_ContinuousSpiral',[(spiralpoint(t)[0],.052,spiralpoint(t)[1]) for t in [1.0,5.0,9.0,13.0]])
joint('Matrix_ThickCutStone','Shell_CentralKnot',[(x,.052,CZ+z) for x,z in [(-.015,0),(.015,0),(0,.02)]])
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={'Matrix_ThickCutStone'};todo=list(seen)
while todo:
 for other in adj[todo.pop()]-seen:seen.add(other);todo.append(other)
assert seen==set(adj),('Unsupported components',set(adj)-seen)
def first_ray(origin,direction,distance):
 hits=[]
 for name,tree in trees.items():
  p,n,_,d=tree.ray_cast(Vector(origin),Vector(direction),distance)
  if p is not None:hits.append((d,name,p,n))
 return min(hits,key=lambda h:h[0]) if hits else None
# Whole-assembly rays pass through each exposed chamber and reach the actual
# matrix floor, .15 m behind the shell cut face. These are not texture checks.
chamber_rays=[]
for i,(ta,tb) in enumerate(zip(SEPTA_TS[:-1],SEPTA_TS[1:])):
 t=(ta+tb)/2;a=THETA0+t;ri=radius(t-TAU) if t>=TAU else .055;ro=radius(t)
 for u in [.36,.64]:
  r=ri+(ro-ri)*u;x=r*math.cos(a);z=CZ+r*math.sin(a)
  h=first_ray((x,-.50,z),(0,1,0),1)
  assert h and h[1]=='Matrix_ThickCutStone' and abs(h[2].y-.04)<1e-6,(i,u,h)
  chamber_rays.append({'chamber_index':i+1,'origin_m':[x,-.50,z],'first_hit':h[1],'point_m':list(h[2]),'shell_front_y_m':-.11,'visible_depth_m':round(h[2].y+.11,6)})
# Real finite downward-facing triangles, not min-Z or AABB alone.
o=byname['Matrix_ThickCutStone'];patch=[]
for t in o.data.loop_triangles:
 v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
 if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
area=sum(t['area_m2'] for t in patch);assert area>.05,area
supports=[{'name':o.name,'ground_z_m':0,'area_m2':area,'triangles':patch}]
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_matrix':sorted(seen),
 'chamber_full_assembly_floor_rays':chamber_rays,'finite_matrix_ground_supports':supports,
 'fossil_geometry':{'spiral_turns':2.25,'septa_count':len(SEPTA_TS),'validated_open_chambers':len(SEPTA_TS)-1,
 'shell_front_y_m':-.11,'septa_front_y_m':-.106,'chamber_floor_y_m':.04,'stone_back_y_m':.20,
 'shell_wall_thickness_m':[.010,.016],'septum_thickness_m':[.009,.013],
 'limitation':'stylized static artistic specimen; no species or scientific reconstruction claim'},
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
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
focus=Vector((0,.035,.61));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.70;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(2.4,-6,2.9),'gray-back3q':(-3.4,5,3.2)} if gray else {
 'thumbnail':(2.4,-6,2.9),'qa-front':(0,-6,.61),'qa-side':(6,0,.61),'qa-top':(0,0,7),
 'qa-back':(0,6,.61),'qa-wireframe':(2.4,-6,2.9)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0008;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-6,.61)),('silhouette-128-side',(6,0,.61))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
