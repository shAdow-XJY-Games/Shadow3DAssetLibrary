"""Original continuous thick folded kneading dough mass; one fixed static visual prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='bakery-folded-kneading-dough-mass-01';VERSION='1.0.0';TITLE='Folded Kneading Dough Mass'
DESCRIPTION=('One original irregular broad thick folded dough mass, counted as one fixed static prop. A single closed continuous body has a plump asymmetric broad base, a thick returning lip, a true deep open fold slit and one complete solid rear root bridge. The entire finite bottom is flat at ground level. The fold is actual empty volume bounded by continuous dough surfaces, not an applied line, intersecting capsules, floating strip, scored round loaf or stripped crescent pastry. One editable closed mesh and one opaque constant unlinked pale dough PBR material. Metres, native Z up, front -Y, horizontally bounds-centred ground origin. No plate, bowl, rolling pin, flour, text, texture, scene, imported historical shape or animation. Only a fixed static visual shape: no eating, recipe, allergens, nutrition, kneading deformation, fermentation, baking process, hygiene, food-contact safety, manufacturing or compatibility with prior utensils is represented.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[]
BODY='Continuous_ThickFoldedDoughBody'
PALETTE=[('RawDough_PaleWarmCream',(.69,.54,.34,1),.82,0)]
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
def box(lo,hi,material=0,role=''):
 return mesh([(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]],BOX_FACES,material,role)
def earclip2(p):
 order=list(range(len(p)));out=[]
 if sum(cr2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))<0:order.reverse()
 while len(order)>3:
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)]
   if cr2(sub(p[b],p[a]),sub(p[c],p[b]))<=1e-14:continue
   def within(q):return all(cr2(sub(y,x),sub(q,x))>=-1e-14 for x,y in [(p[a],p[b]),(p[b],p[c]),(p[c],p[a])])
   if any(within(p[q]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(i);break
  else:raise AssertionError(('untriangulable polygon',p,order))
 out.append(tuple(order));return out

def inset(poly,d):
 if sum(cr2(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<0:poly=list(reversed(poly))
 lines=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a);l=math.hypot(*e);n=(-e[1]/l,e[0]/l);lines.append((n,dot(n,a)+d))
 out=[]
 for i,(b,db) in enumerate(lines):
  a,da=lines[i-1];det=cr2(a,b)
  if abs(det)<1e-12:
   # Collinear consecutive edges retain the exact inset point.
   out.append(add(poly[i],mul(b,d)));continue
  out.append(((da*b[1]-a[1]*db)/det,(a[0]*db-da*b[0])/det))
 return out
# Simple concave section in Y,Z: complete bottom, rounded outer rear/top,
# thick returning lip, rounded deep slit terminus, lower folded mass.
PROFILE=[(-.225,.016),(-.216,0),(-.14,0),(.02,0),(.145,0),(.205,.015),(.245,.050),(.255,.105),(.24,.156),(.205,.191),(.145,.210),(.06,.217),(-.035,.204),(-.105,.188),(-.156,.164),(-.18,.141),(-.181,.124),(-.165,.112),(-.13,.111),(-.065,.119),(.02,.131),(.095,.135),(.145,.125),(.164,.107),(.157,.090),(.132,.081),(.065,.077),(-.025,.071),(-.11,.062),(-.174,.056),(-.215,.045),(-.231,.030)]
# Explicit irregular side taper; each interval is an affine ruled loft.
# Endpoint caps are real closed concave dough sections, not detached overlays.
RINGS=[(-.290,.28,.48,-.007),(-.275,.49,.66,-.013),(-.240,.75,.84,-.022),(-.180,.94,.96,-.018),(-.110,1.01,1.00,-.009),(-.040,1.04,1.02,.003),(.040,1.00,1.00,.016),(.110,.98,.95,.020),(.180,.88,.90,.016),(.235,.68,.78,.009),(.265,.47,.62,.003),(.280,.30,.48,.000)]
SHIFT_X=.005;SHIFT_Y=0

def ring_at(x):
 for a,b in zip(RINGS,RINGS[1:]):
  if a[0]-1e-12<=x<=b[0]+1e-12:
   u=(x-a[0])/(b[0]-a[0]);return(x,)+tuple(a[i]*(1-u)+b[i]*u for i in range(1,4))
 raise AssertionError(x)
def transform(r,p):
 x,sy,sz,cy=r;y,z=p;return(x+SHIFT_X,y*sy+cy+SHIFT_Y,z*sz)
def loft(poly,rings=None,role=''):
 rings=RINGS if rings is None else rings;n=len(poly);vv=[transform(r,p) for r in rings for p in poly];ff=[]
 # Explicit triangles ensure source/GLB triangulation cannot choose diagonals.
 for i in range(len(rings)-1):
  for j in range(n):
   a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j;ff.extend([(a,b,c),(a,c,d)])
 for t in earclip2(poly):ff.append(tuple(reversed(t)));ff.append(tuple((len(rings)-1)*n+j for j in t))
 return mesh(vv,ff,0,role)
raw=loft(PROFILE);SHIFT_Y=-(min(p[1] for p in raw['vertices'])+max(p[1] for p in raw['vertices']))/2
G[BODY]=loft(PROFILE,role='One complete closed thick mass. Every cross-section is one simple C-like folded solid: whole lower body, continuous rear root bridge and thick returning upper lip. Entire fold slit remains actual air. All lateral caps are concave complete sections, with no seam overlays.')
FEET=[BODY]
DOMAIN_RINGS=[ring_at(RINGS[0][0]+.003)]+RINGS[1:-1]+[ring_at(RINGS[-1][0]-.003)]
SOLID_VOLUMES['WholeInsetContinuousBaseRootAndLip'] = dict(loft(inset(PROFILE,.004),DOMAIN_RINGS),targets=[BODY],role='Entire continuous material body: full base/bottom, all lateral ends, complete rear root, entire thick lip and every fold corner. Cross-sectional 4 mm inward allowance, and 3 mm lateral end allowance; no isolated center witness.')
# Full bounded slit runs through the entire material-width X interval. The
# only clipped opening boundary is the explicit front mouth plane y=-.235.
VOID_PROFILE=[(-.235,.047),PROFILE[30],*list(reversed(PROFILE[16:30])),(-.235,.124)]
# PROFILE[30], reverse[29..16] traces floor->root->lip underside.
VOID_VOLUMES['WholeDeepFoldSlitAndFrontMouth']=dict(loft(inset(VOID_PROFILE,.004),DOMAIN_RINGS),targets=[BODY],role='Complete finite deep fold slit, including full rounded terminus and all underside/floor facets, across the full X interval with 3 mm end allowance and 4 mm boundary allowance. Includes front mouth to explicit y=-.235 section plane; no center-ray substitute.')
# Root and lip are additionally named connected material subdomains rather
# than unrelated boxes: half-plane-clipped complete inset material sections.
def clip_yz(poly,axis,value,keep_positive):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-value)*(1 if keep_positive else -1);db=(b[axis]-value)*(1 if keep_positive else -1)
  if da>=0:out.append(a)
  if (da>=0)!=(db>=0):out.append(add(a,mul(sub(b,a),da/(da-db))))
 return out
ROOT_PROFILE=clip_yz(inset(PROFILE,.005),0,.177,True)
LIP_PROFILE=clip_yz(inset(PROFILE,.005),1,.145,True)
SOLID_VOLUMES['WholeRearRootBridge']=dict(loft(ROOT_PROFILE,DOMAIN_RINGS),targets=[BODY],role='Complete rear material bridge behind the full slit terminus, from lower to upper body, across the whole X span, bounded forward at local Y=.177 and inset 5 mm from exterior.')
SOLID_VOLUMES['WholeReturningThickUpperLip']=dict(loft(LIP_PROFILE,DOMAIN_RINGS),targets=[BODY],role='Entire upper thick return above local Z=.145, all the way across X, including both side ends and forward upper lip. Complementary whole-body material domain covers the rounded lip underside.')
# Complete finite ground patch is computed from the actual entire flat base.
vs=G[BODY]['vertices'];ground_faces=[f for f in G[BODY]['faces'] if all(abs(vs[i][2])<1e-12 for i in f)]
GROUND_AREA=sum(math.sqrt(dot(cross(sub(vs[f[1]],vs[f[0]]),sub(vs[f[2]],vs[f[0]])),cross(sub(vs[f[1]],vs[f[0]]),sub(vs[f[2]],vs[f[0]]))))/2 for f in ground_faces)
FOOT_CONTACTS=[{'name':'WholeFlatDoughBottom','mesh':BODY,'x':0,'y':0,'half_x':.31,'half_y':.30,'minimum_area_m2':GROUND_AREA-1e-8,'expected_area_m2':GROUND_AREA}]
CONTRACT={'single_prop_count':1,'mesh_count':1,'continuous_folded_thick_body':1,'entire_deep_slit_domains':len(VOID_VOLUMES),'whole_material_domains':len(SOLID_VOLUMES),'full_finite_flat_bottom_area_m2':GROUND_AREA,'cross_section_vertices':len(PROFILE),'whole_x_sections':len(RINGS),'solid_rear_root':True,'thick_returning_lip':True,'ground_exported':False,'fixed_static_visual_only':True}
def measure_folded_dough_geometry(vertices):
 assert set(vertices)=={BODY};v=vertices[BODY];assert abs(min(p[2] for p in v))<2e-7
 assert len(v)==len(PROFILE)*len(RINGS)
 return dict(CONTRACT,geometry_scope='Actual whole closed boundary coordinates, complete finite empty/material domain and self-intersection proof separately required. Static appearance only.')
INSIDE_TESTS=[(BODY,(0,SHIFT_Y,.03),(0,SHIFT_Y,.10)),(BODY,(0,.215+SHIFT_Y,.105),(0,-.15+SHIFT_Y,.085))]
FOCUS=(0,0,.105);ORTHO=.85
CAMERAS={'gray-front3q':(1.25,-2.5,1.35),'gray-back3q':(-1.25,2.5,1.45),'thumbnail':(1.25,-2.5,1.35),'qa-front':(0,-3,.72),'qa-side':(3,0,1.1),'qa-top':(0,0,3.0),'qa-back':(0,3,1.05),'qa-wireframe':(1.25,-2.5,1.35),'silhouette-128-front':(0,-3,.72),'silhouette-128-side':(3,0,1.1)}
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
root=bpy.data.objects.new('OneContinuousFoldedDoughMass',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred complete flat bottom ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_folded_dough_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'folded_dough_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/bakery/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'bakery','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
