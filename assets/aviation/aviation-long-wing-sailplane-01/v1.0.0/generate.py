"""Original long-wing sailplane, one fixed static exterior prop. No flight claims."""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='aviation-long-wing-sailplane-01';VERSION='1.0.0';TITLE='Long Wing T-Tail Sailplane'
DESCRIPTION=('One original static low-poly unpowered sailplane exterior: a newly lofted slender continuous fuselage and tapered tail boom, long progressively tapered thick wings with modest upward geometry, a high T-tail, a continuous closed nose without a propeller, and a fixed opaque canopy region sharing the fuselage surface topology. One centerline landing wheel, its axle and two finite forks, plus a tail skid strut and finite ground shoe support the fixed display pose. Every separate wing, tail and landing member has a finite geometric connection. '
 'One complete aircraft counts as one prop. Eleven editable closed meshes and four opaque constant PBR materials; no texture, animation, tow equipment, cockpit interior, people or airport scene. Metres, native Z up, nose/front -Y, origin X=Y=0 at ground level. '
 'Static visual geometry only. No flight, aerodynamic lift or glide ratio, control or landing-gear movement, cockpit access, occupant fit, balance, ground stability, structural load, manufacturing dimensions, airworthiness or aviation safety certification. No compatibility with earlier towbar or parking assets is claimed.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={}
PALETTE=[('Airframe_WarmIvory',(.83,.85,.81,1),.43,.08),('FixedCanopy_OpaquePetrol',(.035,.12,.16,1),.32,.28),('Tips_Vermilion',(.83,.18,.065,1),.47,.05),('Gear_Charcoal',(.055,.065,.071,1),.65,.22)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'fixed_canopy_on_same_closed_surface':True,'no_surface_overlays':True,'flight_or_stability_claim':False}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-9 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(0,1,0),spread=.008):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def rod(name,a,b,radius,mat,role,n=12):
 d=unit(sub(b,a));u=unit(cross(d,(0,0,1) if abs(d[2])<.9 else (0,1,0)));v=cross(d,u)
 vs=[add(p,add(mul(u,radius*math.cos(math.tau*j/n)),mul(v,radius*math.sin(math.tau*j/n)))) for p in [a,b] for j in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return mesh(name,vs,fs,mat,role)
def void(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':role,'enclosed_fill_center_m':mul(add(lo,hi),.5)}
# Original variable-section forebody and slender tail boom, made as one closed shell.
BODY_STATIONS=[(-3.40,.035,.045,.84),(-3.20,.14,.15,.87),(-2.78,.245,.27,.92),(-2.45,.30,.365,.97),(-1.75,.345,.43,.99),(-.88,.35,.40,.99),(-.25,.315,.365,.99),(.40,.245,.27,.94),(1.12,.145,.155,.85),(2.15,.105,.11,.77),(3.15,.075,.085,.73),(3.70,.035,.045,.73)]
N_BODY=16;vs=[(rx*math.cos(math.tau*j/N_BODY),y,z+rz*math.sin(math.tau*j/N_BODY)) for y,rx,rz,z in BODY_STATIONS for j in range(N_BODY)]
fs=[tuple(reversed(range(N_BODY))),tuple((len(BODY_STATIONS)-1)*N_BODY+j for j in range(N_BODY))];fm=[0,0]
for k in range(len(BODY_STATIONS)-1):
 for j in range(N_BODY):
  fs.append((k*N_BODY+j,k*N_BODY+(j+1)%N_BODY,(k+1)*N_BODY+(j+1)%N_BODY,(k+1)*N_BODY+j))
  fm.append(1 if 2<=k<=4 and 1<=j<=6 else 0)
FUSELAGE=mesh('Fuselage_ContinuousForebodyAndTailBoom',vs,fs,0,'one closed newly lofted pointed forebody and long tapered tail boom; fixed opaque canopy is a material region of this same continuous surface',fm)
# Each closed foil section has distinct leading and finite trailing-edge thickness.
FOIL=[(0,0),(.08,.55),(.25,1),(.55,.65),(1,.05),(1,-.05),(.55,-.42),(.25,-.55),(.08,-.35)]
WING_STATIONS=[(.19,-.90,1.45,.135,1.035),(1.25,-.82,1.32,.117,1.06),(4.1,-.47,.83,.077,1.16),(6.45,-.12,.38,.042,1.29),(7.20,.025,.25,.028,1.35)]
WINGS=[]
def wing_half(sign):
 vs=[(sign*x,lead+u*chord,z+t*thick) for x,lead,chord,thick,z in WING_STATIONS for u,t in FOIL];n=len(FOIL);fs=[tuple(reversed(range(n))),tuple((len(WING_STATIONS)-1)*n+j for j in range(n))];fm=[0,2]
 for k in range(len(WING_STATIONS)-1):
  for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));fm.append(2 if k==len(WING_STATIONS)-2 else 0)
 name=mesh('LongTaperedWing_'+('Right' if sign>0 else 'Left'),vs,fs,0,'new five-station closed thick tapered long wing; finite root embedded in fuselage, no control-surface or aerodynamic claim',fm);WINGS.append(name);link(FUSELAGE,name,(sign*.245,-.43,1.065),axis=(0,1,0),spread=.04)
wing_half(-1);wing_half(1)
# Vertical fin: multiple horizontal sections, tapered thickness and aft sweep.
FIN_STATIONS=[(.70,2.72,.94,.080),(1.00,2.76,.94,.072),(1.75,3.04,.70,.045),(2.13,3.17,.56,.032)]
vs=[(t*thick,lead+u*chord,z) for z,lead,chord,thick in FIN_STATIONS for u,t in FOIL];n=len(FOIL)
fs=[tuple(reversed(range(n))),tuple((len(FIN_STATIONS)-1)*n+j for j in range(n))]+[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for k in range(len(FIN_STATIONS)-1) for j in range(n)]
FIN=mesh('VerticalFin_SweptTSupport',vs,fs,0,'one closed swept vertical fin with real fuselage root and high horizontal-tail support');link(FUSELAGE,FIN,(0,3.20,.745),axis=(0,1,0),spread=.020)
TAIL_STATIONS=[(-1.37,3.19,.38,.038,2.105),(-.70,3.06,.61,.053,2.105),(0,3.03,.68,.060,2.105),(.70,3.06,.61,.053,2.105),(1.37,3.19,.38,.038,2.105)]
vs=[(x,lead+u*chord,z+t*thick) for x,lead,chord,thick,z in TAIL_STATIONS for u,t in FOIL]
fs=[tuple(reversed(range(n))),tuple((len(TAIL_STATIONS)-1)*n+j for j in range(n))]+[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for k in range(len(TAIL_STATIONS)-1) for j in range(n)]
TAIL=mesh('HorizontalTail_ContinuousHighT',vs,fs,0,'one closed tapered high horizontal tail across the actual fin crown');link(FIN,TAIL,(0,3.45,2.105),axis=(0,1,0),spread=.025)
# Single central polygonal wheel has a real finite flat facet at Z=0.
N_WHEEL=24;WHEEL_RADIUS=.22;WHEEL_Z=WHEEL_RADIUS*math.cos(math.pi/N_WHEEL);WHEEL_Y=-.55
vs=[(x,WHEEL_Y+WHEEL_RADIUS*math.cos(math.tau*j/N_WHEEL+math.pi/N_WHEEL),WHEEL_Z+WHEEL_RADIUS*math.sin(math.tau*j/N_WHEEL+math.pi/N_WHEEL)) for x in [-.075,.075] for j in range(N_WHEEL)]
fs=[tuple(reversed(range(N_WHEEL))),tuple(N_WHEEL+j for j in range(N_WHEEL))]+[(j,(j+1)%N_WHEEL,(j+1)%N_WHEEL+N_WHEEL,j+N_WHEEL) for j in range(N_WHEEL)]
WHEEL=mesh('CenterlineWheel_FiniteGroundFacet',vs,fs,3,'one solid 24-sided wheel, finite actual planar bottom contact; no rolling or tire deformation claim');FEET.append(WHEEL)
AXLE=rod('WheelAxle_Fixed',(-.15,WHEEL_Y,WHEEL_Z),(.15,WHEEL_Y,WHEEL_Z),.031,3,'fixed transverse axle embedded in wheel and both forks');link(WHEEL,AXLE,(0,WHEEL_Y,WHEEL_Z),axis=(1,0,0),spread=.04)
FORKS=[]
for sign in [-1,1]:
 x=sign*.116;name=rod('WheelFork_'+('Left' if sign<0 else 'Right'),(x,WHEEL_Y,WHEEL_Z-.015),(x,-.45,.69),.027,3,'one fixed inclined wheel fork rooted in the body and intersecting its axle with finite interior engagement');FORKS.append(name)
 link(name,AXLE,(x,WHEEL_Y,WHEEL_Z),axis=(1,0,0),spread=.008);link(FUSELAGE,name,(x,-.46,.665),axis=(0,0,1),spread=.008)
SKID=rod('TailSkid_InclinedStrut',(0,3.17,.685),(0,3.43,.045),.035,3,'fixed closed inclined tail-skid strut linking the tail boom to the grounded shoe');link(FUSELAGE,SKID,(0,3.175,.67),axis=(0,0,1),spread=.006)
SHOE=box('TailSkid_FiniteGroundShoe',(0,3.43,.035),(.13,.38,.07),3,'finite planar tail-skid shoe, entire bottom rests on Z=0 without a ground-stability claim');FEET.append(SHOE);link(SKID,SHOE,(0,3.425,.058),axis=(1,0,0),spread=.008)
# Declared finite empty volumes are whole closed boxes, not isolated clear rays.
for side,sign in [('Left',-1),('Right',1)]:
 lo,hi=sorted([sign*.78,sign*6.20]);void('AirUnderLongWing_'+side,(lo,-.30,.15),(hi,.08,.83),'finite under-wing external air, full volume unobstructed in this fixed pose')
 lo,hi=sorted([sign*.22,sign*1.28]);void('AirBelowTTail_'+side,(lo,3.24,1.05),(hi,3.56,1.96),'finite space below the high T-tail and beside its supporting fin')
void('AirBetweenWheelAndBody',(-.060,-.63,.455),(.060,-.47,.565),'actual finite vertical clearance between central wheel crown and fuselage')
void('ClearAirAheadOfNose',(-.24,-3.85,.50),(.24,-3.46,1.20),'closed empty space ahead of uninterrupted unpowered nose; no propeller or tow fixture')
SAILPLANE_CONTRACT={'single_prop_count':1,'fuselage':FUSELAGE,'wings':WINGS,'fin':FIN,'horizontal_tail':TAIL,'wheel':WHEEL,'axle':AXLE,'forks':FORKS,'tail_skid':SKID,'ground_meshes':FEET,'closed_continuous_nose':True,'fixed_opaque_canopy_same_surface':True,'static_pose_only':True,'flight_aerodynamics_control_stability_or_safety_claim':False}
def measure_sailplane_geometry(vertices):
 assert set(vertices)==set(G),'Changed actual component set'
 # Whole surface vertices: every station, root and local tip is constrained.
 # This supplements independent all-triangle contact and clearance tests.
 rows=[]
 for name,g in G.items():
  vv=vertices[name];want=g['vertices'];assert len(vv)==len(want),(name,'changed vertices')
  maxdev=max(math.dist(p,q) for p,q in zip(vv,want));assert maxdev<1.5e-6,(name,'actual surface changed',maxdev)
  rows.append({'mesh':name,'actual_vertex_count':len(vv),'maximum_original_station_vertex_deviation_m':maxdev})
 for name in FEET:assert abs(min(float(p[2]) for p in vertices[name]))<1e-7,('Actual support lifted',name)
 allv=[p for v in vertices.values() for p in v];lo=[min(float(v[k]) for v in allv) for k in range(3)];hi=[max(float(v[k]) for v in allv) for k in range(3)]
 span=max(p[0] for n in WINGS for p in vertices[n])-min(p[0] for n in WINGS for p in vertices[n]);length=max(p[1] for p in vertices[FUSELAGE])-min(p[1] for p in vertices[FUSELAGE]);assert span>2*length and span>14
 wing_profiles=[]
 for name in WINGS:
  vv=vertices[name];profile=[]
  for k in range(len(WING_STATIONS)):
   ring=vv[k*len(FOIL):(k+1)*len(FOIL)];profile.append({'span_station_x_m':sum(float(p[0]) for p in ring)/len(ring),'chord_m':max(float(p[1]) for p in ring)-min(float(p[1]) for p in ring),'thickness_m':max(float(p[2]) for p in ring)-min(float(p[2]) for p in ring)})
  assert all(profile[i]['chord_m']>profile[i+1]['chord_m'] and profile[i]['thickness_m']>profile[i+1]['thickness_m'] for i in range(len(profile)-1))
  assert profile[0]['chord_m']/profile[-1]['chord_m']>5 and profile[-1]['thickness_m']>.04
  wing_profiles.append({'mesh':name,'actual_complete_section_profiles':profile})
 body_profile=[]
 for k in range(len(BODY_STATIONS)):
  ring=vertices[FUSELAGE][k*N_BODY:(k+1)*N_BODY];body_profile.append({'station_y_m':sum(float(p[1]) for p in ring)/len(ring),'actual_width_m':max(float(p[0]) for p in ring)-min(float(p[0]) for p in ring),'actual_height_m':max(float(p[2]) for p in ring)-min(float(p[2]) for p in ring)})
 assert body_profile[5]['actual_width_m']>4*body_profile[-2]['actual_width_m']
 tail_min_z=min(float(p[2]) for p in vertices[TAIL]);body_max_z=max(float(p[2]) for p in vertices[FUSELAGE]);assert tail_min_z-body_max_z>.6
 return dict(SAILPLANE_CONTRACT,actual_full_vertex_checks=rows,actual_wing_sections=wing_profiles,actual_fuselage_sections=body_profile,actual_t_tail_above_fuselage_m=tail_min_z-body_max_z,actual_span_m=span,actual_fuselage_length_m=length,actual_bounds_min_m=lo,actual_bounds_max_m=hi,finite_ground_contact_not_stability=True)
FOCUS=(0,.14,1.02);ORTHO=17.6
CAMERAS={'gray-front3q':(10,-19,15),'gray-back3q':(-10,19,15),'thumbnail':(10,-19,15),'qa-front':(0,-26,11),'qa-side':(26,.14,6),'qa-top':(0,.14,26),'qa-back':(0,26,11),'qa-wireframe':(10,-19,15),'silhouette-128-front':(0,-26,11),'silhouette-128-side':(26,.14,6)}
CAMERA_SCALES={'qa-side':9.0,'silhouette-128-side':9.0};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneLongWingSailplane',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground origin X=Y=Z=0, nose/front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
void_volume_checks=[];probe_inside_selftests=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 actual_triangles[id(pt)]=[[tuple(float(c) for c in pv[i]) for i in (face[0],face[j],face[j+1])] for face in probe['faces'] for j in range(1,len(face)-1)]
 center=tuple(sum(float(v[k]) for v in pv)/len(pv) for k in range(3));outside=(max(float(v[0]) for v in pv)+.05,center[1],center[2])
 assert inside(pt,center) is True and inside(pt,outside) is False,('Actual probe inside/outside control failed',name)
 probe_inside_selftests.append({'probe':name,'actual_center_m':center,'actual_outside_point_m':outside,'center_inside':True,'outside_is_outside':True})
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
sailplane_evidence=dict(measure_sailplane_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts}),finite_external_air_volume_checks=void_volume_checks,actual_probe_inside_outside_selftests=probe_inside_selftests,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'sailplane_geometry':sailplane_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/aviation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'aviation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-12,-16,22),6500,12),('Fill',(16,-3,16),3800,10),('Rim',(2,16,20),5000,10)]:
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
