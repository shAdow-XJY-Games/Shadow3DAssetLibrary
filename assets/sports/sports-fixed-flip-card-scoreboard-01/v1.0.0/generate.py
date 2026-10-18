"""Original fixed 12 / 08 sports card scoreboard. One static visual prop only.
Metres, Z up, front -Y. True perforated thick cards and seated suspension rings.
No external fonts, textures, logos, live score logic, flipping or animation.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-fixed-flip-card-scoreboard-01';VERSION='1.0.0';TITLE='Fixed 12–08 Sports Card Scoreboard'
DESCRIPTION=('One original static tabletop sports scoreboard with four separately editable perforated thick cards displaying fixed geometric 12 and 08. '
 'Two teal left-team cards and two terracotta right-team cards are separated by a broad real centre gap. Each card has one real circular through-hole and a thick closed suspension ring seated at its lower hole edge; the four rings connect to the rear transverse axle. '
 'Two splayed side frames meet broad flat-bottom feet, with a low rear cross tie. All digit segments are original closed extruded polygon geometry embedded into the card face, without fonts, logos, images or textures. '
 'Constant solid PBR materials, metre scale, source Z up, front -Y and ground-centre origin. All parts have finite support paths and explicit finite empty clearance volumes. '
 'One fixed visual pose and one displayed score only: no flip motion, score changing, automatic scoring, electronics, match rules, team affiliation, installation, load rating, wind resistance, stability test, sports standard or safety certification.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CARD_CENTRES=[(-.285,'LeftTens','1',1),(-.115,'LeftOnes','2',1),(.115,'RightTens','0',2),(.285,'RightOnes','8',2)]
PALETTE=[('Frame_DeepSlate',(.055,.075,.090,1),.54,.35),('LeftTeam_Teal',(.035,.31,.30,1),.6,.05),('RightTeam_Clay',(.57,.17,.095,1),.61,.03),('Digits_WarmIvory',(.93,.89,.75,1),.56,0),('Rings_WarmSteel',(.45,.44,.39,1),.34,.7)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def extrude_y(name,outline,y0,y1,mat,role):
 n=len(outline);vs=[(x,y,z) for y in [y0,y1] for x,z in outline]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def box(name,c,size,mat,role):
 x,y,z=c;w,d,h=size
 return extrude_y(name,[(x-w/2,z-h/2),(x+w/2,z-h/2),(x+w/2,z+h/2),(x-w/2,z+h/2)],y-d/2,y+d/2,mat,role)
def rod(name,a,b,r,mat,role,n=12):
 delta=[b[i]-a[i] for i in range(3)];L=math.sqrt(sum(t*t for t in delta));w=[t/L for t in delta]
 tmp=[0,0,1] if abs(w[2])<.9 else [1,0,0]
 u=[w[1]*tmp[2]-w[2]*tmp[1],w[2]*tmp[0]-w[0]*tmp[2],w[0]*tmp[1]-w[1]*tmp[0]];l=math.sqrt(sum(t*t for t in u));u=[t/l for t in u]
 v=[w[1]*u[2]-w[2]*u[1],w[2]*u[0]-w[0]*u[2],w[0]*u[1]-w[1]*u[0]]
 vs=[tuple(p[j]+r*(u[j]*math.cos(math.tau*i/n)+v[j]*math.sin(math.tau*i/n)) for j in range(3)) for p in [a,b] for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def torus_x(name,x,y,z,R,r,mat,role,n=48,k=8):
 vs=[(x+r*math.sin(math.tau*j/k),y+(R+r*math.cos(math.tau*j/k))*math.cos(math.tau*i/n),z+(R+r*math.cos(math.tau*j/k))*math.sin(math.tau*i/n)) for i in range(n) for j in range(k)]
 fs=[(i*k+j,((i+1)%n)*k+j,((i+1)%n)*k+(j+1)%k,i*k+(j+1)%k) for i in range(n) for j in range(k)]
 return mesh(name,vs,fs,mat,role)
def empty_box(name,c,size,role):
 temp='PROBE_'+name;box(temp,c,size,0,role);VOID_VOLUMES[name]=G.pop(temp)
# Two original broad feet and tapered A-side frames. All static structural
# intersections are intentional finite internal seats, never coplanar mating.
for x,label in [(-.415,'Left'),(.415,'Right')]:
 foot='Foot_'+label;box(foot,(x,.015,.022),(.092,.360,.044),0,'finite planar tabletop contact foot, no mounting or stability rating');FEET.append(foot)
 # One editable, closed A-profile per side keeps the front/rear apex truly joined.
 outline=[(-.145,.029),(-.115,.029),(.036,.487),(.151,.029),(.181,.029),(.055,.550),(.018,.550)]
 # Outline is in local (y,z); extrude along X with exact thickness.
 vs=[(xx,y,z) for xx in [x-.018,x+.018] for y,z in outline];n=len(outline)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 frame='Frame_'+label+'A';mesh(frame,vs,fs,0,'single closed splayed side frame with real triangular lower opening and embedded front/rear foot seats')
 link(frame,foot,(x,-.129,.037),spread=.007);link(frame,foot,(x,.165,.037),spread=.007)
rod('Axle_RearCrossbar',(-.439,.036,.530),(.439,.036,.530),.010,4,'solid transverse rear axle connecting both frame apexes and all four ring roots',n=16)
for x,label in [(-.415,'Left'),(.415,'Right')]:link('Axle_RearCrossbar','Frame_'+label+'A',(x,.036,.530),spread=.008)
rod('Tie_LowerRear',(-.425,.142,.059),(.425,.142,.059),.011,0,'low rear cross tie fixed between side frames without contacting cards',n=12)
# Place rear tie at y=.158 instead of its initial design centre.
G['Tie_LowerRear']['vertices']=[(x,y+.016,z) for x,y,z in G['Tie_LowerRear']['vertices']]
for x,label in [(-.415,'Left'),(.415,'Right')]:link('Tie_LowerRear','Frame_'+label+'A',(x,.158,.059),spread=.006)
# Thick rectangular cards with a genuine circular hole near their top. A radial
# annulus maps the hole onto the outer rectangle, including every corner ray;
# front/back annular faces and the complete cylindrical wall enclose a true bore.
def card(name,cx,mat):
 cz=.520;r=.013;x0=cx-.075;x1=cx+.075;z0=.175;z1=.538
 angles=[math.tau*i/32 for i in range(32)]+[math.atan2(z-cz,x-cx)%math.tau for x,z in [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]];angles=sorted(set(round(a,10) for a in angles));N=len(angles)
 inner=[];outer=[]
 for a in angles:
  dx,dz=math.cos(a),math.sin(a);dist=min((x1-cx)/dx if dx>1e-9 else (x0-cx)/dx if dx< -1e-9 else 1e9,(z1-cz)/dz if dz>1e-9 else (z0-cz)/dz if dz< -1e-9 else 1e9)
  inner.append((cx+r*dx,cz+r*dz));outer.append((cx+dist*dx,cz+dist*dz))
 vs=[(x,y,z) for y in [-.033,-.027] for ring in [outer,inner] for x,z in ring];fs=[]
 for i in range(N):
  j=(i+1)%N
  fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
 mesh(name,vs,fs,mat,'independent 6 mm thick closed card with one genuine 26 mm circular through-hole and complete inner wall')
# Original seven-segment digits. Every bar is a separately editable, closed
# bevel-ended prism positively embedded into its card face; no font assets.
SEGMENTS={'a':(0,.105,'h'),'b':(.039,.053,'v'),'c':(.039,-.053,'v'),'d':(0,-.105,'h'),'e':(-.039,-.053,'v'),'f':(-.039,.053,'v'),'g':(0,0,'h')}
ACTIVE={'1':'bc','2':'abged','0':'abcdef','8':'abcdefg'}
for cx,label,digit,mat in CARD_CENTRES:
 name='Card_'+label;card(name,cx,mat)
 ring='Ring_'+label;torus_x(ring,cx,0,.530,.036,.004,4,'closed 8 mm-thick suspension ring, seated locally on the lower bore edge and fixed to the rear axle; not an animated joint')
 link(ring,'Axle_RearCrossbar',(cx,.0355,.5305),spread=.0015)
 link(name,ring,(cx,-.028,.5068),spread=.0006)
 BORES.append({'mesh':name,'label':label+'_true_card_bore','origin_m':[cx+.008,-.043,.520],'direction':[0,1,0],'length_m':.026})
 GAPS.append({'label':label+'_assembled_bore_clearance','origin_m':[cx+.008,-.043,.520],'direction':[0,1,0],'length_m':.026})
 empty_box('Bore_'+label+'_SideClearance',(cx+.008,-.030,.520),(.005,.026,.008),'complete conservative right-hand finite clearance beside the suspension ring inside the card through-hole')
 empty_box('Ring_'+label+'_CoreClearance',(cx,0,.530),(.014,.032,.032),'complete conservative finite empty core of the thick closed ring; excludes axle and seated card contact')
 for seg in ACTIVE[digit]:
  ox,oz,orient=SEGMENTS[seg];x=cx+ox;z=.330+oz
  # 6-vertex chamfered hexagonal bar. Positive 4 mm gaps between bars.
  L=.059 if orient=='h' else .078;W=.013
  shape=[(-L/2+W/2,-W/2),(L/2-W/2,-W/2),(L/2,0),(L/2-W/2,W/2),(-L/2+W/2,W/2),(-L/2,0)]
  outline=[(x+(a if orient=='h' else b),z+(b if orient=='h' else a)) for a,b in shape]
  dn='Digit_'+label+'_'+digit+'_'+seg;extrude_y(dn,outline,-.039,-.0315,3,'original closed extruded geometric numeral segment with finite embedded card-face seat')
  link(dn,name,(x,-.0322,z),axis=(0,0,1),spread=.002)
empty_box('BetweenTeams_FullCardGap',(0,-.030,.355),(.068,.030,.350),'full conservative central visual separation between the left and right card groups')
for label,x in [('Left',-.20),('Right',.20)]:
 empty_box('Cards_'+label+'_RearStandGap',(x,.060,.325),(.260,.100,.280),'complete finite rear card clearance below suspension axle and above low tie')
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
root=bpy.data.objects.new('OneFixedSportsCardScoreboard',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
void_volume_checks=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
# Actual card thickness and perforated boundary evidence.
card_checks=[]
for cx,label,digit,mat in CARD_CENTRES:
 o=byname['Card_'+label];vv=[o.matrix_world@p.co for p in o.data.vertices];thickness=max(p.y for p in vv)-min(p.y for p in vv)
 assert abs(thickness-.006)<1e-6
 card_checks.append({'mesh':o.name,'displayed_digit':digit,'actual_thickness_m':thickness,'ring':'Ring_'+label,'digit_segment_count':len(ACTIVE[digit])})
scoreboard_evidence={'independent_card_count':4,'fixed_displayed_score':'12 / 08','cards':card_checks,'finite_void_volumes':VOID_VOLUMES,'finite_volume_empty_checks':void_volume_checks,'static_display_only':True,'flip_animation_or_scoring_logic_or_safety_claim':False}
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
 'single_prop_count':1,'scoreboard_working_geometry':scoreboard_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/sports/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.285));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.12;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,3.5),'gray-back3q':(3,5,3.5)} if gray else {
 'thumbnail':(-3,-5,3.5),'qa-front':(0,-7,.285),'qa-side':(7,0,.285),'qa-top':(0,0,8),
 'qa-back':(0,7,.285),'qa-wireframe':(-3,-5,3.5)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.12
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0015;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.285)),('silhouette-128-side',(7,0,.285))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
