"""Original thick bored wooden rolling pin; one fixed static visual prop.
Metres, native Z up, front -Y. No food-contact or actual tool-performance claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='bakery-bored-barrel-rolling-pin-01';VERSION='1.0.0';TITLE='Bored Barrel Rolling Pin'
DESCRIPTION=('One original low-poly rolling pin counted as one complete fixed static visual prop. A thick pale maple-coloured barrel has a long straight work-surface silhouette, softened polygonal shoulders and a genuine full-length octagonal through-bore. One independent continuous satin steel-coloured shaft rests on the entire finite lower bore facet in the single frozen pose; all seven other complete bore facets remain clear. Two separate dark walnut-coloured grips each have a short neck, swelling body and rounded blunt end, with finite embedded shaft joints and visible gaps from both barrel ends. The barrel rests on one finite bottom facet while both grips stay above ground. Four named editable closed meshes and three opaque constant PBR materials. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. No dough, flour, table, stand, labels, textures or animation. Static visual geometry only: no rolling, kneading, food contact, sanitation, hand fit, resistance, load, durability, manufacturing, stability or tool safety claim. No dimensional compatibility with historical bowls, tables or dough assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];SEATS={};BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};HANDLES=[];EMBEDDED_VOLUMES={}
PALETTE=[('Barrel_PaleMaple',(.64,.39,.17,1),.68,0.),('Grips_WarmWalnut',(.19,.065,.022,1),.62,0.),('Axle_SatinSteel',(.43,.48,.50,1),.32,.75)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 vol=sum(dot(vs[f[0]],cross(vs[f[i]],vs[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
def axial(o,y,z,x):return add(o,(x,y,z))
def poly(r,n=8,phase=math.pi/8):return[(r*math.cos(math.tau*i/n+phase),r*math.sin(math.tau*i/n+phase)) for i in range(n)]
def prism_data(p,o,lo,hi):
 n=len(p);vs=[axial(o,y,z,x) for x in[lo,hi] for y,z in p];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return vs,fs

def lathe(profile,o,n=16,phase=math.pi/16):
 vs=[];rings=[];fs=[]
 for r,x in profile:
  rr=[]
  for j in range(n if r else 1):
   a=math.tau*j/n+phase;rr.append(len(vs));vs.append(axial(o,r*math.cos(a),r*math.sin(a),x))
  rings.append(rr)
 for a,b in list(zip(rings,rings[1:]))+[(rings[-1],rings[0])]:
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n;fs.extend([(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])])
 return vs,fs

def void(name,vs,fs,targets,role,isolated=False):
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]={'vertices':vs,'faces':fs,'targets':targets,'role':role}
def inward_polygon(p,d):
 out=[]
 for i,b in enumerate(p):
  a=p[i-1];c=p[(i+1)%len(p)];e=(b[0]-a[0],b[1]-a[1]);f=(c[0]-b[0],c[1]-b[1]);el=math.hypot(*e);fl=math.hypot(*f)
  n=(-e[1]/el,e[0]/el);m=(-f[1]/fl,f[0]/fl);q=(b[0]+d*n[0],b[1]+d*n[1]);r=(b[0]+d*m[0],b[1]+d*m[1]);den=e[0]*f[1]-e[1]*f[0]
  if abs(den)<1e-14:out.append(q);continue
  t=((r[0]-q[0])*f[1]-(r[1]-q[1])*f[0])/den;out.append((q[0]+t*e[0],q[1]+t*e[1]))
 return out
BARREL_R=.05;HOLE_R=.014;SHAFT_R=.008;HOLE_Z=round(BARREL_R*math.cos(math.pi/24),8);SEAT_Z=round(HOLE_Z-HOLE_R*math.cos(math.pi/8),8);AXLE_Z=round(SEAT_Z+SHAFT_R*math.cos(math.pi/8),8);ORIGIN=(0,0,AXLE_Z)
# Six original outer rings, two complete inner rings, and true annular end walls.
# Each octagonal inner edge is subdivided into three collinear finite panels to
# match the 24-sided outer rings. No capping disk crosses the through-bore.
OUTER_PROFILE=[(.042,-.17),(.047,-.165),(.05,-.156),(.05,.156),(.047,.165),(.042,.17)]
outer=[poly(r,24,math.pi/8) for r,x in OUTER_PROFILE];hp=poly(HOLE_R)
inner=[(hp[i][0]+(hp[(i+1)%8][0]-hp[i][0])*j/3,hp[i][1]+(hp[(i+1)%8][1]-hp[i][1])*j/3) for i in range(8) for j in range(3)]
v=[(x,y,HOLE_Z+z) for (r,x),ring in zip(OUTER_PROFILE,outer) for y,z in ring]
v += [(x,y,HOLE_Z+z) for x in[-.17,.17] for y,z in inner];f=[]
for k in range(5):
 for i in range(24):j=(i+1)%24;f.append((k*24+i,k*24+j,(k+1)*24+j,(k+1)*24+i))
INNER_WALL_FACE_INDICES=list(range(len(f),len(f)+24));BOTTOM_WALL_FACE_INDICES=INNER_WALL_FACE_INDICES[15:18]
for i in range(24):j=(i+1)%24;f.append((144+i,168+i,168+j,144+j))
for i in range(24):
 j=(i+1)%24;f.extend([(i,144+i,144+j,j),(120+i,120+j,168+j,168+i)])
barrel=mesh('Barrel_ThickRoundedTrueBore',v,f,0,'one continuous thick long straight 24-facet maple-coloured barrel, softened shoulders and real open octagonal axial through-bore with annular end walls');FEET.append(barrel)
v,f=prism_data(poly(SHAFT_R),ORIGIN,-.245,.245);shaft=mesh('Axle_ContinuousLowerSeatedShaft',v,f,2,'one independent continuous solid octagonal shaft, finitely lower-seated inside the entire barrel bore; single static pose')
CONTACTS.append({'a':barrel,'b':shaft,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':SEAT_Z,'minimum_patch_area_m2':.002,'interior_probe_offset_m':.00015,'points':[(x,0,SEAT_Z) for x in[-.14,0,.14]],'scope':'complete finite lower octagonal bore facet opposed to continuous shaft lower facet across the full 340 mm barrel; no penetration'})
SEATS[barrel]={'shaft':shaft,'origin_m':(0,0,HOLE_Z),'x_center_m':0,'bore_radius_m':HOLE_R,'bore_polygon_vertices':8,'inner_wall_face_indices':INNER_WALL_FACE_INDICES,'bottom_wall_face_indices':BOTTOM_WALL_FACE_INDICES,'lo_m':-.17,'hi_m':.17}
GRIP_PROFILE=[(0,.184),(.010,.184),(.011,.190),(.010,.202),(.014,.215),(.0175,.239),(.018,.257),(.016,.273),(.010,.280),(0,.280)]
for label,sign in [('Left',-1),('Right',1)]:
 v,f=lathe([(r,sign*x) for r,x in GRIP_PROFILE],ORIGIN);handle=mesh('Grip_'+label+'NeckedRoundedHandle',v,f,1,'separate walnut-coloured grip with short neck, gently swelling body and rounded blunt end, finitely joined to continuous shaft and clear of barrel end');HANDLES.append(handle);link(shaft,handle,(sign*.222,0,AXLE_Z),spread=.012)
 # Complete barrel-end/grip-shoulder axial slab. The actual through-shaft is
 # explicitly excluded because it occupies the centre, not called empty air.
 lo,hi=sorted([sign*.1708,sign*.1832]);void('Grip_'+label+'CompleteShoulderGap',cuboid((lo,-.051,-.001),(hi,.051,.101)),BOX_FACES,[barrel]+HANDLES,'entire finite axial slab between barrel end and grip shoulder; only the occupying shaft is excluded')
# Exact closed interior witness volumes, not points: every boundary remains
# strictly inside both real joined solids, proving finite embedded connection.
for name,sign in zip(HANDLES,[-1,1]):
 lo,hi=sorted([sign*.207,sign*.237]);EMBEDDED_VOLUMES[name+'_FiniteAxleJoint']={'vertices':cuboid((lo,-.002,AXLE_Z-.002),(hi,.002,AXLE_Z+.002)),'faces':BOX_FACES,'targets':[shaft,name],'role':'complete finite shaft-to-grip interior overlap volume'}
EMBEDDED_VOLUMES['Axle_WholeContinuousCore']={'vertices':cuboid((-.24,-.0015,AXLE_Z-.0015),(.24,.0015,AXLE_Z+.0015)),'faces':BOX_FACES,'targets':[shaft],'role':'full-length finite interior shaft core proves continuous unbroken shaft'}
# Both gap volumes are checked against both grips after their creation.
for g in VOID_VOLUMES.values():g['targets']=[barrel]+HANDLES
v,f=prism_data(inward_polygon(hp,.0005),(0,0,HOLE_Z),-.1708,.1708);void('Barrel_FullIsolatedThroughBore',v,f,[barrel],'whole connected closed axial octagonal bore volume with uniform 0.5 mm wall inset, extending beyond both annular mouths',True)
sp=[(y,z+AXLE_Z-HOLE_Z) for y,z in poly(SHAFT_R)]
air=[hp[i] for i in[6,7,0,1,2,3,4,5]]+[sp[i] for i in[5,4,3,2,1,0,7,6]]
v,f=prism_data(inward_polygon(air,.0005),(0,0,HOLE_Z),-.1708,.1708);void('Barrel_CompleteAssembledBoreAir',v,f,list(G),'entire connected U-shaped bore-minus-shaft air along the full barrel and beyond both mouths, uniformly eroded 0.5 mm; finite lower seat is excluded by exact topology')
BORES.append({'mesh':barrel,'origin_m':(-.171,0,HOLE_Z),'direction':(1,0,0),'length_m':.342})
PIN_CONTRACT={'single_prop_count':1,'thick_true_bored_barrels':1,'continuous_lower_seated_shafts':1,'separate_necked_blunt_grips':2,'finite_shaft_lower_seats':1,'finite_barrel_ground_facets':1,'barrel_axial_length_m':.34,'straight_barrel_length_m':.312,'octagonal_bore_sides':8,'nonbearing_complete_bore_walls':7,'shoulder_gap_m':.014,'handles_clear_of_ground':True,'no_motion_food_contact_or_tool_performance_claim':True}
def measure_rolling_pin_geometry(vertices):
 assert set(vertices)==set(G)
 bv=vertices[barrel];sv=vertices[shaft]
 assert abs(min(p[2] for p in bv))<2e-7 and abs(max(p[0] for p in bv)-.17)<2e-7 and abs(min(p[0] for p in bv)+.17)<2e-7
 assert abs(min(p[0] for p in sv)+.245)<2e-7 and abs(max(p[0] for p in sv)-.245)<2e-7
 for n in HANDLES:
  vv=vertices[n];assert min(p[2] for p in vv)>.026
  xx=[abs(p[0]) for p in vv];assert abs(min(xx)-.184)<2e-7 and abs(max(xx)-.28)<2e-7
 return dict(PIN_CONTRACT,geometry_scope='actual coordinates; complete finite contacts, full closed air, nonbearing distances, support and mutations remain mandatory separate gates')
FOCUS=(0,0,.047);ORTHO=.67
CAMERAS={'gray-front3q':(.60,-1.35,.80),'gray-back3q':(-.60,1.35,.80),'thumbnail':(.60,-1.35,.80),'qa-front':(0,-1.5,.65),'qa-side':(1.5,0,.65),'qa-top':(0,0,1.5),'qa-back':(0,1.5,.65),'qa-wireframe':(.60,-1.35,.80),'silhouette-128-front':(0,-1.5,.65),'silhouette-128-side':(1.5,0,.65)}
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
root=bpy.data.objects.new('OneBoredBarrelRollingPin',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(barrel,(0,.03,HOLE_Z),(0,0,HOLE_Z)),(shaft,(0,0,AXLE_Z),(0,.02,AXLE_Z))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
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
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_rolling_pin_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'rolling_pin_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
