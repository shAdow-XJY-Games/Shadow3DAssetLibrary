"""Original single grooved wooden quarter-turn puzzle track module.
Metres, Z up. Origin is the centre of the generating arc at ground level.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='toys-grooved-puzzle-track-quarter-01';VERSION='1.0.0';TITLE='Grooved Wooden Quarter-Turn Puzzle Track'
DESCRIPTION=('One original low-poly wooden-colour quarter-turn puzzle track, counted as one static modular asset. A single continuous thick arc board has an entire finite flat bottom, two genuine shallow blind wheel grooves retaining material underneath, a full-height central bridge and outer shoulders. One end has an integral short neck and rounded male puzzle head; the other has a genuine open-neck rounded female cutout through the full board thickness. Two instances of this same frozen source are checked only as evidence at a 90-degree rotation: finite opposed end shoulders, complete head and neck clearance, groove end cross-sections and the actual local join. Only one module is delivered. Original unbranded dimensions and interfaces; no metal railway rails, sleepers, track scene, extra train or QA pairing instance. No insertion process, snap lock, complete circle, rolling, steering, guidance, wheel gauge, old train or brand compatibility, age suitability, child or toy safety, swallowing, pinching, material performance, manufacture, strength or durability claim or certification.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
PALETTE=[('Wood_Honey',(.58,.32,.105,1),.71,0),('Groove_WarmWood',(.40,.205,.062,1),.76,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def c2(a,b):return a[0]*b[1]-a[1]*b[0]
def ear2(p):
 order=list(range(len(p)))
 if area2(p)<0:order.reverse()
 out=[]
 while len(order)>3:
  found=False
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if c2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def contains(q):return all(c2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(contains(p[q]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(i);found=True;break
  assert found,('Cannot triangulate analytic board boundary',len(order))
 out.append(tuple(order));return out
R=.44;H=.022;FLOOR=.016;N=40
RADII=[.38,.4045,.4155,.4645,.4755,.50]
NECK=.024;HEAD=.020;HEAD_C=.026;SOCKET_NECK=.028;SOCKET_HEAD=.022
ANGLE=[math.pi*.5*i/N for i in range(N+1)]
def polar(r,a):return(round(r*math.cos(a),9),round(r*math.sin(a),9))
def arc(r,reverse=False):return[polar(r,a) for a in (list(reversed(ANGLE)) if reverse else ANGLE)]
def male_outline():
 a=math.acos(-NECK/(2*HEAD));b=2*math.pi+math.acos(NECK/(2*HEAD))
 curve=[(R+HEAD*math.cos(a+(b-a)*i/34),-HEAD_C+HEAD*math.sin(a+(b-a)*i/34)) for i in range(35)]
 return[(R-NECK/2,0)]+curve+[(R+NECK/2,0)]
def female_outline(clearance_inset=0):
 # Open cavity perimeter from upper mouth to lower mouth. Same analytic design
 # as rotated male, but wider neck and larger rounded head, never a solid decal.
 w=SOCKET_NECK/2-clearance_inset;r=SOCKET_HEAD-clearance_inset;a=math.pi-math.asin(w/r)
 curve=[(HEAD_C+r*math.cos(a-2*a*i/36),R+r*math.sin(a-2*a*i/36)) for i in range(37)]
 return[(0,R+w)]+curve+[(0,R-w)]
BAND_POLYGONS=[]
for j,(ri,ro) in enumerate(zip(RADII,RADII[1:])):
 p=arc(ri,True)
 if j==2:p+=male_outline()
 p+=arc(ro)
 if j==2:p+=female_outline()
 assert area2(p)>0
 BAND_POLYGONS.append(p)
# Build the sole closed boundary from the five planar top/bottom regions.
# Shared bottom seams have identical vertices. Internal band walls include only
# the exposed groove steps; no hidden coincident/internal walls are generated.
vertices=[];faces=[];materials=[];vmap={};edges={}
def vertex(p):
 key=tuple(round(float(x),9) for x in p)
 if key not in vmap:vmap[key]=len(vertices);vertices.append(key)
 return vmap[key]
def tri(points,material):faces.append(tuple(vertex(p) for p in points));materials.append(material)
def wall(p,q,z0,z1,mat):
 a=(*p,z0);b=(*q,z0);c=(*q,z1);d=(*p,z1);tri([a,b,c],mat);tri([a,c,d],mat)
for j,p in enumerate(BAND_POLYGONS):
 h=FLOOR if j in[1,3] else H
 for a,b,c in ear2(p):
  tri([(*p[a],h),(*p[b],h),(*p[c],h)],int(j in[1,3]));tri([(*p[c],0),(*p[b],0),(*p[a],0)],0)
 for a,b in zip(p,p[1:]+p[:1]):
  a=tuple(round(x,9) for x in a);b=tuple(round(x,9) for x in b);key=tuple(sorted([a,b]));edges.setdefault(key,[]).append((a,b,h,j))
for key,rows in edges.items():
 if len(rows)==1:
  p,q,h,j=rows[0]
  for z0,z1 in zip([0,FLOOR],[FLOOR,H]):
   if z0<h:wall(p,q,z0,min(z1,h),0)
 else:
  assert len(rows)==2
  hi=max(rows,key=lambda r:r[2]);lo=min(rows,key=lambda r:r[2]);assert hi[2]>lo[2]
  wall(hi[0],hi[1],lo[2],hi[2],1)
G['ContinuousGroovedPuzzleBoard']={'vertices':vertices,'faces':faces,'face_materials':materials,'material':0,'role':'one closed continuous thick board, two actual blind grooves, integral male neck/head and true full-through female mouth; no overlapping component unions'}
FEET=['ContinuousGroovedPuzzleBoard']
def prism(poly,z0,z1):
 if area2(poly)<0:poly=list(reversed(poly))
 vs=[(*p,z) for z in[z0,z1] for p in poly];n=len(poly);fs=[]
 for a,b,c in ear2(poly):fs.extend([(c,b,a),(a+n,b+n,c+n)])
 fs.extend([(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
 return {'vertices':vs,'faces':fs}
for j in[1,3]:
 poly=arc(RADII[j]+.0005,True)+arc(RADII[j+1]-.0005)
 g=prism(poly,FLOOR+.0005,H+.002);g.update(targets=list(G),role='complete full-length groove air from finite 0.5 mm wall/floor margins to 2 mm above board top, including both open end cross-sections');VOID_VOLUMES['WholeBlindGrooveAir_%d'%j]=g
# Female open cavity air extends 2 mm beyond its external mouth and both faces.
p=female_outline(.0005);p=[(-.002,p[0][1])]+p[1:-1]+[(-.002,p[-1][1])]
g=prism(p,-.002,H+.002);g.update(targets=list(G),role='entire connected open neck and rounded female cutout through board thickness, 0.5 mm lateral margin, 2 mm beyond mouth and both board faces');VOID_VOLUMES['WholeFemaleThroughAir']=g
PAIRING={'source_mesh':'ContinuousGroovedPuzzleBoard','second_instance_rotation_z_degrees':90,'second_instance_translation_m':[0,0,0],'second_instance_is_qa_only':True,'female_port_m':[0,R,0],'male_port_m':[R,0,0],'opposed_shoulder_plane_x_m':0,'minimum_total_shoulder_contact_area_m2':.00175,'nominal_head_radius_clearance_m':SOCKET_HEAD-HEAD,'nominal_neck_side_clearance_m':(SOCKET_NECK-NECK)/2,'groove_floor_m':FLOOR,'groove_radii_m':[[RADII[1],RADII[2]],[RADII[3],RADII[4]]],'actual_seam_scope':'zero nominal separation at finite planar end shoulders and groove floor edges; independent triangle evidence measures tolerance and local polygon tangent direction difference; no seamless, rolling or full-circle claim'}
TRACK_CONTRACT={'single_modular_count':1,'mesh_components':1,'continuous_board':1,'blind_grooves':2,'integral_male_puzzle_head':1,'open_through_female_puzzle_cutout':1,'groove_retained_floor_thickness_m':FLOOR,'board_height_m':H,'quarter_turn_degrees':90,'finite_empty_volumes':3,'qa_only_pair_instances':2}
def measure_track_geometry(actual):
 assert set(actual)==set(G)
 v=list(actual.values())[0];assert abs(min(p[2] for p in v))<2e-7 and abs(max(p[2] for p in v)-H)<2e-7
 return dict(TRACK_CONTRACT,geometry_scope='actual full source/exported triangle coordinates; complete finite material, cavity, self-crossing and pair interfaces require independent gates')
FOCUS=(.24,.23,.012);ORTHO=.79
CAMERAS={'gray-front3q':(1.2,-1.1,1.2),'gray-back3q':(-1.0,1.3,1.0),'thumbnail':(1.2,-1.1,1.2),'qa-front':(.24,-1.8,.95),'qa-side':(1.8,.23,.95),'qa-top':(.24,.23,2),'qa-back':(.24,1.9,.95),'qa-wireframe':(1.2,-1.1,1.2),'silhouette-128-front':(.24,-1.8,.95),'silhouette-128-side':(1.8,.23,.95)}
WIRE_THICKNESS=ORTHO/1200

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
root=bpy.data.objects.new('OneGroovedPuzzleTrack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='generating arc centre at ground Z=0; male (R,0), female (0,R)';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [('ContinuousGroovedPuzzleBoard',(.311126984,.311126984,.008),(.026,.44,.01))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate independent actual-GLB gates.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_track_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'track_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/toys/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'toys','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
