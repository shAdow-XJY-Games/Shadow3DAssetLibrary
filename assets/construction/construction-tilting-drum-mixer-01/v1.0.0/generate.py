"""Original static tilting-drum concrete mixer, metres, source Z up, front -Y.
Self-contained constant-PBR meshes. One fixed pose only, no motor/tilt animation.
--geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
Every image renders a fresh import of the actual exported GLB.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='construction-tilting-drum-mixer-01';VERSION='1.0.0';TITLE='Tilted Open Drum Concrete Mixer'
DESCRIPTION=('Original static low-poly small concrete mixer with an ochre pear-shaped thick drum, a genuinely open narrowed mouth, '
 'deep interior and three solid wall-rooted paddles. A rear drum spindle sits on a U-shaped tilting cradle with two horizontal '
 'trunnions seated on finite lower facets of true bored side bearings. A separate open handwheel, three spokes, rear motor shroud, '
 'braced teal chassis, solid axle, two faceted wheels and two flat front feet complete the independent assembly. '
 'All editable closed components connect through actual joints to finite ground patches. One fixed tilted pose, four solid PBR materials, '
 'metres, source Z up, ground-centre origin and front -Y. No texture or external asset. '
 'Distinct from a horizontal sealed garden composter. Static game visual only: no mixing performance, drum rotation, tilt animation, '
 'pour trajectory, complete mechanical drive, electrical operation, load, stability or construction-safety certification.')
# Pure mathematical mesh layout: executed before Blender for a light source preflight.
G={};LINKS=[];CONTACTS=[];SPINES={};FEET=[];WHEELS=[];BLADES=[]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def length(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/length(a))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),6) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 return name
def box(name,loc,size,material,role,axes=((1,0,0),(0,1,0),(0,0,1))):
 vs=[add(loc,add(mul(axes[0],sx*size[0]/2),add(mul(axes[1],sy*size[1]/2),mul(axes[2],sz*size[2]/2)))) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role)
def rod(name,a,b,radius,material,role,n=12):
 axis=unit(sub(b,a));ref=(0,0,1) if abs(axis[2])<.9 else (1,0,0);u=unit(cross(axis,ref));v=unit(cross(axis,u))
 vs=[add(p,mul(add(mul(u,math.cos(math.tau*i/n)),mul(v,math.sin(math.tau*i/n))),radius)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 SPINES[name]=(a,b);return mesh(name,vs,fs,material,role)
def cyl_x(name,x0,x1,y,z,radius,material,role,n=16):
 phase=math.pi/n;vs=[(x,y+radius*math.cos(phase+math.tau*i/n),z+radius*math.sin(phase+math.tau*i/n)) for x in [x0,x1] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role)
def ring_x(name,x0,x1,y,z,ro,ri,material,role,n=16):
 phase=math.pi/n;vs=[(x,y+r*math.cos(phase+math.tau*i/n),z+r*math.sin(phase+math.tau*i/n)) for r in [ro,ri] for x in [x0,x1] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def end_link(a,b,end):
 p,q=SPINES[a];point=p if end==0 else q;axis=unit(sub(q,p) if end==0 else sub(p,q));LINKS.append((a,b,[add(point,mul(axis,d)) for d in [.006,.010,.014]]))
TILT=math.radians(35);A=(0,-math.cos(TILT),math.sin(TILT));U=(1,0,0);V=(0,math.sin(TILT),math.cos(TILT));P=(0,.28,1.04)
def local(u,v,t):return add(P,add(mul(U,u),add(mul(V,v),mul(A,t))))
OUTER=[(0,.18),(.10,.34),(.28,.43),(.48,.40),(.68,.29),(.75,.27)]
INNER=[(.055,.14),(.145,.29),(.28,.39),(.48,.36),(.68,.25),(.75,.23)]
def interp(profile,t):
 for (ta,ra),(tb,rb) in zip(profile[:-1],profile[1:]):
  if ta<=t<=tb:return ra+(rb-ra)*(t-ta)/(tb-ta)
 raise ValueError(t)
profile=OUTER+INNER[::-1];N=32;vs=[]
for t,r in profile:vs.extend(local(r*math.cos(math.tau*i/N),r*math.sin(math.tau*i/N),t) for i in range(N))
fs=[]
for k in range(len(profile)-1):
 for i in range(N):j=(i+1)%N;fs.append((k*N+i,k*N+j,(k+1)*N+j,(k+1)*N+i))
# Two distinct filled back disks close a genuinely thick bottom, not the mouth.
for ring,t,reverse in [(0,0,True),(len(profile)-1,.055,False)]:
 c=len(vs);vs.append(local(0,0,t))
 for i in range(N):
  j=(i+1)%N;fs.append((c,ring*N+j,ring*N+i) if reverse else (c,ring*N+i,ring*N+j))
mesh('Drum_ThickPearShell',vs,fs,0,'closed thick open-mouth shell with real bottom')
# Three closed long paddles follow the inside contour and embed into its wall.
for b in range(3):
 name=f'Paddle_{b+1:02d}';BLADES.append(name);stations=[.18,.28,.40,.48,.61];vs=[]
 for t in stations:
  r=interp(INNER,t);a=.45+b*math.tau/3+.22*(t-.18)
  for rr,aa in [(r-.075,a-.035),(r+.012,a-.035),(r+.012,a+.035),(r-.075,a+.035)]:vs.append(local(rr*math.cos(aa),rr*math.sin(aa),t))
 fs=[(3,2,1,0),(16,17,18,19)]
 for k in range(4):
  for i in range(4):j=(i+1)%4;fs.append((k*4+i,k*4+j,(k+1)*4+j,(k+1)*4+i))
 mesh(name,vs,fs,3,'solid internal fixed paddle with root embedded in real shell wall')
 points=[]
 for t in [.23,.34,.46,.565]:
  a=.45+b*math.tau/3+.22*(t-.18);r=interp(INNER,t)+.005
  points.append(local(r*math.cos(a),r*math.sin(a),t))
 LINKS.append((name,'Drum_ThickPearShell',points))
# Chassis: front grounded flat pads, rear faceted wheels, continuous tied rails.
WHEEL_R=.22;WHEEL_Z=WHEEL_R*math.cos(math.pi/16)
for sign,side in [(-1,'Left'),(1,'Right')]:
 x=sign*.48;foot='Foot_'+side;FEET.append(foot)
 box(foot,(x,-.55,.030),(.18,.22,.060),2,'flat finite front ground support')
 rod('FrontLeg_'+side,(x,-.55,.025),(x,-.55,.30),.045,1,'front upright support leg');end_link('FrontLeg_'+side,foot,0)
 rod('BaseRail_'+side,(x,-.575,.28),(x,.625,.28),.040,1,'longitudinal chassis rail')
 link('BaseRail_'+side,'FrontLeg_'+side,(x,-.55,.28))
 rod('AxleBracket_'+side,(x,.50,WHEEL_Z),(x,.50,.30),.045,1,'rear axle to base saddle')
 end_link('AxleBracket_'+side,'BaseRail_'+side,1)
 wheel='Wheel_'+side;WHEELS.append(wheel);cyl_x(wheel,sign*.64-.07,sign*.64+.07,.50,WHEEL_Z,WHEEL_R,2,'closed faceted wheel with finite ground facet')
 cyl_x('WheelHub_'+side,sign*.64-.085,sign*.64+.085,.50,WHEEL_Z,.075,3,'solid metal wheel hub')
 link('WheelHub_'+side,wheel,(sign*.64,.50,WHEEL_Z),(1,0,0),.02)
rod('RearAxle',(-.76,.50,WHEEL_Z),(.76,.50,WHEEL_Z),.028,3,'single fixed solid wheel axle',16)
for sign,side in [(-1,'Left'),(1,'Right')]:
 link('RearAxle','WheelHub_'+side,(sign*.64,.50,WHEEL_Z),(1,0,0),.018)
 link('RearAxle','AxleBracket_'+side,(sign*.48,.50,WHEEL_Z+.012),(1,0,0),.004)
for y,label in [(-.55,'Front'),(.50,'Rear')]:
 name='BaseCrossbar_'+label;rod(name,(-.50,y,.28),(.50,y,.28),.040,1,'chassis transverse tie')
 for end,side in [(0,'Left'),(1,'Right')]:end_link(name,'BaseRail_'+side,end)
# True side bearing bores with horizontal trunnions resting on lower facets.
BORE_R=.047;PIN_R=.045;BEARING_Z=1.10;CONTACT_Z=BEARING_Z-BORE_R*math.cos(math.pi/16);PIN_Z=CONTACT_Z+PIN_R*math.cos(math.pi/16)
REAR=local(0,0,-.14)
rod('Cradle_RearCrossbar',add(REAR,(-.51,0,0)),add(REAR,(.51,0,0)),.045,1,'rear U-cradle cross-member')
for sign,side in [(-1,'Left'),(1,'Right')]:
 x=sign*.59
 rod('BearingPost_'+side,(sign*.48,.03,.28),(x,.03,1.030),.046,1,'splayed vertical bearing support')
 end_link('BearingPost_'+side,'BaseRail_'+side,0)
 ring_x('Bearing_'+side,x-.07,x+.07,.03,BEARING_Z,.105,BORE_R,1,'thick real polygonal bored tilt bearing')
 link('Bearing_'+side,'BearingPost_'+side,(x-.001*sign,.03,1.016),(0,0,1),.005)
 rod('FrameBrace_'+side,(sign*.48,.48,.28),(sign*.575,.03,.92),.029,1,'two-ended diagonal chassis brace')
 end_link('FrameBrace_'+side,'BaseRail_'+side,0);end_link('FrameBrace_'+side,'BearingPost_'+side,1)
 x0,x1=sorted([sign*.465,sign*.715]);pin='Trunnion_'+side
 cyl_x(pin,x0,x1,.03,PIN_Z,PIN_R,3,'fixed horizontal tilt pin seated on lower bore facet')
 CONTACTS.append({'a':pin,'b':'Bearing_'+side,'plane_z_m':round(CONTACT_Z,6),'x_interval_m':[x-.07,x+.07],'y_interval_m':[.03-PIN_R*math.sin(math.pi/16),.03+PIN_R*math.sin(math.pi/16)],'expected_contact_area_m2':.14*2*PIN_R*math.sin(math.pi/16),'mode':'finite coplanar opposed actual triangles'})
 name='Cradle_Arm_'+side;rod(name,add(REAR,(sign*.49,0,0)),(sign*.49,.03,PIN_Z),.045,1,'rear-reaching arm of tilting cradle')
 end_link(name,'Cradle_RearCrossbar',0);end_link(name,pin,1)
rod('Drum_RearSpindle',local(0,0,-.19),local(0,0,.025),.075,3,'fixed rear drum spindle into bottom and cradle',16)
link('Drum_RearSpindle','Cradle_RearCrossbar',REAR,(1,0,0),.012)
link('Drum_RearSpindle','Drum_ThickPearShell',local(0,0,.018),(1,0,0),.012)
# Offset fixed motor shroud overlaps its actual rear-cradle mounting region.
box('Motor_Shroud',local(.25,0,-.20),(.29,.27,.20),2,'closed static motor enclosure, no internal drive claim',(U,V,A))
link('Motor_Shroud','Cradle_RearCrossbar',local(.25,0,-.14),(1,0,0),.015)
# Side control handwheel has a real empty annulus and three supported spokes.
cyl_x('Handwheel_Hub',.69,.805,.03,PIN_Z,.058,3,'solid fixed control hub',16)
link('Handwheel_Hub','Trunnion_Right',(.701,.03,PIN_Z),(1,0,0),.004)
ring_x('Handwheel_Rim',.755,.795,.03,PIN_Z,.235,.207,0,'true open circular tilt control rim',24)
for i in range(3):
 a=math.pi/2+i*math.tau/3;p=(.775,.03,PIN_Z);q=(.775,.03+.221*math.cos(a),PIN_Z+.221*math.sin(a));name=f'Handwheel_Spoke_{i+1:02d}'
 rod(name,p,q,.018,3,'closed handwheel spoke',10);end_link(name,'Handwheel_Hub',0)
 end_link(name,'Handwheel_Rim',1)
# Planned whole-assembly rays through the mouth to the actual blind bottom.
CAVITY_RAYS=[]
for radius in [0,.065,.105]:
 for angle in ([0] if radius==0 else [math.tau*i/6 for i in range(6)]):
  u,v=radius*math.cos(angle),radius*math.sin(angle);CAVITY_RAYS.append({'origin_m':local(u,v,1.0),'direction':mul(A,-1),'maximum_m':1.25,'expected_hit':'Drum_ThickPearShell','expected_local_t_m':.055})
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
for name,color,rough,metal in [('OchreEnamel_Drum',(.67,.36,.095,1),.76,.12),('DeepTeal_Frame',(.075,.23,.22,1),.79,.15),('Charcoal_RubberAndShroud',(.065,.082,.078,1),.92,.04),('PaleSteel_Mechanics',(.48,.55,.51,1),.65,.55)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('TiltedOpenDrumMixer',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.materials.append(mats[g['material']]);o['component_role']=g['role'];parts.append(o);byname[name]=o
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
# Finite bearing seating is established by actual flat source triangles, no AABB.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
contacts=[]
for c in CONTACTS:
 row=dict(c);row['pin_lower_actual_triangles']=horizontal_triangles(c['a'],c['plane_z_m'],-1);row['bore_lower_actual_triangles']=horizontal_triangles(c['b'],c['plane_z_m'],1)
 assert len(row['pin_lower_actual_triangles'])==2 and len(row['bore_lower_actual_triangles'])==2,row
 assert c['expected_contact_area_m2']>.002;contacts.append(row)
adj={o.name:set() for o in parts}
for j in joints+contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET+WHEELS);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET+WHEELS:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>(.03 if name in FEET else .01),(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
cavity=[]
for r in CAVITY_RAYS:
 hits=[]
 for name,tree in trees.items():
  q,_,_,distance=tree.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['maximum_m'])
  if q is not None:hits.append((distance,name,q))
 distance,name,q=min(hits);t=dot(sub(q,P),A)
 assert name==r['expected_hit'] and abs(t-r['expected_local_t_m'])<3e-6,('Mouth cavity obstruction',name,t)
 cavity.append(dict(r,actual_hit=name,actual_distance_m=distance,actual_local_t_m=t))
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
 'finite_bearing_seats':contacts,'mouth_to_bottom_rays':cavity,'drum_axis_world':A,'drum_base_world':P,'drum_outer_profile_t_r_m':OUTER,'drum_inner_profile_t_r_m':INNER,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((.025,.02,.84));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.04;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.6,-7.5,4.5),'gray-back3q':(-4.6,7.5,4.5)} if gray else {
 'thumbnail':(4.6,-7.5,4.5),'qa-front':(0,-7,.84),'qa-side':(7,.02,.84),'qa-top':(0,.02,8),
 'qa-back':(0,7,.84),'qa-wireframe':(4.6,-7.5,4.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.40 if name in ['gray-front3q','gray-back3q','thumbnail','qa-wireframe'] else 2.04
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0007;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.84)),('silhouette-128-side',(7,.02,.84))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
