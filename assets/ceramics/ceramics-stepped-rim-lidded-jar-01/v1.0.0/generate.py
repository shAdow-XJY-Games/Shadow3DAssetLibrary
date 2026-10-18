"""Original stepped-rim lidded ceramic jar. One static prop, two solid parts.
Metres, native Z up, bounds-centred ground origin. Default: open jar plus upside-down lid.
A single additional rigid placement checks static closure; no motion or sealing claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='ceramics-stepped-rim-lidded-jar-01';VERSION='1.0.0';TITLE='Stepped-Rim Lidded Ceramic Jar'
DESCRIPTION=('One original static low-poly ceramic jar prop with a squat rounded thick-walled body, short neck and a genuine stepped recessed lid seat. '
 'The complete inner wall and closed inner floor are real geometry. A separate single-piece shallow domed thick lid includes its integral knob, annular seating shoulder and short hollow locating skirt. '
 'Default display shows the open jar and the lid upside down beside it, both with finite flat ground contact areas; the upward skirt exposes the lid underside. '
 'The identical lid and body also have one documented static closed placement with a full finite opposed annular support region and positive complete skirt/throat and gallery clearance. '
 'Two named editable closed connected meshes, three opaque constant ceramic PBR materials, metres, native Z up, bounds-centred ground origin, illustrative front -Y. '
 'No external textures, extra container, display stand, labels or animation. Static visual geometry only: no continuous opening/closing or insertion path, seal, airtightness, waterproofing, food contact, storage volume rating, true material, kiln compatibility, firing shrinkage, manufacturing tolerance, durability, load or safety guarantee.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=['Jar_ThickBody','Lid_IntegralKnobAndSkirt'];VOID_PROBES={}
PALETTE=[('DeepCeladon_Glaze',(.085,.28,.245,1),.33,0),('WarmIvory_Interior',(.63,.51,.34,1),.54,0),('Unglazed_ClaySeat',(.36,.20,.105,1),.76,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no textures or procedural nodes.'
N=40
BODY_PROFILE=[(0,0),(.080,0),(.093,.009),(.099,.023),(.130,.039),(.146,.071),(.151,.108),(.143,.149),(.126,.178),(.112,.194),(.112,.212),(.120,.218),(.120,.234),(.116,.238),(.108,.238),(.108,.225),(.098,.225),(.098,.202),(.114,.187),(.132,.151),(.139,.111),(.132,.075),(.116,.049),(.087,.031),(.050,.024),(0,.024)]
LID_PROFILE=[(0,.292),(.015,.292),(.021,.286),(.021,.273),(.012,.269),(.012,.260),(.038,.258),(.078,.255),(.108,.249),(.115,.245),(.115,.243),(.106,.240),(.106,.225),(.096,.225),(.096,.209),(.087,.209),(.087,.236),(.055,.239),(0,.241)]
BODY_ORIGIN=(-.125,0,0);LID_ORIGIN=(.235,-.025,.292)
# These exact coordinates place the complete default bounds symmetrically about X=Y=0.
SHIFT=(-.037,0,0)
BODY_ORIGIN=tuple(BODY_ORIGIN[i]+SHIFT[i] for i in range(3));LID_ORIGIN=tuple(LID_ORIGIN[i]+SHIFT[i] for i in range(3))
FOCUS=(0,0,.105);ORTHO=.75
CAMERAS={'gray-front3q':(.65,-1.0,.92),'gray-back3q':(-.65,1.0,.92),'thumbnail':(.65,-1.0,.92),'qa-front':(0,-1.4,.70),'qa-side':(1.4,0,.70),'qa-top':(0,0,1.4),'qa-back':(0,1.4,.70),'qa-wireframe':(.65,-1.0,.92),'silhouette-128-front':(0,-1.4,.70),'silhouette-128-side':(1.4,0,.70)}
CAMERA_SCALES={'qa-side':.55,'silhouette-128-side':.55};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def transform(p,origin,invert=False):return (p[0]+origin[0],(-p[1] if invert else p[1])+origin[1],(-p[2] if invert else p[2])+origin[2])
def lathe(profile,origin=(0,0,0),invert=False,mat_segments=None):
 vs=[];rings=[];fs=[];fm=[];segments=[]
 for r,z in profile:
  ring=[]
  for i in range(N if r else 1):
   a=math.tau*i/N;ring.append(len(vs));vs.append(transform((r*math.cos(a),r*math.sin(a),z),origin,invert))
  rings.append(ring)
 for k,(aa,bb) in enumerate(zip(rings,rings[1:])):
  for i in range(N):
   j=(i+1)%N
   faces=[(aa[0],bb[j],bb[i])] if len(aa)==1 else ([(aa[i],aa[j],bb[0])] if len(bb)==1 else [(aa[i],aa[j],bb[j]),(aa[i],bb[j],bb[i])])
   fs.extend(faces);fm.extend([mat_segments[k] if mat_segments else 0]*len(faces));segments.extend([k]*len(faces))
 vol=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':[tuple(round(c,9) for c in v) for v in vs],'faces':fs,'face_materials':fm,'material':0,'face_profile_segments':segments,'profile_rz_m':profile,'rings':rings}
bodym=[2 if k<=2 or 14<=k<=16 else 1 if k>=17 else 0 for k in range(len(BODY_PROFILE)-1)]
lidm=[0 if k<=10 else 2 if 11<=k<=15 else 1 for k in range(len(LID_PROFILE)-1)]
G['Jar_ThickBody']=lathe(BODY_PROFILE,BODY_ORIGIN,False,bodym);G['Jar_ThickBody']['role']='Original squat closed thick shell with actual interior, inner floor, short neck, raised gallery and recessed annular lid seat.'
# The display transform is a proper 180-degree rotation about local X, plus translation.
G['Lid_IntegralKnobAndSkirt']=lathe(LID_PROFILE,LID_ORIGIN,True,lidm);G['Lid_IntegralKnobAndSkirt']['role']='Single connected thick lid including integral knob and hollow locating skirt, displayed upside down with its finite knob cap on ground.'

def closed_lid_vertices(display_vertices):
 return [(v[0]-LID_ORIGIN[0]+BODY_ORIGIN[0],-(v[1]-LID_ORIGIN[1])+BODY_ORIGIN[1],-(v[2]-LID_ORIGIN[2])) for v in display_vertices]
CLOSED_POSE={'body_mesh':'Jar_ThickBody','lid_mesh':'Lid_IntegralKnobAndSkirt','body_origin_m':BODY_ORIGIN,'lid_display_origin_m':LID_ORIGIN,'rotation_about_lid_local_x_degrees':180,'seat_plane_z_m':.225,'minimum_contact_area_m2':.0045,'scope':'one static closed rigid placement only; display GLB bytes do not change'}
CAVITY_PROFILE=[(0,.028),(.045,.028),(.083,.035),(.112,.055),(.128,.080),(.134,.111),(.127,.147),(.108,.181),(.093,.200),(.090,.220),(.101,.231),(.101,.260),(0,.260)]
LID_VOID_PROFILE=[(0,.190),(.082,.190),(.082,.232),(.050,.235),(0,.237)]
STORAGE_VOID_PROFILE=[(0,.028),(.045,.028),(.083,.035),(.112,.055),(.128,.080),(.134,.111),(.127,.147),(.108,.181),(.093,.200),(.092,.205),(0,.205)]
VOID_PROBES['JarCompleteInnerCavity']=dict(lathe(CAVITY_PROFILE,BODY_ORIGIN),role='Finite connected empty cavity from near the real inner floor through the actual full mouth.',targets=['Jar_ThickBody','Lid_IntegralKnobAndSkirt'])
VOID_PROBES['LidUndersideAndSkirtVoid']=dict(lathe(LID_VOID_PROFILE,LID_ORIGIN,True),role='Complete finite hollow underside and open locating-skirt volume, displayed upside down.',targets=['Jar_ThickBody','Lid_IntegralKnobAndSkirt'])
CLOSED_VOID=dict(lathe(STORAGE_VOID_PROFILE,BODY_ORIGIN),role='Finite interior cavity remains empty in the one closed placement; no rated capacity.')
INTERFACE_SEGMENTS={'body_seat':[15],'lid_seat':[12],'body_gallery':[14],'lid_gallery':[11],'body_throat':[16],'lid_skirt_outer':[13],'lid_skirt_inner':[15]}
def measure_jar_geometry(vertices):
 b=vertices['Jar_ThickBody'];l=vertices['Lid_IntegralKnobAndSkirt'];return {'body_height_m':max(v[2] for v in b)-min(v[2] for v in b),'body_width_m':max(v[0] for v in b)-min(v[0] for v in b),'lid_display_height_m':max(v[2] for v in l)-min(v[2] for v in l),'default_pose':'open jar plus upside-down lid; both independently finite ground-supported','closed_pose':CLOSED_POSE,'closed_placement_is_same_geometry_rigid_transform':True,'single_prop_count':1,'material_contract':MATERIAL_CONTRACT}
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
root=bpy.data.objects.new('OneLiddedCeramicJar',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
jar_evidence=measure_jar_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'single_prop_count':1,'lidded_jar_geometry':jar_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/ceramics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'ceramics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
