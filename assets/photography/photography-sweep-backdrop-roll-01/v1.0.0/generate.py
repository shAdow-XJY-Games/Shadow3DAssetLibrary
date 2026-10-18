"""Original static studio sweep roll. Metres, Z up. No motion or load claim."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-sweep-backdrop-roll-01';VERSION='1.0.0';TITLE='Continuous Sweep Backdrop Roll'
DESCRIPTION=('One original fixed partly unrolled studio backdrop visual prop. A single closed 10 mm thick stylized sheet makes four real separated spiral turns around a solid core, continues down the front, curves smoothly onto a finite floor tail, and stays visibly clear of two independent upright supports. '
 'The transverse shaft is captured by two thick bored fixed-interference seats, each supported by a post and a broad finite ground foot. Actual sheet-edge surfaces, inter-layer gaps, support joints and ground faces are measurable geometry, not texture lines. '
 'One complete assembly counts as one prop. Separate editable closed meshes, four solid PBR materials, no textures, cameras, lights, people or scene; metres, Z up, ground design datum at X midline and Y=0; the datum is not the bounding-box centre. '
 'Only one static display pose is checked. No winding or unwinding animation, textile or paper physics, tension, anti-tip stability, load bearing, standard dimensions, installation, safety certification, photographic color accuracy, optical performance or compatibility with previous camera or lighting assets is claimed.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={}
PALETTE=[('Backdrop_WarmIvory',(.82,.73,.56,1),.86,0),('Stand_Graphite',(.045,.058,.064,1),.57,.33),('Shaft_SatinSteel',(.32,.37,.39,1),.36,.70),('Seats_Ochre',(.74,.35,.075,1),.47,.35)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def basis(axis):
 a=unit(axis);u=unit(cross(a,(0,0,1) if abs(a[2])<.9 else (0,1,0)));v=cross(a,u);return a,u,v
def profile(name,origin,axis,rings,mat,role,n=32):
 a,u,v=basis(axis);vs=[];fs=[]
 for t,r in rings:
  for i in range(n):q=math.tau*i/n;vs.append(add(add(origin,mul(a,t)),add(mul(u,r*math.cos(q)),mul(v,r*math.sin(q)))))
 for j in range(len(rings)-1):
  for i in range(n):k=(i+1)%n;fs.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
def box(name,c,size,mat,role):
 vs=[(c[0]+x*size[0]/2,c[1]+y*size[1]/2,c[2]+z*size[2]/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,role)
def ring(name,x,outer,inner,depth):
 vs=[];fs=[];n=32
 for xx,rr in [(x-depth/2,outer),(x+depth/2,outer),(x-depth/2,inner),(x+depth/2,inner)]:
  for i in range(n):a=math.tau*i/n;vs.append((xx,.3+rr*math.cos(a),2.5+rr*math.sin(a)))
 for i in range(n):j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,3,'closed thick annular fixed shaft seat; isolated bore open; shaft overlaps bore by 5 mm radial interference; no rotation claimed')
# Feet are deliberately outside the sheet width: 130 mm lateral air gap.
for side,x in [('Left',-1.40),('Right',1.40)]:
 foot='Foot_'+side;post='Post_'+side;seat='Seat_'+side
 box(foot,(x,.3,.04),(.24,1.0,.08),1,'broad solid foot with finite 0.24 square metre ground face');FEET.append(foot)
 profile(post,(x,.3,0),(0,0,1),[(.060,.034),(2.445,.034)],1,'single continuous upright with buried ends',n=16)
 ring(seat,x,.100,.024,.130)
 link(foot,post,(x,.3,.070),(0,0,1),.002)
 link(post,seat,(x,.3,2.430),(1,0,0),.005)
 link(seat,'TransverseShaft',(x,.3,2.526),(1,0,0),.008)
 BORES.append({'mesh':seat,'origin_m':(x-.10,.3,2.5),'direction':(1,0,0),'length_m':.20})
profile('TransverseShaft',(0,.3,2.5),(1,0,0),[(-1.51,.029),(1.51,.029)],2,'continuous solid transverse shaft fixed within two interference seats')
profile('RollCore',(0,.3,2.5),(1,0,0),[(-1.22,.074),(1.22,.074)],2,'solid roll core with buried sheet root; no hollow cardboard or moving bearing claim',n=64)
link('RollCore','TransverseShaft',(0,.3,2.5),(1,0,0),.01)
# One path, one shell: a genuine four-turn spiral, drop, quarter-circle and floor tail.
# Sheet edges are both explicit offset surfaces, with closed width/end walls.
CY=.3;CZ=2.5;THICKNESS=.010;WIDTH=2.30;WIND_SEGMENTS=256;SWEEP_SEGMENTS=24
PATH=[]
for i in range(WIND_SEGMENTS+1):
 theta=8*math.pi*i/WIND_SEGMENTS;r=.071+.116*i/WIND_SEGMENTS
 PATH.append((CY-r*math.cos(theta),CZ-r*math.sin(theta)))
PATH += [(.100,2.20),(.100,.505)]
SWEEP_START=len(PATH)-1
for i in range(1,SWEEP_SEGMENTS+1):
 a=math.pi*.5*i/SWEEP_SEGMENTS;PATH.append((.100-.50*(1-math.cos(a)),.505-.50*math.sin(a)))
PATH.append((-1.20,.005));TAIL_START=len(PATH)-2
# Mitered offsets keep both surfaces parallel to every polyline segment.
NORMALS=[]
for i,p in enumerate(PATH):
 tangents=[]
 for a,b in [(max(0,i-1),i),(i,min(len(PATH)-1,i+1))]:
  if a==b:continue
  d=sub(PATH[b],PATH[a]);d=unit(d);tangents.append(d)
 normals=[(-t[1],t[0]) for t in tangents];n=unit(tuple(sum(x) for x in zip(*normals)));den=dot(n,normals[0]);NORMALS.append(mul(n,(THICKNESS/2)/den))
vs=[];fs=[]
for (y,z),(ny,nz) in zip(PATH,NORMALS):
 vs.extend([(-WIDTH/2,y+ny,z+nz),(WIDTH/2,y+ny,z+nz),(WIDTH/2,y-ny,z-nz),(-WIDTH/2,y-ny,z-nz)])
for i in range(len(PATH)-1):
 for j in range(4):k=(j+1)%4;fs.append((4*i+j,4*i+k,4*(i+1)+k,4*(i+1)+j))
fs += [(3,2,1,0),tuple(4*(len(PATH)-1)+i for i in range(4))]
mesh('ContinuousBackdropSheet',vs,fs,0,'single continuous closed thick shell: four separated physical turns, vertical drop, curved floor sweep and finite grounded tail')
# The first row is inside the core; root contact is a short finite volume, not a texture seam.
y,z=mul(add(PATH[0],PATH[1]),.5);link('ContinuousBackdropSheet','RollCore',(0,y,z),axis=(1,0,0),spread=.03)
for side,x in [('Left',-1.40),('Right',1.40)]:
 sign=-1 if x<0 else 1
 box('Empty_SheetSide_'+side,(sign*1.215,.1,1.1),(.10,.10,1.8),0,'test-only finite lateral sheet-to-support air volume');VOID_VOLUMES['Empty_SheetSide_'+side]=G.pop('Empty_SheetSide_'+side)
 GAPS.append({'name':'SheetToPost_'+side,'origin_m':(sign*1.17,.100,1.0),'direction':(sign,0,0),'length_m':.17})
for i,r in enumerate([.100,.129,.158]):
 name=f'Empty_Interlayer_{i}';box(name,(0,CY+r,CZ),(.12,.008,.008),0,'test-only finite closed interlayer gap volume');VOID_VOLUMES[name]=G.pop(name)
 GAPS.append({'name':name,'origin_m':(0,CY+r-.004,CZ),'direction':(0,1,0),'length_m':.008})
# Actual geometric predicates are independent of Blender and consume evaluated vertices.
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def distance_seg(a,b,c,d):
 def hit(a,b,c,d):
  u=sub(b,a);v=sub(d,c);w=sub(c,a);den=cross2(u,v)
  if abs(den)<1e-12:return False
  t=cross2(w,v)/den;s=cross2(w,u)/den;return -1e-9<=t<=1+1e-9 and -1e-9<=s<=1+1e-9
 if hit(a,b,c,d):return 0.0
 def pd(p,a,b):
  v=sub(b,a);t=max(0,min(1,dot(sub(p,a),v)/dot(v,v)));return math.dist(p,add(a,mul(v,t)))
 return min(pd(a,c,d),pd(b,c,d),pd(c,a,b),pd(d,a,b))
def poly_distance(a,b):
 def contains(p,poly):
  vals=[cross2(sub(y,x),sub(p,x)) for x,y in zip(poly,poly[1:]+poly[:1])];return min(vals)>=-1e-9 or max(vals)<=1e-9
 if contains(a[0],b) or contains(b[0],a):return 0.0
 return min(distance_seg(p,q,r,s) for p,q in zip(a,a[1:]+a[:1]) for r,s in zip(b,b[1:]+b[:1]))
def measure_backdrop_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 v=[tuple(float(c) for c in p) for p in vertices['ContinuousBackdropSheet']];assert len(v)==4*len(PATH)
 rows=[v[i:i+4] for i in range(0,len(v),4)];centres=[];thickness=[];cells=[]
 for row in rows:
  assert max(abs(p[0])-WIDTH/2 for p in row)<2e-6
  assert abs(row[0][0]+WIDTH/2)<2e-6 and abs(row[1][0]-WIDTH/2)<2e-6
  assert math.dist(row[0][1:],row[1][1:])<2e-6 and math.dist(row[2][1:],row[3][1:])<2e-6
  thickness.append(math.dist(row[0][1:],row[3][1:]));centres.append(mul(add(row[0][1:],row[3][1:]),.5))
 assert min(thickness)>=THICKNESS-2e-6 and max(thickness)<.0101,('Actual sheet wall thickness invalid',min(thickness),max(thickness))
 for i in range(len(rows)-1):cells.append([rows[i][0][1:],rows[i+1][0][1:],rows[i+1][3][1:],rows[i][3][1:]])
 # Every nonadjacent finite thick cell is checked, so flattening and self-intersection fail.
 min_gap=1e9;min_pair=None;pair_count=0;layer_gap=1e9
 bounds=[([min(p[k] for p in c) for k in range(2)],[max(p[k] for p in c) for k in range(2)]) for c in cells]
 for i,a in enumerate(cells):
  for j in range(i+2,len(cells)):
   pair_count+=1;la,ha=bounds[i];lb,hb=bounds[j]
   lower=math.hypot(max(0,lb[0]-ha[0],la[0]-hb[0]),max(0,lb[1]-ha[1],la[1]-hb[1]))
   layer_candidate=j<WIND_SEGMENTS and j-i>32
   if lower>min_gap and (not layer_candidate or lower>layer_gap):continue
   gap=poly_distance(a,cells[j]);assert gap>1e-6,('Actual sheet self-intersection',i,j,gap)
   if gap<min_gap:min_gap=gap;min_pair=[i,j]
   if layer_candidate:layer_gap=min(layer_gap,gap)
 assert layer_gap>.017,('Roll layers insufficiently separated',layer_gap)
 radii=[math.hypot(y-CY,z-CZ) for y,z in centres[:WIND_SEGMENTS+1]];angles=[]
 for y,z in centres[:WIND_SEGMENTS+1]:angles.append(math.atan2(-(z-CZ),-(y-CY)))
 increments=[(b-a+math.pi)%(2*math.pi)-math.pi for a,b in zip(angles,angles[1:])];turns=sum(increments)/math.tau
 assert abs(turns-4)<1e-5 and abs(radii[0]-.071)<2e-6 and abs(radii[-1]-.187)<2e-6
 assert all(b>a for a,b in zip(radii,radii[1:]))
 assert math.dist(centres[SWEEP_START],(.100,.505))<2e-6
 assert math.dist(centres[-2],(-.400,.005))<2e-6 and math.dist(centres[-1],(-1.20,.005))<2e-6
 floor=[rows[-2][0],rows[-2][1],rows[-1][1],rows[-1][0]]
 # At the floor, positive surface is underneath because the path runs toward -Y.
 assert max(abs(p[2]) for p in floor)<2e-6,('Tail is not grounded',floor)
 nominal_floor_area=WIDTH*(centres[-2][0]-centres[-1][0])
 floor_area=sum(math.sqrt(dot(cross(sub(floor[i],floor[0]),sub(floor[i+1],floor[0])),cross(sub(floor[i],floor[0]),sub(floor[i+1],floor[0]))))/2 for i in [1,2]);assert floor_area>1.83
 xgap=min(abs(float(p[0])) for n in FEET for p in vertices[n])-max(abs(p[0]) for p in v);assert xgap>.129
 return {'single_prop_count':1,'continuous_sheet_mesh_count':1,'actual_spiral_turns':turns,'actual_min_thickness_m':min(thickness),'actual_max_miter_thickness_m':max(thickness),'nonadjacent_thick_cell_pairs_tested':pair_count,'actual_min_nonadjacent_cell_surface_gap_m':min_gap,'minimum_pair':min_pair,'actual_nonadjacent_roll_layer_surface_gap_m':layer_gap,'actual_floor_tail_area_m2':floor_area,'nominal_centerline_tail_area_m2':nominal_floor_area,'actual_sheet_to_feet_lateral_gap_m':xgap,'support_feet_count':2,'fixed_interference_seats':2,'fixed_visual_only':True}

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
root=bpy.data.objects.new('OneStaticSweepBackdrop',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground design datum at X midline, Y=0, Z=0; not bounding-box centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name in ['RollCore','TransverseShaft']:
 tree=trees[name]
 assert inside(tree,(.01,.3,2.5)) is True
 assert inside(tree,(3,.3,2.5)) is False
 a,b,c=actual_triangles[id(tree)][0];centre=mul(add(add(a,b),c),1/3);normal=unit(cross(sub(b,a),sub(c,a)))
 assert inside(tree,add(centre,mul(normal,-1e-5))) is True
 assert inside(tree,add(centre,mul(normal,1e-5))) is False
 inside_predicate_selftests.append({'object':name,'inside_original_witness':True,'outside_rejected':True,'inside_10um_from_face':True,'outside_10um_from_face_rejected':True})
# A ray hits the shared diagonal of two triangles at one point: count one crossing.
probe=[[(1,0,0),(1,.742,0),(1,.742,1.058)],[(1,0,0),(1,.742,1.058),(1,0,1.058)]]
hits=triangle_ray_hits(probe,(0,0,0),unit((1,.371,.529)))
assert len(hits)==2 and len(set(round(t,8) for t in hits))==1
inside_predicate_selftests.append({'case':'two triangles sharing the hit diagonal','raw_hits':len(hits),'unique_boundary_crossings':len(set(round(t,8) for t in hits))})
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
mount_evidence=measure_backdrop_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'backdrop_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/photography/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,-.1,1.3));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.95;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-5.6,-7.5,4.4),'gray-back3q':(5.6,7.5,4.4)} if gray else {
 'thumbnail':(-5.6,-7.5,4.4),'qa-front':(0,-7,2.5),'qa-side':(7,0,2.5),'qa-top':(0,0,8),
 'qa-back':(0,7,2.5),'qa-wireframe':(-5.6,-7.5,4.4)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=3.95
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0055;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,1.3)),('silhouette-128-side',(7,0,1.3))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
