"""Original hollow winter boot pair, a single static visual prop.
Metres, Z up, front -Y. No wearable fit, ski-binding compatibility or safety performance.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-hollow-snow-boot-pair-01';VERSION='1.0.0';TITLE='Hollow Cuff Snow Boot Pair'
DESCRIPTION=('Original mirrored pair of stationary snow boots counted together as one prop. Each has a continuous thick closed shell with a bulbous asymmetric toe, curved instep, narrowing ankle, tall shaft, genuinely open mouth, complete deep interior and closed inner floor. Independent layered soles, three forefoot tread bars and a distinct rear heel make finite ground contact. Thick annular folded cuffs and six fixed coarse lace segments have verified finite embedded roots. The two boots are separated by real empty space. '
 'Metre scale, Z up, front -Y, X midline / design Y=0 / ground Z=0 origin; actual bounding-box midpoint (0, -0.0095, 0.207) metres. Editable closed meshes, four opaque constant solid PBR materials. Laces are actual tubes, the mouth is an open annulus with a deep cavity, and tread is modeled solid geometry. No legs, person, display platform, accessories, logo, textures, animation or new scene. '
 'Stylized static visual only. No foot size or wearable fit, donning, lace motion, thermal insulation, waterproofing, grip, load, manufacturing, installation, sport or occupational protection or safety certification. No compatibility with any ski or binding, including previously created alpine skis. Not functional footwear design or use guidance.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={};BOOTS=[]
PALETTE=[('Upper_DeepForest',(.085,.20,.15,1),.78,0),('Sole_Toe_Graphite',(.027,.044,.036,1),.66,0),('FoldedCuff_WarmIvory',(.78,.66,.44,1),.85,0),('FixedLace_Russet',(.72,.255,.055,1),.70,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.0004):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def void(name,lo,hi,role):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def profile(name,transform,rings,material,role,sides=20,cap=True,segments=None):
 # Rings are (z,rx,ry,cy,xshift). Outward normal winding is repaired in Blender.
 vs=[transform((dx+rx*math.cos(2*math.pi*j/sides),cy+ry*math.sin(2*math.pi*j/sides),z)) for z,rx,ry,cy,dx in rings for j in range(sides)]
 fs=[tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+j for j in range(sides))] if cap else []
 for i in range(len(rings)-(1 if cap else 0)):
  nxt=(i+1)%len(rings)
  for j in range(sides):
   k=(j+1)%sides;fs.append((i*sides+j,i*sides+k,nxt*sides+k,nxt*sides+j))
 mesh(name,vs,fs,material,role)
 if segments is not None:G[name]['face_materials']=([segments[0],segments[-1]] if cap else [])+[m for m in segments for _ in range(sides)]
 return name
def prism(name,transform,poly,z0,z1,material,role):
 vs=[transform((x,y,z)) for z in [z0,z1] for x,y in poly];n=len(poly);fs=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return mesh(name,vs,fs,material,role)
def tube(name,transform,points,radius,material,role,sides=8):
 # Stable miter-free rings perpendicular to local path tangent, embedded ends.
 def sub(a,b):return tuple(x-y for x,y in zip(a,b))
 def unit(v):return mul(v,1/math.sqrt(sum(x*x for x in v)))
 def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
 vs=[]
 for i,p in enumerate(points):
  tangent=unit(sub(points[min(i+1,len(points)-1)],points[max(i-1,0)]));u=unit(cross(tangent,(0,1,0)));v=cross(tangent,u)
  vs.extend(transform(add(p,add(mul(u,radius*math.cos(2*math.pi*j/sides)),mul(v,radius*math.sin(2*math.pi*j/sides))))) for j in range(sides))
 fs=[tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]
 for i in range(len(points)-1):
  for j in range(sides):k=(j+1)%sides;fs.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
 return mesh(name,vs,fs,material,role)
OUTER=[(.057,.073,.163,-.020,.006),(.080,.078,.170,-.025,.007),(.120,.076,.162,-.019,.006),(.160,.069,.132,.004,.003),(.200,.065,.100,.030,0),(.240,.064,.078,.048,0),(.330,.070,.079,.054,0),(.395,.073,.082,.055,0)]
INNER=[(.395,.054,.061,.055,0),(.330,.051,.058,.054,0),(.240,.046,.054,.048,0),(.200,.046,.073,.030,0),(.160,.048,.104,.004,.003),(.120,.050,.132,-.019,.006),(.085,.047,.129,-.019,.006)]
SOLE=[(.023,.075,.164,-.020,.006),(.031,.084,.178,-.022,.006),(.057,.083,.175,-.022,.006),(.068,.076,.166,-.020,.006)]
CUFF=[(.364,.074,.086,.055,0),(.370,.082,.093,.055,0),(.405,.082,.093,.055,0),(.414,.076,.087,.055,0),(.414,.054,.061,.055,0),(.364,.054,.061,.055,0)]
def interp(rings,z):
 for a,b in zip(rings,rings[1:]):
  if a[0]<=z<=b[0]:
   f=(z-a[0])/(b[0]-a[0]);return tuple(x+(y-x)*f for x,y in zip(a,b))
 raise ValueError(z)
def outer_front(x,z):
 _,rx,ry,cy,dx=interp(OUTER,z);return cy-ry*math.sqrt(1-((x-dx)/rx)**2)
for label,cx,cy,hand in [('Left',-.118,0,1),('Right',.118,.025,-1)]:
 def tf(p):return (cx+hand*p[0],cy+p[1],p[2])
 prefix=label+'_';shell=prefix+'HollowShell';sole=prefix+'LayeredSole';cuff=prefix+'FoldedCuff'
 # Outer bottom -> outer top -> inner top -> true internal floor, capped only at the two bottoms.
 rings=OUTER+INNER
 profile(shell,tf,rings,0,'continuous thick shell with bulbous toe, real ankle transition, open mouth, complete inner wall and closed floor',segments=[1,1,1,0,0,0,0,2,0,0,0,0,0,0])
 profile(sole,tf,SOLE,1,'separate thick sculpted outsole, raised forefoot with real arch gap underneath')
 link(shell,sole,tf((.006,-.020,.062)),axis=(1,0,0),spread=.001)
 profile(cuff,tf,CUFF,2,'closed annular folded cuff; real open mouth, finite embedded base',cap=False)
 link(cuff,shell,tf((.066,.055,.380)),axis=(0,1,0),spread=.001)
 # Three tapered front tread bars and one broad discrete rear heel, all grounded at finite faces.
 treads=[]
 for k,(yy,halfwidth) in enumerate([(-.145,.041),(-.098,.062),(-.050,.064)]):
  name=prefix+'ForefootTread'+str(k+1);poly=[(-halfwidth+.006,yy-.013),(halfwidth-.006,yy-.013),(halfwidth,yy-.007),(halfwidth,yy+.009),(halfwidth-.006,yy+.015),(-halfwidth+.006,yy+.015),(-halfwidth,yy+.009),(-halfwidth,yy-.007)]
  prism(name,tf,poly,0,.029,1,'solid forefoot tread bar with finite planar contact patch');link(name,sole,tf((0,yy,.026)),axis=(1,0,0),spread=.001);FEET.append(name);treads.append(name)
 heel=prefix+'HeelPad';poly=[(-.047,.050),(.047,.050),(.061,.067),(.058,.110),(.044,.133),(-.044,.133),(-.058,.110),(-.061,.067)]
 prism(heel,tf,poly,0,.029,1,'distinct solid rear heel; finite flat ground contact, separated from forefoot by true arch clearance');link(heel,sole,tf((0,.080,.026)),axis=(1,0,0),spread=.001);FEET.append(heel)
 laces=[];lace_roots=[]
 for row,(za,zb) in enumerate([(.213,.247),(.265,.299),(.317,.351)]):
  for diagonal in range(2):
   x0=-.049 if diagonal==0 else .049;x1=-x0
   a=(x0,outer_front(x0,za)+.0055,za);b=(x1,outer_front(x1,zb)+.0055,zb);mid=(za+zb)/2
   # The second strand runs 14 mm farther forward at the crossing, leaving a real gap.
   front=outer_front(0,mid)-(.009 if diagonal==0 else .023)
   points=[a,(x0*.65,front,za+.008),(0,front,mid),(x1*.65,front,zb-.008),b]
   name=prefix+f'FixedLace{row+1}{"A" if diagonal==0 else "B"}'
   tube(name,tf,points,.0042,3,'coarse fixed lace tube with two embedded shell roots and separated cross-over strand')
   # Root tests use points just after the terminal section, before emerging from the shell.
   for end,adjacent in [(points[0],points[1]),(points[-1],points[-2])]:
    point=tuple(u+.045*(v-u) for u,v in zip(end,adjacent));link(name,shell,tf(point),axis=(0,0,1),spread=.0003);lace_roots.append(tf(point))
   laces.append(name)
 # Conservative finite central cavity: full depth is tested, plus a forward toe pocket.
 void(prefix+'ShaftDeepAir',(cx-.021,cy+.018,.096),(cx+.021,cy+.076,.438),'complete unobstructed central shaft and ankle volume reaching near actual inner floor')
 # A full shaped finite volume follows every inner-wall ring, conservatively inset by 3 mm.
 cavity_rings=[(z+.004 if i==0 else z,rx-.003,ry-.003,y,dx) for i,(z,rx,ry,y,dx) in enumerate(reversed(INNER))]+[(.440,.051,.058,.055,0)]
 probe_name=prefix+'CompleteShapedInteriorAir';profile(probe_name,tf,cavity_rings,0,'complete finite shaped cavity from toe pocket through ankle and open mouth');VOID_VOLUMES[probe_name]=G.pop(probe_name);VOID_VOLUMES[probe_name]['enclosed_fill_center_m']=tf((0,.052,.260))
 # Toe cavity separate from shaft volume but overlapping it, proving connected L-shaped interior.
 void(prefix+'ToePocketAir',(cx-.024,cy-.108,.094),(cx+.024,cy+.048,.112),'finite forward toe pocket connected with deep shaft volume above the real floor')
 void(prefix+'UnderArchAir',(cx-.030,cy-.012,.002),(cx+.030,cy+.036,.019),'actual finite under-arch space separating heel from forefoot tread')
 GAPS.append({'label':prefix+'mouth_to_inner_floor_air','origin_m':[cx,cy+.052,.438],'direction':[0,0,-1],'length_m':.340})
 BORES.append({'label':prefix+'cuff_opening','mesh':cuff,'origin_m':[cx,cy+.055,.440],'direction':[0,0,-1],'length_m':.090})
 FLOOR_PROBES.append({'label':prefix+'closed_interior_floor','mesh':shell,'origin_m':[cx,cy+.052,.110],'direction':[0,0,-1],'length_m':.100,'expected_hit_z_m':.085,'minimum_floor_thickness_m':.020})
 WALL_PROBES.append({'label':prefix+'shaft_wall','mesh':shell,'origin_m':[cx,cy+.054,.300],'direction':[hand,0,0],'length_m':.100,'minimum_wall_thickness_m':.015})
 BOOTS.append({'label':label,'shell':shell,'sole':sole,'cuff':cuff,'treads':treads,'heel':heel,'laces':laces,'centre_x_m':cx,'offset_y_m':cy,'handedness':hand,'lace_root_points_m':lace_roots,'mouth_top_z_m':.414,'inner_floor_z_m':.085,'closed_floor_thickness_m':.028,'static_only':True})
void('Between_Complete_Boots',(-.025,-.205,.002),(.025,.190,.435),'finite longitudinal air gap separating every left and right boot part')
GAPS.append({'label':'full_pair_separation','origin_m':[0,-.215,.200],'direction':[0,1,0],'length_m':.420})
BOOT_CONTRACT={'boots':BOOTS,'single_prop_count':1,'boot_count':2,'mirrored_foot_geometry':True,'continuous_hollow_shells':True,'static_fixed_laces_only':True,'display_stand':False,'ski_binding_compatibility_claim':False,'wearable_or_safety_claim':False}
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
root=bpy.data.objects.new('OneHollowSnowBootPair',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X midline, design Y=0, ground Z=0; actual bounding-box midpoint (0, -0.0095, 0.207) m';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
boot_evidence=dict(BOOT_CONTRACT,finite_external_air_volume_checks=void_volume_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'snow_boot_pair_geometry':boot_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'actual_inner_floor_checks':floor_checks,'actual_thick_wall_checks':wall_checks,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/winter/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'winter','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,.010,.207));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.68;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-.70,-1.0,.82),'gray-back3q':(.70,1.0,.82)} if gray else {
 'thumbnail':(-.70,-1.0,.82),'qa-front':(0,-4,.64),'qa-side':(4,.010,.64),'qa-top':(0,.010,4),
 'qa-back':(0,4,.64),'qa-wireframe':(-.70,-1.0,.82)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.68
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0010625;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.64)),('silhouette-128-side',(4,.010,.64))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
