"""Original one-piece static navigation sextant with finite integral display support.
Standalone Blender source, metres, Z up, front -Y. No external dependencies.
Real open fan framework, physical scale ticks, fixed arm/axle, two mirror seats,
supported short sight tube, rear grip. Visual only, no calibration or navigation.
--geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
All images render a fresh actual exported GLB, Cycles128 FIXED4, no denoise.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='navigation-sextant-01';VERSION='1.0.0';TITLE='Brass Arc Navigation Sextant'
DESCRIPTION=('Original static low-poly navigation sextant with an open fan-shaped brass framework, '
 'separate dark graduation arc and 61 physical scale marks, a fixed pivot-connected index arm and arc shoe, '
 'two distinct supported silver mirror plates in U-shaped seats, a short supported sighting tube and a rear wooden grip. '
 'Four radial ribs and an inner arch form six real cut-through framework windows. Two integral compact display feet support the arc. '
 'All named components connect through actual finite interior overlaps to grounded feet; handle/frame and tube/frame clearance are checked. '
 'Six flat solid PBR materials, no textures or external resources. Metres, native Z up, front -Y and ground origin at centre. '
 'One original reusable instrument, distinct from the earlier compass, map table and telescope. '
 'Static stylized visual only: no optical-path validity, angular measurement, calibration, navigation, moving mechanism, stability or safety certification.')
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
for name,color,rough,metal in [('Brass_Frame',(.62,.34,.075,1),.40,.66),
 ('DarkTeal_ScaleAndTube',(.025,.115,.12,1),.46,.32),('Walnut_GripAndFeet',(.16,.059,.025,1),.60,0),
 ('PaleBrass_Graduations',(.85,.66,.24,1),.42,.53),('Silver_Mirror',(.46,.65,.69,1),.22,.70),
 ('Graphite_LensAndFasteners',(.017,.025,.026,1),.34,.30)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('BrassNavigationSextant',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True
root['origin_datum']='ground projection of body centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role,asset=True):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if asset:
  o.parent=root;me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
 return o

# GEOMETRY_BEGIN: pure vector-and-mesh construction, no image or external asset.
def obox(name,c,size,material,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 c,u,v,w=Vector(c),Vector(u),Vector(v),Vector(w);a,b,d=[s/2 for s in size]
 vs=[c+u*sx*a+v*sy*b+w*sz*d for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def rod(name,a,b,r,material,role,n=16):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0));u=d.cross(ref).normalized();v=d.cross(u)
 vs=[p+r*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],material,role)
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
P=Vector((0,0,.58))
def radial(r,deg,y=0):
 a=math.radians(deg);return P+Vector((r*math.cos(a),y,r*math.sin(a)))
def arc(name,ri,ro,low,high,material,role,start=209.5,stop=330.5,n=60):
 vs=[radial(r,start+(stop-start)*i/n,y) for y in [low,high] for r in [ri,ro] for i in range(n+1)];k=n+1;fs=[]
 for i in range(n):
  j=i+1;fs.extend([(i,j,k+j,k+i),(2*k+i,3*k+i,3*k+j,2*k+j),(i,2*k+i,2*k+j,j),(k+i,k+j,3*k+j,3*k+i)])
 fs.extend([(0,k,3*k,2*k),(n,2*k+n,3*k+n,k+n)])
 return mesh(name,vs,fs,material,role)
def radialbar(name,r1,r2,deg,width,low,high,material,role):
 d=Vector((math.cos(math.radians(deg)),0,math.sin(math.radians(deg))));u=Vector((-d.z,0,d.x))
 return obox(name,radial((r1+r2)/2,deg,(low+high)/2),(width,high-low,r2-r1),material,role,u=u,w=d)
arc('Frame_OuterFanArc',.446,.486,-.018,.018,0,'continuous closed outer fan arc with actual open interior')
arc('Frame_InnerBraceArc',.237,.257,-.015,.015,0,'concentric inner arch splitting the real framework windows')
rod('Pivot_FixedAxle',(0,-.080,.58),(0,.040,.58),.031,0,'fixed central axle joining radial frame and index arm',n=24)
rod('Pivot_FrontCap',(0,-.085,.58),(0,-.072,.58),.020,5,'fixed dark axle cap',n=16)
joint('Pivot_FrontCap','Pivot_FixedAxle',[(x,-.076,.58) for x in [-.007,0,.007]])
for deg,label in [(210,'LeftEdge'),(250,'LeftInner'),(290,'RightInner'),(330,'RightEdge')]:
 name='Frame_RadialRib_'+label;radialbar(name,.018,.467,deg,.020,-.017,.017,0,'solid radial frame rib joining axle to outer and inner arcs')
 joint(name,'Frame_OuterFanArc',[radial(.456+d,deg,.005) for d in [-.002,0,.002]])
 joint(name,'Frame_InnerBraceArc',[radial(.247+d,deg,.004) for d in [-.002,0,.002]])
 joint(name,'Pivot_FixedAxle',[radial(.024,deg+d,.001) for d in [-1,0,1]])
arc('Graduation_DarkArc',.448,.483,-.025,-.016,1,'dark inset physical graduation band; no numeric angle accuracy',start=209.7,stop=330.3)
joint('Graduation_DarkArc','Frame_OuterFanArc',[radial(.469,deg,-.017) for deg in [222,270,318]])
# Sixty-one physical contrasting ticks, no decal/text/texture. The centre is not a compass dial.
for i in range(61):
 deg=210+2*i;major=i%5==0;name=f'Graduation_Tick_{i:02d}';r1=.451 if major else .460
 radialbar(name,r1,.479,deg,.0028 if major else .0017,-.028,-.024,3,'solid stylized major tick' if major else 'solid stylized minor tick')
 joint(name,'Graduation_DarkArc',[radial(.471+d,deg,-.0245) for d in [-.001,0,.001]])
INDEX=282
radialbar('Index_FixedArm',.008,.478,INDEX,.024,-.055,-.039,3,'single fixed index arm attached to the central axle and lower arc shoe')
joint('Index_FixedArm','Pivot_FixedAxle',[radial(.016,INDEX+d,-.047) for d in [-2,0,2]])
radialbar('Index_ArcShoe',.451,.486,INDEX,.050,-.061,-.012,0,'closed stationary shoe straddling the graduation arc')
joint('Index_ArcShoe','Index_FixedArm',[radial(.467+d,INDEX,-.048) for d in [-.002,0,.002]])
joint('Index_ArcShoe','Frame_OuterFanArc',[radial(.467+d,INDEX,-.015) for d in [-.002,0,.002]])
shoe=radial(.469,INDEX)
rod('Index_LockKnob',(shoe.x,-.083,shoe.z),(shoe.x,-.055,shoe.z),.014,5,'fixed shoe lock knob with embedded support',n=12)
joint('Index_LockKnob','Index_ArcShoe',[(shoe.x+d,-.058,shoe.z) for d in [-.004,0,.004]])
# Two U-shaped metal mirror seats with real inset silver plates. Mirror normals are stylized.
mirror_rows=[]
def mirror(label,center,width,height,degrees):
 c=Vector(center);a=math.radians(degrees);u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));w=Vector((0,0,1))
 base=label+'_SeatBase';left=label+'_SeatLeft';right=label+'_SeatRight';plate=label+'_MirrorPlate';back=label+'_SeatBack'
 # Local y front is negative. A continuous solid backing physically holds the plate.
 obox(base,c+w*(-height/2-.004),(width+.022,.030,.016),0,'lower crossbar of supported mirror U-seat',u,v,w)
 obox(back,c+v*.008,(width+.010,.010,height+.006),0,'continuous mirror-seat rear backing',u,v,w)
 obox(plate,c-v*.002,(width,.012,height),4,'inset opaque silver mirror plate; static visual only',u,v,w)
 joint(back,base,[c+u*x+v*.008+w*(-height/2+.001) for x in [-width*.25,0,width*.25]])
 joint(plate,back,[c+u*x+v*.0035 for x in [-width*.25,0,width*.25]])
 for side,sign in [(left,-1),(right,1)]:
  obox(side,c+u*(sign*(width/2+.003)),(.012,.024,height+.010),0,'raised lateral mirror-seat retaining cheek',u,v,w)
  joint(side,base,[c+u*(sign*(width/2+.003))+v*d+w*(-height/2+.001) for d in [-.006,0,.006]])
  joint(side,plate,[c+u*(sign*(width/2-.001))+v*d for d in [-.003,0,.003]])
 mirror_rows.append({'label':label,'plate':plate,'base':base,'center_m':list(c),'width_m':width,'height_m':height,'local_width_axis':list(u),'local_thickness_axis':list(v),'visual_only':True})
 return base
# Upper mirror rises above the pivot on a closed pedestal; no floating plate.
obox('IndexMirror_Pedestal',(0,-.056,.594),(.045,.086,.034),0,'closed bridge from central axle to upper mirror-seat base')
joint('IndexMirror_Pedestal','Pivot_FixedAxle',[(x,-.030,.591) for x in [-.009,0,.009]])
m=mirror('IndexMirror',(0,-.094,.646),.064,.090,25)
joint(m,'IndexMirror_Pedestal',[(x,-.090,.602) for x in [-.010,0,.010]])
# Horizon mirror is separately supported by left frame rib, away from the index arm.
obox('HorizonMirror_Bracket',(-.255,-.057,.437),(.046,.145,.029),0,'closed cantilever rooted in the left radial frame rib')
joint('HorizonMirror_Bracket','Frame_RadialRib_LeftEdge',[(-.255+d,-.002,.4328-d*.57735) for d in [-.004,0,.004]])
m=mirror('HorizonMirror',(-.255,-.112,.489),.058,.082,-18)
joint(m,'HorizonMirror_Bracket',[(-.255+d,-.112,.446) for d in [-.010,0,.010]])
# Sight tube points horizontally along X. Its barrel and two collars have supporting saddle.
obox('SightTube_FrameBracket',(.255,-.052,.446),(.046,.134,.036),0,'cantilever rooted in right frame rib and carrying the sight-tube saddle')
joint('SightTube_FrameBracket','Frame_RadialRib_RightEdge',[(.255+d,.002,.4328+d*.57735) for d in [-.004,0,.004]])
obox('SightTube_Saddle',(.255,-.112,.466),(.060,.046,.034),0,'finite lower saddle embedded into actual tube wall')
joint('SightTube_Saddle','SightTube_FrameBracket',[(.255+d,-.110,.458) for d in [-.012,0,.012]])
rod('SightTube_Barrel',(.120,-.112,.488),(.396,-.112,.488),.025,1,'short closed sighting barrel supported on fixed saddle',n=24)
joint('SightTube_Barrel','SightTube_Saddle',[(.255+d,-.112,.469) for d in [-.012,0,.012]])
for label,a,b,r in [('ObjectiveRim',.111,.137,.032),('RearCollar',.365,.401,.028),('Eyepiece',.391,.427,.018)]:
 name='SightTube_'+label;rod(name,(a,-.112,.488),(b,-.112,.488),r,0 if label!='Eyepiece' else 5,'closed supported tube fitting',n=24)
 x=(max(a,.120)+min(b,.396))/2;joint(name,'SightTube_Barrel',[(x,-.112+d,.488) for d in [-.004,0,.004]])
rod('SightTube_ObjectiveLens',(.108,-.112,.488),(.117,-.112,.488),.024,4,'opaque stylized objective lens seated in brass rim',n=24)
joint('SightTube_ObjectiveLens','SightTube_ObjectiveRim',[(.114,-.112+d,.488) for d in [-.008,0,.008]])
rod('SightTube_EyeLens',(.423,-.112,.488),(.430,-.112,.488),.012,5,'opaque dark eyepiece face seated within fitting',n=16)
joint('SightTube_EyeLens','SightTube_Eyepiece',[(.425,-.112+d,.488) for d in [-.004,0,.004]])
# Rear grip stands clear of the framework, attached at each end by a distinct metal strut.
rod('Handle_WalnutGrip',(0,.112,.271),(0,.112,.491),.027,2,'rear vertical wooden grip with continuous finite solid section',n=12)
rod('Handle_UpperStrut',(0,.016,.580),(0,.112,.478),.014,0,'upper handle brace embedded in pivot and grip',n=12)
joint('Handle_UpperStrut','Pivot_FixedAxle',[(0,.020+d,.576-d*1.0625) for d in [0,.001,.002]])
joint('Handle_UpperStrut','Handle_WalnutGrip',[(0,.108+d,.482-d*1.0625) for d in [0,.001,.002]])
rod('Handle_LowerStrut',(0,.012,.116),(0,.112,.284),.014,0,'lower handle brace embedded in arc and grip',n=12)
joint('Handle_LowerStrut','Frame_OuterFanArc',[(0,.014+d,.11936+d*1.68) for d in [0,.001,.002]])
joint('Handle_LowerStrut','Handle_WalnutGrip',[(0,.108+d,.27728+d*1.68) for d in [0,.001,.002]])
for label,z in [('Lower',.281),('Upper',.481)]:
 name='Handle_'+label+'Ferrule';rod(name,(0,.112,z-.011),(0,.112,z+.011),.030,0,'brass collar overlapping wooden grip',n=12)
 joint(name,'Handle_WalnutGrip',[(d,.112,z) for d in [-.008,0,.008]])
# Two small display feet belong to this one static asset; no platform or second object is counted.
feet=[]
for deg,label in [(232.5,'Left'),(307.5,'Right')]:
 p=radial(.466,deg);foot='DisplayFoot_'+label;leg='DisplaySupport_'+label;saddle='DisplaySaddle_'+label
 obox(foot,(p.x,.018,.010),(.112,.204,.020),2,'finite grounded compact integral display foot');feet.append(foot)
 obox(leg,(p.x,.018,(p.z+.017)/2),(.029,.038,p.z-.017+.018),0,'short brass upright fixed into foot and arc saddle')
 obox(saddle,(p.x,.008,p.z),(.046,.060,.034),0,'finite saddle clasp embedded into outer fan arc')
 joint(leg,foot,[(p.x+d,.018,.016) for d in [-.006,0,.006]])
 joint(leg,saddle,[(p.x+d,.018,p.z-.005) for d in [-.006,0,.006]])
 joint(saddle,'Frame_OuterFanArc',[radial(.466+d,deg,.006) for d in [-.003,0,.003]])
# GEOMETRY_END
# Apply deterministic triangulation, recalculate closed winding and quantize positions.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for v in o.data.vertices:v.co=Vector(tuple(round(float(c),6) for c in v.co))
 o.data.update()
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-13 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-11 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,2)
   if q is None:break
   hits+=1;p=q+d*1e-6
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in links:
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3])
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.000015,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(feet);todo=list(feet)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)

# Grounding uses actual finite downward-facing foot triangles at Z=0.
supports=[]
for name in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.020;supports.append({'name':name,'area_m2':area,'triangles':patch})
def clear_ray(label,start,direction,length):
 start,direction=Vector(start),Vector(direction).normalized();hits=[]
 for name,tree in trees.items():
  q,_,_,_=tree.ray_cast(start,direction,length)
  if q is not None:hits.append(name)
 assert not hits,('Blocked real aperture',label,list(start),hits)
 return {'start_m':list(start),'direction':list(direction),'length_m':length}
# Six finite windows through the entire fan frame, not painted gaps or AABB promises.
apertures=[]
for r in [.145,.345]:
 for deg in [231,270,310]:
  p=radial(r,deg);rays=[]
  for dx,dz in [(0,0),(-.008,-.008),(-.008,.008),(.008,-.008),(.008,.008)]:
   rays.append(clear_ray('open_fan_window',(p.x+dx,-.068,p.z+dz),(0,1,0),.090))
  apertures.append({'radius_m':r,'angle_degrees':deg,'centre_m':list(p),'window_half_width_m':.008,'rays':rays})
# Rear grip and fixed tube have actual nearest-triangle clearance from the frame.
clearances=[]
frame_names=['Frame_OuterFanArc','Frame_InnerBraceArc']+[f'Frame_RadialRib_{s}' for s in ['LeftEdge','LeftInner','RightInner','RightEdge']]
for obj,targets,minimum in [('Handle_WalnutGrip',frame_names,.045),('SightTube_Barrel',frame_names,.045),('Index_FixedArm',frame_names[1:],.015)]:
 o=byname[obj];near=[]
 for v in o.data.vertices:
  p=o.matrix_world@v.co;distance=min(trees[name].find_nearest(p)[3] for name in targets)
  assert not any(inside(trees[name],p) for name in targets) and distance>minimum,(obj,list(p),distance)
  near.append(distance)
 clearances.append({'object':obj,'against':targets,'minimum_vertex_to_actual_triangle_distance_m':min(near),'required_m':minimum,'tested_vertices':len(near)})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<10000
# Complete Principled signature; no texture nodes or linked Principled sockets are allowed.
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
 'real_fan_apertures':apertures,'two_supported_mirror_seats':mirror_rows,'clearances':clearances,'graduation_tick_count':61,
 'fixed_index_angle_visual_degrees':INDEX,'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/navigation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'navigation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# All renders operate on a freshly imported exact actual GLB, not a second geometry copy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((0,0,.350));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-1.2,-1.5,2.1),140,1.5),('Fill',(1.3,-.1,1.4),75,1.2),('Rim',(.1,1.5,1.5),110,1.3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.04;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.85,-1.9,1.00),'gray-back3q':(-.85,1.9,1.00)} if gray else {
 'thumbnail':(.85,-1.9,1.00),'qa-front':(0,-2,.350),'qa-side':(2,0,.350),'qa-top':(0,0,2),
 'qa-back':(0,2,.350),'qa-wireframe':(.85,-1.9,1.00)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True;t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00020;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-2,.350)),('silhouette-128-side',(2,0,.350))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
