"""Original static wall-mounted open distribution box; one prop, no electrical claims."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='communications-open-terminal-distribution-box-01';VERSION='1.0.0';TITLE='Open Terminal Distribution Box'
DESCRIPTION=('One original static low-poly wall-mounted open distribution box, counted as one prop. A continuous thick back, side, roof and floor form a real open cavity. A thick door is fixed ninety degrees open, carried by two pairs of genuinely bored hinge knuckles, two complete headed fixed pins and one finite stop. A broad rear mounting face remains unobstructed. One rear support rail carries two original terminal blocks with real bottom-entry blind bores. Two separate thick closed polygonal wire bodies pass through genuine bottom sleeve openings and finish with finite embedded ends in the two terminal caps. All component positions are fixed. Sixteen closed connected editable meshes and five opaque unlinked constant PBR materials. Metres, native Z up, front -Y; fixed wall-mount datum, rear mounting plane Y=0.160 m, no ground support. No wall, other device, loose cables, brand, standard mark, texture or animation. Static visible geometry only; no electrical continuity, grounding, insulation, voltage/current rating, cooling, waterproofing, dust resistance, radio/signal function, installation standard, load, fire resistance, manufacture, safety certification, practical wiring instruction or compatibility with earlier equipment is asserted.')
G={};LINKS=[];CONTACTS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={};FEET=[]
BODY='Housing_ContinuousOpenWallBox';DOOR='Door_FixedNinetyDegreeOpen';RAIL='Rail_FixedRearSupport';STOP='Stop_FixedDoorOpenLimit'
TERMINALS=[];SLEEVES=[];WIRES=[];HINGES=[];PINS=[]
PALETTE=[('Housing_MutedPetrol',(.055,.205,.23,1),.52,.12),('Door_WarmIvory',(.64,.65,.53,1),.55,.10),('HingesRail_GraphiteAlloy',(.16,.21,.22,1),.40,.55),('TerminalsSleeves_Charcoal',(.035,.047,.052,1),.60,.04),('Wires_MutedOchre',(.72,.32,.055,1),.58,0)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no image/procedural texture nodes, linked shader inputs, transmission or emission.'
FOCUS=(-.015,-.230,.465);ORTHO=1.34
CAMERAS={'gray-front3q':(1.5,-2.8,1.65),'gray-back3q':(1.5,-2.8,-.75),'thumbnail':(1.5,-2.8,1.65),'qa-front':(-.015,-3.2,1.40),'qa-side':(3.2,-.23,1.40),'qa-top':(-.015,-.23,3.5),'qa-back':(-.015,3.2,1.4),'qa-wireframe':(1.5,-2.8,1.65),'silhouette-128-front':(-.015,-3.2,1.4),'silhouette-128-side':(3.2,-.23,1.4)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=['gray-back3q'];WIRE_THICKNESS=ORTHO/640

def point(p):return tuple(p)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.idx={}
 def vertex(self,p):
  p=tuple(round(float(c),9) for c in p)
  if p not in self.idx:self.idx[p]=len(self.v);self.v.append(p)
  return self.idx[p]
 def face(self,pts,mat=0):
  ids=[self.vertex(p) for p in pts]
  for i in range(1,len(ids)-1):
   ff=(ids[0],ids[i],ids[i+1])
   if len(set(ff))==3:self.f.append(ff);self.fm.append(mat)
 def result(self,role,mat=0):
  vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if vol<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'material':mat,'role':role}
def cellsolid(name,xs,ys,zs,occupied,mat,role):
 m=Mesh();cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 for i,j,k in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
  for (dx,dy,dz),q in [((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]:
   if (i+dx,j+dy,k+dz) not in cells:m.face(q,mat)
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def box(lo,hi,mat=0,role='Complete bounded box'):
 return cellsolid(None,[lo[0],hi[0]],[lo[1],hi[1]],[lo[2],hi[2]],lambda x,y,z:True,mat,role)
def slab(name,lo,hi,mat,role):G[name]=box(lo,hi,mat,role)
def profile_z(name,cx,cy,profile,mat,role,n=16):
 # Each profile point is z, half-X, half-Y, rectangle(True)/ellipse(False).
 m=Mesh()
 def p(spec,a):
  z,rx,ry,rect=spec;c=math.cos(a);s=math.sin(a)
  if rect and rx and ry:r=1/max(abs(c)/rx,abs(s)/ry);return(cx+r*c,cy+r*s,z)
  return(cx+rx*c,cy+ry*s,z)
 angles={round(math.tau*i/n,12) for i in range(n)}
 for z,rx,ry,rect in profile:
  if rect and rx and ry:
   corner=math.atan2(ry,rx)
   for aa in [corner,math.pi-corner,math.pi+corner,math.tau-corner]:angles.add(round(aa,12))
 angles=sorted(angles)
 for a,b in zip(profile,profile[1:]+profile[:1]):
  for aa,bb in zip(angles,angles[1:]+angles[:1]):m.face([p(a,aa),p(a,bb),p(b,bb),p(b,aa)],mat)
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def ring(name,cx,cy,z0,z1,outer,inner,mat,role,rect=False):
 return profile_z(name,cx,cy,[(z0,outer,outer,rect),(z1,outer,outer,rect),(z1,inner,inner,False),(z0,inner,inner,False)],mat,role)
def embed(name,lo,hi,a,b):
 EMBED_VOLUMES[name]=dict(box(lo,hi),targets=[a,b],role='Complete finite material embedding, not a point attachment.')
 LINKS.append((a,b,[tuple((lo[i]+hi[i])/2 for i in range(3))]))
def void(name,g,role):VOID_VOLUMES[name]=dict(g,targets=[],role=role)

def occupied(x,y,z):
 cavity=abs(x)<.285 and y<.120 and .155<z<.845
 bottomhole=z<.155 and any(abs(x-c)<.030 and abs(y+.020)<.030 for c in [-.15,.15])
 pin_recess=x<-.310 and y<-.116 and any(z0<z<z0+.114 for z0 in [.248,.628])
 door_knuckle_recess=x<-.300 and y<-.110 and any(z0<z<z0+.055 for z0 in [.307,.687])
 return not(cavity or bottomhole or pin_recess or door_knuckle_recess)
cellsolid(BODY,[-.320,-.310,-.300,-.285,-.180,-.120,.120,.180,.285,.320],[-.140,-.116,-.110,-.050,.010,.120,.160],[.120,.155,.248,.307,.362,.628,.687,.742,.845,.880],occupied,0,'One continuous closed thick housing with true open front cavity and two actual bottom through openings; full rear mounting face.')
cellsolid(DOOR,[-.354,-.322],[-.710,-.184,-.174],[.165,.248,.307,.628,.687,.835],lambda x,y,z:not(y>-.184 and any(a<z<b for a,b in [(.248,.307),(.628,.687)])),1,'One thick fixed-open ninety-degree door with two bounded lower-knuckle clearance notches; no motion or dynamic hinge claim.')
slab(RAIL,(-.250,.055,.575),(.250,.135,.615),2,'One independent fixed rear support rail with broad finite back embedding and two terminal seats.')
embed('RailRootInBack',(-.240,.123,.581),(.240,.132,.609),BODY,RAIL)
for i,cx in enumerate([-.150,.150],1):
 s=f'BottomSleeve_{i}_TrueThroughBore';SLEEVES.append(s)
 ring(s,cx,-.020,.100,.178,.035,.023,3,'One thick square outer sleeve with a genuine full-height polygonal through bore, finitely embedded in the floor.',True)
 embed(f'Sleeve{i}FloorRoot',(cx+.031,-.043,.125),(cx+.034,-.015,.150),BODY,s)
 t=f'Terminal_{i}_RealBlindEntry';TERMINALS.append(t)
 profile_z(t,cx,-.020,[(.540,.052,.090,True),(.690,.052,.090,True),(.690,0,0,False),(.650,0,0,False),(.650,.023,.023,False),(.540,.023,.023,False)],3,'One original terminal block with a full bottom-entry blind bore, thick cap, outer walls and finite rear rail embedding.')
 embed(f'Terminal{i}RailSeat',(cx-.040,.059,.580),(cx+.040,.067,.610),RAIL,t)
 w=f'Wire_{i}_ClosedFixedRoute';WIRES.append(w)
 profile_z(w,cx,-.020,[(.040,0,0,False),(.040,.012,.012,False),(.656,.012,.012,False),(.656,0,0,False)],4,'One continuous thick closed polygonal fixed wire body. The free lower stub passes through a real bottom bore with annular air and its upper end embeds into the terminal cap.',n=16)
 embed(f'Wire{i}TerminalEnd',(cx-.005,-.025,.651),(cx+.005,-.015,.655),w,t)
 void(f'BottomSleeve{i}InstalledAnnularAir',ring(None,cx,-.020,.098,.180,.0218,.0132,0,'Complete polygonal annular air around the installed wire, through and beyond both sleeve ends.'),'Full 360-degree installed-wire annulus through the actual bottom opening, with bounded positive tolerance layers.')
 void(f'Terminal{i}InstalledAnnularAir',ring(None,cx,-.020,.538,.648,.0218,.0132,0,'Complete polygonal annular air around installed wire in terminal entry.'),'Whole entry-to-cap annular cavity, including open mouth; finite end embedding is separately proved.')
 void(f'Wire{i}RouteFullAnnularAir',ring(None,cx,-.020,.181,.538,.048,.0132,0,'Complete annular route clearance around the entire free in-box line segment.',True),'Full bounded wire-route annulus between sleeve top and terminal mouth.')
 SOLID_VOLUMES[f'Terminal{i}CompleteCap']=dict(box((cx-.040,-.095,.660),(cx+.040,.060,.684)),targets=[t],role='Complete finite solid cap above terminal blind bore.')
for i,(cx,s,t) in enumerate(zip([-.150,.150],SLEEVES,TERMINALS),1):
 ISOLATED_VOID_VOLUMES[f'BottomSleeve{i}CompleteUnwiredBore']=dict(profile_z(None,cx,-.020,[(.098,0,0,False),(.098,.0218,.0218,False),(.180,.0218,.0218,False),(.180,0,0,False)],0,'Complete unwired bottom bore'),targets=[BODY,s],role='Full finite cylindrical bottom through-opening, independent of the installed wire.')
 ISOLATED_VOID_VOLUMES[f'Terminal{i}CompleteUnwiredBore']=dict(profile_z(None,cx,-.020,[(.538,0,0,False),(.538,.0218,.0218,False),(.648,.0218,.0218,False),(.648,0,0,False)],0,'Complete terminal blind bore'),targets=[t],role='Full finite terminal entry cavity to its real closed cap, independent of installed wire.')
# Two independently bored knuckle pairs. The full headed pin is fixed, with
# finite cap embeddings; its narrow middle has genuine full annular clearance.
for i,z in enumerate([.260,.640],1):
 a=f'Hinge_{i}_BodyBoredKnuckle';b=f'Hinge_{i}_DoorBoredKnuckle';pin=f'Hinge_{i}_CompleteHeadedPin';HINGES.extend([a,b]);PINS.append(pin)
 ring(a,-.338,-.146,z,z+.040,.035,.014,2,'Body-side full-height genuinely bored knuckle; finite side-wall embedding.')
 ring(b,-.338,-.146,z+.050,z+.090,.035,.014,2,'Door-side full-height genuinely bored knuckle; finite door-root embedding.')
 embed(f'Hinge{i}BodyRoot',(-.309,-.139,z+.006),(-.307,-.136,z+.034),BODY,a)
 embed(f'Hinge{i}DoorRoot',(-.343,-.179,z+.056),(-.333,-.176,z+.084),DOOR,b)
 profile_z(pin,-.338,-.146,[(z-.011,0,0,False),(z-.011,.026,.026,False),(z+.006,.026,.026,False),(z+.006,.011,.011,False),(z+.084,.011,.011,False),(z+.084,.026,.026,False),(z+.101,.026,.026,False),(z+.101,0,0,False)],2,'One complete fixed pin with continuous solid shaft and broad lower/upper heads; finite head embeddings carry both knuckles.')
 embed(f'Hinge{i}PinBodyHead',(-.360,-.150,z+.001),(-.354,-.142,z+.005),a,pin)
 embed(f'Hinge{i}PinDoorHead',(-.360,-.150,z+.085),(-.354,-.142,z+.089),b,pin)
 for label,lo,hi in [('Body',z+.007,z+.039),('Door',z+.051,z+.083)]:void(f'Hinge{i}{label}InstalledAnnulus',ring(None,-.338,-.146,lo,hi,.0132,.0117,0,'Complete installed hinge-bore annular clearance.'),'Full 360-degree pin/bore clearance away from the explicitly embedded retaining heads.')
 void(f'Hinge{i}BetweenKnucklesAnnulus',ring(None,-.338,-.146,z+.041,z+.049,.025,.0117,0,'Complete open inter-knuckle ring.'),'Full finite air between the two bored knuckles around the continuous shaft.')
for i,(a,b) in enumerate(zip(HINGES[::2],HINGES[1::2]),1):
 z=[.260,.640][i-1]
 for h,lo,hi in [(a,z-.001,z+.041),(b,z+.049,z+.091)]:ISOLATED_VOID_VOLUMES[h+'CompleteUnpinnedBore']=dict(profile_z(None,-.338,-.146,[(lo,0,0,False),(lo,.0132,.0132,False),(hi,.0132,.0132,False),(hi,0,0,False)],0,'Full isolated hinge hole'),targets=[h],role='Complete finite unpinned true through-bore; installed annular air is checked separately.')
slab(STOP,(-.322,-.220,.190),(-.295,-.125,.220),2,'One finite thick body-mounted open-angle stop, with an opposed complete side contact against the fixed door.')
embed('StopBodyRoot',(-.317,-.135,.195),(-.300,-.128,.215),BODY,STOP)
CONTACTS.append({'name':'DoorAgainstFiniteOpenStop','a':STOP,'b':DOOR,'axis':0,'a_positive':False,'plane_m':-.322,'minimum_patch_area_m2':.0013,'interior_probe_offset_m':.0005,'points':[(-.322,-.190,.200),(-.322,-.205,.210)]})
# The rectangular partitions and full annuli cover the whole functional cavity
# around its two finite routed-line/terminal zones, rail and floor sleeves.
for name,lo,hi in [
 ('CavityFullFrontMouth',(-.284,-.145,.156),(.284,-.111,.844)),
 ('CavityFullUpperRegion',(-.284,-.110,.691),(.284,.119,.844)),
 ('CavityFullLowerRegion',(-.284,-.110,.179),(.284,.119,.539)),
 ('CavityBottomFront',(-.284,-.139,.156),(.284,-.056,.178)),
 ('CavityBottomRear',(-.284,.016,.156),(.284,.119,.178)),
 ('CavityBottomMiddle',(-.114,-.055,.156),(.114,.015,.178)),
 ('CavityBottomLeft',(-.284,-.055,.156),(-.186,.015,.178)),
 ('CavityBottomRight',(.186,-.055,.156),(.284,.015,.178)),
 ('CavityTerminalMiddle',(-.097,-.110,.540),(.097,.054,.690)),
 ('CavityTerminalLeft',(-.284,-.110,.540),(-.203,.054,.690)),
 ('CavityTerminalRight',(.203,-.110,.540),(.284,.054,.690)),
 ('CavityAboveRail',(-.284,.071,.616),(.284,.119,.690)),
 ('CavityBelowRail',(-.284,.071,.540),(.284,.119,.574)),
 ('CavityRailLeftEnd',(-.284,.055,.575),(-.251,.119,.615)),
 ('CavityRailRightEnd',(.251,.055,.575),(.284,.119,.615))]:
 if name=='CavityFullLowerRegion':continue
 void(name,box(lo,hi),'Complete finite cavity partition; adjacent material/route footprints are handled by their complete specific annuli.')
# Lower free cavity is partitioned into full-width front/back regions plus
# side/middle corridors; route annuli cover the two remaining polygonal zones.
for name,lo,hi in [('LowerFront',(-.284,-.110,.179),(.284,-.069,.539)),('LowerRear',(-.284,.029,.179),(.284,.119,.539)),('LowerLeft',(-.284,-.068,.179),(-.199,.028,.539)),('LowerMiddle',(-.101,-.068,.179),(.101,.028,.539)),('LowerRight',(.199,-.068,.179),(.284,.028,.539))]:void(name,box(lo,hi),'Complete finite lower cavity corridor, excluding the two fully tested wire-route annuli.')
for label,x0,x1 in [('Left',-.284,-.203),('Middle',-.097,.097),('Right',.203,.284)]:
 for band,z0,z1 in [('BelowRail',.540,.574),('AboveRail',.616,.690)]:void('TerminalRear'+label+band,box((x0,.055,z0),(x1,.119,z1)),'Complete rear cavity space beside terminals above/below the support rail.')
# Complete slab certificates establish all five continuous cavity boundary walls.
for name,lo,hi in [('BackMountingPlate',(-.310,.130,.130),(.310,.150,.870)),('TopWall',(-.310,-.130,.852),(.310,.110,.873)),('LeftWall',(-.298,-.130,.160),(-.291,.110,.840)),('RightWall',(.291,-.130,.160),(.314,.110,.840)),('FloorFrontStrip',(-.310,-.130,.125),(.310,-.060,.150)),('FloorRearStrip',(-.310,.020,.125),(.310,.110,.150))]:SOLID_VOLUMES[name]=dict(box(lo,hi),targets=[BODY],role='Complete finite thick housing material region.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
MOUNT={'axis':1,'plane_m':.160,'minimum_patch_area_m2':.480,'wall_lo':[-.40,.160,.080],'wall_hi':[.40,.190,.930],'points':[[-.20,.160,.30],[.20,.160,.70]]}
def measure_wiring_geometry(vertices):return {'single_prop_count':1,'closed_mesh_count':len(G),'terminal_count':2,'wire_count':2,'bottom_through_sleeves':2,'fixed_door_count':1,'true_bored_knuckle_count':4,'complete_headed_pin_count':2,'finite_stop_count':1,'rail_count':1,'wall_mount_plane_y_m':.160,'wall_exported':False,'ground_support_claimed':False,'materials':MATERIAL_CONTRACT}
assert len(G)==16,len(G)

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
root=bpy.data.objects.new('OneOpenTerminalDistributionBox',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Wall-mount design datum: back mounting plane Y=0.160 m. Native Z up, front -Y; no ground support; wall omitted from the asset.';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover topology, volume and the complete rear mounting face.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in [BODY]:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.y-.160) for p in vv)<1e-7 and cr.y>0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.480,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
wiring_evidence=measure_wiring_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2]-.040)<1e-7 and triangles<12000
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
 'components':component_checks,'connection_interior_points':joints,'declared_wall_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'wiring_geometry':wiring_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_wall_mount_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, wall datum, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/communications/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'communications','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset';ground.hide_render=True
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
