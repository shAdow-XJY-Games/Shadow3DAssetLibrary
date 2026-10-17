"""Original S01 compact two-seat living-room sofa, metres, Z up, front -Y.
Standalone: blender -b -t 4 --python-exit-code 1 --python generate.py
--no-render: geometry/native only; --gray-only: early form evidence;
--preview-only: PBR thumbnail; --extra-views: five other formal images.
No external models, textures, fonts or packages. Static visual furniture.
"""
import bpy, bmesh, json, hashlib, sys, time
from pathlib import Path
from collections import Counter
from mathutils import Vector

START=time.time(); OUT=Path(__file__).resolve().parent
ASSET='interior-two-seat-sofa-01'; VERSION='1.0.0'
TITLE='S01 Compact Two-Seat Sofa'
DESCRIPTION=('Original S01 standalone two-seat living-room sofa, 1.68 m wide, 0.88 m deep and 0.92 m high. '
 'Metres, front -Y and ground-contact origin Z=0. Two broad seafoam seat pads and two rear-leaning back cushions have separate modeled seams. '
 'Low upholstered arms enclose the seats; an inset dark-seafoam deck and rear shell connect to a narrow honey-maple base rail and four short tapered feet. '
 'The stepped front cushion, deck, rail and feet remain legible. Named closed components are independently editable in native source and GLB. '
 'One complete independent sofa, not a sectional snap system. Static visual furniture only; no animation, upholstery simulation, ergonomic, installation, load, tip-resistance or cross-asset compatibility certification.')
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
 'Seafoam upholstery':((.19,.40,.35,1),.83,0),
 'Deep seafoam foundation':((.115,.265,.235,1),.80,0),
 'Honey maple support':((.48,.255,.105,1),.73,0),
}
mats={}
for name,(color,roughness,metallic) in PALETTE.items():
 m=bpy.data.materials.new(name); m.diffuse_color=color; m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=color; p.inputs['Roughness'].default_value=roughness; p.inputs['Metallic'].default_value=metallic; mats[name]=m
root=bpy.data.objects.new('TwoSeatSofa_Static',None); scene.collection.objects.link(root)
root['asset_id']=ASSET; root['origin_contract']='Ground datum at native origin, metres, Z up, front -Y; not bounds-centred'
root['standalone_sofa_no_snap_contract']=True; root['nominal_width_depth_height_m']=[1.68,.88,.92]
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def box(name,lo,hi,material,bevel=.003,segments=1,role='fixed sofa component'):
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
# Original sofa assembly. Broad separate cushions, low enclosing arms and short
# feet make a distinct lounge silhouette; no geometry comes from the booth or bench.
def sloped_box(name,lo,hi,material,lean,bevel=.035,segments=2,role='rear-leaning back'):
 o=box(name,lo,hi,material,bevel,segments,role)
 for v in o.data.vertices: v.co.y+=lean*(v.co.z-lo[2])/(hi[2]-lo[2])
 o.data.update(); return o

def tapered_foot(name,x,y):
 o=box(name,(x-.050,y-.050,0),(x+.050,y+.050,.180),'Honey maple support',.006,1,'short tapered ground support')
 # Reduce only lower X/Y sections to retain a finite, flat floor patch.
 for v in o.data.vertices:
  ratio=.75+.25*v.co.z/.180
  v.co.x=x+(v.co.x-x)*ratio; v.co.y=y+(v.co.y-y)*ratio
 o.data.update(); return o

for sx,x in [('L',-.665),('R',.665)]:
 for sy,y in [('F',-.290),('B',.290)]: tapered_foot('Foot_'+sx+sy,x,y)
box('Maple_base_rail',(-.780,-.390,.145),(.780,.390,.215),'Honey maple support',.012,1,'continuous base rail joining four feet to deck')
box('Upholstered_seat_deck',(-.795,-.415,.195),(.795,.415,.330),'Deep seafoam foundation',.018,1,'fixed cushion support deck')
sloped_box('Rear_support_shell',(-.785,.205,.275),(.785,.340,.865),'Deep seafoam foundation',.100,.018,1,'continuous rear-leaning back support joined to deck and arms')
for label,x0,x1 in [('L',-.840,-.650),('R',.650,.840)]:
 box('Low_armrest_'+label,(x0,-.440,.275),(x1,.440,.665),'Seafoam upholstery',.045,2,'fixed low upholstered armrest joined to deck and rear shell')
for label,x0,x1 in [('L',-.654,-.012),('R',.012,.654)]:
 box('Seat_cushion_'+label,(x0,-.430,.315),(x1,.230,.480),'Seafoam upholstery',.040,2,'separate broad seat pad supported by deck')
 sloped_box('Back_cushion_'+label,(x0,.110,.450),(x1,.290,.920),'Seafoam upholstery',.130,.040,2,'separate rear-leaning back pad supported by rear shell')
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
assert all(abs(a-b)<1e-5 for a,b in zip(bounds,[1.68,.88,.92])),bounds
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
 'placement':'Standalone complete two-seat sofa; front -Y, ground-contact origin Z=0; no sectional snap contract.',
 'scope':'Static visual furniture; no animation, upholstery physics, ergonomics, installation, load, tip-resistance or cross-asset compatibility certification.',
 'status':'producer geometry checks only; independent gates pending'}
# Bounded necessary interfaces, measured on the actual imported GLB triangles.
from mathutils.bvhtree import BVHTree
cache={}
for o in parts:
 vv=[o.matrix_world@v.co for v in o.data.vertices]; o.data.calc_loop_triangles()
 cache[o.name]=(BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True),vv)
directions=[Vector(v).normalized() for v in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]]
def inside(name,xyz):
 tree=cache[name][0]; p=Vector(xyz); results=[]
 for direction in directions:
  hits=0; origin=p.copy()
  for _ in range(64):
   loc,n,idx,d=tree.ray_cast(origin,direction,100)
   if loc is None: break
   hits+=1; origin=loc+direction*1e-5
  else: raise AssertionError('Uncertain interior test')
  results.append(hits%2==1)
 return all(results),tree.find_nearest(p)[3]
interfaces=[]
def anchors(a,b,points):
 witnesses=[]
 for p in points:
  ia,da=inside(a,p); ib,db=inside(b,p)
  assert ia and ib and min(da,db)>.0004,(a,b,p,ia,ib,da,db)
  witnesses.append({'interior_point_m':p,'minimum_surface_clearance_m':min(da,db),'three_ray_inside_a':ia,'three_ray_inside_b':ib})
 assert len(witnesses)>=3
 interfaces.append({'a':a,'b':b,'witnesses':witnesses})
for sx,x in [('L',-.665),('R',.665)]:
 for sy,y in [('F',-.290),('B',.290)]:
  anchors('Foot_'+sx+sy,'Maple_base_rail',[[x+dx,y,.163] for dx in [-.020,0,.020]])
anchors('Maple_base_rail','Upholstered_seat_deck',[[x,0,.205] for x in [-.55,0,.55]])
for label,x in [('L',-.720),('R',.720)]:
 anchors('Low_armrest_'+label,'Upholstered_seat_deck',[[x,y,.306] for y in [-.25,0,.25]])
 anchors('Low_armrest_'+label,'Rear_support_shell',[[x,y,.550] for y in [.275,.300,.325]])
anchors('Rear_support_shell','Upholstered_seat_deck',[[x,.295,.307] for x in [-.55,0,.55]])
for label,x in [('L',-.333),('R',.333)]:
 anchors('Seat_cushion_'+label,'Upholstered_seat_deck',[[x,y,.322] for y in [-.22,-.04,.13]])
 anchors('Back_cushion_'+label,'Rear_support_shell',[[x+dx,.316,.650] for dx in [-.18,0,.18]])
floor=[]
for o in parts:
 if not o.name.startswith('Foot_'): continue
 vv=cache[o.name][1]
 area=sum(t.area for t in o.data.loop_triangles if all(abs(vv[k].z)<1e-6 for k in t.vertices))
 assert area>.003, (o.name,area)
 floor.append({'part':o.name,'planar_contact_z_m':0,'finite_floor_contact_area_m2':area})
assert len(floor)==4
# Cushion centre seams are genuine empty strips; seam measurements derive from actual vertices.
seams=[]
for prefix in ['Seat_cushion_','Back_cushion_']:
 lv=cache[prefix+'L'][1];rv=cache[prefix+'R'][1]
 gap=min(v.x for v in rv)-max(v.x for v in lv)
 assert gap>=.02399,(prefix,gap)
 seams.append({'parts':[prefix+'L',prefix+'R'],'minimum_x_separation_m':gap})
qa['necessary_static_interfaces']={'scope':'Actual GLB finite interior joint witnesses and four finite planar floor contacts. No load, tip-resistance, ergonomic or upholstery mechanics claim.',
 'method':'At least three separated interior witnesses for each necessary joint; three ray directions and finite distance from both triangle surfaces.',
 'interfaces':interfaces,'floor_contacts':floor,'cushion_seams':seams}
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
scene.view_settings.view_transform='AgX'; focus=Vector((0,0,.46))
def aim(o,p): o.location=p; o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,power,location,size in [('Key',480,(-3,-4,5),4),('Fill',210,(4,-1,3),3),('Rim',310,(1,4,5),3)]:
 bpy.ops.object.light_add(type='AREA',location=location); light=bpy.context.object; light.name='Preview_'+name; light.data.energy=power; light.data.size=size; aim(light,location)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Preview_Camera'; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=2.12
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012)); ground=bpy.context.object; ground.name='Preview_Ground_NotAsset'
g=bpy.data.materials.new('Preview_Slate'); g.diffuse_color=(.18,.22,.23,1); g.use_nodes=True; g.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=g.diffuse_color; g.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9; ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384; scene.render.resolution_y=384
 for o in parts:
  for m in o.data.materials:
   p=m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value=(.5,.5,.5,1); p.inputs['Roughness'].default_value=.65; p.inputs['Metallic'].default_value=0
views={'gray-front3q':(3,-5,2.7),'gray-back3q':(-3,5,2.7)} if gray else {'thumbnail':(3,-5,2.7),'qa-front':(0,-5,.46),'qa-side':(5,0,.46),'qa-top':(0,0,6),'qa-back':(0,5,.46),'qa-wireframe':(3,-5,2.7)}
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
 render('silhouette-128-front',(0,-5,.46)); render('silhouette-128-side',(5,0,.46))
if PREVIOUS_QA:
 assert PREVIOUS_QA['actual_glb_sha256']==glb_sha,'Prior PBR thumbnail is bound to a different GLB'
 render_configs={'thumbnail':PREVIOUS_QA['render_configs']['thumbnail'],**render_configs}; render_seconds={'thumbnail':PREVIOUS_QA['render_seconds']['thumbnail'],**render_seconds}
qa.update({'render_configs':render_configs,'render_seconds':render_seconds,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent final gates pending'})
if not gray: save_metadata()
save_qa(); print('ASSET_COMPLETE',ASSET,triangles,glb_sha)
