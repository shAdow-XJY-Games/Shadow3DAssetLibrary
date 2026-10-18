"""Original supported firefighting hose reel. Metres, Z up, axle Y.
One static prop with a continuous 6-turn wound hose and supported parked nozzle.
Self-contained source; every render uses a fresh import of the actual GLB.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='firefighting-supported-hose-reel-01';VERSION='1.0.0';TITLE='Supported Fire Hose Reel'
DESCRIPTION=('Original static firefighting hose reel with twin thick six-spoke open side plates, a broad winding core, a fixed shaft, two visible outboard bearing stands and connected flat ground feet. '
 'One continuous closed hose mesh follows six separated gradually expanding turns, then a smooth outlet route into a parked downward nozzle. '
 'A grounded frame arm and a bored retaining collar support the nozzle; its annular tip has a genuine blind opening, and a short rear inlet coupling has a real recessed bore. '
 'Five solid PBR materials, separate named editable parts, source Z up, metres and ground-centre origin. One reusable prop, no scene, textures or external dependencies. '
 'Distinct from the existing two-extinguisher cabinet, unspooled fishing reel and flat harbor rope. Only one checked static pose: no winding or deployment animation, fluid, pressure, plumbing compatibility, fire suppression performance, real operation, installation or fire-safety certification.')
G={};LINKS=[];CONTACTS=[];SPINES={};FEET=[];VOID_RAYS=[];BEARINGS=[];HOSE=[]
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



WC=(0,0,.75)
def radial(theta,r,y=0):return (r*math.cos(theta),y,WC[2]+r*math.sin(theta))
def ring_y(name,y0,y1,x,z,ro,ri,material,role,n=48):
 phase=math.pi/n;vs=[(x+r*math.cos(phase+math.tau*i/n),y,z+r*math.sin(phase+math.tau*i/n)) for r in [ro,ri] for y in [y0,y1] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def ring_z(name,z0,z1,x,y,ro0,ro1,ri0,ri1,material,role,n=24):
 vs=[(x+r*math.cos(math.tau*i/n),y+r*math.sin(math.tau*i/n),z) for z,r in [(z0,ro0),(z1,ro1),(z0,ri0),(z1,ri1)] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def beam(name,a,b,width,depth,mat,role):
 axis=unit(sub(b,a));y=(0,1,0);tangent=unit(cross(axis,y));return box(name,mul(add(a,b),.5),(length(sub(b,a)),depth,width),mat,role,(axis,y,tangent))
def swept_hose(name,points,radius,n=10):
 vs=[];fs=[]
 for i,p in enumerate(points):
  tangent=unit(sub(points[min(i+1,len(points)-1)],points[max(0,i-1)]));u=unit(cross(tangent,(0,1,0)));v=unit(cross(tangent,u))
  for j in range(n):vs.append(add(p,mul(add(mul(u,math.cos(j*math.tau/n)),mul(v,math.sin(j*math.tau/n))),radius)))
 for i in range(len(points)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]);return mesh(name,vs,fs,1,'single continuous capped 6-turn hose and curved outlet; no joined overlapping tube segments')
def bezier(a,b,c,d,n):
 return [add(add(mul(a,(1-t)**3),mul(b,3*(1-t)**2*t)),add(mul(c,3*(1-t)*t*t),mul(d,t**3))) for t in [i/n for i in range(1,n+1)]]
# Necessary ground chassis and two small outboard bearing stands.
for y,label in [(-.22,'Front'),(.22,'Rear')]:
 name='GroundFoot_'+label;box(name,(0,y,.045),(1.08,.15,.09),2,'flat ground rail for reel stand');FEET.append(name)
 for sign,side in [(-1,'Left'),(1,'Right')]:
  a=(sign*.265,y,.07);b=(sign*.055,y,.70);name='StandLeg_'+label+'_'+side
  beam(name,a,b,.075,.09,2,'splayed frame leg connecting ground foot to bearing bridge')
  link(name,'GroundFoot_'+label,(sign*.262,y,.079),(0,1,0),.018)
 cap='BearingBridge_'+label;box(cap,(0,y,.687),(.23,.112,.094),2,'finite bridge joining both legs and bearing housing')
 for sign,side in [(-1,'Left'),(1,'Right')]:link(cap,'StandLeg_'+label+'_'+side,(sign*.062,y,.681),(0,1,0),.020)
 bearing='BearingSleeve_'+label;ring_y(bearing,y-.046,y+.046,0,.75,.073,.027,4,'closed bored bearing sleeve, fixed shaft seating overlap',24)
 link(bearing,cap,(0,y,.705),(0,1,0),.020)
 BEARINGS.append({'name':bearing,'centre_y_m':y,'inner_radius_m':.027,'outer_radius_m':.073,'shaft_radius_m':.030,'fixed_radial_interference_m':.003})
for x,label in [(-.22,'Left'),(.22,'Right')]:
 name='BaseTie_'+label;box(name,(x,0,.059),(.065,.49,.045),2,'low tie connecting front and rear grounded rails')
 for y,end in [(-.22,'Front'),(.22,'Rear')]:link(name,'GroundFoot_'+end,(x,y,.059),(1,0,0),.018)
rod('ReelAxle',(0,-.285,.75),(0,.285,.75),.030,4,'continuous Y-axis shaft supported by two bored bearing stands',24)
for b in BEARINGS:link('ReelAxle',b['name'],(.0285,b['centre_y_m'],.75),(0,1,0),.015)
rod('WindingCore',(0,-.108,.75),(0,.108,.75),.109,0,'broad central winding drum tied to both side plates',32)
link('WindingCore','ReelAxle',(0,0,.75),(0,1,0),.050)
rod('FrontAxleCap',(0,-.299,.75),(0,-.273,.75),.042,3,'visible front retaining cap overlapping fixed shaft',16)
link('FrontAxleCap','ReelAxle',(0,-.279,.75),(1,0,0),.010)
ring_y('RearInletCoupling',.273,.386,0,.75,.044,.016,3,'short open rear inlet coupling, recessed bore closed by fixed axle; visual only',24)
link('RearInletCoupling','ReelAxle',(.023,.279,.75),(0,0,1),.003)
# True thick six-window side plates; openings let the actual separated hose winding read.
for y,label in [(-.090,'Front'),(.090,'Rear')]:
 rim='ReelFlange_'+label;ring_y(rim,y-.014,y+.014,0,.75,.390,.338,0,'thick continuous outer ring of open hose reel side plate',48)
 for i in range(6):
  theta=math.tau*i/6;name=f'FlangeSpoke_{label}_{i+1:02d}'
  beam(name,radial(theta,.080,y),radial(theta,.363,y),.041,.023,0,'thick radial plate spoke joining winding core to side ring')
  link(name,'WindingCore',radial(theta,.095,y),(0,1,0),.004)
  link(name,rim,radial(theta,.350,y),(0,1,0),.004)
 # Separate central metal washer seats into the drum face, with no coplanar overlay.
 name='HubWasher_'+label;ring_y(name,y-.026,y+.026,0,.75,.060,.026,4,'thick bored metal hub washer seated on central drum',24)
 link(name,'WindingCore',(.042,y,.75),(0,1,0),.010)
# One continuous 6-turn gently conical spiral. Winding pitch exceeds hose diameter.
TURN_STEPS=48;TURNS=6;HOSE_RADIUS=.0145
for i in range(TURN_STEPS*TURNS+1):
 t=i/(TURN_STEPS*TURNS);theta=math.tau*TURNS*(1-t);r=.122+.228*t;y=-.035+.070*t
 HOSE.append(radial(theta,r,y))
COIL_COUNT=len(HOSE)
# Smooth outlet passes below/outside the right flange before moving forwards to its holder.
a=HOSE[-1];b=add(a,(.0025,0,-.120));c=(.49,-.22,.66);d=(.49,-.22,.520)
HOSE.extend(bezier(a,b,c,d,32))
swept_hose('ContinuousWoundHose',HOSE,HOSE_RADIUS)
link('ContinuousWoundHose','WindingCore',(.1083,-.0349,.747),(0,0,1),.00025)
# Lower front nozzle carrier has a real retaining bore and two-sided grounded connection.
box('NozzleCarrierArm',(.306,-.22,.410),(.365,.078,.045),2,'horizontal nozzle carrier joined to front-right frame leg and retaining collar')
link('NozzleCarrierArm','StandLeg_Front_Right',(.153,-.22,.410),(0,1,0),.015)
ring_z('NozzleRetainer',.389,.431,.49,-.22,.042,.042,.0215,.0215,0,'annular parked-nozzle retaining collar with real bore',24)
link('NozzleRetainer','NozzleCarrierArm',(.460,-.22,.410),(0,0,1),.008)
rod('NozzleGrip',(.49,-.22,.320),(.49,-.22,.532),.024,2,'solid fixed nozzle grip supported inside bored retaining collar',20)
link('NozzleGrip','NozzleRetainer',(.5127,-.22,.410),(0,0,1),.010)
rod('HoseEndCoupling',(.49,-.22,.505),(.49,-.22,.551),.0255,3,'brass end coupling surrounds hose terminal and nozzle grip',20)
link('HoseEndCoupling','NozzleGrip',(.49,-.22,.515),(1,0,0),.008)
link('HoseEndCoupling','ContinuousWoundHose',(.49,-.22,.527),(1,0,0),.004)
ring_z('NozzleOpenTip',.250,.334,.49,-.22,.0165,.026,.009,.012,3,'thick tapering open tip; 70mm real blind recess ending at grip face',24)
link('NozzleOpenTip','NozzleGrip',(.508,-.22,.326),(0,1,0),.003)
# Void rays through actual negative-space throats; the nozzle and inlet bores terminate naturally.
VOID_RAYS.extend([
 {'label':'nozzle blind opening','only':'NozzleOpenTip','origin_m':(.49,-.22,.246),'direction':(0,0,1),'length_m':.072},
 {'label':'rear inlet blind bore','only':'RearInletCoupling','origin_m':(0,.390,.75),'direction':(0,-1,0),'length_m':.102}])
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
for name,color,rough,metal in [('SignalRed_Plates',(.55,.036,.024,1),.58,.25),('OchreRubber_Hose',(.49,.38,.14,1),.86,0),('Charcoal_FrameAndGrip',(.035,.055,.062,1),.72,.28),('Brass_Couplings',(.56,.35,.105,1),.48,.64),('SatinSteel_Axle',(.40,.48,.51,1),.44,.70)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('SupportedFireHoseReel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.15,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
voids=[]
for r in VOID_RAYS:
 p=Vector(r['origin_m']);d=Vector(r['direction']);blockers=[n for n,t in trees.items() if t.ray_cast(p,d,r['length_m'])[0] is not None or inside(t,p)]
 assert not blockers,('Blocked functional recess',r,blockers)
 voids.append(dict(r,blockers=blockers))
coil=byname['ContinuousWoundHose'];coil_v=[v.co for v in coil.data.vertices[:COIL_COUNT*10]]
flange_clearance=min(min(v.y+.076,.076-v.y) for v in coil_v);assert flange_clearance>.025
outlet_bottom=min(v.co.z for v in list(coil.data.vertices)[COIL_COUNT*10:]);assert outlet_bottom>.50
bearing_bores=[]
for b in BEARINGS:
 p=Vector((0,b['centre_y_m']-.047,.75));tree=trees[b['name']];assert tree.ray_cast(p,Vector((0,1,0)),.094)[0] is None
 bearing_bores.append(dict(b,actual_sleeve_only_centre_bore_ray_clear=True,limitation='fixed seated overlap; no bearing operation claim'))
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
 'continuous_hose':{'points_m':HOSE,'coil_point_count':COIL_COUNT,'turns':TURNS,'section_radius_m':HOSE_RADIUS,'section_sides':10,'actual_coil_to_flange_axial_clearance_m':flange_clearance,'one_connected_mesh':True},'functional_recess_rays':voids,'bearing_sleeve_bore_checks':bearing_bores,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/firefighting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'firefighting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((.03,.02,.59));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.40;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.0,-7.5,3.5),'gray-back3q':(-4.0,7.5,3.5)} if gray else {
 'thumbnail':(4.0,-7.5,3.5),'qa-front':(.03,-7,.59),'qa-side':(7,.02,.59),'qa-top':(0,0,8),
 'qa-back':(.03,7,.59),'qa-wireframe':(4.0,-7.5,3.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.58 if name in ['gray-front3q','gray-back3q','thumbnail','qa-wireframe'] else 1.40
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00055;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(.03,-7,.59)),('silhouette-128-side',(7,.02,.59))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
