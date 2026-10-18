"""Original horizontal open weekender holdall, one fixed static visual prop.
Metres, Z up, front -Y; length X; flat ground-centre origin.
Self-contained new geometry. No textures, logos, contents or animation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='baggage-open-weekender-holdall-01';VERSION='1.0.0';TITLE='Open Weekender Travel Holdall'
DESCRIPTION=('One original static horizontal travel holdall with a rounded soft-profile thick shell, one genuinely empty main chamber, a broad finite floor and a real elongated top opening. '
 'Two independent wide carry loops rise from the two long sides; four separately editable reinforced anchor bands have finite seating into the shell and the handle terminals. '
 'A separate continuous fixed mouth binding follows the open top without sealing it. Eight closed named editable meshes, four constant solid PBR materials, metre scale, source Z up, length X, front -Y and ground-centre origin. '
 'No textures, logos, clothes, characters, scene or external assets. Original broad shoulder-and-belly profile and paired long-side handles differ from the old vertical closed backpack, divided postal satchel and rigid harvest basket. '
 'One fixed open pose only: no capacity, load, weatherproofing, cloth deformation, human fit, zipper operation, opening or carrying animation, travel performance, manufacture or safety certification.')
G={};LINKS=[];FEET=['Body_SoftOpenMainChamber'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];SINGLE_CHAMBER_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Canvas_BurntSienna',(.39,.115,.060,1),.86,0),('Lining_WarmSand',(.64,.47,.27,1),.91,0),('Webbing_DeepUmber',(.070,.032,.019,1),.78,0),('Binding_Caramel',(.29,.135,.058,1),.72,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.004):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def rounded_rect(rx,ry,c,steps=6):
 # Separate quarter arcs joined by true broad straight sides; CCW, 28 vertices.
 pts=[]
 for cx,cy,start in [(rx-c,ry-c,0),(-rx+c,ry-c,90),(-rx+c,-ry+c,180),(rx-c,-ry+c,270)]:
  for j in range(steps+1):
   a=math.radians(start+90*j/steps);pts.append((cx+c*math.cos(a),cy+c*math.sin(a)))
 return pts
def loft(rings,caps=True,loop=False):
 n=len(rounded_rect(*rings[0][1:]));vs=[(x,y,z) for z,rx,ry,c in rings for x,y in rounded_rect(rx,ry,c)];fs=[]
 for k in range(len(rings) if loop else len(rings)-1):
  q=(k+1)%len(rings)
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,q*n+j,q*n+i))
 if caps:fs=[tuple(reversed(range(n)))]+fs+[tuple((len(rings)-1)*n+i for i in range(n))]
 return vs,fs
# New broad, domed travel-bag profile. Multiple shoulder/belly layers are not a
# scaled postal shell. Surface continues across the rim, down every interior
# wall and across the floor. Nothing covers the single elongated top opening.
OUTER=[(0,.292,.108,.030),(.020,.315,.137,.038),(.090,.345,.160,.046),(.170,.345,.165,.046),(.220,.330,.140,.040),(.265,.310,.110,.034),(.295,.300,.093,.030)]
INNER=[(.295,.286,.079,.026),(.265,.296,.096,.030),(.220,.316,.126,.036),(.170,.331,.151,.042),(.090,.331,.146,.042),(.030,.299,.121,.034),(.020,.278,.094,.026)]
vs,fs=loft(OUTER+INNER);mesh('Body_SoftOpenMainChamber',vs,fs,0,'one closed thick shell with rounded broad belly, sloping shoulders, real 20 mm floor and one empty open main chamber')
n=28;G['Body_SoftOpenMainChamber']['face_materials']=[2]+sum(([2 if k==0 else 0 if k<6 else 3 if k==6 else 1]*n for k in range(13)),[])+[1]
# Complete raised edge binding follows the actual long mouth. Its lower section
# crosses the shell rim in solid material; its inner edge never caps the cavity.
vs,fs=loft([(.286,.307,.100,.033),(.303,.304,.097,.032),(.303,.283,.076,.024),(.286,.282,.075,.024)],False,True)
mesh('Mouth_FixedContinuousBinding',vs,fs,3,'closed annular fixed mouth binding, embedded in the shell around a true open aperture; no zipper motion')
for s in [-1,1]:link('Mouth_FixedContinuousBinding','Body_SoftOpenMainChamber',(s*.23,.086,.292),(1,0,0),.018)
def shell_side(z):
 for (z0,rx0,y0,c0),(z1,rx1,y1,c1) in zip(OUTER,OUTER[1:]):
  if z0<=z<=z1:return y0+(y1-y0)*(z-z0)/(z1-z0)
 raise ValueError(z)
def anchor(name,cx,s):
 zs=[.115,.170,.220,.254];vs=[]
 # Four corners per horizontal slice: front/back layer and 42 mm width.
 for z in zs:
  y=s*shell_side(z)
  for x,d in [(-.021,-.004),(.021,-.004),(.021,.007),(-.021,.007)]:vs.append((cx+x,y+s*d,z))
 fs=[(3,2,1,0),tuple(12+i for i in range(4))]
 for k in range(3):
  for i in range(4):j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
 return mesh(name,vs,fs,2,'42 mm wide reinforcement follows shoulder slope with finite shell seating and carry-loop terminal overlap')
def carry_loop(name,s):
 # A rounded arch, with two long inward-sloping terminal legs. Each short
 # section is an explicit closed quad strip, avoiding a large concave n-gon.
 outer=[(-.185,.195),(-.185,.255)]+[(.185*math.cos(math.pi-j*math.pi/24),.310+.205*math.sin(math.pi-j*math.pi/24)) for j in range(25)]+[(.185,.255),(.185,.195)]
 inner=[(-.161,.195),(-.161,.255)]+[(.161*math.cos(math.pi-j*math.pi/24),.310+.181*math.sin(math.pi-j*math.pi/24)) for j in range(25)]+[(.161,.255),(.161,.195)]
 def yy(z):return .122+max(0,.255-z)*(.034/.060)
 vs=[]
 for a,b in zip(outer,inner):
  vs.extend([(a[0],s*yy(a[1])-.0035,a[1]),(b[0],s*yy(b[1])-.0035,b[1]),(b[0],s*yy(b[1])+.0035,b[1]),(a[0],s*yy(a[1])+.0035,a[1])])
 fs=[(3,2,1,0),tuple((len(outer)-1)*4+i for i in range(4))]
 for k in range(len(outer)-1):
  for i in range(4):j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
 return mesh(name,vs,fs,2,'independent continuous 24 mm wide, 7 mm thick carry loop with two shoulder-seated terminals and a genuine open arch')
for s,side in [(-1,'Front'),(1,'Back')]:
 handle='Handle_'+side+'CarryLoop';carry_loop(handle,s)
 for x,end in [(-.173,'Left'),(.173,'Right')]:
  name='Anchor_'+side+end;anchor(name,x,s)
  link(name,'Body_SoftOpenMainChamber',(x,s*.138,.220),(1,0,0),.010)
  link(handle,name,(x,s*.141833333,.220),(1,0,0),.005)
# Conservative finite empty volume spans the whole chamber, including its
# floor zone, broad belly, shoulders and above-mouth passage. It is acceptance
# geometry only and is never exported as an asset mesh.
vp=[(.024,.269,.083,.024),(.035,.292,.112,.030),(.090,.322,.137,.038),(.170,.322,.142,.038),(.220,.307,.117,.032),(.265,.287,.087,.027),(.283,.274,.064,.022),(.345,.274,.064,.022)]
vv,ff=loft(vp);VOID_VOLUMES['MainChamber_EmptyFiniteVolume']={'vertices':vv,'faces':ff,'role':'finite single-chamber empty volume; triangle intersections and bidirectional containment must all reject any solid obstruction'}
def volume_box(name,lo,hi,role):
 vs=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 VOID_VOLUMES[name]={'vertices':vs,'faces':[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],'role':role}
for s,side in [(-1,'Front'),(1,'Back')]:
 y0,y1=sorted([s*.104,s*.145]);volume_box('Handle_'+side+'_EmptyFiniteOpening',(-.108,y0,.330),(.108,y1,.435),'finite passage through an independent handle arch above the body')
for x in [-.23,0,.23]:
 for y in [-.050,0,.050]:
  GAPS.append({'label':'single_main_chamber_top_to_floor_clear','origin_m':[x,y,.345],'direction':[0,0,-1],'length_m':.324})
  FLOOR_PROBES.append({'label':'single_chamber_real_floor','origin_m':[x,y,.345],'direction':[0,0,-1],'length_m':.37,'mesh':'Body_SoftOpenMainChamber'})
for z in [.100,.180]:
 SINGLE_CHAMBER_PROBES.append({'label':'unpartitioned_main_chamber_across_width','origin_m':[-.26,0,z],'direction':[1,0,0],'length_m':.52})
 SINGLE_CHAMBER_PROBES.append({'label':'unpartitioned_main_chamber_across_depth','origin_m':[0,-.11,z],'direction':[0,1,0],'length_m':.22})
GAPS+=SINGLE_CHAMBER_PROBES
for s,side in [(-1,'Front'),(1,'Back')]:
 for x in [-.09,0,.09]:GAPS.append({'label':side+'_carry_loop_true_opening','origin_m':[x,s*.19,.38],'direction':[0,-s,0],'length_m':.11})
for side in [-1,1]:
 WALL_PROBES.append({'label':'long_side_thick_wall','origin_m':[0,side*.21,.140],'direction':[0,-side,0],'length_m':.10,'mesh':'Body_SoftOpenMainChamber'})
 WALL_PROBES.append({'label':'short_end_thick_wall','origin_m':[side*.39,0,.140],'direction':[-side,0,0],'length_m':.09,'mesh':'Body_SoftOpenMainChamber'})
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
root=bpy.data.objects.new('OneOpenWeekenderHoldall',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 assert abs(hits[0][2]-.020)<1e-6 and abs(hits[1][2])<1e-6,(probe,hits)
 floor_checks.append(dict(probe,actual_intersections_m=hits,actual_floor_thickness_m=hits[0][2]-hits[1][2]))
wall_checks=[]
for probe in WALL_PROBES:
 hits=ray_sequence(trees[probe['mesh']],probe);assert len(hits)==2,(probe,hits)
 thickness=(Vector(hits[0])-Vector(hits[1])).length;assert .012<thickness<.018
 wall_checks.append(dict(probe,actual_intersections_m=hits,actual_thickness_along_ray_m=thickness))
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
# Uniform-volume centroid is reported only as a geometric support check, not a load rating.
volume_sum=0;centroid_sum=Vector((0,0,0))
for o in parts:
 for tri in o.data.loop_triangles:
  a,b,c=[o.matrix_world@o.data.vertices[i].co for i in tri.vertices];vv=a.dot(b.cross(c))/6
  volume_sum+=vv;centroid_sum+=(a+b+c)*(vv/4)
centroid=centroid_sum/volume_sum;assert abs(centroid.x)<.25 and abs(centroid.y)<.08
holdall_evidence={'open_compartment_count':1,'independent_carry_loop_count':2,'anchor_count':4,'interior_floor_rays':floor_checks,'wall_thickness_rays':wall_checks,'finite_void_volumes':VOID_VOLUMES,'finite_volume_empty_checks':void_volume_checks,'uniform_volume_centroid_m':list(centroid),'centroid_projection_within_finite_base':True,'static_display_only':True,'capacity_or_softbody_or_animation_claim':False}
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
 'single_prop_count':1,'holdall_working_geometry':holdall_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/baggage/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'baggage','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.250));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.90;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,6.5),'gray-back3q':(3,5,6.5)} if gray else {
 'thumbnail':(-3,-5,6.5),'qa-front':(0,-7,.250),'qa-side':(7,0,.250),'qa-top':(0,0,8),
 'qa-back':(0,7,.250),'qa-wireframe':(-3,-5,6.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.90
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
 for name,pos in [('silhouette-128-front',(0,-7,.250)),('silhouette-128-side',(7,0,.250))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
