"""Original static hollow boat weaving shuttle, one complete prop.
Continuous thick wooden hull, real side outlet, seated horizontal weft tube.
Metres, Z up, long X axis, viewing front -Y, finite flat ground contact.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='textile-hollow-boat-shuttle-01';VERSION='1.0.0';TITLE='Hollow Wooden Boat Shuttle'
DESCRIPTION=('One original static boat-shaped weaving shuttle with tapered blunt ends, a continuously closed thick wooden hull, a real open elongated cavity and a solid flat-bottomed floor. '
 'One octagonal side outlet genuinely traverses the thick front wall. Two fixed end seats carry a horizontal spindle, one small cream weft core and one faceted muted-teal wound-yarn form. '
 'The internal winding has positive clearances to the wooden side walls and floor; the outlet remains empty and opens into the cavity. '
 'Named closed editable components, five constant solid PBR materials, metres, source Z up, long X axis, front -Y and ground-centre origin. The hull and its internal weft assembly count together as one prop. '
 'Original boat hull geometry, not a reduced basket, recolored frame or duplicate spool set. No loom, extra bobbin, cloth, loose thread tail or surrounding scene. '
 'Static game-art only: no weaving, shuttle motion, yarn release, tension, rotation, disassembly, hand fit, compatibility with any existing loom, manufacture, tool performance or safety guarantee.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];CLEARANCE_PAIRS=[];VOID_VOLUMES={}
PALETTE=[('Wood_Honey',(.48,.225,.075,1),.62,0),('Wood_LightRim',(.72,.415,.16,1),.59,0),('Spindle_DarkSteel',(.12,.145,.155,1),.44,.60),('Core_Cream',(.77,.68,.48,1),.73,0),('Yarn_MutedTeal',(.045,.31,.29,1),.95,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
FBOX=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box_data(c,s):
 x,y,z=c;a,b,d=[q/2 for q in s];return {'vertices':[(x-a,y-b,z-d),(x+a,y-b,z-d),(x+a,y+b,z-d),(x-a,y+b,z-d),(x-a,y-b,z+d),(x+a,y-b,z+d),(x+a,y+b,z+d),(x-a,y+b,z+d)],'faces':FBOX}
def box(name,c,s,mat,role):
 d=box_data(c,s);return mesh(name,d['vertices'],d['faces'],mat,role)
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
# Original matched outlines, CCW from the low front tip around the right end.
# Tapered ends retain 12 mm width; no infinitely sharp zero-thickness tip.
front=[(-.190,-.006),(-.165,-.025),(-.125,-.040),(-.095,-.045),(-.075,-.045),(-.015,-.045),(.015,-.045),(.075,-.045),(.095,-.045),(.125,-.040),(.165,-.025),(.190,-.006)]
innerfront=[(-.143,-.004),(-.132,-.014),(-.118,-.024),(-.095,-.029),(-.075,-.029),(-.015,-.029),(.015,-.029),(.075,-.029),(.095,-.029),(.118,-.024),(.132,-.014),(.143,-.004)]
outer=front+[(x,-y) for x,y in reversed(front)];inner=innerfront+[(x,-y) for x,y in reversed(innerfront)];N=len(outer)
rings=[[(x*.94,y*.78,0) for x,y in outer],[(x,y,.009) for x,y in outer],[(x,y,.044) for x,y in outer],[(x,y,.044) for x,y in inner],[(x,y,.008) for x,y in inner]]
vs=[v for row in rings for v in row];fs=[];fm=[];port_i=6
for j in range(len(rings)-1):
 for i in range(N):
  if i==port_i and j in [1,3]:continue
  fs.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i));fm.append(1 if j==2 else 0)
fs += [tuple(reversed(range(N))),tuple(4*N+i for i in range(N))];fm += [0,0]
# Cut the matching front outer/inner rectangles, construct two annuli around
# real octagonal openings, and bridge corresponding hole edges through 16 mm.
# All original rectangle boundaries are retained without T junctions.
port_rings=[]
for y,lowrow,highrow,inward in [(-.045,1,2,False),(-.029,4,3,True)]:
 h=[]
 for k in range(8):
  a=-3*math.pi/4+math.tau*k/8;h.append(len(vs));vs.append((.045+.006*math.cos(a),y,.027+.006*math.sin(a)))
 port_rings.append(h);rect=[lowrow*N+port_i,lowrow*N+port_i+1,highrow*N+port_i+1,highrow*N+port_i]
 for k in range(4):
  f=(rect[k],rect[(k+1)%4],h[(2*k+2)%8],h[(2*k+1)%8],h[2*k])
  fs.append(tuple(reversed(f)) if inward else f);fm.append(0)
for k in range(8):fs.append((port_rings[0][k],port_rings[0][(k+1)%8],port_rings[1][(k+1)%8],port_rings[1][k]));fm.append(1)
HULL=mesh('Shuttle_ContinuousHollowWoodHull',vs,fs,0,'one closed thick boat shell, real open chamber, integral floor, finite underside and true octagonal side outlet');G[HULL]['face_materials']=fm;FEET.append(HULL)
# Fixed finite bearing blocks rest 1 mm into the real floor. Their gap to the
# end of the ivory core remains visible. No revolute-joint behavior is implied.
for side,x in [('Left',-.112),('Right',.112)]:
 seat=box('Spindle_EndSeat_'+side,(x,0,.021),(.022,.022,.028),0,'solid fixed end seat seated 1 mm into hull floor and carrying the spindle through its upper portion')
 link(HULL,seat,(x,0,.0075),axis=(0,1,0),spread=.004)
def turned(name,profile,mat,role,n=16):
 v=[(x,r*math.cos(math.tau*i/n),.027+r*math.sin(math.tau*i/n)) for x,r in profile for i in range(n)];f=[]
 for j in range(len(profile)-1):
  for i in range(n):f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 f += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 return mesh(name,v,f,mat,role)
shaft=turned('Spindle_FixedHorizontalAxle',[(-.122,.0036),(.122,.0036)],2,'fixed solid horizontal axle held by both end seats; intentionally overlaps the core, no motion or sliding claim')
for side,x in [('Left',-.112),('Right',.112)]:link('Spindle_EndSeat_'+side,shaft,(x,0,.027),axis=(1,0,0),spread=.004)
core=turned('Weft_CreamCore',[(-.094,.0048),(-.089,.006),(.089,.006),(.094,.0048)],3,'one small solid weft core intentionally seats over the fixed spindle')
link(shaft,core,(0,0,.027),axis=(1,0,0),spread=.050)
profile=[(-.077,.009),(-.073,.012),(-.065,.014),(-.050,.0146),(-.035,.015),(-.020,.0147),(0,.0144),(.020,.0147),(.035,.015),(.050,.0146),(.065,.014),(.073,.012),(.077,.009),(.077,.0055),(-.077,.0055)]
n=16;wv=[(x,r*math.cos(math.tau*i/n),.027+r*math.sin(math.tau*i/n)) for x,r in profile for i in range(n)];wf=[]
for j in range(len(profile)):
 for i in range(n):wf.append((j*n+i,j*n+(i+1)%n,((j+1)%len(profile))*n+(i+1)%n,((j+1)%len(profile))*n+i))
yarn=mesh('Weft_SingleWoundYarn',wv,wf,4,'one continuous closed annular faceted yarn winding with real inner sleeve, finite overlap onto cream core and 4 mm minimum floor clearance')
link(core,yarn,(0,.00572,.027),axis=(1,0,0),spread=.04)
# Full finite empty volumes include both long chamber galleries, the continuous
# under-winding gallery, the exposed space above the internal winding, and the
# complete side outlet from exterior to cavity. Probes never become model parts.
VOID_VOLUMES['Cavity_FrontGallery']=box_data((0,-.023,.0255),(.184,.010,.033))
VOID_VOLUMES['Cavity_RearGallery']=box_data((0,.023,.0255),(.184,.010,.033))
VOID_VOLUMES['Cavity_UnderWinding']=box_data((0,0,.010),(.182,.030,.002))
VOID_VOLUMES['Cavity_AboveWinding']=box_data((0,0,.043),(.182,.056,.001))
VOID_VOLUMES['SideOutlet_ThroughThickWall']=box_data((.045,-.039,.027),(.006,.034,.006))
# Front/rear chamber rays deliberately avoid the central weft assembly.
for x in [-.08,0,.08]:
 for y in [-.023,.023]:
  FLOOR_PROBES.append({'mesh':HULL,'origin_m':(x,y,.060),'direction':(0,0,-1),'length_m':.075,'expected_hits_m':[.052,.060]})
  GAPS.append({'label':'empty_chamber_side_gallery','origin_m':(x,y,.050),'direction':(0,0,-1),'length_m':.041})
for x in [-.05,.045]:
 WALL_PROBES.append({'mesh':HULL,'origin_m':(x,-.020,.017),'direction':(0,-1,0),'length_m':.040,'minimum_thickness_m':.0159,'maximum_thickness_m':.0161})
for dx,dz in [(0,0),(-.002,0),(.002,0),(0,-.002),(0,.002)]:
 r={'mesh':HULL,'origin_m':(.045+dx,-.056,.027+dz),'direction':(0,1,0),'length_m':.034};BORES.append(r);GAPS.append(dict(r,label='true_side_outlet_to_cavity'))
# Exact triangle/box clipping supplements the independent all-triangle,
# bidirectional-edge and enclosed-solid checks. It is not a sparse-ray claim.
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
def measure_shuttle_geometry(vertices,triangles):
 checks=[]
 for label,box in VOID_VOLUMES.items():
  lo=[min(v[i] for v in box['vertices']) for i in range(3)];hi=[max(v[i] for v in box['vertices']) for i in range(3)]
  blockers=[n for n,tt in triangles.items() if any(triangle_box_intersects(t,lo,hi) for t in tt)]
  assert not blockers,('Finite empty volume is blocked',label,blockers)
  checks.append({'name':label,'lo_m':lo,'hi_m':hi,'actual_surface_box_intersections':0})
 v=vertices[yarn];floor_gap=min(p[2] for p in v)-.008;side_gap=.029-max(abs(p[1]) for p in v)
 assert floor_gap>.0039 and side_gap>.0139,(floor_gap,side_gap)
 core_gap=min(abs(p[0]) for p in vertices['Spindle_EndSeat_Right'])-max(p[0] for p in vertices[core]);assert core_gap>.0069,core_gap
 return {'finite_empty_volume_surface_checks':checks,'actual_winding_to_floor_clearance_m':floor_gap,'actual_winding_to_central_inner_side_clearance_m':side_gap,'actual_core_to_right_seat_axial_gap_m':core_gap,'floor_thickness_m':.008,'sidewall_thickness_at_outlet_m':.016,'outlet_octagon_circumradius_m':.006,'seat_floor_overlap_m':.001,'counted_props':1,'simulation_tested':False}
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
root=bpy.data.objects.new('OneHollowBoatShuttle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
shuttle_evidence=measure_shuttle_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts},{o.name:[[o.matrix_world@o.data.vertices[i].co for i in t.vertices] for t in o.data.loop_triangles] for o in parts})
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
 'single_prop_count':1,'shuttle_geometry':dict(shuttle_evidence,actual_floor_probes=floor_checks,actual_wall_probes=wall_checks),'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.022));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.46;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-2,-5,4.6),'gray-back3q':(2,5,4.6)} if gray else {
 'thumbnail':(-2,-5,4.6),'qa-front':(0,-7,.022),'qa-side':(7,0,.022),'qa-top':(0,0,8),
 'qa-back':(0,7,.022),'qa-wireframe':(-2,-5,4.6)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.46
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0006;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.022)),('silhouette-128-side',(7,0,.022))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
