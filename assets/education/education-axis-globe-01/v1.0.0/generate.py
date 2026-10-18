"""Original stylized desktop axis globe. One static prop, not geographic reference.
Metres, native Z up. Sphere centred on C, axis tilted 23.5 degrees toward +X.
Self-contained source; renders use a fresh actual GLB import with full solid-PBR guard.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='education-axis-globe-01';VERSION='1.0.0';TITLE='Tilted-Axis Classroom Globe'
DESCRIPTION=('One original static stylized desktop globe with a closed faceted spherical shell, simplified continent-shaped material regions on the same shell, '
 'a 23.5-degree tilted polar axis, two separate pole pins and genuinely bored bearing sleeves, a thick open meridian ring, short turned column and finite flat circular base. '
 'Eight named closed editable meshes form an actual interior-witness support chain from the globe to the base; the spherical surface has measured clearance from the meridian frame. '
 'The globe has its own centre pivot and explicit polar-axis direction. Only the supplied static orientation is checked; no rotation range or controller is promised. '
 'Metres, native Z up, ground-centre origin, front -Y. Five solid PBR materials, no textures, markings, labels or external assets. '
 'Simplified sea/land regions are visual illustration, not accurate geographic, navigation, astronomical or measurement data; no teaching outcome or product-safety claim.')
G={};LINKS=[];FEET=['Stand_WeightedBase'];BORES=[];GAPS=[]
C=(0,0,.315);TILT=math.radians(23.5);AXIS=(math.sin(TILT),0,math.cos(TILT));U=(math.cos(TILT),0,-math.sin(TILT));V=(0,1,0);R=.160
PALETTE=[('Ocean_Blue',(.035,.235,.33,1),.62,0),('Continents_Sage',(.43,.54,.24,1),.75,0),('Polar_Ivory',(.78,.76,.60,1),.79,0),('Meridian_Brass',(.48,.29,.10,1),.42,.65),('Stand_Walnut',(.24,.095,.032,1),.66,.02)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def length(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/length(a))
def world(t,u=0,v=0):return add(C,add(mul(AXIS,t),add(mul(U,u),mul(V,v))))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def revolve(name,profile,centre,axis,u,mat,role,n=32,closed=False):
 v=cross(axis,u);vs=[add(centre,add(mul(axis,t),add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n))))) for t,r in profile for i in range(n)]
 fs=[]
 for j in range(len(profile) if closed else len(profile)-1):
  k=(j+1)%len(profile)
  for i in range(n):ii=(i+1)%n;fs.append((j*n+i,j*n+ii,k*n+ii,k*n+i))
 if not closed:fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
# A shared closed sphere carries sea, land and polar material regions: no overlay shells.
CONTINENTS=[
 [(-168,66),(-145,72),(-125,61),(-106,73),(-62,58),(-53,48),(-74,44),(-83,24),(-97,16),(-104,25),(-118,31),(-126,48),(-153,57)],
 [(-81,11),(-65,10),(-49,-3),(-35,-8),(-42,-24),(-55,-39),(-69,-55),(-75,-40),(-80,-16),(-73,-2)],
 [(-17,34),(2,37),(21,33),(34,30),(43,11),(51,11),(42,-14),(30,-34),(17,-35),(9,-18),(-1,4),(-16,14)],
 [(-10,36),(-6,49),(9,54),(12,67),(29,71),(42,62),(65,72),(96,76),(133,69),(166,58),(155,48),(136,34),(122,23),(109,7),(99,10),(88,24),(77,8),(69,23),(47,30),(37,43),(25,42),(18,37),(8,44),(0,39)],
 [(112,-11),(129,-12),(141,-10),(153,-24),(146,-39),(131,-33),(115,-35),(111,-22)],
 [(-55,60),(-42,61),(-21,72),(-29,82),(-53,82),(-65,69)],
 [(46,-13),(50,-16),(48,-25),(44,-24)],
 [(130,31),(138,36),(142,43),(146,43),(142,35),(134,30)],
 [(166,-35),(173,-40),(177,-45),(170,-44),(164,-40)],
 [(98,4),(108,0),(118,-5),(128,-4),(130,-8),(113,-9),(103,-6)]]
def polygon_has(p,poly):
 x,y=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def land(lon,lat):
 if lat< -70 or polygon_has((lon,lat),CONTINENTS[5]):return 2
 return 1 if any(polygon_has((lon,lat),p) for p in CONTINENTS) else 0
N=64;M=32;vs=[world(-R)];angles=[None];fs=[];fm=[]
for j in range(1,M):
 lat=-math.pi/2+math.pi*j/M
 for i in range(N):
  lon=-math.pi+math.tau*i/N
  # Longitude zero points toward -Y; +longitude turns toward +X before polar tilt.
  vs.append(world(R*math.sin(lat),R*math.cos(lat)*math.sin(lon),-R*math.cos(lat)*math.cos(lon)));angles.append((math.degrees(lon),math.degrees(lat)))
top=len(vs);vs.append(world(R));angles.append(None)
for i in range(N):fs.append((0,1+(i+1)%N,1+i));fm.append(2)
for j in range(M-2):
 for i in range(N):
  a=1+j*N+i;b=1+j*N+(i+1)%N;c=b+N;d=a+N;fs.append((a,b,c,d));fm.append(land(-180+360*(i+.5)/N,-90+180*(j+1.5)/M))
for i in range(N):fs.append((1+(M-2)*N+i,1+(M-2)*N+(i+1)%N,top));fm.append(0)
mesh('Globe_Surface',vs,fs,0,'single closed spherical sea-land shell, simplified geography as mutually exclusive face regions');G['Globe_Surface']['face_materials']=fm
# Beveled solid meridian ring with an empty interior. It lies in XZ, not a flat disc.
profile=[(-.010,.1855),(-.0085,.184),(.0085,.184),(.010,.1855),(.010,.2005),(.0085,.202),(-.0085,.202),(-.010,.2005)]
revolve('Frame_MeridianRing',profile,C,(0,1,0),(1,0,0),3,'closed thick annular meridian frame with genuine central opening',n=72,closed=True)
# Real bored sleeves and solid pins share one explicit polar axis, one static press-fit pose.
for sign,label in [(1,'North'),(-1,'South')]:
 ax=mul(AXIS,sign);origin=world(sign*.1885)
 revolve('Bearing_'+label+'Sleeve',[(-.0155,.016),(-.0135,.018),(.0135,.018),(.0155,.016),(.0155,.0060),(-.0155,.0060)],origin,ax,U,3,'closed annular bearing sleeve; isolated axial bore is open, installed pin occupies it',n=32,closed=True)
 revolve('Axis_'+label+'Pin',[(.148,.0065),(.2045,.0065),(.2045,.011),(.213,.011),(.216,.008)],C,ax,U,3,'solid polar pin embedded in globe and bearing, with an outer retaining head',n=24)
 link('Globe_Surface','Axis_'+label+'Pin',world(sign*.154),axis=U,spread=.0012)
 # Three axially spread points in a narrow intentional press-fit overlap, not a free bearing clearance claim.
 link('Axis_'+label+'Pin','Bearing_'+label+'Sleeve',world(sign*.1885,0,.0062),axis=ax,spread=.003)
 link('Bearing_'+label+'Sleeve','Frame_MeridianRing',world(sign*.190,0,.0080),axis=U,spread=.003)
 BORES.append({'mesh':'Bearing_'+label+'Sleeve','origin_m':list(add(origin,mul(ax,-.020))),'direction':list(ax),'length_m':.040,'scope':'isolated sleeve bore; the installed solid pin intentionally occupies and slightly embeds into this bore'})
revolve('Stand_Column',[(.025,.028),(.044,.028),(.051,.021),(.119,.021),(.133,.026)],(0,0,0),(0,0,1),(1,0,0),4,'short turned column embedded into base and lower meridian frame',n=24)
revolve('Stand_WeightedBase',[(0,.112),(.006,.125),(.021,.125),(.033,.112),(.037,.061)],(0,0,0),(0,0,1),(1,0,0),4,'one solid circular base with a finite flat ground face; name denotes visual form only, not rated mass',n=48)
link('Frame_MeridianRing','Stand_Column',(0,0,.124),axis=(1,0,0),spread=.006)
link('Stand_Column','Stand_WeightedBase',(0,0,.031),axis=(1,0,0),spread=.010)
# Full-assembly rays in the visible sphere/frame gap, excluding the two occupied pole joints.
for angle in [0,30,60,90,120,180,210,240,270,300]:
 a=math.radians(angle);p=add(C,(.173*math.cos(a),-.040,.173*math.sin(a)))
 # Omit rays close to either pole bearing, which is meant to bridge this opening.
 if abs(dot(sub(add(p,(0,.040,0)),C),AXIS))>.168:continue
 GAPS.append({'origin_m':list(p),'direction':[0,1,0],'length_m':.080})
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
root=bpy.data.objects.new('OneTiltedAxisGlobe',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 if name=='Globe_Surface':
  for v in me.vertices:v.co-=Vector(C)
  o.location=C;o['polar_axis_world']=list(AXIS);o['pivot_world_m']=list(C);o['checked_static_angle_degrees']=0.0
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
 assert hit is None,('Bearing sleeve bore capped',r)
 bore_checks.append(dict(r,actual_isolated_sleeve_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Sphere to meridian gap blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
# Measure actual shell vertices against the actual ring, in both directions.
clearances=[trees['Frame_MeridianRing'].find_nearest(o.matrix_world@v.co)[3] for o in [byname['Globe_Surface']] for v in o.data.vertices]
clearances += [trees['Globe_Surface'].find_nearest(o.matrix_world@v.co)[3] for o in [byname['Frame_MeridianRing']] for v in o.data.vertices]
minimum_gap=min(clearances);assert minimum_gap>.022
sphere=byname['Globe_Surface'];radii=[(sphere.matrix_world@v.co-Vector(C)).length for v in sphere.data.vertices];assert max(abs(r-R) for r in radii)<2e-6
axis_evidence={'centre_m':C,'direction_world':AXIS,'tilt_degrees':23.5,'only_checked_display_angle_degrees':0,'sphere_vertex_radius_range_m':[min(radii),max(radii)],'sphere_ring_actual_vertex_surface_clearance_m':minimum_gap,'sphere_pivot_m':list(sphere.matrix_world.translation),'bearing_fit':'static shallow press-fit overlap, not rotating tolerance or performance'}
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
 'single_prop_count':1,'polar_axis_and_sphere':axis_evidence,'actual_meridian_gap_rays':gap_checks,'actual_bearing_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/education/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'education','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.262));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.620;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3,-6,3.0),'gray-back3q':(-3,6,3.0)} if gray else {
 'thumbnail':(3,-6,3.0),'qa-front':(0,-7,.262),'qa-side':(7,0,.262),'qa-top':(0,0,8),
 'qa-back':(0,7,.262),'qa-wireframe':(3,-6,3.0)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.620
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00022;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.262)),('silhouette-128-side',(7,0,.262))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
