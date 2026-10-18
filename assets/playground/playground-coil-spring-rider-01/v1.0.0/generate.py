"""One original abstract-bird spring rider in one fixed static pose.
Metres, Z up, rider faces +X, origin on ground below coil axis. No motion/safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='playground-coil-spring-rider-01';VERSION='1.0.0';TITLE='Abstract Bird Coil Spring Rider'
DESCRIPTION=('One original low-poly abstract bird-shaped rider in one fixed static pose: a thick coral profile body, separate thick petrol saddle, transverse metal handle with two grips, transverse foot bar with two foot pads, and a single continuous three-turn vertical helical spring. The spring has a real closed ten-sided circular section and visible positive turn spacing, with both ends embedded in distinct fixing plates. The upper plate joins the body and the lower plate joins a broad finite grounded base. Constant opaque PBR colors only. One complete assembly counts as one prop. Metres, Z up, bird faces +X, origin at ground under the coil axis. '
 'Original simplified silhouette with no characters, logos, textures, extra rider, soft mat or scene. Static visual geometry only: no spring deformation, rocking, motion, physical simulation, child/adult fit, age guidance, load rating, installation fit, stability or anti-tip performance, manufacturing specification or playground/child safety certification. No asserted compatibility with existing scenes or mats.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};HELIX_CELLS=[]
PALETTE=[('Body_WarmCoral',(.70,.19,.085,1),.51,.0),('Saddle_DeepPetrol',(.035,.18,.19,1),.44,.0),('Spring_SatinHoney',(.77,.48,.12,1),.37,.35),('Mounts_Graphite',(.095,.13,.145,1),.43,.55)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(0,1,0),spread=.012):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def prism_profile(profile,ymin,ymax):
 n=len(profile);v=[(x,y,z) for y in [ymin,ymax] for x,z in profile]
 f=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
 return v,f

def cylinder_geometry(p,q,r,n=12):
 p=tuple(p);q=tuple(q);axis=unit(sub(q,p));u=unit(cross(axis,(0,0,1) if abs(axis[2])<.9 else (0,1,0)));v=cross(axis,u)
 vv=[add(c,mul(add(mul(u,math.cos(j*math.tau/n)),mul(v,math.sin(j*math.tau/n))),r)) for c in [p,q] for j in range(n)]
 ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return vv,ff

def cylinder(name,p,q,r,mat,role,n=12):return mesh(name,*cylinder_geometry(p,q,r,n),mat,role)

def helix_geometry(radius,wire_radius,z0,pitch,turns,segments,sides):
 vv=[]
 for i in range(segments+1):
  a=math.tau*turns*i/segments;p=(radius*math.cos(a),radius*math.sin(a),z0+pitch*a/math.tau)
  tangent=unit((-radius*math.sin(a),radius*math.cos(a),pitch/math.tau));normal=(math.cos(a),math.sin(a),0);binormal=cross(tangent,normal)
  for j in range(sides):
   b=math.tau*j/sides;vv.append(add(p,mul(add(mul(normal,math.cos(b)),mul(binormal,math.sin(b))),wire_radius)))
 ff=[]
 for i in range(segments):
  for j in range(sides):
   k=(j+1)%sides;a=i*sides+j;b=i*sides+k;c=(i+1)*sides+k;d=(i+1)*sides+j
   # Explicit triangles make the same piecewise-flat surfaces unambiguous in GLB.
   ff.extend([(a,b,c),(a,c,d)])
 ff.extend([tuple(reversed(range(sides))),tuple(segments*sides+j for j in range(sides))]);return vv,ff

base=box('Base_BroadGroundedPlinth',(0,0,.0375),(.56,.50,.075),3,'single wide finite ground base, visual only')
FEET.append(base)
lower=box('Mount_LowerFixingPlate',(0,0,.0925),(.37,.37,.055),3,'lower plate embedded 10 mm in base; terminal spring section embedded in plate')
link(base,lower,(0,0,.070),axis=(1,0,0),spread=.10)
RADIUS=.145;WIRE_RADIUS=.024;PITCH=.14;TURNS=3;SEGMENTS=120;SECTION_SIDES=10;Z0=.109
coil=mesh('Spring_ContinuousThreeTurnHelix',*helix_geometry(RADIUS,WIRE_RADIUS,Z0,PITCH,TURNS,SEGMENTS,SECTION_SIDES),2,'ONE continuous closed vertical helical tube, 3 turns, ten-sided real circular section; no separate rings')
# Complete closed finite cells use the exact stored coil-ring vertices. Their caps
# are mathematical cross sections, not additional exported objects.
for i in range(SEGMENTS):
 ids=list(range(i*SECTION_SIDES,(i+2)*SECTION_SIDES));v=[G[coil]['vertices'][j] for j in ids]
 f=[tuple(reversed(range(SECTION_SIDES))),tuple(range(SECTION_SIDES,2*SECTION_SIDES))]
 for j in range(SECTION_SIDES):
  k=(j+1)%SECTION_SIDES;f.extend([(j,k,k+SECTION_SIDES),(j,k+SECTION_SIDES,j+SECTION_SIDES)])
 HELIX_CELLS.append({'index':i,'coil_vertex_indices':ids,'vertices':v,'faces':f})
upper=box('Mount_UpperFixingPlate',(0,0,.553),(.37,.37,.066),3,'upper plate holds terminal coil section and lower body with finite interior overlaps')
link(lower,coil,(RADIUS*math.cos(.04),RADIUS*math.sin(.04),Z0+PITCH*.04/math.tau),axis=(1,0,0),spread=.007)
link(upper,coil,(RADIUS*math.cos(.04),-RADIUS*math.sin(.04),Z0+PITCH*TURNS-PITCH*.04/math.tau),axis=(1,0,0),spread=.007)
profile=[(-.33,.72),(-.36,.81),(-.25,.85),(-.16,.80),(.04,.80),(.10,.92),(.08,1.01),(.17,1.06),(.28,1.04),(.36,.97),(.29,.94),(.26,.80),(.20,.68),(.12,.57),(-.12,.57),(-.22,.68)]
body=mesh('Rider_OriginalAbstractBirdProfile',*prism_profile(profile,-.055,.055),0,'original thick 2D bird-like profile extruded to a real closed body; no likeness or IP')
link(upper,body,(0,0,.578),axis=(1,0,0),spread=.05)
saddle=box('Saddle_ThickSeatBoard',(-.105,0,.81),(.37,.26,.05),1,'separate thick seat board finitely embedded in top body')
link(body,saddle,(-.08,0,.793),axis=(1,0,0),spread=.045)
handle=cylinder('Handle_TransverseBar',(.205,-.18,.985),(.205,.18,.985),.018,3,'solid transverse handle passing through head profile')
link(body,handle,(.205,0,.985),spread=.025)
for suffix,sgn in [('Near',-1),('Far',1)]:
 grip=cylinder('Handle_Grip_'+suffix,(.205,sgn*.125,.985),(.205,sgn*.215,.985),.025,1,'solid colored end grip with finite interior overlap into transverse bar')
 link(handle,grip,(.205,sgn*.151,.985),spread=.009)
footbar=cylinder('Foot_TransverseBar',(.13,-.222,.675),(.13,.222,.675),.018,3,'solid transverse foot support passing through lower body')
link(body,footbar,(.13,0,.675),spread=.025)
for suffix,sgn in [('Near',-1),('Far',1)]:
 pad=box('Foot_Pad_'+suffix,(.13,sgn*.19,.676),(.13,.13,.038),1,'one finite thickness foot pad embedded around transverse bar')
 link(footbar,pad,(.13,sgn*.19,.675),spread=.012)
# Full finite free-space volumes: a two-turn helical corridor halfway between
# neighboring spring turns and a central cylindrical empty bore. Neither exported.
v,f=helix_geometry(RADIUS,.016,Z0+PITCH/2,PITCH,2,80,10)
VOID_VOLUMES['Interturn_ContinuousFiniteCorridor']={'vertices':v,'faces':f,'role':'full two-turn finite helical gap volume, not a centerline or ray'}
v,f=cylinder_geometry((0,0,.126),(0,0,.514),.085,16)
VOID_VOLUMES['Coil_CentralFiniteEmptyBore']={'vertices':v,'faces':f,'role':'finite empty central volume between the two plates'}
GAPS.append({'origin_m':(0,-.11,.32),'direction':(0,1,0),'length_m':.22,'meaning':'supplementary inner-bore ray only; full finite volumes decide acceptance'})
SPRING_CONTRACT={'coil':coil,'lower_plate':lower,'upper_plate':upper,'body':body,'saddle':saddle,'handle':handle,'footbar':footbar,'base':base,'turns':TURNS,'pitch_m':PITCH,'centerline_radius_m':RADIUS,'section_radius_m':WIRE_RADIUS,'section_sides':SECTION_SIDES,'finite_cells':SEGMENTS,'nonadjacent_cell_min_clearance_m':.004,'skip_only_shared_ring_neighbor_cells':1,'minimum_axis_rise_m':.42,'coil_vertex_rings':[list(range(i*SECTION_SIDES,(i+1)*SECTION_SIDES)) for i in range(SEGMENTS+1)],'static_visual_only':True}
def measure_spring_rider_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 bounds=lambda n:([min(float(p[k]) for p in vertices[n]) for k in range(3)],[max(float(p[k]) for p in vertices[n]) for k in range(3)])
 lo,hi=bounds(base);assert abs(lo[2])<1e-7 and abs(hi[2]-.075)<1e-6
 # Every ring is measured from its actual section vertices, never declared AABBs.
 centers=[tuple(sum(float(vertices[coil][j][k]) for j in ring)/SECTION_SIDES for k in range(3)) for ring in SPRING_CONTRACT['coil_vertex_rings']]
 angles=[]
 for i,c in enumerate(centers):
  a=math.tau*TURNS*i/SEGMENTS;expected=(RADIUS*math.cos(a),RADIUS*math.sin(a),Z0+PITCH*a/math.tau)
  assert max(abs(c[k]-expected[k]) for k in range(3))<2e-6,('Changed actual coil section position',i,c,expected)
  radii=[math.sqrt(sum((float(vertices[coil][j][k])-c[k])**2 for k in range(3))) for j in SPRING_CONTRACT['coil_vertex_rings'][i]]
  assert max(abs(r-WIRE_RADIUS) for r in radii)<2e-6,('Changed actual coil finite section',i)
 for name in [lower,upper,body,saddle,handle,footbar]+[n for n in G if n.startswith(('Handle_Grip','Foot_Pad'))]:
  # Full source-vs-actual vertex content equality is independently checked; this
  # dimensional statement gives no physical fit or use-performance guarantee.
  assert len(vertices[name])==len(G[name]['vertices'])
 return {'single_prop_count':1,'coil_continuous_turns':TURNS,'actual_section_rings':len(centers),'actual_axis_rise_m':centers[-1][2]-centers[0][2],'section_diameter_m':WIRE_RADIUS*2,'pitch_m':PITCH,'axis_aligned_nominal_turn_gap_m':PITCH-2*WIRE_RADIUS,'lower_upper_plate_count':2,'separate_seat_handle_foot_supports':True,'finite_base_contact_nominal_m2':.28,'motion_load_or_safety_claim':False}
FOCUS=(0,0,.53);ORTHO=1.55
CAMERAS={'gray-front3q':(2.5,-3,2.05),'gray-back3q':(-2.5,3,2.05),'thumbnail':(2.5,-3,2.05),'qa-front':(0,-3,1.35),'qa-side':(3,0,1.35),'qa-top':(0,0,3),'qa-back':(0,3,1.35),'qa-wireframe':(2.5,-3,2.05),'silhouette-128-front':(0,-3,1.35),'silhouette-128-side':(3,0,1.35)}
WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneAbstractBirdSpringRider',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='+X';root['static_visual_only']=True;root['origin_datum']='ground X midline, Y=0, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in [(coil,(-RADIUS,0,Z0+PITCH/2),(0,0,.30)),(body,(0,0,.70),(.4,0,.70))]:
 assert inside(trees[name],p) is True
 assert inside(trees[name],outside) is False
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_spring_rider_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'spring_rider_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/playground/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
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
 for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
