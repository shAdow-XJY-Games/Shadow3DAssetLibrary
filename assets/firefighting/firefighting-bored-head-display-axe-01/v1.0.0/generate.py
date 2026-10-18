"""Original blunt bored-head axe: one fixed visual prop, never a real tool design."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='firefighting-bored-head-display-axe-01';VERSION='1.0.0';TITLE='Bored-Head Fire Axe Display'
DESCRIPTION=('One original static low-poly blunt fire-axe visual prop, lying flat in one fixed pose. A single continuous thick red metal-style head has a broad curved silver-coloured bit, a real geometric thickness taper, a finite blunt edge and poll, and a genuine rectangular handle eye passing completely through the head along the handle axis. '
 'One continuous lightly curved ochre wooden-style long handle passes through this eye, with finite lateral inset joints, visible upper end, a thicker shoulder and an integral thick dark grip end. The head broad underside and grip underside have real finite flat ground patches. Two named editable closed meshes, four opaque constant PBR materials, metres, source Z up, front -Y, origin on the handle centreline under the head at ground. One whole tool counts as one prop. No textures, logo, animation, separate wedge, sheath, rack, person, fire, target or scene. '
 'Static blunt visual geometry only. No chopping, breaking, cutting, sharpness, material hardness, strength, heat or fire resistance, wearer or hand fit, ergonomics, load, durability, stability, manufacturing tolerance, real tool use, firefighting performance or safety certification is claimed. Not real equipment design, manufacture or use guidance. No brand, model or compatibility with earlier tools or vehicles is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={}
PALETTE=[('OxideRed_Head',(.55,.055,.026,1),.42,.50),('SatinSilver_BluntBit',(.48,.54,.56,1),.31,.75),('HoneyOchre_Handle',(.54,.28,.083,1),.67,0),('Charcoal_IntegralGrip',(.055,.074,.077,1),.78,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(-.055,.300,.035);ORTHO=1.08
CAMERAS={'gray-front3q':(1.10,-1.10,1.65),'gray-back3q':(-1.10,1.70,1.65),'thumbnail':(1.10,-1.10,1.65),'qa-front':(-.055,-1.60,1.35),'qa-side':(1.80,.300,1.50),'qa-top':(-.055,.300,2.00),'qa-back':(-.055,2.00,1.35),'qa-wireframe':(1.10,-1.10,1.65),'silhouette-128-front':(-.055,-1.60,1.35),'silhouette-128-side':(1.80,.300,1.50)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,p,mat=0,tag=''):
  ids=[self.vertex(q) for q in p]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
# A conforming cell boundary creates ONE continuous thick head. Internal faces
# are removed, including the middle X/Z band of the true through-eye.
# X, half-width in Y, full Z thickness. The forward silhouette is bowed.
HEAD_SECTIONS=[(-.216,.010,.020),(-.210,.052,.024),(-.195,.088,.032),(-.175,.108,.044),(-.140,.098,.064),(-.100,.081,.080),(-.050,.065,.080),(-.0188,.065,.080),(-.018,.065,.080),(.018,.065,.080),(.0188,.065,.080),(.045,.060,.080),(.078,.050,.080)]
def headp(i,side,k):
 x,w,h=HEAD_SECTIONS[i];return(x,side*w,.040+h*[-.5,-.225,.225,.5][k])
cells={}
for i in range(len(HEAD_SECTIONS)-1):
 for k in range(3):
  if HEAD_SECTIONS[i][0]==-.018 and k==1:continue
  v=[headp(ii,side,kk) for kk in [k,k+1] for side in [-1,1] for ii in [i,i+1]]
  for face,tag in [((0,2,3,1),'lower'),((4,5,7,6),'upper'),((0,1,5,4),'front'),((2,6,7,3),'back'),((0,4,6,2),'left'),((1,3,7,5),'right')]:
   q=[v[j] for j in face];key=tuple(sorted(q))
   if key in cells:del cells[key]
   else:cells[key]=(q,1 if i<5 else 0,tag)
m=Mesh()
for q,mat,tag in cells.values():m.face(q,mat,tag)
G['Axe_ContinuousBoredHead']=m.result('One continuous thick curved blunt head with an actual axial through-eye, integral geometric taper and finite flat underside; no solid head pierced by a rod substitute.')
# Integral lightly bowed handle, all sections are convex octagons. The end
# profile has finite ground width; the shoulder and grip are continuous geometry.
HANDLE_SECTIONS=[(-.084,0,.0188,.025,.055),(.072,0,.0188,.025,.055),(.090,0,.024,.014,.066),(.150,.001,.022,.017,.063),(.300,.012,.018,.019,.061),(.460,.025,.019,.016,.064),(.580,.029,.024,.009,.071),(.610,.028,.027,0,.080),(.720,.023,.029,0,.080),(.752,.020,.025,.005,.075)]
def handleprofile(s):
 y,c,w,z0,z1=s;h=z1-z0;b=.18*h
 return [(c-.65*w,y,z0),(c+.65*w,y,z0),(c+w,y,z0+b),(c+w,y,z1-b),(c+.65*w,y,z1),(c-.65*w,y,z1),(c-w,y,z1-b),(c-w,y,z0+b)]
profiles=[handleprofile(s) for s in HANDLE_SECTIONS];m=Mesh()
for k,(a,b) in enumerate(zip(profiles,profiles[1:])):
 for i in range(8):j=(i+1)%8;m.face([a[i],a[j],b[j],b[i]],3 if k>=6 else 2,'handle_'+str(k))
m.face(profiles[0][::-1],2,'upper_end');m.face(profiles[-1],3,'grip_end')
G['Axe_ContinuousCurvedHandle']=m.result('One complete lightly curved handle with exposed axial end, wider shoulder and integral thick grip. Two finite 0.8 mm lateral visual insets connect it to the real head eye.',2)
LINKS=[('Axe_ContinuousBoredHead','Axe_ContinuousCurvedHandle',[(x,y,z) for x in [-.0184,.0184] for y in [-.040,.040] for z in [.034,.046]])]
FEET=list(G)
BORES=[{'mesh':'Axe_ContinuousBoredHead','origin_m':(0,-.09,.040),'direction':(0,1,0),'length_m':.18,'role':'isolated head through-eye full axial path'}]
VOID_PROBES={'CompleteIsolatedThroughEye':{'type':'box','lo_m':[-.0175,-.090,.0225],'hi_m':[.0175,.090,.0575],'targets':['Axe_ContinuousBoredHead'],'role':'whole inset rectangular eye through full head depth; isolated before assembly'},'AssembledUpperEyeClearance':{'type':'box','lo_m':[-.010,-.074,.0555],'hi_m':[.010,.067,.0575],'targets':list(G),'role':'entire head depth upper free wall strip after insertion'},'AssembledLowerEyeClearance':{'type':'box','lo_m':[-.010,-.074,.0225],'hi_m':[.010,.067,.0245],'targets':list(G),'role':'entire head depth lower free wall strip after insertion'}}
JOINT_REGIONS=[{'lo_m':[x0,-.065,.022],'hi_m':[x1,.065,.058]} for x0,x1 in [(-.01881,-.01799),(.01799,.01881)]]
def measure_axe_geometry(vertices):
 h=vertices['Axe_ContinuousBoredHead'];w=vertices['Axe_ContinuousCurvedHandle']
 def ext(v,i):return max(p[i] for p in v)-min(p[i] for p in v)
 return {'single_prop_count':1,'mesh_count':len(G),'head_width_x_m':ext(h,0),'head_span_y_m':ext(h,1),'head_body_thickness_z_m':ext(h,2),'minimum_blunt_forward_edge_z_m':.020,'eye_nominal_cross_section_m':[.036,.036],'eye_full_axial_length_m':.130,'finite_lateral_embed_depth_m':.0008,'continuous_handle_length_y_m':ext(w,1),'handle_ground_region_y_m':[.610,.720],'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed blunt display axe; no use, cutting, strength, protection or safety claim'}

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
root=bpy.data.objects.new('OneBoredHeadAxeDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X centreline, design Y=0 and ground Z=0; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]

# Geometry-only source checks are repeated on actual generated Blender triangles.
# Independent acceptance separately imports the final GLB and verifies the entire interface.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
axe_evidence=measure_axe_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
adj={name:set() for name in G}
for a,b,points in LINKS:
 samples=[]
 for p in points:
  margin=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3]);valid=actual_inside(a,p) and actual_inside(b,p) and margin>.0001;assert valid,(a,b,p,margin)
  samples.append({'point_m':p,'both_interiors':True,'nearest_boundary_margin_m':margin})
 joints.append({'a':a,'b':b,'samples':samples});adj[a].add(b);adj[b].add(a)
for r in CONTACTS:
 a,b=r['a'],r['b'];eps=r['interior_probe_offset_m']
 for p in r['points']:
  low=(p[0],p[1],p[2]-eps);high=(p[0],p[1],p[2]+eps)
  assert actual_inside(a,low) and actual_inside(b,high) and not actual_inside(a,high) and not actual_inside(b,low),(a,b,p)
 adj[a].add(b);adj[b].add(a);face_contacts.append(dict(r,actual_opposed_interior_side_probes=True,full_area_scope='pure source and independent actual GLB full-surface audit'))
todo=list(seen)
while todo:
 for name in adj[todo.pop()]-seen:seen.add(name);todo.append(name)
assert seen==set(G),seen
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
 'single_prop_count':1,'axe_geometry':axe_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
