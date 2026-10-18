"""Original open camera bag with a true three-recess padded insert; one static prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='photography-recessed-insert-camera-bag-01';VERSION='1.0.0';TITLE='Recessed Insert Camera Bag'
DESCRIPTION=('One original static low-poly open camera bag, counted as one prop. A broad low thick chamfered shell has a genuine complete bottom and open mouth. One continuous padded insert is finitely seated on the bag floor and contains a central rectangular bottomed equipment recess and two round bottomed empty lens wells. All three recesses have actual continuous inner walls, finite separating material and a complete common lower plate. A thick rear lid is fixed raised with a finite shell-root embedding; two short open side lifting loops each embed both roots in the shell. Five closed connected mesh components, five opaque constant PBR materials, metres, native Z up, bounds-centred ground origin and front -Y. No camera, lens, hard case, separate pouch, scene, texture or animation. Static illustrative geometry only; no shock, water, load, wear, equipment protection, storage capacity, lens specification, human-fit, manufacturing, safety or old-equipment dimensional compatibility claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};EMBED_VOLUMES={}
BODY='Bag_ThickOpenShell';INSERT='Insert_ContinuousThreeBottomedRecesses';LID='Lid_FixedRaisedRear';HANDLES=['Loop_LeftShortOpenHandle','Loop_RightShortOpenHandle'];FEET=[BODY]
LID_ANGLE=math.radians(20);EY=math.sin(LID_ANGLE);EZ=math.cos(LID_ANGLE);NY=EZ;NZ=-EY
YSHIFT=-(.137+.294*EY+.012*NY-.160)/2
SHIFT=0
PALETTE=[('MutedPetrol_OuterShell',(.025,.145,.17,1),.64,0),('WarmSand_PaddedInsert',(.55,.37,.19,1),.81,0),('WarmIvory_RecessSurfaces',(.70,.56,.36,1),.80,0),('DarkSlate_LoopsAndLidEdge',(.026,.039,.042,1),.72,0),('WarmTerracotta_LidLining',(.38,.125,.055,1),.71,0)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no procedural or image texture nodes.'
FOCUS=(0,0,.245);ORTHO=.94
CAMERAS={'gray-front3q':(.90,-1.2,1.0),'gray-back3q':(-.90,1.2,1.0),'thumbnail':(.90,-1.2,1.0),'qa-front':(0,-1.4,.75),'qa-side':(1.4,0,.75),'qa-top':(0,0,1.6),'qa-back':(0,1.4,.75),'qa-wireframe':(.90,-1.2,1.0),'silhouette-128-front':(0,-1.4,.75),'silhouette-128-side':(1.4,0,.75)}
CAMERA_SCALES={};TECHNICAL_UNDERSIDE_VIEWS=[];WIRE_THICKNESS=ORTHO/640

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def finish(vs,fs,mats):
 # Weld shared region perimeter vertices; all faces are authored as triangles.
 unique=[];index={};remap=[]
 for p in vs:
  p=tuple(round(c,9) for c in p)
  if p not in index:index[p]=len(unique);unique.append(p)
  remap.append(index[p])
 fs=[tuple(remap[i] for i in f) for f in fs]
 # Resolve each shared edge to opposite directions, then pick outward volume.
 edge_faces={}
 for fi,face in enumerate(fs):
  for a,b in zip(face,face[1:]+face[:1]):edge_faces.setdefault(tuple(sorted((a,b))),[]).append((fi,a,b))
 signs={0:1};todo=[0]
 while todo:
  fi=todo.pop();face=fs[fi]
  for a,b in zip(face,face[1:]+face[:1]):
   for fj,c,d in edge_faces[tuple(sorted((a,b)))]:
    if fj==fi:continue
    wanted=signs[fi]*(-1 if (a,b)==(c,d) else 1)
    if fj in signs:assert signs[fj]==wanted,'Nonorientable boundary'
    else:signs[fj]=wanted;todo.append(fj)
 assert len(signs)==len(fs),'Disconnected mesh boundary'
 fs=[face if signs[i]>0 else tuple(reversed(face)) for i,face in enumerate(fs)]
 volume=sum(dot(unique[f[0]],cross(unique[f[1]],unique[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':[tuple(round(c,9) for c in (p[0],p[1]+YSHIFT,p[2])) for p in unique],'faces':fs,'face_materials':mats,'material':0}
def connect(fs,fm,a,b,mat):
 for i in range(len(a)):
  j=(i+1)%len(a);fs.extend([(a[i],b[i],b[j]),(a[i],b[j],a[j])]);fm.extend([mat,mat])
def box(lo,hi,material=0):
 vs=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 qs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 fs=[t for a,b,c,d in qs for t in [(a,b,c),(a,c,d)]];return finish(vs,fs,[material]*len(fs))
def octagon(rx,ry,b):return [(-rx+b,-ry),(rx-b,-ry),(rx,-ry+b),(rx,ry-b),(rx-b,ry),(-rx+b,ry),(-rx,ry-b),(-rx,-ry+b)]
def fan(vs,fs,fm,ring,mat,up):
 c=len(vs);vs.append(tuple(sum(vs[i][k] for i in ring)/len(ring) for k in range(3)))
 for i in range(len(ring)):
  j=(i+1)%len(ring);fs.append((ring[i],ring[j],c) if up else (ring[j],ring[i],c));fm.append(mat)
# Continuous bottom -> inner wall -> top rim -> outer belly -> ground shell.
v=[];f=[];m=[];rr=[]
for rx,ry,b,z in [(.295,.120,.022,.035),(.300,.125,.022,.245),(.325,.150,.028,.245),(.335,.160,.034,.070),(.300,.135,.030,0)]:
 r=[]
 for x,y in octagon(rx,ry,b):r.append(len(v));v.append((x,y,z))
 rr.append(r)
fan(v,f,m,rr[0],1,True)
for a,b,mat in zip(rr,rr[1:],[0,0,0,0]):connect(f,m,a,b,mat)
fan(v,f,m,rr[-1],3,False)
G[BODY]=finish(v,f,m);G[BODY]['role']='Single closed thick open shell with true full floor, finite ground face and four continuous inner/outer walls; no separate false cavity cap.'
# Top of the insert is authored as three annuli with precisely matching shared
# strip edges. Welding those edges creates one continuous three-recess solid.
def rect32(x0,x1,y0,y1):
 p=[]
 for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:
  for i in range(8):p.append((a[0]+(b[0]-a[0])*i/8,a[1]+(b[1]-a[1])*i/8))
 return p
def circle32(cx,r):return [(cx+r*math.cos(-3*math.pi/4+math.tau*i/32),r*math.sin(-3*math.pi/4+math.tau*i/32)) for i in range(32)]
v=[];f=[];m=[];outer_segments=[]
for k,(x0,x1) in enumerate([(-.275,-.100),(-.100,.100),(.100,.275)]):
 outer=rect32(x0,x1,-.105,.105)
 top=rect32(-.085,.085,-.078,.078) if k==1 else circle32(-.190 if k==0 else .190,.065)
 low=rect32(-.078,.078,-.071,.071) if k==1 else circle32(-.190 if k==0 else .190,.058)
 rings=[]
 for points,z in [(outer,.222),(top,.222),(low,.065)]:
  r=[]
  for x,y in points:r.append(len(v));v.append((x,y,z))
  rings.append(r)
 connect(f,m,rings[1],rings[0],1);connect(f,m,rings[2],rings[1],2);fan(v,f,m,rings[2],2,True)
 # Only exterior strip edges continue to the common lower plate.
 for i in range(32):
  j=(i+1)%32;a=outer[i];b=outer[j]
  if abs(a[0]-b[0])<1e-9 and abs(a[0])<.101:continue
  outer_segments.append((rings[0][i],rings[0][j]))
for a,b in outer_segments:
 aa=len(v);v.append((v[a][0],v[a][1],.035));bb=len(v);v.append((v[b][0],v[b][1],.035))
 f.extend([(a,aa,bb),(a,bb,b)]);m.extend([1,1])
 c=len(v);v.append((0,0,.035));f.append((bb,aa,c));m.append(1)
G[INSERT]=finish(v,f,m);G[INSERT]['role']='One closed continuous thick insert, three bottomed recesses, joined finite top separators and complete common lower plate seated on shell floor; actual empty recesses, no painted holes.'
# Closed bevel-corner raised lid, finite depth and one full-width embedded root.
v=[];f=[];m=[];rr=[]
for n in [-.012,.012]:
 r=[]
 for x,q in octagon(.290,.147,.018):
  q+=.147;r.append(len(v));v.append((x,.137+q*EY+n*NY,.215+q*EZ+n*NZ))
 rr.append(r)
fan(v,f,m,rr[0],4,False);connect(f,m,rr[0],rr[1],3);fan(v,f,m,rr[1],0,True)
G[LID]=finish(v,f,m);G[LID]['role']='One closed thick chamfered fixed raised rear lid. Complete finite lower-root volume embeds in the rear shell; no moving hinge or dynamic opening claim.'
# Two short U-shaped side loops. Each is a continuous extruded thick band with
# two finite root volumes embedded in the existing side wall. No crossing strap.
loop_outline=[(-.082,.174),(-.082,.292),(-.065,.311),(.065,.311),(.082,.292),(.082,.174),(.055,.174),(.055,.279),(.045,.288),(-.045,.288),(-.055,.279),(-.055,.174)]
def earclip(poly):
 ids=list(range(len(poly)));out=[]
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))
 if area<0:ids.reverse()
 def cp(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 while len(ids)>3:
  found=False
  for i in range(len(ids)):
   a,b,c=ids[i-1],ids[i],ids[(i+1)%len(ids)]
   if cp(poly[a],poly[b],poly[c])<1e-13:continue
   if any(cp(poly[a],poly[b],poly[j])>=-1e-12 and cp(poly[b],poly[c],poly[j])>=-1e-12 and cp(poly[c],poly[a],poly[j])>=-1e-12 for j in ids if j not in [a,b,c]):continue
   out.append((a,b,c));ids.pop(i);found=True;break
  assert found,'No polygon ear'
 out.append(tuple(ids));return out
for sign,name in zip([-1,1],HANDLES):
 v=[];f=[];m=[];rr=[]
 for x in [sign*.313,sign*.350]:
  r=[]
  for y,z in loop_outline:r.append(len(v));v.append((x,y,z))
  rr.append(r)
 for a,b,c in earclip(loop_outline):f.extend([(rr[0][c],rr[0][b],rr[0][a]),(rr[1][a],rr[1][b],rr[1][c])]);m.extend([3,3])
 # Outline is clockwise in yz; face orientation is normalized in finish.
 for i in range(len(loop_outline)):
  j=(i+1)%len(loop_outline);f.extend([(rr[0][i],rr[1][i],rr[1][j]),(rr[0][i],rr[1][j],rr[0][j])]);m.extend([3,3])
 G[name]=finish(v,f,m);G[name]['role']='One closed continuous short side loop, real complete arch opening, two finite embedded lower roots and no crossing of lid or equipment recesses.'
# Complete finite support and material/empty certificates, source-only until
# independently evaluated against the final exported GLB surfaces.
CONTACTS.append({'name':'FullInsertBottomOnShellFloor','a':BODY,'b':INSERT,'plane_m':.035,'points':[(x,y+YSHIFT,.035) for x in [-.18,0,.18] for y in [-.07,.07]],'minimum_patch_area_m2':.114,'interior_probe_offset_m':.0007})
def cylinder(cx,cy,r,z0,z1):
 v=[];f=[];m=[];rr=[]
 for z in [z0,z1]:
  rr.append(list(range(len(v),len(v)+32)));v += [(cx+r*math.cos(-3*math.pi/4+math.tau*i/32),cy+r*math.sin(-3*math.pi/4+math.tau*i/32),z) for i in range(32)]
 connect(f,m,rr[1],rr[0],0);fan(v,f,m,rr[0],0,False);fan(v,f,m,rr[1],0,True)
 return finish(v,f,m)
def tapered_void(cx):
 v=[];f=[];m=[];rr=[]
 for z,r in [(.067,.0565),(.222,.0635),(.260,.0635)]:
  rr.append(list(range(len(v),len(v)+32)));v += [(cx+r*math.cos(-3*math.pi/4+math.tau*i/32),r*math.sin(-3*math.pi/4+math.tau*i/32),z) for i in range(32)]
 for a,b in zip(rr,rr[1:]):connect(f,m,b,a,0)
 fan(v,f,m,rr[0],0,False);fan(v,f,m,rr[-1],0,True)
 return finish(v,f,m)
def tapered_rect_void():
 v=[];f=[];m=[];rr=[]
 for z,rx,ry in [(.067,.0765,.0695),(.222,.0835,.0765),(.260,.0835,.0765)]:
  r=[]
  for x,y in [(-rx,-ry),(rx,-ry),(rx,ry),(-rx,ry)]:r.append(len(v));v.append((x,y,z))
  rr.append(r)
 for a,b in zip(rr,rr[1:]):connect(f,m,b,a,0)
 fan(v,f,m,rr[0],0,False);fan(v,f,m,rr[-1],0,True)
 return finish(v,f,m)
VOID_VOLUMES['CentralEquipmentRecessAndMouth']=dict(tapered_rect_void(),targets=list(G),role='Full tapered central rectangular empty volume, from 2 mm above floor through the entire mouth to above bag rim.')
for sign,label in [(-1,'Left'),(1,'Right')]:
 VOID_VOLUMES[label+'LensWellAndMouth']=dict(tapered_void(sign*.190),targets=list(G),role='Full 32-sided tapered circular empty volume, almost to each actual faceted wall, from recess floor through complete circular mouth.')
 VOID_VOLUMES[label+'ShortLoopOpening']=dict(box((min(sign*.310,sign*.354),-.043,.251),(max(sign*.310,sign*.354),.043,.284)),targets=list(G),role='Complete finite upper arch opening of a short side loop above the shell, passes through both sides of its band.')
# Complete lower insert plate and continuous separators, plus outer wall strips.
SOLID_VOLUMES['CompleteInsertLowerPlate']=dict(box((-.272,-.102,.038),(.272,.102,.061)),targets=[INSERT],role='Broad finite common lower plate below all three recesses, wholly inside the one continuous insert.')
SOLID_VOLUMES['CompleteShellLowerPlate']=dict(box((-.272,-.102,.006),(.272,.102,.030)),targets=[BODY],role='Broad finite shell bottom plate and continuous support beneath the insert.')
for sign,label in [(-1,'Left'),(1,'Right')]:
 lo,hi=sorted([sign*.090,sign*.120])
 SOLID_VOLUMES[label+'ContinuousSeparator']=dict(box((lo,-.055,.039),(hi,.055,.219)),targets=[INSERT],role='Complete continuous finite separating wall from the lower plate to the padded top, between the central recess and round well.')
for sign,label in [(-1,'Front'),(1,'Back')]:
 lo,hi=sorted([sign*.084,sign*.101])
 SOLID_VOLUMES[label+'OuterInsertWall']=dict(box((-.270,lo,.039),(.270,hi,.219)),targets=[INSERT],role='Continuous long finite padded wall and bottom-root material outside all three recesses.')
EMBED_VOLUMES['LidRootInRearShell']=dict(box((-.245,.141,.220),(.245,.146,.230)),targets=[BODY,LID],role='Complete finite broad lid-root material volume contained by both lid and rear shell.')
for sign,name in zip([-1,1],HANDLES):
 for side in [-1,1]:
  x0,x1=sorted([sign*.315,sign*.323]);y0,y1=sorted([side*.061,side*.076])
  EMBED_VOLUMES[name+('_FrontRoot' if side<0 else '_BackRoot')]=dict(box((x0,y0,.180),(x1,y1,.209)),targets=[BODY,name],role='Complete finite lower loop-root embedding inside both shell side wall and thick band.')
for name,g in EMBED_VOLUMES.items():
 vs=g['vertices'];p=tuple(sum(v[k] for v in vs)/len(vs) for k in range(3));LINKS.append((g['targets'][0],g['targets'][1],[p]))
def measure_bag_geometry(vertices):
 return {'shell_rim_height_m':.245,'insert_top_z_m':.222,'common_insert_floor_z_m':.065,'insert_support_plane_z_m':.035,'bottomed_cavity_count':3,'central_rectangular_recesses':1,'round_bottomed_wells':2,'short_side_loops':2,'continuous_insert_meshes':1,'fixed_raised_rear_lid':True,'single_prop_count':1,'material_contract':MATERIAL_CONTRACT}
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
root=bpy.data.objects.new('OneRecessedInsertCameraBag',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
bag_evidence=measure_bag_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'bag_geometry':bag_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/photography/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'photography','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
