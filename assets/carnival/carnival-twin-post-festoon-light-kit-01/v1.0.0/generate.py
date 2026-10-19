"""Original twin octagonal posts with one continuous sagging line and seven fitted pear pendants; one fixed non-emitting prop."""
import math,json,hashlib,sys,time,collections
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='carnival-twin-post-festoon-light-kit-01';VERSION='1.0.0';TITLE='Twin Post Pear Festoon Lights'
DESCRIPTION=('One original twin-post festoon assembly, counted as exactly one static visual prop. Two tall slender octagonal posts have integral broad finite octagonal ground feet and stepped shoulders. Two brass-coloured thick terminal blocks rest on complete post-top faces. One continuous closed eight-sided line sags between their complete inward end faces. Seven short vertical branches have sloped upper caps fitted to actual complete lower line facets, full lower caps on independent shaped holders, and finite holder-to-neck seats for seven original opaque pear-shaped bulbs. The entire closed support chain reaches both finite ground feet. Twenty-six closed editable components and five unlinked solid PBR colors; metre scale, source Z up, front -Y, horizontally bounds-centred ground origin. Original post, terminal, branch, holder and pear surfaces; no imported old barrier, pennant arch or copied lantern, no texture, emission, transmission, animation, power source, stage, crowd or scene. Fixed illustrative geometry only: no electrical circuit, voltage, illumination, waterproofing, fire resistance, electrical/public-event safety, wind loading, line tension, anti-tip, stability, installation, loading, human passage, material/manufacturing, old-arch compatibility or dynamic cable behavior claim.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};SOLID_VOLUMES={};FEET=[];PENDANTS=[]
CABLE='ContinuousSaggingMainLine';BODY=CABLE
PALETTE=[('DeepTeal_Posts',(.055,.19,.20,1),.55,.12),('Charcoal_LineAndFoot',(.035,.052,.049,1),.72,.02),('WarmBrass_Terminals',(.55,.33,.10,1),.43,.58),('OpaqueWarmIvory_Bulb',(.90,.73,.43,1),.54,0),('OpaqueSoftAmber_Bulb',(.75,.31,.10,1),.57,0)]
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
def box(lo,hi,mat=0,role=''):return mesh([(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]],BOX_FACES,mat,role)
def loft(rings,mat=0,role=''):
 n=len(rings[0]);assert all(len(r)==n for r in rings);v=[p for r in rings for p in r];f=[tuple(reversed(range(n))),tuple(range(n*(len(rings)-1),n*len(rings)))]
 f += [(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j) for i in range(len(rings)-1) for j in range(n)]
 return mesh(v,f,mat,role)
def lathe(x,profile,n=12,mat=0,role='',phase=0):return loft([[(x+r*math.cos(math.tau*j/n+phase),r*math.sin(math.tau*j/n+phase),z) for j in range(n)] for z,r in profile],mat,role)
def contact(name,a,b,axis,p,area,points=None,offset=.0004):
 axis=unit(axis);u=unit(cross((0,1,0),axis)) if abs(axis[1])<.9 else (1,0,0);v=cross(axis,u)
 CONTACTS.append({'name':name,'a':a,'b':b,'origin_m':(0,0,0),'u':u,'v':v,'axis':axis,'plane_m':dot(axis,p),'points':points or [p],'minimum_patch_area_m2':area,'interior_probe_offset_m':offset})
def air(name,g,role):VOID_VOLUMES[name]=dict(g,targets=list(G),role=role)
def solid(name,g,targets,role):SOLID_VOLUMES[name]=dict(g,targets=targets,role=role)
# New eight-sided architectural posts, intentionally unlike the older turned
# crowd-barrier stanchions. The block terminal has a real lower bearing and an
# inward complete face, not a floating line end or hidden overlap.
POST_PROFILE=[(0,.265),(.045,.265),(.080,.225),(.080,.110),(.145,.110),(.200,.064),(2.565,.052),(2.615,.070),(2.680,.070)]
for side,s in [('Left',-1),('Right',1)]:
 x=s*1.80;p='OctagonalPost_'+side;t='TopTerminal_'+side;FEET.append(p)
 G[p]=lathe(x,POST_PROFILE,8,0,'One new continuous closed eight-sided finite foot, stepped shoulder, slender tapered post and full upper terminal bearing.',math.pi/8)
 G[p]['face_materials']=[1,2]+[1 if i<3 else 2 if i==7 else 0 for i in range(len(POST_PROFILE)-1) for j in range(8)]
 G[t]=box((x-.115,-.075,2.680),(x+.115,.075,2.850),2,'One thick solid top terminal with a finite underside resting on the post and a complete inward line-end face.')
 contact(t+'_FullPostBearing',p,t,(0,0,1),(x,0,2.680),.0138)
 if s<0:contact('MainLine_LeftCompleteEnd',t,CABLE,(1,0,0),(-1.685,0,2.760),.00223)
 else:contact('MainLine_RightCompleteEnd',CABLE,t,(1,0,0),(1.685,0,2.760),.00223)
 solid(p+'_WholeNarrowShaftCore',lathe(x,[(.201,.040),(2.564,.040)],8),[p],'Complete finite narrow shaft core from above lower shoulder to below upper shoulder; all axial length, 12 mm or greater radial material margin.')
# One uninterrupted thick line with shared full section rings. Constant X-plane
# sections create real planar underside facets; each branch fits one full facet.
LINE_X=[-1.685]+[round(.055+.11*i,9) for i in range(-15,15)]+[1.685]
def curve_z(x):return 2.14+.62*(x/1.685)**2
CABLE_PATH=[(x,0,curve_z(x)) for x in LINE_X];sides=8;LINE_APOTHEM=.026
SECTION=[(LINE_APOTHEM/math.cos(math.pi/8)*math.cos(math.pi/8+math.tau*j/8),LINE_APOTHEM/math.cos(math.pi/8)*math.sin(math.pi/8+math.tau*j/8)) for j in range(8)]
G[CABLE]=loft([[(x,y,z+dz) for y,dz in SECTION] for x,_,z in CABLE_PATH],1,'One closed connected eight-sided main line, 31 complete shared-ring bands, continuously sagging with no separate segments or bevel curves; both end caps finitely seated.')
def line_level(x):
 i=next(i for i in range(len(LINE_X)-1) if LINE_X[i]-1e-10<=x<=LINE_X[i+1]+1e-10);a,b=LINE_X[i:i+2];m=(curve_z(b)-curve_z(a))/(b-a)
 return curve_z(a)+(x-a)*m,m,i
inner_path=[(-1.682,0,line_level(-1.682)[0])]+CABLE_PATH[1:-1]+[(1.682,0,line_level(1.682)[0])]
solid('CompleteContinuousMainLineCore',loft([[(x,y*.25,z+dz*.25) for y,dz in SECTION] for x,_,z in inner_path]),[CABLE],'Entire continuous thin material core through every main-line band, with 3 mm end inset and 19.5 mm radial margin; no sampled point substitute.')
BULB_X=[-.132e1,-.88,-.44,0,.44,.88,.132e1]
for i,x in enumerate(BULB_X,1):
 z,m,band=line_level(x);root=z-LINE_APOTHEM;low=root-.120;neck=low-.075
 branch=f'Pendant_{i}_FittedBranch';holder=f'Pendant_{i}_ShapedHolder';bulb=f'Pendant_{i}_OpaquePear'
 poly=[(.009*math.cos(math.tau*j/12),.009*math.sin(math.tau*j/12)) for j in range(12)]
 G[branch]=loft([[(x+u,v,low) for u,v in poly],[(x+u,v,root+m*u) for u,v in poly]],1,'One closed short vertical drop with a complete sloped cap exactly fitted to the main-line lower facet and a full lower holder seat.')
 G[holder]=lathe(x,[(neck,.029),(neck+.016,.035),(neck+.031,.035),(low-.016,.022),(low,.022)],12,2,'One original closed stepped pendant holder with a finite branch-top seat and a finite underside neck-bearing face.')
 profile=[(neck-.195,.010),(neck-.185,.032),(neck-.160,.054),(neck-.125,.066),(neck-.090,.061),(neck-.052,.041),(neck-.025,.023),(neck,.023)]
 G[bulb]=lathe(x,profile,12,3+(i%3==0),'One original opaque non-emitting closed pear bulb, faceted rounded lower body and an actual narrow full neck capped against its holder; no lantern cage or reused diffuser.')
 contact(branch+'_FullSlopedRoot',CABLE,branch,(m,0,-1),(x,0,root),.000242*math.sqrt(1+m*m))
 contact(branch+'_FullHolderSeat',holder,branch,(0,0,1),(x,0,low),.000242)
 contact(bulb+'_FullNeckSeat',holder,bulb,(0,0,-1),(x,0,neck),.001586)
 solid(branch+'_CompleteCore',loft([[(x+u*.5,v*.5,low+.001) for u,v in poly],[(x+u*.5,v*.5,root+m*u*.5-.001) for u,v in poly]]),[branch],'Complete full-length branch material core; 1 mm cap insets and 4.5 mm radial inset.')
 solid(bulb+'_CompleteNeckCore',lathe(x,[(neck-.024,.015),(neck-.001,.015)],12),[bulb],'Complete finite bulb-neck material core including its full axial extent; 1 mm axial and 8 mm radial margins.')
 PENDANTS.append({'index':i,'x_m':x,'mainline_band':band,'mainline_slope':m,'branch':branch,'holder':holder,'bulb':bulb,'root_z_m':root,'holder_top_z_m':low,'neck_z_m':neck,'bulb_bottom_z_m':neck-.195,'maximum_bulb_radius_m':.066})
# One complete central under-light air body: all full-height lower corridor plus
# every upper inter-pendant bay, under each actual line facet. The seven finite
# pendant silhouette keepouts are explicit 3 mm expanded bounding envelopes.
# The front/back whole side corridors cover air beyond those silhouette envelopes.
A=-1.540;B=1.540;KEEP=.069
stations=sorted(set([A,B]+[x for x in LINE_X if A<x<B]+[x+d for x in BULB_X for d in [-KEEP,KEEP]]))
def ceiling(x,mid):
 q=next((p for p in PENDANTS if abs(mid-p['x_m'])<KEEP),None)
 return q['bulb_bottom_z_m']-.003 if q else line_level(x)[0]-LINE_APOTHEM-.003
upper=[]
for a,b in zip(stations,stations[1:]):
 mid=(a+b)/2
 for p in [(a,ceiling(a,mid)),(b,ceiling(b,mid))]:
  if not upper or abs(upper[-1][0]-p[0])>1e-10 or abs(upper[-1][1]-p[1])>1e-10:upper.append(p)
poly=[(A,.003),(B,.003)]+list(reversed(upper))
def xz_prism(poly,y0,y1):
 n=len(poly);return mesh([(x,y,z) for y in [y0,y1] for x,z in poly],[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
air('WholeCentralUnderLightCorridor',xz_prism(poly,-.180,.180),'One connected complete finite central under-light corridor, full base-to-base useful width and depth, ground to complete line underside in every inter-pendant bay. Only seven explicitly expanded pendant silhouette envelopes are excluded; 3 mm surface margins.')
for side,(a,b) in [('Front',(-.180,-.069)),('Back',(.069,.180))]:
 top=[(x,line_level(x)[0]-.029) for x in [A]+[q for q in LINE_X if A<q<B]+[B]]
 air('WholePendantSideAir_'+side,xz_prism([(A,.003),(B,.003)]+list(reversed(top)),a,b),'Complete finite full-width side corridor outside every pendant and branch, from ground to line underside; three millimetre margin beyond the maximum pear radius.')
FESTOON_CONTRACT={'single_prop_count':1,'closed_posts':2,'finite_terminal_blocks':2,'continuous_mainline_meshes':1,'mainline_bands':len(CABLE_PATH)-1,'mainline_sides':sides,'branch_holder_pear_chains':7,'closed_components':len(G),'finite_opposed_contacts':len(CONTACTS),'whole_empty_volumes':len(VOID_VOLUMES),'solid_material_volumes':len(SOLID_VOLUMES),'non_emitting_opaque_visual_only':True}
def measure_festoon_geometry(vertices):
 assert set(vertices)==set(G);assert all(abs(min(p[2] for p in vertices[n]))<2e-7 for n in FEET)
 for p in PENDANTS:
  assert min(q[2] for q in vertices[p['bulb']])>1.70
  assert abs(max(q[2] for q in vertices[p['bulb']])-p['neck_z_m'])<3e-7
 return dict(FESTOON_CONTRACT,geometry_scope='actual source/exported coordinates; complete opposed surfaces, whole air/material bodies and independent actual negatives remain required')
FOCUS=(0,0,1.37);ORTHO=5.1
CAMERAS={'gray-front3q':(4,-9,5.6),'gray-back3q':(-4,9,5.6),'thumbnail':(4,-9,5.6),'qa-front':(0,-10,4.7),'qa-side':(10,0,4.7),'qa-top':(0,0,10),'qa-back':(0,10,4.7),'qa-wireframe':(4,-9,5.6),'silhouette-128-front':(0,-10,4.7),'silhouette-128-side':(10,0,4.7)}
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
root=bpy.data.objects.new('OneTwinPostPearFestoonAssembly',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='horizontally bounds-centred finite twin-post ground datum, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-1.8,0,.020),(-1.8,0,2.9)),(CABLE,(0,0,line_level(0)[0]),(0,0,1.5))]:
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
mount_evidence=measure_festoon_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'festoon_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
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
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'carnival','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
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
