"""Original open divided postal satchel, one fixed static pose.
Metres, Z up; flat ground-centre origin; presentation front -Y.
Self-contained source. No textures, letters, external assets or animation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='postal-divided-mail-satchel-01';VERSION='1.0.0';TITLE='Open Divided Mail Satchel'
DESCRIPTION=('One original static postal satchel with a genuine open thick-walled tapered shell, visible finite cavity floors and one solid divider forming two empty mail compartments. '
 'A wide rear-attached flap is held in one raised pose. A continuous thick single shoulder strap has two individually seated side anchors and brass rivets. '
 'Eight named closed editable meshes have measured support connections to a finite flat base; both cavities and the shoulder opening have actual full-assembly clear rays. '
 'Four constant solid PBR materials, metre scale, native Z up, ground-centre origin and presentation front -Y. No textures, logos, letters or external assets. '
 'One visual prop only; no capacity, load, human fit, postal specification, weatherproofing, soft-body, opening or carrying animation, manufacture or safety claim.')
G={};LINKS=[];FEET=['Body_OpenThickShell'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];DIVIDER_PROBES=[]
PALETTE=[('Canvas_Petrol',(.055,.205,.255,1),.83,0),('Lining_Ochre',(.54,.34,.16,1),.88,0),('Leather_Chestnut',(.22,.075,.032,1),.72,0),('Rivet_Brass',(.53,.32,.10,1),.40,.65)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def poly_y(name,outline,y0,y1,mat,role):
 k=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def revolve(name,profile,centre,axis,u,mat,role,n=20):
 v=cross(axis,u);vs=[add(centre,add(mul(axis,t),add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n))))) for t,r in profile for i in range(n)];fs=[]
 for j in range(len(profile)-1):
  for i in range(n):ii=(i+1)%n;fs.append((j*n+i,j*n+ii,(j+1)*n+ii,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
def octagon(x,y,c):return [(-x,-y+c),(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c)]
# A closed shell surface runs up the outside, across the true rim, down the inside,
# then across the interior floor. There is no top cap and no dark fake cavity.
RINGS=[(0,.200,.082,.022),(.025,.212,.094,.024),(.295,.224,.104,.025),(.295,.211,.091,.023),(.019,.196,.076,.020)]
vs=[(x,y,z) for z,rx,ry,c in RINGS for x,y in octagon(rx,ry,c)];fs=[tuple(reversed(range(8)))];fm=[2]
for j in range(4):
 for i in range(8):q=(i+1)%8;fs.append((j*8+i,j*8+q,(j+1)*8+q,(j+1)*8+i));fm.append([2,0,2,1][j])
fs.append(tuple(32+i for i in range(8)));fm.append(1)
mesh('Body_OpenThickShell',vs,fs,0,'one continuous closed material shell with actual inner walls, 19 mm interior floor, open mouth and broad Z=0 underside')
G['Body_OpenThickShell']['face_materials']=fm
# Separator has finite thickness and is buried into the floor and both end walls.
DIVIDER=[(-.199,.012),(.199,.012),(.215,.260),(.207,.270),(-.207,.270),(-.215,.260)]
poly_y('Divider_TwoMailCompartments',DIVIDER,-.0045,.0045,1,'solid 9 mm separator; 25 mm below the rim; continuous floor and end-wall seating')
link('Divider_TwoMailCompartments','Body_OpenThickShell',(0,0,.0155),axis=(1,0,0),spread=.090)
for s in [-1,1]:link('Divider_TwoMailCompartments','Body_OpenThickShell',(s*.211,0,.245),axis=(0,1,0),spread=.0015)
# Broad canvas flap is shown already lifted. It is a single thick slab with a
# sloping front lining and backshell, directly embedded across the rear wall.
FLAP=[(-.205,.280),(.205,.280),(.205,.477),(.190,.505),(-.190,.505),(-.205,.477)]
k=len(FLAP);vs=[(x,.100+(z-.280)*.48+d,z) for d in [-.005,.005] for x,z in FLAP]
fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
mesh('Flap_RaisedWideCover',vs,fs,0,'finite 10 mm Y-thick wide cover, rear attached in one static raised pose; not animated')
G['Flap_RaisedWideCover']['face_materials']=[1,0]+[2]*k
link('Flap_RaisedWideCover','Body_OpenThickShell',(0,.100,.285),axis=(1,0,0),spread=.14)
# Continuous U-section shoulder band. Its real two ends meet the two side anchors.
# Width is along Y, thickness lies in XZ; the central opening is not painted.
outer=[(-.246,.247)]+[(.246*math.cos(math.pi-i*math.pi/24),.380+.246*math.sin(math.pi-i*math.pi/24)) for i in range(25)]+[(.246,.247)]
inner=[(.238,.247)]+[(.238*math.cos(i*math.pi/24),.380+.238*math.sin(i*math.pi/24)) for i in range(25)]+[(-.238,.247)]
poly_y('Strap_ContinuousSingleShoulder',outer+inner,-.020,.020,2,'one continuous 40 mm wide, 8 mm thick shoulder strap with two anchored terminals and a true open arch')
for s,label in [(-1,'Left'),(1,'Right')]:
 outline=[(s*.217,.224),(s*.243,.224),(s*.247,.231),(s*.247,.271),(s*.241,.279),(s*.217,.279)]
 poly_y('Anchor_'+label,outline,-.032,.032,2,'separate finite side reinforcement embedded into shell and into shoulder-band terminal')
 link('Anchor_'+label,'Body_OpenThickShell',(s*.220,0,.250),axis=(0,1,0),spread=.018)
 link('Strap_ContinuousSingleShoulder','Anchor_'+label,(s*.242,0,.259),axis=(0,1,0),spread=.012)
 revolve('Rivet_'+label,[(0,.0048),(.0105,.0048),(.0105,.0070),(.0145,.0070),(.0155,.0055)],(s*.237,0,.259),(s,0,0),(0,1,0),3,'solid brass rivet stem seated into each shoulder anchor',n=20)
 link('Rivet_'+label,'Anchor_'+label,(s*.240,0,.259),axis=(0,1,0),spread=.002)
# Each cavity is empty from above the rim to 1 mm above its real floor.
for label,y in [('front',-.045),('rear',.045)]:
 for x in [-.14,0,.14]:
  GAPS.append({'label':'open_'+label+'_mail_cavity','origin_m':[x,y,.355],'direction':[0,0,-1],'length_m':.335})
  FLOOR_PROBES.append({'label':label+'_floor','origin_m':[x,y,.355],'direction':[0,0,-1],'length_m':.38,'mesh':'Body_OpenThickShell'})
for x,z in [(-.12,.560),(0,.570),(.12,.560)]:GAPS.append({'label':'shoulder_arch_through_clearance','origin_m':[x,-.15,z],'direction':[0,1,0],'length_m':.40})
for side in [-1,1]:WALL_PROBES.append({'label':'front_wall' if side<0 else 'rear_wall','origin_m':[0,side*.15,.180],'direction':[0,-side,0],'length_m':.10,'mesh':'Body_OpenThickShell'})
for x in [-.14,0,.14]:
 for z in [.10,.22]:DIVIDER_PROBES.append({'label':'two_cavities_separated','origin_m':[x,-.060,z],'direction':[0,1,0],'length_m':.12,'mesh':'Divider_TwoMailCompartments'})
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
root=bpy.data.objects.new('OneDividedMailSatchel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual closed-shell hit sequences prove cavity floors, wall thickness and separator.
def ray_sequence(tree,probe):
 p=Vector(probe['origin_m']);d=Vector(probe['direction']).normalized();remaining=probe['length_m'];hits=[]
 for _ in range(20):
  q,_,_,distance=tree.ray_cast(p,d,remaining)
  if q is None:break
  hits.append(list(q));advance=distance+1e-5;p=q+d*1e-5;remaining-=advance
 else:raise AssertionError('Unexpected long ray sequence')
 return hits
floor_checks=[]
for probe in FLOOR_PROBES:
 hits=ray_sequence(trees[probe['mesh']],probe);assert len(hits)==2,(probe,hits)
 assert abs(hits[0][2]-.019)<1e-6 and abs(hits[1][2])<1e-6,(probe,hits)
 floor_checks.append(dict(probe,actual_intersections_m=hits,actual_floor_thickness_m=hits[0][2]-hits[1][2]))
wall_checks=[]
for probe in WALL_PROBES:
 hits=ray_sequence(trees[probe['mesh']],probe);assert len(hits)==2,(probe,hits)
 thickness=(Vector(hits[0])-Vector(hits[1])).length;assert .012<thickness<.017
 wall_checks.append(dict(probe,actual_intersections_m=hits,actual_thickness_along_ray_m=thickness))
divider_checks=[]
for probe in DIVIDER_PROBES:
 hits=ray_sequence(trees[probe['mesh']],probe);assert len(hits)==2 and abs(hits[0][1]+.0045)<1e-6 and abs(hits[1][1]-.0045)<1e-6,(probe,hits)
 divider_checks.append(dict(probe,actual_intersections_m=hits,actual_divider_thickness_m=hits[1][1]-hits[0][1]))
# Uniform-volume centroid is reported only as a geometric support check, not a load rating.
volume_sum=0;centroid_sum=Vector((0,0,0))
for o in parts:
 for tri in o.data.loop_triangles:
  a,b,c=[o.matrix_world@o.data.vertices[i].co for i in tri.vertices];vv=a.dot(b.cross(c))/6
  volume_sum+=vv;centroid_sum+=(a+b+c)*(vv/4)
centroid=centroid_sum/volume_sum;assert abs(centroid.x)<.16 and abs(centroid.y)<.06
satchel_evidence={'open_compartment_count':2,'interior_floor_rays':floor_checks,'wall_thickness_rays':wall_checks,'divider_crossing_rays':divider_checks,'uniform_volume_centroid_m':list(centroid),'centroid_projection_within_finite_base':True,'static_display_only':True,'capacity_or_softbody_or_animation_claim':False}
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
 'single_prop_count':1,'satchel_working_geometry':satchel_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/postal/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'postal','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.035,.300));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.780;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,7),'gray-back3q':(3,5,7)} if gray else {
 'thumbnail':(-3,-5,7),'qa-front':(0,-7,.300),'qa-side':(7,0,.300),'qa-top':(0,0,8),
 'qa-back':(0,7,.300),'qa-wireframe':(-3,-5,7)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.780
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00030;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.300)),('silhouette-128-side',(7,0,.300))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
