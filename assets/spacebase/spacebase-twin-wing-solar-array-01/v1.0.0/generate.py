"""Original fixed twin-wing solar-array visual prop. New numeric geometry only.
No functional, power, deployment, safety or prior-interface compatibility claim.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='spacebase-twin-wing-solar-array-01';VERSION='1.0.0';TITLE='Twin-Wing Solar Array'
DESCRIPTION=('One original static spacebase solar-array visual prop: a single central thick mast and full transverse rear spar carry two widely separated inclined three-bay continuous ladder frames and six complete thick panel bodies. Each panel has an integral two-by-five colour-cell surface pattern, real edges and rear surface, with complete finite underside support on its real frame. Six true frame windows remain open underneath; a broad central split separates the wings. A chamfer-corner full grounded base supports the mast. Eleven closed connected editable meshes and four ordinary opaque constant unlinked PBR materials, metres, native Z up, front -Y and base-centre ground origin. One fixed28-degree pose only, one prop and zero scenes. Original newly authored dimensions and geometry; no old solar rack, lamp, flag, lightbox, platform or cabinet geometry imported, resized or recoloured. No texture, transparency, light emission, labels, cable, battery, actuator, terrain, animation or variants. Only illustrative model appearance: no power generation, electrical connections, solar exposure or efficiency, tracking, unfolding, mechanical operation, load, stability, spaceflight performance, manufacture, structural or electrical safety, installation or compatibility with earlier spacebase modules is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=['ChamferedWholeGroundBase'];FOOT_CONTACTS=[]
BASE=FEET[0];MAST='WholeCentralMast';SPAR='WholeTransverseBackSpar';FRAMES=[];PANELS=[];BODY='RightThreeBayContinuousFrame';LEGS=[]
PALETTE=[('Frame_SatinSilver',(.45,.53,.57,1),.39,.65),('Supports_DeepSlate',(.075,.11,.14,1),.53,.40),('Cell_DeepBlue',(.025,.09,.25,1),.34,.36),('Cell_Blue',(.045,.18,.40,1),.36,.30)]
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
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}



TILT=math.radians(28);C=math.cos(TILT);S=math.sin(TILT);ZC=1.36;NORMAL=(0,-S,C);OFFSET=.001
# The tilted local Z coordinate is normal to every frame/panel/beam seat.
def tf(p):x,y,z=p;return (x,C*y-S*z,ZC+S*y+C*z)
def transformed(g,fn):
 g=dict(g);g['vertices']=[tuple(round(v,9) for v in fn(p)) for p in g['vertices']];return g
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,mat=1,role='Complete closed finite block',transform=None):
 m=Mesh();v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
 for f in BOX_FACES:m.quad(*[v[i] for i in f],mat,'WholeFiniteFace')
 g=m.result(role);return transformed(g,transform) if transform else g

def slab(xs,ys,z0,z1,occupied,mat=0,role='Whole continuous planar lattice',colour=None):
 m=Mesh();cells={(i,j) for i in range(len(xs)-1) for j in range(len(ys)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2)}
 for i,j in sorted(cells):
  v=[(x,y,z) for z in[z0,z1] for y in ys[j:j+2] for x in xs[i:i+2]]
  for side,(d,f) in enumerate(zip([(0,0),(0,0),(0,-1),(0,1),(-1,0),(1,0)],BOX_FACES)):
   if side>=2 and (i+d[0],j+d[1]) in cells:continue
   color=colour(i,j) if side==1 and colour else mat
   m.quad(*[v[q] for q in f],color,'TopCell' if side==1 else 'CompleteBottomAndWall')
 return m.result(role)
def frame(sign,inset=0):
 # Every opening grows by inset and every external edge shrinks by inset.
 xs=[.18+inset,.25-inset,.70+inset,.76-inset,1.22+inset,1.28-inset,1.73+inset,1.80-inset];ys=[-.72+inset,-.62-inset,.62+inset,.72-inset]
 xs=sorted(sign*x for x in xs)
 def occupied(x,y):
  x=abs(x);return abs(y)>.62+inset or x<.25-inset or .70+inset<x<.76-inset or 1.22+inset<x<1.28-inset or x>1.73+inset
 return transformed(slab(xs,ys,-.08+inset,-inset,occupied,0,'One continuous real three-through-bay ladder frame with full front/back rails and four full crossmembers'),tf)
def contact(name,a,b,axis,p,area,points=None):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else(1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'minimum_patch_area_m2':area-2e-7,'complete_interface_area_m2':area,'points':points or[p],'interior_probe_offset_m':.0004})
def material(n,g):SOLID_VOLUMES[n+'_WholeInsetMaterial']=dict(g,targets=[n])
# Single broad chamfered base, complete flat finite sole and top.
def base(i=0):
 x=.52-i;y=.46-i;c=.09;poly=[(-x+c,-y),(x-c,-y),(x,-y+c),(x,y-c),(x-c,y),(-x+c,y),(-x,y-c),(-x,-y+c)];m=Mesh()
 for z in[i,.12-i]:
  for a,b in zip(poly,poly[1:]+poly[:1]):m.tri([(0,0,z),(*a,z),(*b,z)],1,'WholeBaseCap')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.quad((*a,i),(*b,i),(*b,.12-i),(*a,.12-i),1,'WholeChamferedBaseWall')
 return m.result('Complete thick chamfer-corner base with full planar ground sole')
G[BASE]=base();material(BASE,base(.001))
# Mast top is cut to the exact tilted underside of the spar. This is one
# whole solid prism, not a vertical pole hidden through a sloping beam.
def mast(i=0):
 x=.13-i;y0=.045-i;y1=.275+i # top footprint corresponds to tilted spar y band
 # Actual mast has fixed world Y footprint, chosen wholly below spar width.
 y0=-.005+i;y1=.185-i
 ztop=lambda y:(ZC*C-.20+S*y)/C-i/C
 v=[(x0,y,.12+i if top==0 else ztop(y)) for top in[0,1] for y in[y0,y1] for x0 in[-x,x]];m=Mesh()
 for f in BOX_FACES:m.quad(*[v[q] for q in f],1,'WholeMastFace')
 return m.result('Single full thick central mast, flat bottom and complete28-degree sloping top')
G[MAST]=mast();material(MAST,mast(.001));contact('WholeMastBaseSeat',BASE,MAST,(0,0,1),(0,.09,.12),.26*.19)
G[SPAR]=box((-1.77,-.13,-.20),(1.77,.13,-.08),0,'One complete transverse tilted rear spar',tf);material(SPAR,box((-1.769,-.129,-.199),(1.769,.129,-.081),0,transform=tf))
contact('WholeMastSlopingSparSeat',MAST,SPAR,NORMAL,(0,.09,(ZC*C-.20+S*.09)/C),.26*.19/C)
for sign,side in[(-1,'Left'),(1,'Right')]:
 fn=side+'ThreeBayContinuousFrame';FRAMES.append(fn);G[fn]=frame(sign);material(fn,frame(sign,.001))
 # Each back spar/frame interface is the whole sum of four disjoint finite
 # crossmember rectangles; no hidden penetration, including outside tips.
 contact(side+'WholeFrameBackSparSeat',SPAR,fn,NORMAL,tf((sign*.72,0,-.08)),(.07+.06+.06+.04)*.26,[tf((sign*x,0,-.08)) for x in[.21,.73,1.25,1.75]])
 for k,(a,b) in enumerate([(.23,.72),(.74,1.24),(1.26,1.75)]):
  n=side+'ThickSolarPanel_'+str(k+1);PANELS.append(n);xlo,xhi=sorted([sign*a,sign*b]);dx=xhi-xlo
  # Top colour-cell grid is an integral subdivision of the same closed solid.
  xs=[xlo,xlo+.014,(xlo+xhi)/2-.004,(xlo+xhi)/2+.004,xhi-.014,xhi];ys=[-.68,-.666]
  for j in range(1,5):v=-.666+j*(1.332/5);ys += [v-.004,v+.004]
  ys += [.666,.68]
  def col(i,j):return (2+(j//2)%2) if i in[1,3] and j in[1,3,5,7,9] else 1
  G[n]=transformed(slab(xs,ys,0,.038,lambda x,y:True,1,'Complete38mm thick solar-looking panel with10 integral opaque colour cells, whole side edges and back',col),tf)
  material(n,box((xlo+.001,-.679,.001),(xhi-.001,.679,.037),1,transform=tf))
  # Contact is exactly panel footprint minus intersection with true frame bay.
  baylo,bayhi=[(.25,.70),(.76,1.22),(1.28,1.73)][k];area=dx*1.36-(bayhi-baylo)*1.24
  contact(n+'WholeFrameUndersideSeat',fn,n,NORMAL,tf(((xlo+xhi)/2,.65,0)),area,[tf(((xlo+xhi)/2,y,0)) for y in[-.65,.65]])
  # Both complete lower windows around the spar are checked against ALL parts.
  qlo,qhi=sorted([sign*baylo,sign*bayhi])
  for label,ylo,yhi in[('Front',-.619,-.131),('Back',.131,.619)]:
   VOID_VOLUMES[n+'Whole'+label+'Window']=dict(box((qlo+.001,ylo,-.199),(qhi-.001,yhi,-.001),transform=tf),targets=None)
  ISOLATED_VOID_VOLUMES[n+'WholeIsolatedFrameAperture']=dict(box((qlo+.001,-.619,-.081),(qhi-.001,.619,.001),transform=tf),targets=[fn])
# Entire central upper split between wings and above the supporting spar.
VOID_VOLUMES['WholeCentralWingSplit']=dict(box((-.179,-.719,-.079),(.179,.719,.08),transform=tf),targets=None)
for x in[-.93,.93]:
 VOID_VOLUMES['WholeUnderArraySideBay'+str(x)]=dict(box((x-.70,-.40,.121),(x+.70,.40,.81)),targets=None)
CONTRACT={'single_prop_count':1,'new_scene_count':0,'kind':'prop','closed_meshes':len(G),'materials':4,'fixed_tilt_degrees':28,'separate_wings':2,'whole_three_bay_frames':2,'true_frame_apertures':6,'whole_thick_panels':6,'panel_thickness_m':.038,'cells_per_panel':10,'central_masts':1,'whole_transverse_spars':1,'whole_ground_bases':1,'finite_opposed_contacts':len(CONTACTS),'whole_material_volumes':len(SOLID_VOLUMES),'whole_air_volumes':len(VOID_VOLUMES),'isolated_frame_void_volumes':len(ISOLATED_VOID_VOLUMES),'old_geometry_imports':0,'ordinary_opaque_PBR':True,'static_visual_only':True}
def measure_array_geometry(vertices):
 assert set(vertices)==set(G);vv=[p for v in vertices.values() for p in v];assert abs(min(p[2] for p in vv))<2e-7
 return dict(CONTRACT,bounds_m=[max(p[i] for p in vv)-min(p[i] for p in vv) for i in range(3)],scope='Producer geometry only; complete separately decoded actual-GLB predicates govern acceptance')
INSIDE_TESTS=[(BASE,(0,0,.06),(2,2,2)),(MAST,(0,.09,.5),(2,2,2)),(SPAR,tf((0,0,-.14)),(2,2,2))]+[(n,tf((s*.21,.68,-.04)),tf((s*.47,.3,-.04))) for n,s in zip(FRAMES,[-1,1])]
FOCUS=(0,0,.85);ORTHO=4.30
CAMERAS={'gray-front3q':(4,-6,4.8),'gray-back3q':(-4,6,4.6),'thumbnail':(4,-6,4.8),'qa-front':(0,-8,4.5),'qa-side':(8,0,4.2),'qa-top':(0,0,8),'qa-back':(0,8,4.2),'qa-wireframe':(-4,6,4.6),'silhouette-128-front':(0,-8,4.5),'silhouette-128-side':(8,0,4.2)}
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
root=bpy.data.objects.new('OneTwinWingSolarArray',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='full base sole at Z0; horizontally centred fixed twin-wing array';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_array_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=4000
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'twin_wing_array_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker product gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/spacebase/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'spacebase','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker visual/native/clean gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
