"""Original four independent compartment pickup locker, one fixed static visual prop.
Native Z up, front -Y, metre coordinates. No security, motion, installation or load claim.
"""
import math,json,hashlib,sys,time,itertools
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='postal-individual-compartment-pickup-locker-01';VERSION='1.0.0';TITLE='Four-Compartment Postal Pickup Locker'
DESCRIPTION=('One original low-poly postal pickup locker, counted as one complete static prop. A unified thick cabinet shell has four genuinely isolated storage cavities in two columns and two unequal-height rows, with full backs, floors, side walls, a continuous central divider and inset front stop frames. '
 'Each compartment has a separate thick door and two independent real through-bored hinge pairs with solid headed pins. The lower-left door is frozen open by 90 degrees; the other three are fixed closed. Finite opposed annular hinge seats support every door, with clear bore air around the shafts and visible separate fixed catch blocks and simple pull tabs. Four broad finite feet connect to the shell. '
 'Named editable closed meshes and five constant opaque PBR materials; no textures, parcel, screen, authentication device, labels, room or animation. Metres, native Z up, front -Y, horizontal bounds-centred ground origin. '
 'Static visual appearance only: no pickup system, lock/security/privacy, package capacity, postal operations, opening/closing path, pin insertion, load, stability, anti-tip, human fit, installation, manufacture, accessibility, facility-standard or safety claim. No historical parcel compatibility is asserted.')
G={};LINKS=[];CONTACTS=[];FEET=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};WALL_VOLUMES={};DOORS={};HINGES=[]
PALETTE=[('Shell_PostalDeepTeal',(.035,.19,.20,1),.47,.26),('Doors_WarmOchre',(.76,.39,.065,1),.47,.22),('Hardware_BrushedSteel',(.40,.47,.49,1),.29,.73),('Feet_Graphite',(.035,.045,.047,1),.77,.0),('Pulls_Cream',(.78,.70,.49,1),.46,.15)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return[tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in[(a,b,c) for c in[0,1] for b in[0,1] for a in[0,1]]]
def mesh(name,vs,fs,material,role):
 assert name not in G
 G[name]={'vertices':[tuple(round(float(c),8) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role};return name

def box(name,c,size,mat,role):return mesh(name,cuboid(sub(c,mul(size,.5)),add(c,mul(size,.5))),BOX_FACES,mat,role)
def link(a,b,p,axis=(0,0,1),spread=.002):LINKS.append((a,b,[add(p,mul(axis,d)) for d in[-spread,0,spread]]))
def void(name,lo,hi,targets,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'targets':targets,'role':role}
def wall(name,lo,hi):WALL_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'target':'Cabinet_ThickIsolatedShell'}
# A regular cell union creates a single connected, manifold cabinet shell.
# Boundary quads share actual vertices; internal voxel faces are removed.
xs=[-.80,-.75,-.71,-.07,-.03,.03,.07,.71,.75,.80];ys=[-.30,-.25,.25,.30];zs=[.12,.18,.22,.78,.82,.88,.92,1.82,1.86,1.92]
cells=set()
for i,j,k in itertools.product(range(len(xs)-1),range(len(ys)-1),range(len(zs)-1)):
 x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2;z=(zs[k]+zs[k+1])/2
 interior=(-.75<x<-.03 or .03<x<.75) and (.18<z<.82 or .88<z<1.86) and -.25<y<.25
 throat=(-.71<x<-.07 or .07<x<.71) and (.22<z<.78 or .92<z<1.82) and -.30<y<-.25
 if not(interior or throat):cells.add((i,j,k))
vs=[];fs=[];index={}
for i,j,k in sorted(cells):
 corners=cuboid((xs[i],ys[j],zs[k]),(xs[i+1],ys[j+1],zs[k+1]))
 for face,neighbour in zip(BOX_FACES,[(i,j,k-1),(i,j,k+1),(i,j-1,k),(i,j+1,k),(i-1,j,k),(i+1,j,k)]):
  if neighbour in cells:continue
  ids=[]
  for q in face:
   p=corners[q]
   if p not in index:index[p]=len(vs);vs.append(p)
   ids.append(index[p])
  fs.append(ids)
mesh('Cabinet_ThickIsolatedShell',vs,fs,0,'one connected thick shell with four isolated cavities, complete back/bottom/sides/partitions, and real recessed front stop frames')
for label,x,y in [('FrontLeft',-.67,-.19),('FrontRight',.67,-.19),('BackLeft',-.67,.19),('BackRight',.67,.19)]:
 n=box('Foot_'+label,(x,y,.075),(.18,.16,.15),3,'finite rectangular ground sole overlapping cabinet bottom');FEET.append(n);link(n,'Cabinet_ThickIsolatedShell',(x,y,.135),axis=(1,0,0),spread=.035)
wall('EntireCenterDivider',(-.029,-.249,.181),(.029,.249,1.859))
wall('EntireCrossShelf',(-.749,-.249,.821),(.749,.249,.879))
wall('EntireBack',(-.749,.251,.181),(.749,.299,1.859))
wall('EntireBottom',(-.749,-.249,.121),(.749,.249,.179))
for side,x1,x2 in [('Left',-.799,-.751),('Right',.751,.799)]:wall('Entire'+side+'Side',(x1,-.249,.181),(x2,.249,1.859))
# Annular extrusions use one continuous real inner cylindrical wall.
def annular(name,pivot,zlo,zhi,outer,inner,mat,role,extension=None,angle=0,n=16):
 vs=[]
 for z in [zlo,zhi]:
  for kind in ['outer','inner']:
   for i in range(n):
    a=math.tau*i/n;x=(outer if kind=='outer' else inner)*math.cos(a);y=(outer if kind=='outer' else inner)*math.sin(a)
    if kind=='outer' and extension:
     if extension=='back' and y>1e-8:y+=.075
     if extension=='door' and x>1e-8:x+=.055;y*=.4
    c,s=math.cos(angle),math.sin(angle);vs.append((pivot[0]+c*x-s*y,pivot[1]+s*x+c*y,z))
 fs=[]
 for i in range(n):
  j=(i+1)%n
  fs += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
 # Correct winding globally for the four closed boundary strips.
 volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]]))+dot(vs[f[0]],cross(vs[f[2]],vs[f[3]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return mesh(name,vs,fs,mat,role)
def pin_mesh(name,pivot,zlo,zseat,zhi):
 n=16;profile=[(0,zlo),(.0075,zlo),(.0075,zseat),(.0205,zseat),(.0205,zhi),(0,zhi)];vs=[];rings=[];fs=[]
 for r,z in profile:
  ring=[]
  for i in range(n if r else 1):
   a=math.tau*i/n;ring.append(len(vs));vs.append((pivot[0]+r*math.cos(a),pivot[1]+r*math.sin(a),z))
  rings.append(ring)
 for a,b in zip(rings,rings[1:]):
  for i in range(n):
   j=(i+1)%n
   fs.extend([(a[0],b[j],b[i])] if len(a)==1 else [(a[i],a[j],b[0])] if len(b)==1 else [(a[i],a[j],b[j]),(a[i],b[j],b[i])])
 volume=sum(dot(vs[f[0]],cross(vs[f[1]],vs[f[2]])) for f in fs)/6
 if volume<0:fs=[tuple(reversed(f)) for f in fs]
 return mesh(name,vs,fs,2,'solid headed fixed pin; true shaft clear of both bored hinge walls, finite upper-head seating')
def rotate_point(p,pivot,angle):
 c,s=math.cos(angle),math.sin(angle);x,y=p[0]-pivot[0],p[1]-pivot[1];return(pivot[0]+c*x-s*y,pivot[1]+s*x+c*y,p[2])
def rotate_mesh(n,pivot,angle):G[n]['vertices']=[rotate_point(p,pivot,angle) for p in G[n]['vertices']]
def contact(a,b,z,pivot,radius=.015):
 CONTACTS.append({'a':a,'b':b,'origin_m':(0,0,0),'axis':(0,0,1),'u':(1,0,0),'v':(0,1,0),'plane_m':z,'minimum_patch_area_m2':.00072,'interior_probe_offset_m':.0003,'points':[(pivot[0]+radius*math.cos(t),pivot[1]+radius*math.sin(t),z) for t in[.3,2.4,4.5]],'scope':'complete opposed annular finite static hinge bearing; no penetration'})
for col,xl,xr in [('Left',-.75,-.03),('Right',.03,.75)]:
 for row,zl,zr in [('Lower',.18,.82),('Upper',.88,1.86)]:
  label=col+row;angle=-math.pi/2 if label=='LeftLower' else 0;pivot=(xl-.005,-.355);door='Door_'+label
  dl,dr=xl+.023,xr-.023;bottom,top=zl+.020,zr-.020
  box(door,((dl+dr)/2,-.355,(bottom+top)/2),(dr-dl,.035,top-bottom),1,'separate thick '+('90-degree fixed-open' if angle else 'fixed-closed')+' compartment door');rotate_mesh(door,pivot,angle)
  DOORS[door]={'label':label,'pivot':pivot,'angle_radians':angle,'interior_bounds':[(xl,-.25,zl),(xr,.25,zr)],'closed_bounds':[(dl,-.3725,bottom),(dr,-.3375,top)]}
  void(label+'_FullInterior',(xl+.001,-.249,zl+.001),(xr-.001,.249,zr-.001),[],'entire finite isolated storage cavity, 1mm surface inset')
  void(label+'_FullThroat',(xl+.041,-.301,zl+.041),(xr-.041,-.249,zr-.041),[],'entire finite recessed mouth and interior join, 1mm boundary inset')
  void(label+'_BehindDoor',(xl+.041,-.3365,zl+.041),(xr-.041,-.301,zr-.041),[],'complete volume from recessed frame to fixed door rear, or open doorway')
  for number,z in enumerate([zl+.145,zr-.145],1):
   stem='Hinge_'+label+'_'+str(number);a=stem+'_FrameBoredLug';b=stem+'_DoorBoredLug';p=stem+'_HeadedPin'
   annular(a,pivot,z-.055,z,.026,.011,2,'real pierced frame knuckle with integrated rear mounting tail','back')
   annular(b,pivot,z,z+.055,.026,.011,2,'real pierced door knuckle with integrated door mounting tail','door',angle)
   pin_mesh(p,pivot,z-.063,z+.055,z+.065)
   link('Cabinet_ThickIsolatedShell',a,(pivot[0],-.275,z-.028),axis=(1,0,0),spread=.010)
   point=rotate_point((pivot[0]+.060,pivot[1],z+.027),pivot,angle);axis=(math.cos(angle),math.sin(angle),0);link(door,b,point,axis=axis,spread=.008)
   contact(a,b,z,pivot);contact(b,p,z+.055,pivot)
   for name,lo,hi in [(a,z-.055,z),(b,z,z+.055)]:
    probe=name+'_FullBore';annular(probe,pivot,lo-.001,hi+.001,.0102,.000001,0,'temporary isolated volume')
    # Replace near-zero inner radius by a solid 16-gon prism for a closed bore probe.
    vs=[(pivot[0]+.0102*math.cos(math.tau*i/16),pivot[1]+.0102*math.sin(math.tau*i/16),zz) for zz in[lo-.001,hi+.001] for i in range(16)]
    fs=[tuple(reversed(range(16))),tuple(range(16,32))]+[(i,(i+1)%16,(i+1)%16+16,i+16) for i in range(16)]
    del G[probe];ISOLATED_VOID_VOLUMES[probe]={'vertices':vs,'faces':fs,'targets':[name],'role':'entire true through bore including both mouths; before pin'}
    BORES.append({'mesh':name,'origin_m':(pivot[0],pivot[1],lo-.001),'direction':(0,0,1),'length_m':hi-lo+.002,'meaning':'supplementary bore centre ray; complete finite volume separately tested'})
   air=stem+'_FullAnnularAir';annular(air,pivot,z-.054,z+.054,.0102,.0083,0,'temporary full annular clearance probe')
   AIR=G.pop(air);AIR.update(targets=[],role='full annular finite air around entire pin shaft inside both hinge knuckles, away from bearing faces');VOID_VOLUMES[air]=AIR
   HINGES.append({'frame':a,'door_lug':b,'pin':p,'door':door,'pivot':pivot,'z':z})
  # Simple thick external pull, plus a clearly distinct shell-mounted catch block.
  pull=box('Pull_'+label,(dr-.07,-.389,(zl+zr)/2),(.040,.052,.12),4,'simple static thick pull tab with positive overlap into its own door');rotate_mesh(pull,pivot,angle)
  point=rotate_point((dr-.07,-.369,(zl+zr)/2),pivot,angle);link(door,pull,point,axis=(0,0,1),spread=.025)
  catch=box('Catch_'+label,(xr+.007,-.317,(zl+zr)/2),(.029,.060,.105),2,'separate visible fixed catch block joined into compartment right jamb; no lock claim')
  link('Cabinet_ThickIsolatedShell',catch,(xr+.010,-.294,(zl+zr)/2),axis=(0,0,1),spread=.020)
# Centre the full frozen assembly horizontally, preserving all audit volumes.
allv=[v for g in G.values() for v in g['vertices']];SHIFT=tuple(-(min(v[i] for v in allv)+max(v[i] for v in allv))/2 if i<2 else 0 for i in range(3))
for g in list(G.values())+list(VOID_VOLUMES.values())+list(ISOLATED_VOID_VOLUMES.values())+list(WALL_VOLUMES.values()):g['vertices']=[add(p,SHIFT) for p in g['vertices']]
LINKS=[(a,b,[add(p,SHIFT) for p in pts]) for a,b,pts in LINKS]
for r in CONTACTS:r['points']=[add(p,SHIFT) for p in r['points']]
for r in BORES:r['origin_m']=add(r['origin_m'],SHIFT)
for r in DOORS.values():r['pivot']=add((*r['pivot'],0),SHIFT);r['interior_bounds']=[add(p,SHIFT) for p in r['interior_bounds']];r['closed_bounds']=[add(p,SHIFT) for p in r['closed_bounds']]
for r in HINGES:r['pivot']=add((*r['pivot'],0),SHIFT)
for g in VOID_VOLUMES.values():
 if not g['targets']:g['targets']=list(G)
LOCKER_CONTRACT={'single_prop_count':1,'independent_complete_cavities':4,'separate_thick_doors':4,'frozen_open_doors':1,'through_bored_hinge_pairs':8,'independent_solid_headed_pins':8,'finite_annular_hinge_contacts':16,'fixed_catch_blocks':4,'finite_feet':4,'native_fixed_pose_only':True}
def measure_parcel_locker_geometry(vertices):
 assert set(vertices)==set(G)
 assert all(abs(min(p[2] for p in vertices[n]))<2e-7 for n in FEET)
 for name,r in DOORS.items():
  p=vertices[name];assert max(v[2] for v in p)-min(v[2] for v in p)>.59
  thickness=max(v[0 if r['angle_radians'] else 1] for v in p)-min(v[0 if r['angle_radians'] else 1] for v in p);assert abs(thickness-.035)<2e-7
 return dict(LOCKER_CONTRACT,geometry_scope='actual source/exported coordinates; independent complete void, partition, contact and separation acceptance required')
SELFTESTS=[(FEET[0],add((-.67,-.19,.075),SHIFT),add((-.67,-.19,.17),SHIFT)),('Cabinet_ThickIsolatedShell',add((0,0,.5),SHIFT),add((-.4,0,.5),SHIFT))]
FOCUS=(0,0,.95);ORTHO=3.0
CAMERAS={'gray-front3q':(3.0,-5.2,3.5),'gray-back3q':(-3,5.2,3.5),'thumbnail':(3.0,-5.2,3.5),'qa-front':(0,-5.2,2.9),'qa-side':(5.2,0,2.9),'qa-top':(0,0,5.3),'qa-back':(0,5.2,2.9),'qa-wireframe':(3.0,-5.2,3.5),'silhouette-128-front':(0,-5.2,2.9),'silhouette-128-side':(5.2,0,2.9)}
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
root=bpy.data.objects.new('OneFourCompartmentPickupLocker',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='bounds-centred ground origin, Z=0';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
for name,p,outside in SELFTESTS:
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
mount_evidence=measure_parcel_locker_geometry({o.name:[o.matrix_world@v.co for v in o.data.vertices] for o in parts})
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
 'single_prop_count':1,'inside_predicate_actual_selftests':inside_predicate_selftests,'finite_opposed_face_contacts':face_contacts,'parcel_locker_geometry':mount_evidence,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/postal/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'postal','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
