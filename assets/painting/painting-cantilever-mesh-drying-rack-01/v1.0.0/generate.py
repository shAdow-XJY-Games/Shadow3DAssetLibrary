"""Original cantilever mesh artwork drying rack. One static empty prop, metres/Z up/front -Y.
New welded perforated horizontal trays, rear-only support, fixed hinge hardware and stops.
No paper, paintings, moving trays, performance or equipment-safety claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='painting-cantilever-mesh-drying-rack-01';VERSION='1.0.0';TITLE='Cantilever Mesh Drying Rack'
DESCRIPTION=('One original empty low-poly artwork drying rack: six independent horizontal welded mesh trays project forward from a pair of rear spines. Each tray is a single connected thick closed solid with a continuous outer frame, fine crossing ribs and 63 true rectangular through-windows. Six continuous rear axles, twelve thick annular hinge ears with real axial bores and six broad fixed rear stop bearers provide a complete static support chain to two long base skids and four finite grounded pads. No front posts obstruct the paper-facing access. '
 'One reusable prop, 40 named editable closed mesh parts, four constant opaque PBR materials, no image or procedural textures, paper, artwork, branding, people or scene. Metres, Z up, front -Y; origin on the ground X midline with Y=0 as the assembly datum. '
 'Fixed visual geometry only. Temporary flat rectangular fixtures verify finite coplanar support, and complete finite volumes verify openings and layer clearances in this pose. These tests do not establish standard paper sizes, insertion/removal paths, tray flipping range, dynamics, drying speed, airflow, paint compatibility, load capacity, anti-tip stability, manufacturing or product safety certification.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};TRAYS=[];AXLES=[];EARS=[];STOPS=[];SPINES=[];FIXTURES=[];WINDOWS=[]
PALETTE=[('Frame_PetrolBlue',(.045,.23,.28,1),.48,.38),('Tray_SatinSilver',(.59,.66,.68,1),.40,.64),('Hardware_Graphite',(.105,.145,.16,1),.36,.60),('Feet_Charcoal',(.032,.043,.047,1),.82,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':role}
def cylinder_x(name,x0,x1,y,z,r,mat,role,n=16):
 vs=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n)) for x in [x0,x1] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat,role)
def annulus_x(name,x0,x1,y,z,ro,ri,mat,role,n=16):
 vs=[(x,y+r*math.cos(math.tau*i/n),z+r*math.sin(math.tau*i/n)) for x,r in [(x0,ro),(x1,ro),(x1,ri),(x0,ri)] for i in range(n)]
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
for side,sign in [('Left',-1),('Right',1)]:
 x=sign*.47
 skid=box('BaseSkid_'+side,(x,-.05,.068),(.084,.880,.060),0,'long base skid, broad front reach with no front upright')
 spine=box('RearSpine_'+side,(x,.295,.740),(.044,.050,1.320),0,'single rear-only vertical support from base skid to top crossbar');SPINES.append(spine)
 link(spine,skid,(x,.295,.089),axis=(0,1,0),spread=.009)
 for label,y in [('Front',-.420),('Back',.320)]:
  foot=box('GroundPad_'+side+'_'+label,(x,y,.020),(.120,.130,.040),3,'finite planar rubber contact pad, underside exactly Z=0');FEET.append(foot)
  link(foot,skid,(x,y,.039),axis=(0,1,0),spread=.030)
for label,z in [('Lower',.165),('Upper',1.365)]:
 brace=box('RearCrossbar_'+label,(0,.295,z),(.960,.040,.042),0,'rear transverse stiffener joining both spines')
 for side,sign in [('Left',-1),('Right',1)]:link(brace,'RearSpine_'+side,(sign*.47,.295,z),axis=(0,0,1),spread=.009)
# Each shelf is the exterior boundary of a union of occupied rectangular cells.
# Shared internal faces are deleted and vertices welded: one connected solid,
# not disconnected cross-bars, paper cards, alpha textures or stacked slats.
NX=9;NY=7;BAR=.005;BORDER=.020;THICKNESS=.008;X0=-.430;X1=.430;Y0=-.395;Y1=.245
XGAP=(X1-X0-2*BORDER-(NX-1)*BAR)/NX;YGAP=(Y1-Y0-2*BORDER-(NY-1)*BAR)/NY
def bands(lo,hi,n,gap):
 out=[lo,lo+BORDER]
 for i in range(n):
  out.append(out[-1]+gap)
  if i<n-1:out.append(out[-1]+BAR)
 out.append(hi);return out
XB=bands(X0,X1,NX,XGAP);YB=bands(Y0,Y1,NY,YGAP)
for level in range(6):
 z=.330+level*.190;label=f'{level+1:02d}';v=[];lookup={};boundary={}
 def index(p):
  key=tuple(round(c,7) for c in p)
  if key not in lookup:lookup[key]=len(v);v.append(key)
  return lookup[key]
 for j in range(len(YB)-1):
  for i in range(len(XB)-1):
   if i%2 and j%2:continue
   ids=[index(p) for p in cuboid((XB[i],YB[j],z-THICKNESS/2),(XB[i+1],YB[j+1],z+THICKNESS/2))]
   for f in BOX_FACES:
    face=tuple(ids[k] for k in f);key=tuple(sorted(face))
    if key in boundary:del boundary[key]
    else:boundary[key]=face
 tray=mesh('Tray_'+label+'_WeldedOpenGrid',v,list(boundary.values()),1,'one welded closed 8 mm thick mesh tray: continuous 20 mm border, 5 mm crossing ribs, 63 true windows');TRAYS.append(tray)
 axle=cylinder_x('Axle_'+label+'_FixedRear',-.490,.490,.240,z,.012,2,'continuous rear hinge axle, fixed display pose with finite engagement into tray back border and hinge bores');AXLES.append(axle)
 stop=box('Stop_'+label+'_RearBearer',(0,.261,z-.030),(.976,.070,.054),0,'broad fixed rear stop bearer under tray frame, finite 1 mm static support engagement; no dynamic hinge claim');STOPS.append(stop)
 link(tray,axle,(0,.236,z),spread=.300)
 link(tray,stop,(0,.230,z-.0035),spread=.300)
 link(axle,stop,(0,.240,z-.008),spread=.300)
 for side,sign in [('Left',-1),('Right',1)]:
  x=sign*.470;ear=annulus_x('Ear_'+label+'_'+side,x-.014,x+.014,.240,z,.039,.011,2,'thick closed annular hinge ear with true axial bore, rear seat in spine, fixed assembly');EARS.append(ear)
  link(ear,axle,(x,.2512,z),spread=.006)
  link(ear,'RearSpine_'+side,(x,.274,z),spread=.006)
  link(ear,stop,(x,.260,z-.030),spread=.006)
  link(stop,'RearSpine_'+side,(x,.282,z-.030),spread=.006)
  BORES.append({'mesh':ear,'origin_m':(x-.018,.240,z),'direction':(1,0,0),'length_m':.036})
 # Full aperture probes stop clear of the frame and every rib. Every one is
 # tested against the entire assembled rack, including hidden contained parts.
 for j in range(NY):
  for i in range(NX):
   lo=(XB[2*i+1]+.001,YB[2*j+1]+.001,z-.010);hi=(XB[2*i+2]-.001,YB[2*j+2]-.001,z+.010)
   name=f'Window_{label}_{i:02d}_{j:02d}';void(name,lo,hi,'full positive-volume through-window, all parts tested');WINDOWS.append(name)
   GAPS.append({'name':name,'origin_m':((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,z-.011),'direction':(0,0,1),'length_m':.022})
 # Complete finite rectangle sits on the actual coplanar upper ribs, with
 # positive area intersections calculated later. It is a test-only fixture.
 FIXTURES.append({'tray':tray,'lo':[-.39,-.350,z+.004],'hi':[.39,.200,z+.006],'minimum_support_area_m2':.020})
 if level<5:void('Interlayer_'+label,(-.425,-.390,z+.005),(.425,.220,z+.185),'full front-open layer envelope; geometry clearance only, no insertion path')
 else:void('AboveTopTray',(-.425,-.390,z+.005),(.425,.220,z+.105),'full top-tray clear envelope')
 # Front approach volume is deliberately external and empty, not a promised
 # insertion trajectory or paper-fit standard.
 void('FrontAccess_'+label,(-.425,-.470,z+.005),(.425,-.397,z+.165),'finite open front space, no front posts or artwork')
def measure_rack_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 bounds=lambda n:([min(float(p[k]) for p in vertices[n]) for k in range(3)],[max(float(p[k]) for p in vertices[n]) for k in range(3)])
 rows=[]
 for level,name in enumerate(TRAYS):
  v=vertices[name];lo,hi=bounds(name);z=.330+.190*level
  assert all(abs(lo[k]-[X0,Y0,z-.004][k])<1.2e-6 and abs(hi[k]-[X1,Y1,z+.004][k])<1.2e-6 for k in range(3)),('Tray actual bounds changed',name,lo,hi)
  actualx=sorted(set(round(float(p[0]),6) for p in v));actualy=sorted(set(round(float(p[1]),6) for p in v));actualz=sorted(set(round(float(p[2]),6) for p in v))
  assert len(actualx)==len(XB) and len(actualy)==len(YB) and len(actualz)==2,('Grid rib layout changed',name)
  assert max(abs(a-b) for a,b in zip(actualx,XB))<1.2e-6 and max(abs(a-b) for a,b in zip(actualy,YB))<1.2e-6
  rows.append({'tray':name,'actual_thickness_m':hi[2]-lo[2],'actual_frame_width_m':actualx[1]-actualx[0],'actual_min_internal_rib_m':min(actualx[i+1]-actualx[i] for i in range(2,len(actualx)-2,2)),'window_count':NX*NY,'bottom_z_m':lo[2],'top_z_m':hi[2]})
 clearances=[rows[i+1]['bottom_z_m']-rows[i]['top_z_m'] for i in range(5)];assert min(clearances)>.1819
 for name in FEET:assert abs(bounds(name)[0][2])<1e-7
 for name in SPINES:assert bounds(name)[0][1]>.2699
 for name in EARS:
  lo,hi=bounds(name);z=(lo[2]+hi[2])/2;radii=[math.hypot(p[1]-.240,p[2]-z) for p in vertices[name]]
  assert abs(min(radii)-.011)<1.2e-6 and abs(max(radii)-.039)<1.2e-6
 return {'single_prop_count':1,'mesh_count':len(vertices),'tray_count':6,'true_window_count':6*NX*NY,'window_columns':NX,'window_rows':NY,'actual_tray_geometry':rows,'actual_min_interlayer_clearance_m':min(clearances),'finite_fixture_count':len(FIXTURES),'full_finite_void_count':len(VOID_VOLUMES),'rear_only_spines':SPINES,'front_posts':0,'fixed_pose_only':True,'drying_load_stability_motion_or_paper_fit_claim':False}
RACK_CONTRACT={'tray_meshes':TRAYS,'axis_meshes':AXLES,'ear_meshes':EARS,'fixed_stop_meshes':STOPS,'rear_spine_meshes':SPINES,'ground_meshes':FEET,'fixture_supports':FIXTURES,'window_probes':WINDOWS,'static_only':True}
FOCUS=(0,-.035,.700);ORTHO=2.20
CAMERAS={'gray-front3q':(2.3,-3.3,2.8),'gray-back3q':(-2.3,3.3,2.8),'thumbnail':(2.3,-3.3,2.8),'qa-front':(0,-4,1.85),'qa-side':(4,-.035,1.85),'qa-top':(0,-.035,4),'qa-back':(0,4,1.85),'qa-wireframe':(2.3,-3.3,2.8),'silhouette-128-front':(0,-4,1.85),'silhouette-128-side':(4,-.035,1.85)}
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
root=bpy.data.objects.new('OneCantileverMeshDryingRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground X midline, Y=0, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p in [('Tray_01_WeldedOpenGrid',(0,-.385,.330)),('Ear_01_Left',(-.470,.270,.330))]:
 assert inside(trees[name],p) is True
 outside=(0,-.35,.33) if name.startswith('Tray') else (-.470,.240,.330)
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
mount_evidence=measure_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/painting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'painting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
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
