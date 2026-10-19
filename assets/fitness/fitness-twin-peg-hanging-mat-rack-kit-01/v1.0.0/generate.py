"""Original twin parallel peg rack and two identical thick, true-two-hole mats."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fitness-twin-peg-hanging-mat-rack-kit-01';VERSION='1.0.0';TITLE='Twin-peg Hanging Mat Rack'
DESCRIPTION=('One original static H-foot hanging mat rack with two rear uprights, a full upper crossbeam, two parallel long chamfer-section pegs, two finite root braces and two fixed end stops. Two identical original thick mats hang at separate positions along both pegs. Every mat is one continuous gently bowed closed mesh with two true reinforced through-holes; the complete top inner-wall bearing patches rest finitely on both peg tops while all other hole walls remain clear. The entire mats are mutually separated and their whole lower edges remain above ground. Fourteen closed editable meshes, four opaque constant PBR materials, metres, source Z up, front -Y and horizontally bounds-centred ground origin. No texture nodes, linked Principled inputs or imported geometry. Both mats are internal same-source instances, not additional assets. Original geometry, not a shelf, coat hook, spool rack recolour or reused scene mat. Only fixed visual geometry: no yoga training, human suitability, fitting to an earlier mat, insertion/removal trajectory, motion, elastic deformation, gravity sag, loading, strength, anti-tip, material durability, manufacture or safety certification.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];MATS=[];PEGS=[];BRACES=[];HOLE_WALLS={}
BODY='UpperCrossbeam';PALETTE=[('GraphitePowdercoat',(.065,.085,.095,1),.51,.20),('MutedSteelPeg',(.30,.34,.36,1),.42,.65),('DeepTealMat',(.045,.30,.32,1),.81,0),('ReinforcedTealHeader',(.025,.13,.15,1),.72,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def cr2(a,b):return a[0]*b[1]-a[1]*b[0]
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def within(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(within(p[q]) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);break
  else:raise AssertionError(('untriangulable polygon',p,order))
 out.append(tuple(order));return out

def prism(poly,t0,t1,material=0,role='',transform=lambda p:p):
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for z in [t0,t1] for x,y in poly];tris=earclip2(poly)
 ff=[tuple(reversed(t)) for t in tris]+[tuple(i+n for i in t) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv],ff,material,role)
def contact(name,a,b,axis,p,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,p),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0004,'points':points or [p],'scope':scope})
def xprism(poly,x0,x1,material=0,role=''):
 return prism(poly,x0,x1,material,role,transform=lambda p:(p[2],p[0],p[1]))
def void(name,lo,hi,role):VOID_VOLUMES[name]=dict(box(lo,hi),targets=[],role=role)
def solid(name,g,target,role):SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
# Original member dimensions. Every member meets on an entire finite face.
def exactcontact(name,a,b,axis,p,area,scope,points=None):
 contact(name,a,b,axis,p,area-1e-8,scope,points);CONTACTS[-1]['complete_interface_area_m2']=area

def yprism(poly,y0,y1,material=0,role=''):
 return prism(poly,y0,y1,material,role,transform=lambda p:(p[0],p[2],p[1]))
def polyinset(poly,d):
 # Inward parallel offset of each convex profile edge, preserving its complete shape.
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);l=math.hypot(*e);n=(-e[1]/l,e[0]/l);lines.append((n,dot(n,a)+d))
 out=[]
 for i,(b,db) in enumerate(lines):
  a,da=lines[i-1];det=cr2(a,b);out.append(((da*b[1]-a[1]*db)/det,(a[0]*db-da*b[0])/det))
 return out

def member_box(n,lo,hi,mat,role):
 G[n]=box(lo,hi,mat,role);solid(n+'WholeInsetMaterial',box(add(lo,(.001,.001,.001)),sub(hi,(.001,.001,.001))),n,'Whole connected inward-offset member material; complete boundary containment.')
for side,s in [('Left',-1),('Right',1)]:
 x=s*.42;foot=side+'GroundRunner';post=side+'RearUpright'
 member_box(foot,(x-.03,-.42,0),(x+.03,.42,.06),0,'One long continuous flat ground runner of the wide H base.');FEET.append(foot)
 FOOT_CONTACTS.append({'name':side+'WholeGroundSole','mesh':foot,'x':x,'y':0,'half_x':.03,'half_y':.42,'minimum_area_m2':.0504-1e-8,'expected_area_m2':.0504})
 member_box(post,(x-.03,.29,.06),(x+.03,.35,2.00),0,'One continuous rear upright, whole base seated on the ground runner.')
 exactcontact(side+'PostFullBase',foot,post,(0,0,1),(x,.32,.06),.0036,'Entire 60 by 60 mm upright base.')
member_box('BaseCrossTie',(-.39,.29,.018),(.39,.35,.05),0,'Complete transverse H base tie, both full end faces meet runners.')
member_box('UpperCrossbeam',(-.39,.27,1.84),(.39,.35,2.00),0,'Continuous thick upper crossbeam between rear posts, full roots for both rods and braces.')
for side,s in [('Left',-1),('Right',1)]:
 for tie,z,h,y,w in [('BaseCrossTie',.034,.032,.32,.06),('UpperCrossbeam',1.92,.16,.31,.08)]:
  target=side+('GroundRunner' if tie=='BaseCrossTie' else 'RearUpright');a,b=(target,tie) if s<0 else(tie,target)
  # Crossbeam's rear 60 mm is supported by each post; its 20 mm front projection stays free.
  area=h*(.06 if tie=='UpperCrossbeam' else w)
  exactcontact(side+tie+'WholeEnd',a,b,(1,0,0),(s*.39,.32,z),area,'Entire actual finite tie/post end-face intersection; projected front lip is unsupported by the side post.')
PEG_SECTION=[(-.022,1.906),(.022,1.906),(.028,1.912),(.028,1.952),(.022,1.958),(-.022,1.958),(-.028,1.952),(-.028,1.912)]
HOLE_SECTION=[(-.040,1.854),(.040,1.854),(.052,1.866),(.052,1.946),(.040,1.958),(-.040,1.958),(-.052,1.946),(-.052,1.866)]
for side,s in [('Left',-1),('Right',1)]:
 x=s*.23;peg=side+'LongParallelPeg';brace=side+'RootBrace';stop=side+'EndStop';PEGS.append(peg);BRACES.append(brace)
 poly=[(a+x,z) for a,z in PEG_SECTION];G[peg]=yprism(poly,-.36,.27,1,'One continuous long horizontal eight-sided peg; full rear root and finite flat upper bearing surface.')
 solid(peg+'WholeInsetMaterial',yprism(polyinset(poly,.001),-.359,.269),peg,'Whole continuous inset peg including full chamfer profile and complete length.')
 area=abs(sum(cr2(poly[i],poly[(i+1)%8]) for i in range(8)))/2
 exactcontact(side+'PegFullRoot',peg,'UpperCrossbeam',(0,1,0),(x,.27,1.932),area,'Entire octagonal peg end seated at crossbeam front.')
 member_box(stop,(x-.045,-.40,1.888),(x+.045,-.36,1.978),0,'Fixed thick end stop, full peg front-end contact, wholly clear of both mats.')
 exactcontact(side+'StopFullPegEnd',stop,peg,(0,1,0),(x,-.36,1.932),area,'Entire octagonal rod-front end against the bounded stop.')
 poly=[(.10,1.906),(.27,1.906),(.27,1.84),(.24,1.84)]
 G[brace]=xprism(poly,x-.020,x+.020,0,'One finite clipped diagonal root brace, with full top/peg and rear/crossbeam contacts.')
 solid(brace+'WholeInsetMaterial',xprism(polyinset(poly,.001),x-.019,x+.019),brace,'Entire continuous inset clipped brace material, both finite ends preserved.')
 exactcontact(side+'BraceFullPegSeat',brace,peg,(0,0,1),(x,.185,1.906),.040*.17,'Whole 40 by 170 mm flat upper brace face beneath peg.')
 exactcontact(side+'BraceFullBeamRoot',brace,'UpperCrossbeam',(0,1,0),(x,.27,1.873),.040*.066,'Whole 40 by 66 mm rear brace root.')
# A shared row mesh gives two same-source continuous genus-two mat bodies.
# Whole thickness is 24 mm, smoothly thickening to 32 mm at the reinforced header.
MAT_ROWS=[.30,.34,.65,1.05,1.40,1.78,1.82,1.854,1.866,1.946,1.958,2.01,2.05]
def bow(z):
 pts=[(.30,0),(.34,-.003),(.65,-.023),(1.05,-.035),(1.40,-.025),(1.78,0),(2.05,0)]
 for (a,x),(b,y) in zip(pts,pts[1:]):
  if a-1e-9<=z<=b+1e-9:return x+(y-x)*(z-a)/(b-a)
 return 0
def half_thickness(z):return .012+.004*min(1,max(0,(z-1.78)/.04))
def matmesh(center_y,inset=0,holes=True,depth_override=None):
 # Inset shifts complete outer/hole profile boundaries, not a sparse centre sample.
 rows=list(MAT_ROWS);rows[0]+=inset;rows[-1]-=inset
 if inset:
  rows[7]-=inset;rows[8]-=inset*(math.sqrt(2)-1);rows[9]+=inset*(math.sqrt(2)-1);rows[10]+=inset
 def hw(z):
  z0=1.854-inset;z1=1.866-inset*(math.sqrt(2)-1);z2=1.946+inset*(math.sqrt(2)-1);z3=1.958+inset
  if z<=z0:return .040+inset*(math.sqrt(2)-1)
  if z>=z3:return .040+inset*(math.sqrt(2)-1)
  if z<z1:return .040+inset*(math.sqrt(2)-1)+(z-z0)
  if z>z2:return .040+inset*(math.sqrt(2)-1)+(z3-z)
  return .052+inset
 pts=[]
 for z in rows:
  outer=min(.35, .31+(z-.30), .31+(2.05-z))-inset
  w=hw(z);xs=[-outer,-.23-w,-.23+w,.23-w,.23+w,outer]
  pts.extend((x,z) for x in xs)
 faces=[]
 for r in range(len(rows)-1):
  for c in range(5):
   if holes and 7<=r<=9 and c in[1,3]:continue
   faces.append((r*6+c,r*6+c+1,(r+1)*6+c+1,(r+1)*6+c))
 used=sorted(set(i for f in faces for i in f));remap={i:j for j,i in enumerate(used)};pts=[pts[i] for i in used];faces=[tuple(remap[i] for i in f) for f in faces];n=len(pts)
 vertices=[(x,center_y+bow(z)+s*((half_thickness(z)-inset) if depth_override is None else depth_override),z) for s in[-1,1] for x,z in pts]
 edges=collections.Counter(tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1]));boundary=[(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1]) if edges[tuple(sorted((a,b)))]==1]
 ff=[tuple(reversed(f)) for f in faces]+[tuple(i+n for i in f) for f in faces]+[(a,b,b+n,a+n) for a,b in boundary]
 g=mesh(vertices,ff,2,'One original continuous bowed thick mat with two true reinforced octagonal holes, full connected bridges, complete rounded-corner outline and sealed thickness.')
 g['face_materials']=[3 if sum(g['vertices'][i][2] for i in f)/len(f)>1.80 else 2 for f in g['faces']]
 return g
for label,y in [('Front',-.23),('Rear',-.07)]:
 name=label+'WholeTwoHoleMat';MATS.append(name);G[name]=matmesh(y)
 solid(name+'WholeInsetMaterial',matmesh(y,.001),name,'Entire connected two-hole mat material, all upper bridges, side necks, body, rounded corners and continuous thickness.')
 for side,s in [('Left',-1),('Right',1)]:
  x=s*.23;peg=side+'LongParallelPeg'
  exactcontact(label+side+'CompleteHoleTopSeat',peg,name,(0,0,1),(x,y,1.958),.044*.032,'Complete 44 by 32 mm upper peg / hole-ceiling opposed bearing patch.',[(x+dx,y+dy,1.958) for dx in[-.014,0,.014] for dy in[-.009,.009]])
  hp=[(a+x,z) for a,z in HOLE_SECTION];ISOLATED_VOID_VOLUMES[label+side+'WholeIsolatedThroughHole']=dict(yprism(polyinset(hp,.0007),y-.018,y+.018),targets=[name],role='Whole finite through-hole air body beyond both mat faces, checked against its entire mat only. The peg is intentionally excluded from this isolated-hole domain.')
  # One closed U-profile is the full remaining assembled hole air around/below peg.
  # Complete 0.7 mm wall allowance and 0.7 mm peg clearance, no sample rays.
  h=polyinset(hp,.0007);lefttop=h[5];righttop=h[4]
  pp=polyinset([(a+x,z) for a,z in PEG_SECTION],-.0007)
  air=[lefttop,pp[5],pp[6],pp[7],pp[0],pp[1],pp[2],pp[3],pp[4],righttop,h[3],h[2],h[1],h[0],h[7],h[6]]
  # Peg expansion reaches above ceiling; trim its top path to the inset ceiling.
  air[1]=(pp[6][0]+(lefttop[1]-pp[6][1]),lefttop[1]);air[8]=(pp[3][0]-(righttop[1]-pp[3][1]),righttop[1])
  VOID_VOLUMES[label+side+'WholeAssembledHoleAir']=dict(yprism(air,y-.0153,y+.0153),targets=[],role='Complete finite connected U air below and beside the occupied peg, full mat thickness with stated 0.7 mm boundary allowance; excludes only the intentional upper seat.')
  BORES.append({'mesh':name,'origin_m':(x,y-.019,1.872),'direction':(0,1,0),'length_m':.038,'meaning':'Supplemental isolated bore ray, whole closed hole domain remains required.'})
  HOLE_WALLS[label+side]={'mesh':name,'peg':peg,'center_x':x,'center_y':y,'hole_section':hp,'excluded_top_z':1.958,'minimum_nonbearing_wall_clearance_m':.011}
# Whole lower-edge ground clearance and mutually separated complete mat surfaces.
void('WholeLowerEdgesToGroundAir',(-.3507,-.281,.0007),(.3507,-.053,.2993),'Entire bounded air below both complete lower mat edges; no ground-reaching mat segment allowed.')
void('WholeFrameCentralAir',(-.3893,.271,.061),(.3893,.349,1.839),'Complete central H-frame opening under the upper beam, all assembled members checked.')
# Full bowed inter-mat domain follows both whole mats with holes widened by 1 mm.
VOID_VOLUMES['WholeBowedBetweenMatsAir']=dict(matmesh(-.15,.001,depth_override=.062),targets=[],role='Complete bowed between-mat air over the full two-hole mat profile with 1 mm edge/hole allowance; all assembly surfaces checked.')
void('WholeStopToFrontMatClearance',(-.3493,-.3593,1.80),(.3493,-.2467,2.0493),'Whole upper front free interval; peg volumes are excluded by targeted stop and mat checks only.')
VOID_VOLUMES['WholeStopToFrontMatClearance']['targets']=MATS+['LeftEndStop','RightEndStop']
for k,g in VOID_VOLUMES.items():
 if not g['targets']:g['targets']=list(G)
CONTRACT={'single_prop_count':1,'mesh_count':len(G),'mat_count':2,'same_source_mat_instances':True,'holes_per_mat':2,'parallel_pegs':2,'root_braces':2,'end_stops':2,'finite_opposed_contacts':len(CONTACTS),'whole_empty_domains':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_domains':len(SOLID_VOLUMES),'mat_body_thickness_m':.024,'header_thickness_m':.032,'mat_bottom_height_m':.30,'mat_y_translation_m':.16,'each_hole_bearing_area_m2':.044*.032,'fixed_pose_only':True,'ground_exported':False}
def measure_hanging_mat_geometry(vertices):
 assert set(vertices)==set(G) and len(vertices)==14
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 a,b=[vertices[n] for n in MATS];assert len(a)==len(b)
 assert max(abs((v[k]-u[k])-(.16 if k==1 else 0)) for u,v in zip(a,b) for k in range(3))<2e-7
 for n in MATS:assert abs(min(p[2] for p in vertices[n])-.30)<2e-7
 return dict(CONTRACT,geometry_scope='Full original coordinates. Complete contacts, whole air/material domains and entire-surface separation remain independently required.')
INSIDE_TESTS=[('LeftGroundRunner',(-.42,0,.03),(0,0,.03)),('FrontWholeTwoHoleMat',(0,-.23,2.02),(-.23,-.23,1.872))]
FOCUS=(0,0,1.025);ORTHO=2.75
CAMERAS={'gray-front3q':(3.1,-5.0,3.6),'gray-back3q':(-3.1,5.0,3.6),'thumbnail':(3.1,-5.0,3.6),'qa-front':(0,-6,3.2),'qa-side':(6,0,3.2),'qa-top':(0,0,6.0),'qa-back':(0,6,3.2),'qa-wireframe':(3.1,-5.0,3.6),'silhouette-128-front':(0,-6,3.2),'silhouette-128-side':(6,0,3.2)}
WIRE_THICKNESS=ORTHO/1600
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
root=bpy.data.objects.new('OneTwinPegHangingMatRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred H-foot ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_hanging_mat_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'hanging_mat_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fitness/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
