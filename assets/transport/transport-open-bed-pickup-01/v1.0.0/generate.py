"""Original S01 static open-bed utility pickup; metres, source Z up, front -Y.
Independent two-seat cabin with genuinely open window apertures and no glazing.
Cargo bed is a separate empty, open-top low-walled tub with a fixed closed tailgate.
Four actual finite contact tyre facets at Z=0; every main component is supported.
No animation, driving, door/tailgate movement, cargo/load, engineering or road claim.
Standalone source; renders import and fingerprint the exact exported GLB.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='transport-open-bed-pickup-01';VERSION='1.0.0';TITLE='Open-bed Utility Pickup'
DESCRIPTION=('Original S01 static utility pickup with a genuinely separate two-seat cab and open-top empty cargo bed. '
 'Cabin has actual open window apertures, supported seats, dashboard and a fixed steering visual; no glazing is claimed. '
 'The low-walled bed has a real interior floor, front bulkhead and fixed closed tailgate. Four finite-contact tyres, '
 'hubs, axles, hangers, chassis rails and floor bearers form actual support chains. Metre scale, source Z up, '
 'front -Y, origin at ground under the wheelbase centre. Five solid PBR materials and named editable closed components. '
 'One fixed parked visual prop; no driving, steering, opening tailgate or doors, animation, cargo capacity, '
 'loading fit, roadworthiness, collision, physics, stability, load or engineering certification.')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials):bpy.data.materials.remove(m)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.seed=17
scene.cycles.use_adaptive_sampling=False;scene.cycles.use_denoising=False
for vl in scene.view_layers:vl.cycles.use_denoising=False
scene.use_nodes=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
EXPECTED={'engine':'CYCLES','samples':128,'adaptive':False,'cycles_denoise':False,'view_layer_denoise':[False],
 'compositor_nodes':False,'compositing':False,'threads_mode':'FIXED','threads':4}
def config():
 return {'engine':scene.render.engine,'samples':scene.cycles.samples,'adaptive':scene.cycles.use_adaptive_sampling,
 'cycles_denoise':scene.cycles.use_denoising,'view_layer_denoise':[v.cycles.use_denoising for v in scene.view_layers],
 'compositor_nodes':scene.use_nodes,'compositing':scene.render.use_compositing,'threads_mode':scene.render.threads_mode,'threads':scene.render.threads}
def guard():
 c=config();assert c==EXPECTED,c;return c
mats=[]
for name,color,rough,metal in [('Seafoam_PaintedBody',(.235,.47,.405,1),.68,.06),
 ('WarmIvory_RoofAndLamps',(.78,.75,.63,1),.70,.02),('WarmGrey_FixedMetal',(.34,.37,.36,1),.58,.42),
 ('Charcoal_TyresAndControls',(.035,.043,.042,1),.88,0),('Ochre_SeatsAndMarkers',(.56,.30,.12,1),.80,0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 mats.append(m)
root=bpy.data.objects.new('OpenBedUtilityPickup',None);scene.collection.objects.link(root)
root['asset_id']=ASSET;root['front_axis']='-Y';root['static_parked_visual_only']=True
root['window_apertures']='intentionally open, no glazing';root['render_contract']=json.dumps(guard(),sort_keys=True)
parts=[];byname={}
def mesh(name,vs,fs,material,role,origin=(0,0,0),bevel=0):
 origin=Vector(origin);me=bpy.data.meshes.new(name);me.from_pydata([Vector(v)-origin for v in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.parent=root;o.location=origin
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 me.materials.append(mats[material]);o['component_role']=role;parts.append(o);byname[name]=o
 if bevel:
  bpy.context.view_layer.objects.active=o;b=o.modifiers.new('Restrained manufactured chamfer','BEVEL');b.width=bevel;b.segments=1
  bpy.ops.object.modifier_apply(modifier=b.name)
 for f in me.polygons:f.use_smooth=False
 return o
def box(name,loc,size,material,role,bevel=.003):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 fs=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return mesh(name,vs,fs,material,role,loc,bevel)
def ring_z(name,center,r_outer,r_inner,depth,material,role,n=16):
 x,y,z=center;vs=[]
 for zz,rr in [(z-depth/2,r_outer),(z+depth/2,r_outer),(z+depth/2,r_inner),(z-depth/2,r_inner)]:
  vs.extend((x+rr*math.cos(i*math.tau/n),y+rr*math.sin(i*math.tau/n),zz) for i in range(n))
 fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def cylinder(name,center,radius,depth,material,role,axis='X',n=16):
 x,y,z=center;vs=[]
 for d in [-depth/2,depth/2]:
  for i in range(n):
   a=i*math.tau/n+math.pi/n;u=radius*math.sin(a);v=radius*math.cos(a)
   vs.append((x+d,y+u,z+v) if axis=='X' else (x+u,y+v,z+d))
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 return mesh(name,vs,fs,material,role,center)
def beam_xy(name,a,b,width,height,material,role):
 a,b=Vector(a),Vector(b);t=(b-a).normalized();n=Vector((-t.y,t.x,0));vs=[]
 for p in [a,b]:
  for z in [-height/2,height/2]:
   for side in [-1,1]:vs.append(p+n*side*width/2+Vector((0,0,z)))
 fs=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
 return mesh(name,vs,fs,material,role,(a+b)/2)
def prism_x(name,x0,x1,yz,material,role):
 n=len(yz);vs=[(x,y,z) for x in [x0,x1] for y,z in yz]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role)
def prism_y(name,y0,y1,xz,material,role):
 n=len(xz);vs=[(x,y,z) for y in [y0,y1] for x,z in xz]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,material,role)
def arch_cut(o,y):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.435,depth=2.3,location=(0,y,.35),rotation=(0,math.pi/2,0))
 cutter=bpy.context.object;bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('Actual wheel arch opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # Boolean output remains a closed volume. Normal and triangulation checks below cover it.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
def roof_pillar(name,side,y0,z0,y1,z1):
 dy,dz=y1-y0,z1-z0;length=math.hypot(dy,dz);ny,nz=dz/length*.048,-dy/length*.048
 return prism_x(name,side*.89-.05,side*.89+.05,[(y0-ny,z0-nz),(y1-ny,z1-nz),(y1+ny,z1+nz),(y0+ny,z0+nz)],1,'sloping solid A pillar joining sill and roof')
# Original pickup underframe. Front and rear axle centres are equidistant from the ground root.
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Chassis_'+label,(side*.52,0,.605),(.12,4.28,.13),2,'continuous load-path visual rail',.006)
for y,label in [(-1.45,'Front'),(-.30,'Cab'),(.65,'BedFront'),(1.45,'Rear'),(2.03,'BedRear')]:
 box('FloorBearer_'+label,(0,y,.73),(1.48,.13,.19),2,'transverse bearer joining both rails and upper floor',.004)
box('CabFloor',(0,-.395,.775),(1.76,1.61,.11),2,'closed cabin floor, upper surface at 0.83 m',.006)
box('BedFloor',(0,1.37,.84),(1.76,1.64,.08),0,'closed cargo bed floor, actual empty interior top 0.88 m',.006)
# The long tapered lower front shell is NOT a single solid cab block: its interior is open.
for side,label in [(-1,'Left'),(1,'Right')]:
 o=prism_x('CabLowerSide_'+label,side*.89-.06,side*.89+.06,
   [(-2.12,.55),(-2.12,1.085),(-1.18,1.25),(.42,1.25),(.42,.55)],0,'closed tapered lower cab side with actual front wheel opening')
 arch_cut(o,-1.45)
 # Side-window aperture is open between this lower sill, the A pillar, rear pillar and roof.
 roof_pillar('CabAPillar_'+label,side,-1.18,1.22,-.88,1.98)
 box('CabRearPillar_'+label,(side*.89,.36,1.61),(.10,.08,.80),1,'rear cabin roof pillar tied into sill and cap',.006)
 box('CabUpperRail_'+label,(side*.89,-.26,1.96),(.115,1.38,.10),1,'side-window upper roof rail',.006)
 # Low cargo sides retain substantial air above the empty bed; true rear wheel openings below the floor.
 o=box('BedSide_'+label,(side*.89,1.37,.94),(.12,1.66,.78),0,'low cargo side with real rear wheel-arch opening',.010)
 arch_cut(o,1.45)
# Front panels and hood have their own depths and bevels; no coplanar decorative sheets.
box('FrontApron',(0,-2.075,.825),(1.80,.11,.54),0,'front lower closed apron supporting bumper and lamps',.008)
prism_x('Hood_ClosedSlopedDeck',-.87,.87,[(-2.11,1.08677),(-1.16,1.255),(-1.16,1.145),(-2.11,.97677)],0,'closed sloping bonnet deck, visibly separate from cab void')
box('CabFrontBulkhead',(0,-1.155,1.025),(1.76,.10,.43),0,'solid lower firewall joins floor and dashboard',.006)
box('CabRearLowerWall',(0,.36,1.0325),(1.77,.09,.425),0,'low rear cab wall below actual open rear window',.006)
box('CabWindshieldHeader',(0,-.875,1.97),(1.86,.14,.11),1,'windshield open aperture upper frame',.007)
box('CabRearHeader',(0,.36,1.965),(1.86,.12,.12),1,'rear-window open aperture upper frame',.006)
box('CabRoof_IndependentCap',(0,-.265,2.005),(1.98,1.42,.13),1,'opaque roof over cabin only, stops before separate cargo bed',.024)
# Cargo bulkhead and fixed closed tailgate terminate below side-wall top, avoiding exposed coplanar top overlaps.
box('BedFrontBulkhead',(0,.59,1.055),(1.78,.12,.50),0,'bed front wall physically separate from cab rear wall',.008)
box('Tailgate_FixedClosed',(0,2.15,1.045),(1.78,.12,.48),0,'fixed closed rear cargo wall; no moving tailgate promise',.008)
box('Tailgate_Handle',(0,2.212,1.165),(.30,.045,.055),3,'fixed attached rear grip visual',.006)
# Two separately supported seats, with backs meeting cushions on buried lower interfaces.
seat_specs=[('DriverSeat',-.46,-.29),('PassengerSeat',.46,-.29)]
for name,x,y in seat_specs:
 box(name+'_Pedestal',(x,y,.96),(.14,.26,.30),2,'pedestal intersects floor and cushion',.004)
 box(name+'_Cushion',(x,y,1.105),(.55,.56,.12),4,'closed fixed cushion with actual pedestal support',.014)
 box(name+'_Back',(x,y+.235,1.405),(.50,.105,.63),4,'closed seat back overlaps cushion below its top',.015)
box('Dashboard_Fixed',(0,-1.07,1.21),(1.72,.25,.14),3,'fixed dashboard overlaps front firewall',.009)
cylinder('SteeringColumn_Fixed',(-.46,-.78,1.06),.03,.49,2,'column penetrates cab floor and spokes',axis='Z',n=12)
ring_z('SteeringWheel_OpenRing',(-.46,-.78,1.30),.195,.145,.04,3,'fixed steering visual with real open centre',n=16)
box('SteeringSpoke_X',(-.46,-.78,1.30),(.34,.035,.027),3,'spoke joins ring and column',.002)
box('SteeringSpoke_Y',(-.46,-.78,1.296),(.035,.34,.024),3,'second steering spoke with offset top plane',.002)
# Honest fixed mirrors and door handles, grounded by explicit solid arms.
for side,label in [(-1,'Left'),(1,'Right')]:
 box('DoorHandle_'+label,(side*.965,.17,1.13),(.065,.17,.045),3,'fixed solid door grip attached to lower cab shell',.005)
 box('MirrorArm_'+label,(side*1.005,-1.12,1.335),(.24,.045,.05),2,'mirror arm joined to front pillar base',.004)
 box('MirrorHousing_'+label,(side*1.12,-1.12,1.395),(.075,.17,.18),3,'solid fixed mirror housing, no reflection material claim',.009)
# Tyres use a 16-sided annular closed ring with a finite horizontal bottom contact facet.
for y,axle in [(-1.45,'Front'),(1.45,'Rear')]:
 cylinder('Axle_'+axle,(0,y,.35),.045,1.94,2,'fixed transverse axle along X')
 for side,label in [(-1,'Left'),(1,'Right')]:
  suffix=axle+'_'+label
  box('AxleHanger_'+suffix,(side*.52,y,.475),(.10,.13,.29),2,'fixed hanger joins axle and longitudinal chassis',.005)
  centre=(side*.89,y,.35);n=16;vs=[]
  for xx,rr in [(centre[0]-.105,.35/math.cos(math.pi/n)),(centre[0]+.105,.35/math.cos(math.pi/n)),(centre[0]+.105,.16),(centre[0]-.105,.16)]:
   vs.extend((xx,y+rr*math.sin(i*math.tau/n+math.pi/n),.35+rr*math.cos(i*math.tau/n+math.pi/n)) for i in range(n))
  fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
  mesh('Tyre_'+suffix+'_FlatContact',vs,fs,3,'closed annular tyre, real flat contact facet at Z0',origin=centre)
  cylinder('Hub_'+suffix,centre,.169,.232,2,'fixed solid hub joins tyre bore and axle')
  xa,xb=sorted((side*.88,side*1.025));n=17;vs=[]
  for x,r in [(xa,.429),(xb,.429),(xb,.478),(xa,.478)]:
   vs.extend((x,y+r*math.cos(i*math.pi/(n-1)),.35+r*math.sin(i*math.pi/(n-1))) for i in range(n))
  fs=[(k*n+i,k*n+i+1,((k+1)%4)*n+i+1,((k+1)%4)*n+i) for k in range(4) for i in range(n-1)]
  fs += [(0,n,2*n,3*n),(n-1,4*n-1,3*n-1,2*n-1)]
  mesh('WheelArchLip_'+suffix,vs,fs,0,'closed arch lip tied to shell, clear of actual tyre')
# Restrained attached lamp and bumper shapes; no text, badges, cargo or extra scene props.
for y,label in [(-2.155,'Front'),(2.17,'Rear')]:
 box('Bumper_'+label,(0,y,.61),(1.98,.18,.15),3,'fixed bumper joined to body through dedicated brackets',.016)
 for side,slabel in [(-1,'Left'),(1,'Right')]:
  box('BumperBracket_'+label+'_'+slabel,(side*.52,y*.95,.61),(.13,.30,.09),2,'fixed bumper bracket intersects chassis and bumper',.004)
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Headlamp_'+label,(side*.62,-2.135,.94),(.27,.045,.14),1,'non-emissive ivory front lamp',.008)
 box('RearMarker_'+label,(side*.73,2.214,1.02),(.12,.040,.18),4,'non-emissive ochre rear marker',.006)
box('FrontGrille',(0,-2.136,.76),(.70,.045,.13),3,'closed grille-colour inset visual',.005)
bpy.context.view_layer.update();triangles=0;component_checks=[];trees={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 o.data.calc_loop_triangles();deg=sum(t.area<1e-12 for t in o.data.loop_triangles)
 assert bad==0 and vol>1e-9 and deg==0,(o.name,bad,vol,deg)
 triangles+=len(o.data.loop_triangles);component_checks.append({'name':o.name,'triangles':len(o.data.loop_triangles),'signed_volume_m3':vol,'nonmanifold_edges':bad,'degenerate_triangles':deg})
 trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True)
def inside(tree,point):
 votes=[]
 for direction in [(1,.371,.529),(.263,1,.619),(.419,.233,1)]:
  p=Vector(point);d=Vector(direction).normalized();hits=0
  for _ in range(64):
   q,_,_,_=tree.ray_cast(p,d,20)
   if q is None:break
   hits+=1;p=q+d*1e-5
  else:raise AssertionError('Uncertain ray parity')
  votes.append(bool(hits%2))
 return all(votes)
joints=[]
def joint(a,b,points):
 rows=[]
 for p in points:
  clearance=min(trees[a].find_nearest(Vector(p))[3],trees[b].find_nearest(Vector(p))[3])
  passed=inside(trees[a],p) and inside(trees[b],p) and clearance>.0001
  assert passed,(a,b,p,clearance)
  rows.append({'world_point_m':p,'minimum_interior_clearance_m':clearance})
 joints.append({'a':a,'b':b,'interior_overlap_points':rows})
# Interior witnesses are points strictly inside BOTH actual meshes, not bounding box overlap.
for side,label in [(-1,'Left'),(1,'Right')]:
 for y,axle in [(-1.45,'Front'),(1.45,'Rear')]:
  suffix=axle+'_'+label
  joint('Chassis_'+label,'AxleHanger_'+suffix,[(side*.52,y+d,.59) for d in [-.02,0,.02]])
  joint('AxleHanger_'+suffix,'Axle_'+axle,[(side*(.51+d),y,.37) for d in [0,.01,.02]])
  joint('Axle_'+axle,'Hub_'+suffix,[(side*(.87+d),y,.35) for d in [0,.02,.04]])
  joint('Hub_'+suffix,'Tyre_'+suffix+'_FlatContact',[(side*(.87+d),y+.163,.35) for d in [0,.02,.04]])
  shell='CabLowerSide_'+label if axle=='Front' else 'BedSide_'+label
  joint('WheelArchLip_'+suffix,shell,[(side*.91,y+d,.80) for d in [-.01,0,.01]])
 for y,which in [(-1.45,'Front'),(-.30,'Cab'),(.65,'BedFront'),(1.45,'Rear'),(2.03,'BedRear')]:
  joint('Chassis_'+label,'FloorBearer_'+which,[(side*.52,y+d,.655) for d in [-.02,0,.02]])
 for y,which in [(-.30,'Cab')]:
  joint('FloorBearer_'+which,'CabFloor',[(side*.52,y+d,.76) for d in [-.02,0,.02]])
 for y,which in [(.65,'BedFront'),(1.45,'Rear'),(2.03,'BedRear')]:
  joint('FloorBearer_'+which,'BedFloor',[(side*.52,y+d,.81) for d in [-.02,0,.02]])
 joint('CabLowerSide_'+label,'CabFloor',[(side*.855,y,.78) for y in [-.7,-.3,.1]])
 joint('BedSide_'+label,'BedFloor',[(side*.855,y,.84) for y in [.8,1.1,1.8]])
 joint('CabLowerSide_'+label,'Hood_ClosedSlopedDeck',[(side*.85,y,z) for y,z in [(-1.9,1.06),(-1.7,1.09),(-1.3,1.16)]])
 joint('CabLowerSide_'+label,'CabAPillar_'+label,[(side*.89,-1.18+d,1.23) for d in [-.01,0,.01]])
 joint('CabAPillar_'+label,'CabWindshieldHeader',[(side*.89+d,-.89,1.96) for d in [-.01,0,.01]])
 joint('CabLowerSide_'+label,'CabRearPillar_'+label,[(side*.89,.36+d,1.23) for d in [-.01,0,.01]])
 joint('CabRearPillar_'+label,'CabUpperRail_'+label,[(side*.89,.36+d,1.96) for d in [-.01,0,.01]])
 joint('CabUpperRail_'+label,'CabRoof_IndependentCap',[(side*.89,y,1.98) for y in [-.8,-.2,.3]])
 joint('DoorHandle_'+label,'CabLowerSide_'+label,[(side*.942,.17+d,1.13) for d in [-.02,0,.02]])
 joint('MirrorArm_'+label,'CabAPillar_'+label,[(side*.91,-1.12+d,1.34) for d in [-.005,0,.005]])
 joint('MirrorArm_'+label,'MirrorHousing_'+label,[(side*1.10,-1.12+d,1.345) for d in [-.01,0,.01]])
 for y,label2 in [(-2.155,'Front'),(2.17,'Rear')]:
  bn='BumperBracket_'+label2+'_'+label
  joint(bn,'Chassis_'+label,[(side*.52,y*.95+d,.61) for d in [-.02,0,.02]])
  joint(bn,'Bumper_'+label2,[(side*.52,y+d,.61) for d in [-.02,0,.02]])
for name,x,y in seat_specs:
 joint(name+'_Pedestal','CabFloor',[(x+d,y,.82) for d in [-.02,0,.02]])
 joint(name+'_Pedestal',name+'_Cushion',[(x+d,y,1.09) for d in [-.02,0,.02]])
 joint(name+'_Cushion',name+'_Back',[(x+d,y+.235,1.13) for d in [-.12,0,.12]])
for name,y in [('CabFrontBulkhead',-1.155),('CabRearLowerWall',.36)]:
 joint(name,'CabFloor',[(x,y,.825) for x in [-.5,0,.5]])
for name,y in [('BedFrontBulkhead',.59),('Tailgate_FixedClosed',2.15)]:
 joint(name,'BedFloor',[(x,y,.85) for x in [-.5,0,.5]])
 for side,label in [(-1,'Left'),(1,'Right')]:
  joint(name,'BedSide_'+label,[(side*.85,y,z) for z in [.90,1.0,1.2]])
joint('FrontApron','Hood_ClosedSlopedDeck',[(x,-2.06,1.06) for x in [-.5,0,.5]])
joint('Dashboard_Fixed','CabFrontBulkhead',[(x,-1.15,1.19) for x in [-.5,0,.5]])
joint('SteeringColumn_Fixed','CabFloor',[(-.46+d,-.78,.823) for d in [-.01,0,.01]])
joint('SteeringColumn_Fixed','SteeringSpoke_X',[(-.46+d,-.78,1.30) for d in [-.01,0,.01]])
joint('SteeringSpoke_X','SteeringSpoke_Y',[(-.46+d,-.78,1.299) for d in [-.01,0,.01]])
joint('SteeringSpoke_X','SteeringWheel_OpenRing',[(-.46+d,-.78,1.30) for d in [-.16,.16]])
for name,y in [('CabWindshieldHeader',-.875),('CabRearHeader',.36)]:
 joint(name,'CabRoof_IndependentCap',[(x,y,1.985) for x in [-.6,0,.6]])
joint('Tailgate_Handle','Tailgate_FixedClosed',[(x,2.20,1.165) for x in [-.10,0,.10]])
for side,label in [(-1,'Left'),(1,'Right')]:
 joint('Headlamp_'+label,'FrontApron',[(side*.62+d,-2.117,.94) for d in [-.06,0,.06]])
 joint('RearMarker_'+label,'Tailgate_FixedClosed',[(side*.73+d,2.204,1.02) for d in [-.025,0,.025]])
joint('FrontGrille','FrontApron',[(x,-2.117,.76) for x in [-.2,0,.2]])
# Complete-assembly rays demonstrate a truly empty, open-top cargo bed and visible cabin apertures.
ray_checks=[]
def first_hit(origin,direction,distance):
 hits=[]
 for name,tree in trees.items():
  q,n,_,d=tree.ray_cast(Vector(origin),Vector(direction),distance)
  if q is not None:hits.append((d,name,q,n))
 return min(hits,key=lambda h:h[0]) if hits else None
for x in [-.65,0,.65]:
 for y in [.80,1.3,1.9]:
  hit=first_hit((x,y,2.6),(0,0,-1),2.0)
  assert hit and hit[1]=='BedFloor' and abs(hit[2].z-.88)<1e-6,('Cargo bed is blocked or missing floor',x,y,hit)
  ray_checks.append({'type':'empty_open_top_bed_to_actual_floor','x_m':x,'y_m':y,'floor_z_m':.88})
for y in [-.55,-.25,.10]:
 hit=first_hit((1.4,y,1.80),(-1,0,0),2.8);assert hit is None,('Cab side window blocked',y,hit)
 ray_checks.append({'type':'open_cabin_side_window','y_m':y,'z_m':1.80})
for x in [-.25,0,.25]:
 hit=first_hit((x,-1.8,1.78),(0,1,0),2.3);assert hit is None,('Cab front/rear window blocked',x,hit)
 ray_checks.append({'type':'open_front_and_rear_cabin_windows','x_m':x,'z_m':1.78})
for x in [-.60,0,.60]:
 hit=first_hit((x,.48,2.6),(0,0,-1),1.7);assert hit is None,('Cab/bed physical gap blocked above chassis',x,hit)
 ray_checks.append({'type':'physical_cab_bed_gap','x_m':x,'y_m':.48,'z_range_m':[2.6,.9]})
supports=[]
for name in [o.name for o in parts if o.name.startswith('Tyre_')]:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  v=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cross=(v[1]-v[0]).cross(v[2]-v[0])
  if max(abs(p.z) for p in v)<1e-7 and cross.z<0:patch.append({'vertices_m':[list(p) for p in v],'area_m2':cross.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.02,(name,area)
 supports.append({'name':name,'area_m2':area,'triangles':patch})
v=[o.matrix_world@v.co for o in parts for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
bounds=[round(hi[i]-lo[i],6) for i in range(3)];assert abs(lo[2])<1e-7
def pbr(m):
 p=m.node_tree.nodes.get('Principled BSDF');assert p is not None
 assert not any(n.type.startswith('TEX_') for n in m.node_tree.nodes),'Solid-only PBR: every TEX_* node is forbidden'
 assert not any(socket.is_linked for socket in p.inputs),'Solid-only PBR: linked shader inputs are forbidden'
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
 'components':component_checks,'connection_interior_points':joints,'cargo_bed_and_cabin_void_rays':ray_checks,'finite_ground_supports':supports,
 'seat_layout':{'driver_seats':1,'passenger_seats':1,'forward_axis':'-Y','window_apertures':'open, no glazing'},
 'cargo_bed':{'empty':True,'open_top':True,'fixed_closed_tailgate':True,'floor_top_z_m':.88,'cab_bed_wall_gap_m':.11},
 'world_oriented_triangle_full_solid_pbr_sha256':source_fp,'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),
 'native_saved_render_config':guard(),'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/transport/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'transport','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
focus=Vector((0,0,.98));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.5;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(6,-8,5.0),'gray-back3q':(-6,7,5.0)} if gray else {
 'thumbnail':(6,-8,5.0),'qa-front':(0,-8,1.05),'qa-side':(8,0,1.05),'qa-top':(.10,0,9),
 'qa-back':(0,8,1.05),'qa-wireframe':(6,-8,5.0)}
if '--preview-only' in sys.argv:views={'thumbnail':views['thumbnail']}
if '--extra-views' in sys.argv:views.pop('thumbnail',None)
seconds={};configs={}
def render(name,pos):
 aim(cam,pos);scene.render.filepath=str(OUT/(name+'.png'));configs[name]=guard();t=time.time();bpy.ops.render.render(write_still=True);seconds[name]=round(time.time()-t,3)
for name,pos in views.items():
 if name=='qa-wireframe':
  wm=bpy.data.materials.new('Preview_wire');wm.diffuse_color=(.012,.018,.015,1)
  for o in parts:
   dup=o.copy();dup.data=o.data.copy();scene.collection.objects.link(dup);dup.name='Preview_wire_'+o.name;dup.data.materials.clear();dup.data.materials.append(wm)
   for f in dup.data.polygons:f.material_index=0
   w=dup.modifiers.new('Preview_actual_edges','WIREFRAME');w.thickness=.0022;w.use_replace=True;w.use_even_offset=False;w.offset=1
 render(name,pos)
if gray:
 black=bpy.data.materials.new('Preview_silhouette');black.use_nodes=True;nt=black.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(0,0,0,1);nt.links.new(em.outputs[0],out.inputs['Surface'])
 for o in parts:
  o.data.materials.clear();o.data.materials.append(black)
  for f in o.data.polygons:f.material_index=0
 ground.hide_render=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
 for name,pos in [('silhouette-128-front',(0,-8,1.05)),('silhouette-128-side',(8,0,1.05))]:render(name,pos)
qa.update({'render_seconds':seconds,'render_configs':configs,'elapsed_seconds':round(time.time()-START,3),'status':'review; independent visual/native/clean/runtime gates pending'})
if not gray:metadata()
saveqa();print('ASSET_COMPLETE',ASSET,triangles,bounds)
