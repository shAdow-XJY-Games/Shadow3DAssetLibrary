"""Original S01 wide shallow open bookcase, metres, Z up, front -Y.
Standalone: blender -b -t 4 --python-exit-code 1 --python generate.py
--no-render: geometry/native only; --gray-only: early form evidence;
--preview-only: PBR thumbnail; --extra-views: five other formal images.
No external models, textures, fonts, packages or book props. Static visual furniture.
"""
import bpy, bmesh, json, hashlib, sys, time
from pathlib import Path
from collections import Counter
from mathutils import Vector

START=time.time(); OUT=Path(__file__).resolve().parent
ASSET='interior-open-bookcase-01'; VERSION='1.0.0'
TITLE='S01 Wide Open Bookcase'
DESCRIPTION=('Original S01 freestanding wide shallow bookcase with four open horizontal book rows. '
 'Overall width 1.12 m, depth 0.34 m and height 1.80 m; metres, front -Y and ground-contact origin Z=0. '
 'Three fixed full-width intermediate shelves and the lower deck provide four long book surfaces, framed by warm-ivory side walls and crown, '
 'with a recessed seafoam backboard, two rear battens and a broad inset floor plinth. '
 'Each shelf has a nominal 0.98 m wide by 0.27 m deep flat placement rectangle; clear row heights exceed 0.35 m. '
 'Named closed components remain separately editable. Empty bookcase only, no books or props are included. '
 'Static visual furniture; no adjustable shelving, moving parts, book-fit validation, installation, load or tip-resistance certification.')
PREVIOUS_QA=json.loads((OUT/'qa-report.json').read_text()) if '--extra-views' in sys.argv and (OUT/'qa-report.json').exists() else None
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for material in list(bpy.data.materials): bpy.data.materials.remove(material)
scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
scene.render.engine='CYCLES'; scene.cycles.samples=128; scene.cycles.use_adaptive_sampling=False; scene.cycles.use_denoising=False
scene.cycles.seed=0
for layer in scene.view_layers: layer.cycles.use_denoising=False
scene.use_nodes=False; scene.render.use_compositing=False; scene.render.threads_mode='FIXED'; scene.render.threads=4
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
  'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
  'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config(); assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,
  'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={
 'Warm ivory frame':((.86,.75,.52,1),.70,0),
 'Honey maple shelves':((.48,.255,.105,1),.73,0),
 'Seafoam inset backing':((.19,.40,.35,1),.76,0),
}
mats={}
for name,(color,roughness,metallic) in PALETTE.items():
 m=bpy.data.materials.new(name); m.diffuse_color=color; m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=color; p.inputs['Roughness'].default_value=roughness; p.inputs['Metallic'].default_value=metallic; mats[name]=m
root=bpy.data.objects.new('OpenBookcase_Static',None); scene.collection.objects.link(root)
root['asset_id']=ASSET; root['origin_contract']='Ground datum at native origin, metres, Z up, front -Y; not bounds-centred'
root['static_empty_bookcase']=True; root['nominal_width_depth_height_m']=[1.12,.34,1.80]
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def box(name,lo,hi,material,bevel=.003,segments=1,role='fixed casework'):
 verts=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
 me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
 o=bpy.data.objects.new(name,me); scene.collection.objects.link(o); o.parent=root; o.data.materials.append(mats[material]); o['role']=role
 bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
 bpy.context.view_layer.objects.active=o
 if bevel:
  mod=o.modifiers.new('Small modeled bevel','BEVEL'); mod.width=min(bevel,.45*min(hi[i]-lo[i] for i in range(3))); mod.segments=segments; bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=o.modifiers.new('Explicit runtime triangles','TRIANGULATE'); bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o); return o
# A broad shallow horizontal-row bookcase, not a narrow cubby or deep pantry case.
# Slight overlap at all intended joints avoids unsupported/floating beveled edges.
box('Floor_plinth',(-.49,-.125,0),(.49,.13,.132),'Seafoam inset backing',.008,1,'ground support')
box('Lower_book_deck',(-.55,-.165,.108),(.55,.165,.166),'Honey maple shelves',.009,1,'bottom book surface and base cap')
for side,x0,x1 in [('L',-.535,-.495),('R',.495,.535)]:
 box('Side_wall_'+side,(x0,-.148,.122),(x1,.148,1.768),'Warm ivory frame',.005,1,'continuous side support')
box('Crown_cap',(-.56,-.17,1.755),(.56,.17,1.80),'Warm ivory frame',.010,1,'upper frame cap')
# Back panel is genuinely inset behind the book surfaces; closed 24 mm thickness.
box('Inset_backboard',(-.515,.126,.145),(.515,.150,1.770),'Seafoam inset backing',.003,1,'continuous closed rear panel')
for i,z0 in enumerate([.530,.930,1.330],1):
 box('Fixed_book_shelf_%02d'%i,(-.512,-.151,z0),(.512,.135,z0+.032),'Honey maple shelves',.004,1,'fixed horizontal book surface')
# Two restrained rear battens show board hierarchy from the back, without new mechanisms.
for side,x in [('L',-.31),('R',.31)]:
 box('Rear_batten_'+side,(x-.024,.145,.156),(x+.024,.164,1.760),'Warm ivory frame',.003,1,'fixed backboard batten')
bpy.context.view_layer.update()
def material_signature(m):
 p=m.node_tree.nodes['Principled BSDF']; return tuple(round(float(v),6) for v in p.inputs['Base Color'].default_value)+(round(float(p.inputs['Roughness'].default_value),6),round(float(p.inputs['Metallic'].default_value),6))
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles(); verts=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(a),6) for a in verts[k]) for k in t.vertices]
   rows.append((o.name,min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),material_signature(o.data.materials[t.material_index])))
 return sorted(rows)
def basic_geometry(objects):
 rows=[]
 for o in objects:
  bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
  nm=sum(not e.is_manifold for e in bm.edges); vol=bm.calc_volume(signed=True); bm.free(); o.data.calc_loop_triangles()
  degenerate=sum(t.area<1e-12 for t in o.data.loop_triangles)
  faces=[tuple(sorted(tuple(round(float(x),7) for x in o.data.vertices[i].co) for i in t.vertices)) for t in o.data.loop_triangles]
  duplicate=sum(c-1 for c in Counter(faces).values() if c>1)
  assert nm==0 and vol>0 and degenerate==duplicate==0,(o.name,nm,vol,degenerate,duplicate)
  rows.append({'name':o.name,'triangles':len(faces),'nonmanifold_edges':nm,'positive_volume_m3':vol,'degenerate_triangles':degenerate,'duplicate_triangles':duplicate})
 return rows
geometry=basic_geometry(parts); expected=records(parts); triangles=sum(r['triangles'] for r in geometry)
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
lo=[min(v[i] for v in verts) for i in range(3)]; hi=[max(v[i] for v in verts) for i in range(3)]; bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert all(abs(a-b)<1e-5 for a,b in zip(bounds,[1.12,.34,1.80])),bounds
assert abs(lo[2])<1e-7
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]: o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
native_config=assert_render(); bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Formal and early views always use a fresh import of the exact GLB bytes.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb')); parts=[o for o in scene.objects if o.type=='MESH']; bpy.context.view_layer.update()
assert records(parts)==expected,'Actual GLB oriented geometry/PBR does not match native source'
roundtrip=basic_geometry(parts); glb_sha=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(PALETTE),'mesh_objects':len(parts),
 'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'geometry':geometry,'actual_glb_roundtrip':roundtrip,
 'actual_glb_sha256':glb_sha,'actual_glb_geometry_and_pbr_exact_match':True,
 'native_saved_render_config':native_config,'render_source':'Freshly imported actual model.glb',
 'palette':[{'name':n,'rgba':v[0],'roughness':v[1],'metallic':v[2]} for n,v in PALETTE.items()],
 'placement':'Standalone empty wide shallow bookcase; front -Y, ground-contact origin Z=0.',
 'scope':'Static visual furniture; no adjustable shelves, book-fit validation, load or tip-resistance certification.',
 'status':'producer geometry checks only; independent gates pending'}
# Required static interfaces only, measured on actual imported geometry.
from mathutils.bvhtree import BVHTree
cache={}
for o in parts:
 vv=[o.matrix_world@v.co for v in o.data.vertices]; o.data.calc_loop_triangles()
 cache[o.name]=(BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True),vv)
def inside(o,xyz):
 tree=cache[o][0]; p=Vector(xyz); direction=Vector((1,.371,.529)).normalized(); hits=0; origin=p.copy()
 for _ in range(32):
  loc,n,idx,d=tree.ray_cast(origin,direction,100)
  if loc is None: break
  hits+=1; origin=loc+direction*1e-5
 else: raise AssertionError('Uncertain interior test')
 return hits%2==1,tree.find_nearest(p)[3]
interfaces=[]
def anchor(a,b,p):
 ia,da=inside(a,p); ib,db=inside(b,p)
 assert ia and ib and min(da,db)>.0004,(a,b,p,ia,ib,da,db)
 interfaces.append({'a':a,'b':b,'interior_point_m':p,'minimum_surface_clearance_m':min(da,db)})
for side,x in [('L',-.505),('R',.505)]:
 for i,z0 in enumerate([.530,.930,1.330],1): anchor('Fixed_book_shelf_%02d'%i,'Side_wall_'+side,[x,0,z0+.016])
 anchor('Lower_book_deck','Side_wall_'+side,[x,0,.145])
 anchor('Crown_cap','Side_wall_'+side,[x,0,1.762])
 anchor('Inset_backboard','Side_wall_'+side,[x,.137,.75])
anchor('Floor_plinth','Lower_book_deck',[0,0,.120])
anchor('Inset_backboard','Lower_book_deck',[0,.137,.156])
anchor('Inset_backboard','Crown_cap',[0,.137,1.762])
for side,x in [('L',-.31),('R',.31)]: anchor('Rear_batten_'+side,'Inset_backboard',[x,.148,.8])
plinth=next(o for o in parts if o.name=='Floor_plinth'); vv=cache[plinth.name][1]
ground_area=sum(t.area for t in plinth.data.loop_triangles if all(abs(vv[k].z)<1e-6 for k in t.vertices))
assert ground_area>.20,ground_area
clear_rows=[{'support_z_m':a,'ceiling_z_m':b,'minimum_clear_height_m':round(b-a,6),'flat_placement_x_m':[-.49,.49],'flat_placement_y_m':[-.145,.125]} for a,b in [(.166,.530),(.562,.930),(.962,1.330),(1.362,1.755)]]
qa['necessary_static_interfaces']={'scope':'Actual GLB finite interior joint checks, broad floor contact and nominal open placement rectangles; no load or tip-resistance claim.','interfaces':interfaces,'floor_planar_contact_area_m2':ground_area,'rows':clear_rows}
def save_qa(): (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def save_metadata():
 if not (OUT/'thumbnail.png').exists(): return
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name; files[role]={'path':f'assets/interior/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric','title':TITLE,
  'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 save_metadata(); print('GEOMETRY_READY',ASSET,triangles,glb_sha); sys.exit(0)
# Studio objects and wire overlays are presentation-only and absent from native source.
scene.render.resolution_x=640; scene.render.resolution_y=640; scene.render.resolution_percentage=100
scene.world.use_nodes=True; scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.35,.37,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
scene.view_settings.view_transform='AgX'; focus=Vector((0,0,.90))
def aim(o,p): o.location=p; o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,power,location,size in [('Key',480,(-3,-4,5),4),('Fill',210,(4,-1,3),3),('Rim',310,(1,4,5),3)]:
 bpy.ops.object.light_add(type='AREA',location=location); light=bpy.context.object; light.name='Preview_'+name; light.data.energy=power; light.data.size=size; aim(light,location)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Preview_Camera'; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=2.30
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012)); ground=bpy.context.object; ground.name='Preview_Ground_NotAsset'
g=bpy.data.materials.new('Preview_Slate'); g.diffuse_color=(.18,.22,.23,1); g.use_nodes=True; g.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=g.diffuse_color; g.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9; ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384; scene.render.resolution_y=384
 for o in parts:
  for m in o.data.materials:
   p=m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value=(.5,.5,.5,1); p.inputs['Roughness'].default_value=.65; p.inputs['Metallic'].default_value=0
views={'gray-front3q':(3,-5,3),'gray-back3q':(-3,5,2.8)} if gray else {'thumbnail':(3,-5,3),'qa-front':(0,-5,.9),'qa-side':(5,0,.9),'qa-top':(0,0,6),'qa-back':(0,5,.9),'qa-wireframe':(3,-5,3)}
if '--preview-only' in sys.argv: views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv: views.pop('thumbnail',None)
for arg in sys.argv:
 if arg.startswith('--views='):
  requested=arg.split('=',1)[1].split(','); assert all(n in views for n in requested),requested; views={n:views[n] for n in requested}
render_configs={}; render_seconds={}
def render(name,location):
 aim(cam,location); scene.render.filepath=str(OUT/(name+'.png')); render_configs[name]=assert_render(); t=time.time(); bpy.ops.render.render(write_still=True); render_seconds[name]=round(time.time()-t,3)
for name,location in views.items():
 if name=='qa-wireframe':
  wire=bpy.data.materials.new('Preview_ActualMeshEdges'); wire.diffuse_color=(.008,.014,.012,1); wire.use_nodes=True; wire.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=wire.diffuse_color
  for o in parts:
   w=o.copy(); w.data=o.data.copy(); scene.collection.objects.link(w); w.name='Preview_Wire_'+o.name; w.data.materials.clear(); w.data.materials.append(wire)
   for p in w.data.polygons: p.material_index=0
   mod=w.modifiers.new('Actual runtime triangle edges','WIREFRAME'); mod.thickness=.0009; mod.use_replace=True; mod.offset=1
 render(name,location)
if gray:
 black=bpy.data.materials.new('Preview_Silhouette'); black.use_nodes=True; nodes=black.node_tree.nodes; nodes.clear(); output=nodes.new('ShaderNodeOutputMaterial'); em=nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(0,0,0,1); black.node_tree.links.new(em.outputs[0],output.inputs['Surface'])
 for o in parts:
  o.data.materials.clear(); o.data.materials.append(black)
  for p in o.data.polygons: p.material_index=0
 ground.hide_render=True; scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1; scene.view_settings.view_transform='Standard'
 scene.render.resolution_x=128; scene.render.resolution_y=128
 render('silhouette-128-front',(0,-5,.9)); render('silhouette-128-side',(5,0,.9))
if PREVIOUS_QA:
 assert PREVIOUS_QA['actual_glb_sha256']==glb_sha,'Prior PBR thumbnail is bound to a different GLB'
 render_configs={'thumbnail':PREVIOUS_QA['render_configs']['thumbnail'],**render_configs}; render_seconds={'thumbnail':PREVIOUS_QA['render_seconds']['thumbnail'],**render_seconds}
qa.update({'render_configs':render_configs,'render_seconds':render_seconds,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent final gates pending'})
if not gray: save_metadata()
save_qa(); print('ASSET_COMPLETE',ASSET,triangles,glb_sha)
