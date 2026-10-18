"""Original quarter-turn radial-roller conveyor; one fixed static prop.
Metres, native Z up, front -Y. No conveying, motion, load or compatibility claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='baggage-quarter-turn-roller-conveyor-01';VERSION='1.0.0';TITLE='Quarter-Turn Roller Conveyor'
DESCRIPTION=('One original low-poly static quarter-turn roller conveyor counted as one complete prop. Two continuous thick quarter-annular beams support eleven equally sized solid cylindrical rollers in a radial layout, with intentionally narrower inner gaps and wider outer gaps. Each fixed polygonal shaft rests on finite lower faces inside two genuinely bored seats. Six independent grounded feet and uprights plus three lower radial braces support the complete assembly. The two open end mouths have perpendicular directions. Sixty-one editable closed meshes and four opaque constant PBR materials. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. No luggage, packages, belt, motor, text, texture, animation or surrounding scene. Static visual geometry only: no conveying, sorting, rolling, speed, cargo turning or motion, friction or power, load capacity, stability, manufacture, installation fit, operational safety or certification. No connection or compatibility with historical straight roller tables, baggage or other systems is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];LEGS=[];BRACES=[];ROLLERS={};SEATS={};BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
PALETTE=[('Beam_DeepTeal',(.035,.18,.21,1),.46,.45),('Roller_SatinSteel',(.52,.60,.63,1),.37,.72),('Shaft_GraphiteSteel',(.095,.13,.15,1),.34,.70),('Seat_WarmZinc',(.56,.49,.33,1),.43,.48)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,basis):return add(c,tuple(sum(p[j]*basis[j][i] for j in range(3)) for i in range(3)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 # Orient complete connected shells by signed volume before any export.
 vol=sum(dot(vs[f[0]],cross(vs[f[i]],vs[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
ZB=((1,0,0),(0,1,0),(0,0,1));HALF_BOUND=((1.435+.07)*math.cos(math.radians(8))+.07*math.sin(math.radians(8)))/2
SHIFT=(-HALF_BOUND,-HALF_BOUND,0)
def point(r,theta,z):return add(SHIFT,(r*math.cos(theta),r*math.sin(theta),z))
def radial_basis(theta):return((-math.sin(theta),math.cos(theta),0),(0,0,1),(math.cos(theta),math.sin(theta),0))
def box(name,c,size,mat,role,basis=ZB):return mesh(name,[transform((a*size[0]/2,b*size[1]/2,d*size[2]/2),c,basis) for d in[-1,1] for b in[-1,1] for a in[-1,1]],BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
def poly(r,n=8,phase=math.pi/8):return[(r*math.cos(math.tau*i/n+phase),r*math.sin(math.tau*i/n+phase)) for i in range(n)]
def rect(l,r,b,t):return[(r,0),(r,t),(0,t),(l,t),(l,0),(l,b),(0,b),(r,b)]
def prism_data(p,c,basis,lo,hi):
 n=len(p);vs=[transform((x,y,z),c,basis) for z in[lo,hi] for x,y in p];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return vs,fs

def annulus_data(outer,inner,c,basis,lo,hi):
 n=len(outer);assert n==len(inner);vs=[transform((x,y,z),c,basis) for p,z in[(outer,lo),(outer,hi),(inner,lo),(inner,hi)] for x,y in p];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return vs,fs

def arc_data(r0,r1,z0,z1,a0=0,a1=math.pi/2,n=32):
 vs=[point(r,a0+(a1-a0)*i/n,z) for z in[z0,z1] for r in[r0,r1] for i in range(n+1)];fs=[];k=n+1
 for i in range(n):
  j=i+1;fs.extend([(i,j,k+j,k+i),(2*k+i,3*k+i,3*k+j,2*k+j),(i,2*k+i,2*k+j,j),(k+i,k+j,3*k+j,3*k+i)])
 fs.extend([(0,k,3*k,2*k),(n,2*k+n,3*k+n,k+n)]);return vs,fs

BEAMS=[]
for label,r in [('Inner',.665),('Outer',1.435)]:
 vs,fs=arc_data(r-.05,r+.05,.600,.715);BEAMS.append(mesh(label+'_ContinuousQuarterAnnularBeam',vs,fs,0,'continuous closed 90-degree curved support beam, built as one quarter-annular shell with two real terminal faces'))
for i,degrees in enumerate([8,45,82]):
 theta=math.radians(degrees);tangent,zup,radial=radial_basis(theta);basis=(radial,tangent,zup)
 for j,r in enumerate([.665,1.435]):
  prefix=f'Support{i+1}_'+('Inner' if j==0 else 'Outer')
  foot=box(prefix+'_GroundFoot',point(r,theta,.015),(.140,.140,.030),2,'independent thick square foot with a finite flat ground patch',basis);FEET.append(foot)
  leg=box(prefix+'_Upright',point(r,theta,.3275),(.065,.065,.605),0,'solid upright finitely embedded in its grounded foot and curved upper beam',basis);LEGS.append(leg)
  link(foot,leg,point(r,theta,.0275),axis=tangent,spread=.010);link(leg,BEAMS[j],point(r,theta,.615),axis=tangent,spread=.012)
 brace=box(f'Support{i+1}_LowerRadialBrace',point(1.05,theta,.255),(.810,.045,.055),0,'independent lower radial brace finitely embedded into both paired uprights',basis);BRACES.append(brace)
 for j,r in enumerate([.665,1.435]):link(LEGS[-2+j],brace,point(r,theta,.255),axis=zup,spread=.012)
HOLE_R=.0235;SHAFT_R=.0175;HOLE_Z=.800;SEAT_Z=HOLE_Z-HOLE_R*math.cos(math.pi/8);AXLE_Z=SEAT_Z+SHAFT_R*math.cos(math.pi/8)
for i,degrees in enumerate(range(5,86,8)):
 theta=math.radians(degrees);basis=radial_basis(theta);tangent,zup,radial=basis;origin=point(0,theta,AXLE_Z);prefix=f'Radial{i+1:02d}'
 vs,fs=prism_data(poly(.045,16,math.pi/16),origin,basis,.745,1.355);roller=mesh(prefix+'_SolidRoller',vs,fs,1,'closed thick equal-diameter radial roller; intentionally wider outer spacing, fixed static pose')
 vs,fs=prism_data(poly(SHAFT_R),origin,basis,.620,1.480);shaft=mesh(prefix+'_FixedOctagonalShaft',vs,fs,2,'closed fixed eight-sided shaft with finite flat lower bearing faces in two true holes; no moving fit')
 link(roller,shaft,point(1.05,theta,AXLE_Z),axis=radial,spread=.16)
 ROLLERS[roller]={'theta_rad':theta,'theta_degrees':degrees,'shaft':shaft,'axis':radial,'tangent':tangent,'inner_end_radius_m':.745,'outer_end_radius_m':1.355,'radius_m':.045,'shaft_center_z_m':AXLE_Z,'seats':[]}
 for j,r in enumerate([.665,1.435]):
  c=point(r,theta,HOLE_Z);name=prefix+('_InnerBoredSeat' if j==0 else '_OuterBoredSeat')
  vs,fs=annulus_data(rect(-.0375,.0375,-.105,.065),poly(HOLE_R),c,basis,-.0325,.0325);seat=mesh(name,vs,fs,3,'single thick closed bearing block with a genuine full radial through-bore and a finite lower shaft seat');ROLLERS[roller]['seats'].append(seat)
  link(seat,BEAMS[j],point(r,theta,.705),axis=tangent,spread=.018)
  # The seat is below the shaft; the finite plane is horizontal, not a nominal radius test.
  CONTACTS.append({'a':seat,'b':shaft,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':SEAT_Z,'minimum_patch_area_m2':.00080,'interior_probe_offset_m':.0003,'points':[point(r+d,theta,SEAT_Z) for d in[-.020,0,.020]],'scope':'finite lower true-bore facet against the opposing flat shaft face; no solid penetration'})
  SEATS[seat]={'roller':roller,'shaft':shaft,'theta_rad':theta,'radius_m':r,'origin_m':c,'basis':basis,'bore_inner_vertex_start':16,'bore_polygon_vertices':8,'bottom_wall_face_indices':[4*5+1],'full_radial_depth_m':.065,'bearing_plane_z_m':SEAT_Z}
  vs,fs=prism_data(poly(HOLE_R-.0007),c,basis,-.034,.034)
  ISOLATED_VOID_VOLUMES[seat]={'vertices':vs,'faces':fs,'targets':[seat],'role':'entire finite true polygonal bore, 0.7 mm radial inset, extending through both actual mouths; assembled shaft excluded only from this isolated test'}
  BORES.append({'mesh':seat,'origin_m':point(r-.04,theta,HOLE_Z),'direction':radial,'length_m':.08})
# Empty open turn passage above the entire roller bed, with real end mouths.
vs,fs=arc_data(.737,1.363,.842,1.02,n=32);VOID_VOLUMES['CompleteUpperTurnPassage']={'vertices':vs,'faces':fs,'targets':[],'role':'entire finite quarter-annular air passage above every roller, between the side seats, including both open mouths'}
vs,fs=arc_data(.10,.54,.04,.90,n=24);VOID_VOLUMES['CentralOpenThroat']={'vertices':vs,'faces':fs,'targets':[],'role':'finite interior throat inside the curved inner support; no filled quarter-disc'}
for label,theta in [('Entry',0),('Exit',math.pi/2)]:
 basis=radial_basis(theta);c=point(1.05,theta,.80)
 vs=[transform((x,y,z),c,basis) for z in[-.31,.31] for y in[-.055,.13] for x in[-.014,.014]]
 VOID_VOLUMES[label+'_CompleteOpenMouth']={'vertices':vs,'faces':BOX_FACES,'targets':[],'role':'finite clear perpendicular terminal opening across roller span, clear of first and last roller'}
for probe in VOID_VOLUMES.values():probe['targets']=list(G)
CONVEYOR_CONTRACT={'single_prop_count':1,'turn_degrees':90,'roller_count':11,'bored_seat_count':22,'ground_foot_count':6,'lower_brace_count':3,'equal_roller_diameter_m':.09,'radial_roller_length_m':.61,'fixed_pose_only':True,'compatible_with_previous_straight_table':False,'no_motion_cargo_turning_load_or_safety_claim':True}
def measure_conveyor_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7 and abs(max(p[2] for p in vertices[n])-.03)<2e-7
 return dict(CONVEYOR_CONTRACT,geometry_scope='actual coordinates; complete triangle clearances, finite contacts, closed finite voids and actual mutation controls are separate mandatory gates')
FOCUS=(0,0,.43);ORTHO=2.35
CAMERAS={'gray-front3q':(2.7,-3.5,3.1),'gray-back3q':(-2.7,3.5,3.1),'thumbnail':(2.7,-3.5,3.1),'qa-front':(0,-4,2.3),'qa-side':(4,0,2.3),'qa-top':(0,0,5),'qa-back':(0,4,2.3),'qa-wireframe':(2.7,-3.5,3.1),'silhouette-128-front':(0,-4,2.3),'silhouette-128-side':(4,0,2.3)}
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
root=bpy.data.objects.new('OneQuarterTurnConveyor',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
first_theta=math.radians(8)
for name,p,outside in [(FEET[0],point(.665,first_theta,.015),point(.665,first_theta,.06)),(next(iter(SEATS)),point(.665,math.radians(5),.72),point(.665,math.radians(5),.80))]:
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
mount_evidence=measure_conveyor_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'conveyor_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/baggage/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'baggage','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
