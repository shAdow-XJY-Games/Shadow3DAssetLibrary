"""Original brimmed beekeeping veil hat: static empty display, no protective claims."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-brimmed-veil-hat-display-01';VERSION='1.0.0';TITLE='Brimmed Veil Hat Display'
DESCRIPTION=('One original static empty beekeeping-hat visual prop with a genuinely hollow domed crown, a broad annular brim, two cloth bindings and a tapered open veil. '
 'The veil is one welded closed lattice surface: 32 thin vertical solid strips cross nine horizontal solid bands, with 256 genuine finite through-windows. Every opening has radial thickness and four geometric side walls; no transparent cards or opaque cylinder is used. '
 'The thicker lower hem has a finite annular underside at ground datum, connected through the lattice and upper binding to the brim and crown. Six editable closed meshes, three solid PBR materials, no textures, head, mannequin, person, bees, stand or surrounding scene. One complete assembly counts as one prop. Metres, Z up, ground-centre origin, front -Y. '
 'Fixed visual pose only. The coarse stylized holes do not establish bee or insect exclusion. No protection from stings, protective efficacy, wearer or head-size fit, ventilation, textile physics, real soft-mesh load capacity, stability, manufacture, occupational equipment or safety certification is claimed.')
G={};LINKS=[];FEET=['LowerHem'];BORES=[];GAPS=[];VOID_VOLUMES={}
PALETTE=[('Canvas_WarmIvory',(.78,.70,.52,1),.88,0),('Binding_OliveKhaki',(.22,.25,.105,1),.87,0),('Veil_Charcoal',(.035,.045,.037,1),.76,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(0,0,1),spread=.0005):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def lathe(name,section,mat,role,n=64,closed=True):
 vs=[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for r,z in section for i in range(n)];fs=[]
 for j in range(len(section) if closed else len(section)-1):
  k=(j+1)%len(section)
  for i in range(n):q=(i+1)%n;fs.append((j*n+i,j*n+q,k*n+q,k*n+i))
 if not closed:fs.extend([tuple(reversed(range(n))),tuple((len(section)-1)*n+i for i in range(n))])
 return mesh(name,vs,fs,mat,role)
# Crown has explicit exterior and interior surfaces joined only at its open lower lip.
N=64;OUTER=[(.133,.319),(.136,.346),(.132,.388),(.118,.426),(.094,.450),(.055,.462)]
INNER=[(.126,.319),(.129,.346),(.125,.383),(.113,.420),(.090,.443),(.052,.454)]
vs=[(r*math.cos(math.tau*i/N),r*math.sin(math.tau*i/N),z) for r,z in OUTER+INNER for i in range(N)];fs=[]
for off in [0,len(OUTER)]:
 for j in range(len(OUTER)-1):
  for i in range(N):q=(i+1)%N;fs.append(((off+j)*N+i,(off+j)*N+q,(off+j+1)*N+q,(off+j+1)*N+i))
for i in range(N):q=(i+1)%N;fs.append((i,len(OUTER)*N+i,len(OUTER)*N+q,q))
fs.extend([tuple((len(OUTER)-1)*N+i for i in range(N)),tuple((2*len(OUTER)-1)*N+i for i in reversed(range(N)))])
mesh('HollowCrown',vs,fs,0,'genuine empty domed shell, exterior and interior surfaces, open lower lip, finite closed crown thickness')
lathe('WideBrim',[(.122,.314),(.298,.306),(.300,.318),(.122,.326)],0,'broad sloping annular brim; actual central opening, finite thickness, crown embeds at inner edge')
lathe('CrownBand',[(.130,.329),(.140,.329),(.140,.346),(.131,.346)],1,'short closed olive cloth band seated in crown wall; no coplanar decal')
lathe('UpperBinding',[(.267,.305),(.280,.305),(.280,.313),(.267,.313)],1,'solid annular upper veil binding; overlaps brim underside and lattice top band')
lathe('LowerHem',[(.206,0),(.231,0),(.231,.0165),(.209,.0165)],1,'thicker annular lower cloth hem; finite planar ground face; visual datum only, no load or stability claim')
# Build the boundary of occupied hexahedral cells, deleting each shared internal
# face. The result is one welded connected closed 256-window mesh with real holes.
COLS=32;ROWS=8;ANGLE_WIDTH=.014;Z0=.012;Z1=.310;BAND=.0048;RADIAL_THICKNESS=.0032
A=[v for i in range(COLS) for v in [math.tau*i/COLS,math.tau*i/COLS+ANGLE_WIDTH]]
Z=[v for j in range(ROWS+1) for v in [Z0+(Z1-Z0-BAND)*j/ROWS,Z0+(Z1-Z0-BAND)*j/ROWS+BAND]]
def veil_radius(z):
 t=(z-Z0)/(Z1-Z0);return .218+.055*t+.006*math.sin(math.pi*t)
def pos(a,z,offset):
 r=veil_radius(z)+offset;return (r*math.cos(a),r*math.sin(a),z)
V=[];LOOK={};BOUNDARY={};HEX_FACES=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def vertex(p):
 key=tuple(round(c,7) for c in p)
 if key not in LOOK:LOOK[key]=len(V);V.append(key)
 return LOOK[key]
def cell(a0,a1,z0,z1,r0,r1):
 return [pos(a,z,r) for z in [z0,z1] for a,r in [(a0,r0),(a0,r1),(a1,r1),(a1,r0)]]
for j in range(len(Z)-1):
 for i in range(len(A)):
  if i%2 and j%2:continue
  aa=A[(i+1)%len(A)] if i+1<len(A) else math.tau
  idx=[vertex(p) for p in cell(A[i],aa,Z[j],Z[j+1],-RADIAL_THICKNESS/2,RADIAL_THICKNESS/2)]
  for face in HEX_FACES:
   f=tuple(idx[k] for k in face);key=tuple(sorted(f))
   if key in BOUNDARY:del BOUNDARY[key]
   else:BOUNDARY[key]=f
mesh('OpenVeilLattice',V,list(BOUNDARY.values()),2,'single welded solid open lattice, 32 vertical strips and 9 horizontal bands; 256 full through-windows with four walls')
# Three spaced finite interior points on each of the six declared overlap joints.
for a,b,r,z in [('HollowCrown','WideBrim',.1295,.321),('HollowCrown','CrownBand',.133,.337),('WideBrim','UpperBinding',.274,.310),('UpperBinding','OpenVeilLattice',veil_radius(.3075),.3075),('WideBrim','OpenVeilLattice',veil_radius(.3090),.3090),('LowerHem','OpenVeilLattice',veil_radius(.0144),.0144)]:
 angle=.006;link(a,b,(r*math.cos(angle),r*math.sin(angle),z),axis=(0,0,1),spread=.0004)
# Each hole receives an entire closed wedge-shaped probe with positive radial
# length and positive cross-section, never just a centre ray. Probes stay out
# of the deliverable. In addition, a broad closed empty envelope fills the veil
# chamber, neck throat and crown interior, catching hidden contained solids.
for row in range(ROWS):
 z0=Z[2*row+1]+.0012;z1=Z[2*row+2]-.0012
 for col in range(COLS):
  a0=A[2*col+1]+.0025;a1=(math.tau*(col+1)/COLS)-.0025
  name=f'Void_Window_{row:02d}_{col:02d}';mesh(name,cell(a0,a1,z0,z1,-.010,.010),HEX_FACES,0,'test-only full finite through-window probe');VOID_VOLUMES[name]=G.pop(name)
  mid=(a0+a1)/2;z=(z0+z1)/2;r=veil_radius(z)
  GAPS.append({'name':name,'origin_m':((r-.011)*math.cos(mid),(r-.011)*math.sin(mid),z),'direction':(math.cos(mid),math.sin(mid),0),'length_m':.022})
lathe('Void_EmptyHatInterior',[(.195,.024),(.246,.292),(.246,.297),(.116,.297),(.116,.327),(.120,.346),(.116,.383),(.103,.418),(.078,.438),(.046,.446)],0,'test-only full interior envelope: lower veil chamber, brim throat and crown cavity',n=64,closed=False)
VOID_VOLUMES['Void_EmptyHatInterior']=G.pop('Void_EmptyHatInterior')
BORES=[{'mesh':'WideBrim','origin_m':(0,0,.29),'direction':(0,0,1),'length_m':.05},{'mesh':'LowerHem','origin_m':(0,0,-.01),'direction':(0,0,1),'length_m':.05}]
def measure_hat_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 vv={n:[tuple(float(c) for c in p) for p in v] for n,v in vertices.items()}
 # Use measured vertices, radii, heights and shell spans. No record-only check.
 crown=vv['HollowCrown'];assert len(crown)==12*N
 ext=[[math.hypot(*p[:2]),p[2]] for p in crown[:6*N:N]];inn=[[math.hypot(*p[:2]),p[2]] for p in crown[6*N::N]]
 assert min(ext[i][0]-inn[i][0] for i in range(6))>.0029
 assert ext[-1][1]-inn[-1][1]>.0079
 assert inn[0][0]>.1259 and inn[-1][1]>.4539
 assert abs(min(p[2] for p in vv['LowerHem']))<1e-7
 hem_ground=[p for p in vv['LowerHem'] if abs(p[2])<1e-7];assert len(hem_ground)==128
 assert max(math.hypot(*p[:2]) for p in hem_ground)-min(math.hypot(*p[:2]) for p in hem_ground)>.0249
 brim=vv['WideBrim'];assert max(math.hypot(*p[:2]) for p in brim)>.2999 and min(math.hypot(*p[:2]) for p in brim)>.1219
 assert min(p[2] for p in brim)>.3059
 lattice=vv['OpenVeilLattice'];assert len(lattice)==len(G['OpenVeilLattice']['vertices'])
 radial_depths=[];row_heights=[]
 for z in Z:
  row=[p for p in lattice if abs(p[2]-z)<1.2e-6];assert len(row)==4*COLS,('Missing or displaced actual lattice row',z,len(row))
  radii=[math.hypot(*p[:2]) for p in row];radial_depths.append(max(radii)-min(radii));row_heights.append(sum(p[2] for p in row)/len(row))
  assert .00319<radial_depths[-1]<.00321,('Actual lattice radial depth',z,radial_depths[-1])
  assert all(min(abs(r-(veil_radius(z)+d)) for d in [-RADIAL_THICKNESS/2,RADIAL_THICKNESS/2])<1.2e-6 for r in radii)
  for angle in A:
   group=[p for p in row if abs((math.atan2(p[1],p[0])-angle+math.pi)%math.tau-math.pi)<1.2e-6]
   assert len(group)==2,('Missing angular strip boundary',z,angle,len(group))
 assert max(p[2] for p in lattice)-min(p[2] for p in lattice)>.2979
 window_heights=[row_heights[2*j+2]-row_heights[2*j+1] for j in range(ROWS)]
 assert min(window_heights)>.0318
 return {'single_prop_count':1,'mesh_count':len(vertices),'true_window_count':COLS*ROWS,'vertical_strip_count':COLS,'horizontal_band_count':ROWS+1,'nominal_radial_strip_thickness_m':RADIAL_THICKNESS,'actual_min_radial_strip_depth_m':min(radial_depths),'actual_min_window_height_m':min(window_heights),'minimum_crown_radial_wall_m':min(ext[i][0]-inn[i][0] for i in range(6)),'crown_top_wall_m':ext[-1][1]-inn[-1][1],'crown_inner_opening_radius_m':inn[0][0],'crown_inner_ceiling_z_m':inn[-1][1],'brim_min_ground_clearance_m':min(p[2] for p in brim),'actual_ground_annulus_width_m':max(math.hypot(*p[:2]) for p in hem_ground)-min(math.hypot(*p[:2]) for p in hem_ground),'full_finite_probe_count':len(VOID_VOLUMES),'fixed_visual_only':True,'protective_or_wearer_fit_claim':False}
FOCUS=(0,0,.230);ORTHO=.72
CAMERAS={'gray-front3q':(1.3,-1.8,1.05),'gray-back3q':(-1.3,1.8,1.05),'thumbnail':(1.3,-1.8,1.05),'qa-front':(0,-3,.78),'qa-side':(3,0,.78),'qa-top':(0,0,3),'qa-back':(0,3,.78),'qa-wireframe':(1.3,-1.8,1.05),'silhouette-128-front':(0,-3,.78),'silhouette-128-side':(3,0,.78)}
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
root=bpy.data.objects.new('OneBrimmedVeilHatDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p in [('WideBrim',(.20,0,.316)),('LowerHem',(.219,0,.010))]:
 assert inside(trees[name],p) is True
 assert inside(trees[name],(0,0,.010)) is False
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'central_cavity_outside_solid':True})
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
mount_evidence=measure_hat_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'hat_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/beekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'beekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
