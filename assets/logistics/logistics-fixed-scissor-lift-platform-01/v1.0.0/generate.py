"""One original static scissor lift platform at one fixed raised height; one prop.
True perforated layered arms, fixed pins, short guide slots and rollers.
Metres, native Z up, front -Y. No motion, hydraulics, load or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='logistics-fixed-scissor-lift-platform-01';VERSION='1.0.0';TITLE='Fixed Scissor Lift Platform'
DESCRIPTION=('One original low-poly static scissor lift platform at one fixed raised height, counted as one prop: an open rectangular ground frame, independent upper support frame and broad thick top platform. Each side has two separate thick crossed arms with three real octagonal through-bores. The layers have positive clearance, with a fixed center pin passing through both actual center holes. Four fixed bored ear seats and four short real through-slots with separate bored fixed rollers carry the arm endpoints to the frames. Fixed pins have small finite radial seating overlaps; these are static visual joints, not moving mechanical fits. All solids have finite ground-connected support paths. Opaque constant PBR colours, no texture, overlay, text, cargo, person, pallet, hydraulics, animation or surrounding scene. Metres, native Z up, front -Y, ground-level origin. '
'Static visual geometry only. No lifting, lowering, hydraulic action, rolling, mechanism motion, complete travel path, load capacity, stability, working-height suitability, people or cargo transport, manufacturing tolerance, installation compatibility, equipment certification or safety claim. No compatibility with previous pallet, pallet-jack or loading-platform assets is implied.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];FLOOR_PROBES=[];WALL_PROBES=[];ARMS=[];GUIDES=[];EARS=[];PINS=[];ISOLATED_VOLUMES={}
PALETTE=[('Frame_DeepBlue',(.035,.105,.155,1),.43,.42),('Arms_WarmOchre',(.86,.43,.055,1),.46,.26),('Pins_BrushedSteel',(.48,.55,.60,1),.29,.78),('Deck_SatinSilver',(.56,.63,.66,1),.52,.58)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,mat,role):
 assert name not in G;G[name]={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':mat,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
ZB=((1,0,0),(0,1,0),(0,0,1));YB=((1,0,0),(0,0,1),(0,-1,0))
def box(name,c,size,mat,role,u=(1,0,0),v=(0,1,0),w=(0,0,1)):
 return mesh(name,[transform((a*size[0]/2,b*size[1]/2,d*size[2]/2),c,u,v,w) for d in [-1,1] for b in [-1,1] for a in [-1,1]],BOX_FACES,mat,role)
def rod(name,a,b,r,mat,role,n=16):
 w=unit(sub(b,a));u=unit(cross(w,(0,0,1) if abs(w[2])<.9 else (1,0,0)));v=cross(w,u)
 vs=[add(p,add(mul(u,r*math.cos(math.tau*i/n)),mul(v,r*math.sin(math.tau*i/n)))) for p in [a,b] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,role)
def ring_data(outer,inner,c,basis,lo,hi):
 n=len(outer);assert n==len(inner);vs=[transform((x,y,z),c,*basis) for poly,z in [(outer,lo),(outer,hi),(inner,lo),(inner,hi)] for x,y in poly];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return vs,fs
def rect(l,r,b,t):return [(r,0),(r,t),(0,t),(l,t),(l,0),(l,b),(0,b),(r,b)]
def circle(r,n=8):return [(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n)) for i in range(n)]
def annulus(name,outer,inner,c,basis,lo,hi,mat,role):
 vs,fs=ring_data(outer,inner,c,basis,lo,hi);return mesh(name,vs,fs,mat,role)
def link(a,b,p,axis=(0,1,0),spread=.003):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void_box(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],'faces':BOX_FACES,'role':role}
def isolated_volume(name,target,poly,c,basis,lo,hi,inset):
 n=len(poly);vs=[transform((x,z,t),c,*basis) for t in [lo,hi] for x,z in poly]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 ISOLATED_VOLUMES[name]={'target_mesh':target,'vertices':vs,'faces':fs,'nominal_boundary_inset_m':inset,'axis_depth_range_m':[lo,hi],'negative_off_axis_point_m':add(c,mul(basis[0],.009)),'role':'complete finite isolated opening, beyond both surfaces of the full actual hole depth; fixed assembled pin intentionally excluded from isolated test'}
def bored_arm(name,a,b,y):
 # Three rectangle-to-octagon annular cells share welded seams. No overlapping internal faces.
 length=math.dist(a,b);u=unit(sub(b,a));v=(-u[2],0,u[0]);w=(0,-1,0);c=((a[0]+b[0])/2,y,(a[2]+b[2])/2)
 limits=[-length/2-.045,-length/4,length/4,length/2+.045];centres=[-length/2,0,length/2];vs=[];fs=[];lookup={}
 def vid(p):
  p=tuple(round(k,9) for k in p)
  if p not in lookup:lookup[p]=len(vs);vs.append(transform(p,c,u,v,w))
  return lookup[p]
 for k,x in enumerate(centres):
  outer=[(xx+x,zz) for xx,zz in rect(limits[k]-x,limits[k+1]-x,-.070,.070)];inner=[(xx+x,zz) for xx,zz in circle(.023)]
  ob=[vid((xx,zz,-.017)) for xx,zz in outer];ot=[vid((xx,zz,.017)) for xx,zz in outer];ib=[vid((xx,zz,-.017)) for xx,zz in inner];it=[vid((xx,zz,.017)) for xx,zz in inner]
  for i in range(8):
   j=(i+1)%8;fs.extend([(ob[i],ib[i],ib[j],ob[j]),(ot[i],ot[j],it[j],it[i]),(ib[i],it[i],it[j],ib[j])])
   if (k>0 and abs(outer[i][0]-limits[k])<1e-8 and abs(outer[j][0]-limits[k])<1e-8) or (k<2 and abs(outer[i][0]-limits[k+1])<1e-8 and abs(outer[j][0]-limits[k+1])<1e-8):continue
   fs.append((ob[i],ob[j],ot[j],ot[i]))
 name=mesh(name,vs,fs,1,'single continuous 34 mm thick three-bore scissor arm; no crossing solid rods')
 holes=[(a[0],y,a[2]),(c[0],y,c[2]),(b[0],y,b[2])]
 for k,p in enumerate(holes):
  BORES.append({'mesh':name,'origin_m':(p[0],y-.05,p[2]),'direction':(0,1,0),'length_m':.10})
  isolated_volume(name+'_FullBore_%02d'%k,name,circle(.020),p,(u,v,w),-.025,.025,.003)
 ARMS.append({'mesh':name,'end_centres_m':holes[::2],'centre_bore_m':holes[1],'thickness_m':.034,'bore_polygon_circumradius_m':.023,'layer_centre_y_m':y})
 return name
base=annulus('Base_ContinuousOpenGroundFrame',rect(-.83,.83,-.52,.52),rect(-.68,.68,-.24,.24),(0,0,0),ZB,0,.09,0,'one continuous rectangular bottom frame with real full opening and finite ground footprint');FEET.append(base)
topframe=annulus('Top_IndependentOpenSupportFrame',rect(-.79,.79,-.51,.51),rect(-.66,.66,-.24,.24),(0,0,0),ZB,1.19,1.29,0,'independent upper rectangular frame; continuous finite support for top deck')
deck=box('Platform_BroadThickDeck',(0,0,1.31),(1.78,1.20,.08),3,'broad 80 mm thick fixed top platform; no surface decal')
link(topframe,deck,(0,-.40,1.28),axis=(1,0,0),spread=.12)
for label,sign in [('Front',-1),('Back',1)]:
 ya=sign*.40;yb=sign*.34;yc=sign*.37;zl=.22;zh=1.10;zm=.66
 arm_a=bored_arm(label+'_RisingPerforatedArm',(-.60,0,zl),(.60,0,zh),ya)
 arm_b=bored_arm(label+'_FallingPerforatedArm',(-.60,0,zh),(.60,0,zl),yb)
 ymin=min(ya,yb)-.037;ymax=max(ya,yb)+.037
 pin=rod(label+'_CenterThroughPin',(0,ymin,zm),(0,ymax,zm),.026,2,'fixed center axle passes both genuine arm holes; static finite radial seat');PINS.append(pin)
 for arm,y in [(arm_a,ya),(arm_b,yb)]:link(arm,pin,(.0245,y,zm))
 for suffix,y1,y2 in [('Minus',ymin-.007,ymin+.012),('Plus',ymax-.012,ymax+.007)]:
  cap=rod(label+'_CenterPinCap_'+suffix,(0,y1,zm),(0,y2,zm),.045,2,'finite external center pin head separated from arm faces');link(pin,cap,(0,(y1+y2)/2,zm),axis=(1,0,0),spread=.006)
 # Low rising arm and high falling arm have genuine fixed bored ear seats.
 for suffix,arm,y,z,upper in [('LowerFixed',arm_a,ya,zl,False),('UpperFixed',arm_b,yb,zh,True)]:
  ey=y+sign*(.07 if y==ya else -.07);lo,hi=(-.15,.10) if not upper else (-.10,.12)
  ear=annulus(label+'_'+suffix+'BoredEar',rect(-.085,.085,lo,hi),circle(.023),(-.60,ey,z),YB,-.017,.017,0,'thick fixed ear with a genuine through hole, finitely attached to its support frame');EARS.append(ear)
  BORES.append({'mesh':ear,'origin_m':(-.60,ey-.06,z),'direction':(0,1,0),'length_m':.12})
  isolated_volume(ear+'_FullBore',ear,circle(.020),(-.60,ey,z),YB,-.025,.025,.003)
  support=topframe if upper else base;link(ear,support,(-.60,ey,1.205 if upper else .08),axis=(1,0,0),spread=.020)
  p=rod(label+'_'+suffix+'Pin',(-.60,min(y,ey)-.019,z),(-.60,max(y,ey)+.019,z),.026,2,'fixed endpoint pin through real arm and ear holes');PINS.append(p)
  link(arm,p,(-.5755,y,z));link(ear,p,(-.5755,ey,z))
 # Opposite endpoints have a short true guide aperture with a separate bored fixed roller.
 for suffix,arm,y,z,upper in [('LowerGuide',arm_b,yb,zl,False),('UpperGuide',arm_a,ya,zh,True)]:
  gy=y+sign*(.07 if y==ya else -.07);lo,hi=(-.15,.10) if not upper else (-.10,.12)
  guide=annulus(label+'_'+suffix+'OpenSlot',rect(-.185,.185,lo,hi),rect(-.15,.15,-.044,.044),(.60,gy,z),YB,-.017,.017,0,'short rectangular through-slot; not a painted recess, travel or motion claim')
  roller=annulus(label+'_'+suffix+'BoredRoller',circle(.046,16),circle(.023,16),(.60,gy,z),YB,-.015,.015,2,'separate 30 mm thick hollow fixed roller seated in guide; no rotation claim')
  support=topframe if upper else base;link(guide,support,(.60,gy,1.205 if upper else .08),axis=(1,0,0),spread=.020)
  link(guide,roller,(.60,gy,z+.045),spread=.005)
  p=rod(label+'_'+suffix+'ThroughPin',(.60,min(y,gy)-.019,z),(.60,max(y,gy)+.019,z),.026,2,'fixed endpoint axle through true arm and roller bores');PINS.append(p)
  link(arm,p,(.6245,y,z));link(roller,p,(.6245,gy,z))
  for part in [guide,roller]:BORES.append({'mesh':part,'origin_m':(.60,gy-.06,z),'direction':(0,1,0),'length_m':.12})
  isolated_volume(guide+'_FullSlot',guide,rect(-.147,.147,-.041,.041),(.60,gy,z),YB,-.025,.025,.003)
  isolated_volume(roller+'_FullBore',roller,circle(.020,16),(.60,gy,z),YB,-.025,.025,.003)
  GUIDES.append({'slot':guide,'roller':roller,'pin':p,'arm':arm,'centre_m':(.60,gy,z),'slot_width_m':.30,'slot_height_m':.088,'slot_plate_thickness_m':.034,'roller_outer_circumradius_m':.046,'roller_bore_circumradius_m':.023,'fixed_static_seat_only':True})
  for side,low,high in [('Left',.47,.54),('Right',.66,.73)]:void_box(label+'_'+suffix+'_FreeSlot'+side,(low,gy-.025,z-.037),(high,gy+.025,z+.037),'complete finite unoccupied end section of true short guide slot')
 # Complete finite layer gap around the only intended cross-gap solid, the fixed center pin.
 outer=rect(-.68,.68,-.51,.51);inner=circle(.032)
 vs,fs=ring_data(outer,inner,(0,yc,zm),YB,-.009,.009)
 VOID_VOLUMES[label+'_CompleteInterlayerGapExceptPin']={'vertices':vs,'faces':fs,'role':'complete finite interlayer slab between arm surfaces, except a bounded center-pin passage','negative_interior_point_m':(-.30,yc,zm)}
void_box('CenterBetweenBothSideMechanisms',(-.62,-.20,.14),(.62,.20,1.17),'complete finite open center between independent side scissor pairs')
void_box('InsideUpperFrameBelowDeck',(-.63,-.20,1.195),(.63,.20,1.263),'finite open upper frame interior below the solid platform')
GAPS.append({'label':'BetweenBothScissorSides','origin_m':(0,-.28,.66),'direction':(0,1,0),'length_m':.56})
SCISSOR_LIFT_CONTRACT={'single_prop_count':1,'base_frame':base,'upper_frame':topframe,'platform':deck,'platform_thickness_m':.08,'platform_top_z_m':1.35,'side_pairs':2,'arms':ARMS,'fixed_bored_ears':EARS,'guide_assemblies':GUIDES,'through_pins':PINS,'interlayer_surface_gap_m':.026,'ground_meshes':FEET,'static_one_height_only':True,'hydraulics_animation_travel_load_or_safety_claim':False}
def measure_scissor_lift_geometry(vertices):
 assert set(vertices)==set(G),'Changed complete platform mesh set'
 rows=[]
 for name,g in G.items():
  actual=sorted(set(tuple(float(c) for c in p) for p in vertices[name]));expected=sorted(set(g['vertices']))
  assert len(actual)==len(expected),('Changed unique surface vertex count',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(i)==1 for i in matches) and len({i[0] for i in matches})==len(expected),('Actual surface lacks bijective unique source match',name)
  rows.append({'mesh':name,'unique_vertices':len(actual),'maximum_position_error_m':max(math.dist(p,expected[i[0]]) for p,i in zip(actual,matches)),'unique_bijective_surface_match':True})
 return dict(SCISSOR_LIFT_CONTRACT,actual_components=rows,full_finite_void_count=len(VOID_VOLUMES),full_isolated_volume_count=len(ISOLATED_VOLUMES),material_contract=MATERIAL_CONTRACT)
FOCUS=(0,0,.675);ORTHO=2.65
CAMERAS={'gray-front3q':(3,-4,3.35),'gray-back3q':(-3,4,3.35),'thumbnail':(3,-4,3.35),'qa-front':(0,-6,2.60),'qa-side':(6,0,2.60),'qa-top':(0,0,6),'qa-back':(0,6,2.60),'qa-wireframe':(3,-4,3.35),'silhouette-128-front':(0,-6,2.60),'silhouette-128-side':(6,0,2.60)}
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
root=bpy.data.objects.new('OneCompleteFixedScissorLiftPlatform',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Design ground datum X=0, Y=0, Z=0; not the whole-platform AABB centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
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
adj={o.name:set() for o in parts}
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
isolated_finite_checks=[]
for name,probe in ISOLATED_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False);target=probe['target_mesh'];obj=byname[target];tree=trees[target]
 crossing=tree.overlap(pt);model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)];probe_inside=[i for i,v in enumerate(pv) if inside(tree,v)]
 assert not crossing and not model_inside and not probe_inside,('Isolated finite opening obstructed',name,target,len(crossing),model_inside,probe_inside)
 isolated_finite_checks.append({'probe':name,'target_mesh':target,'nominal_boundary_inset_m':probe['nominal_boundary_inset_m'],'axis_depth_range_m':probe['axis_depth_range_m'],'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside),'complete_finite_isolated_volume_empty':True})
scissor_evidence=measure_scissor_lift_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'scissor_lift_geometry':scissor_evidence,'finite_empty_volumes':void_volume_checks,'finite_isolated_openings':isolated_finite_checks,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/logistics/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'logistics','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
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
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
