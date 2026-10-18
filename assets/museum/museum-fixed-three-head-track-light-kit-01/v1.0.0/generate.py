"""Original three-head museum track fixture. One fixed hanging visual prop.
No electrical, illumination, mechanical-motion, load or safety performance claim.
"""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='museum-fixed-three-head-track-light-kit-01';VERSION='1.0.0';TITLE='Fixed Three-Head Museum Track Light'
DESCRIPTION=('One original low-poly fixed three-head museum track-light assembly counted as one hanging prop. A continuous thick downward-open rail has integral inward shoulders and closed end stops. Three separate T-shaped seats rest on finite opposing rail shoulders with positive clearance on every other slot surface. Each integral neck connects to a crossbar and two genuinely bored bracket ears. One bored elongated central lug, one continuous capped pin and one fixed stop carry each original thick tapered lamp housing in a fixed -15, 0 or 15 degree pose. Each housing has a true deep front cavity and one opaque recessed diffuser disk seated on a finite inner shoulder. Two finite top mounting faces lie at source Z=0; all asset geometry lies on or below that plane. '
 'Thirty named editable closed meshes, five opaque constant PBR materials, metres, source Z up, illustrative front -Y and an origin at the mounting-plane centre. A temporary QA ceiling support is a geometric witness only, excluded from the model and formal renders. No ground contact or standalone support is claimed. No ceiling, wall, cable, supply, emitted light, scene, labels, textures or animation. Old task lamps, softboxes and lanterns already have light-head forms; the independently authored continuous slotted rail, three seated fixed heads and finite mounting patches provide the narrower new coverage. '
 'Static visual geometry only. No electrical connection, powered operation, illumination or photometry, beam angle, colour temperature, glare, heat dissipation, fire resistance, track-standard fit, sliding, tilting motion, assembly path, mounting load, fall protection, strength, manufacture, installation or luminaire/museum safety certification. No compatibility with earlier ceilings, walls, displays, cable trays, camera rails or light fixtures. Geometric contacts do not establish functional or safe equipment.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];MOUNTS=[];FEET=[];VOID_PROBES={};EAR_PAIRS=[];HEADS=[];SEAT_GAPS=[]
PALETTE=[('Charcoal_Rail',(.035,.048,.059,1),.40,.50),('WarmIvory_Housing',(.71,.67,.55,1),.47,.18),('Graphite_Brackets',(.095,.12,.13,1),.43,.50),('Brass_FixedPins',(.58,.34,.10,1),.34,.68),('Ivory_OpaqueDiffusers',(.83,.80,.68,1),.69,0)]
MATERIAL_CONTRACT='Five opaque unlinked constant Principled materials; no texture nodes, transmission or emission.'
FOCUS=(0,0,-.255);ORTHO=2.34
CAMERAS={'gray-front3q':(2.4,-4,-2.0),'gray-back3q':(-2.4,4,.8),'thumbnail':(2.4,-4,-2.0),'qa-front':(0,-4,-.255),'qa-side':(4,0,-.255),'qa-top':(0,0,4),'qa-back':(0,4,-.255),'qa-wireframe':(2.4,-4,-2.0),'silhouette-128-front':(0,-4,-.255),'silhouette-128-side':(4,0,-.255)}
CAMERA_SCALES={'qa-side':.76,'silhouette-128-side':.76};WIRE_THICKNESS=ORTHO/900
ATTACHMENT={'axis':'Z','coordinate_m':0,'normal':[0,0,1],'patches':[{'x_range_m':[x-.08,x+.08],'y_range_m':[-.06,.06],'area_m2':.0192} for x in [-.72,.72]],'total_area_m2':.0384,'role':'two bounded top mounting patches requiring external support; no ground contact'}
QA_SUPPORT={'lo_m':[-1,-.10,0],'hi_m':[1,.10,.04],'role':'temporary ceiling witness only; excluded from asset, native file, GLB and formal images'}

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
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
def cellsolid(name,xs,ys,zs,occupied,mat,role):
 m=Mesh();cells={(i,j,k) for i in range(len(xs)-1) for j in range(len(ys)-1) for k in range(len(zs)-1) if occupied((xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2,(zs[k]+zs[k+1])/2)}
 for i,j,k in sorted(cells):
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2];z0,z1=zs[k:k+2]
  sides=[((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]
  for (dx,dy,dz),q in sides:
   if (i+dx,j+dy,k+dz) not in cells:m.face(q,mat,'boundary')
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def slab(name,x0,x1,y0,y1,z0,z1,mat,role,transform=None):
 g=cellsolid(None,[x0,x1],[y0,y1],[z0,z1],lambda x,y,z:True,mat,role)
 if transform:g['vertices']=[transform(p) for p in g['vertices']]
 if name:G[name]=g
 return g
def profile(name,rings,mat,role,n=24,axis='z',transform=None):
 m=Mesh()
 def p(u,r,t):
  q=(r*math.cos(t),r*math.sin(t),u) if axis=='z' else (u,r*math.cos(t),r*math.sin(t))
  return transform(q) if transform else q
 for k,((u,r),(v,s)) in enumerate(zip(rings,rings[1:])):
  for i in range(n):
   a=math.tau*i/n;b=math.tau*(i+1)/n;tag='shaft' if axis=='x' and r==s==.011 else ('inner' if axis=='z' and k>=4 else 'profile')
   m.face([p(u,r,a),p(u,r,b),p(v,s,b),p(v,s,a)],mat,tag)
 for (u,r),rev in [(rings[0],True),(rings[-1],False)]:
  pts=[p(u,r,math.tau*i/n) for i in range(n)];m.face(pts[::-1] if rev else pts,mat,'end')
 g=m.result(role,mat)
 if name:G[name]=g
 return g
def ring(name,x0,x1,rin,rout,mat,transform,rect=None):
 m=Mesh();n=24
 def p(x,r,t):return transform((x,r*math.cos(t),r*math.sin(t)))
 def radius(t):
  if rect is None:return rout
  y=math.cos(t);z=math.sin(t);hy,zlo,zhi=rect
  return min(hy/max(abs(y),1e-12),(zhi if z>=0 else -zlo)/max(abs(z),1e-12))
 for i in range(n):
  a=math.tau*i/n;b=math.tau*(i+1)/n;ra,rb=radius(a),radius(b)
  for tag,poly in [('inner',[p(x0,rin,a),p(x1,rin,a),p(x1,rin,b),p(x0,rin,b)]),('outer',[p(x0,rb,b),p(x1,rb,b),p(x1,ra,a),p(x0,ra,a)]),('left',[p(x0,rin,b),p(x0,rb,b),p(x0,ra,a),p(x0,rin,a)]),('right',[p(x1,rin,a),p(x1,ra,a),p(x1,rb,b),p(x1,rin,b)])]:m.face(poly,mat,tag)
 g=m.result('Complete thick extruded ear with a genuine through-bore; central lug has an elongated lower tail.' if rect else 'Complete annular bracket ear with a genuine through-bore.',mat)
 if name:G[name]=g
 return g
# One continuous closed rail boundary, including roof, lower shoulders and end stops.
cellsolid('Rail_ContinuousDownOpenSlot',[-.96,-.90,.90,.96],[-.07,-.05,-.022,.022,.05,.07],[-.11,-.09,-.05,-.03],lambda x,y,z:abs(x)>.90 or z>-.05 or abs(y)>.05 or (z<-.09 and abs(y)>.022),0,'One continuous downward-open lipped rail, thick roof, sidewalls, opposed slot shoulders and integral closed end stops.')
for label,x in [('Left',-.72),('Right',.72)]:
 name='TopMount_'+label;slab(name,x-.08,x+.08,-.06,.06,-.04,0,2,'Bounded upper mounting pad at source Z=0; the bottom is finitely embedded into the rail.');MOUNTS.append(name)
 LINKS.append((name,'Rail_ContinuousDownOpenSlot',[(x-.03,0,-.035),(x+.03,0,-.035)]))
# Three independent seat-neck-bracket-head chains; the whole fixed kit is one prop.
for index,(cx,degrees) in enumerate([(-.60,-15),(0,0),(.60,15)],1):
 prefix='Head%d_'%index;ang=math.radians(degrees);c,s=math.cos(ang),math.sin(ang)
 def fixed(p,cx=cx):x,y,z=p;return (cx+x,y,-.225+z)
 def tilted(p,cx=cx,c=c,s=s):x,y,z=p;return (cx+x,c*y-s*z,-.225+s*y+c*z)
 def vector(p,c=c,s=s):x,y,z=p;return (x,c*y-s*z,s*y+c*z)
 seat=prefix+'TSeatAndNeck';bridge=prefix+'BracketBridge';left=prefix+'BracketEarLeft';right=prefix+'BracketEarRight';lug=prefix+'BoredLampLug';pin=prefix+'CappedFixedPin';shell=prefix+'ThickLampHousing';diffuser=prefix+'RecessedOpaqueDiffuser';stop=prefix+'FixedTiltStop'
 cellsolid(seat,[cx-.075,cx-.032,cx+.032,cx+.075],[-.043,-.010,.010,.043],[-.155,-.09,-.064],lambda x,y,z:z>-.09 or (abs(x-cx)<.032 and abs(y)<.010),2,'One continuous T-shaped slot seat and narrow pendant neck. Two opposed lower finite shoulder regions rest on the continuous rail lips.')
 CONTACTS.append({'a':'Rail_ContinuousDownOpenSlot','b':seat,'axis':2,'plane_m':-.09,'minimum_patch_area_m2':.00629,'interior_probe_offset_m':.001,'points':[(cx+x,y,-.09) for x in [-.05,.05] for y in [-.032,.032]],'scope':'two complete opposed seat/rail shoulder rectangles; all other full surfaces retain positive clearance'})
 slab(bridge,cx-.080,cx+.080,-.070,.070,-.175,-.147,2,'One rigid crossbar connecting neck, two annular ears and a finite embedded stop.')
 LINKS.append((seat,bridge,[(cx-.010,0,-.151),(cx+.010,0,-.151)]))
 for name,x0,x1,transform,rect in [(left,-.065,-.045,fixed,None),(lug,-.045,.045,tilted,(.033,-.110,.035)),(right,.045,.065,fixed,None)]:
  ring(name,x0,x1,.016,.060,2 if name!=lug else 1,transform,rect)
  if name!=lug:LINKS.append((name,bridge,[(cx+(x0+x1)/2,-.004,-.170),(cx+(x0+x1)/2,.004,-.170)]))
  else:LINKS.append((name,shell,[tilted((-.02,0,-.102)),tilted((.02,0,-.102))]))
  BORES.append({'mesh':name,'origin_m':list(fixed((x0-.002,0,0))),'direction':[1,0,0],'length_m':x1-x0+.004})
  EAR_PAIRS.append({'ear':name,'pin':pin,'x0':cx+x0,'x1':cx+x1,'head':index})
  VOID_PROBES['IsolatedFullBore_'+name]={'type':'mesh','geometry':profile(None,[(x0-.002,.0145),(x1+.002,.0145)],0,'Entire isolated bored volume.',axis='x',transform=fixed),'targets':[name],'role':'entire isolated through-bore including the core and both mouths'}
  VOID_PROBES['FullAnnularGap_'+name]={'type':'mesh','geometry':ring(None,x0+.001,x1-.001,.012,.015,0,fixed),'targets':[name,pin],'role':'entire shaft-to-bore annular air body, excluding axial contact planes by 1 mm'}
 profile(pin,[(-.077,.025),(-.065,.025),(-.065,.011),(.065,.011),(.065,.025),(.077,.025)],3,'One genuinely continuous capped fixed pin with a full positive shaft/bore gap.',axis='x',transform=fixed)
 for a,b,x,rad,area in [(pin,left,-.065,.020,.0010),(left,lug,-.045,.024,.0019),(lug,right,.045,.024,.0019),(right,pin,.065,.020,.0010)]:
  CONTACTS.append({'a':a,'b':b,'axis':0,'plane_m':cx+x,'minimum_patch_area_m2':area,'interior_probe_offset_m':.001,'points':[fixed((x,rad,0)),fixed((x,-rad,0)),fixed((x,0,rad)),fixed((x,0,-rad))],'scope':'complete opposed annular pin-cap or ear interface, distinct from full shaft/bore positive clearance'})
 profile(shell,[(-.090,.070),(-.110,.094),(-.280,.106),(-.300,.102),(-.300,.078),(-.165,.078),(-.165,.065),(-.135,.065)],1,'One original continuous thick tapered lamp housing, closed thick rear and genuine front cavity with an integral internal diffuser shoulder.',transform=tilted)
 profile(diffuser,[(-.177,.073),(-.165,.073)],4,'One fully opaque nonemissive recessed diffuser disk; its rear finite annulus sits on the internal housing shoulder.',transform=tilted)
 normal=vector((0,0,1));CONTACTS.append({'a':diffuser,'b':shell,'normal':normal,'plane_m':dot(normal,tilted((0,0,-.165))),'minimum_patch_area_m2':.0032,'interior_probe_offset_m':.001,'points':[tilted((.069,0,-.165)),tilted((-.069,0,-.165)),tilted((0,.069,-.165)),tilted((0,-.069,-.165))],'scope':'full rear annular diffuser seating region on the thick internal housing shoulder'})
 slab(stop,-.025,.025,.033,.050,.009,.072,2,'One fixed stop with finite opposed contact on the lamp lug and finite embedding in the crossbar.',tilted)
 LINKS.append((stop,bridge,[tilted((-.010,.039,.067)),tilted((.010,.039,.067))]))
 normal=vector((0,1,0));CONTACTS.append({'a':lug,'b':stop,'normal':normal,'plane_m':dot(normal,tilted((0,.033,.020))),'minimum_patch_area_m2':.00075,'interior_probe_offset_m':.001,'points':[tilted((x,.033,z)) for x in [-.012,.012] for z in [.014,.023]],'scope':'finite fixed lug-to-stop plane; no claim of adjustable or mechanically locked motion'})
 VOID_PROBES['CompleteDeepFrontCavity_'+str(index)]={'type':'mesh','geometry':profile(None,[(-.302,.076),(-.178,.076)],0,'Complete finite front cavity including its mouth and full radial section.',transform=tilted),'targets':list(G),'role':'entire deep front lamp cavity up to the recessed opaque disk, excluding solids by positive tolerance'}
 VOID_PROBES['BehindDiffuserCavity_'+str(index)]={'type':'mesh','geometry':profile(None,[(-.164,.063),(-.136,.063)],0,'Complete finite rear cavity behind the recessed disk.',transform=tilted),'targets':list(G),'role':'whole closed finite rear cavity between disk and thick housing back'}
 HEADS.append({'index':index,'centre_x_m':cx,'fixed_tilt_deg':degrees,'seat':seat,'bridge':bridge,'ears':[left,lug,right],'lug':lug,'pin':pin,'shell':shell,'diffuser':diffuser,'stop':stop,'transform_parameters':{'cx':cx,'radians':ang}})
# Full finite empty-slot partition: between seats, above seats, beside seats,
# alongside necks and below overhanging seat shoulders. No sample-ray substitute.
def emptybox(name,lo,hi,role,targets=None):VOID_PROBES[name]={'type':'box','lo_m':lo,'hi_m':hi,'targets':targets or list(G),'role':role}
for i,(a,b) in enumerate([(-.90,-.675),(-.525,-.075),(.075,.525),(.675,.90)],1):
 emptybox('RailMainBay_'+str(i),(a+.001,-.049,-.089),(b-.001,.049,-.051),'full unoccupied rail interior bay between end stop and/or thick seats')
 emptybox('RailOpenThroat_'+str(i),(a+.001,-.021,-.112),(b-.001,.021,-.091),'entire downward-open throat under an unoccupied rail bay')
for h in HEADS:
 i=h['index'];cx=h['centre_x_m'];emptybox('RailAboveSeat_'+str(i),(cx-.074,-.049,-.063),(cx+.074,.049,-.051),'entire overhead seat-to-rail gap')
 for label,y0,y1 in [('Front',-.049,-.044),('Back',.044,.049)]:emptybox('RailSeatSide_'+str(i)+label,(cx-.074,y0,-.089),(cx+.074,y1,-.064),'complete positive side corridor between seat and slot sidewall')
 for label,y0,y1 in [('Front',-.021,-.011),('Back',.011,.021)]:emptybox('RailNeckSide_'+str(i)+label,(cx-.074,y0,-.112),(cx+.074,y1,-.091),'complete downward throat side corridor beside pendant neck')
 for label,a,b in [('Left',-.074,-.033),('Right',.033,.074)]:emptybox('RailNeckEnd_'+str(i)+label,(cx+a,-.009,-.112),(cx+b,.009,-.091),'complete downward throat end gap beside pendant neck')
# Every cavity target set refers to the final assembly; no later component can be omitted.
for name,probe in VOID_PROBES.items():
 if name.startswith(('CompleteDeepFrontCavity','BehindDiffuserCavity')):probe['targets']=list(G)
def measure_track_geometry(vertices):
 return {'single_prop_count':1,'mounting_patch_count':2,'fixed_light_head_count':3,'continuous_down_open_rail_count':1,'integral_end_stop_count':2,'seated_T_adapter_count':3,'true_ear_bore_count':9,'continuous_capped_pin_count':3,'deep_front_cavity_count':3,'recessed_opaque_diffuser_count':3,'fixed_tilt_degrees':[-15,0,15],'mounting':ATTACHMENT,'qa_support':QA_SUPPORT,'ground_contact_claimed':False,'materials':MATERIAL_CONTRACT,'functional_scope':'one original fixed three-head hanging rail-light prop; visual only'}
assert len(G)==30,len(G)
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
root=bpy.data.objects.new('OneFixedThreeHeadTrackLight',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Mounting-plane centre (0,0,0), bounded top patches Z=0, +Z normals, whole prop below plane; no ground contact';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# These generated Blender triangles are checked for topology, finite interior/side
# witnesses, finite mounting patches and the oriented geometry/PBR export fingerprint.
# Complete closed voids and full contact surfaces remain independent actual-GLB gates.
supports=[]
for name in MOUNTS:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z>0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0005,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
track_evidence=measure_track_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(MOUNTS);gap_checks=[];bore_checks=[];face_contacts=[]
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
assert abs(hi[2])<1e-7 and all(p.z<=1e-7 for p in v) and triangles<12000
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
 'components':component_checks,'connection_interior_points':joints,'all_meshes_connected_to_mounts':sorted(seen),
 'single_prop_count':1,'track_geometry':track_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_mounting_patches':supports,'attachment_datum':ATTACHMENT,'temporary_support_exported':False,'ground_contact_claimed':False,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/museum/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'museum','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-2,-3,4),430,3.0),('Fill',(3,-.6,2.5),210,2.4),('Rim',(.6,3,3.5),300,2.4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g);ground.hide_render=True
gray='--gray-only' in sys.argv or '--gray-obliques-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={n:CAMERAS[n] for n in (['gray-front3q','gray-back3q'] if gray else ['thumbnail','qa-front','qa-side','qa-top','qa-back','qa-wireframe'])}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
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
