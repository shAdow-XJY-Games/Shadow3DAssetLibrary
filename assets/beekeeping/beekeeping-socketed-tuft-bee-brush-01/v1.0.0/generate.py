"""Original long-backed bee brush with 24 individually seated closed tufts; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-socketed-tuft-bee-brush-01';VERSION='1.0.0';TITLE='Socketed Tuft Bee Brush'
DESCRIPTION=('One original static long-backed bee brush, counted as one prop. One continuous thick honey-brown wooden-looking silhouette joins a broad elongated brush back to a narrowed handle and a true polygonal hanging hole. Three distinct rows of eight cream-coloured closed tuft bundles rise from 24 actual blind seats in the long face. Every tuft has a finite flat root supported on the full seat floor; finite annular root clearance remains inside every pocket. Gently flared, slightly swept and bevel-crowned bundles remain separated by complete real row and column air corridors. The broad continuous back rests flat at ground with bristles pointing upward. Twenty-five closed editable mesh components and three opaque constant PBR materials, metres, native Z up, front -Y and horizontally bounds-centred ground origin. No reused paintbrush, end ferrule, loose bristles, particles, textures, bees, hive, person, stand or scene. Static illustrative geometry only: no sweeping or cleaning performance, softness, hair physics, animal or human use or safety, bee behavior, material suitability, manufacturing, durability, loading, ergonomics, certification or old hive/frame compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={}
BODY='ContinuousLongBackAndHandle';FEET=[BODY];TUFTS=[]
PALETTE=[('HoneyWood',(.34,.145,.044,1),.55,0),('WarmCream_Bundles',(.72,.60,.37,1),.73,0),('PaleCream_Bundles',(.90,.79,.53,1),.76,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs]
 volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
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
  else:raise AssertionError(('untriangulable planar cell',p,order))
 out.append(tuple(order));return out
OUTLINE=[(-.210,-.027),(-.203,-.034),(.024,-.034),(.035,-.028),(.054,-.014),(.195,-.014),(.207,-.008),(.210,0),(.207,.008),(.195,.014),(.054,.014),(.035,.028),(.024,.034),(-.203,.034),(-.210,.027)]
TOP=.019;SEAT=.008;ROWS=[-.018,0,.018];COLUMNS=[round(-.19+.028*i,9) for i in range(8)]
def octagon(x,y,a,b,ch=.0015):return [(x-a+ch,y-b),(x+a-ch,y-b),(x+a,y-b+ch),(x+a,y+b-ch),(x+a-ch,y+b),(x-a+ch,y+b),(x-a,y+b-ch),(x-a,y-b+ch)]
SOCKETS=[(f'Tuft_R{r+1}_C{c+1}',x,y,octagon(x,y,.0108,.0062,.0018)) for r,y in enumerate(ROWS) for c,x in enumerate(COLUMNS)]
HANG=octagon(.176,0,.010,.006,.003)
HOLES=[p for n,x,y,p in SOCKETS]+[HANG]
STATIONS=sorted(set(round(x,9) for p in [OUTLINE]+HOLES for x,y in p))
def interval(poly,x):
 if x<min(a for a,b in poly)-1e-9 or x>max(a for a,b in poly)+1e-9:return None
 ys=[]
 for (a,u),(b,v) in zip(poly,poly[1:]+poly[:1]):
  if abs(b-a)<1e-11:
   if abs(x-a)<1e-9:ys.extend([u,v])
  elif min(a,b)-1e-9<=x<=max(a,b)+1e-9:ys.append(u+(v-u)*(x-a)/(b-a))
 return (min(ys),max(ys)) if ys else None
# Slab triangulation retains every boundary vertex, including the exact starts
# and ends of holes, so the back, handle and all 24 seats are one manifold solid.
def planar_sheet(holes):
 points=[];tris=[];lookup={}
 def vid(p):
  p=tuple(round(c,9) for c in p)
  if p not in lookup:lookup[p]=len(points);points.append(p)
  return lookup[p]
 def cell(a,b,lo_a,lo_b,hi_a,hi_b):
  right=sorted(set(y for poly in holes for q in [interval(poly,b)] if q for y in q if lo_b+1e-9<y<hi_b-1e-9))
  left=sorted(set(y for poly in holes for q in [interval(poly,a)] if q for y in q if lo_a+1e-9<y<hi_a-1e-9),reverse=True)
  pp=[(a,lo_a),(b,lo_b)]+[(b,y) for y in right]+[(b,hi_b),(a,hi_a)]+[(a,y) for y in left]
  qq=[]
  for p in pp:
   p=tuple(round(c,9) for c in p)
   if not qq or qq[-1]!=p:qq.append(p)
  if qq[0]==qq[-1]:qq.pop()
  if len(qq)<3:return
  ids=[vid(p) for p in qq]
  for tri in earclip2(qq):tris.append(tuple(ids[i] for i in tri))
 for a,b in zip(STATIONS,STATIONS[1:]):
  aa=interval(OUTLINE,a);bb=interval(OUTLINE,b);active=sorted((p for p in holes if min(x for x,y in p)<(a+b)/2<max(x for x,y in p)),key=lambda p:interval(p,(a+b)/2)[0])
  lower_a,lower_b=aa[0],bb[0]
  for p in active:
   al,ah=interval(p,a);bl,bh=interval(p,b);cell(a,b,lower_a,lower_b,al,bl);lower_a,lower_b=ah,bh
  cell(a,b,lower_a,lower_b,aa[1],bb[1])
 return points,tris
v=[];f=[];indices={}
def vertex(p):
 p=tuple(round(c,9) for c in p)
 if p not in indices:indices[p]=len(v);v.append(p)
 return indices[p]
def add_face(pp):f.append(tuple(vertex(p) for p in pp))
def boundary(points,tris):
 counts=collections.Counter(tuple(sorted((a,b))) for t in tris for a,b in zip(t,t[1:]+t[:1]))
 return [(points[a],points[b]) for t in tris for a,b in zip(t,t[1:]+t[:1]) if counts[tuple(sorted((a,b)))]==1]
tp,tt=planar_sheet(HOLES)
for t in tt:add_face([(tp[i][0],tp[i][1],TOP) for i in t])
bp,bt=planar_sheet([HANG])
for t in bt:add_face([(bp[i][0],bp[i][1],0) for i in reversed(t)])
# Top boundary loops are classified by the owning full polygon. Outer and
# hanging-hole walls reach the underside; each blind socket wall reaches its floor.
def on_segment(p,a,b):return abs(cr2(sub(b,a),sub(p,a)))<1e-11 and min(a[0],b[0])-1e-9<=p[0]<=max(a[0],b[0])+1e-9 and min(a[1],b[1])-1e-9<=p[1]<=max(a[1],b[1])+1e-9
socket_edges={n:[] for n,x,y,p in SOCKETS}
for a,b in boundary(tp,tt):
 midpoint=mul(add(a,b),.5);owner=next((n for n,x,y,p in SOCKETS if any(on_segment(midpoint,q,r) for q,r in zip(p,p[1:]+p[:1]))),None);z=SEAT if owner else 0
 add_face([(a[0],a[1],TOP),(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],TOP)])
 if owner:socket_edges[owner].append((a,b))
for n,x,y,p in SOCKETS:
 # A centre fan preserves exact subdivided perimeter edges at the blind floor.
 for a,b in socket_edges[n]:add_face([(x,y,SEAT),(b[0],b[1],SEAT),(a[0],a[1],SEAT)])
G[BODY]=mesh(v,f,0,'One connected solid long wooden-looking back and narrowed continuous handle, 24 true blind socket floors/walls, true hanging through-hole and broad finite ground back.')
# Closed eight-facet bundles, with a real finite flat root and four gently
# flared/swept levels. No strand, particle, painted line or detached hair.
TUFT_LEVELS={}
for index,(n,x,y,p) in enumerate(SOCKETS):
 height=.080+.002*(index%3);levels=[(SEAT,.009,.0045,0),(TOP+.002,.009,.0045,0),(.049,.010,.005,-.0006),(height-.003,.0105,.0052,-.0012),(height,.0092,.0042,-.0014)]
 vv=[];ff=[]
 for z,hx,hy,bend in levels:vv.extend((xx,yy,z) for xx,yy in octagon(x,y+bend,hx,hy,.0015))
 for j in range(len(levels)-1):
  for i in range(8):k=(i+1)%8;ff.append((8*j+i,8*j+k,8*(j+1)+k,8*(j+1)+i))
 ff.extend([tuple(reversed(range(8))),tuple(range(8*(len(levels)-1),8*len(levels)))])
 G[n]=mesh(vv,ff,1+(index%3==1),'One closed tapered swept tuft bundle; finite root underside rests on its actual blind socket floor, with complete annular root air and separate neighbouring bundles.');TUFTS.append(n);TUFT_LEVELS[n]=levels
 CONTACTS.append({'name':n+'_FullRootSeat','a':BODY,'b':n,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':SEAT,'points':[(x,y,SEAT)],'minimum_patch_area_m2':.000145,'interior_probe_offset_m':.0005})
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi):return mesh([(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]],BOX_FACES)
def prism(p,z0,z1):
 n=len(p);return mesh([(x,y,z) for z in [z0,z1] for x,y in p],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
def air(name,g,role):VOID_VOLUMES[name]=dict(g,targets=list(G),role=role)
# These are full rectangular row/column corridors through the complete crown
# height and beyond both side mouths, not centre rays. Every opposing entire
# tuft surface is additionally tested, including the chamfered outer corners.
for c,(a,b) in enumerate(zip(COLUMNS,COLUMNS[1:])):
 air(f'WholeColumnCorridor_{c+1}',box((a+.0112,-.035,.020),(b-.0112,.035,.088)),'Complete full-width column-to-column air corridor spanning all three rows and beyond both side mouths; 0.7 mm margin from maximum tuft extent.')
for r,(a,b) in enumerate(zip(ROWS,ROWS[1:])):
 air(f'WholeRowCorridor_{r+1}',box((-.204,a+.0059,.020),(.020,b-.0073,.088)),'Complete full-length row-to-row air corridor, all eight columns, all crown heights; at least 0.7 mm from swept tuft envelope.')
# True annular root air: one closed connected eight-sided ring for each entire
# blind pocket, from above its floor to below its mouth. The two polygon loops
# use uniform finite margins from the actual pocket and actual root.
for n,x,y,p in SOCKETS:
 outer=octagon(x,y,.0104,.0058,.0018);inner=octagon(x,y,.0094,.0049,.0015);vv=[(xx,yy,z) for z in [.009,.0184] for poly in [outer,inner] for xx,yy in poly];ff=[]
 for i in range(8):j=(i+1)%8;ff.extend([(i,j,16+j,16+i),(8+j,8+i,24+i,24+j),(j,i,8+i,8+j),(16+i,16+j,24+j,24+i)])
 air(n+'_WholeSocketAnnularAir',mesh(vv,ff),'Complete finite polygonal annular root clearance inside one actual blind socket; 0.4 mm radial, 1 mm lower and 0.6 mm mouth margins.')
air('WholeHangingHoleAir',prism(octagon(.176,0,.0095,.0055,.003),-.002,.021),'Complete eight-sided hanging through-hole air with 0.5 mm planar margin, extending beyond both mouths.')
BORES.append({'mesh':BODY,'origin_m':(.176,0,-.001),'direction':(0,0,1),'length_m':.021})
SOLID_VOLUMES['ContinuousHandleRootBridge']=dict(box((.029,-.009,.004),(.074,.009,.014)),targets=[BODY],role='Entire finite solid material bridge through the narrowed head-to-handle neck.')
SOLID_VOLUMES['LongBackBelowAllBlindSeats']=dict(box((-.201,-.028,.002),(.018,.028,.006)),targets=[BODY],role='Entire finite solid continuous long back material below all 24 blind socket floors.')
BRUSH_CONTRACT={'single_prop_count':1,'continuous_back_handle_mesh':1,'rows':3,'tufts_per_row':8,'individually_closed_tufts':24,'actual_blind_socket_count':24,'true_hanging_hole':1,'finite_opposed_contacts':24,'whole_empty_volumes':len(VOID_VOLUMES),'solid_material_volumes':len(SOLID_VOLUMES)}
def measure_brush_geometry(vertices):
 assert set(vertices)==set(G);assert abs(min(p[2] for p in vertices[BODY]))<2e-7
 for n in TUFTS:assert abs(min(p[2] for p in vertices[n])-SEAT)<2e-7
 return dict(BRUSH_CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, air/material bodies, separation and independent actual negatives remain required')
FOCUS=(0,0,.036);ORTHO=.515
CAMERAS={'gray-front3q':(.55,-.9,.66),'gray-back3q':(-.55,.9,.66),'thumbnail':(.55,-.9,.66),'qa-front':(0,-1,.40),'qa-side':(1,0,.40),'qa-top':(0,0,1),'qa-back':(0,1,.40),'qa-wireframe':(.55,-.9,.66),'silhouette-128-front':(0,-1,.40),'silhouette-128-side':(1,0,.40)}
WIRE_THICKNESS=ORTHO/1050

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
root=bpy.data.objects.new('OneLongBackSocketedBeeBrush',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred continuous back ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(BODY,(-.10,0,.004),(-.10,0,.11)),(TUFTS[0],(-.19,-.018,.012),(-.19,-.018,.095))]:
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
mount_evidence=measure_brush_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'brush_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
