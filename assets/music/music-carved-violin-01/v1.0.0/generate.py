"""Original single static carved violin, metres, Z up, lying on its flat back.
Four strings, fretless fingerboard, real f holes/cavity, bridge, pegbox and scroll.
Standalone bpy-only source; --geometry-only / --no-render / --gray-only /
--preview-only / --extra-views. Every image renders a fresh actual GLB import.
No musical sound, animation, playable dimensions or instrument certification.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='music-carved-violin-01';VERSION='1.0.0';TITLE='Carved Four-String Violin'
DESCRIPTION=('Original static low-poly single violin lying on a finite flat back. A warm amber waisted body has a real hollow rib cavity and two cut-through f-shaped soundholes. '
 'Four individual solid strings run from a supported tailpiece across a two-foot arched bridge and a fretless curved ebony fingerboard to the nut and four alternate-sided pegs in an open pegbox. '
 'A carved spiral scroll, honey maple neck, fine purfling rim, tail saddle, button and paired tailgut complete the single editable instrument. '
 'All named components are physically connected to the grounded backplate; actual cavity, f-hole apertures, string/fingerboard clearance and bridge-foot support are checked. '
 'Approximately 0.67 m long visual proportions; metres, source Z up, scroll toward +Y and origin at the ground projection of the body centre. '
 'Six solid PBR materials, no textures or external dependencies. Distinct violin anatomy, not a reduced six-string fretted guitar. '
 'Static game visual only; no bow, case, stand, sound, animation, playability, instrument-size accuracy or safety certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('AmberSpruce_Top',(.48,.19,.048,1),.43,0),('WarmMaple_BackRibs',(.27,.075,.020,1),.48,0),
 ('HoneyMaple_NeckBridge',(.65,.38,.13,1),.56,0),('Ebony_Fittings',(.025,.019,.015,1),.38,0),
 ('Ivory_NutSaddle',(.66,.58,.40,1),.48,0),('Silver_String',(.42,.45,.43,1),.32,.72)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;mats.append(m)
root=bpy.data.objects.new('CarvedFourStringViolin',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_direction']='-Y';root['scroll_direction']='+Y';root['static_visual_only']=True
root['origin_datum']='ground projection of body centre';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={};links=[]
def mesh(name,vs,fs,material,role,asset=True):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(round(float(c),6) for c in v) for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if asset:
  o.parent=root;me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role)
def prism(name,xy,low,high,material,role,axis='Z',asset=True):
 n=len(xy)
 vs=[(x,y,z) if axis=='Z' else (x,z,y) for z in [low,high] for x,y in xy]
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role,asset)
def inset(poly,d):
 # Intersect inward-offset adjacent edges; unlike centroid scaling this preserves C-bout corner nesting.
 def cross(a,b):return a[0]*b[1]-a[1]*b[0]
 def sub(a,b):return (a[0]-b[0],a[1]-b[1])
 sign=1 if sum(cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))>0 else -1;out=[]
 for i,p in enumerate(poly):
  a=poly[i-1];b=poly[(i+1)%len(poly)];u=sub(p,a);v=sub(b,p);lu=math.hypot(*u);lv=math.hypot(*v)
  q=(p[0]-sign*d*u[1]/lu,p[1]+sign*d*u[0]/lu);r=(p[0]-sign*d*v[1]/lv,p[1]+sign*d*v[0]/lv)
  den=cross(u,v);assert abs(den)>1e-12;t=cross(sub(r,q),v)/den;out.append((q[0]+u[0]*t,q[1]+u[1]*t))
 return out
def ring(name,outer,inner,low,high,material,role):
 n=len(outer);vs=[(x,y,z) for z in [low,high] for shape in [outer,inner] for x,y in shape];fs=[]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,material,role)
def tube(name,points,radius,material,role,n=10,wide_x=None):
 points=[Vector(p) for p in points];vs=[]
 for i,p in enumerate(points):
  axis=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
  if wide_x is not None:u=Vector((1,0,0));v=axis.cross(u).normalized()
  else:
   ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0));u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
  vs.extend(p+math.cos(math.tau*j/n)*(wide_x or radius)*u+math.sin(math.tau*j/n)*radius*v for j in range(n))
 fs=[tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
 for i in range(len(points)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 return mesh(name,vs,fs,material,role)
def joint(a,b,points):links.append((a,b,[Vector(p) for p in points]))
def cut(target,cutter):
 bpy.context.view_layer.objects.active=target;mod=target.modifiers.new('Real cut through aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Hand-drawn violin-specific C bouts, four pointed corners and separate upper/lower lobes.
half=[(.000,-.225),(.034,-.221),(.063,-.210),(.087,-.193),(.105,-.171),(.113,-.146),(.114,-.119),(.108,-.092),
 (.093,-.071),(.101,-.057),(.078,-.055),(.067,-.038),(.064,-.017),(.069,.004),(.079,.020),(.099,.021),
 (.091,.037),(.098,.058),(.099,.084),(.092,.111),(.076,.134),(.052,.151),(.026,.161),(.000,.164)]
outline=half+[(-x,y) for x,y in reversed(half[1:-1])]
back=prism('Body_Backplate',outline,0,.010,1,'single finite planar grounded backplate')
inner=inset(outline,.008)
ring('Body_RibRing',inset(outline,.003),inner,.007,.047,1,'inset waisted hollow rib wall beneath overhanging plates')
prism('Body_Soundboard',outline,.042,.052,0,'front soundboard with real cut-through paired f holes')
ring('Purfling_Rim',inset(outline,.002),inset(outline,.0038),.051,.053,3,'thin continuous inlaid-style rim')
# Swept, tapered S-channel outlines with bulbous eyes make true f-shaped openings.
fcentres=[(.056,.042,.0070),(.055,.036,.0080),(.048,.029,.0040),(.042,.018,.0036),(.040,.003,.0034),
 (.042,-.013,.0034),(.047,-.029,.0035),(.052,-.046,.0035),(.055,-.064,.0036),(.054,-.082,.0040),(.048,-.096,.0045),(.042,-.104,.0080),(.042,-.113,.0070)]
f_windows=[]
for sign,side in [(-1,'Left'),(1,'Right')]:
 pts=[Vector((sign*x,y)) for x,y,r in fcentres];left=[];right=[]
 for i,p in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized();n=Vector((-t.y,t.x));r=fcentres[i][2]
  left.append(tuple(p+n*r));right.append(tuple(p-n*r))
 shape=left+list(reversed(right));c=prism('Temporary_F_Cutter_'+side,shape,.035,.060,0,'cutter',asset=False);cut(byname['Body_Soundboard'],c)
 for i in [1,2,4,6,8,10,11]:
  x,y,r=fcentres[i];f_windows.append({'side':side,'centre_m':[sign*x,y,.047],'radius_m':.0012})
# Contact witnesses are actual interior points, independently checked after GLB import.
for x,y in [(.109,-.14),(-.109,-.14),(.094,.08)]:
 joint('Body_RibRing','Body_Backplate',[(x,y+d,.0085) for d in [-.001,0,.001]])
 joint('Body_Soundboard','Body_RibRing',[(x,y+d,.0445) for d in [-.001,0,.001]])
# Purfling lies in the upper soundboard skin; points are away from f holes.
joint('Purfling_Rim','Body_Soundboard',[(.1111,-.119+d,.0515) for d in [-.0005,0,.0005]])
# Tapered maple neck. Fingerboard is curved across X and has no fret geometry.
neckxy=[(-.022,.137),(.022,.137),(.013,.344),(-.013,.344)]
vs=[]
for upper in [False,True]:
 for x,y in neckxy:
  t=(y-.137)/(.344-.137);vs.append((x,y,(.048+.016*t) if not upper else (.078+.005*t)))
mesh('Maple_Neck',vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],2,'tapered neck and heel joined into upper rib body')
joint('Maple_Neck','Body_Soundboard',[(x,.147,.050) for x in [-.012,0,.012]])
# Each end has a curved top cross-section; planar bottom remains embedded in neck.
N=12;vs=[]
for y,w,low,top in [(-.005,.025,.070,.081),(.338,.014,.079,.090)]:
 vs.extend([(x,y,top-.004*(x/w)**2) for x in [-w+2*w*i/N for i in range(N+1)]])
 vs.extend([(w,y,low),(-w,y,low)])
k=N+3;fs=[tuple(reversed(range(k))),tuple(k+i for i in range(k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
mesh('Ebony_FretlessFingerboard',vs,fs,3,'arched continuous fretless fingerboard')
joint('Ebony_FretlessFingerboard','Maple_Neck',[(x,.25,.078) for x in [-.007,0,.007]])
box('Nut',(0,.333,.089),(.029,.007,.008),4,'four string upper support at fingerboard end')
joint('Nut','Ebony_FretlessFingerboard',[(x,.332,.088) for x in [-.008,0,.008]])
# Open pegbox: sloping floor, two separate cheeks and a rear root block.
box('Pegbox_Floor',(0,.374,.078),(.025,.074,.008),2,'real recessed pegbox floor')
joint('Pegbox_Floor','Maple_Neck',[(x,.341,.079) for x in [-.006,0,.006]])
for sign,side in [(-1,'Left'),(1,'Right')]:
 xy=[(.337,.076),(.411,.076),(.411,.121),(.337,.101)]
 # Build along X using (Y,Z) cross-section.
 n=len(xy);v=[(x,y,z) for x in [sign*.012-sign*.003,sign*.012+sign*.003] for y,z in xy]
 o=mesh('Pegbox_Cheek_'+side,v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],2,'raised wall of open pegbox')
 joint(o.name,'Pegbox_Floor',[(sign*.011,y,.078) for y in [.35,.37,.39]])
box('Pegbox_ScrollRoot',(0,.410,.095),(.028,.018,.040),2,'rear pegbox wall and scroll root')
joint('Pegbox_ScrollRoot','Pegbox_Cheek_Left',[(-.012,.407,z) for z in [.09,.10,.11]])
joint('Pegbox_ScrollRoot','Pegbox_Cheek_Right',[(.012,.407,z) for z in [.09,.10,.11]])
peg_data=[]
for i,(y,z) in enumerate([(.350,.086),(.366,.091),(.382,.097),(.398,.105)]):
 sign=-1 if i%2==0 else 1;name=f'Peg_{i+1:02d}_Shaft'
 tube(name,[(-.023,y,z),(.023,y,z)],.0028,3,'through-pegbox supported tuning shaft',12)
 for s,side in [(-1,'Left'),(1,'Right')]:joint(name,'Pegbox_Cheek_'+side,[(s*.012,y+d,z) for d in [-.0007,0,.0007]])
 # Flattened oval tuning button extends from the supported shaft.
 button=f'Peg_{i+1:02d}_Button';xy=[(.007*math.cos(math.tau*j/12),.010*math.sin(math.tau*j/12)) for j in range(12)]
 v=[(sign*.027+xx,y+yy,z+zz) for xx in [-.006,.006] for yy,zz in xy];n=12
 mesh(button,v,[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],3,'alternating flattened oval tuning button')
 joint(button,name,[(sign*.022,y+d,z) for d in [-.0005,0,.0005]])
 peg_data.append((name,y,z))
# True carved spiral volute, not a solid round headstock. Broad X section, open centre.
scroll_points=[]
for i in range(49):
 t=i/48;angle=-math.pi/2+t*math.pi*2.2;r=.022-.0165*t
 scroll_points.append((0,.415+math.cos(angle)*r,.124+math.sin(angle)*r))
tube('Carved_SpiralScroll',scroll_points,.0032,2,'closed spiral scroll with visible open volute centre',12,wide_x=.014)
scroll_witness=Vector(scroll_points[0]).lerp(Vector(scroll_points[1]),.30)
joint('Carved_SpiralScroll','Pegbox_ScrollRoot',[(x,scroll_witness.y,scroll_witness.z) for x in [-.006,0,.006]])
# Two-foot arched violin bridge, central under-arch is genuinely empty.
bridge_shape=[(-.029,.0515),(-.012,.0515),(-.012,.066),(-.008,.073),(0,.077),(.008,.073),(.012,.066),(.012,.0515),(.029,.0515),(.030,.089)]
bridge_shape += [(x,.110-.012*(x/.030)**2) for x in [.030-.005*i for i in range(13)]]
bridge_shape += [(-.030,.089)]
prism('Maple_ArchedBridge',bridge_shape,-.058,-.052,2,'single two-foot violin bridge with arch clearance',axis='Y')
for sign,side in [(-1,'Left'),(1,'Right')]:joint('Maple_ArchedBridge','Body_Soundboard',[(sign*x,-.055,.05175) for x in [.017,.021,.025]])
# Tailpiece is held by two real tailgut loops through the saddle/button assembly.
tailxy=[(-.009,-.190),(.009,-.190),(.020,-.111),(.016,-.102),(-.016,-.102),(-.020,-.111)]
prism('Ebony_Tailpiece',tailxy,.066,.075,3,'tapered four-string tailpiece supported by paired tailgut')
box('Tail_Saddle',(0,-.219,.053),(.028,.012,.010),3,'embedded tail saddle')
joint('Tail_Saddle','Body_Soundboard',[(x,-.217,.050) for x in [-.006,0,.006]])
tube('Tail_EndButton',[(0,-.241,.029),(0,-.212,.029)],.006,3,'end button anchored into tail rib',16)
joint('Tail_EndButton','Body_RibRing',[(x,-.220,.029) for x in [-.002,0,.002]])
for sign,side in [(-1,'Left'),(1,'Right')]:
 name='Tailgut_'+side;tube(name,[(sign*.006,-.185,.069),(sign*.006,-.219,.056),(sign*.003,-.238,.029)],.0018,3,'closed static tailgut strand attached to tailpiece saddle and end button',10)
 joint(name,'Ebony_Tailpiece',[(sign*.006,-.185-d,.069-d*(.013/.034)) for d in [.0003,.0006,.0009]])
 joint(name,'Tail_Saddle',[(sign*.006,-.219+d,.056+d*.38) for d in [-.0004,0,.0004]])
 joint(name,'Tail_EndButton',[(sign*.003,-.238+d,.029+d*(.027/.019)) for d in [.0003,.0006,.0009]])
string_rows=[]
for i,x in enumerate([-.015,-.005,.005,.015]):
 nx=x*.70;peg,y,z=peg_data[i];bz=.110-.012*(x/.030)**2-.00025
 px=x*.45
 points=[(x,-.125,.07475),(x,-.055,bz),(nx,.333,.09275),(px,.337,.0925),(px,y,z)]
 name=f'String_{i+1:02d}';tube(name,points,.0009,5,'one of exactly four continuous supported solid strings',10)
 joint(name,'Ebony_Tailpiece',[(x,-.125+d,.07475+d*(bz-.07475)/.07) for d in [.0001,.0002,.0003]])
 joint(name,'Maple_ArchedBridge',[(x,-.055+d,bz+d*(.09275-bz)/.388) for d in [-.0001,0,.0001]])
 joint(name,'Nut',[(nx,.333+d,.09275) for d in [-.0001,0,.0001]])
 peg_end=Vector(points[-1]);peg_direction=(Vector(points[-2])-peg_end).normalized()
 joint(name,peg,[peg_end+peg_direction*d for d in [.0002,.0004,.0006]])
 string_rows.append({'name':name,'centreline_m':[list(p) for p in points],'radius_m':.0009,'support_names':['Ebony_Tailpiece','Maple_ArchedBridge','Nut',peg]})
# Apply deterministic triangulation, recalculate closed winding and quantize positions.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for v in o.data.vertices:v.co=Vector(tuple(round(float(c),6) for c in v.co))
 o.data.update()
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={};extents={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-13 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-11 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 vv=[o.matrix_world@v.co for v in o.data.vertices];trees[o.name]=BVHTree.FromPolygons(vv,[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
 extents[o.name]=([min(v[k] for v in vv) for k in range(3)],[max(v[k] for v in vv) for k in range(3)])
def inside(tree,point):
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(128):
   q,_,_,_=tree.ray_cast(p,d,2)
   if q is None:break
   hits+=1;p=q+d*1e-6
  else:raise AssertionError('Uncertain ray parity')
  if not hits%2:return False
 return True
joints=[]
for a,b,points in links:
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3])
  assert inside(trees[a],p) and inside(trees[b],p) and clearance>.000015,('Invalid physical joint',a,b,list(p),clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
adj={o.name:set() for o in parts}
for j in joints:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
feet=['Body_Backplate'];seen=set(feet);todo=list(feet)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
# Ground is the actual finite planar underside of the back, not an AABB or tangent.
supports=[]
for name in feet:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.04;supports.append({'name':name,'area_m2':area,'triangles':patch})
# Each actual f opening has seven local windows, five rays through the whole soundboard.
apertures=[]
def clear_ray(label,start,direction,length):
 start,direction=Vector(start),Vector(direction).normalized();hits=[]
 for name,tree in trees.items():
  q,_,_,_=tree.ray_cast(start,direction,length)
  if q is not None:hits.append(name)
 assert not hits,('Blocked real aperture',label,list(start),hits)
 return {'start_m':list(start),'direction':list(direction),'length_m':length}
for w in f_windows:
 x,y,z=w['centre_m'];r=w['radius_m'];rays=[]
 for dx,dy in [(0,0),(-r,-r),(-r,r),(r,-r),(r,r)]:rays.append(clear_ray('f_'+w['side'],(x+dx,y+dy,.035),(0,0,1),.026))
 apertures.append(dict(w,rays=rays))
# Interior cavity samples and horizontally traversing rays never touch the shell.
cavity_points=[(x,y,.026) for x in [-.035,0,.035] for y in [-.17,-.08,.02,.10]]
for p in cavity_points:assert not any(inside(t,p) for t in trees.values()),('Cavity filled',p)
cavity_rays=[clear_ray('body_cavity',(-.04,y,.027),(1,0,0),.08) for y in [-.15,-.08,.02,.10]]
scroll_rays=[clear_ray('scroll_centre',(-.022,.415+dy,.124+dz),(1,0,0),.044) for dy,dz in [(0,0),(.0006,0),(-.0006,0),(0,.0006),(0,-.0006)]]
bridge_arch_rays=[clear_ray('bridge_underarch',(x,-.063,.065),(0,1,0),.016) for x in [-.006,0,.006]]
# The four working string spans stay separated from the fretless board at 12 points each.
string_clearance=[]
for row in string_rows:
 a,b=Vector(row['centreline_m'][1]),Vector(row['centreline_m'][2]);samples=[]
 for i in range(1,13):
  y=.005+i*(.315-.005)/13;t=(y-a.y)/(b.y-a.y);p=a.lerp(b,t);distance=trees['Ebony_FretlessFingerboard'].find_nearest(p)[3]-row['radius_m']
  assert not inside(trees['Ebony_FretlessFingerboard'],p) and distance>.001,(row['name'],list(p),distance)
  samples.append({'centre_m':list(p),'surface_clearance_m':distance})
 string_clearance.append({'name':row['name'],'samples':samples})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7 and triangles<10000
# Complete Principled signature; no texture nodes or linked Principled sockets are allowed.
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
 'four_continuous_strings':string_rows,'string_fingerboard_clearance':string_clearance,'f_hole_aperture_windows':apertures,
 'body_cavity_empty_points_m':cavity_points,'body_cavity_empty_rays':cavity_rays,'scroll_open_centre_rays':scroll_rays,'bridge_underarch_rays':bridge_arch_rays,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/music/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'music','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
 'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':len(mats),'files':files,'status':'review','license':'All rights reserved'}
 (OUT/'metadata.json').write_text(json.dumps(d,indent=2)+'\n')
# All renders operate on a freshly imported exact actual GLB, not a second geometry copy.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'));parts=[o for o in scene.objects if o.type=='MESH']
assert len(parts)==mesh_count and records(parts)==source_records,'Fresh GLB oriented geometry / full solid PBR mismatch'
qa['fresh_actual_glb_guard']={'oriented_geometry_and_full_solid_pbr_match':True,'mesh_count':len(parts)};saveqa()
if '--no-render' in sys.argv or '--geometry-only' in sys.argv:
 metadata();print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.view_settings.view_transform='AgX'
focus=Vector((0,.090,.055));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-1.2,-1.5,2.1),140,1.5),('Fill',(1.3,-.1,1.4),75,1.2),('Rim',(.1,1.5,1.5),110,1.3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=.78;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(.63,-.80,1.30),'gray-back3q':(-.63,.95,1.30)} if gray else {
 'thumbnail':(.63,-.80,1.30),'qa-front':(0,-1.5,.30),'qa-side':(1.5,.090,.30),'qa-top':(0,.090,2),
 'qa-back':(0,1.5,.30),'qa-wireframe':(.63,-.80,1.30)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True;t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.00013;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,.090,2)),('silhouette-128-side',(1.5,.090,.055))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
