"""One static open pocket watch, metres, Z up, front -Y. New closed thick case,
recessed dial, layered solid hands/markers, crown, cut-through bow and supported
bored hinge sleeves. Flat integral back rests on the ground; no extra stand.
One fixed 112-degree cover pose; no clockwork, accuracy, animation or wear claim.
Standalone: --geometry-only / --no-render / --gray-only / --preview-only / --extra-views.
All renders freshly import the actual GLB, Cycles128 FIXED4, no denoise.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='timekeeping-pocket-watch-display-01';VERSION='1.0.0';TITLE='Open Brass Pocket Watch'
DESCRIPTION=('Original static low-poly open pocket watch with a thick closed-back brass case, true recessed ivory dial, '
 'sixty separate physical markers, two separated blue-steel hands and a supported spindle, faceted winding crown and a genuine open bow. '
 'The shallow thick cover is fixed at 112 degrees on three individually bored hinge sleeves and an embedded axle, with finite case and cover mounting tongues. '
 'The flat circular back provides a finite ground-contact patch; all mesh components connect to it. No separate stand or chain is included. '
 'Six flat solid PBR materials, no images or textures. Metres, native Z up, dial +Z, front -Y and origin at ground below case centre. '
 'One original reusable prop, distinct from the old open-frame pendulum clock and sundial. '
 'Static stylized visual only: no timekeeping, calibration, clockwork, water resistance, precious-metal value, wearability, moving-cover or safety claim.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('WarmBrass_Case',(.56,.29,.065,1),.36,.68),
 ('Ivory_EnamelDial',(.86,.81,.66,1),.51,.04),('BlueSteel_Hands',(.018,.075,.12,1),.34,.55),
 ('PaleBrass_EdgesAndCrown',(.81,.59,.19,1),.31,.72),('Charcoal_Markers',(.026,.030,.027,1),.47,.12),
 ('Bronze_LidMedallion',(.28,.095,.025,1),.45,.60)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('OpenBrassPocketWatch',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True
root['origin_datum']='ground projection of body centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role,asset=True):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if asset:
  o.parent=root;me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
 return o

# GEOMETRY_BEGIN: newly hand-authored self-contained vector construction.
def obox(name,c,size,material,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 c,u,v,w=Vector(c),Vector(u),Vector(v),Vector(w);a,b,d=[s/2 for s in size]
 vs=[c+u*sx*a+v*sy*b+w*sz*d for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def rod(name,a,b,r,material,role,n=24):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0));u=d.cross(ref).normalized();v=d.cross(u)
 vs=[p+r*(math.cos(math.tau*i/n)*u+math.sin(math.tau*i/n)*v) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],material,role)
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
def lathe(name,profile,material,role,c=(0,0,0),u=(1,0,0),v=(0,1,0),w=(0,0,1),n=64):
 c,u,v,w=Vector(c),Vector(u),Vector(v),Vector(w);vs=[];rings=[];fs=[]
 for r,z in profile:
  if r==0:rings.append([len(vs)]);vs.append(c+w*z)
  else:
   rings.append(list(range(len(vs),len(vs)+n)))
   vs.extend(c+u*(r*math.cos(math.tau*i/n))+v*(r*math.sin(math.tau*i/n))+w*z for i in range(n))
 for a,b in zip(rings,rings[1:]+rings[:1]):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   fs.append((a[0],b[j],b[i]) if len(a)==1 else ((a[i],a[j],b[0]) if len(b)==1 else (a[i],a[j],b[j],b[i])))
 return mesh(name,vs,fs,material,role)
def ring(name,ri,ro,z0,z1,material,role,**kw):
 return lathe(name,[(ri,z0),(ro,z0),(ro,z1),(ri,z1)],material,role,**kw)
def pointer(name,length,width,z0,z1,degrees,material):
 a=math.radians(degrees);u=Vector((math.cos(a),-math.sin(a),0));v=Vector((math.sin(a),math.cos(a),0))
 outline=[(-width*.38,-.003),(width*.38,-.003),(width*.5,.004),(0,length),(-width*.5,.004)]
 vs=[u*x+v*y+Vector((0,0,z)) for z in [z0,z1] for x,y in outline];n=len(outline)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,'separate solid fixed hand, with real vertical separation from dial and other hand')
feet=['Case_ThickClosedBowl']
lathe('Case_ThickClosedBowl',[(0,0),(.024,0),(.0305,.001),(.032,.0026),(.033,.0046),(.0328,.0083),(.0318,.0102),(.028,.0102),(.0278,.0086),(.0278,.0034),(0,.0034)],0,'thick closed-back cup with true upper recess and finite circular planar back support')
rod('Dial_RecessedEnamel',(0,0,.0030),(0,0,.0058),.02755,1,'thick ivory dial seated inside case recess',n=64)
joint('Dial_RecessedEnamel','Case_ThickClosedBowl',[(x,0,.0032) for x in [-.010,0,.010]])
ring('Bezel_RaisedLip',.0290,.0313,.0100,.0106,3,'separate raised annular bezel, physically embedded in case lip')
joint('Bezel_RaisedLip','Case_ThickClosedBowl',[(.030*math.cos(a),.030*math.sin(a),.0101) for a in [0,2.1,4.2]])
for i in range(60):
 a=math.tau*i/60;major=i%5==0;d=Vector((math.sin(a),math.cos(a),0));u=Vector((math.cos(a),-math.sin(a),0));length=.0030 if major else .0014
 name=f'Dial_Marker_{i:02d}';c=d*(.0250-length/2)+Vector((0,0,.0059))
 obox(name,c,(.00075 if major else .00032,length,.0006),4,'solid hour marker' if major else 'solid minute marker',u,d,(0,0,1))
 joint(name,'Dial_RecessedEnamel',[c+d*t+Vector((0,0,-.0002)) for t in [-.00015,0,.00015]])
rod('Hands_CentralSpindle',(0,0,.0054),(0,0,.0093),.00125,3,'solid central spindle rooted in dial and physically supporting both hands',n=24)
joint('Hands_CentralSpindle','Dial_RecessedEnamel',[(x,0,.0056) for x in [-.0004,0,.0004]])
pointer('Hands_Hour',.0160,.0026,.0066,.00715,-55,2)
pointer('Hands_Minute',.0220,.0018,.00765,.00820,55,2)
for name,z in [('Hands_Hour',.0069),('Hands_Minute',.0079)]:
 joint(name,'Hands_CentralSpindle',[(0,y,z) for y in [-.00020,0,.00020]])
rod('Hands_HubCap',(0,0,.0091),(0,0,.0097),.0018,5,'small raised central hub cap on spindle',n=24)
joint('Hands_HubCap','Hands_CentralSpindle',[(x,0,.0092) for x in [-.0004,0,.0004]])
# Crown and bow are oriented along +Y, and supported through the case neck.
rod('Crown_Neck',(0,.0305,.0058),(0,.0370,.0058),.0027,0,'case-supported winding neck, static and decorative',n=24)
joint('Crown_Neck','Case_ThickClosedBowl',[(x,.0318,.0058) for x in [-.0005,0,.0005]])
rod('Crown_FacetedGrip',(0,.0345,.0058),(0,.0418,.0058),.0043,3,'faceted independent winding crown connected to its neck',n=24)
joint('Crown_FacetedGrip','Crown_Neck',[(x,.0355,.0058) for x in [-.0005,0,.0005]])
# Separate narrow rib bands provide actual crown grip relief, not a texture.
for label,y0,y1 in [('Lower',.0344,.0353),('Middle',.0375,.0384),('Upper',.0405,.0414)]:
 name='Crown_GripBand_'+label
 ring(name,.0039,.0048,y0,y1,0,'raised annular grip band embedded into faceted crown',c=(0,0,.0058),u=(1,0,0),v=(0,0,-1),w=(0,1,0),n=24)
 joint(name,'Crown_FacetedGrip',[(.00410,yy,.0058) for yy in [y0+.0002,(y0+y1)/2,y1-.0002]])
BOW=Vector((0,.0470,.0058))
ring('Bow_TrueOpenLoop',.0054,.0076,-.0011,.0011,3,'genuine cut-through hanging bow, physically embedded into crown top',c=BOW,n=48)
joint('Bow_TrueOpenLoop','Crown_FacetedGrip',[(x,.0406,.0058) for x in [-.00045,0,.00045]])
# Three bored sleeves around the actual hinge pin, with visible inter-sleeve gaps.
H=Vector((-.0348,0,.0092));hinges=[]
for label,y0,y1 in [('CaseLower',-.0090,-.0050),('CoverCentre',-.0045,.0045),('CaseUpper',.0050,.0090)]:
 name='Hinge_BoredSleeve_'+label
 ring(name,.00110,.00240,y0,y1,0,'actual annular hinge sleeve with central bore occupied by the embedded fixed axle',c=H,u=(1,0,0),v=(0,0,-1),w=(0,1,0),n=24)
 hinges.append({'mesh':name,'axis_start_m':list(H+Vector((0,y0,0))),'axis_end_m':list(H+Vector((0,y1,0))),'bore_radius_m':.00110,'outer_radius_m':.00240})
 if label!='CoverCentre':
  y=(y0+y1)/2;lug='Hinge_CaseMount_'+label
  obox(lug,(-.0313,y,.0083),(.0042,.0036,.0036),0,'finite hinge lug embedded in thick case side while leaving sleeve bore open')
  joint(lug,'Case_ThickClosedBowl',[(-.0305,y+d,.0083) for d in [-.0005,0,.0005]])
  joint(name,lug,[(H.x+.0021,y+d,H.z) for d in [-.0005,0,.0005]])
rod('Hinge_FixedPin',H+Vector((0,-.0102,0)),H+Vector((0,.0102,0)),.00125,4,'one continuous axle with finite intentional sleeve interference, no movement claim',n=24)
for row in hinges:
 y=(row['axis_start_m'][1]+row['axis_end_m'][1])/2
 joint('Hinge_FixedPin',row['mesh'],[(H.x+.00118,y+d,H.z) for d in [-.0003,0,.0003]])
OPEN_ANGLE=112;a=math.radians(OPEN_ANGLE);U=Vector((math.cos(a),0,math.sin(a)));V=Vector((0,1,0));N=Vector((-math.sin(a),0,math.cos(a)));C=H+U*.0337
obox('Cover_HingeTongue',H+U*.0040,(.0046,.0060,.0020),0,'cover-root tongue embedded in central hinge sleeve and lid rim',U,V,N)
joint('Cover_HingeTongue','Hinge_BoredSleeve_CoverCentre',[H+U*.0021+V*d for d in [-.0006,0,.0006]])
lathe('Cover_ShallowThickLid',[(0,.0010),(.025,.0010),(.0308,.0017),(.0317,.0012),(.032,-.0007),(.0313,-.0018),(.0288,-.0018),(.0282,-.0004),(0,-.0004)],0,'closed shallow hunter cover, actual wall thickness and inward facing inset',c=C,u=U,v=V,w=N)
joint('Cover_ShallowThickLid','Cover_HingeTongue',[H+U*.0040+V*d+N*.0005 for d in [-.0007,0,.0007]])
ring('Cover_InteriorRaisedRing',.0196,.0203,-.00065,-.00030,3,'thin solid decorative concentric ring embedded into lid interior',c=C,u=U,v=V,w=N,n=48)
joint('Cover_InteriorRaisedRing','Cover_ShallowThickLid',[C+U*(.01995*math.cos(t))+V*(.01995*math.sin(t))+N*(-.00035) for t in [0,2.1,4.2]])
lathe('Cover_CentralMedallion',[(0,-.00075),(.0085,-.00075),(.0085,-.00030),(0,-.00030)],5,'unlettered solid central lid medallion with finite embedded support',c=C,u=U,v=V,w=N,n=40)
joint('Cover_CentralMedallion','Cover_ShallowThickLid',[C+U*d+N*(-.00035) for d in [-.003,0,.003]])
# GEOMETRY_END

# Apply deterministic triangulation, recalculate closed winding and quantize positions.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for v in o.data.vertices:v.co=Vector(tuple(round(float(c),6) for c in v.co))
 o.data.update()
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-13 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-13 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,2)
   if q is None:break
   hits+=1;p=q+d*1e-6
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in links:
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3])
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.000010,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(feet);todo=list(feet)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)

# Ground contact is the case's finite planar back, not an AABB or tangent point.
supports=[]
for name in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0017;supports.append({'name':name,'area_m2':area,'triangles':patch})
def clear_ray(label,start,direction,length):
 start,direction=Vector(start),Vector(direction).normalized();hits=[]
 for name,tree in trees.items():
  q,_,_,_=tree.ray_cast(start,direction,length)
  if q is not None:hits.append(name)
 assert not hits,('Blocked real aperture',label,list(start),hits)
 return {'start_m':list(start),'direction':list(direction),'length_m':length}
apertures=[]
for dx,dy in [(0,0),(-.002,-.002),(-.002,.002),(.002,-.002),(.002,.002)]:
 apertures.append(clear_ray('bow_opening',(BOW.x+dx,BOW.y+dy,-.001),(0,0,1),.025))
# Exact triangle-nearest distances at every component vertex, with ray-parity containment tests.
# Independent QA additionally derives complete triangle-to-triangle separation on actual GLB.
clearances=[]
for obj,targets,minimum in [('Hands_Hour',['Dial_RecessedEnamel'],.0007),('Hands_Minute',['Hands_Hour'],.00045),('Hands_Minute',['Dial_RecessedEnamel'],.0017),('Cover_ShallowThickLid',['Case_ThickClosedBowl','Bezel_RaisedLip'],.00015)]:
 o=byname[obj];near=[]
 for v in o.data.vertices:
  p=o.matrix_world@v.co;distance=min(trees[name].find_nearest(p)[3] for name in targets)
  assert not any(inside(trees[name],p) for name in targets) and distance>minimum,(obj,list(p),distance)
  near.append(distance)
 clearances.append({'object':obj,'against':targets,'minimum_vertex_to_actual_triangle_distance_m':min(near),'required_m':minimum,'tested_vertices':len(near)})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<14000
# Complete Principled signature; no texture nodes or linked Principled sockets are allowed.
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
 'real_bow_aperture':apertures,'layer_clearances':clearances,'physical_marker_count':60,
 'fixed_cover_angle_degrees':OPEN_ANGLE,'hinge_sleeves':hinges,'finite_ground_patches':supports,
 'dial_recess_below_bezel_m':.0106-.0058,'cover_wall_minimum_nominal_m':.0014,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
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
# All renders operate on a freshly imported exact actual GLB, not a second geometry copy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((-.012,.008,.030));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-.12,-.18,.24),2.6,.20),('Fill',(.18,-.04,.17),1.5,.18),('Rim',(-.06,.20,.19),2.1,.16)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.132;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,0,-.00005));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.14,-.22,.20),'gray-back3q':(-.16,.21,.18)} if gray else {
 'thumbnail':(.14,-.22,.20),'qa-front':(-.012,-.25,.030),'qa-side':(.25,.008,.030),'qa-top':(-.012,.008,.30),
 'qa-back':(-.012,.25,.030),'qa-wireframe':(.14,-.22,.20)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True;t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.000020;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(-.012,-.25,.030)),('silhouette-128-side',(.25,.008,.030))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
