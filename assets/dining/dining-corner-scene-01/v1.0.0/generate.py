"""Original dining-corner-scene-01. Blender 4.3+: blender -b -t 2 --python generate.py
Geometry is hand-designed via this script; no texture or tutorial assets required.
"""
import bpy, math, json, hashlib, time, os, sys, bmesh
from pathlib import Path
from mathutils import Vector
START=time.time()
OUT=Path(__file__).resolve().parent
ASSET='dining-corner-scene-01'
TITLE='Quiet Corner Dining Set'
DESCRIPTION='Original modular dining vignette with booth, round table, chair, freestanding lattice divider, service counter and a ceramic mug. Self-contained procedural source.'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
PALETTE={'honey':(0.48,0.255,0.105,1),'sand':(0.86,0.75,0.52,1),'teal':(0.19,0.40,0.35,1)}
mats={}
for name,col in PALETTE.items():
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.83
 mats[name]=m
parts=[]
def box(name,loc,scale,mat='honey',bevel=.018,rot=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;o.rotation_euler.z=rot
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]);b=o.modifiers.new('Soft hand-cut edge','BEVEL');b.width=bevel;b.segments=1
 bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 parts.append(o);return o

def mesh(name,verts,faces,material):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mats[material]);parts.append(o);return o
def lathe(name,profile,mat='teal',n=32):
 cyclic=profile[0]==profile[-1]
 if cyclic:profile=profile[:-1]
 verts=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for r,z in profile for i in range(n)]
 faces=[]
 for k in range(len(profile) if cyclic else len(profile)-1):
  nxt=(k+1)%len(profile)
  for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,nxt*n+(i+1)%n,nxt*n+i))
 if not cyclic:faces.extend([tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))])
 return mesh(name,verts,faces,mat)
def tube(name,points,radius,mat='honey',sides=8,cyclic=False):
 verts=[];faces=[]
 axis=min(range(3),key=lambda a:max(p[a] for p in points)-min(p[a] for p in points))
 ref=Vector(tuple(1 if a==axis else 0 for a in range(3)))
 for i,p in enumerate(points):
  tangent=Vector(points[(i+1)%len(points)])-Vector(points[(i-1)%len(points)]) if cyclic else Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
  tangent.normalize();n=tangent.cross(ref)
  if n.length<.001:n=tangent.cross(Vector((1,0,0)))
  n.normalize();bn=tangent.cross(n).normalized()
  for j in range(sides):verts.append(Vector(p)+radius*(math.cos(j*math.tau/sides)*n+math.sin(j*math.tau/sides)*bn))
 for i in range(len(points) if cyclic else len(points)-1):
  for j in range(sides):faces.append((i*sides+j,((i+1)%len(points))*sides+j,((i+1)%len(points))*sides+(j+1)%sides,i*sides+(j+1)%sides))
 if not cyclic:faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
 return mesh(name,verts,faces,mat)

GEOMETRY={'dining-booth-straight-01': "\nbox('Solid maple plinth',(0,0,.2),(1.12,.48,.4),'honey',.025)\nbox('Seafoam seat',(0,0,.46),(1.2,.55,.16),'teal',.04)\nbox('Back support',(0,.29,.77),(1.16,.1,.7),'honey',.018)\nbox('Seafoam back cushion',(0,.23,.8),(1.1,.12,.6),'teal',.035)\nbox('Ivory back crest',(0,.25,1.095),(1.2,.14,.06),'sand',.018)\nbox('Ivory plinth trim',(0,-.24,.1),(1.04,.06,.055),'sand',.01)\n", 'dining-service-counter-01': "\nfor x in [-.6,.6]:box('Seafoam side support',(x,0,.47),(.08,.48,.94),'teal',.014)\nbox('Seafoam rear panel',(0,.22,.47),(1.22,.05,.9),'teal',.01)\nbox('Maple base plinth',(0,0,.04),(1.3,.5,.08),'honey',.015)\nbox('Lower ivory shelf',(0,0,.12),(1.24,.45,.06),'sand',.012)\nbox('Upper ivory shelf',(0,0,.48),(1.24,.43,.055),'sand',.01)\nbox('Maple service top',(0,0,.95),(1.34,.54,.07),'honey',.022)\n", 'dining-lattice-divider-01': "\nfor x in [-.52,.52]:\n box('Maple upright',(x,0,.78),(.08,.08,1.5),'honey',.012)\n box('Stabilizing foot',(x,0,.04),(.16,.48,.08),'teal',.015)\nbox('Maple top rail',(0,0,1.5),(1.04,.06,.08),'honey',.014)\nbox('Maple lower rail',(0,0,.28),(1.04,.06,.08),'honey',.014)\nfor x in [-.36,-.18,0,.18,.36]:box('Seafoam lattice slat',(x,0,.9),(.045,.04,1.2),'teal',.008)\nfor z in [.65,1.15]:box('Ivory crossrail',(0,0,z),(1.04,.045,.045),'sand',.007)\n", 'kitchen-wall-shelf-01': "\nbox('Maple shelf board',(0,0,.19),(.8,.26,.05),'honey',.018)\nfor x in [-.28,.28]:\n verts=[(x+dx,y,z) for dx in [-.018,.018] for y,z in [(.095,0),(.095,.18),(-.1,.18)]]\n mesh('Triangular shelf bracket',verts,[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'teal')\nfor x in [-.2,0,.2]:\n tube('Ivory utility hook',[(x,-.075,.17),(x,-.075,.11),(x,-.095,.085),(x,-.125,.085),(x,-.14,.11)],.009,'sand')\n", 'kitchen-dining-chair-01': "\nbox('Maple chair seat',(0,0,.46),(.43,.43,.055),'honey',.025)\nfor x in [-.17,.17]:\n for y in [-.17,.17]:box('Chair leg',(x,y,.22),(.045,.045,.44),'teal',.009)\n box('Side stretcher',(x,0,.16),(.03,.36,.03),'sand',.006)\n box('Back upright',(x,.17,.69),(.05,.05,.48),'teal',.01)\nbox('Front stretcher',(0,-.17,.16),(.36,.03,.03),'sand',.006)\nbox('Maple back crest',(0,.17,.91),(.43,.065,.07),'honey',.018)\nfor x in [-.1,0,.1]:box('Ivory back slat',(x,.17,.69),(.042,.028,.42),'sand',.008)\n", 'kitchen-round-table-01': "\nlathe('Round maple tabletop',[(.01,.73),(.43,.73),(.46,.745),(.46,.775),(.44,.79),(.01,.79)],'honey',32)\nfor axis in [0,math.pi/2]:box('Cross support apron',(0,0,.7),(.66,.07,.1),'teal',.012,axis)\nfor x in [-.23,.23]:\n for y in [-.23,.23]:\n  box('Stout table leg',(x,y,.365),(.07,.07,.73),'teal',.012)\n  box('Ivory leveling foot',(x,y,.02),(.076,.076,.04),'sand',.008)\n", 'kitchen-mug-01': "\nlathe('Ceramic mug',[(.01,0),(.035,0),(.044,.012),(.046,.095),(.043,.104),(.036,.104),(.035,.025),(.01,.018)],'sand')\nlathe('Seafoam foot',[(.025,0),(.036,0),(.039,.006),(.036,.012),(.025,.012)],'teal')\ntube('Comfort loop',[(.04,.0,.083),(.065,0,.087),(.08,0,.073),(.08,0,.04),(.065,0,.025),(.04,0,.03)],.009,'honey')\n", 'kitchen-measuring-spoon-01': "\nlathe('Measuring bowl',[(.008,0),(.021,0),(.035,.02),(.04,.046),(.035,.05),(.03,.043),(.025,.02),(.008,.012)],'teal')\nlathe('Ivory edge',[(.035,.042),(.041,.045),(.04,.05),(.034,.052),(.031,.047),(.035,.042)],'sand')\nbox('Maple measuring grip',(.094,0,.036),(.125,.025,.021),'honey',.007)\n", 'kitchen-slotted-spatula-01': "\n# Five closed rails form four real slots rather than painted marks.\nfor x in [-.044,-.022,0,.022,.044]:\n box('Slotted head rail',(x,-.035,.009),(.012,.095,.014),'teal',.004)\nfor y in [-.083,.013]:box('Rounded head border',(0,y,.009),(.1,.018,.014),'teal',.004)\nbox('Turner neck',(0,.05,.013),(.022,.08,.017),'teal',.005)\nbox('Ivory ferrule',(0,.095,.015),(.032,.025,.025),'sand',.005)\nbox('Maple grip',(0,.168,.018),(.04,.13,.032),'honey',.009)\n", 'kitchen-stove-01': "\nbox('Seafoam casing',(0,0,.39),(.6,.53,.74),'teal',.035)\nbox('Ivory countertop',(0,0,.78),(.63,.56,.065),'sand',.02)\nbox('Front fascia',(0,-.274,.675),(.55,.025,.12),'sand',.012)\nbox('Dark oven door',(0,-.279,.36),(.49,.03,.42),'honey',.018)\nbox('Inset oven window',(0,-.299,.37),(.39,.012,.27),'teal',.012)\nbox('Oven handle',(0,-.325,.56),(.39,.033,.033),'sand',.01)\nfor x in [-.155,.155]:box('Handle mounting standoff',(x,-.3,.56),(.035,.07,.035),'sand',.006)\nfor x in [-.16,.16]:\n o=lathe('Burner concentric rings',[(.025,.815),(.085,.815),(.091,.829),(.078,.839),(.045,.839),(.025,.83)],'honey',24);o.location.x=x;o.location.z=-.003\n for angle in [0,math.pi/2]:box('Burner pot support',(x,0,.843),(.205,.018,.019),'teal',.003,angle)\nfor x in [-.18,0,.18]:\n bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.026,depth=.025,location=(x,-.304,.675),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='Maple control knob';o.data.materials.append(mats['honey']);parts.append(o)\nfor x in [-.22,.22]:\n for y in [-.19,.19]:box('Short foot',(x,y,.025),(.055,.055,.05),'honey',.009)\n", 'kitchen-sink-cabinet-01': "\nbox('Cabinet case',(0,0,.37),(.7,.52,.7),'teal',.025)\nfor x in [-.17,.17]:\n box('Paneled cabinet door',(x,-.268,.42),(.325,.025,.63),'honey',.012)\n box('Seafoam door inset',(x,-.285,.42),(.25,.014,.51),'teal',.009)\n box('Ivory vertical pull',(x*.22,-.31,.52),(.018,.028,.1),'sand',.005)\n# Rectangular basin with visible bottom and four thick gently beveled walls.\nbox('Basin floor',(0,0,.735),(.57,.39,.04),'sand',.025)\nfor x in [-.31,.31]:box('Basin side wall',(x,0,.79),(.065,.5,.15),'sand',.022)\nfor y in [-.225,.225]:box('Basin end wall',(0,y,.79),(.57,.06,.15),'sand',.018)\ntube('Bent mixer faucet',[(0,.2,.85),(0,.2,1.03),(0,.18,1.06),(0,.07,1.06),(0,.035,1.035),(0,.035,1.0)],.018,'honey')\nbox('Faucet lever',(.07,.2,.88),(.08,.018,.018),'honey',.005)\nfor x in [-.27,.27]:\n for y in [-.18,.18]:box('Cabinet foot',(x,y,.03),(.06,.06,.06),'honey',.01)\n"}
from mathutils import Matrix
def bring(aid,xyz,rz=0):
 global parts
 saved=parts;parts=[]
 exec(GEOMETRY[aid],globals())
 new=parts;parts=saved
 coords=[o.matrix_world@v.co for o in new for v in o.data.vertices]
 # Force dimension-derived transforms to update before world-space normalization.
 bpy.context.view_layer.update()
 coords=[o.matrix_world@v.co for o in new for v in o.data.vertices]
 shift=Vector(((min(v.x for v in coords)+max(v.x for v in coords))/2,(min(v.y for v in coords)+max(v.y for v in coords))/2,min(v.z for v in coords)))
 for o in new:
  o.name=aid+' / '+o.name
  o.matrix_world=Matrix.Translation(Vector(xyz))@Matrix.Rotation(rz,4,'Z')@Matrix.Translation(-shift)@o.matrix_world
  parts.append(o)

bring('dining-booth-straight-01',(0,.65,.06))
bring('kitchen-round-table-01',(0,-.05,.06))
bring('kitchen-dining-chair-01',(0,-.8,.06),math.pi)
bring('dining-service-counter-01',(1.33,.55,.06))
bring('dining-lattice-divider-01',(-.92,.05,.06),math.pi/2)
bring('kitchen-mug-01',(.12,-.03,.85))
box('Ivory dining platform',(.4,-.1,.03),(3.5,2.4,.06),'sand',.03)
# Normalize winding per closed component before export.
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# All mesh origins at the common bottom-center; keep parts separate for editing.
scene.cursor.location=(0,0,0)
for o in parts:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
# Normalize exact full-asset bottom-center after all component transforms.
coords=[v.co.copy() for o in parts for v in o.data.vertices]
shift=Vector(((min(v.x for v in coords)+max(v.x for v in coords))/2,(min(v.y for v in coords)+max(v.y for v in coords))/2,min(v.z for v in coords)))
for o in parts:
 for v in o.data.vertices:v.co-=shift
# Join only for export to reduce runtime draw calls; restore editable components afterwards.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.object.duplicate();export_parts=list(bpy.context.selected_objects);bpy.ops.object.join();model=bpy.context.object;model.name=ASSET
model.data.calc_loop_triangles();triangles=len(model.data.loop_triangles)
bounds=[round(v,5) for v in model.dimensions]
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.data.objects.remove(model,do_unlink=True)
# Persist clean source before adding the non-exported presentation rig.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source.blend'))
# Geometry and format QA. Components closed; deliberate plank overlaps are allowed.
import bmesh
bad=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
assert 100<=triangles<=20000,triangles
assert bounds[2]>0 and min(v.co.z for o in parts for v in o.data.vertices)>-1e-5
assert (OUT/'model.glb').stat().st_size<1500000
if '--geometry-only' in sys.argv:
 print('GEOMETRY_READY',ASSET,triangles,bounds);sys.exit(0)
# A consistent orthographic studio; real Cycles renders, not browser evidence.
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.world.color=(.32,.32,.32)
scene.view_settings.view_transform='AgX'
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=max(bounds)*1.65
focus=Vector((0,0,bounds[2]*.48))
def point(o,xyz):o.location=xyz;o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),180,3),('Rim',(1,4,5),300,3)]:
 bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;point(light,xyz)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object;ground.name='Preview ground (not asset)'
g=bpy.data.materials.new('Studio warm slate');g.diffuse_color=(.18,.22,.24,1);ground.data.materials.append(g)
views={'thumbnail':(3,-4,2.8),'qa-front':(0,-5,focus.z),'qa-side':(5,0,focus.z),'qa-top':(0,0,6),'qa-wireframe':(3,-4,2.8)}
wiremat=bpy.data.materials.new('QA dark edges');wiremat.diffuse_color=(.012,.018,.022,1)
for name,xyz in views.items():
 if '--wire-only' in sys.argv and name!='qa-wireframe':continue
 if '--no-render' in sys.argv:continue
 if name=='qa-wireframe':
  for o in parts:
   o.data.materials.append(wiremat)
   wire=o.modifiers.new('QA edge overlay','WIREFRAME');wire.thickness=.0025;wire.use_replace=False;wire.offset=1;wire.material_offset=len(o.data.materials)-1
 scene.cycles.samples=512 if name=='thumbnail' else 128
 point(cam,tuple(focus+Vector(xyz)-Vector((0,0,0))) if name in ['thumbnail','qa-wireframe'] else xyz);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
files={}
for role,file in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
 p=OUT/file;files[role]={'path':f'assets/dining/{ASSET}/v1.0.0/{file}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
meta={'id':ASSET,'version':'1.0.0','category':'scenes','assetKind':'scene','theme':'dining','style':'soft-low-poly','title':TITLE,'description':DESCRIPTION,'bounds':dict(zip(['x','y','z'],bounds),unit='m'),'triangles':triangles,'materials':3,'files':files,'status':'review','license':'All rights reserved'}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
qa={'asset':ASSET,'blender':bpy.app.version_string,'triangles':triangles,'materials':3,'bounds_m':bounds,'glb_bytes':files['glb']['size'],'nonmanifold_components':bad,'origin':'bottom center 0,0,0','transforms':'applied identity','textures':'none required; solid PBR materials','render_evidence':'Blender Cycles 512px, not browser screenshots','elapsed_seconds':round(time.time()-START,2),'generated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'review_status':'awaiting independent visual and runtime review'}
(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n');print('ASSET_COMPLETE',json.dumps(qa))
