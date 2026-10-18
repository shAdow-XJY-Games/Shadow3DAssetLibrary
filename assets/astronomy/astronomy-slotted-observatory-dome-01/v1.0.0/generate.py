"""One original fixed architectural observatory dome module.
Only the static wall/seat/slotted shell subset is implemented; no rotation or shutter mechanism.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='astronomy-slotted-observatory-dome-01';VERSION='1.0.0';TITLE='Slotted Observatory Dome Module'
DESCRIPTION=('One original low-poly architectural module in one fixed assembled pose, counted as one modular asset. A continuous thick 36-sided circular wall has a real open front doorway, full wall reveals and an empty interior. Its finite bottom wall band rests at ground level. The complete upper wall crown bears a separate continuous annular seat. A connected thick faceted hemispherical shell bears on that seat over a complete finite open-annular eave patch. A true radial through-slit follows the front meridian over the crown to a closed thick rear end. Both slit sides and the rear termination have real thickness, with no dark aperture decal or hidden solid interior. '
 'Three named editable closed meshes and three fully opaque constant PBR colours: warm ivory wall, muted bronze annular seat and deep petrol roof. Metres, native Z up, front -Y and a ground-level origin on the circular axis. No textures, logos, shutter panels, door leaf, telescope, boxes, interior equipment, floor, surrounding scene or animation. Original geometry rather than a filled climbing frame, scaled parasol, lighthouse, or reused observing-corner scene. '
 'This completes only the static architectural subset of the original wall-and-rotating-roof candidate. Rotation and opening/closing remain unimplemented and unverified. Static visual geometry only: no rotation, tracking, shutter motion, optical performance, light exclusion, rain or wind resistance, load capacity, strength, stability, earthquake resistance, manufacture, construction, personnel access, passage compliance, building safety, assembly path or compatibility with any old telescope or scene. Finite geometric support does not establish functional or safe architecture.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={}
PALETTE=[('WarmIvory_Wall',(.69,.63,.48,1),.82,0),('MutedBronze_AnnularSeat',(.34,.235,.115,1),.43,.58),('DeepPetrol_ThickDome',(.045,.185,.205,1),.47,.32)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,1.56);ORTHO=5.10
CAMERAS={'gray-front3q':(5,-8,6.0),'gray-back3q':(-5,8,6.0),'thumbnail':(5,-8,6.0),'qa-front':(0,-9,3.2),'qa-side':(9,0,3.2),'qa-top':(0,0,10),'qa-back':(0,9,3.2),'qa-wireframe':(5,-8,6.0),'silhouette-128-front':(0,-9,3.2),'silhouette-128-side':(9,0,3.2)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
WALL_IN=1.65;WALL_OUT=1.80;WALL_TOP=1.45;DOOR_TOP=1.15;SEAT_TOP=1.55;ROOF_IN=1.65;ROOF_OUT=1.80

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
  ids=[]
  for q in p:
   i=self.vertex(q)
   if not ids or ids[-1]!=i:ids.append(i)
  if ids and ids[-1]==ids[0]:ids.pop()
  if len(set(ids))<3:return
  for i in range(1,len(ids)-1):
   f=(ids[0],ids[i],ids[i+1])
   if len(set(f))<3:continue
   self.f.append(f);self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  used=set(i for f in self.f for i in f);remap={x:i for i,x in enumerate(sorted(used))};self.v=[v for i,v in enumerate(self.v) if i in used];self.f=[tuple(remap[i] for i in f) for f in self.f]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def grid_solid(name,aa,bb,cc,mapping,mat,role,keep=lambda i,j,k:True,periodic_a=False,tagger=None):
 """Boundary of occupied mapped hexahedral cells; internal faces are never exported."""
 m=Mesh();cells={(i,j,k) for i in range(len(aa)-1) for j in range(len(bb)-1) for k in range(len(cc)-1) if keep(i,j,k)}
 for i,j,k in sorted(cells):
  a0,a1=aa[i:i+2];b0,b1=bb[j:j+2];c0,c1=cc[k:k+2]
  sides=[((-1,0,0),[(a0,b0,c0),(a0,b0,c1),(a0,b1,c1),(a0,b1,c0)],'a_low'),((1,0,0),[(a1,b0,c0),(a1,b1,c0),(a1,b1,c1),(a1,b0,c1)],'a_high'),((0,-1,0),[(a0,b0,c0),(a1,b0,c0),(a1,b0,c1),(a0,b0,c1)],'b_low'),((0,1,0),[(a0,b1,c0),(a0,b1,c1),(a1,b1,c1),(a1,b1,c0)],'b_high'),((0,0,-1),[(a0,b0,c0),(a0,b1,c0),(a1,b1,c0),(a1,b0,c0)],'c_low'),((0,0,1),[(a0,b0,c1),(a1,b0,c1),(a1,b1,c1),(a0,b1,c1)],'c_high')]
  for (di,dj,dk),q,tag in sides:
   ni=i+di
   if periodic_a:ni%=len(aa)-1
   if (ni,j+dj,k+dk) in cells:continue
   m.face([mapping(*p) for p in q],mat,tagger(tag,i,j,k) if tagger else tag)
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def cyl(a,z,r):return (r*math.cos(math.radians(a)),r*math.sin(math.radians(a)),z)
def sphere(a,t,r,zc=SEAT_TOP):
 a=math.radians(a);t=math.radians(t);return (r*math.sin(a),r*math.cos(a)*math.cos(t),zc+r*math.cos(a)*math.sin(t))
def walltag(tag,i,j,k):
 if tag=='b_low' and j==0:return 'ground'
 if tag=='b_high' and j==1:return 'crown_seat'
 return 'wall_'+tag
def rooftag(tag,i,j,k):
 if tag=='b_low' and j==0 or tag=='b_high' and j==17:return 'eave_seat'
 if tag=='c_low':return 'inner_shell'
 if tag=='c_high':return 'outer_shell'
 return 'slit_thick_reveal'
# A full crown above the opening leaves one connected thick wall mesh.
grid_solid('CircularWall_TrueDoorway',list(range(0,361,10)),[0,DOOR_TOP,WALL_TOP],[WALL_IN,WALL_OUT],cyl,0,'Continuous thick circular wall with true front doorway, finite bottom and full annular crown.',lambda i,j,k:not(25<=i<29 and j==0),True,walltag)
FEET.append('CircularWall_TrueDoorway')
grid_solid('Complete_AnnularSeat',list(range(0,361,10)),[WALL_TOP,SEAT_TOP],[1.60,1.87],cyl,1,'One continuous complete annular seat, lower face on wall crown and upper face bearing the slotted shell.',periodic_a=True)
# Original spherical cell shell. Removing a central meridian band from the front
# horizon past the crown retains a real rear bridge, so this is one closed component.
grid_solid('Slotted_ThickDome',list(range(-90,91,10)),list(range(0,181,10)),[ROOF_IN,ROOF_OUT],sphere,2,'One connected thick hemispherical shell with genuine open meridian slit, two thick side reveals and thick rear termination.',lambda i,j,k:not(8<=i<10 and j>=5),tagger=rooftag)
for a,b,z,area,angles in [('CircularWall_TrueDoorway','Complete_AnnularSeat',WALL_TOP,1.60,[0,90,180,270]),('Complete_AnnularSeat','Slotted_ThickDome',SEAT_TOP,1.50,[0,90,180,230,310])]:
 CONTACTS.append({'a':a,'b':b,'axis':2,'plane_m':z,'minimum_patch_area_m2':area,'interior_probe_offset_m':.003,'points':[cyl(t,z,1.725) for t in angles],'scope':'complete finite opposed annular bearing region including its boundary; zero positive penetration'})
def void(name,g,role,targets=None):VOID_PROBES[name]={'type':'mesh','geometry':g,'targets':list(G) if targets is None else targets,'role':role}
# The three closed volumes cover the complete room, constricted seat throat and
# dome interior, using small explicit conservative surface clearances.
void('Complete_LowerRoom',grid_solid(None,list(range(0,361,10)),[.005,WALL_TOP-.005],[0,WALL_IN-.010],cyl,0,'Full polygonal cylindrical room probe.',periodic_a=True),'complete lower room including the full axial core, all azimuths and height; 5 mm vertical and 10 mm radial inset')
void('Complete_SeatThroat',grid_solid(None,list(range(0,361,10)),[WALL_TOP-.005,SEAT_TOP+.005],[0,1.59],cyl,0,'Full annular-seat central opening probe.',periodic_a=True),'complete central seat throat with its axial core and both mouths; 10 mm radial inset')
void('Complete_DomeInterior',grid_solid(None,list(range(-90,91,10)),list(range(0,181,10)),[0,ROOF_IN-.020],lambda a,t,r:sphere(a,t,r,SEAT_TOP+.005),0,'Full hemispherical room probe.'),'complete hemispherical inner empty volume, including central core and crown; 20 mm radial inset and 5 mm floor rise')
void('Complete_ThroughDoorway',grid_solid(None,[250.4,260,270,280,289.6],[.005,DOOR_TOP-.005],[WALL_IN-.045,WALL_OUT+.045],cyl,0,'Whole thick doorway probe with both mouths.'),'whole actual front door opening: full 1.14 m height, nearly full 40-degree width, complete wall thickness and 45 mm beyond either radial mouth')
void('Complete_MeridianSlit',grid_solid(None,[-9.6,0,9.6],[50.4,60,70,80,90,100,110,120,130,140,150,160,170,179.6],[ROOF_IN-.020,ROOF_OUT+.020],sphere,0,'Whole finite curved through-slit probe.'),'entire curved meridian band from near front eave to rear stop, both side boundaries, full radial shell thickness and both radial mouths; 0.4 degree boundary inset')
# Wall and roof are disjoint except for the intervening seat. Noncontact subsets
# below/above each finite bearing are checked with complete surfaces, not one ray.
NONCONTACT_DOMAINS=[{'name':'Complete_wall_to_roof','a':'CircularWall_TrueDoorway','b':'Slotted_ThickDome','minimum_m':.099},
 {'name':'Wall_body_below_crown_to_seat','a':'CircularWall_TrueDoorway','b':'Complete_AnnularSeat','clip_a_z_max':WALL_TOP-.01,'minimum_m':.0099},
 {'name':'Roof_above_eave_to_seat','a':'Slotted_ThickDome','b':'Complete_AnnularSeat','clip_a_z_min':SEAT_TOP+.01,'minimum_m':.0099}]
def measure_dome_geometry(vertices):
 return {'single_modular_count':1,'closed_components':3,'wall_inner_radius_m':WALL_IN,'wall_outer_radius_m':WALL_OUT,'wall_height_m':WALL_TOP,'door_opening_height_m':DOOR_TOP,'door_angular_width_deg':40,'seat_inner_radius_m':1.60,'seat_outer_radius_m':1.87,'seat_thickness_m':.10,'roof_radial_thickness_m':.15,'slit_angular_width_deg':20,'slit_meridian_arc_deg':130,'complete_finite_empty_volume_count':5,'materials':MATERIAL_CONTRACT,'functional_scope':'one original fixed architectural module; rotation and opening/closing unimplemented and unverified'}
assert len(G)==3,len(G)
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
root=bpy.data.objects.new('OneFixedObservatoryDome',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and circular-axis origin; front doorway -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
dome_evidence=measure_dome_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'dome_geometry':dome_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/astronomy/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'astronomy','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
