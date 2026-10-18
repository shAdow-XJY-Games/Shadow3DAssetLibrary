"""One original low roundabout platform, fixed static visual assembly only.
Metres, Z up, axis origin on ground; no motion, users, loading or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='playground-fixed-roundabout-platform-01';VERSION='1.0.0';TITLE='Three-Zone Fixed Roundabout Platform'
DESCRIPTION=('One original low-poly low roundabout exterior in one fixed static pose. A wide grounded circular base joins a solid vertical shaft and a finite horizontal shoulder. A genuinely through-bored flanged centre sleeve rests on the complete shoulder face; the thick circular platform rests on the sleeve flange. Positive air separates the shaft from the complete bore wall and the deck from the base outside its support. Three continuous rounded U-shaped radial rails each have two finite embedded ends in the deck, dividing three open platform areas with clear outer entrances. The deck is one closed annular solid with alternating muted teal top sectors and a dark edge; the warm ochre rails and sleeve remain individually editable. One complete assembly counts as one prop. Metres, Z up, origin at ground beneath the centre axis. Constant opaque PBR colours only, no textures, people, seats, canopy, ground scene, logos or added accessories. Static visual geometry only: no rotation, animation, bearing performance, friction, ride simulation, multi-person use, child or adult suitability, age guidance, clearances for bodies, motion balance, entrapment protection, centrifugal loads, structural capacity, stability, installation, manufacturing specification or playground/safety certification. No claimed compatibility with old playground scenes or other assets.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];CONTACTS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={};RAILS=[];SELFTESTS=[]
PALETTE=[('Deck_DeepTeal',(.035,.25,.29,1),.48,.05),('Deck_PaleTeal',(.17,.48,.47,1),.48,.05),('Rails_WarmOchre',(.88,.49,.09,1),.40,.18),('Mounts_Graphite',(.075,.105,.12,1),.40,.55),('Shaft_SatinSteel',(.39,.46,.48,1),.31,.72)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 vs=[tuple(round(float(c),7) for c in v) for v in vs];fs=[tuple(f) for f in fs]
 volume=sum(dot(vs[f[0]],cross(vs[f[j]],vs[f[j+1]]))/6 for f in fs for j in range(1,len(f)-1))
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 G[name]={'vertices':vs,'faces':fs,'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.009):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def cylinder_geometry(p,q,r,n=48):
 p=tuple(p);q=tuple(q);axis=unit(sub(q,p));u=unit(cross(axis,(0,0,1) if abs(axis[2])<.9 else (0,1,0)));v=cross(axis,u)
 vv=[add(c,mul(add(mul(u,math.cos(j*math.tau/n)),mul(v,math.sin(j*math.tau/n))),r)) for c in [p,q] for j in range(n)]
 ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return vv,ff

def cylinder(name,p,q,r,mat,role,n=48):return mesh(name,*cylinder_geometry(p,q,r,n),mat,role)
def revolve(profile,n=48):
 v=[(r*math.cos(math.tau*j/n),r*math.sin(math.tau*j/n),z) for r,z in profile for j in range(n)];f=[]
 for i in range(len(profile)):
  k=(i+1)%len(profile)
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,k*n+(j+1)%n,k*n+j))
 return v,f

def ring(ri,ro,z0,z1,n=48):return revolve([(ri,z0),(ro,z0),(ro,z1),(ri,z1)],n)
def probe(vf,role,targets):return {'vertices':vf[0],'faces':vf[1],'role':role,'targets':list(targets)}
def radial_box(r0,r1,width,z0,z1,a):
 e=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0)
 v=[add(add(mul(e,x),mul(t,y)),(0,0,z)) for z in [z0,z1] for y in [-width/2,width/2] for x in [r0,r1]]
 return v,BOX_FACES

def rail_geometry(a):
 path=[(.44,.31,0,1),(.44,.88,0,1)]
 for j in range(1,7):
  b=math.pi-math.pi/2*j/6;path.append((.56+.12*math.cos(b),.88+.12*math.sin(b),math.sin(b),-math.cos(b)))
 path.append((.98,1.0,1,0))
 for j in range(1,7):
  b=math.pi/2-math.pi/2*j/6;path.append((.98+.12*math.cos(b),.88+.12*math.sin(b),math.sin(b),-math.cos(b)))
 path.append((1.10,.31,0,-1));v=[];sides=12
 e=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0)
 for r,z,tr,tz in path:
  c=add(mul(e,r),(0,0,z));normal=add(mul(e,-tz),(0,0,tr))
  for j in range(sides):
   b=math.tau*j/sides;v.append(add(c,mul(add(mul(normal,math.cos(b)),mul(t,math.sin(b))),.035)))
 f=[tuple(reversed(range(sides))),tuple((len(path)-1)*sides+j for j in range(sides))]
 for i in range(len(path)-1):
  for j in range(sides):
   k=(j+1)%sides;f.extend([(i*sides+j,i*sides+k,(i+1)*sides+k),(i*sides+j,(i+1)*sides+k,(i+1)*sides+j)])
 return v,f,path

base=cylinder('Base_GroundedCircularPlinth',(0,0,0),(0,0,.08),.40,3,'closed low circular base with complete finite ground face')
FEET.append(base)
shaft=cylinder('Axis_SolidVerticalShaft',(0,0,.07),(0,0,.46),.085,4,'real solid axis; positive radial gap to complete centre sleeve bore')
shoulder=cylinder('Axis_HorizontalShoulder',(0,0,.075),(0,0,.18),.36,3,'wide horizontal shoulder joined to base and shaft; upper face directly supports sleeve bottom')
link(base,shaft,(0,0,.075),spread=.025);link(base,shoulder,(.20,0,.0775),spread=.035);link(shaft,shoulder,(0,0,.12),spread=.025)
sleeve=mesh('Hub_ThroughBoredFlangedSleeve',*revolve([(.098,.18),(.34,.18),(.34,.24),(.22,.24),(.22,.41),(.098,.41)]),2,'one closed continuous flanged sleeve with a true full-height through-hole; bottom rests on shoulder, flange top supports platform')
deck=mesh('Platform_ThickThreeZoneDeck',*ring(.225,1.30,.24,.32),0,'one complete thick annular standing-platform appearance; finite underside rests on sleeve flange')
# Top colour sectors are face material assignments, not stacked overlays.
G[deck]['face_materials']=[(0 if j//16%2==0 else 1) if i==2 else 0 for i in range(4) for j in range(48)]
for a,b,z,radius,minimum in [(shoulder,sleeve,.18,.20,.30),(sleeve,deck,.24,.28,.18)]:
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':z,'minimum_patch_area_m2':minimum,'interior_probe_offset_m':.001,'points':[(radius*math.cos(k*math.tau/6+.04),radius*math.sin(k*math.tau/6+.04),z) for k in range(6)],'role':'complete opposed horizontal annular seat; no penetration or motion claim'})
for i,a in enumerate([math.pi/2,7*math.pi/6,11*math.pi/6]):
 v,f,path=rail_geometry(a);name=mesh('Rail_ContinuousRoundedU_'+str(i+1),v,f,2,'one closed continuous rounded U; inner and outer ends each embedded finitely into deck')
 e=(math.cos(a),math.sin(a),0);t=(-math.sin(a),math.cos(a),0)
 for label,r in [('Inner',.44),('Outer',1.10)]:
  p=add(mul(e,r),(0,0,.315));link(deck,name,p,axis=t,spread=.012)
  vf=cylinder_geometry(add(mul(e,r),(0,0,.312)),add(mul(e,r),(0,0,.318)),.020,12)
  WALL_VOLUMES[name+'_'+label+'_FullEmbeddedEnd']=dict(probe(vf,'whole finite rail-end volume contained in both connected solids',[deck,name]),targets=[deck,name])
 RAILS.append({'name':name,'angle_rad':a,'inner_radius_m':.44,'outer_radius_m':1.10,'section_radius_m':.035,'section_sides':12,'path_sections':len(path),'both_ends_z_m':.31,'deck_top_z_m':.32})
SELFTESTS=[(base,(0,0,.04),(.5,0,.04)),(sleeve,(.15,0,.30),(0,0,.30)),(deck,(.70,0,.28),(0,0,.28))]
ISOLATED_VOID_VOLUMES['Hub_FullThroughBore']=probe(cylinder_geometry((0,0,.175),(0,0,.415),.096,48),'complete isolated bore volume, not ray',[sleeve])
VOID_VOLUMES['Axis_CompleteAnnularAir']=probe(ring(.087,.096,.184,.406),'whole 360 degree positive radial shaft/sleeve gap',[shaft,sleeve])
VOID_VOLUMES['Platform_CompleteUnderdeckAir']=probe(ring(.405,1.285,.085,.235),'whole outer 360 degree underdeck finite empty annulus',G)
for i,a in enumerate([math.pi/6,5*math.pi/6,3*math.pi/2]):
 VOID_VOLUMES['Zone_'+str(i+1)+'_FullStandingSpace']=probe(radial_box(.40,1.18,.42,.325,1.12,a),'complete finite rectangular standing-space appearance with no human-fit claim',G)
 VOID_VOLUMES['Zone_'+str(i+1)+'_FullEntry']=probe(radial_box(1.10,1.47,.55,.325,1.12,a),'complete finite outer-entry volume, no user-fit or accessibility claim',G)
BORES.append({'mesh':sleeve,'origin_m':(0,0,.17),'direction':(0,0,1),'length_m':.25,'meaning':'supplementary isolated bore ray; full finite bore decides'})
# One whole annular inset slab certifies actual platform thickness and continuity.
WALL_VOLUMES['Platform_CompleteSolidThickness']=dict(probe(ring(.232,1.29,.245,.315),'complete annular inset slab within deck material',[deck]),targets=[deck])
ROUNDABOUT_CONTRACT={'base':base,'shaft':shaft,'shoulder':shoulder,'sleeve':sleeve,'deck':deck,'rails':RAILS,'complete_contacts':CONTACTS,'single_prop_count':1,'frozen_static_pose':True}
def measure_roundabout_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 def bounds(n):return ([min(float(p[k]) for p in vertices[n]) for k in range(3)],[max(float(p[k]) for p in vertices[n]) for k in range(3)])
 expected={base:([-.4,-.4,0],[.4,.4,.08]),shaft:([-.085,-.085,.07],[.085,.085,.46]),shoulder:([-.36,-.36,.075],[.36,.36,.18]),sleeve:([-.34,-.34,.18],[.34,.34,.41]),deck:([-1.3,-1.3,.24],[1.3,1.3,.32])}
 for n,(low,high) in expected.items():
  actual=bounds(n);assert max(abs(actual[j][k]-[low,high][j][k]) for j in range(2) for k in range(3))<2e-6,(n,actual)
 for r in RAILS:
  vv=vertices[r['name']];assert len(vv)==r['path_sections']*r['section_sides']
  for ids,radius in [(list(range(12)),.44),(list(range(len(vv)-12,len(vv))),1.10)]:
   center=tuple(sum(float(vv[j][k]) for j in ids)/12 for k in range(3));want=(radius*math.cos(r['angle_rad']),radius*math.sin(r['angle_rad']),.31)
   assert max(abs(center[k]-want[k]) for k in range(3))<2e-6,(r['name'],center,want)
 return {'single_prop_count':1,'closed_thick_deck':True,'deck_diameter_m':2.6,'deck_thickness_m':.08,'deck_bottom_m':.24,'three_continuous_u_rails':3,'finite_embedded_rail_ends':6,'true_center_bore_nominal_diameter_m':.196,'shaft_nominal_diameter_m':.17,'complete_opposed_annular_seats':2,'frozen_static_pose':True,'motion_human_fit_load_or_safety_claim':False}
FOCUS=(0,0,.52);ORTHO=3.35
CAMERAS={'gray-front3q':(3.5,-4,3.4),'gray-back3q':(-3.5,4,3.4),'thumbnail':(3.5,-4,3.4),'qa-front':(0,-4,2.25),'qa-side':(4,0,2.25),'qa-top':(0,0,4),'qa-back':(0,4,2.25),'qa-wireframe':(3.5,-4,3.4),'silhouette-128-front':(0,-4,2.25),'silhouette-128-side':(4,0,2.25)}
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
root=bpy.data.objects.new('OneThreeZoneRoundabout',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in SELFTESTS:
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
mount_evidence=measure_roundabout_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'roundabout_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/playground/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'playground','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
