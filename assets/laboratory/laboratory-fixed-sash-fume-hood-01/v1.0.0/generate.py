"""Original fixed half-raised opaque-sash laboratory fume-hood visual prop.
Metres, Z up, front -Y. One benchtop body with genuine empty chamber and gaps.
No ventilation, filtration, protection, chemistry, movement or safety claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-fixed-sash-fume-hood-01';VERSION='1.0.0';TITLE='Fixed-Sash Laboratory Fume Hood'
DESCRIPTION=('Original standalone benchtop laboratory fume-hood visual prop in one static half-raised opaque-sash pose. Thick sidewalls, rear wall, roof frame and a solid dark work deck surround a genuinely empty chamber. '
 'A separate raised rear baffle has real lower, upper and side slots and a finite open gap behind it, with four embedded rear standoffs. Two thick U-section side guides carry actual stop blocks supporting the fixed opaque blue sash; its separate handle has two embedded seats. '
 'A short square roof collar has a real wall and aperture continuous with the roof opening. All parts have explicit finite geometric support routes to the broad flat base. Twenty independently editable closed meshes with four constant fully opaque solid PBR materials. '
 'One original prop, metre scale, source Z up, front -Y, base-centre origin. No textures, logo, equipment, table, samples, chemicals, fluid, fan, hose, people, animation or reused geometry. '
 'Static stylized visual only: no working ventilation, exhaust, airflow, filtration, explosion resistance, chemical or biological isolation, personnel protection, experimental procedure, sash movement, installation compatibility, material resistance, manufacturing, certification or safety compliance. Not real equipment design or use guidance.')
G={};LINKS=[];FEET=['Base_SolidWorkDeck'];BORES=[];GAPS=[];FLOOR_PROBES=[];WALL_PROBES=[];VOID_VOLUMES={}
PALETTE=[('Shell_WarmIvory',(.68,.72,.69,1),.70,.02),('Deck_Graphite',(.10,.135,.15,1),.68,.04),('Sash_OpaqueMutedBlue',(.20,.35,.43,1),.60,.04),('Hardware_Slate',(.21,.27,.29,1),.50,.32)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'sash':'solid opaque colored panel as required by fixed source brief; no glass or transparency claim'}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],BOX_FACES

def box(name,lo,hi,mat,role):return mesh(name,*box_geometry(lo,hi),mat,role)
def void(name,lo,hi,role):
 vs,fs=box_geometry(lo,hi);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'role':role}
def frame(name,outer,inner,z0,z1,mat,role):
 def corners(r,z):a,b,c,d=r;return [(a,b,z),(c,b,z),(c,d,z),(a,d,z)]
 vs=corners(outer,z0)+corners(inner,z0)+corners(outer,z1)+corners(inner,z1);fs=[]
 for i in range(4):
  j=(i+1)%4;fs += [(i,j,j+8,i+8),(i+4,i+12,j+12,j+4),(i+8,j+8,j+12,i+12),(i+4,j+4,j,i)]
 return mesh(name,vs,fs,mat,role)
box('Base_SolidWorkDeck',(-.625,-.395,0),(.625,.395,.085),1,'thick closed work deck and broad finite ground contact; no external table or load claim')
for side,sgn in [('Left',-1),('Right',1)]:
 lo,hi=sorted([sgn*.535,sgn*.605]);box('Shell_'+side,(lo,-.375,.065),(hi,.375,1.125),0,'thick enclosing sidewall seated in the base and roof')
 link('Shell_'+side,'Base_SolidWorkDeck',(sgn*.57,0,.075))
box('Shell_RearWall',(-.565,.325,.06),(.565,.39,1.135),0,'thick independent rear wall behind the open rear-baffle gap')
link('Shell_RearWall','Base_SolidWorkDeck',(0,.355,.072),axis=(1,0,0),spread=.1)
for side,sgn in [('Left',-1),('Right',1)]:link('Shell_RearWall','Shell_'+side,(sgn*.55,.35,.7),axis=(0,0,1),spread=.1)
frame('Roof_TrueOpenFrame',(-.63,-.395,.63,.415),(-.115,.015,.115,.245),1.095,1.17,0,'thick roof with actual central rectangular through aperture, not a painted inlet')
for side,sgn in [('Left',-1),('Right',1)]:link('Roof_TrueOpenFrame','Shell_'+side,(sgn*.57,0,1.11))
link('Roof_TrueOpenFrame','Shell_RearWall',(0,.35,1.115),axis=(1,0,0),spread=.1)
frame('Roof_ShortOpenCollar',(-.135,-.005,.135,.265),(-.105,.025,.105,.235),1.155,1.30,3,'short square hollow roof collar continuous with true roof aperture; static outer shape, no functioning duct claim')
link('Roof_ShortOpenCollar','Roof_TrueOpenFrame',(.124,.13,1.162),spread=.025)
# Each guide is one genuinely thick U-profile extrusion, open toward the sash.
track=[(-.562,-.374),(-.503,-.374),(-.503,-.354),(-.537,-.354),(-.537,-.318),(-.503,-.318),(-.503,-.302),(-.562,-.302)]
for side,sgn in [('Left',-1),('Right',1)]:
 profile=[((-x if sgn==1 else x),y) for x,y in track];n=len(profile)
 vs=[(x,y,z) for z in [.10,1.118] for x,y in profile];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 guide='Guide_'+side+'_UChannel';mesh(guide,vs,fs,3,'closed U-channel with actual clearance on either side of the opaque sash; fixed pose only')
 link(guide,'Shell_'+side,(sgn*.55,-.34,.8),axis=(0,0,1),spread=.06)
 link(guide,'Roof_TrueOpenFrame',(sgn*.55,-.34,1.108),axis=(1,0,0),spread=.003)
 lo,hi=sorted([sgn*.545,sgn*.497]);stop='Stop_'+side
 box(stop,(lo,-.351,.595),(hi,-.321,.631),3,'finite stop seated in the U-guide and sidewall and overlapped by the fixed sash lower corner')
 link(stop,guide,(sgn*.541,-.337,.613),axis=(0,0,1),spread=.007)
 link(stop,'Shell_'+side,(sgn*.541,-.337,.613),axis=(0,0,1),spread=.007)
box('Sash_FixedOpaquePanel',(-.519,-.346,.615),(.519,-.326,1.087),2,'single thick fully opaque solid muted-blue sash, fixed half-raised pose supported by two stops; no transparency or sliding simulation')
for side,sgn in [('Left',-1),('Right',1)]:
 link('Sash_FixedOpaquePanel','Stop_'+side,(sgn*.509,-.336,.623),axis=(1,0,0),spread=.003)
 seat='Handle_'+side+'_Seat';lo,hi=sorted([sgn*.358,sgn*.382]);box(seat,(lo,-.403,.624),(hi,-.337,.646),3,'finite handle seat embedded in opaque sash and front handle bar')
 link(seat,'Sash_FixedOpaquePanel',(sgn*.37,-.342,.635),axis=(0,0,1),spread=.004)
box('Handle_FrontBar',(-.41,-.413,.626),(.41,-.389,.650),3,'static closed front handle bar seated at two finite embedded mounts')
for side,sgn in [('Left',-1),('Right',1)]:link('Handle_FrontBar','Handle_'+side+'_Seat',(sgn*.37,-.396,.637),axis=(1,0,0),spread=.004)
box('Baffle_RaisedRearPanel',(-.502,.225,.145),(.502,.247,1.055),0,'separate raised baffle with real bottom/side/top slots and real open rear spacing, no airflow performance claim')
for side,sgn in [('Left',-1),('Right',1)]:
 for label,z in [('Low',.22),('High',.96)]:
  name='Baffle_'+side+'_'+label+'_Standoff';x=sgn*.435
  box(name,(x-.028,.238,z-.027),(x+.028,.342,z+.027),3,'finite baffle rear standoff embedded in baffle and rear shell; rear gap remains truly empty between mounts')
  link(name,'Baffle_RaisedRearPanel',(x,.242,z),axis=(1,0,0),spread=.01)
  link(name,'Shell_RearWall',(x,.334,z),axis=(1,0,0),spread=.01)
box('Fascia_FrontHeader',(-.62,-.410,1.025),(.62,-.370,1.14),0,'blank thick front header integrated with sidewalls, roof and guide upper ends; no marks or controls')
link('Fascia_FrontHeader','Roof_TrueOpenFrame',(0,-.383,1.12),axis=(1,0,0),spread=.1)
for side,sgn in [('Left',-1),('Right',1)]:
 link('Fascia_FrontHeader','Shell_'+side,(sgn*.57,-.3725,1.06),axis=(1,0,0),spread=.01)
 link('Fascia_FrontHeader','Guide_'+side+'_UChannel',(sgn*.52,-.372,1.07),axis=(1,0,0),spread=.004)
# Conservative complete finite spaces are tested against every actual component,
# including full triangle crossings and model/probe containment in both directions.
void('Front_LowerOpening',(-.48,-.455,.11),(.48,.205,.575),'finite empty lower front aperture plus work chamber; cannot be replaced by a dark surface')
void('Chamber_UpperEmpty',(-.47,-.28,.58),(.47,.205,1.015),'upper chamber behind opaque sash remains physically empty')
void('Baffle_RearGap',(-.38,.255,.17),(.38,.316,1.04),'complete open rear gap between actual baffle and back wall, excluding the four physical standoffs')
void('Baffle_LowerSlot',(-.47,.205,.096),(.47,.28,.135),'true bottom slot under baffle above solid work deck')
void('Baffle_UpperSlot',(-.47,.205,1.064),(.47,.28,1.086),'true top slot over baffle below roof')
for side,sgn in [('Left',-1),('Right',1)]:
 lo,hi=sorted([sgn*.508,sgn*.528]);void('Baffle_'+side+'_SideSlot',(lo,.21,.18),(hi,.28,1.02),'true finite side slot outside baffle and inside shell')
 lo,hi=sorted([sgn*.506,sgn*.530]);void('Guide_'+side+'_FrontClearance',(lo,-.352,.655),(hi,-.348,1.005),'finite open front guide-to-sash clearance')
 void('Guide_'+side+'_BackClearance',(lo,-.324,.655),(hi,-.320,1.005),'finite open rear guide-to-sash clearance')
void('Roof_ContinuousAperture',(-.095,.035,1.06),(.095,.225,1.34),'finite vertical aperture crosses roof and short collar; no functional exhaust claim')
for x in [-.4,0,.4]:
 for z in [.15,.35,.55]:GAPS.append({'label':'lower_front_open_chamber','origin_m':[x,-.46,z],'direction':[0,1,0],'length_m':.66})
for x in [-.30,0,.30]:GAPS.append({'label':'lower_baffle_slot','origin_m':[x,.19,.116],'direction':[0,1,0],'length_m':.10})
for x in [-.06,0,.06]:GAPS.append({'label':'open_roof_collar','origin_m':[x,.13,1.06],'direction':[0,0,1],'length_m':.29})
for x,y in [(-.35,-.15),(0,0),(.35,.15)]:FLOOR_PROBES.append({'mesh':'Base_SolidWorkDeck','origin_m':[x,y,.20],'direction':[0,0,-1],'length_m':.24,'expected_hit_z_m':.085})
for meshname,origin,direction,wall in [('Shell_Left',[0,0,.5],[-1,0,0],.065),('Shell_Right',[0,0,.5],[1,0,0],.065),('Shell_RearWall',[0,.27,.5],[0,1,0],.06),('Baffle_RaisedRearPanel',[0,0,.5],[0,1,0],.02),('Sash_FixedOpaquePanel',[0,-.4,.8],[0,1,0],.018)]:WALL_PROBES.append({'mesh':meshname,'origin_m':origin,'direction':direction,'length_m':.8,'minimum_wall_thickness_m':wall})
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
root=bpy.data.objects.new('OneFixedSashFumeHood',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
hood_evidence={'static_sash_count':1,'true_u_guide_count':2,'finite_stop_count':2,'baffle_standoff_count':4,'finite_void_volumes':VOID_VOLUMES,'finite_volume_empty_checks':void_volume_checks,'actual_work_deck_floor_checks':floor_checks,'actual_wall_thickness_checks':wall_checks,'material_contract':MATERIAL_CONTRACT,'static_visual_only':True,'ventilation_filtration_protection_safety_claim':False}
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
 'single_prop_count':1,'hood_working_geometry':hood_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.65));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.82;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-2.4,-3.8,2.55),'gray-back3q':(2.4,3.8,2.55)} if gray else {
 'thumbnail':(-2.4,-3.8,2.55),'qa-front':(0,-4,.65),'qa-side':(4,0,.65),'qa-top':(0,0,4),
 'qa-back':(0,4,.65),'qa-wireframe':(-2.4,-3.8,2.55)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.82
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0025;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-4,.65)),('silhouette-128-side',(4,0,.65))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
