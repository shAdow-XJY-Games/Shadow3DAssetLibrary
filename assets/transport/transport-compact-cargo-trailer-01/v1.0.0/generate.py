"""Original S01/S06 static compact cargo trailer. Metres; source Z up; tow -Y.
One empty fixed parked trailer, not a recoloured cart or adapted van. Root is ground
under the cargo tub centre (0,0,0), not the asymmetric footprint centre. Wheel axes X;
centres (+/-0.68,0.25,0.28). Tow-eye centre (0,-1.90,0.50), bore axis Z, 90 mm
minimum clear diameter. Existing delivery van has NO mating hitch: no host fit claimed.
No external inputs. --no-render / --geometry-only / --gray-only / --preview-only /
--extra-views. Every image uses fresh exact GLB geometry and full solid PBR binding.
No towing, motion, suspension, loading, stability, engineering or safety certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='transport-compact-cargo-trailer-01';VERSION='1.0.0';TITLE='Compact Parked Cargo Trailer'
DESCRIPTION=('Original S01/S06 static compact cargo trailer with one continuous open tub, a low supporting chassis, '
 'converging A-shaped drawbar, real vertical through-bored towing eye, two independently editable flat-tread tyre/hub '
 'assemblies, two raised mudguards with fixed brackets, and a grounded fixed parking leg. Four solid PBR materials, '
 'metre scale, source Z up, tow direction -Y. Ground origin is under the cargo tub centre; eye centre (0,-1.90,0.50) m '
 'with a 90 mm minimum clear bore along Z. Existing delivery van has no mating hitch; no host compatibility is claimed. '
 'One original reusable static prop, with no cargo or towing vehicle. No towing, animation, turning path, loading, '
 'braking, roadworthiness, stability, engineering, physics or safety certification.')
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
for name,color,rough,metal in [('Seafoam_PaintedBody',(.235,.47,.405,1),.69,.05),
 ('WarmGrey_FixedMetal',(.38,.405,.39,1),.58,.45),('Charcoal_FlatTyre',(.035,.043,.042,1),.88,0),
 ('MutedRed_RearMarkers',(.48,.055,.035,1),.56,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('CompactCargoTrailer',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['forward_tow_axis']='-Y';root['static_parked_visual_only']=True
root['ground_origin']='under cargo tub centre, not full footprint centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Restrained manufactured chamfer','BEVEL');b.width=bevel;b.segments=1
  bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def ring_z(name,center,r_outer,r_inner,depth,material,role,n=16):
 x,y,z=center;vs=[]
 for zz,rr in [(z-depth/2,r_outer),(z+depth/2,r_outer),(z+depth/2,r_inner),(z-depth/2,r_inner)]:
  vs.extend((x+rr*math.cos(i*math.tau/n),y+rr*math.sin(i*math.tau/n),zz) for i in range(n))
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def cylinder(name,center,radius,depth,material,role,axis='X',n=16):
 x,y,z=center;vs=[]
 for d in [-depth/2,depth/2]:
  for i in range(n):
   a=i*math.tau/n+math.pi/n;u=radius*math.sin(a);v=radius*math.cos(a)
   vs.append((x+d,y+u,z+v) if axis=='X' else (x+u,y+v,z+d))
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def beam_xy(name,a,b,width,height,material,role):
 a,b=Vector(a),Vector(b);t=(b-a).normalized();n=Vector((-t.y,t.x,0));vs=[]
 for p in [a,b]:
  for z in [-height/2,height/2]:
   for side in [-1,1]:vs.append(p+n*side*width/2+Vector((0,0,z)))
 fs=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
 return mesh(name,vs,fs,material,role,(a+b)/2)
def clipped(x,y,c):return [(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c),(-x,-y+c)]
# One closed shell around a genuinely empty open-top cavity, including integral floor.
outer=clipped(.57,.93,.06);inner=clipped(.52,.88,.04);vs=[]
for loop,z in [(outer,.56),(outer,.95),(inner,.95),(inner,.62)]:vs.extend((x,y,z) for x,y in loop)
fs=[(k*8+i,k*8+(i+1)%8,(k+1)*8+(i+1)%8,(k+1)*8+i) for k in range(3) for i in range(8)]
fs += [tuple(range(7,-1,-1)),tuple(range(24,32))]
mesh('CargoTub_ContinuousOpenShell',vs,fs,0,'one thick-sided cargo tub with integral floor and true open top',origin=(0,0,.755))
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Chassis_'+label,(side*.40,0,.525),(.08,1.78,.12),1,'long supporting underframe rail')
for y,label in [(-.72,'Front'),(0,'Middle'),(.72,'Rear')]:
 box('Crossmember_'+label,(0,y,.50),(1.02,.075,.10),1,'fixed crossmember attached to both chassis rails')
cylinder('Axle_FixedTransverse',(0,.25,.28),.034,1.56,1,'single fixed axle along X')
for side,label in [(-1,'Left'),(1,'Right')]:
 box('AxleHanger_'+label,(side*.40,.25,.39),(.07,.11,.25),1,'fixed hanger joining axle to chassis')
 # Annular tyres preserve an honest centre bore; the independently editable solid hub occupies it.
 center=(side*.68,.25,.28);n=16;vs=[]
 for xx,rr in [(center[0]-.075,.28/math.cos(math.pi/n)),(center[0]+.075,.28/math.cos(math.pi/n)),
               (center[0]+.075,.12),(center[0]-.075,.12)]:
  vs.extend((xx,.25+rr*math.sin(i*math.tau/n+math.pi/n),.28+rr*math.cos(i*math.tau/n+math.pi/n)) for i in range(n))
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 mesh('Tyre_'+label+'_FlatContact',vs,fs,2,'closed annular tyre with finite horizontal ground facet',origin=center)
 cylinder('Hub_'+label,center,.128,.18,1,'fixed low-poly hub occupying annular tyre bore')
 # Each mudguard is one closed open-bottom half-annular solid, not intersecting the tyre.
 x0,x1=sorted((side*.58,side*.82));n=13;vs=[]
 for x,r in [(x0,.355),(x1,.355),(x1,.395),(x0,.395)]:
  vs.extend((x,.25+r*math.cos(i*math.pi/(n-1)),.28+r*math.sin(i*math.pi/(n-1))) for i in range(n))
 fs=[(k*n+i,k*n+i+1,((k+1)%4)*n+i+1,((k+1)%4)*n+i) for k in range(4) for i in range(n-1)]
 fs += [(0,n,2*n,3*n),(n-1,4*n-1,3*n-1,2*n-1)]
 mesh('Mudguard_'+label,vs,fs,0,'closed raised half-arch with actual tyre clearance',origin=(side*.70,.25,.28))
 for y,where in [(-.05,'Front'),(.55,'Rear')]:
  box('MudguardBracket_'+label+'_'+where,(side*.50,y,.510),(.30,.07,.045),1,'fixed bracket joining mudguard and chassis',bevel=.002)
 beam_xy('Drawbar_A_'+label,(side*.40,-.68,.50),(0,-1.66,.50),.075,.09,1,'one converging fixed A-frame drawbar member')
box('Drawbar_Crossbrace',(0,-1.25,.495),(.46,.075,.074),1,'bridge between A-frame members and parking-leg mount')
box('TowEye_Shank',(0,-1.69,.50),(.10,.29,.10),1,'fixed tongue shank; stops behind clear eye aperture')
ring_z('TowEye_ThroughRing',(0,-1.90,.50),.095,.045/math.cos(math.pi/16),.028,1,'true 90mm minimum vertical through bore')
eye=bpy.data.objects.new('Interface_TowEye_Centre',None);scene.collection.objects.link(eye);eye.parent=root;eye.location=(0,-1.90,.50)
eye['bore_axis_source']='Z';eye['minimum_clear_bore_m']=.09;eye['host_fit']='none tested; existing van has no hitch'
box('ParkingLeg_FixedMount',(0,-1.25,.405),(.10,.10,.21),1,'fixed mount below A-frame crossbrace')
cylinder('ParkingLeg_FixedStem',(0,-1.25,.2175),.027,.385,1,'one fixed vertical parking stem',axis='Z',n=12)
box('ParkingFoot_GroundPlate',(0,-1.25,.0175),(.28,.20,.035),1,'finite ground plate for the fixed parked pose',bevel=.003)
for side,label in [(-1,'Left'),(1,'Right')]:
 box('RearMarker_'+label,(side*.37,.945,.72),(.16,.04,.09),3,'static red rear marker, no working lamp claim',bevel=.003)
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 votes=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  votes.append(bool(hits%2))
 return all(votes)
joints=[]
def joint(a,b,points):
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
for side,label in [(-1,'Left'),(1,'Right')]:
 joint('CargoTub_ContinuousOpenShell','Chassis_'+label,[(side*.4,y,.5725) for y in [-.50,0,.50]])
 for y,where in [(-.72,'Front'),(0,'Middle'),(.72,'Rear')]:
  joint('Chassis_'+label,'Crossmember_'+where,[(side*(.39+d),y,.510) for d in [0,.01,.02]])
 joint('Chassis_'+label,'AxleHanger_'+label,[(side*.4,.25+d,.490) for d in [-.02,0,.02]])
 joint('AxleHanger_'+label,'Axle_FixedTransverse',[(side*(.39+d),.25,.28) for d in [0,.01,.02]])
 joint('Axle_FixedTransverse','Hub_'+label,[(side*(.66+d),.25,.28) for d in [0,.02,.04]])
 joint('Hub_'+label,'Tyre_'+label+'_FlatContact',[(side*(.67+d),.372,.28) for d in [0,.01,.02]])
 for y,where in [(-.05,'Front'),(.55,'Rear')]:
  name='MudguardBracket_'+label+'_'+where
  joint(name,'Chassis_'+label,[(side*(.39+d),y,.510) for d in [0,.01,.02]])
  joint(name,'Mudguard_'+label,[(side*(.60+d),y,.510) for d in [0,.01,.02]])
 joint('Drawbar_A_'+label,'Chassis_'+label,[(side*.37,-.75+d,.50) for d in [-.01,0,.01]])
 joint('Drawbar_A_'+label,'TowEye_Shank',[(side*.02,-1.62+d,.50) for d in [-.01,0,.01]])
 joint('Drawbar_A_'+label,'Drawbar_Crossbrace',[(side*.167,-1.25+d,.50) for d in [-.01,0,.01]])
 joint('RearMarker_'+label,'CargoTub_ContinuousOpenShell',[(side*(.35+d),.927,.72) for d in [0,.02,.04]])
joint('TowEye_Shank','TowEye_ThroughRing',[(x,-1.825,.50) for x in [-.018,0,.018]])
joint('Drawbar_Crossbrace','ParkingLeg_FixedMount',[(x,-1.25,.48) for x in [-.02,0,.02]])
joint('ParkingLeg_FixedMount','ParkingLeg_FixedStem',[(0,-1.25,z) for z in [.34,.36,.38]])
joint('ParkingLeg_FixedStem','ParkingFoot_GroundPlate',[(x,-1.25,.03) for x in [-.01,0,.01]])
# The bore is clear through the whole actual assembly, not merely through its ring object.
eye_rays=[]
for x,y in [(0,-1.90),(.025,-1.90),(-.025,-1.90),(0,-1.925),(0,-1.875)]:
 for name,tree in trees.items():assert tree.ray_cast(Vector((x,y,.35)),Vector((0,0,1)),.30)[0] is None,('Blocked eye bore',name,x,y)
 eye_rays.append([x,y])
cargo_rays=[]
for x,y in [(0,0),(.45,.76),(-.45,.76),(.45,-.76),(-.45,-.76)]:
 hits=[]
 for name,tree in trees.items():
  p,normal,_,distance=tree.ray_cast(Vector((x,y,1.1)),Vector((0,0,-1)),.60)
  if p is not None:hits.append((distance,name,p,normal))
 hit=min(hits,key=lambda h:h[0]);assert hit[1]=='CargoTub_ContinuousOpenShell' and abs(hit[2].z-.62)<1e-6,(x,y,hit)
 cargo_rays.append({'xy_m':[x,y],'first_surface_z_m':hit[2].z})
supports=[]
for name in ['Tyre_Left_FlatContact','Tyre_Right_FlatContact','ParkingFoot_GroundPlate']:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.005,(name,area)
 supports.append({'name':name,'area_m2':area,'triangles':patch})
for side,label in [(-1,'Left'),(1,'Right')]:
 # Actual complete tyre vertices are strictly within the known empty radius of the polygonal mudguard.
 o=byname['Tyre_'+label+'_FlatContact'];radius=max(math.hypot((o.matrix_world@v.co).y-.25,(o.matrix_world@v.co).z-.28) for v in o.data.vertices)
 inward=.355*math.cos(math.pi/24);assert inward-radius>.06,(label,inward-radius)
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes),'Solid-only PBR expected'
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
for o in parts+[root,eye]:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_animations=False,export_extras=True)
guard();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':len(mats),'mesh_objects':mesh_count,'bounds_m':bounds,'bounds_min_m':lo,'bounds_max_m':hi,
 'components':component_checks,'connection_interior_points':joints,'tow_eye_assembly_clear_z_rays_xy_m':eye_rays,'cargo_cavity_floor_rays':cargo_rays,
 'finite_ground_supports':supports,'tyre_to_mudguard_conservative_radial_clearance_m':inward-radius,
 'tow_eye_interface':{'centre_source_m':[0,-1.90,.50],'axis_source':'Z','minimum_bore_m':.09,'host_compatibility':'not tested; existing van has no hitch'},
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'transport','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.50,.44));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-6,3.5),'gray-back3q':(-4,5,3.5)} if gray else {
 'thumbnail':(4,-6,3.5),'qa-front':(0,-6,.44),'qa-side':(6,-.50,.44),'qa-top':(0,-.50,7),
 'qa-back':(0,6,.44),'qa-wireframe':(4,-6,3.5)}
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
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0017;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-6,.44)),('silhouette-128-side',(6,-.50,.44))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
