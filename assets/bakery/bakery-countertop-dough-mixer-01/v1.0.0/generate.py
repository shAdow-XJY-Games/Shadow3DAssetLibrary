"""Original static countertop dough mixer. Metres, Z up, front -Y.
Open thick bowl has real flat support and a separate bent dough hook with measured clearance.
One fixed visual pose only. No mixing, food-contact, motion or operating-safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='bakery-countertop-dough-mixer-01';VERSION='1.0.0';TITLE='Countertop Dough Mixer with Open Bowl'
DESCRIPTION=('Original static low-poly countertop dough mixer with a broad four-foot base, a continuous rear column and an overhanging cream motor head. '
 'A separately editable thick open metal bowl sits on a finite raised support seat. A vertical shaft and one continuous curved dough hook descend from the head into the genuinely empty bowl, with independently measured wall and floor clearance. '
 'A raised charcoal control knob is a fixed visual detail. Five constant PBR materials, named editable closed components, metres, source Z up, front -Y and ground-centre origin. '
 'One reusable prop without dough, food, textures, external assets or scene. Distinct from the old hand bowl and mortar or a wall-paddle construction drum. '
 'One checked static pose only: no mixing or kneading performance, food contact, hygiene, electrical operation, head lifting, shaft motion, continuous rotation, heat, load, manufacture or operating-safety certification.')
G={};LINKS=[];SPINES={};FEET=[];VOID_RAYS=[];BOWL='OpenMixingBowl';HOOK='CurvedDoughHook';SHAFT='DriveShaft';SUPPORT='BowlSupportSeat'
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
def box(name,loc,size,material,role):
 vs=[add(loc,(sx*size[0]/2,sy*size[1]/2,sz*size[2]/2)) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,role)
def chamferbox(name,loc,size,bevel,material,role):
 x,y,z=size; e=bevel
 def ring(h,shrink):
  hx=x/2-shrink;hy=y/2-shrink;c=max(e-shrink,.0005)
  return [add(loc,(a,b,h)) for a,b in [(-hx+c,-hy),(hx-c,-hy),(hx,-hy+c),(hx,hy-c),(hx-c,hy),(-hx+c,hy),(-hx,hy-c),(-hx,-hy+c)]]
 vs=ring(-z/2,e*.65)+ring(-z/2+e,0)+ring(z/2-e,0)+ring(z/2,e*.65);fs=[tuple(reversed(range(8))),tuple(24+i for i in range(8))]
 for k in range(3):
  for i in range(8):j=(i+1)%8;fs.append((k*8+i,k*8+j,(k+1)*8+j,(k+1)*8+i))
 return mesh(name,vs,fs,material,role)
def rod(name,a,b,radius,material,role,n=24):
 axis=unit(sub(b,a));ref=(0,0,1) if abs(axis[2])<.9 else (1,0,0);u=unit(cross(axis,ref));v=unit(cross(axis,u))
 vs=[add(p,mul(add(mul(u,math.cos(math.tau*i/n)),mul(v,math.sin(math.tau*i/n))),radius)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 SPINES[name]=(a,b);return mesh(name,vs,fs,material,role)
def lathe(name,profile,centre,material,role,n=32):
 vs=[];rings=[]
 for r,z in profile:
  if r==0:rings.append([len(vs)]);vs.append((centre[0],centre[1],z))
  else:rings.append(list(range(len(vs),len(vs)+n)));vs.extend((centre[0]+r*math.cos(math.tau*i/n),centre[1]+r*math.sin(math.tau*i/n),z) for i in range(n))
 fs=[]
 for a,b in zip(rings,rings[1:]):
  for i in range(n):
   j=(i+1)%n
   if len(a)==1:fs.append((a[0],b[j],b[i]))
   elif len(b)==1:fs.append((a[i],a[j],b[0]))
   else:fs.append((a[i],a[j],b[j],b[i]))
 return mesh(name,vs,fs,material,role)
def sweep(name,path,radius,material,role,n=12):
 vs=[]
 for i,p in enumerate(path):
  t=unit(sub(path[min(i+1,len(path)-1)],path[max(0,i-1)]));u=unit(cross(t,(0,1,0)));v=unit(cross(t,u))
  vs.extend(add(p,mul(add(mul(u,math.cos(math.tau*j/n)),mul(v,math.sin(math.tau*j/n))),radius)) for j in range(n))
 fs=[tuple(reversed(range(n))),tuple((len(path)-1)*n+j for j in range(n))]
 for k in range(len(path)-1):
  for j in range(n):jj=(j+1)%n;fs.append((k*n+j,k*n+jj,(k+1)*n+jj,(k+1)*n+j))
 return mesh(name,vs,fs,material,role)
def bezier(a,b,c,d,steps):
 return [add(add(mul(a,(1-t)**3),mul(b,3*(1-t)**2*t)),add(mul(c,3*(1-t)*t*t),mul(d,t**3))) for t in [i/steps for i in range(steps+1)]]
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
# Four real flat feet enter the broad base, which supports the rear column and bowl seat.
for x,side in [(-.139,'Left'),(.139,'Right')]:
 for y,end in [(-.212,'Front'),(.204,'Back')]:
  name='RubberFoot_'+side+end
  chamferbox(name,(x,y,.020),(.075,.080,.040),.006,3,'flat grounded rubber foot with finite contact patch');FEET.append(name)
  link(name,'MixerBase',(x,y,.033),(1,0,0),.014)
chamferbox('MixerBase',(0,-.005,.059),(.390,.565,.068),.018,0,'broad low base connects four feet, bowl support and rear column')
chamferbox('RearColumn',(0,.180,.294),(.151,.165,.444),.017,0,'continuous back column enters base and supports overhanging motor head')
link('RearColumn','MixerBase',(0,.180,.083),(1,0,0),.029)
chamferbox('MotorHead',(0,.060,.535),(.220,.445,.142),.025,1,'single overhead motor housing supported by rear column; one fixed pose')
link('RearColumn','MotorHead',(0,.180,.494),(1,0,0),.029)
# Seat overlaps the solid floor in a finite disk, not an unsupported floating bowl.
rod(SUPPORT,(0,-.122,.082),(0,-.122,.119),.092,0,'finite circular bowl support seat entering base and bowl bottom',32)
link(SUPPORT,'MixerBase',(0,-.122,.088),(1,0,0),.040)
BOWL_PROFILE=[(0,.110),(.081,.110),(.098,.128),(.126,.194),(.148,.279),(.159,.365),(.163,.379),(.157,.389),(.149,.383),(.145,.365),(.134,.279),(.113,.199),(.082,.141),(.067,.133),(0,.133)]
lathe(BOWL,BOWL_PROFILE,(0,-.122),2,'continuous closed thick metal bowl, rolled rim, real floor and open cavity',32)
link(BOWL,SUPPORT,(0,-.122,.1145),(1,0,0),.040)
# Separate shaft is visibly seated into head; its independent hook has a clear J-shaped curl.
rod('DriveCollar',(0,-.122,.443),(0,-.122,.481),.029,2,'solid raised metal collar beneath head',24)
link('DriveCollar','MotorHead',(0,-.122,.475),(1,0,0),.010)
rod(SHAFT,(0,-.122,.350),(0,-.122,.475),.0135,2,'fixed vertical drive spindle from head collar into the hook',24)
link(SHAFT,'DriveCollar',(0,-.122,.459),(1,0,0),.006)
HOOK_PATH=bezier((0,-.122,.374),(0,-.122,.319),(.068,-.122,.306),(.069,-.122,.243),14)
HOOK_PATH+=bezier((.069,-.122,.243),(.071,-.122,.179),(-.034,-.148,.164),(-.055,-.148,.186),14)[1:]
sweep(HOOK,HOOK_PATH,.0105,2,'single solid continuous curved dough hook entering the empty bowl with wall and floor clearance',12)
link(HOOK,SHAFT,(.0005,-.122,.362),(1,0,0),.003)
# The control is a physical protrusion, not a flat label; it does not imply an operative mechanism.
rod('ControlKnob',( .102,.133,.536),(.136,.133,.536),.027,3,'fixed charcoal side control dial, raised from the head',16)
link('ControlKnob','MotorHead',(.106,.133,.536),(0,1,0),.008)
rod('ControlCentre',(.131,.133,.536),(.140,.133,.536),.009,4,'small raised coral dial centre; static visual accent',12)
link('ControlCentre','ControlKnob',(.134,.133,.536),(0,1,0),.003)
# Empty cavity sight lines lie well away from the hook and are tested against every mesh.
for x,y in [(-.095,-.122),(.095,-.122),(0,-.218),(0,-.030)]:
 VOID_RAYS.append({'label':'open bowl side-of-hook ray','origin_m':(x,y,.430),'direction':(0,0,-1),'length_m':.180})
vv=[v for g in G.values() for v in g['vertices']];lo=[min(v[k] for v in vv) for k in range(3)];hi=[max(v[k] for v in vv) for k in range(3)]
SHIFT=(-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2])
for g in G.values():g['vertices']=[add(v,SHIFT) for v in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT) for p in points]) for a,b,points in LINKS]
for r in VOID_RAYS:r['origin_m']=add(r['origin_m'],SHIFT)
HOOK_PATH=[add(p,SHIFT) for p in HOOK_PATH]
BOWL_CENTRE=add((0,-.122,0),SHIFT)
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
for name,color,rough,metal in [('Seafoam_Enamel',(.065,.32,.29,1),.48,.22),('WarmCream_Head',(.77,.70,.53,1),.44,.12),('SatinSteel_BowlAndHook',(.46,.53,.55,1),.34,.78),('Charcoal_Rubber',(.025,.035,.037,1),.78,0),('Coral_ControlCentre',(.68,.12,.065,1),.53,.10)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('CountertopDoughMixer',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
voids=[]
for r in VOID_RAYS:
 p=Vector(r['origin_m']);d=Vector(r['direction']);blockers=[n for n,t in trees.items() if t.ray_cast(p,d,r['length_m'])[0] is not None or inside(t,p)]
 assert not blockers,('Blocked functional recess',r,blockers)
 voids.append(dict(r,blockers=blockers))
# Actual mesh vertex-to-triangle distances plus surface crossing and containment checks.
bowl_tree=trees[BOWL];hook_tree=trees[HOOK]
clearance_rows=[]
for name in [HOOK,SHAFT]:
 obj=byname[name];nearest=[bowl_tree.find_nearest(obj.matrix_world@v.co)[3] for v in obj.data.vertices]
 reverse=[trees[name].find_nearest(byname[BOWL].matrix_world@v.co)[3] for v in byname[BOWL].data.vertices]
 minimum=min(nearest+reverse)
 overlaps=bowl_tree.overlap(trees[name])
 contained=[i for i,v in enumerate(obj.data.vertices) if inside(bowl_tree,obj.matrix_world@v.co)]
 assert minimum>.018 and not overlaps and not contained,('Bowl collision/clearance',name,minimum,overlaps,contained)
 clearance_rows.append({'part':name,'bowl':BOWL,'minimum_bidirectional_vertex_triangle_distance_m':minimum,'surface_triangle_intersections':len(overlaps),'part_vertices_inside_bowl_solid':len(contained),'claim':'actual mesh sampled clearance in this one fixed pose; no continuous-motion claim'})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<6000
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
 'normalization_shift_m':SHIFT,'functional_recess_rays':voids,'bowl_hook_static_clearance':clearance_rows,
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
focus=Vector((0,0,.295));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.84;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4.6,-6.3,13.0),'gray-back3q':(-4.6,6.3,5.5)} if gray else {
 'thumbnail':(4.6,-6.3,13.0),'qa-front':(0,-7,.295),'qa-side':(7,0,.295),'qa-top':(0,0,8),
 'qa-back':(0,7,.295),'qa-wireframe':(4.6,-6.3,13.0)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=.96 if name in ['gray-front3q','thumbnail','qa-wireframe'] else .84
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0004;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.295)),('silhouette-128-side',(7,0,.295))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
