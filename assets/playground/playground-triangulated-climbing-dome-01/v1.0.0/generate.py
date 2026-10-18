"""Original static triangulated low dome. Metres, Z up. No climbing or safety claim."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='playground-triangulated-climbing-dome-01';VERSION='1.0.0';TITLE='Triangulated Low Climbing Dome'
DESCRIPTION=('One original fixed low dome visual prop, built from three staggered eight-node rings, a crown node and 64 individually connected rods around 40 genuinely open triangular windows. '
 'Twenty-five faceted junction nodes and eight finite stepped ground feet create a complete connected support graph. Each trimmed rod end enters its own node, while separate rods remain separated. '
 'No platform, floor, solid roof, slide, swing, person, mat or scene. Separate closed editable meshes, four solid PBR materials, no textures or external dependencies. Metres, Z up, ground-centre origin. One complete dome counts as one prop. '
 'Only this fixed visual geometry is checked. No climbability, interaction, human fit, child age suitability, load bearing, fall zone, entrapment protection, anchoring, wind resistance, engineering, installation or playground/child safety certification is claimed.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};NODES={};STRUTS=[];WINDOWS=[]
PALETTE=[('Rod_DeepTeal',(.035,.27,.29,1),.46,.28),('Rod_Seafoam',(.32,.61,.54,1),.49,.20),('Node_WarmOchre',(.89,.48,.10,1),.47,.18),('Foot_Graphite',(.050,.065,.068,1),.79,.05)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def basis(axis):
 a=unit(axis);u=unit(cross(a,(0,0,1) if abs(a[2])<.9 else (0,1,0)));v=cross(a,u);return a,u,v
def profile(name,origin,axis,rings,mat,role,n=12):
 a,u,v=basis(axis);vs=[];fs=[]
 for t,r in rings:
  for i in range(n):q=math.tau*i/n;vs.append(add(add(origin,mul(a,t)),add(mul(u,r*math.cos(q)),mul(v,r*math.sin(q)))))
 for j in range(len(rings)-1):
  for i in range(n):k=(i+1)%n;fs.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
def box(name,c,size,mat,role,axes=((1,0,0),(0,1,0),(0,0,1))):
 vs=[]
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
  vs.append(add(c,add(mul(axes[0],x*size[0]/2),add(mul(axes[1],y*size[1]/2),mul(axes[2],z*size[2]/2)))))
 return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,role)
def node(name,c,r=.083,n=12,lat=6):
 vs=[add(c,(0,0,-r))];fs=[]
 for j in range(1,lat):
  a=-math.pi/2+math.pi*j/lat
  for i in range(n):q=math.tau*i/n;vs.append(add(c,(r*math.cos(a)*math.cos(q),r*math.cos(a)*math.sin(q),r*math.sin(a))))
 top=len(vs);vs.append(add(c,(0,0,r)))
 for i in range(n):k=(i+1)%n;fs += [(0,1+k,1+i),(top,1+(lat-2)*n+i,1+(lat-2)*n+k)]
 for j in range(lat-2):
  for i in range(n):k=(i+1)%n;fs.append((1+j*n+i,1+j*n+k,1+(j+1)*n+k,1+(j+1)*n+i))
 NODES[name]=c;return mesh(name,vs,fs,2,'faceted solid node joining trimmed rods by positive volume')
# Three shrinking rings with alternating angular offset form a new low dome.
# The only ground contacts are eight broad stepped feet under the lowest nodes.
for j,(rad,z,offset) in enumerate([(1.60,.120,0),(1.36,.750,.5),(.72,1.300,0)]):
 for i in range(8):
  a=math.tau*(i+offset)/8;c=(rad*math.cos(a),rad*math.sin(a),z);n=f'Node_R{j}_{i:02d}';node(n,c)
  if j==0:
   foot=f'Foot_{i:02d}';profile(foot,(c[0],c[1],0),(0,0,1),[(0,.120),(.032,.120),(.046,.045),(.100,.045)],3,'finite 16-sided ground flange and integral node seating neck',n=16);FEET.append(foot)
   link(foot,n,(c[0],c[1],.082),(1,0,0),.004)
node('Node_Crown',(0,0,1.580))
def rn(j,i):return f'Node_R{j}_{i%8:02d}'
edges=set()
def edge(a,b):edges.add(tuple(sorted((a,b))))
def window(a,b,c):
 WINDOWS.append((a,b,c));edge(a,b);edge(b,c);edge(c,a)
for i in range(8):
 window(rn(0,i),rn(0,i+1),rn(1,i));window(rn(1,i-1),rn(1,i),rn(0,i))
 window(rn(1,i),rn(1,i+1),rn(2,i+1));window(rn(2,i),rn(2,i+1),rn(1,i))
 window(rn(2,i),rn(2,i+1),'Node_Crown')
for k,(a,b) in enumerate(sorted(edges)):
 p=NODES[a];q=NODES[b];axis=unit(sub(q,p));length=math.sqrt(dot(sub(q,p),sub(q,p)));name=f'Rod_{k:02d}'
 material=1 if ('R1' in a and 'R1' in b) or ('R2' in a and 'R2' in b) else 0
 profile(name,p,axis,[(.071,.0215),(length-.071,.0215)],material,'closed trimmed strut with both caps buried in their two solid junction nodes')
 link(name,a,add(p,mul(axis,.074)),axis,.001);link(name,b,add(q,mul(axis,-.074)),axis,.001)
 STRUTS.append({'name':name,'a':a,'b':b,'trim_m':.071,'radius_m':.0215})
# Full finite inset triangular prisms prove an open region in every triangle.
# These test-only meshes are removed before Blender/native/export.
for i,(a,b,c) in enumerate(WINDOWS):
 p,q,r=[NODES[n] for n in [a,b,c]];centre=mul(add(add(p,q),r),1/3);normal=unit(cross(sub(q,p),sub(r,p)));vs=[]
 for depth in [-.025,.025]:
  for v in [p,q,r]:vs.append(add(add(centre,mul(sub(v,centre),.58)),mul(normal,depth)))
 name=f'Empty_Window_{i:02d}';mesh(name,vs,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],0,'test-only finite inset triangular opening volume');VOID_VOLUMES[name]=G.pop(name)
 GAPS.append({'name':name,'origin_m':add(centre,mul(normal,-.10)),'direction':normal,'length_m':.20})
box('Empty_CentralInterior',(0,0,.41),(1.70,1.70,.56),0,'test-only interior void, verifies absence of an unclaimed floor or platform');VOID_VOLUMES['Empty_CentralInterior']=G.pop('Empty_CentralInterior')

def measure_dome_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 def center(name):
  vs=vertices[name];return tuple(sum(float(p[i]) for p in vs)/len(vs) for i in range(3))
 centres={n:center(n) for n in NODES};ring_rows=[]
 for j,(rad,z,offset) in enumerate([(1.60,.120,0),(1.36,.750,.5),(.72,1.300,0)]):
  for i in range(8):
   name=rn(j,i);c=centres[name];ang=math.tau*(i+offset)/8;expected=(rad*math.cos(ang),rad*math.sin(ang),z)
   assert math.sqrt(dot(sub(c,expected),sub(c,expected)))<2e-6,('Node displaced',name,c)
  ring_rows.append({'ring':j,'nodes':8,'actual_mean_radius_m':sum(math.hypot(*centres[rn(j,i)][:2]) for i in range(8))/8,'actual_mean_height_m':sum(centres[rn(j,i)][2] for i in range(8))/8,'angle_offset_degrees':offset*45})
 assert math.dist(centres['Node_Crown'],(0,0,1.58))<2e-6
 rods=[]
 for r in STRUTS:
  p=centres[r['a']];q=centres[r['b']];axis=unit(sub(q,p));length=math.dist(p,q);vs=[tuple(float(c) for c in v) for v in vertices[r['name']]];ts=[dot(sub(v,p),axis) for v in vs];low=min(ts);high=max(ts)
  ends=[]
  for t in [low,high]:
   ev=[v for v,tt in zip(vs,ts) if abs(tt-t)<2e-6];assert len(ev)==12
   ends.append(tuple(sum(v[i] for v in ev)/len(ev) for i in range(3)))
  assert math.dist(ends[0],add(p,mul(axis,.071)))<2e-6 and math.dist(ends[1],add(q,mul(axis,-.071)))<2e-6,('Rod endpoint detached',r['name'])
  radii=[math.sqrt(max(0,dot(sub(v,p),sub(v,p))-t*t)) for v,t in zip(vs,ts)]
  assert max(abs(rr-.0215) for rr in radii)<2e-6,('Rod radius changed',r['name'])
  rods.append({'name':r['name'],'actual_node_span_m':length,'actual_trim_start_m':low,'actual_trim_end_m':length-high,'actual_radius_m':sum(radii)/len(radii)})
 assert len(centres)==25 and len(STRUTS)==64 and len(WINDOWS)==40
 return {'counted_props':1,'node_count':len(centres),'rod_count':len(rods),'finite_foot_count':len(FEET),'triangular_window_count':len(WINDOWS),'actual_node_rings':ring_rows,'actual_rods':rods,'fixed_visual_geometry_only':True,'climbability_or_child_safety_claimed':False}

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
root=bpy.data.objects.new('OneStaticTriangulatedDome',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_dome_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'triangulated_dome_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.75));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=4.05;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-4.8,-7.0,4.1),'gray-back3q':(4.8,7.0,4.1)} if gray else {
 'thumbnail':(-4.8,-7.0,4.1),'qa-front':(0,-7,.75),'qa-side':(7,0,.75),'qa-top':(0,0,8),
 'qa-back':(0,7,.75),'qa-wireframe':(-4.8,-7.0,4.1)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=4.05
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0051;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.75)),('silhouette-128-side',(7,0,.75))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
