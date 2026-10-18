"""Original freestanding centre-strap tennis training net; one static visual prop.
Single continuous thick perforated sagging mesh, two independent floor posts,
finite side ties and a centre strap connected to its own ground anchor.
Metres, native Z up, front -Y. No sports standard, motion or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-freestanding-centre-strap-tennis-net-01';VERSION='1.0.0';TITLE='Freestanding Centre-Strap Tennis Training Net'
DESCRIPTION=('One original complete static freestanding tennis training net, counted as one prop. Two independent floor-standing blue posts have broad chamfered feet. Six finite side ties connect the posts to the ivory side borders. One continuous opaque 12 mm thick black net has eighty genuine through-openings, a visible shallow centre sag, a thick ivory top ribbon and positive bottom clearance. An ivory central strap crosses the reinforced centre strand and connects the top ribbon to an independent finite ground anchor. All solids have finite support paths to the three ground patches. The single-plane mesh, ground posts and central anchor are original, not a scaled table-tennis net or a football goal with faces removed. Four constant PBR materials, no image textures, transparency, typography, logos, balls, rackets, scenery or animation. Metres, native Z up, front -Y, ground-centre datum. Static non-standard training-net appearance only: no regulation dimensions, tournament or rule compliance, tension analysis, installation compatibility, ball impact, cloth or strap motion, stability, load capacity, manufacturing tolerance, sports equipment certification or safety guarantee.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};CONTACTS=[];FLOOR_PROBES=[];WALL_PROBES=[];ISOLATED_VOLUMES={};HOLES=[];SIDE_TIES=[]
PALETTE=[('Posts_DeepBlue',(.025,.13,.19,1),.44,.36),('Net_Charcoal',(.025,.032,.033,1),.78,.0),('Bands_WarmIvory',(.89,.875,.79,1),.64,.0),('Anchor_BrushedMetal',(.29,.35,.38,1),.38,.68)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'no_surface_overlays':True}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def transform(p,c,u,v,w):return add(c,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def mesh(name,vs,fs,mat,role):
 assert name not in G;G[name]={'vertices':[tuple(0. if abs(c)<1e-10 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':mat,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(name,c,size,mat,role):
 return mesh(name,[(c[0]+a*size[0]/2,c[1]+b*size[1]/2,c[2]+d*size[2]/2) for d in [-1,1] for b in [-1,1] for a in [-1,1]],BOX_FACES,mat,role)
def prism_z(name,outline,z0,z1,mat,role):
 n=len(outline);vs=[(x,y,z) for z in [z0,z1] for x,y in outline];fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def prism_y_data(outline,y0,y1):
 n=len(outline);return [(x,y,z) for y in [y0,y1] for x,z in outline],[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
def prism_y(name,outline,y0,y1,mat,role):
 vs,fs=prism_y_data(outline,y0,y1);return mesh(name,vs,fs,mat,role)
def link(a,b,p,axis=(0,1,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void_box(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]],'faces':BOX_FACES,'role':role}
HALF=2.28;COLS=16;ROWS=5;HEIGHT=.82;NET_DEPTH=.012
XS=[-HALF+2*HALF*c/COLS for c in range(COLS+1)]
def sag_bottom(x):return .12+.12*(x/HALF)**2
def top(x):return sag_bottom(x)+HEIGHT
# One connected closed boundary formed by welded rectangular annular cells.
# Shared cell seams have no internal faces. Every hole has its full sidewall.
net='Net_ContinuousSaggingPerforatedMesh';vs=[];fs=[];lookup={}
def vid(p):
 p=tuple(round(c,7) for c in p)
 if p not in lookup:lookup[p]=len(vs);vs.append(p)
 return lookup[p]
for row in range(ROWS):
 for col in range(COLS):
  x0,x1=XS[col:col+2];t0=HEIGHT*row/ROWS;t1=HEIGHT*(row+1)/ROWS
  xl=x0+(.036 if col==0 else .048 if abs(x0)<1e-8 else .007)
  xr=x1-(.036 if col==COLS-1 else .048 if abs(x1)<1e-8 else .007)
  bottom_offset=.011 if row==0 else .007;upper_offset=.018 if row==ROWS-1 else .007
  outer=[(x0,sag_bottom(x0)+t0),(x1,sag_bottom(x1)+t0),(x1,sag_bottom(x1)+t1),(x0,sag_bottom(x0)+t1)]
  inner=[(xl,sag_bottom(xl)+t0+bottom_offset),(xr,sag_bottom(xr)+t0+bottom_offset),(xr,sag_bottom(xr)+t1-upper_offset),(xl,sag_bottom(xl)+t1-upper_offset)]
  ob=[vid((x,-.006,z)) for x,z in outer];ot=[vid((x,.006,z)) for x,z in outer];ib=[vid((x,-.006,z)) for x,z in inner];it=[vid((x,.006,z)) for x,z in inner]
  for i in range(4):
   j=(i+1)%4;fs.extend([(ob[i],ib[i],ib[j],ob[j]),(ot[i],ot[j],it[j],it[i]),(ib[i],it[i],it[j],ib[j])])
   if (i==0 and row==0) or (i==1 and col==COLS-1) or (i==2 and row==ROWS-1) or (i==3 and col==0):fs.append((ob[i],ob[j],ot[j],ot[i]))
  # Exact linear opening boundaries, inset from all four edges and extending
  # beyond both complete front and back surfaces. These are finite volumes.
  px0=xl+.002;px1=xr-.002
  def low_at(x):return inner[0][1]+(x-xl)/(xr-xl)*(inner[1][1]-inner[0][1])+.002
  def high_at(x):return inner[3][1]+(x-xl)/(xr-xl)*(inner[2][1]-inner[3][1])-.002
  poly=[(px0,low_at(px0)),(px1,low_at(px1)),(px1,high_at(px1)),(px0,high_at(px0))]
  pv,pf=prism_y_data(poly,-.029,.029);label='NetHole_R%02d_C%02d'%(row,col)
  VOID_VOLUMES[label]={'vertices':pv,'faces':pf,'role':'complete conservative finite through-opening; all four inner walls and full net depth tested','nominal_boundary_inset_m':.002}
  HOLES.append({'label':label,'row':row,'column':col,'inner_outline_xz_m':inner,'finite_probe':label})
  center=((px0+px1)/2,-.029,(low_at((px0+px1)/2)+high_at((px0+px1)/2))/2)
  GAPS.append({'label':label,'origin_m':center,'direction':(0,1,0),'length_m':.058})
mesh(net,vs,fs,1,'one continuous closed 12 mm thick opaque welded grid; eighty real full-depth through holes, reinforced center strand and shallow static sag')
# The separate top ribbon follows the same sampled sag curve as the net edge.
band_xs=[-2.292]+XS+[2.292]
outline=[(x,top(x)-.008) for x in band_xs]+[(x,top(x)+.047) for x in reversed(band_xs)]
topband=prism_y('Band_ContinuousSaggingTopRibbon',outline,-.022,.022,2,'continuous 55 mm high thick top ribbon, finite embedded top-edge seat, no tension simulation')
for x in [-1.14,0,1.14]:link(net,topband,(x,0,top(x)-.004),axis=(0,1,0),spread=.002)
for sign,label in [(-1,'Left'),(1,'Right')]:
 px=sign*2.48;nx=sign*HALF
 foot=prism_z('Foot_'+label,[(px+x,y) for x,y in [(-.12,-.36),(.12,-.36),(.16,-.24),(.16,.24),(.12,.36),(-.12,.36),(-.16,.24),(-.16,-.24)]],0,.08,0,'independent chamfered broad ground foot; full finite underside contact, no anti-tip rating');FEET.append(foot)
 post=box('Post_'+label,(px,0,.605),(.09,.10,1.09),0,'independent floor post with finite base seat; no table or return frame')
 link(foot,post,(px,0,.07),axis=(0,1,0),spread=.018)
 border=box('Band_'+label+'VerticalBorder',(nx,0,(sag_bottom(nx)+top(nx)+.020)/2),(.052,.036,HEIGHT+.050),2,'thick side border with full finite net-edge seats and three fixed side ties')
 link(net,border,(sign*2.267,0,.61),axis=(0,0,1),spread=.018)
 link(topband,border,(sign*2.270,0,top(2.270)+.012),axis=(0,1,0),spread=.006)
 for k,z in enumerate([.32,.64,1.025]):
  tie=box('Tie_'+label+'_%02d'%k,(sign*2.37,0,z),(.16,.024,.024),3,'finite solid fixed side connector between border and post; net face remains a single plane')
  link(border,tie,(sign*2.298,0,z),axis=(0,1,0),spread=.004)
  link(post,tie,(sign*2.442,0,z),axis=(0,1,0),spread=.004)
  SIDE_TIES.append({'mesh':tie,'post':post,'border':border,'height_m':z})
 for k,(low,high) in enumerate([(.36,.60),(.68,.98)]):void_box('BetweenSideTies_'+label+'_%d'%k,(min(sign*2.319,sign*2.425),-.027,low),(max(sign*2.319,sign*2.425),.027,high),'complete finite side gap between post and net border, excluding the fixed ties')
anchor=prism_z('Anchor_IndependentCentreGroundSeat',[(-.11,-.12),(.11,-.12),(.13,-.10),(.13,.10),(.11,.12),(-.11,.12),(-.13,.10),(-.13,-.10)],0,.055,3,'independent finite ground anchor under center strap; visual support only');FEET.append(anchor)
strap=box('Strap_CentreToGroundAnchor',(0,0,(.030+top(0)+.038)/2),(.064,.028,top(0)+.038-.030),2,'continuous thick central strap from top ribbon along reinforced centre strand into the independent ground anchor')
link(strap,anchor,(0,0,.042),axis=(1,0,0),spread=.016)
link(strap,net,(0,0,.53),axis=(0,0,1),spread=.028)
link(strap,topband,(0,0,top(0)+.020),axis=(1,0,0),spread=.015)
# Positive complete under-net ground clearance, split by the central strap/anchor.
for label,lo,hi in [('Left',-2.24,-.15),('Right',.15,2.24)]:void_box('BelowNet_'+label,(lo,-.030,.005),(hi,.030,.105),'complete finite under-net empty ground-clearance slab excluding only the declared central strap and anchor')
TENNIS_NET_CONTRACT={'single_prop_count':1,'net_mesh':net,'column_count':COLS,'row_count':ROWS,'true_hole_count':COLS*ROWS,'net_thickness_m':NET_DEPTH,'net_span_m':2*HALF,'center_bottom_z_m':sag_bottom(0),'end_bottom_z_m':sag_bottom(HALF),'center_top_z_m':top(0),'end_top_z_m':top(HALF),'sag_m':.12,'top_band':topband,'centre_strap':strap,'centre_anchor':anchor,'side_ties':SIDE_TIES,'ground_meshes':FEET,'holes':HOLES,'expected_closed_boundary_euler_characteristic':2-2*COLS*ROWS,'static_nonstandard_training_appearance_only':True,'regulation_tension_motion_impact_stability_or_safety_claim':False}
def measure_tennis_net_geometry(vertices):
 assert set(vertices)==set(G),'Changed complete tennis-net mesh set'
 rows=[]
 for name,g in G.items():
  actual=sorted(set(tuple(float(c) for c in p) for p in vertices[name]));expected=sorted(set(g['vertices']))
  assert len(actual)==len(expected),('Changed unique surface vertex count',name)
  matches=[[i for i,q in enumerate(expected) if math.dist(p,q)<2e-7] for p in actual]
  assert all(len(i)==1 for i in matches) and len({i[0] for i in matches})==len(expected),('Actual surface lacks bijective unique source match',name)
  rows.append({'mesh':name,'unique_vertices':len(actual),'maximum_position_error_m':max(math.dist(p,expected[i[0]]) for p,i in zip(actual,matches)),'unique_bijective_surface_match':True})
 return dict(TENNIS_NET_CONTRACT,actual_components=rows,full_finite_void_count=len(VOID_VOLUMES),full_isolated_volume_count=len(ISOLATED_VOLUMES),material_contract=MATERIAL_CONTRACT)
FOCUS=(0,0,.575);ORTHO=6.20
CAMERAS={'gray-front3q':(4,-8,5.30),'gray-back3q':(-4,8,5.30),'thumbnail':(4,-8,5.30),'qa-front':(0,-10,4.8),'qa-side':(10,0,4.8),'qa-top':(0,0,8),'qa-back':(0,10,4.8),'qa-wireframe':(4,-8,5.30),'silhouette-128-front':(0,-10,4.8),'silhouette-128-side':(10,0,4.8)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneCompleteFreestandingTennisNet',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground-centre design datum X=0, Y=0, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
isolated_finite_checks=[]
for name,probe in ISOLATED_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False);target=probe['target_mesh'];obj=byname[target];tree=trees[target]
 crossing=tree.overlap(pt);model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)];probe_inside=[i for i,v in enumerate(pv) if inside(tree,v)]
 assert not crossing and not model_inside and not probe_inside,('Isolated finite opening obstructed',name,target,len(crossing),model_inside,probe_inside)
 isolated_finite_checks.append({'probe':name,'target_mesh':target,'nominal_boundary_inset_m':probe['nominal_boundary_inset_m'],'axis_depth_range_m':probe['axis_depth_range_m'],'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside),'complete_finite_isolated_volume_empty':True})
tennis_evidence=measure_tennis_net_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'tennis_net_geometry':tennis_evidence,'finite_empty_volumes':void_volume_checks,'finite_isolated_openings':isolated_finite_checks,'finite_seated_contacts':CONTACTS,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
focus=Vector(FOCUS);asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
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
