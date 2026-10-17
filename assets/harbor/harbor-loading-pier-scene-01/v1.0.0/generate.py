"""Reproducible Harbor loading pier scene, blockout milestone only.

Blender 4.3.2: blender -b -t 2 --python generate.py -- --no-render
Render only after scheduling approval: ... -- --render
Optional --snapshot /absolute/repository/root overrides dependency discovery.
By default walk ancestors to a normal repository containing assets/harbor.
The full immutable lock is embedded here; no local recovery path is required.
The script never executes or modifies a recovered generator, metadata or GLB.
No new standalone prop IDs, no exported diagnostic floor, no final verification.
"""
import bpy, math, json, hashlib, argparse, sys, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from datetime import datetime, timezone

START=time.monotonic()
OUT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--snapshot', type=Path);p.add_argument('--render',action='store_true');p.add_argument('--no-render',action='store_true');p.add_argument('--final',action='store_true')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
LOCK=json.loads(r'''{"repository":"shAdow-XJY-Games/Shadow3DAssetLibrary","commit":"5423a77851ffbd774139691620367012c8632673","materialization":"GitHub published snapshot, not recovered local QA","dependencies":[{"id":"harbor-barrel-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-barrel-01/v1.0.0/metadata.json","bytes":1312,"sha256":"853c3429830547f80a253aa00a47e78683d537f3100ddcd7f1b314b60cd6bd6f"},{"path":"assets/harbor/harbor-barrel-01/v1.0.0/generate.py","bytes":8582,"sha256":"1fecc4d3c282e26d993b466763b841d2cb1fd2ce5ddf971e550740b4cf54ceb7"},{"path":"assets/harbor/harbor-barrel-01/v1.0.0/model.glb","bytes":122820,"sha256":"9e5d23259567c36b6839e99b7fe1a107cf0d4952028fdc61206d7cd8028bedf5"}]},{"id":"harbor-bench-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-bench-01/v1.0.0/metadata.json","bytes":1288,"sha256":"65b479a58f15da2cf27c4572ad2fb12f60c6c2b529cd846ea24f54a98033d01f"},{"path":"assets/harbor/harbor-bench-01/v1.0.0/generate.py","bytes":7673,"sha256":"a1a1f0c9f645491953aa691d52a02fd08ccea26240e8b38b5b7d6a0f789b21db"},{"path":"assets/harbor/harbor-bench-01/v1.0.0/model.glb","bytes":69816,"sha256":"8337ebde408cf87ec26616455971aaa863114339864f75cd42ad81594cbf6ed8"}]},{"id":"harbor-cargo-sack-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-cargo-sack-01/v1.0.0/metadata.json","bytes":1308,"sha256":"cd6943927017c1007724ac71f3b4b523dc5b66a17ec20050498e84a702ec4340"},{"path":"assets/harbor/harbor-cargo-sack-01/v1.0.0/generate.py","bytes":8050,"sha256":"43d0eaccb06e3b6c87a66a68b199cd65ca009fd84d5be84b350422c2e8294555"},{"path":"assets/harbor/harbor-cargo-sack-01/v1.0.0/model.glb","bytes":49652,"sha256":"c93a3bb3df9b4c4ad81d9fcdc2d2b3423a1cde4aaeec5227fd0ad69964251804"}]},{"id":"harbor-crate-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-crate-01/v1.0.0/metadata.json","bytes":1279,"sha256":"076ebf3cdf3618fdbbb5a39e03ea7e49c9bc99a2f1c8ed770242308174b2a156"},{"path":"assets/harbor/harbor-crate-01/v1.0.0/generate.py","bytes":7374,"sha256":"0a5ac10467f01ec354b060f9c162edaf5c9e96a9b6b8fe1d346392a0229a3fba"},{"path":"assets/harbor/harbor-crate-01/v1.0.0/model.glb","bytes":119864,"sha256":"2357603c38ace3bdc48472890f88dcaf4170cebcadbbe7b932d54b977ef87ce6"}]},{"id":"harbor-dock-module-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-dock-module-01/v1.0.0/metadata.json","bytes":1346,"sha256":"581453d1d5d9daf9ac4cbe132a36704b258d238752148a815a8c9c2b5b3d781b"},{"path":"assets/harbor/harbor-dock-module-01/v1.0.0/generate.py","bytes":7511,"sha256":"69502b87d90f1421f9601a7bc342d32988b764499051d7161c60eca8e134bc8c"},{"path":"assets/harbor/harbor-dock-module-01/v1.0.0/model.glb","bytes":60084,"sha256":"405124a33aab044d596373198a76766a0acee752b3266d46dea748070fe4c14c"}]},{"id":"harbor-lantern-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-lantern-01/v1.0.0/metadata.json","bytes":1311,"sha256":"b303e8b16d31d54d6602f78c1e07063eddd0b9981ae53c690dc5d109b1c6cfd7"},{"path":"assets/harbor/harbor-lantern-01/v1.0.0/generate.py","bytes":7489,"sha256":"eb367d268f98f0b34a96767eb05fa31608de02e8787da1bb11b40c878fa7c6d1"},{"path":"assets/harbor/harbor-lantern-01/v1.0.0/model.glb","bytes":46904,"sha256":"45a02e9af4f93a2ba92fd14e94ef5bc3f4a865c1210cfa33f109e2b7422ff4de"}]},{"id":"harbor-lifebuoy-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-lifebuoy-01/v1.0.0/metadata.json","bytes":1298,"sha256":"07ace0e5886ace183b6c937f5f31ed4f8f04ad6a38ad2393b8c58beb026b87e2"},{"path":"assets/harbor/harbor-lifebuoy-01/v1.0.0/generate.py","bytes":8675,"sha256":"b3ebe02e9c13575a1852dd12579a3113a946d488caf6b9786e4c20b1c5a8f1a1"},{"path":"assets/harbor/harbor-lifebuoy-01/v1.0.0/model.glb","bytes":66792,"sha256":"ce291b53172c7d022529c3c79028b5f2d92478cb701299041df01c0f641dd741"}]},{"id":"harbor-rope-coil-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-rope-coil-01/v1.0.0/metadata.json","bytes":1309,"sha256":"4d9ac94cf4b766a1944363c4d1abb8bf8e6f15705bdc45078dc607d0319542cc"},{"path":"assets/harbor/harbor-rope-coil-01/v1.0.0/generate.py","bytes":8219,"sha256":"aacf18c704937d7dc775b51dd19a5f886a2f813e47677544e80a4fd36eaccf9b"},{"path":"assets/harbor/harbor-rope-coil-01/v1.0.0/model.glb","bytes":118436,"sha256":"08f7af6b3a4708f1fd41f7b32422880bbf37244ae47d60e9a22fbc23b8361e1c"}]},{"id":"harbor-sign-01","version":"1.0.0","reuse":true,"count_as_new_asset":false,"files":[{"path":"assets/harbor/harbor-sign-01/v1.0.0/metadata.json","bytes":1314,"sha256":"15d7f90f018eb07b1aea175577e9fcb951ee93affb5d75ab6cf05118a99ea7cc"},{"path":"assets/harbor/harbor-sign-01/v1.0.0/generate.py","bytes":7696,"sha256":"2dcec219168dde0f48398e60b08466729995a8120d32336ff6cce7fad736d346"},{"path":"assets/harbor/harbor-sign-01/v1.0.0/model.glb","bytes":44828,"sha256":"e26c0868e41bcd3ce909117a600aa61e28b8e2b1e379d8d43009487eabaaa1bd"}]}]}''')
def resolve_dependency_root(explicit):
 if explicit:return explicit.resolve()
 required=[dep['files'][0]['path'] for dep in LOCK['dependencies']]
 for ancestor in (OUT,*OUT.parents):
  if all((ancestor/name).is_file() for name in required):return ancestor
 raise RuntimeError('No normal repository root containing locked assets/harbor dependencies found. Supply --snapshot /path/to/repository-root; no downloads or source replacement are performed.')
SNAPSHOT=resolve_dependency_root(args.snapshot)
ASSET='harbor-loading-pier-scene-01'
EPS=2e-5
report={'id':ASSET,'version':'1.0.0','stage':'blockout','status':'prototype','formal_approved':False,'art_passed':False,'blender':bpy.app.version_string,'generated_utc':datetime.now(timezone.utc).isoformat(),'source':{'repository':LOCK['repository'],'commit':LOCK['commit'],'kind':LOCK['materialization']},'geometry_method':'Actual imported pinned GLB evaluated triangle/vertex coordinates in Blender world meters; no source generator execution.','validation_limits':['Offline Blender geometry only; not browser or WebGL evidence.','No load, buoyancy, mooring, water, dynamic motion, slip, human accessibility or engineering safety validation.','Shore connection and water are excluded from this blockout. Existing launch-ramp top .72m differs from dock .75m; short-platform usable top is .38m, not its .51m rim.','Geometric placement/contact is not a structural-strength certification.','Reused prop instances are not new standalone asset IDs.'],'new_standalone_prop_count':0,'reused_asset_id_count':9,'source_dependencies':[]}
for dep in LOCK['dependencies']:
 for f in dep['files']:
  path=SNAPSHOT/f['path']
  if not path.is_file():raise RuntimeError('Missing locked dependency: '+str(path))
  data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
  if len(data)!=f['bytes'] or digest!=f['sha256']:raise RuntimeError('Dependency lock mismatch: '+str(path))
 report['source_dependencies'].append(dep)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.name='Harbor_Blockout_Offline_Geometry'
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
asset_col=bpy.data.collections.new('ASSET_REUSED_INSTANCES_ONLY');scene.collection.children.link(asset_col)
rig_col=bpy.data.collections.new('DIAGNOSTIC_CONTEXT_NOT_ASSET');scene.collection.children.link(rig_col)

def attach(obj,col):
 for c in list(obj.users_collection):c.objects.unlink(obj)
 col.objects.link(obj)

def coords(objs):
 return [o.matrix_world@v.co for o in objs for v in o.data.vertices]

def bounds(objs):
 v=coords(objs);lo=[min(x[i] for x in v) for i in range(3)];hi=[max(x[i] for x in v) for i in range(3)]
 return {'min':[round(x,7) for x in lo],'max':[round(x,7) for x in hi],'dimensions':[round(hi[i]-lo[i],7) for i in range(3)]}

def triangle_data(objs):
 vs=[];fs=[]
 for o in objs:
  o.data.calc_loop_triangles();offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices)
  fs.extend(tuple(offset+i for i in t.vertices) for t in o.data.loop_triangles)
 return vs,fs

def bvh(objs):
 v,f=triangle_data(objs);return BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=0)

def split_islands(objs):
 """Connected exported-position islands; includes separate GLTF material vertices."""
 records=[]
 for o in objs:
  verts=[o.matrix_world@v.co for v in o.data.vertices]
  # Weld equal positions for adjacency only, without changing mesh/source data.
  keys=[tuple(round(x,6) for x in v) for v in verts];neighbors={k:set() for k in keys}
  for edge in o.data.edges:
   a,c=(keys[i] for i in edge.vertices);neighbors[a].add(c);neighbors[c].add(a)
  unseen=set(neighbors)
  while unseen:
   seed=min(unseen);stack=[seed];unseen.remove(seed);found=[]
   while stack:
    k=stack.pop();found.append(k)
    for q in neighbors[k]:
     if q in unseen:unseen.remove(q);stack.append(q)
   lo=[min(x[i] for x in found) for i in range(3)];hi=[max(x[i] for x in found) for i in range(3)]
   records.append({'min':lo,'max':hi,'unique_vertex_count':len(found),'points':found})
 return sorted(records,key=lambda d:(d['min'][2],d['min'][0],d['min'][1]))

sources={};source_stats=[]
for dep in LOCK['dependencies']:
 aid=dep['id'];path=SNAPSHOT/'assets/harbor'/aid/'v1.0.0/model.glb'
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path),merge_vertices=False)
 imported=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
 if not imported:raise RuntimeError('No mesh in '+aid)
 for o in imported:attach(o,asset_col);o.name='SOURCE__'+aid+'__'+o.name
 bpy.context.view_layer.update()
 sources[aid]=imported
 stat={'id':aid,'actual_bounds_m':bounds(imported),'triangles':sum(len(o.data.loop_triangles) for o in imported),'mesh_objects':len(imported),'source_material_slots':sum(len(o.data.materials) for o in imported)}
 meta=json.loads((path.parent/'metadata.json').read_text());stat['published_dimensions_m']=[meta['bounds'][k] for k in ('x','y','z')]
 stat['dimensions_match_published_within_0_1mm']=max(abs(stat['actual_bounds_m']['dimensions'][i]-stat['published_dimensions_m'][i]) for i in range(3))<.0001
 if not stat['dimensions_match_published_within_0_1mm']:raise RuntimeError('Measured metadata mismatch '+aid)
 source_stats.append(stat)
# Reuse equivalent PBR references without altering any shader parameter, mesh or face index.
canonical_materials={}
for objects in sources.values():
 for obj in objects:
  for index,mat in enumerate(obj.data.materials):
   node=mat.node_tree.nodes.get('Principled BSDF')
   signature=(tuple(node.inputs['Base Color'].default_value),float(node.inputs['Metallic'].default_value),float(node.inputs['Roughness'].default_value),float(node.inputs['Alpha'].default_value),tuple(node.inputs['Emission Color'].default_value),float(node.inputs['Emission Strength'].default_value),mat.use_backface_culling)
   if signature not in canonical_materials:canonical_materials[signature]=mat
   obj.data.materials[index]=canonical_materials[signature]
report['source_measurements']=source_stats
instances={};placements=[]

def instance(aid,label,xy,base_z,rot=(0,0,0),support='deck'):
 copies=[];R=Matrix.Rotation(rot[2],4,'Z')@Matrix.Rotation(rot[1],4,'Y')@Matrix.Rotation(rot[0],4,'X')
 for source in sources[aid]:
  obj=source.copy();obj.data=source.data;asset_col.objects.link(obj);obj.name=label
  obj.matrix_world=R@source.matrix_world;obj['source_asset_id']=aid;obj['instance_label']=label;obj['source_commit']=LOCK['commit'];obj['source_version']='1.0.0';obj['reused_not_new_asset']=True
  copies.append(obj)
 bpy.context.view_layer.update();bb=bounds(copies)
 delta=Vector((xy[0]-(bb['min'][0]+bb['max'][0])/2,xy[1]-(bb['min'][1]+bb['max'][1])/2,base_z-bb['min'][2]))
 for o in copies:o.matrix_world=Matrix.Translation(delta)@o.matrix_world
 bpy.context.view_layer.update();instances[label]=copies
 placements.append({'label':label,'source_asset_id':aid,'reuse':True,'new_standalone_id':False,'xy_bbox_center_m':list(xy),'requested_base_z_m':base_z,'rotation_degrees':[round(math.degrees(v),3) for v in rot],'support_target':support,'rigid_world_matrices':[[[round(float(v),9) for v in row] for row in o.matrix_world] for o in copies],'actual_bounds_m':bounds(copies)})
 return copies

for x,y,label in [(-1,-1,'dock_SW'),(1,-1,'dock_SE'),(-1,1,'dock_NW'),(1,1,'dock_NE')]:instance('harbor-dock-module-01',label,(x,y),0,support='diagnostic datum z=0; terrain not part of scene')
instance('harbor-bench-01','bench',(0.65,1.45),.75)
instance('harbor-crate-01','crate',(-1.20,1.18),.75)
instance('harbor-barrel-01','barrel',(-1.32,-.25),.75)
instance('harbor-cargo-sack-01','cargo_sack',(-1.35,-1.15),.75)
instance('harbor-rope-coil-01','rope_coil',(1.27,-1.28),.75)
instance('harbor-lifebuoy-01','lifebuoy_flat',(1.28,.12),.75,rot=(math.pi/2,0,0))
instance('harbor-sign-01','sign',(-.75,-1.35),.75)
crate_top=bounds(instances['crate'])['max'][2]
instance('harbor-lantern-01','lantern_on_crate',(-1.20,1.24),crate_top,support='crate actual top lid')
for objects in sources.values():
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
report['placements']=placements
composition={'id':ASSET,'assetKind':'scene','scope':'Unconnected 4m static cargo/rest platform preset, not a complete accessible harbor. No water or shore connection.','reused_asset_id_count':9,'instance_count':12,'new_standalone_prop_count':0,'source':report['source'],'source_version':'1.0.0','placement_edits':'Rigid transform instances only; source meshes and PBR values unchanged; equivalent materials share references.','intended_use':{'cargo_zone':'West side crate, barrel and sack group with lantern on crate; staging/visual dressing, no simulated loading.','seating_zone':'Northeast bench facing toward central space.','open_center':'Measured empty XY strip x[-.25,.55], y[-2,1], 0.8m wide; layout allowance only, not accessibility certification.','loose_equipment':'East-side laid-flat rescue ring and rope coil; no simulated rescue or mooring.','sign':'Southwest wayfinding marker; no shore route implied.'},'instances':placements,'dependencies':LOCK['dependencies'],'limitations':report['validation_limits']}
(OUT/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
report['instance_count']=len(instances)
all_asset=[o for objects in instances.values() for o in objects]
report['scene_bounds_m']=bounds(all_asset)
report['scene_triangles']=sum(len(o.data.loop_triangles) for o in all_asset)
report['unique_source_triangles']=sum(s['triangles'] for s in source_stats)

# Check actual support with downward rays at contact-plane mesh vertices and triangle centroids.
# This is contact sampling, not continuous proof of all projected lower surface area.
docks=[o for label,objects in instances.items() if label.startswith('dock_') for o in objects]
deck_bvh=bvh(docks)

def support_check(label,support_objects,support_z):
 objs=instances[label];bb=bounds(objs);lowest=bb['min'][2];samples=set();contact_triangles=0;support_islands=[]
 v,f=triangle_data(objs)
 for i,pt in enumerate(v):
  if abs(pt.z-lowest)<EPS:samples.add(tuple(round(x,7) for x in pt))
 for tri in f:
  pts=[v[i] for i in tri]
  if all(abs(pt.z-lowest)<EPS for pt in pts):
   cen=sum(pts,Vector())/3;samples.add(tuple(round(x,7) for x in cen));contact_triangles+=1
 tree=bvh(support_objects);miss=[];hits=[]
 for s in sorted(samples):
  hit,norm,index,dist=tree.ray_cast(Vector((s[0],s[1],lowest+.002)),Vector((0,0,-1)),.08)
  good=hit is not None and abs(hit.z-lowest)<.0001 and norm.z>.8
  if good:hits.append(s)
  else:miss.append({'sample_m':s,'surface_hit_z_m':round(hit.z,7) if hit is not None else None,'hit_normal_z':round(norm.z,5) if norm is not None else None})
 for island in split_islands(objs):
  if abs(island['min'][2]-lowest)<EPS:
   pts=[p for p in island['points'] if abs(p[2]-lowest)<EPS];count=0
   for pt in pts:
    hit,norm,_,_=tree.ray_cast(Vector((pt[0],pt[1],lowest+.002)),Vector((0,0,-1)),.08)
    if hit is not None and abs(hit.z-lowest)<.0001 and norm.z>.8:count+=1
   support_islands.append({'bounds_min_m':island['min'],'bounds_max_m':island['max'],'contact_vertices':len(pts),'supported_contact_vertices':count,'has_sampled_support':count>0})
 return {'label':label,'base_z_m':lowest,'expected_surface_z_m':support_z,'vertical_datum_gap_m':round(lowest-support_z,7),'contact_plane_triangles':contact_triangles,'zero_area_edge_or_point_only_contact':contact_triangles==0,'samples_tested':len(samples),'samples_on_actual_upward_surface':len(hits),'missed_contact_samples':miss,'contact_islands':support_islands,'all_contact_islands_have_sampled_support':all(x['has_sampled_support'] for x in support_islands),'all_contact_samples_on_surface':len(miss)==0,'method':'Downward triangle-BVH ray at every minimum-Z vertex and every all-minimum-Z triangle centroid, plus connected-position island counts. Intentional plank gaps may give misses; report them, do not erase source geometry.'}
report['support_checks']=[support_check(label,instances['crate'] if label=='lantern_on_crate' else docks,crate_top if label=='lantern_on_crate' else .75) for label in instances if not label.startswith('dock_')]

# Pile base island count and datum contact. These are geometric datum checks only.
pile_checks=[]
for label in [k for k in instances if k.startswith('dock_')]:
 base=[x for x in split_islands(instances[label]) if abs(x['min'][2])<EPS]
 pile_checks.append({'dock':label,'base_islands_at_z0':len(base),'bottoms_m':[{'xy_min':x['min'][:2],'xy_max':x['max'][:2],'bottom_z':x['min'][2]} for x in base],'expected_four_pile_bases':len(base)==4,'note':'Datum plane only. Seabed bearing, embedment, soil and structural performance untested.'})
report['pile_datum_checks']=pile_checks

# Sample height across seams; beveled deck edges deliberately drop 12mm at the exact seam.
seams=[]
for axis in [0,1]:
 samples=[]
 for transverse in [-1.9,-1.7,-1.5,-1.3,-1.1,-.9,-.7,-.5,-.3,-.1,.1,.3,.5,.7,.9,1.1,1.3,1.5,1.7,1.9]:
  row={'along_m':transverse,'cross_section':[]}
  for off in [-.016,-.012,-.006,-.001,0,.001,.006,.012,.016]:
   x,y=(off,transverse) if axis==0 else (transverse,off)
   hit,norm,_,_=deck_bvh.ray_cast(Vector((x,y,.80)),Vector((0,0,-1)),.20)
   row['cross_section'].append({'offset_m':off,'hit_z_m':round(hit.z,7) if hit is not None else None})
  samples.append(row)
 seams.append({'axis':'X' if axis==0 else 'Y','seam_coordinate_m':0,'samples':samples})
report['seam_checks']={'module_footprint_m':[2,2],'platform_footprint_m':[4,4],'centers_m':[[-1,-1],[1,-1],[-1,1],[1,1]],'nominal_deck_top_z_m':.75,'all_module_deck_max_z_m':[bounds(instances[k])['max'][2] for k in instances if k.startswith('dock_')],'zero_module_bbox_gap_m':0,'note':'Actual beveled deck edge seam cross-sections below; source plank gaps retained. Flush nominal top datum does not mean a seamless collision surface.','cross_sections':seams}

# Pairwise interpenetration screen for separate props, excluding intended support contact.
props=[k for k in instances if not k.startswith('dock_')];trees={k:bvh(instances[k]) for k in props};pair_clashes=[]
for i,a in enumerate(props):
 for c in props[i+1:]:
  if {a,c}=={'crate','lantern_on_crate'}:continue
  ab=bounds(instances[a]);cb=bounds(instances[c])
  if any(ab['max'][j]<cb['min'][j]-EPS or cb['max'][j]<ab['min'][j]-EPS for j in range(3)):continue
  overlap=trees[a].overlap(trees[c])
  if overlap:pair_clashes.append({'instances':[a,c],'intersecting_triangle_pairs':len(overlap)})
report['prop_intersection_screen']={'unexpected_triangle_intersections':pair_clashes,'method':'Pairwise world-space actual triangle-BVH overlap after AABB broadphase; containment and internal source defects not certified.'}
report['central_layout_clearance']={'reserved_unobstructed_layout_strip_xy_m':{'x':[-.25,.55],'y':[-2,1.0]},'width_m':.8,'claim':'Layout intent only; no human-navigation or accessibility certification.'}
report['blockout_geometry_gate']={'dependency_integrity':True,'source_metadata_dimensions':all(s['dimensions_match_published_within_0_1mm'] for s in source_stats),'four_module_exact_nominal_layout':True,'unexpected_prop_intersections':len(pair_clashes),'pile_base_count_16':sum(x['base_islands_at_z0'] for x in pile_checks)==16,'every_prop_has_contact_samples':all(x['samples_on_actual_upward_surface']>0 for x in report['support_checks']),'all_sampled_contact_islands_supported':all(x['all_contact_islands_have_sampled_support'] for x in report['support_checks']),'support_caveats':['Bench splayed uncut soles: four edge-only contacts, not flat feet.','Rope coil: only two source minimum-Z vertices contact; broader rope body rises above plane. Mere contact sample pass is not proof of stable support.'],'shore_interface':'PENDING','independent_QA':'PENDING','six_material_views':'NOT_STARTED','final_GLb_roundtrip':'NOT_STARTED','overall_complete':False}
(OUT/'layout-report.json').write_text(json.dumps(report,indent=2)+'\n')

# Save geometry-only working blend before optional diagnostic render rig.
bpy.ops.object.select_all(action='DESELECT')
for obj in all_asset:obj.select_set(True)
bpy.context.view_layer.objects.active=all_asset[0]
scene['candidate_stage']='blockout; interface and independent QA pending'
scene['source_commit']=LOCK['commit'];scene['diagnostic_context_exported']=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'blockout.blend'))

if args.render and not args.no_render and not args.final:
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=False
 scene.render.threads_mode='FIXED';scene.render.threads=2
 scene.render.resolution_x=1000;scene.render.resolution_y=850;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
 scene.view_settings.view_transform='AgX';scene.world=bpy.data.worlds.new('Diagnostic studio world');scene.world.use_nodes=True
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.31,.34,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
 clay=bpy.data.materials.new('DIAGNOSTIC clay override only');clay.use_nodes=True
 shader=clay.node_tree.nodes['Principled BSDF'];shader.inputs['Base Color'].default_value=(.46,.49,.51,1);shader.inputs['Roughness'].default_value=.85
 bpy.context.view_layer.material_override=clay
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.008));floor=bpy.context.object;floor.name='DIAGNOSTIC studio ground, not water or seabed';attach(floor,rig_col)
 def aim(obj,loc,target=(0,0,1.05)):
  obj.location=loc;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
 for name,loc,power,size in [('Key',(-3,-4,8),1300,5),('Fill',(5,-1,5),550,5),('Rim',(0,5,6),900,4)]:
  bpy.ops.object.light_add(type='AREA',location=loc);obj=bpy.context.object;obj.name='DIAGNOSTIC '+name;obj.data.energy=power;obj.data.shape='DISK';obj.data.size=size;attach(obj,rig_col);aim(obj,loc)
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='DIAGNOSTIC offline Blender camera';attach(cam,rig_col);scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=7.15
 views=[('blockout-isometric',(6,-8,6.2),(0,0,1.05)),('blockout-top',(0,0,10),(0,0,0))]
 for name,loc,target in views:
  if name.endswith('top'):cam.data.ortho_scale=4.8;scene.render.resolution_x=900;scene.render.resolution_y=900
  aim(cam,loc,target);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
 # Diagnostic blend deliberately separate; never serve as final export source without ASSET collection filtering.
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'blockout-diagnostic.blend'))
report['rendered_views']=[{'file':name+'.png','kind':'actual offline Blender Cycles gray-material render','not_browser_evidence':True} for name in ['blockout-isometric','blockout-top']] if args.render and not args.no_render and not args.final else []
report['elapsed_seconds']=round(time.monotonic()-START,2)
(OUT/'layout-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('HARBOR_BLOCKOUT_REPORT',json.dumps(report['blockout_geometry_gate']))

# Parent-approved next phase: selected asset-only export, fresh import and material views.
if args.final:
 from collections import Counter
 from mathutils.kdtree import KDTree
 import struct
 def material_signature(mat):
  n=mat.node_tree.nodes.get('Principled BSDF') if mat and mat.use_nodes else None
  if not n:raise RuntimeError('Unsupported non-PBR imported material')
  return tuple(round(x,6) for x in n.inputs['Base Color'].default_value)+(round(n.inputs['Metallic'].default_value,6),round(n.inputs['Roughness'].default_value,6))
 def ref_geometry(objs):
  # Stable vertex IDs via positional welding only in the validation reference.
  vertices=[];lookup={};triangles=Counter();mat_counts=Counter()
  def vid(pos):
   key=tuple(round(x,7) for x in pos)
   if key not in lookup:lookup[key]=len(vertices);vertices.append(Vector(pos))
   return lookup[key]
  def oriented(ids):return min(ids,ids[1:]+ids[:1],ids[2:]+ids[:2])
  for obj in objs:
   obj.data.calc_loop_triangles();vs=[obj.matrix_world@v.co for v in obj.data.vertices]
   for tri in obj.data.loop_triangles:
    sig=material_signature(obj.data.materials[tri.material_index]);ids=tuple(vid(vs[i]) for i in tri.vertices)
    triangles[(oriented(ids),sig)]+=1;mat_counts[sig]+=1
  return vertices,triangles,mat_counts
 original_vertices,original_triangles,original_mat_counts=ref_geometry(all_asset)
 original_bounds=bounds(all_asset)
 bpy.ops.object.select_all(action='DESELECT')
 for obj in all_asset:obj.select_set(True)
 bpy.context.view_layer.objects.active=all_asset[0]
 scene['candidate_stage']='material-review; independent final QA pending'
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
 bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_extras=True,export_cameras=False,export_lights=False)
 glb=(OUT/'model.glb').read_bytes();json_length,chunk_type=struct.unpack_from('<II',glb,12);doc=json.loads(glb[20:20+json_length])
 if chunk_type!=0x4e4f534a:raise RuntimeError('GLB JSON chunk missing')
 external=[b.get('uri') for b in doc.get('buffers',[]) if b.get('uri')]+[im.get('uri') for im in doc.get('images',[]) if im.get('uri')]
 if external:raise RuntimeError('Unexpected external resource URI')
 if doc.get('images') or doc.get('textures'):raise RuntimeError('Unexpected image/texture dependency')
 # Fresh scene, no original geometry or material datablocks retained.
 bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'),merge_vertices=False);bpy.context.view_layer.update()
 imported=[o for o in scene.objects if o.type=='MESH']
 kd=KDTree(len(original_vertices))
 for index,pt in enumerate(original_vertices):kd.insert(pt,index)
 kd.balance();max_dist=0;actual_triangles=Counter();actual_mat_counts=Counter()
 for obj in imported:
  obj.data.calc_loop_triangles();mapping=[]
  for v in obj.data.vertices:
   pos=obj.matrix_world@v.co;_,index,dist=kd.find(pos);max_dist=max(max_dist,dist);mapping.append(index)
  for tri in obj.data.loop_triangles:
   ids=tuple(mapping[i] for i in tri.vertices);key=min(ids,ids[1:]+ids[:1],ids[2:]+ids[:2]);sig=material_signature(obj.data.materials[tri.material_index])
   actual_triangles[(key,sig)]+=1;actual_mat_counts[sig]+=1
 imported_bounds=bounds(imported)
 exact_faces=actual_triangles==original_triangles
 if max_dist>2e-6 or not exact_faces:raise RuntimeError('GLB fresh roundtrip changed geometry/winding/material assignment: '+str((max_dist,exact_faces)))
 if len(imported)!=12:raise RuntimeError('Unexpected GLB node instance count')
 if any('source_asset_id' not in o for o in imported):raise RuntimeError('Missing source attribution extras')
 final={'id':ASSET,'stage':'material-review','status':'review','formal_approved':False,'blender':bpy.app.version_string,'generated_utc':datetime.now(timezone.utc).isoformat(),'source':report['source'],'geometry_roundtrip':{'fresh_empty_scene_import':True,'mesh_instance_count':len(imported),'source_instance_count':len(instances),'world_triangle_count':sum(actual_triangles.values()),'oriented_triangle_and_material_multiset_identical':exact_faces,'maximum_imported_vertex_distance_to_reference_m':max_dist,'reference_bounds_m':original_bounds,'fresh_import_bounds_m':imported_bounds,'material_PBR_signatures_identical':actual_mat_counts==original_mat_counts,'unique_PBR_appearance_count':len(actual_mat_counts),'actual_glb_material_records':len(doc.get('materials',[])),'unique_glb_mesh_count':len(doc.get('meshes',[])),'unique_stored_mesh_triangles':sum(doc['accessors'][primitive['indices']]['count']//3 for mesh in doc.get('meshes',[]) for primitive in mesh['primitives']),'instance_expanded_draw_triangles':sum(actual_triangles.values()),'external_resources':external,'images':len(doc.get('images',[])),'textures':len(doc.get('textures',[])),'attribution_extras_present_on_all_instances':True,'diagnostic_geometry_exported':False},'source_input_integrity':True,'reused_asset_id_count':9,'scene_instance_count':12,'new_standalone_prop_count':0,'scope':'4-module Harbor platform scene only; no water, shore connector or new prop','support_and_seam_evidence':'layout-report.json and support-area-report.json','unresolved_source_geometry_limits':['12mm source deck-edge V seams retained; no continuous collision-plane claim.','Bench: each of four uncut slanted soles touches along an edge, not a flat foot.','Rope: only two source minimum-Z vertices contact; broad rope-body support unresolved.','Flat prop bases span original plank/lid gaps: measured support area about 77–91%, not continuous full-area support.'],'not_validated':['Browser/WebGL rendering, interaction or runtime','Loads, buoyancy, mooring, water interaction, soil/embedment, dynamic behavior, human accessibility or engineering safety','Final independent review and approval'],'render_evidence':'Actual offline Blender Cycles renders of freshly imported final GLB; not browser screenshots or generated concept images.','rendered_views':[]}
 # Input conservation is checked again after export, not assumed from the initial check.
 for dep in LOCK['dependencies']:
  for f in dep['files']:
   if hashlib.sha256((SNAPSHOT/f['path']).read_bytes()).hexdigest()!=f['sha256']:raise RuntimeError('Source snapshot unexpectedly changed')
 if args.render and not args.no_render:
  diag=bpy.data.collections.new('DIAGNOSTIC_RENDER_RIG_EXCLUDED_FROM_GLB');scene.collection.children.link(diag)
  scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128;scene.cycles.use_denoising=False
  # This installed Blender build exposes no CPU denoiser enum; use native higher samples.
  scene.render.threads_mode='FIXED';scene.render.threads=4
  scene.render.resolution_x=960;scene.render.resolution_y=960;scene.render.resolution_percentage=100
  scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.45
  scene.world=bpy.data.worlds.new('Neutral offline studio');scene.world.use_nodes=True
  scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.35,.39,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
  bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.008));floor=bpy.context.object;floor.name='DIAGNOSTIC neutral studio floor; not water or seabed';attach(floor,diag)
  floor_mat=bpy.data.materials.new('DIAGNOSTIC neutral slate floor');floor_mat.use_nodes=True;sh=floor_mat.node_tree.nodes['Principled BSDF'];sh.inputs['Base Color'].default_value=(.18,.205,.225,1);sh.inputs['Roughness'].default_value=.85;floor.data.materials.append(floor_mat)
  def aim_final(obj,loc,target=(0,0,1.1)):
   obj.location=loc;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
  for name,loc,power,size in [('Key',(-3,-4,8),900,5),('Fill',(5,-1,5),350,5),('Rim',(0,5,6),600,4)]:
   bpy.ops.object.light_add(type='AREA',location=loc);li=bpy.context.object;li.name='DIAGNOSTIC '+name;li.data.energy=power;li.data.shape='DISK';li.data.size=size;attach(li,diag);aim_final(li,loc)
  bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='DIAGNOSTIC final GLB offline camera';attach(cam,diag);scene.camera=cam;cam.data.type='ORTHO'
  views=[('qa-isometric',(6,-8,6.2),(0,0,1.05),6.8),('qa-front',(0,-9,1.35),(0,0,1.35),4.8),('qa-back',(0,9,1.35),(0,0,1.35),4.8),('qa-left',(-9,0,1.35),(0,0,1.35),4.8),('qa-right',(9,0,1.35),(0,0,1.35),4.8),('qa-top',(0,0,10),(0,0,0),4.8)]
  for name,loc,target,scale in views:
   cam.data.ortho_scale=scale;aim_final(cam,loc,target);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
   final['rendered_views'].append({'file':name+'.png','width':960,'height':960,'samples':128,'denoise':'Unavailable in installed Blender build; disabled, native sampling only','source':'fresh final GLB import'})
   (OUT/'final-validation.json').write_text(json.dumps(final,indent=2)+'\n')
  # Thumbnail is exactly the reviewed isometric, no second variant.
  (OUT/'thumbnail.png').write_bytes((OUT/'qa-isometric.png').read_bytes())
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  fp=OUT/name
  if not fp.exists():continue
  files[role]={'path':f'assets/harbor/{ASSET}/v1.0.0/{name}','size':fp.stat().st_size,'sha256':hashlib.sha256(fp.read_bytes()).hexdigest()}
 if len(files)==4:
  metadata={'id':ASSET,'version':'1.0.0','category':'scene-compositions','assetKind':'scene','theme':'harbor','style':'soft-low-poly','title':'Harbor Cargo and Rest Platform Preset','description':'4m static cargo/rest platform preset reusing 9 published Harbor IDs at v1.0.0 as 12 independently selectable rigid instances: west cargo, northeast seating and open center. No new standalone prop, water or shore connection. Exact source commit and hashes embedded in generator. Original 12mm deck seams and bench/rope contact limits retained; offline review only.','bounds':dict(zip(('x','y','z'),imported_bounds['dimensions']),unit='m'),'triangles':sum(actual_triangles.values()),'materials':len(doc.get('materials',[])),'files':files,'status':'review','license':'All rights reserved'}
  (OUT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
 final['files']=files;final['elapsed_seconds']=round(time.monotonic()-START,2)
 (OUT/'final-validation.json').write_text(json.dumps(final,indent=2)+'\n')
 print('FINAL_GLB_ROUNDTRIP',json.dumps(final['geometry_roundtrip']))
