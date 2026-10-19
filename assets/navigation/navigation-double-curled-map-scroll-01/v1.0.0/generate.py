"""Original double-curled fictional map. One continuous sheet, one static visual prop."""
import math,json,hashlib,sys,time,struct
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='navigation-double-curled-map-scroll-01';VERSION='1.0.0';TITLE='Double-Curled Fictional Map Scroll'
DESCRIPTION=('One original continuous thick fictional map with both ends curling upward and inward around genuinely open cores. The central broad flat sheet rests on its complete finite underside. Each side is an independently authored 1.375-turn tapered curl continuous with the same central sheet, with explicit closed front and back edge walls, open through-cores and fully separated overlapping layers. Two large irregular low-relief islands, one small islet and three short angular route dashes have complete finite bottom faces seated on the central map. Four opaque unlinked constant PBR colours; metres, Z up, front -Y and horizontal bounds-centred ground origin. No real geography, place names, text, coordinates, brands or logos. No table, stand, rod, shaft, core filler, separate floating rolled block, scene, figure, image or procedural texture. One whole static prop only. No real navigation, position, measurement, route planning, geographical accuracy, teaching reliability, paper or cloth physics, winding or unwinding animation, historical reconstruction, manufacture, material performance or safety claim. The former photography sweep already has real spiral layers; this is an original double-curled tabletop map, not a scaled or stripped copy, and does not cover a textile roll candidate.')
G={};LINKS=[];CONTACTS=[];GAPS=[];BORES=[];VOID_VOLUMES={};ISOLATED_VOID_VOLUMES={};SOLID_VOLUMES={};NONCONTACT_SURFACES=[]
BODY='Map_OneContinuousDoubleCurledThickSheet';FEET=[BODY];RELIEFS=[]
PALETTE=[('Parchment_WarmCream',(.83,.70,.46,1),.86,0),('Parchment_CutEdges',(.46,.27,.105,1),.88,0),('FictionalLand_MutedJade',(.19,.39,.27,1),.78,0),('Route_BurntCoral',(.54,.13,.055,1),.77,0)]
MATERIAL_CONTRACT='Four opaque unlinked constant Principled materials; no procedural or image texture nodes.'
FOCUS=(0,0,.083);ORTHO=1.32
CAMERAS={'gray-front3q':(.76,-1.50,1.31),'gray-back3q':(-.76,1.50,1.31),'thumbnail':(.76,-1.50,1.31),'qa-front':(0,-1.8,1.15),'qa-side':(1.8,0,1.30),'qa-top':(0,0,2.0),'qa-back':(0,1.8,1.15),'qa-wireframe':(.76,-1.50,1.31),'silhouette-128-front':(0,-1.8,1.15),'silhouette-128-side':(1.8,0,1.30)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
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
def area2(poly):return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2
def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def earclip2(poly):
 poly=[tuple(p) for p in poly];ii=list(range(len(poly)));out=[]
 if area2(poly)<0:ii.reverse()
 while len(ii)>3:
  found=False
  for k,b in enumerate(ii):
   a,c=ii[k-1],ii[(k+1)%len(ii)]
   if cross2(poly[a],poly[b],poly[c])<1e-13:continue
   if any(min(cross2(poly[a],poly[b],poly[j]),cross2(poly[b],poly[c],poly[j]),cross2(poly[c],poly[a],poly[j]))>=-1e-13 for j in ii if j not in [a,b,c]):continue
   out.append((a,b,c));ii.pop(k);found=True;break
  assert found,('No ear',len(ii))
 out.append(tuple(ii));return out
def prism(poly,lo,hi,axis=1,mat=0,role='complete closed finite polygon extrusion'):
 # All planar cap triangles use an exact concave polygon triangulation.
 assert hi>lo;poly=[tuple(round(float(v),9) for v in p) for p in poly];m=Mesh()
 def v(p,s):return (p[0],s,p[1]) if axis==1 else (p[0],p[1],s)
 for f in earclip2(poly):
  for s in [lo,hi]:m.face([v(poly[i],s) for i in f],mat,'cap')
 for a,b in zip(poly,poly[1:]+poly[:1]):m.face([v(a,lo),v(a,hi),v(b,hi),v(b,lo)],mat,'complete_boundary')
 return m.result(role,mat)
def box_geometry(lo,hi,mat=0,role='complete finite rectangular prism'):
 return prism([(lo[0],lo[2]),(hi[0],lo[2]),(hi[0],hi[2]),(lo[0],hi[2])],lo[1],hi[1],1,mat,role)
def inset_polygon(poly,d):
 # Finite mitered erosion of the original full polygon, no centre-point test.
 if area2(poly)<0:poly=list(reversed(poly))
 out=[]
 for i,p in enumerate(poly):
  a=poly[i-1];b=poly[(i+1)%len(poly)];u=(p[0]-a[0],p[1]-a[1]);v=(b[0]-p[0],b[1]-p[1]);lu=math.hypot(*u);lv=math.hypot(*v);n1=(-u[1]/lu,u[0]/lu);n2=(-v[1]/lv,v[0]/lv);den=1+dot(n1,n2);assert den>.001
  out.append((p[0]+d*(n1[0]+n2[0])/den,p[1]+d*(n1[1]+n2[1])/den))
 return out
def volume(entries,name,g,targets,role):entries[name]=dict(g,targets=list(targets),role=role)
def contact(a,b,points,area,label):
 CONTACTS.append({'name':label,'a':a,'b':b,'origin_m':(0,0,0),'axis':(0,0,1),'u':(1,0,0),'v':(0,1,0),'plane_m':.008,'points':points,'minimum_patch_area_m2':area,'interior_probe_offset_m':.0006,'scope':'complete finite opposed actual faces with full no-positive-penetration checks; static illustration only'})
WIDTH=.68;THICKNESS=.008;FLAT_HALF=.34;RADIUS=.112;PITCH=.036;TURN_SEGMENTS=64;CURL_SEGMENTS=88
# Original right path starts tangent to the middle, sweeps outward then coils inward.
# A sinusoidally eased radial descent gives an exact horizontal initial tangent.
RIGHT=[]
for i in range(CURL_SEGMENTS+1):
 s=math.tau*i/TURN_SEGMENTS;r=RADIUS-PITCH*(s-math.sin(s))/math.tau
 RIGHT.append((FLAT_HALF+r*math.sin(s),THICKNESS/2+RADIUS-r*math.cos(s)))
PATH=[(-x,z) for x,z in reversed(RIGHT)]+[RIGHT[0]]+RIGHT[1:]
LEFT_ROOT=CURL_SEGMENTS;RIGHT_ROOT=CURL_SEGMENTS+1
NORMALS=[]
for i,p in enumerate(PATH):
 nn=[]
 for j,k in [(max(0,i-1),i),(i,min(len(PATH)-1,i+1))]:
  if j==k:continue
  dx=PATH[k][0]-PATH[j][0];dz=PATH[k][1]-PATH[j][1];l=math.hypot(dx,dz);nn.append((-dz/l,dx/l))
 v=[sum(q[k] for q in nn) for k in range(2)];l=math.hypot(*v);v=[q/l for q in v];d=THICKNESS/2/dot(v,nn[0]);NORMALS.append((v[0]*d,v[1]*d))
# Flat-cell top and bottom remain exactly planar at .008 and 0 despite both bends.
ROWS=[]
for (x,z),(nx,nz) in zip(PATH,NORMALS):ROWS.append([(x+nx,-WIDTH/2,z+nz),(x+nx,WIDTH/2,z+nz),(x-nx,WIDTH/2,z-nz),(x-nx,-WIDTH/2,z-nz)])
def sheet_geometry(rows,role='one continuous closed thick double-curled sheet'):
 m=Mesh()
 for i,(a,b) in enumerate(zip(rows,rows[1:])):
  for j in range(4):k=(j+1)%4;m.face([a[j],a[k],b[k],b[j]],0 if j==0 else 1,'sheet_'+str(i)+'_'+str(j))
 m.face(rows[0],1,'left_tip');m.face(rows[-1],1,'right_tip');return m.result(role,0)
G[BODY]=sheet_geometry(ROWS)
# An entire core polygon follows the innermost full turn of the actual sheet.
# The radial open-tip cut separates this from the complete overlapping-layer band.
AIR_MARGIN=.00065;CORE_POLYS={};LAYER_POLYS={}
for side,sign in [('Left',-1),('Right',1)]:
 rr=ROWS[RIGHT_ROOT:]
 # At a full turn the inward side is the local top of this upward curl.
 inner=[(row[0][0],row[0][2]) for row in rr];outer=[(row[3][0],row[3][2]) for row in rr]
 core=inner[CURL_SEGMENTS-TURN_SEGMENTS:]+[outer[-1]]
 layer=inner[:CURL_SEGMENTS-TURN_SEGMENTS+1]+list(reversed(outer[TURN_SEGMENTS:]))
 core=[(sign*x,z) for x,z in core];layer=[(sign*x,z) for x,z in layer]
 CORE_POLYS[side]=inset_polygon(core,AIR_MARGIN);LAYER_POLYS[side]=inset_polygon(layer,AIR_MARGIN)
 for tag,poly in [('WholeCoreAndBothMouths',CORE_POLYS[side]),('WholeOverlappingInterlayerAirAndBothMouths',LAYER_POLYS[side])]:
  volume(VOID_VOLUMES,side+tag,prism(poly,-WIDTH/2-.002,WIDTH/2+.002),[],f'Complete {side.lower()} {tag} through the entire sheet width and both open mouths, original full finite boundary inset {AIR_MARGIN} m; radial terminal cuts divide connected core and layer domains, never sampled centre boxes.')
 # Full root bend cell material extends from the flat edge through the first 90 degrees.
 # Every polygon boundary is inset from the finite actual sheet faces.
 end=TURN_SEGMENTS//4
 strip=inner[:end+1]+list(reversed(outer[:end+1]));strip=[(sign*x,z) for x,z in strip]
 volume(SOLID_VOLUMES,side+'CompleteRootBendMaterial',prism(inset_polygon(strip,.00075),-.339,.339),[BODY],f'Full finite {side.lower()} root from the central transition through the first quarter-turn, not a point or seam label.')
volume(SOLID_VOLUMES,'WholeCentralFlatMaterial',box_geometry((-.336,-.339,.00075),(.336,.339,.00725)),[BODY],'Complete finite central material inset from its full rectangular flat boundaries.')
# Fictional low-relief shapes have whole opposed seats on the broad flat region.
LANDS=[('Island_West',[(-.292,-.094),(-.257,-.145),(-.199,-.119),(-.169,-.045),(-.087,-.015),(-.107,.061),(-.150,.084),(-.132,.166),(-.202,.222),(-.267,.189),(-.246,.113),(-.301,.056)],2,.014),('Island_East',[(.074,-.216),(.139,-.228),(.167,-.165),(.241,-.123),(.281,-.043),(.243,-.004),(.276,.065),(.213,.126),(.139,.096),(.092,.139),(.058,.066),(.094,.007),(.044,-.067)],2,.013),('Islet_North',[(.004,.186),(.035,.164),(.061,.195),(.039,.229),(-.003,.226),(-.019,.204)],2,.012)]
for name,poly,mat,top in LANDS:
 G[name]=prism(poly,.008,top,2,mat,'Original fictional low-relief land polygon with complete bottom seat; not real geography.');RELIEFS.append(name)
 a=abs(area2(poly));centroid=(sum(x for x,y in poly)/len(poly),sum(y for x,y in poly)/len(poly));contact(BODY,name,[(centroid[0],centroid[1],.008)],a*.999,'WholeSeat_'+name)
for i,(cx,cy,angle) in enumerate([(-.018,-.180,-.30),(.010,-.080,.35),(-.014,.028,-.22)]):
 co,si=math.cos(angle),math.sin(angle);poly=[(cx+x*co-y*si,cy+x*si+y*co) for x,y in [(-.006,-.023),(.006,-.023),(.006,.023),(-.006,.023)]];name='RouteDash_'+str(i+1)
 G[name]=prism(poly,.008,.011,2,3,'Fictional route dash with whole finite bottom seat; no navigation information.');RELIEFS.append(name);contact(BODY,name,[(cx,cy,.008)],abs(area2(poly))*.999,'WholeSeat_'+name)
for n,g in VOID_VOLUMES.items():g['targets']=list(G)
def measure_scroll_geometry(vertices):
 assert set(vertices)==set(G);v=[p for vv in vertices.values() for p in vv]
 return {'scope':'reported actual mesh bounds and counts only; full finite functional predicates are separately required','components':len(vertices),'continuous_sheet_source_segments':len(PATH)-1,'curl_turns_per_end_design':CURL_SEGMENTS/TURN_SEGMENTS,'sheet_thickness_design_m':THICKNESS,'central_ground_area_design_m2':(ROWS[RIGHT_ROOT][3][0]-ROWS[LEFT_ROOT][3][0])*WIDTH,'actual_min_z_m':min(p[2] for p in v),'actual_max_z_m':max(p[2] for p in v),'finite_relief_seats':len(CONTACTS)}
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
root=bpy.data.objects.new('OneStaticContinuousDoubleCurledMap',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground Z=0 and horizontal bounds-centred origin; illustrative front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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

# Producer checks here cover generated topology, volume and finite ground area.
# Connection lists and nominal dimensions below are source declarations only.
# Complete cavity, material and embedding tests require independent actual-GLB acceptance.
supports=[]
for name in FEET:
 o=byname[name];patch=[]
 for t in o.data.loop_triangles:
  vv=[o.matrix_world@o.data.vertices[i].co for i in t.vertices];cr=(vv[1]-vv[0]).cross(vv[2]-vv[0])
  if max(abs(p.z) for p in vv)<1e-7 and cr.z<0:patch.append({'vertices_m':[list(v) for v in vv],'area_m2':cr.length/2})
 area=sum(t['area_m2'] for t in patch);assert area>.0008,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
scroll_evidence=measure_scroll_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts})
joints=[{'a':a,'b':b,'points_m':points} for a,b,points in LINKS];seen=set(G);gap_checks=[];bore_checks=[];face_contacts=[]
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
 'components':component_checks,'connection_interior_points':joints,'declared_ground_connected_meshes':sorted(seen),'connection_evidence_scope':'Declared source link points only; complete embedded volumes not tested in this producer summary',
 'single_prop_count':1,'scroll_geometry':scroll_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer topology, ground, bounds and export fingerprint only; independent finite-volume, visual, native and runtime gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/navigation/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'navigation','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.8,-1.2,1.4),48,1.0),('Fill',(1.0,-.2,.8),24,.8),('Rim',(.2,1.0,1.2),34,.8)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Preview_'+name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,pos)
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Preview_Camera';cam.data.type='ORTHO';cam.data.ortho_scale=ORTHO;scene.camera=cam
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0001));ground=bpy.context.object;ground.name='Preview_ground_not_asset'
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
