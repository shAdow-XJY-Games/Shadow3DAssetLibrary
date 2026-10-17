"""Original S01 closed 90-degree pavement corner, metres, Z up.
Self-contained Blender source; no external models, textures, fonts or add-ons.
blender -b -t 4 --python-exit-code 1 --python generate.py -- --no-render
--gray-only: two gray views plus 128px silhouette; --preview-only: first PBR;
--extra-views: final five after accepted thumbnail; no flag: all six.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from collections import Counter
from mathutils import Vector
START=time.time(); OUT=Path(__file__).resolve().parent
PREVIOUS_QA=json.loads((OUT/'qa-report.json').read_text()) if '--extra-views' in sys.argv and (OUT/'qa-report.json').exists() else None
ASSET='transport-curb-corner-01'; VERSION='1.0.0'; TITLE='S01 Right-Angle Pavement and Curb'
DESCRIPTION=('Original single closed 1.2 m square, 0.15 m high pavement corner with a continuous 0.15 m wide south/east curb band. '
 'West port X=-0.6 and north port Y=+0.6 join unchanged transport-curb-straight-01 or transport-curb-ramp-01. '
 'At identity, neighbours are centred (-1.6,0,0) with Z rotation 0 degrees and (0,1.6,0) with Z rotation +90 degrees. '
 'Rotate all placements together in 90-degree steps. Origin is footprint centre at ground Z=0. The old pieces retain their own 2 m pitch. '
 'One editable original mesh, two exact existing mineral PBR materials; no overlay or overlapping straight pieces. '
 'Static game visual module only; no road, engineering, accessibility, load or motion certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for material in list(bpy.data.materials):bpy.data.materials.remove(material)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for layer in scene.view_layers:layer.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
  'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
  'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,
  'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE=[('Warm gray paving',(.40,.39,.35,1),.88),('Light stone curb',(.57,.55,.49,1),.84)]
mats=[]
for name,color,roughness in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=roughness;p.inputs['Metallic'].default_value=0;mats.append(m)
root=bpy.data.objects.new('CurbCorner_90deg',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['origin_contract']='Footprint centre, ground Z=0, metres, Z up'
root['port_A']='X=-0.6, outward -X; original neighbour (-1.6,0,0), Rz=0'
root['port_B']='Y=+0.6, outward +Y; original neighbour (0,1.6,0), Rz=90'
root['quarter_turns_degrees']='0,90,180,270';root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
# A single rectangular closed shell with two material domains. No intersecting solids.
xs=[-.6,.45,.6];ys=[-.6,-.45,.6];verts=[(x,y,z) for z in [.15,0] for y in ys for x in xs]
faces=[];face_materials=[]
for j in range(2):
 for i in range(2):
  a=j*3+i;b=a+1;c=a+4;d=a+3;mi=int(j==0 or i==1)
  faces.extend([(a,b,c),(a,c,d),(a+9,c+9,b+9),(a+9,d+9,c+9)]);face_materials.extend([mi]*4)
ring=[0,1,2,5,8,7,6,3]
for a,b in zip(ring,ring[1:]+ring[:1]):
 faces.append((a,a+9,b+9,b));face_materials.append(int(all(verts[k][1]<=-.449999 for k in [a,b]) or all(verts[k][0]>=.449999 for k in [a,b])))
mesh=bpy.data.meshes.new('Single closed corner with continuous curb band');mesh.from_pydata(verts,[],faces);mesh.update()
part=bpy.data.objects.new('PavementCorner_ClosedSolid',mesh);scene.collection.objects.link(part);part.parent=root
part['role']='Single closed turn module';part['band_width_m']=.15;part['top_height_m']=.15
for m in mats:mesh.materials.append(m)
for face,mi in zip(mesh.polygons,face_materials):face.material_index=mi;face.use_smooth=False
bpy.context.view_layer.update()
def signature(m):
 p=m.node_tree.nodes['Principled BSDF'];return tuple(round(float(v),6) for v in p.inputs['Base Color'].default_value)+(round(float(p.inputs['Roughness'].default_value),6),round(float(p.inputs['Metallic'].default_value),6))
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();v=[o.matrix_world@p.co for p in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(a),6) for a in v[k]) for k in t.vertices]
   rows.append((min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),signature(o.data.materials[t.material_index])))
 return sorted(rows)
def closed_check(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True)
 remaining=set(bm.verts);components=0
 while remaining:
  stack=[remaining.pop()];components+=1
  while stack:
   for edge in stack.pop().link_edges:
    for v in edge.verts:
     if v in remaining:remaining.remove(v);stack.append(v)
 bm.free();o.data.calc_loop_triangles();degenerate=sum(t.area<1e-12 for t in o.data.loop_triangles)
 triangles=[tuple(sorted(tuple(round(float(x),7) for x in o.data.vertices[i].co) for i in t.vertices)) for t in o.data.loop_triangles]
 duplicate=sum(c-1 for c in Counter(triangles).values() if c>1)
 assert nonmanifold==0 and components==1 and volume>0 and degenerate==duplicate==0,(nonmanifold,components,volume,degenerate,duplicate)
 assert abs(volume-1.2*1.2*.15)<1e-7,volume
 return {'nonmanifold_edges':nonmanifold,'closed_components':components,'signed_volume_m3':volume,'degenerate_triangles':degenerate,'duplicate_triangles':duplicate,'triangles':len(triangles)}
geometry=closed_check(part);expected=records([part]);triangles=geometry['triangles'];assert triangles==32
port_A=sorted((round(float(v.co.y),6),round(float(v.co.z),6)) for v in mesh.vertices if abs(v.co.x+.6)<1e-6)
port_B=sorted((round(float(v.co.x),6),round(float(v.co.z),6)) for v in mesh.vertices if abs(v.co.y-.6)<1e-6)
assert port_A==sorted((y,z) for y in [-.6,-.45,.6] for z in [0,.15])
assert port_B==sorted((x,z) for x in [-.6,.45,.6] for z in [0,.15])
bpy.ops.object.select_all(action='DESELECT');part.select_set(True);root.select_set(True);bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
native_config=assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Read the real exported bytes back before any studio/gray alteration.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];bpy.context.view_layer.update()
assert len(parts)==1 and records(parts)==expected,'Actual GLB oriented geometry/PBR mismatch'
roundtrip=closed_check(parts[0]);assert roundtrip['triangles']==triangles
glb_sha=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':2,'bounds_m':[1.2,1.2,.15],
 'bounds_min_m':[-.6,-.6,0],'bounds_max_m':[.6,.6,.15],'geometry':geometry,'actual_glb_roundtrip':roundtrip,
 'actual_glb_sha256':glb_sha,'actual_glb_geometry_and_pbr_exact_match':True,'port_A_yz_m':port_A,'port_B_xz_m':port_B,
 'palette':[{'name':name,'rgba':color,'roughness':rough,'metallic':0} for name,color,rough in PALETTE],
 'native_saved_render_config':native_config,'render_source':'Freshly imported actual model.glb',
 'scope':'Static visual turn with two compatible full-height ports. Original ramp retains its slope and 15 mm lip. No road/accessibility/load/motion certification.',
 'status':'producer checks only; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,triangles,glb_sha);sys.exit(0)
# Presentation-only objects never enter GLB or clean native source.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.35,.37,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
scene.view_settings.view_transform='AgX';focus=Vector((0,0,.075))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,power,location,size in [('Key',400,(-3,-4,5),4),('Fill',200,(4,-1,3),3),('Rim',260,(1,4,5),3)]:
 bpy.ops.object.light_add(type='AREA',location=location);light=bpy.context.object;light.name='Preview_'+name;light.data.energy=power;light.data.size=size;aim(light,location)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.86
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012));ground=bpy.context.object;ground.name='Preview_Ground_NotAsset'
g=bpy.data.materials.new('Preview_Slate');g.diffuse_color=(.18,.22,.23,1);g.use_nodes=True;g.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=g.diffuse_color;g.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9;ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384;scene.render.resolution_y=384
 for o in parts:
  for m in o.data.materials:
   p=m.node_tree.nodes['Principled BSDF'];v=.62 if abs(p.inputs['Roughness'].default_value-.84)<1e-5 else .45;p.inputs['Base Color'].default_value=(v,v,v,1)
views={'gray-front3q':(2.6,-3.6,2.8),'gray-back3q':(-2.6,3.6,2.8)} if gray else {'thumbnail':(2.6,-3.6,2.8),'qa-front':(0,-4,.075),'qa-side':(4,0,.075),'qa-back':(0,4,.075),'qa-top':(0,0,5),'qa-wireframe':(2.6,-3.6,2.8)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_configs={};render_seconds={}
def render(name,location):
 aim(cam,location);scene.render.filepath=str(OUT/(name+'.png'));render_configs[name]=assert_render();t=time.time();bpy.ops.render.render(write_still=True);render_seconds[name]=round(time.time()-t,3)
for name,location in views.items():
 if name=='qa-wireframe':
  wire=bpy.data.materials.new('Preview_ActualEdges');wire.diffuse_color=(.015,.02,.02,1)
  for o in parts:
   w=o.copy();w.data=o.data.copy();scene.collection.objects.link(w);w.name='Preview_ActualEdges_'+o.name;w.data.materials.clear();w.data.materials.append(wire)
   for p in w.data.polygons:p.material_index=0
   mod=w.modifiers.new('Preview_actual_mesh_edges','WIREFRAME');mod.thickness=.0015;mod.use_replace=True;mod.offset=1
 render(name,location)
if gray:
 black=bpy.data.materials.new('Preview_Silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for p in o.data.polygons:p.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard'
 scene.render.resolution_x=128;scene.render.resolution_y=128;render('silhouette-128',(2.6,-3.6,2.8))
if PREVIOUS_QA:
 assert PREVIOUS_QA['actual_glb_sha256']==glb_sha,'Prior thumbnail does not bind to current GLB'
 render_configs={'thumbnail':PREVIOUS_QA['render_configs']['thumbnail'],**render_configs}
 render_seconds={'thumbnail':PREVIOUS_QA['render_seconds']['thumbnail'],**render_seconds}
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/interface/runtime/schema gates pending'})
if not gray:
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name;files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'infrastructure','assetKind':'modular','theme':'transport','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,'bounds':{'x':1.2,'y':1.2,'z':.15,'unit':'m'},'triangles':triangles,'materials':2,'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa();print('ASSET_COMPLETE',ASSET,triangles,glb_sha)
