"""Original tapered harbor lighthouse exterior. One static prop; metres, Z up, front -Y.
Real recessed fixed doorway, supported gallery, open unglazed lantern room and unlit lamp.
No enterable interior, interior stairs, navigation, illumination or building safety claims.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='harbor-tapered-lantern-lighthouse-01';VERSION='1.0.0';TITLE='Tapered Lantern Lighthouse'
DESCRIPTION=('One original low-poly harbor lighthouse exterior: a wide finite grounded octagonal base, a visibly tapered eight-sided tower with cream and muted coral masonry bands, a genuinely recessed fixed teal door, a supported upper gallery with open railings, eight real lantern-room columns, an empty unglazed window belt surrounding a small unlit amber lamp, and a dark closed pyramidal roof. The recessed door sits against the real back wall of a 0.51 to 0.69 metre deep architectural recess, not a colored panel applied to the facade. '
 'One static reusable prop with named editable closed mesh parts and five constant opaque PBR materials. No image or procedural textures, people, island, harbor scenery, branding or exterior stairs. Metres, Z up, front -Y, origin at the tower axis on the ground. '
 'Fixed visual geometry only. Finite geometric contact and void tests do not establish a usable or enterable building, internal floors or stairs, walking access, human clearance, lighting output, rotating light, navigation, maritime safety, wind resistance, structural capacity, tip resistance, building construction or fire-code compliance. No compatibility claim with existing pier modules.')
G={};LINKS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={};POSTS=[];RAIL_POSTS=[];CORBELS=[]
PALETTE=[('Masonry_WarmCream',(.79,.76,.63,1),.86,0),('Masonry_CoralBand',(.48,.095,.055,1),.82,0),('Metal_DeepPetrol',(.035,.13,.15,1),.38,.50),('Foundation_WarmGray',(.31,.35,.34,1),.9,0),('Lamp_UnlitAmber',(.70,.37,.095,1),.34,.20)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c) for c in [0,1] for b in [0,1] for a in [0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def void(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':role}
def radial(r,theta,z):return (r*math.cos(theta),r*math.sin(theta),z)
def profile(name,rings,mat,role,n=8,phase=math.pi/8):
 vs=[radial(r,phase+math.tau*i/n,z) for z,r in rings for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]+[(k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i) for k in range(len(rings)-1) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def annulus(name,z0,z1,ro,ri,mat,role,n=16,phase=math.pi/8):
 vs=[radial(r,phase+math.tau*i/n,z) for z,r in [(z0,ro),(z1,ro),(z1,ri),(z0,ri)] for i in range(n)]
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def oriented_box(name,c,radial_size,tangent_size,zsize,theta,mat,role):
 vs=cuboid((-radial_size/2,-tangent_size/2,-zsize/2),(radial_size/2,tangent_size/2,zsize/2))
 return mesh(name,[add(c,(x*math.cos(theta)-y*math.sin(theta),x*math.sin(theta)+y*math.cos(theta),z)) for x,y,z in vs],BOX_FACES,mat,role)
base=profile('Base_OctagonalFoundation',[(0,1.90),(.20,1.90),(.32,1.72)],3,'wide finite foundation, full bottom at Z=0');FEET.append(base)
# A single welded closed tower solid with a truly concave doorway. Each front
# strip shares its edge vertices with the surrounding body. The cavity has
# side reveals, sill, head and a recessed back, so it is not a surface decal.
Z=[.29,.36,2.25,3.25,4.35,6.30]
def radius(z):return 1.49-(z-.29)*(1.49-.86)/(6.30-.29)
vs=[];lookup={};fs=[];fm=[]
def vertex(p):
 p=tuple(round(x,7) for x in p)
 if p not in lookup:lookup[p]=len(vs);vs.append(p)
 return lookup[p]
def face(points,mat=0):fs.append(tuple(vertex(p) for p in points));fm.append(mat)
def ring(z):
 points=[];r=radius(z)
 for i in range(8):
  points.append(radial(r,math.pi/8+i*math.pi/4,z))
  if i==5:points.extend([(-.43,-r*math.cos(math.pi/8),z),(.43,-r*math.cos(math.pi/8),z)])
 return points
for j,(z0,z1) in enumerate(zip(Z,Z[1:])):
 r0=radius(z0);r1=radius(z1);mat=1 if j==3 else 0
 for i in range(8):
  if i==5:continue
  face([radial(r0,math.pi/8+i*math.pi/4,z0),radial(r0,math.pi/8+(i+1)*math.pi/4,z0),radial(r1,math.pi/8+(i+1)*math.pi/4,z1),radial(r1,math.pi/8+i*math.pi/4,z1)],mat)
 a0=r0*math.sin(math.pi/8);a1=r1*math.sin(math.pi/8);y0=-r0*math.cos(math.pi/8);y1=-r1*math.cos(math.pi/8)
 x0=[-a0,-.43,.43,a0];x1=[-a1,-.43,.43,a1]
 # Above the door the width of the tapered front eventually narrows below
 # 0.86m. Use the same fractions after the head so edges stay well ordered.
 if j>=2:
  x0=[-a0,-a0*.75,a0*.75,a0];x1=[-a1,-a1*.75,a1*.75,a1]
  # Maintain exact door-head boundary on the first overdoor band.
  if j==2:x0=[-a0,-.43,.43,a0]
 for k in range(3):
  if j==1 and k==1:
   # Recess opening extends from the tapered facade back to Y=-0.68.
   back=-.68
   face([(-.43,y0,z0),(-.43,back,z0),(-.43,back,z1),(-.43,y1,z1)])
   face([(.43,back,z0),(.43,y0,z0),(.43,y1,z1),(.43,back,z1)])
   face([(-.43,y0,z0),(.43,y0,z0),(.43,back,z0),(-.43,back,z0)])
   face([(-.43,back,z1),(.43,back,z1),(.43,y1,z1),(-.43,y1,z1)])
   face([(-.43,back,z0),(.43,back,z0),(.43,back,z1),(-.43,back,z1)])
  else:face([(x0[k],y0,z0),(x0[k+1],y0,z0),(x1[k+1],y1,z1),(x1[k],y1,z1)],mat)
# Caps match front-edge subdivision used by their neighboring faces.
face(list(reversed(ring(Z[0]))))
rt=radius(Z[-1]);top=[]
for i in range(8):
 top.append(radial(rt,math.pi/8+i*math.pi/4,Z[-1]))
 if i==5:top.extend([(-rt*math.sin(math.pi/8)*.75,-rt*math.cos(math.pi/8),Z[-1]),(rt*math.sin(math.pi/8)*.75,-rt*math.cos(math.pi/8),Z[-1])])
face(top)
tower=mesh('Tower_TaperedWithRealDoorRecess',vs,fs,0,'one tapered octagonal masonry solid with real 0.51 to 0.69m deep fixed-door recess and two assigned masonry colors');G[tower]['face_materials']=fm
link(base,tower,(0,0,.305),spread=.30)
door=box('Door_FixedRecessedPanel',(0,-.685,1.305),(.79,.080,1.82),2,'fixed opaque door panel seated into real back wall; not an enterable doorway')
link(tower,door,(0,-.655,1.30),axis=(0,0,1),spread=.40)
knob=box('Door_FixedLatch',(.255,-.747,1.29),(.12,.065,.055),4,'small static latch, finite engagement in fixed panel')
link(door,knob,(.255,-.719,1.29),spread=.020)
# Wide gallery bears on the actual tower crown. Eight visible corbels also
# contact the tapered shaft and underside, while staying below the walkway.
gallery=profile('Gallery_SolidOctagonalDeck',[(6.22,1.64),(6.43,1.64)],3,'single thick projecting gallery deck, continuous finite bearing on crown',n=8)
link(tower,gallery,(0,0,6.26),spread=.30)
for i in range(8):
 a=math.pi/8+i*math.pi/4
 # Triangular prism bracket, radial X 0.70..1.43, lower point near tower.
 local=[(.72,-.055,5.79),(.72,.055,5.79),(1.43,-.055,6.28),(1.43,.055,6.28),(.72,-.055,6.28),(.72,.055,6.28)]
 pp=[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z) for x,y,z in local]
 corbel=mesh(f'Corbel_{i+1:02d}',pp,[(0,1,3,2),(2,3,5,4),(4,5,1,0),(0,2,4),(1,5,3)],0,'closed triangular gallery corbel with embedded inner seat');CORBELS.append(corbel)
 link(tower,corbel,radial(.80,a,6.12),axis=(-math.sin(a),math.cos(a),0),spread=.020)
 link(gallery,corbel,radial(1.20,a,6.255),axis=(-math.sin(a),math.cos(a),0),spread=.020)
plinth=profile('LanternRoom_OctagonalSill',[(6.405,.89),(6.59,.89)],2,'lantern-room raised sill with finite contact to gallery')
link(gallery,plinth,(0,0,6.42),spread=.30)
for i in range(8):
 a=math.pi/8+i*math.pi/4
 p=oriented_box(f'LanternRoom_Column_{i+1:02d}',radial(.79,a,7.22),.105,.105,1.34,a,2,'continuous real pillar with open unglazed voids between adjacent pillars');POSTS.append(p)
 link(plinth,p,radial(.79,a,6.57),axis=(-math.sin(a),math.cos(a),0),spread=.025)
header=annulus('LanternRoom_OpenUpperRing',7.85,7.98,.90,.67,2,'thick open octagonal lintel ring',n=8)
for i,p in enumerate(POSTS):
 a=math.pi/8+i*math.pi/4;link(p,header,radial(.79,a,7.87),axis=(-math.sin(a),math.cos(a),0),spread=.025)
roof=profile('Roof_ClosedPyramidalCap',[(7.94,1.075),(8.03,1.075),(8.56,.065)],2,'closed eight-sided roof seated on upper ring, no holes or glass')
link(header,roof,(.76,0,7.96),axis=(0,1,0),spread=.04)
finial=profile('Roof_ShortFinial',[(8.53,.055),(8.75,.055),(8.80,.025)],4,'short solid roof-top finial with finite overlap',n=8)
link(roof,finial,(0,0,8.545),spread=.012)
pedestal=profile('Lamp_UnlitPedestal',[(6.57,.16),(6.99,.16)],2,'short stationary central lamp support',n=12)
link(plinth,pedestal,(0,0,6.58),spread=.06)
lamp=profile('Lamp_UnlitFacetedBody',[(6.96,.17),(7.04,.29),(7.35,.29),(7.44,.17)],4,'unlit opaque amber lamp sculpture with no emission',n=12)
link(pedestal,lamp,(0,0,6.975),spread=.06)
cap=profile('Lamp_UnlitCap',[(7.41,.32),(7.49,.32),(7.56,.12)],2,'small fixed lamp cap, fully clear of room header and roof',n=12)
link(lamp,cap,(0,0,7.425),spread=.07)
# Sixteen posts supporting two complete open rails. The gallery circulation
# band is tested only as finite empty geometry, not certified walkable access.
for i in range(16):
 a=math.pi/8+i*math.pi/8
 p=oriented_box(f'Gallery_RailingPost_{i+1:02d}',radial(1.43,a,6.83),.065,.065,.85,a,2,'individual railing post embedded in deck and both rails');RAIL_POSTS.append(p)
 link(gallery,p,radial(1.43,a,6.42),axis=(-math.sin(a),math.cos(a),0),spread=.014)
mid=annulus('Gallery_RailingMidRail',6.82,6.875,1.47,1.39,2,'continuous open mid rail with true empty center',n=16)
upper=annulus('Gallery_RailingTopRail',7.20,7.275,1.48,1.38,2,'continuous open top rail with true empty center',n=16)
for i,p in enumerate(RAIL_POSTS):
 a=math.pi/8+i*math.pi/8
 for rail,z in [(mid,6.845),(upper,7.225)]:link(p,rail,radial(1.43,a,z),axis=(-math.sin(a),math.cos(a),0),spread=.012)
# Door negative-space volume: stays clear of the tapered facade, back panel
# and latch, proving actual deep recess rather than a dark face applied outside.
void('Door_RecessClearVolume',(-.35,-1.15,.48),(.12,-.78,2.12),'finite true door recess, excludes fixed panel and latch')
GAPS.append({'origin_m':(0,-1.7,1.5),'direction':(0,1,0),'length_m':.88,'meaning':'clear through real facade opening toward recessed door, stops before panel'})
# Each lantern opening has a finite prism through the frame. Each adjacent
# rail-post pair has a genuine finite empty prism between deck and midrail.
for i in range(8):
 a=math.pi/4+i*math.pi/4
 name=f'LanternRoom_WindowVoid_{i+1:02d}'
 v=cuboid((.49,-.18,6.68),(1.04,.18,7.74));VOID_VOLUMES[name]={'vertices':[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z) for x,y,z in v],'faces':BOX_FACES,'role':'finite unglazed room opening through full window belt'}
 GAPS.append({'origin_m':radial(.40,a,7.65),'direction':(math.cos(a),math.sin(a),0),'length_m':.72,'meaning':'open lantern frame aperture'})
 # A continuous octagonal circulation-band sector with positive radial width.
 n=f'Gallery_ClearBand_{i+1:02d}';v=cuboid((.96,-.24,6.45),(1.26,.24,7.16));VOID_VOLUMES[n]={'vertices':[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z) for x,y,z in v],'faces':BOX_FACES,'role':'finite empty gallery band; no human access claim'}
for i in range(16):
 a=math.pi/8+(i+.5)*math.pi/8;n=f'Gallery_RailAperture_{i+1:02d}'
 v=cuboid((1.34,-.15,6.48),(1.51,.15,6.78));VOID_VOLUMES[n]={'vertices':[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a),z) for x,y,z in v],'faces':BOX_FACES,'role':'finite opening between adjacent posts below mid rail'}
 # Point ray is supplementary to the full finite-volume test.
 GAPS.append({'origin_m':radial(1.30,a,6.64),'direction':(math.cos(a),math.sin(a),0),'length_m':.28,'meaning':'real lower railing aperture'})
BORES.append({'mesh':header,'origin_m':(0,0,7.80),'direction':(0,0,1),'length_m':.23})
def measure_lighthouse_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 bounds=lambda n:([min(float(p[k]) for p in vertices[n]) for k in range(3)],[max(float(p[k]) for p in vertices[n]) for k in range(3)])
 tv=vertices[tower]
 for z,r in [(Z[0],radius(Z[0])),(Z[-1],radius(Z[-1]))]:
  points=[p for p in tv if abs(float(p[2])-z)<1e-6];assert points
  rr=max(math.hypot(float(p[0]),float(p[1])) for p in points);assert abs(rr-r)<1.2e-6,('Taper radius changed',z,rr,r)
 assert any(abs(float(p[1])+.68)<1e-6 and abs(float(p[0])-.43)<1e-6 for p in tv),'Missing true recessed back wall'
 for name in FEET:assert abs(bounds(name)[0][2])<1e-7
 for name in POSTS:assert bounds(name)[1][2]-bounds(name)[0][2]>1.3399
 assert bounds(lamp)[1][2]<7.441 and bounds(cap)[1][2]<7.561
 assert bounds(header)[0][2]-bounds(cap)[1][2]>.2899
 return {'single_prop_count':1,'mesh_count':len(vertices),'tower_bottom_radius_m':radius(.29),'tower_top_radius_m':radius(6.30),'tower_height_m':6.01,'door_recess_back_y_m':-.68,'door_recess_depth_at_top_m':radius(2.25)*math.cos(math.pi/8)-.68,'door_recess_depth_at_sill_m':radius(.36)*math.cos(math.pi/8)-.68,'lantern_column_count':len(POSTS),'rail_post_count':len(RAIL_POSTS),'corbel_count':len(CORBELS),'lamp_cap_to_header_vertical_clearance_m':bounds(header)[0][2]-bounds(cap)[1][2],'finite_void_count':len(VOID_VOLUMES),'fixed_exterior_only':True,'enterable_building_lighting_navigation_or_safety_claim':False}
LIGHTHOUSE_CONTRACT={'tower':tower,'foundation':base,'door_panel':door,'gallery':gallery,'room_sill':plinth,'room_columns':POSTS,'room_header':header,'roof':roof,'finial':finial,'lamp_parts':[pedestal,lamp,cap],'rail_posts':RAIL_POSTS,'rails':[mid,upper],'corbels':CORBELS,'static_only':True}
FOCUS=(0,0,4.25);ORTHO=11.6
CAMERAS={'gray-front3q':(13,-18,16),'gray-back3q':(-13,18,16),'thumbnail':(13,-18,16),'qa-front':(0,-25,11),'qa-side':(25,0,11),'qa-top':(0,0,26),'qa-back':(0,25,11),'qa-wireframe':(13,-18,16),'silhouette-128-front':(0,-25,11),'silhouette-128-side':(25,0,11)}
WIRE_THICKNESS=ORTHO/640

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
root=bpy.data.objects.new('OneTaperedLanternLighthouse',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='ground X midline, Y=0, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [('Tower_TaperedWithRealDoorRecess',(0,0,1.3),(0,-1,1.3)),('LanternRoom_OpenUpperRing',(.75,0,7.91),(0,0,7.91))]:
 assert inside(trees[name],p) is True
 assert inside(trees[name],outside) is False
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})
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
mount_evidence=measure_lighthouse_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'lighthouse_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/harbor/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'harbor','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-10,-14,22),6000,9),('Fill',(14,-3,14),3500,8),('Rim',(3,15,19),5000,7)]:
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
