"""Original S02 static waterfall height transition, metres, Z up.
One continuous terrain solid plus one separate continuous closed water body.
Standalone: blender -b -t 4 --python-exit-code 1 --python generate.py
Flags after --: --geometry-only, --no-render, --gray-only, --preview-only, --extra-views.
Ports X=-1 water Z1.26 and X=+1 water Z.16, both existing narrow-stream sections.
Only actual old width-transition narrow ports are claimed: upstream Rz(pi)+(-2,0,1.10),
downstream +(2,0,0). High end needs raised surrounding terrain. Water cap bottoms
retreat 10mm; paired bottom V gap is 20mm, surface continuity only. No fluid/physics.
No cliff-side/bend/whole-scene snap. No external files, textures or models required.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-waterfall-transition-01';VERSION='1.0.0';TITLE='Stream Waterfall Height Transition'
DESCRIPTION=('Original S02 static stream waterfall transition with a real 1.10 m water-level drop over a 2 m X run. '
 'One continuous closed editable terrain solid surrounds a separate connected closed water body with an upstream lip, steep falling face and widened receiving basin. '
 'Both end sections match the existing stream-width transition narrow port: bank-foot spacing .60 m, raw water width .72 m; downstream X=+1 water Z=.16 m, upstream X=-1 water Z=1.26 m. '
 'Old upstream placement is rotation Z=180 degrees plus translation (-2,0,1.10) m; downstream translation (2,0,0) m. Terrain union caps match within 2e-6 m. '
 'Water bottom edges retreat .01 m, retaining the old 20 mm paired V gap: water-surface continuity only, no full water-volume claim. '
 'Legacy earth/water PBR values remain on visible port-adjacent surfaces; hidden terrain cap material partition is not identical to the old separate bed/bank caps. Upper-end installation requires equally raised supporting terrain. '
 'The escarpment is a height-scale reference only; no cliff-side, bend or whole-scene exact snap. No added decorative rocks or vegetation. '
 'Static visual module only; no animated flow, hydrology, collision, navigation, walkability, support/load or physics certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={'LegacyEarth':((.30,.36,.18,1),.83),'WetRock':((.27,.31,.28,1),.91),'CutBed':((.20,.17,.11,1),.95),'LegacyWater':((.075,.20,.24,1),.23),'FallingWater':((.145,.31,.335,1),.29),'PoolWater':((.10,.255,.28,1),.27)}
mats={}
for n,(c,r) in PALETTE.items():
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=r;mats[n]=m
root=bpy.data.objects.new('WaterfallHeightTransition',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['origin']='Downstream base centre Z=0; flow-axis X; high inlet X=-1'
root['static_visual_only']=True;root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def solid(name,rings,materials,role):
 n=len(rings[0]);verts=[v for r in rings for v in r];faces=[tuple(range(n-1,-1,-1)),tuple(range((len(rings)-1)*n,len(rings)*n))]
 for j in range(len(rings)-1):
  for k in range(n):q=(k+1)%n;faces.append((j*n+k,j*n+q,(j+1)*n+q,(j+1)*n+k))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o['component_role']=role
 for m in materials:me.materials.append(mats[m])
 for p in me.polygons:p.use_smooth=False
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();parts.append(o);return o
# x, bank-foot half-width, water surface z, foundation underside z,
# shoulder heights south/north, outer-bank crest heights south/north.
# End-adjacent spans are horizontal water and preserve exact old cross sections.
STATIONS=[(-1.,.30,1.26,1.10,1.39,1.39,1.74,1.74),
 (-.65,.30,1.26,0.,1.39,1.39,1.74,1.74),
 (-.36,.32,1.26,0.,1.42,1.47,1.73,1.80),
 (-.22,.32,1.22,0.,1.38,1.42,1.67,1.74),
 (.02,.39,.36,0.,.76,.87,1.35,1.48),
 (.24,.49,.16,0.,.41,.49,.94,1.11),
 (.62,.30,.16,0.,.29,.29,.64,.64),
 (1.,.30,.16,0.,.29,.29,.64,.64)]
rings=[]
for x,h,wz,bz,ss,sn,rs,rn in STATIONS:
 z=wz-.07
 rings.append([(x,-h-1.22,bz),(x,-h-1.22,z),(x,-h-1.2,z),(x,-h-1.2,rs),(x,-h-.38,ss),(x,-h,z+.06),(x,-h,z),(x,h,z),(x,h,z+.06),(x,h+.38,sn),(x,h+1.2,rn),(x,h+1.2,z),(x,h+1.22,z),(x,h+1.22,bz)])
terrain=solid('Waterfall_ContinuousTerrain',rings,['LegacyEarth','WetRock','CutBed'],'continuous_bed_and_banks')
for p in terrain.data.polygons:
 xs=[terrain.data.vertices[v].co.x for v in p.vertices];ys=[abs(terrain.data.vertices[v].co.y) for v in p.vertices]
 # Whole end-adjacent exposed spans retain legacy earth. Wet-rock follows real
 # interior fall-bank facets; foundation and cut faces remain dark earth.
 interior=min(xs)>-.651 and max(xs)<.621
 if p.normal.z<-.01:p.material_index=2
 elif interior and max(ys)<1.2:p.material_index=1
 elif abs(p.normal.y)>.95 and min(xs)>-.99 and max(xs)<.99:p.material_index=2
 else:p.material_index=0
water_rings=[]
for x,h,wz,bz,ss,sn,rs,rn in STATIONS:
 bx=x*.99 if abs(x)==1 else x
 water_rings.append([(bx,-h-.06,wz-.07),(bx,h+.06,wz-.07),(x,h+.06,wz),(x,-h-.06,wz)])
water=solid('WaterSurface_Runtime',water_rings,['LegacyWater','FallingWater','PoolWater'],'continuous_static_water')
for p in water.data.polygons:
 xs=[water.data.vertices[v].co.x for v in p.vertices]
 if min(xs)>=-.36001 and max(xs)<=.24001 and p.normal.z>.01:p.material_index=1 if min(xs)<.01999 else 2
water['upstream_water_z_m']=1.26;water['downstream_water_z_m']=.16;water['drop_m']=1.10
water['replace_material_independently']=True;water['surface_continuity_only_at_external_ports']=True
PORTS=[]
for j,label in [(0,'upstream'),(-1,'downstream')]:
 x,h,wz,bz,ss,sn,rs,rn=STATIONS[j]
 actual=sorted((round(v.co.y,6),round(v.co.z,6)) for v in terrain.data.vertices if abs(v.co.x-x)<1e-6)
 expected=sorted((round(y,6),round(z,6)) for xx,y,z in rings[j]);assert actual==expected
 actual_water=sorted((round(v.co.y,6),round(v.co.z,6)) for v in water.data.vertices if abs(v.co.x-x)<1e-6)
 assert actual_water==[(-.36,wz),(.36,wz)]
 PORTS.append({'name':label,'plane_x_m':x,'outward_tangent':[x,0,0],'terrain_union_cap_yz_m':actual,'water_top_yz_m':actual_water,'water_bottom_z_m':wz-.07,'water_bottom_cap_x_m':x*.99,'water_bottom_v_gap_with_old_m':.02,'bank_foot_spacing_m':.60,'raw_water_width_m':.72,'old_narrow_port_instance_translation_m':[-2,0,1.10] if j==0 else [2,0,0],'old_narrow_port_instance_rotation_z_rad':math.pi if j==0 else 0})
root['port_contract']=json.dumps(PORTS,sort_keys=True)
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
geometry_fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'Solid-only PBR expected'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def oriented_pbr_fingerprint(objects):
 records=[]
 for o in objects:
  o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(q),6) for q in vv[i]) for i in t.vertices]
   material_record=pbr(o.data.materials[t.material_index])
   records.append((min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),material_record))
 return hashlib.sha256(json.dumps(sorted(records),separators=(',',':')).encode()).hexdigest()
authored_oriented_pbr=oriented_pbr_fingerprint(parts)
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'origin':'Downstream base centre Z=0; upstream X=-1 is raised 1.10 m','components':checks,'ports':PORTS,'actual_water_drop_m':1.10,'station_sections':STATIONS,'legacy_compatibility_scope':'Only existing width-transition narrow port at supplied two transforms; terrain cap union and water surface continuity within 2e-6 m. No whole fluid volume, bend, scene base or cliff-side snap. Raised inlet needs corresponding raised terrain.','geometry_fingerprint_sha256':geometry_fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
# Render and runtime checks use a fresh import of the exact exported GLB.
# The editable native file above remains the authored component scene, without studio objects.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];bpy.context.view_layer.update()
actual_oriented_pbr=oriented_pbr_fingerprint(parts);assert actual_oriented_pbr==authored_oriented_pbr,('GLB oriented triangles or PBR changed',authored_oriented_pbr,actual_oriented_pbr)
mats={m.name:m for o in parts for m in o.data.materials};assert len(mats)==len(PALETTE)
qa['actual_glb_sha256']=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa['actual_glb_roundtrip']={'fresh_import':True,'oriented_triangles_and_full_solid_pbr_sha256':actual_oriented_pbr,'full_principled_pbr_and_double_sided':True,'textures_rejected':True,'matches_authored':True,'mesh_count':len(parts),'render_source':'fresh exact exported model.glb import'}
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Presentation added only after clean native/runtime have been saved.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX';focus=Vector((0,0,.88))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-5,-7,10),1400,7),('Fill',(7,-2,5),650,6),('Rim',(2,7,8),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=4.6
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview_ground_not_asset';g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.22,.245,.24,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(5,-7,5),'gray-back3q':(-5,7,5)} if gray else {'thumbnail':(5,-7,5),'qa-front':(0,-7,.88),'qa-side':(7,0,.88),'qa-top':(0,0,8),'qa-back':(0,7,.88),'qa-wireframe':(5,-7,5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(n,p):
 cam.data.ortho_scale=2.65 if n in ['qa-front','qa-back','silhouette-128-front'] else (3.8 if n in ['qa-side','silhouette-128-side'] else 4.3)
 aim(cam,p);scene.render.filepath=str(OUT/(n+'.png'));render_configs[n]=assert_render();t=time.time();bpy.ops.render.render(write_still=True);render_seconds[n]=round(time.time()-t,3)
for n,p in views.items():
 if n=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for poly in dup.data.polygons:poly.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.004;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1;scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(0,-7,.88)),('silhouette-128-side',(7,0,.88))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n;files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
