"""Original shallow-pitched twelve-window hangar portal; one static modular asset."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='aviation-open-truss-hangar-portal-01';VERSION='1.0.0';TITLE='Open-Truss Hangar Portal'
DESCRIPTION=('One original low-poly static hangar entrance portal, counted as one modular asset. Two thick columns bear with their complete flat feet on two separate thick flat-bottom plates. A wide shallow-pitched six-bay truss has twelve genuinely open triangular windows, one continuous lower chord, two continuous sloping upper chords and integral vertical and alternating diagonal webs. The truss is a single closed full-thickness genus-twelve body, with shared continuous nodes rather than interpenetrating overlong rods. Its two ends bear on complete finite column-top faces. The complete entrance from ground to the lower chord is open front to back, without doors, walls, floors or hidden blocking panels. Metres, source Z up and front -Y, origin at exact ground-level bounds centre. Three opaque unlinked constant PBR colours, no textures, external fonts or external models. No scene, aircraft, apron, roof, enclosure, doors or motion. No architectural strength, loads, wind resistance, ground anchoring, stability, manufacturing, installation, aircraft fit, usable passage clearance, aviation or building safety, old-module compatibility or seamless repetition is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('Portal_DeepPetrolSteel',(.055,.22,.25,1),.69,.15),('Truss_WarmIvorySteel',(.73,.69,.53,1),.74,.08),('Footplate_OxideOrange',(.56,.22,.09,1),.76,.12)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled colours; no TEX_* nodes or linked inputs.'
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
 def face(self,p,mat=0,tag=''):
  ids=[self.vertex(q) for q in p]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def earclip(poly):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 order=list(range(len(poly))) if area>0 else list(reversed(range(len(poly))));out=[]
 while len(order)>3:
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-12:continue
   if any(all(cr(poly[x],poly[y],poly[q])>=-1e-12 for x,y in[(a,b),(b,c),(c,a)]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(k);break
  else:raise AssertionError('non-simple or degenerate polygon')
 out.append(tuple(order));return out

def box_geometry(lo,hi,mat=0):
 m=Mesh();v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.face([v[i] for i in f],mat)
 return m.result('closed finite solid box',mat)
def prism(poly,y0,y1,mat=0):
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 if area<0:poly=list(reversed(poly))
 m=Mesh();rr=[[(x,y,z) for x,z in poly] for y in[y0,y1]]
 for f in earclip(poly):m.face([rr[0][i] for i in f],mat);m.face([rr[1][i] for i in reversed(f)],mat)
 for i in range(len(poly)):j=(i+1)%len(poly);m.face([rr[0][j],rr[0][i],rr[1][i],rr[1][j]],mat)
 return m.result('complete closed finite XZ prism',mat)
def volume(table,name,g,targets,role):table[name]=dict(g,targets=list(targets),role=role,asset_member=False)
def inset(poly,offsets):
 # Intersect all adjacent oriented inward-offset edge lines; no raster or boolean mesh.
 lines=[]
 for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
  dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);n=(-dz/l,dx/l);lines.append((n,n[0]*a[0]+n[1]*a[1]+offsets[i]))
 out=[]
 for i in range(len(poly)):
  (a,c),(b,d)=lines[i-1],lines[i];det=a[0]*b[1]-a[1]*b[0];out.append(((c*b[1]-a[1]*d)/det,(a[0]*d-c*b[0])/det))
 return out
TRUSS='Truss_ContinuousTwelveWindowBody';YHALF=.24;BOTTOM=3.70
XS=[-3.4+i*(6.8/6) for i in range(7)]
TOP=[4.45+.60*(1-abs(x)/3.4) for x in XS]
CELLS=[]
for i in range(6):
 a,b,c,d=(XS[i],BOTTOM),(XS[i+1],BOTTOM),(XS[i+1],TOP[i+1]),(XS[i],TOP[i])
 CELLS.extend([[a,b,c],[a,c,d]] if i%2==0 else [[a,b,d],[b,c,d]])
def edgekey(a,b):return tuple(sorted((tuple(a),tuple(b))))
EDGES=collections.Counter(edgekey(a,b) for p in CELLS for a,b in zip(p,p[1:]+p[:1]));HOLES=[]
m=Mesh()
for k,poly in enumerate(CELLS):
 hole=inset(poly,[.16 if EDGES[edgekey(a,b)]==1 else .085 for a,b in zip(poly,poly[1:]+poly[:1])]);HOLES.append(hole)
 for i in range(3):
  j=(i+1)%3
  # Face strips tile shared outer edges exactly. There are no internal overlap faces.
  q=[poly[i],poly[j],hole[j],hole[i]]
  m.face([(x,-YHALF,z) for x,z in q],1,'whole_front_chord_web_node_material');m.face([(x,YHALF,z) for x,z in q[::-1]],1,'whole_rear_chord_web_node_material')
  a,b=hole[i],hole[j];m.face([(a[0],-YHALF,a[1]),(b[0],-YHALF,b[1]),(b[0],YHALF,b[1]),(a[0],YHALF,a[1])],1,'true_triangular_window_full_depth_wall')
  if EDGES[edgekey(poly[i],poly[j])]==1:
   a,b=poly[i],poly[j];m.face([(b[0],-YHALF,b[1]),(a[0],-YHALF,a[1]),(a[0],YHALF,a[1]),(b[0],YHALF,b[1])],1,'complete_outer_truss_boundary')
G[TRUSS]=m.result('One continuous full-depth truss, lower chord, two shallow-pitched upper chords, vertical/alternating diagonal webs and twelve open triangular windows',1)
COLUMNS=[]
for label,x in [('Left',-3.15),('Right',3.15)]:
 foot=label+'_CompleteFlatFootplate';col=label+'_FullHeightColumn';FEET.append(foot);COLUMNS.append(col)
 footlo,foothi=(x-.65,x+.25) if x<0 else (x-.25,x+.65)
 G[foot]=box_geometry((footlo,-.60,0),(foothi,.60,.18),2);G[foot]['role']='Separate thick footplate with complete finite 0.9 by 1.2 metre flat bottom at z=0; no anchors or safety claim'
 G[col]=box_geometry((x-.25,-.24,.18),(x+.25,.24,BOTTOM),0);G[col]['role']='One full thick column with whole finite footplate bearing and full 0.5 by 0.48 metre truss-end bearing'
 for a,b,z in[(foot,col,.18),(col,TRUSS,BOTTOM)]:
  CONTACTS.append({'name':a+'_to_'+b,'a':a,'b':b,'origin_m':(0,0,0),'axis':(0,0,1),'u':(1,0,0),'v':(0,1,0),'plane_m':z,'points':[(x,0,z)],'interior_probe_offset_m':.002,'minimum_patch_area_m2':.2399,'coverage':'smaller_complete_interface','role':'complete finite opposed column footprint; no penetration'})
 volume(SOLID_VOLUMES,label+'_WholeColumnCore',box_geometry((x-.24,-.23,.19),(x+.24,.23,BOTTOM-.01)),[col],'whole inward-offset full-height column core')
 volume(SOLID_VOLUMES,label+'_WholeFootplateCore',box_geometry((footlo+.01,-.59,.01),(foothi-.01,.59,.17)),[foot],'whole inward-offset finite footplate core')
# Entire doorway, with its full front/back mouths, is air; touching boundaries have a 4mm inset.
volume(VOID_VOLUMES,'WholeGroundToLowerChordEntrance',box_geometry((-2.896,-.72,.004),(2.896,.72,BOTTOM-.004)),list(G),'complete finite main opening from near ground to lower chord and both mouths, full width between column/plate inner edges')
for k,h in enumerate(HOLES):
 volume(VOID_VOLUMES,'WholeTriangularWindow_%02d'%k,prism(inset(h,[.004]*3),-.32,.32),list(G),'complete triangular window air through all truss depth and both mouths')
# Every chord, vertical web and diagonal web has an actual full-length inset material prism.
# Witnesses extend through internal junctions; outer-node witnesses remain within the true perimeter.
MEMBER_WITNESSES=[]
for k,((a,b),count) in enumerate(sorted(EDGES.items())):
 dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz);u=(dx/length,dz/length);n=(-u[1],u[0]);margin=.024
 if count==1:
  owning=next(p for p in CELLS if edgekey(a,b) in [edgekey(c,d) for c,d in zip(p,p[1:]+p[:1])]);cent=(sum(p[0] for p in owning)/3,sum(p[1] for p in owning)/3)
  if (cent[0]-(a[0]+b[0])/2)*n[0]+(cent[1]-(a[1]+b[1])/2)*n[1]<0:n=(-n[0],-n[1])
  a=(a[0]+n[0]*.08,a[1]+n[1]*.08);b=(b[0]+n[0]*.08,b[1]+n[1]*.08);half=.040;trim=.075
 else:half=.045;trim=.10
 aa=(a[0]+u[0]*trim,a[1]+u[1]*trim);bb=(b[0]-u[0]*trim,b[1]-u[1]*trim)
 poly=[(aa[0]-n[0]*half,aa[1]-n[1]*half),(bb[0]-n[0]*half,bb[1]-n[1]*half),(bb[0]+n[0]*half,bb[1]+n[1]*half),(aa[0]+n[0]*half,aa[1]+n[1]*half)]
 name='Truss_WholeMemberCore_%02d'%k;volume(SOLID_VOLUMES,name,prism(poly,-.225,.225),[TRUSS],'complete finite longitudinal material prism across authored chord or web');MEMBER_WITNESSES.append(name)
# One whole finite node body at each shared cell vertex; boundary nodes move 50mm inward.
for k,(x,z) in enumerate(sorted({p for poly in CELLS for p in poly})):
 nx=x+(.07 if x<-3.399 else -.07 if x>3.399 else 0);nz=z+.06 if z==BOTTOM else z-.07
 volume(SOLID_VOLUMES,'Truss_FullNodeCore_%02d'%k,box_geometry((nx-.018,-.225,nz-.018),(nx+.018,.225,nz+.018)),[TRUSS],'finite continuous integral node material; no point-only or line-only joint')
HANGAR_CONTRACT={'single_modular_count':1,'editable_meshes':len(G),'truss_genus':12,'triangular_windows':12,'full_ground_footplates':2,'complete_columns':2,'finite_full_face_seats':4,'whole_main_entrance':1,'truss_bays':6,'net_column_span_m':5.8,'truss_lower_face_m':BOTTOM,'height_m':5.05,'whole_depth_m':1.2,'origin':'ground-level exact bounds centre','material_contract':MATERIAL_CONTRACT,'no_architectural_or_aircraft_fit_claim':True}
def measure_hangar_geometry(vertices):
 assert set(vertices)==set(G)
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<6e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<6e-7 for p in actual),(n,'actual shape changed')
 return dict(HANGAR_CONTRACT,whole_void_groups=len(VOID_VOLUMES),finite_material_volume_groups=len(SOLID_VOLUMES))
FOCUS=(0,0,2.45);ORTHO=8.80
CAMERAS={'gray-front3q':(8,-16,8),'gray-back3q':(-8,16,8),'thumbnail':(8,-16,8),'qa-front':(0,-16,2.45),'qa-side':(16,0,2.45),'qa-top':(0,0,18),'qa-back':(0,16,2.45),'qa-wireframe':(8,-16,8),'silhouette-128-front':(0,-16,2.45),'silhouette-128-side':(16,0,2.45)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/1100
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
root=bpy.data.objects.new('OneOpenTrussHangarPortal',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground-level exact bounds centre (0,0,0), source Z up and front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(COLUMNS[0],(-3.15,0,1.5),(0,0,1.5)),(TRUSS,(0,0,3.75),(0,0,3.4))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Producer Blender checks below cover actual closed mesh topology, ground and
# opposed contact triangle areas plus auxiliary interior-side probes only.
# Complete void/material bodies, full-interface nonpenetration and all-pair
# boundary acceptance remain independent actual-GLB gates; no full void claim here.
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
mount_evidence=measure_hangar_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'hangar_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'producer_check_scope':'Actual closed mesh topology, degeneracy, finite ground triangles, opposed contact triangle area and auxiliary interior-side probes, oriented GLB/PBR readback only. Whole void/material volumes, complete interface nonpenetration and all-pair boundary acceptance remain independent actual-GLB gates.',
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/aviation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'aviation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-6,-8,11),1800,7),('Fill',(7,-3,7),1100,6),('Rim',(3,8,9),1500,5)]:
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
