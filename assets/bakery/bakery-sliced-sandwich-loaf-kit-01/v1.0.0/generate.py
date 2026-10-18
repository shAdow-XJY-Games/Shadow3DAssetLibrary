"""One original sliced sandwich loaf kit: one remaining loaf and three thick slices.
All cut faces are continuous closed mesh topology. Metres, native Z up, front -Y.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='bakery-sliced-sandwich-loaf-kit-01';VERSION='1.0.0';TITLE='Sliced Sandwich Loaf Kit'
DESCRIPTION=('One static sliced sandwich loaf kit, counted as one prop: a long remaining bread body with a flat base, nearly square shoulders and arched crown, two upright separated 25 mm thick slices and one 25 mm thick slice resting flat to the side. Every cut face is a real closed end surface whose baked crust border and cream crumb are adjacent material regions sharing the same topology. Small shallow crumb dimples are actual connected geometry, never decals, floating inserts or textures. The curved rear heel is fully closed. Every piece has a finite flat ground patch and all four pieces have positive full-surface separation. Four editable closed meshes, four opaque constant PBR colours, no texture or animation. Metres, source Z up, front -Y and ground-centre origin. No plate, knife, chopping board, table, wrapper, label or surrounding scene. '
'Static food appearance only. No edible-product, baking, taste, ingredient, nutrition, allergen, food-safety, hygiene, cutting/fracture physics, softness, manufacture or certification claim. No compatibility with earlier oven, baking tray or display case. Dimensions define visual geometry only.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];CAPS=[];PIECES={}
PALETTE=[('Crust_GoldenBrown',(.47,.205,.066,1),.84,0),('Crown_ToastedOchre',(.34,.116,.031,1),.86,0),('Crumb_WarmCream',(.89,.73,.45,1),.94,0),('CutEdge_HoneyGold',(.66,.335,.099,1),.89,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def polygon_area(p):return abs(sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1])))/2
# CCW in the bread's X/Z cross-section. Bottom and side planes are finite.
PROFILE=[(-.052,0),(.052,0),(.060,.003),(.065,.010),(.067,.020),(.067,.099)]
PROFILE += [(.067*math.cos(math.pi*i/20),.099+.049*math.sin(math.pi*i/20)) for i in range(1,21)]
PROFILE += [(-.067,.020),(-.065,.010),(-.060,.003)]
N=len(PROFILE)
# Strictly convex hull; the inset is a homothety, making a true continuous crust ring.
INNER=[(x*.88,.073+(z-.073)*.88) for x,z in PROFILE]
PORES=[(-.030,.032,.0035),(.014,.028,.0029),(.038,.049,.0037),(-.042,.067,.0030),(-.013,.054,.0040),(.017,.067,.0032),(-.025,.092,.0038),(.034,.099,.0031),(.003,.105,.0041),(-.009,.126,.0028),(.043,.077,.0027),(-.037,.110,.0025)]
def triangulate2(points):
 # Deterministic Bowyer-Watson Delaunay triangulation for the convex crumb outline.
 p=list(points)+[(-10,-10),(10,-10),(0,10)];n=len(points);tri=[(n,n+1,n+2)]
 def incircle(t,q):
  a,b,c=[(p[i][0]-q[0],p[i][1]-q[1]) for i in t]
  det=(a[0]*a[0]+a[1]*a[1])*cross2(b,c)-(b[0]*b[0]+b[1]*b[1])*cross2(a,c)+(c[0]*c[0]+c[1]*c[1])*cross2(a,b)
  return det>1e-18
 for i in range(n):
  bad=[t for t in tri if incircle(t,p[i])];edges=collections.Counter(tuple(sorted((a,b))) for t in bad for a,b in zip(t,t[1:]+t[:1]))
  tri=[t for t in tri if t not in bad]
  for (a,b),count in edges.items():
   if count!=1:continue
   if cross2(sub(p[b],p[a]),sub(p[i],p[a]))<0:a,b=b,a
   tri.append((a,b,i))
 return [t for t in tri if max(t)<n]
def transform(p,pose):
 x,y,z=p
 if pose['flat']:x,y,z=x,z-.074,y+.0125
 a=math.radians(pose['yaw']);c,s=math.cos(a),math.sin(a)
 return (c*x-s*y+pose['centre'][0],s*x+c*y+pose['centre'][1],z)
def inv_transform(p,pose):
 x,y,z=p;x-=pose['centre'][0];y-=pose['centre'][1];a=math.radians(pose['yaw']);c,s=math.cos(a),math.sin(a);x,y=c*x+s*y,-s*x+c*y
 return (x,z-.0125,y+.074) if pose['flat'] else (x,y,z)
def make_bread(name,depth,pose,remaining=False):
 vs=[];fs=[];fm=[];caps=[]
 def vertex(p):vs.append(p);return len(vs)-1
 def face(f,m):fs.append(tuple(f));fm.append(m)
 stations=[(-depth/2,1),(-depth/2+.002,1),(depth/2-.009,1),(depth/2-.003,.982),(depth/2,.94)] if remaining else [(-depth/2,1),(depth/2,1)]
 loops=[]
 for y,scale in stations:loops.append([vertex((x*scale,y,z*scale+(.002 if scale<1 else 0))) for x,z in PROFILE])
 for h,(a,b) in enumerate(zip(loops,loops[1:])):
  for j in range(N):
   k=(j+1)%N;face((a[j],b[j],b[k],a[k]),1 if min(PROFILE[j][1],PROFILE[k][1])>.103 else 0)
 for side,outer in [('front',loops[0]),('back',loops[-1])]:
  y,scale=stations[0 if side=='front' else -1];outward=-1 if side=='front' else 1
  if remaining and side=='back':
   c=vertex((0,y,.073*scale+.002))
   for j in range(N):face((outer[j],outer[(j+1)%N],c),0)
   continue
  inner=[vertex((x,y,z)) for x,z in INNER]
  for j in range(N):face((outer[j],outer[(j+1)%N],inner[(j+1)%N],inner[j]),3)
  pts=list(INNER);depths=[0.]*N;pore_indices=[]
  # The lower face of the flat slice is completely planar for finite support.
  dimples=not(pose['flat'] and side=='front')
  if dimples:
   for cx,cz,r in PORES:
    for k in range(7):
     a=math.tau*k/7;pts.append((cx+r*math.cos(a),cz+r*.77*math.sin(a)));depths.append(0.)
    pore_indices.append(len(pts));pts.append((cx,cz));depths.append(.00065)
  else:pts.append((0,.073));depths.append(0.)
  ids=inner+[vertex((x,y-outward*dep,z)) for (x,z),dep in zip(pts[N:],depths[N:])]
  ts=triangulate2(pts)
  for t in ts:face(tuple(ids[i] for i in t),2)
  # Every small depression is a centre connected only to its seven boundary points.
  for pi in pore_indices:
   neighbors=set(k for t in ts if pi in t for k in t if k!=pi);assert neighbors==set(range(pi-7,pi)),(name,side,pi,neighbors)
  caps.append({'side':side,'local_y_m':y,'outward_sign':outward,'outer_indices':outer,'inner_indices':inner,'crumb_indices':ids,'pore_centre_indices':[ids[i] for i in pore_indices],'cut_crumb_triangle_count':len(ts),'cut_border_faces':N,'dimple_depth_m':.00065 if dimples else 0})
 g={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),7) for c in transform(v,pose)) for v in vs],'faces':fs,'face_materials':fm,'material':0,'role':'remaining closed arched sandwich loaf with genuine exposed cut surface and fully closed rear heel' if remaining else 'separate thick sandwich slice with two continuous closed crumb/crust cut surfaces'}
 G[name]=g;FEET.append(name);PIECES[name]={'depth_m':depth,'pose':pose,'remaining':remaining,'caps':caps};CAPS.extend(dict(c,mesh=name) for c in caps)
make_bread('RemainingLoaf_TrueCutAndHeel',.224,{'centre':(-.036,.068),'yaw':0,'flat':False},True)
make_bread('Slice01_Upright_TrueThickness',.025,{'centre':(-.036,-.089),'yaw':0,'flat':False})
make_bread('Slice02_Upright_TrueThickness',.025,{'centre':(-.026,-.145),'yaw':0,'flat':False})
make_bread('Slice03_Flat_TrueThickness',.025,{'centre':(.150,-.056),'yaw':-13,'flat':True})
# Centre the full visual footprint on the asset origin while retaining z=0.
allv=[p for g in G.values() for p in g['vertices']];SHIFT=[(min(p[i] for p in allv)+max(p[i] for p in allv))/2 for i in [0,1]]
for name,g in G.items():
 g['vertices']=[(round(x-SHIFT[0],7),round(y-SHIFT[1],7),z) for x,y,z in g['vertices']]
 p=PIECES[name]['pose'];p['centre']=(p['centre'][0]-SHIFT[0],p['centre'][1]-SHIFT[1])
def unique(points):return sorted(set(tuple(float(c) for c in p) for p in points))
def measure_loaf_geometry(vertices,triangles=None):
 assert set(vertices)==set(G),'Changed piece count; a kit counts as one prop'
 pieces=[];cap_rows=[]
 for name,g in G.items():
  actual=unique(vertices[name]);expected=unique(g['vertices']);assert len(actual)==len(expected),('Actual closed bread vertex count changed',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(ix)==1 for ix in matches) and len({ix[0] for ix in matches})==len(expected),('Actual bread surface lacks unique one-to-one match',name)
  max_error=max(math.dist(p,expected[ix[0]]) for p,ix in zip(actual,matches))
  p=PIECES[name];local=[inv_transform(v,p['pose']) for v in actual]
  assert abs(max(q[1] for q in local)-min(q[1] for q in local)-p['depth_m'])<3e-6,('True full bread thickness missing',name)
  ground=[q for q in actual if abs(q[2])<1e-6];assert len(ground)>=4,('Finite bottom missing',name)
  patches=[]
  if triangles is not None:
   for t in triangles[name]:
    if max(abs(q[2]) for q in t)<1.1e-6:patches.append(t)
   area=sum(math.sqrt(sum(c*c for c in (sub(t[1],t[0])[1]*sub(t[2],t[0])[2]-sub(t[1],t[0])[2]*sub(t[2],t[0])[1],sub(t[1],t[0])[2]*sub(t[2],t[0])[0]-sub(t[1],t[0])[0]*sub(t[2],t[0])[2],sub(t[1],t[0])[0]*sub(t[2],t[0])[1]-sub(t[1],t[0])[1]*sub(t[2],t[0])[0]))) for t in patches)/2
   assert area>.002,('Finite actual ground area missing',name,area)
  else:area=None
  pieces.append({'mesh':name,'depth_m':p['depth_m'],'flat_slice':p['pose']['flat'],'actual_ground_area_m2':area,'maximum_actual_raw_position_error_m':max_error,'unique_bijective_surface_match':True,'true_closed_shell':True})
  for cap in p['caps']:
   y=cap['local_y_m'];surface=[v for v in local if abs(v[1]-y)<3e-6];assert len(surface)>=2*N,('Actual cut face or adjacent crust border missing',name)
   cap_rows.append({'mesh':name,'side':cap['side'],'true_shared_surface_crust_ring':True,'actual_cut_surface_plane_vertices':len(surface),'shallow_geometry_dimples':len(cap['pore_centre_indices']),'declared_dimple_depth_m':cap['dimple_depth_m']})
 return {'single_prop_count':1,'remaining_loaf_count':1,'thick_separate_slice_count':3,'same_section_profile_vertices':N,'all_surfaces_match_real_mesh':True,'pieces':pieces,'cut_surfaces':cap_rows,'no_texture_or_floating_cut_face_insert':True,'no_edibility_or_cutting_physics_claim':True}
FOCUS=(0,0,.060);ORTHO=.515
CAMERAS={'gray-front3q':(.9,-1.35,1.02),'gray-back3q':(-.9,1.35,1.02),'thumbnail':(.9,-1.35,1.02),'qa-front':(0,-1.5,.58),'qa-side':(1.5,0,.62),'qa-top':(0,0,1.8),'qa-back':(0,1.5,.58),'qa-wireframe':(.9,-1.35,1.02),'silhouette-128-front':(0,-1.5,.58),'silhouette-128-side':(1.5,0,.62)}
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
root=bpy.data.objects.new('OneSlicedSandwichLoafKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
loaf_evidence=dict(measure_loaf_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts},{o.name:[[tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices] for t in o.data.loop_triangles] for o in parts}),material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'loaf_geometry':loaf_evidence,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/bakery/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'bakery','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
