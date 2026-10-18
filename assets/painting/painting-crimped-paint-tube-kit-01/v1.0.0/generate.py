"""Original crimped paint-tube kit, one static prop with three tubes.
Metres; native Z up; capped/open nozzle direction -Y. No branding or text.
Closed solid-wall tube shells, actual neck cavities, folded tails and screw-cap forms.
Self-contained; actual exported GLB is imported and compared before any render.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-crimped-paint-tube-kit-01';VERSION='1.0.0';TITLE='Crimped Paint Tube Kit'
DESCRIPTION=('One original static paint-tube kit counted as one prop: three differently compressed soft-metal tubes '
 'with integral sloping shoulders, modeled hollow necks, finite folded crimp tails and ribbed screw-cap forms. '
 'Two caps are fitted over the necks; the third tube is open with a real visible bore and blind internal cavity, '
 'and its separate cap rests upright on a finite annular rim beside the set. Muted blue, ochre and vermilion '
 'bands are assigned to the body faces, not duplicate overlay surfaces, brands or text labels. '
 'Each tube has a finite flat lower body facet and its crimp joins the solid tail region; all components are '
 'supported in one arranged rest pose. Nine named editable closed meshes, six constant solid PBR materials, '
 'metres, native Z up, front -Y and ground-centre origin. No paint-flow, squeezing, cap animation, '
 'chemical composition, usable quantity, sealing, toxicity, painting performance or manufacturing guarantee.')
G={};LINKS=[];FEET=[];OPENINGS=[];TUBESETS=[]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),6) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
def link(a,b,p,axis=(1,0,0),spread=.0006):LINKS.append((a,b,[tuple(p[i]+axis[i]*d for i in range(3)) for d in [-spread,0,spread]]))
def ring(x,y,z,rx,rz,n=24):
 return [(x+rx*math.sin(math.pi/n+math.tau*i/n),y,z+rz/math.cos(math.pi/n)*math.cos(math.pi/n+math.tau*i/n)) for i in range(n)]
def tube_shell(name,x,kind,colour):
 # y, horizontal radius, vertical half-height, centre-height, off-axis squeeze.
 # The rear is a solid squeezed tail; the inner wall stops before its crimp.
 compression=[1,.72,.86][kind]
 outer=[(.073,.0255,.0018,.0030,0),(.066,.0265,.0027,.0037,0),
 (.052,.0250,.0050,.0050,.0010*kind),(.033,.0255,.0105*compression,.0105*compression,-.0010*kind),
 (.020,.0250,.0120*compression,.0120*compression,0),(-.016,.0240,.0130*compression,.0130*compression,0),
 (-.029,.0230,.0120*compression,.0120*compression,.0007*kind),(-.043,.0210,.0110,.0130,0),
 (-.055,.0100,.0090,.0140,0),(-.059,.0090,.0090,.0140,0),
 (-.061,.0102,.0102,.0140,0),(-.063,.0090,.0090,.0140,0),
 (-.065,.0102,.0102,.0140,0),(-.067,.0090,.0090,.0140,0),
 (-.069,.0102,.0102,.0140,0),(-.071,.0090,.0090,.0140,0),(-.074,.0090,.0090,.0140,0)]
 inner=[(-.074,.0065,.0065,.0140,0),(-.055,.0065,.0065,.0140,0),
 (-.043,.0180,.0080,.0130,0),(-.029,.0200,.0080*compression,.0120*compression,.0007*kind),
 (-.016,.0210,.0090*compression,.0130*compression,0),(.020,.0220,.0080*compression,.0120*compression,0),
 (.033,.0220,.0065*compression,.0105*compression,-.0010*kind),(.048,.0200,.0017,.0055,.0010*kind),(.055,.0180,.0012,.0045,0)]
 n=24;profiles=outer+inner;vs=[v for y,rx,rz,z,dx in profiles for v in ring(x+dx,y,z,rx,rz,n)];fs=[tuple(reversed(range(n)))];fm=[0]
 for k in range(len(profiles)-1):
  # Integrated coloured wrap band on the existing shell faces; no extra layer.
  mid=(profiles[k][0]+profiles[k+1][0])/2;mat=colour if k<len(outer)-1 and -.029<=mid<=.020 else (1 if k<len(outer)-1 and .020<mid<.052 else 0)
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i));fm.append(mat)
 off=(len(profiles)-1)*n;fs.append(tuple(off+i for i in range(n)));fm.append(0)
 mesh(name,vs,fs,0,'closed soft-metal shell with blind interior cavity, squeezed tail, integral shoulder and threaded hollow neck',fm);FEET.append(name)
 return outer,inner

def crimp(name,x):
 p=[(.068,.0021),(.075,.0021),(.079,.0033),(.079,.0062),(.074,.0062),(.074,.0046),(.068,.0046)];n=len(p)
 vs=[(x+xx,y,z) for xx in [-.027,.027] for y,z in p]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh(name,vs,fs,0,'finite thick folded flat tail seam, embedded in the squeezed solid rear of the tube')

def cap(name,x,free=False):
 # Ribbed outer wall and a genuine blind threaded socket; open lip at -.060.
 # Axial knurl grooves are polygonal facets, not overlapping ribs or decals.
 n=48;profile=[(-.060,.0133),(-.063,.0140),(-.081,.0140),(-.084,.0127),(-.084,0),(-.0805,0),(-.0805,.0093),(-.060,.0093)]
 # Collapse the two axis loops to one vertex each, avoiding zero-area faces.
 vs=[];loops=[]
 for k,(y,r) in enumerate(profile):
  loop=[]
  for i in range(n if r else 1):
   a=math.pi/n+math.tau*i/n;rr=r*(.96 if r>.011 and k in [1,2] and i%4 in [1,2] else 1)
   xx=rr*math.sin(a);zz=.014+rr/math.cos(math.pi/n)*math.cos(a)
   v=(x+xx,y,zz) if not free else (x+xx,-.092+(zz-.014),-.060-y)
   loop.append(len(vs));vs.append(v)
  loops.append(loop)
 fs=[]
 for k in range(len(loops)):
  a,b=loops[k],loops[(k+1)%len(loops)]
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:fs.append((a[0],b[j],b[i]))
   elif len(b)==1:fs.append((a[i],a[j],b[0]))
   else:fs.append((a[i],a[j],b[j],b[i]))
 mesh(name,vs,fs,2,'closed ribbed screw-cap with a real blind socket; '+('separate upright cap resting on its annular open lip' if free else 'fitted around the neck with finite thread-ring engagement'))
 if free:FEET.append(name)

for kind,(label,x,colour) in enumerate([('Blue',-.063,3),('Ochre',0,4),('Vermilion',.063,5)]):
 p='Tube_'+label+'_';body=p+'Body';tail=p+'FoldedTail';lid=p+'Cap'
 outer,inner=tube_shell(body,x,kind,colour);crimp(tail,x);link(body,tail,(x,.071,.0032),spread=.0012)
 cap(lid,x if kind<2 else x+.017,free=kind==2)
 if kind<2:
  # Three neck ridges penetrate the inner cap wall only, away from exposed rims.
  link(body,lid,(x+.00955,-.065,.014),axis=(0,0,1),spread=.0006)
 TUBESETS.append({'label':label,'body':body,'tail':tail,'cap':lid,'cap_fitted':kind<2,'meshes':[body,tail,lid],'centre_x_m':x,'outer_profiles_y_rx_rz_z_dx':outer,'inner_profiles_y_rx_rz_z_dx':inner})
 if kind==2:
  OPENINGS.append({'tube':label,'mesh':body,'origin_m':[x,-.078,.014],'direction':[0,1,0],'length_m':.075,
   'probe_offsets_xz_m':[[0,0],[-.002,0],[.002,0],[0,-.002],[0,.002]],'bore_centre_m':[x,-.072,.014],'minimum_bore_span_m':.012,
   'description':'five clear rays through the open mouth into the blind tube cavity; not a tail-through passage'})
# Exact centred XY datum, same shift for all geometry and triangle witnesses.
allvs=[v for g in G.values() for v in g['vertices']];SHIFT=tuple(-(min(v[i] for v in allvs)+max(v[i] for v in allvs))/2 if i<2 else 0 for i in range(3))
for g in G.values():g['vertices']=[tuple(round(c,6) for c in add(v,SHIFT)) for v in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT) for p in ps]) for a,b,ps in LINKS]
for o in OPENINGS:
 for k in ['origin_m','bore_centre_m']:o[k]=list(add(o[k],SHIFT))
for t in TUBESETS:t['centre_x_m']+=SHIFT[0]
# BLENDER PHASE
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('SoftAluminium',(.62,.67,.69,1),.44,.66),('WarmPaperBody',(.81,.78,.67,1),.74,.03),('CharcoalCaps',(.052,.064,.067,1),.57,.05),('UltramarineBand',(.055,.19,.47,1),.68,.02),('YellowOchreBand',(.62,.36,.060,1),.70,.02),('VermilionBand',(.59,.12,.065,1),.68,.02)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('OneCrimpedPaintTubeKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Finite support and true openings are checked against actual generated mesh triangles.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00004,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
opening_checks=[]
for r in OPENINGS:
 rays=[]
 for dx,dz in r['probe_offsets_xz_m']:
  origin=Vector(r['origin_m'])+Vector((dx,0,dz));direction=Vector(r['direction'])
  blockers=[n for n,t in trees.items() if t.ray_cast(origin,direction,r['length_m'])[0] is not None]
  assert not blockers,('Blocked real paint tube bore',r['tube'],dx,dz,blockers)
  rays.append({'origin_m':list(origin),'direction':r['direction'],'length_m':r['length_m'],'blockers':blockers})
 spans=[]
 for axis in [(1,0,0),(0,0,1)]:
  origin=Vector(r['bore_centre_m']);pos=trees[r['mesh']].ray_cast(origin,Vector(axis),.04)[0];neg=trees[r['mesh']].ray_cast(origin,-Vector(axis),.04)[0]
  assert pos is not None and neg is not None
  span=(pos-neg).length;assert span>r['minimum_bore_span_m']
  spans.append({'axis':axis,'negative_hit_m':list(neg),'positive_hit_m':list(pos),'opening_span_m':span})
 opening_checks.append(dict(r,actual_clear_rays=rays,actual_inner_surface_spans=spans))
# Geometry-altering negative: shifting a folded tail breaks its measured attachment.
negative=[]
for a,b,points in LINKS:
 if not b.endswith('FoldedTail'):continue
 o=byname[b];delta=Vector((0,0,.02));moved=BVHTree.FromPolygons([o.matrix_world@v.co+delta for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 failures=sum(not inside(moved,p) for p in points);assert failures==3
 negative.append({'displaced_mesh':b,'translation_m':list(delta),'support':a,'failed_anchor_count':failures})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<12000
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'No procedural or image texture nodes permitted'
 assert not any(socket.is_linked for socket in p.inputs),'No linked Principled inputs permitted'
 values=[]
 for name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight','Coat Roughness','Sheen Weight','Emission Color','Emission Strength']:
  value=p.inputs[name].default_value
  values.append((name,tuple(round(float(x),6) for x in value) if hasattr(value,'__len__') else round(float(value),6)))
 values.append(('double_sided',not m.use_backface_culling));return tuple(values)
def records(objects):
 rows=[]
 for o in objects:
  o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices]
  for t in o.data.loop_triangles:
   q=[tuple(round(float(c),6) for c in vs[i]) for i in t.vertices]
   rows.append((min(tuple(q[i:]+q[:i]) for i in range(3)),pbr(o.data.materials[t.material_index])))
 return sorted(rows)
source_records=records(parts);source_fp=hashlib.sha256(json.dumps(source_records,separators=(',',':')).encode()).hexdigest()
mesh_count=len(parts);bpy.ops.object.select_all(action='DESELECT')
for o in parts+[root]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_ground':sorted(seen),
 'single_kit_prop_count':1,'tube_sets':TUBESETS,'actual_open_neck_cavity':opening_checks,'displaced_folded_tail_negative':negative,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/painting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'painting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# Every formal/early render is of the actual exported file imported into an emptied scene.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((0,0,.014));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.255;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3,-4,6),'gray-back3q':(-3,4,6)} if gray else {
 'thumbnail':(3,-4,6),'qa-front':(0,-7,.014),'qa-side':(7,0,.014),'qa-top':(0,0,8),
 'qa-back':(0,7,.014),'qa-wireframe':(3,-4,6)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.255
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00012;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.014)),('silhouette-128-side',(7,0,.014))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
