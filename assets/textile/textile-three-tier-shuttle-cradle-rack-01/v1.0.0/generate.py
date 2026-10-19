"""Original empty three-tier dual-end shallow-U shuttle cradle rack; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='textile-three-tier-shuttle-cradle-rack-01';VERSION='1.0.0';TITLE='Three-tier Shuttle Cradle Rack'
DESCRIPTION=('One original empty static three-tier weaving-shuttle cradle rack. Two thick chamfer-crowned side uprights stand on two finite flat feet and are tied by two narrow rear crossbeams. Six separate continuous thick U-section cradles form three opposed pairs. Each pair supports the two underside end regions of a single long shuttle; the broad centre remains truly empty rather than a solid shelf. Each cradle has a continuous 12 mm floor and distinct low front and rear lips with genuine open recesses. All three shuttle spaces are empty in this asset. Original numerical cradle and frame geometry, not a reduced spool rack or drying tray. Twelve named closed editable meshes, three opaque constant PBR materials, metres, source Z up, front -Y and ground-centre origin. No texture nodes or linked material inputs. An unchanged fixed earlier shuttle is used externally for three rigid-translation QA placements only, never added to this generator, native asset, GLB, formal images or prop count. Only the explicitly tested fixed positions of that exact version are described; no universal shuttle or loom compatibility, insertion or removal trajectory, movement, clamping, weaving, storage capacity, hand fit, material, load, strength, anti-tip, manufacturing, installation or safety performance is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='LeftSideUpright';CRADLES=[];TIERS=[.105,.235,.365]
PALETTE=[('WarmHoneyUprights',(.40,.205,.080,1),.64,0),('LightAshCradles',(.67,.425,.205,1),.65,0),('DarkTimberFeetAndTies',(.19,.092,.038,1),.67,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def within(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(within(p[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);break
  else:raise AssertionError(('untriangulable polygon',p,order))
 out.append(tuple(order));return out

def prism(poly,t0,t1,material=0,role='',transform=lambda p:p):
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for z in [t0,t1] for x,y in poly];tris=earclip2(poly)
 ff=[tuple(reversed(t)) for t in tris]+[tuple(i+n for i in t) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv],ff,material,role)
def contact(name,a,b,axis,p,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,p),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0004,'points':points or [p],'scope':scope})
def xprism(poly,x0,x1,material=0,role=''):
 return prism(poly,x0,x1,material,role,transform=lambda p:(p[2],p[0],p[1]))
def void(name,lo,hi,role):VOID_VOLUMES[name]=dict(box(lo,hi),targets=[],role=role)
def solid(name,g,target,role):SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
# The paired end uprights are original broad side cheeks. Every U-section
# terminates on a complete finite end patch at the inner cheek face.
for side,sgn in [('Left',-1),('Right',1)]:
 x0,x1=sorted([sgn*.202,sgn*.230]);f0,f1=sorted([sgn*.184,sgn*.248]);foot=side+'FlatFoot';frame=side+'SideUpright'
 G[foot]=box((f0,-.125,0),(f1,.125,.026),2,'One full continuous foot, complete finite flat sole at Z=0.');FEET.append(foot)
 FOOT_CONTACTS.append({'name':side+'CompleteGroundSole','mesh':foot,'x':sgn*.216,'y':0,'fixture_lo':[f0-.001,-.126,-.02],'fixture_hi':[f1+.001,.126,0],'minimum_area_m2':.015999,'expected_area_m2':.016})
 poly=[(-.075,.026),(.075,.026),(.075,.420),(.060,.440),(-.060,.440),(-.075,.420)]
 G[frame]=xprism(poly,x0,x1,0,'One closed thick broad end cheek with two real chamfered crown edges and full base resting on a flat foot.')
 contact(side+'FullFrameFootSeat',foot,frame,(0,0,1),(sgn*.216,0,.026),.004199,'Complete 28 by 150 mm upright base on the bounded foot top.',[(sgn*.216,y,.026) for y in [-.05,0,.05]])
 solid(side+'WholeFootMaterial',box((f0+.0005,-.1245,.0005),(f1-.0005,.1245,.0255)),foot,'Entire inset finite ground runner material body.')
 inset=[(-.0745,.0265),(.0745,.0265),(.0745,.4198),(.05975,.4395),(-.05975,.4395),(-.0745,.4198)]
 solid(side+'WholeUprightMaterial',xprism(inset,x0+.0005,x1-.0005),frame,'Entire inset side-cheek material from full base to both crown chamfers.')
 for i,z in enumerate(TIERS,1):
  name=f'Tier{i:02d}{side}ContinuousUCradle';a,b=sorted([sgn*.105,sgn*.202])
  section=[(-.058,z-.012),(.058,z-.012),(.058,z+.014),(.046,z+.014),(.046,z),(-.046,z),(-.046,z+.008),(-.058,z+.008)]
  G[name]=xprism(section,a,b,1,'One continuous thick U cradle: full 12 mm floor, 8 mm low front lip, 14 mm rear lip, real open recess and complete finite cheek-end root.');CRADLES.append(name)
  # Axis points from a into b; all face triangles, not only these witnesses,
  # determine finite contact area. Opposed full-side penetration is also audited.
  if sgn<0:aa,bb,axis=frame,name,(1,0,0)
  else:aa,bb,axis=name,frame,(1,0,0)
  contact(name+'FullRoot',aa,bb,axis,(sgn*.202,0,z-.006),.0016559,'Complete U-profile end patch on the side cheek; both lips and floor included.',[(sgn*.202,y,zz) for y,zz in [(0,z-.006),(-.052,z+.004),(.052,z+.007)]])
  ins=[(-.0575,z-.0115),(.0575,z-.0115),(.0575,z+.0135),(.0465,z+.0135),(.0465,z-.0005),(-.0465,z-.0005),(-.0465,z+.0075),(-.0575,z+.0075)]
  solid(name+'WholeContinuousUFloorAndLips',xprism(ins,a+.0005,b-.0005),name,'Complete continuous inset U material through full floor and both full-length lips; no sparse samples.')
# Rear ties retain broad physical end contacts, but stay outside every shuttle.
for label,z0,z1 in [('Lower',.050,.074),('Upper',.393,.411)]:
 name=label+'RearTie';G[name]=box((-.202,.059,z0),(.202,.075,z1),2,'One narrow rear transverse tie with full end faces against both side cheeks.')
 for side,sgn in [('Left',-1),('Right',1)]:
  frame=side+'SideUpright';aa,bb=(frame,name) if sgn<0 else (name,frame)
  contact(side+label+'FullTieEnd',aa,bb,(1,0,0),(sgn*.202,.067,(z0+z1)/2),(.075-.059)*(z1-z0)-1e-8,'Complete rear tie end against the actual cheek inner face.')
 solid(name+'WholeMaterial',box((-.2015,.0595,z0+.0005),(.2015,.0745,z1-.0005)),name,'Entire inset finite rear cross-tie material.')
# Three complete empty shuttle slots, with an additional full centre gap at
# each cradle-floor elevation. Nothing spans these middle gaps as a shelf.
for i,z in enumerate(TIERS,1):
 top=TIERS[i]-.0125 if i<3 else .4395
 void(f'Tier{i:02d}WholeShuttleSlot',(-.2015,-.0455,z+.0005),(.2015,.0455,top),'Complete empty slot between inner side cheeks and between the entire lower seat and next layer/top; whole body, no centre ray.')
 void(f'Tier{i:02d}WholeBetweenCradlesGap',(-.1045,-.0585,z-.0115),(.1045,.0585,z+.0145),'Entire middle gap between the two finite end cradles, including their floor and lip elevation; excludes solid shelf substitution.')
 void(f'Tier{i:02d}WholeFrontApproach',(-.2015,-.1245,z+.0145),(.2015,-.0585,top),'Complete finite front-open external space, a static clearance volume without insertion-trajectory claim.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
CONTRACT={'single_prop_count':1,'empty_tiers':3,'paired_cradle_count':3,'continuous_u_cradles':6,'flat_feet':2,'thick_side_uprights':2,'rear_ties':2,'mesh_count':12,'finite_opposed_contacts':len(CONTACTS),'whole_empty_domains':len(VOID_VOLUMES),'whole_material_domains':len(SOLID_VOLUMES),'tier_floor_heights_m':TIERS,'u_floor_thickness_m':.012,'front_lip_height_m':.008,'rear_lip_height_m':.014,'clear_inner_u_width_m':.092,'central_open_gap_x_m':.210,'external_qa_only_shuttle_instances':3,'shuttle_instances_in_asset':0,'fixed_pose_only':True,'ground_exported':False}
def measure_shuttle_rack_geometry(vertices):
 assert set(vertices)==set(G)
 assert len(vertices)==12 and len(CRADLES)==6
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for i,z in enumerate(TIERS,1):
  for side in ['Left','Right']:
   n=f'Tier{i:02d}{side}ContinuousUCradle';v=vertices[n]
   assert abs(min(p[2] for p in v)-(z-.012))<2e-7 and abs(max(p[2] for p in v)-(z+.014))<2e-7
   assert abs(max(p[0] for p in v)-min(p[0] for p in v)-.097)<2e-7
 return dict(CONTRACT,geometry_scope='Actual source/exported coordinates. Complete air/material bodies, finite contacts and full-surface relations remain required. Fixed old shuttle is outside this generator.')
INSIDE_TESTS=[('LeftSideUpright',(-.216,0,.20),(0,0,.20)),('Tier01LeftContinuousUCradle',(-.15,0,.099),(-.15,0,.115))]
FOCUS=(0,0,.214);ORTHO=.72
CAMERAS={'gray-front3q':(.68,-1.25,.89),'gray-back3q':(-.68,1.25,.89),'thumbnail':(.68,-1.25,.89),'qa-front':(0,-1.6,.78),'qa-side':(1.6,0,.78),'qa-top':(0,0,1.9),'qa-back':(0,1.6,.78),'qa-wireframe':(.68,-1.25,.89),'silhouette-128-front':(0,-1.6,.78),'silhouette-128-side':(1.6,0,.78)}
WIRE_THICKNESS=ORTHO/1600

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
root=bpy.data.objects.new('OneEmptyThreeTierShuttleCradleRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred two-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in INSIDE_TESTS:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate independent actual-GLB gates.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_shuttle_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'shuttle_rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
