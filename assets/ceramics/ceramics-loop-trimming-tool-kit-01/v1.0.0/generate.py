"""Original pottery loop-trimming kit: three differentiated tools, one static prop.
Metres, native Z up, blades toward -Y. Not a functional or certified cutting tool.
Self-contained source; exported GLB is reimported and compared before any rendering.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='ceramics-loop-trimming-tool-kit-01';VERSION='1.0.0';TITLE='Pottery Loop Trimming Tool Kit'
DESCRIPTION=('One original static pottery trimming tool kit counted as one prop, not three new models. '
 'A circular loop, triangular loop and asymmetric curved kidney scraper each have a genuine cut-through opening, '
 'a closed thick ribbon blade, a bent solid metal tang, a hollow stepped ferrule and an individual turned walnut handle. '
 'The ferrule has a narrow tang bore and a wider handle socket; actual interior witnesses connect the blade, tang, collar and wood. '
 'Flat lower blade surfaces and finite flat grip facets rest on the ground in this one arranged display pose. '
 'Twelve named editable closed meshes use walnut, dark walnut, warm brass and pale steel constant solid PBR materials. '
 'Source Z up, metres, ground-centre origin, blade direction -Y; no external textures or separate display stand. '
 'Static stylized game visual only: no sharpness, cutting performance, grip ergonomics, material certification or real-world tool safety claim.')
G={};LINKS=[];CONTACTS=[];SPINES={};FEET=[];OPENINGS=[];FERRULE_BORES=[];TOOLSETS=[]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def length(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/length(a))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 return name
def link(a,b,p,axis=(1,0,0),spread=.0006):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def prism_x(name,x0,x1,outline,mat,role):
 n=len(outline);vs=[(x,y,z) for x in [x0,x1] for y,z in outline]
 # Concave outline faces are triangulated by Blender, not assumed to be convex fans.
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def signed_area(p):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2

def inset(p,d):
 if signed_area(p)<0:p=list(reversed(p))
 out=[]
 for k,b in enumerate(p):
  a=p[k-1];c=p[(k+1)%len(p)];u=(b[0]-a[0],b[1]-a[1]);v=(c[0]-b[0],c[1]-b[1]);lu=math.hypot(*u);lv=math.hypot(*v);u=(u[0]/lu,u[1]/lu);v=(v[0]/lv,v[1]/lv)
  nu=(-u[1],u[0]);nv=(-v[1],v[0]);den=1+nu[0]*nv[0]+nu[1]*nv[1];assert den>.01
  out.append((b[0]+d*(nu[0]+nv[0])/den,b[1]+d*(nu[1]+nv[1])/den))
 return p,out

def ribbon(name,x,outline,width):
 outer,inner=inset(outline,width);n=len(outer)
 vs=[(x+xx,y,z) for z in [0,.005] for row in [outer,inner] for xx,y in row];fs=[]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),
             (i,n+i,n+j,j),(2*n+i,2*n+j,3*n+j,3*n+i)])
 mesh(name,vs,fs,3,'closed five-millimetre-thick ribbon blade with an actual empty central opening')
 FEET.append(name)
 return outer,inner

def smooth_closed(points,steps=4):
 out=[];n=len(points)
 for i in range(n):
  p0,p1,p2,p3=[points[k%n] for k in [i-1,i,i+1,i+2]]
  for j in range(steps):
   t=j/steps
   out.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in range(2)))
 return out

def handle(name,x):
 n=12;stations=[(.015,.0092),(.028,.0100),(.046,.0140),(.133,.0140),(.157,.0110),(.173,.0065)];vs=[]
 for y,r in stations:
  for i in range(n):
   a=math.pi/n+math.tau*i/n
   vs.append((x+r*math.sin(a),y,.014+r/math.cos(math.pi/n)*math.cos(a)))
 fs=[tuple(reversed(range(n)))];fm=[1]
 for k in range(len(stations)-1):
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i));fm.append(1 if i in [1,2,7,8] else 0)
 off=(len(stations)-1)*n;fs.append(tuple(off+i for i in range(n)));fm.append(1)
 mesh(name,vs,fs,0,'turned tapered walnut grip with a finite flat polygonal resting facet');G[name]['face_materials']=fm;FEET.append(name)

def ferrule(name,x):
 # Closed annular meridian: outer sleeve, rear socket, front shoulder and smaller tang bore.
 profile=[(.009,.0115),(.031,.0115),(.031,.0088),(.014,.0088),(.014,.0033),(.009,.0033)];n=24
 vs=[(x+r*math.cos(math.tau*i/n),y,.014+r*math.sin(math.tau*i/n)) for y,r in profile for i in range(n)];fs=[]
 for k in range(len(profile)):
  l=(k+1)%len(profile)
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,l*n+j,l*n+i))
 mesh(name,vs,fs,2,'hollow stepped brass ferrule with a wide handle socket and a narrower tang bore')
 FERRULE_BORES.append({'mesh':name,'origin_m':[x,.007,.014],'direction':[0,1,0],'length_m':.026,'scope':'collar-only bore topology; installed tang and handle intentionally occupy the bore'})

ROUND=[(.033*math.cos(math.tau*i/40),-.0655+.033*math.sin(math.tau*i/40)) for i in range(40)]
TRIANGLE=[(0,-.0315),(-.035,-.1015),(.035,-.1015)]
CURVE=smooth_closed([(0,-.0315),(-.012,-.040),(-.019,-.055),(-.020,-.070),(-.012,-.087),(.006,-.103),(.026,-.108),(.037,-.103),(.039,-.094),(.035,-.084),(.023,-.075),(.012,-.065),(.007,-.049)])
CONFIGS=[('Round',-.090,ROUND,(0,-.0655),-.0345),('Triangle',0,TRIANGLE,(0,-.075),-.0368),('Curved',.090,CURVE,(.001,-.080),-.0368)]
for kind,x,outline,hole,joint_y in CONFIGS:
 p='Tool_'+kind+'_';blade=p+'LoopBlade';tang=p+'BentTang';collar=p+'Ferrule';grip=p+'WalnutGrip'
 outer,inner=ribbon(blade,x,outline,.0045);handle(grip,x);ferrule(collar,x)
 # The thin tang is vertically inset into the ribbon root, avoiding coincident exposed faces.
 ys=[-.0378,-.027,-.007,.026];zs=[.0025,.0025,.014,.014]
 poly=[(y,z-.0018) for y,z in zip(ys,zs)]+[(y,z+.0018) for y,z in reversed(list(zip(ys,zs)))]
 prism_x(tang,x-.0042,x+.0042,poly,3,'solid bent tang embedded in the blade root and inside the handle/ferrule assembly')
 link(blade,tang,(x,joint_y,.0025),spread=.0005)
 link(tang,grip,(x,.022,.014),axis=(0,1,0),spread=.001)
 link(tang,collar,(x+.0038,.0115,.014),axis=(0,1,0),spread=.001)
 link(collar,grip,(x+.0092,.027,.014),axis=(0,1,0),spread=.0008)
 cx,cy=hole
 OPENINGS.append({'tool':kind,'blade':blade,'centre_xy_m':[x+cx,cy],'probe_offsets_m':[[0,0],[-.004,0],[.004,0],[0,-.004],[0,.004]],'z_interval_m':[-.010,.020],
 'description':'five finite clear rays through the complete installed tool set, plus measured in-plane opening span'})
 TOOLSETS.append({'kind':kind,'centre_x_m':x,'meshes':[blade,tang,collar,grip],'blade_outer_xy_m':[[x+a,b] for a,b in outer],'blade_inner_xy_m':[[x+a,b] for a,b in inner]})
# Exact horizontal bounds centre is the source origin; all witnesses move with geometry.
allvs=[v for g in G.values() for v in g['vertices']];SHIFT=tuple(-(min(v[i] for v in allvs)+max(v[i] for v in allvs))/2 if i<2 else 0 for i in range(3))
for g in G.values():g['vertices']=[tuple(round(c,6) for c in add(v,SHIFT)) for v in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT) for p in ps]) for a,b,ps in LINKS]
for o in OPENINGS:o['centre_xy_m']=[o['centre_xy_m'][i]+SHIFT[i] for i in [0,1]]
for o in FERRULE_BORES:o['origin_m']=list(add(o['origin_m'],SHIFT))
for t in TOOLSETS:
 t['centre_x_m']+=SHIFT[0]
 for key in ['blade_outer_xy_m','blade_inner_xy_m']:t[key]=[[p[i]+SHIFT[i] for i in [0,1]] for p in t[key]]
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
for name,color,rough,metal in [('Walnut_Main',(.30,.135,.047,1),.67,.02),('Walnut_Facets',(.20,.075,.022,1),.73,.01),('WarmBrass_Ferrules',(.48,.30,.11,1),.39,.68),('PaleSteel_BladesAndTangs',(.49,.57,.60,1),.37,.78)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('OnePotteryTrimmingToolKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
opening_checks=[]
for r in OPENINGS:
 rays=[];cx,cy=r['centre_xy_m'];z0,z1=r['z_interval_m']
 for dx,dy in r['probe_offsets_m']:
  origin=Vector((cx+dx,cy+dy,z0));direction=Vector((0,0,1));distance=z1-z0
  blockers=[n for n,t in trees.items() if t.ray_cast(origin,direction,distance)[0] is not None]
  assert not blockers,('Blocked blade opening',r['tool'],dx,dy,blockers)
  rays.append({'origin_m':list(origin),'direction':[0,0,1],'length_m':distance,'blockers':blockers})
 spans=[]
 for axis in [(1,0,0),(0,1,0)]:
  origin=Vector((cx,cy,.0025));positive=trees[r['blade']].ray_cast(origin,Vector(axis),.2)[0];negative=trees[r['blade']].ray_cast(origin,-Vector(axis),.2)[0]
  assert positive is not None and negative is not None
  span=(positive-negative).length;assert span>.012,(r['tool'],axis,span)
  spans.append({'axis':axis,'negative_hit_m':list(negative),'positive_hit_m':list(positive),'opening_span_m':span})
 opening_checks.append(dict(r,actual_clear_rays=rays,actual_inner_surface_spans=spans))
bore_checks=[]
for r in FERRULE_BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Ferrule bore capped',r)
 bore_checks.append(dict(r,actual_collar_only_ray_clear=True))
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
 'single_kit_prop_count':1,'distinct_tools':TOOLSETS,'actual_loop_openings':opening_checks,'actual_hollow_ferrule_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/ceramics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'ceramics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.014));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.375;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3,-4,9),'gray-back3q':(-3,4,9)} if gray else {
 'thumbnail':(3,-4,9),'qa-front':(0,-7,.014),'qa-side':(7,0,.014),'qa-top':(0,0,8),
 'qa-back':(0,7,.014),'qa-wireframe':(3,-4,9)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.375
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00012;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.014)),('silhouette-128-side',(7,0,.014))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
