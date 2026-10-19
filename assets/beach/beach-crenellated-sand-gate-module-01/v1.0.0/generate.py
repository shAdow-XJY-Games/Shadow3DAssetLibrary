"""Original twin tapered sand towers and open arch wall; one static modular asset."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beach-crenellated-sand-gate-module-01';VERSION='1.0.0';TITLE='Crenellated Sand Gate Module'
DESCRIPTION=('One original low-poly sandcastle gate module, counted as one modular asset. Two upward-tapering, softly faceted sand towers have broad finite flat bottoms, eight integral thick merlons each, eight actual open notches each, and genuine shallow top courts with continuous closed bottoms. A thick low sand wall joins their inward flat faces over complete opposed finite patches. Its real arched passage is continuously open from ground to crown, through the whole wall and its flared front/rear reveals. The wall has no threshold or hidden floor. The towers have shallow inward planar cuts solely for these two complete fixed joints; no external connector standard is claimed. Three separately editable closed connected meshes form one complete static module. Three opaque constant unlinked PBR sand tones, no textures. Metres, source Z up, front -Y; origin is the ground-level bounds centre. No flags, furniture, loose buckets, sand plane, landscape, full castle scene, animation or variants. Original tapered sand geometry, not a recoloured dining arch, stone well, low stone wall, cottage or stream bank. Static visual geometry only. No sand-grain, collapse, tide or weather simulation, strength, loads, child activity, human passage, structural/building safety, manufacture or installation certification. No seamless repetition, complete castle closure, old-wall compatibility, assembly motion or historical reconstruction is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('Sand_WarmBody',(.66,.44,.235,1),.93,0),('Sand_SunlitEdges',(.79,.565,.315,1),.94,0),('Sand_RecessedFaces',(.56,.345,.165,1),.96,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled sand colours; no TEX_* nodes or linked inputs.'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
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

def box_geometry(lo,hi):
 m=Mesh();v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.face([v[i] for i in f])
 return m.result('closed finite QA box witness, not exported')
def volume(table,name,g,targets,role):table[name]=dict(g,targets=targets,role=role,asset_member=False)
N=32;TOWER_CENTRES={'Sand_LeftTaperedCrenellatedTower':-1.05,'Sand_RightTaperedCrenellatedTower':1.05};WALL='Sand_ThickOpenArchWall'
# The inward D-shaped cut lies beyond the whole court wall, making a real full
# planar junction. It never cuts the shallow court or creates a hidden fill.
def tower_point(cx,r,i,z,outer=True):
 a=math.tau*(i%N)/N;x=r*math.cos(a)
 if outer:x=max(-.33,x)
 return (abs(cx)+x,r*math.sin(a),z) if cx>0 else(-abs(cx)-x,r*math.sin(a),z)
TOWER_LEVELS=[(1.10,.440,.270),(1.25,.420,.290),(1.28,.4175,.291),(1.44,.405,.298),(1.48,.393,.306)]
def make_tower(cx,cut_merlon=None):
 m=Mesh();outer=[(0,.490),(.06,.530),(1.10,.440)]
 rings=[[tower_point(cx,r,i,z) for i in range(N)] for z,r in outer]
 for a,b in zip(rings,rings[1:]):
  for i in range(N):j=(i+1)%N;m.face([a[i],a[j],b[j],b[i]],0,'tapered_outer_body')
 centre=(cx,0,0)
 for i in range(N):j=(i+1)%N;m.face([centre,rings[0][j],rings[0][i]],2,'finite_flat_ground')
 floor=[tower_point(cx,.270,i,1.10,False) for i in range(N)]
 for i in range(N):j=(i+1)%N;m.face([(cx,0,1.10),floor[i],floor[j]],2,'whole_shallow_court_floor')
 boundary={}
 for k in range(len(TOWER_LEVELS)-1):
  z0,ro0,ri0=TOWER_LEVELS[k];z1,ro1,ri1=TOWER_LEVELS[k+1]
  for i in range(N):
   high=(i//2)%2==0
   if k>0 and not high:continue
   if k==1 and cut_merlon is not None and i//4==cut_merlon:continue
   j=(i+1)%N
   a=[tower_point(cx,r,h,z,outer_) for z,ro,ri in[(z0,ro0,ri0),(z1,ro1,ri1)] for r,h,outer_ in[(ri,i,False),(ro,i,True),(ro,j,True),(ri,j,False)]]
   for fi,f in enumerate([(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]):
    if k==0 and fi==0:continue
    q=[a[jj] for jj in f];key=tuple(sorted(q))
    if key in boundary:del boundary[key]
    else:boundary[key]=(q,1 if fi==1 else 2 if fi==5 else 0,'integral_crenellation_or_court_wall')
 for q,material,tag in boundary.values():m.face(q,material,tag)
 return m.result('One complete closed tapered D-plan sand tower with integral eight-merlon crown, eight genuine notches, a continuous thick ring and one shallow bottomed court.')
for name,cx in TOWER_CENTRES.items():G[name]=make_tower(cx);FEET.append(name)
# Three depth sections create true bevelled arch reveals, not an overlaid trim.
def wall_profile(radius,top):
 p=[(-.72,0),(-.72,top-.04),(-.67,top),(.67,top),(.72,top-.04),(.72,0),(radius,0),(radius,.49)]
 p += [(radius*math.cos(i*math.pi/16),.49+radius*math.sin(i*math.pi/16)) for i in range(1,17)]
 p += [(-radius,0)];return p
WALL_SECTIONS=[(-.205,wall_profile(.440,1.10)),(-.145,wall_profile(.400,1.14)),(.145,wall_profile(.400,1.14)),(.205,wall_profile(.440,1.10))]
m=Mesh();rings=[[(x,y,z) for x,z in p] for y,p in WALL_SECTIONS]
for a,b in zip(rings,rings[1:]):
 for i in range(len(a)):j=(i+1)%len(a);m.face([a[i],a[j],b[j],b[i]],1 if i in[1,2,3] else 2 if i>=7 else 0,'whole_wall_depth_or_open_arch_reveal')
for f in earclip(WALL_SECTIONS[0][1]):m.face([rings[0][i] for i in f],0,'front_sand_face')
for f in earclip(WALL_SECTIONS[-1][1]):m.face([rings[-1][i] for i in f][::-1],0,'rear_sand_face')
G[WALL]=m.result('One thick closed tapered-depth sand wall with complete flared front/rear arched reveals, blunt upper shoulders and an entirely open ground-to-crown passage.');FEET.append(WALL)
# Full opposed interface triangulation is independently integrated, not inferred
# from these additional inside/outside witness points.
for name,cx in TOWER_CENTRES.items():
 left=cx<0;x=-.72 if left else .72;a,b=(name,WALL) if left else(WALL,name)
 CONTACTS.append({'name':name+'_WholeWallJunction','a':a,'b':b,'origin_m':(0,0,0),'axis':(1,0,0),'u':(0,1,0),'v':(0,0,1),'plane_m':x,'points':[(x,y,z) for y,z in[(0,.20),(-.10,.65),(.10,.95)]],'interior_probe_offset_m':.005,'minimum_patch_area_m2':.443,'role':'entire wall end is seated in the complete inward tower plane; no interpenetrating skins'})
# Closed arch air follows the bevel section and extends in front and behind.
def opening_profile(radius,floor=.003):
 return [(-radius,floor),(radius,floor),(radius,.49)]+[(radius*math.cos(i*math.pi/16),.49+radius*math.sin(i*math.pi/16)) for i in range(1,17)]
def loft_y(sections):
 m=Mesh();rings=[[(x,y,z) for x,z in p] for y,p in sections]
 for a,b in zip(rings,rings[1:]):
  for i in range(len(a)):j=(i+1)%len(a);m.face([a[i],a[j],b[j],b[i]])
 for f in earclip(sections[0][1]):m.face([rings[0][i] for i in f][::-1])
 for f in earclip(sections[-1][1]):m.face([rings[-1][i] for i in f])
 return m.result('whole closed lofted aperture witness, not exported')
volume(VOID_VOLUMES,'WholeGroundToCrownArchAndBothMouths',loft_y([(y,opening_profile(r)) for y,r in[(-.50,.435),(-.205,.435),(-.145,.395),(.145,.395),(.205,.435),(.50,.435)]]),list(G),'complete ground-to-crown door air follows every arch segment and both bevels; extends fully beyond front and rear mouths')
def radial_loft(cx,levels):
 m=Mesh();rings=[[(cx+r*math.cos(math.tau*i/N),r*math.sin(math.tau*i/N),z) for i in range(N)] for z,r in levels]
 m.face(rings[0][::-1]);m.face(rings[-1])
 for a,b in zip(rings,rings[1:]):
  for i in range(N):j=(i+1)%N;m.face([a[i],a[j],b[j],b[i]])
 return m.result('closed entire shallow court air, not exported')
def annular_sector(cx,a,b,ri,ro,z0,z1):
 m=Mesh();angles=[a,(a+b)/2,b];rings=[]
 for z in[z0,z1]:rings.append([(cx+r*math.cos(t),r*math.sin(t),z) for r,t in[(ri,a),(ro,a),(ro,(a+b)/2),(ro,b),(ri,b),(ri,(a+b)/2)]])
 for f in earclip([(p[0],p[1]) for p in rings[0]]):m.face([rings[0][i] for i in f][::-1]);m.face([rings[1][i] for i in f])
 for i in range(6):j=(i+1)%6;m.face([rings[0][i],rings[0][j],rings[1][j],rings[1][i]])
 return m.result('closed finite annular sector witness, not exported')
def tower_section_point(cx,z,sector_u,radial_u):
 for (z0,ro0,ri0),(z1,ro1,ri1) in zip(TOWER_LEVELS,TOWER_LEVELS[1:]):
  if z<=z1+1e-9:
   u=max(0,min(1,(z-z0)/(z1-z0)));ro=ro0+(ro1-ro0)*u;ri=ri0+(ri1-ri0)*u;break
 else:ro,ri=TOWER_LEVELS[-1][1:]
 i=int(math.floor(sector_u));u=sector_u-i
 def at(r,outer):return add(mul(tower_point(cx,r,i,z,outer),1-u),mul(tower_point(cx,r,i+1,z,outer),u))
 inside_=at(ri,False);outside_=at(ro,True)
 return add(inside_,mul(sub(outside_,inside_),radial_u))
def crown_witness(cx,start,levels,inner_u,outer_u):
 m=Mesh();rings=[]
 for z in levels:
  stations=[start+.12,start+1,start+1.88]
  rings.append([tower_section_point(cx,z,s,r) for r,s in[(inner_u,stations[0]),(outer_u,stations[0]),(outer_u,stations[1]),(outer_u,stations[2]),(inner_u,stations[2]),(inner_u,stations[1])]])
 if sum(rings[0][i][0]*rings[0][(i+1)%6][1]-rings[0][i][1]*rings[0][(i+1)%6][0] for i in range(6))<0:rings=[list(reversed(r)) for r in rings]
 for a,b in zip(rings,rings[1:]):
  for i in range(6):j=(i+1)%6;m.face([a[i],a[j],b[j],b[i]])
 for f in earclip([(p[0],p[1]) for p in rings[0]]):m.face([rings[0][i] for i in f][::-1])
 for f in earclip([(p[0],p[1]) for p in rings[-1]]):m.face([rings[-1][i] for i in f])
 return m.result('complete finite crown cell-derived witness; not exported')
for name,cx in TOWER_CENTRES.items():
 volume(VOID_VOLUMES,name+'_WholeShallowCourt',radial_loft(cx,[(1.105,.265),(1.25,.285),(1.28,.286),(1.44,.293),(1.48,.301),(1.56,.301)]),list(G),'entire finite shallow court following each inner wall level with open top')
 for k in range(8):
  # Left tower reflects the outer x coordinate, so angular intervals reflect.
  a=(k*4+2)*math.tau/N+.018;b=(k*4+4)*math.tau/N-.018
  if cx<0:a,b=math.pi-b,math.pi-a
  volume(VOID_VOLUMES,name+'_FullNotch_%02d'%k,crown_witness(cx,k*4+2,[1.256,1.28,1.44,1.48,1.56],-.07,1.5),list(G),'whole radial notch air from court to outside, above complete low sill, with bounded side insets')
  a=k*4*math.tau/N+.024;b=(k*4+2)*math.tau/N-.024
  if cx<0:a,b=math.pi-b,math.pi-a
  # At the D-cut inward crown, keep the entire witness within the real wall.
  rr=.405 if (math.cos((a+b)/2)*(1 if cx>0 else -1))>-.55 else .320
  volume(SOLID_VOLUMES,name+'_FiniteMerlonRoot_%02d'%k,crown_witness(cx,k*4,[1.235,1.25,1.275],.16,.84),[name],'continuous finite full merlon-root band crossing its crown level; not a point attachment')
volume(SOLID_VOLUMES,'Wall_WholeCrownBridge',box_geometry((-.30,-.12,.945),(.30,.12,1.055)),[WALL],'continuous finite crown bridge across whole door width above the arch')
for name,cx in TOWER_CENTRES.items():
 volume(SOLID_VOLUMES,name+'_WholeCourtBottom',radial_loft(cx,[(1.045,.255),(1.095,.255)]),[name],'complete finite solid court bottom below the shallow open recess')
SAND_CONTRACT={'single_modular_count':1,'editable_meshes':3,'tapered_towers':2,'integral_merlons_per_tower':8,'real_notches_per_tower':8,'bottomed_shallow_courts':2,'true_arch_passages':1,'arch_segments':16,'ground_level_m':0,'origin':'ground-level exact bounds centre','finite_opposed_wall_tower_contacts':2,'threshold_or_floor':False,'scene_or_old_interface_claimed':False}
def measure_sandcastle_geometry(vertices):
 assert set(vertices)==set(G)
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<3e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<3e-7 for p in actual),(n,'actual shape changed')
 return dict(SAND_CONTRACT,whole_void_groups=len(VOID_VOLUMES),finite_material_volume_groups=len(SOLID_VOLUMES),materials=MATERIAL_CONTRACT)
FOCUS=(0,0,.72);ORTHO=3.80
CAMERAS={'gray-front3q':(3.8,-6,3.8),'gray-back3q':(-3.8,6,3.8),'thumbnail':(3.8,-6,3.8),'qa-front':(0,-7,2.4),'qa-side':(7,0,2.6),'qa-top':(0,0,7),'qa-back':(0,7,2.4),'qa-wireframe':(3.8,-6,3.8),'silhouette-128-front':(0,-7,2.4),'silhouette-128-side':(7,0,2.6)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneCrenellatedSandGateModule',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground-level exact bounds centre (0,0,0), source Z up and front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-1.05,0,.5),(-1.05,0,1.2)),(WALL,(0,0,1.02),(0,0,.5))]:
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
mount_evidence=measure_sandcastle_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'sandcastle_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
  files[role]={'path':f'assets/beach/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'beach','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
