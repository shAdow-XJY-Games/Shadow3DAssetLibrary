"""Reproducible two-bay fresh-market exterior-handoff game preset.

Normal repository, only this generator plus its locked original dependencies:
  blender -b -t 4 --python assets/retail/retail-fresh-market-scene-01/v1.0.0/generate.py -- --render-final --threads 4 --qa qa/retail-fresh-market-scene-01/v1.0.0
This creates the five core files (generate.py, metadata.json, model.glb,
source.blend, thumbnail.png) and six clean-background 128-sample QA views.
The isometric image is reused as thumbnail, with no seventh render.

For geometry/source rebuilding without rendering use --no-render instead of
--render-final. That mode does not reproduce PNG evidence or claim a complete
newly-rendered five-file delivery. Metadata is emitted only when the thumbnail is available, avoiding an invalid
partial schema document in a fresh --no-render geometry-only build. Optional --snapshot /path/to/root
selects an explicit immutable source tree; normal repositories are discovered
through ancestors containing all locked assets. No sidecar lock is needed.

All four dependency GLBs are complete scale-one rigid instances. The embedded
byte lock and sourceId-specific publication map are distinct provenance layers.
Original generators are verified but never executed. No source mesh or PBR is
modified. Routes/custom XY regions are preset-local Blender Z-up metres;
glTF point=(x,z,-y). Root placement applies afterwards. Explicit glTF-local
Y-up bounds are also provided in port/root extras. Diagnostic ground, lights,
cameras, route marks and text are never exported in source.blend or model.glb.

This is static exterior-handoff layout evidence. Nominal 1.95m stall interiors
have effectively zero headroom margin for a 1.95m body and remain excluded.
No navigation, accessibility, commercial or load certification. Metadata stays
review until the separate independent final and local-runtime gates pass.
"""
import argparse, hashlib, json, math, sys, time
from collections import Counter
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--snapshot',type=Path)
parser.add_argument('--qa',type=Path)
parser.add_argument('--render-gray',action='store_true')
parser.add_argument('--render-pbr',action='store_true')
parser.add_argument('--render-final',action='store_true')
parser.add_argument('--no-render',action='store_true')
parser.add_argument('--threads',type=int,default=2,choices=range(1,9))
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
QA=(args.qa or OUT/'qa').resolve();QA.mkdir(parents=True,exist_ok=True)
# Complete immutable byte lock and sourceId-specific publication map are embedded.
# No sibling sidecar is required by the five-file delivery.
LOCK=json.loads(r'''{"repository":"shAdow-XJY-Games/Shadow3DAssetLibrary","commit":"86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb","tree":"18e4c6a856ecbf56fc36ae8781a67f03ef9e0746","recovery_kind":"minimal published-source snapshot; no generator executed","files":[{"path":"assets/interior/interior-open-worktable-01/v1.0.0/generate.py","git_blob_sha1":"b39f3850fb4167f4536ec075871f992aef1a8c29","bytes":30478,"sha256":"b4880f9c24dda10b566fa215c394295b6522a8ad448486918c591826480c09d8","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/interior/interior-open-worktable-01/v1.0.0/generate.py","materialized_from":"same-blob local recovery copy"},{"path":"assets/interior/interior-open-worktable-01/v1.0.0/metadata.json","git_blob_sha1":"58b455a57f2836387feca1e2cf1640e1ad6c6ddd","bytes":1606,"sha256":"09788691add9172e1c82ef35ffa67c878dbceff10d34808e4d0f1998bcbea48a","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/interior/interior-open-worktable-01/v1.0.0/metadata.json","materialized_from":"same-blob local recovery copy"},{"path":"assets/interior/interior-open-worktable-01/v1.0.0/model.glb","git_blob_sha1":"a72289a98d82a03f8d699ba065c62161ad1c7e0e","bytes":46720,"sha256":"78ec9cdb829e12c333ade0356adee759b8f95bdc7f037fe93ce946b0a487265b","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/interior/interior-open-worktable-01/v1.0.0/model.glb","materialized_from":"same-blob local recovery copy"},{"path":"assets/retail/retail-fresh-produce-set-01/v1.0.0/generate.py","git_blob_sha1":"3c7a4075373a18b5dca21d74c0d45bec7bd2aedd","bytes":35481,"sha256":"ac262e701005a56f82305e8e4d9f34f64e6811e3ffdef269dd47a1214dba7578","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-fresh-produce-set-01/v1.0.0/generate.py","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/retail/retail-fresh-produce-set-01/v1.0.0/metadata.json","git_blob_sha1":"e081412cc44872ade7fdc4e4780af241cdc6ee08","bytes":1805,"sha256":"7fb35d70135fef38a5844ba9dfdde1b4d218dc4c6b5ab2d7262b78277e27f6e8","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-fresh-produce-set-01/v1.0.0/metadata.json","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/retail/retail-fresh-produce-set-01/v1.0.0/model.glb","git_blob_sha1":"a20a3dc7025c1a4c65d0e12973f8aefab46a6315","bytes":91948,"sha256":"be6cc5f519fff43c2d39e3b6781a86ee1b9a6d12ea9100c02a5af1e563b4f9ce","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-fresh-produce-set-01/v1.0.0/model.glb","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/retail/retail-stackable-produce-crate-01/v1.0.0/generate.py","git_blob_sha1":"076d4cf0f7a526efb34cb49c15bff49114f35ef2","bytes":32493,"sha256":"948043e43d96a8579d7baa3e2cde48cc18f7aab9e888e96bd4b1b5aaf39b725d","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-stackable-produce-crate-01/v1.0.0/generate.py","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/retail/retail-stackable-produce-crate-01/v1.0.0/metadata.json","git_blob_sha1":"ee9b3acee94606ea0e6877daa8a60197f88f3ee1","bytes":1816,"sha256":"dff917e9d3cc57631dce90011a0a1cfe163694e437b00720047342749eb8c69e","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-stackable-produce-crate-01/v1.0.0/metadata.json","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/retail/retail-stackable-produce-crate-01/v1.0.0/model.glb","git_blob_sha1":"a47aba0fb6b2344b81ae4b75b7468c2ef83562b8","bytes":27140,"sha256":"4a658aa164de5993ac38a46f3d4bf8f4f506f33c072b459904c572bfb7b3bf43","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/retail/retail-stackable-produce-crate-01/v1.0.0/model.glb","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/village/village-market-stall-01/v1.0.0/generate.py","git_blob_sha1":"ea02a17cdc11f3db1e4425caab37fc07497f2684","bytes":9061,"sha256":"26d03969db8ab1ebcafff5ca016b61de796d547f134ede78340ec6e6055ad89c","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/village/village-market-stall-01/v1.0.0/generate.py","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/village/village-market-stall-01/v1.0.0/metadata.json","git_blob_sha1":"e651fcd44f80310b0f1a25be77ed4623f0aa000d","bytes":1360,"sha256":"80f2516c8ae8022856b317031cd9f5203b7710a7f994bdb6e685e57249f80aeb","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/village/village-market-stall-01/v1.0.0/metadata.json","materialized_from":"GitHub fixed-commit fetch_file base64"},{"path":"assets/village/village-market-stall-01/v1.0.0/model.glb","git_blob_sha1":"f6642bca1db411d12cc28ce7303395c1d2d91e3d","bytes":237424,"sha256":"cc7c8f05aeafc36e1906a623c0c5d229b73bf6ceedf553f82cd191997ea881ed","source_url":"https://github.com/shAdow-XJY-Games/Shadow3DAssetLibrary/blob/86b8bf090aa8374fa5f0cacc6939e3d6a46c10cb/assets/village/village-market-stall-01/v1.0.0/model.glb","materialized_from":"GitHub fixed-commit fetch_file base64"}],"source_material_policy":"Original imported PBR shader values retained. No node filtering, mesh edits or scale edits.","catalog_source_mapping":{"interior-open-worktable-01":{"catalog_source_id":"access-core","catalog_source_commit":"e179cdc82c1f57e36dc0a78704146783f711484d","catalog_shard":"940f9c69e06194b8e52b441d41dde0500138d9b6c39e0350cffcd2165f3bba9e.json"},"retail-fresh-produce-set-01":{"catalog_source_id":"retail-produce-pair","catalog_source_commit":"c5cbcc552feaa6629711fa28299c58613bc9a3f5","catalog_shard":"7e758e3fc64be3fc8cff996e720acd21c35183e88737e8d16bc0ce1ae16fc91e.json"},"retail-stackable-produce-crate-01":{"catalog_source_id":"retail-produce-pair","catalog_source_commit":"c5cbcc552feaa6629711fa28299c58613bc9a3f5","catalog_shard":"7e758e3fc64be3fc8cff996e720acd21c35183e88737e8d16bc0ce1ae16fc91e.json"},"village-market-stall-01":{"catalog_source_id":"expanded-collection","catalog_source_commit":"a4f9ab53d3bb40010aa60c4f77669622055ec724","catalog_shard":"9bf9fa5eb2bbe0ddabf076e841a00bc6540b458a95d0cb4e946bedee1f5e456c.json"}},"provenance_note":"commit is the exact dependency byte snapshot, not the original publication reference. Original per-asset publication references resolve sourceId first in catalog_source_mapping."}''')
required=[f['path'] for f in LOCK['files']]
if args.snapshot:SNAPSHOT=args.snapshot.resolve()
else:
 SNAPSHOT=next((p for p in (OUT,*OUT.parents) if all((p/f).is_file() for f in required)),None)
 if SNAPSHOT is None:raise RuntimeError('Locked assets not found under repository ancestors. Supply --snapshot /path/to/published-source-root.')
for f in LOCK['files']:
 data=(SNAPSHOT/f['path']).read_bytes()
 assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],'Dependency byte lock mismatch: '+f['path']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==f['git_blob_sha1'],'Git blob mismatch: '+f['path']

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.name='Fresh_Market_Static_Game_Preset'
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
asset_col=bpy.data.collections.new('ASSET__Fresh_Market_Preset');scene.collection.children.link(asset_col)
diag_col=bpy.data.collections.new('DIAGNOSTIC__Never_Export');scene.collection.children.link(diag_col)
def move_collection(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 c.objects.link(o)
def empty(name,parent=None,location=(0,0,0)):
 o=bpy.data.objects.new(name,None);asset_col.objects.link(o);o.empty_display_type='PLAIN_AXES';o.empty_display_size=.18;o.location=location;o.parent=parent;return o
root=empty('PRESET__retail-fresh-market-scene-01');root['preset_id']='retail-fresh-market-scene-01';root['asset_kind']='scene';root['dependency_snapshot_commit']=LOCK['commit'];root['layout_envelope_m']='x[-3,3] y[-2.2,3.1]';root['layout_envelope_gltf_local_xz_m']='[-3,3,-3.1,2.2]';root['requires_external_flat_ground_z_m']=0;root['under_canopy_1_95m_workflow']='Not passed: nominal 1.95m beam gives effectively zero overhead margin. External handoff only.';root['layout_coordinate_frame']='Preset-local Blender Z-up metres; glTF point=(x,z,-y). Custom XY regions remain in this frame; root placement applies afterwards.';root['navigation_claim']='Static reserved volumes only; no navmesh, dynamics, commercial or accessibility certification.'
def vecs(objects):return [o.matrix_world@v.co for o in objects for v in o.data.vertices]
def bounds(objects):
 vv=vecs(objects);lo=[min(v[i] for v in vv) for i in range(3)];hi=[max(v[i] for v in vv) for i in range(3)]
 return {'min':[round(v,7) for v in lo],'max':[round(v,7) for v in hi],'dimensions':[round(hi[i]-lo[i],7) for i in range(3)]}
def triangles(objects):
 result=[]
 for o in objects:
  o.data.calc_loop_triangles();v=[o.matrix_world@p.co for p in o.data.vertices]
  result.extend((o,tuple(v[i] for i in t.vertices),t.material_index) for t in o.data.loop_triangles)
 return result
def pbr(m):
 n=m.node_tree.nodes.get('Principled BSDF');assert n
 names=['Base Color','Roughness','Metallic','Alpha','Emission Color','Emission Strength']
 def value(v):
  try:return [round(float(x),6) for x in v]
  except TypeError:return round(float(v),6)
 return {k:value(n.inputs[k].default_value) for k in names}|{'backface_culling':m.use_backface_culling}
def fingerprint(objects):
 rows=[]
 for o,t,mi in triangles(objects):
  pts=[tuple(round(float(x),5) for x in v) for v in t]
  oriented=min(tuple(pts[i:]+pts[:i]) for i in range(3))
  rows.append((oriented,json.dumps(pbr(o.data.materials[mi]),sort_keys=True)))
 return hashlib.sha256(json.dumps(sorted(rows),separators=(',',':')).encode()).hexdigest()
sources={};measurements=[]
for f in LOCK['files']:
 if not f['path'].endswith('/model.glb'):continue
 path=SNAPSHOT/f['path'];aid=path.parent.parent.name
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path),merge_vertices=False)
 added=[o for o in bpy.data.objects if o not in before];objects=[o for o in added if o.type=='MESH']
 assert objects,'No source meshes: '+aid
 bpy.context.view_layer.update()
 for o in objects:
  world=o.matrix_world.copy();o.parent=None;o.matrix_world=world;move_collection(o,asset_col)
 for o in added:
  if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
 bpy.context.view_layer.update();sources[aid]=objects
 b=bounds(objects);meta=json.loads((path.parent/'metadata.json').read_text())
 assert max(abs(b['dimensions'][i]-meta['bounds'][k]) for i,k in enumerate('xyz'))<.0001,('Source published bounds mismatch',aid,b)
 measurements.append({'id':aid,'source_style':meta['style'],'catalog_source_mapping':LOCK['catalog_source_mapping'][aid],'mesh_nodes':len(objects),'triangles':len(triangles(objects)),'actual_bounds_m':b,'geometry_and_pbr_signature':fingerprint(objects),'complete_source_preserved':True})

instances={};placements=[]
def instantiate(aid,label,xy,z,parent):
 group=empty('INSTANCE__'+label,parent);group['source_asset_id']=aid;group['source_version']='1.0.0';group['source_commit']=LOCK['catalog_source_mapping'][aid]['catalog_source_commit'];group['catalog_source_id']=LOCK['catalog_source_mapping'][aid]['catalog_source_id'];group['dependency_snapshot_commit']=LOCK['commit'];group['instance_label']=label;group['complete_source_instance']=True;group['reused_not_new_asset']=True
 objects=[]
 sb=bounds(sources[aid]);delta=Vector((xy[0]-(sb['min'][0]+sb['max'][0])/2,xy[1]-(sb['min'][1]+sb['max'][1])/2,z-sb['min'][2]))
 group.location=delta
 for index,s in enumerate(sources[aid]):
  o=s.copy();o.data=s.data;asset_col.objects.link(o);o.name=label+'__'+s.name;o.parent=group;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=s.matrix_world.copy()
  for key in ('source_asset_id','source_version','source_commit','catalog_source_id','dependency_snapshot_commit','instance_label','complete_source_instance','reused_not_new_asset'):o[key]=group[key]
  o['source_mesh_name']=s.name
  objects.append(o)
 bpy.context.view_layer.update();instances[label]=objects
 row={'label':label,'source_asset_id':aid,'source_version':'1.0.0','source_commit':LOCK['catalog_source_mapping'][aid]['catalog_source_commit'],'catalog_source_id':LOCK['catalog_source_mapping'][aid]['catalog_source_id'],'dependency_snapshot_commit':LOCK['commit'],'group_node':group.name,'source_mesh_count':len(objects),'complete_source_instance':True,'scale':[1,1,1],'rotation_degrees':[0,0,0],'translation_m':[round(v,9) for v in delta],'actual_bounds_m':bounds(objects)};placements.append(row)
 return objects
for side,x in [('west',-1.4),('east',1.4)]:
 station=empty('STATION__'+side,root);station['role']='Complete market stall plus side-pocket two-crate restock stack'
 instantiate('village-market-stall-01',side+'_stall',(x,0),0,station)
 cx=-2.25 if x<0 else 2.25
 instantiate('retail-stackable-produce-crate-01',side+'_crate_lower',(cx,1.2),0,station)
 instantiate('retail-stackable-produce-crate-01',side+'_crate_upper',(cx,1.2),.21,station)
prep=empty('STATION__shared_backstock_prep',root);prep['role']='Shared rear produce preparation/display surface; different legacy style retained for review'
instantiate('interior-open-worktable-01','backstock_table',(0,1.3),0,prep)
table_top=bounds(instances['backstock_table'])['max'][2]
instantiate('retail-fresh-produce-set-01','whole_produce_kit',(0,1.3),table_top,prep)
for objects in sources.values():
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
all_asset=[o for objects in instances.values() for o in objects]

# Convex polygon clipping, used on actual mesh triangles rather than vertex-only tests.
def clip(poly,axis,bound,greater):
 if not poly:return []
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-bound)*(1 if greater else -1);db=(b[axis]-bound)*(1 if greater else -1);ia=da>=-1e-9;ib=db>=-1e-9
  if ia:out.append(a)
  if ia!=ib:out.append(a+(b-a)*(da/(da-db)))
 return out
def area3(poly):
 if len(poly)<3:return 0
 return sum((poly[i]-poly[0]).cross(poly[i+1]-poly[0]).length/2 for i in range(1,len(poly)-1))
def area2(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if len(poly)>2 else 0
def intersect_xy(subject,host):
 p=[Vector((v.x,v.y)) for v in subject];q=[Vector((v.x,v.y)) for v in host]
 sign=1 if sum(a.x*b.y-b.x*a.y for a,b in zip(q,q[1:]+q[:1]))>=0 else -1
 for a,b in zip(q,q[1:]+q[:1]):
  out=[]
  for s,t in zip(p,p[1:]+p[:1]):
   ds=sign*((b.x-a.x)*(s.y-a.y)-(b.y-a.y)*(s.x-a.x));dt=sign*((b.x-a.x)*(t.y-a.y)-(b.y-a.y)*(t.x-a.x));ins=ds>=-1e-9;int_=dt>=-1e-9
   if ins:out.append(s)
   if ins!=int_:out.append(s+(t-s)*(ds/(ds-dt)))
  p=out
  if not p:break
 return area2(p)
def flat_faces(objects,z,up):
 found=[]
 for o,t,mi in triangles(objects):
  n=(t[1]-t[0]).cross(t[2]-t[0])
  if n.length<1e-12:continue
  if max(abs(v.z-z) for v in t)<2e-6 and n.normalized().z*(1 if up else -1)>.999:found.append((o,t))
 return found
def support(label,z,host=None,kind='ground datum'):
 contact=flat_faces(instances[label],z,False)
 if host:tops=flat_faces(instances[host],z,True)
 else:
  v=[Vector((-3.3,-2.5,z)),Vector((3.3,-2.5,z)),Vector((3.3,3.4,z)),Vector((-3.3,3.4,z))];tops=[(None,(v[0],v[1],v[2])),(None,(v[0],v[2],v[3]))]
 rows=[];total=covered=0
 for o,t in contact:
  a=area2(t);c=min(a,sum(intersect_xy(t,q) for _,q in tops));total+=a;covered+=c
  rows.append({'mesh':o.name,'area_m2':round(a,10),'covered_area_m2':round(c,10),'uncovered_area_m2':round(max(0,a-c),10)})
 return {'instance':label,'host':host or 'External game-ground datum Z=0, diagnostic plane not exported','mode':kind,'contact_z_m':z,'downward_contact_triangles':len(contact),'actual_contact_area_m2':round(total,10),'supported_contact_area_m2':round(covered,10),'uncovered_contact_area_m2':round(max(0,total-covered),10),'all_contact_area_supported':total>1e-9 and total-covered<1e-8,'method':'Continuous projected area intersection of each real coplanar downward triangle with real upward host triangles; no AABB or vertex-only full-support inference. Only these contact patches are certified.','triangles':rows}
supports=[]
for label in instances:
 if label.endswith('_upper'):supports.append(support(label,.22,label.replace('_upper','_lower'),'Outer landing pads at upper local Z=.01 meet lower rim; locator tongues enter existing cavity'))
 elif label=='whole_produce_kit':supports.append(support(label,table_top,'backstock_table','Complete source kit; pear/carrot/cabbage real flat contact facets'))
 else:supports.append(support(label,0))

routes=[{'id':'customer_trunk','role':'public customer passage','box':[-3,3,-2.2,-.8,.001,2.5],'target_width_m':1.4,'ports':['public_west','public_east']},{'id':'restock_trunk','role':'independent rear replenishment passage','box':[-3,3,1.9,3.1,.001,2.5],'target_width_m':1.2,'ports':['restock_west','restock_east']},{'id':'prep_access','role':'rear worktable access from restock trunk','box':[-.6,.6,1.61,2.1,.001,2.5],'target_width_m':1.2}]
for side,x in [('west',-1.4),('east',1.4)]:
 routes.append({'id':side+'_vendor_access','role':'rear restock to external rear handoff port; does not enter canopy','box':[x-.55,x+.55,.75,2.1,.001,2.5],'target_width_m':1.1})
 routes.append({'id':side+'_customer_approach','role':'public passage to front counter edge','box':[x-.55,x+.55,-.8,-.58,.001,2.0],'target_width_m':1.1})
for route in routes:
 route['coordinate_frame']='Preset-local Blender Z-up metres; box=[minX,maxX,minY,maxY,minZ,maxZ]. glTF point=(x,z,-y); root placement applies afterwards.'
 b=route['box'];route['gltf_local_y_up_box_m']=[b[0],b[1],b[4],b[5],-b[3],-b[2]];route['gltf_box_axis_order']='[minX,maxX,minY,maxY,minZ,maxZ], glTF Y-up metres'
root['reserved_routes_json']=json.dumps(routes,separators=(',',':'))

# Explicit game interface nodes are non-mesh markers, not geometry or new props.
ports=[]
def add_port(name,xyz,role,region,radius=None):
 node=empty('PORT__'+name,root,xyz);node['port_id']=name;node['role']=role;node['reserved_region_xy_m']=json.dumps(region);node['reserved_region_coordinate_frame']='Preset-local Blender Z-up metres; point (x,y,z) maps to glTF (x,z,-y). Root placement applies afterwards.';node['reserved_region_gltf_local_xz_m']=json.dumps([region[0],region[1],-region[3],-region[2]]);node['gltf_region_axis_order']='[minX,maxX,minZ,maxZ], glTF Y-up metres';node['static_only']=True
 if radius is not None:node['stationary_footprint_radius_m']=radius;node['stationary_body_height_target_m']=2.5
 ports.append({'id':name,'node':node.name,'location_m':list(xyz),'role':role,'reserved_region_xy_m':region,'region_coordinate_frame':'Preset-local Blender Z-up metres; glTF point=(x,z,-y); root placement applies afterwards.','reserved_region_gltf_local_xz_m':[region[0],region[1],-region[3],-region[2]],'stationary_footprint_radius_m':radius,'definition':'Location is a suggested stationary interaction center when radius is present; otherwise an open route boundary marker. Route-prism clearance includes full listed region, not just this point.'})
for side,x in [('west',-1.4),('east',1.4)]:add_port('restock_handoff_'+side,(x,1.05,0),'External rear stall handoff; no under-canopy entry',[x-.55,x+.55,.75,1.35],.30)
for side,x in [('west',-3),('east',3)]:
 add_port('public_'+side,(x,-1.5,0),'Public trunk boundary',[x,x,-2.2,-.8])
 add_port('restock_'+side,(x,2.5,0),'Rear replenishment trunk boundary',[x,x,1.9,3.1])
add_port('prep_stand',(0,1.95,0),'Rear shared-prep stationary interaction; footprint spans prep and restock route union',[-.6,.6,1.61,3.1],.30)
def check_route(r):
 hits=[];box=r['box'];overhead=[]
 for o,t,mi in triangles(all_asset):
  poly=list(t)
  xy_poly=clip(clip(clip(clip(poly,0,box[0],True),0,box[1],False),1,box[2],True),1,box[3],False)
  if area3(xy_poly)>1e-9:overhead.append(min(v.z for v in xy_poly))
  for axis,(lo,hi) in enumerate(((box[0],box[1]),(box[2],box[3]),(box[4],box[5]))):poly=clip(clip(poly,axis,lo,True),axis,hi,False)
  if area3(poly)>1e-9:hits.append({'mesh':o.name,'triangle_area_in_reserved_volume_m2':round(area3(poly),10)})
 return r|{'tested_clear_height_m':box[5],'lowest_actual_geometry_in_xy_m':round(min(overhead),7) if overhead else None,'actual_triangle_intrusions':len(hits),'intrusions':hits[:20],'clear':len(hits)==0}
route_checks=[check_route(r) for r in routes]
excluded_access=[check_route({'id':side+'_source_under_canopy_original_target','role':'Excluded under-canopy vendor connector; original target retained as failure','box':[x-.55,x+.55,.15,2.1,.001,1.95],'target_width_m':1.1}) for side,x in [('west',-1.4),('east',1.4)]]
limited_access=[check_route({'id':side+'_source_under_canopy_limited_body','role':'Alternate body-height measurement only; does not pass original target','box':[x-.55,x+.55,.15,2.1,.001,1.94],'target_width_m':1.1}) for side,x in [('west',-1.4),('east',1.4)]]
def rect_adj(a,b):
 dx=min(a[1],b[1])-max(a[0],b[0]);dy=min(a[3],b[3])-max(a[2],b[2]);return dx>=-1e-7 and dy>=-1e-7 and max(dx,dy)>.1
edges=[]
for i,a in enumerate(routes):
 for b in routes[i+1:]:
  if rect_adj(a['box'],b['box']):edges.append([a['id'],b['id']])
route_graph={'edges':edges,'public_component':['customer_trunk','west_customer_approach','east_customer_approach'],'service_component':['restock_trunk','west_vendor_access','east_vendor_access','prep_access'],'public_and_service_reserved_volumes_disjoint':not any(rect_adj(a['box'],b['box']) for a in routes if a['id'] in ['customer_trunk','west_customer_approach','east_customer_approach'] for b in routes if b['id'] in ['restock_trunk','west_vendor_access','east_vendor_access','prep_access']),'clearance_note':'Public and restock trunks, prep access, and external rear handoff connectors tested to 2.50m with no geometry in their XY footprints. Rear handoff connectors stop outside the canopy at Y=.75m; they do not certify entry into the stall. Original under-canopy access target 1.95m did not pass: actual beam underside is nominally 1.95m (measured 1.9499999m in float geometry). The issue is effectively zero headroom margin, not a 0.1-micrometre modeling defect. A 1.94m limited-height body would have 10mm static margin, but this does not pass the original target. Customer front approaches tested to 2.0m. All heights are game-layout targets, not real-world passage standards.','connection_method':'Exact axis-aligned reserved rectangle intersections. Shared positive-width boundary counts as a connected entrance; these rectangles have exhaustive actual-triangle volume clipping. No computed navmesh or moving-agent collision claim.'}

def bvh(objects):
 ts=triangles(objects);v=[p for _,t,_ in ts for p in t];return BVHTree.FromPolygons(v,[(i,i+1,i+2) for i in range(0,len(v),3)],all_triangles=True,epsilon=0),ts
cache={k:bvh(v) for k,v in instances.items()};clashes=[];contact_pairs=[]
for i,a in enumerate(instances):
 for b in list(instances)[i+1:]:
  aa=bounds(instances[a]);bb=bounds(instances[b])
  if any(aa['max'][k]<bb['min'][k]-1e-6 or bb['max'][k]<aa['min'][k]-1e-6 for k in range(3)):continue
  ta,at=cache[a];tb,bt=cache[b];pairs=ta.overlap(tb);penetrations=[];coplanar=0;boundary_contacts=0
  for ia,ib in pairs:
   qa=at[ia][1];qb=bt[ib][1];na=(qa[1]-qa[0]).cross(qa[2]-qa[0]).normalized();nb=(qb[1]-qb[0]).cross(qb[2]-qb[0]).normalized()
   if abs(na.dot(nb))>.99999 and max(abs((v-qa[0]).dot(na)) for v in qb)<2e-6:coplanar+=1
   else:
    da=[(v-qb[0]).dot(nb) for v in qa];db=[(v-qa[0]).dot(na) for v in qb]
    if min(da)<-2e-6 and max(da)>2e-6 and min(db)<-2e-6 and max(db)>2e-6:penetrations.append([ia,ib])
    else:boundary_contacts+=1
  row={'instances':[a,b],'bvh_surface_pair_count':len(pairs),'coplanar_surface_pairs':coplanar,'edge_or_tangent_boundary_contacts':boundary_contacts,'proper_crossing_pairs':len(penetrations),'note':'Surface intersection screen, not a full solid-penetration certificate. Intended coplanar contact documented separately.'}
  if penetrations:clashes.append(row)
  elif pairs:contact_pairs.append(row)

# For rectilinear crates, an actual-mesh coordinate partition gives a stronger
# static volumetric check than BVH tangency counts. Every box cell is bounded by
# existing source face planes, so its open interior has a constant solid state.
def inside(tree,p):
 direction=Vector((.811,.337,.479)).normalized();pos=p.copy();count=0
 for _ in range(512):
  hit,normal,index,distance=tree.ray_cast(pos,direction,20)
  if hit is None:return count%2==1
  count+=1;pos=hit+direction*2e-6
 raise RuntimeError('Parity iteration limit')
def crate_volume_check(a,b):
 ta,_=bvh(instances[a]);tb,_=bvh(instances[b])
 av=vecs(instances[a]);bv=vecs(instances[b]);at=triangles(instances[a]);bt=triangles(instances[b]);axis_aligned=True
 for _,t,_ in at+bt:
  n=(t[1]-t[0]).cross(t[2]-t[0]).normalized()
  if max(abs(v) for v in n)<.999999:axis_aligned=False
 assert axis_aligned,'Crate volume partition requires all actual faces axis-aligned'
 grid=[]
 for k in range(3):
  lo=max(min(v[k] for v in av),min(v[k] for v in bv));hi=min(max(v[k] for v in av),max(v[k] for v in bv))
  values=sorted(set([round(lo,6),round(hi,6)]+[round(v[k],6) for v in av+bv if lo<v[k]<hi]))
  grid.append([(x,y) for x,y in zip(values,values[1:]) if y-x>2e-6])
 occupied=[];tested=0;volume=0
 for xa,xb in grid[0]:
  for ya,yb in grid[1]:
   for za,zb in grid[2]:
    tested+=1;p=Vector(((xa+xb)/2,(ya+yb)/2,(za+zb)/2))
    if inside(ta,p) and inside(tb,p):
     v=(xb-xa)*(yb-ya)*(zb-za);volume+=v;occupied.append({'min':[xa,ya,za],'max':[xb,yb,zb],'volume_m3':v})
 return {'instances':[a,b],'all_actual_face_normals_axis_aligned':axis_aligned,'partition_cells_tested':tested,'overlap_volume_m3':volume,'occupied_overlap_cells':occupied,'tolerance_m':.000002,'method':'Partition overlapping bounds by all actual source mesh coordinate planes at 1um quantization; parity-classify every open cell in both unchanged closed crate meshes. Exact for retained axis-aligned face arrangement within 2um numerical margin.'}

stack_volume=[crate_volume_check(side+'_crate_lower',side+'_crate_upper') for side in ['west','east']]
negative_controls=[]
upper_group=instances['west_crate_upper'][0].parent
original_upper_location=upper_group.location.copy();upper_group.location.x+=.03;bpy.context.view_layer.update()
negative_controls.append({'name':'crate_upper_shift_30mm','support':support('west_crate_upper',.22,'west_crate_lower'),'solid_overlap':crate_volume_check('west_crate_lower','west_crate_upper')})
upper_group.location=original_upper_location;bpy.context.view_layer.update()
assert not negative_controls[0]['support']['all_contact_area_supported'] and negative_controls[0]['solid_overlap']['overlap_volume_m3']>0,'Negative stack control failed to detect actual support loss and penetration'
# Any wholly enclosed reserve volume must also be rejected: triangle clipping
# alone would not see its boundary. Sample an interior witness against all mesh
# solids; source-internal disconnected components remain separate surfaces.
for r in route_checks:
 b=r['box'];p=Vector(((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2));contained=[]
 for label,(tree,ts) in cache.items():
  bb=bounds(instances[label])
  if all(bb['min'][k]+2e-6<p[k]<bb['max'][k]-2e-6 for k in range(3)) and inside(tree,p):contained.append(label)
 r['solid_containment_witnesses']=contained;r['clear']=r['clear'] and not contained

# Conservative stationary-body checks: cover the full radius-enclosing square,
# not only the marker center. The prep square uses the union of two clear prisms.
port_checks=[]
for port in ports:
 r=port['stationary_footprint_radius_m']
 if r is None:continue
 x,y,z=port['location_m'];box=[x-r,x+r,y-r,y+r]
 ids=['prep_access','restock_trunk'] if port['id']=='prep_stand' else [port['id'].replace('restock_handoff_','')+'_vendor_access']
 hosts=[v for v in route_checks if v['id'] in ids]
 xs=sorted(set([box[0],box[1]]+[h['box'][i] for h in hosts for i in [0,1] if box[0]<h['box'][i]<box[1]]))
 ys=sorted(set([box[2],box[3]]+[h['box'][i] for h in hosts for i in [2,3] if box[2]<h['box'][i]<box[3]]))
 missing=0;cells=0
 for xa,xb in zip(xs,xs[1:]):
  for ya,yb in zip(ys,ys[1:]):
   cells+=1;cx=(xa+xb)/2;cy=(ya+yb)/2
   if not any(h['box'][0]-2e-6<=cx<=h['box'][1]+2e-6 and h['box'][2]-2e-6<=cy<=h['box'][3]+2e-6 for h in hosts):missing+=(xb-xa)*(yb-ya)
 ok=missing<1e-10 and all(h['clear'] for h in hosts)
 port_checks.append({'port':port['id'],'center_m':port['location_m'],'radius_m':r,'tested_body_height_m':min(h['box'][5] for h in hosts),'complete_enclosing_square_xy_m':box,'source_clear_volume_ids':ids,'continuous_union_partition_cells':cells,'uncovered_square_area_m2':missing,'static_full_footprint_and_height_clear':ok,'method':'Partition the whole radius-enclosing square by clear-volume rectangle boundaries; every open cell must lie in the tested union. Since the entire square is covered, the complete circular footprint is also covered. Static only; no swept navigation or motion claim.'})
assert all(p['static_full_footprint_and_height_clear'] for p in port_checks),'Stationary interaction footprint is not fully covered by clear prisms'

# Export a clean editable hierarchy and actual GLB, then reimport this GLB for
# triangle/PBR roundtrip evidence. Diagnostics are added only after these files.
bpy.ops.object.select_all(action='DESELECT')
for o in asset_col.objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
before_sig=fingerprint(all_asset)
scene['candidate_stage']='source/interface candidate; art and runtime independent review pending';scene['diagnostics_exported']=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_extras=True)
import struct
raw=(OUT/'model.glb').read_bytes();json_len=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+json_len]);export_stats={'bytes':len(raw),'nodes':len(gltf.get('nodes',[])),'mesh_nodes':sum('mesh' in n for n in gltf.get('nodes',[])),'unique_meshes':len(gltf.get('meshes',[])),'materials':len(gltf.get('materials',[])),'textures':len(gltf.get('textures',[])),'extensions_used':gltf.get('extensionsUsed',[]),'mesh_reference_counts':dict(Counter(str(n['mesh']) for n in gltf.get('nodes',[]) if 'mesh' in n))}
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);reimport=[o for o in bpy.data.objects if o not in before];roundtrip=[o for o in reimport if o.type=='MESH'];bpy.context.view_layer.update();after_sig=fingerprint(roundtrip)
roundtrip_report={'all_oriented_world_triangles_and_pbr_equal_at_10um':before_sig==after_sig,'before_signature':before_sig,'after_signature':after_sig,'mesh_nodes_before':len(all_asset),'mesh_nodes_after':len(roundtrip),'triangles_before':len(triangles(all_asset)),'triangles_after':len(triangles(roundtrip)),'diagnostic_nodes_exported':False,'actual_glb_reimport':True,'export_stats':export_stats}
for o in reimport:bpy.data.objects.remove(o,do_unlink=True)
dependency_after=[]
for f in LOCK['files']:
 data=(SNAPSHOT/f['path']).read_bytes();dependency_after.append(hashlib.sha256(data).hexdigest()==f['sha256'])
report={'id':'retail-fresh-market-scene-01','stage':'gray/interface','formal_approved':False,'art_passed':False,'dependency_snapshot_commit':LOCK['commit'],'catalog_source_mapping':LOCK['catalog_source_mapping'],'dependency_integrity_before_after':all(dependency_after),'reused_source_ids':4,'new_standalone_props':0,'instance_count':len(instances),'source_measurements':measurements,'placements':placements,'geometry_bounds_m':bounds(all_asset),'layout_envelope_m':{'x':[-3,3],'y':[-2.2,3.1]},'triangles':len(triangles(all_asset)),'support_checks':supports,'route_checks':route_checks,'excluded_under_canopy_access':{'original_target_height_m':1.95,'precision_note':'Measured 1.9499999m is the floating-point representation of nominal 1.95m. Original-height body has effectively zero headroom margin; this is not a 0.1um source modeling defect.','actual_minimum_beam_underside_m':min(r['lowest_actual_geometry_in_xy_m'] for r in excluded_access),'original_target_pass':all(r['clear'] for r in excluded_access),'original_target_tests':excluded_access,'limited_body_tests':limited_access,'limited_body_height_m':1.94,'limited_body_static_margin_m':.0099999,'excluded_from_public_and_restock_network':True,'scope':'Source-preserved stall interior is not claimed as a passing walk-through vendor replenishment workflow. Network terminates at external rear handoff interaction ports.'},'route_graph':route_graph,'interface_port_footprint_checks':port_checks,'unexpected_noncoplanar_surface_intersections':clashes,'intended_boundary_contacts':contact_pairs,'crate_stack_solid_volume_checks':stack_volume,'negative_controls':negative_controls,'support_separation_fact':{'table_max_z_m':table_top,'whole_kit_min_z_m':bounds(instances['whole_produce_kit'])['min'][2],'nonpenetration':'All source table vertices at or below table top; all complete kit vertices at or above it. Horizontal separation plane proves no positive-volume overlap within 2um.'},'roundtrip':roundtrip_report,'limits':['Static game-layout targets only; no commercial, building-code or accessibility compliance.','No dynamics, crate load/stack stability, food safety or structural strength certification.','Source-internal generic produce proxies, stem/leaf attachments and complete stall topology remain unchanged.','External flat ground at Z=0 required. Diagnostic ground and route marks are not included in GLB.','Styles remain original and intentionally unmodified; single-view original-PBR coordination review is still required.','No Firefox/WebGL runtime claim; pending original local Firefox review.'],'gate':{'all_real_contact_patches_supported':all(x['all_contact_area_supported'] for x in supports),'all_reserved_volumes_surface_clear':all(x['clear'] for x in route_checks),'original_1_95m_under_canopy_service_workflow':False,'scope':'External rear handoff only; preserved stall interior remains restricted.','public_service_separated':route_graph['public_and_service_reserved_volumes_disjoint'],'no_unexpected_proper_surface_crossings':not clashes,'no_crate_solid_overlap':all(x['overlap_volume_m3']==0 for x in stack_volume),'all_declared_stationary_port_footprints_clear':all(p['static_full_footprint_and_height_clear'] for p in port_checks),'negative_control_detects_30mm_stack_failure':not negative_controls[0]['support']['all_contact_area_supported'] and negative_controls[0]['solid_overlap']['overlap_volume_m3']>0,'exact_imported_glb_triangle_pbr_match_10um':before_sig==after_sig,'independent_review':'PENDING','pbr_style_review':'NOT_STARTED','browser_runtime':'NOT_STARTED'}}
(QA/'geometry-report.json').write_text(json.dumps(report,indent=2)+'\n')
composition={'id':report['id'],'assetKind':'scene','description':'Two complete front-facing produce stalls, a shared rear prep table with complete produce kit, and two side-pocket two-crate stacks. Separate front public and rear restock interface volumes.','dependency_snapshot_commit':LOCK['commit'],'catalog_source_mapping':LOCK['catalog_source_mapping'],'instance_policy':'Complete source GLB mesh sets, scale 1, rigid translations only. Each instance is an independently selectable source-tagged group under a single movable preset root.','instances':placements,'coordinate_frame':{'layout':'Preset-local Blender Z-up metres; root placement applies afterwards','gltf_point_mapping':['x','z','-y'],'custom_region_extras':'Remain in stated layout frame; GLB node transforms use standard glTF Y-up.'},'layout_envelope_m':report['layout_envelope_m'],'interface_ports':ports,'routes':routes,'route_graph':route_graph,'reuse_counting':{'new_scene_presets':1,'new_standalone_props':0,'reused_asset_ids':4,'reused_instances':len(instances)},'limits':report['limits']}
(OUT/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
(QA/'roundtrip-report.json').write_text(json.dumps(roundtrip_report,indent=2)+'\n')
def emit_metadata():
 if not (OUT/'thumbnail.png').is_file():
  print('METADATA_PENDING_THUMBNAIL: geometry-only build has no rendered PNG; no partial metadata emitted.',flush=True);return
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  path=OUT/name
  if not path.is_file():continue
  data=path.read_bytes();files[role]={'path':'assets/retail/retail-fresh-market-scene-01/v1.0.0/'+name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 metadata={'id':'retail-fresh-market-scene-01','version':'1.0.0','category':'scenes','assetKind':'scene','theme':'retail','style':'original-source-mix','title':'Two-Bay Fresh Market Handoff Preset','description':'Static game layout: two complete published produce stalls, shared rear prep table with whole produce kit, and two side-pocket two-crate stacks. Separate front public and rear external handoff/storage interfaces. Stall interior has nominal 1.95m beam clearance and does not pass a 1.95m-body workflow. Exterior routes terminate at handoff points outside canopy. External flat ground Z=0 required. Seven named game ports and full reserved-route data are embedded in the GLB. Custom regions use preset-local Blender Z-up metres and map to glTF Y-up by (x,y,z) to (x,z,-y). No moving navigation, accessibility, commercial, load or dynamics certification.','bounds':dict(zip('xyz',report['geometry_bounds_m']['dimensions']),unit='m'),'triangles':report['triangles'],'materials':export_stats['materials'],'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
emit_metadata()
print('GRAY_GEOMETRY_RESULT',json.dumps(report['gate']),flush=True)

if (args.render_gray or args.render_pbr or args.render_final) and not args.no_render:
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128 if args.render_final else 24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=args.threads
 scene.render.resolution_x=1024 if args.render_final else 1200;scene.render.resolution_y=1024 if args.render_final else 1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.exposure=0;scene.view_settings.gamma=1;scene.world=bpy.data.worlds.new('Diagnostic studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.5,.5,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 def material(name,color):
  m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=.85;return m
 gray=material('DIAGNOSTIC clay override',(.43,.45,.46));floor_mat=material('DIAGNOSTIC ground',(.22,.24,.25));route_mat=material('DIAGNOSTIC route',(.46,.48,.49));text_mat=material('DIAGNOSTIC labels',(.04,.05,.055))
 def plane(name,xy,size,z,mat):
  bpy.ops.mesh.primitive_plane_add(size=1,location=(*xy,z));o=bpy.context.object;o.name='DIAGNOSTIC '+name;o.scale=(size[0],size[1],1);o.data.materials.append(mat);move_collection(o,diag_col);return o
 plane('external ground datum',(0,.45),(200,200) if args.render_final else (7.0,6.5),-.004,floor_mat)
 if not args.render_final:
  for r in routes:
   if r['id'] not in ('customer_trunk','restock_trunk'):continue
   b=r['box'];plane(r['id'],((b[0]+b[1])/2,(b[2]+b[3])/2),(b[1]-b[0],b[3]-b[2]),-.002,route_mat)
  def text(body,loc,size=.17):
   cu=bpy.data.curves.new('DIAGNOSTIC text','FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=size;o=bpy.data.objects.new('DIAGNOSTIC '+body,cu);diag_col.objects.link(o);o.location=loc;o.data.materials.append(text_mat)
  text('CUSTOMER PASSAGE   1.40 m',(0,-1.5,.001),.19);text('REAR RESTOCK   1.20 m',(0,2.5,.001),.19)
  text('PREP',(0,1.3,1.14),.12)
  for x,label in [(-1.4,'A'),(1.4,'B')]:text(label+' HANDOFF',(x,1.02,.001),.14)
 def aim(o,loc,target):o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,loc,power,size in [('Key',(-4,-5,9),1600,6),('Fill',(6,-1,6),850,5),('Rim',(0,6,8),1300,5)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name='DIAGNOSTIC '+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;move_collection(o,diag_col);aim(o,loc,(0,.4,.9))
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='DIAGNOSTIC camera';move_collection(cam,diag_col);cam.data.type='ORTHO';scene.camera=cam
 if args.render_gray:
  # Per-object material override clones are presentation-only, after the saved
  # source/GLB and integrity checks. Original material values remain untouched.
  original=[]
  for o in all_asset:
   o.data=o.data.copy();original.append((o,list(o.data.materials)))
   for i in range(len(o.data.materials)):o.data.materials[i]=gray
  for name,loc,target,scale in [('gray-isometric',(8,-10,9),(0,.4,.6),9.6),('gray-top',(0,.45,12),(0,.45,0),7.8)]:
   cam.data.ortho_scale=scale;aim(cam,loc,target);scene.render.filepath=str(QA/(name+'.png'));bpy.ops.render.render(write_still=True)
  for o,mats in original:
   for i,m in enumerate(mats):o.data.materials[i]=m
 if args.render_pbr:
  cam.data.ortho_scale=8.5;aim(cam,(7,9,13),(0,.6,.8));scene.render.filepath=str(QA/'original-pbr-coordination.png');render_start=time.monotonic();bpy.ops.render.render(write_still=True);(QA/'pbr-render-timing.json').write_text(json.dumps({'image':'original-pbr-coordination.png','samples':scene.cycles.samples,'denoising':False,'engine':'Cycles CPU','threads':args.threads,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'render_seconds':round(time.monotonic()-render_start,3),'camera_location_m':[7,9,13],'target_m':[0,.6,.8],'purpose':'Single original-PBR style-coordination gate; not six-view final art evidence.'},indent=2)+'\n')
 if args.render_final:
  import shutil
  from bpy_extras.object_utils import world_to_camera_view
  points=vecs(all_asset);render_rows=[]
  bb=report['geometry_bounds_m'];center=Vector(tuple((bb['min'][i]+bb['max'][i])/2 for i in range(3)))
  views=[('qa-isometric',(7,9,13),(0,.6,.8)),('qa-front',(0,-12,center.z),center),('qa-back',(0,12,center.z),center),('qa-left',(-12,center.y,center.z),center),('qa-right',(12,center.y,center.z),center),('qa-top',(0,center.y,12),center)]
  for name,loc,target in views:
   aim(cam,loc,target);cam.data.ortho_scale=1
   basis=cam.rotation_euler.to_matrix();right=basis@Vector((1,0,0));up=basis@Vector((0,1,0))
   xs=[v.dot(right) for v in points];ys=[v.dot(up) for v in points]
   cam.location+=right*((min(xs)+max(xs))/2-cam.location.dot(right))+up*((min(ys)+max(ys))/2-cam.location.dot(up))
   frame=cam.data.view_frame(scene=scene);fw=max(v.x for v in frame)-min(v.x for v in frame);fh=max(v.y for v in frame)-min(v.y for v in frame)
   cam.data.ortho_scale=max((max(xs)-min(xs))/(fw*.80),(max(ys)-min(ys))/(fh*.80))
   bpy.context.view_layer.update();ndc=[world_to_camera_view(scene,cam,v) for v in points];image_bounds={'min':[min(v[i] for v in ndc) for i in range(2)],'max':[max(v[i] for v in ndc) for i in range(2)]}
   assert min(image_bounds['min'])>.06 and max(image_bounds['max'])<.94 and min(v.z for v in ndc)>0,('Asset clipped',name,image_bounds)
   scene.render.filepath=str(QA/(name+'.png'));started=time.monotonic();print('FORMAL_VIEW_START',name,flush=True);bpy.ops.render.render(write_still=True)
   render_rows.append({'image':name+'.png','samples':128,'denoising':False,'seconds':round(time.monotonic()-started,3),'camera_location_m':list(cam.location),'camera_rotation_euler_rad':list(cam.rotation_euler),'ortho_scale_m':cam.data.ortho_scale,'actual_asset_normalized_image_bounds':image_bounds,'all_mesh_vertices_inside_with_margin':True})
   (QA/'formal-render-report.json').write_text(json.dumps({'engine':'Cycles CPU','threads':args.threads,'samples':128,'denoising':False,'resolution':[1024,1024],'view_transform':'AgX','exposure':0,'gamma':1,'fixed_lighting':True,'floor':'Clean neutral diagnostic studio floor, never exported','diagnostic_route_marks_or_text':False,'views':render_rows},indent=2)+'\n')
   if name=='qa-isometric':shutil.copyfile(QA/(name+'.png'),OUT/'thumbnail.png')
  emit_metadata()
 bpy.ops.wm.save_as_mainfile(filepath=str(QA/'diagnostic.blend'))
 if args.render_pbr:
  import shutil
  shutil.copyfile(QA/'original-pbr-coordination.png',OUT/'thumbnail.png')
  emit_metadata()
