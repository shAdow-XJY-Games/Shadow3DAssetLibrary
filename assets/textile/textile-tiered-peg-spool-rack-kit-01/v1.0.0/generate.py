"""Original two-tier inclined-peg spool rack; one static visual prop.
Metres, native Z up, front -Y. No motion, manufacture or compatibility claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='textile-tiered-peg-spool-rack-kit-01';VERSION='1.0.0';TITLE='Two-Tier Inclined-Peg Spool Rack'
DESCRIPTION=('One original low-poly free-standing spool rack, counted together as one complete prop. Two ground feet and uprights support two separate crossrails. '
 'Each crossrail carries three forward-and-upward inclined pegs and independent annular end-shoulder seats. Three true through-bore spools sit on their shoulders and three positions remain empty. '
 'Each spool has thick shaped end flanges, a genuinely hollow core and an attached coloured thread wrap. The entire nonbearing peg/bore interface remains positively separated. '
 'Twenty-four editable closed meshes and five opaque constant PBR materials; metres, native Z up, front -Y, horizontally bounds-centred ground origin. '
 'No tray, fabric, loose thread, sewing machine, labels, textures, scene or animation. Static storage-display pose only: no unwinding, weaving, sewing, rotation, insertion/removal path, thread tension, friction, material behaviour, manufacture, load, stability or safety claim. '
 'No compatibility with historical spools, machines or scenes is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];ISOLATED_VOID_VOLUMES={};VOID_VOLUMES={};PEG_SLOTS={};SPOOLS={}
PALETTE=[('Frame_WarmAsh',(.34,.20,.105,1),.55,0),('Shoulder_DarkWalnut',(.13,.073,.037,1),.50,0),('Thread_DesaturatedTeal',(.055,.29,.28,1),.68,0),('Thread_MutedCoral',(.57,.18,.115,1),.68,0),('Thread_Ochre',(.67,.40,.11,1),.68,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
U=(1,0,0);D=(0,-math.cos(math.radians(20)),math.sin(math.radians(20)));V=cross(D,U)
def axial(o,x,y,t):return add(o,add(mul(U,x),add(mul(V,y),mul(D,t))))
def lathe(profile,o,n=24,closed=True):
 vs=[];rings=[];fs=[];segments=[]
 for r,t in profile:
  rr=[]
  for j in range(n if r else 1):
   a=math.tau*j/n;rr.append(len(vs));vs.append(axial(o,r*math.cos(a),r*math.sin(a),t))
  rings.append(rr)
 edges=list(zip(rings,rings[1:]))+([(rings[-1],rings[0])] if closed else [])
 for k,(a,b) in enumerate(edges):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   ff=[(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])]
   fs.extend(ff);segments.extend([k]*len(ff))
 vol=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 return vs,fs,segments,rings

def axial_mesh(name,profile,o,mat,role):
 v,f,segments,rings=lathe(profile,o);mesh(name,v,f,mat,role);G[name].update(face_profile_segments=segments,rings=rings);return name
UPRIGHTS=[];RAILS=[];PEGS=[];SHOULDERS=[];WRAPS=[]
for i,x in enumerate([-.31,.31]):
 foot=box(f'Rack_Foot_{i+1}',(x,0,.016),(.09,.38,.032),1,'finite flat ground foot with broad front and rear support');FEET.append(foot)
 upright=box(f'Rack_Upright_{i+1}',(x,.04,.3075),(.055,.054,.565),0,'independent solid side upright overlapping its ground foot and both crossrails');UPRIGHTS.append(upright);link(foot,upright,(x,.04,.029),axis=(0,1,0),spread=.01)
for row,z in enumerate([.215,.465]):
 rail=box(f'Rack_Crossrail_{row+1}',(0,.035,z),(.64,.060,.060),0,'independent horizontal row rail with three embedded inclined peg roots');RAILS.append(rail)
 for i,x in enumerate([-.31,.31]):link(UPRIGHTS[i],rail,(x,.038,z),axis=(0,0,1),spread=.012)
 for col,x in enumerate([-.205,0,.205]):
  slot=f'Row{row+1}_Slot{col+1}';o=(x,.005,z)
  peg=axial_mesh(slot+'_InclinedPeg',[(0,-.022),(.010,-.022),(.010,.178),(.007,.186),(0,.186)],o,0,'one closed 20-degree upward inclined peg with chamfered exposed tip and embedded rear root');PEGS.append(peg);link(rail,peg,axial(o,0,0,-.013),axis=U,spread=.004)
  shoulder=axial_mesh(slot+'_AnnularShoulder',[(.008,.027),(.028,.027),(.030,.030),(.030,.039),(.008,.039)],o,1,'independent thick annular end shoulder; inner ring is statically embedded 2 mm into its peg and front annulus is the finite spool seat');SHOULDERS.append(shoulder)
  LINKS.append((peg,shoulder,[axial(o,.009*math.cos(a),.009*math.sin(a),.034) for a in[0,math.tau/3,2*math.tau/3]]))
  PEG_SLOTS[slot]={'origin_m':o,'axis':D,'u':U,'v':V,'peg':peg,'shoulder':shoulder,'rail':rail,'occupied':(row,col) in[(0,0),(0,2),(1,1)]}
  if not PEG_SLOTS[slot]['occupied']:continue
  count=len(SPOOLS)+1;core=slot+'_HollowSpool';wrap=slot+'_ThreadWrap'
  profile=[(.014,.039),(.055,.039),(.057,.042),(.057,.047),(.053,.050),(.026,.050),(.026,.137),(.053,.137),(.057,.140),(.057,.145),(.054,.148),(.014,.148)]
  axial_mesh(core,profile,o,0,'one continuous annular spool core with two thick shaped end flanges and a true axial through-bore; finite back end rests on its shoulder')
  wrap_profile=[(.024,.054),(.044,.054)]
  for j in range(9):wrap_profile.extend([(.047,.057+j*.009),(.046,.061+j*.009)])
  wrap_profile.extend([(.044,.133),(.024,.133)])
  axial_mesh(wrap,wrap_profile,o,2+count-1,'one connected coloured thread wrap with restrained geometric winding bands; real radial overlap with spool barrel');WRAPS.append(wrap)
  LINKS.append((core,wrap,[axial(o,.025*math.cos(a),.025*math.sin(a),.089) for a in[0,math.tau/3,2*math.tau/3]]))
  CONTACTS.append({'a':shoulder,'b':core,'origin_m':o,'axis':D,'u':U,'v':V,'plane_m':.039,'minimum_patch_area_m2':.0020,'interior_probe_offset_m':.0003,'points':[axial(o,.021*math.cos(a),.021*math.sin(a),.039) for a in[0,math.tau/4,math.tau/2,3*math.tau/4]],'scope':'complete opposed annular end-face contact perpendicular to the inclined peg; no penetration'})
  SPOOLS[core]={'slot':slot,'origin_m':o,'peg':peg,'shoulder':shoulder,'wrap':wrap,'bore_radius_m':.014,'front_t_m':.148,'back_t_m':.039,'inner_wall_profile_segment':11}
  v,f,_,_=lathe([(0,.037),(.0133,.037),(.0133,.150),(0,.150)],o)
  ISOLATED_VOID_VOLUMES[core]={'vertices':v,'faces':f,'targets':[core,wrap],'role':'entire finite axial through-bore with 0.7 mm radial wall inset and 2 mm projection through both mouths'}
  v,f,_,_=lathe([(.0108,.041),(.0133,.041),(.0133,.147),(.0108,.147)],o)
  VOID_VOLUMES[core+'_AssembledAnnularClearance']={'vertices':v,'faces':f,'targets':list(G),'role':'complete finite annular air around the peg across nearly full spool length, beyond the declared end shoulder contact'}
  BORES.append({'mesh':core,'origin_m':axial(o,0,0,.037),'direction':D,'length_m':.113,'meaning':'supplementary isolated spool centre ray; full finite bore also required'})
# All assembled annular clearance volumes test every final component.
for probe in VOID_VOLUMES.values():probe['targets']=list(G)
RACK_CONTRACT={'single_prop_count':1,'row_count':2,'peg_count':6,'shoulder_count':6,'hollow_spool_count':3,'empty_peg_count':3,'peg_upward_angle_degrees':20,'spool_axial_length_m':.109,'bore_nominal_diameter_m':.028,'peg_nominal_diameter_m':.020,'finite_end_shoulder_contact_required':True,'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_spool_rack_geometry(vertices):
 assert set(vertices)==set(G)
 for name in FEET:
  assert abs(min(p[2] for p in vertices[name]))<2e-7
  assert abs(max(p[2] for p in vertices[name])-.032)<2e-7
 for name,r in SPOOLS.items():
  axial_values=[dot(sub(p,r['origin_m']),D) for p in vertices[name]]
  assert abs(min(axial_values)-.039)<2e-7 and abs(max(axial_values)-.148)<2e-7
 return dict(RACK_CONTRACT,geometry_scope='actual source/exported coordinates; full finite contacts, entire peg and bore surfaces, closed void volumes and negative controls remain separate acceptance requirements')
FOCUS=(0,0,.285);ORTHO=.99
CAMERAS={'gray-front3q':(.95,-1.5,1.12),'gray-back3q':(-.95,1.5,1.12),'thumbnail':(.95,-1.5,1.12),'qa-front':(0,-1.8,.88),'qa-side':(1.8,0,.88),'qa-top':(0,0,2),'qa-back':(0,1.8,.88),'qa-wireframe':(.95,-1.5,1.12),'silhouette-128-front':(0,-1.8,.88),'silhouette-128-side':(1.8,0,.88)}
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
root=bpy.data.objects.new('OneTwoTierSpoolRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.31,0,.016),(-.31,0,.05)),(next(iter(SPOOLS)),axial(SPOOLS[next(iter(SPOOLS))]['origin_m'],.020,0,.09),axial(SPOOLS[next(iter(SPOOLS))]['origin_m'],0,0,.09))]:
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
mount_evidence=measure_spool_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'spool_rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/textile/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'textile','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
