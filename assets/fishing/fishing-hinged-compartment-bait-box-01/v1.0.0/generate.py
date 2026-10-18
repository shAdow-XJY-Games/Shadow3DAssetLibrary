"""One original low hard-shell six-compartment bait box with fixed raised lid.
Metres, native Z up, front -Y. Static decorative geometry only, no hinge motion.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fishing-hinged-compartment-bait-box-01';VERSION='1.0.0';TITLE='Six-Compartment Hinged Bait Box'
DESCRIPTION=('One original low-poly low hard-shell empty bait box. A single closed tray mesh has a real thick bottom, four outer walls and an open interior, divided into six shallow rectangular compartments by three finitely connected solid partitions. A thick hard lid with a shallow recessed interior stays in one fixed raised pose. Two complete hinge assemblies each have three genuinely bored annular knuckles, two body brackets, a lid tongue and one fixed pin with finite static overlap in the hole walls. Two small front latch plates are fixed appearance only. One complete grounded assembly counts as one prop. Metres, native Z up, front -Y, origin centered on the box footprint at ground. Opaque constant PBR colors only; no textures, contents, hooks, sharp fittings, floats, line, duplicate box or scene. '
 'Static visual geometry only: no lid opening path, hinge motion, animation, latch closure testing, sealing, waterproofness, corrosion resistance, bait or food-contact suitability, storage capacity, physical tool fit, load rating, stability, anti-tip performance, manufacture or safety certification. No compatibility asserted with existing fishing floats, eyepieces, tools or scenes.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};ISOLATED_VOIDS={};HINGES=[]
PALETTE=[('Shell_DeepPetrol',(.035,.20,.22,1),.43,0),('Interior_PaleStone',(.62,.67,.59,1),.62,0),('Latch_WarmOchre',(.78,.43,.10,1),.45,.15),('Hinge_Graphite',(.12,.15,.16,1),.37,.55)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
def tray_geometry(hx,hy,z0,zt,ix,iy,floor):
 v=[]
 for x,y,z in[(hx,hy,z0),(hx,hy,zt),(ix,iy,zt),(ix,iy,floor)]:v.extend([(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)])
 f=[(3,2,1,0),(12,13,14,15)]
 for i in range(4):
  j=(i+1)%4;f.extend([(i,j,j+4,i+4),(i+4,j+4,j+8,i+8),(i+8,j+8,j+12,i+12)])
 return v,f

def cylinder_geometry(p,q,r,n=16):
 p=tuple(p);q=tuple(q);axis=unit(sub(q,p));u=unit(cross(axis,(0,0,1) if abs(axis[2])<.9 else(0,1,0)));v=cross(axis,u)
 vv=[add(c,mul(add(mul(u,math.cos(j*math.tau/n)),mul(v,math.sin(j*math.tau/n))),r)) for c in[p,q] for j in range(n)]
 ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 return vv,ff

def cylinder(name,p,q,r,mat,role,n=16):return mesh(name,*cylinder_geometry(p,q,r,n),mat,role)
def annulus_geometry(x0,x1,y,z,ro,ri,n=16):
 v=[(x,y+r*math.cos(j*math.tau/n),z+r*math.sin(j*math.tau/n)) for x,r in[(x0,ro),(x1,ro),(x0,ri),(x1,ri)] for j in range(n)];f=[]
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j,j+n,i+n),(i+2*n,i+3*n,j+3*n,j+2*n),(i,i+2*n,j+2*n,j),(i+n,j+n,j+3*n,i+3*n)])
 return v,f

tray=mesh('Shell_ContinuousBottomAndFourWalls',*tray_geometry(.28,.17,0,.100,.265,.155,.017),0,'single closed manifold shell: 17 mm solid bottom and 15 mm walls, open top; no filled block or black plane')
G[tray]['face_materials']=[0,1]+[m for _ in range(4) for m in[0,0,1]];FEET.append(tray)
partitions=[]
for i,x in enumerate([-.09,.09]):
 p=box('Partition_Long_'+str(i+1),(x,0,.050),(.009,.320,.080),1,'real 9 mm wall, overlaps bottom by 7 mm and the rear/front walls by 5 mm')
 partitions.append(p);link(tray,p,(x,.10,.014),axis=(0,1,0),spread=.025)
crosspart=box('Partition_Cross',(0,0,.0515),(.542,.011,.085),1,'11 mm cross partition, real 8 mm floor overlap and 6 mm side-wall overlap; top staggered to avoid coincident caps')
partitions.append(crosspart);link(tray,crosspart,(.15,0,.013),spread=.025)
for p,x in zip(partitions[:2],[-.09,.09]):link(p,crosspart,(x,0,.050),axis=(0,0,1),spread=.015)
# Six complete finite closed compartment interiors, with 0.4 mm boundary inset.
XSPANS=[(-.265,-.0945),(-.0855,.0855),(.0945,.265)];YSPANS=[(-.155,-.0055),(.0055,.155)]
for row,(y0,y1) in enumerate(YSPANS):
 for col,(x0,x1) in enumerate(XSPANS):
  name=f'Compartment_Row{row+1}_Col{col+1}';lo=(x0+.0004,y0+.0004,.0174);hi=(x1-.0004,y1-.0004,.104)
  VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':'entire rectangular compartment free volume up to above rim, excluding only 0.4 mm boundary inset','inner_boundary_m':[(x0,y0,.017),(x1,y1,.104)],'boundary_inset_m':.0004}
  GAPS.append({'origin_m':((x0+x1)/2,(y0+y1)/2,.018),'direction':(0,0,1),'length_m':.09,'meaning':name+' supplementary open-top ray; complete volume is authoritative'})
HINGE_Y=.186;HINGE_Z=.110;T=(0,.35,math.sqrt(1-.35**2));N=(0,-T[2],T[1])
def lidpoint(x,s,w):return add((x,HINGE_Y,HINGE_Z),add(mul(T,s),mul(N,w)))
v,f=tray_geometry(.28,.165,-.007,.010,.264,.149,.002)
lid=mesh('Lid_FixedRaisedRecessedHardShell',[lidpoint(x,y+.182,w) for x,y,w in v],f,0,'one thick rigid lid in a fixed raised pose; shallow true inset; no kinematic path or animation')
G[lid]['face_materials']=[0,1]+[m for _ in range(4) for m in[0,0,1]]
for index,c in enumerate([-.19,.19]):
 rings=[];brackets=[]
 for side,a,b in[('Left',c-.035,c-.015),('Right',c+.015,c+.035)]:
  ring=mesh(f'Hinge_{index+1}_BodyKnuckle_{side}',*annulus_geometry(a,b,HINGE_Y,HINGE_Z,.014,.006),3,'true 12 mm diameter through bore; fixed pin embeds by finite overlap, no rotational fit claim')
  bracket=box(f'Hinge_{index+1}_BodyBracket_{side}',((a+b)/2,.177,.089),(.016,.030,.026),0,'thick bracket overlaps rear shell wall and lower knuckle arc')
  link(tray,bracket,((a+b)/2,.166,.085),axis=(0,0,1),spread=.004)
  link(bracket,ring,((a+b)/2,HINGE_Y,.100),spread=.003)
  rings.append(ring);brackets.append(bracket)
 middle=mesh(f'Hinge_{index+1}_LidKnuckle',*annulus_geometry(c-.012,c+.012,HINGE_Y,HINGE_Z,.014,.006),3,'central true-bore knuckle, 3 mm positive axial gaps to both body knuckles')
 tongue=mesh(f'Hinge_{index+1}_LidTongue',[lidpoint(x,s,w) for x,s,w in cuboid((c-.009,.008,-.004),(c+.009,.028,.004))],BOX_FACES,0,'rigid tongue embedded in lid bottom and upper knuckle arc')
 link(middle,tongue,lidpoint(c,.010,0),spread=.003)
 link(tongue,lid,lidpoint(c,.023,-.002),spread=.003)
 rings.append(middle)
 pin=cylinder(f'Hinge_{index+1}_FixedPin',(c-.040,HINGE_Y,HINGE_Z),(c+.040,HINGE_Y,HINGE_Z),.0068,2,'one fixed polygonal pin; 0.8 mm nominal radial overlap into bore walls for finite static contact; not moving/machined fit')
 for r in rings:
  vv=G[r]['vertices'];a=min(p[0] for p in vv);b=max(p[0] for p in vv)
  link(pin,r,((a+b)/2,HINGE_Y+.0064,HINGE_Z),spread=.003)
  probe_v,probe_f=cylinder_geometry((a-.001,HINGE_Y,HINGE_Z),(b+.001,HINGE_Y,HINGE_Z),.0057,16)
  ISOLATED_VOIDS[r]={'vertices':probe_v,'faces':probe_f,'role':'whole finite isolated through-bore volume, with radial inset; assembled pin deliberately occupies bore'}
  BORES.append({'mesh':r,'origin_m':(a-.001,HINGE_Y,HINGE_Z),'direction':(1,0,0),'length_m':b-a+.002,'meaning':'supplementary isolated through-bore ray; finite isolated volume also tested'})
 HINGES.append({'rings':rings,'brackets':brackets,'tongue':tongue,'pin':pin,'center_x_m':c,'nominal_hole_radius_m':.006,'nominal_pin_radius_m':.0068,'nominal_outer_radius_m':.014,'static_radial_overlap_m':.0008,'positive_axial_gap_m':.003})
for i,x in enumerate([-.16,.16]):
 latch=box('Front_FixedLatchPlate_'+str(i+1),(x,-.176,.065),(.040,.018,.040),2,'small fixed front appearance plate; no tested closure or latch motion')
 link(tray,latch,(x,-.168,.065),axis=(1,0,0),spread=.010)
BOX_CONTRACT={'tray':tray,'partitions':partitions,'lid':lid,'six_full_empty_compartments':list(VOID_VOLUMES),'hinge_assemblies':HINGES,'grounded_bottom_m':0,'shell_floor_height_m':.017,'shell_top_height_m':.100,'wall_thickness_m':.015,'fixed_lid_pose_only':True,'minimum_noncontact_surface_clearance_m':.0003}
def measure_bait_box_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 for name in G:
  assert len(vertices[name])==len(G[name]['vertices']),(name,'Changed vertex count')
 # Actual vertex dimensions and local plane distances, not declared role tags.
 tv=vertices[tray];assert max(abs(float(tv[i][2])) for i in range(4))<1e-7
 assert max(abs(float(tv[i][2])-.017) for i in range(12,16))<1e-6
 assert max(abs(float(tv[i][2])-.100) for i in range(4,12))<1e-6
 for i in range(4):
  assert abs(abs(float(tv[i][0]))-.280)<1e-6 and abs(abs(float(tv[i][1]))-.170)<1e-6
  assert abs(abs(float(tv[i+12][0]))-.265)<1e-6 and abs(abs(float(tv[i+12][1]))-.155)<1e-6
 for name in partitions+[lid]+[n for h in HINGES for n in h['rings']+h['brackets']+[h['tongue'],h['pin']]]:
  assert max(abs(float(p[k])-G[name]['vertices'][j][k]) for j,p in enumerate(vertices[name]) for k in range(3))<2e-6,('Changed actual critical vertices',name)
 return {'single_prop_count':1,'real_empty_compartments':6,'floor_thickness_m':.017,'wall_thickness_m':.015,'partition_count':3,'fixed_rigid_lid_count':1,'hinge_assemblies':2,'true_bored_knuckles':6,'fixed_pin_count':2,'nominal_fixed_pin_radial_overlap_m':.0008,'finite_ground_contact_m2':.56*.34,'motion_seal_fit_load_or_safety_claim':False}
FOCUS=(0,.06,.205);ORTHO=.92
CAMERAS={'gray-front3q':(1.2,-1.65,1.45),'gray-back3q':(-1.2,1.65,1.4),'thumbnail':(1.2,-1.65,1.45),'qa-front':(0,-2,1.00),'qa-side':(2,0,1.00),'qa-top':(0,.06,2.20),'qa-back':(0,2,1.00),'qa-wireframe':(1.2,-1.65,1.45),'silhouette-128-front':(0,-2,1.00),'silhouette-128-side':(2,0,1.00)}
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
root=bpy.data.objects.new('OneHingedCompartmentBaitBox',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground box footprint center, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(tray,(0,0,.008),(0,.08,.06)),(lid,lidpoint(0,.17,-.003),lidpoint(0,.17,.020))]:
 assert inside(trees[name],p) is True
 assert inside(trees[name],outside) is False
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
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_bait_box_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'bait_box_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fishing/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
