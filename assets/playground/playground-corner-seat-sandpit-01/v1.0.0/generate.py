"""Original low-wide four-corner-seat sandpit, one complete static visual prop.
Metres, native Z up, front -Y. No child suitability, load or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='playground-corner-seat-sandpit-01';VERSION='1.0.0';TITLE='Low Corner-Seat Sandpit'
DESCRIPTION=('One original low-wide chamfered sandpit, counted as one complete static visual prop. A continuous thick octagonal pit has a full 60 mm floor and eight low walls. A separate closed 100 mm sand layer sits over its entire bottom on that floor, with a positive continuous side clearance and a flat subtly colour-faceted top below the rim. Four broad thick bevel-edged corner seat plates span both adjacent low walls, with their complete finite bearing regions opposed to the actual rim and with the remaining underside visibly open above the sand. Six editable closed meshes and four constant opaque PBR colours; metres, native Z up, front -Y and bounds-centred ground origin. No scene ground, people, tools, toys, sand castle, particles, physics or animation. All low basin, sand and corner-seat geometry is newly authored, not a resized planter, recoloured roundabout or extracted old bench. Fixed static visual arrangement only: no child suitability, human fit, seating performance, load, strength, stability, fall protection, hygiene, sand safety, capacity, standard depth, manufacture, installation compatibility or public-safety certification.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};SEATS=[]
PALETTE=[('Pit_DeepTeal',(.045,.20,.205,1),.76,0),('Seat_WarmTimber',(.56,.285,.105,1),.73,0),('Sand_WarmCream',(.68,.53,.31,1),.93,0),('Sand_SoftOchre',(.64,.49,.28,1),.93,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def ccw(p):return p if area2(p)>0 else list(reversed(p))
def polyarea(p):return abs(area2(p))*.5

def inset_convex(poly,d):
 p=ccw(list(poly));lines=[]
 for a,b in zip(p,p[1:]+p[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy);n=(-dy/ln,dx/ln);lines.append((n[0],n[1],n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for i,(a,b,c) in enumerate(lines):
  d1,e,f=lines[i-1];det=a*e-b*d1;q=((c*e-b*f)/det,(a*f-c*d1)/det)
  assert all(n*q[0]+m*q[1]>=v-1e-8 for n,m,v in lines),(poly,d,q)
  out.append(q)
 return out

def clip(poly,n,c):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=dot(n,a)-c;db=dot(n,b)-c;ia=da<=1e-12;ib=db<=1e-12
  if ia!=ib:out.append(add(a,mul(sub(b,a),da/(da-db))))
  if ib:out.append(b)
 clean=[]
 for p in out:
  if not clean or math.dist(p,clean[-1])>1e-9:clean.append(p)
 if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-9:clean.pop()
 return ccw(clean)

def mesh(name,vs,fs,material,role,tags=None,face_materials=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 if face_materials:g['face_materials']=face_materials
 G[name]=g;return name

def prism(poly,z0,z1):
 p=ccw(list(poly));n=len(p);vs=[(x,y,z) for z in[z0,z1] for x,y in p];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 return vs,fs

def ring(outer,inner,z0,z1):
 n=len(outer);assert len(inner)==n;vs=[(x,y,z) for z in[z0,z1] for loop in[outer,inner] for x,y in loop];fs=[]
 for i in range(n):
  j=(i+1)%n
  fs += [(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),(j,i,n+i,n+j),(2*n+i,2*n+j,3*n+j,3*n+i)]
 return vs,fs

def probe(name,vf,targets,role,solid=False):
 vs,fs=vf;(SOLID_VOLUMES if solid else VOID_VOLUMES)[name]={'vertices':vs,'faces':fs,'targets':targets,'role':role}

def contact(a,b,z,area,points,scope):
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':(0,0,1),'u':(1,0,0),'v':(0,1,0),'plane_m':z,'minimum_patch_area_m2':area-.000001,'expected_complete_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':[(x,y,z) for x,y in points],'scope':scope})

OUTER=[(-.75,-1.08),(.75,-1.08),(1.08,-.75),(1.08,.75),(.75,1.08),(-.75,1.08),(-1.08,.75),(-1.08,-.75)]
INNER=inset_convex(OUTER,.12);SAND_POLY=inset_convex(INNER,.012)
BODY='One_ContinuousClosedBottomPit';SAND='Complete_ClosedSandLayer'
# A single connected boundary directly joins ground, outer walls, rim, inner
# walls and full inner floor. No stacked box seams, hidden intersecting blocks,
# Boolean approximation, texture displacement or pre-existing asset geometry.
n=8;vs=[(x,y,z) for loop,z in[(OUTER,0),(OUTER,.24),(INNER,.24),(INNER,.06)] for x,y in loop];fs=[tuple(reversed(range(n)))];tags=['ground']
for i in range(n):
 j=(i+1)%n
 fs += [(i,j,n+j,n+i),(n+i,n+j,2*n+j,2*n+i),(2*n+i,2*n+j,3*n+j,3*n+i)];tags += ['outer_wall','rim','inner_wall']
fs.append(tuple(3*n+i for i in range(n)));tags.append('floor')
mesh(BODY,vs,fs,0,'one continuous thick closed-bottom low octagonal pit, eight uninterrupted walls and complete floor',tags);FEET.append(BODY)
vs,fs=prism(SAND_POLY,.06,.16);fs.pop(1);vs.append((0,0,.16));fs += [(16,8+i,8+(i+1)%8) for i in range(8)]
tags=['sand_bottom']+['sand_side']*8+['sand_top']*8
mesh(SAND,vs,fs,2,'one closed thick sand layer with its entire bottom finitely seated on the pit floor; a flat eight-facet constant-colour top',tags,[2]*9+[2,2,3,2,2,3,2,2])
contact(BODY,SAND,.06,polyarea(SAND_POLY),[(-.6,0),(0,0),(.6,0)],'entire closed sand bottom, not point supports, on the full pit floor')
SEAT_POLYGONS={};UNDER_SEAT_POLYGONS={}
for label,sx,sy in[('NE',1,1),('NW',-1,1),('SW',-1,-1),('SE',1,-1)]:
 p=ccw([(sx*x,sy*y) for x,y in[(1.08,.30),(1.08,.75),(.75,1.08),(.30,1.08)]]);top=inset_convex(p,.012);vs=[(x,y,z) for loop,z in[(p,.24),(p,.283),(top,.295)] for x,y in loop];fs=[(3,2,1,0)]+[(i,(i+1)%4,4+(i+1)%4,4+i) for i in range(4)]+[(4+i,4+(i+1)%4,8+(i+1)%4,8+i) for i in range(4)]+[(8,9,10,11)]
 name=label+'_BroadCornerSeat';mesh(name,vs,fs,1,'one 55 mm thick broad bevel-edged cut-corner plate spanning both adjacent walls with a complete finite three-part rim bearing', ['seat_bottom']+['seat_side']*4+['seat_bevel']*4+['seat_top']);SEATS.append(name);SEAT_POLYGONS[name]=p
 overhang=clip(INNER,(-sx,-sy),-1.38);UNDER_SEAT_POLYGONS[name]=overhang
 contact(BODY,name,.24,polyarea(p)-polyarea(overhang),[(sx*.99,sy*.55),(sx*.55,sy*.99),(sx*.90,sy*.90)],'entire actual corner-plate/rim overlap across both straight wall tops and the diagonal wall top; remaining underside is explicitly nonbearing')
# Complete finite void partition: the full central opening, four under-seat
# corner cells, and the complete eight-sided sand/wall air ring below sand top.
CENTRAL=INNER
for sx,sy in[(1,1),(-1,1),(-1,-1),(1,-1)]:CENTRAL=clip(CENTRAL,(sx,sy),1.38)
probe('Whole_CentralOpenAir',prism(inset_convex(CENTRAL,.001),.161,.70),list(G),'whole finite central open body above sand and between all four seat inner edges; 1 mm face margins')
for name,p in UNDER_SEAT_POLYGONS.items():probe('Whole_UnderSeatAir_'+name,prism(inset_convex(p,.001),.161,.239),list(G),'entire remaining nonbearing seat underside corner cell between sand top and seat bottom; 1 mm face margins')
probe('Whole_SandSideAirRing',ring(inset_convex(INNER,.001),inset_convex(SAND_POLY,-.001),.061,.159),list(G),'continuous full eight-sided positive sand/wall air ring, not local probes')
probe('Whole_PitFloorMaterial',prism(inset_convex(OUTER,.001),.001,.059),[BODY],'whole complete floor inset slab; 1 mm margins',True)
probe('Whole_EightWallMaterial',ring(inset_convex(OUTER,.001),inset_convex(INNER,-.001),.061,.239),[BODY],'whole continuous eight-wall inset ring material',True)
probe('Whole_WallFloorRootMaterial',ring(inset_convex(OUTER,.001),inset_convex(INNER,-.001),.059,.061),[BODY],'complete continuous eight-wall/floor root crossing the floor-height datum',True)
SELFTESTS=[(BODY,(0,0,.03),(0,0,.20)),(SAND,(0,0,.10),(0,0,.20))]
SANDPIT_CONTRACT={'single_prop_count':1,'continuous_closed_bottom_pit':1,'fully_floor_seated_closed_sand_layer':1,'broad_corner_seats':4,'pit_floor_thickness_m':.06,'pit_wall_height_m':.24,'pit_wall_normal_thickness_m':.12,'sand_thickness_m':.10,'sand_wall_full_side_clearance_m':.012,'sand_top_below_rim_m':.08,'seat_total_thickness_m':.055,'whole_finite_contacts':5,'whole_empty_partition_cells':6,'whole_material_probes':3,'dimensions_only_visual_no_human_or_standard_claim':True}
def measure_sandpit_geometry(vertices):
 assert set(vertices)==set(G)
 for name,expected in[(BODY,([ -1.08,-1.08,0],[1.08,1.08,.24])),(SAND,([-.948,-.948,.06],[.948,.948,.16]))]:
  for k in range(3):assert abs(min(p[k] for p in vertices[name])-expected[0][k])<2e-7 and abs(max(p[k] for p in vertices[name])-expected[1][k])<2e-7,(name,k)
 for name in SEATS:assert abs(min(p[2] for p in vertices[name])-.24)<2e-7 and abs(max(p[2] for p in vertices[name])-.295)<2e-7
 return dict(SANDPIT_CONTRACT,geometry_scope='actual coordinates; complete closed shell, full contacts, whole air/material and noncontact surface checks still required')
FOCUS=(0,0,.105);ORTHO=3.24
CAMERAS={'gray-front3q':(4.5,-5.8,4.6),'gray-back3q':(-4.5,5.8,4.6),'thumbnail':(4.5,-5.8,4.6),'qa-front':(0,-6.8,3.4),'qa-side':(6.8,0,3.4),'qa-top':(0,0,7),'qa-back':(0,6.8,3.4),'qa-wireframe':(4.5,-5.8,4.6),'silhouette-128-front':(0,-6.8,3.4),'silhouette-128-side':(6.8,0,3.4)}
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
root=bpy.data.objects.new('OneCornerSeatSandpit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in SELFTESTS:
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
mount_evidence=measure_sandpit_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'sandpit_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/playground/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
