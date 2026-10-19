"""Original open twin battery-box exterior kit. One static visual prop.
Metres, native Z up, front -Y. No electrical, chemical, moving or safety function.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='renewable-open-twin-battery-box-kit-01';VERSION='1.0.0';TITLE='Open Twin Battery-Box Exterior Kit'
DESCRIPTION=('One original low thick twin-compartment battery-box exterior kit, counted as one static visual prop. A connected closed material shell contains a complete 45 mm bottom, four thick walls, an integral central divider and two real elevated through-handholds. Two closed battery-shaped exteriors have complete flat bottoms finitely seated in the separate deep bays, with real positive clearance around each body, stepped wide shoulders, raised top covers and two thick fixed posts each. These are disconnected decorative battery exteriors without chemistry, polarity or voltage labels, cables or external wiring. A thick hard lid is fixed upright at 90 degrees, joined by two three-knuckle through-bored hinge assemblies and continuous square pins; side and upper bore clearance is real and each pin has a finite lower bearing face. Two separate finite angle-stop blocks connect the box rear to the lid lower face. Every mesh has a finite contact path to the full box bottom. Original battery bodies, deep-bay proportions and whole support arrangement, not a resized bait box, solid off-grid cabinet, inverter cabinet, camera bag or repainted general case. Opaque constant PBR colors, no textures, logos, photovoltaic panel, whole station or environment. No electrical circuit, power, capacity, charge/discharge, connection, chemical, insulation, thermal, fire, explosion, transport, battery-standard, sealing, waterproofing, impact, moving hinge, lid-closing path, load, stability, human fit, manufacture, installation, compatibility or safety certification claim.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};ROOT_INTERIOR_PROBES=[];BATTERIES=[];POSTS=[];HINGES=[];STOPS=[]
PALETTE=[('Shell_MutedSage',(.20,.31,.27,1),.65,.08),('Battery_DeepGraphite',(.055,.075,.080,1),.72,.10),('Cap_WarmOchre',(.71,.44,.12,1),.60,.06),('Hardware_DullAlloy',(.37,.42,.43,1),.47,.55),('Lid_InsidePaleSage',(.39,.48,.40,1),.70,.04)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role,tags=None):
 assert name not in G
 g={'vertices':[tuple(round(float(c),9) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 vol=sum(dot(g['vertices'][f[0]],cross(g['vertices'][f[i]],g['vertices'][f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if vol<0:g['faces']=[tuple(reversed(f)) for f in fs]
 if tags:g['face_tags']=tags
 G[name]=g;return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def voidbox(name,lo,hi,role,targets=None,isolated=False):
 (ISOLATED_VOID_VOLUMES if isolated else VOID_VOLUMES)[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'targets':targets,'role':role}
def contact(a,b,axis,point,area,scope,points=None):
 axis=unit(axis);ref=(0,1,0) if abs(axis[0])>.9 else (1,0,0);u=unit(sub(ref,mul(axis,dot(ref,axis))));v=cross(axis,u)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':points or [point],'scope':scope})
def grid_solid(xs,ys,zs,occupied):
 # Boundary of an exact Cartesian material union. Shared cell faces are removed,
 # all coincident vertices welded; the shell includes the handle-hole boundaries.
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 vv=[];ff=[];ids={}
 def face(coords):
  ids2=[]
  for p in coords:
   if p not in ids:ids[p]=len(vv);vv.append(p)
   ids2.append(ids[p])
  ff.append(tuple(ids2))
 for i,j,k in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
  for delta,q in[((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]:
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:face(q)
 return vv,ff

def shell_geometry(detach_divider_root=False):
 xs=[-.42,-.385,-.0125,.0125,.385,.42];ys=[-.23,-.195,-.11,.11,.195,.23];zs=[0,.045,.075,.24,.275,.30]
 def occupied(x,y,z):
  if z<.045:return True
  if abs(y)>.195:return True
  if abs(x)>.385:return not(abs(y)<.11 and .24<z<.275)
  if abs(x)<.0125:return not(detach_divider_root and z<.075)
  return False
 return grid_solid(xs,ys,zs,occupied)
SHELL=mesh('TwinBay_ContinuousBottomWallsDivider',*shell_geometry(),0,'one continuous closed thick material shell with full bottom, two deep open bays, central rooted divider and two full elevated side handholes');FEET.append(SHELL)
FLOOR_MATERIAL_PROBE={'name':'CompleteBottomMaterialSlab','lo_m':[-.419,-.229,.001],'hi_m':[.419,.229,.044],'target':SHELL,'role':'whole finite full-thickness base region, 1 mm inside every outer boundary'}
ROOT_INTERIOR_PROBES.append({'name':'CompleteCentralDividerRootBridge','lo_m':[-.0065,-.190,.034],'hi_m':[.0065,.190,.060],'target':SHELL,'role':'finite complete useful-length root bridge inside the integral base and central divider, not isolated point samples'})
for side in[-1,1]:
 lo,hi=(.384,.421) if side>0 else(-.421,-.384)
 voidbox(('Right' if side>0 else 'Left')+'CompleteHandhold',(lo,-.109,.241),(hi,.109,.274),'entire rectangular side handhold through both wall mouths, 1 mm inset around aperture')

# The complete solid battery body and stepped shoulder are one closed original mesh.
def battery_geometry(cx):
 rings=[(.145,.145,.045),(.145,.145,.325),(.160,.160,.325),(.160,.160,.350),(.128,.145,.375),(.128,.145,.390)]
 vs=[(cx+x,y,z) for hx,hy,z in rings for x,y in[(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]];fs=[(3,2,1,0)];fm=[1]
 for k in range(len(rings)-1):
  for i in range(4):fs.append((4*k+i,4*k+(i+1)%4,4*(k+1)+(i+1)%4,4*(k+1)+i));fm.append(1 if k==0 else 2)
 fs.append(tuple(4*(len(rings)-1)+i for i in range(4)));fm.append(2)
 return vs,fs,fm
for i,cx in enumerate([-.19875,.19875]):
 vs,fs,fm=battery_geometry(cx);n=mesh('Battery_%d_ClosedSteppedShoulder'%i,vs,fs,1,'one complete closed battery exterior with full planar bottom, wide shoulder and tapered raised top; no chemistry or electrical internals');G[n]['face_materials']=fm;BATTERIES.append(n)
 contact(SHELL,n,(0,0,1),(cx,0,.045),.29*.29-.00000001,'entire 290 x 290 mm battery bottom seated on its own full bay floor',points=[(cx+x,y,.045) for x,y in[(-.09,-.09),(.09,-.09),(.09,.09),(-.09,.09),(0,0)]])
 for j,y in enumerate([-.085,.085]):
  poly=[(.022*math.cos(math.tau*k/12),.022*math.sin(math.tau*k/12)) for k in range(12)];vv=[(cx+x,y+yy,z) for z in[.390,.425] for x,yy in poly];ff=[tuple(reversed(range(12))),tuple(range(12,24))]+[(k,(k+1)%12,(k+1)%12+12,k+12) for k in range(12)]
  post=mesh('Battery_%d_FixedPost_%d'%(i,j),vv,ff,3,'one thick fixed 12-sided appearance post with a complete planar bottom on the closed top cover');POSTS.append(post)
  contact(n,post,(0,0,1),(cx,y,.390),.0014519,'entire twelve-sided post bottom on closed battery top')
 # Four complete disjoint strips partition all nominal bay air outside the body.
 x0,x1=(-.385,-.0125) if i==0 else(.0125,.385);bx0,bx1=cx-.145,cx+.145
 for label,lo,hi in [('OuterLeft',(x0,-.195,.045),(bx0,.195,.301)),('OuterRight',(bx1,-.195,.045),(x1,.195,.301)),('Front',(bx0,-.195,.045),(bx1,-.145,.301)),('Back',(bx0,.145,.045),(bx1,.195,.301))]:
  voidbox('Bay_%d_CompleteRemainingAir_%s'%(i,label),tuple(v+.001 for v in lo),tuple(v-.001 for v in hi),'complete remaining bay-air partition cell with explicit 1 mm boundary inset; battery body is the intended sole bay occupant')

# Fixed upright 90 degree lid. Its inside face is a solid lighter-colored face.
LID=box('Lid_FixedUprightThickPanel',(0,.310,.5575),(.84,.028,.465),0,'one complete thick upright lid fixed at 90 degrees, supported at two lower patches and joined to two real bored hinge assemblies')
G[LID]['face_materials']=[0,0,4,0,0,0]
for i,cx in enumerate([-.36,.36]):
 n=box('FiniteAngleStop_%d'%i,(cx,.277,.300),(.050,.094,.050),3,'finite fixed 90-degree stop block from box rear wall to lid lower edge; no motion path claimed');STOPS.append(n)
 contact(SHELL,n,(0,1,0),(cx,.23,.2875),.05*.025-.00000001,'complete 50 x 25 mm stop-root patch on rear wall')
 contact(n,LID,(0,0,1),(cx,.310,.325),.05*.028-.00000001,'complete finite lid-bottom patch on fixed angle stop')

def bored_knuckle_geometry(x0,x1):
 # One watertight extrusion of a thick rectangular annulus with a true through hole.
 outer=[(.239,.305),(.289,.305),(.289,.355),(.239,.355)];inner=[(.251,.317),(.277,.317),(.277,.343),(.251,.343)]
 vs=[(x,y,z) for x,poly in[(x0,outer),(x1,outer),(x0,inner),(x1,inner)] for y,z in poly];fs=[]
 for i in range(4):
  j=(i+1)%4;fs.extend([(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)])
 return vs,fs
for j,cx in enumerate([-.25,.25]):
 rings=[];brackets=[]
 for label,a,b in[('Left',cx-.043,cx-.023),('Center',cx-.017,cx+.017),('Right',cx+.023,cx+.043)]:
  ring=mesh('Hinge_%d_%sTrueBoredKnuckle'%(j,label),*bored_knuckle_geometry(a,b),3,'closed thick annular knuckle with complete coaxial rectangular through-bore');rings.append(ring)
  voidbox('Hinge_%d_%sWholeIsolatedBore'%(j,label),(a-.001,.252,.318),(b+.001,.276,.342),'complete isolated finite through-hole extending past both mouths, tested against this knuckle only',[ring],True)
  # Bottom pin face and complete lower bore face are opposed over the pin width.
  contact(ring,'Hinge_%d_ContinuousFixedPin'%j,(0,0,1),((a+b)/2,.264,.317),(b-a)*.020-.000000001,'entire flat lower pin-bearing face within this true bore')
  if label!='Center':
   bracket=box('Hinge_%d_%sBodyBracket'%(j,label),((a+b)/2,.2345,.3025),(b-a,.009,.035),0,'complete short connector between rear wall and the knuckle outer front face');brackets.append(bracket)
   # Bracket bridges the rear rim with distinct finite root and knuckle patches.
   contact(SHELL,bracket,(0,1,0),((a+b)/2,.23,.2925),(b-a)*.015-.000000001,'whole bracket-root overlap on rear wall below rim')
   contact(bracket,ring,(0,1,0),((a+b)/2,.239,.3125),(b-a)*.015-.000000001,'whole bracket end patch on lower front of thick knuckle')
  else:
   tongue=box('Hinge_%d_LidTongue'%j,(cx,.2925,.350),(.034,.007,.010),0,'finite full-end tongue from center knuckle rear face to fixed lid front')
   contact(ring,tongue,(0,1,0),(cx,.289,.350),.034*.010-.000000001,'complete tongue end on center knuckle rear outer surface')
   contact(tongue,LID,(0,1,0),(cx,.296,.350),.034*.010-.000000001,'complete tongue end on upright lid inside face')
 pin=box('Hinge_%d_ContinuousFixedPin'%j,(cx,.264,.327),(.100,.020,.020),3,'one continuous solid fixed square pin through all three coaxial holes, complete bottom seating and positive side/top clearance')
 caps=[]
 for sign in[-1,1]:
  cap=box('Hinge_%d_PinEnd_%s'%(j,'L' if sign<0 else 'R'),(cx+sign*.055,.264,.327),(.010,.028,.028),3,'fixed square pin end plate, finite attachment to full pin end, clear of knuckle side');caps.append(cap)
  if sign<0:contact(cap,pin,(1,0,0),(cx-.050,.264,.327),.000399999,'complete pin left end to end plate')
  else:contact(pin,cap,(1,0,0),(cx+.050,.264,.327),.000399999,'complete pin right end to end plate')
 for label,lo,hi in [('LeftSide',(cx-.049,.251,.317),(cx+.049,.254,.343)),('RightSide',(cx-.049,.274,.317),(cx+.049,.277,.343)),('AbovePin',(cx-.049,.254,.337),(cx+.049,.274,.343))]:
  voidbox('Hinge_%d_CompleteAssembledBoreAir_%s'%(j,label),tuple(v+.0006 for v in lo),tuple(v-.0006 for v in hi),'entire continuous assembled coaxial-bore residual air strip through all three knuckles and both axial gaps; 0.6 mm boundary inset')
 HINGES.append({'knuckles':rings,'body_brackets':brackets,'lid_tongue':tongue,'pin':pin,'pin_end_plates':caps,'coaxial_bore_y_m':[.251,.277],'coaxial_bore_z_m':[.317,.343],'pin_y_m':[.254,.274],'pin_z_m':[.317,.337],'side_clearance_m':.003,'top_clearance_m':.006,'inter_knuckle_axial_clearance_m':.006})
# Entire useful space in front of the upright inner lid above every battery post.
voidbox('WholeRaisedLidFrontAir',(-.419,-.229,.426),(.419,.295,.789),'complete finite open space in front of the raised inner lid above the battery posts, to the front outer footprint and below lid upper edge')
for row in list(VOID_VOLUMES.values())+list(ISOLATED_VOID_VOLUMES.values()):
 if row['targets'] is None:row['targets']=list(G)
BATTERYBOX_CONTRACT={'single_prop_count':1,'continuous_twin_bay_shell':1,'complete_battery_exteriors':2,'fixed_posts':4,'side_handholes':2,'fixed_upright_lid':1,'fixed_lid_angle_degrees':90,'coaxial_true_bored_hinges':2,'through_bored_knuckles':6,'continuous_solid_pins':2,'finite_angle_stops':2,'integral_divider_root_bridges':len(ROOT_INTERIOR_PROBES),'whole_empty_volumes':len(VOID_VOLUMES),'isolated_bore_volumes':len(ISOLATED_VOID_VOLUMES),'finite_opposed_contacts':len(CONTACTS),'electrical_or_safety_claim':False}
def measure_batterybox_geometry(vertices):
 assert set(vertices)==set(G),'component set changed'
 assert abs(min(p[2] for p in vertices[SHELL]))<2e-7
 for n in BATTERIES:assert abs(min(p[2] for p in vertices[n])-.045)<2e-7
 assert abs(max(p[2] for p in vertices[LID])-.79)<2e-7
 return dict(BATTERYBOX_CONTRACT,geometry_scope='actual full source/export coordinates; full contact, void, root, separation and real negative gates remain required')
FOCUS=(0,.065,.37);ORTHO=1.32
CAMERAS={'gray-front3q':(1.4,-2.1,1.45),'gray-back3q':(-1.4,2.1,1.45),'thumbnail':(1.4,-2.1,1.45),'qa-front':(0,-2.8,1.18),'qa-side':(2.8,0,1.18),'qa-top':(0,.065,3),'qa-back':(0,2.8,1.18),'qa-wireframe':(1.4,-2.1,1.45),'silhouette-128-front':(0,-2.8,1.18),'silhouette-128-side':(2.8,0,1.18)}
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
root=bpy.data.objects.new('OneOpenTwinBatteryBoxKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='box footprint centre ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(SHELL,(0,0,.020),(.19875,.17,.15)),(BATTERIES[0],(-.19875,0,.15),(-.19875,.18,.15))]:
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
mount_evidence=measure_batterybox_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'batterybox_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/renewable/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'renewable','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
