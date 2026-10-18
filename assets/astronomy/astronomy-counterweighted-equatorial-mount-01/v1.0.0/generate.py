"""Original static counterweighted equatorial mount; metres, Z up.
The two orthogonal shafts, hollow bearing sleeves, empty saddle and pierced
counterweight are real geometry. Fixed visual pose only, no tracking/fit claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='astronomy-counterweighted-equatorial-mount-01';VERSION='1.0.0';TITLE='Counterweighted Equatorial Mount'
DESCRIPTION=('One original fixed equatorial-mount stand with a new three-leg finite-foot support, a wedged 45-degree polar bearing sleeve, perpendicular declination spindle, empty raised-rail instrument saddle and a genuinely bored counterweight threaded over its rod. '
 'The weight is seated on a separate stop collar and a terminal retention cap remains below it. Hollow sleeves have visible radial gaps around their shafts; positive-volume shoulder seats fix this static arrangement. '
 'Separate closed editable meshes, five solid PBR materials, no textures or external dependencies. Metres, Z up, ground-centre origin. One complete stand counts as one prop. '
 'Only this pictured fixed pose is checked. No telescope included and no compatibility with existing telescope assets claimed. No tracking, alignment, rotation range, balancing, precision measurement, load rating, manufacture, installation or safety guarantee.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[]
PALETTE=[('Frame_DeepTeal',(.045,.18,.20,1),.55,.32),('Shaft_BrushedSteel',(.42,.49,.52,1),.27,.72),('Housing_Seafoam',(.36,.53,.51,1),.46,.25),('Foot_Graphite',(.032,.045,.048,1),.82,0),('Hardware_WarmBrass',(.69,.38,.095,1),.36,.65)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def basis(axis):
 a=unit(axis);u=unit(cross(a,(0,0,1) if abs(a[2])<.9 else (0,1,0)));v=cross(a,u);return a,u,v
def profile(name,origin,axis,rings,mat,role,n=24):
 a,u,v=basis(axis);vs=[];fs=[]
 for t,r in rings:
  for i in range(n):q=math.tau*i/n;vs.append(add(add(origin,mul(a,t)),add(mul(u,r*math.cos(q)),mul(v,r*math.sin(q)))))
 for j in range(len(rings)-1):
  for i in range(n):k=(i+1)%n;fs.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
 fs += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,mat,role)
def tube(name,origin,axis,lo,hi,outer,inner,mat,role,n=24):
 a,u,v=basis(axis);vs=[];fs=[]
 for t,r in [(lo,outer),(hi,outer),(lo,inner),(hi,inner)]:
  for i in range(n):q=math.tau*i/n;vs.append(add(add(origin,mul(a,t)),add(mul(u,r*math.cos(q)),mul(v,r*math.sin(q)))))
 for i in range(n):
  k=(i+1)%n;fs += [(i,k,n+k,n+i),(2*n+k,2*n+i,3*n+i,3*n+k),(k,i,2*n+i,2*n+k),(n+i,n+k,3*n+k,3*n+i)]
 BORES.append({'mesh':name,'origin_m':add(origin,mul(a,lo-.015)),'direction':a,'length_m':hi-lo+.030})
 return mesh(name,vs,fs,mat,role)
def box(name,c,size,mat,role,axes=((1,0,0),(0,1,0),(0,0,1))):
 vs=[]
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
  vs.append(add(c,add(mul(axes[0],x*size[0]/2),add(mul(axes[1],y*size[1]/2),mul(axes[2],z*size[2]/2)))))
 return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,role)
def rod(name,a,b,r,mat,role,n=16):return profile(name,a,sub(b,a),[(0,r),(math.sqrt(dot(sub(b,a),sub(b,a))),r)],mat,role,n)
# Entirely new low tripod: finite rubber soles, tapered-looking angled metal members,
# three radial spreaders and an elevated hub. Feet never collapse to point contact.
profile('Tripod_Crown',(0,0,0),(0,0,1),[(.710,.125),(.790,.145),(.830,.145)],0,'solid three-leg crown and upper azimuth plinth')
profile('Tripod_SpreaderHub',(0,0,0),(0,0,1),[(.350,.065),(.410,.065)],4,'central three-arm spreader junction')
for k in range(3):
 ang=math.radians(-90+120*k);rad=(math.cos(ang),math.sin(ang),0);bottom=add(mul(rad,.50),(0,0,.045));top=add(mul(rad,.10),(0,0,.770));fn='Tripod_Foot_%d'%k;ln='Tripod_Leg_%d'%k;bn='Tripod_Brace_%d'%k
 box(fn,add(mul(rad,.50),(0,0,.025)),(.14,.12,.05),3,'finite flat rubber sole at ground datum');FEET.append(fn)
 rod(ln,bottom,top,.037,1,'solid inclined tripod leg, seated in foot and crown')
 link(fn,ln,add(bottom,mul(unit(sub(top,bottom)),.003)),rad,.002)
 link(ln,'Tripod_Crown',add(top,(0,0,-.012)),rad,.002)
 # Exact leg centre at z=.385; radial brace reaches its interior.
 rr=.50+(.385-.045)/(.770-.045)*(.10-.50);outer=add(mul(rad,rr),(0,0,.385));inner=add(mul(rad,.038),(0,0,.385))
 rod(bn,inner,outer,.014,0,'radial spreader positively seated in leg and spreader hub')
 link(bn,'Tripod_SpreaderHub',add(mul(rad,.048),(0,0,.385)),(0,0,1),.002)
 link(bn,ln,add(outer,mul(rad,-.009)),(0,0,1),.002)
# Triangular latitude wedge is a real closed prism, not a painted tilt mark.
vv=[(x,y,z) for x in [-.085,.085] for y,z in [(-.14,.816),(.16,.816),(.16,1.052)]]
mesh('Polar_LatitudeWedge',vv,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],0,'closed triangular prism supporting underside of tilted hollow polar bearing')
link('Tripod_Crown','Polar_LatitudeWedge',(0,.045,.823),(1,0,0),.015)
RA=unit((0,1,1));DEC=unit((math.cos(math.radians(35)),-math.sin(math.radians(35))/math.sqrt(2),math.sin(math.radians(35))/math.sqrt(2)));SIDE=unit(cross(DEC,RA));P=(0,0,1.035);Q=add(P,mul(RA,.29))
tube('Polar_BearingSleeve',P,RA,-.180,.175,.100,.041,2,'true open polar bearing sleeve, inclined 45 degrees, radial clearance around shaft')
link('Polar_LatitudeWedge','Polar_BearingSleeve',(0,.095,.995),(1,0,0),.012)
profile('Polar_Spindle',P,RA,[(-.208,.038),(.162,.038),(.162,.074),(.191,.074),(.191,.038),(.230,.038)],1,'polar shaft with integral front shoulder overlapping sleeve rim; shaft end stops outside declination bore')
link('Polar_BearingSleeve','Polar_Spindle',add(add(P,mul(RA,.169)),(.055,0,0)),(1,0,0),.002)
tube('Declination_BearingSleeve',Q,DEC,-.110,.110,.077,.033,0,'perpendicular hollow declination housing seated on end of polar spindle')
link('Polar_Spindle','Declination_BearingSleeve',add(Q,mul(RA,-.067)),DEC,.004)
profile('Declination_Spindle',Q,DEC,[(-.605,.018),(-.117,.018),(-.117,.030),(.098,.030),(.098,.061),(.129,.061),(.129,.030),(.289,.030)],1,'single continuous declination and counterweight shaft; integral shoulder fixes bearing position')
link('Declination_BearingSleeve','Declination_Spindle',add(add(Q,mul(DEC,.104)),mul(RA,.046)),RA,.002)
# Pierced weight has 3 mm radial clearance to its 18 mm rod; separate stop collar
# supports the lower annulus by finite axial overlap. No solid disc masquerades as bore.
tube('Counterweight_PiercedDisk',Q,DEC,-.465,-.345,.130,.021,3,'closed annular counterweight with true axial through bore surrounding rod')
profile('Counterweight_StopCollar',Q,DEC,[(-.491,.035),(-.456,.035)],4,'fixed shaft collar beneath counterweight; finite annular support overlap')
link('Counterweight_StopCollar','Declination_Spindle',add(Q,mul(DEC,-.480)),RA,.003)
link('Counterweight_StopCollar','Counterweight_PiercedDisk',add(add(Q,mul(DEC,-.460)),mul(RA,.027)),RA,.001)
profile('Counterweight_EndCap',Q,DEC,[(-.616,.030),(-.590,.030)],4,'terminal retaining cap at end of shaft, visibly below weight')
link('Counterweight_EndCap','Declination_Spindle',add(Q,mul(DEC,-.599)),RA,.003)
# Empty mounting seat has a real clear top span and two raised side rails.
SADDLE=add(Q,mul(DEC,.286));box('Saddle_Base',SADDLE,(.300,.180,.034),2,'empty planar saddle base, positively seated on declination spindle',(RA,SIDE,DEC))
link('Saddle_Base','Declination_Spindle',add(Q,mul(DEC,.280)),RA,.006)
for sign,label in [(-1,'Left'),(1,'Right')]:
 c=add(add(SADDLE,mul(SIDE,sign*.071)),mul(DEC,.022));n='Saddle_Rail_'+label
 box(n,c,(.270,.022,.027),0,'raised longitudinal jaw rail flanking unobstructed mounting surface',(RA,SIDE,DEC))
 link('Saddle_Base',n,add(add(SADDLE,mul(SIDE,sign*.071)),mul(DEC,.013)),RA,.020)
 # Short clamp knob stem meets rail outer side, no loose or floating knob.
 a=add(add(c,mul(DEC,.006)),mul(SIDE,sign*.007));b=add(add(c,mul(DEC,.006)),mul(SIDE,sign*.042));rn='Saddle_ClampStem_'+label;hn='Saddle_ClampHead_'+label
 rod(rn,a,b,.008,1,'fixed clamp stem entering its side jaw',12);link(n,rn,add(c,mul(SIDE,sign*.008)),RA,.001)
 profile(hn,b,SIDE,[(-.009,.021),(.009,.021)],4,'faceted fixed clamp head on stem',12);link(rn,hn,add(b,mul(SIDE,-sign*.004)),RA,.002)
# Actual full-assembly rays through finite clear saddle space and the two side
# crescent clearances in the pierced weight. Volumetric checks are in companion test.
for u in [-.09,0,.09]:
 GAPS.append({'name':'saddle_clear_top_'+str(u),'origin_m':add(add(SADDLE,mul(RA,u)),mul(DEC,.12)),'direction':mul(DEC,-1),'length_m':.095})
for sign in [-1,1]:
 GAPS.append({'name':'counterweight_bore_crescent_'+str(sign),'origin_m':add(add(Q,mul(DEC,-.453)),mul(RA,sign*.0195)),'direction':DEC,'length_m':.120})

# Bounded empty mesh probes are deliberately excluded from the exported asset.
# Every probe is checked as a full closed finite volume, including containment.
VOID_VOLUMES={}
def void_box(name,c,size,axes):
 box(name,c,size,0,'test-only finite empty region',axes);VOID_VOLUMES[name]=G.pop(name)
def void_tube(name,origin,axis,lo,hi,outer,inner):
 tube(name,origin,axis,lo,hi,outer,inner,0,'test-only annular empty region');VOID_VOLUMES[name]=G.pop(name);BORES.pop()
void_box('Empty_SaddleInstallation',add(SADDLE,mul(DEC,.065)),(.240,.095,.085),(RA,SIDE,DEC))
void_tube('Empty_PolarBearingAnnulus',P,RA,-.150,.150,.0400,.0387)
void_tube('Empty_DeclinationBearingAnnulus',Q,DEC,-.090,.090,.0320,.0306)
void_tube('Empty_WeightBoreAnnulus',Q,DEC,-.450,-.351,.0202,.0188)

def measure_equatorial_geometry(vertices):
 assert set(vertices)==set(G)
 def axial(name,axis,origin):
  ps=[tuple(float(c) for c in p) for p in vertices[name]];t=[dot(sub(p,origin),axis) for p in ps];r=[math.sqrt(max(0,dot(sub(p,origin),sub(p,origin))-tt*tt)) for p,tt in zip(ps,t)]
  return {'min_axis_m':min(t),'max_axis_m':max(t),'min_radius_m':min(r),'max_radius_m':max(r)}
 def centre_of_end(name,axis,front):
  ps=[tuple(float(c) for c in p) for p in vertices[name]];ts=[dot(p,axis) for p in ps];end=max(ts) if front else min(ts);v=[p for p,t in zip(ps,ts) if abs(t-end)<2e-6];assert len(v)>=12
  return tuple(sum(p[i] for p in v)/len(v) for i in range(3))
 def axis_of(name,known):return unit(sub(centre_of_end(name,known,True),centre_of_end(name,known,False)))
 ra=axis_of('Polar_BearingSleeve',RA);dec=axis_of('Declination_BearingSleeve',DEC);dp=dot(ra,dec);tilt=math.degrees(math.asin(ra[2]));assert abs(dp)<2e-5 and abs(tilt-45)<.001
 rows={n:axial(n,a,c) for n,a,c in [('Polar_BearingSleeve',RA,P),('Polar_Spindle',RA,P),('Declination_BearingSleeve',DEC,Q),('Declination_Spindle',DEC,Q),('Counterweight_PiercedDisk',DEC,Q),('Counterweight_StopCollar',DEC,Q),('Counterweight_EndCap',DEC,Q)]}
 for n,lo,hi,ri,ro in [('Polar_BearingSleeve',-.180,.175,.041,.100),('Declination_BearingSleeve',-.110,.110,.033,.077),('Counterweight_PiercedDisk',-.465,-.345,.021,.130)]:
  r=rows[n];assert abs(r['min_axis_m']-lo)<2e-6 and abs(r['max_axis_m']-hi)<2e-6 and abs(r['min_radius_m']-ri)<2e-6 and abs(r['max_radius_m']-ro)<2e-6
 # Counterweight should be on the opposing side of the empty upper saddle.
 wc=tuple(sum(float(p[i]) for p in vertices['Counterweight_PiercedDisk'])/len(vertices['Counterweight_PiercedDisk']) for i in range(3));sc=tuple(sum(float(p[i]) for p in vertices['Saddle_Base'])/len(vertices['Saddle_Base']) for i in range(3));assert dot(sub(wc,Q),dec)<-.40 and dot(sub(sc,Q),dec)>.28
 return {'polar_axis_actual_direction':ra,'declination_axis_actual_direction':dec,'actual_axis_dot_product':dp,'polar_inclination_degrees':tilt,'actual_component_axial_bounds_and_radii':rows,'counterweight_and_saddle_opposite_sides':True,'counted_props':1,'fixed_pose_only':True,'old_telescope_compatibility_claimed':False}
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
root=bpy.data.objects.new('OneStaticEquatorialMount',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground centre, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.003,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_equatorial_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'equatorial_mount_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/astronomy/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'astronomy','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.72));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=1.85;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(-3,-5,3.4),'gray-back3q':(3,5,3.4)} if gray else {
 'thumbnail':(-3,-5,3.4),'qa-front':(0,-7,.72),'qa-side':(7,0,.72),'qa-top':(0,0,8),
 'qa-back':(0,7,.72),'qa-wireframe':(-3,-5,3.4)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=1.85
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();assert records(parts)==source_records if not gray else True; t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0023;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray and '--gray-obliques-only' not in sys.argv:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-7,.72)),('silhouette-128-side',(7,0,.72))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
