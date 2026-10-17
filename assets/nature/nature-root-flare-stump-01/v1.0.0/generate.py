"""Original S02 Root-Flared Broken Stump. Metres, Z up, static visual prop.
Standalone, no external geometry or textures. One closed continuous authored shell.
Flags: --geometry-only / --gray-only / --preview-only / --extra-views.
Every render and native save: Cycles 128, no adaptive or denoising, FIXED 4 threads.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from collections import Counter
from mathutils import Vector

START=time.time(); OUT=Path(__file__).resolve().parent
ASSET='nature-root-flare-stump-01'; VERSION='1.0.0'; TITLE='Root-Flared Broken Stump'
DESCRIPTION=('Original S02 hard-edge faceted standing tree stump. Five unequal buttress root flares flow into an offset tapered trunk in one continuous closed mesh. '
 'An irregular broken bark rim and angled exposed sapwood surround a solid eccentric heartwood section, with two subtle annual bands and a modeled radial V fissure. '
 'Metres, trunk-centre ground origin Z=0, named editable continuous mesh and solid untextured PBR. Original geometry, not a stripped anvil base or a rotated fallen log. '
 'Static natural ground dressing only; no decorative axe, mushrooms, collision mesh, physics, wind rig, animation or species-accuracy guarantee.')
PREVIOUS_QA=json.loads((OUT/'qa-report.json').read_text()) if '--extra-views' in sys.argv and (OUT/'qa-report.json').exists() else None
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
scene.render.engine='CYCLES'; scene.cycles.samples=128; scene.cycles.use_adaptive_sampling=False; scene.cycles.use_denoising=False; scene.cycles.seed=0
for layer in scene.view_layers: layer.cycles.use_denoising=False
scene.use_nodes=False; scene.render.use_compositing=False; scene.render.threads_mode='FIXED'; scene.render.threads=4
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
  'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
  'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config(); assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={
 'Bark_Broad':(.205,.105,.049,1), 'Bark_Ridge':(.265,.146,.073,1), 'Bark_Furrow':(.145,.067,.032,1),
 'Sapwood_Break':(.59,.383,.183,1), 'Heartwood':(.475,.282,.125,1), 'Annual_Band':(.385,.212,.088,1)}
mats={}
for n,c in PALETTE.items():
 m=bpy.data.materials.new(n); m.diffuse_color=c; m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=c; p.inputs['Roughness'].default_value=.9; mats[n]=m
root=bpy.data.objects.new('RootFlareStump_Static',None); scene.collection.objects.link(root)
root['asset_id']=ASSET; root['origin_contract']='Standing trunk basal axis at Z=0; asymmetric root footprint, metres; GLB Y up'
root['static_visual_only']=True; root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)

# One coherent radial shell. No cylinders, imported old props, overlapping root solids or detached decorative details.
# Irregular sample spacing preserves a narrow V fissure in the surface without a painted-on black stripe.
ANGLES=[-180,-168,-155,-141,-128,-116,-104,-92,-81,-68,-55,-43,-31,-19,-6,8,22,35,48,60,73,87,100,112,124,137,150,164,176]
# Fissure runs along -128 degrees; shoulders at -131/-125 degrees keep it narrow.
ANGLES=sorted(set(ANGLES+[-131,-125])); N=len(ANGLES)
ROOTS=[(-155,.41,20),(-81,.31,18),(-19,.48,20),(60,.29,22),(137,.38,20)]
def delta(a,b):return (a-b+180)%360-180
def root_lobe(a):return max(h*max(0,math.cos(math.radians(delta(a,b)*90/w)))**2 if abs(delta(a,b))<w else 0 for b,h,w in ROOTS)
def scalar_radius(a):
 t=math.radians(a); return .377*(1+.052*math.sin(t*3+.8)+.027*math.cos(t*5-1.1))
def broken_height(a):
 # One high split shoulder on the back, a low front-side break and broad irregular lip elsewhere.
 return .695+.023*math.sin(math.radians(a*2+28))+.016*math.cos(math.radians(a*5-50))+(.142 if a==124 else .075 if a in [112,137] else .035 if a==100 else 0)-(.067 if a==-128 else .018 if a in [-131,-125] else 0)
def xy(a,r,cx=0,cy=0):
 t=math.radians(a); return cx+r*math.cos(t),cy+r*.88*math.sin(t)
verts=[]; faces=[]; labels=[]; loop_ids=[]
def loop(coords):
 ids=[]
 for co in coords:ids.append(len(verts)); verts.append(tuple(co))
 loop_ids.append(ids); return ids
def face(indices,label):faces.append(tuple(indices)); labels.append(label)
def bridge(a,b,label_function):
 for i in range(N):j=(i+1)%N; face((a[i],a[j],b[j],b[i]),label_function(i))
def bark_label(i):
 a=(ANGLES[i]+ANGLES[(i+1)%N])/2 if i<N-1 else 178
 # Broad coherent stripes follow selected root ridges. No random per-face color noise.
 if any(abs(delta(a,b))<10 for b in [-155,-19,137]):return 'Bark_Ridge'
 if any(abs(delta(a,b))<7 for b in [-116,35,100]):return 'Bark_Furrow'
 return 'Bark_Broad'
for level in range(5):
 coords=[]
 for a in ANGLES:
  r=scalar_radius(a); lobe=root_lobe(a)
  if level==0: r=r+.055+lobe; z=0; cx=cy=0
  elif level==1: r=r+.026+lobe*.87; z=.035+.038*(1-min(lobe/.40,1)); cx=.006; cy=.004
  elif level==2: r=r+.043+lobe*.26; z=.230+.025*math.cos(math.radians(a+25)); cx=.025; cy=.005
  elif level==3: r=r+lobe*.055; z=.465+.019*math.sin(math.radians(a*2)); cx=.060; cy=-.006
  else: r=r*.94; z=broken_height(a); cx=.082; cy=-.018
  x,y=xy(a,r,cx,cy); coords.append((x,y,z))
 loop(coords)
bottom_center=len(verts); verts.append((0,0,0))
for i in range(N):face((bottom_center,loop_ids[0][(i+1)%N],loop_ids[0][i]),'Bark_Broad')
for j in range(4):bridge(loop_ids[j],loop_ids[j+1],bark_label)
# Bark thickness is actual shell surface, then broad sloping fracture facets descend to solid end grain.
lip=[]
for a in ANGLES:
 x,y=xy(a,scalar_radius(a)*.94-.026,.082,-.018); lip.append((x,y,broken_height(a)-.012))
inner_lip=loop(lip); bridge(loop_ids[4],inner_lip,lambda i:'Bark_Furrow')
face_boundary=[]
for a in ANGLES:
 x,y=xy(a,scalar_radius(a)*.78,.082,-.018)
 z=.656+.040*(x-.082)-(.052 if a==-128 else 0)
 face_boundary.append((x,y,z))
endgrain=loop(face_boundary); bridge(inner_lip,endgrain,lambda i:'Sapwood_Break')
# Eccentric pith differs from both base and top axes. Rings are modeled partitions of one solid surface, never floating disks.
pith=Vector((.020,.023,.655)); previous=endgrain
for scale,region in [(.76,'Heartwood'),(.714,'Annual_Band'),(.438,'Heartwood'),(.393,'Annual_Band'),(.13,'Heartwood')]:
 coords=[]
 for i,a in enumerate(ANGLES):
  p=pith.lerp(Vector(face_boundary[i]),scale); p.z=.656+.040*(p.x-.082)
  if a==-128:p.z-=.052*max(0,(scale-.31)/.69)
  coords.append(tuple(p))
 current=loop(coords); bridge(previous,current,lambda i,region=region:region); previous=current
pith.z=.656+.040*(pith.x-.082); centre=len(verts); verts.append(tuple(pith))
for i in range(N):face((previous[i],previous[(i+1)%N],centre),'Heartwood')
me=bpy.data.meshes.new('Stump_ContinuousRootToBreak'); me.from_pydata(verts,[],faces); me.update()
obj=bpy.data.objects.new('Stump_ContinuousRootToBreak',me); scene.collection.objects.link(obj); obj.parent=root
for m in mats.values():me.materials.append(m)
for p,label in zip(me.polygons,labels):p.material_index=list(PALETTE).index(label); p.use_smooth=False
bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
# Pin triangulation before export so regenerated native and GLB surfaces are compared exactly.
bpy.context.view_layer.objects.active=obj; obj.select_set(True)
mod=obj.modifiers.new('Explicit runtime triangles','TRIANGULATE'); bpy.ops.object.modifier_apply(modifier=mod.name)
obj['component_role']='continuous grounded root flares, tapering trunk and solid fractured end grain'
obj['root_count']=5; obj['pith_position_m']=list(pith); obj['root_plan']=json.dumps(ROOTS)
parts=[obj]; bpy.context.view_layer.update()

def records(objects):
 out=[]
 for o in objects:
  o.data.calc_loop_triangles(); vv=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(a),6) for a in vv[i]) for i in t.vertices]
   p=o.data.materials[t.material_index].node_tree.nodes['Principled BSDF']
   sig=tuple(round(float(a),6) for a in p.inputs['Base Color'].default_value)+(round(float(p.inputs['Roughness'].default_value),6),round(float(p.inputs['Metallic'].default_value),6))
   out.append((min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),sig))
 return sorted(out)
def topology(o):
 bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bad=sum(not e.is_manifold for e in bm.edges); loose=sum(not v.link_edges for v in bm.verts); vol=bm.calc_volume(signed=True)
 remaining=set(bm.verts); components=0
 while remaining:
  queue=[remaining.pop()]; components+=1
  while queue:
   for e in queue.pop().link_edges:
    for v in e.verts:
     if v in remaining:remaining.remove(v); queue.append(v)
 bm.free(); o.data.calc_loop_triangles(); deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 tris=[tuple(sorted(tuple(round(float(a),7) for a in o.data.vertices[i].co) for i in t.vertices)) for t in o.data.loop_triangles]
 dup=sum(c-1 for c in Counter(tris).values() if c>1)
 assert bad==loose==deg==dup==0 and vol>1e-8 and components==1,(bad,loose,deg,dup,vol,components)
 return {'nonmanifold_edges':bad,'loose_vertices':loose,'degenerate_triangles':deg,'duplicate_triangles':dup,'signed_volume_m3':vol,'connected_components':components,'triangles':len(tris)}
geo=topology(obj); expected=records(parts); fingerprint=hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()
vv=[v.co for v in obj.data.vertices]; lo=[min(v[i] for v in vv) for i in range(3)]; hi=[max(v[i] for v in vv) for i in range(3)]; bounds=[round(hi[i]-lo[i],6) for i in range(3)]
ground=[p for p in obj.data.polygons if all(abs(obj.data.vertices[i].co.z)<1e-7 for i in p.vertices)]; ground_area=sum(p.area for p in ground)
assert abs(lo[2])<1e-7 and ground_area>.3 and .65<bounds[2]<.95 and 400<geo['triangles']<2000,(lo,ground_area,bounds,geo)
assert all(abs(v-1)<1e-8 for v in obj.scale) and obj.location.length==0 and obj.rotation_euler.to_quaternion().angle==0
bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); root.select_set(True); bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
native_config=assert_render(); bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Clean original native above remains editable. Preview always uses a fresh import of the exact GLB.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb')); parts=[o for o in scene.objects if o.type=='MESH']; bpy.context.view_layer.update()
assert len(parts)==1; assert records(parts)==expected,'GLB oriented triangles/PBR differ from authored source'
roundtrip=topology(parts[0]); mats={m.name:m for o in parts for m in o.data.materials}; assert len(mats)==len(PALETTE)
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':geo['triangles'],'mesh_objects':1,'materials':len(mats),
 'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'geometry':geo,'actual_glb_roundtrip':roundtrip,
 'geometry_fingerprint_sha256':fingerprint,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'actual_glb_geometry_and_pbr_exact_match':True,'native_saved_render_config':native_config,'render_source':'fresh exact exported model.glb import',
 'ground_contact':{'minimum_z_m':lo[2],'finite_flat_area_m2':ground_area,'triangles':len(ground)},
 'root_flare_plan':[{'bearing_deg':b,'radial_extension_m':h,'half_width_deg':w} for b,h,w in ROOTS],
 'topology_scope':'One continuous closed shell carries every root ridge, bark wall, broken rim and endgrain surface; no attached components need mechanical support proof.',
 'cross_section':{'pith_m':list(pith),'top_axis_m':[.082,-.018],'basal_axis_m':[0,0],'fissure_bearing_deg':-128,'fissure_depth_at_outer_endgrain_m':.052,'annual_bands':2},
 'scope':'Static nature dressing only, no animation, physics, collision or species-accuracy claim.','status':'producer geometry checked; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def write_metadata():
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n
  if not p.exists():return
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 m={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':geo['triangles'],'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 write_metadata(); print('GEOMETRY_READY',ASSET,geo['triangles'],bounds); sys.exit(0)
scene.render.resolution_x=640; scene.render.resolution_y=640; scene.render.resolution_percentage=100
scene.world.use_nodes=True; scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX'; focus=Vector((0,0,.37))
def aim(o,p):o.location=p; o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-3,-4,5),420,4),('Fill',(4,-1,3),170,3),('Rim',(1,4,4),280,3)]:
 bpy.ops.object.light_add(type='AREA',location=p); o=bpy.context.object; o.name='Preview_'+n; o.data.energy=e; o.data.shape='DISK'; o.data.size=s; aim(o,p)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Preview_Camera'; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=1.98
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002)); ground=bpy.context.object; ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate'); g.diffuse_color=(.22,.245,.24,1); ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384; scene.render.resolution_y=384
 for m in mats.values():m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(3,-4,3.4),'gray-back3q':(-3,4,3.4)} if gray else {'thumbnail':(3,-4,3.4),'qa-front':(0,-4,.37),'qa-side':(4,0,.37),'qa-top':(0,0,5),'qa-back':(0,4,.37),'qa-wireframe':(3,-4,3.4)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={}; render_configs={}
def render(n,p):
 aim(cam,p); scene.render.filepath=str(OUT/(n+'.png')); render_configs[n]=assert_render(); t=time.time(); bpy.ops.render.render(write_still=True); render_seconds[n]=round(time.time()-t,3)
for n,p in views.items():
 if n=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire'); wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy(); dup.data=o.data.copy(); scene.collection.objects.link(dup); dup.name='Preview_wire_'+o.name; dup.data.materials.clear(); dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME'); w.thickness=.0012; w.use_replace=True; w.use_even_offset=False; w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette'); black.use_nodes=True; nodes=black.node_tree.nodes; nodes.clear(); out=nodes.new('ShaderNodeOutputMaterial'); em=nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(0,0,0,1); black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear(); o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True; scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard'; scene.render.resolution_x=128; scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(0,-4,.37)),('silhouette-128-side',(4,0,.37))]:render(n,p)
if PREVIOUS_QA and PREVIOUS_QA.get('actual_glb_sha256')==qa['actual_glb_sha256']:
 qa['render_seconds']=dict(PREVIOUS_QA.get('render_seconds',{}),**render_seconds); qa['render_configs']=dict(PREVIOUS_QA.get('render_configs',{}),**render_configs)
else:qa.update({'render_seconds':render_seconds,'render_configs':render_configs})
qa['elapsed_seconds']=round(time.time()-START,3)
if not gray:write_metadata()
save_qa(); print('ASSET_COMPLETE',ASSET,geo['triangles'],bounds)
