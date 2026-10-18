"""Original wide shallow snow shovel. One static prop; no snow or mechanical simulation.
Continuous thick concave blade, rear ribs, socket, long shaft, truly open D grip.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-wide-scoop-snow-shovel-01';VERSION='1.0.0';TITLE='Wide Scoop Snow Shovel'
DESCRIPTION=('One original fixed snow shovel counted as one prop: a broad shallow concave blue scoop has a continuous closed 10 mm vertical-thickness shell, low side wings and a blunt front edge. Two solid rear ribs meet the back of the scoop. A hollow rear socket has a finite join with the scoop and surrounds the inserted end of a long wooden shaft. The other end enters the solid lower stem of one orange D-shaped grip with a true full-thickness opening. The tool lies horizontally with finite support at the front scoop underside and the rear grip. Six editable closed meshes and four opaque constant PBR colours; no texture, animation, person, snow pile, footprints, plinth or surrounding scene. Metres, source Z up, front -Y, origin at ground under the shaft centreline, 700 mm behind the scoop front edge. '
'Static visual geometry only. No snow-clearing action, snow or force simulation, capacity, ergonomics, cold resistance, sharpness, physical strength, manufacture, load, durability or winter-tool safety claim. No fit with prior snow piles, porches or characters. Dimensions describe this fixed visual geometry only.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};CONTACTS=[]
PALETTE=[('Scoop_IceBlue',(.075,.34,.47,1),.62,0),('Socket_DarkSteel',(.11,.15,.17,1),.40,.55),('Shaft_HoneyWood',(.46,.25,.095,1),.70,0),('DGrip_BurntOrange',(.85,.22,.055,1),.58,0)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def polygon_area(p):return abs(sum(cross2(a,b) for a,b in zip(p,p[1:]+p[:1])))/2

def emit(name,vs,fs,mat,role):
 g={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),8) for c in p) for p in vs],'faces':fs,'material':mat,'role':role};G[name]=g;return g

def grid_shell(top,bottom,nx,ny):
 n=nx*ny;vs=top+bottom;fs=[]
 for j in range(ny-1):
  for i in range(nx-1):
   a=j*nx+i;b=a+1;c=a+nx+1;d=a+nx;fs += [(a,b,c),(a,c,d),(n+a,n+c,n+b),(n+a,n+d,n+c)]
 edge=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
 for a,b in zip(edge,edge[1:]+edge[:1]):fs += [(a,n+a,n+b),(a,n+b,b)]
 return vs,fs

# Broad original scoop, not a scaled ski or excavator bucket. Its lip is a
# blunt closed 10 mm edge and the middle surface continuously curves upward.
BLADE='Scoop_ContinuousThickCurvedShell';YS=[-.70,-.66,-.58,-.50,-.42,-.34,-.30];ZS=[.010,.010,.016,.029,.048,.078,.100]
US=[-1.,-.90,-.78,-.40,0.,.40,.78,.90,1.];WINGS=[.038,.016,0,0,0,0,0,.016,.038]
def halfwidth(y):return .235-.030*((y+.70)/.40)
def baseheight(y):
 for a,b,za,zb in zip(YS,YS[1:],ZS,ZS[1:]):
  if a-1e-8<=y<=b+1e-8:return za+(zb-za)*(y-a)/(b-a)
 raise ValueError(y)
top=[(u*halfwidth(y),y,z+w*((y+.70)/.40)) for y,z in zip(YS,ZS) for u,w in zip(US,WINGS)]
bottom=[(x,y,z-.010) for x,y,z in top]
vs,fs=grid_shell(top,bottom,len(US),len(YS));emit(BLADE,vs,fs,0,'one continuous shallow concave shell; low side wings, blunt thick front lip and finite flat front underside')
FEET.append(BLADE)
# Underblade ribs are solid shaped extrusions following the rear shell. Each
# overlaps only the scoop and has finite separation from the socket and ground.
RIBS=[]
for label,x in [('Left',-.075),('Right',.075)]:
 name='RearRib_'+label;ys=[-.565,-.49,-.41,-.335];outline=[(y,baseheight(y)-.005) for y in ys]+[(y,max(.003,baseheight(y)-.025)) for y in reversed(ys)]
 v=[(xx,y,z) for xx in [x-.007,x+.007] for y,z in outline];n=len(outline);f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]
 for i in range(n):j=(i+1)%n;f.append((i,j,n+j,n+i))
 emit(name,v,f,0,'solid rear reinforcement rib finitely embedded into scoop underside');RIBS.append(name)
 LINKS.append((BLADE,name,[(x,-.49,baseheight(-.49)-.007),(x,-.41,baseheight(-.41)-.007),(x,-.35,baseheight(-.35)-.007)]))

# Shaft axis slopes gently down towards the ground-supported rear D grip.
SLOPE=-.027/.985
def axis_z(y):return .052+SLOPE*(y+.335)
AXIS=(0,1/math.sqrt(1+SLOPE*SLOPE),SLOPE/math.sqrt(1+SLOPE*SLOPE));VEC=(0,-AXIS[2],AXIS[1])
ANGLES=[math.tau*i/20 for i in range(20)]
def shaft_loop(y,r):return [(r*math.cos(a),y+VEC[1]*r*math.sin(a),axis_z(y)+VEC[2]*r*math.sin(a)) for a in ANGLES]
def ring_mesh(loops,closed):
 n=len(loops[0]);v=sum(loops,[]);f=[]
 for h in range(len(loops) if closed else len(loops)-1):
  k=(h+1)%len(loops)
  for i in range(n):j=(i+1)%n;f.append((h*n+i,h*n+j,k*n+j,k*n+i))
 if not closed:f += [tuple(reversed(range(n))),tuple((len(loops)-1)*n+i for i in range(n))]
 return v,f
SOCKET='Socket_RealHollowRearCollar';v,f=ring_mesh([shaft_loop(-.335,.028),shaft_loop(-.235,.028),shaft_loop(-.235,.014),shaft_loop(-.335,.014)],True)
emit(SOCKET,v,f,1,'closed thick real tubular socket, finite rear-scoop connection and inserted shaft connection')
LINKS.append((BLADE,SOCKET,[(.009,-.332,.076),(-.009,-.332,.076),(.006,-.330,.076)]))
SHAFT='Shaft_LongInsertedWood';v,f=ring_mesh([shaft_loop(-.315,.015),shaft_loop(.673,.015)],False);emit(SHAFT,v,f,2,'one long wooden shaft inserted into socket and lower D-handle stem, fixed pose')
LINKS.append((SOCKET,SHAFT,[(.0145,-.27,axis_z(-.27)),(-.0145,-.27,axis_z(-.27)),(.0145,-.25,axis_z(-.25))]))

# A single connected D-shaped annulus, extruded 50 mm; the hole is never capped.
GRIP='DGrip_TrueThroughOpening';outer=[(-.027,.630),(.027,.630),(.080,.700),(.085,.800),(.060,.880),(-.060,.880),(-.085,.800),(-.080,.700)]
inner=[(-.013,.695),(.013,.695),(.052,.735),(.055,.795),(.044,.845),(-.044,.845),(-.055,.795),(-.052,.735)]
loops=[[(x,y,0) for x,y in outer],[(x,y,.050) for x,y in outer],[(x,y,.050) for x,y in inner],[(x,y,0) for x,y in inner]]
v=sum(loops,[]);f=[];n=8
for h in range(4):
 k=(h+1)%4
 for i in range(n):j=(i+1)%n;f.append((h*n+i,h*n+j,k*n+j,k*n+i))
emit(GRIP,v,f,3,'one thick orange D-handle with complete true through-hole and flat finite ground face');FEET.append(GRIP)
LINKS.append((SHAFT,GRIP,[(0,.645,axis_z(.645)),(.006,.650,axis_z(.650)),(-.006,.660,axis_z(.660))]))
BORES.append({'mesh':GRIP,'origin_m':(0,.77,-.010),'direction':(0,0,1),'length_m':.070,'role':'actual full-thickness D-grip opening'})
GAPS.append({'origin_m':(0,.77,-.005),'direction':(0,0,1),'length_m':.060,'role':'assembled true D opening'})
GAPS.append({'origin_m':(0,0,.001),'direction':(0,0,1),'length_m':.025,'role':'open air below long raised shaft'})
# Whole D opening, inset only 2.5 mm from its inner contour and extending
# through both exterior faces. Includes the entire upper handgrip clearance.
ci=(0,.770);hole=[(ci[0]+(x-ci[0])*.94,ci[1]+(y-ci[1])*.94) for x,y in inner];v=[(x,y,z) for z in [-.005,.055] for x,y in hole];f=[tuple(reversed(range(8))),tuple(8+i for i in range(8))]
for i in range(8):j=(i+1)%8;f.append((i,j,8+j,8+i))
VOID_VOLUMES['DGrip_EntireFiniteOpening']={'vertices':v,'faces':f,'role':'whole finite D opening with full boundary and volume, inset 6 percent from exact inner contour'}
# Full shallow-scoop interior volume. Its bottom follows the actual triangulated
# inner surface, with 2 mm inset from each open edge and 2 mm vertical clearance.
def height_on_inner(x,y):
 for tri in [f for f in G[BLADE]['faces'] if max(f)<len(top)]:
  a,b,c=[top[i] for i in tri];den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den;w=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den;v=1-u-w
  if min(u,v,w)>=-1e-8:return u*a[2]+w*b[2]+v*c[2]
 raise ValueError((x,y))
cv=[]
for y in YS:
 yy=max(YS[0]+.002,min(YS[-1]-.002,y))
 for u in US:
  xx=u*(halfwidth(yy)-.002);cv.append((xx,yy,height_on_inner(xx,yy)+.002))
vv,ff=grid_shell([(x,y,.155) for x,y,z in cv],cv,len(US),len(YS));VOID_VOLUMES['Scoop_EntireFiniteInterior']={'vertices':vv,'faces':ff,'role':'whole scoop interior above real curved floor and low wings, 2 mm edge and floor inset, top at 155 mm'}

def unique(points):return sorted(set(tuple(float(c) for c in p) for p in points))
def measure_shovel_geometry(vertices,triangles=None):
 assert set(vertices)==set(G),'Exactly the six connected planned shovel components'
 rows=[]
 for name,g in G.items():
  actual=unique(vertices[name]);expected=unique(g['vertices']);assert len(actual)==len(expected),('Unique mesh vertex count changed',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(ix)==1 for ix in matches) and len({ix[0] for ix in matches})==len(expected),('Actual mesh surface changed',name)
  rows.append({'mesh':name,'maximum_actual_position_error_m':max(math.dist(p,expected[ix[0]]) for p,ix in zip(actual,matches)),'unique_bijective_surface_match':True})
 blade=unique(vertices[BLADE]);assert abs(max(p[0] for p in blade)-min(p[0] for p in blade)-.470)<1e-6
 assert abs(max(p[1] for p in blade)-min(p[1] for p in blade)-.400)<1e-6
 thickness=[]
 for x,y,z in G[BLADE]['vertices'][:len(top)]:
  column=sorted(p[2] for p in blade if abs(p[0]-x)<2e-7 and abs(p[1]-y)<2e-7);assert len(column)==2;thickness.append(column[1]-column[0])
 assert min(thickness)>.009999 and max(thickness)<.010001
 allv=[p for v in vertices.values() for p in v];assert min(p[2] for p in allv)>-1e-7
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<1e-7
 return {'single_prop_count':1,'meshes':rows,'actual_scoop_width_m':.470,'actual_scoop_depth_m':.400,'actual_vertical_shell_thickness_range_m':[min(thickness),max(thickness)],'actual_scoop_back_inner_height_m':.100,'actual_wing_rise_at_rear_m':.038,'whole_scoop_cavity_and_D_hole_finite_volume_required':True,'static_fixed_pose_only':True,'no_snow_or_mechanical_claim':True}
FOCUS=(0,.090,.060);ORTHO=1.98
CAMERAS={'gray-front3q':(1.8,-2.8,2.8),'gray-back3q':(-1.8,2.8,2.8),'thumbnail':(1.8,-2.8,2.8),'qa-front':(0,-3,1.4),'qa-side':(3,.09,1.55),'qa-top':(0,.09,3.3),'qa-back':(0,3,1.4),'qa-wireframe':(1.8,-2.8,2.8),'silhouette-128-front':(0,-3,1.4),'silhouette-128-side':(3,.09,1.55)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneWideScoopSnowShovel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground below shaft centreline, 0.70 m behind front edge; Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
isolated_volume_checks=[]
for name,probe in ISOLATED_VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False);model_tree=trees[name];obj=byname[name]
 crossing=model_tree.overlap(pt);model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)];probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
 assert not crossing and not model_inside and not probe_inside,('Actual isolated full through bore blocked',name,crossing,model_inside,probe_inside)
 isolated_volume_checks.append({'mesh':name,'complete_closed_volume_empty':True,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
shovel_evidence=dict(measure_shovel_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts},{o.name:[[tuple(o.matrix_world@o.data.vertices[i].co) for i in t.vertices] for t in o.data.loop_triangles] for o in parts}),material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'shovel_geometry':shovel_evidence,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'actual_finite_void_volumes':void_volume_checks,'actual_isolated_bore_volumes':isolated_volume_checks,'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
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
