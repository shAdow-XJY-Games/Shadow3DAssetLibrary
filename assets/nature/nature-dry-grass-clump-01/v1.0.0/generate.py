"""Original S02 Dryland Bent-Blade Grass Clump. Metres, Z-up, static editable prop.
No external textures/models. Blender -b -t 4 --python-exit-code 1 --python generate.py
Flags after --: --no-render, --gray-only, --preview-only, --extra-views.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-dry-grass-clump-01';VERSION='1.0.0';TITLE='Dryland Bent-Blade Grass Clump'
DESCRIPTION=('Original S02 hard-edge faceted dryland grass tussock: twenty-four slender folded blades form three unequal '
 'grounded leaf fans, with an upright central crown and lower outward-bending secondary crowns. Each narrow blade has '
 'a shaped midrib, closed thin volume, varied arch and single tapering tip. Olive new growth and ochre older outer leaves '
 'support the low dryland silhouette without seed stems, reed culms or a soil pedestal. Metre scale, ground origin Z=0; '
 'named editable leaves and basal crowns. Solid PBR, no external textures, wind rig, animation or collision mesh. '
 'Independently authored geometry, not a scaled or recoloured wetland grass variant.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=False

def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
  'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
  'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={'Leaf_Olive':(.285,.335,.115,1),'Leaf_Sunlit':(.415,.455,.185,1),
 'Leaf_OlderGold':(.54,.395,.17,1),'Leaf_OlderShade':(.365,.265,.105,1),'Root_Sheath':(.185,.135,.065,1)}
mats={}
for n,c in PALETTE.items():
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.88;mats[n]=m
root=bpy.data.objects.new('DryGrassClump',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['ground_plane_z_m']=0.;root['static_visual_only']=True;root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[];crowns=[];leaf_design=[]
def mesh(n,v,f,material_names,role):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for name in material_names:me.materials.append(mats[name])
 for face in me.polygons:face.use_smooth=False
 o.parent=root;o['component_role']=role;parts.append(o);return o
CROWNS={'Main':((0.,0.),.032,.016),'Left':((-.05,-.017),.029,.014),'Right':((.048,.022),.027,.013)}
for group,(xy,r,h) in CROWNS.items():
 v=[];N=7
 for z,scale in [(0,1),(h*.32,.91),(h,.53)]:
  for k in range(N):
   a=2*math.pi*k/N+.2;rad=r*scale*(1+.09*math.sin(k*2.4));v.append((xy[0]+rad*math.cos(a),xy[1]+rad*.83*math.sin(a),z))
 f=[tuple(range(N-1,-1,-1)),tuple(range(2*N,3*N))]
 for j in range(2):
  for k in range(N):q=(k+1)%N;f.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
 o=mesh('Crown_'+group,v,f,['Root_Sheath'],'basal_sheath');crowns.append(o)
# bearing degrees, maximum height, outward reach, full blade width, twist, old/arched.
# Separate original parameters create unequal leaf fans rather than duplicated radial copies.
BLADES={
'Main':[(18,.66,.13,.038,.14,False),(111,.62,.19,.043,-.12,False),(220,.59,.17,.042,.10,False),
 (298,.64,.20,.039,-.18,False),(62,.53,.28,.049,.21,False),(164,.55,.27,.045,-.15,False),
 (258,.51,.31,.048,.15,False),(338,.49,.30,.044,-.14,False),(204,.39,.36,.043,.12,True),
 (91,.43,.34,.039,-.16,True)],
'Left':[(154,.47,.27,.043,.12,False),(231,.43,.25,.039,-.16,False),(82,.48,.20,.039,.18,False),
 (326,.40,.23,.042,-.13,False),(186,.32,.32,.041,.20,True),(269,.31,.29,.038,-.19,True),
 (125,.35,.29,.040,.15,True),(28,.37,.20,.035,-.16,True)],
'Right':[(27,.40,.25,.040,.18,False),(113,.42,.23,.036,-.12,False),(281,.36,.27,.037,.17,False),
 (353,.29,.30,.036,-.18,True),(68,.31,.29,.037,.14,True),(216,.30,.23,.035,-.20,True)]}
for group,specs in BLADES.items():
 xy,r,crown_h=CROWNS[group]
 for i,(bearing,height,reach,width,twist,old) in enumerate(specs,1):
  a=math.radians(bearing);u=Vector((math.cos(a),math.sin(a),0));w=Vector((-u.y,u.x,0))
  base=Vector((xy[0],xy[1],.006))+u*(.013+(i%3)*.004)+w*((i%2-.5)*.011)
  ts=[0,.22,.48,.74,.92];rs=[0,.14,.36,.66,.88];ws=[.38,1,.81,.46,.15]
  zs=[0,.39,.76,.98,1.0] if old else [0,.28,.56,.81,.955]
  centres=[base+u*(reach*rr)+w*(.018*math.sin(t*math.pi)*(1 if twist>0 else -1))+Vector((0,0,height*zz)) for t,rr,zz in zip(ts,rs,zs)]
  tip=base+u*reach+Vector((0,0,height*(.93 if old else 1.)))
  v=[]
  for j,(c,t,ww) in enumerate(zip(centres,ts,ws)):
   tangent=((centres[j+1] if j<len(centres)-1 else tip)-(centres[j-1] if j>0 else centres[0]-Vector((0,0,.03)))).normalized()
   side=(w*math.cos(twist*t)+u*math.sin(twist*t)).normalized();normal=tangent.cross(side).normalized()
   half=width*ww*.5;fold=width*ww*.15
   # Diamond cross-section forms a visible longitudinal midrib with a restrained closed thickness.
   v.extend([tuple(c+side*half),tuple(c+normal*fold),tuple(c-side*half),tuple(c-normal*fold*.34)])
  v.append(tuple(tip));f=[(3,2,1,0)]
  for j in range(len(ts)-1):
   for k in range(4):q=(k+1)%4;f.append((j*4+k,j*4+q,(j+1)*4+q,(j+1)*4+k))
  for k in range(4):f.append((16+k,16+(k+1)%4,20))
  n='Blade_%s_%02d'%(group,i);o=mesh(n,v,f,['Leaf_OlderGold','Leaf_OlderShade'] if old else ['Leaf_Sunlit','Leaf_Olive'],'old_leaf' if old else 'new_leaf')
  for p in o.data.polygons:p.material_index=0 if p.index>0 and (p.index-1)%4 in (0,1) else 1
  o['root_crown']='Crown_'+group;o['design_height_m']=height;o['design_reach_m']=reach;o['old_outer_leaf']=old
  leaf_design.append({'name':n,'crown':'Crown_'+group,'base_m':list(base),'bearing_deg':bearing,'height_m':height,'reach_m':reach,'full_width_m':width,'old_outer_leaf':old})
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-10 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7
contacts=[]
for o in crowns:
 cv=[v.co for v in o.data.vertices if abs(v.co.z)<1e-7];assert len(cv)>=3
 contacts.append({'part':o.name,'ground_vertices':len(cv),'minimum_z_m':min(v.co.z for v in o.data.vertices)})
fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'mesh_objects':len(parts),'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'origin':'central crown ground point at Z=0; asymmetric bounds','components':checks,'ground_contacts':contacts,'blade_design':leaf_design,
 'support_scope':'Basal blade overlap within their named crowns is intentional. Visual static leaf support, not physics or strength testing.',
 'geometry_fingerprint_sha256':fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
save_qa()
def write_metadata():
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n
  if not p.exists():return
  files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 m={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 write_metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Preview scene is created after clean export, never saved in the asset blend.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX';focus=Vector((-.01,.025,.31))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-2,-3,4),190,3),('Fill',(3,-1,2),95,3),('Rim',(1,3,3),135,2.5)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.20
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_neutral');g.diffuse_color=(.25,.265,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(1.5,-2.2,1.15),'gray-back3q':(-1.5,2.2,1.15)} if gray else {'thumbnail':(1.5,-2.2,1.15),'qa-front':(-.01,-3,.31),'qa-side':(3,.025,.31),'qa-top':(-.01,.025,3),'qa-back':(-.01,3,.31),'qa-wireframe':(1.5,-2.2,1.15)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(n,p):
 aim(cam,p);scene.render.filepath=str(OUT/(n+'.png'));render_configs[n]=assert_render();t=time.time();bpy.ops.render.render(write_still=True);render_seconds[n]=round(time.time()-t,3)
for n,p in views.items():
 if n=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for poly in dup.data.polygons:poly.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0009;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for face in o.data.polygons:face.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(-.01,-3,.31)),('silhouette-128-side',(3,.025,.31))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:write_metadata()
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
