"""Original S01 raised-platform terminal ramp, metres, Z up, uphill +X.
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
ASSET='transport-raised-platform-ramp-01'; VERSION='1.0.0'
TITLE='Fitted Loading Platform End Ramp'
DESCRIPTION=('Original 1.4 m nominal-pitch end ramp for the existing 0.38 m loading platform. '
 'Metres, Z up, ground datum origin, uphill +X and rear curb +Y. Place the unchanged transport-short-platform-01 at (+1.4,0,0), no rotation. '
 'A low tapered toe and inclined cream deck rise to an upper landing; two grounded seafoam supports carry the deck and a honey rear curb follows the slope. '
 'The 25 mm high-end tongue fits the actual platform deck bevel; a 15 mm curb tongue meets its rear-curb bevel. '
 'The 1.425 m full X envelope includes the tongue and is not the nominal pitch. Full depth is 1.2 m. '
 'Static visual connector only; no accessibility, driving, collision, navigation, load, installation, safety or engineering certification. '
 'Not compatible with 2 m pavement modules or the 0.12/0.72 m launch ramp. No external model is embedded in this asset.')
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
 'Warm sand deck':((.86,.75,.52,1),.83,0),
 'Honey rear curb':((.48,.255,.105,1),.83,0),
 'Seafoam support':((.19,.40,.35,1),.83,0),
}
mats={}
for name,(color,roughness,metallic) in PALETTE.items():
 m=bpy.data.materials.new(name); m.diffuse_color=color; m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=color; p.inputs['Roughness'].default_value=roughness; p.inputs['Metallic'].default_value=metallic; mats[name]=m
root=bpy.data.objects.new('RaisedPlatformRamp_Static',None); scene.collection.objects.link(root)
root['asset_id']=ASSET; root['origin_contract']='Nominal cell centre on ground; metres, Z up, uphill +X, rear curb +Y; not bounds-centred'
root['nominal_pitch_depth_rise_m']=[1.4,1.2,.38]; root['neighbour_origin_m']=[1.4,0,0]; root['docking_tongue_m']=.025
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def loft_profile(name,profile,outer_profile,ys,material,role):
 # A Y-only chamfer preserves the exact authored X/Z docking polygon.
 # Four corresponding profile rings create a closed single component.
 profiles=[outer_profile,profile,profile,outer_profile]; verts=[]; faces=[]; n=len(profile)
 assert len(outer_profile)==n
 for y,points in zip(ys,profiles): verts.extend((x,y,z) for x,z in points)
 faces.extend([tuple(reversed(range(n))),tuple(3*n+i for i in range(n))])
 for ring in range(3):
  for i in range(n): faces.append((ring*n+i,ring*n+(i+1)%n,(ring+1)*n+(i+1)%n,(ring+1)*n+i))
 me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
 o=bpy.data.objects.new(name,me); scene.collection.objects.link(o); o.parent=root; o.data.materials.append(mats[material]); o['role']=role
 bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(me); bm.free()
 bpy.context.view_layer.objects.active=o; mod=o.modifiers.new('Explicit runtime triangles','TRIANGULATE'); bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o); return o

# One terminal approach. Nominal X pitch 1.4 m; adjacent original platform at +1.4 m.
# The 25 mm upper tongue fills the exact old platform top bevel, not a flat AABB seam.
deck_profile=[(-.700,0),(-.550,.025),(.425,.380),(.725,.380),(.700,.355),(.700,.300),(.425,.300),(-.550,0)]
deck_outer=[(-.675,0),(-.550,.010),(.425,.355),(.725,.355),(.700,.330),(.700,.315),(.425,.315),(-.525,0)]
loft_profile('Fitted_ramp_deck',deck_profile,deck_outer,[-.600,-.575,.575,.600],'Warm sand deck',
 'grounded tapered approach and upper landing with true 25 mm mating-bevel tongue')
curb_profile=[(-.550,.010),(-.550,.155),(.425,.510),(.715,.510),(.700,.495),(.700,.365),(.425,.350)]
curb_outer=[(-.535,.025),(-.535,.140),(.425,.495),(.715,.495),(.700,.480),(.700,.380),(.425,.365)]
loft_profile('Rear_sloping_curb',curb_profile,curb_outer,[.480,.495,.585,.600],'Honey rear curb',
 'fixed rear +Y curb continues the neighbour orientation and fits its 15 mm upper bevel')
# Two grounded wedge supports provide visible, finite deck support.
for label,y in [('Front',-.380),('Rear',.380)]:
 support=[(-.400,0),(-.400,.064154),(.425,.318),(.640,.318),(.640,0)]
 outer=[(-.394,.006),(-.394,.058154),(.425,.312),(.634,.312),(.634,.006)]
 loft_profile('Grounded_support_'+label,support,outer,[y-.090,y-.084,y+.084,y+.090],'Seafoam support',
  'grounded longitudinal support under the inclined deck and high landing')
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
assert all(abs(a-b)<1e-5 for a,b in zip(bounds,[1.425,1.2,.51])),bounds
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
 'placement':'Uphill +X; original platform at (+1.4,0,0), no rotation. Rear curbs +Y. Nominal X pitch 1.4 m; envelope with mating tongue is 1.425 m.',
 'scope':'Static visual connector; bounded original-platform mesh docking only. No accessibility, driving, load, collision, navigation, installation, safety or engineering certification.',
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
def deck_top(x):
 if x<=-.550: return (x+.700)*.025/.150
 if x<.425: return .025+(x+.550)*.355/.975
 return .380
def deck_under(x):
 if x<-.550:return 0.
 if x<.425:return (x+.550)*.300/.975
 return .300
for label,y in [('Front',-.380),('Rear',.380)]:
 anchors('Grounded_support_'+label,'Fitted_ramp_deck',[[x,y,deck_under(x)+.009] for x in [-.250,.100,.500]])
anchors('Rear_sloping_curb','Fitted_ramp_deck',[[x,.540,deck_top(x)-.009] for x in [-.300,.000,.400]])
floor=[]
for name in ['Fitted_ramp_deck','Grounded_support_Front','Grounded_support_Rear']:
 o=next(o for o in parts if o.name==name); vv=cache[name][1]
 area=sum(t.area for t in o.data.loop_triangles if all(abs(vv[k].z)<1e-6 for k in t.vertices))
 assert area>.015,(name,area)
 floor.append({'part':name,'planar_contact_z_m':0,'finite_floor_contact_area_m2':area})
qa['necessary_static_interfaces']={'scope':'Actual GLB finite interior witnesses for two deck supports and rear curb; finite toe/support ground patches. Separate pinned-neighbour QA tests the real bevel fit.',
 'method':'At least three separated interior witnesses per necessary joint, three ray directions and finite distance from both triangle surfaces.',
 'interfaces':interfaces,'floor_contacts':floor}
qa['docking_contract']={'nominal_pitch_m':1.4,'depth_m':1.2,'rise_m':.38,'full_envelope_x_m':1.425,
 'original_platform_origin_m':[1.4,0,0],'rotation_degrees':[0,0,0], 'uphill':'+X','rear_curb':'+Y',
 'deck_bevel_tongue_x_m':[.7,.725],'deck_bevel_equation':'z=x-0.345 for central Y strip',
 'curb_bevel_tongue_x_m':[.7,.715],'curb_bevel_equation':'z=x-0.205 for central curb Y strip',
 'lower_toe_x_m':-.7,'lower_toe_z_m':0,'upper_landing_x_m':[.425,.725],
 'independent_actual_neighbour_validation':'required; not implied by source parameters'}
def save_qa(): (OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def save_metadata():
 if not (OUT/'thumbnail.png').exists(): return
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name; files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'transport','style':'S01-clean-geometric','title':TITLE,
  'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(PALETTE),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 save_metadata(); print('GEOMETRY_READY',ASSET,triangles,glb_sha); sys.exit(0)
# Studio objects and wire overlays are presentation-only and absent from native source.
scene.render.resolution_x=640; scene.render.resolution_y=640; scene.render.resolution_percentage=100
scene.world.use_nodes=True; scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.35,.37,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
scene.view_settings.view_transform='AgX'; focus=Vector((.01,0,.255))
def aim(o,p): o.location=p; o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,power,location,size in [('Key',480,(-3,-4,5),4),('Fill',210,(4,-1,3),3),('Rim',310,(1,4,5),3)]:
 bpy.ops.object.light_add(type='AREA',location=location); light=bpy.context.object; light.name='Preview_'+name; light.data.energy=power; light.data.size=size; aim(light,location)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Preview_Camera'; scene.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=1.90
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012)); ground=bpy.context.object; ground.name='Preview_Ground_NotAsset'
g=bpy.data.materials.new('Preview_Slate'); g.diffuse_color=(.18,.22,.23,1); g.use_nodes=True; g.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=g.diffuse_color; g.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9; ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384; scene.render.resolution_y=384
 for o in parts:
  for m in o.data.materials:
   p=m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value=(.5,.5,.5,1); p.inputs['Roughness'].default_value=.65; p.inputs['Metallic'].default_value=0
views={'gray-front3q':(-3,-5,2.8),'gray-back3q':(3,5,2.8)} if gray else {'thumbnail':(-3,-5,2.8),'qa-front':(0,-5,.255),'qa-side':(-5,0,.255),'qa-top':(0,0,6),'qa-back':(0,5,.255),'qa-wireframe':(-3,-5,2.8)}
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
 render('silhouette-128-front',(0,-5,.255)); render('silhouette-128-side',(-5,0,.255))
if PREVIOUS_QA:
 assert PREVIOUS_QA['actual_glb_sha256']==glb_sha,'Prior PBR thumbnail is bound to a different GLB'
 render_configs={'thumbnail':PREVIOUS_QA['render_configs']['thumbnail'],**render_configs}; render_seconds={'thumbnail':PREVIOUS_QA['render_seconds']['thumbnail'],**render_seconds}
qa.update({'render_configs':render_configs,'render_seconds':render_seconds,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent final gates pending'})
if not gray: save_metadata()
save_qa(); print('ASSET_COMPLETE',ASSET,triangles,glb_sha)
