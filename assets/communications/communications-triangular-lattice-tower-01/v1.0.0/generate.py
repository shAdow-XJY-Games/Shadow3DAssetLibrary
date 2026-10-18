"""Original freestanding three-chord tapered communications tower visual module.
Metres, Z up, front -Y. Independent X repeats only; no radio or structural claims.
"""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-triangular-lattice-tower-01';VERSION='1.0.0';TITLE='Triangular Lattice Communications Tower'
DESCRIPTION=('One original freestanding tapered triangular lattice tower visual module. Three continuous inclined main chords connect three finite ground pads to five triangular horizontal levels and twelve alternating face diagonals. The three sides contain twenty-four true triangular windows around an open tapered central cavity. Three top radial bearers support a short central mast; six horizontal arms support three separated solid antenna panels. Every intended junction has finite interior engagement. Independent X repetition is checked using actual full envelopes, a positive 0.650 m separation and matching surface witnesses; the second instance is a test fixture, not another asset or delivered scene. '
 'Metres, Z up, front -Y. Origin is the design triangle centre at ground Z=0, not the asymmetric Y bounds midpoint. Editable closed meshes and four opaque constant PBR materials. No textures, logos, animation, platform, ladder, people, fence, terrain or extra equipment. '
 'Static visual only. No radio transmission or reception, frequency, power, coverage, tracking, cabling, electricity, climbing, wind resistance, structural load, stability, lightning protection, foundation anchorage, installation, construction or communications safety certification. No vertical stacking, mechanical connector or compatibility with earlier dish antennas or other equipment. Not an engineering, manufacturing or use design.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CHORDS=[];HORIZONTALS=[];DIAGONALS=[];PANELS=[];ARMS=[];NODES={};RODS={};WINDOWS=[]
PALETTE=[('Lattice_OxideRed',(.59,.095,.045,1),.55,.24),('Brace_WarmIvory',(.80,.76,.62,1),.56,.18),('Mast_Charcoal',(.075,.10,.115,1),.48,.45),('Panel_Porcelain',(.77,.84,.82,1),.62,.04)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box_geometry(lo,hi):return cuboid(lo,hi),BOX_FACES
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(0,0,1),spread=.003):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def node(key,p,names):
 if key not in NODES:NODES[key]={'point':p,'members':[]}
 assert math.dist(NODES[key]['point'],p)<1e-7
 NODES[key]['members'].extend(names)
def rod(name,a,b,radius,material,role,extend=.026,n=8):
 d=unit(sub(b,a));u=unit(cross(d,(0,1,0) if abs(d[1])<.9 else (1,0,0)));v=cross(d,u);aa=sub(a,mul(d,extend));bb=add(b,mul(d,extend))
 vs=[add(p,add(mul(u,radius*math.cos(math.tau*j/n)),mul(v,radius*math.sin(math.tau*j/n)))) for p in [aa,bb] for j in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 RODS[name]={'a':a,'b':b,'radius':radius,'extension':extend,'sides':n}
 return mesh(name,vs,fs,material,role)
ANGLES=[-math.pi/2,math.pi/6,5*math.pi/6];LEVELS=[.26,1.54,2.82,4.10,5.38]
def radius(z):return 1.05-(z-.06)*(.75/5.34)
def at(i,z):return (radius(z)*math.cos(ANGLES[i]),radius(z)*math.sin(ANGLES[i]),z)
for i in range(3):
 label=str(i+1);bottom=at(i,.06);foot=box('GroundPad_'+label,(bottom[0],bottom[1],.05),(.42,.42,.10),2,'finite planar independent ground pad, bottom exactly Z=0; visual footing without anchor or foundation claim');FEET.append(foot)
 chord=rod('MainChord_'+label,bottom,at(i,5.43),.066,0,'one continuous inclined primary chord, widening the triangular footprint toward ground',extend=0);CHORDS.append(chord);link(chord,foot,at(i,.078))
 for k,z in enumerate(LEVELS):node(('tower',i,k),at(i,z),[chord])
for k,z in enumerate(LEVELS):
 for i in range(3):
  j=(i+1)%3;name=rod(f'Horizontal_{k+1}_Face{i+1}',at(i,z),at(j,z),.041,1,'finite closed side of a horizontal triangular frame');HORIZONTALS.append(name)
  node(('tower',i,k),at(i,z),[name]);node(('tower',j,k),at(j,z),[name])
for k in range(4):
 for i in range(3):
  j=(i+1)%3;a=at(i,LEVELS[k]);b=at(j,LEVELS[k]);c=at(j,LEVELS[k+1]);d=at(i,LEVELS[k+1])
  start,end=(a,c) if k%2==0 else (b,d);si,ei=(i,j) if k%2==0 else (j,i)
  name=rod(f'Diagonal_{k+1}_Face{i+1}',start,end,.038,0,'alternating single diagonal on a tapered triangular tower face, embedded at both frame nodes');DIAGONALS.append(name)
  node(('tower',si,k),start,[name]);node(('tower',ei,k+1),end,[name])
  # Every complete triangular window is inset 100 mm from its three edges,
  # then extruded through the face plane by 30 mm in each direction.
  tris=[(a,b,c),(a,c,d)] if k%2==0 else [(a,b,d),(b,c,d)]
  for w,tri in enumerate(tris):
   lengths=[math.dist(tri[1],tri[2]),math.dist(tri[0],tri[2]),math.dist(tri[0],tri[1])];perimeter=sum(lengths);cen=tuple(sum(tri[j][k]*lengths[j] for j in range(3))/perimeter for k in range(3));cr=cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]));normal=unit(cr);inradius=math.sqrt(dot(cr,cr))/perimeter;assert inradius>.12;inner=[add(cen,mul(sub(p,cen),1-.10/inradius)) for p in tri]
   vs=[add(p,mul(normal,s)) for s in [-.030,.030] for p in inner];faces=[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]
   key=f'TriangularWindow_{k+1}_Face{i+1}_{w+1}';VOID_VOLUMES[key]={'vertices':vs,'faces':faces,'role':'complete finite triangular through-window; no rods or hidden solids may occupy it','enclosed_fill_center_m':cen};WINDOWS.append(key)
   GAPS.append({'label':key,'origin_m':sub(cen,mul(normal,.034)),'direction':normal,'length_m':.068})
# A finite triangular tapered chamber spans almost the full lattice height.
cv=[((radius(z)-.20)*math.cos(a),(radius(z)-.20)*math.sin(a),z) for z in [.38,5.22] for a in ANGLES]
VOID_VOLUMES['CentralTaperedAir']={'vertices':cv,'faces':[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'role':'full finite triangular central cavity, all rods and any hidden fill excluded','enclosed_fill_center_m':(0,0,2.8)}
mast=rod('ShortAntennaMast',(0,0,5.32),(0,0,7.14),.057,2,'short central antenna mast supported by three top radial bearers',extend=0)
for i in range(3):
 name=rod('CrownBearer_'+str(i+1),at(i,5.38),(0,0,5.38),.046,2,'one radial crown bearer from main-chord node to central mast')
 node(('tower',i,4),at(i,5.38),[name]);node(('mast',0),(0,0,5.38),[name,mast])
for i,a in enumerate(ANGLES):
 u=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0);c=mul(u,.50);name='AntennaPanel_'+str(i+1)
 poly=[(-.11,-.060),(.11,-.060),(.13,-.040),(.13,.040),(.11,.060),(-.11,.060),(-.13,.040),(-.13,-.040)]
 vs=[add(c,add(mul(t,x),add(mul(u,y),(0,0,z)))) for z in [5.80,6.90] for x,y in poly];n=len(poly)
 mesh(name,vs,[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],3,'solid chamfered vertical antenna-panel visual, two genuine horizontal support roots');PANELS.append(name)
 for k,z in enumerate([6.05,6.65]):
  endpoint=add(c,(0,0,z));arm=rod(f'PanelArm_{i+1}_{k+1}',(0,0,z),endpoint,.037,2,'fixed radial panel support arm, finite embedded mast and panel roots');ARMS.append(arm)
  node(('mast',k+1),(0,0,z),[arm,mast]);link(arm,name,endpoint)
# Enumerate every pair of intentionally overlapping members at each shared node.
# These are real geometric junctions, not blanket exemptions for a whole asset.
for record in NODES.values():
 for a,b in itertools.combinations(sorted(set(record['members'])),2):link(a,b,record['point'])
# Entire clear vertical envelopes behind each panel, excluding its two arms.
for i,a in enumerate(ANGLES):
 u=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0)
 vs=[add(mul(u,r),add(mul(t,w),(0,0,z))) for z in [6.11,6.58] for w in [-.085,.085] for r in [.11,.42]]
 VOID_VOLUMES['MastPanelAir_'+str(i+1)]={'vertices':vs,'faces':BOX_FACES,'role':'complete finite arm-free gap between central mast and antenna panel','enclosed_fill_center_m':add(mul(u,.265),(0,0,6.34))}
ALL_VERTICES=[v for g in G.values() for v in g['vertices']];XMIN=min(v[0] for v in ALL_VERTICES);XMAX=max(v[0] for v in ALL_VERTICES);REPEAT_CLEARANCE=.650;REPEAT_SPACING=round(XMAX-XMIN+REPEAT_CLEARANCE,7)
TOWER_CONTRACT={'single_module_count':1,'main_chords':CHORDS,'horizontal_frames':HORIZONTALS,'face_diagonals':DIAGONALS,'ground_pads':FEET,'antenna_panels':PANELS,'panel_arms':ARMS,'triangular_windows':WINDOWS,'repeat_axis':'X','repeat_spacing_m':REPEAT_SPACING,'repeat_surface_clearance_m':REPEAT_CLEARANCE,'vertical_stacking':False,'legacy_compatibility':False,'static_visual_only':True}
def measure_tower_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 # Cylinder end-ring centroids and all end-ring radii, not object bounds.
 rods=[]
 for name,record in RODS.items():
  v=vertices[name];n=record['sides'];assert len(v)==2*n
  centres=[tuple(sum(float(p[k]) for p in v[j*n:(j+1)*n])/n for k in range(3)) for j in range(2)];axis=unit(sub(record['b'],record['a']));wanted=[sub(record['a'],mul(axis,record['extension'])),add(record['b'],mul(axis,record['extension']))]
  assert all(math.dist(x,y)<1.4e-6 for x,y in zip(centres,wanted)),('Actual rod endpoints changed',name,centres)
  measured=[math.dist(p,centres[j]) for j in range(2) for p in v[j*n:(j+1)*n]];assert max(abs(r-record['radius']) for r in measured)<1.4e-6,('Actual rod radius changed',name)
  rods.append({'mesh':name,'actual_end_ring_centres_m':centres,'actual_radius_range_m':[min(measured),max(measured)]})
 for name in FEET:assert abs(min(float(p[2]) for p in vertices[name]))<1e-7,('Lifted actual ground pad',name)
 for name in PANELS:
  v=vertices[name];assert abs(min(float(p[2]) for p in v)-5.80)<1.4e-6 and abs(max(float(p[2]) for p in v)-6.90)<1.4e-6
 v=[p for values in vertices.values() for p in values];lo=[min(float(p[k]) for p in v) for k in range(3)];hi=[max(float(p[k]) for p in v) for k in range(3)];gap=REPEAT_SPACING-(hi[0]-lo[0]);assert abs(gap-.65)<1.4e-6
 # Disjoint full X envelopes bound every triangle pair from below. Opposed
 # actual ground-pad face vertices sharing Y,Z attain that bound exactly.
 left=vertices['GroundPad_3'];right=vertices['GroundPad_2'];witness=[]
 for p in right:
  for q in left:
   if abs(float(p[0])-hi[0])<1e-6 and abs(float(q[0])-lo[0])<1e-6 and abs(float(p[1])-float(q[1]))<1e-7 and abs(float(p[2])-float(q[2]))<1e-7:witness.append({'a':list(map(float,p)),'b_translated':[float(q[0])+REPEAT_SPACING,float(q[1]),float(q[2])],'distance_m':math.dist(p,add(q,(REPEAT_SPACING,0,0)))})
 assert witness and all(abs(w['distance_m']-gap)<1.5e-6 for w in witness),'Missing actual attaining surface witness'
 return dict(TOWER_CONTRACT,actual_rods=rods,actual_bounds_min_m=lo,actual_bounds_max_m=hi,actual_x_repeat_spacing_m=REPEAT_SPACING,actual_full_surface_repeat_clearance_m=gap,repeat_attaining_surface_witnesses=witness,repeat_method='complete X separation is a lower bound for every triangle pair, attained by actual opposed pad-face vertices; both translated copies retain their finite ground patches')
FOCUS=(0,-.2625,3.57);ORTHO=9.4
CAMERAS={'gray-front3q':(11,-16,11.5),'gray-back3q':(-11,16,11.5),'thumbnail':(11,-16,11.5),'qa-front':(0,-20,10),'qa-side':(20,-.2625,10),'qa-top':(0,-.2625,20),'qa-back':(0,20,10),'qa-wireframe':(11,-16,11.5),'silhouette-128-front':(0,-20,10),'silhouette-128-side':(20,-.2625,10)}
CAMERA_SCALES={'qa-top':3.5};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneTriangularLatticeTower',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Design triangle centre X=Y=0, ground Z=0; asymmetric Y bounds midpoint -0.2625 m';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
tower_evidence=dict(measure_tower_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts}),finite_external_air_volume_checks=void_volume_checks,material_contract=MATERIAL_CONTRACT)
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
 'single_module_count':1,'tower_geometry':tower_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/communications/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'communications','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-8,-12,16),3000,8),('Fill',(10,-3,9),1600,6),('Rim',(2,10,13),2200,6)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
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
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
