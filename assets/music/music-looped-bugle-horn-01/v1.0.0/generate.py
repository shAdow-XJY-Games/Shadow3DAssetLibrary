"""Original hollow looped valveless bugle. One static stylized visual prop.
Metres, source Z up, front -Y, finite flat tube contacts at Z=0.
Complete outer/inner wall geometry; no textures, external fonts or acoustic claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='music-looped-bugle-horn-01';VERSION='1.0.0';TITLE='Hollow Looped Brass Bugle'
DESCRIPTION=('One original static stylized valveless brass bugle with a long hollow return tube, a gradually flared open bell, a separately editable hollow cup mouthpiece and two small fixed connecting stays. '
 'The entire curved tube and bell have continuous true inner and outer wall geometry; both end apertures and the assembled passage remain open. No black cavity disks or solid curved rods are used. '
 'The long U-return layout is an original authored instrument silhouette. It rests in one fixed low horizontal pose on finite flat facets of its main tube and bell, without a stand, case, player or spare components. '
 'Four closed editable meshes, constant solid PBR materials, metre scale, source Z up, front -Y and ground-centre origin. '
 'Static visual prop only: no sound, acoustic pitch, musical tuning, playability, real instrument scale, breath flow simulation, performance, ergonomic fit, manufacture, structural stability guarantee, certification or animation.')
G={};LINKS=[];FEET=['Tube_ContinuousReturnAndBell'];BORES=[];GAPS=[];VOID_VOLUMES={};VOID_CENTRES={};WALL_PROBES=[]
PALETTE=[('Brass_WarmBody',(.58,.32,.075,1),.34,.72),('Brass_InnerGold',(.42,.205,.045,1),.40,.63),('Mouthpiece_SatinSilver',(.60,.64,.62,1),.30,.75),('Stays_DarkerBrass',(.37,.22,.065,1),.42,.65)]
N=16;C=math.cos(math.pi/N);R=.030;RI=.022;Z=R*C

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name

def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size
 vs=[(x+a*w/2,y+b*d/2,z+c*h/2) for c in [-1,1] for b in [-1,1] for a in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def empty_box(name,c,size,role):
 temp='PROBE_'+name;box(temp,c,size,0,role);VOID_VOLUMES[name]=G.pop(temp);VOID_CENTRES[name]=c

def rod(name,a,b,r,mat,role,n=12):
 delta=[b[i]-a[i] for i in range(3)];L=math.sqrt(sum(t*t for t in delta));w=[t/L for t in delta];tmp=[0,0,1]
 u=[w[1]*tmp[2]-w[2]*tmp[1],w[2]*tmp[0]-w[0]*tmp[2],w[0]*tmp[1]-w[1]*tmp[0]];l=math.sqrt(sum(t*t for t in u));u=[t/l for t in u]
 v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[j]+r*(u[j]*math.cos(math.tau*i/n)+v[j]*math.sin(math.tau*i/n)) for j in range(3)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
# Each station stores centre, in-plane radial direction, outer and inner radius.
# Two matching polygonal shells plus annular end rims create one material solid.
# This is true hollow mesh construction, with no Boolean or end-cap disk.
def hollow(name,stations,mat,inner,role,n=N):
 vs=[];fs=[];fm=[];L=len(stations)
 for c,u,ro,ri in stations:
  for radius in [ro,ri]:
   for j in range(n):
    a=math.tau*j/n+math.pi/n
    vs.append((c[0]+u[0]*radius*math.cos(a),c[1]+u[1]*radius*math.cos(a),c[2]+radius*math.sin(a)))
 for i in range(L-1):
  for j in range(n):
   k=(j+1)%n;a=i*2*n+j;b=i*2*n+k;d=(i+1)*2*n+j;e=(i+1)*2*n+k
   fs.extend([(a,b,e,d),(a+n,d+n,e+n,b+n)]);fm.extend([mat,inner])
 for i in [0,L-1]:
  for j in range(n):
   k=(j+1)%n;fs.append((i*2*n+j,i*2*n+k,i*2*n+k+n,i*2*n+j+n));fm.append(mat)
 mesh(name,vs,fs,mat,role);G[name]['face_materials']=fm

def solid_sweep_probe(name,stations,r=.010,n=8):
 vs=[];fs=[]
 for c,u,ro,ri in stations:
  for j in range(n):
   a=math.tau*j/n+math.pi/n;vs.append((c[0]+u[0]*r*math.cos(a),c[1]+u[1]*r*math.cos(a),c[2]+r*math.sin(a)))
 for i in range(len(stations)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.extend([tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]);temp='PROBE_'+name
 mesh(temp,vs,fs,0,'continuous complete conservative inner-channel clearance volume, from outside mouthpiece through return bend to outside bell');VOID_VOLUMES[name]=G.pop(temp);VOID_CENTRES[name]=stations[len(stations)//2][0]
# Upper neck starts at +X. It returns around the left semicircle then extends
# along the lower branch into an up-offset flared bell. Bottom facets are flat.
STATIONS=[]
for x,z in [(.440,.041),(.300,.041),(.100,.034),(-.100,Z),(-.300,Z)]:STATIONS.append(((x,.170,z),(0,1,0),R,RI))
for i in range(1,25):
 a=math.pi/2+math.pi*i/24
 STATIONS.append(((-.300+.170*math.cos(a),.170*math.sin(a),Z),(math.cos(a),math.sin(a),0),R,RI))
for x in [-.100,.100,.180]:STATIONS.append(((x,-.170,Z),(0,-1,0),R,RI))
for x,ro in [(.260,.032),(.330,.038),(.395,.048),(.455,.063),(.510,.083),(.560,.106),(.605,.132),(.625,.136),(.635,.136)]:
 STATIONS.append(((x,-.170,ro*C),(0,-1,0),ro,ro-.008))
hollow('Tube_ContinuousReturnAndBell',STATIONS,0,1,'single continuous thick hollow U-return tube and gradually widening bell; true inner shell, outer shell and annular end rims')
MOUTH_STATIONS=[((x,.170,.041),(0,1,0),ro,ri) for x,ro,ri in [(.412,.034,.025),(.445,.034,.025),(.475,.031,.023),(.500,.032,.024),(.535,.038,.030),(.555,.040,.032),(.570,.040,.032),(.578,.038,.030)]]
hollow('Mouthpiece_HollowCup',MOUTH_STATIONS,2,2,'separate thick open mouthpiece sleeve and shallow cup, positively seated around the open upper neck')
# Three interior annular witnesses are on the neck/sleeve's shared brass volume.
link('Mouthpiece_HollowCup','Tube_ContinuousReturnAndBell',(.427,.197,.041),axis=(1,0,0),spread=.006)
# Connecting stays end inside the inward tube walls, without plugging the bore.
for x,label in [(-.100,'Rear'),(.100,'Front')]:
 upperz=Z if x<0 else .034
 a=(x,-.145,Z);b=(x,.145,upperz)
 name='Stay_'+label;rod(name,a,b,.006,3,'small fixed closed connecting stay with finite seats in both inward tube walls; no valves or accessory count')
 link(name,'Tube_ContinuousReturnAndBell',(x,-.144,Z),spread=.002)
 link(name,'Tube_ContinuousReturnAndBell',(x,.144,upperz),spread=.002)
# Complete through-channel probe extends beyond both apertures. Its narrow
# conservative core establishes continuity through every station and join.
channel=[((.600,.170,.041),(0,1,0),R,RI)]+[(c,u,ro,ri) for c,u,ro,ri in reversed(MOUTH_STATIONS) if c[0]>.440]+STATIONS+[((.660,-.170,.136*C),(0,-1,0),.136,.128)]
solid_sweep_probe('FullMouthToBellChannel',channel)
empty_box('BetweenBranches_Left',(-.235,0,Z),(.100,.250,.040),'full finite gap between both branches to the left of the rear stay')
empty_box('BetweenStays',(0,0,Z),(.170,.250,.038),'full finite central open frame between the two stays and both tube branches')
empty_box('BetweenBranches_Right',(.215,0,.048),(.160,.230,.050),'full finite gap between neck and flaring branch, beyond the front stay')
# Aperture rays include centre and four offsets. They span the end and interior.
for name,meshname,x,y,z,sgn,length in [('Mouth','Mouthpiece_HollowCup',.600,.170,.041,-1,.180),('Bell','Tube_ContinuousReturnAndBell',.660,-.170,.136*C,-1,.030)]:
 for dy,dz in [(0,0),(.008,0),(-.008,0),(0,.008),(0,-.008)]:
  r={'label':name+'_open_'+str((dy,dz)),'origin_m':[x,y+dy,z+dz],'direction':[sgn,0,0],'length_m':length};GAPS.append(r);BORES.append(dict(r,mesh=meshname))
# Every axial segment is sampled at its midpoint in both +/-Z wall directions.
# This crosses the actual inner and outer polygonal wall, not metadata radii.
for part,stations in [('Tube_ContinuousReturnAndBell',STATIONS),('Mouthpiece_HollowCup',MOUTH_STATIONS)]:
 for i,(a,b) in enumerate(zip(stations,stations[1:])):
  centre=tuple((a[0][k]+b[0][k])/2 for k in range(3));ri=(a[3]+b[3])/2;ro=(a[2]+b[2])/2
  for sign in [-1,1]:WALL_PROBES.append({'mesh':part,'label':str(i)+'_'+str(sign),'origin_m':centre,'direction':[0,0,sign],'length_m':ro+.002,'expected_hits_m':[ri*C,ro*C]})
# Centre the complete asset's ground envelope at the root origin. The same
# translation is applied to every mesh, probe, station and interior witness.
vv=[v for g in G.values() for v in g['vertices']];PIVOT=((min(v[0] for v in vv)+max(v[0] for v in vv))/2,(min(v[1] for v in vv)+max(v[1] for v in vv))/2,0)
def recenter(v):return tuple(round(v[i]-PIVOT[i],7) for i in range(3))
for g in list(G.values())+list(VOID_VOLUMES.values()):g['vertices']=[recenter(v) for v in g['vertices']]
LINKS=[(a,b,[recenter(p) for p in ps]) for a,b,ps in LINKS]
VOID_CENTRES={n:recenter(p) for n,p in VOID_CENTRES.items()}
for r in BORES+GAPS+WALL_PROBES:r['origin_m']=recenter(r['origin_m'])
STATIONS=[(recenter(c),u,ro,ri) for c,u,ro,ri in STATIONS]
MOUTH_STATIONS=[(recenter(c),u,ro,ri) for c,u,ro,ri in MOUTH_STATIONS]
HORN_SPEC={'main_stations':STATIONS,'mouthpiece_stations':MOUTH_STATIONS,'radial_sides':N,'hollow_parts':['Tube_ContinuousReturnAndBell','Mouthpiece_HollowCup'],'wall_probe_count':len(WALL_PROBES),'finite_return_radius_m':.170,'static_visual_only':True,'acoustic_or_playability_claim':False}
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
root=bpy.data.objects.new('OneHollowLoopedBugle',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual imported/generated triangle wall probes and source station evidence.
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);hits=[];travel=0.0
 for _ in range(4):
  q,_,_,dist=trees[r['mesh']].ray_cast(p,d,r['length_m']-travel)
  if q is None:break
  absolute=travel+dist;hits.append(absolute);p=q+d*1e-6;travel=absolute+1e-6
 assert len(hits)==2 and all(abs(hits[i]-r['expected_hits_m'][i])<2e-6 for i in range(2)),('wall thickness',r,hits)
 wall_checks.append(dict(r,actual_hits_m=hits,actual_thickness_m=hits[1]-hits[0]))
horn_evidence=dict(HORN_SPEC,actual_wall_probes=wall_checks,finite_void_volumes=VOID_VOLUMES,finite_volume_empty_checks=void_volume_checks)

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
 'single_prop_count':1,'horn_geometry':horn_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/music/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.090));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.42;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-5,4.5),'gray-back3q':(-4,5,4.5)} if gray else {
 'thumbnail':(4,-5,4.5),'qa-front':(0,-7,.090),'qa-side':(7,0,.090),'qa-top':(0,0,8),
 'qa-back':(0,7,.090),'qa-wireframe':(4,-5,4.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.42
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0022;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.090)),('silhouette-128-side',(7,0,.090))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
