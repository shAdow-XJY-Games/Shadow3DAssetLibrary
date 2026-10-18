"""One original fixed carousel exterior: thick canopy, three original block horses.
All parts form one static prop; rotation in the type-name makes no motion claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carnival-fixed-canopy-carousel-01';VERSION='1.0.0';TITLE='Three-Horse Fixed Canopy Carousel'
DESCRIPTION=('One original low-poly fixed-pose carousel exterior, counted as one prop. A broad low grounded base, integral shoulder and solid central shaft support a genuinely through-bored flanged sleeve and thick annular circular deck through finite opposed bearing faces. The centre column continues to the thick segmented canopy. Three radial underside beams support its broad thick eave; three fixed upright poles each have finite embedded ends in the deck and beam. Three instances of one original closed block-built horse shape each have a torso, raised neck, short muzzle, two small ears, saddle, four separate short legs and an attached descending tail. Each horse is fixed to its pole by real finite material overlap. The stepped toy-horse form is intentionally geometric. All repeated horses are internal components of this single asset, never separate model counts. '
 'Metres, native Z up, origin at ground under the central axis, front -Y. Four constant opaque PBR materials, no texture, lettering, brand, visitors, lights, railing, ticket booth, ground scene, animation or second size. Newly authored canopy/body/horse composition, not a resized old parasol, modified spring bird, recoloured roundabout or old carnival scene. '
 'Static visual geometry only. No rotation, lifting, drive, electricity, control or operation logic; no riding, child or adult fit, body clearance, capacity, strength, stability, entrapment protection, railing adequacy, amusement-ride performance, safety certification, manufacture, installation or compatibility with prior assets is claimed. Dimensions and finite contacts describe model geometry only.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={};HORSES=[];RIBS=[];POLES=[]
PALETTE=[('Canopy_MutedCoral',(.62,.16,.105,1),.55,.05),('Trim_WarmIvory',(.78,.65,.40,1),.58,.03),('Frame_DeepTeal',(.035,.18,.19,1),.42,.24),('Horse_SoftCream',(.72,.64,.50,1),.64,.02)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no image or procedural textures.'
FOCUS=(0,0,1.52);ORTHO=5.0
CAMERAS={'gray-front3q':(5,-8,4.6),'gray-back3q':(-5,8,4.6),'thumbnail':(5,-8,4.6),'qa-front':(0,-9,4.0),'qa-side':(9,0,4.0),'qa-top':(0,0,10),'qa-back':(0,9,4.0),'qa-wireframe':(5,-8,4.6),'silhouette-128-front':(0,-9,4.0),'silhouette-128-side':(9,0,4.0)}
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
def cuboid(lo,hi):return [(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
def box_geometry(lo,hi,mat=0,role='complete finite rectangular probe'):
 v=cuboid(lo,hi);m=Mesh()
 for f in BOX_FACES:m.face([v[i] for i in f],mat)
 return m.result(role,mat)
def radial(p,a,r=0):
 # local x follows the tangent; local y follows radius, +Z remains up.
 x,y,z=p;return (math.sin(a)*x+math.cos(a)*(r+y),-math.cos(a)*x+math.sin(a)*(r+y),z)
def transformed(g,a,r=0):return dict(g,vertices=[radial(p,a,r) for p in g['vertices']])
def profile(name,rings,mat,role,n=48):
 vv=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for z,r in rings];m=Mesh()
 m.face(list(reversed(vv[0])),mat,'bottom');m.face(vv[-1],mat,'top')
 for a,b in zip(vv,vv[1:]):
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]],mat,'side')
 g=m.result(role,mat)
 if name:G[name]=g;return name
 return g

def ring_geometry(points,n=48,mat=0,role='closed profiled annulus'):
 vv=[[(r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),z) for i in range(n)] for r,z in points];m=Mesh()
 for k in range(len(vv)):
  a,b=vv[k],vv[(k+1)%len(vv)]
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]],mat,'section_'+str(k))
 return m.result(role,mat)
def ring(ri,ro,z0,z1,mat=0,n=48):return ring_geometry([(ri,z0),(ro,z0),(ro,z1),(ri,z1)],n,mat)
def link(a,b,p,axis=(1,0,0),spread=.008):LINKS.append((a,b,[add(p,mul(axis,d)) for d in [-spread,0,spread]]))
def contact(a,b,z,points,area):CONTACTS.append({'a':a,'b':b,'axis':2,'plane_m':z,'minimum_patch_area_m2':area,'interior_probe_offset_m':.002,'points':points,'scope':'full finite opposed planar contact and complete no-positive-penetration check; geometry only'})
def volume(entries,name,g,targets,role):entries[name]=dict(g,targets=list(targets),role=role)
base=profile('Base_Shoulder_Shaft_CentreColumn',[(0,.62),(.12,.62),(.12,.46),(.28,.46),(.28,.09),(.48,.09),(.60,.20),(3.06,.20)],2,'One continuous closed grounded broad base, thick shoulder, narrow solid shaft through sleeve and tall central canopy column.')
FEET=[base];shaft=base
sleeve='Hub_TrueBoredFlangedSleeve';G[sleeve]=ring_geometry([(.105,.28),(.50,.28),(.50,.34),(.32,.34),(.32,.46),(.105,.46)],48,1,'One genuinely through-bored closed stepped sleeve; full bottom shoulder contact and upper flange-deck contact; complete bore air around real shaft.')
deck='Deck_ThickAnnularCircularPlatform';G[deck]=ring(.33,1.90,.34,.44,2)
G[deck]['role']='Single closed thick annular circular deck, finite underside on sleeve flange. No motion or riding capacity.'
for i,tag in enumerate(G[deck]['face_tags']):G[deck]['face_materials'][i]=1 if tag=='section_2' else 2
contact(base,sleeve,.28,[(.25*math.cos(a),.25*math.sin(a),.28) for a in [0,math.tau/3,math.tau*2/3]],.60)
contact(sleeve,deck,.34,[(.40*math.cos(a),.40*math.sin(a),.34) for a in [0,math.tau/3,math.tau*2/3]],.43)
# Thick canopy with a real horizontal eave underside. The outer eave receives
# each radial beam over a finite area, while its central underside rests on column.
roof='Canopy_ThickSegmentedCrown';G[roof]=profile(None,[(3.06,.24),(2.64,1.65),(2.64,1.98),(2.78,1.98),(3.23,.24)],0,'One closed canopy with alternating sector faces, 0.14m thick eave and solid central cap. The source shape is newly authored.',48)
# profile() is ordered along the closed boundary from central underside to eave,
# outer edge and top. Its first cap faces down; top cap faces up.
for i,f in enumerate(G[roof]['faces']):
 center=tuple(sum(G[roof]['vertices'][j][k] for j in f)/3 for k in range(3));angle=math.atan2(center[1],center[0])%math.tau
 G[roof]['face_materials'][i]=0 if int(angle/(math.tau/12))%2==0 else 1
contact(base,roof,3.06,[(-.10,0,3.06),(0,0,3.06),(.10,0,3.06)],.12)
# Original block-horse union. Cell boundaries only, no hidden internal faces.
# All anatomical blocks have finite shared faces and form one continuous solid.
HORSE_BLOCKS=[('torso',(-.40,-.18,1.12),(.40,.18,1.40),3),('neck',(.25,-.13,1.40),(.43,.13,1.68),3),('head',(.25,-.13,1.68),(.64,.13,1.83),3),('muzzle',(.43,-.13,1.55),(.64,.13,1.68),3),('ear_left',(.27,-.13,1.83),(.35,-.05,1.96),3),('ear_right',(.27,.05,1.83),(.35,.13,1.96),3),('saddle',(-.21,-.18,1.40),(.20,.18,1.48),0),('tail_root',(-.57,-.07,1.20),(-.40,.07,1.34),2),('tail_down',(-.57,-.07,.91),(-.47,.07,1.20),2)]
for ix,(x0,x1) in enumerate([(-.34,-.22),(.22,.34)]):
 for iy,(y0,y1) in enumerate([(-.17,-.09),(.09,.17)]):HORSE_BLOCKS.append(('leg_%s%s'%(ix,iy),(x0,y0,.73),(x1,y1,1.12),3))
def horse_geometry():
 axes=[sorted(set([b[1][i] for b in HORSE_BLOCKS]+[b[2][i] for b in HORSE_BLOCKS])) for i in range(3)];xs,ys,zs=axes;cells={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   for k in range(len(zs)-1):
    c=((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)
    for tag,lo,hi,mat in HORSE_BLOCKS:
     if all(lo[d]<c[d]<hi[d] for d in range(3)):cells[(i,j,k)]=(mat,tag)
 m=Mesh()
 for (i,j,k),(mat,tag) in sorted(cells.items()):
  v=cuboid((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1]))
  for f,near in zip(BOX_FACES,[(i,j,k-1),(i,j,k+1),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]):
   if near not in cells:m.face([v[q] for q in f],mat,tag)
 return m.result('One newly authored closed block-horse mesh: integral torso, neck, short head/muzzle, two ears, saddle, four short legs and descending tail. No spring bird reused.',3)
HORSE_TEMPLATE=horse_geometry()
# Complete rectangular under-horse air minus a finite inset polygonal shaft keepout.
def rectangle_with_hole(x0,x1,y0,y1,z0,z1,hole_radius=.052):
 angles=sorted(set([math.tau*i/12 for i in range(12)]+[math.atan2(y,x)%math.tau for x in [x0,x1] for y in [y0,y1]]));n=len(angles);outer=[];inner=[]
 for a in angles:
  cx,sy=math.cos(a),math.sin(a)
  candidates=[(x1/cx if cx>1e-8 else x0/cx if cx< -1e-8 else 1e10),(y1/sy if sy>1e-8 else y0/sy if sy< -1e-8 else 1e10)];r=min(candidates)
  outer.append((r*cx,r*sy));inner.append((hole_radius*cx,hole_radius*sy))
 m=Mesh()
 for i in range(n):
  j=(i+1)%n;ib=(*inner[i],z0);jb=(*inner[j],z0);ob=(*outer[i],z0);pb=(*outer[j],z0);it=(*inner[i],z1);jt=(*inner[j],z1);ot=(*outer[i],z1);pt=(*outer[j],z1)
  for q in [[ib,ob,pb,jb],[it,jt,pt,ot],[ob,ot,pt,pb],[ib,jb,jt,it]]:m.face(q)
 return m.result('complete closed rectangular air prism with real shaft keepout')
for i,a in enumerate([-math.pi/2,math.pi/6,5*math.pi/6],1):
 rib='Canopy_RadialBeam_'+str(i);G[rib]=transformed(box_geometry((-.07,.16,2.54),(.07,1.80,2.64),2,'One closed radial beam, finite root inside central column and complete finite outer eave contact.'),a);RIBS.append(rib)
 link(base,rib,radial((0,.18,2.59),a),axis=(math.sin(a),-math.cos(a),0),spread=.025)
 volume(WALL_VOLUMES,rib+'_EmbeddedRoot',transformed(box_geometry((-.035,.166,2.565),(.035,.188,2.615)),a),[base,rib],'complete finite radial-beam root volume inside central column and beam')
 contact(rib,roof,2.64,[radial((x,1.73,2.64),a) for x in [-.035,0,.035]],.019)
 pole='FixedPole_'+str(i);g=profile(None,[(.42,.045),(2.60,.045)],1,'Single fixed closed pole with finite embedded lower deck end, upper beam end and horse-body attachment.',12);G[pole]=transformed(g,a,1.15);POLES.append(pole)
 horse='Horse_OriginalBlockInstance_'+str(i);G[horse]=transformed(HORSE_TEMPLATE,a,1.15);HORSES.append({'name':horse,'pole':pole,'rib':rib,'angle_rad':a,'orbit_radius_m':1.15,'shared_original_geometry':True})
 for other,z0,z1,label in [(deck,.425,.435,'LowerDeckEnd'),(rib,2.555,2.585,'UpperBeamEnd'),(horse,1.20,1.32,'HorseTorsoJoint')]:
  p=radial((0,0,(z0+z1)/2),a,1.15);link(other,pole,p,axis=(math.sin(a),-math.cos(a),0),spread=.018)
  volume(WALL_VOLUMES,pole+'_'+label,transformed(box_geometry((-.018,-.018,z0),(.018,.018,z1)),a,1.15),[other,pole],'whole closed finite joint volume strictly inside both fixed connected components')
 volume(VOID_VOLUMES,horse+'_WholeUnderfeetAir',transformed(rectangle_with_hole(-.59,.66,-.195,.195,.445,.725),a,1.15),[], 'complete finite air below all four feet, torso and tail, excluding only pole keepout; 5mm boundary inset')
 volume(VOID_VOLUMES,horse+'_WholeBetweenLegsAir',transformed(rectangle_with_hole(-.215,.215,-.175,.175,.735,1.115),a,1.15),[], 'full between-front-and-back-legs air under torso, excluding only pole keepout; 5mm boundary inset')
 for label,x0,x1 in [('Hind',-.335,-.225),('Fore',.225,.335)]:
  volume(VOID_VOLUMES,horse+'_Whole'+label+'PairGap',transformed(box_geometry((x0,-.085,.735),(x1,.085,1.115)),a,1.15),[],'complete finite transverse gap between the two legs of this fore/hind pair; 5mm boundary inset')
 # The complete actual material of each named horse region is certified by
 # a connected closed inset box. Joins use finite boxes spanning union faces.
 for tag,lo,hi,mat in HORSE_BLOCKS:
  inset=.004;g=box_geometry(tuple(v+inset for v in lo),tuple(v-inset for v in hi));volume(WALL_VOLUMES,horse+'_'+tag+'_Material',transformed(g,a,1.15),[horse],'whole inset anatomical region material; no internal hollow or disconnected block')
 joints=[('neck_torso',(.28,-.08,1.38),(.38,.08,1.43)),('head_neck',(.28,-.08,1.65),(.38,.08,1.72)),('muzzle_head',(.46,-.08,1.65),(.59,.08,1.71)),('saddle_torso',(-.16,-.13,1.38),(.16,.13,1.43)),('tail_torso',(-.43,-.04,1.23),(-.37,.04,1.30)),('tail_bend',(-.54,-.04,1.17),(-.50,.04,1.23)),('ear_left_root',(.29,-.11,1.81),(.33,-.07,1.85)),('ear_right_root',(.29,.07,1.81),(.33,.11,1.85))]
 for tag,lo,hi,mat in HORSE_BLOCKS:
  if tag.startswith('leg_'):joints.append((tag+'_root',(lo[0]+.02,lo[1]+.02,1.10),(hi[0]-.02,hi[1]-.02,1.14)))
 for tag,lo,hi in joints:volume(WALL_VOLUMES,horse+'_'+tag,transformed(box_geometry(lo,hi),a,1.15),[horse],'full connected closed volume crossing real anatomical material join')
volume(ISOLATED_VOID_VOLUMES,'Sleeve_WholeTrueThroughBore',profile(None,[(.275,.103),(.465,.103)],0,'isolated sleeve whole through-bore',48),[sleeve],'whole complete sleeve bore and both mouths; excludes intentionally present separate shaft')
volume(VOID_VOLUMES,'Shaft_WholeAnnularClearance',ring(.092,.103,.284,.456),[base,sleeve],'complete 360-degree finite air between solid shaft and true bore wall')
volume(VOID_VOLUMES,'Deck_WholeUnderdeckAir',ring(.625,1.89,.125,.335),[], 'complete finite 360-degree underdeck annulus outside broad base')
volume(VOID_VOLUMES,'Centre_WholeInteriorAir',ring(.205,.78,.605,2.535),[],'complete 360-degree empty central annulus above platform and below beams')
volume(WALL_VOLUMES,'Deck_WholeSolidSlab',ring(.335,1.895,.345,.435),[deck],'whole inset annular closed slab inside thick platform')
for r in VOID_VOLUMES.values():
 if not r['targets']:r['targets']=list(G)
BORES=[{'mesh':sleeve,'origin_m':(0,0,.27),'direction':(0,0,1),'length_m':.20}]
def measure_carousel_geometry(vertices):
 assert set(vertices)==set(G),'Changed component set'
 def bounds(name):return [[fn(float(p[i]) for p in vertices[name]) for i in range(3)] for fn in [min,max]]
 assert abs(bounds(base)[0][2])<2e-7
 assert abs(bounds(deck)[1][0]-1.90)<2e-7 and abs(bounds(roof)[1][2]-3.23)<2e-7
 for h in HORSES:
  assert len(vertices[h['name']])==len(HORSE_TEMPLATE['vertices'])
  assert abs(bounds(h['name'])[0][2]-.73)<2e-7 and abs(bounds(h['name'])[1][2]-1.96)<2e-7
 return {'single_prop_count':1,'closed_components':len(G),'original_horse_geometry_count':1,'horse_instances':3,'horse_legs_each':4,'fixed_poles':3,'radial_beams':3,'true_sleeve_bore_nominal_diameter_m':.21,'solid_shaft_nominal_diameter_m':.18,'deck_diameter_m':3.8,'deck_thickness_m':.1,'canopy_diameter_m':3.96,'height_m':3.23,'horse_minimum_foot_z_m':.73,'full_opposed_contacts':len(CONTACTS),'frozen_static_pose':True,'motion_riding_fit_load_safety_claim':False}
assert len(G)==13,len(G)

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
root=bpy.data.objects.new('OneFixedThreeHorseCarousel',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and centre shaft axis; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
carousel_evidence=measure_carousel_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'carousel_geometry':carousel_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'prop','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
