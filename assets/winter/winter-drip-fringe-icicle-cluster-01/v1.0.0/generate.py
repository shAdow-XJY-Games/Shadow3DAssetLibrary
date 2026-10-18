"""Original continuous drip-fringe icicles. Static hanging attachment, one prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-drip-fringe-icicle-cluster-01';VERSION='1.0.0';TITLE='Continuous Drip-Fringe Icicle Cluster'
DESCRIPTION=('One original low-poly hanging icicle fringe, seven unequal drips and their continuous irregular thick frozen lip form one closed editable mesh and count as one prop. Each drip has seven descending octagonal sections with continuous nonlinear narrowing, a mild drifting axis, a broad joined root and a finite blunt end. A planar bounded back attachment patch lies on source Y=0.075 m, X=-0.56 to 0.56 m, Z=1.015 to 1.065 m, facing +Y. The origin is the source design datum at (0,0,0), below the central lip, not a ground contact; all parts belong to one monolithic boundary. This is a hanging attachment with no independent standing or stability claim. Four opaque constant PBR ice colours, metres, source Z up, front -Y. No textures, transmission, refractive or fluid simulation, roof, support, scene, animation or variants. '
 'A temporary rectangular QA support touching the back patch is a geometric witness only and is excluded from the native model, GLB and formal images. No ice-growth, melting, dripping, scientific ice morphology, temperature, ice mass, hanging load, strength, falling-ice safety, manufacture, installation or physical suitability claim. No universal attachment, existing roof, snowbank, cliff, waterfall or other earlier asset compatibility is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[]
PALETTE=[('GlacialBlue_Body',(.32,.62,.76,1),.36,0),('PaleIce_Facets',(.57,.80,.86,1),.40,0),('DeepIce_Recess',(.21,.47,.62,1),.43,0),('FrostedLip',(.73,.88,.90,1),.53,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures, no transmission.'
FOCUS=(0,-.025,.59);ORTHO=1.62
CAMERAS={'gray-front3q':(1.3,-3.8,1.65),'gray-back3q':(-1.5,3.7,1.7),'thumbnail':(1.3,-3.8,1.65),'qa-front':(0,-4,.85),'qa-side':(4,-.025,1.15),'qa-top':(0,-.025,4.0),'qa-back':(0,4,.85),'qa-wireframe':(1.3,-3.8,1.65),'silhouette-128-front':(0,-4,.85),'silhouette-128-side':(4,-.025,1.15)}
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
# Seven unequal roots. cx, rx, ry, root z, length, final x drift, final y drift.
DRIPS=[(-.54,.058,.058,.944,.47,-.020,.012),(-.36,.074,.069,.925,.75,.018,-.012),(-.18,.052,.052,.953,.39,-.010,.008),(0,.083,.073,.918,.87,-.024,-.016),(.18,.064,.061,.944,.59,.022,.008),(.36,.071,.064,.934,.72,-.012,-.010),(.54,.050,.050,.958,.35,.014,.012)]
LEVELS=[0,.12,.29,.50,.72,.89,1.0];RADII=[1,.82,.64,.44,.255,.115,.055]
X_EDGES=[-.66,-.45,-.27,-.09,.09,.27,.45,.66]
LIP_LOWER=[.990,.980,.993,.984,.996,.982,.992,.985]
LIP_UPPER=[1.088,1.105,1.096,1.118,1.103,1.114,1.094,1.085]
Y_FRONT=-.150;Y_BACK=.075;Y_MID=-.0375
ATTACHMENT={'axis':'Y','coordinate_m':.075,'normal':[0,1,0],'x_range_m':[-.56,.56],'z_range_m':[1.015,1.065],'area_m2':.056,'role':'complete finite back patch, requiring external support; no ground contact'}
QA_SUPPORT={'lo_m':[-.56,.075,1.015],'hi_m':[.56,.18,1.065],'asset_member':False,'role':'temporary independent QA rectangular witness only, not a scene or an exported model'}
DRIP_RINGS=[];ROOT_INTERIOR_PROBES=[];VOID_PROBES={};m=Mesh();side_faces={}
def outer(i,top):
 l,r=X_EDGES[i:i+2];z0,z1=(LIP_UPPER if top else LIP_LOWER)[i:i+2];xm=(l+r)/2;zm=(z0+z1)/2
 return [(xm,Y_FRONT,zm),(r,Y_FRONT,z1),(r,Y_MID,z1),(r,Y_BACK,z1),(xm,Y_BACK,zm),(l,Y_BACK,z0),(l,Y_MID,z0),(l,Y_FRONT,z0)]
for i,(cx,rx,ry,rootz,length,dx,dy) in enumerate(DRIPS):
 rings=[]
 for level,radius in zip(LEVELS,RADII):
  drift=level*level*(3-2*level);cy=-.0375+dy*drift
  ring=[(cx+dx*drift+rx*radius*math.cos(-math.pi/2+j*math.pi/4),cy+ry*radius*math.sin(-math.pi/2+j*math.pi/4),rootz-length*level) for j in range(8)];rings.append(ring)
 DRIP_RINGS.append(rings)
 lower,upper=outer(i,False),outer(i,True)
 for j in range(8):
  k=(j+1)%8;m.face([lower[j],rings[0][j],rings[0][k],lower[k]],3,'lip_root_'+str(i))
  center=((X_EDGES[i]+X_EDGES[i+1])/2,Y_MID,(LIP_UPPER[i]+LIP_UPPER[i+1])/2+.022)
  m.face([center,upper[j],upper[k]],3,'lip_top_'+str(i))
  q=[lower[j],lower[k],upper[k],upper[j]];key=tuple(sorted(q))
  if key in side_faces:del side_faces[key]
  else:side_faces[key]=(q,3,'lip_back' if j in [3,4] else 'lip_outer')
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  for j in range(8):
   nxt=(j+1)%8;mat=[1,0,0,2,2,0,1,1][j]
   m.face([a[j],b[j],b[nxt],a[nxt]],mat,'drip_%d_level_%d'%(i,k))
 m.face(rings[-1][::-1],1,'tip_'+str(i))
 # A finite interior bridge straddles the seam, not merely an axis ray.
 ROOT_INTERIOR_PROBES.append({'name':'root_'+str(i),'lo_m':[cx-.012,-.0495,rootz-.012],'hi_m':[cx+.012,-.0255,rootz+.012]})
for q,mat,tag in side_faces.values():m.face(q,mat,tag)
G['Ice_ContinuousLipAndSevenDrips']=m.result('One connected closed monolithic frozen lip with seven continuous narrowing drip branches and a finite planar rear attachment patch.')
for i in range(6):
 # Whole finite box down from below every lip surface and through full depth.
 left=max(p[0] for ring in DRIP_RINGS[i] for p in ring);right=min(p[0] for ring in DRIP_RINGS[i+1] for p in ring)
 VOID_PROBES['FullInterDripGap_'+str(i)]={'type':'box','lo_m':[left+.004,-.16,.035],'hi_m':[right-.004,.085,.900],'targets':list(G),'role':'whole finite interdrip empty volume, full front/back depth and entire hanging span below roots'}
def measure_icicle_geometry(vertices):
 v=vertices['Ice_ContinuousLipAndSevenDrips'];ext=lambda axis:max(p[axis] for p in v)-min(p[axis] for p in v)
 return {'single_prop_count':1,'mesh_count':len(G),'drip_count':len(DRIPS),'section_count_per_drip':len(LEVELS),'span_m':[ext(i) for i in range(3)],'attachment':ATTACHMENT,'qa_support':QA_SUPPORT,'finite_root_connection_count':7,'minimum_tip_width_m':min(2*d[1]*RADII[-1] for d in DRIPS),'root_to_tip_lengths_m':[d[4] for d in DRIPS],'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed hanging visual attachment; requires an external support, no standalone ground or load claim'}

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
root=bpy.data.objects.new('OneContinuousIcicleFringe',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Source design datum (0,0,0), no ground contact; hanging back patch Y=0.075, +Y normal; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# The asset is one monolithic hanging attachment. No stand, roof or ground is exported.
assert len(parts)==1
icicle_evidence=measure_icicle_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert lo[2]>.04 and triangles<12000
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
 'components':component_checks,'single_prop_count':1,'icicle_geometry':icicle_evidence,'attachment_datum':ATTACHMENT,'temporary_support_exported':False,'ground_contact_claimed':False,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/winter/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'winter','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.11,.17,.21,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g);ground.hide_render=True
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
