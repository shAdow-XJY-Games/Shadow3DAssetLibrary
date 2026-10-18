"""Original twin-upright barbell display rack; one complete static visual prop.
Metres, native Z up, front -Y. No use, load, stability or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='fitness-twin-upright-barbell-rack-kit-01';VERSION='1.0.0';TITLE='Twin-Upright Barbell Display Rack'
DESCRIPTION=('One original low-poly twin-upright barbell rack, counted as one complete static prop. Two broad ground feet and solid uprights are joined by one low rear crossbrace. '
 'Each upright carries a thick open J-shaped cradle; two finite lower facets of one continuous long bar sit on the opposed horizontal cradle seats. The central grip span remains clear. '
 'Two thick bevelled annular weight plates have real through-bores. Each plate is held in one frozen position between independent inner shoulder and outer retaining rings with finite opposed annular end-face contacts. The complete bore walls retain positive clearance around the bar. '
 'Fourteen named editable closed meshes, five opaque constant PBR materials; metres, native Z up, front -Y, horizontally bounds-centred ground origin. '
 'No athlete, bench, extra plates, room, textures, labels or animation. Static visual pose only: no exercise suitability, height adjustment, lifting, insertion/removal path, weight, friction, load, stability, anti-tip, manufacturing, installation, equipment-standard or safety claim. No compatibility with historical fitness assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];ISOLATED_VOID_VOLUMES={};VOID_VOLUMES={};PLATES={};HOOKS=[];UPRIGHTS=[];COLLARS=[]
PALETTE=[('Frame_DeepTeal',(.045,.205,.225,1),.42,.40),('Bar_BrushedSteel',(.43,.49,.51,1),.28,.78),('Plate_MutedCoral',(.48,.135,.085,1),.62,.08),('Foot_Graphite',(.035,.046,.050,1),.79,0),('Collar_WarmBrass',(.68,.39,.095,1),.31,.65)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(1,0,0),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
U=(0,1,0);V=(0,0,1);D=(1,0,0);BAR_ORIGIN=(0,0,1.16);BAR_RADIUS=.022;BAR_SIDES=16
SEAT_Z=round(1.16-BAR_RADIUS*math.cos(math.pi/BAR_SIDES),8)
def axial(o,x,y,t):return add(o,add(mul(U,x),add(mul(V,y),mul(D,t))))
def lathe(profile,o,n=32,phase=0,closed=True):
 vs=[];rings=[];fs=[];segments=[]
 for r,t in profile:
  rr=[]
  for j in range(n if r else 1):
   a=math.tau*j/n+phase;rr.append(len(vs));vs.append(axial(o,r*math.cos(a),r*math.sin(a),t))
  rings.append(rr)
 edges=list(zip(rings,rings[1:]))+([(rings[-1],rings[0])] if closed else [])
 for k,(a,b) in enumerate(edges):
  if len(a)==len(b)==1:continue
  for i in range(n):
   j=(i+1)%n
   ff=[(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])]
   fs.extend(ff);segments.extend([k]*len(ff))
 vol=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if vol<0:fs=[tuple(reversed(f)) for f in fs]
 return vs,fs,segments,rings

def axial_mesh(name,profile,o,mat,role,n=32,phase=0):
 v,f,segments,rings=lathe(profile,o,n,phase);mesh(name,v,f,mat,role);G[name].update(face_profile_segments=segments,rings=rings);return name

def prism_x(name,x,width,yz,mat,role):
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 # yz profile is counterclockwise as viewed along +X; face winding is outward.
 return mesh(name,vs,fs,mat,role)

def void_box(name,lo,hi,targets,scope):
 VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'targets':targets,'role':scope}
for label,x in [('Left',-.62),('Right',.62)]:
 foot=box('Rack_Foot_'+label,(x,0,.0225),(.20,.80,.045),3,'broad finite rectangular ground pad');FEET.append(foot)
 upright=box('Rack_Upright_'+label,(x,.14,.65),(.094,.070,1.24),0,'solid side upright seated into ground pad and rear cradle wall');UPRIGHTS.append(upright);link(foot,upright,(x,.14,.038),axis=(1,0,0),spread=.020)
 hook='Rack_JCradle_'+label;HOOKS.append(hook)
 prism_x(hook,x,.12,[(-.125,SEAT_Z-.040),(.115,SEAT_Z-.040),(.115,1.31),(.075,1.31),(.075,SEAT_Z),(-.085,SEAT_Z),(-.085,1.205),(-.125,1.205)],4,'one closed thick J-profile cradle, broad bottom seat, high rear wall and shorter front lip; full top opening')
 link(upright,hook,(x,.110,1.20),axis=(1,0,0),spread=.028)
 CONTACTS.append({'a':hook,'b':'Bar_ContinuousShaft','origin_m':(0,0,0),'axis':(0,0,1),'u':(1,0,0),'v':(0,1,0),'plane_m':SEAT_Z,'minimum_patch_area_m2':.0009,'interior_probe_offset_m':.0003,'points':[(x+d,0,SEAT_Z) for d in[-.04,0,.04]],'scope':'complete finite horizontal opposed bar lower-facet/cradle-seat contact, no penetration'})
 void_box(hook+'_FullIsolatedOpening',(x-.059,-.084,SEAT_Z+.0008),(x+.059,.074,1.315),[hook],'complete finite empty J opening before inserted bar; open at full upper throat')
 void_box(hook+'_UpperThroat',(x-.059,-.084,1.183),(x+.059,.074,1.315),[],'complete assembled open throat above bar')
 void_box(hook+'_FrontAir',(x-.059,-.084,SEAT_Z+.0008),(x+.059,-.023,1.182),[],'assembled front clearance volume beside entire seated bar section')
 void_box(hook+'_RearAir',(x-.059,.023,SEAT_Z+.0008),(x+.059,.074,1.182),[],'assembled rear clearance volume beside entire seated bar section')
brace=box('Rack_LowRearCrossbrace',(0,.14,.22),(1.28,.058,.070),0,'one low crossbrace joined positively into both independent side uprights')
for upright,x in zip(UPRIGHTS,[-.62,.62]):link(upright,brace,(x,.14,.22),axis=(0,0,1),spread=.015)
axial_mesh('Bar_ContinuousShaft',[(0,-1.15),(.022,-1.15),(.022,1.15),(0,1.15)],BAR_ORIGIN,1,'one continuous horizontal solid 16-facet bar with two finite flat underside seats; long unobstructed central span',16,math.pi/16)
for label,sign in [('Left',-1),('Right',1)]:
 lo,hi=sorted([sign*.87,sign*.95]);name='Weight_'+label+'_PiercedPlate'
 axial_mesh(name,[(.030,lo),(.214,lo),(.240,lo+.008),(.240,hi-.008),(.214,hi),(.030,hi)],BAR_ORIGIN,2,'thick bevel-edged annular plate with continuous real axial through-bore; fixed between finite inner and outer ring contacts')
 for kind,a,b in [('Inner',.835,.87),('Outer',.95,.987)]:
  cl,ch=sorted([sign*a,sign*b]);cn='Weight_'+label+'_'+kind+'Ring';COLLARS.append(cn)
  axial_mesh(cn,[(.019,cl),(.055,cl),(.055,ch),(.019,ch)],BAR_ORIGIN,4,'separate annular static '+kind.lower()+' collar with finite shaft overlap and finite opposed plate end-face contact')
  LINKS.append(('Bar_ContinuousShaft',cn,[axial(BAR_ORIGIN,.020*math.cos(t),.020*math.sin(t),(cl+ch)/2) for t in[0,math.tau/3,2*math.tau/3]]))
  plane=lo if ch<=lo+1e-7 else hi
  aobj,bobj=(cn,name) if ch<=lo+1e-7 else (name,cn)
  CONTACTS.append({'a':aobj,'b':bobj,'origin_m':BAR_ORIGIN,'axis':D,'u':U,'v':V,'plane_m':plane,'minimum_patch_area_m2':.006,'interior_probe_offset_m':.0003,'points':[axial(BAR_ORIGIN,.042*math.cos(t),.042*math.sin(t),plane) for t in[0,math.tau/3,2*math.tau/3]],'scope':'complete finite opposed annular ring-to-plate end faces; frozen static placement, no penetration'})
 PLATES[name]={'origin_m':BAR_ORIGIN,'lo_m':lo,'hi_m':hi,'bar':'Bar_ContinuousShaft','bore_radius_m':.030,'inner_wall_profile_segment':5,'sign':sign}
 v,f,_,_=lathe([(0,lo-.001),(.0292,lo-.001),(.0292,hi+.001),(0,hi+.001)],BAR_ORIGIN)
 ISOLATED_VOID_VOLUMES[name+'_FullBore']={'vertices':v,'faces':f,'targets':[name],'role':'entire finite pierced bore with 0.8 mm radial wall inset, extending past both mouths'}
 v,f,_,_=lathe([(.023,lo+.0008),(.0292,lo+.0008),(.0292,hi-.0008),(.023,hi-.0008)],BAR_ORIGIN)
 VOID_VOLUMES[name+'_AssembledAnnularAir']={'vertices':v,'faces':f,'targets':[],'role':'complete finite annular empty volume around full bar through plate, inset only from end contacts'}
 BORES.append({'mesh':name,'origin_m':axial(BAR_ORIGIN,0,0,lo-.001),'direction':D,'length_m':hi-lo+.002,'meaning':'supplementary isolated bore axis ray; full finite volume acceptance also required'})
void_box('Rack_CentralClearSpan',(-.54,-.082,.270),(.54,.075,1.120),[],'full finite empty central space beneath bar between uprights and above low brace')
for name,g in VOID_VOLUMES.items():
 if not g['targets']:g['targets']=list(G)
RACK_CONTRACT={'single_prop_count':1,'upright_count':2,'open_j_cradle_count':2,'continuous_bar_count':1,'true_through_bore_plate_count':2,'independent_shoulder_retainer_ring_count':4,'finite_bar_to_cradle_seats':2,'finite_plate_end_face_contacts':4,'nonbearing_full_bore_wall_clearance_required':True,'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_barbell_rack_geometry(vertices):
 assert set(vertices)==set(G)
 assert all(abs(min(p[2] for p in vertices[n]))<2e-7 for n in FEET)
 bar=vertices['Bar_ContinuousShaft'];assert abs(min(p[0] for p in bar)+1.15)<2e-7 and abs(max(p[0] for p in bar)-1.15)<2e-7
 assert abs(min(p[2] for p in bar)-SEAT_Z)<2e-7
 for n,r in PLATES.items():
  assert abs(min(p[0] for p in vertices[n])-r['lo_m'])<2e-7 and abs(max(p[0] for p in vertices[n])-r['hi_m'])<2e-7
 return dict(RACK_CONTRACT,geometry_scope='actual source/exported coordinates; finite contacts, complete nonbearing surfaces, closed void volumes and actual mutation controls remain required')
FOCUS=(0,0,.66);ORTHO=2.82
CAMERAS={'gray-front3q':(2.8,-4.6,3.2),'gray-back3q':(-2.8,4.6,3.2),'thumbnail':(2.8,-4.6,3.2),'qa-front':(0,-4.8,2.7),'qa-side':(4.8,0,2.7),'qa-top':(0,0,4.5),'qa-back':(0,4.8,2.7),'qa-wireframe':(2.8,-4.6,3.2),'silhouette-128-front':(0,-4.8,2.7),'silhouette-128-side':(4.8,0,2.7)}
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
root=bpy.data.objects.new('OneTwinUprightBarbellRack',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-.62,0,.0225),(-.62,0,.06)),('Weight_Right_PiercedPlate',(.91,.10,1.16),(.91,0,1.16))]:
 assert inside(trees[name],p) and not inside(trees[name],outside)
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
mount_evidence=measure_barbell_rack_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'barbell_rack_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/fitness/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'fitness','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
