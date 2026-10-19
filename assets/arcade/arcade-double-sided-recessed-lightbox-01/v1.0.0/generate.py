"""Original complete double-sided recessed lightbox frame and fixed floor supports."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='arcade-double-sided-recessed-lightbox-01';VERSION='1.0.0';TITLE='Double-Sided Recessed Lightbox'
DESCRIPTION=('One original independent double-sided recessed opaque-panel lightbox appearance, counted as one static prop. One continuous thick rectangular frame has a genuine through aperture and two opposing integral inner shoulders. Two independent 18 mm thick opaque blank panels seat on those shoulders with complete finite annular contacts. Both faces are recessed by 57 mm, each panel retains 6 mm edge clearance, and a real complete stepped air chamber separates the panels. Two fixed short columns support the whole frame on two wide ground runners. Seven closed editable meshes and four opaque constant unlinked PBR materials. Metres, native Z up, front -Y and horizontally bounds-centred ground origin. Every shape is newly authored, without importing or copying old cabinet marquees, work lights or softboxes. No textures, text, logos, emission, circuitry, cables, animation or opening mechanism. Fixed unlit static appearance only: no lighting, reflectance/transmission optics, advertising/game functionality, electrical performance, panel replacement, installation, carrying capacity, stability or safety certification claim. Finite geometric support does not establish real-world safe use.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];FOOT_CONTACTS=[];PILLARS=[]
BODY='Continuous_DoubleShoulderThroughFrame';FRONT='Front_ThickOpaqueBlankPanel';BACK='Back_ThickOpaqueBlankPanel'
PALETTE=[('Frame_MutedPlum',(.16,.055,.10,1),.55,.20),('Panels_WarmIvory',(.76,.75,.62,1),.66,.0),('Columns_DullBronze',(.28,.20,.10,1),.49,.50),('Runners_DeepGraphite',(.035,.045,.055,1),.79,.12)]
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
def box(lo,hi,material=0,role=''):return mesh([(x,y,z) for z in[lo[2],hi[2]] for y in[lo[1],hi[1]] for x in[lo[0],hi[0]]],BOX_FACES,material,role)
def rect_y(y,w,z0,z1):return [(-w,y,z0),(w,y,z0),(w,y,z1),(-w,y,z1)]
def loopmesh(loops,closed=False,material=0,role=''):
 vv=[v for loop in loops for v in loop];fs=[]
 for k in range(len(loops)-1):
  for i in range(4):j=(i+1)%4;fs.append((k*4+i,k*4+j,(k+1)*4+j,(k+1)*4+i))
 if closed:
  k=len(loops)-1
  for i in range(4):j=(i+1)%4;fs.append((k*4+i,k*4+j,j,i))
 else:fs += [(3,2,1,0),tuple((len(loops)-1)*4+i for i in range(4))]
 return mesh(vv,fs,material,role)
def framemesh(i=0):
 # One closed genus-one surface: exterior, front annulus, full stepped tunnel,
 # rear annulus. No component, cap, dark face or hidden solid fills the aperture.
 W=.425+i;N=.385+i;z0=.345-i;z1=1.355+i;n0=.385-i;n1=1.315+i
 specs=[(.14-i,.49-i,.28+i,1.42-i),(-.14+i,.49-i,.28+i,1.42-i),(-.14+i,W,z0,z1),(-.065+i,W,z0,z1),(-.065+i,N,n0,n1),(-.045-i,N,n0,n1),(-.045-i,W,z0,z1),(.045+i,W,z0,z1),(.045+i,N,n0,n1),(.065-i,N,n0,n1),(.065-i,W,z0,z1),(.14-i,W,z0,z1)]
 return loopmesh([rect_y(*q) for q in specs],True,0,'One continuous thick genus-one rectangular through frame with two complete opposed integral inner shoulder annuli; no closed back or filled centre.')
def contact(name,a,b,axis,p,area,scope,points=None):
 axis=unit(axis);u=(0,1,0) if abs(axis[0])>.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':dot(axis,p),'minimum_patch_area_m2':area-1e-8,'complete_interface_area_m2':area,'interior_probe_offset_m':.0004,'points':points or[p],'scope':scope})
def solid(name,g,target,role):SOLID_VOLUMES[name]=dict(g,targets=[target],role=role)
def air(name,g,role):VOID_VOLUMES[name]=dict(g,targets=[],role=role)
def member(n,lo,hi,material,role):
 G[n]=box(lo,hi,material,role);solid(n+'WholeInsetMaterial',box(add(lo,(.001,.001,.001)),sub(hi,(.001,.001,.001))),n,'Whole closed member material, complete ends and thickness, with 1 mm inward boundary allowance.')
G[BODY]=framemesh();solid('WholeFrameFourBridgesBothShouldersAndCorners',framemesh(.001),BODY,'Entire continuous frame material, four bridges, all corners, front/rear lips, both integral complete shoulder rings; 1 mm inward offset of every outer and tunnel boundary.')
member(FRONT,(-.419,-.083,.351),(.419,-.065,1.349),1,'Independent 18 mm thick opaque unlit blank front panel; complete shoulder bearing, 57 mm genuine recess and 6 mm side clearance.')
member(BACK,(-.419,.065,.351),(.419,.083,1.349),1,'Independent 18 mm thick opaque unlit blank back panel; complete opposing shoulder bearing, 57 mm genuine recess and 6 mm side clearance.')
SEAT_AREA=.838*.998-.77*.93
for label,panel,sign in [('Front',FRONT,-1),('Back',BACK,1)]:
 contact(label+'WholePanelShoulderAnnulus',BODY,panel,(0,sign,0),(0,sign*.065,.37),SEAT_AREA,'Complete finite rectangular shoulder annulus beneath this panel, all four sides and corners; no interpenetration.',[(x,sign*.065,z) for x,z in[(0,.368),(0,1.332),(-.402,.85),(.402,.85)]])
for label,x in [('Left',-.31),('Right',.31)]:
 foot=label+'_WideGroundRunner';col=label+'_FixedShortColumn';FEET.append(foot);PILLARS.append(col)
 member(foot,(x-.08,-.29,0),(x+.08,.29,.065),3,'One full thick fixed ground runner with a complete 160 by 580 mm planar sole.')
 member(col,(x-.0375,-.05,.065),(x+.0375,.05,.28),2,'One full fixed 75 by 100 mm short rectangular support column joining runner top and frame underside.')
 contact(label+'WholeColumnLowerSeat',foot,col,(0,0,1),(x,0,.065),.075*.10,'Entire finite lower column rectangle supported on runner top.')
 contact(label+'WholeColumnUpperSeat',col,BODY,(0,0,1),(x,0,.28),.075*.10,'Entire finite upper column rectangle supported beneath continuous lower frame bridge.')
 FOOT_CONTACTS.append({'name':foot+'WholeGroundSole','mesh':foot,'x':x,'y':0,'half_x':.08,'half_y':.29,'minimum_area_m2':.16*.58-1e-8,'expected_area_m2':.16*.58})
# Whole finite air volumes, not rays, sparse samples, or black material patches.
air('WholeFrontRecessAndMouth',box((-.424,-.16,.346),(.424,-.084,1.354)),'Entire bounded front recess and its open mouth, full width and height, with 1 mm clearance from front panel and inner frame surfaces.')
air('WholeBackRecessAndMouth',box((-.424,.084,.346),(.424,.16,1.354)),'Entire bounded rear recess and open mouth, full width and height, with 1 mm clearance from back panel and inner frame surfaces.')
chamber=[(-.064,.384,.386,1.314),(-.044,.384,.386,1.314),(-.044,.424,.346,1.354),(.044,.424,.346,1.354),(.044,.384,.386,1.314),(.064,.384,.386,1.314)]
air('WholeSteppedAirChamberBetweenPanels',loopmesh([rect_y(*q) for q in chamber]),'Complete connected stepped middle air body from front panel rear to back panel rear, including full central chamber and both narrower shoulder throats; 1 mm inward allowance.')
for label,y0,y1 in [('Front',-.082,-.066),('Back',.066,.082)]:
 loops=[rect_y(y0,.424,.346,1.354),rect_y(y1,.424,.346,1.354),rect_y(y1,.420,.350,1.350),rect_y(y0,.420,.350,1.350)]
 air(label+'WholeFourSidePanelEdgeClearance',loopmesh(loops,True),'Complete connected rectangular annular air around all four panel edges and corners, across its thickness; 1 mm allowance from panel/frame/seat.')
def slab_with_holes(xs,ys,z0,z1,holes):
 cells={(i,j) for i in range(len(xs)-1) for j in range(len(ys)-1) if not any(a<(xs[i]+xs[i+1])/2<b and c<(ys[j]+ys[j+1])/2<d for a,b,c,d in holes)}
 vs=[];fs=[];lookup={}
 def face(points):
  inds=[]
  for p in points:
   if p not in lookup:lookup[p]=len(vs);vs.append(p)
   inds.append(lookup[p])
  fs.append(tuple(inds))
 for i,j in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2]
  face([(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]);face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
  for step,q in [((-1,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)])]:
   if (i+step[0],j+step[1]) not in cells:face(q)
 return mesh(vs,fs)
holes=[(x-.0385,x+.0385,-.051,.051) for x in[-.31,.31]]
xs=sorted(set([-.489,.489]+[a for h in holes for a in h[:2]]))
air('WholeUnderFrameAirAroundBothColumns',slab_with_holes(xs,[-.139,-.051,.051,.139],.066,.279,holes),'Entire bounded space beneath the complete frame footprint and above both runners, around both full columns with 1 mm clearance.')
air('WholeFloorBayBetweenRunners',box((-.229,-.289,.001),(.229,.289,.064)),'Entire bounded floor-level gap between the two full runners; 1 mm boundary allowance.')
for g in VOID_VOLUMES.values():g['targets']=list(G)
# Independent isolated frame test proves the whole stepped through-hole.
passage=[(-.16,.424,.346,1.354),(-.066,.424,.346,1.354),(-.066,.384,.386,1.314),(-.044,.384,.386,1.314),(-.044,.424,.346,1.354),(.044,.424,.346,1.354),(.044,.384,.386,1.314),(.066,.384,.386,1.314),(.066,.424,.346,1.354),(.16,.424,.346,1.354)]
ISOLATED_VOID_VOLUMES['WholeIsolatedSteppedThroughFrameAperture']=dict(loopmesh([rect_y(*q) for q in passage]),targets=[BODY],role='Entire continuous stepped through aperture of frame alone, all mouth, throat and enlarged middle portions; panels deliberately excluded only for this isolated frame test.')
CONTRACT={'single_prop_count':1,'mesh_count':len(G),'whole_through_frame':1,'opposing_integral_shoulder_rings':2,'independent_thick_panels':2,'panel_thickness_m':.018,'panel_recess_depth_m':.057,'panel_edge_clearance_m':.006,'middle_chamber_depth_m':.13,'fixed_short_columns':2,'whole_ground_runners':2,'finite_opposed_contacts':len(CONTACTS),'whole_air_domains':len(VOID_VOLUMES),'isolated_whole_aperture_domains':len(ISOLATED_VOID_VOLUMES),'whole_material_domains':len(SOLID_VOLUMES),'fixed_unlit_static_only':True,'ground_exported':False}
def measure_lightbox_geometry(vertices):
 assert set(vertices)==set(G) and len(vertices)==7
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for n in[FRONT,BACK]:assert abs(max(p[1] for p in vertices[n])-min(p[1] for p in vertices[n])-.018)<2e-7
 assert abs(min(p[2] for p in vertices[BODY])-.28)<2e-7 and abs(max(p[2] for p in vertices[BODY])-1.42)<2e-7
 return dict(CONTRACT,geometry_scope='Actual complete coordinates; full finite interfaces and whole air/material boundaries separately certified. No light, electrical, load or safety inference.')
INSIDE_TESTS=[(BODY,(.46,0,.85),(0,0,.85)),(BODY,(.40,-.055,.85),(0,-.055,.85)),(FRONT,(0,-.074,.85),(0,0,.85)),(BACK,(0,.074,.85),(0,0,.85))]
FOCUS=(0,0,.71);ORTHO=1.88
CAMERAS={'gray-front3q':(3.2,-5.0,2.7),'gray-back3q':(-3.2,5.0,2.7),'thumbnail':(3.2,-5.0,2.7),'qa-front':(0,-6,2.5),'qa-side':(6,0,2.5),'qa-top':(0,0,6),'qa-back':(0,6,2.5),'qa-wireframe':(3.2,-5.0,2.7),'silhouette-128-front':(0,-6,2.5),'silhouette-128-side':(6,0,2.5)}
WIRE_THICKNESS=ORTHO/1600
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
root=bpy.data.objects.new('OneDoubleSidedRecessedLightbox',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred dual-runner ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
 if r['name'] in ['FrontWholePanelShoulderAnnulus','BackWholePanelShoulderAnnulus']:
  is_front=r['name'].startswith('Front');panel=FRONT if is_front else BACK
  # Every actual vertex of the frame and panel must remain within a newly added strict
  # 1e-7 m all-vertex source-space bound; no coordinate is modified or snapped.
  for name in [BODY,panel]:
   original=G[name]['vertices'];actual=[tuple(o) for o in [byname[name].matrix_world@v.co for v in byname[name].data.vertices]]
   assert len(original)==len(actual)
   assert max(abs(a-b) for p,q in zip(original,actual) for a,b in zip(p,q))<1e-7,(name,'Source-space vertex mismatch')
  panel_indices=[2,3,6,7] if is_front else [0,1,4,5]
  inner_indices=list(range(16,20)) if is_front else list(range(36,40))
  outer_indices=list(range(12,16)) if is_front else list(range(40,44))
  def full_rectangle(name,indices):
   o=byname[name];points=[local(tuple(o.matrix_world@o.data.vertices[i].co)) for i in indices]
   assert max(abs(p[2]-r['plane_m']) for p in points)<1e-7
   xx=sorted({p[0] for p in points});yy=sorted({p[1] for p in points})
   assert len(xx)==len(yy)==2 and {(p[0],p[1]) for p in points}=={(x,y) for x in xx for y in yy},'Incomplete rectangular boundary'
   return xx,yy,(xx[1]-xx[0])*(yy[1]-yy[0])
  px,pz,panel_area=full_rectangle(panel,panel_indices)
  ix,iz,hole_area=full_rectangle(BODY,inner_indices)
  ox,oz,_=full_rectangle(BODY,outer_indices)
  assert all(o[0]<p[0]<i[0]<i[1]<p[1]<o[1] for o,p,i in [(ox,px,ix),(oz,pz,iz)]),'Panel/shoulder complete annulus nesting'
  actual_boundary_expected_area=panel_area-hole_area
  assert abs(actual_boundary_expected_area-r['complete_interface_area_m2'])<1e-7,'Nominal full-domain area drift'
  assert abs(area-actual_boundary_expected_area)<1e-8,(r,area,actual_boundary_expected_area)
 else:
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
mount_evidence=measure_lightbox_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'lightbox_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/arcade/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'arcade','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
