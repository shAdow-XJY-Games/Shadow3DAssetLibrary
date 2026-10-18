"""Original open-throat carpentry hand plane. Static visual tool, not cutting equipment.
Metres, Z up; ground-centre origin; toe/cutting direction -X; presentation front -Y.
Self-contained source; renders use a fresh actual GLB import and full solid-PBR guard.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carpentry-open-throat-hand-plane-01';VERSION='1.0.0';TITLE='Open-Throat Carpenter Hand Plane'
DESCRIPTION=('One original static hand-plane prop with a finite flat steel sole and a real through-mouth, paired seafoam cast cheeks, '
 'a separate 45-degree iron supported by an inclined frog, a brass lever cap and seated pressure screw, turned walnut toe knob and a closed wooden rear tote with a true hand opening. '
 'Ten independently named closed editable meshes have measured interior-witness connections to the sole. Nine unobstructed full-assembly rays pass through the working mouth; three pass through the tote opening. '
 'The blunt display edge remains at least 2 mm above the ground plane in the supplied static pose. Metres, Z up, ground-centre origin, toe -X, presentation front -Y. '
 'Four solid PBR materials without textures, markings, branding or external assets. One visual tool only; no cutting, sharpening, adjustment, disassembly, ergonomics, accuracy, manufacture or tool-safety guarantee.')
G={};LINKS=[];FEET=['Sole_ThroughMouth'];BORES=[];GAPS=[]
PALETTE=[('Machined_Steel',(.32,.39,.40,1),.39,.72),('Body_Seafoam',(.12,.28,.23,1),.65,.30),('LeverCap_Brass',(.53,.32,.10,1),.43,.62),('Grip_Walnut',(.26,.095,.030,1),.64,0)]
T=(math.sqrt(.5),0,math.sqrt(.5));N=(-math.sqrt(.5),0,math.sqrt(.5));EDGE=(-.012,0,.0025)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def bladepoint(t,n=0,y=0):return add(EDGE,add(mul(T,t),add(mul(N,n),(0,y,0))))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def poly_y(name,outline,y0,y1,mat,role):
 k=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def band(name,outer,inner,levels,world,mat,role):
 assert len(outer)==len(inner);k=len(outer)
 vs=[world(p,a) for a in levels for poly in [outer,inner] for p in poly];fs=[]
 for i in range(k):
  j=(i+1)%k
  fs.extend([(i,j,k+j,k+i),(2*k+i,3*k+i,3*k+j,2*k+j),(i,2*k+i,2*k+j,j),(k+i,k+j,3*k+j,3*k+i)])
 return mesh(name,vs,fs,mat,role)
def revolve(name,profile,centre,axis,u,mat,role,n=24):
 v=cross(axis,u);vs=[add(centre,add(mul(axis,t),add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n))))) for t,r in profile for i in range(n)];fs=[]
 for j in range(len(profile)-1):
  for i in range(n):ii=(i+1)%n;fs.append((j*n+i,j*n+ii,(j+1)*n+ii,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
# A single closed annular plate. The through-mouth has side walls and no cap or decal.
OUTER=[(-.140,-.031),(-.134,-.037),(.134,-.037),(.140,-.031),(.140,.031),(.134,.037),(-.134,.037),(-.140,.031)]
MOUTH=[(-.030,-.024),(-.028,-.026),(-.004,-.026),(-.002,-.024),(-.002,.024),(-.004,.026),(-.028,.026),(-.030,.024)]
band('Sole_ThroughMouth',OUTER,MOUTH,[0,.009],lambda p,z:(p[0],p[1],z),0,'one closed annular steel sole; finite ground face, actual through-mouth')
# Paired profiled cheeks stay outside the open cutting passage.
CHEEK=[(-.126,.0065),(.126,.0065),(.128,.014),(.121,.024),(.055,.030),(.025,.042),(-.040,.034),(-.090,.027),(-.126,.016)]
for sign,label in [(-1,'Near'),(1,'Far')]:
 a,b=sorted([sign*.0285,sign*.0355]);poly_y('Body_'+label+'Cheek',CHEEK,a,b,1,'cast cheek with shallow buried foot and raised profile; leaves a wide open centre')
 link('Body_'+label+'Cheek','Sole_ThroughMouth',(.015,sign*.032,.0077),axis=(1,0,0),spread=.018)
# A real closed wedge supports the iron on its sloping face z=x+0.013.
poly_y('Frog_InclinedBed',[(.002,.006),(.047,.006),(.047,.060),(.002,.015)],-.023,.023,1,'45-degree frog wedge anchored through its foot into sole, supporting separate iron')
link('Frog_InclinedBed','Sole_ThroughMouth',(.025,0,.0075),spread=.012)
# Blunt visual edge, fully above the ground: n is iron-normal, t runs up the blade.
IRON_TN=[(0,-.0005),(.004,-.0018),(.108,-.0018),(.108,.0018),(.004,.0018),(0,.0005)]
poly_y('Blade_PlaningIron',[(bladepoint(t,n)[0],bladepoint(t,n)[2]) for t,n in IRON_TN],-.0245,.0245,0,'independent inclined blade with a modeled bevel and finite blunt display edge above the sole datum')
link('Blade_PlaningIron','Frog_InclinedBed',bladepoint(.045,-.00145),spread=.012)
CAP_TN=[(.014,.0010),(.083,.0010),(.083,.0040),(.077,.0060),(.020,.0060),(.014,.0042)]
poly_y('Clamp_LeverCap',[(bladepoint(t,n)[0],bladepoint(t,n)[2]) for t,n in CAP_TN],-.0195,.0195,2,'solid brass pressure cap with shallow modeled seating into the iron, no motion claim')
link('Clamp_LeverCap','Blade_PlaningIron',bladepoint(.052,.0014),spread=.010)
revolve('Clamp_PressureScrew',[(.0048,.0030),(.0095,.0030),(.0095,.0060),(.0130,.0060),(.0142,.0048)],bladepoint(.061),N,(0,1,0),0,'faceted pressure screw embedded into cap, axial head and stem',n=20)
link('Clamp_PressureScrew','Clamp_LeverCap',bladepoint(.061,.0054),spread=.0010)
# Turned front knob with seated top screw. No disconnected rings or decorative overlays.
revolve('Grip_FrontKnob',[(.0065,.011),(.013,.014),(.021,.011),(.038,.020),(.050,.021),(.059,.015),(.062,.008)],(-.094,0,0),(0,0,1),(1,0,0),3,'turned solid walnut front grasp knob, stem embedded into sole',n=28)
link('Grip_FrontKnob','Sole_ThroughMouth',(-.094,0,.0077),spread=.005)
revolve('Fastener_KnobScrew',[(.060,.0040),(.063,.0040),(.0645,.0032)],(-.094,0,0),(0,0,1),(1,0,0),0,'plain seated knob fastener head; not a painted disc',n=16)
link('Fastener_KnobScrew','Grip_FrontKnob',(-.094,0,.061),spread=.0012)
# Closed ring tote is authored directly with corresponding outer and inner loops.
TOTE_OUTER=[(.059,.0068),(.120,.0068),(.128,.025),(.121,.066),(.107,.099),(.089,.119),(.065,.116),(.058,.100),(.072,.078),(.078,.043)]
TOTE_INNER=[(.079,.027),(.106,.027),(.111,.037),(.106,.063),(.096,.088),(.086,.100),(.074,.101),(.073,.096),(.087,.073),(.092,.043)]
band('Grip_RearOpenTote',TOTE_OUTER,TOTE_INNER,[-.0105,.0105],lambda p,y:(p[0],y,p[1]),3,'one closed walnut rear tote with true hand opening, wide foot embedded into sole')
link('Grip_RearOpenTote','Sole_ThroughMouth',(.095,0,.0078),spread=.005)
# Vertical rays pass from below the sole through the assembled mouth to open air.
for x in [-.026,-.022,-.018]:
 for y in [-.018,0,.018]:GAPS.append({'label':'working_throat','origin_m':[x,y,-.008],'direction':[0,0,1],'length_m':.125})
for x,z in [(.098,.050),(.096,.070),(.083,.096)]:GAPS.append({'label':'rear_tote_hand_opening','origin_m':[x,-.045,z],'direction':[0,1,0],'length_m':.090})
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
root=bpy.data.objects.new('OneOpenThroatHandPlane',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual edge clearance and two width-spanning tip vertices locate the iron inside its mouth.
blade=byname['Blade_PlaningIron'];bv=[blade.matrix_world@v.co for v in blade.data.vertices]
minimum_edge=min(v.z for v in bv);assert minimum_edge>.002
edge_vertices=[list(v) for v in bv if v.z<.0030];assert len(edge_vertices)==4
assert all(-.030<v[0]<-.008 and abs(v[1])<.026 for v in edge_vertices)
# Complete actual blade/sole disjointness: all actual edges in both directions plus all vertices.
# A blade can fit at its lowest points but intersect the rear mouth wall above them.
blade_sole_checks=[]
for first,second in [('Blade_PlaningIron','Sole_ThroughMouth'),('Sole_ThroughMouth','Blade_PlaningIron')]:
 obj=byname[first];verts=[obj.matrix_world@v.co for v in obj.data.vertices];tree=trees[second]
 contained=[i for i,p in enumerate(verts) if inside(tree,p)]
 crossings=[]
 for e in obj.data.edges:
  a,b=[verts[i] for i in e.vertices];delta=b-a
  hit=tree.ray_cast(a,delta.normalized(),delta.length)[0]
  if hit is not None:crossings.append(list(e.vertices))
 nearest_clearance=min(tree.find_nearest(p)[3] for p in verts)
 assert not contained and not crossings and nearest_clearance>.0003,('Iron intersects rear mouth',first,second,contained,crossings,nearest_clearance)
 blade_sole_checks.append({'from_mesh':first,'to_mesh':second,'vertices_tested':len(verts),'edges_tested':len(obj.data.edges),'contained_vertices':contained,'edge_surface_crossings':crossings,'minimum_vertex_surface_clearance_m':nearest_clearance})
plane_evidence={'blade_slope_degrees':45,'minimum_actual_blade_z_m':minimum_edge,'blunt_edge_vertices_m':edge_vertices,'toe_direction_world':[-1,0,0],'ground_datum_m':0,'complete_iron_sole_disjointness':blade_sole_checks,'through_mouth_clear_rays':9,'tote_clear_rays':3,'only_checked_pose':'static assembled display; no adjustment range or cutting performance'}
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
 'single_prop_count':1,'hand_plane_working_geometry':plane_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carpentry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.050));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.350;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-6,3.8),'gray-back3q':(3,6,3.8)} if gray else {
 'thumbnail':(-3,-6,3.8),'qa-front':(0,-7,.050),'qa-side':(7,0,.050),'qa-top':(0,0,8),
 'qa-back':(0,7,.050),'qa-wireframe':(-3,-6,3.8)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.350
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
 for name,pos in [('silhouette-128-front',(0,-7,.050)),('silhouette-128-side',(7,0,.050))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
