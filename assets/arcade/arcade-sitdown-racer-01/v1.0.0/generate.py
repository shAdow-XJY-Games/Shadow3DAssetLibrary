"""Original single static sit-down arcade racer, metres, Z up, rider faces +Y.
One grounded shared base, bucket seat, open footwell, two fixed pedals, tilted
steering wheel/support frame and display pod. Exclusive Screen_Runtime mesh.
Bpy-only source; --geometry-only / --no-render / --gray-only / --preview-only /
--extra-views. Every render uses a fresh actual GLB import. No gameplay,
input/electrical function, animated controls, human fit or safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='arcade-sitdown-racer-01';VERSION='1.0.0';TITLE='Sit-Down Arcade Racer'
DESCRIPTION=('Original single static low-poly sit-down arcade racing machine on a continuous chamfered ground base. '
 'An orange deep bucket seat has a reclined back, side bolsters and enclosed lower support. An open footwell leads to two separate inclined fixed pedals on real struts. '
 'A three-spoke tilted steering ring is attached by a shaft to a separate console with two base-supported inclined legs. A broad framed blank screen pod is supported by the front cabinet. '
 'Screen_Runtime is an exclusive named mesh with its own Runtime screen exclusive solid PBR material, ready for content replacement by a consuming application. '
 'Teal shell, coral upholstery, dark rubber and pale bezel remain separately editable; all components have actual interior support witnesses leading to the shared base. '
 'Finite seat, lap and foot-approach volumes are geometrically empty; the geometry is not a human-fit guarantee. '
 'Metres, source Z up, rider facing +Y, origin at ground projection of base centre. Seven solid PBR materials, no textures or external dependencies. '
 'Static game visual only: no game content, trademarks, networking, input device, steering/pedal action, driving physics, human fit, load or amusement-equipment safety certification.')
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
for name,color,rough,metal in [('Midnight_Chassis',(.026,.045,.052,1),.57,.15),('Lagoon_Shell',(.035,.31,.34,1),.43,.08),
 ('WarmIvory_Bezel',(.74,.70,.55,1),.50,0),('Coral_Upholstery',(.64,.105,.047,1),.70,0),
 ('Rubber_Controls',(.018,.022,.025,1),.72,0),('BrushedSteel_Fittings',(.34,.39,.39,1),.36,.70),
 ('Runtime screen exclusive',(.015,.065,.092,1),.34,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('SitDownArcadeRacer',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['rider_direction']='+Y';root['static_visual_only']=True
root['origin_datum']='ground projection of shared base centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o.parent=root;me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def prism(name,xy,low,high,material,role,axis='Z'):
 n=len(xy);vs=[(x,y,z) if axis=='Z' else (z,x,y) for z in [low,high] for x,y in xy]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],material,role)
def octagon(xmin,xmax,ymin,ymax,c):
 return [(xmin+c,ymin),(xmax-c,ymin),(xmax,ymin+c),(xmax,ymax-c),(xmax-c,ymax),(xmin+c,ymax),(xmin,ymax-c),(xmin,ymin+c)]
def obox(name,centre,width,height,depth,normal,material,role):
 c=Vector(centre);n=Vector(normal).normalized();u=Vector((1,0,0));v=n.cross(u).normalized()
 vs=[c+u*(sx*width/2)+v*(sy*height/2)+n*(sz*depth/2) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def tube(name,points,radius,material,role,n=12):
 pp=[Vector(p) for p in points];vs=[]
 for i,p in enumerate(pp):
  axis=(pp[min(i+1,len(pp)-1)]-pp[max(i-1,0)]).normalized()
  ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0));u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
  vs.extend(p+math.cos(math.tau*j/n)*radius*u+math.sin(math.tau*j/n)*radius*v for j in range(n))
 fs=[tuple(reversed(range(n))),tuple((len(pp)-1)*n+j for j in range(n))]
 for i in range(len(pp)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 return mesh(name,vs,fs,material,role)
def torus(name,c,n,R,r,material,role,N=32,K=8):
 c=Vector(c);n=Vector(n).normalized();u=Vector((1,0,0));v=n.cross(u).normalized();vs=[]
 for i in range(N):
  radial=u*math.cos(math.tau*i/N)+v*math.sin(math.tau*i/N)
  for j in range(K):vs.append(c+radial*(R+r*math.cos(math.tau*j/K))+n*(r*math.sin(math.tau*j/K)))
 fs=[(i*K+j,((i+1)%N)*K+j,((i+1)%N)*K+(j+1)%K,i*K+(j+1)%K) for i in range(N) for j in range(K)]
 return mesh(name,vs,fs,material,role)
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
def triple_x(c,d=.018):return [Vector(c)+Vector((x,0,0)) for x in [-d,0,d]]
# One unbroken chamfered platform ties rear seat, footwell and front display together.
prism('SharedBase_Continuous',octagon(-.58,.58,-1.35,1.25,.10),0,.16,0,'single finite grounded chassis under every assembly')
prism('Seat_LowerShell',octagon(-.43,.43,-1.27,-.40,.09),.14,.34,1,'integral low bucket-seat shell attached to the shared base')
joint('Seat_LowerShell','SharedBase_Continuous',triple_x((0,-.85,.15),.20))
prism('Display_FootPlinth',octagon(-.49,.49,.71,1.17,.065),.14,.30,1,'front display support plinth attached to common chassis')
joint('Display_FootPlinth','SharedBase_Continuous',triple_x((0,.94,.15),.25))
box('Footwell_Floor',(0,.18,.20),(.72,1.17,.10),0,'real open cockpit footwell floor, no solid block in leg passage')
joint('Footwell_Floor','SharedBase_Continuous',triple_x((0,.2,.155),.20))
# Raised side strips have real depth and embedded support, not overlapping decal sheets.
for s,label in [(-1,'Left'),(1,'Right')]:
 box('BaseAccent_'+label,(s*.573,-.10,.105),(.025,1.75,.085),1,'side-mounted inset-thickness base accent')
 joint('BaseAccent_'+label,'SharedBase_Continuous',[(s*.568,y,.105) for y in [-.60,-.10,.40]])
box('Seat_Pedestal',(0,-.86,.40),(.56,.54,.24),0,'finite pedestal joins lower shell and seat cushion')
joint('Seat_Pedestal','Seat_LowerShell',triple_x((0,-.86,.32),.15))
prism('Seat_Cushion',octagon(-.29,.29,-1.12,-.53,.055),.48,.58,3,'deep orange seat pad with visible forward lip')
joint('Seat_Cushion','Seat_Pedestal',triple_x((0,-.86,.50),.16))
# Reclined structural back and separate thick upholstery; upper back is farther rearward.
seat_n=Vector((0,math.sqrt(1-.22**2),.22));seat_v=Vector((0,-.22,math.sqrt(1-.22**2)));seat_c=Vector((0,-1.135,.77))
obox('Seat_BackShell',seat_c,.69,.92,.16,seat_n,1,'reclined bucket back with a buried connection into lower shell')
joint('Seat_BackShell','Seat_LowerShell',triple_x(seat_c-seat_v*.445,.16))
obox('Seat_BackCushion',seat_c+seat_n*.085+seat_v*.025,.51,.75,.055,seat_n,3,'thick reclined coral back pad nested into back shell')
joint('Seat_BackCushion','Seat_BackShell',triple_x(seat_c+seat_n*.068+seat_v*.02,.15))
for s,label in [(-1,'Left'),(1,'Right')]:
 profile=[(-1.17,.30),(-.54,.30),(-.45,.43),(-.52,.65),(-.79,.68),(-1.17,.86)]
 prism('Seat_SideBolster_'+label,profile,min(s*.23,s*.39),max(s*.23,s*.39),1,'shaped bucket side wing containing seat cushion without crossing seat void',axis='X')
 joint('Seat_SideBolster_'+label,'Seat_LowerShell',[(s*.32,y,.32) for y in [-1.05,-.80,-.60]])
 # Coral pad follows the inner side wall, above the seat surface.
 profile=[(-1.06,.56),(-.56,.56),(-.55,.61),(-.79,.645),(-1.06,.77)]
 prism('Seat_BolsterPad_'+label,profile,min(s*.210,s*.255),max(s*.210,s*.255),3,'raised inner upholstered side pad with real shell overlap',axis='X')
 joint('Seat_BolsterPad_'+label,'Seat_SideBolster_'+label,[(s*.25,y,z) for y,z in [(-.95,.64),(-.80,.60),(-.63,.59)]])
# Screen support rises only at the far end; it does not occupy the rider's footwell.
profile=[(.77,.23),(1.13,.23),(1.12,1.20),(.76,1.07),(.66,.64)]
prism('Display_Cabinet',profile,-.42,.42,1,'tapered front screen cabinet with finite broad support',axis='X')
joint('Display_Cabinet','Display_FootPlinth',triple_x((0,.94,.265),.25))
screen_n=Vector((0,-math.sqrt(1-.12**2),.12));screen_v=screen_n.cross(Vector((1,0,0)));screen_c=Vector((0,.87,1.42))
obox('Display_BezelHousing',screen_c,1.02,.70,.13,screen_n,2,'pale deep widescreen bezel pod physically supported by front cabinet')
joint('Display_BezelHousing','Display_Cabinet',triple_x((0,.88,1.105),.25))
obox('Screen_Runtime',screen_c+screen_n*.071,.84,.49,.024,screen_n,6,'exclusive blank thin closed display solid; consuming application may replace content')
joint('Screen_Runtime','Display_BezelHousing',triple_x(screen_c+screen_n*.062,.25))
# Dedicated planar UV coordinates are available without bundling textures or game content.
screen_mesh=byname['Screen_Runtime'].data;screen_uv=screen_mesh.uv_layers.new(name='ScreenUV')
for loop in screen_mesh.loops:
 q=screen_mesh.vertices[loop.vertex_index].co-(screen_c+screen_n*.071)
 screen_uv.data[loop.index].uv=(q.x/.84+.5,q.dot(screen_v)/.49+.5)
# Independent top visor reads as a screen pod, without game artwork or a brand marquee.
obox('Display_TopVisor',screen_c+screen_v*.333+screen_n*.015,1.075,.065,.20,screen_n,1,'short deep top visor attached through screen bezel shell')
joint('Display_TopVisor','Display_BezelHousing',triple_x(screen_c+screen_v*.325,.30))
# Console legs flank an actual empty knee passage. Both run into the same floor chassis.
for s,label in [(-1,'Left'),(1,'Right')]:
 a=Vector((s*.38,.55,.12));b=Vector((s*.38,.43,.98))
 tube('Console_Support_'+label,[a,b],.062,0,'inclined support leg beside leg passage, joined to shared base and console',8)
 joint('Console_Support_'+label,'SharedBase_Continuous',[a.lerp(b,t) for t in [.015,.025,.035]])
 joint('Console_Support_'+label,'Console_Deck',[b.lerp(a,t) for t in [.010,.020,.030]])
prism('Console_Deck',[(.19,.88),(.69,.88),(.64,1.09),(.26,1.09)],-.43,.43,1,'separate sloped steering console supported by paired legs',axis='X')
# Tilted three-spoke steering wheel; its axis is neither horizontal floor nor a vertical pole.
wheel_n=Vector((0,-.85,math.sqrt(1-.85**2)));wheel_u=Vector((1,0,0));wheel_v=wheel_n.cross(wheel_u)
wheel_c=Vector((0,-.02,1.09));shaft_a=wheel_c-wheel_n*.30;shaft_b=wheel_c+wheel_n*.028
shaft=tube('Steering_Shaft',[shaft_a,shaft_b],.035,5,'inclined shaft embedded in console and steering hub',16)
joint('Steering_Shaft','Console_Deck',[shaft_a+wheel_n*d for d in [.003,.007,.011]])
tube('Steering_Hub',[wheel_c-wheel_n*.042,wheel_c+wheel_n*.04],.059,4,'closed hub of fixed tilted steering wheel',16)
joint('Steering_Hub','Steering_Shaft',[wheel_c+wheel_n*d for d in [-.018,0,.018]])
torus('Steering_Rim',wheel_c,wheel_n,.20,.024,4,'continuous tilted low-poly steering ring with real spoke openings')
for i,angle in enumerate([0,math.pi,-math.pi/2],1):
 radial=wheel_u*math.cos(angle)+wheel_v*math.sin(angle)
 tube(f'Steering_Spoke_{i:02d}',[wheel_c+radial*.025,wheel_c+radial*.205],.016,5,'solid radial spoke from hub into rim',8)
 joint(f'Steering_Spoke_{i:02d}','Steering_Hub',[wheel_c+radial*d for d in [.030,.035,.040]])
 joint(f'Steering_Spoke_{i:02d}','Steering_Rim',[wheel_c+radial*d for d in [.192,.197,.202]])
# Two fixed pedal plates, each with its own finite load path through an inclined strut.
pedal_n=Vector((0,-.76,math.sqrt(1-.76**2)));pedal_v=pedal_n.cross(Vector((1,0,0)));pedals=[]
for x,label in [(-.15,'Left'),(.15,'Right')]:
 c=Vector((x,.53,.39));a=Vector((x,.61,.225));b=c-pedal_n*.008
 tube('Pedal_Strut_'+label,[a,b],.037,5,'fixed inclined pedal support physically connected to footwell floor and plate',8)
 joint('Pedal_Strut_'+label,'Footwell_Floor',[a.lerp(b,t) for t in [.02,.05,.08]])
 obox('Pedal_Plate_'+label,c,.15,.23,.036,pedal_n,5,'inclined static pedal plate; no hinge or animation claim')
 joint('Pedal_Plate_'+label,'Pedal_Strut_'+label,[b+(a-b).normalized()*d for d in [.002,.005,.008]])
 for j,k in enumerate([-.065,0,.065],1):
  name=f'Pedal_Grip_{label}_{j:02d}';centre=c+pedal_v*k+pedal_n*.021
  obox(name,centre,.12,.024,.014,pedal_n,4,'raised static rubber tread embedded in pedal plate')
  joint(name,'Pedal_Plate_'+label,triple_x(c+pedal_v*k+pedal_n*.016,.035))
 pedals.append({'plate':'Pedal_Plate_'+label,'strut':'Pedal_Strut_'+label,'centre_m':list(c),'normal':list(pedal_n),'width_m':.15,'height_m':.23})
# Small console buttons are visual accents, distinct from the exclusive replaceable screen.
for i,x in enumerate([-.30,.30],1):
 tube(f'Console_Button_{i:02d}',[(x,.49,1.08),(x,.49,1.115)],.026,3,'fixed round console accent; no electronic behavior',12)
 joint(f'Console_Button_{i:02d}','Console_Deck',triple_x((x,.49,1.085),.009))
# Normalize actual closed triangles before any support or opening measurement.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for v in o.data.vertices:v.co=Vector(tuple(round(float(c),6) for c in v.co))
 o.data.update()
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};world_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-13 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 world_triangles[o.name]=[[vv[i] for i in t.vertices] for t in o.data.loop_triangles]
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,6)
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
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.00015,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen={'SharedBase_Continuous'};todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
# Finite downward-facing triangles, not a tangent or AABB, establish ground contact.
ground_patch=[]
for tri in world_triangles['SharedBase_Continuous']:
 cross=(tri[1]-tri[0]).cross(tri[2]-tri[0])
 if max(abs(p.z) for p in tri)<1e-7 and cross.z<0:ground_patch.append({'vertices_m':[list(p) for p in tri],'area_m2':cross.length/2})
ground_area=sum(t['area_m2'] for t in ground_patch);assert ground_area>2.5
# Exact triangle-box separating-axis tests plus solid containment establish real voids.
def triangle_box_overlap(tri,lo,hi):
 centre=(lo+hi)*.5;half=(hi-lo)*.5;v=[p-centre for p in tri]
 axes=[Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))];edges=[v[1]-v[0],v[2]-v[1],v[0]-v[2]]
 axes += [edges[0].cross(edges[1])]+[e.cross(a) for e in edges for a in axes[:3]]
 for axis in axes:
  if axis.length_squared<1e-18:continue
  projections=[q.dot(axis) for q in v];r=sum(abs(axis[i])*half[i] for i in range(3))
  if min(projections)>r+1e-8 or max(projections)<-r-1e-8:return False
 return True
void_specs=[('seat_pelvis',(-.20,-.92,.60),(.20,-.54,.80)),('seat_torso',(-.22,-.93,.81),(.22,-.57,1.16)),
 ('lap_knee_passage',(-.22,-.52,.55),(.22,.13,.78)),('foot_approach',(-.24,-.32,.27),(.24,.32,.48))]
clear_volumes=[]
for name,lo,hi in void_specs:
 lo,hi=Vector(lo),Vector(hi);hits=[]
 for part,ts in world_triangles.items():
  if inside(trees[part],(lo+hi)*.5) or any(triangle_box_overlap(t,lo,hi) for t in ts):hits.append(part)
 assert not hits,('Occupied declared actual clearance volume',name,hits)
 clear_volumes.append({'name':name,'min_m':list(lo),'max_m':list(hi),'method':'all actual triangles SAT against finite rectangular volume, plus solid-centre containment','intersecting_meshes':hits})
def clear_ray(label,start,direction,length):
 start,direction=Vector(start),Vector(direction).normalized();hits=[]
 for name,tree in trees.items():
  q,_,_,_=tree.ray_cast(start,direction,length)
  if q is not None:hits.append(name)
 assert not hits,('Blocked real aperture',label,list(start),hits)
 return {'start_m':list(start),'direction':list(direction),'length_m':length}
wheel_openings=[]
for angle in [math.pi/4,3*math.pi/4,-math.pi/4,-3*math.pi/4]:
 radial=wheel_u*math.cos(angle)+wheel_v*math.sin(angle);c=wheel_c+radial*.115
 rays=[clear_ray('steering_spoke_aperture',c+wheel_u*dx-wheel_n*.05,wheel_n,.10) for dx in [-.008,0,.008]]
 wheel_openings.append({'angle_rad':angle,'rays':rays})
assert .45<wheel_n.z<.65 and abs(wheel_n.y)>.8
# Exclusive display replacement boundary is verified by object, mesh and material identity.
screen=byname['Screen_Runtime'];assert len(screen.data.materials)==1 and screen.data.materials[0] is mats[6]
assert [o.name for o in parts if mats[6] in list(o.data.materials)]==['Screen_Runtime']
assert sum(o.data is screen.data for o in parts)==1
assert len(screen.data.uv_layers)==1 and len(screen.data.uv_layers[0].data)>0
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<10000
# Full solid PBR and oriented-world-triangle equality across native-to-GLB export.
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
 'clear_occupancy_volumes':clear_volumes,'finite_ground_patches':[{'name':'SharedBase_Continuous','area_m2':ground_area,'triangles':ground_patch}],
 'steering_wheel':{'centre_m':list(wheel_c),'axis':list(wheel_n),'major_radius_m':.20,'minor_radius_m':.024,'openings':wheel_openings},
 'two_fixed_pedals':pedals,'runtime_screen':{'mesh':'Screen_Runtime','material':'Runtime screen exclusive','exclusive_mesh_and_material':True,'blank_closed_solid':True,'planar_display_uv':True},
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/arcade/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
screen=next(o for o in parts if o.name=='Screen_Runtime');assert len(screen.data.materials)==1
assert len(screen.data.uv_layers)==1
screenmat=screen.data.materials[0];assert [o.name for o in parts if screenmat in list(o.data.materials)]==['Screen_Runtime']
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts),'exclusive_runtime_screen':True};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((0,-.04,.80));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-3.8,-4.5,6.2),650,4.0),('Fill',(4.3,-.1,4.8),400,3.5),('Rim',(.1,4.5,5.5),600,3.5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.20;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3.7,-4.6,3.3),'gray-back3q':(-3.7,4.6,3.3)} if gray else {
 'thumbnail':(4.8,-3.1,3.6),'qa-front':(0,-5.5,1.9),'qa-side':(5.5,-.04,1.9),'qa-top':(0,-.04,6),
 'qa-back':(0,5.5,1.9),'qa-wireframe':(4.8,-3.1,3.6)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0007;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-5.5,.80)),('silhouette-128-side',(5.5,-.04,.80))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
