"""Original recess-front watchmaker bench, one complete static visual prop.
Metres, native Z up, front -Y. No repair, motion, human fit, load or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='timekeeping-recess-front-watchmaker-bench-01';VERSION='1.0.0';TITLE='Recess-Front Watchmaker Bench'
DESCRIPTION=('One original static watchmaker-bench appearance, counted as one prop. A continuous 60 mm thick horizontal workboard has an open-to-front half-ellipse recess, two broad side arms and an uninterrupted rear bridge. A single solid 28 mm thick U-shaped low backstop covers the rear and both sides. A separate fixed shallow tray below the recess has a complete 18 mm bottom and four 18 mm walls; its two bottom margins sit on finite brass-coloured rails attached to the front legs. Four full grounded legs, two upper side beams, a full rear upper beam and a lower rear stretcher form an open frame. Every separate component is attached by finite opposed faces without hidden penetration. The forward knee region, full curved recess, full tray cavity, tray-to-workboard gap and both side frame bays remain real empty volumes. Thirteen editable closed meshes and four opaque constant PBR materials. Metres, native Z up, front -Y, horizontally bounds-centred ground datum. No watch, clock, magnifier, tool, stool, drawer motion, scene platform, text or logo. The continuous front cut, complete lower tray and full support arrangement are newly authored; no old square worktable, sewing-machine aperture, pottery turntable, tilted drafting board or wagon bench geometry is loaded or transformed. Fixed static visual only: no real watch repair, precision, parts retention, capacity, motion, human dimensions, posture or ergonomics, load, stability, material, antistatic, manufacture, assembly, installation or occupational-safety claim; no compatibility with old watches, chairs or tools.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('Frame_DeepPetrol',(.045,.18,.19,1),.66,.06),('Board_PaleBirch',(.72,.535,.31,1),.74,0),('Rail_MutedBrass',(.47,.315,.115,1),.42,.55),('Backstop_DarkWalnut',(.17,.09,.045,1),.72,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))
def mesh(name,vs,fs,mat,role):
 assert name not in G
 vs=[tuple(round(float(c),9) for c in p) for p in vs]
 volume=sum(dot(vs[f[0]],cross(vs[f[i]],vs[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 G[name]={'vertices':vs,'faces':fs,'material':mat,'role':role};return name
def prism_geometry(poly,z0,z1):
 if area2(poly)<0:poly=list(reversed(poly))
 n=len(poly);vs=[(x,y,z) for z in [z0,z1] for x,y in poly]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return vs,fs
def prism(name,poly,z0,z1,mat,role):return mesh(name,*prism_geometry(poly,z0,z1),mat,role)
def rect(x0,x1,y0,y1):return[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
def box(name,lo,hi,mat,role):return prism(name,rect(lo[0],hi[0],lo[1],hi[1]),lo[2],hi[2],mat,role)
def contact(name,a,b,axis,point,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,point),'minimum_patch_area_m2':area-1e-7,'interior_probe_offset_m':.0003,'points':points or [point],'scope':scope})
def inset(poly,d):
 p=list(poly)
 if area2(p)<0:p.reverse()
 lines=[]
 for a,b in zip(p,p[1:]+p[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy);n=(-dy/ln,dx/ln);lines.append((n[0],n[1],n[0]*a[0]+n[1]*a[1]+d))
 out=[]
 for i,(a,b,c) in enumerate(lines):
  d1,e,f=lines[i-1];det=a*e-b*d1;assert abs(det)>1e-12
  out.append(((c*e-b*f)/det,(a*f-c*d1)/det))
 return out
def probe(name,poly,z0,z1,role,targets=None,solid=False):
 vs,fs=prism_geometry(poly,z0,z1)
 (SOLID_VOLUMES if solid else VOID_VOLUMES)[name]={'vertices':vs,'faces':fs,'targets':list(G) if targets is None else targets,'role':role}
def probe_box(name,lo,hi,role,targets=None,solid=False):probe(name,rect(lo[0],hi[0],lo[1],hi[1]),lo[2],hi[2],role,targets,solid)

# The original front edge follows 24 complete planar arc facets, open at the
# actual outer front boundary. It is not a central hole or an added dark decal.
ARC=[(.4*math.cos(math.pi-i*math.pi/24),-.49+.39*math.sin(math.pi-i*math.pi/24)) for i in range(25)]
TOP_POLY=[(-.75,-.49)]+ARC+[(.75,-.49),(.75,.49),(-.75,.49)]
BODY=prism('Continuous_RecessFrontWorkboard',TOP_POLY,1.02,1.08,1,'one closed 60 mm thick horizontal board; 24-facet open front elliptical cut; broad continuous side arms and rear bridge')
U_POLY=[(-.75,-.42),(-.722,-.42),(-.722,.462),(.722,.462),(.722,-.42),(.75,-.42),(.75,.49),(-.75,.49)]
BORDER=prism('Continuous_ThickUBackstop',U_POLY,1.08,1.15,3,'one continuous 28 mm thick low solid backstop with open front, two sides and full rear')
contact('WholeBackstopBottom',BODY,BORDER,(0,0,1),(0,.476,1.08),abs(area2(U_POLY))/2,'entire U-shaped underside against full board top',[(0,.476,1.08),(-.736,0,1.08),(.736,0,1.08)])
LEGS=[];SIDE_BEAMS=[];RAILS=[]
for label,x0,x1,sign in [('Left',-.65,-.54,-1),('Right',.54,.65,1)]:
 x=(x0+x1)/2
 for end,y0,y1 in [('Front',-.40,-.29),('Rear',.25,.36)]:
  n=box(label+'_'+end+'FullLeg',(x0,y0,0),(x1,y1,.91),0,'full four-sided leg with complete 110 by 110 mm ground and upper support faces');FEET.append(n);LEGS.append(n)
 beam=box(label+'_UpperSideBeam',(x0,-.40,.91),(x1,.36,1.02),0,'continuous upper side beam directly supporting the board side arm');SIDE_BEAMS.append(beam)
 for end,y in [('Front',-.345),('Rear',.305)]:contact(label+end+'LegTop',label+'_'+end+'FullLeg',beam,(0,0,1),(x,y,.91),.11*.11,'whole leg top seated beneath upper side beam')
 contact(label+'BeamBoardSeat',beam,BODY,(0,0,1),(x,0,1.02),.11*.76,'entire upper side beam top directly against continuous board side arm',[(x,-.33,1.02),(x,0,1.02),(x,.30,1.02)])
 rx0,rx1=(-.54,-.44) if sign<0 else (.44,.54)
 rail=box(label+'_FixedTraySupportRail',(rx0,-.39,.80),(rx1,.02,.825),2,'fixed solid rail with finite root on front leg inner face and finite upper tray support strip');RAILS.append(rail)
 # For each root the axis is from leg toward the rail, preserving opposed sides.
 contact(label+'RailRoot',label+'_FrontFullLeg',rail,(-sign,0,0),(sign*.54,-.34,.8125),.10*.025,'complete 100 by 25 mm rail-root patch on front leg inner face',[(sign*.54,y,.8125) for y in [-.375,-.34,-.305]])
rear=box('Rear_UpperBridgeBeam',(-.54,.25,.915),(.54,.36,1.02),0,'full rear upper beam between side beams, supporting the continuous tabletop rear bridge')
low=box('Rear_LowerOpenFrameStretcher',(-.54,.25,.24),(.54,.36,.32),0,'full rear lower stretcher between rear legs; front knee region remains empty')
contact('RearUpperLeftRoot',SIDE_BEAMS[0],rear,(1,0,0),(-.54,.305,.9675),.11*.105,'complete rear beam left end on side beam inner face')
contact('RearUpperRightRoot',rear,SIDE_BEAMS[1],(1,0,0),(.54,.305,.9675),.11*.105,'complete rear beam right end on side beam inner face')
contact('RearBridgeBoardSeat',rear,BODY,(0,0,1),(0,.305,1.02),1.08*.11,'whole rear beam top directly supporting the continuous rear board bridge',[(x,.305,1.02) for x in [-.45,0,.45]])
contact('RearLowerLeftRoot','Left_RearFullLeg',low,(1,0,0),(-.54,.305,.28),.11*.08,'complete rear lower stretcher left end')
contact('RearLowerRightRoot',low,'Right_RearFullLeg',(1,0,0),(.54,.305,.28),.11*.08,'complete rear lower stretcher right end')

# One coherent tray boundary, including exterior underside, full inner floor,
# outer walls, top rims and inner walls. Nothing caps its real shallow cavity.
outer=rect(-.48,.48,-.55,.02);inner=rect(-.462,.462,-.532,.002)
vs=[(x,y,z) for poly,z in [(outer,.825),(outer,.90),(inner,.90),(inner,.843)] for x,y in poly]
fs=[(3,2,1,0),(12,13,14,15)]
for k in range(3):
 for i in range(4):j=(i+1)%4;fs.append((4*k+i,4*k+j,4*(k+1)+j,4*(k+1)+i))
TRAY=mesh('Fixed_CompleteShallowCatchTray',vs,fs,0,'single full-bottom shallow tray: 18 mm floor, four 18 mm walls, real open interior; fixed 60 mm beyond the front board edge')
for label,x,rail in zip(['Left','Right'],[-.46,.46],RAILS):
 contact(label+'RailTraySeat',rail,TRAY,(0,0,1),(x,-.185,.825),.04*.41,'complete 40 by 410 mm finite rail-top strip against actual tray underside',[(x,y,.825) for y in [-.36,-.185,-.01]])

# Complete whole air bodies, bounded 1 mm from physical surfaces, no rays used
# to stand in for volume acceptance. The recess probe covers its full curved
# outline, entire board thickness, open front mouth and passage down to tray.
NOTCH_POLY=[(-.4,-.531),(.4,-.531)]+list(reversed(ARC))
probe('WholeCurvedFrontRecessAndCollectionPassage',inset(NOTCH_POLY,.001),.844,1.151,'whole original curved front opening and direct passage down toward the tray; complete panel thickness and open front mouth')
probe_box('WholeTrayInnerCavity',(-.461,-.531,.844),(.461,.001,.899),'complete shallow tray cavity including every inner side, inner bottom and open top')
probe_box('WholeTrayToBoardGap',(-.479,-.549,.901),(.479,.019,1.019),'entire broad gap above tray rim and beneath workboard, no hidden tray-board contact')
probe_box('WholeFrontKneeAir',(-.539,-.55,.001),(.539,.249,.799),'whole clear forward knee volume under rails and tray, from ground to rail underside and open to front')
probe_box('WholeBetweenRailsAir',(-.439,-.389,.800),(.439,.019,.824),'entire inter-rail gap directly under tray floor')
for label,x0,x1 in [('Left',-.539,-.481),('Right',.481,.539)]:
 probe_box(label+'WholeTrayLegCorridor',(x0,-.389,.826),(x1,.019,.909),'whole corridor between tray outer side and leg envelope, above fixed rail')
for label,x0,x1 in [('Left',-.649,-.541),('Right',.541,.649)]:
 probe_box(label+'WholeSideFrameAir',(x0,-.289,.001),(x1,.249,.909),'whole open side-frame bay between front/rear legs and below side beam')
probe_box('WholeRearLowerBay',(-.539,.251,.001),(.539,.359,.239),'whole rear bay below the lower stretcher')
probe_box('WholeRearUpperBay',(-.539,.251,.321),(.539,.359,.909),'whole rear bay between lower stretcher and upper beam')
probe('WholeBoardMaterial',inset(TOP_POLY,.001),1.021,1.079,'whole continuous concave workboard material with side arms and rear bridge, 1 mm boundary margins',[BODY],True)
probe('WholeBackstopMaterial',inset(U_POLY,.001),1.081,1.149,'whole continuous thick U-backstop material, including both bends',[BORDER],True)
probe_box('WholeTrayBottomMaterial',(-.479,-.549,.826),(.479,.019,.842),'entire tray bottom material beneath the cavity, 1 mm boundary margins',[TRAY],True)
for label,x0,x1 in [('Left',-.479,-.463),('Right',.463,.479)]:probe_box(label+'WholeTrayWallMaterial',(x0,-.549,.844),(x1,.019,.899),'whole thick tray side wall above inner floor',[TRAY],True)
for label,y0,y1 in [('Front',-.549,-.533),('Back',.003,.019)]:probe_box(label+'WholeTrayWallMaterial',(-.461,y0,.844),(.461,y1,.899),'whole thick tray end wall above inner floor',[TRAY],True)

# Translate all evidence and asset vertices together to a horizontal bounds
# centre at (0,0). Original local construction coordinates remain documented.
SHIFT=(0,-.03,0)
for g in list(G.values())+list(VOID_VOLUMES.values())+list(SOLID_VOLUMES.values()):g['vertices']=[sub(p,SHIFT) for p in g['vertices']]
for r in CONTACTS:r['origin_m']=sub(r['origin_m'],SHIFT);r['points']=[sub(p,SHIFT) for p in r['points']]
CONTRACT={'single_prop_count':1,'closed_editable_components':13,'continuous_front_arc_facets':24,'board_thickness_m':.06,'backstop_thickness_m':.028,'full_bottom_fixed_tray':1,'tray_floor_and_wall_thickness_m':.018,'complete_ground_legs':4,'finite_fixed_tray_rails':2,'continuous_upper_side_beams':2,'rear_upper_bridge_beam':1,'rear_lower_stretcher':1,'finite_opposed_contacts':len(CONTACTS),'whole_air_bodies':len(VOID_VOLUMES),'whole_material_bodies':len(SOLID_VOLUMES)}
def measure_bench_geometry(vertices):
 assert set(vertices)==set(G) and len(vertices)==13
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<2e-7
 for name,z0,z1 in [(BODY,1.02,1.08),(TRAY,.825,.90)]:
  assert abs(min(p[2] for p in vertices[name])-z0)<2e-7 and abs(max(p[2] for p in vertices[name])-z1)<2e-7
 return dict(CONTRACT,geometry_scope='actual source/exported coordinates; complete contacts, whole air/material bodies, separation and independent actual negatives remain required')
INSIDE_TESTS=[(BODY,sub((0,.2,1.05),SHIFT),sub((0,-.3,1.05),SHIFT)),(TRAY,sub((0,-.2,.835),SHIFT),sub((0,-.2,.87),SHIFT))]
FOCUS=(0,0,.60);ORTHO=2.08
CAMERAS={'gray-front3q':(4.5,-6.2,3.7),'gray-back3q':(-4.5,6.2,3.7),'thumbnail':(4.5,-6.2,3.7),'qa-front':(0,-6.8,2.8),'qa-side':(6.8,0,2.8),'qa-top':(0,0,7),'qa-back':(0,6.8,2.8),'qa-wireframe':(4.5,-6.2,3.7),'silhouette-128-front':(0,-6.8,2.8),'silhouette-128-side':(6.8,0,2.8)}
WIRE_THICKNESS=ORTHO/1300

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
root=bpy.data.objects.new('OneRecessFrontWatchmakerBench',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred four-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in INSIDE_TESTS:
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_bench_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'bench_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/timekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'timekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
