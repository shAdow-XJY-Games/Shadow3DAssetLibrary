"""Original S01 empty dish drying rack. Metres, Z-up, bottom-centre origin.
Nine dividers / eight slots, three bearing strips, separate catch tray, four feet.
Flags: --geometry-only / --gray-only / --preview-only / --extra-views.
All images render a fresh import of the exact exported GLB at Cycles 128/FIXED4.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='interior-dish-drying-rack-01';VERSION='1.0.0';TITLE='Eight-Slot Empty Dish Drying Rack'
DESCRIPTION=('Original S01 empty countertop dish rack: nine continuous rounded ivory dividers make eight vertical slots '
 'with measured 35 mm clear spacing. Three 14 mm wide bottom bearing strips have a 71 mm top support plane; '
 'the open spaces between them expose a separate shallow seafoam catch tray below. Four grounded broad foot-posts, '
 'low fixed frame and two maple-colored end loops complete one editable static rack. Metres, bottom-centre origin, '
 'slot repeat along X. No dishes, moving tray, water flow, load rating, stability certification, capacity, '
 'dynamic insertion or existing-tableware compatibility claim.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c==EXPECTED,c;return c
PALETTE={'Seafoam_Frame':((.19,.40,.35,1),.62),'Ivory_CoatedRack':((.86,.78,.60,1),.48),'Maple_EndLoops':((.48,.255,.105,1),.72)};mats={}
for name,(color,rough) in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;mats[name]=m
root=bpy.data.objects.new('DishDryingRack',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_axis']='-Y';root['slot_repeat_axis']='+X';root['ground_z_m']=0.;root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def mesh(name,verts,faces,mat,role):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[mat])
 for f in me.polygons:f.use_smooth=False
 o.parent=root;o['component_role']=role;parts.append(o);return o
def box(name,loc,dims,mat,role,bevel=.001):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  b=o.modifiers.new('Restrained edge bevel','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 o.data.materials.append(mats[mat]);o.parent=root;o['component_role']=role;parts.append(o);return o
def tube(name,points,radius,mat,role,sides=8):
 # Planar YZ sweep: fixed X cross-section axis makes divider width exactly 2*radius.
 pts=[Vector(p) for p in points];verts=[]
 for i,c in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();n=Vector((0,-t.z,t.y));axis=Vector((1,0,0))
  for k in range(sides):a=2*math.pi*k/sides;verts.append(tuple(c+radius*(axis*math.cos(a)+n*math.sin(a))))
 faces=[tuple(range(sides-1,-1,-1)),tuple(range((len(pts)-1)*sides,len(pts)*sides))]
 for i in range(len(pts)-1):
  for k in range(sides):j=(k+1)%sides;faces.append((i*sides+k,i*sides+j,(i+1)*sides+j,(i+1)*sides+k))
 return mesh(name,verts,faces,mat,role)
def rect8(w,d,c,z):
 return [(x,y,z) for x,y in [(-w/2+c,-d/2),(w/2-c,-d/2),(w/2,-d/2+c),(w/2,d/2-c),
  (w/2-c,d/2),(-w/2+c,d/2),(-w/2,d/2-c),(-w/2,-d/2+c)]]
# One continuous tray shell, not four intersecting walls: solid floor and a real open recess.
profile=[(.448,.300,.018,.022),(.448,.300,.018,.044),(.444,.296,.016,.046),
 (.424,.276,.012,.046),(.420,.272,.011,.043),(.420,.272,.011,.029)]
tv=[v for w,d,c,z in profile for v in rect8(w,d,c,z)];tf=[tuple(range(7,-1,-1))]
for i in range(len(profile)-1):
 for j in range(8):k=(j+1)%8;tf.append((i*8+j,i*8+k,(i+1)*8+k,(i+1)*8+j))
tf.append(tuple(range((len(profile)-1)*8,len(profile)*8)))
tray=mesh('CatchTray_ContinuousShallowShell',tv,tf,'Seafoam_Frame','catch_tray_shell')
feet=[]
for x in [-.195,.195]:
 for y in [-.117,.117]:
  feet.append(box('GroundedFootPost_%s_%s'%('L' if x<0 else 'R','Front' if y<0 else 'Back'),(x,y,.038),(.028,.028,.076),'Seafoam_Frame','grounded_foot_post',.0015))
side_rails=[]
for y in [-.117,.117]:side_rails.append(box('LongSideRail_'+('Front' if y<0 else 'Back'),(0,y,.071),(.414,.016,.014),'Seafoam_Frame','long_frame_rail',.001))
end_rails=[]
for x in [-.195,.195]:end_rails.append(box('EndCrossRail_'+('L' if x<0 else 'R'),(x,0,.066),(.018,.250,.012),'Seafoam_Frame','end_bearer',.001))
supports=[]
for i,y in enumerate([-.070,0,.070]):supports.append(box('BottomBearingStrip_%02d'%(i+1),(0,y,.066),(.398,.014,.010),'Ivory_CoatedRack','bottom_bearing_strip',0))
# Nine independent continuous U loops give eight repeated open slots.
ribs=[]
YZ=[(-.117,.071),(-.117,.140),(-.114,.153),(-.106,.163),(-.094,.170),(-.080,.172),
 (.080,.172),(.094,.170),(.106,.163),(.114,.153),(.117,.140),(.117,.071)]
for i in range(9):
 x=(i-4)*.042;ribs.append(tube('PlateSlotDivider_%02d'%(i+1),[(x,y,z) for y,z in YZ],.0035,'Ivory_CoatedRack','plate_slot_divider'))
# Lower, thicker end loops attach to end cross rails; their apertures remain genuinely empty.
handles=[]
for x in [-.195,.195]:
 points=[(x,y,z) for y,z in [(-.109,.066),(-.109,.087),(-.104,.101),(-.092,.110),(-.078,.112),(.078,.112),(.092,.110),(.104,.101),(.109,.087),(.109,.066)]]
 handles.append(tube('LowEndLoop_'+('L' if x<0 else 'R'),points,.006,'Maple_EndLoops','low_end_loop'))
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();degenerate=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and volume>1e-10 and degenerate==0,(o.name,bad,volume,degenerate)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),
 'signed_volume_m3':volume,'nonmanifold_edges':bad,'degenerate_triangles':degenerate})
world=lambda o:[o.matrix_world@v.co for v in o.data.vertices]
limits=lambda o:([min(v[i] for v in world(o)) for i in range(3)],[max(v[i] for v in world(o)) for i in range(3)])
deps=bpy.context.evaluated_depsgraph_get();bvhs={o.name:BVHTree.FromObject(o,deps) for o in parts}
def nearest_ray(point,direction,objects=parts,length=1):
 hits=[]
 for o in objects:
  loc,normal,index,dist=bvhs[o.name].ray_cast(Vector(point),Vector(direction),length)
  if loc is not None:hits.append((dist,o.name,list(loc),list(normal)))
 return min(hits,key=lambda h:h[0]) if hits else None
# Actual mesh bounds establish full divider X width, not a nominal pitch-only assertion.
slots=[]
for i in range(8):
 left=limits(ribs[i])[1][0];right=limits(ribs[i+1])[0][0];gap=right-left;mid=(right+left)/2
 assert abs(gap-.035)<1e-6,(i,gap)
 clear=nearest_ray((mid,-.16,.12),(0,1,0),length=.32);assert clear is None,(i,clear)
 contact=nearest_ray((mid,0,.25),(0,0,-1));assert contact[1]=='BottomBearingStrip_02' and abs(contact[2][2]-.071)<1e-6,contact
 drain=nearest_ray((mid,.035,.25),(0,0,-1));assert drain[1]==tray.name and abs(drain[2][2]-.029)<1e-6,drain
 slots.append({'slot':i+1,'left_divider_max_x_m':left,'right_divider_min_x_m':right,'clear_x_m':gap,
 'clear_through_y_at_z_m':.12,'bearing_probe':{'first_mesh':contact[1],'point_m':contact[2],'normal':contact[3]},
 'open_floor_channel_probe':{'first_mesh':drain[1],'point_m':drain[2]}})
# Root points are embedded in real bearing volumes. These are bounded connection samples, not mechanics.
def inside(o,point):
 p=Vector(point);direction=Vector((.381,.729,.568)).normalized();hits=0
 for _ in range(30):
  loc,normal,index,dist=bvhs[o.name].ray_cast(p,direction,2)
  if loc is None:break
  hits+=1;p=loc+direction*1e-6
 return bool(hits%2)
connections=[]
for i,rib in enumerate(ribs):
 for y,rail in zip([-.117,.117],side_rails):
  p=((i-4)*.042,y,.071);assert inside(rail,p);connections.append({'part':rib.name,'bearer':rail.name,'point_m':p,'inside_actual_bearer':True})
for x,end in zip([-.195,.195],end_rails):
 for strip,y in zip(supports,[-.070,0,.070]):
  p=(x,y,.066);assert inside(end,p) and inside(strip,p);connections.append({'part':strip.name,'bearer':end.name,'point_m':p,'inside_both_actual_parts':True})
foot_checks=[]
for f in feet:
 lo,hi=limits(f);assert abs(lo[2])<1e-7
 contact=[list(v) for v in world(f) if abs(v.z)<1e-7];assert len(contact)>=4
 foot_checks.append({'name':f.name,'bottom_z_m':lo[2],'ground_contact_vertices':contact})
allv=[v for o in parts for v in world(o)];lo=[min(v[i] for v in allv) for i in range(3)];hi=[max(v[i] for v in allv) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and max(abs(lo[i]+hi[i]) for i in (0,1))<1e-7
# A few true adverse fixtures exercise the same bounded actual-geometry probes.
blocked=nearest_ray((-.168,-.16,.12),(0,1,0),length=.32)
assert blocked is not None and blocked[1]=='PlateSlotDivider_01',blocked
without_middle=nearest_ray((-.147,0,.25),(0,0,-1),objects=[o for o in parts if o.name!='BottomBearingStrip_02'])
assert without_middle[1]==tray.name and abs(without_middle[2][2]-.029)<1e-6,without_middle
assert not inside(side_rails[0],(-.168,-.117,.101))
negatives={'lateral_slot_probe_moved_into_divider':{'detected_obstruction':blocked[1],'point_m':blocked[2]},
 'middle_bearing_removed':{'first_hit':without_middle[1],'support_z_m':without_middle[2][2],'required_bearing_z_m':.071,'required_support_rejected':True},
 'divider_root_raised_30mm':{'inside_actual_rail':False,'join_rejected':True}}
def material_signature(m):
 p=m.node_tree.nodes['Principled BSDF'];result=[]
 for name in ['Base Color','Roughness','Metallic','Alpha','IOR','Transmission Weight','Emission Color','Emission Strength']:
  v=p.inputs[name].default_value
  result.extend(round(float(a),6) for a in v) if hasattr(v,'__len__') else result.append(round(float(v),6))
 return tuple(result)
def oriented_records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(a),6) for a in vv[k]) for k in t.vertices]
   rows.append((o.name,min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),material_signature(o.data.materials[t.material_index])))
 return sorted(rows)
bearing_report={'count':3,'actual_width_y_m':[limits(o)[1][1]-limits(o)[0][1] for o in supports],
 'actual_top_z_m':[limits(o)[1][2] for o in supports],'actual_bottom_z_m':[limits(o)[0][2] for o in supports]}
expected_records=oriented_records(parts)
geometry_fingerprint=hashlib.sha256(json.dumps(expected_records,separators=(',',':')).encode()).hexdigest()
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Round-trip every oriented world triangle and complete used PBR signature before any presentation edit.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];bpy.context.view_layer.update()
actual_records=oriented_records(parts);assert actual_records==expected_records,'Actual GLB oriented world triangles / PBR differ from native source'
assert len(parts)==23
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':len(parts),'bounds_m':bounds,
 'bounds_min_m':lo,'bounds_max_m':hi,'origin':'bottom centre 0,0,0; front -Y, slot repeat X','components':checks,
 'slot_measurements':slots,'bearing_strips':bearing_report,
 'catch_tray_floor_z_m':.029,'foot_contacts':foot_checks,'essential_connection_samples':connections,
 'structure_scope':'Actual static slot gaps, bottom-strip/floor rays, essential joins and grounded feet only. No dish fit, fluid, load or mechanics claim.',
 'bounded_negative_tests':negatives,'geometry_fingerprint_sha256':geometry_fingerprint,
 'actual_glb_geometry_and_pbr_exact_match':True,'oriented_world_triangle_count':len(actual_records),
 'material_signature_fields':['Base Color RGBA','Roughness','Metallic','Alpha','IOR','Transmission Weight','Emission Color RGBA','Emission Strength'],
 'render_source':'Freshly imported exact model.glb; oriented world triangles and complete used PBR signature matched native source',
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def write_metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/interior/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'interior','style':'S01-clean-geometric',
  'title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,
  'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:
 write_metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Save/export were clean. All presentation objects stay out of source.blend and model.glb.
asset_mats={m for o in parts for m in o.data.materials}
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX';focus=Vector((0,0,.083))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,energy,size in [('Key',(-1.6,-2,2.4),120,1.8),('Fill',(1.5,-.6,1),45,1.3),('Rim',(.7,1.6,1.8),75,1.6)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.59;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.8,-1.2,.9),'gray-back3q':(-.8,1.2,.9)} if gray else {
 'thumbnail':(.8,-1.2,.9),'qa-front':(0,-1,.083),'qa-side':(1,0,.083),'qa-top':(0,0,1),
 'qa-back':(0,1,.083),'qa-wireframe':(.8,-1.2,.9)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));render_configs[name]=assert_render();t=time.time()
 bpy.ops.render.render(write_still=True);render_seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for poly in dup.data.polygons:poly.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00030;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-1,.083)),('silhouette-128-side',(1,0,.083))]:render(name,pos)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:write_metadata()
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
