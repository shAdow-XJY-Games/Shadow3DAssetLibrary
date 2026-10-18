"""Original fixed half-inserted mortise-and-tenon sample, two closed wood pieces.
One prop, metres, Z up, front -Y, each body rests on a finite ground patch.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carpentry-mortise-tenon-sample-kit-01';VERSION='1.0.0';TITLE='Half-Inserted Mortise and Tenon Sample'
DESCRIPTION=('One original static woodworking sample set, counted as one prop: two short chamfered wooden pieces in a fixed half-inserted T arrangement. '
 'The cross-member has a real rectangular through-mortise with continuous thick walls. The other piece is one connected closed mesh with an integral reduced rectangular tenon and broad shoulders. '
 'The tenon tip reaches halfway through the 160 mm-deep mortise; 70 mm of neck remains exposed before the shoulder and 80 mm of the hole remains unoccupied behind the tip. '
 'Both bodies have finite flat ground contact. The inserted tenon has a finite face contact on the mortise floor, positive side and upper clearances, and a subtly chamfered tip. '
 'Two named editable closed meshes, four constant solid wood PBR materials, metres, source Z up, front -Y and ground-centre origin. No round peg, extra tool, mounting base or surrounding scene. '
 'Static visual and geometry sample only: no insertion path, sliding, assembly animation, disassembly, mechanical load, joint strength, wood tolerance or shrinkage, glue, machining drawing, manufacturing feasibility, furniture suitability or woodworking safety guarantee.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Receiver_HoneyWood',(.50,.265,.105,1),.67,0),('Receiver_EndWood',(.64,.36,.16,1),.72,0),('Tenon_WarmWood',(.64,.39,.18,1),.67,0),('Tenon_EndWood',(.76,.49,.25,1),.72,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
FBOX=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box_data(c,s):
 x,y,z=c;a,b,d=[q/2 for q in s];return {'vertices':[(x-a,y-b,z-d),(x+a,y-b,z-d),(x+a,y+b,z-d),(x-a,y+b,z-d),(x-a,y-b,z+d),(x+a,y-b,z+d),(x+a,y+b,z+d),(x-a,y+b,z+d)],'faces':FBOX}
def octagon(w,low,high,c):return [(-w+c,low),(w-c,low),(w,low+c),(w,high-c),(w-c,high),(-w+c,high),(-w,high-c),(-w,low+c)]
def ring(v,profile,y):
 ids=list(range(len(v),len(v)+len(profile)));v.extend((x,y,z) for x,z in profile);return ids
# Annular end between a chamfered outer rectangle and a genuine four-sided
# opening. Each outer corner has its own triangle; no T-junctions or fake cap.
def annulus(f,fm,outer,inner,material,reverse=False):
 a=[]
 for j in range(4):
  k=2*j;a.append((outer[k],outer[(k+1)%8],inner[(j+1)%4],inner[j]))
  a.append((outer[(k+1)%8],outer[(k+2)%8],inner[(j+1)%4]))
 for q in a:f.append(tuple(reversed(q)) if reverse else q);fm.append(material)
def bridge(f,fm,a,b,material,reverse=False):
 for i in range(len(a)):
  q=(a[i],a[(i+1)%len(a)],b[(i+1)%len(b)],b[i]);f.append(tuple(reversed(q)) if reverse else q);fm.append(material)
# Cross-member outer end chamfers are separate from its sharply rectangular
# through-hole. The entire receiver is a single closed genus-one material shell.
v=[];f=[];fm=[]
rings=[ring(v,octagon(w,lo,hi,.003),y) for y,w,lo,hi in [(.08,.227,.003,.117),(.083,.23,0,.12),(.237,.23,0,.12),(.24,.227,.003,.117)]]
for a,b in zip(rings,rings[1:]):bridge(f,fm,a,b,0)
hole=[(-.042,.036),(.042,.036),(.042,.084),(-.042,.084)]
h0=ring(v,hole,.08);h1=ring(v,hole,.24)
annulus(f,fm,rings[0],h0,1,True);annulus(f,fm,rings[-1],h1,1);bridge(f,fm,h0,h1,0,True)
RECEIVER=mesh('Receiver_ContinuousThroughMortise',v,f,0,'one closed chamfered cross-member with actual rectangular through-hole and four continuous thick cavity walls',fm);FEET.append(RECEIVER)
# One uninterrupted closed male mesh. The front annulus is real wood shoulder
# material and its inner loop continues straight into the reduced tenon.
v=[];f=[];fm=[]
rings=[ring(v,octagon(w,lo,hi,.003),y) for y,w,lo,hi in [(-.24,.072,.003,.117),(-.237,.075,0,.12),(.007,.075,0,.12),(.01,.072,.003,.117)]]
for a,b in zip(rings,rings[1:]):bridge(f,fm,a,b,2)
f.append(tuple(reversed(rings[0])));fm.append(3)
neck=[(-.037,.036),(.037,.036),(.037,.080),(-.037,.080)]
n0=ring(v,neck,.01);n1=ring(v,neck,.1585)
nt=ring(v,[(-.0355,.0375),(.0355,.0375),(.0355,.0785),(-.0355,.0785)],.16)
annulus(f,fm,rings[-1],n0,3);bridge(f,fm,n0,n1,2);bridge(f,fm,n1,nt,3);f.append(tuple(nt));fm.append(3)
MALE=mesh('Male_IntegralShoulderedTenon',v,f,2,'one closed chamfered grounded body, four real shoulders and integral reduced rectangular tenon; bevel tip half-inserted into mortise',fm);FEET.append(MALE)
# Explicit outward face winding is retained before Blender normal validation.
for g in G.values():g['faces']=[tuple(reversed(f)) for f in g['faces']]
# Only the hidden, opposing horizontal faces share finite area: the tenon
# underside touches the mortise floor at Z .036, X +/- .037, Y .08 to .1585.
# This is contact, never interpenetration or a duplicated externally visible face.
CONTACT={'a':RECEIVER,'b':MALE,'plane_z_m':.036,'rectangle_xy_m':[-.037,.037,.08,.1585],'expected_contact_area_m2':.074*.0785,'nature':'opposing finite floor contact, zero interior overlap'}
# Every probe is a complete finite volume, not a rendered asset component.
VOID_VOLUMES['Mortise_RemainingRearCavity']=box_data((0,.2105,.060),(.082,.099,.046))
VOID_VOLUMES['InsertedTenon_LeftSideClearance']=box_data((-.0395,.1195,.058),(.004,.077,.042))
VOID_VOLUMES['InsertedTenon_RightSideClearance']=box_data((.0395,.1195,.058),(.004,.077,.042))
VOID_VOLUMES['InsertedTenon_UpperClearance']=box_data((0,.1195,.082),(.072,.077,.003))
# Full hole opening is only tested against the isolated receiver. In the full
# assembly the tenon intentionally occupies its lower central front half.
for x,z in [(0,.060),(-.040,.060),(.040,.060),(0,.082)]:BORES.append({'mesh':RECEIVER,'origin_m':(x,.06,z),'direction':(0,1,0),'length_m':.20})
for x,z in [(-.040,.060),(.040,.060),(0,.082)]:GAPS.append({'label':'assembled_longitudinal_positive_gap','origin_m':(x,.06,z),'direction':(0,1,0),'length_m':.20})
for x in [-.025,0,.025]:
 FLOOR_PROBES.append({'mesh':RECEIVER,'origin_m':(x,.20,.060),'direction':(0,0,-1),'length_m':.08,'expected_hits_m':[.024,.060]})
for x,d in [(-.05,(-1,0,0)),(.05,(1,0,0))]:
 # Begins inside solid wood, so for thickness use a full inward-origin ray.
 WALL_PROBES.append({'mesh':RECEIVER,'origin_m':(0,.20,.060),'direction':d,'length_m':.30,'minimum_thickness_m':.1879,'maximum_thickness_m':.1881})
def triangle_box_intersects(triangle,lo,hi):
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
def measure_joinery_geometry(vertices,triangles):
 checks=[]
 for label,box in VOID_VOLUMES.items():
  lo=[min(v[i] for v in box['vertices']) for i in range(3)];hi=[max(v[i] for v in box['vertices']) for i in range(3)]
  blockers=[n for n,tt in triangles.items() if any(triangle_box_intersects(t,lo,hi) for t in tt)];assert not blockers,('Finite empty volume blocked',label,blockers)
  checks.append({'name':label,'lo_m':lo,'hi_m':hi,'actual_surface_box_intersections':0})
 tv=[p for p in vertices[MALE] if p[1]>=.01-1e-7];iv=[p for p in vertices[RECEIVER] if abs(abs(p[0])-.042)<1e-7 and .0359<p[2]<.0841]
 assert len(tv)==20 and len(iv)==8,(len(tv),len(iv))
 hole_lo=[min(p[i] for p in iv) for i in range(3)];hole_hi=[max(p[i] for p in iv) for i in range(3)]
 neck=[p for p in tv if abs(p[0])<=.03701 and .0359<p[2]<.0801];assert len(neck)==12
 tip=max(p[1] for p in neck);start=min(p[1] for p in neck)
 clear={'left':min(p[0] for p in neck)-hole_lo[0],'right':hole_hi[0]-max(p[0] for p in neck),'above':hole_hi[2]-max(p[2] for p in neck),'floor':min(p[2] for p in neck)-hole_lo[2]}
 assert all(abs(clear[k]-val)<1e-6 for k,val in [('left',.005),('right',.005),('above',.004),('floor',0)]),clear
 assert abs((tip-hole_lo[1])/(hole_hi[1]-hole_lo[1])-.5)<1e-6
 assert abs(hole_lo[1]-start-.07)<1e-6 and abs(hole_hi[1]-tip-.08)<1e-6
 return {'finite_empty_volume_surface_checks':checks,'actual_rectangular_hole_bounds_m':[hole_lo,hole_hi],'whole_tenon_coordinate_extreme_clearance_to_planar_inner_walls_m':clear,'inserted_tip_depth_m':tip-hole_lo[1],'hole_depth_m':hole_hi[1]-hole_lo[1],'tip_insertion_fraction':.5,'exposed_neck_length_m':hole_lo[1]-start,'remaining_hole_length_m':hole_hi[1]-tip,'declared_finite_contact':CONTACT,'counted_props':1,'closed_wood_pieces':2,'simulation_tested':False}
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
root=bpy.data.objects.new('OneMortiseTenonSampleKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.001,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
def actual_ray_distances(r):
 origin=Vector(r['origin_m']);direction=Vector(r['direction']).normalized();current=origin.copy();distances=[]
 for _ in range(8):
  q,_,_,_=trees[r['mesh']].ray_cast(current,direction,r['length_m'])
  if q is None:break
  distance=(q-origin).length
  if distance>r['length_m']:break
  distances.append(float(distance));current=q+direction*1e-5
 return distances
floor_checks=[];wall_checks=[]
for r in FLOOR_PROBES:
 distances=actual_ray_distances(r);assert len(distances)==2 and all(abs(distances[i]-r['expected_hits_m'][i])<2e-6 for i in range(2)),('Actual thick floor missing',r,distances)
 floor_checks.append(dict(r,actual_hit_distances_m=distances,actual_floor_thickness_m=distances[1]-distances[0]))
for r in WALL_PROBES:
 distances=actual_ray_distances(r);assert len(distances)==2 and r['minimum_thickness_m']<distances[1]-distances[0]<r['maximum_thickness_m'],('Actual thick wall missing',r,distances)
 wall_checks.append(dict(r,actual_hit_distances_m=distances,actual_wall_thickness_m=distances[1]-distances[0]))
joinery_evidence=measure_joinery_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts},{o.name:[[o.matrix_world@o.data.vertices[i].co for i in t.vertices] for t in o.data.loop_triangles] for o in parts})
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
 'single_prop_count':1,'joinery_geometry':dict(joinery_evidence,actual_floor_probes=floor_checks,actual_wall_probes=wall_checks),'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carpentry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.060));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.69;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,4),'gray-back3q':(3,5,3)} if gray else {
 'thumbnail':(-5,-3,5),'qa-front':(0,-7,.060),'qa-side':(7,0,.060),'qa-top':(0,0,8),
 'qa-back':(0,7,.060),'qa-wireframe':(-5,-3,5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.69
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0009;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.060)),('silhouette-128-side',(7,0,.060))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
