"""RECOVERY-R2 SOURCE RECONSTRUCTION: standing copy pickup / document staging.

This is a new reconstruction assembled from complete source text and explicit
patches still visible in the original worker conversation, not a recovered old
disk file. Previous geometry, images, hashes and QA approvals do not approve this
file or its future outputs. Every model, image and acceptance gate must be rerun.

Normal repository full render:
 blender -b -t 4 --python assets/office/office-standing-copy-staging-scene-01/v1.0.0/generate.py -- --render-final --threads 4
Geometry only: replace --render-final with --no-render. A fresh geometry-only run
writes model.glb, source.blend and QA evidence; with no thumbnail it deliberately
writes no metadata.json or thumbnail.png. --snapshot can select a source root;
normal repository ancestors are discovered without it. No mandatory sidecar.
--render-gray and --render-pbr are separate review milestones. --render-final
renders six actual-GLB views at 128 samples, no denoising; isometric bytes are the
thumbnail, with no seventh render. No cameras/studio/diagnostic ground in GLB.

One scene ID only. Complete unchanged legacy copier, worktable and shallow tray;
no cabinet and no new file tray. Two editable AUTHORED_A4 closed paper nodes are
part of the scene, not standalone catalog props. Paper .210 x .297 x .0002 m;
0.2mm thickness is an explicit authored static geometry design, not a weight,
manufacturing or flexible-paper claim. Original nonsemantic ink bars are material
regions of the same closed solid; no floating decals, text or personal data.

Blender local (x,y,z) -> glTF local (x,z,-y), then root placement applies. Reserved
body volumes are Z[0,2.2], with whole .60 x .60m footprints and finite connections.
Access prisms are static empty reference volumes, not arm reach or paper-motion
certification. No copying, scanning, feeding, drawer operation, dynamics,
load, electrical, ergonomic, accessibility or safety/code compliance claim.
"""
import argparse,hashlib,json,math,sys,struct
from collections import Counter
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent
ASSET='office-standing-copy-staging-scene-01'
# Expected historical byte locks are reconstructed from visible tool text only.
# They are not evidence that dependencies have been downloaded/verified in r2.
LOCK={
 'repository':'shAdow-XJY-Games/Shadow3DAssetLibrary',
 'catalog_snapshot_commit':'034142c2d18816fe3c2096be20b29175b3c63813',
 'catalog_snapshot_tree':'d208f07bd15607e197397af0eeb6ff0e29f1b21b',
 'recovery_read_reference_commit':'bb994a632eea4aca2bea12c2871756777bc642aa',
 'recovery_kind':'reconstructed expected three-ID nine-file runtime dependency lock; actual r2 downloads and matching verification still required; no old generator is executed',
 'source_id_and_pin_mapping':{
  'bakery-shallow-baking-tray-01':{'sourceId':'bakery-frontshop-pair','origin_pin':'4649b2d892940a853afaf82da2ebc0320297a2cb'},
  'interior-open-worktable-01':{'sourceId':'access-core','origin_pin':'e179cdc82c1f57e36dc0a78704146783f711484d'},
  'office-floorstanding-copier-01':{'sourceId':'sports-office-extension','origin_pin':'e2a7cc05631ba3699d982cce4c9a65ee45448f20'}},
 'files':[
 {'path':'assets/bakery/bakery-shallow-baking-tray-01/v1.0.0/generate.py','bytes':30505,'git_blob_sha1':'f746f440af967a6664d3b3f2f08016e80289d6f3','sha256':'74655f292e62ffa4962b48a4e37fa4105955ace0b13074dd11023bec32489afe'},
 {'path':'assets/bakery/bakery-shallow-baking-tray-01/v1.0.0/metadata.json','bytes':1781,'git_blob_sha1':'a6d00a45136001b40ec3958e02ee5d73d6b8bbe1','sha256':'9e3c4cb0f43396916bd44192648795cd9a2e91f7aa1f77f12fb1592e39bcb488'},
 {'path':'assets/bakery/bakery-shallow-baking-tray-01/v1.0.0/model.glb','bytes':3808,'git_blob_sha1':'2308081e55c502505febc24e3e8bde66b07d5463','sha256':'0acc433d25fa436784b8a467cb780437a0ba80f9fb8925cb9e0916874ce8a5ec'},
 {'path':'assets/interior/interior-open-worktable-01/v1.0.0/generate.py','bytes':30478,'git_blob_sha1':'b39f3850fb4167f4536ec075871f992aef1a8c29','sha256':'b4880f9c24dda10b566fa215c394295b6522a8ad448486918c591826480c09d8'},
 {'path':'assets/interior/interior-open-worktable-01/v1.0.0/metadata.json','bytes':1606,'git_blob_sha1':'58b455a57f2836387feca1e2cf1640e1ad6c6ddd','sha256':'09788691add9172e1c82ef35ffa67c878dbceff10d34808e4d0f1998bcbea48a'},
 {'path':'assets/interior/interior-open-worktable-01/v1.0.0/model.glb','bytes':46720,'git_blob_sha1':'a72289a98d82a03f8d699ba065c62161ad1c7e0e','sha256':'78ec9cdb829e12c333ade0356adee759b8f95bdc7f037fe93ce946b0a487265b'},
 {'path':'assets/office/office-floorstanding-copier-01/v1.0.0/generate.py','bytes':37423,'git_blob_sha1':'770e0bb105d607e8be71146b1d2e45e04cf17613','sha256':'66c0e6f454905cc606db3bba3b081a164c7bd463ef074a07476b0b3ecc9f0db0'},
 {'path':'assets/office/office-floorstanding-copier-01/v1.0.0/metadata.json','bytes':1920,'git_blob_sha1':'491f6957db4729970ad3a1c21989e4fba2a051e6','sha256':'5f8385174dabb9e344b4ed1ea7e0f8d864cd4dbfdbf4b50c5b3105e629de9137'},
 {'path':'assets/office/office-floorstanding-copier-01/v1.0.0/model.glb','bytes':74168,'git_blob_sha1':'b2e80182efa6573b7312a7205ada5033856ce54a','sha256':'e9004c944a703afba469c7b14b0e654ad78235d74f5df2180abd86bc96f283a7'}]}
PAPER={'width_m':.210,'depth_m':.297,'thickness_m':.0002,'thickness_basis':'Explicit 0.2mm authored rigid static design, not paper-weight/manufacturing inference','origin':'bottom centre','printed_marks':'One original nonsemantic header and five line bars, top material regions only','base_color':[.83,.825,.78,1],'ink_color':[.13,.18,.205,1],'roughness':.87}
parser=argparse.ArgumentParser();parser.add_argument('--snapshot',type=Path);parser.add_argument('--qa',type=Path);parser.add_argument('--render-gray',action='store_true');parser.add_argument('--render-pbr',action='store_true');parser.add_argument('--render-final',action='store_true');parser.add_argument('--no-render',action='store_true');parser.add_argument('--threads',type=int,choices=range(1,9),default=2);parser.add_argument('--formal-views',default='isometric,front,back,left,right,top')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
QA=(args.qa or OUT/'qa').resolve();QA.mkdir(parents=True,exist_ok=True)
if args.no_render:assert not(args.render_gray or args.render_pbr or args.render_final)
required=[f['path'] for f in LOCK['files']]
SNAPSHOT=args.snapshot.resolve() if args.snapshot else next((p for p in (OUT,*OUT.parents) if all((p/f).is_file() for f in required)),None)
if SNAPSHOT is None:raise RuntimeError('Locked old source files missing. Use normal repository ancestors or --snapshot /path/to/source-root. R2 inputs require actual matching verification.')
def check_dependencies():
 for f in LOCK['files']:
  raw=(SNAPSHOT/f['path']).read_bytes();assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],('Dependency byte lock',f['path']);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==f['git_blob_sha1'],('Dependency Git blob',f['path'])
check_dependencies()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.name='Original_A4_Document_Standing_Copy_Staging';scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
asset=bpy.data.collections.new('ASSET__'+ASSET);scene.collection.children.link(asset)
def move(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
def empty(name,parent=None,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);asset.objects.link(o);o.parent=parent;o.location=loc;o.empty_display_type='PLAIN_AXES';o.empty_display_size=.08;return o
root=empty('PRESET__'+ASSET);root['asset_id']=ASSET;root['asset_kind']='scene';root['metadata_coordinate_space']='Preset-local metres; Blender Z up';root['metadata_to_gltf_mapping']='(x,y,z) -> (x,z,-y)';root['paper_design_parameters_json']=json.dumps(PAPER,sort_keys=True);root['static_scope']='Rigid original paper representation; no copying, scanning, feed, drawer operation, physics, reach, ergonomics or compliance claim';root['dependency_catalog_snapshot_commit']=LOCK['catalog_snapshot_commit'];root['source_id_and_origin_pin_mapping_json']=json.dumps(LOCK['source_id_and_pin_mapping'],sort_keys=True);root['requires_external_flat_game_ground_z_m']=0;root['layout_envelope_xy_minmax_m']=[-.40,1.95,-1.25,.40];root['layout_envelope_gltf_xz_minmax_m']=[-.40,1.95,-.40,1.25];root['source_recovery_status']='R2 reconstructed source, all output acceptance pending'

def triangles(obs,local=False):
 result=[]
 for o in obs:
  o.data.calc_loop_triangles();v=[(o.matrix_basis if local else o.matrix_world)@a.co for a in o.data.vertices]
  result.extend((o,tuple(v[i] for i in t.vertices),t.material_index) for t in o.data.loop_triangles)
 return result

def bounds(obs):
 v=[o.matrix_world@a.co for o in obs for a in o.data.vertices];lo=[min(a[i] for a in v) for i in range(3)];hi=[max(a[i] for a in v) for i in range(3)]
 return {'min':[round(a,8) for a in lo],'max':[round(a,8) for a in hi],'dimensions':[round(hi[i]-lo[i],8) for i in range(3)]}

def pbr(m):
 n=m.node_tree.nodes.get('Principled BSDF');assert n
 def val(v):
  try:return [round(float(x),6) for x in v]
  except TypeError:return round(float(v),6)
 return {k:val(n.inputs[k].default_value) for k in ['Base Color','Roughness','Metallic','Alpha','Emission Color','Emission Strength','Transmission Weight','IOR']}|{'backface_culling':m.use_backface_culling}

def records(obs,transform=None,local=False):
 rows=[]
 for o,t,mi in triangles(obs,local):
  pts=[tuple(round(float(x),5) for x in (transform@v if transform is not None else v)) for v in t];pts=min(tuple(pts[i:]+pts[:i]) for i in range(3));rows.append((pts,json.dumps(pbr(o.data.materials[mi]),sort_keys=True)))
 return rows

def fingerprint(obs,transform=None,local=False):return hashlib.sha256(json.dumps(sorted(records(obs,transform,local)),separators=(',',':')).encode()).hexdigest()

def clip(poly,axis,bound,greater):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-bound)*(1 if greater else -1);db=(b[axis]-bound)*(1 if greater else -1);ia=da>=-1e-9;ib=db>=-1e-9
  if ia:out.append(a)
  if ia!=ib:out.append(a+(b-a)*(da/(da-db)))
 return out

def area3(poly):return sum((poly[i]-poly[0]).cross(poly[i+1]-poly[0]).length/2 for i in range(1,len(poly)-1)) if len(poly)>2 else 0

def area2(poly):return abs(sum(a.x*b.y-b.x*a.y for a,b in zip(poly,poly[1:]+poly[:1])))/2 if len(poly)>2 else 0

def intersect_xy(subject,host):
 # Complete prior float64 clipping fix; no float32 Vector interpolation here.
 p=[(float(v.x),float(v.y)) for v in subject];q=[(float(v.x),float(v.y)) for v in host]
 sign=1 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(q,q[1:]+q[:1]))>=0 else -1
 for a,b in zip(q,q[1:]+q[:1]):
  rows=p;p=[]
  for u,v in zip(rows,rows[1:]+rows[:1]):
   du=sign*((b[0]-a[0])*(u[1]-a[1])-(b[1]-a[1])*(u[0]-a[0]));dv=sign*((b[0]-a[0])*(v[1]-a[1])-(b[1]-a[1])*(v[0]-a[0]));iu=du>=-1e-14;iv=dv>=-1e-14
   if iu:p.append(u)
   if iu!=iv:
    t=du/(du-dv);p.append((u[0]+(v[0]-u[0])*t,u[1]+(v[1]-u[1])*t))
  if not p:break
 return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))/2 if len(p)>2 else 0.

def flat_faces(obs,z,up):
 rows=[]
 for o,t,_ in triangles(obs):
  n=(t[1]-t[0]).cross(t[2]-t[0])
  if n.length>1e-12 and max(abs(v.z-z) for v in t)<2e-6 and n.normalized().z*(1 if up else -1)>.999:rows.append((o,t))
 return rows

def support(obs,z,host=None,contact_z=None):
 faces=flat_faces(obs,z if contact_z is None else contact_z,False)
 if host:tops=flat_faces(host,z,True)
 else:
  v=[Vector((-3,-3,z)),Vector((3,-3,z)),Vector((3,3,z)),Vector((-3,3,z))];tops=[(None,(v[0],v[1],v[2])),(None,(v[0],v[2],v[3]))]
 total=covered=0;rows=[]
 for o,t in faces:
  a=area2(t);c=min(a,sum(intersect_xy(t,u) for _,u in tops));total+=a;covered+=c;rows.append({'mesh':o.name,'area_m2':round(a,11),'covered_m2':round(c,11)})
 return {'plane_z_m':z,'tested_downward_plane_z_m':z if contact_z is None else contact_z,'actual_contact_triangles':len(faces),'actual_area_m2':round(total,11),'covered_area_m2':round(covered,11),'uncovered_area_m2':round(max(0,total-covered),11),'all_area_supported':total>1e-9 and total-covered<1e-8,'method':'Actual downward/upward triangle continuous area clipping, 2um coplanarity tolerance and 1e-8m2 area tolerance.','patches':rows}

def tree(obs):
 ts=triangles(obs);v=[p for _,t,_ in ts for p in t];return BVHTree.FromPolygons(v,[(i,i+1,i+2) for i in range(0,len(v),3)],all_triangles=True,epsilon=0),ts

def inside(bt,p):
 votes=[]
 for v in [(.811,.337,.479),(.257,.887,.383),(.419,.293,.861)]:
  d=Vector(v).normalized();pos=p.copy();hits=0
  for _ in range(256):
   q,n,i,distance=bt.ray_cast(pos,d,100)
   if q is None:break
   hits+=1;pos=q+d*1e-5
  votes.append(hits%2==1)
 return sum(votes)>=2

def collisions(a,b):
 ba=bounds(a);bb=bounds(b)
 if any(ba['max'][k]<bb['min'][k]-2e-6 or bb['max'][k]<ba['min'][k]-2e-6 for k in range(3)):return {'broad_phase_separated':True,'proper_crossings':0,'strict_containment_witnesses':0}
 ta,at=tree(a);tb,bt=tree(b);pairs=ta.overlap(tb);crossings=[];coplanar=0
 for ia,ib in pairs:
  qa=at[ia][1];qb=bt[ib][1];na=(qa[1]-qa[0]).cross(qa[2]-qa[0]).normalized();nb=(qb[1]-qb[0]).cross(qb[2]-qb[0]).normalized();da=[(v-qb[0]).dot(nb) for v in qa];db=[(v-qa[0]).dot(na) for v in qb]
  if abs(na.dot(nb))>.99999 and max(abs(x) for x in db)<2e-6:coplanar+=1
  elif min(da)<-2e-6 and max(da)>2e-6 and min(db)<-2e-6 and max(db)>2e-6:crossings.append([ia,ib])
 separating=[{'axis':'XYZ'[k],'max_a_m':ba['max'][k],'min_b_m':bb['min'][k],'max_b_m':bb['max'][k],'min_a_m':ba['min'][k],'overlap_depth_m':min(ba['max'][k],bb['max'][k])-max(ba['min'][k],bb['min'][k])} for k in range(3) if min(ba['max'][k],bb['max'][k])-max(ba['min'][k],bb['min'][k])<=2e-6]
 if separating:return {'broad_phase_separated':False,'bvh_surface_pairs':len(pairs),'coplanar_pairs':coplanar,'candidate_plane_straddles_at_tangent_contact':len(crossings),'proper_crossings':0,'strict_containment_witnesses':0,'actual_vertex_separating_planes':separating,'scope':'Actual vertex separating plane within 2um; opposed contact area tested separately.'}
 witnesses=[]
 for obs,dest,bd in [(a,tb,bb),(b,ta,ba)]:
  for o,t,_ in triangles(obs):
   n=(t[1]-t[0]).cross(t[2]-t[0]).normalized();q=sum(t,Vector())/3-n*.00005
   if all(bd['min'][k]+2e-6<q[k]<bd['max'][k]-2e-6 for k in range(3)):
    hit,normal,idx,dist=dest.find_nearest(q)
    if dist is not None and dist>2e-6 and inside(dest,q):witnesses.append({'mesh':o.name,'point_m':list(q),'clearance_m':dist});break
  if witnesses:break
 return {'broad_phase_separated':False,'bvh_surface_pairs':len(pairs),'coplanar_pairs':coplanar,'proper_crossings':len(crossings),'strict_containment_witnesses':len(witnesses),'witnesses':witnesses,'scope':'Actual triangle intersections plus inward centroid solid probes; no motion simulation.'}

def topology(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bad=[e for e in bm.edges if not e.is_manifold];loose=[v for v in bm.verts if not v.link_edges];deg=[f for f in bm.faces if f.calc_area()<1e-14];vol=bm.calc_volume(signed=True)
 result={'joined_vertex_tolerance_m':1e-7,'nonmanifold_edges':len(bad),'loose_vertices':len(loose),'degenerate_faces':len(deg),'signed_volume_m3':vol};bm.free();assert not bad and not loose and not deg and vol>1e-12,(o.name,result);return result

def solid_material(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=color;m.use_backface_culling=False;n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=color;n.inputs['Metallic'].default_value=0;n.inputs['Roughness'].default_value=PAPER['roughness'];return m

def make_paper(label,parent=None,xyz=(0,0,0),deg=0):
 # Matching grid boundaries on top, bottom and all edges make one closed solid.
 w=PAPER['width_m'];d=PAPER['depth_m'];h=PAPER['thickness_m'];xs=[-w/2,-.077,.075,w/2]
 bands=[(-.031,-.027),(-.006,-.002),(.019,.023),(.044,.048),(.069,.073),(.0985,.1105)]
 ys=sorted([-d/2,d/2]+[v for pair in bands for v in pair]);nx=len(xs);ny=len(ys)
 verts=[(x,y,z) for z in [0,h] for y in ys for x in xs]
 def vi(k,i,j):return k*nx*ny+j*nx+i
 faces=[];mats=[]
 for j in range(ny-1):
  for i in range(nx-1):
   faces.append((vi(0,i,j+1),vi(0,i+1,j+1),vi(0,i+1,j),vi(0,i,j)));mats.append(0)
   faces.append((vi(1,i,j),vi(1,i+1,j),vi(1,i+1,j+1),vi(1,i,j+1)))
   yc=(ys[j]+ys[j+1])/2;mats.append(1 if i==1 and any(lo<yc<hi for lo,hi in bands) else 0)
 for i in range(nx-1):
  faces.extend([(vi(0,i,0),vi(0,i+1,0),vi(1,i+1,0),vi(1,i,0)),(vi(0,i+1,ny-1),vi(0,i,ny-1),vi(1,i,ny-1),vi(1,i+1,ny-1))]);mats.extend([0,0])
 for j in range(ny-1):
  faces.extend([(vi(0,0,j+1),vi(0,0,j),vi(1,0,j),vi(1,0,j+1)),(vi(0,nx-1,j),vi(0,nx-1,j+1),vi(1,nx-1,j+1),vi(1,nx-1,j))]);mats.extend([0,0])
 me=bpy.data.meshes.new('Original A4 closed paper material grid');me.from_pydata(verts,[],faces);me.update();me.materials.append(solid_material('Warm off-white rigid paper',PAPER['base_color']));me.materials.append(solid_material('Original nonsemantic document ink',PAPER['ink_color']))
 for p,mi in zip(me.polygons,mats):p.material_index=mi
 o=bpy.data.objects.new(label,me);asset.objects.link(o);o.parent=parent;o.location=xyz;o.rotation_euler.z=math.radians(deg);o['original_design_id']='AUTHORED_A4';o['paper_width_depth_thickness_m']=[w,d,h];o['thickness_is_authored_design_value']=True;o['printed_marks_are_surface_material_regions']=True;o['static_rigid_sheet']=True;return o

instances={};groups={};placements=[];sources={};source_rows=[];source_hash={}
for f in LOCK['files']:
 if not f['path'].endswith('/model.glb'):continue
 path=SNAPSHOT/f['path'];aid=path.parent.parent.name;before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path),merge_vertices=False);added=[o for o in bpy.data.objects if o not in before];obs=[o for o in added if o.type=='MESH'];assert obs;bpy.context.view_layer.update()
 for o in obs:
  mw=o.matrix_world.copy();o.parent=None;o.matrix_world=mw;move(o,asset)
 for o in added:
  if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.view_layer.update();sources[aid]=obs;meta=json.loads((path.parent/'metadata.json').read_text());b=bounds(obs);assert max(abs(b['dimensions'][i]-meta['bounds'][k]) for i,k in enumerate('xyz'))<1e-4
 source_hash[aid]=fingerprint(obs);source_rows.append({'id':aid,'catalog_source_and_origin':LOCK['source_id_and_pin_mapping'][aid],'glb_sha256':f['sha256'],'mesh_nodes':len(obs),'triangles':len(triangles(obs)),'actual_bounds_m':b,'source_geometry_pbr_sha256_10um':source_hash[aid],'per_mesh_closed_topology':{o.name:topology(o) for o in obs}})

def place_old(aid,label,xyz):
 g=empty('INSTANCE__'+label,root,xyz);groups[label]=g;mapping=LOCK['source_id_and_pin_mapping'][aid];obs=[]
 for orig in sources[aid]:
  o=orig.copy();o.data=orig.data;asset.objects.link(o);o.parent=g;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=orig.matrix_world.copy();o.name=label+'__'+orig.name
  for target in [g,o]:
   target['instance_label']=label;target['source_asset_id']=aid;target['source_version']='1.0.0';target['source_commit']=mapping['origin_pin'];target['catalog_source_id']=mapping['sourceId'];target['dependency_catalog_snapshot_commit']=LOCK['catalog_snapshot_commit'];target['complete_source_instance']=True;target['reused_not_new_asset']=True
  o['source_mesh_name']=orig.name;obs.append(o)
 bpy.context.view_layer.update();assert fingerprint(obs,local=True)==source_hash[aid],('Changed old mesh or PBR',label);instances[label]=obs;placements.append({'label':label,'source_asset_id':aid,**mapping,'translation_blender_m':list(xyz),'translation_gltf_m':[xyz[0],xyz[2],-xyz[1]],'rotation_degrees':[0,0,0],'scale':[1,1,1],'complete_source_meshes':len(obs),'source_geometry_pbr_preserved':True,'actual_bounds_m':bounds(obs)})

place_old('office-floorstanding-copier-01','standing_copier',(0,0,0));place_old('interior-open-worktable-01','document_staging_table',(1.24,0,0));table_z=bounds(instances['document_staging_table'])['max'][2];place_old('bakery-shallow-baking-tray-01','original_metal_staging_tray',(1.24,0,table_z))
tray_floor_z=table_z+.003;output_parts=[o for o in instances['standing_copier'] if o['source_mesh_name']=='Output collection tray'];assert len(output_parts)==1;output_z=bounds(output_parts)['max'][2]
for label,xyz,deg in [('pickup_document',(0,-.15,output_z),0),('staged_document',(1.24,0,tray_floor_z),90)]:
 g=empty('ORIGINAL__'+label,root,xyz);g.rotation_euler.z=math.radians(deg);g['instance_label']=label;groups[label]=g;o=make_paper('AUTHORED_A4__'+label,g);o['instance_label']=label;g['original_design_id']='AUTHORED_A4';g['new_original_geometry']=True;instances[label]=[o]
for obs in sources.values():
 for o in obs:bpy.data.objects.remove(o,do_unlink=True)
bpy.context.view_layer.update();all_asset=[o for obs in instances.values() for o in obs]
for o in all_asset:assert all(abs(v-1)<1e-6 for v in o.scale),(o.name,list(o.scale))

ports=[];routes=[];standing=[]
def region(name,box,role,kind,connects=()):
 lo=[box[0],box[2],box[4]];hi=[box[1],box[3],box[5]];dims=[hi[i]-lo[i] for i in range(3)];assert min(dims)>0
 e=empty('REGION__'+name,root,[(lo[i]+hi[i])/2 for i in range(3)]);e['region_id']=name;e['role']=role;e['region_kind']=kind;e['box_xyz_minmax_m']=box;e['gltf_box_xyz_minmax_m']=[box[0],box[1],box[4],box[5],-box[3],-box[2]];e['dimensions_xyz_m']=dims;e['gltf_dimensions_xyz_m']=[dims[0],dims[2],dims[1]];e['connects_to']=json.dumps(list(connects));e['static_only']=True;e['metadata_to_gltf_mapping']='(x,y,z) -> (x,z,-y)'
 row={'id':name,'node':e.name,'box':box,'gltf_box_xyz_minmax_m':list(e['gltf_box_xyz_minmax_m']),'role':role,'kind':kind,'connects_to':list(connects)};ports.append(row);return row
routes.append(region('front_transfer_corridor',[-.325,1.565,-1.145,-.495,0,2.2],'Complete reserved front transfer region','body_route',['pickup_stand','staging_stand','west_entry','east_exit']))
routes.append(region('pickup_stand',[-.3,.3,-1.145,-.545,0,2.2],'Static .60 by .60m pickup reference footprint','body_route',['front_transfer_corridor']))
routes.append(region('staging_stand',[.94,1.54,-1.145,-.545,0,2.2],'Static .60 by .60m staging reference footprint','body_route',['front_transfer_corridor']))
routes.append(region('west_entry',[-.325,-.025,-1.145,-.495,0,2.2],'Finite-width surrounding-game-level connection','body_route',['front_transfer_corridor']))
routes.append(region('east_exit',[1.265,1.565,-1.145,-.495,0,2.2],'Finite-width surrounding-game-level connection','body_route',['front_transfer_corridor']))
hand_regions=[region('copier_front_static_access',[-.1,.1,-.70,-.285,.65,.77],'Empty static front prism; no human hand/reach certification','access_volume',['pickup_stand']),region('staging_tray_static_top_access',[1.06,1.42,-.70,.15,.93,1.13],'Whole static empty prism from stand to above original tray; no arm reach or paper-motion certification','access_volume',['staging_stand'])]
for label in ['pickup_document','staged_document']:
 b=bounds(instances[label]);e=empty('PORT__'+label,root,[(b['min'][i]+b['max'][i])/2 for i in range(3)]);e['port_id']=label;e['document_instance_label']=label;e['occupied_document_bounds_blender_json']=json.dumps(b);e['gltf_port_position_m']=[e.location.x,e.location.z,-e.location.y];e['static_only']=True;e['function']='visible copier pickup' if label=='pickup_document' else 'visible temporary tray staging'
for name,x in [('pickup',0),('staging',1.24)]:
 r=[x-.3,x+.3,-1.145,-.545];e=empty('STAND__'+name,root,(x,-.845,0));e['standing_center_xy_m']=[x,-.845];e['footprint_width_depth_m']=[.6,.6];e['body_height_target_m']=2.2;e['gltf_footprint_xz_minmax_m']=[r[0],r[1],-r[3],-r[2]];e['static_geometric_reference_only']=True;standing.append({'id':name,'center_xy_m':[x,-.845],'footprint_xy_minmax_m':r,'gltf_footprint_xz_minmax_m':list(e['gltf_footprint_xz_minmax_m']),'body_height_target_m':2.2,'whole_footprint_inside_corridor':r[0]>=-.325 and r[1]<=1.565 and r[2]>=-1.145 and r[3]<=-.495})
access_connections=[]
for access_region in hand_regions:
 for target in access_region['connects_to']:
  body=next(r for r in routes if r['id']==target);a=access_region['box'];b=body['box'];overlap=[min(a[i+1],b[i+1])-max(a[i],b[i]) for i in [0,2,4]]
  row={'access_region':access_region['id'],'body_region':target,'actual_overlap_dimensions_blender_xyz_m':overlap,'positive_volume_overlap_m3':max(0,overlap[0])*max(0,overlap[1])*max(0,overlap[2]),'positive_volume_connected':all(v>1e-6 for v in overlap),'scope':'Static overlapping empty reference volumes only; no reach, transport or dynamics claim.'};assert row['positive_volume_connected'],row;access_connections.append(row)

def prism_test(r,obs):
 hits=[];b=r['box']
 for o,t,_ in triangles(obs):
  poly=list(t)
  for axis,(lo,hi) in enumerate(((b[0],b[1]),(b[2],b[3]),(b[4],b[5]))):poly=clip(clip(poly,axis,lo,True),axis,hi,False)
  a=area3(poly)
  if a>1e-10:hits.append({'mesh':o.name,'triangle_area_in_prism_m2':a})
 center=Vector(((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2));inside_witnesses=[]
 for o in obs:
  bb=bounds([o])
  if all(bb['min'][k]+1e-6<center[k]<bb['max'][k]-1e-6 for k in range(3)) and inside(tree([o])[0],center):inside_witnesses.append(o.name)
 return {**r,'clear':not hits and not inside_witnesses,'actual_triangle_intrusions':len(hits),'intrusions':hits[:10],'solid_containment_witnesses':inside_witnesses,'method':'Every actual triangle clipped against whole finite prism, plus enclosed center rejection per closed mesh; not route point sampling.'}

def geometry_report(data):
 rows=[];op=[o for o in data['standing_copier'] if o['source_mesh_name']=='Output collection tray']
 contacts=[('standing_copier',0,None),('document_staging_table',0,None),('original_metal_staging_tray',table_z,'document_staging_table'),('pickup_document',output_z,'standing_copier'),('staged_document',tray_floor_z,'original_metal_staging_tray')]
 for label,z,host in contacts:
  actual_host=op if label=='pickup_document' else data[host] if host else None;rows.append({'instance':label,'host':host or 'external flat ground datum Z=0','support':support(data[label],z,actual_host)})
 route_tests=[prism_test(r,[o for obs in data.values() for o in obs]) for r in routes+hand_regions];pairs=[]
 for i,a in enumerate(data):
  for b in list(data)[i+1:]:pairs.append({'instances':[a,b],**collisions(data[a],data[b])})
 return {'supports':rows,'all_contacts_supported':all(r['support']['all_area_supported'] for r in rows),'route_and_access_prisms':route_tests,'all_prisms_clear':all(r['clear'] for r in route_tests),'cross_instance_collisions':pairs,'no_cross_instance_positive_penetration_detected':all(r['proper_crossings']==0 and r['strict_containment_witnesses']==0 for r in pairs)}
geometry=geometry_report(instances)

def shifted(label,delta,fn):
 g=groups[label];saved=g.location.copy();g.location+=Vector(delta);bpy.context.view_layer.update()
 try:return fn()
 finally:g.location=saved;bpy.context.view_layer.update()
negative=[]
for label,z,host in [('pickup_document',output_z,output_parts),('staged_document',tray_floor_z,instances['original_metal_staging_tray'])]:
 r=shifted(label,(0,0,.012),lambda:support(instances[label],z,host));negative.append({'fixture':label+' lifted 12mm','support':r,'rejected':not r['all_area_supported']})
r=shifted('staged_document',(.30,0,0),lambda:support(instances['staged_document'],tray_floor_z,instances['original_metal_staging_tray']));negative.append({'fixture':'A4 +300mm X off original tray','support':r,'rejected':not r['all_area_supported']})
r=shifted('original_metal_staging_tray',(.5,0,0),lambda:support(instances['original_metal_staging_tray'],table_z,instances['document_staging_table']));negative.append({'fixture':'Original tray +500mm X off table','support':r,'rejected':not r['all_area_supported']})
r=shifted('standing_copier',(0,-.45,0),lambda:prism_test(routes[0],all_asset));negative.append({'fixture':'Copier moved into full standing corridor','route':r,'rejected':not r['clear']})
(QA/'preexport-geometry-diagnostic.json').write_text(json.dumps({'geometry':geometry,'negative_controls':negative},indent=2)+'\n')
assert geometry['all_contacts_supported'] and geometry['all_prisms_clear'] and geometry['no_cross_instance_positive_penetration_detected'],geometry
assert all(r['rejected'] for r in negative),negative
source_topology={o.name:topology(o) for o in all_asset}
bpy.ops.object.select_all(action='DESELECT')
for o in asset.objects:o.select_set(True)
bpy.context.view_layer.objects.active=root;scene['candidate_stage']='R2 reconstructed source: independent acceptance pending';scene['diagnostics_exported']=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'));bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_extras=True)
raw=(OUT/'model.glb').read_bytes();jl=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+jl]);gn=gltf['nodes'];assert not any(n.get('name','').startswith('DIAGNOSTIC') for n in gn)
region_nodes=[n for n in gn if n.get('extras',{}).get('region_id')];assert len(region_nodes)==len(ports)
for n in region_nodes:
 e=n['extras'];b=e['box_xyz_minmax_m'];assert e['gltf_box_xyz_minmax_m']==[b[0],b[1],b[4],b[5],-b[3],-b[2]]
before_sig=fingerprint(all_asset);before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);added=[o for o in bpy.data.objects if o not in before];reobs=[o for o in added if o.type=='MESH'];bpy.context.view_layer.update();after_sig=fingerprint(reobs);actual={label:[o for o in reobs if o.get('instance_label')==label] for label in instances};assert all(actual.values())
actual_geometry=geometry_report(actual);actual_topology={o.name:topology(o) for o in reobs};assert before_sig==after_sig,(before_sig,after_sig)
roundtrip={'actual_exported_glb_reimported':True,'complete_world_oriented_triangles_pbr_equal_10um':before_sig==after_sig,'before_sha256':before_sig,'after_sha256':after_sig,'source_mesh_nodes':len(all_asset),'imported_mesh_nodes':len(reobs),'source_triangles':len(triangles(all_asset)),'imported_triangles':len(triangles(reobs)),'actual_reimport_geometry_tests':actual_geometry,'actual_reimport_per_mesh_closed_topology':actual_topology,'exported_finite_region_nodes':len(region_nodes),'coordinate_extras_checked':True,'diagnostic_nodes_exported':False}
for o in added:bpy.data.objects.remove(o,do_unlink=True)
check_dependencies()
gate={'all_source_contacts_supported':geometry['all_contacts_supported'],'all_imported_contacts_supported':actual_geometry['all_contacts_supported'],'all_source_and_imported_prisms_clear':geometry['all_prisms_clear'] and actual_geometry['all_prisms_clear'],'no_cross_instance_positive_penetration_detected':geometry['no_cross_instance_positive_penetration_detected'] and actual_geometry['no_cross_instance_positive_penetration_detected'],'all_negative_controls_rejected':all(r['rejected'] for r in negative),'complete_world_triangle_pbr_roundtrip':before_sig==after_sig,'all_independent_parts_closed':True,'all_full_standing_footprints_inside_corridor':all(r['whole_footprint_inside_corridor'] for r in standing),'independent_gray_review':'PENDING_R2','original_pbr_review':'PENDING_R2','final_independent_qa':'PENDING_R2','local_firefox':'PENDING_R2','approved':False}
limits=['Rigid authored 0.2mm paper geometry; no bending, folding or paper simulation.','No printing, scanning, feeding, drawer operation, electrical, load, reach, ergonomics, accessibility or safety/code certification.','Original nonsemantic document marks; no text, brands or personal data.','Complete old source PBR and mesh at unit scale; no cabinet or new file tray.','Original shallow metal tray supports the planned landscape A4 on its real floor; actual contacts are tested at this run.','External flat game ground Z=0 required; studio ground is not asset geometry.','R2 reconstruction is a new source file; previous results do not approve this file or its outputs.']
report={'id':ASSET,'source_stage':'recovery-r2-source-stage01','stage':'new reconstruction geometry, independent acceptance pending','approved':False,'art_passed':False,'paper_design':PAPER,'coordinate_contract':{'blender':'local X/Y horizontal, Z up, metres','gltf':'local X/Z horizontal, Y up, metres','conversion':'(x,y,z) -> (x,z,-y)'},'source_measurements':source_rows,'placements':placements,'instance_count':len(instances),'paper_instance_count':2,'reused_source_ids':3,'geometry_bounds_m':bounds(all_asset),'triangles':len(triangles(all_asset)),'materials':len(gltf.get('materials',[])),'geometry_tests':geometry,'original_per_mesh_closed_topology':source_topology,'negative_controls':negative,'standing_footprints':standing,'access_connections':access_connections,'roundtrip':roundtrip,'gate':gate,'limits':limits}
(QA/'geometry-report.json').write_text(json.dumps(report,indent=2)+'\n');(QA/'roundtrip-report.json').write_text(json.dumps(roundtrip,indent=2)+'\n')
composition={'id':ASSET,'assetKind':'scene','embedded_dependency_lock':True,'paper_design':PAPER,'instances':placements,'regions':ports,'standing_footprints':standing,'access_connections':access_connections,'reuse_counting':{'new_scene_presets':1,'new_standalone_props':0,'authored_A4_mesh_nodes':2,'reused_old_ids':3,'new_file_trays':0},'limits':limits};(QA/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
print('R2_GEOMETRY_GATE_READY',ASSET,json.dumps(gate),flush=True)

def emit_metadata():
 if not (OUT/'thumbnail.png').is_file():return
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  b=(OUT/name).read_bytes();files[role]={'path':f'assets/office/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 description='Static standing copy-pickup to tabletop document-staging preset with complete unchanged legacy floor copier, worktable and reused shallow metal tray; two independently editable original A4 nodes occupy pickup and storage endpoints. Finite standing/access metadata includes Blender/glTF coordinates. Authored static paper thickness .0002m, not a manufacturing claim. No printing, feeding, bending, drawer motion, human-reach or compliance simulation. Reconstructed r2 source; independent acceptance required.'
 md={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'office','style':'source-preserved-S01-and-satin-metal','title':'Standing Copier Pickup and Document Staging','description':description,'bounds':dict(zip('xyz',report['geometry_bounds_m']['dimensions']),unit='m'),'triangles':report['triangles'],'materials':report['materials'],'files':files,'status':'review','license':'All rights reserved'};(OUT/'metadata.json').write_text(json.dumps(md,indent=2)+'\n')

if args.render_gray or args.render_pbr or args.render_final:
 from bpy_extras.object_utils import world_to_camera_view
 render_scene=bpy.data.scenes.new('STUDIO__actual_exported_GLB');bpy.context.window.scene=render_scene;bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);render_parts=[o for o in render_scene.objects if o.type=='MESH'];assert fingerprint(render_parts)==before_sig
 render_scene.render.engine='CYCLES';render_scene.cycles.device='CPU';render_scene.cycles.use_denoising=False;render_scene.render.threads_mode='FIXED';render_scene.render.threads=args.threads;render_scene.render.resolution_x=896 if args.render_final else 768;render_scene.render.resolution_y=896 if args.render_final else 768;render_scene.render.resolution_percentage=100;render_scene.render.image_settings.file_format='PNG';render_scene.view_settings.view_transform='AgX';render_scene.view_settings.exposure=0;render_scene.view_settings.gamma=1
 render_scene.world=bpy.data.worlds.new('Fixed neutral studio');render_scene.world.use_nodes=True;wn=render_scene.world.node_tree.nodes['Background'];wn.inputs['Color'].default_value=(.5,.5,.5,1);wn.inputs['Strength'].default_value=.5
 def studio_material(name,color):
  m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*color,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85;return m
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.004));floor=bpy.context.object;floor.name='RENDER ONLY ground';floor.data.materials.append(studio_material('RENDER ONLY neutral ground',(.25,.27,.28)))
 def aim(o,xyz,target):o.location=xyz;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,xyz,power,size in [('Key',(-4,-5,8),1400,5),('Fill',(5,-1,5),700,4),('Rim',(0,5,7),1000,4)]:
  bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name='RENDER ONLY '+name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;aim(light,xyz,(.6,0,.4))
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='RENDER ONLY fitted orthographic camera';cam.data.type='ORTHO';cam.data.clip_start=.001;cam.data.clip_end=200;render_scene.camera=cam
 b=bounds(render_parts);center=Vector([(b['min'][i]+b['max'][i])/2 for i in range(3)]);dirs={'isometric':Vector((6,-8,7 if args.render_gray else 4)),'front':Vector((0,-10,0)),'back':Vector((0,10,0)),'left':Vector((-10,0,0)),'right':Vector((10,0,0)),'top':Vector((0,0,10))}
 def fitted_render(name,file,samples):
  render_scene.cycles.samples=samples;cam.location=center+dirs[name]
  if name=='top':cam.rotation_euler=(0,0,0)
  else:aim(cam,cam.location,center)
  bpy.context.view_layer.update();pp=[cam.matrix_world.inverted()@(o.matrix_world@v.co) for o in render_parts for v in o.data.vertices];lo=[min(v[k] for v in pp) for k in [0,1]];hi=[max(v[k] for v in pp) for k in [0,1]];cam.location+=cam.matrix_world.to_3x3()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0));cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*1.20;bpy.context.view_layer.update();uv=[world_to_camera_view(render_scene,cam,o.matrix_world@v.co) for o in render_parts for v in o.data.vertices];fr={'min_u':min(v.x for v in uv),'max_u':max(v.x for v in uv),'min_v':min(v.y for v in uv),'max_v':max(v.y for v in uv)};assert all(.03<v.x<.97 and .03<v.y<.97 for v in uv),fr
  render_scene.render.filepath=str(file);bpy.ops.render.render(write_still=True);return {'path':file.name,'samples':samples,'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'camera_location_m':list(cam.location),'camera_rotation_radians':list(cam.rotation_euler),'orthographic_scale_m':cam.data.ortho_scale,'actual_projection_bbox':fr}
 if args.render_gray:
  clay=studio_material('DIAGNOSTIC monochrome furniture',(.45,.46,.47));paperclay=studio_material('DIAGNOSTIC monochrome paper',(.8,.8,.8));inkclay=studio_material('DIAGNOSTIC monochrome printed marks',(.13,.13,.13));saved=[]
  for o in render_parts:
   o.data=o.data.copy();saved.append((o,list(o.data.materials)))
   for i in range(len(o.data.materials)):o.data.materials[i]=inkclay if o.get('original_design_id') and i==1 else paperclay if o.get('original_design_id') else clay
  gray={}
  for name in ['isometric','top']:gray[name]=fitted_render(name,QA/('gray-'+name+'.png'),24);print('R2_GRAY_VIEW_READY',ASSET,name,flush=True)
  (QA/'gray-view-manifest.json').write_text(json.dumps({'asset':ASSET,'source_glb_sha256':hashlib.sha256(raw).hexdigest(),'views':gray,'scope':'New r2 diagnostic monochrome materials on fresh actual GLB import; never exported; acceptance pending'},indent=2)+'\n')
  for o,ms in saved:
   for i,m in enumerate(ms):o.data.materials[i]=m
 if args.render_pbr:
  row=fitted_render('isometric',QA/'original-pbr-coordination.png',48);(QA/'pbr-coordination-manifest.json').write_text(json.dumps({'asset':ASSET,'source_glb_sha256':hashlib.sha256(raw).hexdigest(),'view':row,'fixed_studio':True,'recovery_stage':'r2_new_acceptance_required'},indent=2)+'\n');print('R2_PBR_VIEW_READY',ASSET,flush=True)
 if args.render_final:
  manifest={'asset':ASSET,'source_glb_sha256':hashlib.sha256(raw).hexdigest(),'actual_glb_geometry_pbr_sha256_10um':before_sig,'samples_all_views':128,'cpu_threads':args.threads,'denoising':False,'resolution':[896,896],'coordinate_space':'Blender Z-up world metres; front -Y, back +Y, left -X, right +X, top +Z','fixed_studio':{'world_strength':.5,'exposure':0,'gamma':1,'lights_watts':[1400,700,1000]},'recovery_stage':'r2_new_acceptance_required','views':{}}
  existing=QA/'formal-view-manifest.json'
  if existing.is_file():
   previous=json.loads(existing.read_text())
   if previous.get('source_glb_sha256')==manifest['source_glb_sha256']:manifest['views'].update(previous.get('views',{}))
  views=args.formal_views.split(',');assert len(views)==len(set(views)) and all(v in dirs for v in views)
  for name in views:
   manifest['views'][name]=fitted_render(name,QA/('qa-'+name+'.png'),128);existing.write_text(json.dumps(manifest,indent=2)+'\n')
   if name=='isometric':(OUT/'thumbnail.png').write_bytes((QA/'qa-isometric.png').read_bytes())
   print('R2_FORMAL_VIEW_READY',ASSET,name,flush=True)
  assert fingerprint(render_parts)==before_sig,'Studio changed original material or geometry'
  print('R2_FORMAL_RENDER_SET_READY',ASSET,sorted(manifest['views']),flush=True)
emit_metadata()
print('R2_CANDIDATE_READY_ACCEPTANCE_PENDING',ASSET,'scene',len(all_asset),report['triangles'],flush=True)
