"""One original open-ended perforated U-channel cable tray visual module.
One 1.2 m repeat segment with two complete inset supports; no cable system.
Metres, Z up, long axis X, origin on ground under module center.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='renewable-perforated-cable-tray-straight-01';VERSION='1.0.0';TITLE='Perforated Straight Cable Tray'
DESCRIPTION=('One original low-poly straight cable-tray visual module: one continuous thick U-channel with fourteen genuinely through-cut rectangular bottom slots and fourteen through-cut sidewall slots, two completely open U-shaped ends, and two inset flared low supports with finite ground patches. The full welded channel has real hole walls and a clear full-length open interior. Satin light silver channel and dark petrol supports use two constant opaque PBR materials. '
 'Exact 1.2 metre X repeat pitch for this same complete module only: opposing matching U-end faces make finite geometric contact, while every other surface stays in its own half-space and the inset supports remain separated. This does not establish joint strength or compatibility with other assets. One segment counts as one modular asset; a second translated validation instance is neither exported nor counted. Metres, Z up, front -Y, origin at ground under the segment center. '
 'Static empty visual geometry only. No cables, wires, windings, electrical equipment, power or communication system, electrical continuity, insulation, fire or water resistance, cooling, grounding, loads, span or structural strength, construction, engineering or electrical safety certification. No old turbine, solar rack or communications-device fit claim. No bends, corners, vertical joins, scenes, textures or branding.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};SLOTS=[]
PALETTE=[('Channel_SatinSilver',(.56,.65,.67,1),.36,.72),('Supports_DeepPetrol',(.035,.105,.115,1),.52,.45)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(0,1,0),spread=.02):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':role}
# Boundary of an exact structured-cell solid, with shared vertices and internal
# faces removed. The final result is ONE welded closed perforated U-solid;
# empty cells are genuine through-holes, never dark surface patches.
CENTERS=[-.48,-.32,-.16,0,.16,.32,.48]
XS=sorted(set([-.6,.6]+[round(c+d,7) for c in CENTERS for d in [-.045,.045]]))
YS=[-.18,-.17,-.11,-.05,.05,.11,.17,.18]
ZS=[.09,.10,.16,.205,.27]
occupied=set()
for i in range(len(XS)-1):
 for j in range(len(YS)-1):
  for k in range(len(ZS)-1):
   x=(XS[i]+XS[i+1])/2;y=(YS[j]+YS[j+1])/2;z=(ZS[k]+ZS[k+1])/2
   inslot=any(abs(x-c)<.045-1e-9 for c in CENTERS)
   bottom=z<.10 and not (inslot and .05<abs(y)<.11)
   side=abs(y)>.17 and not (inslot and .16<z<.205)
   if bottom or side:occupied.add((i,j,k))
vs=[];faces=[];index={}
def vtx(p):
 p=tuple(round(x,7) for x in p)
 if p not in index:index[p]=len(vs);vs.append(p)
 return index[p]
for i,j,k in sorted(occupied):
 v=cuboid((XS[i],YS[j],ZS[k]),(XS[i+1],YS[j+1],ZS[k+1]))
 for neighbor,f in [((i,j,k-1),BOX_FACES[0]),((i,j,k+1),BOX_FACES[1]),((i,j-1,k),BOX_FACES[2]),((i,j+1,k),BOX_FACES[3]),((i-1,j,k),BOX_FACES[4]),((i+1,j,k),BOX_FACES[5])]:
  if neighbor not in occupied:faces.append(tuple(vtx(v[q]) for q in f))
tray=mesh('Tray_ContinuousPerforatedU',vs,faces,0,'one welded closed U-channel solid; 14 bottom and 14 side true slots; both ends fully open')
# A low transverse flared pedestal supports an unperforated web. Its top is
# embedded 4 mm into the 10 mm floor. Nothing enters the clear channel.
for number,x in enumerate([-.4,.4],1):
 yz=[(-.22,0),(.22,0),(.22,.018),(.173,.018),(.15,.094),(-.15,.094),(-.173,.018),(-.22,.018)]
 v=[(x+dx,y,z) for dx in [-.026,.026] for y,z in yz];n=len(yz)
 f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 support=mesh(f'Support_InsetFlared_{number:02d}',v,f,1,'complete short flared transverse support, finite grounded foot, top embedded in intact bottom web')
 FEET.append(support);link(tray,support,(x,0,.092),spread=.10)
# Finite open volumes have 1 mm clearance to actual slot walls. Each extends
# beyond BOTH wall faces. The uninterrupted channel probe extends past both ends.
void('Channel_FullLengthOpenVoid',(-.605,-.169,.101),(.605,.169,.275),'finite complete open U-channel volume across both ends and above sidewalls')
for i,x in enumerate(CENTERS,1):
 for j,y in enumerate([-.08,.08],1):
  name=f'BottomSlot_{i:02d}_{j:02d}';lo=(x-.044,y-.029,.085);hi=(x+.044,y+.029,.105)
  void(name,lo,hi,'full thickness bottom slot with positive wall clearance');SLOTS.append({'name':name,'wall_axis':2,'center':(x,y,.095),'wall_faces':[.09,.10],'opening_widths_m':[.09,.06]})
  GAPS.append({'origin_m':(x,y,.08),'direction':(0,0,1),'length_m':.04,'meaning':name+' supplementary axial through-ray'})
 for j,side in enumerate([-1,1],1):
  name=f'SideSlot_{i:02d}_{j:02d}';lo=(x-.044,min(side*.185,side*.165),.161);hi=(x+.044,max(side*.185,side*.165),.204)
  void(name,lo,hi,'full thickness sidewall slot with positive wall clearance');SLOTS.append({'name':name,'wall_axis':1,'center':(x,side*.175,.1825),'wall_faces':sorted([side*.17,side*.18]),'opening_widths_m':[.09,.045]})
  GAPS.append({'origin_m':(x,side*.185,.1825),'direction':(0,-side,0),'length_m':.03,'meaning':name+' supplementary transverse through-ray'})
GAPS.append({'origin_m':(-.605,0,.185),'direction':(1,0,0),'length_m':1.21,'meaning':'supplementary full-channel axial ray across both open ends'})
CABLE_TRAY_CONTRACT={'tray':tray,'supports':FEET,'repeat_axis':'X','repeat_translation_m':[1.2,0,0],'end_planes_m':[-.6,.6],'bottom_z_m':[.09,.10],'inside_y_m':[-.17,.17],'wall_top_z_m':.27,'slot_count':28,'bottom_slot_count':14,'side_slot_count':14,'allowed_repeat_contact':'matching full U end faces only; no other part can contact','support_to_end_setback_m':.174,'static_visual_only':True}
def measure_cable_tray_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 bounds=lambda n:([min(float(p[k]) for p in vertices[n]) for k in range(3)],[max(float(p[k]) for p in vertices[n]) for k in range(3)])
 lo,hi=bounds(tray);expected=[(-.6,.6),(-.18,.18),(.09,.27)]
 assert all(abs(lo[k]-a)<1e-6 and abs(hi[k]-b)<1e-6 for k,(a,b) in enumerate(expected)),('Tray bounds',lo,hi)
 for name,x in zip(FEET,[-.4,.4]):
  a,b=bounds(name);assert abs(a[2])<1e-7 and abs(b[2]-.094)<1e-7
  assert abs(a[0]-(x-.026))<1e-6 and abs(b[0]-(x+.026))<1e-6,('Support displaced',name)
 return {'single_modular_asset_count':1,'complete_support_count':len(FEET),'repeat_pitch_m':1.2,'wall_thickness_m':.01,'bottom_slot_count':14,'side_slot_count':14,'channel_clear_width_m':.34,'channel_floor_to_rim_m':.17,'support_end_setback_m':.174,'nearest_repeated_support_gap_m':.348,'cable_or_electrical_or_safety_claim':False}
FOCUS=(0,0,.13);ORTHO=1.55
CAMERAS={'gray-front3q':(1.65,-2.2,1.8),'gray-back3q':(-1.65,2.2,1.8),'thumbnail':(1.65,-2.2,1.8),'qa-front':(0,-3,1.10),'qa-side':(3,0,1.10),'qa-top':(0,0,3),'qa-back':(0,3,1.10),'qa-wireframe':(1.65,-2.2,1.8),'silhouette-128-front':(0,-3,1.10),'silhouette-128-side':(3,0,1.10)}
WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OnePerforatedCableTray',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground X midline, Y=0, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};actual_triangles={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 actual_triangles[id(trees[o.name])]=[[tuple(float(c) for c in (o.matrix_world@o.data.vertices[i].co)) for i in t.vertices] for t in o.data.loop_triangles]
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in [(tray,(0,0,.095),(0,.08,.095)),(FEET[0],(-.4,0,.04),(-.4,.21,.06))]:
 assert inside(trees[name],p) is True
 assert inside(trees[name],outside) is False
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})
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
mount_evidence=measure_cable_tray_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_asset_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'cable_tray_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/renewable/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'renewable','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=WIRE_THICKNESS;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
