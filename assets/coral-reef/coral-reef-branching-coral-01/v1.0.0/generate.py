"""Original continuous branching coral; no previous visible model is imported.
One fixed stylised prop, with one closed connected material boundary.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='coral-reef-branching-coral-01';VERSION='1.0.0';TITLE='Asymmetric Branching Coral'
DESCRIPTION=('One original static stylised branching coral, approximately .60 m wide, with a low integral attachment base, three unequal main branches and six progressively tapered blunt-ended secondary branches. Every junction and branch is one continuous closed editable mesh with shared surface vertices and real open negative spaces; there are no separate capped overlapping pipes, leaves, rocks or copied vegetation. Three constant opaque unlinked PBR tones, no textures. Metres, native Z up, front -Y, ground-level horizontal bounds centre. One complete prop only, not multiple branch or colour assets. Stylised visual form only; no species accuracy, living tissue, polyps, biological or ecological fidelity, growth, animation, underwater simulation, real attachment, load, safety, manufacturing or physical-performance claim. No water, seabed, reef rock, pot, label, other organism or scene.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FOOT_CONTACTS=[]
BODY='ContinuousBranchingCoral';FEET=[BODY]
PALETTE=[('WarmClayCoral',(.48,.155,.095,1),.86,0),('CoralUpperFaces',(.64,.255,.155,1),.86,0),('CoralDeepFaces',(.34,.087,.060,1),.9,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat,tag):self.f.append(tuple(self.vertex(x) for x in p));self.fm.append(mat);self.tags.append(tag)
 def quad(self,a,b,c,d,mat,tag):self.tri([a,b,c],mat,tag);self.tri([a,c,d],mat,tag)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),('not closed',[(k,v) for k,v in edges.items() if len(v)!=2][:8])
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  # Coherent directional colour zones, never random per-face noise.
  for i,f in enumerate(self.f):
   n=unit(cross(sub(self.v[f[1]],self.v[f[0]]),sub(self.v[f[2]],self.v[f[0]])))
   self.fm[i]=1 if n[2]>.47 else 2 if n[2]<-.42 else 0
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}
N=8
# Entire numerical branch graph is authored for this asset. Axes are not old
# shrub limbs; each node is a unified convex open-port junction surface.
CENTRES={'Root':(0,0,.055),'Left':(-.158,-.025,.255),'Tall':(.003,.068,.330),'Right':(.160,.020,.230)}
TIP_PATHS={
 'LeftOuter':[(-.252,-.045,.322),(-.287,-.039,.365)],
 'LeftInner':[(-.175,.005,.378),(-.164,.008,.425)],
 'TallLeft':[(-.038,.108,.446),(-.047,.110,.485)],
 'TallRight':[(.064,.076,.415),(.084,.061,.451)],
 'RightOuter':[(.260,.030,.280),(.292,.035,.322)],
 'RightInner':[(.190,-.026,.343),(.173,-.036,.390)]}
# Each endpoint is a finite outward-facing port, never a capped joint.
PORT_SPECS={
 'Root': [('Base',(0,0,0),(0,0,-1),.065),('L',(-.057,-.009,.126),unit(sub(CENTRES['Left'],CENTRES['Root'])),.023),('T',(.002,.028,.148),unit(sub(CENTRES['Tall'],CENTRES['Root'])),.021),('R',(.060,.007,.121),unit(sub(CENTRES['Right'],CENTRES['Root'])),.025)],
 'Left':[('In',add(CENTRES['Left'],mul(unit(sub(CENTRES['Root'],CENTRES['Left'])),.038)),unit(sub(CENTRES['Root'],CENTRES['Left'])),.019),('Outer',add(CENTRES['Left'],mul(unit(sub(TIP_PATHS['LeftOuter'][0],CENTRES['Left'])),.038)),unit(sub(TIP_PATHS['LeftOuter'][0],CENTRES['Left'])),.016),('Inner',add(CENTRES['Left'],mul(unit(sub(TIP_PATHS['LeftInner'][0],CENTRES['Left'])),.038)),unit(sub(TIP_PATHS['LeftInner'][0],CENTRES['Left'])),.015)],
 'Tall':[('In',add(CENTRES['Tall'],mul(unit(sub(CENTRES['Root'],CENTRES['Tall'])),.037)),unit(sub(CENTRES['Root'],CENTRES['Tall'])),.017),('Outer',add(CENTRES['Tall'],mul(unit(sub(TIP_PATHS['TallLeft'][0],CENTRES['Tall'])),.041)),unit(sub(TIP_PATHS['TallLeft'][0],CENTRES['Tall'])),.014),('Inner',add(CENTRES['Tall'],mul(unit(sub(TIP_PATHS['TallRight'][0],CENTRES['Tall'])),.041)),unit(sub(TIP_PATHS['TallRight'][0],CENTRES['Tall'])),.014)],
 'Right':[('In',add(CENTRES['Right'],mul(unit(sub(CENTRES['Root'],CENTRES['Right'])),.039)),unit(sub(CENTRES['Root'],CENTRES['Right'])),.020),('Outer',add(CENTRES['Right'],mul(unit(sub(TIP_PATHS['RightOuter'][0],CENTRES['Right'])),.039)),unit(sub(TIP_PATHS['RightOuter'][0],CENTRES['Right'])),.016),('Inner',add(CENTRES['Right'],mul(unit(sub(TIP_PATHS['RightInner'][0],CENTRES['Right'])),.039)),unit(sub(TIP_PATHS['RightInner'][0],CENTRES['Right'])),.015)]}
def ring(c,axis,r):
 axis=unit(axis);ref=(0,1,0) if abs(axis[1])<.9 else (1,0,0);u=unit(cross(axis,ref));v=cross(axis,u)
 return [add(c,mul(add(mul(u,math.cos(2*math.pi*i/N)),mul(v,math.sin(2*math.pi*i/N))),r)) for i in range(N)]
def poly(m,pts,tag):
 for i in range(1,len(pts)-1):m.tri([pts[0],pts[i],pts[i+1]],0,tag)
def hub(m,ports,label):
 pts=[p for q in ports.values() for p in q];groups=[set(range(i*N,(i+1)*N)) for i in range(len(ports))];found=set();port_found=set()
 for ia,ib,ic in itertools.combinations(range(len(pts)),3):
  a,b,c=pts[ia],pts[ib],pts[ic];n=cross(sub(b,a),sub(c,a));length=norm(n)
  if length<1e-11:continue
  n=mul(n,1/length);d=[dot(sub(p,a),n) for p in pts]
  if max(d)>1e-8 and min(d)<-1e-8:continue
  ids=frozenset(i for i,x in enumerate(d) if abs(x)<1e-8)
  if len(ids)<3 or ids in found:continue
  found.add(ids)
  if any(ids==g for g in groups):port_found.add(ids);continue
  if max(d)>1e-8:n=mul(n,-1)
  centre=mul(tuple(sum(pts[i][k] for i in ids) for k in range(3)),1/len(ids));u=unit(sub(pts[min(ids)],centre));v=cross(n,u)
  order=sorted(ids,key=lambda i:math.atan2(dot(sub(pts[i],centre),v),dot(sub(pts[i],centre),u)))
  poly(m,[pts[i] for i in order],label+'_ContinuousNodeSkin')
 assert len(port_found)==len(ports),(label,'buried/overlapping branch ports',len(port_found),len(ports))
def connect(m,a,b,label):
 # Preserve complete ring order but choose the least-twisted cyclic pairing.
 candidates=[q[k:]+q[:k] for q in [b,list(reversed(b))] for k in range(N)]
 b=min(candidates,key=lambda q:sum(dot(sub(x,y),sub(x,y)) for x,y in zip(a,q)))
 for i in range(N):j=(i+1)%N;m.quad(a[i],a[j],b[j],b[i],0,label+'_ContinuousTaper')
 return b
def coral(delta=0):
 # Positive delta expands the whole body; negative gives the finite material
 # inset. All external tips/base also move out/in, so no probe touches caps.
 m=Mesh();portmap={}
 for label,specs in PORT_SPECS.items():
  ports={}
  for name,c,axis,r in specs:
   if name=='Base':c=add(c,(0,0,-delta))
   ports[name]=ring(c,axis,r+delta)
  hub(m,ports,label);portmap[label]=ports
 poly(m,portmap['Root']['Base'],'WholeFiniteBaseSole')
 for port,node in [('L','Left'),('T','Tall'),('R','Right')]:connect(m,portmap['Root'][port],portmap[node]['In'],node+'_MainBranch')
 for node,port,tip in [('Left','Outer','LeftOuter'),('Left','Inner','LeftInner'),('Tall','Outer','TallLeft'),('Tall','Inner','TallRight'),('Right','Outer','RightOuter'),('Right','Inner','RightInner')]:
  a,b=TIP_PATHS[tip];axis=unit(sub(b,a));first=ring(a,unit(sub(b,CENTRES[node])),.0125+delta);second=ring(b,axis,.0075+delta);cap=ring(add(b,mul(axis,.008+delta)),axis,.0045+delta)
  prev=connect(m,portmap[node][port],first,tip+'_Taper1');prev=connect(m,prev,second,tip+'_Taper2');prev=connect(m,prev,cap,tip+'_BluntShoulder');poly(m,prev,tip+'_FiniteBluntCap')
 return m.result('One complete continuous low attachment base, three unequal main limbs, six tapered blunt-ended secondary branches and four shared-surface junctions.')
G[BODY]=coral()
# Origin is fixed to the whole original horizontal envelope, not each branch.
vv=G[BODY]['vertices'];SHIFT=tuple(-(min(p[i] for p in vv)+max(p[i] for p in vv))/2 for i in [0,1])+(0.,)
def shifted(g):
 g['vertices']=[add(p,SHIFT) for p in g['vertices']];return g
shifted(G[BODY]);SOLID_VOLUMES['WholeContinuousCoralMaterial']=dict(shifted(coral(-.003)),targets=[BODY])
# Entire finite surrounding air volume: outward box and inward expanded coral
# form two boundary components of one connected volume, not disconnected probes.
expanded=shifted(coral(.003));outer=[(-.38,-.20,-.04),(.38,.25,.57)]
def air_shell():
 m=Mesh();a,b=outer;v=[(a[0] if not i&1 else b[0],a[1] if not i&2 else b[1],a[2] if not i&4 else b[2]) for i in range(8)]
 for f in [(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:poly(m,[v[i] for i in f],'FiniteAirEnvelope')
 g=m.result('Finite outer air envelope');n=len(g['vertices']);g['vertices']+=expanded['vertices'];g['faces'] += [tuple(n+i for i in reversed(f)) for f in expanded['faces']];g['face_materials'] += [0]*len(expanded['faces']);g['face_tags']+=['ExpandedCoralCavityWall']*len(expanded['faces']);g['boundary_components']=2;g['targets']=[BODY];return g
VOID_VOLUMES['CompleteSurroundingAirIncludingEveryFork']=air_shell()
CONTRACT={'single_prop_count':1,'original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','horizontal_shift_m':SHIFT,'main_branch_count':3,'secondary_tip_count':6,'continuous_junction_count':4,'closed_meshes':1,'materials':3,'old_geometry_imports':0,'whole_material_inset_m':.003,'whole_air_cavity_expansion_m':.003,'air_boundary_components':2,'complete_base_at_z_m':0,'fixed_visual_only':True}
def measure_coral_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for vs in vertices.values() for p in vs];assert abs(min(p[2] for p in vv))<2e-7
 for i in [0,1]:assert abs(min(p[i] for p in vv)+max(p[i] for p in vv))<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],scope='Pure source/producer geometry only; independent actual GLB acceptance still required')
INSIDE_TESTS=[(BODY,add((0,0,.025),SHIFT),add((.30,-.10,.45),SHIFT))]
FOCUS=(0.,0.,.245);ORTHO=.79
CAMERAS={'gray-front3q':(1.4,-3.0,1.6),'gray-back3q':(-1.4,3.,1.6),'thumbnail':(1.4,-3.,1.6),'qa-front':(0,-3.,.90),'qa-side':(-3.,0.,.90),'qa-top':(0,0,3.),'qa-back':(0,3.,.90),'qa-wireframe':(-1.4,3.,1.6),'silhouette-128-front':(0,-3.,.90),'silhouette-128-side':(-3.,0.,.90)}
WIRE_THICKNESS=ORTHO/1500
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
root=bpy.data.objects.new('OneContinuousBranchingCoral',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete horizontal envelope centred, one complete low base sole Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_coral_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=3000
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'branching_coral_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/coral-reef/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'coral-reef','style':'hard-edge-faceted-nature','title':TITLE,'description':DESCRIPTION,
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
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
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
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
