"""Original S02 Mature Open-Bough Conifer, metres, Z up; static visual prop.
Self-contained Blender source, no external models, textures, fonts, or plug-ins.
blender -b -t 4 --python-exit-code 1 --python generate.py -- --geometry-only
Use --gray-only for two early gray views and 128px front/side silhouettes;
--preview-only for first PBR; no flag for final six images. --no-render is clean build.
"""
import bpy, bmesh, math, json, hashlib, sys, time
from pathlib import Path
from mathutils import Vector
START=time.time(); OUT=Path(__file__).resolve().parent
ASSET='nature-mature-conifer-01'; VERSION='1.0.0'; TITLE='Mature Open-Bough Conifer'
DESCRIPTION=('Original S02 hard-edge faceted mature conifer with a thick tapered central trunk, five unequal root flares, '
 'staggered spreading lower boughs, ascending upper boughs and narrow pointed leader. Individual angular needle masses '
 'follow visible supporting branches; crown gaps and unequal lengths make an independently authored mature silhouette. '
 'Ground interface is Z=0 at the trunk centre; roots spread beyond the stem. Named editable trunk, roots, primary branches, '
 'secondary forks and foliage components. Solid PBR materials, no external textures. Static visual prop with no wind rig, '
 'animation, collision mesh or continuous mechanical simulation. Not a scaled or recoloured young-conifer variant.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
def render_config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
  'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[vl.cycles.use_denoising for vl in scene.view_layers],
  'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def assert_render():
 c=render_config();assert c=={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False]*len(scene.view_layers),'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4},c
 return c
PALETTE={'Bark':(.19,.115,.067,1),'Bark_light':(.235,.151,.094,1),'Needles_shade':(.055,.115,.080,1),
 'Needles_body':(.105,.215,.13,1),'Needles_top':(.20,.325,.155,1)}
mats={}
for n,c in PALETTE.items():
 a=bpy.data.materials.new(n);a.diffuse_color=c;a.use_nodes=True
 p=a.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=.89;mats[n]=a
parts=[];support=[];ground_parts=[]
root=bpy.data.objects.new('MatureConifer',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['ground_plane_z_m']=0.0;root['static_visual_only']=True
root['native_render_contract']=json.dumps(assert_render(),sort_keys=True)
def mesh(n,v,f,role,parent_support=None):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 names=['Needles_shade','Needles_body','Needles_top'] if role=='foliage' else ['Bark','Bark_light']
 for name in names:me.materials.append(mats[name])
 for face in me.polygons:
  face.use_smooth=False
  face.material_index=(2 if face.normal.z>.48 else (0 if face.normal.z<-.25 else 1)) if role=='foliage' else (1 if face.normal.x<-.30 and face.normal.y<.3 else 0)
 o.parent=root;o['component_role']=role
 if parent_support:o['supported_by']=parent_support;support.append({'child':n,'parent':parent_support})
 parts.append(o);return o
# Reused generic closed ring-path helper pattern; all coordinates and profiles below are original.
def tube(n,centres,radii,sides=8,role='branch',parent_support=None,ground=False):
 centres=[Vector(c) for c in centres];v=[]
 for j,(c,r) in enumerate(zip(centres,radii)):
  axis=(centres[min(j+1,len(centres)-1)]-centres[max(0,j-1)]).normalized()
  ref=Vector((0,1,0)) if abs(axis.y)<.9 else Vector((1,0,0));u=axis.cross(ref).normalized();w=axis.cross(u).normalized()
  for k in range(sides):
   a=2*math.pi*k/sides;factor=1+.045*math.sin(k*2.1+j*.7)
   p=c+r*factor*(math.cos(a)*u+math.sin(a)*w)
   if ground:p.z=max(0,p.z)
   v.append(tuple(p))
 f=[tuple(range(sides-1,-1,-1)),tuple(range((len(centres)-1)*sides,len(centres)*sides))]
 for j in range(len(centres)-1):
  for k in range(sides):q=(k+1)%sides;f.append((j*sides+k,j*sides+q,(j+1)*sides+q,(j+1)*sides+k))
 return mesh(n,v,f,role,parent_support)
TRUNK=[(0,0,0),(.015,-.015,.24),(.045,0,1.25),(.06,.03,2.5),(.09,.04,3.85),(.07,.065,5.1),(.13,.055,6.45),(.11,.04,7.65),(.13,.04,8.55)]
RADII=[.40,.33,.265,.215,.168,.127,.082,.037,.009]
tube('Trunk_MatureCentralLeader',TRUNK,RADII,10,'trunk',ground=True);ground_parts.append('Trunk_MatureCentralLeader')
def stem(z):
 for a,b in zip(TRUNK,TRUNK[1:]):
  if a[2]<=z<=b[2]:return Vector(a).lerp(Vector(b),(z-a[2])/(b[2]-a[2]))
 return Vector(TRUNK[-1])
for i,(angle,length,width) in enumerate([(12,1.02,.24),(88,.83,.20),(165,1.15,.26),(229,.91,.21),(302,1.08,.23)],1):
 a=math.radians(angle);u=Vector((math.cos(a),math.sin(a),0));w=Vector((-u.y,u.x,0));v=[]
 # Finite ground footprint at each end; upper ridge blends into the lower stem.
 for r,z,half in [(.10,.51,width),(length*.48,.20,width*.60),(length,.035,.055)]:
  c=u*r;v += [tuple(c-w*half),tuple(c+w*half),tuple(c+w*half*.25+Vector((0,0,z))),tuple(c-w*half*.25+Vector((0,0,z)))]
 f=[(3,2,1,0),(8,9,10,11)]
 for row in range(2):
  for k in range(4):q=(k+1)%4;f.append((row*4+k,row*4+q,(row+1)*4+q,(row+1)*4+k))
 name='RootFlare_%02d'%i;mesh(name,v,f,'root','Trunk_MatureCentralLeader');ground_parts.append(name)
# Primary boughs are explicitly staggered, not complete concentric whorls.
# id, height, bearing, radial length, width, vertical lift at outer end, foliage crest.
BOUGHS=[('L01',2.14,192,2.52,.88,-.24,1.12),('L02',2.42,320,2.74,.91,-.31,1.15),
 ('L03',2.66,62,2.43,.85,-.16,1.08),('L04',2.94,131,2.27,.81,-.11,1.04),
 ('M01',3.57,256,2.14,.76,-.02,1.02),('M02',3.88,15,2.22,.78,.03,1.01),
 ('M03',4.13,158,1.98,.70,.10,.98),('M04',4.43,90,1.82,.65,.15,.91),
 ('U01',4.92,298,1.76,.62,.23,.87),('U02',5.22,202,1.54,.56,.27,.82),
 ('U03',5.53,50,1.47,.52,.31,.78),('U04',5.93,130,1.21,.45,.36,.72),
 ('T01',6.38,340,1.06,.38,.40,.62),('T02',6.67,222,.85,.32,.43,.57)]
def foliage(n,base,u,w,length,width,lift,height,phase,parent_support):
 # Three low conical needle sprays follow the branch and its secondary forks.
 # Independent tips and shallow uneven rims replace the failed single broad leaf hood.
 profiles=[('Inner',.35,-.10,.33,.68,.68),('Outer',.77,.045,.29,.54,.47),('Fork',.57,.39,.245,.59,.55)]
 if length<1.3:profiles=profiles[:2]
 for suffix,t,side,rr,ww,hh in profiles:
  centre=base+u*(length*t)+w*(width*side)+Vector((0,0,lift*t))
  rx=length*rr;ry=width*ww;h=height*hh
  angles=[0,.72,1.57,2.54,3.19,4.20,5.36];v=[];N=len(angles)
  for row,(scale,zoff,shift) in enumerate([(.61,-.025,0),(1,.10,.03),(.08,h,.15)]):
   for k,a in enumerate(angles):
    variation=1+.13*math.sin(k*1.8+phase)+( .10 if k==2 else 0)
    uneven=(.065*math.sin(k*2.2+phase) if row<2 else .015*math.sin(k+phase))
    q=centre+u*(rx*(scale*variation*math.cos(a)+shift))+w*(ry*scale*variation*math.sin(a))+Vector((0,0,zoff+uneven))
    v.append(tuple(q))
  f=[tuple(range(N-1,-1,-1)),tuple(range(2*N,3*N))]
  for j in range(2):
   for k in range(N):q=(k+1)%N;f.append((j*N+k,j*N+q,(j+1)*N+q,(j+1)*N+k))
  mesh(n+'_'+suffix,v,f,'foliage',parent_support)
for i,(name,z,angle,length,width,lift,height) in enumerate(BOUGHS):
 a=math.radians(angle);u=Vector((math.cos(a),math.sin(a),0));w=Vector((-u.y,u.x,0));base=stem(z)
 main='Bough_'+name;rad=.105 if name.startswith('L') else (.077 if name.startswith('M') else .053)
 tube(main,[base,base+u*length*.30+Vector((0,0,-.08)),base+u*length*.68+Vector((0,0,lift*.65)),base+u*length*.985+Vector((0,0,lift+.015))],[rad,rad*.75,rad*.40,.012],7,'primary_branch','Trunk_MatureCentralLeader')
 # Short paired secondary supports meet the underside of each broad needle fan.
 for sign,t in [(-1,.48),(1,.60)]:
  original_c=base+u*length*t+Vector((0,0,lift*t))
  blend=(t-.30)/(.68-.30);branch_z=-.08*(1-blend)+(lift*.65)*blend
  c=base+u*length*t+Vector((0,0,branch_z))
  end=original_c+u*length*.16+w*width*.69*sign+Vector((0,0,.16))
  tube('Fork_'+name+('_L' if sign<0 else '_R'),[c,end],[rad*.40,.012],6,'secondary_branch',main)
 foliage('NeedleFan_'+name,base,u,w,length,width,lift,height,i*.73,main)
# A narrow, off-axis terminal crown integrates the leader; no separate levitating tip.
verts=[];n=9
for z,r,cx,cy in [(6.63,.39,.10,.04),(6.92,.69,.08,.035),(7.42,.45,.11,.03),(7.92,.22,.10,.045),(8.62,.007,.13,.04)]:
 for k in range(n):
  a=2*math.pi*k/n+.25;fac=1+.14*math.sin(k*2.4+z);verts.append((cx+r*fac*math.cos(a),cy+r*fac*math.sin(a),z+(.10*math.sin(a*3+.6) if z<7 else .025*math.cos(a))))
faces=[tuple(range(n-1,-1,-1)),tuple(range(4*n,5*n))]
for j in range(4):
 for k in range(n):q=(k+1)%n;faces.append((j*n+k,j*n+q,(j+1)*n+q,(j+1)*n+k))
mesh('Needles_TerminalLeader',verts,faces,'foliage','Trunk_MatureCentralLeader')
bpy.context.view_layer.update();triangles=0;checks=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);checks.append({'name':o.name,'role':o['component_role'],'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7
# Simple surface grounding evidence; no invented mechanical proof.
ground_checks=[]
for name in ground_parts:
 o=bpy.data.objects[name];contact=[v.co for v in o.data.vertices if abs(v.co.z)<1e-7]
 assert len(contact)>=3,(name,'missing finite ground contact')
 ground_checks.append({'part':name,'minimum_z_m':min(v.co.z for v in o.data.vertices),'ground_vertices':len(contact)})
# Component anchors document the original construction, while visual/independent QA verifies support.
geometry_fingerprint=hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in parts],sort_keys=True).encode()).hexdigest()
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
assert_render();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'origin':'trunk centre at ground Z=0; not bounds centre','components':checks,'ground_contacts':ground_checks,'support_design':support,
 'support_scope':'Named construction relationships plus visible primary/secondary branches; static visual support, not a physics or strength test.',
 'geometry_fingerprint_sha256':geometry_fingerprint,'native_saved_render_config':assert_render(),'status':'producer geometry check; independent gates pending'}
def save_qa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
save_qa()
if '--geometry-only' in sys.argv or '--no-render' in sys.argv:print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# Studio presentation is added only after clean native and runtime export.
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.32,.32,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.view_settings.view_transform='AgX';focus=Vector((.04,0,4.20))
def aim(o,p):o.location=p;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for n,p,e,s in [('Key',(-7,-10,15),2100,8),('Fill',(9,-3,8),1050,7),('Rim',(2,10,13),1700,6)]:
 bpy.ops.object.light_add(type='AREA',location=p);o=bpy.context.object;o.name='Preview_'+n;o.data.energy=e;o.data.shape='DISK';o.data.size=s;aim(o,p)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=10.35
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.22,.245,.24,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in mats.values():m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(11,-15,9),'gray-back3q':(-11,15,9)} if gray else {'thumbnail':(11,-15,9),'qa-front':(0,-15,4.2),'qa-side':(15,0,4.2),'qa-top':(.04,0,18),'qa-back':(0,15,4.2),'qa-wireframe':(11,-15,9)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.008;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(n,p)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);black.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for n,p in [('silhouette-128-front',(0,-15,4.2)),('silhouette-128-side',(15,0,4.2))]:render(n,p)
qa.update({'render_seconds':render_seconds,'render_configs':render_configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/runtime/schema gates pending'})
if not gray:
 files={}
 for role,n in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/n;files[role]={'path':f'assets/nature/{ASSET}/v{VERSION}/{n}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 meta={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'nature','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
save_qa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
