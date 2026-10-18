"""One original fixed dry-display harbor marker buoy exterior. No navigation meaning.
Broad closed float body, narrow finite sole, four-post open frame, thick plaque and real lug eye.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='harbor-open-frame-marker-buoy-01';VERSION='1.0.0';TITLE='Open-Frame Harbor Marker Buoy'
DESCRIPTION=('One original low-poly static harbor marker-buoy exterior, counted as one prop. A broad low faceted closed float body has a sloping upper shoulder and short neck over a narrower closed ballast-shaped lower body with a finite flat dry-display sole. Four separated square posts form an open short frame with four genuine side windows and an empty middle. A solid square header connects the posts to one thick upright chamfered geometric top plaque. A single thick lower lug has a genuine through-eye, a complete finite top-root contact and positive clearance above the floor. '
 'Nine named editable closed meshes and four opaque constant PBR colours: muted ochre float, dark graphite lower body, deep violet frame and pale mint top plaque. No texture, words, numbers, lights, reflective surfaces, water, rope, chain, anchor, boat, pier, animation or alternate size/colour set. Metres, native Z up, front -Y and origin at the circular body axis on ground Z=0. The original broad-body/open-frame/top-plaque/eye combination is not a scaled fishing float, filled lifebuoy, modified barrel or miniature lighthouse. '
 'One fixed dry-display visual pose only. Finite contacts, closed surfaces and empty-volume tests establish geometry only. No buoyancy, stability, draft, water dynamics, anchoring or mooring loads, reflection, illumination, navigation meaning, maritime standard, safety certification, manufacture, strength, installation, moving mechanism or compatibility with any previous pier, boat or rope asset is claimed. The custom palette and geometric top plaque have no asserted navigational significance.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={}
PALETTE=[('Float_MutedOchre',(.66,.32,.075,1),.64,.12),('Ballast_Graphite',(.045,.065,.075,1),.70,.18),('Frame_DeepViolet',(.17,.10,.25,1),.43,.42),('Plaque_PaleMint',(.47,.70,.56,1),.55,.05)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,1.20);ORTHO=3.30
CAMERAS={'gray-front3q':(4,-7,4.0),'gray-back3q':(-4,7,4.0),'thumbnail':(4,-7,4.0),'qa-front':(0,-8,2.8),'qa-side':(8,0,2.8),'qa-top':(0,0,9),'qa-back':(0,8,2.8),'qa-wireframe':(4,-7,4.0),'silhouette-128-front':(0,-8,2.8),'silhouette-128-side':(8,0,2.8)}
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
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
def box_geometry(lo,hi,mat=0,role='complete finite rectangular probe'):
 v=cuboid(lo,hi);m=Mesh()
 for f in BOX_FACES:m.face([v[i] for i in f],mat)
 return m.result(role,mat)
def box(name,lo,hi,mat,role):G[name]=box_geometry(lo,hi,mat,role);return name
def profile(name,rings,mat,role,n=16):
 vv=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for z,r in rings];m=Mesh()
 m.face(list(reversed(vv[0])),mat,'bottom');m.face(vv[-1],mat,'top')
 for a,b in zip(vv,vv[1:]):
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]],mat,'side')
 G[name]=m.result(role,mat);return name
base=profile('Ballast_NarrowFlatSole',[(0,.42),(.10,.42),(.36,.63)],1,'Narrow faceted closed lower ballast-shaped body with full finite flat sole at ground Z=0; appearance only.');FEET.append(base)
body=profile('Float_BroadShoulderShortNeck',[(.36,1.00),(.47,1.12),(.70,1.12),(.88,.82),(.94,.40),(1.04,.40)],0,'Broad low closed float exterior, lower shoulder, sloping upper shoulder and integral short narrow neck; no actual buoyancy claim.')
# The lug is a single cell-boundary solid around a true rectangular through-eye.
# Its lower surface stays 50mm above the floor. The full top face meets the broad body.
xs=[-.18,-.09,.09,.18];ys=[-.91,-.73];zs=[.05,.12,.25,.36];cells={(i,0,k) for i in range(3) for k in range(3) if not(i==1 and k==1)};m=Mesh()
for i,j,k in sorted(cells):
 v=cuboid((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1]))
 for f,near in zip(BOX_FACES,[(i,j,k-1),(i,j,k+1),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]):
  if near not in cells:m.face([v[q] for q in f],2,'eye_ring')
ear='Lug_TrueThroughEye';G[ear]=m.result('One thick continuous lower attachment lug with true through-eye and complete top root; no rope or load claim.',2)
posts=[]
for x in [-.23,.23]:
 for y in [-.23,.23]:
  name='Frame_Post_'+('L' if x<0 else 'R')+('F' if y<0 else 'B');posts.append(box(name,(x-.045,y-.045,1.04),(x+.045,y+.045,1.79),2,'One square frame leg, finite foot on neck and finite top against header; four complete open windows between separate legs.'))
header=box('Frame_ThickTopHeader',(-.35,-.35,1.79),(.35,.35,1.90),2,'Solid thick square header with separate finite bearing faces for four legs and top plaque.')
# Upright non-standard chamfered plaque, thick in Y with a broad flat bottom.
xz=[(-.18,1.90),(.18,1.90),(.35,2.07),(.35,2.29),(.18,2.46),(-.18,2.46),(-.35,2.29),(-.35,2.07)];vv=[[(x,y,z) for x,z in xz] for y in [-.09,.09]];m=Mesh()
m.face(vv[0],3,'front');m.face(list(reversed(vv[1])),3,'back')
for i in range(8):j=(i+1)%8;m.face([vv[0][i],vv[1][i],vv[1][j],vv[0][j]],3,'edge')
marker='Topmark_ThickChamferedPlaque';G[marker]=m.result('Single thick upright chamfered geometric plaque; custom colour and contour, no navigational meaning.',3)
def contact(a,b,z,points,area):CONTACTS.append({'a':a,'b':b,'axis':2,'plane_m':z,'minimum_patch_area_m2':area,'interior_probe_offset_m':.003,'points':points,'scope':'complete finite opposed planar connection, its full boundary and no positive interpenetration; visual geometry only'})
contact(base,body,.36,[(-.2,0,.36),(0,0,.36),(.2,0,.36)],1.20)
contact(ear,body,.36,[(-.12,-.82,.36),(0,-.82,.36),(.12,-.82,.36)],.064)
for p in posts:
 v=G[p]['vertices'];x=sum(q[0] for q in v)/len(v);y=sum(q[1] for q in v)/len(v)
 contact(body,p,1.04,[(x-.02,y,1.04),(x,y,1.04),(x+.02,y,1.04)],.0080)
 contact(p,header,1.79,[(x-.02,y,1.79),(x,y,1.79),(x+.02,y,1.79)],.0080)
contact(header,marker,1.90,[(-.12,0,1.90),(0,0,1.90),(.12,0,1.90)],.064)
def void(name,lo,hi,role):VOID_PROBES[name]={'type':'mesh','geometry':box_geometry(lo,hi),'targets':list(G),'role':role}
void('WholeFrame_InnerCore',(-.184,-.184,1.041),(.184,.184,1.789),'Complete central frame air volume between neck and header; 1mm face inset, no hidden middle solid.')
for side,lo,hi in [('Front',(-.184,-.36,1.041),(.184,-.184,1.789)),('Back',(-.184,.184,1.041),(.184,.36,1.789)),('Left',(-.36,-.184,1.041),(-.184,.184,1.789)),('Right',(.184,-.184,1.041),(.36,.184,1.789))]:
 void('WholeFrame_Window'+side,lo,hi,'Entire full-height and full-width frame window between the two bordering legs, through complete post depth and both mouths; 1mm inset at real boundary.')
void('WholeLug_ThroughEye',(-.089,-.93,.121),(.089,-.71,.249),'Complete eye width and height, full lug thickness and 20mm beyond both mouths; 1mm inner-boundary inset.')
BORES=[{'mesh':ear,'origin_m':(0,-.94,.185),'direction':(0,1,0),'length_m':.24}]
# The entire lower and upper surfaces outside each contact strip remain apart.
NONCONTACT_DOMAINS=[]
for i,r in enumerate(CONTACTS):
 NONCONTACT_DOMAINS += [{'name':'Connection_%02d_lower_body'%i,'a':r['a'],'b':r['b'],'clip_a_z_max':r['plane_m']-.005,'minimum_m':.0049},{'name':'Connection_%02d_upper_body'%i,'a':r['b'],'b':r['a'],'clip_a_z_min':r['plane_m']+.005,'minimum_m':.0049}]
def measure_buoy_geometry(vertices):
 assert set(vertices)==set(G)
 def bound(name,i,fn):return fn(float(p[i]) for p in vertices[name])
 assert abs(bound(base,2,min))<2e-7
 assert abs(bound(body,0,max)-1.12)<2e-7 and abs(bound(body,2,max)-1.04)<2e-7
 assert abs(bound(ear,2,min)-.05)<2e-7
 assert abs(bound(marker,2,max)-2.46)<2e-7
 return {'single_prop_count':1,'closed_components':9,'body_width_m':2.24,'total_height_m':2.46,'ground_sole_radius_m':.42,'ear_floor_clearance_m':.05,'leg_count':4,'complete_frame_window_count':4,'complete_empty_volume_count':6,'topmark_thickness_m':.18,'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed dry-display buoy exterior; no buoyancy, navigation, loads or safety claims'}
assert len(G)==9,len(G)

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
root=bpy.data.objects.new('OneOpenFrameHarborBuoy',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and circular-body axis origin; front lug -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
buoy_evidence=measure_buoy_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])
 assert hit[0] is None,(r,hit)
 bore_checks.append(dict(r,actual_ear_axis_clear=True,full_volume_scope='source finite-volume and independent imported-GLB audits'))
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
  normal=Vector(r.get('normal',tuple(1 if i==r.get('axis',2) else 0 for i in range(3))));low=Vector(p)-normal*eps;high=Vector(p)+normal*eps
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
 'single_prop_count':1,'buoy_geometry':buoy_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/harbor/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,8),1700,5.0),('Fill',(6,-1.2,5),840,4.8),('Rim',(1.2,6,7),1200,4.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
if '--ground-views' in sys.argv:views={n:CAMERAS[n] for n in ['qa-front','qa-side','qa-back']}
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
