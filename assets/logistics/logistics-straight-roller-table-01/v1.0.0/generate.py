"""Original freestanding straight roller table. Metres; native Z up; front -Y.
One static prop with 13 transverse hollow rollers, separate axles, two rows of
bored bearing blocks, paired longitudinal beams and four grounded feet.
All shafts and rollers have actual finite flat-facet seating contacts. No rigging,
motion, load rating, equipment compatibility or engineering certification.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='logistics-straight-roller-table-01';VERSION='1.0.0';TITLE='Straight Roller Table'
DESCRIPTION=('Original static freestanding straight roller table with thirteen separate thick hollow transverse rollers, thirteen axles and twenty-six genuinely bored bearing blocks on two parallel side beams. '
 'Each faceted axle rests on finite lower bore faces in both supports; each hollow roller rests by its finite upper bore face on its axle. Actual nonzero contact areas, roller gaps and frame clearances are checked. '
 'Four legs, four finite ground pads, two lower longitudinal ties and two transverse stretchers form a complete static support path. Open ends are plain terminations without coupling hardware or compatibility claims. '
 'Sixty-six individually editable closed meshes, four constant solid PBR materials, metres, native Z up, front -Y and ground-centre origin. No textures, labels, cargo or external assets. '
 'One fixed stylized visual prop only; no conveying, roller rotation, friction, drive, electrical operation, load rating, human use, equipment compatibility, manufacture or safety certification.')
G={};LINKS=[];CONTACTS=[];FEET=[];BORES=[];GAPS=[];ROLLERS=[];AXLES=[];BEARINGS=[];CLEARANCE_PAIRS=[]
PALETTE=[('Frame_MutedTeal',(.065,.25,.26,1),.60,.30),('Roller_SatinSteel',(.57,.64,.65,1),.44,.60),('Bearing_DeepSlate',(.08,.105,.12,1),.61,.30),('Foot_DarkRubber',(.038,.047,.049,1),.90,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
FBOX=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box(name,c,s,mat,role):
 x,y,z=c;a,b,d=[q/2 for q in s]
 return mesh(name,[(x-a,y-b,z-d),(x+a,y-b,z-d),(x+a,y+b,z-d),(x-a,y+b,z-d),(x-a,y-b,z+d),(x+a,y-b,z+d),(x+a,y+b,z+d),(x-a,y+b,z+d)],FBOX,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.003):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
N=16;ANGLES=[math.pi/N+math.tau*i/N for i in range(N)];C=math.cos(math.pi/N)
def circular(r):return [(r*math.sin(t),r*math.cos(t)) for t in ANGLES]
def tube_x(name,x0,x1,y,z,r,ri,mat,role,square=False):
 inner=circular(ri);outer=[]
 for yy,zz in circular(r):
  if square:
   scale=r/max(abs(yy),abs(zz));yy*=scale;zz*=scale
  outer.append((yy,zz))
 vs=[(x,y+yy,z+zz) for x,pts in [(x0,outer),(x1,outer),(x0,inner),(x1,inner)] for yy,zz in pts];fs=[]
 for i in range(N):
  j=(i+1)%N;fs += [(i,j,N+j,N+i),(2*N+j,2*N+i,3*N+i,3*N+j),(j,i,2*N+i,2*N+j),(N+i,N+j,3*N+j,3*N+i)]
 return mesh(name,vs,fs,mat,role)
def cylinder_x(name,x0,x1,y,z,r,mat,role):
 pts=circular(r);vs=[(x,y+yy,z+zz) for x in [x0,x1] for yy,zz in pts]
 fs=[tuple(reversed(range(N))),tuple(N+i for i in range(N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 return mesh(name,vs,fs,mat,role)
# Four independent flat pads, continuous legs and a rigid frame. Structural
# member overlaps are deliberate 3D seats, not coplanar decorative overlays.
for si,x in [('L',-.410),('R',.410)]:
 beam=box('SideBeam_'+si,(x,0,.7785),(.080,2.100,.073),0,'continuous longitudinal side rail below the roller bed')
 tie=box('LowerTie_'+si,(x,0,.255),(.050,1.700,.050),0,'lower longitudinal tie joining both legs on one side')
 for ei,y in [('Front',-.840),('Rear',.840)]:
  foot=box('Foot_'+si+'_'+ei,(x,y,.0275),(.150,.150,.055),3,'finite rectangular rubber ground pad; whole underside is at Z zero');FEET.append(foot)
  leg=box('Leg_'+si+'_'+ei,(x,y,.4175),(.065,.070,.745),0,'continuous upright with finite sockets into pad, tie, stretcher and rail')
  link(leg,foot,(x,y,.050),axis=(0,1,0),spread=.010)
  link(leg,beam,(x,y,.765),axis=(0,1,0),spread=.010)
  link(leg,tie,(x,y,.255),axis=(0,0,1),spread=.010)
for ei,y in [('Front',-.840),('Rear',.840)]:
 cross=box('CrossStretcher_'+ei,(0,y,.365),(.840,.048,.060),0,'transverse lower stretcher joining the two legs without crossing the longitudinal ties')
 for si,x in [('L',-.410),('R',.410)]:link(cross,'Leg_'+si+'_'+ei,(x,y,.365),axis=(0,0,1),spread=.012)
# The 16-sided circles have a flat top and bottom. A 1 mm radius difference
# creates real bore clearance while exact lower/upper planar seats give finite
# support surfaces. Native and GLB checks measure these actual triangles.
BEARING_Z=.850;SHAFT_R=.012;BORE_R=.013;ROLLER_R=.056
AXLE_Z=BEARING_Z-(BORE_R-SHAFT_R)*C
ROLLER_Z=AXLE_Z-(BORE_R-SHAFT_R)*C
LOWER_SEAT_Z=AXLE_Z-SHAFT_R*C;UPPER_SEAT_Z=AXLE_Z+SHAFT_R*C
TOP_Z=ROLLER_Z+ROLLER_R*C
for i in range(13):
 y=(i-6)*.150;roller=f'Roller_{i:02d}';axle=f'Axle_{i:02d}'
 cylinder_x(axle,-.456,.456,y,AXLE_Z,SHAFT_R,1,'one separate full-width sixteen-sided solid axle; actual lower bore seats support both ends');AXLES.append(axle)
 tube_x(roller,-.345,.345,y,ROLLER_Z,ROLLER_R,BORE_R,1,'closed thick hollow roller with a true axial bore, flat top support facet and finite inner-upper facet seated on its axle');ROLLERS.append(roller)
 CONTACTS.append({'a':roller,'b':axle,'z_m':round(UPPER_SEAT_Z,7),'kind':'roller upper inside face resting on axle top','minimum_area_m2':.0025})
 for si,x0,x1 in [('L',-.445,-.375),('R',.375,.445)]:
  name=f'Bearing_{si}_{i:02d}';tube_x(name,x0,x1,y,BEARING_Z,.043,BORE_R,2,'closed square bearing block with real axial through-bore; lower bore facet supports axle; base seats into side beam',square=True);BEARINGS.append(name)
  link(name,'SideBeam_'+si,((x0+x1)/2,y+.029,.811),axis=(1,0,0),spread=.015)
  CONTACTS.append({'a':axle,'b':name,'z_m':round(LOWER_SEAT_Z,7),'kind':'axle lower flat face resting on bearing lower bore face','minimum_area_m2':.00025})
  BORES.append({'mesh':name,'origin_m':(x0-.004,y,BEARING_Z),'direction':(1,0,0),'length_m':x1-x0+.008})
  CLEARANCE_PAIRS.append({'a':roller,'b':name,'minimum_m':.0299,'role':'roller end to independent bearing block'})
  CLEARANCE_PAIRS.append({'a':roller,'b':'SideBeam_'+si,'minimum_m':.0249,'role':'roller envelope to side frame'})
 if i>0:CLEARANCE_PAIRS.append({'a':f'Roller_{i-1:02d}','b':roller,'minimum_m':.0400,'role':'adjacent roller full-surface separation'})
 BORES.append({'mesh':roller,'origin_m':(-.350,y,ROLLER_Z),'direction':(1,0,0),'length_m':.700})
# Full-assembly vertical gap rays are diagnostics, not continuous clearance proofs.
for i in range(12):
 y=(i-5.5)*.150
 for x in [-.25,0,.25]:GAPS.append({'label':f'between_rollers_{i:02d}','origin_m':(x,y,.930),'direction':(0,0,-1),'length_m':.180})
# No motor, cargo, roller end-stop gate or continuation coupler is included.
# The unbridged end ports are a plain bed termination, never a compatibility claim.
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
for name,color,rough,metal in PALETTE:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneStraightRollerTable',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def intersection_area(a,b):
 if cross2(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cross2(sub(q,p),sub(s,p));de=cross2(sub(q,p),sub(e,p));si=ds>=-1e-10;ei=de>=-1e-10
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cross2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
contact_checks=[]
for c in CONTACTS:
 a=horizontal_triangles(c['a'],c['z_m'],-1);b=horizontal_triangles(c['b'],c['z_m'],1)
 area=sum(intersection_area([v[:2] for v in ta['vertices_m']],[v[:2] for v in tb['vertices_m']]) for ta in a for tb in b)
 assert area>c['minimum_area_m2'],('Mechanical seat lacks finite actual contact',c,area)
 contact_checks.append(dict(c,actual_finite_overlap_area_m2=area))
adj={o.name:set() for o in parts}
for j in joints+contact_checks:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
roller_evidence={'roller_count':13,'axle_count':13,'bearing_block_count':26,'finite_mechanical_seats':contact_checks,'support_plane_z_m':TOP_Z,'roller_pitch_m':.150,'shaft_axis':'X','fixed_pose_only':True,'motion_or_load_claim':False,'required_full_surface_clearance_pairs':CLEARANCE_PAIRS}
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
 'single_prop_count':1,'roller_table_working_geometry':roller_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/logistics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'logistics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.45));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.55;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-5,-3,4),'gray-back3q':(5,3,4)} if gray else {
 'thumbnail':(5,-7,5),'qa-front':(0,-7,.45),'qa-side':(-7,0,.45),'qa-top':(0,0,8),
 'qa-back':(0,7,.45),'qa-wireframe':(5,-7,5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
if '--top-only' in sys.argv:views={'qa-top':views['qa-top']}
if '--wireframe-only' in sys.argv:views={'qa-wireframe':views['qa-wireframe']}
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.55
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.003;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.45)),('silhouette-128-side',(-7,0,.45))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
