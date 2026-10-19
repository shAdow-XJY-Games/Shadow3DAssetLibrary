"""Original square four-face clock tower with through arch; one static modular asset."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='timekeeping-four-face-arch-clock-tower-01';VERSION='1.0.0';TITLE='Four-Face Arch Clock Tower'
DESCRIPTION=('One original low-poly square clock tower, counted as one modular asset. A continuous thick square tower has a genuine front-to-back arched opening from ground to crown, two full finite strip feet and no floor or hidden blockage. A stepped square shoulder supports a thick four-face clock box. All four faces have actual blind circular recesses, complete supported ivory dial plates with twelve integral raised indices each, two independently layered fixed pointers and two real short central axles. Fixed illustrative display only. A thick four-hip roof with broad stepped eaves bears on the complete clock-box top. The tower, box and roof use square geometry distinct from prior tapering octagonal lighthouse, small tabletop clock, alarm clock or cottage meshes. Metres, source Z up and front -Y, origin at exact ground-level bounds centre. Constant opaque unlinked PBR colours, no textures, external fonts or external models. No scene, interior floors, stairs, animation, sound or moving mechanism. No timekeeping, accuracy, calibration, chiming, passage or climbing function, interior occupation, structural strength, stability, manufacture, installation, public-building safety, seamless repetition, historic reconstruction or prior wall compatibility is claimed.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};SOLID_VOLUMES={}
PALETTE=[('Tower_WarmLimestone',(.57,.42,.28,1),.87,0),('Tower_LightStoneEdges',(.74,.61,.43,1),.82,0),('Clock_IvoryFace',(.91,.83,.64,1),.80,0),('Clock_DeepTealMetal',(.035,.15,.17,1),.53,.12),('Roof_OxideCopper',(.16,.30,.27,1),.72,.12)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled colours; no TEX_* nodes or linked inputs.'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
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
def earclip(poly):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 order=list(range(len(poly))) if area>0 else list(reversed(range(len(poly))));out=[]
 while len(order)>3:
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-12:continue
   if any(all(cr(poly[x],poly[y],poly[q])>=-1e-12 for x,y in[(a,b),(b,c),(c,a)]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(k);break
  else:raise AssertionError('non-simple or degenerate polygon')
 out.append(tuple(order));return out

def box_geometry(lo,hi,mat=0):
 m=Mesh();v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 for f in[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.face([v[i] for i in f],mat)
 return m.result('closed finite solid box')
def volume(table,name,g,targets,role):table[name]=dict(g,targets=list(targets),role=role,asset_member=False)
def loft_y(sections,mat=0):
 sections=[(y,list(reversed(p)) if sum(p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0] for i in range(len(p)))>0 else p) for y,p in sections]
 m=Mesh();rings=[[(x,y,z) for x,z in p] for y,p in sections]
 for a,b in zip(rings,rings[1:]):
  for i in range(len(a)):j=(i+1)%len(a);m.face([a[i],a[j],b[j],b[i]],mat,'continuous_arch_depth')
 for f in earclip(sections[0][1]):m.face([rings[0][i] for i in f],mat,'front_polygon_cap')
 for f in earclip(sections[-1][1]):m.face([rings[-1][i] for i in f][::-1],mat,'rear_polygon_cap')
 return m.result('complete closed loft through Y')
def tower_profile(radius):
 return [(-.8,0),(-.8,3.15),(.8,3.15),(.8,0),(radius,0),(radius,1.14)]+[(radius*math.cos(i*math.pi/20),1.14+radius*math.sin(i*math.pi/20)) for i in range(1,21)]+[(-radius,0)]
TOWER='Tower_ContinuousSquareThroughArch';SHOULDER='Tower_SteppedSquareShoulder';CASE='ClockBox_FourActualBlindRecesses';ROOF='Roof_ThickFourHipAndEaves'
ARCH_SECTIONS=[(-.8,.52),(-.69,.46),(.69,.46),(.8,.52)]
G[TOWER]=loft_y([(y,tower_profile(r)) for y,r in ARCH_SECTIONS]);G[TOWER]['role']='One continuous square tower with full ground-to-crown front-to-back arched passage and two finite strip feet; no hidden floor or rear wall';FEET=[TOWER]
def square_loft(levels,mats):
 m=Mesh();rings=[[(x*h,y*h,z) for x,y in[(-1,-1),(1,-1),(1,1),(-1,1)]] for z,h in levels];m.face(rings[0][::-1],mats[0]);m.face(rings[-1],mats[-1])
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]],mats[k])
 return m.result('single continuous stepped square closed body')
G[SHOULDER]=square_loft([(3.15,.8),(3.21,.94),(3.35,.94)],[1,1]);G[SHOULDER]['role']='Thick square shoulder with full tower-top finite bearing and a complete finite clock-box seat'
# Every face uses local U horizontal, V upward and W outward; U x V = W.
FRAMES={'Front':((1,0,0),(0,0,1),(0,-1,0)),'Right':((0,1,0),(0,0,1),(1,0,0)),'Back':((-1,0,0),(0,0,1),(0,1,0)),'Left':((0,-1,0),(0,0,1),(-1,0,0))}
CENTER=(0,0,4.10)
def world(label,p):
 u,v,w=FRAMES[label];return add(CENTER,add(mul(u,p[0]),add(mul(v,p[1]),mul(w,p[2]))))
def transformed(g,label):
 q=dict(g);q['vertices']=[world(label,p) for p in g['vertices']];return q
ANGLES=sorted(set([round(math.tau*i/48,12) for i in range(48)]+[round(math.atan2(y*.75,x*1.01)%math.tau,12) for x,y in[(-1,-1),(1,-1),(1,1),(-1,1)]]))
m=Mesh();outer_by_face={}
for label in FRAMES:
 outer=[]
 for a in ANGLES:
  co,si=math.cos(a),math.sin(a);r=min(1.01/abs(co) if abs(co)>1e-10 else 99,.75/abs(si) if abs(si)>1e-10 else 99);x,z=r*co,r*si
  if abs(abs(x)-1.01)<1e-8:x=math.copysign(1.01,x)
  if abs(abs(z)-.75)<1e-8:z=math.copysign(.75,z)
  outer.append(world(label,(x,z,1.01)))
 outer_by_face[label]=outer
 rings=[outer]+[[world(label,(r*math.cos(a),r*math.sin(a),d)) for a in ANGLES] for r,d in[(.64,1.01),(.61,.975),(.61,.84)]]
 for k,(a,b) in enumerate(zip(rings,rings[1:])):
  for i in range(len(a)):j=(i+1)%len(a);m.face([a[i],a[j],b[j],b[i]],1 if k==0 else 0,'true_blind_recess_ring')
 for i in range(len(ANGLES)):j=(i+1)%len(ANGLES);m.face([world(label,(0,0,.84)),rings[-1][i],rings[-1][j]],0,'whole_recess_back')
for z,sign in[(3.35,-1),(4.85,1)]:
 pts={tuple(p) for points in outer_by_face.values() for p in points if abs(p[2]-z)<1e-8};pts=sorted(pts,key=lambda p:math.atan2(p[1],p[0]));pts=pts if sign>0 else list(reversed(pts))
 for i in range(len(pts)):m.face([(0,0,z),pts[i],pts[(i+1)%len(pts)]],1,'complete_square_top_or_bottom')
G[CASE]=m.result('One thick closed square clock box, four separately recessed circular blind seats with continuous backs and side walls')
G[ROOF]=square_loft([(4.85,1.15),(4.99,1.15),(5.07,1.10),(6.05,.15),(6.13,.15)],[1,4,4,4]);G[ROOF]['role']='One thick four-hip closed roof with full four-sided stepped eave band and finite whole clock-box top support'
def seat(name,a,b,axis,u,v,plane,points,minarea,offset=.002,coverage='smaller_complete_interface'):
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':plane,'points':points,'interior_probe_offset_m':offset,'minimum_patch_area_m2':minarea,'coverage':coverage,'role':'finite opposed whole-area seat; no interpenetration'})
seat('TowerToShoulder',TOWER,SHOULDER,(0,0,1),(1,0,0),(0,1,0),3.15,[(0,0,3.15)],2.55)
seat('ShoulderToClockBox',SHOULDER,CASE,(0,0,1),(1,0,0),(0,1,0),3.35,[(0,0,3.35)],3.53)
seat('ClockBoxToRoof',CASE,ROOF,(0,0,1),(1,0,0),(0,1,0),4.85,[(0,0,4.85)],4.08)
N=48
def rad(r,i,z):a=math.tau*(i-.5)/N;return(r*math.cos(a),r*math.sin(a),z)
def cylinder(r,z0,z1,n=N,mat=3):
 m=Mesh();rr=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for z in[z0,z1]]
 for i in range(n):j=(i+1)%n;m.face([(0,0,z0),rr[0][j],rr[0][i]],mat);m.face([(0,0,z1),rr[1][i],rr[1][j]],mat);m.face([rr[0][i],rr[0][j],rr[1][j],rr[1][i]],mat)
 return m.result('closed finite cylinder')
def dial_geometry():
 m=Mesh()
 for i in range(N):
  j=(i+1)%N;m.face([(0,0,.84),rad(.58,j,.84),rad(.58,i,.84)],2,'whole_dial_back');m.face([rad(.58,i,.84),rad(.58,j,.84),rad(.58,j,.87),rad(.58,i,.87)],2)
  m.face([(0,0,.87),rad(.44,i,.87),rad(.44,j,.87)],2,'unmarked_face')
  m.face([rad(.53,i,.87),rad(.58,i,.87),rad(.58,j,.87),rad(.53,j,.87)],2,'outer_face')
  raised=i%4==0;z=.89 if raised else .87
  m.face([rad(.44,i,z),rad(.53,i,z),rad(.53,j,z),rad(.44,j,z)],3 if raised else 2,'integral_raised_index' if raised else 'between_indices')
  if raised:
   a=[rad(.44,i,.87),rad(.53,i,.87),rad(.53,j,.87),rad(.44,j,.87)];b=[(x,y,.89) for x,y,z in a]
   for k in range(4):l=(k+1)%4;m.face([a[k],a[l],b[l],b[k]],3,'integral_index_root')
 return m.result('One complete solid dial with twelve integral raised indices, no pasted marks')
def hand_geometry(length,angle,z0,z1):
 poly=[(-.055,-.035),(-.035,-.060),(.035,-.060),(.055,-.035),(.055,.05),(.028,length-.045),(0,length),(-.028,length-.045),(-.055,.05)];a=math.radians(angle);poly=[(x*math.cos(a)+y*math.sin(a),-x*math.sin(a)+y*math.cos(a)) for x,y in poly];m=Mesh();rr=[[(x,y,z) for x,y in poly] for z in[z0,z1]]
 for f in earclip(poly):m.face([rr[0][i] for i in f][::-1],3);m.face([rr[1][i] for i in f],3)
 for i in range(len(poly)):j=(i+1)%len(poly);m.face([rr[0][i],rr[0][j],rr[1][j],rr[1][i]],3)
 return m.result('Fixed solid pointed hand with broad octagonal heel, independently axially supported')
DIALS=[];HAND_GROUPS=[]
for label,(u,v,w) in FRAMES.items():
 names={k:label+'_'+k for k in['IntegralIndexDial','HourAxle','FixedHourHand','MinuteAxle','FixedMinuteHand']};d,hx,h,mx,mn=[names[k] for k in names]
 for name,geom in[(d,dial_geometry()),(hx,cylinder(.045,.87,.925,24)),(h,hand_geometry(.31,-60,.925,.95)),(mx,cylinder(.030,.95,.98,24)),(mn,hand_geometry(.40,60,.98,1.005))]:G[name]=transformed(geom,label)
 DIALS.append(d);HAND_GROUPS.append(dict(label=label,dial=d,hour_axle=hx,hour_hand=h,minute_axle=mx,minute_hand=mn))
 for key,a,b,plane,area in[('DialBack',CASE,d,.84,1.05),('HourAxleRoot',d,hx,.87,.0062),('HourHandSeat',hx,h,.925,.0062),('MinuteAxleRoot',h,mx,.95,.0027),('MinuteHandSeat',mx,mn,.98,.0027)]:
  # The clock-box is concave: global halfspace separation is inappropriate for
  # its dial seat. Full noncontact triangle pairs are checked independently.
  seat(label+'_'+key,a,b,w,u,v,plane,[world(label,(0,0,plane))],area,offset=.001,coverage='complete_supported_back' if key=='DialBack' else 'smaller_complete_interface')
# QA-only full finite volumes follow actual geometry; they are never exported.
def opening_profile(radius):return[(-radius,.004),(radius,.004),(radius,1.14)]+[(radius*math.cos(i*math.pi/20),1.14+radius*math.sin(i*math.pi/20)) for i in range(1,21)]
volume(VOID_VOLUMES,'WholeGroundToCrownArchAndBothMouths',loft_y([(y,opening_profile(r)) for y,r in[(-1,.515),(-.8,.515),(-.69,.455),(.69,.455),(.8,.515),(1,.515)]]),list(G),'complete ground-to-crown arch air with both flared reveals and extended front/rear mouths')
for side,sgn in[('Left',-1),('Right',1)]:
 lo,hi=sorted([sgn*.55,sgn*.77]);volume(SOLID_VOLUMES,'Tower_'+side+'_ContinuousArchRoot',box_geometry((lo,-.67,.02),(hi,.67,1.80)),[TOWER],'full finite continuous jamb band from near ground through spring and crown elevations')
volume(SOLID_VOLUMES,'Tower_WholeAboveArchCrown',box_geometry((-.76,-.65,1.67),(.76,.65,3.12)),[TOWER],'continuous full-width crown and square upper tower material')
volume(SOLID_VOLUMES,'ClockBox_WholeCentralCore',box_geometry((-.82,-.82,3.38),(.82,.82,4.82)),[CASE],'finite continuous central box material behind all four blind recesses')
volume(SOLID_VOLUMES,'Roof_ContinuousThickEaveAndCrown',square_loft([(4.87,1.12),(4.98,1.12),(5.05,1.07),(6.02,.13),(6.10,.12)],[0,0,0,0]),[ROOF],'whole inward-offset roof material across all four eaves, slopes and crown')
def annulus(ri,ro,z0,z1,n=48):
 m=Mesh();rr=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for z,r in[(z0,ri),(z0,ro),(z1,ri),(z1,ro)]]
 for i in range(n):
  j=(i+1)%n
  for inds in[( (0,j),(1,j),(1,i),(0,i)),((2,i),(3,i),(3,j),(2,j)),((0,j),(0,i),(2,i),(2,j)),((1,i),(1,j),(3,j),(3,i))]:m.face([rr[a][b] for a,b in inds])
 return m.result('complete closed annular air body')
for group in HAND_GROUPS:
 label=group['label'];d=group['dial']
 volume(VOID_VOLUMES,label+'_WholeBlindRecess',transformed(cylinder(.605,.844,.970),label),[CASE],'whole circular blind recess volume before assembly contents, fully separated from every recess wall and back')
 for key,geom in [('FullDialSurroundAir',annulus(.585,.603,.845,.970)),('FullRaisedIndexToHourLayerAir',annulus(.050,.575,.895,.920)),('FullHourToMinuteLayerAir',annulus(.035,.575,.954,.976))]:volume(VOID_VOLUMES,label+'_'+key,transformed(geom,label),list(G),'complete finite annular clear region excluding only the actual central axle; whole assembly tested')
 volume(SOLID_VOLUMES,label+'_WholeDialBacking',transformed(cylinder(.575,.845,.865),label),[d],'complete finite dial backing below all indices and short hour axle')
 for k in range(12):
  i=k*4;a=math.tau*(i-.5)/N+.008;b=math.tau*(i+.5)/N-.008;poly=[(r*math.cos(t),r*math.sin(t)) for r,t in[(.447,a),(.523,a),(.523,b),(.447,b)]];mm=Mesh();rr=[[(x,y,z) for x,y in poly] for z in[.862,.884]]
  for f in[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:mm.face([(rr[0]+rr[1])[q] for q in f])
  volume(SOLID_VOLUMES,label+'_FiniteIndexRoot_%02d'%k,transformed(mm.result('index root material'),label),[d],'whole finite raised-index root crosses the dial face; no detached marking')
CLOCK_CONTRACT={'single_modular_count':1,'editable_meshes':len(G),'square_tower':True,'whole_through_arch':1,'full_ground_strip_patches':2,'blind_dial_recesses':4,'integral_indices_per_dial':12,'fixed_hour_hands':4,'fixed_minute_hands':4,'real_short_central_axles':8,'hour_angle_degrees':-60,'minute_angle_degrees':60,'thick_four_hip_roof':True,'ground_level_m':0,'origin':'ground-level exact bounds centre','no_timekeeping_motion_or_passage_claim':True}
def measure_clocktower_geometry(vertices):
 assert set(vertices)==set(G)
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices'];assert all(min(math.dist(p,q) for q in actual)<6e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<6e-7 for p in actual),(n,'actual shape changed')
 return dict(CLOCK_CONTRACT,whole_void_groups=len(VOID_VOLUMES),finite_material_volume_groups=len(SOLID_VOLUMES),materials=MATERIAL_CONTRACT)
FOCUS=(0,0,3.04);ORTHO=7.60
CAMERAS={'gray-front3q':(8,-13,8),'gray-back3q':(-8,13,8),'thumbnail':(8,-13,8),'qa-front':(0,-15,4.15),'qa-side':(15,0,4.15),'qa-top':(0,0,16),'qa-back':(0,15,4.15),'qa-wireframe':(8,-13,8),'silhouette-128-front':(0,-15,4.15),'silhouette-128-side':(15,0,4.15)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/1100

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
root=bpy.data.objects.new('OneFourFaceArchClockTower',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground-level exact bounds centre (0,0,0), source Z up and front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
def triangle_ray_hits(triangles,p,d):
 hits=[]
 for a,b,c in triangles:
  e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
  if abs(det)<1e-12:continue
  inv=1/det;ss=sub(p,a);u=dot(ss,h)*inv;q=cross(ss,e1);v=dot(d,q)*inv;t=dot(e2,q)*inv
  if u>=-1e-10 and v>=-1e-10 and u+v<=1+1e-10 and 1e-7<t<20:hits.append(t)
 return hits

def inside(tree,point):
 # Actual loop triangles with Python float64 winding AND three-ray parity.
 # Duplicate shared-edge hits are one boundary crossing. Uncertain cases raise.
 triangles=actual_triangles[id(tree)];p=tuple(float(c) for c in point);omega=0.0
 for a,b,c in triangles:
  a,b,c=sub(a,p),sub(b,p),sub(c,p);la=math.sqrt(dot(a,a));lb=math.sqrt(dot(b,b));lc=math.sqrt(dot(c,c))
  den=la*lb*lc+dot(a,b)*lc+dot(b,c)*la+dot(c,a)*lb
  omega+=2*math.atan2(dot(a,cross(b,c)),den)
 w=abs(omega/(4*math.pi));parities=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  hits=triangle_ray_hits(triangles,p,unit(direction));parities.append(len(set(round(t,8) for t in hits))%2)
 if abs(w-1)<1e-5 and parities==[1,1,1]:return True
 if w<1e-5 and parities==[0,0,0]:return False
 raise AssertionError(('Uncertain winding or ray-parity disagreement',w,parities,point))
inside_predicate_selftests=[]
for name,p,outside in [(TOWER,(.65,0,.5),(0,0,.5)),(CASE,(0,0,4.1),(0,-.91,4.1))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Producer Blender checks below cover actual closed mesh topology, ground and
# opposed contact triangle areas plus auxiliary interior-side probes only.
# Complete void/material bodies, full-interface nonpenetration and all-pair
# boundary acceptance remain independent actual-GLB gates; no full void claim here.
def horizontal_triangles(name,z,up):
 o=byname[name];out=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z-z) for p in vv)<1.1e-6 and cr.z*up>0:out.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 return out
# Finite exact opposed shoulder seats are graph edges, distinct from overlaps.
def clip_area(a,b):
 def cr(a,b):return a[0]*b[1]-a[1]*b[0]
 if cr(sub(b[1],b[0]),sub(b[2],b[0]))<0:b=list(reversed(b))
 poly=list(a)
 for p,q in zip(b,b[1:]+b[:1]):
  old=poly;poly=[]
  if not old:break
  for s,e in zip(old,old[1:]+old[:1]):
   ds=cr(sub(q,p),sub(s,p));de=cr(sub(q,p),sub(e,p));si=ds>=-1e-12;ei=de>=-1e-12
   if si!=ei:poly.append(add(s,mul(sub(e,s),ds/(ds-de))))
   if ei:poly.append(e)
 return abs(sum(cr(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2 if len(poly)>2 else 0
face_contacts=[]
for r in CONTACTS:
 def local(p):
  q=sub(p,r['origin_m']);return(dot(q,r['u']),dot(q,r['v']),dot(q,r['axis']))
 def seat_triangles(name,sign):
  out=[];o=byname[name]
  for t in o.data.loop_triangles:
   q=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in t.vertices]
   if max(abs(p[2]-r['plane_m']) for p in q)<1.1e-6 and cross(sub(q[1],q[0]),sub(q[2],q[0]))[2]*sign>0:out.append(q)
  return out
 aa=seat_triangles(r['a'],1);bb=seat_triangles(r['b'],-1)
 area=sum(clip_area([p[:2] for p in a],[p[:2] for p in b]) for a in aa for b in bb)
 assert area>=r['minimum_patch_area_m2'],(r,area)
 for p in r['points']:
  down=sub(p,mul(r['axis'],r['interior_probe_offset_m']));up=add(p,mul(r['axis'],r['interior_probe_offset_m']))
  assert inside(trees[r['a']],down) and inside(trees[r['b']],up) and not inside(trees[r['a']],up) and not inside(trees[r['b']],down)
 face_contacts.append(dict(r,actual_opposed_triangle_contact_area_m2=area))

adj={o.name:set() for o in parts}
for j in joints+face_contacts:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
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
 blockers=[name for name,t in trees.items() if name in r.get('targets',trees) and t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
mount_evidence=measure_clocktower_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_modular_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'clocktower_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'producer_check_scope':'Actual closed mesh topology, degeneracy, finite ground triangles, opposed contact triangle area and auxiliary interior-side probes, oriented GLB/PBR readback only. Whole void/material volumes, complete interface nonpenetration and all-pair boundary acceptance remain independent actual-GLB gates.',
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/timekeeping/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'modular','assetKind':'modular','theme':'timekeeping','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-6,-8,11),1800,7),('Fill',(7,-3,7),1100,6),('Rim',(3,8,9),1500,5)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={k:CAMERAS[k] for k in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={};qa['render_source_actual_glb_match']=qa['fresh_actual_glb_guard']
def render(name,pos):
 cam.data.ortho_scale=ORTHO
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
 for name,pos in [(name,CAMERAS[name]) for name in ['silhouette-128-front','silhouette-128-side']]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
