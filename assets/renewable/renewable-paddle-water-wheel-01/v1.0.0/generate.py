"""Original static twin-rim paddle water wheel. Metres, Z up, axle Y.
One prop including grounded bearing stands, not a mill or electrical system.
Self-contained source; every render uses a fresh import of the actual GLB.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='renewable-paddle-water-wheel-01';VERSION='1.0.0';TITLE='Twin-Rim Paddle Water Wheel'
DESCRIPTION=('Original static water wheel with two thick open timber rims, eight radial spokes per side, a broad solid hub and a Y-axis shaft. '
 'Sixteen broad radial paddle boards span the wheel width and seat into both rims, giving visible water-receiving faces. '
 'Two outboard A-frame stands support closed annular bearing sleeves; each has a real central bore with a small fixed seated shaft overlap. '
 'Two broad flat feet and low cross-ties form one connected grounded assembly. Real spoke apertures, wheel-to-frame side clearance and raised paddle bottom. '
 'Four solid PBR materials, separately named closed editable meshes, source Z up, metres and ground-centre origin. One reusable prop including necessary supports. '
 'Distinct water-receiving geometry, not a recolored spinning wheel; no mill building, water channel, belt, generator, external textures or third-party marks. '
 'One checked static pose only: no rotation, water flow, hydrodynamics, energy generation, transmission, bearing function, loading, engineering or safety certification.')
G={};LINKS=[];CONTACTS=[];SPINES={};FEET=[];VOID_RAYS=[];PADDLES=[];BEARINGS=[]
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


WC=(0,0,1.20)
def radial(theta,r,y=0):return (r*math.cos(theta),y,WC[2]+r*math.sin(theta))
def ring_y(name,y0,y1,x,z,ro,ri,material,role,n=64):
 phase=math.pi/n;vs=[(x+r*math.cos(phase+math.tau*i/n),y,z+r*math.sin(phase+math.tau*i/n)) for r in [ro,ri] for y in [y0,y1] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def beam(name,a,b,width,depth,mat,role):
 axis=unit(sub(b,a));y=(0,1,0);tangent=unit(cross(axis,y));return box(name,mul(add(a,b),.5),(length(sub(b,a)),depth,width),mat,role,(axis,y,tangent))
# Low open support chassis belongs to the water wheel, not a scene or pedestal.
for y,label in [(-.56,'Front'),(.56,'Rear')]:
 name='GroundFoot_'+label;box(name,(0,y,.06),(1.48,.24,.12),1,'broad flat ground foot for outboard bearing stand');FEET.append(name)
 for sign,side in [(-1,'Left'),(1,'Right')]:
  a=(sign*.59,y,.09);b=(sign*.105,y,1.115);name='FrameLeg_'+label+'_'+side
  beam(name,a,b,.12,.15,1,'splayed A-frame leg seated in foot and bearing cross-cap')
  link(name,'GroundFoot_'+label,(sign*.582,y,.108),(0,1,0),.025)
 cap='BearingMount_'+label;box(cap,(0,y,1.075),(.40,.185,.16),2,'steel pillow-block mounting bridge joining both A-frame legs')
 for sign,side in [(-1,'Left'),(1,'Right')]:link(cap,'FrameLeg_'+label+'_'+side,(sign*.115,y,1.09),(0,1,0),.030)
 bearing='BearingSleeve_'+label;ring_y(bearing,y-.069,y+.069,0,1.20,.13,.052,2,'closed thick bearing housing with actual Y-axis bore; fixed 3mm seating overlap',32)
 link(bearing,cap,(0,y,1.10),(0,1,0),.030)
 BEARINGS.append({'name':bearing,'centre_y_m':y,'inner_radius_m':.052,'outer_radius_m':.13,'shaft_radius_m':.055,'fixed_radial_interference_m':.003})
for x,label in [(-.53,'Left'),(.53,'Right')]:
 name='BaseTie_'+label;box(name,(x,0,.075),(.12,1.20,.07),2,'low cross-tie connects the two outboard grounded stands')
 for y,end in [(-.56,'Front'),(.56,'Rear')]:link(name,'GroundFoot_'+end,(x,y,.075),(1,0,0),.025)
rod('WheelAxle',(0,-.735,1.20),(0,.735,1.20),.055,2,'solid supported Y-axis shaft, fixed pose',32)
for b in BEARINGS:link('WheelAxle',b['name'],(.0535,b['centre_y_m'],1.20),(0,1,0),.025)
rod('WheelHub',(0,-.365,1.20),(0,.365,1.20),.145,0,'broad timber hub joins twin spoke planes to shaft',32)
link('WheelHub','WheelAxle',(0,0,1.20),(0,1,0),.10)
for y,label in [(-.705,'Front'),(.705,'Rear')]:
 name='AxleEndCap_'+label;rod(name,(0,y-.022,1.20),(0,y+.022,1.20),.078,3,'solid retaining end cap visibly seated on axle',16)
 link(name,'WheelAxle',(0,y,1.20),(1,0,0),.020)
for y,label in [(-.31,'Front'),(.31,'Rear')]:
 rim='WaterRim_'+label;ring_y(rim,y-.04,y+.04,0,1.20,.92,.80,0,'continuous thick open rim carrying water paddle roots',64)
 for i in range(8):
  theta=math.tau*i/8;name=f'Spoke_{label}_{i+1:02d}';a=radial(theta,.105,y);b=radial(theta,.86,y)
  beam(name,a,b,.074,.065,0,'solid radial spoke connecting broad hub to open rim')
  link(name,'WheelHub',radial(theta,.122,y),(0,1,0),.012)
  link(name,rim,radial(theta,.837,y),(0,1,0),.012)
 band='HubBand_'+label;ring_y(band,y-.020,y+.020,0,1.20,.157,.135,2,'steel hoop embracing timber hub',32)
 link(band,'WheelHub',(.141,y,1.20),(0,1,0),.010)
# Broad radial paddle boards have actual thickness and two rim-root seats.
for i in range(16):
 theta=math.tau*i/16;axis=(math.cos(theta),0,math.sin(theta));tan=(-math.sin(theta),0,math.cos(theta))
 name=f'WaterPaddle_{i+1:02d}';box(name,radial(theta,.9525),(.175,.65,.050),0 if i%4 else 1,'broad radial water-receiving board with thick edge; not a decorative wheel spoke',(axis,(0,1,0),tan))
 for y,label in [(-.31,'Front'),(.31,'Rear')]:link(name,'WaterRim_'+label,radial(theta,.890,y),(0,1,0),.006)
 PADDLES.append({'name':name,'angle_rad':theta,'radial_span_m':[.865,1.040],'axial_width_m':.650,'tangential_thickness_m':.050})
 # Rivets are short solids embedded in paddle/root area, one at each axial end.
 for sign,label in [(-1,'Front'),(1,'Rear')]:
  y=sign*.326;name2=f'PaddleRivet_{i+1:02d}_'+label;c=radial(theta,.890,y)
  rod(name2,(c[0],y-.012,c[2]),(c[0],y+.012,c[2]),.012,3,'solid rivet at paddle-to-rim seat',10)
  link(name2,name,radial(theta,.890,sign*.319),(1,0,0),.002)
# Apertures are measured only through the full wheel throat, excluding outboard support stands.
for i in range(8):
 theta=math.tau*(i+.5)/8
 for r in [.43,.64]:
  p=radial(theta,r,-.38);VOID_RAYS.append({'window':i+1,'radius_m':r,'origin_m':p,'direction':[0,1,0],'length_m':.76})
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
for name,color,rough,metal in [('HoneyTimber_Wheel',(.44,.25,.105,1),.78,0),('DeepTimber_StandAndPaddles',(.19,.115,.060,1),.86,0),('PatinatedTeal_BearingHardware',(.055,.18,.17,1),.64,.50),('PaleBronze_Fasteners',(.49,.39,.22,1),.56,.60)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('TwinRimPaddleWaterWheel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.30,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
voids=[]
for r in VOID_RAYS:
 p=Vector(r['origin_m']);d=Vector(r['direction']);blockers=[n for n,t in trees.items() if t.ray_cast(p,d,r['length_m'])[0] is not None]
 assert not blockers,('Blocked spoke aperture',r,blockers)
 assert not any(inside(t,p) for t in trees.values())
 voids.append(dict(r,blockers=blockers))
# Clear wheel/stand strips at both sides; axle intentionally occupies their central region.
lateral=[]
for sign,label in [(-1,'Front'),(1,'Rear')]:
 for x,z in [(.50,1.20),(-.50,1.20),(.20,1.55)]:
  p=Vector((x,sign*.36,z));d=Vector((0,sign,0));L=.10
  blockers=[n for n,t in trees.items() if t.ray_cast(p,d,L)[0] is not None or inside(t,p)]
  assert not blockers,('Wheel stand side clearance',label,x,z,blockers)
  lateral.append({'side':label,'origin_m':list(p),'direction':list(d),'length_m':L,'blockers':blockers})
paddle_bottom=min(v.co.z for o in parts if o.name.startswith('WaterPaddle_') for v in o.data.vertices);assert paddle_bottom>.159
bearing_bores=[]
for b in BEARINGS:
 p=Vector((0,b['centre_y_m']-.070,1.20));tree=trees[b['name']];assert tree.ray_cast(p,Vector((0,1,0)),.14)[0] is None
 bearing_bores.append(dict(b,actual_sleeve_only_centre_bore_ray_clear=True,limitation='shaft occupies bore in assembly; fixed seated interference, no bearing or rotation performance'))
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
 'sixteen_water_paddles':PADDLES,'spoke_window_throat_rays':voids,'wheel_frame_side_clear_rays':lateral,'actual_paddle_bottom_z_m':paddle_bottom,'bearing_sleeve_bore_checks':bearing_bores,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/renewable/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'renewable','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,1.16));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.72;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.6,-7.5,4.3),'gray-back3q':(-4.6,7.5,4.3)} if gray else {
 'thumbnail':(4.6,-7.5,4.3),'qa-front':(0,-7,1.16),'qa-side':(7,0,1.16),'qa-top':(0,0,8),
 'qa-back':(0,7,1.16),'qa-wireframe':(4.6,-7.5,4.3)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.95 if name in ['gray-front3q','gray-back3q','thumbnail','qa-wireframe'] else 2.72
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.001;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,1.16)),('silhouette-128-side',(7,0,1.16))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
