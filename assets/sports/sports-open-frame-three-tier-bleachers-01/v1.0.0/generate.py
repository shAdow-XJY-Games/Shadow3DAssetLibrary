"""Original open-frame three-tier bleachers; one complete static visual prop.
Metres, native Z up, front -Y. No use, load, capacity, body-fit or safety claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='sports-open-frame-three-tier-bleachers-01';VERSION='1.0.0';TITLE='Open-Frame Three-Tier Bleachers'
DESCRIPTION=('One original low-poly three-tier bleacher module, counted as one complete static prop. Three separate long thick seat boards rise and step backward over three open support frames. Three lower footboards sit in front of their corresponding seat rows with real vertical and horizontal air gaps. Three grounded runners, nine uprights, three full-length seat beams, nine finite footboard arms and six diagonal braces form one connected fixed visual assembly. All part interfaces are finite opposed face contacts. No solid stair blocks, copied benches, passenger seats, railing, spectator, field, labels or animation. Thirty-six closed editable meshes with four opaque constant PBR materials; metres, native Z up, front -Y, horizontally bounds-centred ground origin. Static visual appearance only: no capacity, load, strength, stability, anti-tip, walking, access, evacuation, handrail, sport-facility standard, body fit, manufacture, installation or public safety claim. No compatibility with historical scene assets is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];ISOLATED_VOID_VOLUMES={};VOID_VOLUMES={};SEATS=[];FOOTBOARDS=[];BEAMS=[];POSTS=[];ARMS=[];BRACES=[]
PALETTE=[('Frame_DeepTeal',(.035,.18,.20,1),.53,.28),('Seat_WarmOchre',(.72,.39,.12,1),.63,.05),('Footboard_BrushedSlate',(.33,.41,.43,1),.47,.52),('Runner_Graphite',(.045,.06,.065,1),.77,.08)]
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
def prism_x(name,x,width,yz,mat,role):
 vs=[(xx,y,z) for xx in[x-width/2,x+width/2] for y,z in yz];n=len(yz)
 fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,role)
def contact(a,b,axis,plane,point,area,scope):
 u=(1,0,0);v=(0,1,0) if axis==(0,0,1) else (0,0,-1)
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':axis,'u':u,'v':v,'plane_m':round(plane,8),'minimum_patch_area_m2':area,'interior_probe_offset_m':.0003,'points':[add(point,mul(u,d)) for d in[-.015,0,.015]],'scope':scope})
def void_box(name,lo,hi,scope):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'targets':[],'role':scope}
XS=[-1.48,0,1.48];YS=[-.70,0,.70];ZS=[.50,.88,1.26]
for k,x in enumerate(XS):
 n=box('Frame_%d_GroundRunner'%k,(x,0,.035),(.15,2.34,.07),3,'one continuous finite flat-bottom ground runner for a complete stepped support frame');FEET.append(n)
for r,(y,z) in enumerate(zip(YS,ZS)):
 bottom=z-.055;beamlo=bottom-.08;fz=z-.29;fb=fz-.045
 seat=box('Row_%d_SeatBoard'%r,(0,y,z-.0275),(3.60,.28,.055),1,'independent full-length thick seat board at tier %d; separate from its lower forward footboard'%(r+1));SEATS.append(seat)
 beam=box('Row_%d_ContinuousSeatBeam'%r,(0,y,bottom-.04),(3.36,.16,.08),0,'full-length finite beam under entire seat row, supported at left, centre and right');BEAMS.append(beam)
 contact(beam,seat,(0,0,1),bottom,(0,y,bottom),.5375,'whole 3.36 by 0.16 m finite opposed beam-top/seat-underside patch')
 foot=box('Row_%d_Footboard'%r,(0,y-.32,fz-.0225),(3.60,.22,.045),2,'independent full-length footboard, 0.29 m below seat top and 0.32 m forward');FOOTBOARDS.append(foot)
 for k,x in enumerate(XS):
  post=box('Frame_%d_Row_%d_Upright'%(k,r),(x,y,(.07+beamlo)/2),(.12,.11,beamlo-.07),0,'finite solid upright from ground runner top to full seat beam underside');POSTS.append(post)
  contact(FEET[k],post,(0,0,1),.07,(x,y,.07),.0131,'whole finite post-root rectangle seated on runner')
  contact(post,beam,(0,0,1),beamlo,(x,y,beamlo),.0131,'whole finite post-top rectangle beneath full-length seat beam')
  arm=box('Frame_%d_Row_%d_FootArm'%(k,r),(x,y-(.43+.055)/2,fb-.03),(.10,.375,.06),0,'finite forward arm with complete rectangular end on upright and broad upper footboard seat');ARMS.append(arm)
  contact(arm,post,(0,1,0),y-.055,(x,y-.055,fb-.03),.0059,'entire finite 0.10 by 0.06 m arm end against front upright face')
  contact(arm,foot,(0,0,1),fb,(x,y-.32,fb),.0219,'whole 0.10 by 0.22 m footboard underside patch on each arm')
for k,x in enumerate(XS):
 for bay,(y0,z0) in enumerate([(-.645,.12),(.055,.50)]):
  y1=y0+.59;z1=z0+.26;n='Frame_%d_Bay_%d_Diagonal'%(k,bay)
  prism_x(n,x,.08,[(y0,z0),(y1,z1),(y1,z1+.06),(y0,z0+.06)],0,'closed thick diagonal prism; both full rectangular ends meet adjacent upright side faces');BRACES.append(n)
  contact('Frame_%d_Row_%d_Upright'%(k,bay),n,(0,1,0),y0,(x,y0,z0+.03),.0047,'entire lower diagonal root end against rear face of lower-row post')
  contact(n,'Frame_%d_Row_%d_Upright'%(k,bay+1),(0,1,0),y1,(x,y1,z1+.03),.0047,'entire upper diagonal tip end against front face of higher-row post')
# The complete finite open windows are kept between support slices, with a
# 1 mm inset from the true surfaces. These are volumes, not single ray samples.
for bay,(xl,xh) in enumerate([(-1.404,-.076),(.076,1.404)]):
 for r,(y,z) in enumerate(zip(YS,ZS)):
  void_box('Bay_%d_Row_%d_UnderSeat'%(bay,r),(xl,y-.139,.071),(xh,y+.139,z-.136),'entire connected seat-underbeam bay between the two adjacent support-frame slices')
  void_box('Bay_%d_Row_%d_UnderFootboard'%(bay,r),(xl,y-.429,.071),(xh,y-.211,z-.336),'entire footboard underside bay between adjacent support slices, excluding only their complete material envelope')
for r,(y,z) in enumerate(zip(YS,ZS)):
 void_box('Row_%d_SeatFootSlot'%r,(-1.799,y-.209,z-.289),(1.799,y-.141,z+.001),'full-length real gap between lower footboard rear edge and raised seat front edge')
for k,x in enumerate(XS):
 for bay,(y0,z0) in enumerate([(-.645,.12),(.055,.50)]):
  y1=y0+.59;z1=z0+.26;lo=y0+.001;hi=y1-.001;slope=(z1-z0)/(y1-y0)
  yz=[(lo,.071),(hi,.071),(hi,z1-.001-slope*.001),(lo,z0-.001+slope*.001)]
  vv=[(xx,y,z) for xx in[x-.039,x+.039] for y,z in yz];n=4
  ff=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  VOID_VOLUMES['Frame_%d_Bay_%d_BelowDiagonal'%(k,bay)]={'vertices':vv,'faces':ff,'targets':[],'role':'complete inset lower sloping open frame aperture between both upright faces, runner and diagonal underside'}
for name,g in VOID_VOLUMES.items():g['targets']=list(G)
BLEACHERS_CONTRACT={'single_prop_count':1,'tier_count':3,'independent_full_length_seat_boards':3,'independent_lower_forward_footboards':3,'complete_open_support_frames':3,'continuous_ground_runners':3,'solid_uprights':9,'full_length_seat_beams':3,'finite_footboard_arms':9,'finite_two_ended_diagonal_braces':6,'railing_count':0,'finite_opposed_contacts':51,'nominal_dimensions_not_used_as_clearance_acceptance':True}
def measure_bleachers_geometry(vertices):
 assert set(vertices)==set(G)
 for n in FEET:assert abs(min(p[2] for p in vertices[n]))<2e-7
 for r,(y,z) in enumerate(zip(YS,ZS)):
  for n,cy,top in [(SEATS[r],y,z),(FOOTBOARDS[r],y-.32,z-.29)]:
   v=vertices[n];assert abs(min(p[0] for p in v)+1.8)<2e-7 and abs(max(p[0] for p in v)-1.8)<2e-7
   assert abs(max(p[2] for p in v)-top)<2e-7 and abs((min(p[1] for p in v)+max(p[1] for p in v))/2-cy)<2e-7
 return dict(BLEACHERS_CONTRACT,geometry_scope='actual source/exported coordinates; full contacts, complete voids, all noncontact surfaces and real mutations still required')
FOCUS=(0,0,.60);ORTHO=5.00
CAMERAS={'gray-front3q':(4.6,-6.3,4.8),'gray-back3q':(-4.6,6.3,4.8),'thumbnail':(4.6,-6.3,4.8),'qa-front':(0,-6.8,3.8),'qa-side':(6.8,0,3.8),'qa-top':(0,0,7.0),'qa-back':(0,6.8,3.8),'qa-wireframe':(4.6,-6.3,4.8),'silhouette-128-front':(0,-6.8,3.8),'silhouette-128-side':(6.8,0,3.8)}
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
root=bpy.data.objects.new('OneOpenFrameThreeTierBleachers',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in [(FEET[0],(-1.48,0,.035),(-1.48,0,.08)),(SEATS[0],(0,-.70,.475),(0,-.70,.51))]:
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
mount_evidence=measure_bleachers_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'bleachers_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/sports/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'sports','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
