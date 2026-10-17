"""Static coffee order-to-ceramic-pickup game layout; complete pinned source assets.

Normal repository: blender -b -t 2 --python assets/cafe/cafe-order-pickup-counter-scene-01/v1.0.0/generate.py
Minimal published-source recovery: add -- --snapshot /path/to/source-root --qa /path/to/qa.
--render-gray produces only two diagnostic clay views; --render-pbr produces one
original-material coordination view. No diagnostic geometry is exported.
All provenance, dependency byte locks and layout parameters are embedded here;
no unpublished sidecar or dot-specific absolute path is required.
--render-final adds the six clean original-PBR standard directions at 128 samples (back: 512)
and promotes its isometric bytes to thumbnail.png. Optional --formal-views can
select directions, and --render-threads accepts 2 (default) or 4.
This is a static game preset, not payment, brewing, navigation, safety or code compliance.
"""
import argparse,hashlib,json,math,sys,struct
from collections import Counter
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent
ASSET='cafe-order-pickup-counter-scene-01'
LOCK={'repository': 'shAdow-XJY-Games/Shadow3DAssetLibrary', 'commit': '034142c2d18816fe3c2096be20b29175b3c63813', 'tree': 'd208f07bd15607e197397af0eeb6ff0e29f1b21b', 'recovery_kind': 'exact four-ID minimal published-source snapshot; original GLBs kept complete, source generators not executed', 'catalog_source_mapping': {'cafe-countertop-espresso-machine-01': {'catalog_source_id': 'cafe-espresso-extension', 'catalog_source_commit': 'eabbea86f4039715c77eb21383fbf838a95de2a4'}, 'dining-service-counter-01': {'catalog_source_id': 'expanded-collection', 'catalog_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, 'interior-open-worktable-01': {'catalog_source_id': 'access-core', 'catalog_source_commit': 'e179cdc82c1f57e36dc0a78704146783f711484d'}, 'kitchen-mug-01': {'catalog_source_id': 'expanded-collection', 'catalog_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}}, 'files': [{'path': 'assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/generate.py', 'bytes': 36449, 'git_blob_sha1': '4eb9e55a514083996fcd0dac9976d7da779a949b', 'sha256': '71335932447bab296473a070db799f570aee6e1cfc3fb61128b53fea4f04d8e0', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/generate.py', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'eabbea86f4039715c77eb21383fbf838a95de2a4'}, {'path': 'assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/metadata.json', 'bytes': 2013, 'git_blob_sha1': '8d76586572e8a52ed37256a7fa37bffbd1b630c6', 'sha256': '2fc329a3f242a3aff948df579426fe7063ad8b5aac5a7fac7f866b3fcc5961fc', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/metadata.json', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'eabbea86f4039715c77eb21383fbf838a95de2a4'}, {'path': 'assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/model.glb', 'bytes': 91740, 'git_blob_sha1': 'bd84ef6a477bd38f08c14497feed1a1481c8e50f', 'sha256': 'a69dd818c7a2d928d9c315b9bbc05442b17bafa8542fc7b793870d707181c402', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/cafe/cafe-countertop-espresso-machine-01/v1.0.0/model.glb', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'eabbea86f4039715c77eb21383fbf838a95de2a4'}, {'path': 'assets/dining/dining-service-counter-01/v1.0.0/generate.py', 'bytes': 9935, 'git_blob_sha1': '0ae5cf4578237bab51f0ac7a44b63be149a1e655', 'sha256': 'c8b32d0f843a7ea660533d96110ea36eacd136077c1184c14ae9a45d3acb0d3b', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/dining/dining-service-counter-01/v1.0.0/generate.py', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, {'path': 'assets/dining/dining-service-counter-01/v1.0.0/metadata.json', 'bytes': 1591, 'git_blob_sha1': 'ea7cbeff00576fa8b2fb9807568949b4d7fc58a4', 'sha256': 'ffdeab56f236b9226cedf9ff11c495982d6b8ad19796abe8e5005d8a4bf0a703', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/dining/dining-service-counter-01/v1.0.0/metadata.json', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, {'path': 'assets/dining/dining-service-counter-01/v1.0.0/model.glb', 'bytes': 25756, 'git_blob_sha1': '9c9da302879912a69e0537a46995d8bacb35d976', 'sha256': 'e1351b492c8fc1ceb0a6fd1509161acd0caec27211f3c626e5b7e919d1f8bcab', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/dining/dining-service-counter-01/v1.0.0/model.glb', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, {'path': 'assets/interior/interior-open-worktable-01/v1.0.0/generate.py', 'bytes': 30478, 'git_blob_sha1': 'b39f3850fb4167f4536ec075871f992aef1a8c29', 'sha256': 'b4880f9c24dda10b566fa215c394295b6522a8ad448486918c591826480c09d8', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/interior/interior-open-worktable-01/v1.0.0/generate.py', 'materialized_from': 'hash-verified existing local recovery', 'catalog_asset_source_commit': 'e179cdc82c1f57e36dc0a78704146783f711484d'}, {'path': 'assets/interior/interior-open-worktable-01/v1.0.0/metadata.json', 'bytes': 1606, 'git_blob_sha1': '58b455a57f2836387feca1e2cf1640e1ad6c6ddd', 'sha256': '09788691add9172e1c82ef35ffa67c878dbceff10d34808e4d0f1998bcbea48a', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/interior/interior-open-worktable-01/v1.0.0/metadata.json', 'materialized_from': 'hash-verified existing local recovery', 'catalog_asset_source_commit': 'e179cdc82c1f57e36dc0a78704146783f711484d'}, {'path': 'assets/interior/interior-open-worktable-01/v1.0.0/model.glb', 'bytes': 46720, 'git_blob_sha1': 'a72289a98d82a03f8d699ba065c62161ad1c7e0e', 'sha256': '78ec9cdb829e12c333ade0356adee759b8f95bdc7f037fe93ce946b0a487265b', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/interior/interior-open-worktable-01/v1.0.0/model.glb', 'materialized_from': 'hash-verified existing local recovery', 'catalog_asset_source_commit': 'e179cdc82c1f57e36dc0a78704146783f711484d'}, {'path': 'assets/kitchen/kitchen-mug-01/v1.0.0/generate.py', 'bytes': 9205, 'git_blob_sha1': 'c78385398a70bb53c31c0959e6449e87fb95ebab', 'sha256': 'f8f5bda63bcc4c9c4da68203ac2fb1909339c1a69ec15ca4513b50669047e8d5', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/kitchen/kitchen-mug-01/v1.0.0/generate.py', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, {'path': 'assets/kitchen/kitchen-mug-01/v1.0.0/metadata.json', 'bytes': 1275, 'git_blob_sha1': '4ddabf6fa7a7354ee3fb3c79700a6d054f1cbed4', 'sha256': 'b907f691ae5b5a5678075a6ad73b36c6bb94a706e89599746e956b921eba277a', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/kitchen/kitchen-mug-01/v1.0.0/metadata.json', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}, {'path': 'assets/kitchen/kitchen-mug-01/v1.0.0/model.glb', 'bytes': 40784, 'git_blob_sha1': '0b017f4ce9ffebb9decd815b5540ccdefdbb8296', 'sha256': '688bd42250f0434acef8801df1280caca75ab93c75e0c426ecaec31b3307fca8', 'source_url': 'https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/034142c2d18816fe3c2096be20b29175b3c63813/assets/kitchen/kitchen-mug-01/v1.0.0/model.glb', 'materialized_from': 'GitHub fixed-commit fetch_file base64', 'catalog_asset_source_commit': 'a4f9ab53d3bb40010aa60c4f77669622055ec724'}]}

LAYOUT={'counter_centers_x_m':[-.67,.67],'counter_y_m':0,'counter_rotation_z_deg':180,'table_origin_m':[0,1.75,0],'machine_origin_xy_m':[0,1.75],'pickup_mug_origin_xy_m':[.67,-.04],'geometry_scale':[1,1,1],'layout_envelope_m':{'x':[-1.95,1.95],'y':[-1.65,2.15]},'staff_reserved_box_m':[-1.75,1.75,.30,1.40,.001,2.20],'customer_reserved_box_m':[-1.75,1.75,-1.60,-.30,.001,2.20]}
p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path);p.add_argument('--qa',type=Path);p.add_argument('--render-gray',action='store_true');p.add_argument('--render-pbr',action='store_true');p.add_argument('--render-final',action='store_true');p.add_argument('--render-threads',type=int,choices=[2,4],default=2);p.add_argument('--formal-views',default='isometric,front,back,left,right,top')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
QA=(args.qa or OUT/'qa').resolve();QA.mkdir(parents=True,exist_ok=True)
required=[f['path'] for f in LOCK['files']]
SNAPSHOT=args.snapshot.resolve() if args.snapshot else next((q for q in (OUT,*OUT.parents) if all((q/f).is_file() for f in required)),None)
if SNAPSHOT is None:raise RuntimeError('Pinned assets not found beneath a repository ancestor. Supply --snapshot /path/to/published-source-root.')
def check_dependencies():
 for f in LOCK['files']:
  b=(SNAPSHOT/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],('Dependency byte lock mismatch',f['path']);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha1'],('Git blob mismatch',f['path'])
check_dependencies()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.name='Coffee_Order_to_Ceramic_Pickup_Static_Preset';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
asset=bpy.data.collections.new('ASSET__Coffee_Order_Pickup');s.collection.children.link(asset)
diag=bpy.data.collections.new('DIAGNOSTIC__Not_Exported');s.collection.children.link(diag)
def move(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
def empty(name,parent=None,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);asset.objects.link(o);o.empty_display_type='PLAIN_AXES';o.empty_display_size=.12;o.parent=parent;o.location=loc;return o
root=empty('PRESET__'+ASSET);root['preset_id']=ASSET;root['asset_kind']='scene';root['version']='1.0.0';root['dependency_snapshot_commit']=LOCK['commit'];root['origin']='Ground datum Z=0; layout +Y is staff side';root['static_scope']='Order/pickup region metadata only; no payment, brewing, navmesh, dynamics, food-safety or real-world passage certification';root['layout_envelope_xy_m']=[-1.95,1.95,-1.65,2.15];root['metadata_coordinate_space']='Preset-local meters; Blender X/Y horizontal, +Z up';root['metadata_to_gltf_mapping']='(x,y,z) -> (x,z,-y); glTF X/Z horizontal, +Y up';root['layout_envelope_gltf_xz_m']=[-1.95,1.95,-2.15,1.65]
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
sources={};source_rows=[];source_hash={}
for f in LOCK['files']:
 if not f['path'].endswith('/model.glb'):continue
 path=SNAPSHOT/f['path'];aid=path.parent.parent.name;before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path),merge_vertices=False);added=[o for o in bpy.data.objects if o not in before];obs=[o for o in added if o.type=='MESH'];assert obs;bpy.context.view_layer.update()
 for o in obs:
  world=o.matrix_world.copy();o.parent=None;o.matrix_world=world;move(o,asset)
 for o in added:
  if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.view_layer.update();sources[aid]=obs;meta=json.loads((path.parent/'metadata.json').read_text());b=bounds(obs);assert max(abs(b['dimensions'][i]-meta['bounds'][k]) for i,k in enumerate('xyz'))<1e-4
 source_hash[aid]=fingerprint(obs);source_rows.append({'id':aid,'version':'1.0.0','style':meta['style'],'catalog_origin':LOCK['catalog_source_mapping'][aid],'source_glb_sha256':f['sha256'],'actual_bounds_m':b,'mesh_nodes':len(obs),'triangles':len(triangles(obs)),'geometry_pbr_sha256_10um':source_hash[aid]})
instances={};groups={};placements=[]
def place(aid,label,xyz,deg=0,parent=root):
 g=empty('INSTANCE__'+label,parent,xyz);g.rotation_euler.z=math.radians(deg);mapping=LOCK['catalog_source_mapping'][aid]
 tags={'source_asset_id':aid,'source_version':'1.0.0','source_commit':mapping['catalog_source_commit'],'catalog_source_id':mapping['catalog_source_id'],'dependency_snapshot_commit':LOCK['commit'],'instance_label':label,'complete_source_instance':True,'reused_not_new_asset':True}
 for k,v in tags.items():g[k]=v
 obs=[]
 for orig in sources[aid]:
  o=orig.copy();o.data=orig.data;asset.objects.link(o);o.name=label+'__'+orig.name;o.parent=g;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=orig.matrix_world.copy()
  for k,v in tags.items():o[k]=v
  o['source_mesh_name']=orig.name;obs.append(o)
 bpy.context.view_layer.update();instances[label]=obs;groups[label]=g;sig=fingerprint(obs,local=True);assert sig==source_hash[aid],('Changed source geometry/PBR',label)
 placements.append({'label':label,'group_node':g.name,'source_asset_id':aid,'source_version':'1.0.0',**mapping,'dependency_snapshot_commit':LOCK['commit'],'translation_m':list(xyz),'rotation_degrees':[0,0,deg],'scale':[1,1,1],'source_mesh_count':len(obs),'complete_source_instance':True,'source_geometry_pbr_signature_equal':True,'actual_bounds_m':bounds(obs)})
 return obs
place('dining-service-counter-01','order_counter',(-.67,0,0),180)
place('dining-service-counter-01','pickup_counter',(.67,0,0),180)
place('interior-open-worktable-01','staff_worktable',LAYOUT['table_origin_m'])
top=bounds(instances['staff_worktable'])['max'][2];counter_top=bounds(instances['pickup_counter'])['max'][2]
place('cafe-countertop-espresso-machine-01','complete_static_espresso_machine',(*LAYOUT['machine_origin_xy_m'],top))
place('kitchen-mug-01','single_ceramic_pickup_mug',(*LAYOUT['pickup_mug_origin_xy_m'],counter_top))
for obs in sources.values():
 for o in obs:bpy.data.objects.remove(o,do_unlink=True)
all_asset=[o for obs in instances.values() for o in obs]

# Real polygon clipping and support-area tests; AABBs below are broad-phase only.
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
 p=[Vector((v.x,v.y)) for v in subject];q=[Vector((v.x,v.y)) for v in host];sign=1 if sum(a.x*b.y-b.x*a.y for a,b in zip(q,q[1:]+q[:1]))>=0 else -1
 for a,b in zip(q,q[1:]+q[:1]):
  out=[]
  for u,v in zip(p,p[1:]+p[:1]):
   du=sign*((b.x-a.x)*(u.y-a.y)-(b.y-a.y)*(u.x-a.x));dv=sign*((b.x-a.x)*(v.y-a.y)-(b.y-a.y)*(v.x-a.x));iu=du>=-1e-10;iv=dv>=-1e-10
   if iu:out.append(u)
   if iu!=iv:out.append(u+(v-u)*(du/(du-dv)))
  p=out
  if not p:break
 return area2(p)
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
 return {'plane_z_m':z,'tested_downward_plane_z_m':z if contact_z is None else contact_z,'actual_contact_triangles':len(faces),'actual_area_m2':round(total,11),'covered_area_m2':round(covered,11),'uncovered_area_m2':round(max(0,total-covered),11),'all_area_supported':total>1e-9 and total-covered<1e-8,'method':'Continuous area intersection of actual downward triangles and actual upward support triangles, within 2um coplanarity tolerance.','patches':rows}
routes=[{'id':'customer_order_to_pickup_trunk','role':'customer passage, west entry to east exit','box':LAYOUT['customer_reserved_box_m'],'target_width_m':1.30,'network':'customer'},{'id':'staff_prep_lane','role':'independent staff lane between front shelf openings and rear machine front','box':LAYOUT['staff_reserved_box_m'],'target_width_m':1.10,'network':'staff'},{'id':'order_approach','role':'west counter customer interaction region','box':[-1.20,-.14,-.85,-.285,.001,2.20],'target_width_m':1.06,'network':'customer'},{'id':'ceramic_pickup_approach','role':'east counter customer interaction region','box':[.14,1.20,-.85,-.285,.001,2.20],'target_width_m':1.06,'network':'customer'},{'id':'machine_front_staff_stand','role':'static machine front interaction region within staff lane','box':[-.48,.48,.75,1.40,.001,2.20],'target_width_m':.96,'network':'staff'}]
ports=[]
def region(name,box,role,network,connects):
 lo=[box[0],box[2],box[4]];hi=[box[1],box[3],box[5]];dims=[hi[i]-lo[i] for i in range(3)];assert min(dims)>0
 o=empty('REGION__'+name,root,tuple((lo[i]+hi[i])/2 for i in range(3)));o['region_id']=name;o['role']=role;o['network']=network;o['box_xyz_minmax_m']=box;o['dimensions_xyz_m']=dims;o['gltf_box_xyz_minmax_m']=[box[0],box[1],box[4],box[5],-box[3],-box[2]];o['gltf_dimensions_xyz_m']=[dims[0],dims[2],dims[1]];o['metadata_to_gltf_mapping']='(x,y,z) -> (x,z,-y)';o['connects_to']=json.dumps(connects);o['space']='preset-local meters, Z up';o['static_only']=True
 ports.append({'id':name,'node':o.name,'box_m':box,'center_m':list(o.location),'dimensions_xyz_m':dims,'metadata_space':'Blender preset-local XYZ, Z up, meters','gltf_box_xyz_minmax_m':[box[0],box[1],box[4],box[5],-box[3],-box[2]],'gltf_dimensions_xyz_m':[dims[0],dims[2],dims[1]],'metadata_to_gltf_mapping':'(x,y,z) -> (x,z,-y)','role':role,'network':network,'connects_to':connects})
for r in routes:region(r['id'],r['box'],r['role'],r['network'],['customer_order_to_pickup_trunk'] if r['id'] in ['order_approach','ceramic_pickup_approach'] else ['staff_prep_lane'] if r['id']=='machine_front_staff_stand' else [])
for name,box,network,link in [('customer_west_entry',[-1.95,-1.65,-1.6,-.3,.001,2.2],'customer','customer_order_to_pickup_trunk'),('customer_east_exit',[1.65,1.95,-1.6,-.3,.001,2.2],'customer','customer_order_to_pickup_trunk'),('staff_west_access',[-1.95,-1.65,.3,1.4,.001,2.2],'staff','staff_prep_lane'),('staff_east_access',[1.65,1.95,.3,1.4,.001,2.2],'staff','staff_prep_lane')]:
 region(name,box,'Finite-width side connection to surrounding game level',network,[link]);routes.append({'id':name,'role':'Finite-width side connection','box':box,'target_width_m':box[3]-box[2],'network':network})
root['intended_customer_sequence']=json.dumps(['customer_west_entry','order_approach','ceramic_pickup_approach','customer_east_exit']);root['ceramic_vessel_semantics']='Existing hollow ceramic mug, not a takeaway container';root['route_region_nodes_exported']=True

def route_test(r,obs):
 hits=[];b=r['box']
 for o,t,_ in triangles(obs):
  poly=list(t)
  for axis,(lo,hi) in enumerate(((b[0],b[1]),(b[2],b[3]),(b[4],b[5]))):poly=clip(clip(poly,axis,lo,True),axis,hi,False)
  if area3(poly)>1e-9:hits.append({'mesh':o.name,'area_in_region_m2':round(area3(poly),10)})
 return {**r,'clear':not hits,'actual_triangle_intrusions':len(hits),'intrusions':hits[:12]}
def tree(obs):
 ts=triangles(obs);v=[p for _,t,_ in ts for p in t];return BVHTree.FromPolygons(v,[(i,i+1,i+2) for i in range(0,len(v),3)],all_triangles=True,epsilon=0),ts

def inside(bt,p):
 votes=[]
 for v in [( .811,.337,.479),(.257,.887,.383),(.419,.293,.861)]:
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
 if separating:return {'broad_phase_separated':False,'bvh_surface_pairs':len(pairs),'coplanar_pairs':coplanar,'candidate_plane_straddles_at_tangent_contact':len(crossings),'proper_crossings':0,'strict_containment_witnesses':0,'actual_vertex_separating_planes':separating,'scope':'Every actual vertex lies on the appropriate side of a separating plane within 2um, excluding positive-volume overlap beyond this tolerance. Actual opposed face contact and contact areas are tested separately; infinite-plane straddles at a tangent are not counted as proper crossings.'}
 witnesses=[]
 for obs,dest,bd in [(a,tb,bb),(b,ta,ba)]:
  for o,t,_ in triangles(obs):
   n=(t[1]-t[0]).cross(t[2]-t[0]).normalized();q=sum(t,Vector())/3-n*.00005
   if all(bd['min'][k]+2e-6<q[k]<bd['max'][k]-2e-6 for k in range(3)):
    hit,normal,idx,dist=dest.find_nearest(q)
    if dist is not None and dist>2e-6 and inside(dest,q):witnesses.append({'mesh':o.name,'point_m':list(q),'clearance_m':dist});break
  if witnesses:break
 return {'broad_phase_separated':False,'bvh_surface_pairs':len(pairs),'coplanar_pairs':coplanar,'proper_crossings':len(crossings),'strict_containment_witnesses':len(witnesses),'witnesses':witnesses,'scope':'Actual triangle intersections plus inward triangle-centroid solid probes; separation planes additionally prove intended support pairs have zero positive-volume overlap.'}

def geometry_report(data):
 rows=[]
 for label,obs in data.items():
  host='staff_worktable' if label=='complete_static_espresso_machine' else 'pickup_counter' if label=='single_ceramic_pickup_mug' else None;z=top if host=='staff_worktable' else counter_top if host else 0
  rows.append({'instance':label,'host':host or 'External game-ground datum Z=0','support':support(obs,z,data[host] if host else None)})
 tests=[route_test(r,[o for obs in data.values() for o in obs]) for r in routes]
 # A wholly enclosed route box has no boundary crossing; reject its center inside a source solid too.
 for r in tests:
  b=r['box'];q=Vector(((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2));witness=[]
  for label,obs in data.items():
   bb=bounds(obs)
   if all(bb['min'][k]+2e-6<q[k]<bb['max'][k]-2e-6 for k in range(3)) and inside(tree(obs)[0],q):witness.append(label)
  r['solid_containment_witnesses']=witness;r['clear']=r['clear'] and not witness
 pairs=[]
 for i,a in enumerate(data):
  for b in list(data)[i+1:]:pairs.append({'instances':[a,b],**collisions(data[a],data[b])})
 return {'supports':rows,'route_tests':tests,'cross_instance_collision_tests':pairs,'all_contacts_supported':all(x['support']['all_area_supported'] for x in rows),'all_route_prisms_clear':all(x['clear'] for x in tests),'no_cross_instance_positive_penetration_detected':all(x['proper_crossings']==0 and x['strict_containment_witnesses']==0 for x in pairs)}
geometry=geometry_report(instances)
# Foot contact is distinct from chassis projection: chassis bottom is raised 25mm.
chassis=[o for o in instances['complete_static_espresso_machine'] if 'Continuous lower chassis' in o['source_mesh_name']];assert len(chassis)==1
chassis_low=bounds(chassis)['min'][2];chassis_projection=support(chassis,top,instances['staff_worktable'],contact_z=chassis_low)
feet=[o for o in instances['complete_static_espresso_machine'] if 'Machine ground foot' in o['source_mesh_name']];assert len(feet)==4
foot_rows=[{'mesh':o.name,'support':support([o],top,instances['staff_worktable'])} for o in feet]
# Front/rear complete chassis and foot-pad margins against real top-face envelope.
tops=flat_faces(instances['staff_worktable'],top,True);tv=[v for _,t in tops for v in t];cb=bounds(chassis);footb=bounds(feet)
margins={'chassis_front_m':cb['min'][1]-min(v.y for v in tv),'chassis_rear_m':max(v.y for v in tv)-cb['max'][1],'foot_front_m':footb['min'][1]-min(v.y for v in tv),'foot_rear_m':max(v.y for v in tv)-footb['max'][1],'chassis_bottom_height_above_top_m':chassis_low-top,'note':'Top-face actual flat envelope margins; continuous real triangle projected coverage also tested. Chassis underside is not contact.'}
# Intended support pairs are separated by a measured Z plane; the adjacent counter pair by X=0.
planes=[{'instances':['staff_worktable','complete_static_espresso_machine'],'axis':'Z','lower_max':bounds(instances['staff_worktable'])['max'][2],'upper_min':bounds(instances['complete_static_espresso_machine'])['min'][2]},{'instances':['pickup_counter','single_ceramic_pickup_mug'],'axis':'Z','lower_max':bounds(instances['pickup_counter'])['max'][2],'upper_min':bounds(instances['single_ceramic_pickup_mug'])['min'][2]},{'instances':['order_counter','pickup_counter'],'axis':'X','lower_max':bounds(instances['order_counter'])['max'][0],'upper_min':bounds(instances['pickup_counter'])['min'][0]}]
for v in planes:v['nonpenetration_within_2um']=v['lower_max']<=v['upper_min']+2e-6
# Opposed real faces at the modular seam; top bevel groove remains authored.
seam=[]
for label,axis_sign in [('order_counter',1),('pickup_counter',-1)]:
 ts=[]
 for o,t,_ in triangles(instances[label]):
  n=(t[1]-t[0]).cross(t[2]-t[0])
  if n.length>1e-12 and max(abs(v.x) for v in t)<2e-6 and n.normalized().x*axis_sign>.999:ts.append((o,t))
 seam.append(ts)
seam_area=0
for _,a in seam[0]:
 for _,b in seam[1]:seam_area+=intersect_xy([Vector((v.y,v.z,0)) for v in a],[Vector((v.y,v.z,0)) for v in b])
seam_report={'actual_opposed_contact_area_m2':seam_area,'contact_at_x_m':0,'no_counter_positive_volume_overlap':planes[-1]['nonpenetration_within_2um'],'source_top_bevel_retained':True,'actual_top_flat_inner_edges_x_m':[max(v.x for _,t in flat_faces(instances['order_counter'],counter_top,True) for v in t),min(v.x for _,t in flat_faces(instances['pickup_counter'],counter_top,True) for v in t)],'scope':'Complete neighboring modules meet on opposed side patches. Their original bevels leave a visible top groove; no seamless combined top or cross-seam cup support is claimed.'}
def shifted(label,delta,fn):
 g=groups[label];old=g.location.copy();g.location+=Vector(delta);bpy.context.view_layer.update()
 try:return fn()
 finally:g.location=old;bpy.context.view_layer.update()
negative=[{'fixture':'machine lifted 15mm','rejected':not shifted('complete_static_espresso_machine',(0,0,.015),lambda:support(instances['complete_static_espresso_machine'],top,instances['staff_worktable']))['all_area_supported']},{'fixture':'machine shifted X +550mm off table','support':shifted('complete_static_espresso_machine',(.55,0,0),lambda:support(instances['complete_static_espresso_machine'],top,instances['staff_worktable']))},{'fixture':'ceramic mug lifted 12mm','rejected':not shifted('single_ceramic_pickup_mug',(0,0,.012),lambda:support(instances['single_ceramic_pickup_mug'],counter_top,instances['pickup_counter']))['all_area_supported']},{'fixture':'pickup counter moved 20mm into neighboring counter','collision':shifted('pickup_counter',(-.02,0,0),lambda:collisions(instances['order_counter'],instances['pickup_counter']))},{'fixture':'order counter shifted into staff lane','route':shifted('order_counter',(0,.55,0),lambda:route_test(routes[1],all_asset))}]
negative[1]['rejected']=not negative[1]['support']['all_area_supported'];negative[3]['rejected']=negative[3]['collision']['proper_crossings']>0 or negative[3]['collision']['strict_containment_witnesses']>0;negative[4]['rejected']=not negative[4]['route']['clear']
# Finite 0.60m static standing squares must lie fully inside the measured same-network region union.
def footprint_coverage(xy,network):
 rect=[xy[0]-.30,xy[0]+.30,xy[1]-.30,xy[1]+.30];rr=[r['box'] for r in routes if r['network']==network];xs=sorted(set([rect[0],rect[1]]+[max(rect[0],min(rect[1],r[i])) for r in rr for i in [0,1]]));ys=sorted(set([rect[2],rect[3]]+[max(rect[2],min(rect[3],r[i])) for r in rr for i in [2,3]]));covered=0
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   x=(a+b)/2;y=(c+d)/2
   if any(r[0]-1e-9<=x<=r[1]+1e-9 and r[2]-1e-9<=y<=r[3]+1e-9 for r in rr):covered+=(b-a)*(d-c)
 return {'metadata_space':'Blender preset-local XY horizontal, Z up, meters','metadata_to_gltf_mapping':'(x,y,z) -> (x,z,-y)','gltf_standing_center_xyz_m':[xy[0],0,-xy[1]],'gltf_footprint_xz_minmax_m':[rect[0],rect[1],-rect[3],-rect[2]],'standing_center_xy_m':xy,'network':network,'square_width_depth_m':[.60,.60],'footprint_xy_minmax_m':rect,'covered_area_m2':round(covered,9),'uncovered_area_m2':round(max(0,.36-covered),9),'whole_footprint_in_verified_region_union':.36-covered<1e-9,'scope':'Single static axis-aligned footprint, no dynamic avoidance or real-world clearance certification.'}
standing=[{'id':name,**footprint_coverage(xy,network)} for name,xy,network in [('order_stand',[-.67,-.60],'customer'),('ceramic_pickup_stand',[.67,-.60],'customer'),('machine_front_stand',[0,1.05],'staff'),('customer_west_boundary_stand',[-1.65,-.95],'customer'),('customer_east_boundary_stand',[1.65,-.95],'customer'),('staff_west_boundary_stand',[-1.65,.85],'staff'),('staff_east_boundary_stand',[1.65,.85],'staff')]]
for stand in standing:
 node=empty('STAND__'+stand['id'],root,(*stand['standing_center_xy_m'],0));node['metadata_space']='Blender preset-local XY horizontal, Z up, meters';node['metadata_to_gltf_mapping']='(x,y,z) -> (x,z,-y)';node['gltf_standing_center_xyz_m']=[stand['standing_center_xy_m'][0],0,-stand['standing_center_xy_m'][1]];node['gltf_footprint_xz_minmax_m']=[stand['footprint_xy_minmax_m'][0],stand['footprint_xy_minmax_m'][1],-stand['footprint_xy_minmax_m'][3],-stand['footprint_xy_minmax_m'][2]];node['stand_id']=stand['id'];node['network']=stand['network'];node['square_footprint_width_depth_m']=[.60,.60];node['body_height_target_m']=2.20;node['whole_footprint_in_verified_region_union']=stand['whole_footprint_in_verified_region_union'];node['static_only']=True
negative.append({'fixture':'0.60m order standing square placed too close to counter at Y=-.35m','footprint':footprint_coverage([-.67,-.35],'customer'),'rejected':not footprint_coverage([-.67,-.35],'customer')['whole_footprint_in_verified_region_union']})
# Route-region connectivity is numeric geometry metadata rather than render labels.
def overlap_xy(a,b):return min(a[1],b[1])-max(a[0],b[0])>1e-6 and min(a[3],b[3])-max(a[2],b[2])>1e-6
edges=[[a['id'],b['id']] for i,a in enumerate(routes) for b in routes[i+1:] if overlap_xy(a['box'],b['box'])]
separate=not any(overlap_xy(a['box'],b['box']) for a in routes for b in routes if a['network']=='customer' and b['network']=='staff')
orientation={'counter_open_shelves_world_direction':[0,1,0],'customer_counter_solid_backs_world_direction':[0,-1,0],'machine_front_world_direction':[0,-1,0],'counter_top_to_table_front_clear_gap_m':bounds(instances['staff_worktable'])['min'][1]-max(bounds(instances[k])['max'][1] for k in ['order_counter','pickup_counter']),'staff_region_target_width_m':1.10,'staff_region_target_height_m':2.20,'customer_region_target_width_m':1.30,'note':'Actual lane gap and empty prisms are static game-layout targets, not real-world safety or code certification.'}
# Save the clean source and export the actual complete hierarchy before adding a rig.
bpy.ops.object.select_all(action='DESELECT')
for o in asset.objects:o.select_set(True)
bpy.context.view_layer.objects.active=root;s['candidate_stage']='original-PBR-approved static preset; final independent QA pending' if args.render_final else 'gray-interface, independent review pending';s['diagnostics_exported']=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_extras=True)
raw=(OUT/'model.glb').read_bytes();jl=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+jl]);gn=gltf['nodes'];export_region=[n for n in gn if n.get('extras',{}).get('region_id')];assert len(export_region)==len(ports)
for n in export_region:assert len(n['extras']['dimensions_xyz_m'])==3 and min(n['extras']['dimensions_xyz_m'])>0
before_sig=fingerprint(all_asset);before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);added=[o for o in bpy.data.objects if o not in before];reobs=[o for o in added if o.type=='MESH'];bpy.context.view_layer.update();after_sig=fingerprint(reobs)
actual={label:[o for o in reobs if o.get('instance_label')==label] for label in instances};assert all(actual.values());actual_geometry=geometry_report(actual)
roundtrip={'actual_glb_imported':True,'world_oriented_triangle_and_pbr_equal_at_10um':before_sig==after_sig,'before_sha256':before_sig,'after_sha256':after_sig,'mesh_nodes_before':len(all_asset),'mesh_nodes_after':len(reobs),'triangles_before':len(triangles(all_asset)),'triangles_after':len(triangles(reobs)),'exported_region_nodes':len(export_region),'region_dimensions_and_connections_preserved':True,'no_diagnostic_nodes_exported':not any(n.get('name','').startswith('DIAGNOSTIC') for n in gn),'unique_meshes':len(gltf.get('meshes',[])),'materials':len(gltf.get('materials',[])),'textures':len(gltf.get('textures',[])),'actual_reimport_geometry_tests':actual_geometry}
for o in added:bpy.data.objects.remove(o,do_unlink=True)
check_dependencies()
gate={'all_real_contacts_supported':geometry['all_contacts_supported'],'all_actual_import_contacts_supported':actual_geometry['all_contacts_supported'],'all_four_machine_foot_contacts_supported':all(x['support']['all_area_supported'] for x in foot_rows),'complete_chassis_projection_supported_without_calling_it_contact':chassis_projection['all_area_supported'],'all_static_600mm_standing_footprints_in_measured_region_union':all(v['whole_footprint_in_verified_region_union'] for v in standing),'all_route_regions_clear':geometry['all_route_prisms_clear'] and actual_geometry['all_route_prisms_clear'],'customer_staff_regions_separate':separate,'no_cross_instance_penetration_detected':geometry['no_cross_instance_positive_penetration_detected'] and actual_geometry['no_cross_instance_positive_penetration_detected'],'actual_separation_planes_nonpenetrating':all(v['nonpenetration_within_2um'] for v in planes),'counter_seam_opposed_faces_contact':seam_area>1e-6,'negative_fixtures_all_rejected':all(v['rejected'] for v in negative),'complete_original_triangle_pbr_glb_roundtrip':before_sig==after_sig,'independent_gray_review':'PENDING','original_pbr_style_review':'NOT_STARTED','browser_runtime':'NOT_STARTED','formal_approved':False}
limits=['Only a static game scene with suggested numeric interaction regions; no payment, coffee preparation, water, heat, pressure, electrical or food-safety capability.','Existing hollow ceramic mug is not a takeaway cup.','No dynamic agents, navmesh, accessibility, building-code, workplace-safety or commercial-operation certification.','Counter module original beveled seam is retained. It is not a seamless shared countertop.','External flat game ground at Z=0 required. Studio floor, labels and route fills are not part of the GLB.','Original S01 machine/table and soft-low-poly counter/mug PBR remain unchanged; style coordination pending.']
report={'id':ASSET,'coordinate_contract':{'metadata':'Preset-local meters; Blender XY horizontal, Z up','to_gltf':'(x,y,z) -> (x,z,-y)','gltf':'Preset-local meters; XZ horizontal, Y up; node transforms converted normally by glTF exporter'},'stage':'gray-interface','formal_approved':False,'art_passed':False,'dependency_snapshot_commit':LOCK['commit'],'catalog_source_mapping':LOCK['catalog_source_mapping'],'dependency_bytes_before_after_equal':True,'source_measurements':source_rows,'placements':placements,'instance_count':len(instances),'reused_source_ids':4,'new_standalone_props':0,'geometry_bounds_m':bounds(all_asset),'triangles':len(triangles(all_asset)),'geometry_tests':geometry,'machine_foot_contacts':foot_rows,'chassis_projection_only':chassis_projection,'machine_table_actual_margins':margins,'support_separation_planes':planes,'double_counter_seam':seam_report,'orientation_and_clearance':orientation,'standing_footprints':standing,'negative_controls':negative,'route_graph':{'edges':edges,'customer_staff_disjoint':separate,'method':'Positive-area XY overlap of finite width/depth regions; region height tested against actual triangles. Side connections are distinct customer/staff boundary regions. Static metadata, no pathfinding simulation.'},'roundtrip':roundtrip,'limits':limits,'gate':gate}
(QA/'geometry-report.json').write_text(json.dumps(report,indent=2)+'\n');(QA/'roundtrip-report.json').write_text(json.dumps(roundtrip,indent=2)+'\n')
composition={'id':ASSET,'assetKind':'scene','description':'Two complete front service-counter modules with separate order and ceramic-mug pickup regions; rear complete worktable carries original static machine facing the independent staff lane.','dependency_lock_embedded_in_generator':True,'layout_parameters':LAYOUT,'instances':placements,'regions':ports,'standing_footprints':standing,'route_graph':report['route_graph'],'reuse_counting':{'new_scene_presets':1,'new_standalone_props':0,'reused_asset_ids':4,'complete_rigid_instances':5},'limits':limits}
(OUT/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
# Review metadata never claims verified at this milestone; optional thumbnail is only listed after it exists.
files={}
for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 if (OUT/name).is_file():
  b=(OUT/name).read_bytes();files[role]={'path':f'assets/cafe/{ASSET}/v1.0.0/{name}','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
metadata={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'cafe','style':'source-preserved-S01-and-soft-low-poly','title':'Coffee Order to Ceramic Pickup Layout','description':composition['description']+' Existing ceramic mug, not a takeaway container. Original materials and beveled modular seam retained. Static game-layout regions only; no brewing, payment, navigation or safety claim.','bounds':dict(zip('xyz',report['geometry_bounds_m']['dimensions']),unit='m'),'triangles':report['triangles'],'materials':len(gltf.get('materials',[])),'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print('GRAY_GEOMETRY_RESULT',json.dumps(gate),flush=True)
assert all(v for k,v in gate.items() if isinstance(v,bool) and k!='formal_approved'),gate
if args.render_gray or args.render_pbr:
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.world=bpy.data.worlds.new('Diagnostic studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.5,.5,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 def mat(name,c):
  m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=.85;return m
 clay=mat('DIAGNOSTIC clay',(.48,.49,.50));floor=mat('DIAGNOSTIC floor',(.25,.27,.28));route=mat('DIAGNOSTIC route',(.43,.45,.46));ink=mat('DIAGNOSTIC labels',(.035,.04,.045))
 def plane(name,box,z,m):
  bpy.ops.mesh.primitive_plane_add(size=1,location=((box[0]+box[1])/2,(box[2]+box[3])/2,z));o=bpy.context.object;o.name='DIAGNOSTIC '+name;o.scale=((box[1]-box[0]),(box[3]-box[2]),1);o.data.materials.append(m);move(o,diag)
 plane('external game ground',[-2.3,2.3,-1.95,2.35],-.004,floor)
 for r in routes:
  if r['id'] in ['customer_order_to_pickup_trunk','staff_prep_lane']:plane(r['id'],r['box'],-.002,route)
 def label(body,xyz,size=.13):
  c=bpy.data.curves.new('DIAGNOSTIC label','FONT');c.body=body;c.align_x='CENTER';c.align_y='CENTER';c.size=size;o=bpy.data.objects.new('DIAGNOSTIC '+body,c);diag.objects.link(o);o.location=xyz;c.materials.append(ink)
 label('CUSTOMER   ENTRY  >  ORDER  >  PICKUP  >  EXIT',(0,-1.32,.002),.12);label('STAFF LANE   1.10 m RESERVED',(0,.73,.002),.13)
 label('ORDER',(-.67,-.04,counter_top+.002),.14);label('CERAMIC PICKUP',(.67,.13,counter_top+.002),.105)
 def aim(o,xyz,target):o.location=xyz;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,xyz,power,size in [('Key',(-4,-5,8),1400,5),('Fill',(5,-1,5),700,4),('Rim',(0,5,7),1000,4)]:
  bpy.ops.object.light_add(type='AREA',location=xyz);o=bpy.context.object;o.name='DIAGNOSTIC '+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;move(o,diag);aim(o,xyz,(0,.5,.6))
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='DIAGNOSTIC camera';move(cam,diag);cam.data.type='ORTHO';s.camera=cam
 def render(name,xyz,target,scale):
  cam.data.ortho_scale=scale;aim(cam,xyz,target);s.render.filepath=str(QA/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDER_READY',str(QA/(name+'.png')),flush=True)
 if args.render_gray:
  original=[]
  for o in all_asset:
   o.data=o.data.copy();original.append((o,list(o.data.materials)))
   for i in range(len(o.data.materials)):o.data.materials[i]=clay
  render('gray-isometric',(6,-8,7),(0,.35,.55),6.2);render('gray-top',(0,.20,10),(0,.20,0),5.4)
  for o,ms in original:
   for i,m in enumerate(ms):o.data.materials[i]=m
 if args.render_pbr:render('original-pbr-coordination',(6,-8,7),(0,.35,.55),6.2)
 bpy.ops.wm.save_as_mainfile(filepath=str(QA/'diagnostic.blend'))


if args.render_final:
 # Render a fresh import of the actual exported GLB. The clean source was saved
 # before adding this studio. No diagnostic letters, region fills or source edits.
 from bpy_extras.object_utils import world_to_camera_view
 formal=bpy.data.scenes.new('Formal_Actual_GLB_Original_PBR_Studio');bpy.context.window.scene=formal
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);render_parts=[o for o in formal.objects if o.type=='MESH'];assert render_parts
 assert fingerprint(render_parts)==before_sig,'Final fresh GLB triangle/PBR mismatch'
 formal.render.engine='CYCLES';formal.cycles.device='CPU';formal.cycles.samples=128;formal.cycles.use_denoising=False;formal.render.threads_mode='FIXED';formal.render.threads=args.render_threads;formal.render.resolution_x=896;formal.render.resolution_y=896;formal.render.resolution_percentage=100;formal.render.image_settings.file_format='PNG';formal.view_settings.view_transform='AgX';formal.view_settings.exposure=0;formal.view_settings.gamma=1
 formal.world=bpy.data.worlds.new('Formal neutral studio world');formal.world.use_nodes=True;formal.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.5,.5,1);formal.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.004));floor=bpy.context.object;floor.name='RENDER ONLY neutral ground';fm=bpy.data.materials.new('Formal neutral studio ground');fm.use_nodes=True;fn=fm.node_tree.nodes['Principled BSDF'];fn.inputs['Base Color'].default_value=(.25,.27,.28,1);fn.inputs['Roughness'].default_value=.85;floor.data.materials.append(fm)
 def formal_aim(o,xyz,target):o.location=xyz;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,xyz,power,size in [('Key',(-4,-5,8),1400,5),('Fill',(5,-1,5),700,4),('Rim',(0,5,7),1000,4)]:
  bpy.ops.object.light_add(type='AREA',location=xyz);o=bpy.context.object;o.name='RENDER ONLY '+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;formal_aim(o,xyz,(0,.5,.6))
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='RENDER ONLY formal orthographic camera';cam.data.type='ORTHO';formal.camera=cam
 center=Vector((0,.89,.6615));dirs={'isometric':Vector((6,-8,7)),'front':Vector((0,-10,0)),'back':Vector((0,10,0)),'left':Vector((-10,0,0)),'right':Vector((10,0,0)),'top':Vector((0,0,10))};views=args.formal_views.split(',');assert len(views)==len(set(views)) and all(v in dirs for v in views)
 manifest={'asset':ASSET,'stage':'formal original-PBR six directions; independent final QA pending','source_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'actual_glb_geometry_pbr_sha256_10um':fingerprint(render_parts),'samples_by_view':{'isometric':128,'front':128,'back':512,'left':128,'right':128,'top':128},'cpu_threads':args.render_threads,'denoising':False,'resolution':[896,896],'fixed_studio':{'world_strength':.5,'exposure':0,'gamma':1,'key_fill_rim_watts':[1400,700,1000]},'method':'Fresh actual GLB import; fixed original PBR and fixed studio; per-view actual projected-vertex fit. No diagnostic text or route fills. Front -Y, back +Y, left -X, right +X, top +Z in Blender Z-up coordinates.','views':{}}
 existing=QA/'formal-view-manifest.json'
 if existing.is_file():
  previous=json.loads(existing.read_text())
  if previous.get('source_glb_sha256')==manifest['source_glb_sha256']:manifest['views'].update(previous.get('views',{}))
 for name in views:
  formal.cycles.samples=512 if name=='back' else 128
  cam.location=center+dirs[name]
  if name=='top':cam.rotation_euler=(0,0,0)
  else:formal_aim(cam,cam.location,center)
  bpy.context.view_layer.update();pp=[cam.matrix_world.inverted()@(o.matrix_world@v.co) for o in render_parts for v in o.data.vertices];lo=[min(v[k] for v in pp) for k in [0,1]];hi=[max(v[k] for v in pp) for k in [0,1]];cam.location+=cam.matrix_world.to_3x3()@Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0));cam.data.ortho_scale=max(hi[0]-lo[0],hi[1]-lo[1])*1.20;bpy.context.view_layer.update();uv=[world_to_camera_view(formal,cam,o.matrix_world@v.co) for o in render_parts for v in o.data.vertices];fr={'min_u':min(v.x for v in uv),'max_u':max(v.x for v in uv),'min_v':min(v.y for v in uv),'max_v':max(v.y for v in uv)};assert all(.03<v.x<.97 and .03<v.y<.97 for v in uv),fr
  image=QA/('qa-'+name+'.png');formal.render.filepath=str(image);bpy.ops.render.render(write_still=True);manifest['views'][name]={'path':image.name,'samples':formal.cycles.samples,'bytes':image.stat().st_size,'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'camera_location_m':list(cam.location),'camera_rotation_radians':list(cam.rotation_euler),'orthographic_scale_m':cam.data.ortho_scale,'actual_projection_bbox':fr};existing.write_text(json.dumps(manifest,indent=2)+'\n')
  if name=='isometric':
   (OUT/'thumbnail.png').write_bytes(image.read_bytes())
   b=(OUT/'thumbnail.png').read_bytes();metadata['files']['render']={'path':f'assets/cafe/{ASSET}/v1.0.0/thumbnail.png','size':len(b),'sha256':hashlib.sha256(b).hexdigest()};(OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
  print('FORMAL_VIEW_READY',name,str(image),flush=True)
 assert fingerprint(render_parts)==before_sig,'Formal render changed actual GLB geometry/PBR'
 print('FORMAL_RENDER_SET_READY',sorted(manifest['views']),flush=True)
