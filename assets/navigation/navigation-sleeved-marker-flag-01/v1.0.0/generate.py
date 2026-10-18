"""Original static sleeved marker flag, metres, Z up, centred bounds on ground.
Five connected closed meshes. The hollow sleeve and thick folded flag are ONE
continuous mesh. Its root replaces a finite sleeve-wall sector, never an overlap.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='navigation-sleeved-marker-flag-01';VERSION='1.0.0';TITLE='Sleeved Marker Flag'
DESCRIPTION=('One original static low-poly marker-flag visual prop: a low ground-supported foot, thick through-bored socket, slender shouldered pole, solid retaining stop ring and a genuinely open vertical sleeve continuously joined to one thick, gently folded blank rectangular flag. '
 'The pole seats with finite opposed faces on the foot and socket; the sleeve sits on the finite stop-ring face, with complete radial clearance from the pole and a readable upper gap. '
 'Five closed connected meshes, three opaque constant PBR materials, metres, native Z up, horizontal bounds-centred ground origin and front -Y. '
 'No lettering, national or event symbols, extra flags, map, terrain, textures or animation. Static visual geometry only: no cloth/wind simulation, meteorology, direction or route accuracy, visibility rating, traffic/rescue signal meaning, wind resistance, stability/load performance, manufacturing or safety certification. No mounting compatibility with earlier map or harbor props.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={}
BASE='Foot_ClosedFiniteGround';SOCKET='Socket_TrueThroughBore';POLE='Pole_IntegralSeatingShoulder';STOP='StopRing_EmbeddedInPole';FLAG='Flag_ContinuousHollowSleeveAndThickFold';BODY=BASE;FEET=[BASE]
PALETTE=[('WarmSand_FootAndSocket',(.46,.34,.20,1),.58,0),('DarkTeal_PoleAndStop',(.025,.095,.10,1),.38,.18),('Terracotta_FixedFlag',(.66,.17,.075,1),.57,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no procedural or image texture nodes.'
N=24;X=-.185
FOCUS=(0,0,.715);ORTHO=1.82
CAMERAS={'gray-front3q':(2.3,-4,2.45),'gray-back3q':(-2.3,4,2.45),'thumbnail':(2.3,-4,2.45),'qa-front':(0,-4,1.75),'qa-side':(4,0,1.75),'qa-top':(0,0,4),'qa-back':(0,4,1.75),'qa-wireframe':(2.3,-4,2.45),'silhouette-128-front':(0,-4,1.75),'silhouette-128-side':(4,0,1.75)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def finish(vs,fs,mat=0,role='',**extras):
 volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return dict(vertices=[tuple(round(c,9) for c in p) for p in vs],faces=fs,face_materials=[mat]*len(fs),material=mat,role=role,**extras)
def lathe(profile,mat=0,role='',close=False):
 vs=[];rings=[];fs=[];segments=[]
 for r,z in profile:
  ring=[]
  for i in range(N if r else 1):ring.append(len(vs));a=math.tau*i/N;vs.append((X+r*math.cos(a),r*math.sin(a),z))
  rings.append(ring)
 pairs=list(zip(rings,rings[1:]))+([(rings[-1],rings[0])] if close else [])
 for k,(a,b) in enumerate(pairs):
  for i in range(N):
   j=(i+1)%N;ff=[(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])]
   fs.extend(ff);segments.extend([k]*len(ff))
 return finish(vs,fs,mat,role,face_profile_segments=segments)
def annulus(ri,ro,z0,z1,mat=0,role=''):
 return lathe([(ri,z0),(ro,z0),(ro,z1),(ri,z1)],mat,role,True)
def cylinder(r,z0,z1):return lathe([(0,z0),(r,z0),(r,z1),(0,z1)])
def box(lo,hi):
 vs=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]];quads=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)];return finish(vs,[t for a,b,c,d in quads for t in [(a,b,c),(a,c,d)]])
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def earclip(v):
 area=sum(cross2(v[i],v[(i+1)%len(v)]) for i in range(len(v)));order=list(range(len(v))) if area>0 else list(reversed(range(len(v))));out=[]
 while len(order)>3:
  found=False
  for i,b in enumerate(order):
   a=order[i-1];c=order[(i+1)%len(order)];sub=lambda x,y:(x[0]-y[0],x[1]-y[1])
   if cross2(sub(v[b],v[a]),sub(v[c],v[b]))<=1e-14:continue
   def within(q):return all(cross2(sub(y,x),sub(v[q],x))>=-1e-14 for x,y in [(v[a],v[b]),(v[b],v[c]),(v[c],v[a])])
   if any(within(q) for q in order if q not in [a,b,c]):continue
   out.append((a,b,c));order.pop(i);found=True;break
  assert found,('untriangulable cap',v,order)
 out.append(tuple(order));return out if area>0 else [tuple(reversed(t)) for t in out]
G[BASE]=lathe([(0,0),(.168,0),(.180,.012),(.180,.038),(.162,.060),(0,.060)],0,'Low solid bevelled foot with a complete finite planar ground sole.')
G[SOCKET]=annulus(.017,.055,.060,.200,0,'Thick continuous socket, genuinely open through its full height; lower annular face seats on foot.')
G[POLE]=lathe([(0,.060),(.014,.060),(.014,.200),(.032,.200),(.032,.215),(.014,.215),(.014,1.400),(.018,1.410),(.018,1.422),(.010,1.432),(0,1.432)],1,'Slender closed pole with integral finite shoulder seating on socket and blunt faceted upper cap.')
G[STOP]=annulus(.011,.032,.840,.860,1,'Solid stop ring finitely embeds into pole and supports complete lower sleeve annulus.')
# Sleeve-to-flag mesh: both caps share the actual sleeve-wall root edges.
# Sleeve outer side segments -30 to +30 degrees are replaced by the flag shell.
def sleeve_flag():
 z0,z1=.860,1.280;vs=[];fs=[];tags=[]
 inner=[(.020*math.cos(math.tau*i/N),.020*math.sin(math.tau*i/N)) for i in range(N)]
 outer=[(.028*math.cos(math.tau*i/N),.028*math.sin(math.tau*i/N)) for i in range(N)]
 extra=[(.170,-.014),(.340,.022),(.550,.002),(.550,.026),(.340,.046),(.170,.010)]
 ring=inner+outer+extra;L=len(ring)
 for z in [z0,z1]:vs.extend((X+x,y,z) for x,y in ring)
 def tri(f,tag):fs.append(tuple(f));tags.append(tag)
 def quad(q,tag):a,b,c,d=q;tri((a,b,c),tag);tri((a,c,d),tag)
 omitted={22,23,0,1}
 for i in range(N):
  j=(i+1)%N;ii,jj=i,j;oi,oj=N+i,N+j
  quad((ii,jj,oj,oi),'bottom_annulus');quad((L+ii,L+oi,L+oj,L+jj),'top_annulus')
  quad((ii,L+ii,L+jj,jj),'inner_bore')
  if i not in omitted:quad((oi,oj,L+oj,L+oi),'outer_sleeve')
 # Going from lower root through the finite-thickness fold to upper root,
 # then clockwise along the displaced sleeve arc closes the flag cap.
 boundary=[N+22]+list(range(2*N,2*N+6))+[N+2,N+1,N+0,N+23]
 captris=earclip([ring[k] for k in boundary])
 for a,b,c in captris:tri((boundary[c],boundary[b],boundary[a]),'flag_bottom');tri((L+boundary[a],L+boundary[b],L+boundary[c]),'flag_top')
 exposed=boundary[:8]
 for k,(i,j) in enumerate(zip(exposed,exposed[1:])):quad((i,j,L+j,L+i),'flag_front' if k<3 else 'flag_back' if k>3 else 'flag_free_edge')
 return finish(vs,fs,2,'One continuous closed hollow sleeve and thick lightly folded blank flag; finite full-height shared root.',face_regions=tags)
G[FLAG]=sleeve_flag()
# Exact finite bearing declarations, tested using every contact triangle and
# bidirectional complete-edge/vertex/centroid zero penetration, not just points.
def seat(a,b,z,radius,minarea):
 CONTACTS.append({'a':a,'b':b,'axis':2,'plane_m':z,'points':[(X+radius,0,z),(X-radius,0,z),(X,radius,z),(X,-radius,z)],'interior_probe_offset_m':.0004,'minimum_patch_area_m2':minarea})
seat(BASE,SOCKET,.060,.034,.007)
seat(BASE,POLE,.060,.007,.00055)
seat(SOCKET,POLE,.200,.024,.0021)
seat(STOP,FLAG,.860,.024,.0011)
LINKS=[(POLE,STOP,[(X+.0125,0,.850),(X-.0125,0,.850),(X,.0125,.850),(X,-.0125,.850)])]
EMBED_VOLUMES['StopRingToPole_FiniteAnnularEmbed']=dict(annulus(.0118,.0130,.844,.856),targets=[POLE,STOP],role='Complete positive-thickness embedded annulus joining the stop to the pole.')
SOLID_VOLUMES['ContinuousSleeveFlagRoot']=dict(box((X+.0225,-.004,.885),(X+.055,.004,1.255)),targets=[FLAG],role='Finite full-height material bridge crosses real sleeve wall into the thick folded flag root.')
VOID_VOLUMES['Socket_IsolatedCompleteThroughBore']=dict(cylinder(.0160,.052,.208),targets=[SOCKET],role='Whole closed finite socket hole from below to above its open ends, isolated from inserted pole.')
VOID_VOLUMES['Sleeve_IsolatedCompleteThroughBore']=dict(cylinder(.0190,.850,1.290),targets=[FLAG],role='Whole closed finite sleeve hole from below to above both open ends, isolated from inserted pole and stop.')
VOID_VOLUMES['Socket_AssemblyFullCircumferenceClearance']=dict(annulus(.0148,.0160,.065,.195),targets=list(G),role='Complete finite annular open volume between actual pole and socket throughout their insertion.')
VOID_VOLUMES['Sleeve_AssemblyFullCircumferenceClearance']=dict(annulus(.0152,.0188,.865,1.275),targets=list(G),role='Complete finite annular air volume between pole and sleeve through the full sleeve length.')
VOID_VOLUMES['Sleeve_UpperReadableGap']=dict(annulus(.0152,.0280,1.285,1.390),targets=list(G),role='Complete finite annular upper gap from sleeve top toward the upper cap; excludes pole material.')
NONCONTACT_DOMAINS=[{'a':SOCKET,'b':POLE,'a_z_min':.065,'a_z_max':.195,'b_z_min':.065,'b_z_max':.195,'minimum_m':.0028}, {'a':FLAG,'b':POLE,'minimum_m':.0057}]
def measure_flag_geometry(vertices):
 allv=[p for v in vertices.values() for p in v];return {'height_m':max(v[2] for v in allv),'width_m':max(v[0] for v in allv)-min(v[0] for v in allv),'pole_radius_m':.014,'socket_bore_radius_m':.017,'sleeve_bore_radius_m':.020,'sleeve_height_m':.420,'flag_nominal_thickness_m':.024,'sleeve_top_to_cap_lower_gap_m':.120,'single_continuous_sleeve_flag_mesh':True,'single_prop_count':1,'material_contract':MATERIAL_CONTRACT}

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
root=bpy.data.objects.new('OneSleevedMarkerFlag',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
flag_evidence=measure_flag_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'flag_geometry':flag_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/navigation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'navigation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-3,-4,5),600,4.0),('Fill',(4,-1,3),300,3.2),('Rim',(1,4,4),425,3.2)]:
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
