"""Original low round and rounded-triangular beakers; one static visual prop.
Each independently authored polygon shell is closed and continuous across its
outer bottom, wall, extended open pour lip, inner wall and real inner floor.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laboratory-round-and-triangular-beaker-kit-01';VERSION='1.0.0';TITLE='Round and Triangular Beaker Kit'
DESCRIPTION=('One original static pair of opaque thick-walled beaker forms, counted as one prop: a low wide round straight-sided beaker with a broad V-shaped pouring notch and a taller tapered rounded-triangular beaker whose front corner extends into a pouring lip. Each mouth, lip, inner wall, thick complete bottom and outer wall belongs to one continuous connected closed shell. Three short solid illustrative ticks are finitely embedded in the round exterior. Both complete flat bases rest on ground, with full separation between the two beakers. Four opaque unlinked constant PBR materials; metres, native Z up, front -Y and horizontal bounds-centred ground origin. No separate foot ring, handle, lid, liquid, transparent surface, numbers, units, logos or scene. Both different cross sections are authored from new polygon geometry, not resized cylinders, pitchers without handles, old bowls or colour variants. Static visual appearance only: no volume value, calibrated graduation, measurement accuracy, glass or refraction, pouring or fluid simulation, chemical, temperature, laboratory procedure, material performance, hygiene, human fit, manufacture or laboratory safety certification claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={};MARKS=[]
ROUND='RoundBeaker_ContinuousLowStraightShell';TRIANGLE='TriangularBeaker_ContinuousTaperedShell';BODIES=[ROUND,TRIANGLE];FEET=BODIES[:]
PALETTE=[('RoundBody_Seafoam',(.23,.48,.44,1),.40,0),('TriangleBody_SlateBlue',(.17,.30,.40,1),.42,0),('WarmCream_InnerWalls',(.77,.72,.59,1),.53,0),('DarkSlate_IllustrativeTicks',(.025,.075,.10,1),.45,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no procedural or image textures.'
FOCUS=(0,0,.084);ORTHO=.70
CAMERAS={'gray-front3q':(.40,-1.25,.94),'gray-back3q':(-.40,1.25,.94),'thumbnail':(.40,-1.25,.94),'qa-front':(0,-1.5,.73),'qa-side':(1.5,0,.84),'qa-top':(0,0,1.6),'qa-back':(0,1.5,.73),'qa-wireframe':(.40,-1.25,.94),'silhouette-128-front':(0,-1.5,.73),'silhouette-128-side':(1.5,0,.84)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def result(v,f,m,segments,role):
 if sum(dot(v[a],cross(v[b],v[c])) for a,b,c in f)<0:f=[(c,b,a) for a,b,c in f]
 return {'vertices':[tuple(round(x,9) for x in p) for p in v],'faces':f,'face_materials':m,'face_profile_segments':segments,'material':0,'role':role}
def rounded_triangle():
 # Three true straight sides connect three circular 120-degree corner arcs.
 # 9 arc samples plus 7 intervening straight-side samples per corner = 48.
 points=[]
 for k in range(3):
  a=-math.pi/2+k*math.tau/3;ca=(.105*math.cos(a),.105*math.sin(a));b=a+math.tau/3;cb=(.105*math.cos(b),.105*math.sin(b))
  for j in range(9):
   t=a-math.pi/3+j*math.pi/12;points.append((ca[0]+.024*math.cos(t),ca[1]+.024*math.sin(t)))
  t=a+math.pi/3;end=(ca[0]+.024*math.cos(t),ca[1]+.024*math.sin(t));start=(cb[0]+.024*math.cos(t),cb[1]+.024*math.sin(t))
  for j in range(1,8):points.append(tuple(end[d]+(start[d]-end[d])*j/8 for d in [0,1]))
 return points
ROUND_OUTLINE=[(.103*math.cos(-math.pi/2+i*math.tau/48),.103*math.sin(-math.pi/2+i*math.tau/48)) for i in range(48)]
TRIANGLE_OUTLINE=rounded_triangle()
CENTERS={ROUND:(-.145,-.008),TRIANGLE:(.145,.016)}
OUTLINES={ROUND:ROUND_OUTLINE,TRIANGLE:TRIANGLE_OUTLINE}
# Rows are (outline scale, height, lip extension, lip drop). Round wall stays
# straight; triangular wall has a separate original long tapered construction.
PROFILES={ROUND:[(0,0,0,0),(.95,0,0,0),(1,.006,0,0),(1,.118,0,0),(1,.135,.012,.002),(1,.145,.027,.005),(.91,.145,.027,.005),(.91,.135,.012,.002),(.91,.118,0,0),(.91,.020,0,0),(.87,.014,0,0),(0,.014,0,0)],TRIANGLE:[(0,0,0,0),(.75,0,0,0),(.78,.006,0,0),(.98,.160,0,0),(1,.178,.013,.002),(1,.188,.025,.005),(.90,.188,.025,.005),(.90,.178,.013,.002),(.88,.160,0,0),(.68,.024,0,0),(.64,.018,0,0),(0,.018,0,0)]}
def lip_weight(x,y):
 angle=abs(math.atan2(x,-y));return max(0,1-angle/(math.pi/5))
def shell(name,rows,role,mat=0,closed=False):
 poly=OUTLINES[name];cx,cy=CENTERS[name];n=len(poly);v=[];rings=[];f=[];fm=[];seg=[]
 for scale,z,ext,drop in rows:
  r=[]
  for x,y in (poly if scale else [(0,0)]):
   w=lip_weight(x,y) if scale else 0;r.append(len(v));v.append((cx+scale*x,cy+scale*y-ext*w,z-drop*w))
  rings.append(r)
 pairs=list(zip(rings,rings[1:]));
 if closed:pairs.append((rings[-1],rings[0]))
 for k,(a,b) in enumerate(pairs):
  for i in range(n):
   j=(i+1)%n
   faces=[(a[0],b[j],b[i])] if len(a)==1 else ([(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])])
   f.extend(faces);fm.extend([2 if k>=5 and not closed else mat]*len(faces));seg.extend([k]*len(faces))
 g=result(v,f,fm,seg,role);g['rings']=rings;return g
for body,mat in [(ROUND,0),(TRIANGLE,1)]:G[body]=shell(body,PROFILES[body],'One complete closed thick shell with plain flat base, actual cavity and continuous open pouring lip.',mat)
# Minimal nonnumeric illustrative marks, not a measurement scale.
def wedge_mark(ri,ro,z0,z1,half=.12,angle=-math.pi*.68):
 cx,cy=CENTERS[ROUND];v=[];f=[];steps=4
 for z in [z0,z1]:
  for r in [ri,ro]:
   for j in range(steps+1):
    a=angle-half+2*half*j/steps;v.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
 def ix(k,r,j):return (k*2+r)*(steps+1)+j
 for j in range(steps):
  for a,b,c,d in [(ix(0,0,j),ix(0,0,j+1),ix(0,1,j+1),ix(0,1,j)),(ix(1,0,j),ix(1,1,j),ix(1,1,j+1),ix(1,0,j+1)),(ix(0,0,j),ix(1,0,j),ix(1,0,j+1),ix(0,0,j+1)),(ix(0,1,j),ix(0,1,j+1),ix(1,1,j+1),ix(1,1,j))]:f.extend([(a,b,c),(a,c,d)])
 for a,b,c,d in [(ix(0,0,0),ix(0,1,0),ix(1,1,0),ix(1,0,0)),(ix(0,0,steps),ix(1,0,steps),ix(1,1,steps),ix(0,1,steps))]:f.extend([(a,b,c),(a,c,d)])
 return result(v,f,[3]*len(f),[0]*len(f),'Solid short illustrative tick, finitely embedded in round exterior; no number or units.')
for i,z in enumerate([.045,.071,.097]):
 name=f'IllustrativeTick_{i+1:02d}';G[name]=wedge_mark(.101,.1045,z-.0014,z+.0014,half=.12 if i!=1 else .085);MARKS.append(name)
 g=wedge_mark(.1015,.1020,z-.0007,z+.0007,half=.055);g['targets']=[ROUND,name];EMBED_VOLUMES[name]=g
 a=-math.pi*.68;cx,cy=CENTERS[ROUND];LINKS.append((ROUND,name,[(cx+.10175*math.cos(a),cy+.10175*math.sin(a),z)]))

def box(lo,hi,role):
 v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]];q=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];f=[t for a,b,c,d in q for t in [(a,b,c),(a,c,d)]];return result(v,f,[0]*12,[0]*12,role)
for body in BODIES:
 p=PROFILES[body];inner=p[6:-1];rows=[(0,p[-1][1]+.003,0,0),(p[-2][0]-.035,p[-1][1]+.003,0,0)]+[(s-.035,z,e,d) for s,z,e,d in reversed(inner[:-1])]+[(inner[0][0]-.035,p[5][1]+.025,p[5][2],p[5][3]),(0,p[5][1]+.025,0,0)]
 g=shell(body,rows,'Complete finite cavity following the actual floor, lower bevel, full straight or tapered inner wall, deformed lip and entire open mouth.');g['targets']=list(G);VOID_VOLUMES[body+'_WholeCavityAndMouth']=g
 cx,cy=CENTERS[body];y=-.120 if body==ROUND else -.139;z=p[5][1]+.002
 g=box((cx-.006,cy+y-.014,z),(cx+.006,cy+y+.014,z+.009),'Complete finite open spout corridor across the lowered front lip into air.');g['targets']=list(G);VOID_VOLUMES[body+'_OpenSpoutCorridor']=g
 s=.88 if body==ROUND else .69;z1=.011 if body==ROUND else .015
 g=shell(body,[(0,.003,0,0),(s,.003,0,0),(s,z1,0,0),(0,z1,0,0)],'Complete finite inset bottom material covering the full usable floor plan.');g['targets']=[body];SOLID_VOLUMES[body+'_CompleteBottomMaterial']=g
 # Continuous annular material follows every major wall and lip section.
 outer=[(s-.025,z,e,d) for s,z,e,d in p[2:6]];outer[0]=(outer[0][0],.025,0,0)
 inner=[(s+.025,z,e,d) for s,z,e,d in p[6:10]];inner[-1]=(inner[-1][0],.025,0,0)
 # Inset lip-top witness prevents its boundary from touching the actual rim.
 outer[-1]=(outer[-1][0],outer[-1][1]-.0015,outer[-1][2]-.0015,outer[-1][3]);inner[0]=(inner[0][0],inner[0][1]-.0015,inner[0][2]-.0015,inner[0][3])
 g=shell(body,outer+inner,'Complete connected finite annular wall-and-lip material bridge.',closed=True);g['targets']=[body];SOLID_VOLUMES[body+'_CompleteWallAndLipMaterial']=g
# Recenter geometry and all probes by exact full asset bounds; no nominal offset claim.
verts=[p for g in G.values() for p in g['vertices']];SHIFT=tuple(-(min(p[i] for p in verts)+max(p[i] for p in verts))/2 for i in [0,1])
for collection in [G,VOID_VOLUMES,SOLID_VOLUMES,EMBED_VOLUMES]:
 for g in collection.values():g['vertices']=[(round(x+SHIFT[0],9),round(y+SHIFT[1],9),z) for x,y,z in g['vertices']]
LINKS=[(a,b,[(x+SHIFT[0],y+SHIFT[1],z) for x,y,z in points]) for a,b,points in LINKS]
CENTERS={k:(v[0]+SHIFT[0],v[1]+SHIFT[1]) for k,v in CENTERS.items()}
def measure_beaker_geometry(vertices):
 return {'beaker_count':2,'single_prop_count':1,'round_height_m':max(p[2] for p in vertices[ROUND]),'triangular_height_m':max(p[2] for p in vertices[TRIANGLE]),'round_inner_floor_z_m':.014,'triangular_inner_floor_z_m':.018,'round_nominal_wall_thickness_m':.00927,'triangular_full_height_taper':True,'round_cross_section':'48-edge circular polygon','triangular_cross_section':'three true straight sides and three 120-degree rounded corners','same_shell_open_pouring_lips':2,'ground_supported_complete_flat_bases':2,'illustrative_tick_count':len(MARKS),'material_contract':MATERIAL_CONTRACT}

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
root=bpy.data.objects.new('OneRoundAndTriangularBeakerKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0008,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
beaker_evidence=measure_beaker_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'beaker_geometry':beaker_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laboratory/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'laboratory','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
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
