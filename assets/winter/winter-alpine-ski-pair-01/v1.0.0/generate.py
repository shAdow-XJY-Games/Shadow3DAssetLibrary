"""Original static alpine ski pair: one paired product, one prop ID.
Metres, source Z up, ski tips toward -Y. Not functional safety equipment.
Self-contained source; every render uses a fresh import of the actual GLB.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-alpine-ski-pair-01';VERSION='1.0.0';TITLE='Sidecut Alpine Ski Pair'
DESCRIPTION=('One original low-poly alpine ski pair counted as one static prop. Two long continuous closed boards have genuine '
 'wide shovels, narrow waists, flared tails, variable thickness, upturned tapered tips and gently lifted tail ends. '
 'Each ski has separate mounted toe and heel rail plates, a shaped toe housing with two solid retaining wings, '
 'a low toe sole pad, a tall heel housing, forward heel clamp, heel sole pad, fixed release lever, pivot and two bent raised brake arms. '
 'The measured empty space between the bindings is a visual boot bay, not a fit or release specification. '
 'Teal tops, dark bases, pale steel sidewalls and cream inlaid geometric marks use four constant solid PBR materials. '
 'Named closed editable meshes, actual finite flat sole support and connected binding components; source Z up, metres, ground-centre origin, tips -Y. '
 'One paired product, not two new models; no boots, poles, stand or external textures. '
 'Static artistic game visual only: no skiing, turning, snow interaction, binding release, wearable fit, brake operation, load or sports-safety certification.')
G={};LINKS=[];CONTACTS=[];SPINES={};FEET=[];BOOT_BAYS=[];BOARD_MEASUREMENTS=[]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def length(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/length(a))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),6) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 return name
def box(name,loc,size,material,role,axes=((1,0,0),(0,1,0),(0,0,1))):
 vs=[add(loc,add(mul(axes[0],sx*size[0]/2),add(mul(axes[1],sy*size[1]/2),mul(axes[2],sz*size[2]/2)))) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role)
def rod(name,a,b,radius,material,role,n=12):
 axis=unit(sub(b,a));ref=(0,0,1) if abs(axis[2])<.9 else (1,0,0);u=unit(cross(axis,ref));v=unit(cross(axis,u))
 vs=[add(p,mul(add(mul(u,math.cos(math.tau*i/n)),mul(v,math.sin(math.tau*i/n))),radius)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 SPINES[name]=(a,b);return mesh(name,vs,fs,material,role)
def cyl_x(name,x0,x1,y,z,radius,material,role,n=16):
 phase=math.pi/n;vs=[(x,y+radius*math.cos(phase+math.tau*i/n),z+radius*math.sin(phase+math.tau*i/n)) for x in [x0,x1] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role)
def ring_x(name,x0,x1,y,z,ro,ri,material,role,n=16):
 phase=math.pi/n;vs=[(x,y+r*math.cos(phase+math.tau*i/n),z+r*math.sin(phase+math.tau*i/n)) for r in [ro,ri] for x in [x0,x1] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def end_link(a,b,end):
 p,q=SPINES[a];point=p if end==0 else q;axis=unit(sub(q,p) if end==0 else sub(p,q));LINKS.append((a,b,[add(point,mul(axis,d)) for d in [.006,.010,.014]]))

# Profile stations are (Y, half-width, sole Z, thickness), not a constant-width runner.
PROFILE=[(-.900,.012,.120,.009),(-.875,.045,.090,.010),(-.820,.067,.044,.012),
 (-.720,.071,.010,.016),(-.640,.069,0,.020),(-.450,.059,0,.022),
 (-.200,.045,0,.024),(0,.042,0,.024),(.250,.047,0,.023),
 (.500,.058,0,.020),(.700,.063,0,.018),(.820,.061,.004,.015),
 (.880,.045,.016,.012),(.900,.022,.026,.010)]
CENTRES={'Left':-.120,'Right':.120}
def station(y):
 for a,b in zip(PROFILE[:-1],PROFILE[1:]):
  if a[0]<=y<=b[0]:
   q=(y-a[0])/(b[0]-a[0]);return tuple(a[k]+q*(b[k]-a[k]) for k in [1,2,3])
 raise ValueError(y)
def board(name,x):
 vs=[]
 for y,w,z,t in PROFILE:vs.extend([(x-w,y,z),(x+w,y,z),(x+w,y,z+t),(x-w,y,z+t)])
 fs=[(3,2,1,0)];fm=[3]
 for k in range(len(PROFILE)-1):
  for i in range(4):
   j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i));fm.append([2,3,0,3][i])
 n=4*(len(PROFILE)-1);fs.append((n,n+1,n+2,n+3));fm.append(3)
 mesh(name,vs,fs,0,'continuous closed variable-width sidecut ski with tapered upturned nose and lifted tail');G[name]['face_materials']=fm
def prism_x(name,x0,x1,outline,mat,role):
 n=len(outline);vs=[(x,y,z) for x in [x0,x1] for y,z in outline]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def graphic(name,x,y0,y1,width):
 ys=[y0]+[p[0] for p in PROFILE if y0<p[0]<y1]+[y1];vs=[]
 for y in ys:
  w,z,t=station(y);vs.extend([(x-width/2,y,z+t-.0008),(x+width/2,y,z+t-.0008),(x+width/2,y,z+t+.0012),(x-width/2,y,z+t+.0012)])
 fs=[(3,2,1,0)]
 for k in range(len(ys)-1):
  for i in range(4):j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
 n=4*(len(ys)-1);fs.append((n,n+1,n+2,n+3));mesh(name,vs,fs,1,'thin solid cream graphic following top surface, 0.8mm embedded')
 y=(y0+y1)/2;w,z,t=station(y);link(name,boardname,(x,y,z+t-.0004),(1,0,0),min(.003,width/5))
for side,x in CENTRES.items():
 prefix='Ski_'+side+'_';boardname=prefix+'Board';board(boardname,x);FEET.append(boardname)
 graphic(prefix+'FrontMark',x,-.790,-.395,.019)
 graphic(prefix+'TailBand',x,.585,.625,.078)
 graphic(prefix+'TailMark',x,.675,.755,.014)
 toe=prefix+'ToeRail';box(toe,(x,-.2375,.0315),(.078,.205,.019),3,'solid toe mounting rail rooted into ski top')
 link(toe,boardname,(x,-.245,.0227),(1,0,0),.018)
 body=prefix+'ToeHousing';prism_x(body,x-.038,x+.038,[(-.335,.039),(-.335,.061),(-.307,.082),(-.245,.086),(-.218,.071),(-.218,.039)],2,'chamfered closed toe binding housing')
 link(body,toe,(x,-.270,.040),(1,0,0),.018)
 for sign,label in [(-1,'Left'),(1,'Right')]:
  wing=prefix+'ToeWing_'+label
  prism_x(wing,x+sign*.032-.012,x+sign*.032+.012,[(-.237,.049),(-.237,.077),(-.209,.090),(-.168,.078),(-.168,.060),(-.207,.049)],2,'solid raised toe retaining wing, open space between wings')
  link(wing,body,(x+sign*.032,-.229,.063),(0,0,1),.004)
 pad=prefix+'ToeSolePad';box(pad,(x,-.160,.044),(.076,.048,.014),1,'low toe sole pad under the open visual boot bay, rail-end face inset')
 link(pad,toe,(x,-.163,.0395),(1,0,0),.018)
 heelrail=prefix+'HeelRail';box(heelrail,(x,.255,.030),(.078,.220,.018),3,'solid heel mounting rail rooted into ski top')
 link(heelrail,boardname,(x,.255,.0220),(1,0,0),.018)
 heel=prefix+'HeelHousing';prism_x(heel,x-.038,x+.038,[(.180,.037),(.180,.105),(.220,.135),(.290,.128),(.320,.090),(.320,.037)],2,'raised chamfered heel binding housing')
 link(heel,heelrail,(x,.250,.038),(1,0,0),.018)
 clamp=prefix+'HeelClamp';box(clamp,(x,.1765,.083),(.072,.063,.018),2,'forward-projecting closed heel retaining lip, side faces inset from housing')
 link(clamp,heel,(x,.195,.083),(1,0,0),.018)
 pad=prefix+'HeelSolePad';box(pad,(x,.155,.0435),(.070,.060,.014),1,'low heel sole pad leaving a visible empty boot space')
 link(pad,heelrail,(x,.165,.038),(1,0,0),.018)
 lever=prefix+'HeelReleaseLever';prism_x(lever,x-.0275,x+.0275,[(.275,.113),(.375,.068),(.382,.084),(.282,.132)],0,'fixed rearward release-lever silhouette; no release mechanism claim')
 link(lever,heel,(x,.287,.120),(1,0,0),.014)
 pivot=prefix+'HeelPivot';cyl_x(pivot,x-.047,x+.047,.242,.110,.010,3,'solid transverse fixed heel pivot',12)
 link(pivot,heel,(x,.242,.110),(1,0,0),.020)
 for sign,label in [(-1,'Left'),(1,'Right')]:
  pts=[(x+sign*.030,.245,.060),(x+sign*.064,.260,.060),(x+sign*.068,.190,.090),(x+sign*.068,.140,.090)]
  previous=None
  for i,(a,b) in enumerate(zip(pts[:-1],pts[1:])):
   name=prefix+'Brake_'+label+'_'+str(i+1);axis=unit(sub(b,a));rod(name,sub(a,mul(axis,.004)),add(b,mul(axis,.004)),.0055,3,'solid overlapping segment of raised static bent brake arm',10)
   if previous:link(name,previous,a,(1,0,0),.0012)
   else:link(name,heel,add(a,mul(unit(sub(b,a)),.004)),(0,0,1),.002)
   previous=name
 BOOT_BAYS.append({'ski':side,'centre_x_m':x,'x_interval_m':[x-.026,x+.026],'y_interval_m':[-.156,.140],'z_interval_m':[.055,.071],
  'limitation':'empty visual envelope only, not boot compatibility, insertion path or release specification'})
 BOARD_MEASUREMENTS.append({'board':boardname,'centre_x_m':x,'width_probes_y_m':[-.720,0,.700],
  'expected_widths_m':[.142,.084,.126],'tip_y_m':-.890,'waist_y_m':0,
  'expected_tip_sole_z_m':.108,'expected_tip_thickness_m':.0094,'expected_waist_sole_z_m':0,'expected_waist_thickness_m':.024})
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
for name,color,rough,metal in [('Teal_Topsheet',(.035,.32,.34,1),.63,.08),('Cream_MarksAndSolePads',(.79,.80,.65,1),.74,.02),('Graphite_BindingsAndSole',(.035,.045,.055,1),.77,.08),('PaleSteel_EdgesAndHardware',(.47,.54,.55,1),.47,.65)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('OnePairedAlpineSkiProduct',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# Finite support and sidecut/tip/boot-bay checks use actual generated mesh triangles.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.12,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
measurements=[]
for r in BOARD_MEASUREMENTS:
 tree=trees[r['board']];x=r['centre_x_m'];widths=[]
 for y,wanted in zip(r['width_probes_y_m'],r['expected_widths_m']):
  z=station(y)[1]+station(y)[2]/2
  l,_,_,_=tree.ray_cast(Vector((x-.2,y,z)),Vector((1,0,0)),.4);rr,_,_,_=tree.ray_cast(Vector((x+.2,y,z)),Vector((-1,0,0)),.4)
  assert l is not None and rr is not None;actual=rr.x-l.x;assert abs(actual-wanted)<3e-6,(r,actual);widths.append(actual)
 heights=[]
 for label,y in [('tip',r['tip_y_m']),('waist',r['waist_y_m'])]:
  lohit,_,_,_=tree.ray_cast(Vector((x,y,-.1)),Vector((0,0,1)),.5);hihit,_,_,_=tree.ray_cast(Vector((x,y,.3)),Vector((0,0,-1)),.5)
  assert lohit is not None and hihit is not None
  assert abs(lohit.z-r['expected_'+label+'_sole_z_m'])<3e-6
  assert abs(hihit.z-lohit.z-r['expected_'+label+'_thickness_m'])<3e-6
  heights.append({'label':label,'sole_z_m':lohit.z,'top_z_m':hihit.z,'thickness_m':hihit.z-lohit.z})
 measurements.append(dict(r,actual_widths_m=widths,actual_vertical_sections=heights))
boot_checks=[]
for b in BOOT_BAYS:
 rays=[];x=b['centre_x_m'];y0,y1=b['y_interval_m']
 for dx in [-.025,0,.025]:
  for z in [.056,.063,.070]:
   origin=Vector((x+dx,y0,z));direction=Vector((0,1,0));length=y1-y0
   blockers=[n for n,t in trees.items() if t.ray_cast(origin,direction,length)[0] is not None]
   assert not blockers,('Visual boot bay obstructed',b['ski'],dx,z,blockers)
   assert not any(inside(t,origin) for t in trees.values())
   rays.append({'origin_m':list(origin),'direction':[0,1,0],'length_m':length,'blockers':blockers})
 boot_checks.append(dict(b,actual_mesh_clear_rays=rays))
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
 'single_prop_pair_count':1,'ski_board_profile_y_halfwidth_solez_thickness_m':PROFILE,'sidecut_and_tip_actual_mesh_sections':measurements,'empty_visual_boot_bays':boot_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
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
focus=Vector((0,0,.070));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=2.02;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(3,-4,7),'gray-back3q':(-3,4,7)} if gray else {
 'thumbnail':(3,-4,7),'qa-front':(0,-7,.070),'qa-side':(7,0,.070),'qa-top':(0,0,8),
 'qa-back':(0,7,.070),'qa-wireframe':(3,-4,7)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=2.02
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00045;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.070)),('silhouette-128-side',(7,0,.070))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
