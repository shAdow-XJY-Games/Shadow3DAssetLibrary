"""Original tall graduated cylinder, a static illustrative prop only.
Metres, Z up, ground origin. An integral hexagonal foot and genuine deep cavity
are one continuous solid; the pouring lip deforms both sides of the same rim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-footed-graduated-cylinder-01';VERSION='1.0.0';TITLE='Footed Graduated Cylinder'
DESCRIPTION=('One original static low-poly graduated-cylinder visual prop: a slender straight thick-walled tube, real deep empty cavity and inner floor, an integral forward pouring lip and a broad six-sided ground-supported foot. '
 'The lip continuously deforms both inner and outer top surfaces of the same connected solid. Fifteen separate solid illustrative ticks, five long and ten short, embed finitely in the outside wall without entering the cavity. '
 'One main closed connected mesh plus fifteen closed connected tick meshes, three plain opaque constant PBR materials, metres, native Z up, bounds-centred ground origin and front -Y. '
 'No numbers, units, capacity, handle, lid, liquid, rack, additional size, textures or animation. Static visual geometry only: no calibrated scale, measurement accuracy, rated volume, transparency or refraction, fluid or meniscus simulation, pouring behavior, experimental procedure, diagnostic, chemical, temperature, material-performance, hygiene, human-fit, manufacturing, laboratory safety or certification claim. No compatibility claim with earlier laboratory props.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];BODY='Cylinder_IntegralFootAndSpout';FEET=[BODY];MARKS=[];VOID_VOLUMES={};EMBED_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('PaleMint_Exterior',(.40,.62,.56,1),.36,0),('WarmIvory_Interior',(.69,.65,.50,1),.54,0),('DeepTeal_FootAndTicks',(.025,.115,.12,1),.43,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no procedural or image textures.'
N=48
# Each profile row is (nominal radius, height, front-lip extension, hexagonal).
# The ordered meridian starts beneath the foot, travels up outside, over the
# open rim, and returns down the actual cavity to its closed inner floor.
PROFILE=[(0,0,0,False),(.082,0,0,True),(.094,.006,0,True),(.094,.013,0,True),(.083,.020,0,True),(.045,.020,0,False),(.038,.030,0,False),(.038,.290,0,False),(.038,.308,.008,False),(.040,.326,.021,False),(.040,.334,.023,False),(.031,.334,.023,False),(.030,.326,.021,False),(.030,.308,.008,False),(.030,.290,0,False),(.030,.050,0,False),(.025,.042,0,False),(0,.042,0,False)]
FOCUS=(0,0,.161);ORTHO=.43
CAMERAS={'gray-front3q':(.62,-.92,.70),'gray-back3q':(-.62,.92,.70),'thumbnail':(.62,-.92,.70),'qa-front':(0,-1.1,.46),'qa-side':(1.1,0,.46),'qa-top':(0,0,1.2),'qa-back':(0,1.1,.46),'qa-wireframe':(.62,-.92,.70),'silhouette-128-front':(0,-1.1,.46),'silhouette-128-side':(1.1,0,.46)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def front_weight(a):
 d=abs((a+math.pi/2+math.pi)%math.tau-math.pi)
 return max(0,1-d/(math.pi/6))
def ringpoint(r,z,e,h,a):
 if h:r=r*math.cos(math.pi/6)/math.cos((a+math.pi/6)%(math.pi/3)-math.pi/6)
 w=front_weight(a)
 return (r*math.cos(a),r*math.sin(a)-e*w,z-.004*w*(e/.023))
def finish(vs,fs,mats,segments=None):
 volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 g={'vertices':[tuple(round(c,9) for c in p) for p in vs],'faces':fs,'face_materials':mats,'material':0}
 if segments is not None:g['face_profile_segments']=segments
 return g
def shell(profile,materials=None):
 vs=[];rings=[];fs=[];fm=[];sg=[]
 for r,z,e,h in profile:
  ring=[]
  for i in range(N if r else 1):ring.append(len(vs));vs.append(ringpoint(r,z,e,h,math.tau*i/N))
  rings.append(ring)
 for k,(aa,bb) in enumerate(zip(rings,rings[1:])):
  for i in range(N):
   j=(i+1)%N;ff=[(aa[0],bb[j],bb[i])] if len(aa)==1 else ([(aa[i],aa[j],bb[0])] if len(bb)==1 else [(aa[i],aa[j],bb[j]),(aa[i],bb[j],bb[i])]);fs.extend(ff);fm.extend([materials[k] if materials else 0]*len(ff));sg.extend([k]*len(ff))
 g=finish(vs,fs,fm,sg);g['rings']=rings;return g
def sector(ri,ro,z0,z1,half,steps=6):
 vs=[]
 for z in [z0,z1]:
  for r in [ri,ro]:
   for j in range(steps+1):
    a=-math.pi/2-half+2*half*j/steps;vs.append((r*math.cos(a),r*math.sin(a),z))
 stride=steps+1
 def ix(k,r,j):return k*2*stride+r*stride+j
 quads=[]
 for j in range(steps):
  quads.extend([(ix(0,0,j),ix(0,0,j+1),ix(0,1,j+1),ix(0,1,j)),(ix(1,0,j),ix(1,1,j),ix(1,1,j+1),ix(1,0,j+1)),(ix(0,0,j),ix(1,0,j),ix(1,0,j+1),ix(0,0,j+1)),(ix(0,1,j),ix(0,1,j+1),ix(1,1,j+1),ix(1,1,j))])
 quads.extend([(ix(0,0,0),ix(0,1,0),ix(1,1,0),ix(1,0,0)),(ix(0,0,steps),ix(1,0,steps),ix(1,1,steps),ix(0,1,steps))])
 fs=[t for a,b,c,d in quads for t in [(a,b,c),(a,c,d)]];return finish(vs,fs,[2]*len(fs))
G[BODY]=shell(PROFILE,[2 if k<=4 else 1 if k>=11 else 0 for k in range(len(PROFILE)-1)]);G[BODY]['role']='One continuous thick shell, deep cavity and inner floor, broad integral hexagonal foot and continuously deformed open pouring lip.'
for i in range(15):
 z=.069+i*.0146;half=.28 if i%3==0 else .155;name=f'IllustrativeTick_{i+1:02d}_'+('Long' if i%3==0 else 'Short')
 g=sector(.0364,.0401,z-.00125,z+.00125,half);g['role']='Solid illustrative raised tick, embedded in outer wall; no numeric value or calibrated measurement.';G[name]=g;MARKS.append(name)
 embed=sector(.0367,.0371,z-.0008,z+.0008,half-.025);embed['targets']=[BODY,name];EMBED_VOLUMES[name]=embed
 LINKS.append((BODY,name,[(0,-.0369,z)]))
# Closed finite probes occupy the complete usable deep interior and its mouth.
# They stay strictly inset from actual walls, including the deformed lip region.
VOID_VOLUMES['CompleteDeepCavityAndOpenMouth']=dict(shell([(0,.046,0,False),(.023,.046,0,False),(.027,.052,0,False),(.027,.290,0,False),(.027,.308,.008,False),(.028,.326,.021,False),(.028,.334,.023,False),(.028,.356,.023,False),(0,.356,0,False)]),targets=list(G),role='Complete connected tall finite empty cavity from near the actual floor through the open lip and mouth.')
VOID_VOLUMES['FrontLipPassage']=dict(sector(.032,.047,.331,.343,.055,4),targets=list(G),role='Finite open front pour-lip corridor beyond the normal straight throat; crosses the lowered lip top into air.')
# Finite interior material witnesses are wholly inside actual body material.
SOLID_VOLUMES['CompleteFloorMaterial']=dict(shell([(0,.033,0,False),(.024,.033,0,False),(.024,.039,0,False),(0,.039,0,False)]),targets=[BODY],role='Finite complete central closed bottom plate material below the inner floor.')
def annulus(ri,ro,z0,z1):
 g=shell([(ri,z0,0,False),(ro,z0,0,False),(ro,z1,0,False),(ri,z1,0,False)])
 vs=g['vertices'];fs=list(g['faces']);fm=list(g['face_materials']);sg=list(g['face_profile_segments'])
 aa=g['rings'][-1];bb=g['rings'][0]
 for i in range(N):
  j=(i+1)%N;fs.extend([(aa[i],aa[j],bb[j]),(aa[i],bb[j],bb[i])]);fm.extend([0,0]);sg.extend([3,3])
 return finish(vs,fs,fm,sg)
SOLID_VOLUMES['TubeToFootMaterial']=dict(annulus(.0315,.0355,.015,.055),targets=[BODY],role='Complete finite annular material bridges foot, shoulder and cylinder wall.')
def measure_cylinder_geometry(vertices):
 b=vertices[BODY];return {'height_m':max(v[2] for v in b),'foot_width_m':max(v[0] for v in b)-min(v[0] for v in b),'body_nominal_outer_diameter_m':.076,'inner_floor_z_m':.042,'rim_z_m':.334,'minimum_nominal_inner_depth_m':.288,'front_lip_extension_m':.023,'illustrative_tick_count':len(MARKS),'long_ticks':5,'short_ticks':10,'single_continuous_body_foot_lip':True,'single_prop_count':1,'material_contract':MATERIAL_CONTRACT}
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
root=bpy.data.objects.new('OneFootedGraduatedCylinder',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
cylinder_evidence=measure_cylinder_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'cylinder_geometry':cylinder_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
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
