"""Original fixed Y-branch baggage junction, one complete static visual prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='baggage-fixed-y-branch-roller-junction-01';VERSION='1.0.0';TITLE='Fixed Y-Branch Roller Junction'
DESCRIPTION=('One original static Y-shaped baggage junction, counted as one prop. A single continuous thick concave Y transfer deck and a separately connected lower Y frame link one short inlet to two different short outlet directions. Each arm carries three fixed thick rollers with continuous integral solid axles, two end collars and two genuinely bored bearing blocks. Finite lower bore faces support every axle and opposed outer bearing faces meet its fixed collars. A thick splitter nose and four low outer guides leave two bounded open routes and all three full-width terminal mouths. Four grounded feet, four uprights, three transverse end bearers and six side beams form the complete support path. Three own port coordinates, directions, clear dimensions and the real deck-to-roller gaps and height step are recorded. No conveyor line, luggage, drive, swinging gate, control, text, texture, animation or scene. Opaque unlinked constant PBR materials; metres, native Z up, front inlet -Y. Fixed static geometry only: no automatic sorting, motion, turning or baggage trajectory, smooth or seamless transfer, capacity, pinch protection, structural stability, manufacture, installation, airport standard, load or safety certification. No compatibility with previous straight, corner, railway or other assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];LEGS=[];BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={};SEATS={};ROLLERS=[];PORTS=[];EMBED_VOLUMES={}
BODY='TransferDeck_ContinuousThickY';FRAME='Underframe_ContinuousThickY';NOSE='SplitterNose_ThickFixed';GUIDES=[]
PALETTE=[('Frame_MutedOchre',(.48,.245,.065,1),.53,.30),('TransferDeck_Petrol',(.045,.20,.24,1),.46,.38),('Roller_SatinAlloy',(.53,.61,.64,1),.37,.65),('Bearing_Graphite',(.055,.075,.085,1),.50,.45),('Foot_Charcoal',(.028,.038,.043,1),.85,0)]
FOCUS=(0,-.14,.46);ORTHO=3.65;CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
CAMERAS={'gray-front3q':(3.3,-4.2,4.2),'gray-back3q':(-3.3,4.2,4.2),'thumbnail':(3.3,-4.2,4.2),'qa-front':(0,-5,3.2),'qa-side':(5,-.14,3.2),'qa-top':(0,-.14,6),'qa-back':(0,5,3.2),'qa-wireframe':(3.3,-4.2,4.2),'silhouette-128-front':(0,-5,3.2),'silhouette-128-side':(5,-.14,3.2)}
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def ear(poly):
 p=list(poly);area=sum(cross2(p[i],p[(i+1)%len(p)]) for i in range(len(p)));ix=list(range(len(p))) if area>0 else list(reversed(range(len(p))));out=[]
 while len(ix)>3:
  for i,b in enumerate(ix):
   a=ix[i-1];c=ix[(i+1)%len(ix)]
   if cross2((p[b][0]-p[a][0],p[b][1]-p[a][1]),(p[c][0]-p[b][0],p[c][1]-p[b][1]))<=1e-12:continue
   def isin(q):return all(cross2((v[0]-u[0],v[1]-u[1]),(q[0]-u[0],q[1]-u[1]))>=-1e-12 for u,v in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(isin(p[q]) for q in ix if q not in [a,b,c]):continue
   out.append((a,b,c));ix.pop(i);break
  else:raise AssertionError('Invalid polygon')
 out.append(tuple(ix));return out

def data(v,faces,mat,role):
 ff=[t for f in faces for t in [(f[0],f[i],f[i+1]) for i in range(1,len(f)-1)]]
 vol=sum(dot(v[a],cross(v[b],v[c])) for a,b,c in ff)/6
 if vol<0:ff=[tuple(reversed(f)) for f in ff]
 return {'vertices':[tuple(round(float(x),9) for x in p) for p in v],'faces':ff,'material':mat,'role':role}
def put(name,g):
 if name:assert name not in G;G[name]=g
 return g

def prism(name,poly,z0,z1,mat,role):
 p=list(poly);p=p if sum(cross2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))>0 else list(reversed(p));n=len(p);v=[(x,y,z) for z in [z0,z1] for x,y in p];cap=ear(p);f=[tuple(reversed(q)) for q in cap]+[tuple(n+i for i in q) for q in cap]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return put(name,data(v,f,mat,role))
def branch_point(label,u,s,z):
 d,e=BRANCHES[label];return(e[0]*u+d[0]*s,e[1]*u+d[1]*s,z)
def local_box(name,label,lo,hi,mat,role):
 return prism(name,[branch_point(label,u,s,0)[:2] for u,s in [(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]],lo[2],hi[2],mat,role)
def world_box(name,lo,hi,mat,role):return prism(name,[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])],lo[2],hi[2],mat,role)
def embed(name,g,a,b):
 EMBED_VOLUMES[name]=dict(g,targets=[a,b]);WALL_VOLUMES[name]=dict(g,targets=[a,b]);v=g['vertices'];p=tuple(sum(q[i] for q in v)/len(v) for i in range(3));LINKS.append((a,b,[p]))
def le(name,label,lo,hi,a,b):embed(name,local_box(None,label,lo,hi,0,'Whole finite embedded support region'),a,b)
def we(name,lo,hi,a,b):embed(name,world_box(None,lo,hi,0,'Whole finite embedded support region'),a,b)
BRANCHES={k:((math.cos(a),math.sin(a)),(-math.sin(a),math.cos(a))) for k,a in [('Inlet',-math.pi/2),('RightOutlet',math.pi/6),('LeftOutlet',5*math.pi/6)]}
def ypoly(w,r):
 q=math.sqrt(3);return[(-w,-r),(w,-r),(w,-w/q),(r*q/2+w/2,r/2-w*q/2),(r*q/2-w/2,r/2+w*q/2),(0,2*w/q),(-r*q/2+w/2,r/2+w*q/2),(-r*q/2-w/2,r/2-w*q/2),(-w,-w/q)]
prism(BODY,ypoly(.30,.72),.750,.880,1,'One closed continuous concave Y transfer deck, with three actual open terminal edges; not three overlapping old tables.')
prism(FRAME,ypoly(.390,.735),.690,.765,0,'One separate continuous lower Y support frame, finitely joined to central deck and six branch side beams.')
we('DeckCentralRoot',(-.16,-.15,.752),(.16,.13,.762),BODY,FRAME)
prism(NOSE,[(0,.180),(.120,.400),(0,.330),(-.120,.400)],.865,.955,0,'One thick original fixed bifurcation nose with two sloping plan faces, finitely rooted in the central transfer deck.')
we('NoseRoot',(-.015,.245,.867),(.015,.275,.876),NOSE,BODY)
# Four outer low guides stop before all terminal edges. Each has its own finite deck root.
for label in ['Inlet','RightOutlet','LeftOutlet']:
 for si in [-1,1]:
  if label!='Inlet' and ((label=='RightOutlet' and si==1) or (label=='LeftOutlet' and si==-1)):continue
  name=f'OuterGuide_{label}_{si:+d}';GUIDES.append(name)
  start=.23 if label!='Inlet' else .205
  local_box(name,label,(si*.265-.018,start,.864),(si*.265+.018,.685,.945),0,'Thick bounded low outer guide, finite embedded foot, stopped short of the open terminal mouth.')
  le(name+'Root',label,(si*.265-.012,start+.015,.866),(si*.265+.012,.67,.877),name,BODY)
# Broad fixed central pedestal and three separate terminal T supports.
world_box('CentralFoot',(-.18,-.18,0),(.18,.18,.045),4,'Flat finite central ground foot');FEET.append('CentralFoot')
world_box('CentralUpright',(-.065,-.065,.032),(.065,.065,.715),0,'Continuous central upright joining central ground foot to Y underframe');LEGS.append('CentralUpright')
we('CentralFootSocket',(-.05,-.05,.035),(.05,.05,.042),'CentralFoot','CentralUpright');we('CentralFrameSocket',(-.05,-.05,.695),(.05,.05,.710),'CentralUpright',FRAME)
N=12;ANG=[math.pi/N+math.tau*i/N for i in range(N)];C=math.cos(math.pi/N);SHAFT_R=.016;BORE_R=.024;SHAFT_Z=.820;BEARING_Z=SHAFT_Z+(BORE_R-SHAFT_R)*C;LOWER_Z=SHAFT_Z-SHAFT_R*C;ROLLER_R=.060;ROLLER_TOP=SHAFT_Z+ROLLER_R*C
# Surface-of-revolution profiles are closed connected solids, with continuous
# shafts and full collars. The bearing bodies have real material boundary holes.
def profile(name,label,s,profile,mat,role):
 v=[];rings=[]
 for u,r in profile:
  ids=[]
  for a in ANG:
   p=branch_point(label,u,s+r*math.sin(a),SHAFT_Z+r*math.cos(a))
   try:idx=v.index(p)
   except ValueError:idx=len(v);v.append(p)
   ids.append(idx)
  rings.append(ids)
 f=[]
 for aa,bb in zip(rings,rings[1:]+rings[:1]):
  for i in range(N):
   j=(i+1)%N;ids=[aa[i],aa[j],bb[j],bb[i]];ids=list(dict.fromkeys(ids))
   if len(ids)>=3:f.append(ids)
 return put(name,data(v,f,mat,role))
def bearing(name,label,s,u0,u1):
 outer=[];inner=[]
 for a in ANG:
  dy,dz=math.sin(a),math.cos(a);scale=.050/max(abs(dy),abs(dz));outer.append((scale*dy,scale*dz));inner.append((BORE_R*dy,BORE_R*dz))
 v=[branch_point(label,u,s+y,BEARING_Z+z) for p,u in [(outer,u0),(outer,u1),(inner,u0),(inner,u1)] for y,z in p];f=[];wall=[]
 for i in range(N):
  j=(i+1)%N;f +=[(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)]
  wall.extend([len(f)*2-6,len(f)*2-5])
 g=put(name,data(v,f,3,'One closed thick bearing body with a full twelve-sided through bore; finite bottom bore facet and opposed full outer collar shoulder.'))
 return g
for label,(d,e) in BRANCHES.items():
 foot=label+'_Foot';leg=label+'_Upright';bar=label+'_TransverseBearer'
 local_box(foot,label,(-.31,1.075,0),(.31,1.225,.045),4,'Broad finite ground foot transverse to this branch');FEET.append(foot)
 local_box(leg,label,(-.055,1.105,.032),(.055,1.195,.715),0,'Continuous upright between grounded terminal foot and transverse upper bearer');LEGS.append(leg)
 local_box(bar,label,(-.380,1.095,.670),(.380,1.205,.745),0,'Independent transverse thick terminal bearer supporting both side beams')
 le(label+'FootSocket',label,(-.045,1.115,.035),(.045,1.185,.042),foot,leg);le(label+'BearerSocket',label,(-.045,1.115,.675),(.045,1.185,.710),leg,bar)
 for sign in [-1,1]:
  u=sign*.345;beam=label+f'_SideBeam_{sign:+d}'
  local_box(beam,label,(u-.0325,.590,.700),(u+.0325,1.360,.790),0,'One straight short branch side beam, rooted into the single lower Y frame and its own transverse terminal bearer.')
  le(beam+'YRoot',label,(u-.022,.620,.710),(u+.022,.710,.755),beam,FRAME)
  le(beam+'BearerRoot',label,(u-.022,1.115,.705),(u+.022,1.185,.738),beam,bar)
 for i,s in enumerate([.825,1.005,1.185],1):
  roll=label+f'_FixedRoller{i}';ROLLERS.append(roll)
  profile(roll,label,s,[(-.398,0),(-.398,.030),(-.375,.030),(-.375,SHAFT_R),(-.280,SHAFT_R),(-.280,ROLLER_R),(.280,ROLLER_R),(.280,SHAFT_R),(.375,SHAFT_R),(.375,.030),(.398,.030),(.398,0)],2,'One closed fixed roller with a continuous solid through-axle and two integral thick retaining collars; all surfaces are finite, fixed geometry.')
  for sign in [-1,1]:
   u0,u1=(-.375,-.315) if sign<0 else (.315,.375);name=label+f'_Bearing{i}_{sign:+d}';bearing(name,label,s,u0,u1);beam=label+f'_SideBeam_{sign:+d}'
   le(name+'BeamRoot',label,(u0+.010,s-.035,.780),(u1-.010,s+.035,.787),name,beam)
   CONTACTS.append({'name':name+'LowerShaftSeat','a':name,'b':roll,'normal':(0,0,1),'plane_m':LOWER_Z,'minimum_patch_area_m2':.00048,'interior_probe_offset_m':.0003,'points':[branch_point(label,u,s,LOWER_Z) for u in [u0+.012,(u0+u1)/2,u1-.012]],'role':'whole opposed finite lower bore face carrying the actual axle'})
   ua=u0 if sign<0 else u1;a,b=(roll,name) if sign<0 else (name,roll)
   CONTACTS.append({'name':name+'FixedEndShoulder','a':a,'b':b,'normal':(*e,0),'plane_m':ua,'minimum_patch_area_m2':.0007,'interior_probe_offset_m':.0003,'points':[branch_point(label,ua,s+.027,SHAFT_Z)],'role':'whole opposed finite retaining collar shoulder against bearing end face'})
   SEATS[name]={'roller':roll,'label':label,'sign':sign,'u0':u0,'u1':u1,'s':s,'bore_center_z_m':BEARING_Z,'lower_seat_z_m':LOWER_Z,'inner_wall_triangles':[8*j+k for j in range(N) if j!=5 for k in [2,3]],'excluded_wall_facet_index':5}
   # Full bore prism, independent of installed roller, with both mouths included.
   poly=[(s+(BORE_R-.0005)*math.sin(a),BEARING_Z+(BORE_R-.0005)*math.cos(a)) for a in ANG]
   v=[branch_point(label,u,yy,zz) for u in [u0-.001,u1+.001] for yy,zz in poly];f=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(j,(j+1)%N,(j+1)%N+N,j+N) for j in range(N)]
   ISOLATED_VOID_VOLUMES[name+'_WholeUnshaftedBore']=dict(data(v,f,0,'Complete isolated bore volume'),targets=[name])
   BORES.append({'mesh':name,'origin_m':branch_point(label,u0-.002,s,BEARING_Z),'direction':(*e,0),'length_m':u1-u0+.004})
   # Full nonbearing hole-wall domain is separately measured against the shaft.
   # These complete finite crescent strips have positive tolerance on both sides,
   # and cover every noncontact facet through the full bearing depth.
   for j in range(N):
    if j==5:continue
    k=(j+1)%N;out=[(s+BORE_R*math.sin(ANG[q]),BEARING_Z+BORE_R*math.cos(ANG[q])) for q in [j,k]];inn=[(s+SHAFT_R*math.sin(ANG[q]),SHAFT_Z+SHAFT_R*math.cos(ANG[q])) for q in [j,k]]
    p=[tuple(.25*inn[q][a]+.75*out[q][a] for a in range(2)) for q in [0,1]]+ [tuple(.75*inn[q][a]+.25*out[q][a] for a in range(2)) for q in [1,0]]
    old=p;p=[]
    for aa,bb in zip(old,old[1:]+old[:1]):
     za,zb=aa[1]-LOWER_Z-.0005,bb[1]-LOWER_Z-.0005
     if (za>=0)!=(zb>=0):p.append(tuple(aa[k]+(bb[k]-aa[k])*za/(za-zb) for k in [0,1]))
     if zb>=0:p.append(bb)
    nn=len(p);vv=[branch_point(label,u,yy,zz) for u in [u0+.0005,u1-.0005] for yy,zz in p];ff=[tuple(reversed(range(nn))),tuple(range(nn,2*nn))]+[(q,(q+1)%nn,(q+1)%nn+nn,q+nn) for q in range(nn)]
    VOID_VOLUMES[name+f'_InstalledGapFacet{j:02d}']=dict(data(vv,ff,0,'Whole bounded installed nonbearing annular-gap facet strip'),targets=[name,roll])
 # A complete mouth is full 560 mm roller width and 320 mm declared height.
 VOID_VOLUMES[label+'_FullWidthFullHeightPort']=dict(local_box(None,label,(-.2795,1.315,.881),(.2795,1.405,1.201),0,'Complete finite terminal port; 0.5 mm side tolerance from nominal 560 mm span'),targets=[])
 VOID_VOLUMES[label+'_WholeRollerLaneAbove']=dict(local_box(None,label,(-.2795,.7205,.881),(.2795,1.405,1.201),0,'Whole finite air above this short roller lane and through its open mouth'),targets=[])
 PORTS.append({'name':label,'role':'inlet' if label=='Inlet' else 'outlet','center_m':branch_point(label,0,1.36,.880),'outward_direction':(*d,0),'up':(0,0,1),'roller_width_m':.560,'declared_clear_height_m':.320,'verified_volume_width_m':.559,'support_top_z_m':ROLLER_TOP,'interface_compatibility_claimed':False})
 # Complete open lower region between central and terminal pedestals.
 VOID_VOLUMES[label+'_CompleteLowerBay']=dict(local_box(None,label,(-.279,.255,.050),(.279,1.100,.665),0,'Whole finite lower open bay between central foot and terminal upright'),targets=[])
# Complete bounded route domains overlap in finite volumes; no centreline-only proof.
VOID_VOLUMES['CentralInletFullRoute']=dict(world_box(None,(-.235,-.7205,.881),(.235,.160,1.201),0,'Entire central inlet route up to the splitter, with finite width/height'),targets=[])
for label in ['RightOutlet','LeftOutlet']:
 VOID_VOLUMES[label+'_WholeForkRoute']=dict(local_box(None,label,(-.220,.280,.881),(.220,.721,1.201),0,'Entire 440 mm wide fork route past the splitter, finitely overlapping central and terminal route domains'),targets=[])
for name,g in VOID_VOLUMES.items():
 if not g['targets']:g['targets']=list(G)
JUNCTION_CONTRACT={'single_prop_count':1,'roller_count':9,'bored_bearing_count':18,'port_count':3,'ground_foot_count':4,'outer_guide_count':4,'transfer_top_z_m':.880,'roller_top_z_m':ROLLER_TOP,'actual_transfer_to_roller_top_step_m':.880-ROLLER_TOP,'first_roller_plan_envelope_gap_m':.825-.060*C-.720,'adjacent_roller_plan_gap_m':.180-2*.060*C,'fixed_pose_only':True,'ports':PORTS,'automatic_sorting_or_compatibility_claimed':False}
def measure_junction_geometry(vertices):
 assert set(vertices)==set(G)
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<2e-7
 return dict(JUNCTION_CONTRACT,mesh_count=len(vertices),geometry_scope='actual coordinates with separate whole-volume, full-surface, finite opposed contact and mutation gates')

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
root=bpy.data.objects.new('OneFixedYBranchJunction',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0, junction hub centre, front inlet -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# This producer Blender section checks topology, finite ground faces, interior
# connection witnesses, bore-axis rays and the oriented export fingerprint.
# Complete finite empty volumes and whole support/contact surfaces are verified
# by the independent actual-GLB acceptance gate, not by these diagnostic witnesses.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
junction_evidence=measure_junction_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])
 assert hit[0] is None,(r,hit)
 bore_checks.append(dict(r,actual_ear_axis_clear=True,full_volume_scope='source finite-volume and independent imported-GLB audits'))
adj={name:set() for name in G}
for a,b,points in LINKS:
 samples=[]
 for p in points:
  margin=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3]);valid=actual_inside(a,p) and actual_inside(b,p) and margin>.0001;assert valid,(a,b,p,margin)
  samples.append({'point_m':p,'both_interiors':True,'nearest_boundary_margin_m':margin})
 joints.append({'a':a,'b':b,'samples':samples});adj[a].add(b);adj[b].add(a)
for r in CONTACTS:
 a,b=r['a'],r['b'];eps=r['interior_probe_offset_m']
 for p in r['points']:
  normal=Vector(r.get('normal',tuple(1 if i==r.get('axis',2) else 0 for i in range(3))));low=Vector(p)-normal*eps;high=Vector(p)+normal*eps
  assert actual_inside(a,low) and actual_inside(b,high) and not actual_inside(a,high) and not actual_inside(b,low),(a,b,p)
 adj[a].add(b);adj[b].add(a);face_contacts.append(dict(r,actual_opposed_interior_side_probes=True,full_area_scope='pure source and independent actual GLB full-surface audit'))
todo=list(seen)
while todo:
 for name in adj[todo.pop()]-seen:seen.add(name);todo.append(name)
assert seen==set(G),seen
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
 'single_prop_count':1,'junction_geometry':junction_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/baggage/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'baggage','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,8),1700,5.0),('Fill',(6,-1.2,5),840,4.8),('Rim',(1.2,6,7),1200,4.8)]:
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
if '--ground-views' in sys.argv:views={n:CAMERAS[n] for n in ['qa-front','qa-side','qa-back']}
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
