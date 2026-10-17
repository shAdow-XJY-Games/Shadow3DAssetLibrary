"""Original S01 static short passenger minibus. Metres; source Z up; front -Y.
Ground root (0,0,0); four finite tyre facets at Z0. Three paired passenger rows
and a separate driver seat have actual supports joined to the cabin floor. The
right-front entry has an integral two-tread fixed staircase. Side, front and rear
window apertures are honestly open: no opaque fake glazing and no glass claimed.
One static parked pose. No door leaf, animation, driving, passenger simulation,
roadworthiness, accessibility, engineering or precise station compatibility.
No external inputs. Every render uses a fresh import of the exact exported GLB.
"""
import bpy,bmesh,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='transport-passenger-minibus-01';VERSION='1.0.0';TITLE='Open-window Passenger Minibus'
DESCRIPTION=('Original S01 static short passenger minibus with a genuine hollow cabin, three paired passenger '
 'seat rows, separate driver seat and fixed steering visual, open window apertures, right-front entry and integral '
 'two-tread fixed stair. Every seat pedestal joins the floor; four flat-facet tyres join fixed hubs, axles and chassis. '
 'Metre scale, source Z up, front -Y, ground origin under the body centre. Five solid PBR materials and named editable '
 'closed components. Window apertures are intentionally open with no glass or opaque glazing. One parked visual prop, '
 'without door leaf, animation, driving, passenger capacity certification, navigation, collision, roadworthiness, '
 'accessibility, load, engineering, physics or exact station compatibility claims.')
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
root=bpy.data.objects.new('PassengerMinibus',None);scene.collection.objects.link(root)
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
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.445,depth=2.3,location=(0,y,.36),rotation=(0,math.pi/2,0))
 cutter=bpy.context.object;bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('Actual wheel arch opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # Boolean output remains a closed volume. Normal and triangulation checks below cover it.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
def roof_pillar(name,side,y0,z0,y1,z1):
 # Closed diagonal rectangular prism; actual overlap with apron and roof header.
 dy,dz=y1-y0,z1-z0;length=math.hypot(dy,dz);ny,nz=dz/length*.045,-dy/length*.045
 return prism_x(name,side*.89-.045,side*.89+.045,[(y0-ny,z0-nz),(y1-ny,z1-nz),(y1+ny,z1+nz),(y0+ny,z0+nz)],1,'fixed sloping front roof pillar')
# Underframe and floor. The real right entry notch is cut into the floor outline.
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Chassis_'+label,(side*.53,0,.63),(.11,4.20,.12),2,'continuous supporting longitudinal chassis rail',.005)
for y,label in [(-1.62,'Front'),(0,'Middle'),(1.48,'Rear')]:
 box('FloorBearer_'+label,(0,y,.72),(1.72 if label=='Middle' else 1.58,.14,.14),2,'cross bearer overlaps both chassis rails and floor',.004)
# Re-entrant right edge leaves a genuine stair well rather than steps ending at a solid slab.
xy=[(-.86,-2.08),(.86,-2.08),(.86,-1.035),(.40,-1.035),(.40,-.225),(.86,-.225),(.86,2.18),(-.86,2.18)]
n=len(xy);vs=[(x,y,z) for z in [.73,.81] for x,y in xy]
fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
mesh('CabinFloor_RealEntryNotch',vs,fs,2,'one closed floor with real re-entrant stair notch')
# Side lower shells have actual wheel-arch voids. No solid box fills the passenger cabin.
for side,label in [(-1,'Left'),(1,'Right')]:
 spans=[(-2.18,2.20,'Full')] if side<0 else [(-2.18,-1.03,'Front'),(-.23,2.20,'Rear')]
 for ya,yb,seg in spans:
  o=box('LowerSide_'+label+'_'+seg,(side*.89,(ya+yb)/2,.93),(.10,yb-ya,.74),0,'thick lower side shell with actual wheel openings',.008)
  for wy in [-1.62,1.48]:
   if ya-.445<wy<yb+.445:arch_cut(o,wy)
 # Upper window rhythm comprises real open apertures, with no dark sheets across them.
 ys=[-1.03,-.23,.56,1.36,2.17]
 for i,y in enumerate(ys):
  bottom=.77 if side>0 and y in [-1.03,-.23] else 1.24
  box('WindowPillar_'+label+'_'+str(i),(side*.89,y,(bottom+2.20)/2),(.12,.085,2.20-bottom),1,'closed window pillar joining body sill and roof',.004)
 box('UpperRail_'+label,(side*.89,.175,2.14),(.11,4.05,.12),1,'continuous side-window upper rail tied into roof',.006)
 roof_pillar('WindshieldPillar_'+label,side,-2.055,1.26,-1.79,2.20)
# The front lower apron slopes into a genuinely open windshield, which is framed above.
prism_x('FrontApron_Sloped',-.92,.92,[(-2.20,.565),(-2.20,1.08),(-2.08,1.295),(-1.96,1.295),(-2.04,1.06),(-2.04,.565)],0,'closed low apron leaving windshield void')
box('Windshield_Header',(0,-1.80,2.13),(1.86,.13,.14),1,'full-width open windshield top frame',.008)
box('RearLowerPanel',(0,2.17,.93),(1.84,.10,.72),0,'low rear wall leaves actual open rear window',.008)
box('RearWindow_Header',(0,2.17,2.14),(1.88,.10,.10),1,'open rear-window top frame',.004)
box('Roof_ContinuousCap',(0,.185,2.225),(1.98,4.15,.15),1,'continuous opaque roof supported by window pillars',.035)
# One closed connected zigzag stair has two visible treads, risers, and a short top landing.
stair=[(1.21,.255),(1.21,.345),(.83,.345),(.83,.585),(.51,.585),(.51,.805),(.38,.805),(.38,.735),(.435,.735),(.435,.510),(.755,.510),(.755,.255)]
prism_y('EntryStair_IntegralTwoTreads',-1.02,-.24,stair,2,'actual fixed two-tread stair joins notched floor; not ground supported')
for y,label in [(-.94,'Front'),(-.32,'Rear')]:
 box('StairBracket_'+label,(.65,y,.63),(.33,.075,.08),2,'fixed bracket overlaps stair riser and right chassis rail',.003)
# Seven individual seats: three paired passenger rows and one driver. Every pedestal intersects the floor and cushion.
seat_specs=[]
for row,y in enumerate([.02,.82,1.62],1):
 for side,label in [(-1,'Left'),(1,'Right')]:seat_specs.append(('PassengerSeat_Row'+str(row)+'_'+label,side*.50,y))
seat_specs.append(('DriverSeat',-.50,-1.20))
for name,x,y in seat_specs:
 box(name+'_Pedestal',(x,y,.98),(.12,.28,.38),2,'fixed seat pedestal joined to floor and cushion',.004)
 box(name+'_Cushion',(x,y,1.16),(.54,.52,.12),4,'closed upholstered cushion with actual pedestal support',.015)
 box(name+'_Back',(x,y+.22,1.48),(.50,.10,.65),4,'closed backrest joined directly into cushion',.018)
box('Dashboard_Fixed',(0,-1.94,1.235),(1.72,.28,.14),3,'fixed dashboard embedded in front apron',.010)
cylinder('SteeringColumn_Fixed',(-.50,-1.58,1.095),.028,.61,2,'fixed steering column joined to floor and cross spokes',axis='Z',n=12)
ring_z('SteeringWheel_OpenRing',(-.50,-1.58,1.38),.20,.15,.035,3,'fixed horizontal steering-wheel visual with true open centre',n=16)
box('SteeringSpoke_X',(-.50,-1.58,1.38),(.35,.035,.027),3,'fixed spoke joins steering ring and column',.002)
box('SteeringSpoke_Y',(-.50,-1.58,1.38),(.035,.35,.023),3,'fixed spoke joins steering ring and column',.002)
# Axles, support hangers and closed annular tyres with genuine flat contact facets.
for y,axle in [(-1.62,'Front'),(1.48,'Rear')]:
 cylinder('Axle_'+axle,(0,y,.36),.04,1.94,2,'fixed transverse axle along X')
 for side,label in [(-1,'Left'),(1,'Right')]:
  suffix=axle+'_'+label
  box('AxleHanger_'+suffix,(side*.53,y,.48),(.10,.12,.26),2,'fixed hanger joins axle and longitudinal chassis',.004)
  centre=(side*.91,y,.36);n=16;vs=[]
  for xx,rr in [(centre[0]-.10,.36/math.cos(math.pi/n)),(centre[0]+.10,.36/math.cos(math.pi/n)),(centre[0]+.10,.16),(centre[0]-.10,.16)]:
   vs.extend((xx,y+rr*math.sin(i*math.tau/n+math.pi/n),.36+rr*math.cos(i*math.tau/n+math.pi/n)) for i in range(n))
  fs=[(k*n+i,k*n+(i+1)%n,((k+1)%4)*n+(i+1)%n,((k+1)%4)*n+i) for k in range(4) for i in range(n)]
  mesh('Tyre_'+suffix+'_FlatContact',vs,fs,3,'closed annular tyre with finite horizontal ground facet',origin=centre)
  cylinder('Hub_'+suffix,centre,.169,.22,2,'fixed solid hub joins tyre bore and axle')
  # Outside arch bead overlaps the cut side-shell boundary and stays clear of the tyre.
  xa,xb=sorted((side*.88,side*1.015));n=17;vs=[]
  for x,r in [(xa,.438),(xb,.438),(xb,.483),(xa,.483)]:
   vs.extend((x,y+r*math.cos(i*math.pi/(n-1)),.36+r*math.sin(i*math.pi/(n-1))) for i in range(n))
  fs=[(k*n+i,k*n+i+1,((k+1)%4)*n+i+1,((k+1)%4)*n+i) for k in range(4) for i in range(n-1)]
  fs += [(0,n,2*n,3*n),(n-1,4*n-1,3*n-1,2*n-1)]
  mesh('WheelArchLip_'+suffix,vs,fs,0,'closed fixed half-arch bead joined to side shell with tyre clearance')
# Restrained vehicle cues, without text decals or operational lamp promises.
for y,label in [(-2.21,'Front'),(2.20,'Rear')]:
 box('Bumper_'+label,(0,y,.60),(1.98,.17,.15),3,'fixed bumper penetrates lower body panel',.018)
for side,label in [(-1,'Left'),(1,'Right')]:
 box('Headlamp_'+label,(side*.61,-2.205,.96),(.27,.045,.16),1,'fixed ivory front lamp face, no emission',.009)
 box('RearMarker_'+label,(side*.70,2.222,1.01),(.13,.035,.18),4,'fixed ochre rear marker, no emission',.006)
box('FrontGrille',(0,-2.205,.78),(.70,.04,.12),3,'closed grille-colour inset visual; no cooling function',.004)
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
# Exact interior overlap witnesses establish the critical support paths, not bounding-box proximity.
for side,label in [(-1,'Left'),(1,'Right')]:
 for y,axle in [(-1.62,'Front'),(1.48,'Rear')]:
  suffix=axle+'_'+label
  joint('Chassis_'+label,'FloorBearer_'+axle,[(side*.53,y+d,.67) for d in [-.02,0,.02]])
  joint('Chassis_'+label,'AxleHanger_'+suffix,[(side*.53,y+d,.59) for d in [-.02,0,.02]])
  joint('AxleHanger_'+suffix,'Axle_'+axle,[(side*(.52+d),y,.37) for d in [0,.01,.02]])
  joint('Axle_'+axle,'Hub_'+suffix,[(side*(.88+d),y,.36) for d in [0,.02,.04]])
  joint('Hub_'+suffix,'Tyre_'+suffix+'_FlatContact',[(side*(.88+d),y+.163,.36) for d in [0,.02,.04]])
 for y,label2 in [(-1.62,'Front'),(0,'Middle'),(1.48,'Rear')]:
  joint('FloorBearer_'+label2,'CabinFloor_RealEntryNotch',[(side*.53,y+d,.76) for d in [-.02,0,.02]])
for name,x,y in seat_specs:
 joint(name+'_Pedestal','CabinFloor_RealEntryNotch',[(x+d,y,.80) for d in [-.02,0,.02]])
 joint(name+'_Pedestal',name+'_Cushion',[(x+d,y,1.13) for d in [-.02,0,.02]])
 joint(name+'_Cushion',name+'_Back',[(x+d,y+.22,1.19) for d in [-.10,0,.10]])
joint('EntryStair_IntegralTwoTreads','CabinFloor_RealEntryNotch',[(.39,y,.775) for y in [-.8,-.63,-.45]])
for y,label in [(-.94,'Front'),(-.32,'Rear')]:
 joint('StairBracket_'+label,'Chassis_Right',[(.53,y+d,.64) for d in [-.01,0,.01]])
 joint('StairBracket_'+label,'EntryStair_IntegralTwoTreads',[(.495,y+d,.64) for d in [-.01,0,.01]])
for name,x,y in [('LowerSide_Left_Full',-.85,.80),('LowerSide_Right_Front',.85,-1.96),('LowerSide_Right_Rear',.85,.80)]:
 joint(name,'CabinFloor_RealEntryNotch',[(x,y+d,.77) for d in [-.01,0,.01]])
joint('FrontApron_Sloped','CabinFloor_RealEntryNotch',[(x,-2.06,.77) for x in [-.40,0,.40]])
joint('RearLowerPanel','CabinFloor_RealEntryNotch',[(x,2.15,.77) for x in [-.40,0,.40]])
joint('Dashboard_Fixed','FrontApron_Sloped',[(x,-2.04,1.25) for x in [-.40,0,.40]])
joint('SteeringColumn_Fixed','CabinFloor_RealEntryNotch',[(-.50+d,-1.58,.80) for d in [-.01,0,.01]])
joint('SteeringColumn_Fixed','SteeringSpoke_X',[(-.50+d,-1.58,1.38) for d in [-.01,0,.01]])
for side,label in [(-1,'Left'),(1,'Right')]:
 joint('UpperRail_'+label,'Roof_ContinuousCap',[(side*.89,y,2.18) for y in [-1.5,0,1.5]])
 for i,y in enumerate([-1.03,-.23,.56,1.36,2.17]):
  joint('WindowPillar_'+label+'_'+str(i),'UpperRail_'+label,[(side*.89,y+d,2.15) for d in [-.01,0,.01]])
# Actual complete assembly rays verify a clear aisle and an honest hollow passenger volume.
ray_checks=[]
def first_hit(origin,direction,distance):
 hits=[]
 for name,tree in trees.items():
  q,n,_,d=tree.ray_cast(Vector(origin),Vector(direction),distance)
  if q is not None:hits.append((d,name,q,n))
 return min(hits,key=lambda h:h[0]) if hits else None
for x in [-.17,0,.17]:
 hit=first_hit((x,-.85,1.50),(0,1,0),2.9);assert hit is None,('Aisle blocked',x,hit)
 hit=first_hit((x,.8,1.0),(0,0,-1),.5);assert hit and hit[1]=='CabinFloor_RealEntryNotch' and abs(hit[2].z-.81)<1e-6
 ray_checks.append({'type':'longitudinal_clear_aisle','x_m':x,'y_range_m':[-.85,2.05],'z_m':1.50})
for y in [.42,1.22,2.02]:
 hit=first_hit((1.3,y,1.95),(-1,0,0),2.60);assert hit is None,('Window void blocked',y,hit)
 ray_checks.append({'type':'open_side_window_through_cabin','y_m':y,'z_m':1.95})
for x,z,expected in [(1.06,.8,.345),(.68,1.0,.585),(.45,1.0,.805)]:
 hit=first_hit((x,-.63,z),(0,0,-1),1.0)
 assert hit and hit[1]=='EntryStair_IntegralTwoTreads' and abs(hit[2].z-expected)<1e-6,('Stair top',x,hit)
 ray_checks.append({'type':'stair_surface','x_m':x,'y_m':-.63,'top_z_m':expected})
hit=first_hit((1.3,-.63,1.6),(-1,0,0),1.4);assert hit is None,('Entry blocked',hit)
ray_checks.append({'type':'open_right_entry','y_m':-.63,'z_m':1.6,'x_range_m':[1.3,-.1]})
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
 assert not any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes),'Solid-only PBR expected'
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
 'components':component_checks,'connection_interior_points':joints,'cabin_entry_aisle_and_stair_rays':ray_checks,'finite_ground_supports':supports,
 'seat_layout':{'passenger_rows':3,'seats_per_row':2,'separate_driver_seats':1,'forward_axis':'-Y','window_apertures':'open, no glazing'},
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
focus=Vector((.10,0,1.05));asset_mats={m for o in parts for m in o.data.materials}
def aim(o,pos):o.location=pos;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-4,-6,7),1200,5),('Fill',(5,-1,4),600,4),('Rim',(1,5,6),850,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=5.65;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.003));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
gray='--gray-only' in sys.argv
if gray:
 for m in asset_mats:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.50,.50,.50,1)
views={'gray-front3q':(6,-8,4.3),'gray-back3q':(-6,7,4.3)} if gray else {
 'thumbnail':(6,-8,4.3),'qa-front':(0,-8,1.05),'qa-side':(8,0,1.05),'qa-top':(.10,0,9),
 'qa-back':(0,8,1.05),'qa-wireframe':(6,-8,4.3)}
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
