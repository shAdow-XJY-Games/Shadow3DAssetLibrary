"""Original freestanding static ticket booth with genuinely open service and rear access.
Metres, Z up, ground-centre origin, public front -Y. No people or ticketing software.
One enclosed volume, supported inside counter, thick ceiling and striped solid roof.
Self-contained: fresh actual GLB renders and full oriented-geometry/solid-PBR guard.
"""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carnival-service-window-ticket-booth-01';VERSION='1.0.0';TITLE='Open-Service Carnival Ticket Booth'
DESCRIPTION=('One original freestanding static ticket booth with thick enclosing walls, a real open front service window, a supported interior counter extending into an exterior handover shelf, and a rear staff access opening. '
 'A finite ground plinth supports a single closed wall-shell mesh, corner posts, countertop and its interior triangular brackets, a thick ceiling cornice and a striped eight-face hipped roof. '
 'A small seated TICKETS plaque uses original solid polygon letters. Rear doorway nominal clear width 0.86 m, clear height 2.03 m above the 0.10 m floor step. Service opening nominal clear width 1.256 m, height 0.976 m above the 1.08 m counter. '
 'One static building prop, metres, Z up, ground-centre origin, public front -Y. Five constant PBR materials, no textures, people, equipment, tickets or external assets. '
 'No ticket sales, payments, opening animation, navigation, wheelchair accessibility, crowd or fire safety, operation, architectural compliance, load guarantee or compatibility with other building families is claimed.')
G={};LINKS=[];FEET=['Base_GroundPlinth'];BORES=[];GAPS=[];FLOOR_RAYS=[];CLEAR_BOXES=[]
PALETTE=[('Wall_WarmIvory',(.73,.60,.38,1),.73,0),('Trim_CarnivalCrimson',(.48,.035,.045,1),.55,0),('Timber_DarkWalnut',(.17,.065,.026,1),.62,0),('Accent_WarmGold',(.71,.37,.065,1),.49,.15),('Sign_DeepTeal',(.025,.095,.105,1),.59,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.02):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def box(name,lo,hi,mat,role):
 x0,y0,z0=lo;x1,y1,z1=hi;vs=[(x,y,z) for z in [z0,z1] for y in [y0,y1] for x in [x0,x1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,role)
def poly_y(name,outline,y0,y1,mat,role):
 k=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline];fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def poly_x(name,outline,x0,x1,mat,role):
 k=len(outline);vs=[(x,y,z) for x in [x0,x1] for y,z in outline];fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 return mesh(name,vs,fs,mat,role)
def union_boxes(name,boxes,mat,role):
 # Direct boundary of the rectilinear union. No internal faces or overlapping wall bricks.
 axes=[sorted({b[k][i] for b in boxes for k in [0,1]}) for i in range(3)];occupied=set()
 for i in range(len(axes[0])-1):
  for j in range(len(axes[1])-1):
   for k in range(len(axes[2])-1):
    p=[(axes[a][n]+axes[a][n+1])/2 for a,n in enumerate([i,j,k])]
    if any(all(lo[a]<p[a]<hi[a] for a in range(3)) for lo,hi in boxes):occupied.add((i,j,k))
 vs=[];fs=[];lookup={}
 def vid(p):
  p=tuple(p)
  if p not in lookup:lookup[p]=len(vs);vs.append(p)
  return lookup[p]
 corners=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
 faces=[((-1,0,0),(0,4,7,3)),((1,0,0),(1,2,6,5)),((0,-1,0),(0,1,5,4)),((0,1,0),(3,7,6,2)),((0,0,-1),(0,3,2,1)),((0,0,1),(4,5,6,7))]
 for cell in sorted(occupied):
  vv=[tuple(axes[a][cell[a]+c[a]] for a in range(3)) for c in corners]
  for delta,ids in faces:
   if tuple(cell[a]+delta[a] for a in range(3)) not in occupied:fs.append(tuple(vid(vv[t]) for t in ids))
 return mesh(name,vs,fs,mat,role)
box('Base_GroundPlinth',(-1,-.88,0),(1,.88,.10),2,'single broad finite ground-bearing base; top floor at 100mm creates a step at rear access')
# A true single wall shell, not black planes on a solid box. Front window and rear doorway are omitted volume.
W=[((-.9,-.78,.075),(.9,-.66,1.02)),((-.9,-.78,1.02),(-.64,-.66,2.34)),((.64,-.78,1.02),(.9,-.66,2.34)),((-.64,-.78,2.08),(.64,-.66,2.34)),
 ((-.9,-.66,.075),(-.78,.66,2.34)),((.78,-.66,.075),(.9,.66,2.34)),
 ((-.9,.66,.075),(-.43,.78,2.34)),((.43,.66,.075),(.9,.78,2.34)),((-.43,.66,2.13),(.43,.78,2.34))]
union_boxes('Body_ThickOpenWallShell',W,0,'single closed thick wall shell surrounding an empty interior; genuine front service aperture and full-height rear entry aperture')
link('Body_ThickOpenWallShell','Base_GroundPlinth',(0,-.72,.087),spread=.55)
for sx,lx in [(-1,'Left'),(1,'Right')]:
 for sy,ly in [(-1,'Front'),(1,'Back')]:
  x=sx*.90;y=sy*.78;n='Post_'+lx+ly
  box(n,(x-.055,y-.055,.082),(x+.055,y+.055,2.37),1,'finite crimson corner post, embedded in wall and plinth, supporting top cornice')
  link(n,'Body_ThickOpenWallShell',(sx*.872,sy*.752,1.5),axis=(0,0,1),spread=.55)
  link(n,'Base_GroundPlinth',(x,y,.091),axis=(1,0,0),spread=.025)
box('Counter_InsideAndHandover',(-.70,-.96,.99),(.70,-.37,1.08),2,'continuous 90mm-thick counter; 290mm interior working depth from inner front wall, 180mm exterior handover overhang')
link('Counter_InsideAndHandover','Body_ThickOpenWallShell',(0,-.72,1.005),spread=.50)
for x,label in [(-.49,'Left'),(.49,'Right')]:
 name='CounterBracket_'+label
 poly_x(name,[(-.705,.80),(-.705,1.015),(-.395,1.015)],x-.035,x+.035,3,'solid triangular interior bracket connecting the wall to the underside of the counter')
 link(name,'Body_ThickOpenWallShell',(x,-.686,.91),axis=(0,0,1),spread=.045)
 link(name,'Counter_InsideAndHandover',(x,-.55,1.005),axis=(0,1,0),spread=.055)
# Narrow red frame is seated into the wall and does not cap the aperture.
for sx,label in [(-1,'Left'),(1,'Right')]:
 x=sx*.651;n='WindowFrame_'+label
 box(n,(x-.023,-.811,1.045),(x+.023,-.650,2.105),1,'solid vertical service-window trim embedded in structural wall, open aperture retained')
 link(n,'Body_ThickOpenWallShell',(sx*.658,-.72,1.5),axis=(0,0,1),spread=.30)
box('WindowFrame_Header',(-.681,-.818,2.056),(.681,-.645,2.112),1,'finite horizontal service-window head, embedded in structural header and side frame')
link('WindowFrame_Header','Body_ThickOpenWallShell',(0,-.72,2.095),spread=.45)
box('Roof_ThickCeilingCornice',(-1.015,-.895,2.31),(1.015,.895,2.43),3,'thick continuous ceiling and eave band, supported by walls/posts; actual interior ceiling at 2.31m')
link('Roof_ThickCeilingCornice','Body_ThickOpenWallShell',(0,-.72,2.325),spread=.55)
for sx,lx in [(-1,'Left'),(1,'Right')]:
 for sy,ly in [(-1,'Front'),(1,'Back')]:link('Roof_ThickCeilingCornice','Post_'+lx+ly,(sx*.90,sy*.78,2.35),spread=.02)
# Rectangular thick roof: eight triangular upper slope panels share real edges and one apex.
ring=[(-1.08,-.96),(0,-.96),(1.08,-.96),(1.08,0),(1.08,.96),(0,.96),(-1.08,.96),(-1.08,0)]
vs=[(x,y,z) for z in [2.395,2.48] for x,y in ring]+[(0,0,2.96)]
fs=[tuple(reversed(range(8)))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]+[(i+8,(i+1)%8+8,16) for i in range(8)]
mesh('Roof_StripedHipSolid',vs,fs,1,'closed solid hipped roof with eight alternating crimson/ivory triangular upper faces and finite eave thickness')
G['Roof_StripedHipSolid']['face_materials']=[1]*9+[1,0,1,0,1,0,1,0]
link('Roof_StripedHipSolid','Roof_ThickCeilingCornice',(0,0,2.412),spread=.55)
# Original solid polygon lettering requires no font, textures or external models.
box('Sign_SeatedBoard',(-.61,-.807,2.145),(.61,-.771,2.307),4,'small teal sign board seated in the actual front structural header')
link('Sign_SeatedBoard','Body_ThickOpenWallShell',(0,-.775,2.22),spread=.45)
letters={
 'T':[(0,1),(1,1),(1,.78),(.62,.78),(.62,0),(.38,0),(.38,.78),(0,.78)],
 'I':[(0,1),(1,1),(1,.8),(.62,.8),(.62,.2),(1,.2),(1,0),(0,0),(0,.2),(.38,.2),(.38,.8),(0,.8)],
 'C':[(0,0),(1,0),(1,.22),(.24,.22),(.24,.78),(1,.78),(1,1),(0,1)],
 'K':[(0,0),(.24,0),(.24,.39),(.72,0),(1,0),(.48,.51),(1,1),(.72,1),(.24,.61),(.24,1),(0,1)],
 'E':[(0,0),(1,0),(1,.22),(.24,.22),(.24,.41),(.84,.41),(.84,.61),(.24,.61),(.24,.78),(1,.78),(1,1),(0,1)],
 'S':[(0,0),(1,0),(1,.61),(.24,.61),(.24,.78),(1,.78),(1,1),(0,1),(0,.41),(.76,.41),(.76,.22),(0,.22)]}
for i,char in enumerate('TICKETS'):
 x=-.405+i*.12;n='SignLetter_%d_%s'%(i,char);poly_y(n,[(x+a*.09,2.161+b*.128) for a,b in letters[char]],-.823,-.802,0,'original polygon letter extruded into supporting sign board')
 # Every glyph has its upper-left stroke at this point, away from all outline edges.
 link(n,'Sign_SeatedBoard',(x+.0108,-.8045,2.2762),axis=(0,0,1),spread=.003)
# Bounded clear prisms explicitly test whole volumes, not only sparse center rays.
CLEAR_BOXES=[{'label':'front_service_aperture','lo':(-.620,-1.03,1.090),'hi':(.620,-.35,2.048)},
 {'label':'rear_access_above_100mm_step','lo':(-.420,.60,.110),'hi':(.420,1.03,2.120)},
 {'label':'interior_operator_space','lo':(-.760,-.350,.110),'hi':(.760,.640,2.290)}]
for r in CLEAR_BOXES:
 lo,hi=r['lo'],r['hi'];axis=1 if r['label']!='interior_operator_space' else 2
 for a in [.1,.5,.9]:
  for b in [.1,.5,.9]:
   others=[i for i in range(3) if i!=axis];p=list(lo);p[others[0]]=lo[others[0]]+(hi[others[0]]-lo[others[0]])*a;p[others[1]]=lo[others[1]]+(hi[others[1]]-lo[others[1]])*b;d=[0,0,0];d[axis]=1
   GAPS.append({'label':r['label'],'origin_m':p,'direction':d,'length_m':hi[axis]-lo[axis]})
for x in [-.60,0,.60]:
 for y in [-.2,.2,.55]:FLOOR_RAYS.append({'label':'interior_actual_floor','origin_m':[x,y,2.2],'direction':[0,0,-1],'length_m':2.2,'expected_mesh':'Base_GroundPlinth','expected_z_m':.10})
for x in [-.50,0,.50]:
 for y in [-.90,-.55]:FLOOR_RAYS.append({'label':'actual_supported_counter','origin_m':[x,y,1.9],'direction':[0,0,-1],'length_m':1.0,'expected_mesh':'Counter_InsideAndHandover','expected_z_m':1.08})
def triangle_box_intersects(triangle,lo,hi):
 polygon=[tuple(v) for v in triangle]
 for axis in range(3):
  for limit,sign in [(lo[axis],1),(hi[axis],-1)]:
   old=polygon;polygon=[]
   if not old:return False
   for start,end in zip(old,old[1:]+old[:1]):
    ds=(start[axis]-limit)*sign;de=(end[axis]-limit)*sign;si=ds>=-1e-10;ei=de>=-1e-10
    if si!=ei:polygon.append(add(start,mul(sub(end,start),ds/(ds-de))))
    if ei:polygon.append(end)
 return bool(polygon)
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
root=bpy.data.objects.new('OneOpenServiceTicketBooth',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
for name,g in G.items():
 me=bpy.data.meshes.new(name);me.from_pydata(g['vertices'],[],g['faces']);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();
 for m in mats:me.materials.append(m)
 for i,f in enumerate(me.polygons):f.material_index=g.get('face_materials',[g['material']]*len(me.polygons))[i]
 o['component_role']=g['role'];parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg);triangles+=len(o.data.loop_triangles)
 component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Finite support and true openings are checked against actual generated mesh triangles.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
# Actual finite clear volumes and actual bearing surfaces are measured from mesh triangles.
volume_checks=[]
for r in CLEAR_BOXES:
 lo,hi=r['lo'],r['hi'];blockers=[];corners=[(x,y,z) for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]]
 for name,o in byname.items():
  for index,t in enumerate(o.data.loop_triangles):
   if triangle_box_intersects([o.matrix_world@o.data.vertices[i].co for i in t.vertices],lo,hi):blockers.append({'mesh':name,'triangle':index})
  for i,p in enumerate(corners):
   if inside(trees[name],p):blockers.append({'mesh':name,'contained_corner':i})
 assert not blockers,('Finite clear volume obstructed',r,blockers)
 volume_checks.append(dict(r,actual_triangle_or_containment_blockers=blockers))
floor_checks=[]
for r in FLOOR_RAYS:
 hits=[]
 for name,t in trees.items():
  point,normal,face,distance=t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])
  if point is not None:hits.append((distance,name,point,normal))
 assert hits,('No actual bearing surface',r)
 distance,name,point,normal=min(hits,key=lambda row:row[0]);assert name==r['expected_mesh'] and abs(point.z-r['expected_z_m'])<1.1e-6 and normal.z>.99,(r,name,list(point))
 floor_checks.append(dict(r,first_hit_mesh=name,first_hit_m=list(point),normal=list(normal)))
booth_evidence={'clear_volumes':volume_checks,'actual_bearing_surface_probes':floor_checks,'nominal_rear_width_m':.86,'nominal_rear_clear_height_above_floor_m':2.03,'floor_step_m':.10,'nominal_service_width_m':1.256,'nominal_service_height_above_counter_m':.976,'nominal_interior_wall_width_m':1.56,'interior_ceiling_z_m':2.31,'counter_top_z_m':1.08,'nominal_wall_thickness_m':.12,'counter_brackets':2,'no_navigation_accessibility_compliance_or_family_fit_claim':True}
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
 'single_prop_count':1,'ticket_booth_geometry':booth_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/carnival/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,1.45));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=3.65;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(4,-6,4.0),'gray-back3q':(-4,6,3.8)} if gray else {
 'thumbnail':(4,-6,4.0),'qa-front':(0,-7,1.45),'qa-side':(7,0,1.45),'qa-top':(0,0,8),
 'qa-back':(0,7,1.45),'qa-wireframe':(4,-6,4.0)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
if '--wireframe-only' in sys.argv:views={'qa-wireframe':views['qa-wireframe']}
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=3.65
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.003;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,1.45)),('silhouette-128-side',(7,0,1.45))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
