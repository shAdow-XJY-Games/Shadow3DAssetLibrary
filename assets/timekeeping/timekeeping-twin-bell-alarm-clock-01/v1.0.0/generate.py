"""Original static twin-bell alarm clock with true hollow bells and a recessed dial.
One prop, metres, Z up, front -Y, centred finite ground support. No clockwork or sound.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='timekeeping-twin-bell-alarm-clock-01';VERSION='1.0.0';TITLE='Twin-Bell Desk Alarm Clock'
DESCRIPTION=('One original static twin-bell desk alarm clock: a deep upright circular closed-back case with a real front recess, twelve raised solid hour batons and two separate fixed hands on a shared supported spindle. '
 'Two outward-tilted bell domes are genuine continuous thick shells with open underside cavities, each seated on its own case-rooted support rod. The central fixed hammer head has positive clearance to both bells. Two splayed feet have finite flat ground patches. '
 'Twenty-six named editable closed meshes, five constant fully opaque solid PBR materials, metres, source Z up, front -Y and ground-centre origin. Gold-toned rim and bells, deep jade case, ivory dial and dark solid hands. All visible markings are actual geometry. No text, texture, glass, logo, separate base or surrounding scene. '
 'A single fixed display pose only. No timekeeping, alarm sound, ringing motion, clockwork, winding, electricity, accuracy, calibration, mechanical movement, assembly path, load, manufacturing, lifetime or safety performance is modeled or guaranteed. Not a working or calibrated instrument.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Case_DeepJade',(.052,.25,.225,1),.57,.18),('Dial_WarmIvory',(.85,.79,.63,1),.72,0),('Hands_Graphite',(.025,.039,.042,1),.58,.18),('Metal_BrushedChampagne',(.53,.36,.15,1),.49,.68),('Bell_InnerBronze',(.25,.17,.070,1),.63,.55)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'visible_markings':'solid mesh batons','no_timekeeping_sound_or_motion_claim':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name

def link(a,b,p,axis=(0,1,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def void(name,lo,hi,role,c=(0,0,0),u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':[transform(p,c,u,v,w) for p in vs],'faces':fs,'role':role}
def lathe(name,profile,material,role,c=(0,0,0),u=(1,0,0),v=(0,1,0),w=(0,0,1),n=48,segment_mats=None):
 vs=[];rings=[];fs=[];fm=[]
 for r,z in profile:
  if r==0:rings.append([len(vs)]);vs.append(add(c,mul(w,z)))
  else:
   rings.append(list(range(len(vs),len(vs)+n)))
   vs.extend(transform((r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z),c,u,v,w) for i in range(n))
 for k,(a,b) in enumerate(zip(rings,rings[1:]+rings[:1])):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   fs.append((a[0],b[j],b[i]) if len(a)==1 else ((a[i],a[j],b[0]) if len(b)==1 else (a[i],a[j],b[j],b[i])))
   fm.append(material if segment_mats is None else segment_mats[k])
 return mesh(name,vs,fs,material,role,fm)
def rod(name,a,b,r,material,role,n=24):
 w=unit(sub(b,a));u=unit(cross((0,1,0) if abs(w[1])<.9 else (1,0,0),w));v=cross(w,u);L=math.sqrt(dot(sub(b,a),sub(b,a)))
 return lathe(name,[(0,0),(r,0),(r,L),(0,L)],material,role,c=a,u=u,v=v,w=w,n=n)
def obox(name,c,size,material,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 vs,fs=box_geometry(tuple(-x/2 for x in size),tuple(x/2 for x in size))
 return mesh(name,[transform(p,c,u,v,w) for p in vs],fs,material,role)
C=(0,0,.155);U=(1,0,0);V=(0,0,-1);W=(0,1,0)
# Closed-back annular bowl, not a flat disk: 15 mm side wall and 15 mm rear wall.
CASE=lathe('Case_DeepClosedBackShell',[(0,.060),(.110,.060),(.119,.051),(.119,-.052),(.115,-.060),(.103,-.060),(.103,.038),(.096,.045),(0,.045)],0,'continuous deep circular shell with real 103 mm-radius front opening and thick closed back',c=C,u=U,v=V,w=W,n=64,segment_mats=[0,0,0,3,3,0,0,0,0])
DIAL=rod('Dial_RecessedIvoryFace',(0,-.038,.155),(0,-.026,.155),.107,1,'solid recessed face seated by finite radial overlap within the surrounding case wall',n=64)
for side in [-1,1]:link(DIAL,CASE,(side*.105, -.032,.155),axis=(0,0,1),spread=.005)
MARKERS=[]
for i in range(12):
 a=math.tau*i/12;rad=(math.sin(a),0,math.cos(a));tan=(math.cos(a),0,-math.sin(a));name=f'Dial_RaisedHourBaton_{i:02d}';p=add(C,mul(rad,.089))
 obox(name,add(p,(0,-.039,0)),(.005,.004,.014),2,'individually supported solid raised hour baton; no painted or texture marking',u=tan,v=(0,1,0),w=rad)
 link(name,DIAL,add(p,(0,-.0375,0)),axis=rad,spread=.002);MARKERS.append(name)
SPINDLE=rod('Hands_CommonFixedSpindle',(0,-.056,.155),(0,-.034,.155),.006,3,'one common fixed solid spindle embedded into face and both separated hands',n=24)
link(SPINDLE,DIAL,(0,-.036,.155),axis=(1,0,0),spread=.002)
def pointer(name,length,width,y0,y1,degrees):
 a=math.radians(degrees);rad=(math.sin(a),0,math.cos(a));tan=(math.cos(a),0,-math.sin(a))
 outline=[(-width*.45,-.009),(width*.45,-.009),(width*.5,.006),(width*.25,length-.008),(0,length),(-width*.25,length-.008),(-width*.5,.006)]
 vs=[add(C,add(mul(tan,x),add(mul(rad,z),(0,y,0)))) for y in [y0,y1] for x,z in outline];n=len(outline)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,2,'separate tapered solid fixed hand; common central spindle with positive face, index and other-hand separation')
HOUR=pointer('Hands_FixedHour',.057,.010,-.047,-.044,-55)
MINUTE=pointer('Hands_FixedMinute',.080,.007,-.053,-.050,60)
for name,y in [(HOUR,-.0455),(MINUTE,-.0515)]:link(name,SPINDLE,(0,y,.155),axis=(1,0,0),spread=.0015)
HUB=rod('Hands_FrontHubCap',(0,-.058,.155),(0,-.054,.155),.009,3,'small solid hub cap overlapping the end of the fixed spindle',n=24)
link(HUB,SPINDLE,(0,-.055,.155),axis=(1,0,0),spread=.002)
# Integral splayed foot prisms: broad planar bottoms and narrowed shell seats.
for label,sgn in [('Left',-1),('Right',1)]:
 name='Foot_'+label+'_SplayedFlat';vs=[]
 for cx,z,wx,dy in [(sgn*.083,0,.016,.038),(sgn*.062,.076,.013,.020)]:
  vs.extend([(cx-wx,-dy,z),(cx+wx,-dy,z),(cx+wx,dy,z),(cx-wx,dy,z)])
 fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 mesh(name,vs,fs,2,'one splayed solid foot with a finite 32 by 76 mm ground patch and finite shell overlap');FEET.append(name)
 link(name,CASE,(sgn*.064,0,.063),axis=(0,1,0),spread=.012)
BELLS=[]
for label,sgn in [('Left',-1),('Right',1)]:
 ang=math.radians(18);w=(sgn*math.sin(ang),0,math.cos(ang));u=(math.cos(ang),0,-sgn*math.sin(ang));v=(0,1,0);c=(sgn*.074,0,.275)
 support='Bell_'+label+'_SupportRod';bell='Bell_'+label+'_TrueHollowDome'
 rod(support,add(c,mul(w,-.040)),add(c,mul(w,.051)),.0045,3,'fixed solid bell support traverses the open cavity centre and seats inside the thick dome crown',n=24)
 link(support,CASE,add(c,mul(w,-.035)),axis=(0,1,0),spread=.001)
 profile=[(.050,0),(.047,.018),(.036,.037),(.020,.049),(0,.053),(0,.047),(.016,.043),(.031,.032),(.041,.014),(.044,0)]
 lathe(bell,profile,3,'real continuous thick bell shell with open underside, inner dome and annular rim; no solid hemisphere substitute',c=c,u=u,v=v,w=w,n=48,segment_mats=[3,3,3,3,3,4,4,4,4,3])
 link(bell,support,add(c,mul(w,.049)),axis=(0,1,0),spread=.001)
 for side,ylo,yhi in [('Front',-.024,-.010),('Back',.010,.024)]:
  void('Bell_'+label+'_'+side+'Cavity',(-.018,ylo,-.006),(.018,yhi,.026),'finite uncapped inner bell air volume, offset from the real central support rod',c,u,v,w)
 for x,y in [(-.014,-.018),(.014,-.018),(-.014,.018),(.014,.018)]:
  origin=transform((x,y,-.009),c,u,v,w);BORES.append({'mesh':bell,'origin_m':origin,'direction':w,'length_m':.038});GAPS.append({'label':label+'_open_cavity_ray','origin_m':origin,'direction':w,'length_m':.038})
 WALL_PROBES.append({'mesh':bell,'origin_m':transform((0,-.012,.012),c,u,v,w),'direction':(0,-1,0),'length_m':.070,'minimum_wall_thickness_m':.004})
 WALL_PROBES.append({'mesh':bell,'origin_m':transform((.010,0,.030),c,u,v,w),'direction':w,'length_m':.040,'minimum_wall_thickness_m':.004})
 BELLS.append({'shell':bell,'support':support,'origin_m':c,'local_x':u,'local_y':v,'axis':w,'rim_outer_radius_m':.050,'rim_inner_radius_m':.044,'thick_open_shell':True})
HAMMER=rod('Hammer_CentralFixedStem',(0,0,.263),(0,0,.307),.0035,3,'fixed central stem rooted in the case top; no oscillation or motion',n=24)
link(HAMMER,CASE,(0,0,.270),axis=(0,1,0),spread=.001)
HEAD=rod('Hammer_FixedCrossHead',(-.013,0,.306),(.013,0,.306),.007,2,'fixed short transverse solid hammer head clear of both bell shells',n=24)
link(HEAD,HAMMER,(0,0,.3045),axis=(0,1,0),spread=.001)
# Complete bounded empty volumes, not merely visual centre rays.
void('Case_InternalEmptyChamber',(-.050,-.020,.105),(.050,.030,.205),'finite actual case chamber behind the solid dial and ahead of the thick back')
for label,sgn in [('Left',-1),('Right',1)]:
 xa,xb=sorted([sgn*.065,sgn*.090]);void('Dial_'+label+'_FrontRecess',(xa,-.059,.125),(xb,-.043,.185),'finite front recess in front of the markings, separated from the side wall and pointer tips')
 xa,xb=sorted([sgn*.016,sgn*.026]);void('Hammer_'+label+'_ClearAir',(xa,-.005,.300),(xb,.005,.310),'complete finite empty space between central hammer head and bell')
void('Hands_InterlayerAir',(.015,-.049,.135),(.060,-.048,.175),'finite clear slab between fixed hour and minute pointer planes, clear of spindle')
WALL_PROBES.append({'mesh':CASE,'origin_m':(0,.020,.155),'direction':(0,1,0),'length_m':.060,'minimum_wall_thickness_m':.014})
CLOCK_CONTRACT={'single_prop_count':1,'bell_count':2,'independent_hour_baton_count':12,'bells':BELLS,'fixed_hand_meshes':[HOUR,MINUTE],'spindle_mesh':SPINDLE,'hammer_head_mesh':HEAD,'case_mesh':CASE,'dial_mesh':DIAL,'feet':FEET,'minimum_hand_layer_gap_m':.003,'minimum_hour_hand_to_indices_gap_m':.003,'minimum_hour_hand_to_face_gap_m':.006,'fixed_time_display_only':True,'timekeeping_sound_alarm_animation_or_mechanical_performance':False}
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
root=bpy.data.objects.new('OneStaticTwinBellDeskClock',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
clock_evidence=dict(CLOCK_CONTRACT,finite_empty_volume_checks=void_volume_checks,actual_shell_thickness_checks=wall_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'clock_geometry':clock_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/timekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'timekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.163));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.42;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv or '--gray-back-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-2.4,-4,1.7),'gray-back3q':(2.4,3.8,.80)} if gray else {
 'thumbnail':(-2.4,-4,1.7),'qa-front':(0,-4,.50),'qa-side':(4,0,.50),'qa-top':(0,0,4),
 'qa-back':(0,4,.50),'qa-wireframe':(-2.4,-4,1.7)}
if '--gray-back-only' in sys.argv:views={'gray-back3q':views['gray-back3q']}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.42
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00065;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv and '--gray-back-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.163)),('silhouette-128-side',(4,0,.163))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
