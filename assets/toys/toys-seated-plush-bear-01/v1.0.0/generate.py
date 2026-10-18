"""Original short-ear seated fabric bear. One static prop, metres, Z up, front -Y.
New body, head, arms, feet and integral indented seam recipes; no old cushion geometry.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='toys-seated-plush-bear-01';VERSION='1.0.0';TITLE='Short-Ear Seated Plush Bear'
DESCRIPTION=('One original static short-ear seated fabric bear with a pear-shaped padded torso, broad distinct head, two short round ears, two gently hanging short arms and two forward resting feet. '
 'A real indented front belly-panel boundary and sagittal head and muzzle seams are sculpted into the continuous closed surfaces, not overlaid coplanar patches or painted dark lines. The cream belly and ear inset regions use constant face materials on those same closed meshes. '
 'Twelve named editable closed meshes, three constant opaque rough PBR materials, metres, source Z up, front -Y and fixed design origin on the X midline, torso-design Y=0 and ground Z=0. Butt and both feet have finite flat resting patches. Face, ears and limbs have finite body-rooted connections. No textures, fur, labels, logos, recognizable branded character, clothing, extra toys, base plinth or surrounding scene. '
 'A fixed fictional visual prop only. No animation, cloth or stuffing simulation, material or seam strength, load, pose stability, manufacturing, playability, age suitability, swallowing-risk assessment, child safety or toy certification is modeled or guaranteed.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={};SEAM_PROBES=[];LOFT_LAYOUT={}
PALETTE=[('Fabric_Cinnamon',(.38,.18,.085,1),.93,0),('Fabric_WarmOat',(.72,.57,.36,1),.96,0),('Face_Espresso',(.035,.020,.013,1),.82,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'seams':'real continuous inward vertex displacement','no_cloth_simulation_or_toy_safety_claim':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name

def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def void(name,lo,hi,role):
 vs=[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
 VOID_VOLUMES[name]={'vertices':vs,'faces':BOX_FACES,'role':role}
def angular_distance(a,b):return abs((a-b+math.pi)%math.tau-math.pi)
def loft(name,rings,material,role,c=(0,0,0),u=(1,0,0),v=(0,1,0),w=(0,0,1),n=28,seams=(),seam_depth=.004,panel=None):
 # Rings: (height, radius_x, radius_y, center_y). Singular end rings are actual poles.
 angles=sorted(set([round(math.tau*i/n,10) for i in range(n)]+[round((s+d)%math.tau,10) for s in seams for d in [-.055,0,.055]]));N=len(angles)
 vs=[];idx=[];fs=[];fm=[]
 for k,(z,rx,ry,cy) in enumerate(rings):
  if rx==0:idx.append([len(vs)]);vs.append(transform((0,cy,z),c,u,v,w));continue
  ring=[]
  for theta in angles:
   delta=min([angular_distance(theta,s) for s in seams] or [10]);depth=seam_depth*max(0,1-delta/.055)
   # The belly piece has a truly recessed four-sided boundary in this same mesh.
   if panel and panel['zlo']-1e-8<=z<=panel['zhi']+1e-8 and panel['amin']-1e-8<=theta<=panel['amax']+1e-8:
    if abs(z-panel['zlo'])<1e-8 or abs(z-panel['zhi'])<1e-8:depth=max(depth,seam_depth)
   p=((rx-depth)*math.cos(theta),(ry-depth)*math.sin(theta)+cy,z)
   ring.append(len(vs));vs.append(transform(p,c,u,v,w))
  idx.append(ring)
 for k,(a,b) in enumerate(zip(idx,idx[1:])):
  for i in range(N):
   j=(i+1)%N
   if len(a)==1:faces=[(a[0],b[j],b[i])]
   elif len(b)==1:faces=[(a[i],a[j],b[0])]
   else:faces=[(a[i],a[j],b[j]),(a[i],b[j],b[i])]
   theta=(angles[i]+(angles[j] if j else math.tau))/2;z=(rings[k][0]+rings[k+1][0])/2
   mat=material
   if panel and panel['zlo']<z<panel['zhi'] and panel['amin']<theta<panel['amax']:mat=panel['material']
   fs.extend(faces);fm.extend([mat]*len(faces))
 LOFT_LAYOUT[name]={'angles':angles,'rings':idx}
 return mesh(name,vs,fs,material,role,fm)
def ellipsoid(name,c,r,material,role,n=28,steps=14,seams=(),depth=.003,u=(1,0,0),v=(0,1,0),w=(0,0,1),panel=None):
 rings=[]
 for k in range(steps+1):
  a=-math.pi/2+math.pi*k/steps;scale=math.cos(a) if k not in [0,steps] else 0
  rings.append((r[2]*math.sin(a),r[0]*scale,r[1]*scale,0))
 return loft(name,rings,material,role,c,u,v,w,n,seams,depth,panel)
# Custom pear outline: finite butt contact, expanded lower belly, narrow padded shoulders.
body_rings=[(0,0,0,.015),(0,.100,.081,.015),(.026,.149,.108,.014),(.065,.178,.129,.012),(.100,.190,.140,.010),(.105,.191,.141,.010),(.110,.192,.142,.010),(.180,.190,.140,.008),(.250,.169,.123,.006),(.290,.148,.108,.004),(.295,.145,.106,.004),(.300,.142,.104,.004),(.335,.119,.089,.002),(.367,.065,.052,0),(.379,0,0,0)]
panel={'zlo':.105,'zhi':.295,'amin':math.radians(230),'amax':math.radians(310),'material':1}
BODY=loft('Body_PearStuffedTorso',body_rings,0,'new pear-shaped stuffed torso with real indented belly-panel boundary and finite flat seated butt',n=36,seams=(panel['amin'],panel['amax']),seam_depth=.0045,panel=panel);FEET.append(BODY)
HEAD=ellipsoid('Head_BroadSoftRound',(0,-.005,.503),(.171,.143,.155),0,'broad distinct padded head with actual sagittal recessed seam, finitely rooted in shoulders',n=32,steps=16,seams=(math.pi/2,3*math.pi/2),depth=.0035)
link(HEAD,BODY,(0,0,.361),axis=(1,0,0),spread=.010)
# Soft short round ears are tilted only by the natural head contour, never thin discs.
EARS=[];ARMS=[];PAWS=[];EYES=[]
for label,sgn in [('Left',-1),('Right',1)]:
 ear='Ear_'+label+'_ShortRound'
 ear_panel={'zlo':-.055,'zhi':.055,'amin':math.radians(215),'amax':math.radians(325),'material':1}
 ellipsoid(ear,(sgn*.133,.003,.636),(.056,.038,.055),0,'short rounded ear with cream front region integral to its closed shell',n=24,steps=12,panel=ear_panel)
 link(ear,HEAD,(sgn*.118,.002,.610),axis=(0,1,0),spread=.005);EARS.append(ear)
 # Arm axis leans inward toward the shoulder; hand tips hang clear of both forward paws.
 w=unit((-sgn*.38,0,1));u=(w[2],0,-w[0]);v=(0,1,0)
 arm='Arm_'+label+'_SoftHanging'
 ellipsoid(arm,(sgn*.190,-.012,.256),(.060,.070,.123),0,'short hanging padded arm with finite upper shoulder seat and clear lower tip',n=24,steps=12,seams=(math.pi/2,),depth=.0028,u=u,v=v,w=w)
 link(arm,BODY,(sgn*.130,-.010,.300),axis=(0,1,0),spread=.007);ARMS.append(arm)
 # Both paws are original rounded soles with a broad finite ground cap and a tapered body seat.
 foot='Foot_'+label+'_ForwardFlatPaw'
 rings=[(0,0,0,0),(0,.066,.092,0),(.018,.091,.131,0),(.048,.105,.151,0),(.083,.102,.143,.008),(.115,.082,.113,.023),(.137,.049,.067,.041),(.148,0,0,.052)]
 loft(foot,rings,0,'forward resting padded foot with actual finite flat sole and finite rear body seat',c=(sgn*.123,-.142,0),n=28,seams=(math.pi/2,),seam_depth=.003)
 link(foot,BODY,(sgn*.105,-.079,.083),axis=(0,1,0),spread=.006);FEET.append(foot);PAWS.append(foot)
 eye='Eye_'+label+'_SoftOval'
 ellipsoid(eye,(sgn*.062,-.134,.547),(.012,.011,.014),2,'small rounded dark oval face detail with finite head overlap; no floating or texture eye',n=16,steps=10)
 link(eye,HEAD,(sgn*.062,-.128,.547),axis=(0,0,1),spread=.002);EYES.append(eye)
MUZZLE=ellipsoid('Muzzle_RoundedCreamSnout',(0,-.139,.466),(.092,.054,.065),1,'soft short cream muzzle with real vertical indented seam, finitely embedded into head',n=28,steps=14,seams=(3*math.pi/2,),depth=.0022)
link(MUZZLE,HEAD,(0,-.118,.468),axis=(1,0,0),spread=.013)
NOSE=ellipsoid('Nose_RoundedEspresso',(0,-.190,.486),(.025,.018,.019),2,'small rounded dark nose genuinely rooted in cream muzzle',n=20,steps=10)
link(NOSE,MUZZLE,(0,-.180,.486),axis=(1,0,0),spread=.004)
# Complete finite clear volumes between the paws and below free arm tips.
void('BetweenForwardPaws',(-.013,-.272,.018),(.013,-.185,.105),'finite visible air separating the two forward paws, entirely ahead of the torso')
for label,sgn in [('Left',-1),('Right',1)]:
 xa,xb=sorted((sgn*.220,sgn*.251));void('Under_'+label+'_Hand',(xa,-.025,.035),(xb,.025,.118),'finite air below the short hanging arm tip, outside the paws and torso')
# Direct shape witnesses for indented seam channels; each maps actual vertices in one closed surface.
for name,theta,z in [(BODY,panel['amin'],.180),(BODY,panel['amax'],.180),(HEAD,math.pi/2,.503),(HEAD,3*math.pi/2,.503),(MUZZLE,3*math.pi/2,.466)]:
 g=G[name];vs=g['vertices'];layout=LOFT_LAYOUT[name]
 ring=min((r for r in layout['rings'] if len(r)>1),key=lambda r:abs(vs[r[0]][2]-z))
 def index(theta):return ring[min(range(len(layout['angles'])),key=lambda i:angular_distance(layout['angles'][i],theta))]
 center=index(theta);before=index(theta-.055);after=index(theta+.055)
 cx,cy=(0,.008) if name==BODY else ((0,-.005) if name==HEAD else (0,-.139))
 SEAM_PROBES.append({'mesh':name,'centre_vertex':center,'left_bank_vertex':before,'right_bank_vertex':after,'local_center_xy':[cx,cy],'minimum_radial_indent_m':.0013})
PLUSH_CONTRACT={'single_prop_count':1,'body_mesh':BODY,'head_mesh':HEAD,'ear_meshes':EARS,'arm_meshes':ARMS,'foot_meshes':PAWS,'eye_meshes':EYES,'muzzle_mesh':MUZZLE,'nose_mesh':NOSE,'ground_meshes':FEET,'seam_probes':SEAM_PROBES,'original_anatomical_silhouette':True,'static_fictional_visual_only':True,'cloth_simulation_toy_age_safety_or_playability_claim':False}
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
root=bpy.data.objects.new('OneOriginalSeatedPlushBear',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X midline; torso-design Y=0; ground Z=0; not a bounds-centred origin';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Actual floor and wall tests supplement finite void and support tests.
floor_checks=[]
for r in FLOOR_PROBES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is not None and abs(hit.z-r['expected_hit_z_m'])<1e-6
 floor_checks.append(dict(r,actual_hit_m=list(hit)))
wall_checks=[]
for r in WALL_PROBES:
 p=Vector(r['origin_m']);d=Vector(r['direction']);t=trees[r['mesh']];inner=t.ray_cast(p,d,r['length_m'])[0]
 assert inner is not None
 outer=t.ray_cast(inner+d*1e-6,d,r['length_m'])[0];assert outer is not None
 thickness=(outer-inner).length;assert thickness>r['minimum_wall_thickness_m']
 wall_checks.append(dict(r,actual_inner_hit_m=list(inner),actual_outer_hit_m=list(outer),actual_wall_thickness_m=thickness))
seam_checks=[]
for r in SEAM_PROBES:
 o=byname[r['mesh']];cx,cy=r['local_center_xy']
 def radius(k):p=o.data.vertices[k].co;return math.hypot(p.x-cx,p.y-cy)
 depth=(radius(r['left_bank_vertex'])+radius(r['right_bank_vertex']))/2-radius(r['centre_vertex'])
 assert depth>r['minimum_radial_indent_m'],('Actual seam is not recessed',r,depth)
 seam_checks.append(dict(r,actual_vertex_radial_indent_m=depth))
plush_evidence=dict(PLUSH_CONTRACT,finite_empty_volume_checks=void_volume_checks,actual_shell_thickness_checks=wall_checks,material_contract=MATERIAL_CONTRACT,actual_recessed_seam_checks=seam_checks)
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
 'single_prop_count':1,'plush_geometry':plush_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'toys','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.025,.345));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.90;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-back-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-2.4,-4,2.05),'gray-back3q':(2.4,3.8,1.75)} if gray else {
 'thumbnail':(-2.4,-4,2.05),'qa-front':(0,-4,.95),'qa-side':(4,0,.95),'qa-top':(0,-.025,4),
 'qa-back':(0,4,.95),'qa-wireframe':(-2.4,-4,2.05)}
if '--gray-back-only' in sys.argv:views={'gray-back3q':views['gray-back3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.90
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00140;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-back-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-12,1)),('silhouette-128-side',(12,-.025,1))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
