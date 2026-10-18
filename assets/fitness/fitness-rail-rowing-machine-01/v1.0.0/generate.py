"""Original single static long-rail rowing machine, metres/Z up/front -Y.
Captured roller saddle, toe-up strapped trays with actual openings, supported
parked pull handle and connected cord, guarded resistance wheel, four floor pads.
No old chair geometry, continuous motion, exercise or equipment-safety claim.
Standalone modes: --geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
Fresh actual GLB renders, Cycles128 FIXED4, adaptive/denoising/compositor off.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fitness-rail-rowing-machine-01';VERSION='1.0.0';TITLE='Long Rail Rowing Machine'
DESCRIPTION=('Original static low-poly indoor rowing machine with a 1.84m longitudinal rail, independent chamfered saddle and a captured four-roller carriage. '
 'Two upper rollers and two lower capture rollers engage the rail in one stored pose; external carrier cheeks have actual lateral clearance, with physical front and rear stops. '
 'Two inclined foot trays have raised heel edges and true open arch straps. A separate transverse pull handle rests on a solid cradle and connects to the front resistance enclosure by a fixed cord. '
 'The front unit has a thick annular enclosure, separately editable inner wheel, radial protective grilles, central hub and bearing-style caps. '
 'Front and rear crossfeet terminate in four finite ground pads. Six solid flat PBR materials, no textures, characters or imported seat geometry. '
 'Metres, native Z up, front -Y, origin on the ground under rail centreline. One original reusable prop. '
 'Static stylized visual only: no exercise prescription, body-fit guarantee, resistance/power specification, continuous sliding/rope controller, load rating or safety certification.')
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
for name,color,rough,metal in [('Graphite_Frame',(.045,.062,.072,1),.42,.48),
 ('SatinAluminum_Rail',(.49,.59,.63,1),.31,.72),('DeepTeal_Guard',(.025,.29,.31,1),.38,.30),
 ('SoftCharcoal_SeatGrip',(.024,.029,.032,1),.76,.0),('WarmAmber_Stops',(.87,.32,.055,1),.44,.14),
 ('ShadowGray_WheelCord',(.075,.105,.116,1),.62,.22)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('LongRailRowingMachine',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True
root['origin_datum']='ground under rail centreline, machine front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role,asset=True):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if asset:
  o.parent=root;me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
 return o

# GEOMETRY_BEGIN: original rowing-specific geometry, no imported existing asset meshes.
def obox(name,c,size,material,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 c,u,v,w=Vector(c),Vector(u),Vector(v),Vector(w);a,b,d=[s/2 for s in size]
 vs=[c+u*sx*a+v*sy*b+w*sz*d for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def rod(name,a,b,r,material,role,n=24):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0));u=d.cross(ref).normalized();v=d.cross(u)
 vs=[p+r*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],material,role)
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
def tx(c,d=.01):return [Vector(c)+Vector((x,0,0)) for x in [-d,0,d]]
def lathe(name,profile,material,role,c=(0,0,0),u=(1,0,0),v=(0,1,0),w=(0,0,1),n=48):
 c,u,v,w=Vector(c),Vector(u),Vector(v),Vector(w);vs=[];rings=[];fs=[]
 for r,z in profile:
  if r==0:rings.append([len(vs)]);vs.append(c+w*z)
  else:
   rings.append(list(range(len(vs),len(vs)+n)))
   vs.extend(c+u*(r*math.cos(math.tau*i/n))+v*(r*math.sin(math.tau*i/n))+w*z for i in range(n))
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n;fs.append((a[0],b[j],b[i]) if len(a)==1 else ((a[i],a[j],b[0]) if len(b)==1 else (a[i],a[j],b[j],b[i])))
 return mesh(name,vs,fs,material,role)
def ring(name,ri,ro,z0,z1,material,role,**kw):return lathe(name,[(ri,z0),(ro,z0),(ro,z1),(ri,z1)],material,role,**kw)
def beam(name,a,b,width,depth,material,role):
 a,b=Vector(a),Vector(b);v=(b-a).normalized();u=Vector((1,0,0));w=u.cross(v)
 return obox(name,(a+b)/2,(width,math.sqrt(sum(t*t for t in b-a)),depth),material,role,u,v,w)
def padded_seat(name,c,width,length,material):
 c=Vector(c);vs=[];fs=[]
 for z,inset in [(-.032,.018),(-.022,0),(.022,0),(.032,.015)]:
  x=width/2-inset;y=length/2-inset;ch=.035
  vs.extend(c+Vector((a,b,z)) for a,b in [(-x+ch,-y),(x-ch,-y),(x,-y+ch),(x,y-ch),(x-ch,y),(-x+ch,y),(-x,y-ch),(-x,-y+ch)])
 fs=[tuple(reversed(range(8))),tuple(24+i for i in range(8))]
 for k in range(3):
  for i in range(8):j=(i+1)%8;fs.append((k*8+i,k*8+j,(k+1)*8+j,(k+1)*8+i))
 return mesh(name,vs,fs,material,'chamfered independent rowing saddle, broad solid pad without backrest')
# Four real finite pads tie the front and rear floor bars to the rail and fan frame.
feet=[]
for label,y,half in [('Front',-.88,.31),('Rear',1.26,.27)]:
 bar='Frame_FloorBar_'+label;obox(bar,(0,y,.072),(half*2+.13,.12,.075),0,'low transverse floor beam')
 for s,side in [(-1,'Left'),(1,'Right')]:
  pad='GroundPad_'+label+'_'+side;feet.append(pad)
  obox(pad,(s*half,y,.023),(.14,.16,.046),3,'finite planar rubber foot, underside Z=0')
  joint(pad,bar,[(s*half+x,y,.040) for x in [-.025,0,.025]])
obox('Rail_Main',(0,.50,.31),(.14,1.84,.08),1,'single full-length longitudinal slide beam; Y axis, top Z=.35 and underside Z=.27')
beam('Frame_FrontDiagonal',(0,-.90,.08),(0,-.30,.31),.11,.085,0,'inclined structural rail support joining front floor bar')
joint('Frame_FrontDiagonal','Frame_FloorBar_Front',tx((0,-.875,.090)))
joint('Frame_FrontDiagonal','Rail_Main',tx((0,-.32,.300)))
obox('Frame_RearPost',(0,1.26,.18),(.11,.10,.23),0,'short finite rear rail post')
joint('Frame_RearPost','Frame_FloorBar_Rear',tx((0,1.26,.088)))
joint('Frame_RearPost','Rail_Main',tx((0,1.26,.282)))
# Stops cross the entire track and physically overlap it; only one stored seat pose is supplied.
for label,y in [('Front',-.400),('Rear',1.400)]:
 name='Rail_EndStop_'+label;obox(name,(0,y,.365),(.19,.030,.070),4,'physical axial stop, not a declared or invisible limit')
 joint(name,'Rail_Main',tx((0,y,.340),.035))
# Slider assembly: two upper rollers carry the seat and two lower rollers capture the rail.
# 5 mm intentional static tread engagement is finite support, not a friction/rolling claim.
rollers=[]
for label,y,z,r in [('TopFront',.40,.390,.045),('TopRear',.70,.390,.045),('LowerFront',.46,.235,.040),('LowerRear',.64,.235,.040)]:
 name='Slider_Roller_'+label;rollers.append(name)
 rod(name,(-.130,y,z),(.130,y,z),r,3,'closed axis-X roller, supporting or capturing the longitudinal rail',24)
 contact_z=.3475 if label.startswith('Top') else .2725
 joint(name,'Rail_Main',tx((0,y,contact_z),.035))
 axle='Slider_Axle_'+label;rod(axle,(-.150,y,z),(.150,y,z),.012,1,'continuous roller axle through both carrier cheeks',16)
 joint(axle,name,tx((0,y,z),.065))
 for s,side in [(-1,'Left'),(1,'Right')]:
  joint(axle,'Slider_Cheek_'+side,[(s*.133,y+d,z) for d in [-.003,0,.003]])
for s,side in [(-1,'Left'),(1,'Right')]:
 obox('Slider_Cheek_'+side,(s*.130,.55,.335),(.035,.40,.280),0,'outside rail guide cheek, capturing upper/lower axles without blocking rail')
obox('Slider_SeatBridge',(0,.55,.470),(.34,.32,.060),0,'cross-seat bridge seated on both carrier cheeks')
for s,side in [(-1,'Left'),(1,'Right')]:joint('Slider_SeatBridge','Slider_Cheek_'+side,[(s*.130,y,.465) for y in [.46,.55,.64]])
padded_seat('Seat_ChamferedPad',(0,.55,.525),.39,.35,3)
joint('Seat_ChamferedPad','Slider_SeatBridge',tx((0,.55,.497),.09))
# Two inclined foot trays with a real open strap each. Local V points toward raised toes.
U=Vector((1,0,0));V=Vector((0,-math.cos(math.radians(55)),math.sin(math.radians(55))));N=U.cross(V)
# N points toward the underside with U,V above, so explicitly choose the outward normal.
N=Vector((0,math.sin(math.radians(55)),math.cos(math.radians(55))))
obox('Feet_SupportCrossbar',(0,-.327,.307),(.60,.085,.065),0,'foot-tray support crossing rail at its nose')
joint('Feet_SupportCrossbar','Rail_Main',tx((0,-.327,.310),.04))
foot_frames=[]
for s,side in [(-1,'Left'),(1,'Right')]:
 C=Vector((s*.215,-.400,.430));plate='FootTray_'+side;foot_frames.append({'side':side,'centre_m':list(C),'toe_axis':list(V),'outward_normal':list(N)})
 obox(plate,C,(.190,.310,.028),0,'solid toe-up foot tray with real supported heel',U,V,N)
 joint(plate,'Feet_SupportCrossbar',[C+V*(-.143)+U*x for x in [-.025,0,.025]])
 # Two raised longitudinal edges and a solid heel stop form a real shallow cup.
 for t,edge in [(-1,'Inner'),(1,'Outer')]:
  name='FootTray_Rim_'+side+'_'+edge;rc=C+U*(t*.087)+N*.019
  obox(name,rc,(.022,.300,.045),4,'raised side edge of shallow foot tray',U,V,N)
  joint(name,plate,[rc+V*v-N*.015 for v in [-.09,0,.09]])
 name='FootTray_HeelStop_'+side;hc=C+V*(-.146)+N*.025
 obox(name,hc,(.180,.028,.058),4,'finite heel stop across the lower end of tray',U,V,N)
 joint(name,plate,[hc+U*x-N*.022 for x in [-.05,0,.05]])
 for t,edge in [(-1,'Inner'),(1,'Outer')]:
  name='FootStrap_Upright_'+side+'_'+edge;sc=C+U*(t*.087)+V*.025+N*.043
  obox(name,sc,(.018,.050,.100),3,'solid arch end rooted into foot tray, leaving central aperture open',U,V,N)
  joint(name,plate,[sc+V*v-N*.040 for v in [-.010,0,.010]])
 strap='FootStrap_Bridge_'+side;sc=C+V*.025+N*.088
 obox(strap,sc,(.194,.046,.020),3,'solid upper strap spans true open volume above tray',U,V,N)
 for t,edge in [(-1,'Inner'),(1,'Outer')]:joint(strap,'FootStrap_Upright_'+side+'_'+edge,[sc+U*(t*.087)+V*v for v in [-.010,0,.010]])
# Annular resistance enclosure with visible grilles and a separately editable internal wheel.
F=Vector((0,-.88,.570));fanaxis={'c':F,'u':(0,1,0),'v':(0,0,1),'w':(1,0,0),'n':48}
ring('Resistance_ThickAnnularCover',.215,.280,-.100,.100,2,'thick annular fan enclosure with genuine central cavity',**fanaxis)
obox('Frame_FanStanchion',(0,-.88,.238),(.12,.11,.33),0,'upright front frame enters bottom annular enclosure wall')
joint('Frame_FanStanchion','Frame_FloorBar_Front',tx((0,-.88,.090)))
joint('Frame_FanStanchion','Resistance_ThickAnnularCover',tx((0,-.88,.305)))
rod('Resistance_InternalWheel',F+Vector((-.069,0,0)),F+Vector((.069,0,0)),.205,5,'separate solid dark resistance wheel enclosed by the guard',48)
rod('Resistance_CentralHub',F+Vector((-.125,0,0)),F+Vector((.125,0,0)),.057,4,'central cylinder supporting internal wheel and exterior grille spokes',24)
joint('Resistance_CentralHub','Resistance_InternalWheel',[F+Vector((x,.020,0)) for x in [-.045,0,.045]])
for s,side in [(-1,'Left'),(1,'Right')]:
 # Spokes overlap both hub and outer annulus by finite lengths, and extend outside the inner wheel face.
 for i in range(10):
  a=math.tau*i/10;R=Vector((0,math.cos(a),math.sin(a)));T=Vector((0,-math.sin(a),math.cos(a)));x=s*.099
  name=f'Resistance_Grille_{side}_{i:02d}';obox(name,F+Vector((x,0,0))+R*.151,(.025,.237,.014),0,'radial solid protective grille, open between ribs',Vector((1,0,0)),R,T)
  joint(name,'Resistance_CentralHub',[F+Vector((x+d,0,0))+R*.045 for d in [-.004,0,.004]])
  joint(name,'Resistance_ThickAnnularCover',[F+Vector((x-s*.008,0,0))+R*r for r in [.235,.245,.255]])
 # Small central bearing caps are supported through the projecting central hub.
 name='Resistance_BearingCap_'+side
 rod(name,F+Vector((s*.118,0,0)),F+Vector((s*.139,0,0)),.040,1,'small external static bearing-style cap',24)
 joint(name,'Resistance_CentralHub',[F+Vector((s*.122,y,0)) for y in [-.015,0,.015]])
# Handle is explicitly parked on a visible solid cradle, not suspended on a cable.
obox('Handle_DockArm',(0,-.540,.650),(.11,.245,.045),0,'fixed cradle arm embedded into upper-rear fan wall')
joint('Handle_DockArm','Resistance_ThickAnnularCover',tx((0,-.645,.650),.025))
obox('Handle_DockSaddle',(0,-.445,.671),(.095,.085,.042),4,'small solid parking saddle carrying the horizontal pull handle')
joint('Handle_DockSaddle','Handle_DockArm',tx((0,-.455,.660),.02))
rod('Handle_Crossbar',(-.222,-.445,.698),(.222,-.445,.698),.020,1,'one continuous independent transverse return pull handle',24)
joint('Handle_Crossbar','Handle_DockSaddle',tx((0,-.445,.687),.02))
for s,side in [(-1,'Left'),(1,'Right')]:
 name='Handle_Grip_'+side
 rod(name,(s*.089,-.445,.698),(s*.220,-.445,.698),.027,3,'thick solid grip sleeve on handle end',24)
 joint(name,'Handle_Crossbar',[(s*x,-.445,.698) for x in [.11,.15,.19]])
obox('Return_Fairlead',(0,-.670,.731),(.075,.055,.050),4,'finite cable outlet seated in the guard wall')
joint('Return_Fairlead','Resistance_ThickAnnularCover',tx((0,-.680,.725),.018))
rod('Return_ConnectedCord',(0,-.674,.733),(0,-.445,.698),.007,5,'straight fixed return cord, connected to housing outlet and parked handle; no rope simulation',12)
joint('Return_ConnectedCord','Return_Fairlead',[(x,-.670,.732) for x in [-.002,0,.002]])
joint('Return_ConnectedCord','Handle_Crossbar',[(x,-.450,.699) for x in [-.002,0,.002]])
SEAT_POSE_Y=.55
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
 assert bad==0 and vol>1e-13 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,5)
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
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.000010,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(feet);todo=list(feet)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)

# Four finite ground patches are derived from actual triangles, not AABB minima.
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
 return {'label':label,'start_m':list(start),'direction':list(direction),'length_m':length}
apertures=[]
for frame in foot_frames:
 c,v,n=Vector(frame['centre_m']),Vector(frame['toe_axis']),Vector(frame['outward_normal'])
 for x in [-.04,0,.04]:
  apertures.append(clear_ray('FootStrap_'+frame['side'],c+Vector((x,0,0))+v*(-.02)+n*.052,v,.09))
# Positive-width front-to-seat air corridor: physical ray tests through intended body-use empty band.
for x in [-.08,0,.08]:
 for z in [.66,.78,.96]:apertures.append(clear_ray('UnobstructedAboveRail',(x,-.20,z),(0,1,0),.57))
# Actual-vertex to actual-triangle distances, independently complemented by full pair QA.
clearances=[]
for obj,targets,minimum in [('Slider_Cheek_Left',['Rail_Main'],.040),('Slider_Cheek_Right',['Rail_Main'],.040),('Seat_ChamferedPad',['Rail_Main'],.140),('Resistance_InternalWheel',['Resistance_ThickAnnularCover'],.008)]:
 o=byname[obj];near=[]
 for v in o.data.vertices:
  p=o.matrix_world@v.co;distance=min(trees[name].find_nearest(p)[3] for name in targets)
  assert not any(inside(trees[name],p) for name in targets) and distance>minimum,(obj,list(p),distance)
  near.append(distance)
 clearances.append({'object':obj,'against':targets,'minimum_vertex_to_actual_triangle_distance_m':min(near),'required_m':minimum,'tested_vertices':len(near)})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<14000
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
 'real_strap_and_user_band_apertures':apertures,'geometry_clearances':clearances,'finite_ground_patches':supports,
 'stored_seat_centre_y_m':SEAT_POSE_Y,'seat_axis':'Y','tested_seat_poses_m':[SEAT_POSE_Y],
 'continuous_motion_or_body_fit_claim':False,'foot_tray_frames':foot_frames,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fitness/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.16,.38));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2.2,-3.5,4.3),460,3.0),('Fill',(3.1,-.4,2.9),310,2.5),('Rim',(-.8,3.2,3.4),380,2.3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.95;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3.2,-4.2,2.8),'gray-back3q':(-3.2,4.1,2.5)} if gray else {
 'thumbnail':(3.2,-4.2,2.8),'qa-front':(0,-4,.38),'qa-side':(4,.16,.38),'qa-top':(0,.16,4),
 'qa-back':(0,4,.38),'qa-wireframe':(3.2,-4.2,2.8)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0005;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.38)),('silhouette-128-side',(4,.16,.38))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
