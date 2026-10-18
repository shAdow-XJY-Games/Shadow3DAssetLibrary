"""Original empty handheld charging cradle. Static visual prop only.
Metres, Z up; floor-centre origin; front -Y. No handheld is included.
Cavity and contact dimensions describe this geometry, not any device compatibility.
Self-contained; every render uses a fresh actual GLB import and full solid-PBR guard.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-handheld-charging-cradle-kit-01';VERSION='1.0.0';TITLE='Deep-Cavity Handheld Charging Cradle'
DESCRIPTION=('One original empty handheld charging-cradle visual prop with a true tapered deep cavity, closed thick walls and a solid bearing floor. '
 'Two inward guide ribs, a raised rear stop, a floor-mounted contact carrier with two small separate brass contact points, and four finite rubber feet are modeled as ten independently editable closed meshes. '
 'Overall 148 x 128 x 82 mm, metres, Z up, floor-centre origin, front -Y. The unblocked central cavity and actual bearing floor are measured from the complete exported geometry. '
 'Four solid PBR materials, no textures or external assets. No handheld is included; no previous radio or other device compatibility is tested or claimed. '
 'One static prop only; no charging, circuit, battery, voltage, radio communication, insertion animation, manufacture, electrical or product-safety guarantee.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_RAYS=[];WALL_RAYS=[]
PALETTE=[('Housing_BlueGraphite',(.065,.145,.19,1),.57,.18),('Cavity_Slate',(.19,.25,.27,1),.67,.06),('Rubber_Charcoal',(.035,.045,.048,1),.83,0),('Contact_Brass',(.65,.40,.105,1),.34,.78)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def octagon(x,y,c):return [(-x,-y+c),(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c)]
def solid_loops(name,loops,mat,role):
 k=len(loops[0]);assert all(len(l)==k for l in loops);vs=[p for loop in loops for p in loop];fs=[tuple(reversed(range(k)))]
 for level in range(len(loops)-1):
  for i in range(k):j=(i+1)%k;fs.append((level*k+i,level*k+j,(level+1)*k+j,(level+1)*k+i))
 fs.append(tuple((len(loops)-1)*k+i for i in range(k)));return mesh(name,vs,fs,mat,role)
def box(name,lo,hi,mat,role):
 x0,y0,z0=lo;x1,y1,z1=hi
 return solid_loops(name,[[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)] for z in [z0,z1]],mat,role)
def poly_y(name,outline,y0,y1,mat,role):
 k=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def revolve(name,profile,centre,mat,role,n=20):
 vs=[(centre[0]+r*math.cos(math.tau*i/n),centre[1]+r*math.sin(math.tau*i/n),z) for z,r in profile for i in range(n)];fs=[]
 for j in range(len(profile)-1):
  for i in range(n):ii=(i+1)%n;fs.append((j*n+i,j*n+ii,(j+1)*n+ii,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
# One watertight cup: outer bottom -> shoulder -> sloping rim -> inner rim -> actual floor.
# The last cap is at the bottom of the cavity, not its mouth. No false dark-plane hollow.
loops=[]
for x,y,c,z in [(.070,.060,.010,.004),(.074,.064,.012,.018)]:loops.append([(a,b,z) for a,b in octagon(x,y,c)])
for x,y,c in [(.066,.055,.009),(.040,.031,.006)]:loops.append([(a,b,.069+b*(.013/.055)) for a,b in octagon(x,y,c)])
loops.append([(a,b,.022) for a,b in octagon(.034,.025,.005)])
solid_loops('Cradle_ThickCavityShell',loops,0,'single closed thick shell; sloping open mouth, taller rear stop, continuous actual inner walls and 18mm solid floor above the underside')
# 1 bottom, 4x8 joining faces, 1 inner floor. Interior wall and floor have a lighter solid material.
G['Cradle_ThickCavityShell']['face_materials']=[0]+[0]*24+[1]*8+[1]
# Two real tapered guide ribs overlap the sidewalls. The central channel remains open.
for sign,label in [(-1,'Left'),(1,'Right')]:
 profile=[(sign*x,z) for x,z in [(.029,.021),(.041,.021),(.041,.065),(.036,.065)]]
 poly_y('Guide_'+label+'Rib',profile,-.018,.005,2,'solid tapered side guide with broad sidewall seating; central gap 58mm at lower ends, 72mm at top')
 link('Guide_'+label+'Rib','Cradle_ThickCavityShell',(sign*.0395,-.006,.050),spread=.006)
# A seated carrier and two small separately editable static brass contact heads.
box('Contact_FloorCarrier',(-.024,.013,.0205),(.024,.0255,.0255),2,'closed carrier partially embedded into actual cavity floor; occupies only the rear strip')
link('Contact_FloorCarrier','Cradle_ThickCavityShell',(0,.018,.0212),axis=(1,0,0),spread=.016)
for x,label in [(-.013,'Left'),(.013,'Right')]:
 revolve('Contact_'+label+'Point',[(.024,.0025),(.0285,.0025),(.0295,.0015)],(x,.019),3,'static brass contact point seated into its carrier, rounded faceted upper edge; no electrical behavior',n=20)
 link('Contact_'+label+'Point','Contact_FloorCarrier',(x,.019,.0247),axis=(1,0,0),spread=.001)
# Four broad closed feet start exactly on Z=0 and enter the bottom shell by 2mm.
for x,lx in [(-.052,'Left'),(.052,'Right')]:
 for y,ly in [(-.044,'Front'),(.044,'Back')]:
  name='Foot_'+lx+ly;FEET.append(name)
  solid_loops(name,[[(a+x,b+y,z) for a,b in octagon(.010,.009,.002)] for z in [0,.006]],2,'finite rubber support pad; lower planar octagon at Z=0, upper 2mm buried in shell')
  link(name,'Cradle_ThickCavityShell',(x,y,.005),axis=(1,0,0),spread=.004)
# Nine clear vertical cavity paths stop just above the real floor. The companion downward rays hit it.
for x in [-.023,0,.023]:
 for y in [-.012,0,.009]:
  GAPS.append({'label':'clear_cavity_column','origin_m':[x,y,.0222],'direction':[0,0,1],'length_m':.0778})
  FLOOR_RAYS.append({'label':'actual_solid_bearing_floor','origin_m':[x,y,.100],'direction':[0,0,-1],'length_m':.100,'expected_hit_z_m':.022})
# A finite horizontal 50x20 mm open rectangle has no contact-carrier or guide obstruction.
for z in [.030,.050,.070]:
 for y in [-.012,0,.009]:GAPS.append({'label':'clear_central_width','origin_m':[-.025,y,z],'direction':[1,0,0],'length_m':.050})
# Horizontal shell-only thickness probes stay away from the guide ribs and contact carrier.
for z in [.030,.045,.055]:
 for y in [-.010,.010]:
  WALL_RAYS.append({'origin_m':[0,y,z],'direction':[1,0,0],'length_m':.100,'side':'right'})
  WALL_RAYS.append({'origin_m':[0,y,z],'direction':[-1,0,0],'length_m':.100,'side':'left'})
# Convex clipping detects any complete actual triangle intersecting the finite empty prism.
CLEAR_BOX=((- .025,-.012,.0222),(.025,.009,.100))
def triangle_box_intersects(triangle,lo=CLEAR_BOX[0],hi=CLEAR_BOX[1]):
 polygon=[tuple(v) for v in triangle]
 for axis in range(3):
  for limit,sign in [(lo[axis],1),(hi[axis],-1)]:
   old=polygon;polygon=[]
   if not old:return False
   for start,end in zip(old,old[1:]+old[:1]):
    ds=(start[axis]-limit)*sign;de=(end[axis]-limit)*sign;si=ds>=-1e-10;ei=de>=-1e-10
    if si!=ei:polygon.append(add(start,mul(sub(end,start),ds/(ds-de))))
    if ei:polygon.append(end)
 return bool(polygon)
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
root=bpy.data.objects.new('OneEmptyHandheldChargingCradle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual cavity bottom, support patch and thick walls are measured from the generated triangles.
floor_checks=[]
for r in FLOOR_RAYS:
 hits=[]
 for name,t in trees.items():
  point,normal,face,distance=t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])
  if point is not None:hits.append((distance,name,point,normal))
 assert hits,('No actual bearing floor',r)
 distance,name,point,normal=min(hits,key=lambda row:row[0]);assert name=='Cradle_ThickCavityShell' and abs(point.z-.022)<1e-6 and normal.z>.99,(r,name,list(point),list(normal))
 floor_checks.append(dict(r,first_hit_mesh=name,first_hit_m=list(point),normal=list(normal),clear_depth_from_100mm_m=distance))
bearing=horizontal_triangles('Cradle_ThickCavityShell',.022,1);bearing_area=sum(t['area_m2'] for t in bearing);assert bearing_area>.0033
wall_checks=[]
for r in WALL_RAYS:
 tree=trees['Cradle_ThickCavityShell'];direction=Vector(r['direction']);first=tree.ray_cast(Vector(r['origin_m']),direction,r['length_m'])[0]
 assert first is not None
 second=tree.ray_cast(first+direction*1e-5,direction,r['length_m'])[0];assert second is not None
 thickness=(second-first).length;assert thickness>.025,(r,thickness)
 wall_checks.append(dict(r,inner_hit_m=list(first),outer_hit_m=list(second),actual_thickness_m=thickness))
# Both contacts are above the carrier yet remain well below the open rim.
contact_checks=[]
for name in ['Contact_LeftPoint','Contact_RightPoint']:
 vv=[byname[name].matrix_world@v.co for v in byname[name].data.vertices];low=min(v.z for v in vv);high=max(v.z for v in vv)
 assert low<.0255<high and abs(high-.0295)<1e-6
 contact_checks.append({'name':name,'bottom_z_m':low,'top_z_m':high,'carrier_top_z_m':.0255})
volume_blockers=[];volume_corners=[(x,y,z) for x in [CLEAR_BOX[0][0],CLEAR_BOX[1][0]] for y in [CLEAR_BOX[0][1],CLEAR_BOX[1][1]] for z in [CLEAR_BOX[0][2],CLEAR_BOX[1][2]]]
for name,o in byname.items():
 for index,t in enumerate(o.data.loop_triangles):
  triangle=[o.matrix_world@o.data.vertices[i].co for i in t.vertices]
  if triangle_box_intersects(triangle):volume_blockers.append({'mesh':name,'triangle':index})
 for i,p in enumerate(volume_corners):
  if inside(trees[name],p):volume_blockers.append({'mesh':name,'contained_corner':i})
assert not volume_blockers,('Finite empty cavity obstructed',volume_blockers)
cradle_evidence={'finite_empty_box_m':CLEAR_BOX,'finite_empty_box_actual_triangle_or_containment_blockers':volume_blockers,'actual_floor_z_m':.022,'floor_thickness_to_outer_bottom_m':.018,'actual_floor_area_before_mounted_parts_m2':bearing_area,'actual_floor_triangles':bearing,
 'full_assembly_downward_floor_probes':floor_checks,'shell_thickness_probes':wall_checks,'actual_contacts':contact_checks,
 'guide_low_inner_gap_m':.058,'guide_top_inner_gap_m':.072,'finite_clear_width_test_m':.050,'clear_cavity_grid_xy_m':[[-.023,0,.023],[-.012,0,.009]],
 'handheld_included':False,'device_compatibility_tested':False,'only_checked_scope':'empty static cradle geometry; no insertion, charging or radio operation'}
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
 'single_prop_count':1,'charging_cradle_geometry':cradle_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/communications/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'communications','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.038));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.205;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,4.6),'gray-back3q':(3,5,4.6)} if gray else {
 'thumbnail':(-3,-5,4.6),'qa-front':(0,-7,.038),'qa-side':(7,0,.038),'qa-top':(0,0,8),
 'qa-back':(0,7,.038),'qa-wireframe':(-3,-5,4.6)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.205
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00008;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.038)),('silhouette-128-side',(7,0,.038))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
