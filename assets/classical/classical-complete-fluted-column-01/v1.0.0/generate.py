"""Original complete sixteen-flute stone-column appearance; no old asset geometry.
Three closed editable parts. Fixed static prop, no historical-order or loading claim.
"""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='classical-complete-fluted-column-01';VERSION='1.0.0';TITLE='Complete Fluted Stone Column'
DESCRIPTION=('One original complete stylised classical stone-column appearance, counted as one static prop. A broad chamfered square plinth supports one continuous turned base, gently tapering shaft with sixteen true longitudinal concave flutes, rounded-off flute ends, a clear neck and annulet, and a thick outward-flaring echinus. A separate thick chamfered square abacus completes the capital. Three closed editable meshes meet at two entire finite opposed planar seats. Flute valleys and shaft ridges share one uniform material: the recesses are geometry, never painted strips. Three constant opaque matte ordinary PBR stone tones, no textures. Metres, native Z up, front -Y, ground-level column-axis origin. All geometry newly authored; no imported plinth, lighthouse, support post, fluted tool or old column. No scene, debris, vegetation, building, carving set, lettering or variants. Static visual appearance only: no archaeological precision, canonical historic order, real material properties, structural capacity, load, stability, manufacture, installation, building safety, collision/navigation, or interface compatibility with previous buildings or modules is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FOOT_CONTACTS=[]
BASE='Plinth_CompleteChamferedSquare';BODY='Shaft_ContinuousSixteenFlutesNeckEchinus';CAP='Capital_ThickSquareAbacus';FEET=[BASE]
PALETTE=[('Plinth_WarmLimestone',(.57,.51,.39,1),.88,0),('Shaft_UniformPaleLimestone',(.74,.68,.54,1),.84,0),('Abacus_WarmPaleStone',(.65,.59,.46,1),.87,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))
N=64;FLUTES=16
# Angular samples ridge, concave shoulder, valley, shoulder. True 42 mm relief.
FLUTE_WEIGHTS=(0.,.62,1.,.62)
BASE_SPEC=[(0,.405,0,'square'),(.025,.43,0,'square'),(.155,.43,0,'square'),(.18,.405,0,'square')]
BODY_SPEC=[(.18,.33,0,'round'),(.205,.355,0,'round'),(.245,.37,0,'round'),(.285,.355,0,'round'),(.325,.315,0,'round'),(.35,.295,0,'round'),(.385,.31,0,'round'),(.415,.31,0,'round'),(.455,.294,0,'round'),(.51,.292,.020,'round'),(.57,.290,.042,'round'),(1.12,.283,.041,'round'),(2.32,.255,.037,'round'),(2.46,.250,.036,'round'),(2.515,.248,.018,'round'),(2.555,.247,0,'round'),(2.605,.247,0,'round'),(2.625,.275,0,'round'),(2.67,.275,0,'round'),(2.685,.255,0,'round'),(2.70,.255,0,'round'),(2.755,.30,0,'round'),(2.815,.36,0,'round'),(2.84,.36,0,'round')]
CAP_SPEC=[(2.84,.405,0,'square'),(2.865,.43,0,'square'),(2.995,.43,0,'square'),(3.02,.405,0,'square')]
def ring(spec,radial_offset=0,z_override=None):
 z,r,d,shape=spec;z=z if z_override is None else z_override;out=[]
 for i in range(N):
  a=math.tau*i/N;c,s=math.cos(a),math.sin(a)
  rr=(r/max(abs(c),abs(s)) if shape=='square' else r-d*FLUTE_WEIGHTS[i%4])+radial_offset
  out.append((rr*c,rr*s,z))
 return out

def profile(specs,mat,role,radial_offset=0,end_inset=0):
 rings=[ring(s,radial_offset,s[0]+(end_inset if i==0 else -end_inset if i==len(specs)-1 else 0)) for i,s in enumerate(specs)]
 vv=[];ff=[];fm=[];tags=[]
 for rr in rings:vv.extend(rr)
 vv.extend([(0,0,rings[0][0][2]),(0,0,rings[-1][0][2])]);bottom=len(vv)-2;top=len(vv)-1
 def f(ids,tag):ff.append(tuple(ids));fm.append(mat);tags.append(tag)
 for i in range(N):j=(i+1)%N;f((bottom,j,i),'CompleteLowerSeat');f((top,(len(rings)-1)*N+i,(len(rings)-1)*N+j),'CompleteUpperSeat')
 for k in range(len(rings)-1):
  for i in range(N):
   j=(i+1)%N;a=k*N+i;b=k*N+j;c=(k+1)*N+j;d=(k+1)*N+i
   f((a,b,c),'ProfileSegment_%02d_Flute_%02d_Facet_%d'%(k,i//4,i%4));f((a,c,d),'ProfileSegment_%02d_Flute_%02d_Facet_%d'%(k,i//4,i%4))
 return {'vertices':[tuple(round(float(c),9) for c in p) for p in vv],'faces':ff,'face_materials':fm,'face_tags':tags,'material':mat,'role':role}
G[BASE]=profile(BASE_SPEC,0,'Complete chamfered square plinth with broad finite flat ground sole and complete upper seat')
G[BODY]=profile(BODY_SPEC,1,'One continuous turned base, sixteen genuinely concave straight axial channels with curved-end taper, gently tapering shaft, full neck and annulet, and thick flared echinus; no internal overlays')
G[CAP]=profile(CAP_SPEC,2,'One thick chamfered square abacus with complete lower bearing seat and full upper stone face')
for a,b,z,r in [(BASE,BODY,.18,.33),(BODY,CAP,2.84,.36)]:
 area=N*.5*r*r*math.sin(math.tau/N)
 CONTACTS.append({'name':a+'_to_'+b,'a':a,'b':b,'origin_m':(0,0,0),'u':(1,0,0),'v':(0,1,0),'axis':(0,0,1),'plane_m':z,'points':[(0,0,z),(.12,0,z),(-.12,0,z),(0,.12,z),(0,-.12,z)],'minimum_patch_area_m2':area-2e-7,'complete_interface_area_m2':area,'interior_probe_offset_m':.0005,'coverage':'complete smaller circular polygon face','role':'Entire finite opposed seat, no intersection/penetration or oversized infinite-plane exemption'})
for name,spec in [(BASE,BASE_SPEC),(BODY,BODY_SPEC),(CAP,CAP_SPEC)]:
 SOLID_VOLUMES[name+'_WholeInsetMaterial']=dict(profile(spec,0,'Complete inward radial-offset material boundary, all face corners and longitudinal grooves',-.014,.003),targets=[name])
# Exact union boundary: remove the three internal seat discs; connect the outer
# plinth/body/cap outlines at their full seat planes with finite annular surfaces.
# Expand radial walls by 14 mm, move the two outward horizontal ledges 6 mm
# toward air and the absolute bottom/top by 6 mm. All clearance is tested.
union=BASE_SPEC+BODY_SPEC+CAP_SPEC
expanded=[]
for i,s in enumerate(union):
 z,r,d,shape=s
 if z==0:z=-.006
 elif z==.18:z=.186
 elif z==2.84:z=2.834
 elif z==3.02:z=3.026
 expanded.append((z,r,d,shape))
AIR_CAVITY=profile(expanded,0,'Whole continuous outward-offset assembled column exclusion boundary',.014)
def boxgeo(lo,hi):
 v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]];quads=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];f=[(a,b,c) for a,b,c,d in quads]+[(a,c,d) for a,b,c,d in quads];return {'vertices':v,'faces':f,'material':0,'role':'finite outer enclosure'}
air=boxgeo((-.85,-.85,-.08),(.85,.85,3.10));off=len(air['vertices']);air['vertices']+=AIR_CAVITY['vertices'];air['faces'] += [tuple(off+i for i in reversed(f)) for f in AIR_CAVITY['faces']]
air.update(targets=list(G),role='One complete finite connected surrounding-air volume including all sixteen groove recesses, between outer box and inward-facing expanded assembled-column exclusion. The 14mm radial/6mm ledge near-surface band is excluded; every exact original oriented surface is separately compared.')
VOID_VOLUMES['WholeSurroundingAirAndSixteenFlutes']=air
INSIDE_TESTS=[(BASE,(0,0,.09),(.6,0,.09)),(BODY,(0,0,1.5),(.5,0,1.5)),(CAP,(0,0,2.93),(.6,0,2.93))]
# Supplementary rays only; the full finite air region above is the main proof.
for i in range(FLUTES):
 a=math.tau*(i*4+2)/N;rr=.265
 GAPS.append({'origin_m':(rr*math.cos(a),rr*math.sin(a),.65),'direction':(0,0,1),'length_m':.40,'targets':[BODY],'meaning':'longitudinal air at lower flute valley, full finite volume separately checked'})
def measure_column_geometry(vertices):
 assert set(vertices)==set(G)
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<2e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<2e-7 for p in actual),(n,'changed geometric boundary')
 return {'single_prop_count':1,'closed_editable_meshes':3,'actual_longitudinal_flute_count':16,'flutes_are_geometry_same_uniform_shaft_material':True,'maximum_authored_flute_depth_m':.042,'full_flute_lower_outer_radius_m':.290,'full_flute_upper_outer_radius_m':.250,'whole_shaft_taper_m':.040,'height_m':3.02,'maximum_square_width_m':.86,'full_finite_internal_seats':2,'complete_flat_ground_sole':1,'historical_order_or_load_or_module_interface_claim':False}
FOCUS=(0,0,1.49);ORTHO=3.95
CAMERAS={'gray-front3q':(5,-7,4.7),'gray-back3q':(-5,7,4.7),'thumbnail':(5,-7,4.7),'qa-front':(0,-10,2.4),'qa-side':(10,0,2.4),'qa-top':(0,0,10),'qa-back':(0,10,2.4),'qa-wireframe':(5,-7,4.7),'silhouette-128-front':(0,-10,2.4),'silhouette-128-side':(10,0,2.4)}
WIRE_THICKNESS=ORTHO/1100

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
root=bpy.data.objects.new('OneCompleteFlutedColumn',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='column-axis ground origin, one complete square sole Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
mount_evidence=measure_column_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert abs(lo[2])<1e-7 and triangles<=5000
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'fluted_column_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; maker gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/classical/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'classical','style':'soft-low-poly-stone','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-3,-4,6),600,4),('Fill',(4,-2,4),360,3.5),('Rim',(2,4,5),480,3)]:
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
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; maker visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
