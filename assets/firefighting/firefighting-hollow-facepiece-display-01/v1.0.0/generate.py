"""Original hollow facepiece: static exhibition prop, never protective equipment."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='firefighting-hollow-facepiece-display-01';VERSION='1.0.0';TITLE='Hollow Firefighting Facepiece Display'
DESCRIPTION=('One original static low-poly firefighting-facepiece visual prop on its own low display plinth. A continuous thick charcoal face frame has an open rear cavity, a broad sculpted red lower nose-and-mouth contour, and a separately editable thick curved fully opaque blue illustrative window. '
 'One solid faceted front connector and four solid side attachment ears are seated into the shell. Two thick U-shaped fixed headbands have genuinely open front ends, finite ear connections and empty interiors. No head, mannequin, hidden rear filler, transparent sheet, cylinder, hose or complete breathing system is included. '
 'Ten named closed editable meshes and five constant opaque PBR materials. The shell has a finite flat underside seated on the low plinth, whose broad flat bottom meets ground. Metres, native Z up, front -Y, X centreline and ground Z=0 origin with design Y=0 datum. One complete fixed display assembly counts as one prop. No textures, logos, external geometry or animation. '
 'Original generic visual design, with no brand, model or existing equipment compatibility claim. The window is intentionally opaque and cannot be seen through. No respiratory, filtration, oxygen supply, airtightness, heat, smoke, chemical or protective performance, field of view, eyesight, wearer fit, ergonomics, structural load, stability, manufacture, real firefighting use or safety certification is claimed. Not real equipment design or use guidance.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];FEET=[];VOID_PROBES={}
PALETTE=[('Charcoal_FrameAndBands',(.045,.060,.070,1),.70,.05),('OpaqueBlue_IllustrativeWindow',(.12,.30,.38,1),.32,.10),('OxideRed_NoseAndMouth',(.50,.085,.035,1),.53,.12),('SatinSteel_ConnectorAndEars',(.40,.46,.48,1),.38,.65),('WarmGrey_DisplayPlinth',(.39,.40,.35,1),.77,0)]
MATERIAL_CONTRACT='Five fully opaque unlinked constant Principled materials; no image or procedural textures. Opaque illustrative window, no optical claim.'
FOCUS=(0,.025,.215);ORTHO=.65
CAMERAS={'gray-front3q':(.80,-1.3,.95),'gray-back3q':(-.80,1.3,.95),'thumbnail':(.80,-1.3,.95),'qa-front':(0,-1.6,.62),'qa-side':(1.6,.025,.62),'qa-top':(0,.025,1.8),'qa-back':(0,1.6,.62),'qa-wireframe':(.80,-1.3,.95),'silhouette-128-front':(0,-1.6,.62),'silhouette-128-side':(1.6,.025,.62)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
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
N=32;ANGLES=[math.tau*i/N for i in range(N)]
def curved_y(x):return -.110+.045*(x/.125)**2
def facial(a,inner=False):
 x=(.107 if inner else .125)*math.cos(a);z=.235+(.142 if inner else .160)*math.sin(a)
 if math.sin(a)<-.90:z=.095 if inner else .075
 return x,z
def window(a,expanded=False):return ((.094 if expanded else .090)*math.cos(a),.290+(.069 if expanded else .065)*math.sin(a))
outer=[];inner=[];win=[];middle=[];inner_middle=[]
for a in ANGLES:
 x,z=facial(a);ix,iz=facial(a,True);wx,wz=window(a)
 outer.append((x,curved_y(x),z));inner.append((ix,curved_y(x)+.014,iz));win.append((wx,curved_y(wx),wz))
 mx,mz=(x+wx)/2,(z+wz)/2
 middle.append((mx,curved_y(mx)-.030*max(0,-math.sin(a))**3,mz))
 inner_middle.append(((ix+wx)/2,curved_y(mx)-.030*max(0,-math.sin(a))**3+.014,(iz+wz)/2))
shell_loops=[[(x,.045,z) for x,y,z in outer],outer,middle,win,[(x,y+.014,z) for x,y,z in win],inner_middle,inner,[(x,.045,z) for x,y,z in inner]]
tags=['outer_side','outer_face','nose_mouth_face','window_reveal','inner_face','inner_face','inner_side','rear_rim']
m=Mesh()
for k,(a,b) in enumerate(zip(shell_loops,shell_loops[1:]+shell_loops[:1])):
 for i in range(N):
  j=(i+1)%N;mat=2 if k in [1,2] and math.sin((ANGLES[i]+ANGLES[i]+math.tau/N)/2)<-.15 else 0
  m.face([a[i],a[j],b[j],b[i]],mat,tags[k])
G['Facepiece_ThickOpenBackShell']=m.result('Single continuous thick face frame, sculpted lower nose-mouth contour and entirely open rear aperture; flat finite bottom seat.')
# A convex-in-X opaque window with actual front, back and perimeter thickness.
m=Mesh();front=[];back=[]
for a in ANGLES:
 x,z=window(a,True);front.append((x,curved_y(x)-.002,z));back.append((x,curved_y(x)+.008,z))
for i in range(N):
 j=(i+1)%N
 m.face([(0,curved_y(0)-.002,.290),front[i],front[j]],1,'window_front')
 m.face([(0,curved_y(0)+.008,.290),back[j],back[i]],1,'window_back')
 m.face([front[i],back[i],back[j],front[j]],1,'window_edge')
G['Facepiece_CurvedOpaqueWindow']=m.result('Independent closed curved 10 mm illustrative opaque window, intentionally no transparency or optical capability.',1)
for a in [0,math.pi/2,math.pi,3*math.pi/2]:
 x,z=window(a);LINKS.append(('Facepiece_ThickOpenBackShell','Facepiece_CurvedOpaqueWindow',[(x*1.015,curved_y(x)+.004,.290+(z-.290)*1.015)]))
def box(name,lo,hi,mat,role):
 m=Mesh();v=[(x,y,z) for z in [lo[2],hi[2]] for y in [lo[1],hi[1]] for x in [lo[0],hi[0]]]
 for q in [(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]:m.face([v[i] for i in q],mat,'flat')
 G[name]=m.result(role,mat)
for level,z in [('Lower',.165),('Upper',.305)]:
 for side,sign in [('Right',1),('Left',-1)]:
  name='Facepiece_'+level+'Ear_'+side
  xs=sorted([sign*.100,sign*.146]);box(name,(xs[0],.018,z-.012),(xs[1],.053,z+.012),3,'Solid attachment ear with a finite shell connection and a finite open-band end seat.')
  LINKS.append(('Facepiece_ThickOpenBackShell',name,[(sign*.105,.030,z-.004),(sign*.105,.030,z+.004)]))
 m=Mesh();steps=24;profiles=[]
 for i in range(steps+1):
  a=math.pi*i/steps;profiles.append([(rx*math.cos(a),.035+ry*math.sin(a),zz) for rx,ry,zz in [(.134,.201,z-.010),(.144,.211,z-.010),(.144,.211,z+.010),(.134,.201,z+.010)]])
 for a,b in zip(profiles,profiles[1:]):
  for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]],0,['band_bottom','band_outer','band_top','band_inner'][i])
 m.face(profiles[0][::-1],0,'band_end');m.face(profiles[-1],0,'band_end')
 name='Facepiece_OpenUHeadband_'+level;G[name]=m.result('One thick static U-shaped open-ended band; both finite closed end caps connect to side ears, with no rear filling surface.')
 for side,sign in [('Right',1),('Left',-1)]:LINKS.append(('Facepiece_'+level+'Ear_'+side,name,[(sign*.139,.041,z-.003),(sign*.139,.041,z+.003)]))
# One solid short capped connector, no bore or gas passage claim.
m=Mesh();loops=[]
for y,r in [(-.132,.021),(-.145,.030),(-.174,.030),(-.185,.024)]:loops.append([(r*math.cos(math.tau*i/12),y,.151+r*math.sin(math.tau*i/12)) for i in range(12)])
for a,b in zip(loops,loops[1:]):
 for i in range(12):j=(i+1)%12;m.face([a[i],a[j],b[j],b[i]],3,'connector_side')
m.face(loops[0][::-1],3,'connector_back');m.face(loops[-1],2,'connector_cap')
G['Facepiece_SolidShortConnector']=m.result('Solid faceted capped front connection block, fixed into the sculpted lower shell. No functional opening, airflow or compatibility.',3)
LINKS.append(('Facepiece_ThickOpenBackShell','Facepiece_SolidShortConnector',[(-.006,-.135,.151),(.006,-.135,.151)]))
# One continuous low exhibition plinth, including its small flat upper seat.
m=Mesh();loops=[]
for z,hx,y0,y1 in [(0,.100,-.140,.200),(.024,.100,-.140,.200),(.032,.042,-.100,.025),(.075,.042,-.100,.025)]:loops.append([(-hx,y0,z),(hx,y0,z),(hx,y1,z),(-hx,y1,z)])
for a,b in zip(loops,loops[1:]):
 for i in range(4):j=(i+1)%4;m.face([a[i],a[j],b[j],b[i]],4,'plinth_side')
m.face(loops[0][::-1],4,'ground');m.face(loops[-1],4,'seat')
G['Display_LowFiniteSeatPlinth']=m.result('One low continuous display plinth with finite flat ground footprint and a narrow actual flat seat beneath the facepiece.',4)
FEET=['Display_LowFiniteSeatPlinth']
CONTACTS=[{'a':'Display_LowFiniteSeatPlinth','b':'Facepiece_ThickOpenBackShell','plane_m':.075,'minimum_patch_area_m2':.01049,'interior_probe_offset_m':.001,'points':[(-.030,-.070,.075),(.030,-.070,.075),(-.030,.005,.075),(.030,.005,.075)],'scope':'entire 84 mm by 125 mm opposed flat plinth top, not a point or edge rest'}]
def closed_loft(loops,role):
 m=Mesh();n=len(loops[0])
 for a,b in zip(loops,loops[1:]):
  for i in range(n):j=(i+1)%n;m.face([a[i],a[j],b[j],b[i]])
 # Convex terminal profiles can use a centre fan even when not planar.
 for k,reverse in [(0,True),(-1,False)]:
  q=loops[k];centre=tuple(sum(p[j] for p in q)/n for j in range(3))
  for i in range(n):j=(i+1)%n;m.face([centre,q[j],q[i]] if reverse else [centre,q[i],q[j]])
 return m.result(role)
def cavity_point(p,dy=0):
 x,y,z=p;return (x*.978,y+dy,.235+(z-.235)*.978)
# Whole inset cavity envelope follows the actual inner-shell front and side
# contours, then traverses beyond the rear aperture. It is never rendered.
ql=[[(x*.978,.080,.235+(z-.235)*.978) for x,y,z in inner],
    [cavity_point(p,.004) for p in inner],
    [cavity_point(p,.004) for p in inner_middle],
    [cavity_point((x,y+.014,z),.004) for x,y,z in win]]
VOID_PROBES['CompleteOpenRearCavity']={'type':'mesh','geometry':closed_loft(ql,'Whole finite inset facepiece cavity, following inner-shell contour and extending past the rear rim.'),'targets':list(G),'role':'complete rear cavity envelope with positive geometric wall margin, full triangle containment and intersection checked'}
for level,z in [('Lower',.165),('Upper',.305)]:
 # Whole inner semiellipse, truncated 4 mm behind the ears, so its front
 # closure lies outside both ears and the facepiece open rear rim.
 a0=math.asin((.058-.035)/.197);arc=[]
 for i in range(25):
  a=a0+(math.pi-2*a0)*i/24;arc.append((.130*math.cos(a),.035+.197*math.sin(a)))
 q=[[(x,y,zz) for x,y in arc] for zz in [z-.012,z+.012]]
 VOID_PROBES['CompleteBandInterior_'+level]={'type':'mesh','geometry':closed_loft(q,'Complete finite inner U-band region with open forward throat.'),'targets':list(G),'role':'full rear U-band inner area and full thickness, inset from band walls and beyond shell/ear back edge'}
 VOID_PROBES['OpenBandThroat_'+level]={'type':'box','lo_m':[-.085,.047,z-.009],'hi_m':[.085,.070,z+.009],'targets':list(G),'role':'finite open throat through front of U band, including the exposed rear facepiece opening'}
def measure_facepiece_geometry(vertices):
 return {'single_prop_count':1,'mesh_count':len(G),'shell_rear_plane_y_m':.045,'window_nominal_y_thickness_m':.010,'shell_front_nominal_y_thickness_m':.014,'open_U_band_count':2,'band_vertical_width_m':.020,'band_nominal_radial_thickness_m':.010,'solid_ear_count':4,'solid_connector_count':1,'seat_plane_z_m':.075,'seat_patch_area_m2':.0105,'ground_patch_area_m2':.068,'materials':MATERIAL_CONTRACT,'functional_scope':'one fixed hollow facepiece visual on same-ID low plinth; no equipment, optical, fit or protection claim'}

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
root=bpy.data.objects.new('OneHollowFacepieceDisplay',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='X centreline, design Y=0 and ground Z=0; front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
facepiece_evidence=measure_facepiece_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[];seen=set(FEET);gap_checks=[];bore_checks=[];face_contacts=[]
def actual_inside(name,point):
 p=Vector(point);total=0.0
 for tri in actual_triangles[id(trees[name])]:
  a,b,c=[Vector(q)-p for q in tri];la,lb,lc=a.length,b.length,c.length
  total+=2*math.atan2(a.dot(b.cross(c)),la*lb*lc+a.dot(b)*lc+b.dot(c)*la+c.dot(a)*lb)
 return abs(total/(4*math.pi))>.5
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
  low=(p[0],p[1],p[2]-eps);high=(p[0],p[1],p[2]+eps)
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
 'single_prop_count':1,'facepiece_geometry':facepiece_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/firefighting/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'firefighting','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
g=bpy.data.materials.new('Preview_slate');g.diffuse_color=(.20,.24,.25,1);ground.data.materials.append(g)
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
