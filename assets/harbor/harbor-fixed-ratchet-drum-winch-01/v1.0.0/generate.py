"""Original freestanding ratchet drum winch; one fixed static visual prop.
Metres, native Z up, front -Y. No operation, load, brake or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-ratchet-drum-winch-01';VERSION='1.0.0';TITLE='Fixed Ratchet Drum Winch'
DESCRIPTION=('One original low-poly freestanding ratchet drum winch counted as one complete static visual prop. Four broad ground feet and two base rails support two thick tapered side pedestals with genuine polygonal through-bores. A continuous horizontal shaft rests by finite lower facets in both bores. One bare stepped drum has two integral flanges and a complete empty winding bay. One continuous twelve-tooth asymmetric ratchet wheel meets one separate thick fixed pawl at exactly one finite opposed stop face. The pawl has its own grounded root pedestal and embedded axial pin. An independent offset crank and short axial handgrip complete the single frozen pose. Sixteen named editable closed meshes, five opaque constant PBR materials; metres, native Z up, front -Y, horizontally bounds-centred ground origin. No rope, cargo, boat, dock, motor, labels, texture or animation. Static visual geometry only: no winching, hauling, rotation, reverse prevention, braking, locking, continuous engagement, transmission ratio, torque, load, stability, anti-tip, manufacture, installation fit, marine or equipment safety claim. No compatibility with historical harbor, reel or well assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];RAILS=[];SEATS={};BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={}
PALETTE=[('Frame_DeepHarborTeal',(.035,.17,.185,1),.47,.45),('Drum_MutedCoral',(.45,.12,.065,1),.45,.55),('Shaft_SatinSteel',(.43,.50,.53,1),.31,.78),('Ratchet_WarmBrass',(.59,.36,.10,1),.38,.70),('Grip_Graphite',(.035,.043,.046,1),.78,.03)]
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
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
U=(0,1,0);V=(0,0,1);D=(1,0,0)
def axial(o,y,z,x):return add(o,(x,y,z))
def poly(r,n=8,phase=math.pi/8):return[(r*math.cos(math.tau*i/n+phase),r*math.sin(math.tau*i/n+phase)) for i in range(n)]
def prism_data(p,o,lo,hi):
 n=len(p);vs=[axial(o,y,z,x) for x in[lo,hi] for y,z in p];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return vs,fs

def annulus_data(outer,inner,o,lo,hi):
 n=len(outer);assert n==len(inner);vs=[axial(o,y,z,x) for p,x in[(outer,lo),(outer,hi),(inner,lo),(inner,hi)] for y,z in p];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return vs,fs

def lathe(profile,o,n=32,phase=0):
 vs=[];rings=[];fs=[]
 for r,x in profile:
  rr=[]
  for j in range(n if r else 1):
   a=math.tau*j/n+phase;rr.append(len(vs));vs.append(axial(o,r*math.cos(a),r*math.sin(a),x))
  rings.append(rr)
 for a,b in list(zip(rings,rings[1:]))+[(rings[-1],rings[0])]:
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n;fs.extend([(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])])
 return vs,fs

def void(name,vs,fs,targets,role,isolated=False):
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]={'vertices':vs,'faces':fs,'targets':targets,'role':role}
def void_box(name,lo,hi,role):void(name,cuboid(lo,hi),BOX_FACES,[],role)
def inward_polygon(p,d):
 # Exact intersections of the inward-offset boundary lines. The connected U
 # profile includes all available bore air, with a uniform boundary inset.
 out=[]
 for i,b in enumerate(p):
  a=p[i-1];c=p[(i+1)%len(p)];e=(b[0]-a[0],b[1]-a[1]);f=(c[0]-b[0],c[1]-b[1]);el=math.hypot(*e);fl=math.hypot(*f)
  n=(-e[1]/el,e[0]/el);m=(-f[1]/fl,f[0]/fl);q=(b[0]+d*n[0],b[1]+d*n[1]);r=(b[0]+d*m[0],b[1]+d*m[1]);den=e[0]*f[1]-e[1]*f[0]
  if abs(den)<1e-14:out.append(q);continue
  t=((r[0]-q[0])*f[1]-(r[1]-q[1])*f[0])/den;out.append((q[0]+t*e[0],q[1]+t*e[1]))
 return out
for label,y in [('Front',-.35),('Back',.35)]:
 rail=box('Base_'+label+'Rail',(0,y,.0775),(1.18,.09,.095),0,'independent continuous base rail with finite joints to two feet and both thick side pedestals');RAILS.append(rail)
 for side,x in [('Left',-.55),('Right',.55)]:
  foot=box('Base_'+label+side+'Foot',(x,y,.0175),(.24,.22,.035),4,'thick rectangular ground foot with a complete finite sole');FEET.append(foot);link(rail,foot,(x,y,.0325),spread=.03)
HOLE_R=.055;SHAFT_R=.039;HOLE_Z=.63;SEAT_Z=round(HOLE_Z-HOLE_R*math.cos(math.pi/8),8);AXLE_Z=round(SEAT_Z+SHAFT_R*math.cos(math.pi/8),8);ORIGIN=(0,0,AXLE_Z)
shaft='Axle_ContinuousOctagonalShaft';v,f=prism_data(poly(SHAFT_R),ORIGIN,-.57,.59);mesh(shaft,v,f,2,'one continuous solid horizontal octagonal shaft with finite flat lower bearing facets; fixed static pose')
for side,x in [('Left',-.39),('Right',.39)]:
 name='Frame_'+side+'TrueBoredPedestal';o=(x,0,HOLE_Z);outer=[(.14,0),(.105,.14),(0,.16),(-.105,.14),(-.14,0),(-.36,-.54),(0,-.54),(.36,-.54)]
 v,f=annulus_data(outer,poly(HOLE_R),o,-.04,.04);mesh(name,v,f,0,'one thick tapered side pedestal with a real complete octagonal axial through-hole; no solid cap or false bearing insert')
 for rail,y in zip(RAILS,[-.35,.35]):link(name,rail,(x,y,.105),axis=(1,0,0),spread=.022)
 CONTACTS.append({'a':name,'b':shaft,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':SEAT_Z,'minimum_patch_area_m2':.0022,'interior_probe_offset_m':.0003,'points':[(x+d,0,SEAT_Z) for d in[-.025,0,.025]],'scope':'complete finite lower true-bore facet opposed to complete shaft lower facet; no penetration'})
 SEATS[name]={'shaft':shaft,'origin_m':o,'x_center_m':x,'bore_radius_m':HOLE_R,'bore_polygon_vertices':8,'inner_wall_face_indices':[4*i+1 for i in range(8)],'bottom_wall_face_indices':[21],'lo_m':x-.04,'hi_m':x+.04}
 v,f=prism_data(inward_polygon(poly(HOLE_R),.0007),o,-.041,.041);void(name+'_FullIsolatedBore',v,f,[name],'entire closed finite true bore, uniform 0.7 mm wall inset, extending past both mouths',True)
 # Hole minus lower-seated shaft is one connected U-shaped polygon. Preserve
 # its entire upper and side air, rather than testing a handful of empty rays.
 hp=poly(HOLE_R);sp=[(a,b+AXLE_Z-HOLE_Z) for a,b in poly(SHAFT_R)]
 air=[hp[i] for i in[6,7,0,1,2,3,4,5]]+[sp[i] for i in[5,4,3,2,1,0,7,6]]
 v,f=prism_data(inward_polygon(air,.0007),o,-.041,.041);void(name+'_CompleteAssembledBoreAir',v,f,[],'entire connected U-shaped bore-minus-shaft air, uniformly eroded 0.7 mm from every actual boundary; finite bearing facet excluded by exact topology')
 BORES.append({'mesh':name,'origin_m':(x-.041,0,HOLE_Z),'direction':D,'length_m':.082})
# One integral bare drum. The stepped lathe has two flanges, not piled disks.
v,f=lathe([(0,-.31),(.255,-.31),(.28,-.295),(.28,-.275),(.255,-.26),(.18,-.26),(.18,.26),(.255,.26),(.28,.275),(.28,.295),(.255,.31),(0,.31)],ORIGIN)
drum=mesh('Drum_IntegralBareDoubleFlange',v,f,1,'one continuous bare drum with two integral bevel-edged flanges, open empty winding bay and no rope');link(shaft,drum,(0,0,AXLE_Z),spread=.18)
v,f=lathe([(.181,-.258),(.253,-.258),(.253,.258),(.181,.258)],ORIGIN);void('Drum_CompleteEmptyWindingBay',v,f,[],'entire finite empty polygonal annular winding bay across the full bare barrel, inset from barrel and inner flange shoulders')
# Twelve truly asymmetric sawteeth. Each stop rises radially at a single angle;
# the next long ramp spans 30 degrees. No copied symmetrical spur-gear outline.
TEETH=12;ROOT_R=.195;TIP_R=.255;ratchet_profile=[]
for i in range(TEETH):
 a=math.tau*i/TEETH
 for r in[ROOT_R,TIP_R]:ratchet_profile.append((r*math.cos(a),r*math.sin(a)))
# Explicit convex-root cap plus twelve tooth triangles avoids ambiguous
# triangulation of a single highly concave 24-vertex cap.
v=[axial(ORIGIN,y,z,x) for x in[.49,.535] for y,z in ratchet_profile];n=len(ratchet_profile)
f=[tuple(reversed(range(0,n,2))),tuple(n+i for i in range(0,n,2))]
for i in range(TEETH):
 a=2*i;b=a+1;c=(a+2)%n;f.extend([(c,b,a),(n+a,n+b,n+c)])
RATCHET_STOP_FACE_INDEX=len(f)
for i in range(n):j=(i+1)%n;f.append((i,j,n+j,n+i))
wheel=mesh('Ratchet_ContinuousAsymmetric12ToothWheel',v,f,3,'one continuous closed original twelve-tooth asymmetric ratchet wheel; radial stop faces and long sloping ramps');link(shaft,wheel,(.513,0,AXLE_Z),axis=(0,1,0),spread=.015)
# Only the horizontal end face touches the zero-angle radial stop face.
pawl_profile=[(.214,AXLE_Z),(.246,AXLE_Z),(.445,.48),(.45,.425),(.39,.412),(.225,AXLE_Z-.030)]
v,f=prism_data(pawl_profile,(0,0,0),.4985,.5265);pawl=mesh('Pawl_FixedThickStopArm',v,f,3,'separate thick fixed pawl; one finite upper end face contacts exactly one radial tooth stop, while all other wheel surfaces remain clear')
CONTACTS.append({'a':pawl,'b':wheel,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':AXLE_Z,'minimum_patch_area_m2':.00085,'interior_probe_offset_m':.0003,'points':[(x,.230,AXLE_Z) for x in[.504,.5125,.521]],'scope':'one and only one complete finite opposed pawl-end/radial-tooth-stop contact; frozen pose, not a locking or movement claim'})
root=box('Pawl_IndependentRootPedestal',(.5125,.42,.285),(.09,.08,.39),0,'separate grounded root support of the fixed pawl, positively embedded in the back base rail and pawl root');link(root,RAILS[1],(.5125,.39,.105),axis=(1,0,0),spread=.02);link(root,pawl,(.5125,.42,.45),axis=(0,0,1),spread=.008)
v,f=lathe([(0,.455),(.026,.455),(.026,.57),(0,.57)],(0,.42,.45),n=16,phase=math.pi/16);pin=mesh('Pawl_FixedAxialRootPin',v,f,2,'real solid axial pin embedded through the distinct pawl root and its supporting pedestal; fixed, not a rotating joint');link(root,pin,(.49,.42,.45),axis=(0,0,1),spread=.01);link(pawl,pin,(.5125,.42,.45),axis=(0,0,1),spread=.01)
crank=box('Crank_OffsetFlatArm',(-.5225,0,AXLE_Z+.1325),(.035,.05,.315),2,'independent eccentric crank arm, finitely joined to horizontal shaft and axial handgrip');link(shaft,crank,(-.5225,0,AXLE_Z),axis=(0,1,0),spread=.012)
v,f=lathe([(0,-.65),(.032,-.65),(.032,-.508),(0,-.508)],(0,0,AXLE_Z+.275),n=16,phase=math.pi/16);grip=mesh('Crank_AxialGraphiteHandgrip',v,f,4,'short solid axial grip finitely embedded in the outer crank end; complete static hand-crank silhouette');link(crank,grip,(-.5225,0,AXLE_Z+.275),axis=(0,1,0),spread=.010)
# Every complete intertooth pocket is a closed finite triangular prism,
# bounded by the actual long ramp, next stop and tip chord. Only the engaged
# pocket deliberately contains the fixed pawl; that isolated check excludes it.
for i in range(TEETH):
 a=math.tau*i/TEETH;b=math.tau*(i+1)/TEETH
 pocket=[(TIP_R*math.cos(a),TIP_R*math.sin(a)),(TIP_R*math.cos(b),TIP_R*math.sin(b)),(ROOT_R*math.cos(b),ROOT_R*math.sin(b))]
 v,f=prism_data(inward_polygon(pocket,.001),ORIGIN,.491,.534)
 targets=[k for k in G if k!=pawl] if i==TEETH-1 else list(G)
 void('Ratchet_FullToothPocket%02d'%(i+1),v,f,targets,'entire finite intertooth ramp-to-next-stop pocket; 1 mm boundary inset; '+('engaged pocket isolated from its intentionally inserted pawl' if i==TEETH-1 else 'complete assembled pocket remains empty'))
void_box('Drum_LeftFullSideGap',(-.348,-.282,AXLE_Z-.282),(-.312,.282,AXLE_Z+.282),'complete finite slab between drum left flange and left side pedestal, excluding only the separately seated through-shaft')
void_box('Drum_RightFullSideGap',(.312,-.282,AXLE_Z-.282),(.348,.282,AXLE_Z+.282),'complete finite slab between drum right flange and right side pedestal, excluding only the separately seated through-shaft')
# Side slabs are checked against the full frame, drum and fittings. Their central
# axial passage is occupied by the real shaft and therefore is not called empty.
for n in ['Drum_LeftFullSideGap','Drum_RightFullSideGap']:VOID_VOLUMES[n]['targets']=[k for k in G if k!=shaft]
void_box('Frame_CompleteUnderDrumOpening',(-.345,-.295,.127),(.345,.295,AXLE_Z-.282),'complete finite central under-drum opening above the two base rails and between independent side pedestals')
for g in VOID_VOLUMES.values():
 if not g['targets']:g['targets']=list(G)
WINCH_CONTRACT={'single_prop_count':1,'true_bored_side_pedestals':2,'continuous_horizontal_shafts':1,'integral_bare_double_flange_drums':1,'asymmetric_sawteeth':TEETH,'separate_fixed_pawls':1,'fixed_pawl_root_pedestals':1,'real_fixed_pawl_axial_pins':1,'finite_shaft_lower_seats':2,'finite_pawl_stop_contacts':1,'ground_feet':4,'independent_base_rails':2,'nonbearing_full_bore_wall_clearance_required':True,'no_motion_locking_braking_or_load_claim':True}
def measure_winch_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 vv=vertices[wheel];n=TEETH*2
 # Actual exported stop edges are radial and the distinct ramp joins the next root.
 for i in range(TEETH):
  a,b,c=[vv[j] for j in[2*i,2*i+1,(2*i+2)%n]];ra=math.hypot(a[1],a[2]-AXLE_Z);rb=math.hypot(b[1],b[2]-AXLE_Z)
  assert abs(ra-ROOT_R)<2e-7 and abs(rb-TIP_R)<2e-7 and abs(a[1]*(b[2]-AXLE_Z)-(a[2]-AXLE_Z)*b[1])<2e-7
  assert math.dist(b,c)>math.dist(a,b)*1.8
 return dict(WINCH_CONTRACT,geometry_scope='actual coordinates; finite full faces, closed complete air volumes, full nonbearing distances and actual mutations are separate mandatory gates')
FOCUS=(0,0,.46);ORTHO=1.91
CAMERAS={'gray-front3q':(3.6,-4.8,3.4),'gray-back3q':(-3.6,4.8,3.4),'thumbnail':(3.6,-4.8,3.4),'qa-front':(0,-4.8,2.7),'qa-side':(4.8,0,2.7),'qa-top':(0,0,4.5),'qa-back':(0,4.8,2.7),'qa-wireframe':(3.6,-4.8,3.4),'silhouette-128-front':(0,-4.8,2.7),'silhouette-128-side':(4.8,0,2.7)}
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
root=bpy.data.objects.new('OneFixedRatchetDrumWinch',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.55,-.35,.0175),(-.55,-.35,.06)),('Frame_RightTrueBoredPedestal',(.39,.10,HOLE_Z),(.39,0,HOLE_Z))]:
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
mount_evidence=measure_winch_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'winch_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/harbor/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
