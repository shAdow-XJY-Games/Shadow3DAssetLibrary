"""One newly authored continuous bottomless rebated hive super, static visual only.
No old beehive, crate, frame or other comparison geometry is imported or executed.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-open-rebated-hive-super-01';VERSION='1.0.0';TITLE='Open Rebated Hive Super'
DESCRIPTION=('One original continuous thick-walled wooden hive layer, truly open through top and bottom. Two complete integral upper inner end shoulders and two actual exterior blind recessed grips coexist with a full perimeter upper bearing ring, an inward registration lip and a complete receiving bottom mouth. One connected closed positive material shell. One module only; the second identical rigid +Z instance is a QA fixture for one fixed static interface and is neither exported nor rendered as another asset. No old hive/frame/crate geometry, base, floor, lid, frames, bees, honey, label or scene. Constant opaque unlinked PBR, no textures. Native Z up, front -Y, metres, horizontal envelope centred, full bottom annulus Z=0. No real hive standard, old-item compatibility, bee suitability, food-contact, load, stability, sealing, mechanical locking, arbitrary stack height, manufacturing, transport, continuous assembly or safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FOOT_CONTACTS=[]
BODY='ContinuousOpenRebatedHiveSuper';FEET=[BODY]
PALETTE=[('HoneyTimberLongGrain',(.48,.285,.115,1),.69,0),('WarmEndGrain',(.37,.205,.078,1),.77,0),('FreshCutInnerTimber',(.57,.365,.17,1),.73,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def quad(self,points,normal,mat,tag):
  if dot(cross(sub(points[1],points[0]),sub(points[2],points[0])),normal)<0:points=list(reversed(points))
  ids=[self.vertex(p) for p in points]
  for f in [(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])]:self.f.append(f);self.fm.append(mat);self.tags.append(tag)
 def result(self,role):return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}
# Entire original stepped wall profile. All numbers are explicit metres.
# A single exact cell decomposition emits only the external material boundary;
# shared grid vertices give conforming triangles at every wall/corner/step.
PROFILE=[(0.,.022,.320,.250,.308,.238),(.022,.214,.320,.250,.276,.206),(.214,.250,.320,.250,.292,.206),(.250,.266,.304,.234,.292,.206)]
GRIP={'floor_abs_x':.302,'half_y':.118,'z_low':.102,'z_high':.144}
REPEAT_Z=.250
PROBE_PROFILE=[(.001,.023,.319,.249,.309,.239),(.023,.213,.319,.249,.277,.207),(.213,.249,.319,.249,.293,.207),(.249,.265,.303,.233,.293,.207)]
PROBE_GRIP={'floor_abs_x':.301,'half_y':.119,'z_low':.101,'z_high':.145}
def in_material(p,profile=PROFILE,grip=GRIP):
 x,y,z=p
 for low,high,ox,oy,ix,iy in profile:
  if low<z<high and abs(x)<ox and abs(y)<oy and not(abs(x)<ix and abs(y)<iy):
   return not(abs(x)>grip['floor_abs_x'] and abs(y)<grip['half_y'] and grip['z_low']<z<grip['z_high'])
 return False
def cell_boundary(profile,grip,role):
 xs=sorted(set([s*v for r in profile for v in [r[2],r[4]] for s in [-1,1]]+[-grip['floor_abs_x'],grip['floor_abs_x']]))
 ys=sorted(set([s*v for r in profile for v in [r[3],r[5]] for s in [-1,1]]+[-grip['half_y'],grip['half_y']]))
 zs=sorted(set([v for r in profile for v in r[:2]]+[grip['z_low'],grip['z_high']]))
 axes=[xs,ys,zs];cells=set()
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    if in_material(tuple((axes[a][q]+axes[a][q+1])/2 for a,q in enumerate([i,j,k])),profile,grip):cells.add((i,j,k))
 m=Mesh()
 for cell in sorted(cells):
  for axis in range(3):
   others=[a for a in range(3) if a!=axis]
   for sign in [-1,1]:
    neighbor=list(cell);neighbor[axis]+=sign
    if tuple(neighbor) in cells:continue
    value=axes[axis][cell[axis]+(sign>0)];points=[]
    for p,q in [(0,0),(1,0),(1,1),(0,1)]:
     v=[0,0,0];v[axis]=value;v[others[0]]=axes[others[0]][cell[others[0]]+p];v[others[1]]=axes[others[1]][cell[others[1]]+q];points.append(v)
    normal=[0,0,0];normal[axis]=sign;c=tuple(sum(p[a] for p in points)/4 for a in range(3));mat=0;tag='Wall'
    if axis==0:mat=1;tag='OuterEndWall' if abs(value)==profile[0][2] else 'InnerEndWall'
    if axis==1:tag='OuterLongWall' if abs(value)==profile[0][3] else 'InnerLongWall'
    if axis==2:
     mat=2;tag='HorizontalStep'
     if value==profile[0][0]:tag='WholeBottomBearingRing'
     if value==profile[1][0]:tag='ReceivingMouthRoof'
     if value==profile[2][0]:tag='CompleteInnerEndShoulder'
     if value==profile[3][0]:tag='WholeUpperBearingRing'
     if value==profile[-1][1]:tag='WholeLipCrown'
    if c[2]>profile[3][0] and axis!=2:tag='WholeGuideLipWall';mat=2
    if axis==0 and abs(value)==grip['floor_abs_x'] and abs(c[1])<grip['half_y'] and grip['z_low']<c[2]<grip['z_high']:tag='BlindGripFloor';mat=1
    if abs(c[0])>grip['floor_abs_x'] and ((axis==1 and abs(value)==grip['half_y'] and grip['z_low']<c[2]<grip['z_high']) or (axis==2 and value in [grip['z_low'],grip['z_high']] and abs(c[1])<grip['half_y'])):tag='BlindGripSidewall';mat=2
    m.quad(points,normal,mat,tag)
 return m.result(role)
def box(lo,hi,role):
 m=Mesh()
 for axis in range(3):
  others=[a for a in range(3) if a!=axis]
  for sign in [-1,1]:
   points=[]
   for p,q in [(0,0),(1,0),(1,1),(0,1)]:
    v=[0,0,0];v[axis]=(lo if sign<0 else hi)[axis];v[others[0]]=(lo if p==0 else hi)[others[0]];v[others[1]]=(lo if q==0 else hi)[others[1]];points.append(v)
   normal=[0,0,0];normal[axis]=sign;m.quad(points,normal,0,'probe')
 return m.result(role)
G[BODY]=cell_boundary(PROFILE,GRIP,'One continuous closed genus-one bottomless hive layer with integral two inner end shoulders, two blind grips, full upper/lower bearing annuli and inward registration lip.')
SOLID_VOLUMES['EntireContinuousWallShoulderGripFloorLipMaterial']=dict(cell_boundary(PROBE_PROFILE,PROBE_GRIP,'Whole continuous positive material domain, every corner/wall/shoulder/grip floor and lip root; 1 mm boundary inset with exact oriented surface fidelity covering all inset margins.'),targets=[BODY])
# Complete overlapping union of finite empty boxes. Each covers its entire
# rectangular cross-section and every height interval, not a centre ray.
AIR_BOXES=[('WholeBottomReceivingMouth',[-.307,-.237,-.030],[.307,.237,.021]),('WholeMainThroughCavity',[-.275,-.205,.020],[.275,.205,.268]),('WholeTopEndRebateAndEgress',[-.291,-.205,.215],[.291,.205,.300])]
for name,lo,hi in AIR_BOXES:VOID_VOLUMES[name]=dict(box(lo,hi,'Complete finite empty rectangular domain with 1 mm boundary inset; overlapping union with adjacent height domains.'),targets=[BODY])
for sign in [-1,1]:
 lo,hi=([.303,-.117,.103],[.34,.117,.143]) if sign>0 else ([-.34,-.117,.103],[-.303,.117,.143])
 VOID_VOLUMES['WholeBlindGripCavity'+str(sign)]=dict(box(lo,hi,'Entire exterior blind grip recess including exterior egress, 1 mm inset from every blind floor and side wall.'),targets=[BODY])
# Immutable finite bearing-ring domain. Both copies are same asset and use only
# an exact pure Z translation; they never enter G or any output object list.
STACK_PATCHES=[[(.308,-.250),(.320,-.250),(.320,.250),(.308,.250)],[(-.320,-.250),(-.308,-.250),(-.308,.250),(-.320,.250)],[(-.308,.238),(.308,.238),(.308,.250),(-.308,.250)],[(-.308,-.250),(.308,-.250),(.308,-.238),(-.308,-.238)]]
STACK_AREA=.640*.500-.616*.476
STACK_CONTACT={'name':'EntireOpposedPerimeterBearingRing','a':'SameIDLowerInstance','b':'SameIDUpperInstance','origin_m':[0,0,0],'u':[1,0,0],'v':[0,1,0],'axis':[0,0,1],'plane_m':REPEAT_Z,'points':[(.314,0,REPEAT_Z),(-.314,0,REPEAT_Z),(0,.244,REPEAT_Z),(0,-.244,REPEAT_Z)],'minimum_patch_area_m2':STACK_AREA-1e-7,'declared_patch_area_m2':STACK_AREA,'declared_patch_polygons_uv_m':STACK_PATCHES,'interior_probe_offset_m':.0005}
GUIDE_GAPS=[('PositiveXGuideGap',[.3046,-.2334,.2506],[.3074,.2334,.2654]),('NegativeXGuideGap',[-.3074,-.2334,.2506],[-.3046,.2334,.2654]),('PositiveYGuideGap',[-.3074,.2346,.2506],[.3074,.2374,.2654]),('NegativeYGuideGap',[-.3074,-.2374,.2506],[.3074,-.2346,.2654]),('WholeLipAboveCrownGap',[-.3074,-.2374,.2666],[.3074,.2374,.2714])]
# The crown gap includes the full open centre: it is entirely empty at this level.
QA_TRANSFORMS=[[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],[[1,0,0,0],[0,1,0,0],[0,0,1,REPEAT_Z],[0,0,0,1]]]
CONTRACT={'single_asset_count':1,'exported_instance_count':1,'qa_only_instance_count':2,'native_axis_up':'Z','front_direction':'-Y','profile_z_outer_inner_m':PROFILE,'blind_grip_m':GRIP,'same_id_rigid_transforms':QA_TRANSFORMS,'repeat_direction':'+Z','repeat_distance_m':REPEAT_Z,'whole_bearing_contact_area_m2':STACK_AREA,'guide_side_clearance_m':.004,'guide_crown_clearance_m':.006,'minimum_blind_grip_back_material_m':.026,'whole_inner_shoulder_area_each_m2':.016*.412,'expected_euler_characteristic':0,'expected_connected_mesh_count':1,'old_imports':0,'continuous_assembly_or_physical_performance_claim':False}
def measure_hive_geometry(vertices):
 assert set(vertices)=={BODY};vv=vertices[BODY]
 for axis,low,high in [(0,-.32,.32),(1,-.25,.25),(2,0,.266)]:assert abs(min(p[axis] for p in vv)-low)<2e-7 and abs(max(p[axis] for p in vv)-high)<2e-7
 return dict(CONTRACT,scope='single original static open hive layer; same-ID second rigid instance only for independent finite interface QA')
INSIDE_TESTS=[(BODY,(.31,.16,.16),(0,0,.13))]
FOCUS=(0.,0.,.133);ORTHO=.95
CAMERAS={'gray-front3q':(1.8,-2.6,1.9),'gray-back3q':(-1.8,2.6,1.9),'thumbnail':(1.8,-2.6,1.9),'qa-front':(0,-3.,1.8),'qa-side':(3.,0.,1.5),'qa-top':(0,0,3.5),'qa-back':(0,3.,1.8),'qa-wireframe':(-1.8,2.6,1.9),'silhouette-128-front':(0,-3.,1.8),'silhouette-128-side':(3.,0.,1.5)}
WIRE_THICKNESS=ORTHO/1800
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
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneOpenRebatedHiveSuper',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete horizontal envelope centred, complete bottom bearing annulus Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_hive_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=3500
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'hive_super_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'modular','theme':'beekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
original_slots={o:list(o.data.materials) for o in parts};original_indices={o:[f.material_index for f in o.data.polygons] for o in parts}
original_socket_counts={m:len(m.node_tree.nodes.get('Principled BSDF').inputs) for m in asset_mats}
original_inputs={m:[(i,s.identifier,s.type,tuple(s.default_value) if hasattr(s.default_value,'__len__') else s.default_value) for i,s in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(s,'default_value')] for m in asset_mats}
def restore_materials():
 for m,values in original_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,kind,value in values:
   socket=p.inputs[index];assert socket.identifier==identifier and socket.type==kind;socket.default_value=value
 for o,slots in original_slots.items():
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for face,index in zip(o.data.polygons,original_indices[o]):face.material_index=index
 for m,values in original_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF');assert len(p.inputs)==original_socket_counts[m]
  for index,identifier,kind,value in values:
   socket=p.inputs[index];actual=tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value
   assert socket.identifier==identifier and socket.type==kind and actual==value,(m.name,index,identifier,actual,value)
 for o,slots in original_slots.items():
  assert len(o.data.materials)==len(slots) and list(o.data.materials)==slots
  assert len(o.data.polygons)==len(original_indices[o]) and [f.material_index for f in o.data.polygons]==original_indices[o]
 assert records(parts)==source_records
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
try:
 if gray:
  for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
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
finally:
 if gray:restore_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
