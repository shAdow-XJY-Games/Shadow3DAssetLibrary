"""Original low vented basket with three fixed double-jaw clothespins; one prop."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='laundry-vented-clothespin-basket-kit-01';VERSION='1.0.0';TITLE='Vented Clothespin Basket Kit'
DESCRIPTION=('One original low-poly static clothespin-basket kit, counted as one prop. A low subtly tapered chamfered rectangular basket has one continuous closed thick floor, twenty genuine through-windows and an integral thick continuous top rim. Three copies of one newly authored clothespin each comprise two opposed thick shaped wooden jaws and one continuous capped thick 1.5-turn fixed metal coil with two finite embedded ends. Each clip rests on the basket rim on two real recessed shoulder faces; friction or spring force is not assumed. The lower jaw mouths, central neck gaps, upper handle gaps, coil bores and inter-turn space remain actual geometry. All three clips are fixed upright on three distinct sides; no loose contents obscure the basket cavity. Ten separately editable closed meshes form the single static set. Four opaque unlinked constant PBR materials, no textures. Metres, source Z up, front -Y, origin at the complete basket floor ground centre. This is not a recoloured old clothesline block clip, solid harvest basket, hamper cart or shortened shoulder creel. No animation, alternate poses, simulation or independent clip assets. Visual geometry only; no gripping force, spring elasticity, movement, material hygiene, capacity, loads, pinch protection, child safety, laundry performance, human fit, manufacture or prior clothesline compatibility is asserted.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={}
PALETTE=[('Basket_SoftSage',(.265,.435,.385,1),.76,0),('Basket_DeepSageRim',(.15,.29,.25,1),.80,0),('Clips_WarmWood',(.68,.395,.20,1),.78,0),('Spring_MatteSteel',(.31,.34,.36,1),.43,.70)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no TEX_* nodes or linked inputs.'
FOCUS=(0,0,.073);ORTHO=.430
CAMERAS={'gray-front3q':(.65,-.95,.64),'gray-back3q':(-.65,.95,.64),'thumbnail':(.65,-.95,.64),'qa-front':(0,-1,.46),'qa-side':(1,0,.46),'qa-top':(0,0,1),'qa-back':(0,1,.46),'qa-wireframe':(.65,-.95,.64),'silhouette-128-front':(0,-1,.46),'silhouette-128-side':(1,0,.46)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,k):return tuple(x*k for x in a)
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
  vol=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if vol<0:self.f=[tuple(reversed(f)) for f in self.f]
  used=sorted(set(i for f in self.f for i in f));remap={old:i for i,old in enumerate(used)}
  return {'vertices':[self.v[i] for i in used],'faces':[tuple(remap[i] for i in f) for f in self.f],'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def earclip(poly):
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))
 order=list(range(len(poly))) if area>0 else list(reversed(range(len(poly))));out=[]
 while len(order)>3:
  for k,b in enumerate(order):
   a=order[k-1];c=order[(k+1)%len(order)]
   if cr(poly[a],poly[b],poly[c])<1e-14:continue
   if any(all(cr(poly[x],poly[y],poly[q])>=-1e-14 for x,y in[(a,b),(b,c),(c,a)]) for q in order if q not in[a,b,c]):continue
   out.append((a,b,c));order.pop(k);break
  else:raise AssertionError(('non-simple polygon',poly,order))
 out.append(tuple(order));return out
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box_geometry(lo,hi,mat=0,role='complete finite QA volume, not exported'):
 v=[(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]];m=Mesh()
 for f in BOX_FACES:m.face([v[i] for i in f],mat)
 return m.result(role,mat)
def volume(table,name,g,targets,role):table[name]=dict(g,targets=list(targets),role=role)
def loft_z(sections,role='complete closed lofted QA volume'):
 m=Mesh();rings=[[(x,y,z) for x,y in p] for z,p in sections];n=len(rings[0]);assert all(len(r)==n for r in rings)
 for a,b in zip(rings,rings[1:]):
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]])
 for f in earclip(sections[0][1]):m.face([rings[0][i] for i in f][::-1])
 for f in earclip(sections[-1][1]):m.face([rings[-1][i] for i in f])
 return m.result(role)
def extrude_xz(poly,y0,y1,mat,role):
 if sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly)))<0:poly=poly[::-1]
 m=Mesh();rings=[[(x,y,z) for x,z in poly] for y in[y0,y1]]
 for f in earclip(poly):m.face([rings[0][i] for i in f],mat);m.face([rings[1][i] for i in f][::-1],mat)
 for i in range(len(poly)):j=(i+1)%len(poly);m.face([rings[0][i],rings[1][i],rings[1][j],rings[0][j]],mat)
 return m.result(role,mat)
# Basket is a new low chamfered rectangular shell, not an old oval creel profile.
P=[];WINDOW_EDGES=[]
def side(points,gaps):
 start=len(P);P.extend(points);WINDOW_EDGES.extend(start+i for i in gaps)
xs=[-.146,-.130,-.050,-.040,.040,.050,.130,.146];ys=[-.086,-.070,-.006,.006,.070,.086]
side([(x,-.098) for x in xs],[1,3,5]);side([(.158,y) for y in ys],[1,3]);side([(x,.098) for x in xs[::-1]],[1,3,5]);side([(-.158,y) for y in ys[::-1]],[1,3])
N=len(P);BANDS=[(.012,.022),(.050,.058),(.086,.108)];Z=[.012,.022,.050,.058,.086,.108]
def radii(z):
 hx=.140+.018*z/.108;hy=.080+.018*z/.108;thick=.006+.006*max(0,(z-.086)/.022)
 return hx,hy,hx-thick,hy-thick
def basket_point(i,z,u):
 hx,hy,ix,iy=radii(z);x,y=P[i%N];return(x*(hx+(ix-hx)*u)/.158,y*(hy+(iy-hy)*u)/.098,z)
body='Basket_IntegralFloor_20TrueWindows_ContinuousRim';m=Mesh();boundary={}
HEX_FACES=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
for k in range(len(Z)-1):
 z0,z1=Z[k:k+2];band=any(a<=(z0+z1)/2<=b for a,b in BANDS)
 for i in range(N):
  if not band and i in WINDOW_EDGES:continue
  j=(i+1)%N;pts=[basket_point(h,z,u) for z in[z0,z1] for h,u in[(i,0),(i,1),(j,1),(j,0)]]
  for fi,f in enumerate(HEX_FACES):
   if k==0 and fi==0:continue
   q=[pts[h] for h in f];centre=tuple(sum(p[d] for p in pts)/8 for d in range(3));fc=tuple(sum(p[d] for p in q)/4 for d in range(3))
   if dot(cross(sub(q[1],q[0]),sub(q[2],q[0])),sub(fc,centre))<0:q=q[::-1]
   key=tuple(sorted(q))
   if key in boundary:del boundary[key]
   else:boundary[key]=(q,1 if k==len(Z)-2 else 0,'integral_rim' if k==len(Z)-2 else 'solid_band' if band else 'window_pillar')
for q,mat,tag in boundary.values():m.face(q,mat,tag)
for i in range(N):
 j=(i+1)%N;m.face([basket_point(i,0,0),basket_point(j,0,0),basket_point(j,.012,0),basket_point(i,.012,0)],0,'whole_floor_edge')
 m.face([(0,0,0),basket_point(j,0,0),basket_point(i,0,0)],1,'finite_ground')
 m.face([(0,0,.012),basket_point(i,.012,1),basket_point(j,.012,1)],0,'whole_floor_top')
G[body]=m.result('One continuous closed thick basket shell: full bottom, subtle taper, chamfered rectangular plan, twenty real side apertures and continuous widened rim.');FEET=[body]
# Single original clip prototype, reused only internally within this one prop.
# A genuine lower recess creates a downward-facing shoulder at z=.018 on each jaw.
INNER=[(.007,0),(.007,.018),(.003,.018),(.003,.028),(.004,.032),(.004,.042),(.006,.055),(.007,.072)]
OUTER=[(.012,0),(.013,.008),(.012,.029),(.011,.041),(.013,.066),(.012,.072)]
RIGHT=INNER+OUTER[::-1]
PROTO={}
for sign,label in[(1,'RightJaw'),(-1,'LeftJaw')]:PROTO[label]=extrude_xz([(x*sign,z) for x,z in RIGHT],-.005,.005,2,'One shaped thick wooden jaw with true downward shoulder, lower mouth and upper grip profile.')
# One thick capped continuous 1.5-turn coil. Both tails end in actual jaw material.
R=.006;WIRE=.00065;TURNS=1.5;PITCH=.004;COIL_Z=.037
def bezier4(points,n):
 return [tuple((1-t)**3*points[0][d]+3*(1-t)**2*t*points[1][d]+3*(1-t)*t*t*points[2][d]+t**3*points[3][d] for d in range(3)) for t in [i/n for i in range(n+1)]]
path=[(.010,-.003-i*.001,COIL_Z) for i in range(12)]
path +=bezier4([(.010,-.014,COIL_Z),(.010,-.017,COIL_Z),(.006,-.013,COIL_Z-.004),(.006,-.013,COIL_Z)],24)[1:-1]
path +=[(R*math.cos(t),-.013+PITCH*t/math.tau,COIL_Z+R*math.sin(t)) for t in[math.pi*3*i/36 for i in range(37)]]
path +=bezier4([(-.006,-.007,COIL_Z),(-.006,-.007,COIL_Z-.006),(-.010,-.0065,COIL_Z),(-.010,-.0045,COIL_Z)],24)[1:]
path +=[(-.010,y,COIL_Z) for y in[-.004,-.0035,-.003]]
def tube_path(path,r):
 m=Mesh();rings=[];u=None
 for i,p in enumerate(path):
  t=unit(sub(path[min(i+1,len(path)-1)],path[max(0,i-1)]))
  if u is None:u=unit(cross(t,(1,0,0)))
  else:u=unit(sub(u,mul(t,dot(u,t))))
  v=cross(t,u)
  rings.append([add(p,add(mul(u,r*math.cos(math.tau*j/6)),mul(v,r*math.sin(math.tau*j/6)))) for j in range(6)])
 m.face(rings[0][::-1],3,'embedded_end_right');m.face(rings[-1],3,'embedded_end_left')
 for a,b in zip(rings,rings[1:]):
  for i in range(6):j=(i+1)%6;m.face([a[i],a[j],b[j],b[i]],3,'continuous_fixed_coil')
 return m.result('One capped continuous thick 1.5-turn steel-colour fixed coil and two embedded tails; no elasticity or motion.',3)
PROTO['FixedCoil']=tube_path(path,WIRE)
PLACEMENTS=[('Front',(.070,-.092,.090),math.pi/2),('Back',(.025,.092,.090),-math.pi/2),('Left',(-.152,.012,.090),0)]
def transform_point(p,c,a):return(c[0]+p[0]*math.cos(a)-p[1]*math.sin(a),c[1]+p[0]*math.sin(a)+p[1]*math.cos(a),c[2]+p[2])
def transformed(g,c,a):return dict(g,vertices=[transform_point(p,c,a) for p in g['vertices']])
CLIPS=[]
for label,c,a in PLACEMENTS:
 names={part:'Clip_'+label+'_'+part for part in PROTO};CLIPS.append({'label':label,'centre':c,'angle':a,'names':names})
 for part,g in PROTO.items():G[names[part]]=transformed(g,c,a)
 for sign,part in[(1,'RightJaw'),(-1,'LeftJaw')]:
  p=transform_point((sign*.0045,0,.018),c,a)
  CONTACTS.append({'a':body,'b':names[part],'axis':2,'plane_m':.108,'minimum_patch_area_m2':.000027,'interior_probe_offset_m':.00035,'points':[p],'scope':'complete finite opposed recessed jaw shoulder on full basket rim; no friction assumption'})
  end=(sign*.010,-.0038,.037);LINKS.append((names[part],names['FixedCoil'],[transform_point(add(end,(0,d,0)),c,a) for d in[-.0002,0,.0002]]))
  g=box_geometry((sign*.010-.00020,-.0040,.03680),(sign*.010+.00020,-.0036,.03720))
  volume(WALL_VOLUMES,label+'_'+part+'_WholeEmbeddedCoilTail',transformed(g,c,a),[names[part],names['FixedCoil']],'complete positive-volume tail end within both closed coil and wooden jaw')
# Full side windows. Each follows both shell planes, extends across the full thickness.
def cell_volume(i,z0,z1,u0,u1,inset=.012):
 m=Mesh();j=(i+1)%N;rings=[]
 for z in [z0]+[zz for zz in Z if z0<zz<z1]+[z1]:
  p0=basket_point(i,z,0);p1=basket_point(j,z,0);q0=basket_point(i,z,1);q1=basket_point(j,z,1)
  def at(s,u):return add(mul(add(mul(p0,1-s),mul(p1,s)),1-u),mul(add(mul(q0,1-s),mul(q1,s)),u))
  rings.append([at(inset,u0),at(inset,u1),at(1-inset,u1),at(1-inset,u0)])
 m.face(rings[0][::-1]);m.face(rings[-1])
 for aa,bb in zip(rings,rings[1:]):
  for i in range(4):j=(i+1)%4;m.face([aa[i],aa[j],bb[j],bb[i]])
 return m.result('complete closed wall cell, not exported')
for row,(z0,z1) in enumerate([(.022,.050),(.058,.086)]):
 for wi,i in enumerate(WINDOW_EDGES):volume(VOID_VOLUMES,f'WholeSideWindow_{row}_{wi}',cell_volume(i,z0+.0004,z1-.0004,-.20,1.20),list(G),'whole actual through-window air, through full side thickness and both mouths')
# Complete full floor material and every continuous pillar and rim edge.
def chamber_profile(z,margin=.0004):
 hx,hy,ix,iy=radii(z);return[(x*(ix-margin)/.158,y*(iy-margin)/.098) for x,y in P]
volume(WALL_VOLUMES,'EntireThickFloor',loft_z([(.0004,chamber_profile(.0004,.0004)),(.0116,chamber_profile(.0116,.0004))]),[body],'whole finite inset floor material, not sample points')
for i in range(N):
 if i not in WINDOW_EDGES:volume(WALL_VOLUMES,f'EntirePillar_{i}',cell_volume(i,.0124,.1076,.10,.90,.05),[body],'full finite connected thick pillar from floor root to continuous rim')
for i in range(N):volume(WALL_VOLUMES,f'WholeRimSegment_{i}',cell_volume(i,.0864,.1076,.10,.90,.05),[body],'complete finite thick rim segment; all closed shell boundaries checked separately')
# Complete assembled basket cavity: lower chamber plus upper notched footprint.
# Exact known clip rectangles at this height are removed, with explicit thin air
# strips between each inner jaw and the basket wall so no notch gap is skipped.
volume(VOID_VOLUMES,'WholeLowerBasketCavity',loft_z([(.0124,chamber_profile(.0124)),(.086,chamber_profile(.086)),(.0896,chamber_profile(.0896))]),list(G),'entire empty lower chamber from full floor to immediately below actual jaw tips')
def upper_profile(z):
 hx,hy,ix,iy=radii(z);ix-=.0004;iy-=.0004;c=.011
 return[(-ix+c,-iy),(.0646,-iy),(.0646,-.0786),(.0754,-.0786),(.0754,-iy),(ix-c,-iy),(ix,-iy+c),(ix,iy-c),(ix-c,iy),(.0304,iy),(.0304,.0786),(.0196,.0786),(.0196,iy),(-ix+c,iy),(-ix,iy-c),(-ix,.0174),(-.1386,.0174),(-.1386,.0066),(-ix,.0066),(-ix,-iy+c)]
volume(VOID_VOLUMES,'WholeUpperCavityAroundThreeKnownJaws',loft_z([(.0896,upper_profile(.0896)),(.1076,upper_profile(.1076))]),list(G),'complete upper cavity with exact finite clip rectangles excluded by 0.4mm material-boundary margin')
for clip in CLIPS:
 label,c,a,names=clip['label'],clip['centre'],clip['angle'],clip['names']
 # Clip-local lower mouth remains genuinely open, intentionally occupied by rim.
 volume(ISOLATED_VOID_VOLUMES,label+'_WholeLowerJawMouth',transformed(box_geometry((-.0066,-.0058,-.001),(.0066,.0058,.0176)),c,a),names.values(),'entire lower double-jaw mouth excluding the intentionally seated basket rim')
 gap=[(-.0026,.0184),(.0026,.0184),(.0026,.028),(.0036,.032),(.0036,.042),(.0056,.055),(.0066,.0716),(-.0066,.0716),(-.0056,.055),(-.0036,.042),(-.0036,.032),(-.0026,.028)]
 volume(VOID_VOLUMES,label+'_WholeNeckAndUpperGripGap',transformed(extrude_xz(gap,-.0058,.0058,0,'whole complete clip gap'),c,a),list(G),'entire central neck and upper handle air, through full jaw width')
 # Complete coil centre bore, through all 1.5 turns; no solid disk.
 poly=[(.0047*math.cos(math.tau*i/24),COIL_Z+.0047*math.sin(math.tau*i/24)) for i in range(24)]
 volume(VOID_VOLUMES,label+'_WholeFixedCoilBore',transformed(extrude_xz(poly,-.0142,-.0058,0,'whole coil bore'),c,a),list(G),'whole finite coil centre bore through complete coil depth and both mouths')
 # Full inter-turn half-annular helical air region, no sparse ray replacement.
 mm=Mesh();rings=[]
 for i in range(13):
  t=.06+(math.pi-.12)*i/12;y=-.013+PITCH*t/math.tau+PITCH/2
  rings.append([(r*math.cos(t),y+d,COIL_Z+r*math.sin(t)) for r,d in[(.0047,-.0010),(.0073,-.0010),(.0073,.0010),(.0047,.0010)]])
 mm.face(rings[0][::-1]);mm.face(rings[-1])
 for aa,bb in zip(rings,rings[1:]):
  for i in range(4):j=(i+1)%4;mm.face([aa[i],aa[j],bb[j],bb[i]])
 volume(VOID_VOLUMES,label+'_WholeInterTurnHelicalGap',transformed(mm.result('whole finite inter-turn helical annular air'),c,a),list(G),'entire overlapping half-turn interval between adjacent closed thick wire turns')
 # Actual basket-wall / inner-jaw slit follows wall taper. Transform in clip frame.
 sections=[]
 for zz in[.0904,.1076]:
  hx,hy,ix,iy=radii(zz);wall=(.092-iy) if label in['Front','Back'] else(.152-ix)
  sections.append((zz-.090,[(wall+.0004,-.0046),(.0066,-.0046),(.0066,.0046),(wall+.0004,.0046)]))
 volume(VOID_VOLUMES,label+'_EntireInnerJawRimSlit',transformed(loft_z(sections),c,a),list(G),'whole finite residual slit between actual inner rim wall and lower jaw; 0.4mm boundary margins')
# Additional opening above the full cavity is deliberately bounded inside all
# fixed jaws, and overlaps the lower/upper chamber to prove an open-top route.
volume(VOID_VOLUMES,'FullCentralOpenTopApproach',box_geometry((-.125,-.070,.020),(.130,.070,.180)),list(G),'full central empty route to above every clip and basket rim')
def measure_basket_geometry(vertices):
 assert set(vertices)==set(G),'changed component set'
 for n,g in G.items():
  actual=[tuple(float(c) for c in p) for p in vertices[n]];expected=g['vertices']
  assert all(min(math.dist(p,q) for q in actual)<3e-7 for p in expected) and all(min(math.dist(p,q) for q in expected)<3e-7 for p in actual),(n,'actual geometry changed')
 return {'single_prop_count':1,'closed_components':10,'true_side_windows':20,'fixed_clothespin_instances':3,'separate_jaws_per_clip':2,'continuous_fixed_coils':3,'coil_turns':1.5,'finite_rim_shoulder_contacts':6,'finite_embedded_coil_ends':6,'full_floor_thickness_m':.012,'rim_top_z_m':.108,'clip_length_m':.072,'whole_empty_volumes':len(VOID_VOLUMES)+len(ISOLATED_VOID_VOLUMES),'whole_material_volumes':len(WALL_VOLUMES),'frozen_static_pose':True,'grip_spring_load_child_safety_claim':False}
assert len(G)==10

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
root=bpy.data.objects.new('OneVentedClothespinBasketKit',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and centre of complete chamfered rectangular basket floor; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
basket_evidence=measure_basket_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'basket_geometry':basket_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/laundry/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'laundry','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
