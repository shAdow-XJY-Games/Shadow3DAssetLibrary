"""Original eight-lamella wall-mounted loading-dock bumper; one fixed visual prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='logistics-wall-mounted-laminated-dock-bumper-01';VERSION='1.0.0';TITLE='Wall-mounted Laminated Dock Bumper'
DESCRIPTION=('One original static wall-mounted loading-dock bumper appearance, counted as one prop. Eight thick closed chamfer-cornered lamellae are separated by real full-depth gaps. Every lamella has two complete through holes, carried on two continuous fixed octagonal cross-rods by finite upper internal seats. Two separately bored side brackets support the rods on finite lower seats and meet a complete thick backplate. Four thick end caps meet the rod ends with full finite faces and remain clear of the brackets. Four actual backplate mounting holes pierce its complete thickness. The entire rear mounting face is planar at Y=0.130 m, with every component in the front halfspace; temporary QA wall and mounting bolts are not delivered. All positions fixed, no rotation or elastic operation. Metres, native Z up, front -Y, fixed wall datum; no self-standing or ground-support claim. No textures, labels, vehicle, quay, warehouse scene or reused wheel-chock geometry. Static visual appearance only: no shock absorption, impact resistance, rubber elasticity, vehicle guidance, dock/platform/ship compatibility, anchoring, installation, load capacity, wear, service life, material, manufacture or workplace/port safety certification claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[]
BODY='CompleteFourHoleBackplate';PLATES=[];BRACKETS=[];RODS=[];CAPS=[]
PALETTE=[('BackplateWeatheredBlue',(.075,.19,.22,1),.55,.32),('LamellaGraphite',(.065,.079,.078,1),.78,0),('SideBracketSlateSteel',(.24,.30,.31,1),.44,.62),('RodEndcapsWarmAlloy',(.57,.46,.25,1),.40,.55)]
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
  else:raise AssertionError(('untriangulable planar cell',p,order))
 out.append(tuple(order));return out

def perforated(outline,holes,t0,t1,material=0,role='',transform=lambda p:p):
 # Exact conforming scanline triangulation. Front and back both contain the
 # complete genuine holes; every remaining boundary gets a full-depth side.
 stations=sorted(set(round(x,9) for p in [outline]+holes for x,y in p))
 def interval(poly,x):
  if x<min(a for a,b in poly)-1e-9 or x>max(a for a,b in poly)+1e-9:return None
  yy=[]
  for (a,u),(b,v) in zip(poly,poly[1:]+poly[:1]):
   if abs(b-a)<1e-11:
    if abs(x-a)<1e-9:yy.extend([u,v])
   elif min(a,b)-1e-9<=x<=max(a,b)+1e-9:yy.append(u+(v-u)*(x-a)/(b-a))
  return (min(yy),max(yy)) if yy else None
 pp=[];tt=[];lk={}
 def vid(p):
  p=tuple(round(c,9) for c in p)
  if p not in lk:lk[p]=len(pp);pp.append(p)
  return lk[p]
 def cell(a,b,al,bl,ah,bh):
  right=sorted(set(y for poly in holes for q in [interval(poly,b)] if q for y in q if bl+1e-9<y<bh-1e-9));left=sorted(set(y for poly in holes for q in [interval(poly,a)] if q for y in q if al+1e-9<y<ah-1e-9),reverse=True)
  p=[(a,al),(b,bl)]+[(b,y) for y in right]+[(b,bh),(a,ah)]+[(a,y) for y in left];q=[]
  for r in p:
   r=tuple(round(c,9) for c in r)
   if not q or q[-1]!=r:q.append(r)
  if q[0]==q[-1]:q.pop()
  if len(q)<3:return
  ids=[vid(p) for p in q];tt.extend(tuple(ids[j] for j in tri) for tri in earclip2(q))
 for a,b in zip(stations,stations[1:]):
  aa=interval(outline,a);bb=interval(outline,b);active=sorted((p for p in holes if min(x for x,y in p)<(a+b)/2<max(x for x,y in p)),key=lambda p:interval(p,(a+b)/2)[0]);al,bl=aa[0],bb[0]
  for p in active:
   lo,hi=interval(p,a);ll,hh=interval(p,b);cell(a,b,al,bl,lo,ll);al,bl=hi,hh
  cell(a,b,al,bl,aa[1],bb[1])
 n=len(pp);vv=[(x,y,z) for z in [t0,t1] for x,y in pp];ff=[tuple(reversed(t)) for t in tt]+[tuple(i+n for i in t) for t in tt]
 counts=collections.Counter(tuple(sorted((a,b))) for t in tt for a,b in zip(t,t[1:]+t[:1]))
 for t in tt:
  for a,b in zip(t,t[1:]+t[:1]):
   if counts[tuple(sorted((a,b)))]==1:ff.append((a,b,b+n,a+n))
 return mesh([transform(p) for p in vv],ff,material,role)
def prism(poly,t0,t1,material=0,role='',transform=lambda p:p):
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 n=len(poly);vv=[(x,y,z) for z in [t0,t1] for x,y in poly];tris=earclip2(poly)
 ff=[tuple(reversed(t)) for t in tris]+[tuple(i+n for i in t) for t in tris]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv],ff,material,role)
def octrect(x0,x1,y0,y1,ch):return [(x0+ch,y0),(x1-ch,y0),(x1,y0+ch),(x1,y1-ch),(x1-ch,y1),(x0+ch,y1),(x0,y1-ch),(x0,y0+ch)]
def contact(name,a,b,origin,axis,plane,points,area,offset=.0005):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':origin,'u':u,'v':v,'axis':axis,'plane_m':plane,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=list(G) if targets is None else targets,role=role)
def axial(p):return(p[2],p[0],p[1])
def backmap(p):return(p[0],p[2],p[1])
ROD_Y=-.080;ROD_Z=[.225,.435]
outline=octrect(-.240,.075,.120,.540,.035);bracket_outline=octrect(-.180,.100,.120,.540,.015)
def bore(z,bracket=False,inset=0):
 q=octrect(-.026+inset,.026-inset,-.028+inset,.018-inset,.007)
 return [(ROD_Y+y,z+(-v if bracket else v)) for y,v in q]
def shaft(z,expand=0):return [(ROD_Y+y,z+v) for y,v in octrect(-.018-expand,.018+expand,-.018-expand,.018+expand,.006)]
def installed_air(z,bracket=False):
 q=[(-.0182,.0172),(-.0252,.0102),(-.0252,-.0202),(-.0182,-.0272),(.0182,-.0272),(.0252,-.0202),(.0252,.0102),(.0182,.0172),(.0152,.0172),(.0192,.0132),(.0192,-.0132),(.0132,-.0192),(-.0132,-.0192),(-.0192,-.0132),(-.0192,.0132),(-.0152,.0172)]
 return [(ROD_Y+y,z+(-v if bracket else v)) for y,v in q]
mount_centres=[(x,z) for x in [-.394,.394] for z in [.060,.600]]
mount_holes=[octrect(x-.017,x+.017,z-.017,z+.017,.006) for x,z in mount_centres]
G[BODY]=perforated(octrect(-.440,.440,.010,.650,.018),mount_holes,.100,.130,0,'One complete thick chamfered mounting backplate, four actual full-depth mounting holes, full planar rear face.',backmap)
for i,(lo,hi) in enumerate([(-.370,-.342),(.342,.370)],1):
 n=f'SideBracket_{i}_TwoTrueBores';BRACKETS.append(n);G[n]=perforated(bracket_outline,[bore(z,True) for z in ROD_Z],lo,hi,2,'One closed thick side bracket with two real cross-rod through holes and full finite backplate mounting face.',axial)
 contact(f'Bracket{i}FullBackplateSeat',n,BODY,(0,0,0),(0,1,0),.100,[((lo+hi)/2,.100,.330)],.010)
for j,z in enumerate(ROD_Z,1):
 n=f'ContinuousOctagonalCrossRod_{j}';RODS.append(n);G[n]=prism(shaft(z),-.406,.406,2,'One continuous closed fixed octagonal cross-rod through every lamella and both side brackets.',axial)
 for i,b in enumerate(BRACKETS,1):
  x=[-.356,.356][i-1];contact(f'Rod{j}Bracket{i}LowerFiniteSeat',b,n,(0,0,0),(0,0,1),z-.018,[(x,ROD_Y,z-.018)],.00065)
 for side,x0,x1 in [('Left',-.424,-.406),('Right',.406,.424)]:
  c=f'Rod{j}{side}ThickEndCap';CAPS.append(c);G[c]=prism([(ROD_Y+y,z+v) for y,v in octrect(-.033,.033,-.033,.033,.010)],x0,x1,3,'One thick fixed cap, full finite rod end-face seat; positive complete clearance from bracket.',axial)
  if side=='Left':contact(c+'FiniteRodEnd',c,n,(0,0,0),(1,0,0),x1,[(x1,ROD_Y,z)],.00110)
  else:contact(c+'FiniteRodEnd',n,c,(0,0,0),(1,0,0),x0,[(x0,ROD_Y,z)],.00110)
for i in range(8):
 lo=-.332+i*.084;hi=lo+.076;n=f'Lamella_{i+1:02d}_TwinThroughHoles';PLATES.append(n);G[n]=perforated(outline,[bore(z) for z in ROD_Z],lo,hi,1,'One original full-thickness closed blunt-cornered lamella with two complete cross holes; real air gap from adjacent lamellae.',axial)
 for j,z in enumerate(ROD_Z,1):contact(f'Lamella{i+1}Rod{j}UpperFiniteSeat',RODS[j-1],n,(0,0,0),(0,0,1),z+.018,[((lo+hi)/2,ROD_Y,z+.018)],.00180)
# Whole isolated hole volumes prove that each opening exists through its full
# actual thickness. Installed U-shaped air bodies cover every noncontact side.
for n in PLATES+BRACKETS:
 lo=min(p[0] for p in G[n]['vertices']);hi=max(p[0] for p in G[n]['vertices']);bracket=n in BRACKETS
 for j,z in enumerate(ROD_Z,1):
  name=n+f'Bore{j}';ISOLATED_VOID_VOLUMES[name]=dict(prism(bore(z,bracket,.0008),lo-.001,hi+.001,transform=axial),targets=[n],role='Entire full finite through-hole, all corner facets and both mouths; rod excluded only for this isolated-bore proof.')
  air(name+'InstalledNoncontactU',prism(installed_air(z,bracket),lo-.0008,hi+.0008,transform=axial),'Complete finite U-shaped noncontact bore corridor around the installed rod, full thickness plus both mouths; only the declared finite support face is excluded.')
  BORES.append({'mesh':n,'origin_m':(lo-.001,ROD_Y,z),'direction':(1,0,0),'length_m':hi-lo+.002})
for i,(x,z) in enumerate(mount_centres,1):
 air(f'MountingHole{i}WholeThroughAir',prism(octrect(x-.0162,x+.0162,z-.0162,z+.0162,.006),.099,.131,transform=backmap),'Complete finite mounting-hole air volume through entire backplate and both mouths. No bolt or wall is part of the asset.')
 BORES.append({'mesh':BODY,'origin_m':(x,.099,z),'direction':(0,1,0),'length_m':.032})
# Full lamella gaps and side/end corridors, including all corner facets, are
# perforated only for the two actual continuous rod profiles expanded 1.2 mm.
gap_outline=octrect(-.2392,.0742,.1208,.5392,.035)
for i in range(7):
 lo=-.332+i*.084+.076+.0008;hi=lo+.0064
 air(f'InterLamellaGap{i+1}WholeAir',perforated(gap_outline,[shaft(z,.0012) for z in ROD_Z],lo,hi,transform=axial),'Whole finite inter-lamella air slab across the complete shaped profile; only two actual rod envelopes excluded.')
for side,lo,hi in [('Left',-.3412,-.3328),('Right',.3328,.3412)]:air(side+'LamellaFrameWholeAir',perforated(gap_outline,[shaft(z,.0012) for z in ROD_Z],lo,hi,transform=axial),'Whole finite lamella-to-side-frame air corridor, excluding only actual continuous rods.')
for side,lo,hi in [('Left',-.4052,-.3708),('Right',.3708,.4052)]:air(side+'EndCapBracketWholeAir',perforated(octrect(-.1792,.0992,.1208,.5392,.015),[shaft(z,.0012) for z in ROD_Z],lo,hi,transform=axial),'Full bracket-to-endcap axial corridor across the complete bracket profile; only actual rod envelopes excluded.')
air('WholeLamellaBackplateAir',box((-.3312,.0758,.1208),(.3312,.0992,.5392)),'Whole rear corridor between all lamella backs and the backplate, across the complete assembly width and height.')
SOLID_VOLUMES['BackplateFullCentralBridge']=dict(box((-.383,.106,.102),(.383,.124,.558)),targets=[BODY],role='Full substantial central mounting-plate bridge connecting both side bracket seats; four corner holes remain outside.')
for i,n in enumerate(PLATES,1):
 lo=min(p[0] for p in G[n]['vertices']);hi=max(p[0] for p in G[n]['vertices'])
 SOLID_VOLUMES[n+'CompleteFrontBridge']=dict(box((lo+.001,-.233,.160),(hi-.001,-.110,.500)),targets=[n],role='Whole thick solid front lamella bridge joining both bored support zones.')
MOUNT={'plane_m':.130,'wall_lo':[-.47,.130,-.020],'wall_hi':[.47,.160,.680],'minimum_patch_area_m2':.550,'points':[(-.25,.130,.2),(.25,.130,.45)]}
MOUNT_CONTACT={'name':'CompleteRearMountingFace','a':BODY,'b':'TemporaryQA_Wall_NotAsset','origin_m':(0,0,0),'u':(1,0,0),'v':(0,0,-1),'axis':(0,1,0),'plane_m':.130,'minimum_patch_area_m2':.550,'interior_probe_offset_m':.0005,'points':MOUNT['points']}
SUPPORT_ROOTS=[BODY]
CONTRACT={'single_prop_count':1,'thick_lamellae':8,'lamella_through_holes':16,'continuous_cross_rods':2,'bored_side_brackets':2,'side_bracket_through_holes':4,'thick_end_caps':4,'backplate_through_mounting_holes':4,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'wall_mount_plane_y_m':.130,'wall_exported':False,'ground_support_claimed':False}
def measure_dock_bumper_geometry(vertices):
 assert set(vertices)==set(G)
 assert max(p[1] for v in vertices.values() for p in v)<=.1300002
 for n in PLATES:assert abs(max(p[0] for p in vertices[n])-min(p[0] for p in vertices[n])-.076)<2e-7
 for n in RODS:assert abs(max(p[0] for p in vertices[n])-min(p[0] for p in vertices[n])-.812)<2e-7
 return dict(CONTRACT,geometry_scope='actual source/exported coordinates; full finite mounting, contacts, empty/material volumes and actual geometry negatives remain required')
INSIDE_TESTS=[(BODY,(0,.115,.33),(-.394,.115,.06)),(PLATES[0],(-.30,-.19,.33),(-.30,ROD_Y,.225))]
FOCUS=(0,-.05,.33);ORTHO=1.15
CAMERAS={'gray-front3q':(1.2,-2.3,1.2),'gray-back3q':(-1.2,2.3,1.2),'thumbnail':(1.2,-2.3,1.2),'qa-front':(0,-3,1.1),'qa-side':(3,-.05,1.1),'qa-top':(0,-.05,3),'qa-back':(0,3,1.1),'qa-wireframe':(1.2,-2.3,1.2),'silhouette-128-front':(0,-3,1.1),'silhouette-128-side':(3,-.05,1.1)}
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
root=bpy.data.objects.new('OneWallMountedLaminatedDockBumper',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Fixed wall datum: rear face Y=0.130 m, front -Y, Z up. Wall and bolts omitted; no ground support.';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
# This Blender segment checks closed shells, finite mounting faces, contact areas,
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
seen=set(SUPPORT_ROOTS);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in SUPPORT_ROOTS:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.y-MOUNT['plane_m']) for p in vv)<1.1e-6 and cr.y>0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>=MOUNT['minimum_patch_area_m2'],(name,area)
 supports.append({'name':name,'area_m2':area,'triangles':patch,'rear_plane_y_m':MOUNT['plane_m'],'ground_claim':False})
assert all(p[1]<=MOUNT['plane_m']+2e-7 for g in G.values() for p in g['vertices'])
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
mount_evidence=measure_dock_bumper_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2]-.010)<1e-7 and triangles<12000
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_mount':sorted(seen),
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'dock_bumper_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_mount_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
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
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset';ground.hide_render=True
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
