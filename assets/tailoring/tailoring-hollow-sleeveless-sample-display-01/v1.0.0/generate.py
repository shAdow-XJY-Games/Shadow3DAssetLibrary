"""Original hollow square-neck sleeveless sample garment on a dedicated twin-shoulder stand; one static prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='tailoring-hollow-sleeveless-sample-display-01';VERSION='1.0.0';TITLE='Hollow Sleeveless Sample Display'
DESCRIPTION=('One original square-neck sleeveless sample garment, with a gently narrowed waist, flared open hem and convex front/back surfaces, on its own thin central post and finite base. The garment is one continuous closed material shell with complete inner and outer surfaces and four genuine openings: neck, both armholes, and the entire hem. A narrow connected yoke has two short broad internal shoulder pads, each contacting a complete finite shoulder underside patch. The isolated garment cavity is empty; the assembled cavity is partitioned around the declared thin post and yoke, and the post passes through the otherwise open hem. No mannequin torso or hidden filler. All fixed pieces together are one prop, and this one form leaves other original sample-garment forms partial/unreviewed. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. Constant opaque PBR only: no TEX_* nodes, linked Principled inputs, image/procedural textures, text, branding or animation. Entire geometry newly authored, neither an extruded clothesline T-shirt nor a converted hat veil or hamper. Static visual appearance only; no body, size, gender or age fit, wearable/dressing action, cloth dynamics, sewing/cutting/manufacturing, comfort, protection, material/load/stability/safety or old-hanger compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='ContinuousHollowSleevelessGarment';YOKE='DedicatedTwinShoulderYoke';POST='ThinCentralDisplayPost';BASE='FiniteGroundDisplayBase'
PALETTE=[('MutedSageSample',(.22,.34,.27,1),.86,0),('WarmBirchShoulderYoke',(.48,.34,.19,1),.65,0),('GraphitePostAndBase',(.045,.058,.056,1),.49,.35)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs]
 # Explicit stable triangulation of every deformed quad; no nonplanar n-gon.
 fs=[(f[0],f[i],f[i+1]) for f in fs for i in range(1,len(f)-1)]
 volume=sum(dot(vv[f[0]],cross(vv[f[1]],vv[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role=''):
 return mesh([(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]],BOX_FACES,material,role)
def grid(xs,ys,zs,occupied,material=0,role='',transform=None):
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};vv=[];ff=[];ids={}
 def vertex(p):
  p=tuple(round(x,9) for x in p)
  if p not in ids:ids[p]=len(vv);vv.append(p)
  return ids[p]
 for i,j,k in sorted(cells):
  cell=[(x,y,z) for z in zs[k:k+2] for y in ys[j:j+2] for x in xs[i:i+2]]
  for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:ff.append(tuple(vertex(cell[n]) for n in face))
 return mesh([transform(p) for p in vv] if transform else vv,ff,material,role)
Z_SHAPE=[(.60,1.,1.),(.78,.88,.93),(.94,.81,.88),(1.10,.93,1.),(1.24,.98,1.03),(1.396,.94,.97)]
X_SHAPE=[-.25,-.244,-.215,-.18,-.14,-.12,-.06,0,.06,.12,.14,.18,.215,.244,.25]
def interp(z,col):
 if z<=Z_SHAPE[0][0]:return Z_SHAPE[0][col]
 if z>=Z_SHAPE[-1][0]:return Z_SHAPE[-1][col]
 for a,b in zip(Z_SHAPE,Z_SHAPE[1:]):
  if a[0]<=z<=b[0]:return a[col]+(b[col]-a[col])*(z-a[0])/(b[0]-a[0])
def convex(x):
 # Piecewise-linear convex front/back profile, with matching tessellation in all domains.
 if x<=X_SHAPE[0]:return 1-.35*(X_SHAPE[0]/.25)**2
 if x>=X_SHAPE[-1]:return 1-.35*(X_SHAPE[-1]/.25)**2
 for a,b in zip(X_SHAPE,X_SHAPE[1:]):
  if a<=x<=b:
   aa=1-.35*(a/.25)**2;bb=1-.35*(b/.25)**2;return aa+(bb-aa)*(x-a)/(b-a)
def shaped(p):
 x,y,z=p;return(x*interp(z,1),y*interp(z,2)*convex(x),z)
def stations(a,b,additional=()):return sorted(set([a,b]+[x for x in additional if a<x<b]))
def shaped_grid(xs,ys,zs,occupied,material=0,role=''):
 xs=sorted(set(xs+[x for x in X_SHAPE if min(xs)<x<max(xs)]));zs=sorted(set(zs+[r[0] for r in Z_SHAPE if min(zs)<r[0]<max(zs)]))
 return grid(xs,ys,zs,occupied,material,role,shaped)
def shaped_box(lo,hi,material=0,role=''):
 return shaped_grid([lo[0],hi[0]],[lo[1],hi[1]],[lo[2],hi[2]],lambda x,y,z:True,material,role)
def garment(e=0,role=''):
 xs=[-.25+e,-.244-e,-.12-e,.12+e,.244+e,.25-e]
 ys=[-.13+e,-.124-e,-.08-e,.08+e,.124+e,.13-e]
 zs=[.60+e,1.10-e,1.31-e,1.39+e,1.396-e]
 def occupied(x,y,z):
  shell=abs(x)>.244+e or abs(y)>.124+e or z>1.39+e
  arm=abs(y)<.08+e and 1.10-e<z<1.39+e
  neck=abs(x)<.12+e and y<.08+e and z>1.31-e
  return shell and not arm and not neck
 return shaped_grid(xs,ys,zs,occupied,0,role)
def contact(name,a,b,z,nominal_rect,points):
 x0,x1,y0,y1=nominal_rect;xx=stations(x0,x1,X_SHAPE);poly=[shaped((x,y0,z)) for x in xx]+[shaped((x,y1,z)) for x in reversed(xx)];area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))/2
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':z,'points':[shaped((x,y,z)) for x,y in points],'minimum_patch_area_m2':area*.9999,'interior_probe_offset_m':.0004,'nominal_entire_patch_rectangle':nominal_rect})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=list(G) if targets is None else targets,role=role)
def isolated(name,g,role):ISOLATED_VOID_VOLUMES[name]=dict(g,targets=[BODY],role=role)
def solid(name,g,target,role):SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
G[BODY]=garment(0,'One newly authored continuous closed thin material shell, four open portals, complete inner/outer panels and thick opening rims, with all shoulder/underarm/waist joins welded into the same surface.')
G[BASE]=box((-.17,-.145,0),(.17,.145,.035),2,'Complete finite flat ground base, not a scenery platform.');FEET.append(BASE)
G[POST]=shaped_box((-.012,-.012,.035),(.012,.012,1.30),2,'Thin continuous central post. It passes through the open hem and stops under the yoke; it is not a mannequin torso.')
yoke_boxes=[((-.215,-.025,1.30),(.215,.025,1.33)),((-.215,-.055,1.33),(-.14,.055,1.39)),((.14,-.055,1.33),(.215,.055,1.39))]
ys=[-.055,-.025,.025,.055];xs=[-.215,-.14,.14,.215];zs=[1.30,1.33,1.39]
G[YOKE]=shaped_grid(xs,ys,zs,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in yoke_boxes),1,'One narrow continuous dedicated yoke with two short broad upper shoulder pads; both top faces are full finite seats, with no fill of the remaining torso cavity.')
contact('PostWholeBaseSeat',BASE,POST,.035,(-.012,.012,-.012,.012),[(0,0)])
contact('YokeWholePostSeat',POST,YOKE,1.30,(-.012,.012,-.012,.012),[(0,0)])
for side,label in [(-1,'Left'),(1,'Right')]:
 x0,x1=(-.215,-.14) if side<0 else (.14,.215)
 contact(label+'WholeShoulderPadSeat',YOKE,BODY,1.39,(x0,x1,-.055,.055),[(side*.1775,0),(side*.15,-.04),(side*.202,.04)])
FOOT_CONTACTS.append({'mesh':BASE,'name':'EntireBaseGroundSole','x':0,'y':0,'minimum_area_m2':.098599,'fixture_lo':[-.171,-.146,-.02],'fixture_hi':[.171,.146,0]})
# Complete whole finite material domains, not isolated witnesses.
solid('WholeGarmentMaterialIncludingFourRimsAndShoulderBridges',garment(.0012),BODY,'One connected complete inset thin material domain across both convex body panels, both sides, both shoulders, all underarm transitions, and the entire four thick opening rims; nominal 1.2 mm boundary inset.')
solid('EntireCentralPost',shaped_box((-.0108,-.0108,.0362),(.0108,.0108,1.2988)),POST,'The whole finite post material, 1.2 mm nominal boundary inset.')
solid('EntireBase',box((-.1688,-.1438,.0012),(.1688,.1438,.0338)),BASE,'Complete finite ground base material with 1.2 mm inset.')
# A connected yoke material domain keeps both shoulders and the full narrow bridge.
solid('EntireYokeAndBothShoulderPads',shaped_grid([-.2138,-.1412,.1412,.2138],[-.0538,-.0238,.0238,.0538],[1.3012,1.3288,1.3312,1.3888],lambda x,y,z:(abs(y)<.0238 and z<1.3288) or (abs(x)>.1412 and (abs(y)<.0238 or z>1.3312)),1),YOKE,'Entire connected inset yoke: narrow transverse bridge, two short full-width shoulder pads and both integral roots. Nominal 1.2 mm inset; roots overlap inside the actual union.')
# Four positive-volume isolated openings, including their entire finite mouth areas.
isolated('WholeIsolatedNeckOpening',shaped_grid([-.1188,.1188],[-.132,-.0788,.0788],[1.3112,1.3888,1.398],lambda x,y,z:y<-.0788 or z>1.3888), 'Complete connected square-neck opening: full 86 mm front neckline cut and top portal, extending beyond the front and upper mouths with 1.2 mm edge margins.')
for side,label in [(-1,'Left'),(1,'Right')]:
 lo,hi=(-.252,-.2428) if side<0 else (.2428,.252)
 isolated('WholeIsolated'+label+'Armhole',shaped_box((lo,-.0788,1.1012),(hi,.0788,1.3888)),'Entire '+label.lower()+' armhole from inside the body through and beyond the side wall, including its full height/depth with 1.2 mm edge margins.')
isolated('WholeIsolatedOpenHem',shaped_box((-.2428,-.1228,.598),(.2428,.1228,.6012)),'The entire isolated garment hem cross-section is open, 1.2 mm perimeter margin; the stand is deliberately excluded from this isolated test.')
isolated('WholeIsolatedBodyCavity',shaped_box((-.2428,-.1228,.6012),(.2428,.1228,1.3888)),'The complete continuous body cavity from hem to shoulder undersides, including front/back curves and waist, independent of its dedicated stand; 1.2 mm boundary margins.')
# Assembly air is explicitly the same entire cavity minus bounded stand envelopes.
# The removed envelopes include the exact post/yoke occupancy plus a 1.2 mm
# nominal clearance jacket. The shoulder seat plane is excluded, not called air.
EXCLUSIONS=[((-.0132,-.0132,.597),(.0132,.0132,1.3012)),((-.2162,-.0262,1.2988),(.2162,.0262,1.3312)),((-.2162,-.0562,1.3288),(-.1388,.0562,1.3912)),((.1388,-.0562,1.3288),(.2162,.0562,1.3912))]
def assembly_cavity(lo,hi):
 st=[stations(lo[k],hi[k],[p[k] for b in EXCLUSIONS for p in b]) for k in range(3)]
 return shaped_grid(*st,lambda x,y,z:not any(all(a[k]<p<b[k] for k,p in enumerate([x,y,z])) for a,b in EXCLUSIONS))
air('WholeAssembledBodyAirAroundPostAndYoke',assembly_cavity((-.2428,-.1228,.6012),(.2428,.1228,1.3888)),'Entire connected assembled cavity, with only the explicit post/yoke occupancy and 1.2 mm nominal clearance jackets removed. Includes full front/back, side, waist and under-shoulder air; no mannequin filler.')
air('WholeAssembledHemAirAroundPost',assembly_cavity((-.2428,-.1228,.598),(.2428,.1228,.6012)),'Entire assembled hem opening except the declared thin post plus its 1.2 mm margin; does not claim that the installed hem is empty of the post.')
for name in ['WholeIsolatedNeckOpening','WholeIsolatedLeftArmhole','WholeIsolatedRightArmhole']:
 g=ISOLATED_VOID_VOLUMES[name];air(name.replace('Isolated','Assembled'),g,g['role']+' Tested against the entire assembled prop.')
SHIFT=(0,0,0)
CONTRACT={'single_prop_count':1,'original_sample_forms_covered':1,'remaining_original_sample_form_family':'partial/unreviewed','closed_connected_garment_material_shells':1,'genuine_openings':4,'dedicated_shoulder_pad_seats':2,'thin_central_posts':1,'finite_ground_bases':1,'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'nominal_material_thickness_m':.006,'isolated_vs_assembled_void_scope_separated':True,'wearable_cloth_or_safety_claim':False}
def measure_sample_garment_geometry(vertices):
 assert set(vertices)==set(G)
 v=vertices[BODY];assert abs(min(p[2] for p in v)-.60)<2e-7 and abs(max(p[2] for p in v)-1.396)<2e-7
 assert max(p[1] for p in v)-min(p[1] for p in v)>.25,'Body compressed into flat clothesline slab'
 assert abs(min(p[2] for p in vertices[BASE]))<2e-7
 return dict(CONTRACT,geometry_scope='actual full source/export coordinates; complete finite material/air domains, contacts, whole-surface self-crossing and real negative gates remain required')
INSIDE_TESTS=[(BODY,shaped((0,-.127,.94)),shaped((0,0,.94))),(YOKE,shaped((.18,0,1.36)),shaped((.08,.05,1.36))),(POST,shaped((0,0,.70)),shaped((.03,0,.70)))]
FOCUS=(0,0,.698);ORTHO=1.86
CAMERAS={'gray-front3q':(2.8,-4,2.5),'gray-back3q':(-2.8,4,2.5),'thumbnail':(2.8,-4,2.5),'qa-front':(0,-6,2.0),'qa-side':(6,0,2.0),'qa-top':(0,0,6),'qa-back':(0,6,2.0),'qa-wireframe':(2.8,-4,2.5),'silhouette-128-front':(0,-6,2.0),'silhouette-128-side':(6,0,2.0)}
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
root=bpy.data.objects.new('OneHollowSleevelessSampleDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred single-base ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_sample_garment_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'sample_garment_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/tailoring/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'tailoring','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
