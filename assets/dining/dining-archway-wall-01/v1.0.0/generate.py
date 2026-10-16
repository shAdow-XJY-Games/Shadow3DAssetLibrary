"""Original dining architecture module. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='dining-archway-wall-01'
TITLE='Maple Archway Wall'
DESCRIPTION='Original 1.4 m grid architectural module with a real open arched doorway, maple reveal and seafoam threshold. Repeat wall instances along X at 1.4 m spacing, Z up. Maple trim faces -Y. Overall wall height is 2.4 m; structural opening width 0.9 m and crown 2.1 m; maple reveals leave 0.844 m clear width at the straight jambs. Each module is complete and needs no shared-part deletion.'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(0.48,0.255,0.105,1),'sand':(0.86,0.75,0.52,1),'teal':(0.19,0.40,0.35,1)}
mats={}
for name,col in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.83
 mats[name]=m
parts=[]
def box(name,loc,scale,mat='honey',bevel=.018,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]);b=o.modifiers.new('Soft hand-cut edge','BEVEL');b.width=bevel;b.segments=1
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 parts.append(o);return o

def mesh(name,verts,faces,material):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats[material]);parts.append(o);return o
def lathe(name,profile,mat='teal',n=32):
 cyclic=profile[0]==profile[-1]
 if cyclic:profile=profile[:-1]
 verts=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for r,z in profile for i in range(n)]
 faces=[]
 for k in range(len(profile) if cyclic else len(profile)-1):
  nxt=(k+1)%len(profile)
  for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,nxt*n+(i+1)%n,nxt*n+i))
 if not cyclic:faces.extend([tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))])
 return mesh(name,verts,faces,mat)
def tube(name,points,radius,mat='honey',sides=8,cyclic=False):
 verts=[];faces=[]
 axis=min(range(3),key=lambda a:max(p[a] for p in points)-min(p[a] for p in points))
 ref=Vector(tuple(1 if a==axis else 0 for a in range(3)))
 for i,p in enumerate(points):
  tangent=Vector(points[(i+1)%len(points)])-Vector(points[(i-1)%len(points)]) if cyclic else Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
  tangent.normalize();n=tangent.cross(ref)
  if n.length<.001:n=tangent.cross(Vector((1,0,0)))
  n.normalize();bn=tangent.cross(n).normalized()
  for j in range(sides):verts.append(Vector(p)+radius*(math.cos(j*math.tau/sides)*n+math.sin(j*math.tau/sides)*bn))
 for i in range(len(points) if cyclic else len(points)-1):
  for j in range(sides):faces.append((i*sides+j,((i+1)%len(points))*sides+j,((i+1)%len(points))*sides+(j+1)%sides,i*sides+(j+1)%sides))
 if not cyclic:faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
 return mesh(name,verts,faces,mat)

def extruded_outline(name,outline,depth,material):
 from mathutils.geometry import tessellate_polygon
 pts=[Vector((x,0,z)) for x,z in outline];N=len(pts)
 verts=[(x,y,z) for y in [-depth/2,depth/2] for x,z in outline];faces=[]
 for tri in tessellate_polygon([pts]):
  ids=tuple(v if isinstance(v,int) else min(range(N),key=lambda k:(pts[k]-v).length) for v in tri)
  faces.extend([ids,tuple(N+i for i in reversed(ids))])
 for i in range(N):faces.append((i,(i+1)%N,(i+1)%N+N,i+N))
 return mesh(name,verts,faces,material)

outline=[(-.7,0),(-.7,2.4),(.7,2.4),(.7,0),(.45,0),(.45,1.65)]
outline += [(.45*math.cos(i*math.pi/12),1.65+.45*math.sin(i*math.pi/12)) for i in range(1,13)]
outline += [(-.45,0)]
extruded_outline('Ivory arch wall',outline,.16,'sand')
points=[(.45,-.08,.025),(.45,-.08,1.65)]+[(.45*math.cos(i*math.pi/12),-.08,1.65+.45*math.sin(i*math.pi/12)) for i in range(1,13)]+[(-.45,-.08,.025)]
tube('Maple arch reveal front',points,.028,'honey',8)
tube('Maple arch reveal rear',[(x,-y,z) for x,y,z in points],.028,'honey',8)
box('Seafoam threshold',(0,0,.025),(1.36,.2,.05),'teal',.008)
# Normalize winding per closed component before export.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# All mesh origins at the common bottom-center; keep parts separate for editing.
scene.cursor.location=(0,0,0)
for o in parts:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
# Normalize exact full-asset bottom-center after all component transforms.
coords=[v.co.copy() for o in parts for v in o.data.vertices]
shift=Vector(((min(v.x for v in coords)+max(v.x for v in coords))/2,(min(v.y for v in coords)+max(v.y for v in coords))/2,min(v.z for v in coords)))
for o in parts:
 for v in o.data.vertices:v.co-=shift
from mathutils.bvhtree import BVHTree
import itertools
objs=[o for o in bpy.context.scene.objects if o.type=='MESH'];cache={}
for o in objs:
 assert not o.modifiers, 'Unapplied modifiers: '+o.name
 o.data.calc_loop_triangles();vs=[o.matrix_world@v.co for v in o.data.vertices];fs=[tuple(t.vertices) for t in o.data.loop_triangles]
 cache[o.name]=(BVHTree.FromPolygons(vs,fs,all_triangles=True),Vector([min(v[a] for v in vs) for a in range(3)]),Vector([max(v[a] for v in vs) for a in range(3)]))
clearance=.002
directions=[Vector((1,.371,.529)).normalized(),Vector((.263,1,.619)).normalized(),Vector((.419,.233,1)).normalized()]
def inside(tree,point):
 results=[]
 for d in directions:
  origin=point.copy();count=0
  for _ in range(100):
   loc,norm,idx,dist=tree.ray_cast(origin,d,100)
   if loc is None:break
   # Advance 10 micrometers to avoid float32 re-hitting the same face at distance -0.0.
   # This is 50x smaller than even the smallest required 0.5mm clearance.
   count+=1;origin=loc+d*1e-5
  else:raise RuntimeError('Ray parity uncertain: 100 hits exceeded')
  results.append(count%2==1)
 return all(results)
def anchors(a,b):
 ta,la,ha=cache[a.name];tb,lb,hb=cache[b.name]
 lo=Vector([max(la[i],lb[i]) for i in range(3)]);hi=Vector([min(ha[i],hb[i]) for i in range(3)])
 if min(hi-lo)<2*clearance: return []
 good=[]
 for uvw in itertools.product([.05,.2,.35,.5,.65,.8,.95],repeat=3):
  v=Vector([lo[i]+uvw[i]*(hi[i]-lo[i]) for i in range(3)])
  da=ta.find_nearest(v)[3];db=tb.find_nearest(v)[3]
  if min(da,db)<clearance or not inside(ta,v) or not inside(tb,v):continue
  if any((v-Vector(q['world_anchor_m'])).length<.002 for q in good):continue
  good.append({'world_anchor_m':list(v),'surface_clearance_a_m':da,'surface_clearance_b_m':db,'three_ray_inside_a':True,'three_ray_inside_b':True})
  if len(good)>=3:return good
 return good
checks=[]
def relation(ap,bp,count=1):
 assert any(o.name.startswith(ap) for o in objs), 'Missing required A: '+ap
 assert any(o.name.startswith(bp) for o in objs), 'Missing required B: '+bp
 for a in [o for o in objs if o.name.startswith(ap)]:
  contacts=[]
  for b in [o for o in objs if o.name.startswith(bp)]:
   pts=anchors(a,b)
   if len(pts)>=3:contacts.append({'part_b':b.name,'mode':'overlap','anchors':pts})
  checks.append({'part_a':a.name,'required_b_prefix':bp,'minimum_contacts':count,'contacts':contacts,'pass':len(contacts)>=count})
def manual_relation(ap,bp,points_fn):
 aa=[o for o in objs if o.name.startswith(ap)];bb=[o for o in objs if o.name.startswith(bp)]
 assert aa and len(bb)==1, 'Missing or ambiguous declared contact parts'
 b=bb[0]
 for a in aa:
  pts=[];all_good=True
  for raw in points_fn(a.name):
   v=Vector(raw);ta=cache[a.name][0];tb=cache[b.name][0];da=ta.find_nearest(v)[3];db=tb.find_nearest(v)[3];ia=inside(ta,v);ib=inside(tb,v)
   passed=ia and ib and min(da,db)>=clearance;all_good &= passed
   pts.append({'world_anchor_m':list(v),'surface_clearance_a_m':da,'surface_clearance_b_m':db,'three_ray_inside_a':ia,'three_ray_inside_b':ib,'pass':passed})
  checks.append({'part_a':a.name,'required_b_prefix':bp,'minimum_contacts':1,'contacts':[{'part_b':b.name,'mode':'overlap','anchors':pts}],'pass':all_good and len(pts)>=3})

manual_relation('Maple arch reveal','Ivory arch wall',lambda name:[(x,.066 if 'rear' in name else -.066,z) for x in [-.46,.46] for z in [.7,1.0,1.3]])
manual_relation('Maple arch reveal','Seafoam threshold',lambda name:[(.45,.075 if 'rear' in name else -.075,z) for z in [.032,.038,.044]])
relation('Seafoam threshold','Ivory arch wall')
assert checks and all(c['pass'] for c in checks), 'Required structural contact failed'
fingerprint=hashlib.sha256(json.dumps([(o.name,[list(o.matrix_world@v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in objs],sort_keys=True).encode()).hexdigest()
connection_report={'method':'Evaluated triangles, 3 ray parity directions and at least 3 separate overlap anchors per edge','minimum_inside_clearance_m':clearance,'evaluated_mesh_sha256':fingerprint,'checks':checks,'passed':True}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 assert not any(not e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)>0, o.name
 bm.free()

# Join only for export to reduce runtime draw calls; restore editable components afterwards.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.duplicate();export_parts=list(bpy.context.selected_objects);bpy.ops.object.join();model=bpy.context.object;model.name=ASSET
model.data.calc_loop_triangles();triangles=len(model.data.loop_triangles)
bounds=[round(v,5) for v in model.dimensions]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(model,do_unlink=True)
# Persist clean source before adding the non-exported presentation rig.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Geometry and format QA. Components closed; deliberate plank overlaps are allowed.
import bmesh
bad=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
assert 100<=triangles<=6000,triangles
assert bounds[2]>0 and min(v.co.z for o in parts for v in o.data.vertices)>-1e-5
assert (OUT/'model.glb').stat().st_size<500000
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.world.color=(.32,.32,.32)
scene.view_settings.view_transform='AgX'
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(bounds)*1.65
focus=Vector((0,0,bounds[2]*.48))
def point(o,xyz):o.location=xyz;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),180,3),('Rim',(1,4,5),300,3)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;point(light,xyz)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview ground (not asset)'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
views={'thumbnail':(3,-4,2.8),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-back':(3,4,2.8),'qa-wireframe':(3,-4,2.8)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  for o in parts:
   o.data.materials.append(wiremat)
   wire=o.modifiers.new('QA edge overlay','WIREFRAME');wire.thickness=.0025;wire.use_replace=False;wire.offset=1;wire.material_offset=len(o.data.materials)-1
 scene.cycles.samples=512 if name=='thumbnail' else 128
 point(cam,tuple(focus+Vector(xyz)-Vector((0,0,0))) if name in ['thumbnail','qa-back','qa-wireframe'] else xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/dining/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'props','assetKind':'modular','theme':'dining','style':'soft-low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':3,'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'bottom center 0,0,0','transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
qa['modularity']={'origin': 'Exact full-asset bottom center at 0,0,0. Wall center plane is Y=0; symmetric front/back reveals preserve common wall alignment. Floor instances align on X/Y grid; place walls at Z=0.045 when supported on finished floor tiles.', 'connection_points_m': {'left': [-0.7, 0, 0], 'right': [0.7, 0, 0], 'top': [0, 0, 2.4]}, 'grid_step_m': {'x': 1.4}, 'assembly': 'Repeat wall instances along X at 1.4 m spacing, Z up. Maple trim faces -Y. Overall wall height is 2.4 m; structural opening width 0.9 m and crown 2.1 m; maple reveals leave 0.844 m clear width at the straight jambs. Each module is complete and needs no shared-part deletion.'}
qa['connections']=connection_report
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
