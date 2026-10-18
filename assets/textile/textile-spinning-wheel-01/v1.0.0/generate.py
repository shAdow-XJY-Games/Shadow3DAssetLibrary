"""Original static treadle spinning wheel, metres, source Z up; wheel/spindle axes Y.
Distinct eight-spoke driving wheel, fixed treadle/crank/linkage and supported winding spindle.
Every image renders a fresh import of the exact GLB. No external dependencies.
--geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
No animation, spinning, belt transmission, cloth, torque, ergonomics or mechanical simulation.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='textile-spinning-wheel-01';VERSION='1.0.0';TITLE='Timber Treadle Spinning Wheel'
DESCRIPTION=('Original static timber spinning wheel with a large eight-spoke open driving wheel, separate solid axle and two supporting posts. '
 'A broad sloped treadle connects through an offset crank pin and diagonal connecting rod. A side-mounted winding spindle has two bearing posts, '
 'a small pulley, two flanges and a cream wound-yarn sleeve; a real closed cord loop follows the wheel and pulley. '
 'The eight spoke apertures, lateral wheel clearances, raised wheel bottom and treadle clearance are real geometry. '
 'All named parts have physical fixed-pose support routes to two long grounded feet. Metres, source Z up, wheel and spindle axes Y, '
 'ground-centre origin; four solid PBR materials, separate editable source components and no external dependencies. '
 'Distinct yarn preparation prop, not a loom or a loose spool tray. Static visual game asset only; no spinning animation, '
 'working transmission, cloth simulation, torque, human ergonomics, engineering or safety certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('HoneyTimber_WheelAndTreadle',(.49,.29,.13,1),.78,0),
 ('WalnutTimber_FrameAndBobbin',(.24,.12,.055,1),.81,0),('DarkIron_AxlesAndLinkage',(.12,.17,.17,1),.55,.45),
 ('CreamFiber_YarnAndDriveCord',(.72,.67,.49,1),.90,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('TimberTreadleSpinningWheel',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['wheel_and_spindle_axis']='Y';root['static_visual_only']=True
root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Hand-cut edge','BEVEL');b.width=bevel;b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def beam(name,a,b,width,material,role,bevel=.002):
 a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(width,width,(b-a).length),material,role,bevel)
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def cylinder(name,a,b,radius,material,role,n=16):
 a,b=Vector(a),Vector(b);axis=(b-a).normalized();ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0));u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
 vs=[p+radius*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,(a+b)/2)
def ring_y(name,c,profile,material,role,n=48):
 x,y,z=c;vs=[(x+r*math.cos(math.tau*i/n),y+dy,z+r*math.sin(math.tau*i/n)) for r,dy in profile for i in range(n)]
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%len(profile))*n+(i+1)%n,((k+1)%len(profile))*n+i) for k in range(len(profile)) for i in range(n)]
 return mesh(name,vs,fs,material,role,c)
def cord_loop(name,points,radius,material,role,sides=8):
 vs=[]
 for i,p in enumerate(points):
  tangent=(Vector(points[(i+1)%len(points)])-Vector(points[(i-1)%len(points)])).normalized();u=Vector((0,1,0));v=tangent.cross(u).normalized()
  vs.extend([Vector(p)+radius*(math.cos(math.tau*j/sides)*u+math.sin(math.tau*j/sides)*v) for j in range(sides)])
 fs=[(i*sides+j,i*sides+(j+1)%sides,((i+1)%len(points))*sides+(j+1)%sides,((i+1)%len(points))*sides+j) for i in range(len(points)) for j in range(sides)]
 return mesh(name,vs,fs,material,role)
def link(a,b):links.append((a,b))
# A low open chassis, with finite flat feet rather than a presentation plinth.
for y,label in [(-.28,'Front'),(.28,'Rear')]:
 box('GroundFoot_'+label,(0,y,.05),(1.62,.15,.10),1,'long grounded timber foot',.008)
for x,label in [(-.52,'Left'),(-.24,'Wheel'),(.58,'Spindle')]:
 box('BaseCrossbar_'+label,(x,0,.145),(.115,.66,.12),1,'transverse foot connection and post support',.006)
 for end in ['Front','Rear']:link('BaseCrossbar_'+label,'GroundFoot_'+end)
# Wheel in XZ, two outboard bearing posts leave visible side clearances.
WC=(-.24,0,.79)
for y,label in [(-.16,'Front'),(.16,'Rear')]:
 box('WheelPost_'+label,(-.24,y,.46),(.085,.08,.64),1,'wheel axle support post',.006)
 cylinder('WheelBearing_'+label,(-.24,y-.052,.79),(-.24,y+.052,.79),.048,1,'fixed bearing cap through post',16)
 link('WheelPost_'+label,'BaseCrossbar_Wheel');link('WheelBearing_'+label,'WheelPost_'+label)
cylinder('DriveAxle',(-.24,-.31,.79),(-.24,.235,.79),.024,2,'solid wheel axle',16)
for end in ['Front','Rear']:link('DriveAxle','WheelBearing_'+end)
cylinder('DriveHub',(-.24,-.06,.79),(-.24,.06,.79),.079,0,'thick eight-spoke wheel hub',24);link('DriveHub','DriveAxle')
ring_y('DriveRim',WC,[(.420,-.035),(.470,-.035),(.470,.035),(.420,.035)],0,'continuous thick driving-wheel rim with open centre',48)
for i in range(8):
 theta=math.tau*i/8;d=Vector((math.cos(theta),0,math.sin(theta)));a=Vector(WC)+d*.055;b=Vector(WC)+d*.444
 name=f'DriveSpoke_{i+1:02d}';beam(name,a,b,.036,0,'solid radial spoke joined into hub and rim',.002)
 link(name,'DriveHub');link(name,'DriveRim')
# The front offset crank, steel pin and slender pitman rod show an explicit static connection.
beam('CrankArm',(-.24,-.285,.795),(-.24,-.285,.655),.038,2,'fixed downward crank arm',.004);link('CrankArm','DriveAxle')
cylinder('CrankPin',(-.24,-.325,.66),(-.24,-.26,.66),.022,2,'offset linkage pin',12);link('CrankPin','CrankArm')
# Rear treadle hinge has an actual cross-support tied to the rear ground foot.
box('TreadleHingeSupport',(.16,.235,.115),(.54,.17,.09),1,'rear hinge support grounded through rear foot',.006)
link('TreadleHingeSupport','GroundFoot_Rear')
cylinder('TreadlePivot',(-.085,.18,.165),(.405,.18,.165),.022,2,'fixed transverse treadle pivot',16);link('TreadlePivot','TreadleHingeSupport')
# A broad, sloped board: front Z=.113, rear Z=.183; thickness .033 m.
outline=[(.01,-.49),(.31,-.49),(.31,.205),(.01,.205)]
zs=lambda y:.113+(y+.49)*(.070/.695)
vs=[(x,y,zs(y)+off) for off in [-.0165,.0165] for x,y in outline]
fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
mesh('TreadleBoard',vs,fs,0,'broad sloped foot treadle with ground clearance',origin=(.16,-.1425,.148),bevel=.004);link('TreadleBoard','TreadlePivot')
B=(.16,-.302,zs(-.302)+.004)
cylinder('TreadleLinkPin',(.16,-.33,B[2]),(.16,-.268,B[2]),.022,2,'lower pin embedded in treadle',12);link('TreadleLinkPin','TreadleBoard')
beam('ConnectingRod',(.16,-.312,B[2]),(-.24,-.312,.66),.025,1,'static pitman rod linking treadle to crank pin',.003)
link('ConnectingRod','TreadleLinkPin');link('ConnectingRod','CrankPin')
# Separate side-mounted winding spindle. Bearing caps and shaft are intentionally fixed solids.
for y,label in [(-.25,'Front'),(.25,'Rear')]:
 box('SpindlePost_'+label,(.58,y,.55),(.075,.075,.82),1,'spindle bearing post tied to base',.005)
 cylinder('SpindleBearing_'+label,(.58,y-.045,.97),(.58,y+.045,.97),.043,1,'fixed spindle bearing cap',16)
 link('SpindlePost_'+label,'BaseCrossbar_Spindle');link('SpindleBearing_'+label,'SpindlePost_'+label)
cylinder('SpindleShaft',(.58,-.36,.97),(.58,.32,.97),.016,2,'straight supported winding spindle',16)
for end in ['Front','Rear']:link('SpindleShaft','SpindleBearing_'+end)
cylinder('SpindlePulley',(.58,-.049,.97),(.58,-.007,.97),.068,0,'small solid drive pulley on spindle',24);link('SpindlePulley','SpindleShaft')
for y,label in [(.018,'Front'),(.225,'Rear')]:
 cylinder('BobbinFlange_'+label,(.58,y-.010,.97),(.58,y+.010,.97),.071,0,'bobbin end flange on spindle',24);link('BobbinFlange_'+label,'SpindleShaft')
# Annular yarn sleeve with a real bored centre and deliberately low ridges.
profile=[(.013,.035),(.045,.035)]+[(.050+(.003 if i%2==0 else 0),.042+i*.012) for i in range(15)]+[(.045,.216),(.013,.216)]
ring_y('WoundYarnSleeve',(.58,0,.97),profile,3,'cream wound yarn with real circumferential ridges and spindle bore',24);link('WoundYarnSleeve','SpindleShaft')
# Open belt geometry: true tangent spans and two wrap arcs, built as one closed solid cord.
R=.467;r=.063;dx=.82;dz=.18;phi=math.atan2(dz,dx);alpha=math.acos((R-r)/math.hypot(dx,dz));upper=phi+alpha;lower=phi-alpha
points=[]
for i in range(49):
 a=upper+(math.tau-2*alpha)*i/48;points.append((-.24+R*math.cos(a),-.028,.79+R*math.sin(a)))
for i in range(17):
 a=lower+2*alpha*i/16;points.append((.58+r*math.cos(a),-.028,.97+r*math.sin(a)))
cord_loop('DriveCordLoop',points,.006,3,'continuous static cord wrapped around wheel and spindle pulley')
# Bake final rotation/scale before verification/export to avoid glTF quaternion
# drift, preserving each component's editable origin and all check thresholds.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
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
def joint(a,b,points=None):
 if points is None:
  lo=[max(extents[a][0][k],extents[b][0][k]) for k in range(3)];hi=[min(extents[a][1][k],extents[b][1][k]) for k in range(3)]
  assert all(hi[k]>lo[k] for k in range(3)),('No overlap bounds',a,b,lo,hi)
  valid=[]
  for fx in [.01,.03,.08,.25,.5,.75,.92,.97,.99]:
   for fy in [.01,.03,.08,.25,.5,.75,.92,.97,.99]:
    for fz in [.01,.03,.08,.25,.5,.75,.92,.97,.99]:
     p=Vector([lo[k]+(hi[k]-lo[k])*f for k,f in enumerate([fx,fy,fz])])
     if all(trees[n].find_nearest(p)[3]>.00015 and inside(trees[n],p) for n in [a,b]):valid.append(p)
  assert len(valid)>=3,('No genuine interior overlap',a,b,len(valid))
  centre=Vector([(lo[k]+hi[k])/2 for k in range(3)]);points=[min(valid,key=lambda p:(p-centre).length_squared)]
  for _ in range(2):points.append(max(valid,key=lambda p:min((p-q).length_squared for q in points)))
 rows=[]
 for p in points:
  p=Vector(p);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,(a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
for a,b in links:joint(a,b)
# These witnesses are midpoints of actual sampled cord rings, away from tangent changes.
joint('DriveCordLoop','DriveRim',[points[i] for i in [22,24,26]])
joint('DriveCordLoop','SpindlePulley',[points[i] for i in [55,57,59]])
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={'GroundFoot_Front','GroundFoot_Rear'};todo=list(seen)
while todo:
 for other in adj[todo.pop()]-seen:seen.add(other);todo.append(other)
assert seen==set(adj),('Unsupported components',set(adj)-seen)
def rayhits(origin,direction,distance):
 hits=[]
 for name,tree in trees.items():
  p,n,_,d=tree.ray_cast(Vector(origin),Vector(direction),distance)
  if p is not None:hits.append({'name':name,'distance_m':d,'point_m':list(p)})
 return sorted(hits,key=lambda h:h['distance_m'])
# Test eight apertures through the wheel-depth throat (Y=-.10 to +.10).
# Independent full-depth window checks also account for outer posts and the front linkage.
voids=[]
for i in range(8):
 a=math.tau*(i+.5)/8;p=[-.24+.30*math.cos(a),-.10,.79+.30*math.sin(a)]
 hits=rayhits(p,(0,1,0),.20);assert not hits,('Blocked spoke aperture',i,hits);voids.append({'origin_m':p,'direction':[0,1,0],'length_m':.20})
# Quantitative clearances are measured from real geometry bounds, not just design parameters.
wheel_low=extents['DriveRim'][0][2];assert wheel_low>.31
lateral=[]
for end,sign in [('Front',-1),('Rear',1)]:
 rim=extents['DriveRim'];post=extents['WheelPost_'+end]
 gap=post[0][1]-rim[1][1] if sign>0 else rim[0][1]-post[1][1];assert gap>.08;lateral.append({'post':end,'actual_gap_m':gap})
pedal_low=extents['TreadleBoard'][0][2];assert pedal_low>.09
# The complete side-placed treadle must clear every nonjoint solid. Test actual
# triangle intersections AND both containment directions, not only bounding boxes.
treadle_clearances=[];board=byname['TreadleBoard'];board_vs=[board.matrix_world@v.co for v in board.data.vertices]
for other in parts:
 if other.name in ['TreadleBoard','TreadlePivot','TreadleLinkPin','ConnectingRod']:continue
 intersections=trees['TreadleBoard'].overlap(trees[other.name])
 other_vs=[other.matrix_world@v.co for v in other.data.vertices]
 board_inside=sum(inside(trees[other.name],p) for p in board_vs)
 other_inside=sum(inside(trees['TreadleBoard'],p) for p in other_vs)
 assert not intersections and not board_inside and not other_inside,('Treadle intersects nonjoint component',other.name,len(intersections),board_inside,other_inside)
 treadle_clearances.append({'other':other.name,'actual_triangle_intersections':len(intersections),'board_vertices_inside_other':board_inside,'other_vertices_inside_board':other_inside})
supports=[]
for name in ['GroundFoot_Front','GroundFoot_Rear']:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.15;supports.append({'name':name,'area_m2':area,'triangles':patch})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
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
 'eight_wheel_throat_spoke_void_rays':voids,'actual_wheel_post_lateral_clearances':lateral,'actual_wheel_bottom_z_m':wheel_low,
 'actual_treadle_bottom_z_m':pedal_low,'full_assembly_treadle_nonjoint_clearance':treadle_clearances,'finite_ground_patches':supports,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((-.01,-.03,.63));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.95;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-7,3.5),'gray-back3q':(-4,6,3.5)} if gray else {
 'thumbnail':(4,-7,3.5),'qa-front':(-.01,-6,.63),'qa-side':(6,-.03,.63),'qa-top':(0,0,7),
 'qa-back':(-.01,6,.63),'qa-wireframe':(4,-7,3.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0010;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(-.01,-6,.63)),('silhouette-128-side',(6,-.03,.63))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
