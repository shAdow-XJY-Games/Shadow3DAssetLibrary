"""Original dual-ended A-frame sheet storage rack, one fixed static visual prop.
Metres, native Z up, front -Y. No load, stability, operation or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carpentry-a-frame-sheet-storage-rack-kit-01';VERSION='1.0.0';TITLE='A-Frame Sheet Storage Rack'
DESCRIPTION=('One original dual-ended A-frame sheet storage rack, counted as one fixed static prop including two inclined thick boards. Two flat-ground runners, four sloped uprights, two cross ties, two apex caps, two longitudinal beams and a central diagonal connect the two open end frames. Two full-length thick bottom bearers and toe stops hold the two original fixed boards. Each board has a horizontal bevel-cut bottom face and a short lower front shoulder giving complete finite opposed contact with its bearer and toe stop; its inclined back bears on two matching finite strips. All joints use opposed finite face patches, with actual empty space between the boards and inside each end frame. Twenty-three editable closed meshes; four opaque constant PBR materials; metres, native Z up, front -Y, horizontally bounds-centred ground origin. No extra stock pile, saw, wheels, people, scene or animation. Static visual appearance only: no load capacity, strength, friction, stability, anti-tip, stock-size compatibility, loading access, ergonomics, manufacture, construction, installation or work-safety certification. No compatibility with historical sawhorse, pallet-rack, dish-rack or ladder interfaces is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];ISOLATED_VOID_VOLUMES={};VOID_VOLUMES={};BOARDS=[];BEARERS=[];STOPS=[];STRIPS=[];LEGS=[];CAPS=[];CROSSBARS=[];BEAMS=[];BRACES=[]
PALETTE=[('Frame_DeepPetrol',(.035,.16,.18,1),.60,.30),('Sheet_PaleBirch',(.72,.54,.31,1),.78,0),('Sheet_HoneyBirch',(.48,.27,.105,1),.78,0),('Runner_Charcoal',(.045,.055,.06,1),.75,.08)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def prism_geometry(x,width,yz):
 if sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(yz,yz[1:]+yz[:1]))<0:yz=list(reversed(yz))
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return vs,fs
def prism_x(name,x,width,yz,mat,role):return mesh(name,*prism_geometry(x,width,yz),mat,role)
def prism_y(name,y,width,xz,mat,role):
 vs,fs=prism_geometry(y,width,xz);return mesh(name,[(b,a,c) for a,b,c in vs],[tuple(reversed(f)) for f in fs],mat,role)
def contact(a,b,axis,point,area,scope):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':[add(point,mul(u,d)) for d in[-.015,0,.015]],'scope':scope})
def void_x(name,x,w,yz,scope):
 vs,fs=prism_geometry(x,w,yz);VOID_VOLUMES[name]={'vertices':vs,'faces':fs,'targets':[],'role':scope}
def void_y(name,y,w,xz,scope):
 vs,fs=prism_geometry(y,w,xz);VOID_VOLUMES[name]={'vertices':[(b,a,c) for a,b,c in vs],'faces':[tuple(reversed(f)) for f in fs],'targets':[],'role':scope}
XS=[-.90,.90];SIGNS=[-1,1]
for k,x in enumerate(XS):
 foot=box('End_%d_GroundRunner'%k,(x,0,.04),(.16,1.60,.08),3,'continuous flat-bottom ground runner for one open A end frame');FEET.append(foot)
 cap=box('End_%d_ApexCap'%k,(x,0,1.49),(.14,.204,.08),0,'finite top cap meeting both inclined upright tops');CAPS.append(cap)
 bar=prism_x('End_%d_LowerCrossTie'%k,x,.14,[(-.462,.30),(.462,.30),(.422,.40),(-.422,.40)],0,'horizontal end tie with two sloped full end faces on inward upright planes');CROSSBARS.append(bar)
 for s in SIGNS:
  label='Front' if s<0 else 'Back';n=(0,s,.4)
  leg=prism_x('End_%d_%s_InclinedUpright'%(k,label),x,.14,[(s*.55,.08),(s*.65,.08),(s*.102,1.45),(s*.002,1.45)],0,'original full-thickness sloped upright, horizontal bottom/top and parallel inclined inner/outer faces');LEGS.append(leg)
  contact(foot,leg,(0,0,1),(x,s*.60,.08),.01399,'complete finite upright horizontal bottom on runner top')
  contact(leg,cap,(0,0,1),(x,s*.052,1.45),.01399,'complete finite upright horizontal top on cap underside')
  contact(bar,leg,n,(x,s*(.582-.4*.35),.35),.01507,'complete inclined cross-tie end against inward upright face')
  strip=prism_x('End_%d_%s_BackBearingStrip'%(k,label),x,.12,[(s*(.682-.4*.44),.44),(s*(.717-.4*.44),.44),(s*(.717-.4*1.29),1.29),(s*(.682-.4*1.29),1.29)],3,'0.85 m long finite inclined bearing strip with matching parallel support faces');STRIPS.append(strip)
  contact(leg,strip,n,(x,s*(.682-.4*.865),.865),.10985,'entire 0.12 by 0.85 m inclined strip underside against upright')
for label,z,h,w in [('Lower',.35,.10,.12),('Upper',1.49,.06,.13)]:
 beam=box(label+'_LongitudinalBeam',(0,0,z),(1.66,w,h),0,'continuous longitudinal beam whose complete ends meet both end frames');BEAMS.append(beam)
 supports=CROSSBARS if label=='Lower' else CAPS
 contact(supports[0],beam,(1,0,0),(-.83,0,z),w*h-.00001,'complete left beam end against end-frame inner face')
 contact(beam,supports[1],(1,0,0),(.83,0,z),w*h-.00001,'complete right beam end against end-frame inner face')
brace=prism_y('Central_LongitudinalDiagonal',0,.08,[(-.60,.40),(-.50,.40),(.60,1.46),(.50,1.46)],0,'one continuous diagonal linking lower and upper beams with full horizontal cut end faces');BRACES.append(brace)
contact(BEAMS[0],brace,(0,0,1),(-.55,0,.40),.00799,'whole lower horizontal cut end of longitudinal diagonal')
contact(brace,BEAMS[1],(0,0,1),(.55,0,1.46),.00799,'whole upper horizontal cut end of longitudinal diagonal')
for j,s in enumerate(SIGNS):
 label='Front' if s<0 else 'Back';n=(0,s,.4)
 bearer=prism_x(label+'_ContinuousBottomBearer',0,2.30,[(s*.660,.08),(s*.770,.08),(s*.770,.20),(s*.612,.20)],0,'full-length thick bottom bearer with sloped inner clearance face and horizontal top seat');BEARERS.append(bearer)
 for k,x in enumerate(XS):contact(FEET[k],bearer,(0,0,1),(x,s*.715,.08),.01759,'complete finite runner-top/bearer-bottom overlap at each end')
 stop=box(label+'_ContinuousToeStop',(0,s*.707,.225),(2.30,.060,.050),3,'continuous solid front toe stop with full base on bottom bearer');STOPS.append(stop)
 contact(bearer,stop,(0,0,1),(0,s*.707,.20),.13799,'whole full-length toe-stop underside on continuous bearer')
 board=prism_x(label+'_FixedInclinedBoard',0,2.20,[(s*.637,.20),(s*.677,.20),(s*.677,.25),(s*.657,.25),(s*.165,1.48),(s*.125,1.48)],1+j,'one fixed inclined thick original board with bevel-cut horizontal bottom and short front shoulder; internal witness part of one rack');BOARDS.append(board)
 contact(bearer,board,(0,0,1),(0,s*.657,.20),.08799,'entire 2.20 by 0.04 m horizontal cut board bottom supported by bearer')
 # The stop and board share an actual finite vertical shoulder, not a line.
 contact(board,stop,(0,s,0),(0,s*.677,.225),.10999,'whole 2.20 by 0.05 m lower board shoulder against inner toe-stop face')
 for k,x in enumerate(XS):contact('End_%d_%s_BackBearingStrip'%(k,label),board,n,(x,s*(.717-.4*.865),.865),.10985,'entire 0.12 by 0.85 m inclined board-back/strip contact at each end')
# Complete closed void bodies, inset 1 mm from their bounding actual surfaces.
for k,x in enumerate(XS):
 for label,z0,z1 in [('BelowTie',.081,.299),('AboveTie',.401,1.449)]:
  a=.582-.4*z0-.001;b=.582-.4*z1-.001
  void_x('End_%d_%s_OpenA'%(k,label),x,.138,[(-a,z0),(a,z0),(b,z1),(-b,z1)],'complete open A-frame aperture between inward upright faces, runner/cross-tie/cap')
for s in SIGNS:
 yz=[(s*.066,.201),(s*(.717-.4*.201-.001),.201),(s*(.717-.4*1.479-.001),1.479),(s*.066,1.479)]
 void_x(('Front' if s<0 else 'Back')+'_WholeBetweenBoardCorridor',0,1.658,yz,'complete finite between-board lateral corridor outside longitudinal beam/brace envelope, between both end-frame slices')
for label,z0,z1,intercept in [('UnderBearerInnerBay',.081,.199,.692),('BelowLowerBeam',.201,.299,.717)]:
 a=intercept-.4*z0-.001;b=intercept-.4*z1-.001
 void_x(label,0,1.658,[(-a,z0),(a,z0),(b,z1),(-b,z1)],'full finite lower inside bay between both end frames and the two sloped bearer/board inside boundaries')
z0=.401;z1=1.449;slope=1.10/1.06
left=lambda z:-.60+slope*(z-.40)
right=lambda z:-.50+slope*(z-.40)
void_y('Central_LeftOfDiagonal',0,.078,[(-.829,z0),(left(z0)-.001,z0),(left(z1)-.001,z1),(-.829,z1)],'complete central open wedge left of the diagonal, between longitudinal beams')
void_y('Central_RightOfDiagonal',0,.078,[(right(z0)+.001,z0),(.829,z0),(.829,z1),(right(z1)+.001,z1)],'complete central open wedge right of the diagonal, between longitudinal beams')
for g in VOID_VOLUMES.values():g['targets']=list(G)
RACK_CONTRACT={'single_prop_count':1,'original_fixed_boards':2,'complete_open_A_end_frames':2,'continuous_ground_runners':2,'inclined_uprights':4,'continuous_bottom_bearers':2,'continuous_toe_stops':2,'finite_inclined_back_strips':4,'finite_opposed_contacts':len(CONTACTS),'empty_volume_count':len(VOID_VOLUMES),'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_rack_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in BOARDS:
  v=vertices[n];assert abs(min(p[0] for p in v)+1.10)<2e-7 and abs(max(p[0] for p in v)-1.10)<2e-7
  assert abs(min(p[2] for p in v)-.20)<2e-7 and abs(max(p[2] for p in v)-1.48)<2e-7
 return dict(RACK_CONTRACT,geometry_scope='actual source/exported coordinates; full contacts, complete voids, all noncontact surfaces and real mutations still required')
FOCUS=(0,0,.72);ORTHO=3.25
CAMERAS={'gray-front3q':(4.6,-6.3,4.0),'gray-back3q':(-4.6,6.3,4.0),'thumbnail':(4.6,-6.3,4.0),'qa-front':(0,-6.8,2.8),'qa-side':(6.8,0,2.8),'qa-top':(0,0,7.0),'qa-back':(0,6.8,2.8),'qa-wireframe':(4.6,-6.3,4.0),'silhouette-128-front':(0,-6.8,2.8),'silhouette-128-side':(6.8,0,2.8)}
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
root=bpy.data.objects.new('OneAFrameSheetStorageRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.90,0,.04),(-.90,0,.09)),(BOARDS[0],(0,-.337,1.0),(0,-.38,1.0))]:
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
mount_evidence=measure_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carpentry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
