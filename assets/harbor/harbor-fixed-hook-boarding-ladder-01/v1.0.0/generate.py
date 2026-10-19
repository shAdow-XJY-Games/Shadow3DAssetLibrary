"""Original fixed twin-return-hook boarding ladder. One static visual prop."""
import math,json,hashlib,sys,time,collections,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='harbor-fixed-hook-boarding-ladder-01';VERSION='1.0.0';TITLE='Twin Return-Hook Boarding Ladder'
DESCRIPTION=('One original static visual prop: two whole closed continuous angled side rails with integral polygonal return hooks, four independent 50 mm thick horizontal treads and two complete flat ground pads. Three opaque unlinked constant Principled PBR materials. Metres, native Z up, front -Y, origin at the midpoint of the two ground pads. The one QA-only placement translates this ladder by (0,-1.47,0) metres beside the unchanged pinned harbor-dock-module-01. Two complete 80 by 80 mm hook terminal underside faces rest at Z=0.75 on two whole original deck planks at X=-0.30 and +0.30. Every original 12 mm bevel, plank gap, stringer, piling and collar remains. The old dock is not exported or included in this prop. Newly dimensioned geometry, not a reduced A-frame, detached slide ladder or copied high-seat ladder. No boat, generic vessel or dock compatibility, traversability, climbing, folding, swinging, load, human suitability, anti-slip, construction, rescue, maritime or safety claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};ISOLATED_VOID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];RAILS=[];TREADS=[];OLD_CONTACTS=[]
PALETTE=[('MarineTealRails',(.075,.235,.245,1),.62,.14),('HoneyTimberTreads',(.58,.335,.135,1),.78,0),('GraphiteGroundPads',(.065,.078,.080,1),.79,0)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(vs,fs,material=0,role=''):
 vv=[tuple(round(float(c),9) for c in v) for v in vs];volume=sum(dot(vv[f[0]],cross(vv[f[i]],vv[f[i+1]])) for f in fs for i in range(1,len(f)-1))/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return {'vertices':vv,'faces':[tuple(f) for f in fs],'material':material,'role':role}
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def box(lo,hi,material=0,role='',transform=None):
 vv=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 return mesh([transform(p) for p in vv] if transform else vv,BOX_FACES,material,role)
def prism(poly,z0,z1,material=0,role='',transform=None):
 n=len(poly);vv=[(x,y,z) for z in [z0,z1] for x,y in poly];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh([transform(p) for p in vv] if transform else vv,ff,material,role)
def grid(xs,ys,zs,occupied,material=0,role=''):
 cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)};vv=[];ff=[];ids={}
 def vertex(p):
  p=tuple(round(x,9) for x in p)
  if p not in ids:ids[p]=len(vv);vv.append(p)
  return ids[p]
 for i,j,k in sorted(cells):
  cell=[(x,y,z) for z in zs[k:k+2] for y in ys[j:j+2] for x in xs[i:i+2]]
  for delta,face in zip([(0,0,-1),(0,0,1),(0,-1,0),(0,1,0),(-1,0,0),(1,0,0)],BOX_FACES):
   if (i+delta[0],j+delta[1],k+delta[2]) not in cells:ff.append(tuple(vertex(cell[n]) for n in face))
 return mesh(vv,ff,material,role)
def union_boxes(boxes,material=0,role=''):
 stations=[sorted(set(p[k] for lo,hi in boxes for p in [lo,hi])) for k in range(3)]
 return grid(*stations,lambda x,y,z:any(all(lo[k]<p<hi[k] for k,p in enumerate([x,y,z])) for lo,hi in boxes),material,role)
def contact(name,a,b,axis,p,area,points=None,offset=.0004):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'points':points or [p],'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role,targets=None):VOID_VOLUMES[name]=dict(g,targets=targets,role=role)
def solid(name,g,targets,role):SOLID_VOLUMES[name]=dict(g,targets=targets,role=role)
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.fm=[];self.tags=[];self.index={}
 def vertex(self,p):
  p=tuple(round(float(x),9) for x in p)
  if p not in self.index:self.index[p]=len(self.v);self.v.append(p)
  return self.index[p]
 def face(self,points,mat=0,tag=''):
  ids=[self.vertex(p) for p in points]
  if len(ids)==3:self.f.append(tuple(ids));self.fm.append(mat);self.tags.append(tag);return
  c=self.vertex(tuple(sum(p[k] for p in points)/len(points) for k in range(3)))
  for a,b in zip(ids,ids[1:]+ids[:1]):
   if a==b:continue
   self.f.append((a,b,c));self.fm.append(mat);self.tags.append(tag)
 def result(self,role,mat=0):
  edges={}
  for i,f in enumerate(self.f):
   for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((i,a,b))
  signs={0:1};todo=[0]
  while todo:
   i=todo.pop()
   for a,b in zip(self.f[i],self.f[i][1:]+self.f[i][:1]):
    for j,c,d in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     want=signs[i]*(-1 if (a,b)==(c,d) else 1)
     if j in signs:assert signs[j]==want,'nonorientable surface'
     else:signs[j]=want;todo.append(j)
  assert len(signs)==len(self.f),'disconnected surface'
  self.f=[f if signs[i]>0 else tuple(reversed(f)) for i,f in enumerate(self.f)]
  volume=sum(dot(self.v[f[0]],cross(self.v[f[1]],self.v[f[2]])) for f in self.f)/6
  if volume<0:self.f=[tuple(reversed(f)) for f in self.f]
  return {'vertices':self.v,'faces':self.f,'face_materials':self.fm,'face_tags':self.tags,'material':mat,'role':role}
def rect(y0,y1,z0,z1):return [(y0,z0),(y1,z0),(y1,z1),(y0,z1)]
def chamfer(y0,y1,z0,z1,c):return [(y0+c,z0),(y1-c,z0),(y1,z0+c),(y1,z1-c),(y1-c,z1),(y0+c,z1),(y0,z1-c),(y0,z0+c)]
def inside2(p,poly):
 y,z=p;inside=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>z)!=(b[1]>z) and y<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def extrude_region(outer,holes,x0,x1,mat=0,role='closed finite prism'):
 # Exact horizontal decomposition of the polygon-with-holes. Every slab end
 # shares all boundary breakpoints; no T-junctions and no booleans or fake caps.
 outer=[tuple(round(c,9) for c in p) for p in outer];holes=[[tuple(round(c,9) for c in p) for p in h] for h in holes]
 loops=[outer]+holes;levels=sorted(set(round(p[1],9) for loop in loops for p in loop));m=Mesh()
 segs=[(a,b,k) for k,loop in enumerate(loops) for a,b in zip(loop,loop[1:]+loop[:1])]
 def hit(a,b,z):return a[0]+(b[0]-a[0])*(z-a[1])/(b[1]-a[1])
 cuts={}
 for z in levels:
  yy=[]
  for a,b,k in segs:
   if min(a[1],b[1])-1e-8<=z<=max(a[1],b[1])+1e-8:
    yy.extend([a[0],b[0]] if abs(a[1]-b[1])<1e-8 else [hit(a,b,z)])
  cuts[z]=sorted(set(round(y,9) for y in yy))
 for z0,z1 in zip(levels,levels[1:]):
  z=(z0+z1)/2;active=sorted([(hit(a,b,z),a,b) for a,b,k in segs if min(a[1],b[1])<z<max(a[1],b[1])],key=lambda r:r[0])
  for left,right in zip(active,active[1:]):
   p=((left[0]+right[0])/2,z)
   if not inside2(p,outer) or any(inside2(p,h) for h in holes):continue
   l0,l1=hit(left[1],left[2],z0),hit(left[1],left[2],z1);r0,r1=hit(right[1],right[2],z0),hit(right[1],right[2],z1)
   low=[(y,z0) for y in cuts[z0] if l0+1e-8<y<r0-1e-8];high=[(y,z1) for y in reversed(cuts[z1]) if l1+1e-8<y<r1-1e-8]
   poly=[(l0,z0)]+low+[(r0,z0),(r1,z1)]+high+[(l1,z1)];clean=[]
   for p in poly:
    if not clean or math.dist(clean[-1],p)>1e-8:clean.append(p)
   if math.dist(clean[0],clean[-1])<1e-8:clean.pop()
   for x in [x0,x1]:m.face([(x,*p) for p in clean],mat,'side_face')
 for a,b,k in segs:
  if abs(a[1]-b[1])<1e-8:
   z=round(a[1],9);ys=[a[0]]+[y for y in cuts[z] if min(a[0],b[0])+1e-8<y<max(a[0],b[0])-1e-8]+[b[0]];ys=sorted(ys);pp=[(y,z) for y in ys]
  else:
   zs=sorted([a[1]]+[z for z in levels if min(a[1],b[1])+1e-8<z<max(a[1],b[1])-1e-8]+[b[1]]);pp=[(hit(a,b,z),z) for z in zs]
  for p,q in zip(pp,pp[1:]):m.face([(x0,*p),(x1,*p),(x1,*q),(x0,*q)],mat,'outer_wall' if k==0 else 'hole_wall_'+str(k))
 return m.result(role,mat)
def box_geometry(lo,hi,mat=0,role='complete finite rectangular prism'):
 return extrude_region(rect(lo[1],hi[1],lo[2],hi[2]),[],lo[0],hi[0],mat,role)
def yz_prism(poly,x0,x1,mat=0,role=''):
 return prism(poly,x0,x1,mat,role,lambda p:(p[2],p[0],p[1]))
def xy_region(outer,holes,z0,z1,mat=0,role=''):
 g=extrude_region(outer,holes,z0,z1,mat,role)
 g['vertices']=[(y,z,x) for x,y,z in g['vertices']]
 return g

def offset_convex(poly,amount):
 # CCW polygon offset inward by an exact distance from every finite side.
 rows=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);n=(-dy/length,dx/length);rows.append((n,n[0]*a[0]+n[1]*a[1]+amount))
 out=[]
 for (a,da),(b,db) in zip(rows[-1:]+rows[:-1],rows):
  det=a[0]*b[1]-a[1]*b[0];out.append(((da*b[1]-a[1]*db)/det,(a[0]*db-da*b[0])/det))
 return out

# All numerical geometry below is new. Only generic mesh/predicate/output
# scaffolding is reused. No pinned original is an input to this generator.
DATUM_Y=1.47
QA_NEW_TRANSFORM={'translation_m':[0,-1.47,0],'rotation_z_degrees':0,'scale':[1,1,1]}
QA_OLD_TRANSFORM={'translation_m':[0,0,0],'rotation_z_degrees':0,'scale':[1,1,1]}
def local_poly(poly):return [(y+DATUM_Y,z) for y,z in poly]
def area2(poly):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2
def inset(poly,e):
 poly=poly if area2(poly)>0 else poly[::-1]
 return offset_convex(poly,e)
def shape(poly,x0,x1,mat=0,role=''):
 return extrude_region(local_poly(poly),[],x0,x1,mat,role)
def whole_material(name,g,role):solid(name,g,[name.replace('_CompleteMaterial','')],role)
def outer_y(z):return -1.54+.5*(z-.05)
def inner_y(z):return -1.40+.5*(z-.05)
RAIL_PROFILE=[(-1.54,.05),(-1.14,.85),(-1.14,1.02),(-1.10,1.10),(-.90,1.10),(-.86,1.06),(-.86,.75),(-.94,.75),(-.94,1.00),(-.96,1.02),(-.98,1.02),(-1.00,1.00),(-1.00,.85),(-1.40,.05)]
HOOK_AIR_PROFILE=[(inner_y(.75),.75),(-.94,.75),(-.94,1.00),(-.96,1.02),(-.98,1.02),(-1.00,1.00),(-1.00,.85)]
for side,x in [('Left',-.30),('Right',.30)]:
 rail='ContinuousReturnHookRail_'+side;foot='FlatGroundPad_'+side;RAILS.append(rail);FEET.append(foot)
 G[rail]=shape(RAIL_PROFILE,x-.04,x+.04,0,'One whole unbroken closed side rail from its finite lower cut to the complete integral return hook and full terminal underside; no stacked segments.')
 solid(rail+'_CompleteMaterial',shape(inset(RAIL_PROFILE,.001),x-.039,x+.039),[rail],'Entire connected inward-offset rail including the full lower stem, both bend corners, top bridge and complete return terminal.')
 G[foot]=box((x-.07,-.13,0),(x+.07,.13,.05),2,'Whole flat 140 by 260 mm ground pad, full 50 mm thickness, complete rail seat and ground sole.')
 solid(foot+'_CompleteMaterial',box((x-.069,-.129,.001),(x+.069,.129,.049)),[foot],'Entire finite pad material through all corners, sole, top and full thickness, 1 mm inset.')
 contact(foot+'_WholeRailSeat',foot,rail,(0,0,1),(x,0,.05),.0112-1e-7)
 FOOT_CONTACTS.append({'name':foot+'_WholeGroundSole','mesh':foot,'x':x,'y':0,'half_x':.07,'half_y':.13,'minimum_area_m2':.0364-1e-7})
 OLD_CONTACTS.append({'name':rail+'_WholeOriginalDeckSeat','a':'Deck plank 03' if side=='Left' else 'Deck plank 06','b':rail,'origin_m':[0,0,0],'u':[1,0,0],'v':[0,1,0],'axis':[0,0,1],'plane_m':.75,'points':[(x,-.90,.75)],'minimum_patch_area_m2':.0064-1e-7,'interior_probe_offset_m':.0005,'expected_rectangle_world_m':[[x-.04,-.94,.75],[x+.04,-.86,.75]]})
 # Complete hook aperture through and beyond both rail side skins. The datum
 # cut at Z=.75 is open air above a separate QA-only old deck, not a fake cap.
 air('WholeHookInnerAir_'+side,shape(inset(HOOK_AIR_PROFILE,.001),x-.041,x+.041),'Entire finite return-hook inner aperture with both mouth sides, both inner bevels, back face and bridge underside; 1 mm physical margins.')
 back=[(-1.599,.051),(outer_y(.051)-.0012,.051),(-1.1412,.8503),(-1.1412,1.0203),(-1.102,1.099),(-1.599,1.099)]
 air('WholeOutsideBackRailAir_'+side,shape(back,x-.039,x+.039),'Whole rear strip alongside the full sloped stem, outer upper shoulder and rounded polygonal return; no hidden back rib.')
 front=[(inner_y(.051)+.0012,.051),(-.859,.051),(-.859,.749),(inner_y(.749)+.0012,.749)]
 air('WholeBelowHookFrontAir_'+side,shape(front,x-.039,x+.039),'Whole front free region from pad top to just below the terminal underside, including the entire sloped inner stem face. Fixed old geometry is not part of this asset air test.')
TREAD_PROFILES=[]
for i,z0 in enumerate([.17,.34,.51,.68],1):
 z1=z0+.05;name='WholeThickHorizontalTread_%02d'%i;TREADS.append(name)
 poly=[(outer_y(z0)+.01,z0),(inner_y(z0)-.01,z0),(inner_y(z1)-.01,z1),(outer_y(z1)+.01,z1)];TREAD_PROFILES.append(poly)
 G[name]=shape(poly,-.26,.26,1,'One full 520 mm span, 120 mm deep, 50 mm thick horizontal-topped tread with finite whole trapezoid end faces exactly meeting both rail inner skins.')
 solid(name+'_CompleteMaterial',shape(inset(poly,.001),-.259,.259),[name],'Whole thick tread including both full ends and every top, bottom and sloped front/back facet; 1 mm inset.')
 y=(outer_y(z0+.025)+inner_y(z0+.025))/2+DATUM_Y;z=z0+.025
 contact(name+'_WholeLeftEnd',RAILS[0],name,(1,0,0),(-.26,y,z),.006-1e-7)
 contact(name+'_WholeRightEnd',name,RAILS[1],(1,0,0),(.26,y,z),.006-1e-7)
outer=local_poly([(-1.599,.051),(-.859,.051),(-.859,1.099),(-1.599,1.099)])
holes=[local_poly(inset(p,-.001)) for p in TREAD_PROFILES]
air('WholeInterTreadAndUpperAir',extrude_region(outer,holes,-.259,.259),'Complete connected middle volume around all four entire thick treads, all inter-tread spaces, below the first tread, above the last tread and through the complete twin-hook opening; only 1 mm physical skin offsets.')
for row in VOID_VOLUMES.values():
 if row['targets'] is None:row['targets']=list(G)
BODY=RAILS[0]
CONTRACT={'single_prop_count':1,'whole_continuous_return_hook_rails':2,'whole_thick_treads':4,'flat_ground_pads':2,'tread_thickness_m':.05,'tread_depth_m':.12,'rail_width_m':.08,'rail_centres_x_m':[-.30,.30],'complete_hook_bearing_area_each_m2':.0064,'fixed_old_deck_top_world_z_m':.75,'hook_terminal_y_world_m':[-.94,-.86],'finite_opposed_internal_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'whole_material_volumes':len(SOLID_VOLUMES),'qa_new_transform':QA_NEW_TRANSFORM,'qa_old_transform':QA_OLD_TRANSFORM,'exported_old_or_boat_count':0,'climbing_or_load_or_safety_claim':False}
def measure_boarding_ladder_geometry(vertices):
 assert set(vertices)==set(G)
 for rail in RAILS:
  vv=vertices[rail];assert abs(min(p[2] for p in vv)-.05)<2e-7 and abs(max(p[2] for p in vv)-1.10)<2e-7
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 return dict(CONTRACT,geometry_scope='one original static ladder; full actual triangles, complete air/material bodies, full finite surfaces and fixed-old interfaces require separate independent acceptance')
INSIDE_TESTS=[(RAILS[0],(-.30,.37,1.05),(-.30,.495,.90)),(TREADS[0],(0,.0725,.195),(0,.0725,.26))]
FOCUS=(0,.24,.55);ORTHO=1.65
CAMERAS={'gray-front3q':(2.2,-3.0,2.0),'gray-back3q':(-2.2,3.1,2.0),'thumbnail':(2.2,-3.0,2.0),'qa-front':(0,-4,1.4),'qa-side':(4,.24,1.4),'qa-top':(0,.24,5),'qa-back':(0,4,1.4),'qa-wireframe':(2.2,-3.0,2.0),'silhouette-128-front':(0,-4,1.4),'silhouette-128-side':(4,.24,1.4)}
WIRE_THICKNESS=ORTHO/1500
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
root=bpy.data.objects.new('OneTwinHookBoardingLadder',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='midpoint of both pad ground soles; QA translation (0,-1.47,0)';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in INSIDE_TESTS:
 assert inside(trees[name],p) and not inside(trees[name],outside)
 inside_predicate_selftests.append({'object':name,'inside_solid_witness':True,'void_witness_outside_solid':True})

joints=[]
for a,b,points in LINKS:
 rows=[]
 for point in points:
  p=Vector(point);clearance=min(trees[a].find_nearest(p)[3],trees[b].find_nearest(p)[3]);assert inside(trees[a],p) and inside(trees[b],p) and clearance>.0001,('Invalid joint',a,b,point,clearance)
  rows.append({'world_point_m':list(p),'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# This Blender segment checks closed shells, finite ground faces, contact areas,
# finite sided interior witnesses and export fingerprints. Complete empty bodies
# and whole-surface nonpenetration remain separate independent actual-GLB gates.
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
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
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
mount_evidence=measure_boarding_ladder_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'boarding_ladder_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
for name,pos,power,size in [('Key',(-2,-3,4),260,3),('Fill',(3,-1,2.5),160,2.5),('Rim',(1,3,3),220,2)]:
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
