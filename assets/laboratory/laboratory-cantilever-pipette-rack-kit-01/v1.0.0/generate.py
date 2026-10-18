"""Original three-slot cantilever pipette rack with two static visual pipettes.
Metres, native Z up, front -Y. One complete prop; no experimental use or mechanism.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-cantilever-pipette-rack-kit-01';VERSION='1.0.0';TITLE='Three-Slot Cantilever Pipette Rack'
DESCRIPTION=('One original low-poly tabletop cantilever rack with a wide chamfered ground base, solid rear spine and a single thick projecting comb plate. '
 'Three genuine front-open U slots pass through the plate. Two original static pipette exterior models have recognizable rounded grips, raised thumb buttons, integral finger-rest shoulders and narrow tapered tips. '
 'Each shoulder rests with finite opposed contact on both sides of its fork slot. Both thin shafts and tips are suspended above the base, and the third slot stays empty. '
 'Five named editable closed connected meshes, five opaque constant PBR materials, metres, native Z up, front -Y, bounds-centred ground origin. The complete rack and two pipettes count as one prop. '
 'No labels, liquid, sample tubes, textures, animation, room or additional equipment. Static visual geometry only: no pipetting, aspiration, dispensing, volume measurement, calibration, experiment, sterilization, chemical compatibility, medical use, hygiene, ergonomic, load, stability, manufacture or safety claim. '
 'No insertion/removal trajectory, mechanism motion or compatibility with earlier sample tubes, racks, centrifuges or scenes is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};SLOT_VOLUMES={};TIP_VOLUMES={}
PALETTE=[('Rack_MutedPetrol',(.055,.27,.28,1),.44,0),('Base_Graphite',(.115,.145,.15,1),.51,0),('Grip_WarmPorcelain',(.74,.78,.70,1),.42,0),('Stem_SatinAlloy',(.38,.47,.49,1),.37,.42),('Button_MutedOchre',(.74,.38,.09,1),.42,0)]
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
def extrude(poly,z0,z1):
 # CCW outline, concave front slots are part of the single closed plate boundary.
 a=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))
 if a<0:poly=list(reversed(poly))
 n=len(poly);v=[(x,y,z) for z in[z0,z1] for x,y in poly]
 f=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return v,f
BASE='Rack_WideChamferedBase';SPINE='Rack_SolidRearSpine';FORK='Rack_ThreeFrontOpenForks'
base_poly=[(-.179,-.113),(.179,-.113),(.195,-.097),(.195,.097),(.179,.113),(-.179,.113),(-.195,.097),(-.195,-.097)]
mesh(BASE,*extrude(base_poly,0,.018),1,'one real wide 18 mm thick ground base with finite flat bottom');FEET.append(BASE)
# Real closed trapezoidal rear spine; no rods resembling earlier test-tube racks.
sp=[(-.079,.013),(.079,.013),(.112,.273),(-.112,.273)]
v=[(x,y,z) for y in[.066,.090] for x,z in sp]
f=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
mesh(SPINE,v,f,0,'solid tapered rear spine with finite overlaps into base and rear comb bridge')
link(BASE,SPINE,(0,.077,.015),spread=.035)
SLOT_CENTERS=[-.120,0,.120];SLOT_HALF=.021;SLOT_END_Y=.009;PLATE_TOP=.279;PLATE_BOTTOM=.263;PIPETTE_Y=-.028
outline=[(-.180,-.078)]
for x in SLOT_CENTERS:
 outline.extend([(x-.026,-.078),(x-SLOT_HALF,-.068),(x-SLOT_HALF,SLOT_END_Y)])
 for i in range(1,9):
  a=math.pi-i*math.pi/8;outline.append((x+SLOT_HALF*math.cos(a),SLOT_END_Y+SLOT_HALF*math.sin(a)))
 outline.extend([(x+SLOT_HALF,-.068),(x+.026,-.078)])
outline.extend([(.180,-.078),(.180,.093),(-.180,.093)])
mesh(FORK,*extrude(outline,PLATE_BOTTOM,PLATE_TOP),0,'one continuous 16 mm thick cantilever comb plate with three true front-open rounded U slots')
link(SPINE,FORK,(0,.078,.268),spread=.05)
# Each single connected solid includes the delicate tapered tip, shaft, grip,
# integral finite annular finger rest, neck and raised thumb button.
N=24
PIPETTE_PROFILE=[(0,.055),(.0016,.055),(.0045,.096),(.0058,.172),(.0105,.209),(.0120,.242),(.0120,.279),(.031,.279),(.031,.287),(.022,.293),(.0255,.307),(.027,.335),(.025,.373),(.018,.398),(.011,.404),(.010,.416),(.017,.416),(.017,.428),(.013,.433),(0,.433)]
def lathe(profile,cx,cy,accent):
 vs=[];rings=[];fs=[];fm=[];segments=[]
 for r,z in profile:
  ring=[]
  for i in range(N if r else 1):
   a=math.tau*i/N;ring.append(len(vs));vs.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
  rings.append(ring)
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  mat=3 if k<=4 else accent if k in[6,7,8,14,15,16,17,18] else 2
  for i in range(N):
   j=(i+1)%N
   ff=[(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])]
   fs.extend(ff);fm.extend([mat]*len(ff));segments.extend([k]*len(ff))
 vol=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 return vs,fs,fm,segments,rings
PIPETTES=[]
for index,x in enumerate(SLOT_CENTERS[:2]):
 name=f'Pipette_{index+1}_IntegralGripShoulderStemTipButton';v,f,fm,segments,rings=lathe(PIPETTE_PROFILE,x,PIPETTE_Y,4 if index==0 else 0)
 mesh(name,v,f,2,'one original static pipette exterior: integral shoulder supported on both fork sides, entire stem and tip suspended');G[name].update(face_materials=fm,face_profile_segments=segments,rings=rings)
 PIPETTES.append(name)
 CONTACTS.append({'a':FORK,'b':name,'plane_m':PLATE_TOP,'minimum_patch_area_m2':.00045,'minimum_each_side_area_m2':.00020,'interior_probe_offset_m':.0003,'x_center_m':x,'points':[(x+s*.025,PIPETTE_Y+d,PLATE_TOP) for s in[-1,1] for d in[-.005,0,.005]],'scope':'finite opposed shoulder underside on both fork upper surfaces; no interpenetration'})
 # Finite protected air immediately beneath and around the lower tip.
 TIP_VOLUMES[name]={'vertices':cuboid((x-.016,PIPETTE_Y-.016,.019),(x+.016,PIPETTE_Y+.016,.054)),'faces':BOX_FACES,'role':'full finite air between base top and tip bottom with 1 mm boundary inset'}
for index,x in enumerate(SLOT_CENTERS):
 # Almost the entire slot, with 0.6 mm wall inset. It crosses the front boundary
 # and both plate surfaces. For occupied slots, isolated rack clearance applies.
 r=SLOT_HALF-.0006;poly=[(x-r,-.103),(x+r,-.103),(x+r,SLOT_END_Y)]
 for j in range(1,9):
  a=j*math.pi/8;poly.append((x+r*math.cos(a),SLOT_END_Y+r*math.sin(a)))
 v,f=extrude(poly,PLATE_BOTTOM-.003,PLATE_TOP+.003)
 SLOT_VOLUMES[f'Slot_{index+1}_FullFrontOpenVolume']={'vertices':v,'faces':f,'role':'finite full U opening through both plate surfaces and beyond front lip','targets':[BASE,SPINE,FORK]}
 if index==2:VOID_VOLUMES[f'Slot_{index+1}_EmptyFullAssembly']=dict(SLOT_VOLUMES[f'Slot_{index+1}_FullFrontOpenVolume'],targets=list(G))
 GAPS.append({'origin_m':(x,-.102,.270),'direction':(0,1,0),'length_m':.129,'meaning':f'Slot {index+1} supplementary front-open centre ray','targets':[BASE,SPINE,FORK]})
RACK_CONTRACT={'single_prop_count':1,'slot_count':3,'pipette_count':2,'empty_slot_count':1,'tip_height_m':.055,'base_top_m':.018,'tip_air_height_m':.037,'plate_thickness_m':.016,'shoulder_contact_plane_m':.279,'shaft_slot_minimum_clearance_m':.009,'finite_contact_required_both_sides':True}
def measure_pipette_rack_geometry(vertices):
 assert set(vertices)==set(G)
 bb=vertices[BASE];pp=vertices[FORK]
 assert abs(min(p[2] for p in bb))<1e-7 and abs(max(p[2] for p in bb)-.018)<1e-7
 assert abs(min(p[2] for p in pp)-.263)<1e-7 and abs(max(p[2] for p in pp)-.279)<1e-7
 for name in PIPETTES:
  vv=vertices[name];assert abs(min(p[2] for p in vv)-.055)<1e-7
  assert abs(max(p[2] for p in vv)-.433)<1e-7
 return dict(RACK_CONTRACT,geometry_scope='actual source/exported coordinates; full finite contact, clearance and void acceptance is separately required')
FOCUS=(0,0,.211);ORTHO=.64
CAMERAS={'gray-front3q':(.85,-1.25,.93),'gray-back3q':(-.85,1.25,.93),'thumbnail':(.85,-1.25,.93),'qa-front':(0,-1.6,.72),'qa-side':(1.6,0,.72),'qa-top':(0,0,1.7),'qa-back':(0,1.6,.72),'qa-wireframe':(.85,-1.25,.93),'silhouette-128-front':(0,-1.6,.72),'silhouette-128-side':(1.6,0,.72)}
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
root=bpy.data.objects.new('OneCantileverPipetteRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(BASE,(0,0,.009),(0,0,.04)),(FORK,(.06,0,.270),(.12,-.03,.270))]:
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
 aa=horizontal_triangles(r['a'],r['plane_m'],1);bb=horizontal_triangles(r['b'],r['plane_m'],-1)
 area=sum(clip_area([tuple(p[:2]) for p in a['vertices_m']],[tuple(p[:2]) for p in b['vertices_m']]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,(0,0,r['interior_probe_offset_m']));up=add(p,(0,0,r['interior_probe_offset_m']))
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
mount_evidence=measure_pipette_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'pipette_rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
