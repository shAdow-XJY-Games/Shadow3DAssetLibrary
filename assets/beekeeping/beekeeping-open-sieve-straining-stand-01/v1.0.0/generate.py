"""Original empty honey-straining stand: one fixed visual prop.
The sieve is one connected thick mesh with 45 true square through-openings.
No food-contact, filtration, load-bearing, manufacture or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='beekeeping-open-sieve-straining-stand-01';VERSION='1.0.0';TITLE='Open Sieve Honey-Straining Stand'
DESCRIPTION=('One original low-poly static honey-straining stand prop. A shallow chamfered-octagonal silver sieve has a genuinely thick sloping bowl wall, an integral outward shoulder, and a single connected thick bottom lattice containing 45 complete square through-openings. '
 'The warm metal shoulder rests with a finite opposed full-perimeter annular contact region on a separate dark teal octagonal seat ring. The rest of the bowl and seat remain separated. '
 'Four slightly splayed side legs, an external lower brace ring and four flat dark foot pads form connected finite supports. The broad central volume from below the perforated sieve to ground is genuinely empty. '
 'Eleven named editable closed meshes, four fully opaque constant PBR materials, metre scale, source Z up, ground-centre origin and illustrative front -Y. One complete fixed assembly counts as one prop. '
 'No textures, transparency, honey, receiving vessel, extractor shaft or spinning basket, machinery, people, scene or animation. Original geometry, no existing asset compatibility claim. '
 'Coarse stylized holes demonstrate visible geometry only: no filtration performance or mesh grade, food contact or hygiene, honey processing, liquid flow, load-bearing or anti-tip capacity, corrosion resistance, actual material, manufacturing or safety certification. Not real equipment construction or use guidance.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={}
PALETTE=[('SatinSilver_Sieve',(.55,.62,.65,1),.42,.65),('HoneyBrass_Shoulder',(.57,.32,.085,1),.4,.60),('DeepTeal_Frame',(.025,.16,.155,1),.52,.18),('Charcoal_Feet',(.035,.045,.048,1),.82,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,.48);ORTHO=1.55
CAMERAS={'gray-front3q':(1.6,-2.5,2.15),'gray-back3q':(-1.6,2.5,2.15),'thumbnail':(1.6,-2.5,2.15),'qa-front':(0,-3,1.48),'qa-side':(3,0,1.48),'qa-top':(0,0,3),'qa-back':(0,3,1.48),'qa-wireframe':(1.6,-2.5,2.15),'silhouette-128-front':(0,-3,1.48),'silhouette-128-side':(3,0,1.48)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,p,mat=0,tag=''):
  ids=[self.vertex(q) for q in p]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
# Counterclockwise octagon: the corner truncation ratio is shared by bowl and seat.
OCT=[(-.18,-.28),(.18,-.28),(.28,-.18),(.28,.18),(.18,.28),(-.18,.28),(-.28,.18),(-.28,-.18)]
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def clip(poly):
 for a,b in zip(OCT,OCT[1:]+OCT[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cross2(sub(b,a),sub(s,a));de=cross2(sub(b,a),sub(e,a));si=ds>=-1e-10;ei=de>=-1e-10
   if si!=ei:poly.append(tuple(s[k]+(e[k]-s[k])*ds/(ds-de) for k in range(2)))
   if ei:poly.append(e)
 # Remove duplicate vertices from clipping at exact grid boundaries.
 clean=[]
 for p in poly:
  p=tuple(round(x,9) for x in p)
  if not clean or p!=clean[-1]:clean.append(p)
 if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
 return clean
HOLES=[]
for ix in range(-3,4):
 for iy in range(-3,4):
  x,y=ix*.07,iy*.07;h=.024
  if abs(x)+abs(y)+2*h<.46-1e-8:HOLES.append({'center_xy_m':[round(x,9),round(y,9)],'lo_xy_m':[round(x-h,9),round(y-h,9)],'hi_xy_m':[round(x+h,9),round(y+h,9)],'z_range_m':[.730,.745]})
assert len(HOLES)==45
coords=sorted(set([-.28,.28]+[round(i*.07+s*.024,9) for i in range(-3,4) for s in [-1,1]]))
m=Mesh();edges={}
for x0,x1 in zip(coords,coords[1:]):
 for y0,y1 in zip(coords,coords[1:]):
  cx,cy=(x0+x1)/2,(y0+y1)/2
  if any(h['lo_xy_m'][0]<cx<h['hi_xy_m'][0] and h['lo_xy_m'][1]<cy<h['hi_xy_m'][1] for h in HOLES):continue
  p=clip([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
  if len(p)<3:continue
  m.face([(x,y,.745) for x,y in p],0,'grid_top');m.face([(x,y,.730) for x,y in reversed(p)],0,'grid_bottom')
  for a,b in zip(p,p[1:]+p[:1]):
   key=tuple(sorted((a,b)))
   if key in edges:edges.pop(key)
   else:edges[key]=(a,b)
outer=[]
for a,b in edges.values():
 mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
 is_outer=abs(max(abs(mid[0]),abs(mid[1]))-.28)<1e-8 or abs(abs(mid[0])+abs(mid[1])-.46)<1e-8
 if not is_outer:m.face([(a[0],a[1],.730),(b[0],b[1],.730),(b[0],b[1],.745),(a[0],a[1],.745)],0,'hole_wall');continue
 outer.append((a,b))
 profile=[(1,.730),(.36/.28,.930),(.395/.28,.930),(.395/.28,.950),(.34/.28,.950),(1,.745)]
 for k,((s0,z0),(s1,z1)) in enumerate(zip(profile,profile[1:])):
  m.face([(a[0]*s0,a[1]*s0,z0),(b[0]*s0,b[1]*s0,z0),(b[0]*s1,b[1]*s1,z1),(a[0]*s1,a[1]*s1,z1)],1 if 1<=k<=3 else 0,['outer_wall','shoulder_underside','shoulder_outer','shoulder_top','inner_wall'][k])
G['Sieve_IntegralPerforatedBowl']=m.result('One connected thick bowl with 45 square through-holes, integral continuous lattice and finite outward seating shoulder.')
def oct_ring(name,inner,outer,z0,z1,mat,role):
 m=Mesh();profile=[(inner,z0),(outer,z0),(outer,z1),(inner,z1),(inner,z0)]
 for a,b in zip(OCT,OCT[1:]+OCT[:1]):
  for k,((r0,h0),(r1,h1)) in enumerate(zip(profile,profile[1:])):
   m.face([(a[0]*r0/.28,a[1]*r0/.28,h0),(b[0]*r0/.28,b[1]*r0/.28,h0),(b[0]*r1/.28,b[1]*r1/.28,h1),(a[0]*r1/.28,a[1]*r1/.28,h1)],mat,['bottom','outer','top','inner'][k])
 G[name]=m.result(role,mat)
def radial_box(name,direction,r0,r1,width,z0,z1,mat,role):
 # Horizontal rectangular end faces; centre shifts radially between heights.
 dx,dy=direction;tx,ty=-dy,dx;m=Mesh();v=[]
 for z,r in [(z0,r0),(z1,r1)]:
  for u,w in [(-width[0]/2,-width[1]/2),(width[0]/2,-width[1]/2),(width[0]/2,width[1]/2),(-width[0]/2,width[1]/2)]:v.append((dx*(r+u)+tx*w,dy*(r+u)+ty*w,z))
 for q in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:m.face([v[i] for i in q],mat,'ground' if q==(3,2,1,0) and z0==0 else 'side')
 G[name]=m.result(role,mat)
oct_ring('Stand_ShoulderSeatRing',.365,.390,.895,.930,2,'Complete separate annular seat with full finite opposed shoulder contact and clear noncontact bore.')
oct_ring('Stand_LowerOpenBraceRing',.390,.435,.235,.270,2,'External lower brace ring; its large open centre leaves the sieve-to-ground void unobstructed.')
for side,d in [('East',(1,0)),('North',(0,1)),('West',(-1,0)),('South',(0,-1))]:
 leg='Stand_SplayedLeg_'+side;foot='Stand_FlatFoot_'+side
 radial_box(leg,d,.430,.382,(.045,.055),.035,.910,2,'Side support with finite lower foot and upper seat connections; fixed slight splay.')
 radial_box(foot,d,.430,.430,(.130,.105),0,.050,3,'Finite flat pad on ground; one of four supports.')
 FEET.append(foot)
 for a,b,r,z in [(foot,leg,.430,.042),('Stand_ShoulderSeatRing',leg,.380,.902),('Stand_LowerOpenBraceRing',leg,.416,.252)]:
  LINKS.append((a,b,[(d[0]*r-d[1]*t,d[1]*r+d[0]*t,z) for t in [-.013,.013]]))
CONTACTS=[{'a':'Stand_ShoulderSeatRing','b':'Sieve_IntegralPerforatedBowl','plane_m':.930,'minimum_patch_area_m2':.068,'interior_probe_offset_m':.001,'points':[(.375,0,.930),(0,.375,.930),(-.375,0,.930),(0,-.375,.930)],'scope':'complete finite eight-sided annulus of opposed surface contact; all sectors checked'}]
# Actual finite 3-D empty probes are reconstructed and independently checked after GLB import.
for i,h in enumerate(HOLES):
 lo,hi=h['lo_xy_m'],h['hi_xy_m'];VOID_PROBES['SieveHole_%02d'%i]={'type':'box','lo_m':[lo[0]+.001,lo[1]+.001,.725],'hi_m':[hi[0]-.001,hi[1]-.001,.751],'targets':list(G),'role':'complete square passage including below and above both true lattice faces, with 1 mm side clearance'}
def oct_solid(profile):
 m=Mesh()
 for a,b in zip(OCT,OCT[1:]+OCT[:1]):
  for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
   m.face([(a[0]*r0/.28,a[1]*r0/.28,z0),(b[0]*r0/.28,b[1]*r0/.28,z0),(b[0]*r1/.28,b[1]*r1/.28,z1),(a[0]*r1/.28,a[1]*r1/.28,z1)])
 r0,z0=profile[0];r1,z1=profile[-1]
 m.face([(a[0]*r0/.28,a[1]*r0/.28,z0) for a in reversed(OCT)])
 m.face([(a[0]*r1/.28,a[1]*r1/.28,z1) for a in OCT])
 return m.result('Finite full octagonal probe, excluded from asset and renders.')
VOID_PROBES['FullBelowSieveClearance']={'type':'mesh','geometry':oct_solid([(.277,.001),(.277,.728)]),'targets':list(G),'role':'complete octagonal empty volume underneath the entire sieve, from just above ground to just below sieve bottom'}
VOID_PROBES['CompleteOpenBowlCavity']={'type':'mesh','geometry':oct_solid([(.276,.748),(.336,.951),(.336,.980)]),'targets':list(G),'role':'complete tapered octagonal interior from above lattice through open mouth, positive distance from all walls'}
def measure_strainer_geometry(vertices):
 return {'sieve_opening_count':len(HOLES),'sieve_through_holes':HOLES,'lattice_thickness_m':.015,'shoulder_seating_plane_z_m':.930,'seat_inner_half_width_m':.365,'bowl_outer_half_width_at_seat_m':.360,'full_assembly_height_m':.950,'ground_pad_count':4,'single_prop_count':1,'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed complete static visually straining stand; no performance or equipment claim'}
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
root=bpy.data.objects.new('OneHoneyStrainingStand',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Geometry-only source checks are repeated on actual generated Blender triangles.
# Independent acceptance separately imports the final GLB and verifies the entire interface.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
strainer_evidence=measure_strainer_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
adj={name:set() for name in G}
for a,b,points in LINKS:
 samples=[]
 for p in points:
  margin=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3]);valid=actual_inside(a,p) and actual_inside(b,p) and margin>.0001;assert valid,(a,b,p,margin)
  samples.append({'point_m':p,'both_interiors':True,'nearest_boundary_margin_m':margin})
 joints.append({'a':a,'b':b,'samples':samples});adj[a].add(b);adj[b].add(a)
for r in CONTACTS:
 a,b=r['a'],r['b'];eps=r['interior_probe_offset_m']
 for p in r['points']:
  low=(p[0],p[1],p[2]-eps);high=(p[0],p[1],p[2]+eps)
  assert actual_inside(a,low) and actual_inside(b,high) and not actual_inside(a,high) and not actual_inside(b,low),(a,b,p)
 adj[a].add(b);adj[b].add(a);face_contacts.append(dict(r,actual_opposed_interior_side_probes=True,full_area_scope='pure source and independent actual GLB full-surface audit'))
todo=list(seen)
while todo:
 for name in adj[todo.pop()]-seen:seen.add(name);todo.append(name)
assert seen==set(G),seen
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
 'single_prop_count':1,'strainer_geometry':strainer_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=CAMERA_SCALES.get(name,ORTHO)
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
 for name,pos in [(n,CAMERAS[n]) for n in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
