"""Original fixed 12/18-tooth study kit. One static prop; no moving or transmission claim.
True thick annular gears, open shaft clearances and fixed supports. Metres; Z up.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='timekeeping-fixed-spur-gear-study-kit-01';VERSION='1.0.0';TITLE='Fixed Spur Gear Study Kit'
DESCRIPTION=('One original static gear study kit counted as one prop: two continuously meshed thick annular wheels with twelve and eighteen genuine teeth, supported above a chamfered base by two fixed stepped shafts with lower seating collars and upper stop caps. Teeth and roots are part of each single closed gear shell, not attached blocks. Both real through-bores retain finite annular clearance around their shafts. The two wheels are fixed in one offset phase: teeth enter the opposite slot envelope while all opposing gear surfaces retain positive clearance. Every gear is finitely seated on its collar; both shafts are finitely fixed into the grounded base. Five editable closed meshes, four opaque constant PBR colours, no textures or animation. Metres, source Z up, front -Y and ground-centred origin. No clock casing, numbered instruction card, person, motor, extra gear variant or scene. '
'Static visual geometry only. No rotation, continuous meshing, gear ratio performance, involute or engineering accuracy, time measurement, educational effectiveness, mechanical efficiency, loading, manufacture tolerance, assembly-path or safety-certification claim. No compatibility with earlier clock internals. Dimensions describe this fixed visual geometry only.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};CONTACTS=[];GEARS={}
PALETTE=[('Base_DeepPetrol',(.045,.135,.145,1),.70,0),('Gear12_WarmBrass',(.66,.345,.085,1),.42,.55),('Gear18_SlateBlue',(.13,.29,.37,1),.48,.45),('ShaftCaps_DarkSteel',(.15,.18,.19,1),.36,.65)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def polygon_area(p):return abs(sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1])))/2

def emit(name,vs,fs,mat,role):
 g={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),8) for c in p) for p in vs],'faces':fs,'material':mat,'role':role};G[name]=g;return g

def loop_solid(name,loops,mat,role,caps=True):
 n=len(loops[0]);vs=sum(loops,[]);fs=[]
 for a in range(len(loops)-1):
  for i in range(n):j=(i+1)%n;fs.append((a*n+i,a*n+j,(a+1)*n+j,(a+1)*n+i))
 if caps:fs += [tuple(reversed(range(n))),tuple((len(loops)-1)*n+i for i in range(n))]
 return emit(name,vs,fs,mat,role)

def circle(cx,cy,r,z,angles):return [(cx+r*math.cos(a),cy+r*math.sin(a),z) for a in angles]
def annular_volume(cx,cy,inner,outer,z0,z1,angles,role):
 loops=[circle(cx,cy,outer,z0,angles),circle(cx,cy,outer,z1,angles),circle(cx,cy,inner,z1,angles),circle(cx,cy,inner,z0,angles)]
 n=len(angles);v=sum(loops,[]);f=[]
 for h in range(4):
  k=(h+1)%4
  for i in range(n):j=(i+1)%n;f.append((h*n+i,h*n+j,k*n+j,k*n+i))
 return {'vertices':v,'faces':f,'role':role}

# The single broad base has real chamfered edges and a finite flat bottom.
base='Base_ChamferedGrounded';footprint=[(-.34,-.23),(.34,-.23),(.36,-.21),(.36,.21),(.34,.23),(-.34,.23),(-.36,.21),(-.36,-.21)]
loops=[[(x*.99,y*.985,0) for x,y in footprint],[(x,y,.005) for x,y in footprint],[(x,y,.023) for x,y in footprint],[(x*.99,y*.985,.028) for x,y in footprint]]
loop_solid(base,loops,0,'one chamfered grounded base; actual flat finite bottom');FEET.append(base)

# Five vertices per tooth. The high plateau is one tooth; its continuous flanks
# descend into the shared root valley. There is no separate tooth object.
TOOTH_FRACTIONS=[-.5,-.32,-.16,.16,.32]
TOOTH_RADII=[0,0,1,1,0]
for label,count,cx,cy,pitch,phase,mat in [('12',12,-.1825,0,.120,0,1),('18',18,.1225,0,.180,-math.pi/18,2)]:
 name='Gear'+label+'_ContinuousTeethAndBore';shaft='Shaft'+label+'_FixedCollarAndStopCap';step=math.tau/count;root=pitch-.012;tip=pitch+.012
 angles=[phase+(k+f)*step for k in range(count) for f in TOOTH_FRACTIONS]
 radii=[root+(tip-root)*high for k in range(count) for high in TOOTH_RADII];n=len(angles)
 loops=[]
 for z,inset in [(.085,.0018),(.088,0),(.117,0),(.120,.0018)]:loops.append([(cx+(r-inset)*math.cos(a),cy+(r-inset)*math.sin(a),z) for a,r in zip(angles,radii)])
 for z,r in [(.120,.025),(.117,.024),(.088,.024),(.085,.025)]:loops.append(circle(cx,cy,r,z,angles))
 vs=sum(loops,[]);fs=[]
 for h in range(8):
  k=(h+1)%8
  for i in range(n):j=(i+1)%n;fs.append((h*n+i,h*n+j,k*n+j,k*n+i))
 emit(name,vs,fs,mat,'one closed continuous '+label+'-tooth thick annular gear with bevelled tooth edges and true through bore')
 GEARS[name]={'count':count,'centre':(cx,cy),'pitch_visual_m':pitch,'root_radius_m':root,'tip_radius_m':tip,'phase_rad':phase,'z_min_m':.085,'z_max_m':.120,'angles':angles,'n':n,'shaft':shaft,'outer_mid_ring_indices':list(range(n,2*n)),'bore_bottom_ring_indices':list(range(7*n,8*n)),'bore_inner_radius_m':.024,'bore_end_radius_m':.025}
 # A single closed lathed support includes foot, collar, shaft and upper cap.
 # Collar's top annulus at z=.085 seats the gear; cap underside is 20 mm above it.
 profile=[(.029,.014),(.032,.019),(.032,.071),(.039,.076),(.039,.082),(.037,.085),(.014,.085),(.014,.140),(.028,.140),(.028,.147),(.025,.150)]
 loop_solid(shaft,[circle(cx,cy,r,z,angles) for r,z in profile],3,'one fixed shaft, supporting collar and stop cap; not a rotational bearing')
 LINKS.append((base,shaft,[(cx,cy,.020),(cx+.010,cy,.022),(cx,cy+.010,.022)]))
 contact_area=polygon_area([(x-cx,y-cy) for x,y,z in circle(cx,cy,.037,.085,angles)])-polygon_area([(x-cx,y-cy) for x,y,z in circle(cx,cy,.025,.085,angles)])
 CONTACTS.append({'a':shaft,'b':name,'type':'finite opposed annular seated faces','z_m':.085,'normal_a':[0,0,1],'normal_b':[0,0,-1],'expected_contact_area_m2':contact_area,'gear_top_cap_clearance_m':.020,'shaft_to_gear_min_radial_clearance_m':.009})
 BORES.append({'mesh':name,'origin_m':(cx,cy,.080),'direction':(0,0,1),'length_m':.045,'role':'isolated real through bore, central axial ray'})
 # Finite isolated cylindrical hole test, along the entire gear thickness.
 # It is isolated because the required support shaft intentionally occupies its centre.
 test_angles=[math.tau*i/48 for i in range(48)]
 vv=circle(cx,cy,.0225,.084,test_angles)+circle(cx,cy,.0225,.121,test_angles);ff=[]
 for i in range(48):j=(i+1)%48;ff.append((i,j,48+j,48+i))
 ff += [tuple(reversed(range(48))),tuple(48+i for i in range(48))]
 ISOLATED_VOID_VOLUMES[name]={'vertices':vv,'faces':ff,'role':'complete closed finite isolated shaft-bore volume'}
 VOID_VOLUMES['Gear'+label+'_EntireAnnularShaftClearance']=annular_volume(cx,cy,.015,.0225,.0855,.1195,angles,'closed full-circumference annular volume, clear of every assembled part')
 # Witness under the wheel, well outside its supporting collar.
 GAPS.append({'origin_m':(cx,cy+.062,.029),'direction':(0,0,1),'length_m':.054,'role':'visible free wheel underside-to-base gap'})

# A finite witness box inside small gear tooth and inside the large wheel's
# tip-radius envelope demonstrates actual insertion into an empty opposing slot.
INTERMESH_WITNESS={'centre_m':(-.053,0,.102),'half_extent_m':(.001,.001,.005)}

def unique(points):return sorted(set(tuple(float(c) for c in p) for p in points))
def measure_gear_geometry(vertices,triangles=None):
 assert set(vertices)==set(G),'A study kit has exactly its five planned components and counts as one prop'
 rows=[]
 for name,g in G.items():
  actual=unique(vertices[name]);expected=unique(g['vertices']);assert len(actual)==len(expected),('Actual unique mesh vertex count changed',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(ix)==1 for ix in matches) and len({ix[0] for ix in matches})==len(expected),('Actual raw mesh has no unique source position match',name)
  rows.append({'mesh':name,'maximum_actual_raw_position_error_m':max(math.dist(p,expected[ix[0]]) for p,ix in zip(actual,matches)),'unique_bijective_surface_match':True})
 gear_rows=[]
 for name,p in GEARS.items():
  cx,cy=p['centre'];v=unique(vertices[name]);assert abs(max(x[2] for x in v)-min(x[2] for x in v)-.035)<1e-6
  ring=sorted([(math.atan2(y-cy,x-cx),math.hypot(x-cx,y-cy)) for x,y,z in v if abs(z-.088)<1e-6 and math.hypot(x-cx,y-cy)>.05])
  assert len(ring)==p['n'];peaks=[r>p['pitch_visual_m'] for a,r in ring];teeth=sum(peaks[i] and not peaks[i-1] for i in range(len(peaks)));assert teeth==p['count'],('Actual continuous outer contour tooth count changed',name,teeth)
  assert abs(min(r for a,r in ring)-p['root_radius_m'])<1e-6 and abs(max(r for a,r in ring)-p['tip_radius_m'])<1e-6
  hole=[math.hypot(x-cx,y-cy) for x,y,z in v if abs(z-.088)<1e-6 and math.hypot(x-cx,y-cy)<.05];assert len(hole)==p['n'] and abs(min(hole)-.024)<1e-6
  gear_rows.append({'mesh':name,'actual_counted_teeth':teeth,'actual_outline_vertices':len(ring),'actual_root_radius_m':min(r for a,r in ring),'actual_tip_radius_m':max(r for a,r in ring),'actual_inner_bore_vertices':len(hole),'actual_bore_radius_m':min(hole),'actual_thickness_m':.035,'closed_connected_annular_shell_required':True})
 allv=[p for v in vertices.values() for p in v];assert abs(min(p[2] for p in allv))<1e-6
 gear_names=list(GEARS);a,b=[GEARS[n] for n in gear_names];distance=math.dist(a['centre'],b['centre']);envelope_overlap=a['tip_radius_m']+b['tip_radius_m']-distance;assert envelope_overlap>.018
 return {'single_prop_count':1,'meshes':rows,'gears':gear_rows,'actual_tooth_counts':[r['actual_counted_teeth'] for r in gear_rows],'fixed_centre_distance_m':distance,'outer_envelope_overlap_m':envelope_overlap,'static_fixed_phase_only':True,'no_motion_or_gear_accuracy_claim':True}
FOCUS=(0,0,.065);ORTHO=.98
CAMERAS={'gray-front3q':(.95,-1.45,1.40),'gray-back3q':(-.95,1.45,1.40),'thumbnail':(.95,-1.45,1.40),'qa-front':(0,-1.7,.72),'qa-side':(1.7,0,.78),'qa-top':(0,0,2.0),'qa-back':(0,1.7,.72),'qa-wireframe':(.95,-1.45,1.40),'silhouette-128-front':(0,-1.7,.72),'silhouette-128-side':(1.7,0,.78)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneFixedGearStudyKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
isolated_volume_checks=[]
for name,probe in ISOLATED_VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False);model_tree=trees[name];obj=byname[name]
 crossing=model_tree.overlap(pt);model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)];probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
 assert not crossing and not model_inside and not probe_inside,('Actual isolated full through bore blocked',name,crossing,model_inside,probe_inside)
 isolated_volume_checks.append({'mesh':name,'complete_closed_volume_empty':True,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
gear_evidence=dict(measure_gear_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts},{o.name:[[tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices] for t in o.data.loop_triangles] for o in parts}),material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'gear_geometry':gear_evidence,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'actual_finite_void_volumes':void_volume_checks,'actual_isolated_bore_volumes':isolated_volume_checks,'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/timekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'timekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
