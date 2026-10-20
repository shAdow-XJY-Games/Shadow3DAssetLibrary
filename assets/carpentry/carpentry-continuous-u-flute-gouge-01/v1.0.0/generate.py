"""Original longitudinal deep U-flute, continuous root/neck/tang, blind grip and thick through ferrule.
One fixed static visual prop. No prior visible tool geometry is imported or evaluated.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carpentry-continuous-u-flute-gouge-01';VERSION='1.0.0';TITLE='Continuous U-Flute Gouge'
DESCRIPTION=('One original fixed U-flute gouge visual prop, with a deep transverse U channel extending longitudinally to an open front mouth, real finite blunt U lip and external bevel. The complete metal blade, rising root, narrow neck and tang form one closed connected body. One original thick grip has a genuine blind insertion cavity, complete bottom seat and radial clearance around the tang. One thick through-bored ferrule seats on the complete finite grip shoulder with nonzero bore clearance. The blade back and grip bottom each have a full finite ground sole at Z=0. Exactly three editable closed meshes form one asset. Three constant opaque unlinked PBR materials, no textures or transmission. All numerical profiles are new, not an extracted old flat chisel, loop blade, spoon, scraper or compressed shovel. Metres, native Z up, front -Y, complete horizontal envelope centred. One fixed static form only. No cutting, sharpness, strength, hardness, impact, manufacture, fit tolerance, anatomy, operation, load or safety claim. No workpiece, chips, tool rack, scene, second blade or animation. The original chisel-form family remains partial.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FOOT_CONTACTS=[]
BLADE='ContinuousUFluteRootNeckTang';GRIP='ThickBlindCavityGrip';FERRULE='ThickThroughBoredFerrule';FEET=[BLADE,GRIP]
PALETTE=[('SatinSteelAppearance',(.36,.40,.42,1),.43,.65),('WarmWoodAppearance',(.30,.12,.048,1),.76,0),('WarmFerruleAppearance',(.45,.29,.10,1),.46,.60)]
SHIFT=(0.,0.,0.);N=20;HN=20;CX=0.;CZ=.025*math.cos(math.pi/HN)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def area2(poly):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2
def world(p):return add(p,SHIFT)
def point(p,y):return world((p[0],y,p[1]))
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def tri(self,p,mat,tag):self.f.append(tuple(self.vertex(x) for x in p));self.fm.append(mat);self.tags.append(tag)
 def quad(self,a,b,c,d,mat,tag):self.tri([a,b,c],mat,tag);self.tri([a,c,d],mat,tag)
 def result(self,role):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  assert all(len(v)==2 for v in edges.values()),('not closed',[(k,v) for k,v in edges.items() if len(v)!=2][:8])
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':0,'role':role}
def earclip2(poly):
 order=list(range(len(poly))) if area2(poly)>0 else list(reversed(range(len(poly))));out=[]
 def cr(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(order)>3:
  ok=False
  for j,b in enumerate(order):
   a=order[j-1];c=order[(j+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-13:continue
   if any(all(cr(poly[u],poly[v],poly[q])>=-1e-13 for u,v in [(a,b),(b,c),(c,a)]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(j);ok=True;break
  assert ok,('untriangulable polygon',poly,order)
 out.append(tuple(order));return out

def offset(poly,d):
 # Positive offsets move a CCW contour inward. The same finite line
 # intersections also offset concave neck/foot corners; no smoothing proxy.
 reverse=area2(poly)<0
 if reverse:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=(b[0]-a[0],b[1]-a[1]);l=math.hypot(*e);n=(-e[1]/l,e[0]/l);lines.append(((a[0]+d*n[0],a[1]+d*n[1]),e))
 out=[]
 for i,(q,v) in enumerate(lines):
  p,u=lines[i-1];den=u[0]*v[1]-u[1]*v[0]
  if abs(den)<1e-12:
   assert u[0]*v[0]+u[1]*v[1]>0;out.append(q);continue
  t=((q[0]-p[0])*v[1]-(q[1]-p[1])*v[0])/den;out.append((p[0]+t*u[0],p[1]+t*u[1]))
 return list(reversed(out)) if reverse else out

def solid_loft(loops,ys,role,mat=0):
 m=Mesh();n=len(loops[0]);assert all(len(q)==n for q in loops)
 for k in [0,len(ys)-1]:
  for tri in earclip2(loops[k]):m.tri([point(loops[k][i],ys[k]) for i in tri],mat,'End_'+str(k))
 for k in range(len(ys)-1):
  for i in range(n):
   q=(i+1)%n;m.quad(point(loops[k][i],ys[k]),point(loops[k][q],ys[k]),point(loops[k+1][q],ys[k+1]),point(loops[k+1][i],ys[k+1]),mat,'Wall_Layer_'+str(k)+'_Sector_'+str(i))
 return m.result(role)
def tube(stations,role,mat):return solid_loft([circle(r) for y,r in stations],[y for y,r in stations],role,mat)
def annulus(outer,inner,ys,role,mat=1):
 m=Mesh();n=len(inner[0]);assert all(len(q)==n for q in outer+inner)
 for k in [0,len(ys)-1]:
  for i in range(n):
   q=(i+1)%n;m.quad(point(outer[k][i],ys[k]),point(outer[k][q],ys[k]),point(inner[k][q],ys[k]),point(inner[k][i],ys[k]),mat,'AnnularEnd_'+str(k)+'_Sector_'+str(i))
 for k in range(len(ys)-1):
  for label,loops in [('OuterWall',outer),('InnerWall',inner)]:
   for i in range(n):
    q=(i+1)%n;m.quad(point(loops[k][i],ys[k]),point(loops[k][q],ys[k]),point(loops[k+1][q],ys[k+1]),point(loops[k+1][i],ys[k+1]),mat,label+'_Layer_'+str(k)+'_Sector_'+str(i))
 return m.result(role)
# Original cross section: eleven outside points and nine inside points.
# The outside lower facet is a finite back sole; the inner floor remains 5 mm above it.
OUTER=[(-.022,.028),(-.022,.020),(-.018,.009),(-.012,.003),(-.006,0),(.006,0),(.012,.003),(.018,.009),(.022,.020),(.022,.025),(.022,.028)]
INNER=[(.017,.028),(.017,.021),(.013,.012),(.007,.007),(0,.005),(-.007,.007),(-.013,.012),(-.017,.021),(-.017,.028)]
# Split points are intentionally asymmetric on the outer vertical facets, while the visible outline is symmetric.
# At the finite front lip, the external contour rises inward towards (but never reaches) the inner contour.
TIP_OUTER=[(-.0185,.028),(-.0185,.021),(-.0145,.011),(-.008,.0054),(-.003,.0035),(.003,.0035),(.008,.0054),(.0145,.011),(.0185,.021),(.0185,.025),(.0185,.028)]
FLUTE=OUTER+INNER
TIP=TIP_OUTER+INNER
ROOT=list(OUTER)+[(x,.028 if i in [0,8] else .027) for i,(x,z) in enumerate(INNER)]
# The ordered concave cross section continuously closes into a convex 20-sided neck/tang.
NECK=[(.0055*math.cos(math.pi+2*math.pi*i/20),CZ+.0055*math.sin(math.pi+2*math.pi*i/20)) for i in range(20)]
BLADE_Y=[-.175,-.162,-.045,-.018,.004,.028,.084]
BLADE_LOOPS=[TIP,FLUTE,FLUTE,ROOT,NECK,NECK,NECK]
GRIP_STATIONS=[(.035,.013),(.055,.013),(.055,.022),(.075,.025),(.145,.025),(.163,.022),(.175,.017)]
FERRULE_Y=[.035,.055]
TANG_R=.0055;BORE_R=.0075;BLIND_BOTTOM=.084;FERRULE_INNER=.015;FERRULE_OUTER=.020

def circle(r):return [(r*math.cos(-math.pi/2+math.pi/HN+2*math.pi*i/HN),CZ+r*math.sin(-math.pi/2+math.pi/HN+2*math.pi*i/HN)) for i in range(HN)]
def grip(inset=0.,through=False):
 m=Mesh();ys=[y for y,r in GRIP_STATIONS];ys[0]+=inset;ys[-1]-=inset;ys[1]+=inset;ys[2]+=inset;loops=[circle(r-inset) for y,r in GRIP_STATIONS];hole=circle(BORE_R+inset);n=HN;bottom=(ys[-1] if through else BLIND_BOTTOM+inset)
 for k in range(len(ys)-1):
  for i in range(n):
   j=(i+1)%n;m.quad(point(loops[k][i],ys[k]),point(loops[k][j],ys[k]),point(loops[k+1][j],ys[k+1]),point(loops[k+1][i],ys[k+1]),1,'OuterGrip_'+str(k)+'_'+str(i))
 for i in range(n):
  j=(i+1)%n;m.quad(point(loops[0][i],ys[0]),point(loops[0][j],ys[0]),point(hole[j],ys[0]),point(hole[i],ys[0]),1,'FrontAnnularWall_'+str(i))
  m.quad(point(hole[i],ys[0]),point(hole[j],ys[0]),point(hole[j],bottom),point(hole[i],bottom),1,'CompleteBlindBoreWall_'+str(i))
 if through:
  for i in range(n):
   j=(i+1)%n;m.quad(point(loops[-1][i],ys[-1]),point(loops[-1][j],ys[-1]),point(hole[j],ys[-1]),point(hole[i],ys[-1]),1,'FalseThroughRearAnnulus_'+str(i))
 else:
  for tri in earclip2(hole):m.tri([point(hole[i],bottom) for i in tri],1,'CompleteBlindBottom')
  for tri in earclip2(loops[-1]):m.tri([point(loops[-1][i],ys[-1]) for i in tri],1,'WholeGripRear')
 return m.result('One original thick shaped grip with complete blind insertion cavity, true closed bottom and its own finite ground sole.')
G[BLADE]=solid_loft(BLADE_LOOPS,BLADE_Y,'One continuous thick deep U-channel blade, finite blunt open front lip, external bevel, rising root, narrow solid neck and tang.',0)
G[GRIP]=grip()
G[FERRULE]=annulus([circle(FERRULE_OUTER)]*2,[circle(FERRULE_INNER)]*2,FERRULE_Y,'One complete thick through-bored ferrule with full rear annular shoulder seat.',2)
# Three complete inset material solids retain each actual component topology.
by=[y+(.0005 if i==0 else -.0005 if i==len(BLADE_Y)-1 else 0) for i,y in enumerate(BLADE_Y)]
SOLID_VOLUMES['WholeUFluteBevelRootNeckTangMaterial']=dict(solid_loft([offset(p,.00045 if i==0 else .002 if i==3 else .003 if i>3 else .0008) for i,p in enumerate(BLADE_LOOPS)],by,'Full finite blade material interior, every station and wall',0),targets=[BLADE])
SOLID_VOLUMES['WholeBlindGripWallAndBottomMaterial']=dict(grip(.0005),targets=[GRIP])
SOLID_VOLUMES['WholeThickFerruleMaterial']=dict(annulus([circle(FERRULE_OUTER-.0005)]*2,[circle(FERRULE_INNER+.0005)]*2,[.0355,.0545],'Full finite ferrule material interior',2),targets=[FERRULE])
# Whole flute air follows the complete concave floor and both corner regions,
# every length interval, above the rims and through the open front egress.
def channel(poly):
 floor=list(poly[11:]);return floor+[(floor[-1][0],.043),(floor[0][0],.043)]
air_loops=[[(x*.90,z+.0025) for x,z in p[11:]]+[(p[19][0]*.90,.0425),(p[11][0]*.90,.0425)] for p in BLADE_LOOPS[:5]]
VOID_VOLUMES['WholeLongitudinalUChannelAndFrontEgress']=dict(solid_loft([air_loops[0]]+air_loops,[-.195]+BLADE_Y[:5],'Full bounded U air with forward and top egress, including off-axis side corners and root transition'),targets=list(G))
# Full assembled residual annuli exclude only actual occupied tang/wood-neck solids.
VOID_VOLUMES['WholeTangRadialClearance']=dict(annulus([circle(BORE_R-.0005)]*2,[circle(TANG_R+.0005)]*2,[.0345,.0835],'Complete blind cavity residual around solid tang up to finite bottom seat'),targets=list(G))
VOID_VOLUMES['WholeFerruleRadialClearance']=dict(annulus([circle(FERRULE_INNER-.0005)]*2,[circle(.0135)]*2,[.0355,.0545],'Complete residual ferrule bore around handle neck, excluding full rear shoulder seat'),targets=list(G))
ISOLATED_VOID_VOLUMES['IsolatedWholeBlindGripCavity']=dict(solid_loft([circle(BORE_R-.0005)]*2,[.025,.0835],'Complete isolated blind cavity, front egress to finite closed bottom'),targets=[GRIP])
ISOLATED_VOID_VOLUMES['IsolatedWholeFerruleThroughBore']=dict(solid_loft([circle(FERRULE_INNER-.0005)]*2,[.025,.065],'Whole isolated ferrule bore and both end egresses'),targets=[FERRULE])
# No volume overlap is intended. Two finite opposed seats define assembly.
POLY_AREA=lambda r:HN*r*r*math.sin(2*math.pi/HN)/2
CONTACTS=[{'name':'TangCompleteBlindBottomSeat','a':BLADE,'b':GRIP,'origin_m':SHIFT,'u':(1,0,0),'v':(0,0,-1),'axis':(0,1,0),'plane_m':BLIND_BOTTOM,'points':[(0,BLIND_BOTTOM,CZ)],'minimum_patch_area_m2':POLY_AREA(TANG_R)-2e-7,'interior_probe_offset_m':.00035},{'name':'FerruleCompleteRearShoulderSeat','a':FERRULE,'b':GRIP,'origin_m':SHIFT,'u':(1,0,0),'v':(0,0,-1),'axis':(0,1,0),'plane_m':.055,'points':[(.017,.055,CZ)],'minimum_patch_area_m2':POLY_AREA(FERRULE_OUTER)-POLY_AREA(FERRULE_INNER)-2e-7,'interior_probe_offset_m':.00035}]
INSIDE_TESTS=[(BLADE,(0,-.10,.002),(0,-.10,.02)),(GRIP,(0,.10,CZ),(0,.06,CZ)),(FERRULE,(.017,.045,CZ),(0,.045,CZ))]
CONTRACT={'single_prop_count':1,'original_numeric_whole':True,'native_axis_up':'Z','front_direction':'-Y','closed_meshes':3,'materials':3,'blade_station_y_m':BLADE_Y,'deep_u_flute_length_m':.157,'finite_front_blunt_lip':True,'continuous_blade_root_neck_tang':True,'blind_bottom_y_m':BLIND_BOTTOM,'tang_radius_m':TANG_R,'blind_bore_radius_m':BORE_R,'tang_radial_clearance_m':BORE_R-TANG_R,'ferrule_radial_clearance_m':.002,'two_separate_complete_ground_soles_z_m':0,'original_chisel_form_family':'partial','old_geometry_imports':0,'fixed_opaque_visual_only':True}
def measure_gouge_geometry(vertices):
 assert set(vertices)==set(G)
 for name in FEET:assert abs(min(p[2] for p in vertices[name]))<2e-7
 vv=[p for vs in vertices.values() for p in vs]
 for i in [0,1]:assert abs(min(p[i] for p in vv)+max(p[i] for p in vv))<2e-7
 return dict(CONTRACT,scope='Pure source/producer geometry only; independent actual GLB gates required')
FOCUS=(0.,0.,.021);ORTHO=.43
CAMERAS={'gray-front3q':(.8,-1.0,1.0),'gray-back3q':(-.8,1.0,1.0),'thumbnail':(.8,-1.0,1.0),'qa-front':(0,-1.5,.70),'qa-side':(-1.5,0,.75),'qa-top':(0,0,1.5),'qa-back':(0,1.5,.70),'qa-wireframe':(-.8,1.,1.),'silhouette-128-front':(0,-1.5,.70),'silhouette-128-side':(-1.5,0,.75)}
WIRE_THICKNESS=ORTHO/1500

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
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Alpha'].default_value=1.;p.inputs['Transmission Weight'].default_value=0.;p.inputs['Emission Strength'].default_value=0.;mats.append(m)
bpy.context.preferences.filepaths.save_version=0
root=bpy.data.objects.new('OneContinuousUFluteGouge',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='complete horizontal envelope centred, two complete ground soles Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_gouge_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=1800
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'u_flute_gouge_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carpentry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carpentry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
def diagnostic_snapshot():
 return {m:[(i,socket.identifier,socket.bl_idname,tuple(socket.default_value) if hasattr(socket.default_value,'__len__') else socket.default_value) for i,socket in enumerate(m.node_tree.nodes.get('Principled BSDF').inputs) if hasattr(socket,'default_value')] for m in asset_mats}
original_material_inputs=diagnostic_snapshot()
original_slots={o:(list(o.data.materials),[f.material_index for f in o.data.polygons]) for o in parts}
def restore_diagnostic_materials():
 for m,inputs in original_material_inputs.items():
  p=m.node_tree.nodes.get('Principled BSDF')
  for index,identifier,socket_type,value in inputs:
   assert index<len(p.inputs),'Diagnostic socket index disappeared'
   socket=p.inputs[index]
   assert socket.identifier==identifier and socket.bl_idname==socket_type,'Diagnostic socket identity/type changed'
   socket.default_value=value
 for o,(slots,indices) in original_slots.items():
  assert len(o.data.polygons)==len(indices),'Diagnostic face count changed'
  o.data.materials.clear()
  for m in slots:o.data.materials.append(m)
  for f,index in zip(o.data.polygons,indices):f.material_index=index
  assert list(o.data.materials)==slots and [f.material_index for f in o.data.polygons]==indices
 assert diagnostic_snapshot()==original_material_inputs,'Diagnostic full socket-index/identifier/type/value restoration differs'
 assert records(parts)==source_records,'Diagnostic restoration changed complete oriented geometry/full solid PBR signature'
 qa['diagnostic_exact_restoration']={'try_finally':True,'full_socket_index_identifier_type_value_match':True,'all_material_slots_and_face_indices_match':True,'full_oriented_geometry_and_pbr_records_match':True}
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
try:
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
finally:
 restore_diagnostic_materials()
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
