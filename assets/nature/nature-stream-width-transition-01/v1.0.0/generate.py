"""Original S02 stream-width transition, metres, Z up. Static visual module.
Standalone Blender generator, no external files/models/textures/fonts.
blender -b -t 4 --python-exit-code 1 --python generate.py -- --geometry-only
--gray-only: two early gray views and 128px silhouettes. --preview-only: first PBR.
No flags: six formal images. --no-render: clean native/runtime rebuild.
Narrow/wide end planes X=-1/+1; bank-foot spacing .60/1.40; water body .72/1.52.
Fixed water top .16; longitudinal slope zero; see PORTS and qa-report for exact sections.
The legacy bend raw water width .60 differs from straight-style .72; no universal snap claim.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='nature-stream-width-transition-01';VERSION='1.0.0';TITLE='Narrow-to-Wide Stream Transition'
DESCRIPTION=('Original S02 two-port stream-width transition over a 2 m run, with channel bank-foot spacing changing from .60 to 1.40 m. '
 'End planes X=-1 and +1; tangent X; fixed water top Z=.16 m and zero longitudinal slope. Independent water body widens from .72 to 1.52 m, '
 'with .06 m lateral bank penetration matching the original straight-scene water style. Water top edges remain on the ports, but bottom edges retreat .01 m to make slanted closed caps without overlapping bank end faces; paired bottoms have a V gap and only surface continuity is claimed. Bank relative cross-sections preserve the original '
 '.06/.20/.55 m profile with +.09 m placement offset. Independently editable bed, banks, water and four inset original faceted rocks. '
 'Bed top Z=.09 m meets bank and water bottoms without overlapping end caps; bed extends .02 m past each outer bank. Legacy earth and water PBR values retained at end surfaces. Original bend raw water width is .60 m, so exact bend-water seam and whole legacy-scene '
 'base snapping are not claimed. Static visual module only; no hydrology, collision, navigation, walkability or physics certification.')
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
PALETTE={'LegacyEarth':((.30,.36,.18,1),.83),'DampEarth':((.22,.235,.135,1),.92),'CutBed':((.20,.17,.11,1),.95),'LegacyWater':((.075,.20,.24,1),.23),'StoneSide':((.36,.405,.38,1),.86),'StoneTop':((.46,.505,.46,1),.86)}
mats={}
for n,(c,r) in PALETTE.items():
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=r;mats[n]=m
root=bpy.data.objects.new('StreamWidthTransition',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['origin']='Bed underside centre, Z=0';root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
parts=[]
def mesh(name,verts,faces,material_names,role):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o['component_role']=role
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for n in material_names:me.materials.append(mats[n])
 for p in me.polygons:p.use_smooth=False
 parts.append(o);return o
def ring_solid(name,rings,materials,role):
 n=len(rings[0]);verts=[v for r in rings for v in r];faces=[tuple(range(n-1,-1,-1)),tuple(range((len(rings)-1)*n,len(rings)*n))]
 for j in range(len(rings)-1):
  for k in range(n):q=(k+1)%n;faces.append((j*n+k,j*n+q,(j+1)*n+q,(j+1)*n+k))
 return mesh(name,verts,faces,materials,role)
# x, channel-foot half-width, lower-shelf width, outer bank width, shoulder elevation, ridge elevation.
# Both actual end sections are exact legacy-bank profiles after their scene placement offset.
STATIONS=[(-1,.30,.38,1.20,.29,.64),(-.68,.325,.40,1.20,.305,.665),(-.12,.45,.45,1.22,.315,.68),(.43,.62,.405,1.18,.30,.655),(1,.70,.38,1.20,.29,.64)]
bed=ring_solid('Bed_ContinuousGround',[[ (x,-(h+outer+.02),0),(x,h+outer+.02,0),(x,h+outer+.02,.09),(x,-(h+outer+.02),.09)] for x,h,s,outer,sz,oz in STATIONS],['LegacyEarth','CutBed'],'ground_bed')
for p in bed.data.polygons:p.material_index=0 if p.normal.z>.5 else 1
banks=[]
for sign,label in [(-1,'South'),(1,'North')]:
 rings=[]
 for j,(x,h,s,outer,sz,oz) in enumerate(STATIONS):
  # An unequal interior crest avoids mirror-identical slopes while retaining both exact ports.
  variation=0 if j in [0,len(STATIONS)-1] else (.015 if sign<0 else -.012)*math.sin(j*1.2)
  rings.append([(x,sign*h,.09),(x,sign*h,.15),(x,sign*(h+s),sz+variation),(x,sign*(h+outer),oz+variation),(x,sign*(h+outer),.09)])
 o=ring_solid('Bank_'+label,rings,['LegacyEarth','DampEarth','CutBed'],'bank');banks.append(o)
 for p in o.data.polygons:
  xs=[o.data.vertices[k].co.x for k in p.vertices];ys=[abs(o.data.vertices[k].co.y) for k in p.vertices]
  # Interior low facets only are damp. End spans retain complete legacy earth colour.
  interior=min(xs)>-.69 and max(xs)<.44
  p.material_index=1 if interior and p.normal.z>.1 and max(ys)<1.1 else (2 if p.normal.z<-.5 else 0)
water_rings=[]
for x,h,s,outer,sz,oz in STATIONS:
 bottom_x=x*.99 if abs(x)==1 else x
 water_rings.append([(bottom_x,-(h+.06),.09),(bottom_x,h+.06,.09),(x,h+.06,.16),(x,-(h+.06),.16)])
water=ring_solid('WaterSurface_Runtime',water_rings,['LegacyWater'],'water')
water['water_surface_z_m']=.16;water['longitudinal_slope']=0.0;water['replace_material_independently']=True
# Four compact original rock solids; lower vertices penetrate their local sloping bank.
def station_at(x):
 for a,b in zip(STATIONS,STATIONS[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return tuple(a[k]+t*(b[k]-a[k]) for k in range(6))
 raise ValueError(x)
def surface_at(x,y):
 _,h,s,outer,sz,oz=station_at(x);d=abs(y)-h
 return .15+(sz-.15)*d/s if d<=s else sz+(oz-sz)*(d-s)/(outer-s)
for i,(x,sign,d,rx,ry,height) in enumerate([(-.52,-1,.60,.19,.22,.23),(.45,-1,.84,.22,.16,.19),(-.24,1,.78,.20,.19,.24),(.52,1,.32,.15,.17,.17)],1):
 _,h,*_=station_at(x);cy=sign*(h+d);cz=surface_at(x,cy);a=.31*i
 rings=[]
 for scale,zoff,dx,dy in [(1,-.12,0,0),(1.07,.03,.025,-.012),(.56,height,.012,.02)]:
  ring=[]
  for k in range(7):
   t=2*math.pi*k/7+a;f=1+.10*math.sin(k*1.83+i);ring.append((x+dx+rx*scale*f*math.cos(t),cy+dy+ry*scale*f*math.sin(t),cz+zoff+.018*math.cos(k*2.2+i)))
  rings.append(ring)
 o=ring_solid('BankRock_%02d'%i,rings,['StoneSide','StoneTop'],'bank_rock');o['supported_by']='Bank_'+('South' if sign<0 else 'North')
 for p in o.data.polygons:p.material_index=1 if p.normal.z>.44 else 0
# Numeric port proofs read back actual authored vertices, not only design parameters.
PORTS=[]
for x,h,label in [(-1,.30,'narrow'),(1,.70,'wide')]:
 records={}
 for sign,o in zip([-1,1],banks):
  actual=sorted((round(v.co.y,6),round(v.co.z,6)) for v in o.data.vertices if abs(v.co.x-x)<1e-6)
  expected=sorted([(round(sign*h,6),.09),(round(sign*h,6),.15),(round(sign*(h+.38),6),.29),(round(sign*(h+1.2),6),.64),(round(sign*(h+1.2),6),.09)])
  assert actual==expected,(label,o.name,actual,expected);records[o.name]=actual
 actual_water=sorted((round(v.co.y,6),round(v.co.z,6)) for v in water.data.vertices if abs(v.co.x-x)<1e-6)
 expected_water=sorted([(h+.06,.16),(-(h+.06),.16)])
 assert all(max(abs(a[i]-b[i]) for i in range(2))<1e-6 for a,b in zip(actual_water,expected_water))
 PORTS.append({'name':label,'plane_x_m':x,'outward_tangent':[x,0,0],'bank_foot_width_m':2*h,'raw_water_body_width_m':2*(h+.06),'bank_vertices_yz_m':records,'water_vertices_yz_m':actual_water,'water_top_z_m':.16,'water_bottom_z_m':.09,'water_closed_cap_bottom_x_m':x*.99,'water_bottom_end_inset_m':.01,'bed_top_z_m':.09,'bank_profile_matches_legacy_with_z_offset_m':.09})
# Finite wide-to-wide pair: second module rotated pi around Z and translated +2m X.
# Its wide plane maps from X=+1 to world X=+1; both cross-sections have identical unordered yz pairs.
wide=PORTS[1];pair_max=0
for key in ['Bank_North','Bank_South']:
 other='Bank_South' if key=='Bank_North' else 'Bank_North';a=sorted(wide['bank_vertices_yz_m'][key]);b=sorted((-y,z) for y,z in wide['bank_vertices_yz_m'][other]);pair_max=max(pair_max,max(abs(p[k]-q[k]) for p,q in zip(a,b) for k in range(2)))
assert pair_max<1e-6
root['port_contract']=json.dumps(PORTS,sort_keys=True)
bpy.context.view_layer.update();checks=[];triangles=0
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(v[i] for v in verts) for i in range(3)];hi=[max(v[i] for v in verts) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
geometry_fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
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
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,'origin':'Bed underside centre at Z=0; X is flow-axis, no flow simulation','components':checks,'ports':PORTS,'finite_wide_pair':{'second_rotation_z_rad':math.pi,'second_translation_m':[2,0,0],'max_bank_port_vertex_error_m':pair_max,'surface_continuity_only':True,'water_bottom_v_gap_m':.02,'instances_are_not_new_assets':True},'legacy_compatibility_scope':'Exact original bank profile with +.09m vertical placement; straight-style water width. Original .60m bend water and whole legacy scene-base geometry are not exact compatible water/body snaps.','geometry_fingerprint_sha256':geometry_fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
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
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Presentation added only after clean native/runtime have been saved.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX';focus=Vector((0,0,.28))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-5,-7,10),1400,7),('Fill',(7,-2,5),650,6),('Rim',(2,7,8),900,5)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=4.6
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview_ground_not_asset';g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.22,.245,.24,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1)
views={'gray-front3q':(-5,-7,7),'gray-back3q':(5,7,7)} if gray else {'thumbnail':(-5,-7,7),'qa-front':(0,-7,.28),'qa-side':(-7,0,.28),'qa-top':(0,0,8),'qa-back':(0,7,.28),'qa-wireframe':(-5,-7,7)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
render_seconds={};render_configs={}
def render(n,p):
 cam.data.ortho_scale=2.7 if n in ['qa-front','qa-back','silhouette-128-front'] else (4.3 if n in ['qa-side','silhouette-128-side'] else 4.6)
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
 for n,p in [('silhouette-128-front',(0,-7,.28)),('silhouette-128-side',(-7,0,.28))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n;files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
