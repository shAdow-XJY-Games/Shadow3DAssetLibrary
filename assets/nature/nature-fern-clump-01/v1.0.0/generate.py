"""Original S02 Low-Crown Pinnate Fern. Metres, Z-up; static botanical prop.
Self-contained original mesh generation. Flags: --geometry-only / --gray-only / --preview-only / --extra-views.
All render paths: Cycles 128 samples, no adaptive sampling or denoising, FIXED 4 threads.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-fern-clump-01';VERSION='1.0.0';TITLE='Low-Crown Pinnate Fern'
DESCRIPTION=('Original S02 hard-edge faceted fern with seven unequal arching fronds and a small grounded crown. '
 'Each continuous central rachis carries six pairs of separate folded lanceolate pinnae and a terminal leaflet; '
 'open pinna gaps form a feathered silhouette distinct from unsegmented grass blades. Five mature outward-bowing '
 'fronds and two shorter ascending inner fronds create a low asymmetric clump. Named editable closed-volume parts, '
 'solid PBR materials, metre scale and crown-centre ground origin Z=0. Independently authored static visual prop: '
 'no external textures, wind rig, animation, collision mesh, physics or species-accuracy guarantee.')
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
PALETTE={'Leaf_Upper':(.17,.32,.085,1),'Leaf_Body':(.095,.235,.065,1),'Leaf_Underside':(.065,.145,.05,1),
 'Rachis':(.245,.30,.075,1),'Crown':(.12,.105,.04,1)}
mats={}
for n,c in PALETTE.items():
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.9;mats[n]=m
root=bpy.data.objects.new('FernClump',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['ground_plane_z_m']=0.;root['static_visual_only']=True;root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[];frond_design=[];contacts=[]
def mesh(n,v,f,material_names,role,support=None):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for name in material_names:me.materials.append(mats[name])
 for face in me.polygons:face.use_smooth=False
 o.parent=root;o['component_role']=role
 if support:o['supported_by']=support
 parts.append(o);return o
# Crown is a modest closed basal sheath with a finite footprint; no terrain pedestal.
N=9;v=[]
for z,r in [(0,.024),(.012,.023),(.028,.014)]:
 for k in range(N):
  a=2*math.pi*k/N+.2;rr=r*(1+.075*math.sin(k*2.2));v.append((rr*math.cos(a),rr*.86*math.sin(a),z))
f=[tuple(range(N-1,-1,-1)),tuple(range(2*N,3*N))]
for j in range(2):
 for k in range(N):q=(k+1)%N;f.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
crown=mesh('Crown_BasalSheath',v,f,['Crown'],'ground_crown')
# Closed path tube helper; all botanical paths and profiles below are original.
def tube(name,centres,radii):
 v=[];sides=5
 for i,(c,r) in enumerate(zip(centres,radii)):
  tangent=(centres[min(i+1,len(centres)-1)]-centres[max(0,i-1)]).normalized()
  side=tangent.cross(Vector((0,0,1)))
  if side.length<.01:side=Vector((1,0,0))
  side.normalize();normal=tangent.cross(side).normalized()
  for k in range(sides):
   a=2*math.pi*k/sides;v.append(tuple(c+r*(math.cos(a)*side+math.sin(a)*normal)))
 f=[tuple(range(sides-1,-1,-1)),tuple(range((len(centres)-1)*sides,len(centres)*sides))]
 for i in range(len(centres)-1):
  for k in range(sides):q=(k+1)%sides;f.append((i*sides+k,i*sides+q,(i+1)*sides+q,(i+1)*sides+k))
 return mesh(name,v,f,['Rachis'],'rachis','Crown_BasalSheath')
def leaflet(name,base,forward,side,length,width,normal,support):
 # Narrow root inserts into the rachis; folded thin-volume pinna broadens then tapers to a single tip.
 direction=(side+forward*.27).normalized();cross=normal.cross(direction).normalized();v=[]
 for t,scale,fold in [(0,.10,.0035),(.28,1.,.006),(.64,.68,.0045)]:
  c=base+direction*(length*t)+normal*(length*.11*math.sin(math.pi*t))
  hw=width*scale*.5
  v.extend([tuple(c+cross*hw),tuple(c+normal*fold),tuple(c-cross*hw),tuple(c-normal*fold*.45)])
 tip=base+direction*length+normal*(length*.025);v.append(tuple(tip));f=[(3,2,1,0)]
 for j in range(2):
  for k in range(4):q=(k+1)%4;f.append((j*4+k,j*4+q,(j+1)*4+q,(j+1)*4+k))
 for k in range(4):f.append((8+k,8+(k+1)%4,12))
 o=mesh(name,v,f,['Leaf_Upper','Leaf_Body','Leaf_Underside'],'pinna',support)
 for p in o.data.polygons:p.material_index=0 if p.normal.z>.45 else (2 if p.normal.z<-.25 else 1)
 return o
# bearing, horizontal reach, arch height, terminal height, pinna span, frond-plane roll.
FRONDS=[('A',8,.62,.30,.17,.155,-.18),('B',80,.53,.31,.20,.145,.24),
 ('C',156,.61,.28,.15,.16,-.22),('D',220,.55,.27,.14,.145,.23),('E',292,.60,.29,.18,.15,-.20),
 ('F',47,.30,.36,.29,.105,.32),('G',190,.32,.335,.27,.108,-.30)]
# Pinna roots lie exactly on the piecewise-linear rachis; no free-floating construction points.
TS=[0,.13,.26,.37,.48,.59,.70,.80,.89,1.]
for idx,(label,bearing,reach,height,tip_height,span,roll) in enumerate(FRONDS):
 a=math.radians(bearing);u=Vector((math.cos(a),math.sin(a),0));w=Vector((-u.y,u.x,0))
 base=u*.005+Vector((0,0,.010+(idx%2)*.003))
 centres=[]
 for t in TS:
  radial=reach*(t**1.17);z=4*(height-tip_height*.5)*t*(1-t)+tip_height*t
  centres.append(base+u*radial+w*(.018*math.sin(math.pi*t)*(1 if idx%2 else -1))+Vector((0,0,z)))
 rachis='Rachis_'+label;tube(rachis,centres,[.0085*(1-t)+.0018 for t in TS])
 def sample(t):
  for j in range(len(TS)-1):
   if TS[j]<=t<=TS[j+1]:return centres[j].lerp(centres[j+1],(t-TS[j])/(TS[j+1]-TS[j])),(centres[j+1]-centres[j]).normalized()
  return centres[-1],(centres[-1]-centres[-2]).normalized()
 for pair,t in enumerate([.13,.25,.39,.53,.67,.80],1):
  c,tangent=sample(t);normal=tangent.cross(w).normalized();lateral=(w*math.cos(roll)+normal*math.sin(roll)).normalized();normal=tangent.cross(lateral).normalized()
  taper=[.70,.96,1.,.94,.76,.48][pair-1]
  for sign in [-1,1]:
   asym=1.+(.045 if sign==1 else -.035)*math.sin(idx+pair*.6)
   # Whole pinna root overlaps the stem; offset does not move it outside the axis radius.
   leafbase=c+lateral*(sign*.0012)
   leaflet('Pinna_%s_%02d_%s'%(label,pair,'L' if sign<0 else 'R'),leafbase,tangent,lateral*sign,span*taper*asym,.055*taper*(span/.15),normal,rachis)
 c=centres[-2];terminal_vector=centres[-1]-c;tangent=terminal_vector.normalized();normal=tangent.cross(w).normalized()
 leaflet('Pinna_'+label+'_Terminal',c,tangent,tangent,terminal_vector.length*1.12,.025*(span/.15),normal,rachis)
 frond_design.append({'name':rachis,'bearing_deg':bearing,'reach_m':reach,'arch_parameter_m':height,'pinna_pairs':6,'terminal_pinna':1,'root_m':list(base)})
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-10 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7
cv=[v.co for v in crown.data.vertices if abs(v.co.z)<1e-7];assert len(cv)==N
fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
def oriented_pbr_fingerprint(objects):
 records=[]
 for o in objects:
  o.data.calc_loop_triangles();vv=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   xyz=[tuple(round(float(q),6) for q in vv[i]) for i in t.vertices]
   m=o.data.materials[t.material_index];node=m.node_tree.nodes.get('Principled BSDF');assert node is not None
   pbr=tuple(round(float(q),6) for q in node.inputs['Base Color'].default_value)+(round(float(node.inputs['Roughness'].default_value),6),round(float(node.inputs['Metallic'].default_value),6))
   records.append((min(tuple(xyz[k:]+xyz[:k]) for k in range(3)),pbr))
 return hashlib.sha256(json.dumps(sorted(records),separators=(',',':')).encode()).hexdigest()
authored_oriented_pbr=oriented_pbr_fingerprint(parts)
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'mesh_objects':len(parts),'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'origin':'crown centre at ground Z=0; asymmetric bounds','components':checks,'ground_contacts':[{'part':crown.name,'ground_vertices':len(cv),'minimum_z_m':0}],
 'frond_design':frond_design,'frond_count':7,'pinna_count':91,
 'support_scope':'Continuous axes start within grounded crown; pinna root centres sample actual piecewise rachis paths. Botanical overlaps intentional; no mechanical or physics claim.',
 'geometry_fingerprint_sha256':fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
# Render and runtime checks use a fresh import of the exact exported GLB.
# The editable native file above remains the authored component scene, without studio objects.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH'];bpy.context.view_layer.update()
actual_oriented_pbr=oriented_pbr_fingerprint(parts);assert actual_oriented_pbr==authored_oriented_pbr,('GLB oriented triangles or PBR changed',authored_oriented_pbr,actual_oriented_pbr)
mats={m.name:m for o in parts for m in o.data.materials};assert len(mats)==len(PALETTE)
qa['actual_glb_sha256']=hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest()
qa['actual_glb_roundtrip']={'fresh_import':True,'oriented_triangles_and_pbr_sha256':actual_oriented_pbr,'matches_authored':True,'mesh_count':len(parts),'render_source':'fresh exact exported model.glb import'}
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
scene.view_settings.view_transform='AgX';focus=Vector((0,0,.27))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-2,-3,4),190,3),('Fill',(3,-1,2),95,3),('Rim',(1,3,3),135,2.5)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.52
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.002));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.22,.245,.24,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 scene.render.resolution_x=384;scene.render.resolution_y=384
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(2.8,-4,2.6),'gray-back3q':(-2.8,4,2.6)} if gray else {'thumbnail':(2.8,-4,2.6),'qa-front':(0,-4,.27),'qa-side':(4,0,.27),'qa-top':(0,0,5),'qa-back':(0,4,.27),'qa-wireframe':(2.8,-4,2.6)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0010;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(0,-4,.27)),('silhouette-128-side',(4,0,.27))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:write_metadata()
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
