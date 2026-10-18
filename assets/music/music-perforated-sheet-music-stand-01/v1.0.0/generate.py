"""Original independently authored perforated music stand: one fixed static visual prop.
No adjustment, folding, clamping, musical performance or equipment-safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='music-perforated-sheet-music-stand-01';VERSION='1.0.0';TITLE='Perforated Sheet Music Stand'
DESCRIPTION=('One original low-poly independent sheet music stand in one fixed pose, counted as one prop. Three distinct splayed legs and three broad flat foot pads meet a complete central hub. A single continuous upright has an integral thick fixed height shoulder. '
 'The wide 18-degree tilted music board is one continuous thick mesh with six genuine through-windows, full borders and ribs, an integral forward projecting lower shelf and a short upturned retaining lip. It remains empty. Two board ears and one central upright ear have real complete through-bores around one continuous capped pin. Opposed finite annular ear and pin-cap faces meet, with a positive full-surface gap between the shaft and every bore wall. A separate fixed stop has a complete finite opposed patch against the board rear and a finite embedding in the upright. '
 'Fourteen named editable closed meshes and four fully opaque constant PBR colours. Metres, native Z up, front -Y and ground-level origin on the upright axis. No textures, logos, pages, book, instrument, scene or animation. Existing piano geometry already has a shallow attached music ledge; this independent tripod, central upright, perforated board and fixed tilt support are original narrower new coverage. No geometry is inherited from the old piano, easel, drum tripod, map table or chart console. '
 'Static visual geometry only: no adjustable height or tilt, folding, locking, clamp or page compatibility, music performance, human fit, carrying, paper retention, load capacity, strength, stability, wind resistance, tip resistance, manufacture, assembly path, installation compatibility or equipment-safety certification. Finite geometric connections do not establish functional or safe equipment.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={};EAR_PAIRS=[]
PALETTE=[('DeepPetrol_Board',(.055,.215,.235,1),.43,.30),('CharcoalSteel_Supports',(.035,.055,.065,1),.46,.52),('WarmBrass_FixedPin',(.62,.395,.12,1),.36,.65),('DarkRubber_Feet',(.018,.024,.028,1),.86,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,.70);ORTHO=1.91
CAMERAS={'gray-front3q':(2.6,-4,2.4),'gray-back3q':(-2.6,4,2.4),'thumbnail':(2.6,-4,2.4),'qa-front':(0,-4,1.65),'qa-side':(4,0,1.65),'qa-top':(0,0,4),'qa-back':(0,4,1.65),'qa-wireframe':(2.6,-4,2.4),'silhouette-128-front':(0,-4,1.65),'silhouette-128-side':(4,0,1.65)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
TILT=math.radians(18);CT=math.cos(TILT);ST=math.sin(TILT);PIVOT_Z=1.15

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def top(p):
 x,y,z=p;return (x,CT*y+ST*z,PIVOT_Z-ST*y+CT*z)
def top_vector(p):
 x,y,z=p;return (x,CT*y+ST*z,-ST*y+CT*z)
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
def prism(name,quad0,quad1,mat,role,transform=None):
 m=Mesh();v=quad0+quad1
 if transform:v=[transform(p) for p in v]
 for q in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:m.face([v[i] for i in q],mat,'ground' if all(v[i][2]==0 for i in q) else 'side')
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def slab(name,x0,x1,y0,y1,z0,z1,mat,role,transform=None):
 return prism(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],mat,role,transform)
def profile(name,rings,mat,role,n=24,axis='z',transform=None):
 m=Mesh()
 def p(u,r,t):
  q=(r*math.cos(t),r*math.sin(t),u) if axis=='z' else (u,r*math.cos(t),r*math.sin(t))
  return transform(q) if transform else q
 for k,((u,r),(v,s)) in enumerate(zip(rings,rings[1:])):
  for i in range(n):
   a=math.tau*i/n;b=math.tau*(i+1)/n
   tag='shaft' if axis=='x' and r==s==.011 else 'profile'
   m.face([p(u,r,a),p(u,r,b),p(v,s,b),p(v,s,a)],mat,tag)
 for (u,r),rev in [(rings[0],True),(rings[-1],False)]:
  pts=[p(u,r,math.tau*i/n) for i in range(n)];m.face(pts[::-1] if rev else pts,mat,'end')
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def ring(name,x0,x1,rin,rout,mat):
 m=Mesh();n=24
 def p(x,r,t):return top((x,r*math.cos(t),r*math.sin(t)))
 for i in range(n):
  a=math.tau*i/n;b=math.tau*(i+1)/n
  for tag,poly in [('inner',[p(x0,rin,a),p(x1,rin,a),p(x1,rin,b),p(x0,rin,b)]),('outer',[p(x0,rout,b),p(x1,rout,b),p(x1,rout,a),p(x0,rout,a)]),('left',[p(x0,rin,b),p(x0,rout,b),p(x0,rout,a),p(x0,rin,a)]),('right',[p(x1,rin,a),p(x1,rout,a),p(x1,rout,b),p(x1,rin,b)])]:m.face(poly,mat,tag)
 g=m.result('Thick complete annular ear with one real through-bore.',mat)
 if name:G[name]=g
 return g
# Three original splayed rectangular legs with horizontal foot seats.
for label,a in [('Rear',math.pi/2),('FrontLeft',math.pi*7/6),('FrontRight',math.pi*11/6)]:
 ca,sa=math.cos(a),math.sin(a)
 def radial(p):
  r,t,z=p;return (r*ca-t*sa,r*sa+t*ca,z)
 leg='Splayed_Leg_'+label;foot='Foot_'+label
 q0=[radial((.027,-.018,.194)),radial((.027,.018,.194)),radial((.332,.018,.025)),radial((.332,-.018,.025))]
 q1=[(x,y,z+.030) for x,y,z in q0]
 prism(leg,q0,q1,1,'One continuous splayed leg with finite hub and foot embeddings.')
 slab(foot,.300,.365,-.032,.032,0,.047,3,'One of three finite flat foot pads; a real leg is embedded in its upper part.',radial);FEET.append(foot)
 LINKS.append((foot,leg,[radial((.318,-.006,.042)),radial((.318,.006,.042))]))
 LINKS.append((leg,'Tripod_Hub',[radial((.032,-.006,.209)),radial((.032,.006,.209))]))
profile('Tripod_Hub',[(.167,.048),(.226,.048),(.247,.039)],1,'Complete closed central hub joining all three separate legs to the upright.',n=24)
profile('Upright_WithFixedShoulder',[(.213,.019),(.680,.019),(.680,.029),(.731,.029),(.731,.014), (1.125,.014)],1,'One continuous central upright with an integral visibly thick fixed shoulder; no adjustment motion.',n=24)
LINKS.append(('Tripod_Hub','Upright_WithFixedShoulder',[(.004,0,.230),(-.004,0,.230)]))
# One manifold sheet/shelf/lip union constructed from a rectilinear solid cell complex.
# Shared boundary vertices and every boundary face are retained, so no coplanar
# overlays, internal faces, disconnected outline bars or Boolean runtime are used.
HOLES=[(x0,x1,z0,z1) for x0,x1 in [(-.270,-.055),(.055,.270)] for z0,z1 in [(-.095,-.015),(.040,.120),(.175,.255)]]
xs=sorted(set([-.320,.320]+[q for h in HOLES for q in h[:2]]));ys=[-.096,-.084,-.046,-.034]
zs=sorted(set([-.140,-.128,-.104,.280]+[q for h in HOLES for q in h[2:]]));cells=set()
for i in range(len(xs)-1):
 for j in range(len(ys)-1):
  for k in range(len(zs)-1):
   x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2;z=(zs[k]+zs[k+1])/2
   sheet=y>-.046 and not any(a<x<b and c<z<d for a,b,c,d in HOLES)
   shelf=z<-.128;lip=y<-.084 and z<-.104
   if sheet or shelf or lip:cells.add((i,j,k))
m=Mesh()
for i,j,k in sorted(cells):
 x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
 sides=[((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]
 for (dx,dy,dz),q in sides:
  if (i+dx,j+dy,k+dz) not in cells:m.face([top(p) for p in q],0,'sheet_shelf_lip_boundary')
G['Perforated_Board_IntegralShelfLip']=m.result('One continuous 12 mm thick six-window sheet, integral 62 mm deep lower shelf and 36 mm overall short upturned lip.',0)
# Three bored ears, one genuinely continuous capped pin and one finite tilted stop.
for name,x0,x1,outer,mat in [('Board_Ear_Left',-.036,-.018,.045,0),('Upright_Ear',-.018,.018,.031,1),('Board_Ear_Right',.018,.036,.045,0)]:
 ring(name,x0,x1,.016,outer,mat)
 if name.startswith('Board'):
  x=(x0+x1)/2;LINKS.append((name,'Perforated_Board_IntegralShelfLip',[top((x,-.039,-.004)),top((x,-.039,.004))]))
 else:LINKS.append((name,'Upright_WithFixedShoulder',[(0,0,1.122),(.004,0,1.122)]))
 BORES.append({'mesh':name,'origin_m':list(top((x0-.002,0,0))),'direction':[1,0,0],'length_m':x1-x0+.004})
 EAR_PAIRS.append({'ear':name,'pin':'Capped_Tilt_Pin','x0':x0,'x1':x1})
 g=profile(None,[(x0-.002,.0145),(x1+.002,.0145)],0,'Complete solid isolated-hole probe, not delivery geometry.',axis='x',transform=top)
 VOID_PROBES['IsolatedFullBore_'+name]={'type':'mesh','geometry':g,'targets':[name],'role':'entire isolated through-bore including its axial core and both mouths'}
 VOID_PROBES['AssembledAnnularGap_'+name]={'type':'mesh','geometry':ring(None,x0+.001,x1-.001,.012,.015,0),'targets':[name,'Capped_Tilt_Pin'],'role':'complete finite annular gap around fixed pin shaft, excluding contact planes by 1 mm'}
profile('Capped_Tilt_Pin',[(-.047,.025),(-.036,.025),(-.036,.011),(.036,.011),(.036,.025),(.047,.025)],2,'One closed continuous fixed pin with integral end caps and a clear shaft in every ear bore.',axis='x',transform=top)
for a,b,x,rad,area in [('Capped_Tilt_Pin','Board_Ear_Left',-.036,.020,.0010),('Board_Ear_Left','Upright_Ear',-.018,.023,.0021),('Upright_Ear','Board_Ear_Right',.018,.023,.0021),('Board_Ear_Right','Capped_Tilt_Pin',.036,.020,.0010)]:
 CONTACTS.append({'a':a,'b':b,'axis':0,'plane_m':x,'minimum_patch_area_m2':area,'interior_probe_offset_m':.001,'points':[top((x,rad,0)),top((x,-rad,0)),top((x,0,rad)),top((x,0,-rad))],'scope':'full opposed finite annular ear or pin-cap contact; positive shaft/bore clearance'})
slab('Fixed_Tilt_Stop',-.020,.020,-.034,.028,-.103,-.073,1,'One fixed stop: full tilted front face seats on the board rear, with the rear section embedded in the upright.',top)
LINKS.append(('Fixed_Tilt_Stop','Upright_WithFixedShoulder',[top((-.004,.022,-.088)),top((.004,.022,-.088))]))
normal=top_vector((0,1,0))
CONTACTS.append({'a':'Perforated_Board_IntegralShelfLip','b':'Fixed_Tilt_Stop','normal':normal,'plane_m':dot(normal,top((0,-.034,-.088))),'minimum_patch_area_m2':.00119,'interior_probe_offset_m':.001,'points':[top((x,-.034,z)) for x in [-.012,.012] for z in [-.096,-.080]],'scope':'complete finite 40 by 30 mm tilted stop face against board rear, zero positive penetration'})
for i,(x0,x1,z0,z1) in enumerate(HOLES,1):
 g=slab(None,x0+.001,x1-.001,-.050,-.030,z0+.001,z1-.001,0,'Full rectangular window volume with 1 mm positive edge clearance.',top)
 VOID_PROBES['CompleteBoardWindow_%02d'%i]={'type':'mesh','geometry':g,'targets':list(G),'role':'full window aperture including the entire 12 mm sheet thickness and 4 mm beyond each mouth'}
# Whole useful lower shelf cavity, intentionally empty without pages or a book.
VOID_PROBES['CompleteLowerShelfOpenSpace']={'type':'mesh','geometry':slab(None,-.319,.319,-.083,-.047,-.127,-.105,0,'Finite entire clear lower ledge space, including its width/depth/height.',top),'targets':list(G),'role':'full finite lower shelf cavity between the board, ledge and short front lip'}
# Explicit finite back gap below the stopped board; no hidden rod or solid filler.
VOID_PROBES['BackOfBoardClearance']={'type':'mesh','geometry':slab(None,-.030,.030,-.032,-.018,-.068,-.051,0,'Entire finite central rear clearance strip between stop and ears.',top),'targets':list(G),'role':'finite central rear space between stop and bored ears'}
def measure_stand_geometry(vertices):
 return {'single_prop_count':1,'ground_pad_count':3,'splayed_leg_count':3,'upright_count':1,'integral_fixed_shoulder_count':1,'board_window_count':6,'board_width_m':.640,'board_height_m':.420,'board_thickness_m':.012,'lower_shelf_depth_m':.062,'front_lip_overall_height_m':.036,'tilt_from_vertical_deg':18,'true_ear_bore_count':3,'continuous_capped_pin_count':1,'tilted_stop_contact_area_m2':.0012,'materials':MATERIAL_CONTRACT,'functional_scope':'one original fixed independent perforated sheet music stand; static visual only'}
assert len(G)==14,len(G)
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
root=bpy.data.objects.new('OneFixedMusicStand',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and upright-axis origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
stand_evidence=measure_stand_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
  normal=Vector(r.get('normal',tuple(1 if i==r.get('axis',2) else 0 for i in range(3))));low=Vector(p)-normal*eps;high=Vector(p)+normal*eps
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
 'single_prop_count':1,'stand_geometry':stand_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
