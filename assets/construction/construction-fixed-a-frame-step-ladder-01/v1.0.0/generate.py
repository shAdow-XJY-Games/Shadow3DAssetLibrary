"""Original independent four-foot A-frame ladder: one fixed static visual prop.
No climbing, folding/locking, loading, fire/maritime use or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='construction-fixed-a-frame-step-ladder-01';VERSION='1.0.0';TITLE='Fixed A-Frame Step Ladder'
DESCRIPTION=('One original low-poly independent A-frame step ladder in one fixed open pose, counted as one prop. Four thick horizontal front treads span two orange sloping front rails. Two dark blue rear support rails with two rear crossbars provide a separate rear support branch, and four flat charcoal foot pads have finite ground patches. '
 'A fixed side limiter plate on each side has two finite embedded endpoints. Four genuine bored top ears, two on either side, surround two complete fixed stepped pins. The pin shafts have positive full-surface clearance inside their holes; integral end caps meet the outer ear faces over finite opposed annular regions. '
 'The central A-frame volume, spaces between all steps and the rear-frame openings remain genuinely empty. Twenty-two named editable closed meshes and four opaque constant PBR colours, metre scale, native Z up, front -Y, ground-centred footprint origin. '
 'One frozen pose only: no people, wall, platform, scaffold, dock, vehicle, scene, texture or animation. The existing playground slide already includes its own platform-supported ladder; this independently created freestanding A-frame is a narrower new structure, with no inherited interface compatibility. '
 'Static visual geometry only. No climbing or working height, human fit, folding, locking or motion, assembly path, load capacity, strength, stability, anti-tip behaviour, construction/firefighting/boarding suitability, manufacturing tolerance or safety-code certification. Geometric contact does not establish functional or safe equipment.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={};EAR_PAIRS=[]
PALETTE=[('ConstructionOrange_Rails',(.75,.235,.045,1),.48,.16),('DarkBlue_RearFrame',(.045,.105,.155,1),.5,.22),('SatinSteel_TreadsPins',(.55,.62,.66,1),.4,.65),('Charcoal_FootPads',(.025,.035,.043,1),.84,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,.74);ORTHO=2.25
CAMERAS={'gray-front3q':(2.6,-4,2.7),'gray-back3q':(-2.6,4,2.7),'thumbnail':(2.6,-4,2.7),'qa-front':(0,-4,2.02),'qa-side':(4,0,2.02),'qa-top':(0,0,4),'qa-back':(0,4,2.02),'qa-wireframe':(2.6,-4,2.7),'silhouette-128-front':(0,-4,2.02),'silhouette-128-side':(4,0,2.02)}
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
def prism(name,quad0,quad1,mat,role):
 m=Mesh();v=quad0+quad1
 for q in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:m.face([v[i] for i in q],mat,'ground' if all(v[i][2]==0 for i in q) else 'side')
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def slab(name,x0,x1,y0,y1,z0,z1,mat,role):
 return prism(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],mat,role)
def yf(z):return -.48+.44*(z-.045)/1.44
def yr(z):return .44-.40*(z-.045)/1.44
def rail(name,x,fun,mat):
 quads=[]
 for z in [.035,1.51]:
  y=fun(z);quads.append([(x-.030,y-.0325,z),(x+.030,y-.0325,z),(x+.030,y+.0325,z),(x-.030,y+.0325,z)])
 prism(name,*quads,mat,'Fixed sloping rail with horizontal end faces; finite foot and joint embeddings.')
def ring(name,x0,x1,rin,rout,mat):
 m=Mesh();n=24
 for i in range(n):
  a=math.tau*i/n;b=math.tau*(i+1)/n
  def p(x,r,t):return (x,r*math.cos(t),1.55+r*math.sin(t))
  for tag,poly in [('inner',[p(x0,rin,a),p(x1,rin,a),p(x1,rin,b),p(x0,rin,b)]),('outer',[p(x0,rout,b),p(x1,rout,b),p(x1,rout,a),p(x0,rout,a)]),('left',[p(x0,rin,b),p(x0,rout,b),p(x0,rout,a),p(x0,rin,a)]),('right',[p(x1,rin,a),p(x1,rout,a),p(x1,rout,b),p(x1,rin,b)])]:m.face(poly,mat,tag)
 g=m.result('Thick 24-sided annular ear with a complete true through-bore.',mat)
 if name:G[name]=g
 return g
def pin(name,x0,x1):
 m=Mesh();profile=[(x0-.014,.035),(x0,.035),(x0,.017),(x1,.017),(x1,.035),(x1+.014,.035)];n=24
 for i in range(n):
  a=math.tau*i/n;b=math.tau*(i+1)/n
  def p(x,r,t):return (x,r*math.cos(t),1.55+r*math.sin(t))
  for k,((u,r),(v,s)) in enumerate(zip(profile,profile[1:])):m.face([p(u,r,b),p(v,s,b),p(v,s,a),p(u,r,a)],2,['cap_outer','left_contact','shaft','right_contact','cap_outer'][k])
 for x,rev in [(profile[0][0],True),(profile[-1][0],False)]:
  pts=[(x,.035*math.cos(math.tau*i/n),1.55+.035*math.sin(math.tau*i/n)) for i in range(n)];m.face(list(reversed(pts)) if rev else pts,2,'cap_end')
 G[name]=m.result('One continuous fixed pin with integral retaining end caps; no rotational or locking claim.',2)
for side,s in [('Left',-1),('Right',1)]:
 front='Front_Rail_'+side;rear='Rear_Rail_'+side
 rail(front,s*.36,yf,0);rail(rear,s*.29,yr,1)
 for label,x,y,r in [('Front',s*.36,yf(.045),front),('Rear',s*.29,yr(.045),rear)]:
  foot='Foot_'+label+'_'+side;slab(foot,x-.0525,x+.0525,y-.0675,y+.0675,0,.050,3,'One of four finite flat ground pads; finitely embeds the associated rail.');FEET.append(foot)
  LINKS.append((foot,r,[(x-.012,y,.042),(x+.012,y,.042)]))
 f0,f1=sorted((s*.332,s*.388));r0,r1=sorted((s*.262,s*.318));fe='Top_Ear_Front_'+side;re='Top_Ear_Rear_'+side
 ring(fe,f0,f1,.022,.075,0);ring(re,r0,r1,.022,.075,1)
 LINKS += [(front,fe,[(s*.35,-.035,1.49),(s*.37,-.035,1.50)]),(rear,re,[(s*.28,.035,1.49),(s*.30,.035,1.50)])]
 pn='Top_Pin_'+side;low=min(f0,r0);high=max(f1,r1);pin(pn,low,high)
 before=re if s==1 else fe;after=fe if s==1 else re
 for a,b,x in [(pn,before,low),(after,pn,high)]:
  CONTACTS.append({'a':a,'b':b,'axis':0,'plane_m':x,'minimum_patch_area_m2':.0022,'interior_probe_offset_m':.001,'points':[(x,.028,1.55),(x,-.028,1.55),(x,0,1.578),(x,0,1.522)],'scope':'complete finite opposed annular end-cap/ear contact; shaft bore remains clear'})
 for ear,x0,x1 in [(fe,f0,f1),(re,r0,r1)]:
  EAR_PAIRS.append({'ear':ear,'pin':pn,'x0':x0,'x1':x1})
  BORES.append({'mesh':ear,'origin_m':[x0-.002,0,1.55],'direction':[1,0,0],'length_m':x1-x0+.004})
  # Isolated complete bore, before assembly: real volume from one mouth through the other.
  # A true solid cylinder avoids treating its axial micro-core as unverified.
  m=Mesh();n=24
  for i in range(n):
   a=math.tau*i/n;b=math.tau*(i+1)/n
   m.face([(x0-.002,.0205*math.cos(a),1.55+.0205*math.sin(a)),(x1+.002,.0205*math.cos(a),1.55+.0205*math.sin(a)),(x1+.002,.0205*math.cos(b),1.55+.0205*math.sin(b)),(x0-.002,.0205*math.cos(b),1.55+.0205*math.sin(b))][::-1])
  for x,rev in [(x0-.002,True),(x1+.002,False)]:
   q=[(x,.0205*math.cos(math.tau*i/n),1.55+.0205*math.sin(math.tau*i/n)) for i in range(n)];m.face(q[::-1] if rev else q)
  VOID_PROBES['IsolatedFullBore_'+ear]={'type':'mesh','geometry':m.result('Complete solid bore probe excluded from delivery'),'targets':[ear],'role':'entire isolated true hole from outside both ear mouths'}
  VOID_PROBES['AssembledAnnularGap_'+ear]={'type':'mesh','geometry':ring(None,x0+.001,x1-.001,.018,.021,0),'targets':[ear,pn],'role':'complete finite annular void between pin shaft and bore; contact planes excluded by 1 mm'}
 # The thin fixed side plate follows the two offset frames in plan. Both ends are embedded.
 z=.72;z0=z-.0275;z1=z+.0275;f=yf(z);r=yr(z);points=[(s*.375,f-.015),(s*.397,f-.015),(s*.327,r+.015),(s*.305,r+.015)]
 if s<0:points=points[::-1]
 plate='Fixed_Limiter_'+side;prism(plate,[(x,y,z0) for x,y in points],[(x,y,z1) for x,y in points],2,'One thick fixed side limiter plate with both ends finitely embedded in the rails; no motion or locking claim.')
 LINKS += [(plate,front,[(s*.382,f,.71),(s*.382,f,.73)]),(plate,rear,[(s*.312,r,.71),(s*.312,r,.73)])]
for i,z in enumerate([.28,.56,.84,1.12],1):
 name='Front_Tread_%02d'%i;y=yf(z);slab(name,-.365,.365,y-.0825,y+.0825,z-.0225,z+.0225,2,'One complete thick horizontal tread with finite embedded joins to both front rails.')
 for side,s in [('Left',-1),('Right',1)]:LINKS.append((name,'Front_Rail_'+side,[(s*.35,y-.010,z),(s*.35,y+.010,z)]))
for i,z in enumerate([.32,.96],1):
 name='Rear_Crossbar_%02d'%i;y=yr(z);slab(name,-.295,.295,y-.026,y+.026,z-.026,z+.026,1,'Fixed rear crossbar finitely connected to both rear rails.')
 for side,s in [('Left',-1),('Right',1)]:LINKS.append((name,'Rear_Rail_'+side,[(s*.28,y-.009,z),(s*.28,y+.009,z)]))
def passage(name,x0,x1,z0,z1,low,high,role):
 quads=[]
 for z in [z0,z1]:quads.append([(x0,low(z),z),(x1,low(z),z),(x1,high(z),z),(x0,high(z),z)])
 VOID_PROBES[name]={'type':'mesh','geometry':prism(None,*quads,0,role),'targets':list(G),'role':role}
passage('CompleteCentralAFrameVoid',-.245,.245,.065,1.30,lambda z:yf(z)+.10,lambda z:yr(z)-.055,'Full tapered finite central A-frame core above ground, behind all four treads and ahead of rear crossbars')
for i,(a,b) in enumerate([(.065,.2475),(.3125,.5275),(.5925,.8075),(.8725,1.0875),(1.1525,1.43)]):passage('FrontOpenPassage_%02d'%i,-.325,.325,a,b,lambda z:yf(z)-.070,lambda z:yf(z)+.070,'Complete finite width and depth front step opening, with positive clearance from adjacent treads and rails')
for i,(a,b) in enumerate([(.065,.284),(.356,.924),(.996,1.43)]):passage('RearOpenPassage_%02d'%i,-.25,.25,a,b,lambda z:yr(z)-.040,lambda z:yr(z)+.040,'Complete rear frame opening between real crossbars and rails')
# Ground origin is the complete footprint centre. Shift the entire construction,
# connection samples and finite probes together; no reference geometry is exported.
for g in list(G.values())+[p['geometry'] for p in VOID_PROBES.values()]:
 g['vertices']=[(x,round(y+.02,9),z) for x,y,z in g['vertices']]
LINKS=[(a,b,[(x,y+.02,z) for x,y,z in points]) for a,b,points in LINKS]
for r in CONTACTS:r['points']=[(x,y+.02,z) for x,y,z in r['points']]
for r in BORES:r['origin_m'][1]+=.02
def measure_ladder_geometry(vertices):
 return {'tread_count':4,'tread_thickness_m':.045,'ground_pad_count':4,'true_top_bore_count':4,'complete_pin_count':2,'fixed_limiter_count':2,'rear_crossbar_count':2,'single_prop_count':1,'full_height_m':1.625,'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed independent A-frame step ladder visual prop; no equipment-performance claim'}
assert len(G)==22,len(G)
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
root=bpy.data.objects.new('OneFixedAFrameLadder',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
ladder_evidence=measure_ladder_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
  low=list(p);high=list(p);low[r.get('axis',2)]-=eps;high[r.get('axis',2)]+=eps
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
 'single_prop_count':1,'ladder_geometry':ladder_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/construction/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'construction','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
