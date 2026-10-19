"""Original wide-bellied shoulder creel with real lattice windows and inset opening.
One fixed visual prop; no claims of weaving, carrying, food or fishing performance.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fishing-latticed-shoulder-creel-01';VERSION='1.0.0';TITLE='Latticed Shoulder Creel'
DESCRIPTION=('One original low-poly static fishing-creel exterior, counted as one prop. A broad oval belly tapers into a narrower shoulder and continuous neck rim. Sixteen thick upright strips and five full horizontal bands form one welded closed lattice boundary with sixty-four actual through-windows, each bounded by four thick sides. A complete thick flat oval floor connects finitely to the lower band. A fixed thick lid rests over the full finite neck-rim face and contains a genuine front-offset oval drop opening; the opening, neck and belly lead to one actual empty cavity above the bottom. One thick rear-offset arch handle has two finite embedded shoulder ends and stays clear of the opening. Four editable closed components and three opaque constant PBR materials. The wide belly, closed flat bottom, narrow covered shoulder and offset drop opening are newly authored geometry, not a recoloured harvest basket, upside-down hat net or modified landing net. '
 'Metres, native Z up, ground-centre origin, front -Y. Fixed pose only. No fish, water, loose contents, second basket, scene, strap variant, textures, transparency, labels, animation or branding. Welded stylized geometric strips do not represent an actual weaving process. '
 'Static visual geometry only. No actual holding, capacity, drainage, ventilation, fish survival, capture, food or material safety, human grip fit, carrying load, durability, stability, manufacturing, fishing or other safety performance is claimed. No interface compatibility with prior fishing assets is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={}
PALETTE=[('Lattice_WarmReed',(.49,.29,.115,1),.87,0),('Bindings_DeepReed',(.285,.16,.065,1),.90,0),('Lid_MutedOlive',(.27,.32,.12,1),.78,0)]
MATERIAL_CONTRACT='Three opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,.305);ORTHO=.86
CAMERAS={'gray-front3q':(.95,-1.45,1.05),'gray-back3q':(-.95,1.45,1.05),'thumbnail':(.95,-1.45,1.05),'qa-front':(0,-2,.80),'qa-side':(2,0,.80),'qa-top':(0,0,3),'qa-back':(0,2,.80),'qa-wireframe':(.95,-1.45,1.05),'silhouette-128-front':(0,-2,.80),'silhouette-128-side':(2,0,.80)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,k):return tuple(x*k for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  for i in range(1,len(ids)-1):self.f.append((ids[0],ids[i],ids[i+1]));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi,mat=0,role='complete finite rectangular volume'):
 v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]];m=Mesh()
 for f in BOX_FACES:m.face([v[i] for i in f],mat)
 return m.result(role,mat)
def volume(entries,name,g,targets,role):entries[name]=dict(g,targets=list(targets),role=role)
def link(a,b,p,axis=(1,0,0),spread=.001):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def ellipse_profile(rings,mat=0,role='closed complete oval volume',angles=None,cy=0):
 angles=angles or [math.tau*i/48 for i in range(48)];vv=[[(rx*math.cos(a),cy+ry*math.sin(a),z) for a in angles] for rx,ry,z in rings];m=Mesh();n=len(angles)
 m.face(list(reversed(vv[0])),mat,'bottom');m.face(vv[-1],mat,'top')
 for a,b in zip(vv,vv[1:]):
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]],mat,'side')
 return m.result(role,mat)
def annulus(outer,inner,z0,z1,mat=0,angles=None,cy_inner=0,role='thick closed oval annulus'):
 angles=angles or [math.tau*i/48 for i in range(48)];m=Mesh();n=len(angles)
 for i,a in enumerate(angles):
  b=angles[(i+1)%n];o0=(outer[0]*math.cos(a),outer[1]*math.sin(a),z0);o1=(outer[0]*math.cos(b),outer[1]*math.sin(b),z0);i0=(inner[0]*math.cos(a),cy_inner+inner[1]*math.sin(a),z0);i1=(inner[0]*math.cos(b),cy_inner+inner[1]*math.sin(b),z0)
  O0=add(o0,(0,0,z1-z0));O1=add(o1,(0,0,z1-z0));I0=add(i0,(0,0,z1-z0));I1=add(i1,(0,0,z1-z0))
  for pts,tag in [([o1,o0,i0,i1],'bottom'),([O0,O1,I1,I0],'top'),([o0,o1,O1,O0],'outside'),([i1,i0,I0,I1],'inside')]:m.face(pts,mat,tag)
 return m.result(role,mat)
# New creel silhouette: broad middle, narrowed shoulder and neck, no solid side skin.
PROFILE=[(.025,.270,.190),(.055,.285,.202),(.125,.320,.232),(.225,.325,.236),(.295,.295,.214),(.360,.248,.181),(.380,.238,.173),(.425,.210,.150)]
def radii(z):
 for (a,x0,y0),(b,x1,y1) in zip(PROFILE,PROFILE[1:]):
  if a-1e-9<=z<=b+1e-9:
   t=(z-a)/(b-a);return (x0+(x1-x0)*t,y0+(y1-y0)*t)
 raise AssertionError(z)
COLS=16;ROWS=4;STRIP_ANGLE=.090;DEPTH=.020
A=[v for i in range(COLS) for v in [math.tau*i/COLS,math.tau*i/COLS+STRIP_ANGLE]]
# Every profile corner is a lattice row; vertical cells never span a kink.
BANDS=[(.025,.055),(.120,.140),(.215,.235),(.300,.320),(.350,.425)]
Z=sorted(set([z for b in BANDS for z in b]+[p[0] for p in PROFILE]))
def lattice_point(a,z,inset=0):
 rx,ry=radii(z);return ((rx-inset)*math.cos(a),(ry-inset)*math.sin(a),z)
HEX_FACES=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def wedge_geometry(a0,a1,zs,in0,in1,role='closed finite oval-wall sector'):
 vv=[[lattice_point(a,z,d) for a,d in [(a0,in0),(a0,in1),(a1,in1),(a1,in0)]] for z in zs];m=Mesh()
 m.face(list(reversed(vv[0])));m.face(vv[-1])
 for a,b in zip(vv,vv[1:]):
  for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]])
 return m.result(role)
body='Welded_ThroughWindow_BellyShoulderNeck';boundary={};m=Mesh()
for k in range(len(Z)-1):
 z0,z1=Z[k:k+2];band=any(a<=(z0+z1)/2<=b for a,b in BANDS)
 for i,a0 in enumerate(A):
  if not band and i%2:continue
  a1=A[i+1] if i+1<len(A) else math.tau
  pts=[lattice_point(a,z,d) for z in [z0,z1] for a,d in [(a0,0),(a0,DEPTH),(a1,DEPTH),(a1,0)]];ids=[m.vertex(p) for p in pts]
  for ff in HEX_FACES:
   f=tuple(ids[i] for i in ff);key=tuple(sorted(f))
   if key in boundary:del boundary[key]
   else:boundary[key]=(f,1 if band else 0,'horizontal_band' if band else 'upright_strip')
for f,mat,tag in boundary.values():m.face([m.v[i] for i in f],mat,tag)
# Compact away interior-only cell vertices before topology checks.
g=m.result('One connected thick welded oval lattice with 64 real through-windows; broad belly, narrowed shoulder and continuous finite neck face. Shared cell faces removed.');used=sorted(set(q for f in g['faces'] for q in f));remap={q:i for i,q in enumerate(used)};g['vertices']=[g['vertices'][i] for i in used];g['faces']=[tuple(remap[i] for i in f) for f in g['faces']];G[body]=g
base='Complete_Thick_Flat_OvalFloor';G[base]=ellipse_profile([(.276,.196,0),(.276,.196,.045)],1,'Complete flat-bottom thick oval floor; no hidden hole and no ground pedestal. The full perimeter joins the lower lattice band.',A);FEET=[base]
lid='Fixed_ThickLid_TrueOvalDropOpening';G[lid]=annulus((.219,.159),(.105,.071),.425,.447,2,cy_inner=-.035,role='One thick fixed oval lid; real offset through-opening, finite whole underside on neck ring.')
handle='RearOffset_ThickArchHandle';HANDLE_Y=.125;HANDLE_RX=.178;HANDLE_RISE=.240;HANDLE_Z=.355;HANDLE_T=.012;HANDLE_D=.010
m=Mesh();sections=[]
for i in range(19):
 a=math.pi*i/18;c=(HANDLE_RX*math.cos(a),HANDLE_Y+.040*math.sin(a),HANDLE_Z+HANDLE_RISE*math.sin(a));normal=(math.cos(a),0,math.sin(a));sections.append([add(add(c,mul(normal,s)),(0,d,0)) for s,d in [(-HANDLE_T,-HANDLE_D),(HANDLE_T,-HANDLE_D),(HANDLE_T,HANDLE_D),(-HANDLE_T,HANDLE_D)]])
m.face(list(reversed(sections[0])),1,'right_end');m.face(sections[-1],1,'left_end')
for a,b in zip(sections,sections[1:]):
 for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]],1,'arch')
G[handle]=m.result('One thick fixed arch, rear offset Y=.125 at ends and .165 at crown; both lower ends embedded in shoulder and entire upper arch stays behind offset entry.',1)
# Full finite embedding volume of the lower rim in the complete floor.
link(base,body,lattice_point(.045,.037,.011),axis=(0,0,1),spread=.002)
volume(WALL_VOLUMES,'Floor_LowerBand_WholeEmbeddedRing',annulus((.263,.184),(.258,.179),.032,.039,angles=A),[base,body],'complete closed 360-degree material ring within both floor and lower lattice band')
volume(WALL_VOLUMES,'Floor_CompleteInsetSlab',ellipse_profile([(.271,.191,.004),(.271,.191,.041)],angles=A),[base],'complete finite full oval bottom slab, positive inset to each surface')
# Lid is fixed by its complete finite opposed seating face, not hidden positive penetration.
CONTACTS=[{'a':body,'b':lid,'axis':2,'plane_m':.425,'minimum_patch_area_m2':.019,'interior_probe_offset_m':.001,'points':[(.199,0,.425),(-.199,0,.425),(0,-.139,.425)],'scope':'whole finite opposed neck/lid seat with no positive penetration'}]
volume(WALL_VOLUMES,'Lid_CompleteInsetAnnulus',annulus((.215,.155),(.109,.075),.429,.443,cy_inner=-.035),[lid],'whole thick lid material excluding positive boundary margin around true entry')
for sign,label in [(1,'Right'),(-1,'Left')]:
 lo=(.168,.118,.359);hi=(.172,.122,.365)
 if sign<0:lo=(-.172,.118,.359);hi=(-.168,.122,.365)
 p=tuple((a+b)/2 for a,b in zip(lo,hi));link(body,handle,p,axis=(0,0,1),spread=.001)
 volume(WALL_VOLUMES,'Handle_'+label+'_WholeEmbeddedEnd',box_geometry(lo,hi),[body,handle],'whole positive-volume handle end inside both shoulder band and handle')
# Complete real windows, each extending through the full wall depth. Split at
# all profile corners so no hexahedron shortcuts the actual belly silhouette.
for row in range(ROWS):
 z0=BANDS[row][1]+.0015;z1=BANDS[row+1][0]-.0015;zs=[z0]+[z for z in Z if z0<z<z1]+[z1]
 for col in range(COLS):
  a0=A[2*col+1]+.008;a1=math.tau*(col+1)/COLS-.008
  volume(VOID_VOLUMES,f'Window_{row:02d}_{col:02d}',wedge_geometry(a0,a1,zs,-.009,DEPTH+.009),list(G),'whole finite through-window air across wall, bounded by all four actual sides and inset only at surface tolerance')
# Material envelopes check all sixteen entire strips and every complete hoop.
for col in range(COLS):
 a0=A[2*col]+.009;a1=A[2*col+1]-.009;zs=[.027]+[z for z in Z if .027<z<.423]+[.423]
 volume(WALL_VOLUMES,f'UprightStrip_{col:02d}_EntireConnectedMaterial',wedge_geometry(a0,a1,zs,.003,.017),[body],'whole full-height thick upright including every horizontal crossing')
for row,(z0,z1) in enumerate(BANDS):
 # An annular envelope follows every profile corner and the actual polygon angles.
 zs=[z0+.002]+[z for z in Z if z0+.002<z<z1-.002]+[z1-.002];mm=Mesh();outer=[[(radii(z)[0]-.003)*math.cos(a),(radii(z)[1]-.003)*math.sin(a),z] for z in zs for a in A];inner=[[(radii(z)[0]-.017)*math.cos(a),(radii(z)[1]-.017)*math.sin(a),z] for z in zs for a in A];n=len(A)
 for i in range(n):
  j=(i+1)%n
  mm.face([outer[j],outer[i],inner[i],inner[j]])
  off=(len(zs)-1)*n;mm.face([outer[off+i],outer[off+j],inner[off+j],inner[off+i]])
 for k in range(len(zs)-1):
  for i in range(n):
   j=(i+1)%n;a=k*n+i;b=k*n+j;c=(k+1)*n+i;d=(k+1)*n+j;mm.face([outer[a],outer[b],outer[d],outer[c]]);mm.face([inner[b],inner[a],inner[c],inner[d]])
 volume(WALL_VOLUMES,f'HorizontalBand_{row:02d}_EntireConnectedMaterial',mm.result('full closed annular band material'),[body],'whole 360-degree horizontal band including all upright crossings')
# Whole connected belly and shoulder air reaches the bottom surface with only
# 2mm boundary tolerance. The entry probe overlaps the chamber, making its
# continuous real empty path explicit. All probes are QA only, never exported.
zs=[.047]+[z for z in Z if .047<z<.423]+[.423]
volume(VOID_VOLUMES,'Complete_BellyShoulder_Neck_Cavity',ellipse_profile([(radii(z)[0]-.023,radii(z)[1]-.023,z) for z in zs],angles=A),list(G),'whole finite empty belly, full shoulder and neck, 3mm wall clearance and 2mm floor/lid clearance')
volume(VOID_VOLUMES,'Complete_OffsetDropOpening_PathToFloor',ellipse_profile([(.102,.068,.047),(.102,.068,.500)],cy=-.035),list(G),'whole finite entry-to-bottom path, including both lid mouths and above-lid approach; no handle obstruction')
# The full under-arch air is not a grip or human-clearance claim. It proves the
# upper handle does not become an opaque disk; the entry corridor above remains separately checked.
def arch_aperture(min_z):
 t0=math.asin(max(0,(min_z-HANDLE_Z)/.221));ts=[t0+(math.pi-2*t0)*i/24 for i in range(25)];section=[(.162*math.cos(t),HANDLE_Z+.221*math.sin(t)) for t in ts];m=Mesh()
 # Section follows the arch from right to left and closes with its bottom chord.
 vv=[[(x,y,z) for x,z in section] for y in [.104,.186]];m.face(list(reversed(vv[0])));m.face(vv[1])
 for i in range(len(section)):
  j=(i+1)%len(section);m.face([vv[0][i],vv[0][j],vv[1][j],vv[1][i]])
 return m.result('whole complete through-thickness arch opening volume')
volume(ISOLATED_VOID_VOLUMES,'Handle_WholeIsolatedArchOpening',arch_aperture(.358),[handle],'whole finite arch aperture through entire curved handle depth; excludes intentionally present separate lid and basket')
volume(VOID_VOLUMES,'Handle_WholeUpperAssemblyOpening',arch_aperture(.452),list(G),'whole assembled upper arch opening above the lid, across full handle depth; no human-fit claim')
BORES=[{'mesh':lid,'origin_m':(0,-.035,.416),'direction':(0,0,1),'length_m':.045}]
def measure_creel_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 def bounds(n):return [[fn(float(p[i]) for p in vertices[n]) for i in range(3)] for fn in [min,max]]
 assert abs(bounds(base)[0][2])<2e-7 and abs(bounds(base)[1][2]-.045)<2e-7
 assert abs(bounds(body)[1][0]-.325)<2e-7 and abs(bounds(body)[1][2]-.425)<2e-7
 assert abs(bounds(lid)[0][2]-.425)<2e-7 and abs(bounds(lid)[1][2]-.447)<2e-7
 assert bounds(handle)[0][1]>.11499 and bounds(handle)[1][2]>.60699
 return {'single_prop_count':1,'closed_components':len(G),'true_through_windows':COLS*ROWS,'upright_strips':COLS,'horizontal_bands':len(BANDS),'full_wall_depth_axis_m':DEPTH,'belly_max_x_m':.650,'belly_max_y_m':.472,'neck_outer_axes_m':[.420,.300],'true_entry_nominal_axes_m':[.210,.142],'entry_offset_y_m':-.035,'flat_floor_thickness_m':.045,'lid_thickness_m':.022,'full_opposed_contacts':len(CONTACTS),'handle_finite_embedded_ends':2,'full_finite_voids':len(VOID_VOLUMES),'whole_material_support_volumes':len(WALL_VOLUMES),'frozen_static_pose':True,'carrying_capture_food_fish_survival_safety_claim':False}
assert len(G)==4

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
root=bpy.data.objects.new('OneLatticedShoulderCreel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and centre of flat oval floor; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
creel_evidence=measure_creel_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'creel_geometry':creel_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fishing/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'fishing','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,8),1700,5.0),('Fill',(6,-1.2,5),840,4.8),('Rim',(1.2,6,7),1200,4.8)]:
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
if '--ground-views' in sys.argv:views={n:CAMERAS[n] for n in ['qa-front','qa-side','qa-back']}
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
