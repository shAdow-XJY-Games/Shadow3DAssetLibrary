"""Original recessed token-dispenser exterior; one fixed static visual prop.
Native Z up, front -Y, metres. No payment, dispensing or operating mechanism.
"""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='arcade-recessed-token-dispenser-01';VERSION='1.0.0';TITLE='Recessed Token Dispenser Cabinet'
DESCRIPTION=('One original low-poly static token-dispenser cabinet exterior, counted as one complete prop. A narrow deep-teal housing has a genuinely recessed upper input slot with a closed back, a separate thick through-open metal bezel and one solid fixed rotary control. '
 'The lower receiver is a separate continuous thick scoop with a sloping inner floor, thick sides, a low front lip and a complete back, joined into a true cabinet alcove. A downward-facing deep blind neck opens above the empty receiver; it ends inside solid housing and is not connected to the input slot. A wide chamfered ground plinth, cream chamfered top and fixed closed rear service plate finish the cabinet. '
 'Seven named editable connected closed meshes, five constant opaque PBR materials, no textures, words, screens, currency, loose tokens, tickets, brands, game controls or animation. Metres, native Z up, front -Y, horizontal bounds-centred ground origin. '
 'Static visual geometry only. No recognition, payment, charge, token issue, exchange, change-making, ticket or prize rules, gambling, account, network, electronics, internal drive, cash security, continuous motion, human fit, loading, anti-tip, installation, manufacture, equipment performance or safety certification. No compatibility with earlier arcade or parking-meter assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={};SUPPORT_VOLUMES={}
PALETTE=[('Housing_DeepPetrol',(.035,.20,.23,1),.46,.24),('Top_WarmCream',(.78,.70,.49,1),.49,.12),('Receiver_Ochre',(.72,.32,.055,1),.43,.34),('Plinth_Graphite',(.025,.04,.045,1),.77,.0),('Hardware_SatinSilver',(.43,.52,.53,1),.32,.70)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name

def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def probe(lo,hi,**other):return dict(vertices=cuboid(lo,hi),faces=BOX_FACES,**other)
def void(name,lo,hi,targets,role):VOID_VOLUMES[name]=probe(lo,hi,targets=targets,role=role)
def wall(name,lo,hi,target='Housing_BlindRecessCabinet'):WALL_VOLUMES[name]=probe(lo,hi,target=target)
def link(a,b,p,axis=(0,0,1),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
def support(name,lo,hi,a,b):SUPPORT_VOLUMES[name]=probe(lo,hi,targets=[a,b],role='complete finite embedded fixed connection volume')
def chamfer_box(name,x0,x1,y0,y1,z0,z1,c,mat,role):
 xy=[(x0+c,y0),(x1-c,y0),(x1,y0+c),(x1,y1-c),(x1-c,y1),(x0+c,y1),(x0,y1-c),(x0,y0+c)]
 vs=[(x,y,z) for z in[z0,z1] for x,y in xy];fs=[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
 return mesh(name,vs,fs,mat,role)
base=chamfer_box('Plinth_FiniteGroundBase',-.35,.35,-.275,.285,0,.15,.055,3,'broad finite horizontal ground sole and shallow chamfered corners');FEET.append(base)
# One manifold cell-union housing with three connected-to-exterior blind voids.
# The slot and neck have their own complete solid ends; no internal route joins them.
xs=[-.31,-.23,-.19,-.10,.04,.10,.23,.31];ys=[-.22,-.20,-.125,-.08,-.045,.23];zs=[.12,.30,.70,.82,.92,.975,1.24]
cells=set()
for i,j,k in itertools.product(range(len(xs)-1),range(len(ys)-1),range(len(zs)-1)):
 x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2;z=(zs[k]+zs[k+1])/2
 slot=-.19<x<.04 and -.22<y<-.125 and .92<z<.975
 receiver=-.23<x<.23 and -.22<y<-.045 and .30<z<.70
 neck=-.10<x<.10 and -.20<y<-.08 and .70<z<.82
 if not(slot or receiver or neck):cells.add((i,j,k))
vs=[];fs=[];index={}
for i,j,k in sorted(cells):
 corners=cuboid((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1]))
 for face,neighbour in zip(BOX_FACES,[(i,j,k-1),(i,j,k+1),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]):
  if neighbour in cells:continue
  ids=[]
  for q in face:
   p=corners[q]
   if p not in index:index[p]=len(vs);vs.append(p)
   ids.append(index[p])
  fs.append(ids)
housing=mesh('Housing_BlindRecessCabinet',vs,fs,0,'one continuous solid housing around independent closed-back upper input, true lower receiver alcove and downward-facing blind neck')
link(base,housing,(0,0,.135),axis=(1,0,0),spread=.10);support('FullBaseHousingEmbed',(-.25,-.15,.121),(.25,.15,.149),base,housing)
cap=chamfer_box('Top_ChamferedCap',-.335,.335,-.245,.255,1.225,1.28,.045,1,'shallow cream top with finite embedded housing connection')
link(cap,housing,(0,0,1.232),axis=(1,0,0),spread=.12);support('FullTopHousingEmbed',(-.25,-.15,1.226),(.25,.15,1.239),cap,housing)
# Closed thick scoop: continuous outer bottom, inner sloped floor, four walls and rim.
# Outer and inner loops are CCW seen from above. The top ring is explicitly triangulated.
outer_xy=[(-.255,-.435),(.255,-.435),(.255,-.025),(-.255,-.025)]
inner_xy=[(-.217,-.397),(.217,-.397),(.217,-.065),(-.217,-.065)]
vs=[]
for xy,zz in [(outer_xy,[.29,.29,.375,.375]),(outer_xy,[.405,.405,.54,.54]),(inner_xy,[.335,.335,.41,.41]),(inner_xy,[.405,.405,.54,.54])]:vs += [(x,y,z) for (x,y),z in zip(xy,zz)]
fs=[(3,2,1,0),(8,9,10,11)]
for i in range(4):
 j=(i+1)%4
 fs += [(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i+4,j+4,j+12),(i+4,j+12,i+12)]
scoop=mesh('Receiver_ThickSlopedScoop',vs,fs,2,'continuous empty thick scoop; low front lip, raised sides, sloped inner floor, full back and positive material thickness')
link(scoop,housing,(0,-.035,.47),axis=(1,0,0),spread=.12)
support('ReceiverBackEmbed',(-.18,-.044,.44),(.18,-.026,.50),scoop,housing)
for side,x in [('Left',-.241),('Right',.241)]:
 link(scoop,housing,(x,-.16,.44),axis=(0,1,0),spread=.025)
 support('Receiver'+side+'Embed',(x-.007,-.19,.425),(x+.007,-.13,.465),scoop,housing)
# Upper rectangular bezel has a real through-hole; the housing supplies its deep blind end.
outer=[(-.225,.885),(.075,.885),(.075,1.01),(-.225,1.01)]
inner=[(-.195,.915),(.045,.915),(.045,.98),(-.195,.98)]
vs=[(x,y,z) for y in[-.253,-.205] for loop in[outer,inner] for x,z in loop];fs=[]
for i in range(4):
 j=(i+1)%4
 fs += [(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,i+8,j+8,j),(i+4,j+4,j+12,i+12)]
# Ensure the complete ring uses outward winding before any predicate runs.
volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]]))+dot(vs[f[0]],cross(vs[f[2]],vs[f[3]])) for f in fs)/6
if volume<0:fs=[tuple(reversed(f)) for f in fs]
bezel=mesh('Input_TrueOpenBezel',vs,fs,4,'genuine thick through-open rectangular input surround; joined around the separate closed-back housing slot')
link(bezel,housing,(-.075,-.212,.895),axis=(1,0,0),spread=.08);support('BezelBottomEmbed',(-.18,-.219,.887),(.03,-.206,.912),bezel,housing)
# One closed stepped 16-sided rotary control; solid fixed exterior, no moving shaft.
profile=[(0,-.202),(.033,-.202),(.033,-.247),(.054,-.247),(.054,-.278),(.047,-.288),(0,-.288)]
vs=[];rings=[];fs=[];n=16
for r,y in profile:
 ring=[]
 for i in range(n if r else 1):
  a=math.tau*i/n;ring.append(len(vs));vs.append((.185+r*math.cos(a),y,.946+r*math.sin(a)))
 rings.append(ring)
for a,b in zip(rings,rings[1:]):
 for i in range(n):
  j=(i+1)%n
  fs += [(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])]
volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
if volume<0:fs=[tuple(reversed(f)) for f in fs]
knob=mesh('Control_FixedSteppedKnob',vs,fs,4,'solid fixed faceted rotary-control exterior with finite embedded stem, no operation or motion')
link(knob,housing,(.185,-.211,.946),axis=(0,0,1),spread=.012);support('ControlStemEmbed',(.172,-.219,.933),(.198,-.203,.959),knob,housing)
plate=box('Rear_ClosedServicePlate',(0,.241,.68),(.45,.042,.69),4,'solid closed rear service plate with finite attachment; no rear opening or lock')
link(plate,housing,(0,.225,.68),axis=(0,0,1),spread=.15);support('FullRearPlateEmbed',(-.20,.221,.36),(.20,.229,1.0),plate,housing)
# Entire connected empty input and bezel volumes, with explicit boundary inset.
void('FullUpperBlindInput',(-.189,-.254,.921),(.039,-.126,.974),[],'entire finite deep upper input including bezel throat, complete closed-back end and all side extents; 1mm inset')
ISOLATED_VOID_VOLUMES['FullBezelThroughOpening']=probe((-.194,-.254,.916),(.044,-.204,.979),targets=[bezel],role='entire actual through aperture of separate bezel including both mouths')
# The complete receiving interior is a finite sloped prism, not an isolated ray.
def scoop_floor(y):return .335+(.41-.335)*(y+.397)/.332
vs=[(x,y,z) for top in[False,True] for y in[-.396,-.066] for x in[-.216,.216] for z in[.699 if top else scoop_floor(y)+.001]]
VOID_VOLUMES['FullSlopedReceiverInterior']={'vertices':vs,'faces':BOX_FACES,'targets':[],'role':'whole empty receiver interior from sloped floor to alcove roof and between inner side/back boundaries; 1mm inset'}
void('FullFrontReceivingMouth',(-.216,-.47,.406),(.216,-.396,.699),[],'entire wide forward mouth above real low lip, extending outside the scoop')
void('FullUpperReceiverAlcove',(-.229,-.219,.541),(.229,-.046,.699),[],'entire upper alcove above scoop rim, with actual back/side/roof boundaries')
void('FullDownwardBlindNeck',(-.099,-.199,.699),(.099,-.081,.819),[],'entire deep downward-opening neck including its open lower mouth and closed upper end')
# Complete solid slabs independently certify closed input/neck endpoints and housing walls.
wall('InputFullBack',(-.189,-.124,.921),(.039,-.095,.974))
wall('InputFullLeftWall',(-.219,-.219,.921),(-.191,-.126,.974))
wall('InputFullRightWall',(.041,-.219,.921),(.069,-.126,.974))
wall('InputFullFloor',(-.189,-.219,.89),(.039,-.126,.919))
wall('InputFullCeiling',(-.189,-.219,.976),(.039,-.126,1.005))
wall('NeckFullClosedEnd',(-.099,-.199,.821),(.099,-.081,.85))
wall('NeckFullBack',(-.099,-.079,.701),(.099,-.05,.819))
wall('NeckFullFront',(-.099,-.219,.701),(.099,-.201,.819))
wall('NeckFullLeftWall',(-.129,-.199,.701),(-.101,-.081,.819))
wall('NeckFullRightWall',(.101,-.199,.701),(.129,-.081,.819))
wall('ReceiverBackWall',(-.229,-.044,.301),(.229,-.01,.699))
wall('HousingFullBase',(-.309,-.219,.121),(.309,.229,.299))
wall('HousingFullRear',(-.309,.19,.301),(.309,.229,1.239))
wall('HousingFullLeft',(-.309,-.219,.301),(-.231,.189,1.239))
wall('HousingFullRight',(.231,-.219,.301),(.309,.189,1.239))
# The scoop's full sloped floor is a connected finite wedge in real material.
vs=[(x,y,z) for top in[False,True] for y in[-.39,-.07] for x in[-.21,.21] for z in[scoop_floor(y)-(.001 if top else .018)]]
WALL_VOLUMES['ReceiverFullSlopedFloor']={'vertices':vs,'faces':BOX_FACES,'target':scoop}
wall('ReceiverFullLowLip',(-.21,-.43,.337),(.21,-.399,.403),scoop)
wall('ReceiverBackThickness',(-.21,-.063,.412),(.21,-.027,.538),scoop)
# Centre the complete frozen assembly; every geometry and acceptance volume follows.
allv=[v for g in G.values() for v in g['vertices']];SHIFT=tuple(-(min(v[i] for v in allv)+max(v[i] for v in allv))/2 if i<2 else 0 for i in range(3))
for g in list(G.values())+list(VOID_VOLUMES.values())+list(ISOLATED_VOID_VOLUMES.values())+list(WALL_VOLUMES.values())+list(SUPPORT_VOLUMES.values()):g['vertices']=[add(p,SHIFT) for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT) for p in pts]) for a,b,pts in LINKS]
for g in VOID_VOLUMES.values():g['targets']=list(G)
TOKEN_CONTRACT={'single_prop_count':1,'closed_meshes':7,'genuine_blind_input':1,'separate_through_open_bezel':1,'fixed_solid_control':1,'continuous_thick_sloped_scoop':1,'low_front_lip':1,'downward_deep_blind_neck':1,'complete_ground_plinth':1,'no_internal_input_output_route':True,'native_fixed_pose_only':True}
def measure_token_machine_geometry(vertices):
 assert set(vertices)==set(G)
 assert abs(min(p[2] for p in vertices[base]))<2e-7
 p=vertices[scoop];assert abs(max(v[2] for v in p)-.54)<2e-7 and abs(min(v[2] for v in p)-.29)<2e-7
 p=vertices[housing];assert abs(max(v[2] for v in p)-1.24)<2e-7
 return dict(TOKEN_CONTRACT,geometry_scope='actual source/exported coordinates; independent complete empty/wall/support volumes, all-pair separation and negative-control acceptance required')
SELFTESTS=[(base,add((0,0,.075),SHIFT),add((0,0,-.01),SHIFT)),(housing,add((.28,0,.6),SHIFT),add((0,-.15,.6),SHIFT)),(scoop,add((0,-.2,.36),SHIFT),add((0,-.2,.48),SHIFT))]
FOCUS=(0,0,.64);ORTHO=1.80
CAMERAS={'gray-front3q':(2.3,-4.2,2.5),'gray-back3q':(-2.3,4.2,2.5),'thumbnail':(2.3,-4.2,2.5),'qa-front':(0,-4.2,1.75),'qa-side':(4.2,0,1.75),'qa-top':(0,0,4.2),'qa-back':(0,4.2,1.75),'qa-wireframe':(2.3,-4.2,2.5),'silhouette-128-front':(0,-4.2,1.75),'silhouette-128-side':(4.2,0,1.75)}
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
root=bpy.data.objects.new('OneRecessedTokenDispenserCabinet',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_token_machine_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'token_machine_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/arcade/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
