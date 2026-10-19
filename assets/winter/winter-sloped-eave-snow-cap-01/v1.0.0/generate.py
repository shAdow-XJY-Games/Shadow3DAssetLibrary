"""Original thick sloped eave snow cap with a continuous blunt hanging lip; one prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='winter-sloped-eave-snow-cap-01';VERSION='1.0.0';TITLE='Sloped Eave Snow Cap'
DESCRIPTION=('One original closed thick low-poly snow cap with a broad gently uneven sloped upper blanket and a continuous rounded downturned front lip, one static prop and one editable monolithic mesh. Its complete finite underside attachment rectangle lies on source z=0.80+0.40y m, x=[-0.95,0.95] m, y=[0.02,0.72] m; the roof rises 0.40 m per metre toward +Y, slope 21.801409 degrees. The outward underside normal is (0,0.371391,-0.928477); the required matching support has the opposite normal. The source origin (0,0,0) is a design datum, not ground contact. All asset vertices lie on or above the declared sloped support plane. The continuous snow lip extends toward -Y outside the bounded contact patch and hangs below its front elevation. An external matching sloped support is required; the temporary QA support never enters the asset, native scene or formal images. Three opaque constant PBR snow colours; no texture, transmission, scene, house, roof, animation or variants. Metres, source Z up, front -Y. '
 'Static stylised appearance only: no snow or ice material physics, melting, sliding, climate or weather simulation, snow load, adhesion, stability, structural or human safety, manufacture or construction/installation claim. No previous cottage or shop-house tile-roof fit, universal eave interface, arbitrary roof pitch, seamless repetition or length compatibility is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[]
PALETTE=[('Snow_Upper',(.83,.90,.94,1),.88,0),('Snow_SoftFacet',(.72,.82,.88,1),.90,0),('Snow_ShadedUnderside',(.49,.65,.74,1),.94,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled snow colours; no texture nodes or linked inputs, no transmission.'
FOCUS=(0,.18,1.015);ORTHO=3.00
CAMERAS={'gray-front3q':(2.7,-4.1,2.8),'gray-back3q':(-2.9,4.0,2.5),'thumbnail':(2.7,-4.1,2.8),'qa-front':(0,-5,1.40),'qa-side':(5,.18,1.5),'qa-top':(0,.18,5.5),'qa-back':(0,5,1.50),'qa-wireframe':(2.7,-4.1,2.8),'silhouette-128-front':(0,-5,1.40),'silhouette-128-side':(5,.18,1.5)}
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

SLOPE=.40;BASE=.80;PLANE_NORMAL_UP=(0,-SLOPE/math.sqrt(1+SLOPE*SLOPE),1/math.sqrt(1+SLOPE*SLOPE))
X_STATIONS=[-1.10,-.90,-.65,-.36,-.10,.18,.47,.74,.95,1.10]
UPPER_VARIATION=[-.045,.013,.034,-.009,.024,.045,.012,-.012,.014,-.042]
LIP_VARIATION=[.025,.008,-.012,.015,-.008,-.020,.012,-.008,.009,.027]
# Each YZ cross-section is a closed substantial snow body: support-back,
# rounded rear shoulder, broad upper blanket, rounded outer roll, underside,
# and planar support-front. New geometry; no prior snowbank or ice mesh is used.
SECTION_BASE=[(.78,1.112),(.83,1.225),(.70,1.340),(.40,1.300),(.07,1.140),(-.24,1.060),(-.40,.920),(-.41,.790),(-.31,.710),(-.18,.770),(0,.800)]
SECTIONS=[]
for x,up,lip in zip(X_STATIONS,UPPER_VARIATION,LIP_VARIATION):
 ring=[]
 for j,(y,z) in enumerate(SECTION_BASE):
  dz=0 if j in [0,10] else (up if j in [1,2,3,4] else lip if j in [6,7,8,9] else (up+lip)/2)
  ring.append((x,y,z+dz))
 SECTIONS.append(ring)
# A small deterministic ear clipper is used only for the two concave end caps.
def ear_triangles(ring):
 ids=list(range(len(ring)));out=[]
 def area(a,b,c):return (b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1])
 def contains(a,b,c,p):return min(area(a,b,p),area(b,c,p),area(c,a,p))>=-1e-12
 while len(ids)>3:
  found=False
  for k,b in enumerate(ids):
   a,c=ids[k-1],ids[(k+1)%len(ids)]
   if area(ring[a],ring[b],ring[c])<=1e-12:continue
   if any(contains(ring[a],ring[b],ring[c],ring[v]) for v in ids if v not in [a,b,c]):continue
   out.append([ring[a],ring[b],ring[c]]);ids.pop(k);found=True;break
  assert found,'End cap ear clipping failed'
 out.append([ring[i] for i in ids]);return out
m=Mesh()
for i,(left,right) in enumerate(zip(SECTIONS,SECTIONS[1:])):
 for j in range(len(left)):
  k=(j+1)%len(left)
  if j==10:tag='finite_planar_support';material=2
  elif j in [1,2,3,4]:tag='cap_top_'+str(j);material=0 if (i+j)%4 else 1
  elif j in [5,6,7,8,9]:tag='continuous_front_lip_'+str(j);material=1 if j in [5,6] else 2
  else:tag='rounded_rear_edge';material=1
  m.face([left[j],left[k],right[k],right[j]],material,tag)
for tri in ear_triangles(SECTIONS[0]):m.face(tri[::-1],1,'left_closed_end')
for tri in ear_triangles(SECTIONS[-1]):m.face(tri,1,'right_closed_end')
NAME='Snow_ContinuousCapAndRoundedEaveLip'
G[NAME]=m.result('One closed connected thick sloped snow cap with a continuous rounded downturned lip, closed end caps and a finite planar underside support patch.')
ATTACHMENT={'plane_equation':'z=0.80+0.40*y','slope_rise_per_run':SLOPE,'slope_angle_degrees':math.degrees(math.atan(SLOPE)),'outward_normal':[0,-PLANE_NORMAL_UP[1],-PLANE_NORMAL_UP[2]],'x_range_m':[-.95,.95],'y_range_m':[.02,.72],'area_m2':1.9*.70*math.sqrt(1+SLOPE*SLOPE),'role':'whole finite sloped underside patch; external matching roof support required; no ground contact'}
QA_SUPPORT={'x_range_m':[-.95,.95],'y_range_m':[.02,.72],'top_base_m':BASE,'top_slope':SLOPE,'vertical_depth_m':.16,'asset_member':False,'role':'temporary bounded closed sloped support witness only, excluded from asset and formal images'}
ROOT_INTERIOR_PROBES=[{'name':'whole_width_continuous_front_lip_bridge','lo_m':[-1.02,-.035,.845],'hi_m':[1.02,.035,.895]}]
# This complete closed under-eave void follows every actual lower strip segment
# across the entire asset width, 12mm below it, rather than testing a few rays.
VOID_Y=[-.405,-.31,-.18,-.015];VOID_FLOOR=.18;VOID_CLEARANCE=.012
VOID_TOP=[]
for ring in SECTIONS:
 lower=[ring[j] for j in [7,8,9,10]];row=[]
 for y in VOID_Y:
  for a,b in zip(lower,lower[1:]):
   if a[1]-1e-10<=y<=b[1]+1e-10:
    u=(y-a[1])/(b[1]-a[1]);z=a[2]+u*(b[2]-a[2]);row.append((a[0],y,z-VOID_CLEARANCE));break
 assert len(row)==len(VOID_Y);VOID_TOP.append(row)
vm=Mesh()
for i in range(len(X_STATIONS)-1):
 for j in range(len(VOID_Y)-1):
  a,b,c,d=VOID_TOP[i][j],VOID_TOP[i+1][j],VOID_TOP[i+1][j+1],VOID_TOP[i][j+1]
  vm.face([a,b,c,d],0,'void_top')
  vm.face([(a[0],a[1],VOID_FLOOR),(d[0],d[1],VOID_FLOOR),(c[0],c[1],VOID_FLOOR),(b[0],b[1],VOID_FLOOR)],0,'void_floor')
for side in [0,len(X_STATIONS)-1]:
 for a,b in zip(VOID_TOP[side],VOID_TOP[side][1:]):
  q=[(a[0],a[1],VOID_FLOOR),(b[0],b[1],VOID_FLOOR),b,a];vm.face(q if side else q[::-1],0,'void_end')
for j in [0,len(VOID_Y)-1]:
 for i in range(len(X_STATIONS)-1):
  a,b=VOID_TOP[i][j],VOID_TOP[i+1][j];q=[(a[0],a[1],VOID_FLOOR),a,b,(b[0],b[1],VOID_FLOOR)];vm.face(q if j else q[::-1],0,'void_outer')
VOID_PROBES={'FullWidthProfiledUnderEaveVoid':dict(vm.result('Whole closed empty under-eave witness, follows actual underside across all X stations, not exported.'),asset_member=False)}
def measure_eave_snow_geometry(vertices):
 v=vertices[NAME];ext=lambda axis:max(p[axis] for p in v)-min(p[axis] for p in v)
 return {'single_prop_count':1,'mesh_count':len(G),'span_m':[ext(i) for i in range(3)],'attachment':ATTACHMENT,'qa_support':QA_SUPPORT,'finite_whole_width_bridge_count':1,'complete_profiled_under_eave_void_count':1,'cross_sections':len(SECTIONS),'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed static externally supported sloped-eave snow attachment; no house or standalone ground/load claim'}
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
root=bpy.data.objects.new('OneContinuousSlopedEaveSnowCap',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Source design datum (0,0,0), no ground contact; finite sloped underside z=0.80+0.40y, external matching support required; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# The asset is one monolithic sloped-eave attachment. No stand, roof or ground is exported.
assert len(parts)==1
eave_snow_evidence=measure_eave_snow_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds=[round(hi[i]-lo[i],6) for i in range(3)]
assert lo[2]>.04 and triangles<12000
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
 'components':component_checks,'single_prop_count':1,'eave_snow_geometry':eave_snow_evidence,'attachment_datum':ATTACHMENT,'temporary_support_exported':False,'ground_contact_claimed':False,
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/winter/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'winter','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.11,.17,.21,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g);ground.hide_render=True
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
