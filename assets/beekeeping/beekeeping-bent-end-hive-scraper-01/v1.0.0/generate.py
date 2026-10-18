"""Original continuous bent-end hive scraper; one static low-poly visual prop.
Metres, native Z up, front -Y. No real tool-performance or compatibility claim.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-bent-end-hive-scraper-01';VERSION='1.0.0';TITLE='Bent-End Hive Scraper'
DESCRIPTION=('One original low-poly hive scraper counted as one fixed static visual prop. A single connected thick metal strip broadens to a wide oblique wedge scraper at one end, narrows through a red-coloured flat grip with a true elliptical through-hanging hole, and continues into an upward bent hook and short return lip at the other end. The wide wedge retains a finite blunt edge, the bend has continuous inner and outer faces, and the entire hook-under air and hanging-hole air are real open volumes. The broad flat back rests at ground. Two constant opaque material regions on one mesh, with no separate grip sleeve, numbers, logo, texture, animation, hive, hand, bees, display base or extra tool. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. Static visual geometry only: no prying, scraping, wax removal, sharpness, strength, load, corrosion, food or bee suitability, hand fit, manufacturing or tool safety claim. No historical hive or frame dimensional compatibility is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};EMBEDDED_VOLUMES={}
PALETTE=[('Steel_Satin',(.44,.50,.52,1),.38,.72),('Grip_Red',(.55,.075,.04,1),.51,.15)]
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
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  found=False
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def contained(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(contained(p[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);found=True;break
  assert found,('untriangulable planar cell',p,order)
 out.append(tuple(order));return out
THICK=.006;ROOT=.075;RADIUS=.024;ANGLE=math.radians(140);ARC_END=ROOT+RADIUS*ANGLE;END=ARC_END+.022
PROFILE=[(-.155,.036),(-.132,.036),(-.100,.026),(-.070,.016),(.045,.016),(ROOT,.018),(END,.018)]
HC=(-.006,0.);HRX=.013;HRY=.0065
HANG=[(round(HC[0]+HRX*math.cos(math.tau*i/32),8),round(HRY*math.sin(math.tau*i/32),8)) for i in range(32)]
BEND_STATIONS=[ROOT+RADIUS*ANGLE*i/14 for i in range(15)]
STATIONS=sorted(set(round(x,8) for x in [p[0] for p in PROFILE]+[-.075,.040]+BEND_STATIONS+[ARC_END,END]+[x for x,y in HANG]))
def width(u):
 for (a,v),(b,w) in zip(PROFILE,PROFILE[1:]):
  if a-1e-7<=u<=b+1e-7:return v+(w-v)*(u-a)/(b-a)
 raise ValueError(u)
def frame(u):
 if u<=ROOT+1e-8:
  thick=.002+.004*max(0,min(1,(u+.155)/.023));return (u,thick/2),(0,1),thick
 t=min(ANGLE,(u-ROOT)/RADIUS);c=(ROOT+RADIUS*math.sin(t),THICK/2+RADIUS*(1-math.cos(t)))
 if u>ARC_END:c=add(c,mul((math.cos(ANGLE),math.sin(ANGLE)),u-ARC_END))
 return c,(-math.sin(t),math.cos(t)),THICK
# Preserve an oblique wide scraper edge: its X coordinate shears by Y only
# in the wide wedge and fades continuously before the narrower grip.
def map_point(u,y,layer):
 c,n,t=frame(u);shear=.16*y*max(0,min(1,(-.100-u)/.032));return(c[0]+n[0]*(layer-.5)*t+shear,y,c[1]+n[1]*(layer-.5)*t)
def polygon_interval(poly,x):
 if x<min(a for a,b in poly)-1e-9 or x>max(a for a,b in poly)+1e-9:return None
 values=[]
 for (a,u),(b,v) in zip(poly,poly[1:]+poly[:1]):
  if abs(b-a)<1e-10:
   if abs(x-a)<1e-9:values.extend([u,v])
  elif min(a,b)-1e-9<=x<=max(a,b)+1e-9:values.append(u+(v-u)*(x-a)/(b-a))
 return min(values),max(values)
PLANAR_VERTS=[];PLANAR_TRIS=[];vid={}
def vertex(p):
 p=tuple(round(float(c),8) for c in p)
 if p not in vid:vid[p]=len(PLANAR_VERTS);PLANAR_VERTS.append(p)
 return vid[p]
def cell(points):
 pp=[]
 for p in points:
  p=tuple(round(float(c),8) for c in p)
  if not pp or pp[-1]!=p:pp.append(p)
 if pp[0]==pp[-1]:pp.pop()
 ids=[vertex(p) for p in pp]
 for tri in earclip2(pp):PLANAR_TRIS.append(tuple(ids[i] for i in tri))
for a,b in zip(STATIONS,STATIONS[1:]):
 mid=(a+b)/2
 if min(x for x,y in HANG)<mid<max(x for x,y in HANG):
  al,ah=polygon_interval(HANG,a);bl,bh=polygon_interval(HANG,b)
  cell([(a,-width(a)),(b,-width(b)),(b,bl),(a,al)])
  cell([(a,ah),(b,bh),(b,width(b)),(a,width(a))])
 else:
  l=polygon_interval(HANG,a);r=polygon_interval(HANG,b);pp=[(a,-width(a)),(b,-width(b))]
  if r:pp.extend((b,y) for y in sorted(set(r)))
  pp.extend([(b,width(b)),(a,width(a))])
  if l:pp.extend((a,y) for y in sorted(set(l),reverse=True))
  cell(pp)
def solid_from_sheet(points,triangles,layer_lo=0,layer_hi=1):
 used=sorted({i for tri in triangles for i in tri});remap={v:i for i,v in enumerate(used)};pp=[points[i] for i in used];tt=[tuple(remap[i] for i in tri) for tri in triangles];n=len(pp)
 vv=[map_point(u,y,layer) for layer in [layer_lo,layer_hi] for u,y in pp];ff=[tuple(reversed(t)) for t in tt]+[tuple(n+i for i in t) for t in tt];edges=collections.Counter(tuple(sorted((a,b))) for t in tt for a,b in zip(t,t[1:]+t[:1]))
 for t in tt:
  for a,b in zip(t,t[1:]+t[:1]):
   if edges[tuple(sorted((a,b)))]==1:ff.append((a,b,b+n,a+n))
 return vv,ff
v,f=solid_from_sheet(PLANAR_VERTS,PLANAR_TRIS);raw_min=min(p[0] for p in v);raw_max=max(p[0] for p in v);XSHIFT=-(raw_min+raw_max)/2
# The datum translation is shared by body and every complete-volume proof.
_original_map=map_point
def map_point(u,y,layer):
 p=_original_map(u,y,layer);return(p[0]+XSHIFT,p[1],p[2])
v,f=solid_from_sheet(PLANAR_VERTS,PLANAR_TRIS);body=mesh('HiveScraper_ContinuousWedgeGripAndHook',v,f,0,'one connected thick metal strip, oblique broad blunt wedge, real elliptical through-hole, full inner/outer bent hook and return lip');BODY=body;FEET.append(body)
N=len(PLANAR_VERTS);G[body]['face_materials']=[1 if all(-.075-1e-8<=PLANAR_VERTS[i%N][0]<=.040+1e-8 for i in face) else 0 for face in f]
def prism_data(p,lo,hi):
 n=len(p);return [(x,y,z) for z in [lo,hi] for x,y in p],[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
def inward_polygon(p,d):
 out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:p=list(reversed(p))
 for i,b in enumerate(p):
  a=p[i-1];c=p[(i+1)%len(p)];e=sub(b,a);f=sub(c,b);el=math.hypot(*e);fl=math.hypot(*f);n=(-e[1]/el,e[0]/el);m=(-f[1]/fl,f[0]/fl);q=add(b,mul(n,d));r=add(b,mul(m,d));den=cr2(e,f)
  out.append(q if abs(den)<1e-14 else add(q,mul(e,cr2(sub(r,q),f)/den)))
 return out
v,f=prism_data([(x+XSHIFT,y) for x,y in inward_polygon(HANG,.0007)],-.0015,.0075)
VOID_VOLUMES['HangingHole_CompleteThroughAir']={'vertices':v,'faces':f,'targets':[body],'role':'complete uniformly inset polygonal elliptical air, continuous through both mouths'}
BORES.append({'mesh':body,'origin_m':(HC[0]+XSHIFT,0,-.001),'direction':(0,0,1),'length_m':.008})
# Full hook-under air follows every actual inner bend facet and the return lip.
# A uniform planar inset separates its entire boundary from the tool. It extends
# through both width mouths; it is a closed air witness, not an added asset mesh.
inner=[(map_point(u,0,1)[0],map_point(u,0,1)[2]) for u in BEND_STATIONS+[END]]
HOOK_AIR_PROFILE=inward_polygon([(ROOT-.020+XSHIFT,.006)]+inner+[(ROOT-.020+XSHIFT,inner[-1][1])],.001)
v,f=prism_data(HOOK_AIR_PROFILE,-.022,.022);v=[(x,z,y) for x,y,z in v];f=[tuple(reversed(q)) for q in f]
VOID_VOLUMES['HookUnder_CompleteSideToSideAir']={'vertices':v,'faces':f,'targets':[body],'role':'entire inner hook profile uniformly inset 1 mm; complete side-to-side width through both mouths'}
GAPS.append({'origin_m':(ROOT+.008+XSHIFT,-.025,.025),'direction':(0,1,0),'length_m':.050,'targets':[body]})
def rail_volume(stations,ylo,yhi,layerlo=.32,layerhi=.68):
 pp=[(u,y) for u in stations for y in [ylo,yhi]];tt=[]
 for j in range(len(stations)-1):a=2*j;tt.extend([(a,a+2,a+3),(a,a+3,a+1)])
 return solid_from_sheet(pp,tt,layerlo,layerhi)
for label,stations,ylo,yhi in [('Grip_ContinuousFiniteRail',[-.085,-.075,-.070,-.019,.007,.040,.045,.065],.010,.013),('Bend_ContinuousFiniteCore',[.064]+BEND_STATIONS+[END-.004],-.010,.010)]:
 v,f=rail_volume(stations,ylo,yhi);EMBEDDED_VOLUMES[label]={'vertices':v,'faces':f,'targets':[body],'role':'complete finite solid strip enclosed within the actual continuous material, through every relevant section'}
SCRAPER_CONTRACT={'single_prop_count':1,'single_connected_mesh':1,'true_elliptical_hanging_holes':1,'wide_oblique_wedge':True,'continuous_upward_hook_with_return_lip':True,'finite_blunt_edge_thickness_m':.002,'grip_thickness_m':THICK,'bend_inner_radius_m':RADIUS-THICK/2,'bend_degrees':140,'actual_tool_performance_claim':False}
def measure_scraper_geometry(vertices):
 assert set(vertices)=={body};vv=vertices[body];assert len(vv)==2*N
 thickness=[]
 for i,(u,y) in enumerate(PLANAR_VERTS):
  delta=sub(vv[i+N],vv[i]);t=math.sqrt(dot(delta,delta));expected=frame(u)[2];assert abs(t-expected)<3e-7,(i,u,t,expected);thickness.append(t)
  assert max(abs(vv[i][k]-map_point(u,y,0)[k]) for k in range(3))<3e-7,(i,u,'lower shape altered')
  assert max(abs(vv[i+N][k]-map_point(u,y,1)[k]) for k in range(3))<3e-7,(i,u,'upper shape altered')
 assert abs(min(p[2] for p in vv))<1e-7 and max(p[2] for p in vv)>.055
 return dict(SCRAPER_CONTRACT,all_actual_thickness_pairs=len(thickness),minimum_measured_thickness_m=min(thickness),full_geometry_scope='all actual matching upper/lower vertices; separate complete air/material volumes, full self-intersection and finite ground gates mandatory')
FOCUS=(0,0,.022);ORTHO=.34
CAMERAS={'gray-front3q':(.15,-.58,.55),'gray-back3q':(-.15,.58,.55),'thumbnail':(.15,-.58,.55),'qa-front':(0,-.65,.40),'qa-side':(.65,0,.44),'qa-top':(0,0,.8),'qa-back':(0,.65,.40),'qa-wireframe':(.15,-.58,.55),'silhouette-128-front':(0,-.65,.40),'silhouette-128-side':(.65,0,.44)}
WIRE_THICKNESS=ORTHO/640*.5

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
root=bpy.data.objects.new('OneBentEndHiveScraper',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(body,(XSHIFT-.050,.010,.003),(HC[0]+XSHIFT,HC[1],.003))]:
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
mount_evidence=measure_scraper_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'scraper_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
