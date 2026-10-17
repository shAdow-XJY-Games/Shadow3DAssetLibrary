#!/usr/bin/env python3
"""Original static S03 two-storey shop-house, authored from approved design r2c.

SELF-CONTAINED: Blender 4.3+ and its bundled Python only; no external models,
textures, helper scripts, credentials or downloads. Copy this file alone to a
clean directory for recovery. Default phase is geometry and never renders.

Example after production-manager authorization:
  blender -b -t 4 --python generate.py -- --phase geometry --no-render --out NEW_DIR

Independent S03-SH04x06-v1 family, 4 x 6 m wall-centre grid. This is a NON-ENTERABLE
STATIC EXTERIOR SHELL: fixed closed rebated entry board, opaque fixed glazing,
real wall apertures and two real floor decks. NO stairs, interior fitout,
floor-to-floor passage, runtime opening, animation, load or safety claims.
Eleven static parents retain named child meshes and component-role extras.
Do not substitute old 2 m modules or old cottage approvals for this model's QA.

Approved design-only pins (not approval of any generated mesh or image):
  SPEC 6affee9466d1bea22f95826df5bfdba2068f280af888fddea5cef2d195335a23
  DESIGN 357341e2a3678015336a0445fd1e12dbaef31af77f20b63b1848e76a1990d0c2
All output must use a fresh directory. No overwrite/resume/remote/Git actions.
"""
import argparse
import base64
import bmesh
import bpy
import hashlib
import json
import math
import shutil
import sys
import time
import zlib
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ASSET = 'village-two-storey-shop-house-01'
VERSION = '1.0.0'
TITLE = 'Timber Shop House with Upper Dwelling'
FAMILY = 'S03-SH04x06-v1'
SPEC_SHA256 = '6affee9466d1bea22f95826df5bfdba2068f280af888fddea5cef2d195335a23'
DESIGN_SHA256 = '357341e2a3678015336a0445fd1e12dbaef31af77f20b63b1848e76a1990d0c2'
DESCRIPTION = ('Original static S03 two-storey shop-house shell on a 4 x 6 m wall-centre grid. '
 'Lower display opening and fixed entry board, distinct upper dwelling windows, real floor decks, '
 'aligned timber columns, ring-and-joist upper floor, thick gables, clay roof and integral stone steps. '
 'Independent S03-SH04x06-v1 family; existing 2 m modules are dimensional references only. '
 'Door and opaque glazing are fixed. No stairs, enterable interior, floor-to-floor passage, '
 'runtime opening, animation, structural capacity or safety certification. '
 'Named child mesh identities are preserved under eleven static parent groups.')
EPS = 0.0002
AREA_FRACTION = 0.95
RAY_DIRS = [Vector(v).normalized() for v in [(1,.371,.193),(.219,1,.413),(.317,.277,1)]]


def rounded(v, n=8):
    return [round(float(x), n) for x in v]


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def configure_render(scene):
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 128
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.use_denoising = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.use_nodes = False
    scene.render.use_compositing = False
    scene.render.use_sequencer = False
    if scene.node_tree:
        for node in list(scene.node_tree.nodes):
            if node.type == 'DENOISE':
                scene.node_tree.nodes.remove(node)
    for layer in scene.view_layers:
        if hasattr(layer, 'cycles') and hasattr(layer.cycles, 'use_denoising'):
            layer.cycles.use_denoising = False
        if hasattr(layer, 'cycles') and hasattr(layer.cycles, 'use_pass_denoising_data'):
            layer.cycles.use_pass_denoising_data = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'AgX'


def assert_render_config(scene, event, log):
    denoise_nodes = [n.name for n in scene.node_tree.nodes if n.type == 'DENOISE'] if scene.node_tree else []
    layers = {v.name: bool(v.cycles.use_denoising) for v in scene.view_layers
              if hasattr(v, 'cycles') and hasattr(v.cycles, 'use_denoising')}
    record = {'event': event, 'engine': scene.render.engine, 'samples': scene.cycles.samples,
              'adaptive': bool(scene.cycles.use_adaptive_sampling),
              'cycles_denoise': bool(scene.cycles.use_denoising),
              'threads_mode': scene.render.threads_mode, 'threads': scene.render.threads,
              'scene_use_nodes': bool(scene.use_nodes),
              'use_compositing': bool(scene.render.use_compositing),
              'compositor_denoise_nodes': denoise_nodes, 'view_layer_denoise': layers}
    assert record['engine'] == 'CYCLES' and record['samples'] == 128, record
    assert not record['adaptive'] and not record['cycles_denoise'], record
    assert record['threads_mode'] == 'FIXED' and record['threads'] == 4, record
    assert not record['scene_use_nodes'] and not record['use_compositing'], record
    assert not denoise_nodes and not any(layers.values()), record
    log.append(record)
    return record


def in_box(p, b):
    return all(b[2*i] < p[i] < b[2*i+1] for i in range(3))


def ortho_solid(union_boxes, subtract_boxes=()):
    """Exact axis-aligned cell-boundary solid; removes every internal shared face.
    Cutters are scoped real dimensions. No hidden complete wall or fake black hole.
    """
    lo = [min(b[2*i] for b in union_boxes) for i in range(3)]
    hi = [max(b[2*i+1] for b in union_boxes) for i in range(3)]
    cuts = [b for b in subtract_boxes if all(b[2*i] < hi[i] and b[2*i+1] > lo[i] for i in range(3))]
    axes = [sorted(set(round(v,10) for v in [lo[i],hi[i]] + [max(lo[i],min(hi[i],float(b[j])))
             for b in list(union_boxes)+cuts for j in [2*i,2*i+1]])) for i in range(3)]
    filled = set()
    for ix in range(len(axes[0])-1):
        for iy in range(len(axes[1])-1):
            for iz in range(len(axes[2])-1):
                p = [(axes[i][q]+axes[i][q+1])/2 for i,q in enumerate([ix,iy,iz])]
                if any(in_box(p,b) for b in union_boxes) and not any(in_box(p,b) for b in cuts):
                    filled.add((ix,iy,iz))
    assert filled, 'Empty orthogonal result'
    vertices, faces, lookup = [], [], {}
    def vi(p):
        key = tuple(round(c,10) for c in p)
        if key not in lookup:
            lookup[key] = len(vertices); vertices.append(key)
        return lookup[key]
    for ix,iy,iz in sorted(filled):
        x0,x1 = axes[0][ix:ix+2]; y0,y1 = axes[1][iy:iy+2]; z0,z1 = axes[2][iz:iz+2]
        quads = [((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),
                 ((1,0,0),[(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]),
                 ((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]),
                 ((0,1,0),[(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)]),
                 ((0,0,-1),[(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)]),
                 ((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])]
        for delta, pts in quads:
            neighbour = (ix+delta[0],iy+delta[1],iz+delta[2])
            if neighbour not in filled:
                faces.append(tuple(vi(p) for p in pts))
    return vertices, faces


def split_shells(vertices, faces):
    """Keep each connected source shell separately identifiable in native and GLB."""
    links = defaultdict(set)
    for f in faces:
        for a,b in zip(f, f[1:]+f[:1]):
            links[a].add(b); links[b].add(a)
    remaining = set(range(len(vertices))); groups = []
    while remaining:
        seed=min(remaining); remaining.remove(seed); group={seed}; todo=[seed]
        while todo:
            for j in links[todo.pop()]:
                if j in remaining: remaining.remove(j); group.add(j); todo.append(j)
        order=sorted(group); remap={old:i for i,old in enumerate(order)}
        ff=[tuple(remap[i] for i in f) for f in faces if f[0] in group]
        groups.append(([vertices[i] for i in order],ff))
    groups.sort(key=lambda g: tuple(min(v[k] for v in g[0]) for k in range(3)))
    return groups


def box_mesh(bounds):
    return ortho_solid([bounds])


def prism_y(section, y0, y1):
    n=len(section)
    vertices=[(x,y,z) for y in [y0,y1] for x,z in section]
    faces=[tuple(range(n-1,-1,-1)), tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return vertices, faces


def wall_box(wall, a0, a1, depth, z0, z1):
    if wall in ['front','rear']:
        c=-3 if wall=='front' else 3
        return [a0,a1,c-depth/2,c+depth/2,z0,z1]
    c=-2 if wall=='left' else 2
    return [c-depth/2,c+depth/2,a0,a1,z0,z1]


class Builder:
    def __init__(self, scene, spec):
        self.scene=scene; self.spec=spec; self.parts=[]; self.objects={}; self.parents={}
        self.component_audit=[]; self.cutters=defaultdict(list); self.openings=[]
        self.mats={}
        for key,rgba in spec['palette_rgba'].items():
            mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=rgba
            node=mat.node_tree.nodes.get('Principled BSDF');node.inputs['Base Color'].default_value=rgba
            node.inputs['Roughness'].default_value=.32 if key=='fixed_glazing' else (.90 if key.startswith('stone') else .83)
            node.inputs['Metallic'].default_value=.65 if key=='iron_detail' else 0
            self.mats[key]=mat
        for name in spec['planned_runtime_nodes']:
            o=bpy.data.objects.new(name,None);scene.collection.objects.link(o)
            o['asset_id']=ASSET;o['family']=FAMILY;o['static_group_role']=name
            self.parents[name]=o
    def add(self, name, geometry, material, group, role, storey, audit=None):
        results=[]
        shells=split_shells(*geometry)
        for index,(verts,faces) in enumerate(shells):
            component=name if len(shells)==1 else name+'_Shell%02d'%index
            assert component not in self.objects, component
            mesh=bpy.data.meshes.new(component+'_Mesh');mesh.from_pydata(verts,[],faces);mesh.update()
            bm=bmesh.new();bm.from_mesh(mesh)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-9)
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
            bmesh.ops.triangulate(bm,faces=list(bm.faces))
            assert all(e.is_manifold for e in bm.edges),('Source shell not closed',component)
            assert bm.calc_volume(signed=True)>1e-10,('Nonpositive source shell',component)
            bm.to_mesh(mesh);bm.free();mesh.update()
            o=bpy.data.objects.new(component,mesh);self.scene.collection.objects.link(o)
            o.parent=self.parents[group];o.data.materials.append(self.mats[material])
            o['component_id']=component;o['structural_role']=role;o['storey']=storey;o['static_parent_group']=group
            self.parts.append(o);self.objects[component]=o;results.append(o)
            self.component_audit.append({'component_id':component,'role':role,'storey':storey,'parent':group,'construction':audit or {}})
        return results
    def box(self,name,bounds,material,group,role,storey,cuts=(),audit=None):
        return self.add(name,ortho_solid([bounds],cuts),material,group,role,storey,audit)
    def one(self,name):
        return self.objects[name]
    def add_cut(self,wall,storey,name,bounds):
        self.cutters[(wall,storey)].append({'id':name,'bounds_m':bounds})


def build_asset(scene, spec):
    b=Builder(scene,spec)
    # Continuous stepped foundation and new three-rise entry are one true union.
    foundation_boxes=[[-2.18,2.18,-3.18,3.18,0,.15],[-2.2,2.2,-3.2,3.2,.15,.30],
       [.36,1.64,-4.02,-3.16,0,.38/3], [.36,1.64,-3.74,-3.16,0,.38*2/3],
       [.36,1.64,-3.46,-3.16,0,.38]]
    b.add('Foundation_Entry_Union',ortho_solid(foundation_boxes),'stone','Foundation_Entry_Static','ground_root',0,
          {'union_boxes_m':foundation_boxes,'internal_faces_removed':True,'nonconvex_actual_bottom_area_m2':28.8048})
    for layer in spec['decks']:
        b.box(layer['name'],layer['bounds_m'],'secondary_wood',layer['name'],'floor_deck',1 if 'Ground' in layer['name'] else 2)
    # Ten independent columns per storey; no stock corner module or duplicate corner.
    for storey,width,z0,z1,group in [(1,.28,.38,2.80,'Structure_Lower_Static'),(2,.24,3.28,5.70,'Structure_Upper_Static')]:
        for i,(x,y) in enumerate(spec['structure']['post_centres_xy_m']):
            name='Post_S%d_%02d'%(storey,i);bounds=[x-width/2,x+width/2,y-width/2,y+width/2,z0,z1]
            b.box(name,bounds,'primary_timber',group,'main_post',storey)
            for wall in (['front'] if y==-3 else ['rear'] if y==3 else []) + (['left'] if x==-2 else ['right'] if x==2 else []):
                b.add_cut(wall,storey,name,bounds)
    # Every cap/ring has one corner owner: front/back full span, sides end at inner faces.
    for label,width,z0,z1,group,role,storey in [
       ('Cap_Lower',.30,2.80,2.98,'Structure_Lower_Static','wall_cap',1),
       ('TransferRing',.28,2.98,3.20,'FloorStructure_Upper_Static','transfer_ring',2),
       ('Cap_Upper',.26,5.70,5.88,'Structure_Upper_Static','wall_cap',2)]:
        for wall,y in [('front',-3),('rear',3)]:
            b.box(label+'_'+wall,[-2-width/2,2+width/2,y-width/2,y+width/2,z0,z1],
                  'primary_timber',group,role,storey)
        for wall,x in [('left',-2),('right',2)]:
            b.box(label+'_'+wall,[x-width/2,x+width/2,-3+width/2,3-width/2,z0,z1],
                  'primary_timber',group,role,storey)
    for name,bounds in [('Ledger_Left',[-1.88,-1.70,-2.8,2.8,3.00,3.04]),('Ledger_Right',[1.70,1.88,-2.8,2.8,3.00,3.04])]:
        b.box(name,bounds,'primary_timber','FloorStructure_Upper_Static','ledger',2,
              audit={'only_declared_structural_volume_embed':'20mm into corresponding side ring'})
    for i,y in enumerate(spec['structure']['joists']['y_centres_m']):
        b.box('Joist_%02d'%i,[-1.86,1.86,y-.06,y+.06,3.04,3.20],
              'primary_timber','FloorStructure_Upper_Static','joist',2)
    # Frame corner ownership is explicit; cut actual frame solids out of plaster.
    for op in spec['openings']:
        oid=op['id'];wall=op['wall'];storey=op['storey'];a=op['centre_along_wall_m']
        group='Structure_Lower_Static' if storey==1 else 'Structure_Upper_Static'
        zlo,zhi=op['clear_z_m'];jwidth,jdepth=op['jamb_section_m']
        offset=(op['rough_width_m']/2)
        for side,sgn in [('L',-1),('R',1)]:
            ja=a+sgn*offset
            zj0,zj1=op.get('jamb_z_m',[zlo,zhi])
            bounds=wall_box(wall,ja-jwidth/2,ja+jwidth/2,jdepth,zj0,zj1)
            cuts=[]
            if oid=='entry_front':cuts=[op['jamb_slot_bounds_m'][0 if side=='L' else 1]]
            name=oid+'_Jamb_'+side
            b.box(name,bounds,'primary_timber',group,'opening_jamb',storey,cuts=cuts,
                  audit={'actual_panel_slot_m':cuts,'no_uncut_jamb_panel_overlap':True})
            b.add_cut(wall,storey,name,bounds)
        hw,hd,hh=op['header_width_depth_height_m']
        bounds=wall_box(wall,a-hw/2,a+hw/2,hd,*op['header_z_m'])
        b.box(oid+'_Header',bounds,'primary_timber',group,'opening_header',storey)
        b.add_cut(wall,storey,oid+'_Header',bounds)
        if oid!='entry_front':
            sw=op['sill_width_m'];bounds=wall_box(wall,a-sw/2,a+sw/2,op['sill_depth_m'],*op['sill_z_m'])
            b.box(oid+'_Sill',bounds,'stone' if oid=='display_front' else 'secondary_wood',group,'opening_sill',storey)
            b.add_cut(wall,storey,oid+'_Sill',bounds)
        rw=op['rough_width_m'];raw=wall_box(wall,a-rw/2,a+rw/2,.60,*op['rough_z_m'])
        b.add_cut(wall,storey,oid+'_RoughOpening',raw)
        if oid=='entry_front':
            b.box('Entry_FixedPanel',[.490,1.510,-3.0225,-2.9775,.380,2.430],
                  'secondary_wood','DoorLeaf_Fixed_Static','fixed_closed_panel',1,
                  audit={'fixed_in_actual_jamb_slots':True,'operational_hinge':False,'no_gap':True})
        else:
            width=op['clear_width_m']
            b.box(oid+'_FixedGlazing',wall_box(wall,a-width/2,a+width/2,.030,zlo,zhi),
                  'fixed_glazing','Glazing_Fixed_Static','fixed_opaque_glazing',storey)
        b.openings.append(op)
    for storey,z0,z1,group in [(1,.38,2.80,'Infill_Lower_Static'),(2,3.28,5.70,'Infill_Upper_Static')]:
        for wall in ['front','rear','left','right']:
            a0,a1=(-2.11,2.11) if wall in ['front','rear'] else (-2.89,2.89)
            base=wall_box(wall,a0,a1,.22,z0,z1);cuts=b.cutters[(wall,storey)]
            b.box('Infill_S%d_%s'%(storey,wall),base,'plaster',group,'plaster_infill',storey,
                  cuts=[x['bounds_m'] for x in cuts],audit={'precut_bounds_m':base,'actual_scoped_cutters':cuts,
                  'remaining_wood_intersection_volume_expected':0,'no_generic_half_embed':True})
    # Four pitched trusses, new positive-area flat heel seats, continuous new deck.
    mount=5.88
    for i,y in enumerate(spec['roof']['trusses_y_m']):
        b.box('Roof_Tie_%02d'%i,[-2.08,2.08,y-.09,y+.09,mount,mount+.22],
              'primary_timber','Roof_Static','roof_tie',2)
        for side,sign in [('L',-1),('R',1)]:
            sec=[(sign*x,mount+z) for x,z in spec['roof']['right_rafter_section_xz_m']]
            b.add('Roof_Rafter_%02d_%s'%(i,side),prism_y(sec,y-.07,y+.07),
                  'primary_timber','Roof_Static','rafter',2)
    for side,sign in [('L',-1),('R',1)]:
        sec=[(0,mount+1.82),(sign*2.3,mount+1.82-.7*2.3),
             (sign*2.3,mount+1.96-.7*2.3),(0,mount+1.96)]
        b.add('Roof_Deck_'+side,prism_y(sec,-3.32,3.32),'clay','Roof_Static','roof_deck',2)
        # Broad staggered clay courses, with explicit narrow seams and real thickness.
        for row,(a0,a1) in enumerate([(.18,.85),(.86,1.56),(1.57,2.30)]):
            ys=[-3.32,-1.66,0,1.66,3.32] if row!=1 else [-3.32,-2.5,-.84,.82,2.48,3.32]
            for j,(y0,y1) in enumerate(zip(ys,ys[1:])):
                y0=y0 if j==0 else y0+.003;y1=y1 if j==len(ys)-2 else y1-.003
                z0=mount+1.96-.7*a0;z1=mount+1.96-.7*a1
                sec=[(sign*a0,z0),(sign*a1,z1),(sign*a1,z1+.035),(sign*a0,z0+.020)]
                b.add('Clay_%s_%d_%d'%(side,row,j),prism_y(sec,y0,y1),
                      'clay_light' if (row,j) in [(0,1),(2,0)] else 'clay','Roof_Static','clay_course',2)
    ridge=[(-.16,mount+1.848),(0,mount+1.96),(.16,mount+1.848),
           (.16,mount+1.948),(0,mount+2.06),(-.16,mount+1.948)]
    b.add('Roof_RidgeCap',prism_y(ridge,-3.32,3.32),'clay_light','Roof_Static','ridge_cap',2)
    for end,y in [('Front',-3),('Rear',3)]:
        # Two plaster half-panels have a true kingpost-shaped cut, not overlaid wood.
        for side,sign in [('L',-1),('R',1)]:
            sec=[(sign*.07,mount+.22),(sign*1.90,mount+.22),
                 (sign*1.90,mount+.27),(sign*.07,mount+1.551)]
            b.add('Gable_'+end+'_Plaster_'+side,prism_y(sec,y-.08,y+.08),
                  'plaster','Roof_Static','gable_plaster',2,
                  {'precut_plaster_bottom_m2':.608,'actual_plaster_total_bottom_m2':.5856})
        sec=[(x,mount+z) for x,z in spec['roof']['gable_kingpost']['local_section_xz_m']]
        b.add('Gable_'+end+'_Kingpost',prism_y(sec,y-.09,y+.09),
              'primary_timber','Roof_Static','gable_kingpost',2,
              {'actual_bottom_contact_m2':.0252,'actual_top_contact_each_m2':.07*math.sqrt(1.49)*.14})
    bpy.context.view_layer.update()
    return b


def build_eave_closures(b,delta,baseline):
    b.eave_delta=delta;b.original_baseline=baseline
    for record in delta['boards']:
        x0,x1=record['x_bounds_m'];right=x0>0;cuts=[]
        cut_x=[2.06,2.08] if right else [-2.08,-2.06]
        for y in delta['notches']['truss_y_m']:
            cuts += [[*cut_x,y-.09,y+.09,5.88,6.10],
                     [*cut_x,y-.07,y+.07,6.10,6.258]]
        vertices,faces=ortho_solid([[x0,x1,-3.09,3.09,5.88,6.258]],cuts)
        # On this bounded heel domain the actual rafter bottom is6.10 and its
        # top is the roof plane. This is the true intersection, not rafter AABB.
        vertices=[(x,y,7.70-.70*abs(x) if abs(z-6.258)<1e-10 else z) for x,y,z in vertices]
        made=b.add(record['component_id'],(vertices,faces),'primary_timber','Roof_Static','fixed_eave_closure',2,
             {'approved_delta_sha256':EAVE_DELTA_SHA256,'true_scoped_tie_rafter_notches':cuts,
              'top_plane':'z=7.70-.70absX','raw_volume_m3':.0899808,'remaining_volume_m3':.0851216,
              'continuous_outer_thickness_m':.02,'no_existing_component_modified':True})
        assert len(made)==1 and made[0]['component_id']==record['component_id'],'Eave closure split unexpectedly'
    bpy.context.view_layer.update()


def exact_native_state(obj):
    obj.data.calc_loop_triangles()
    vertices=[tuple(float(c) for c in obj.matrix_world@v.co) for v in obj.data.vertices]
    materials=[]
    for mat in obj.data.materials:
        node=mat.node_tree.nodes.get('Principled BSDF');assert node is not None
        materials.append(tuple(float(c) for c in node.inputs['Base Color'].default_value)+
            tuple(float(node.inputs[k].default_value) for k in ['Roughness','Metallic','Alpha']))
    records=[]
    for t in obj.data.loop_triangles:
        xyz=[vertices[i] for i in t.vertices]
        records.append((min(tuple(xyz[i:]+xyz[:i]) for i in range(3)),materials[t.material_index]))
    return {'vertices_exact_sha256':digest_json(sorted(vertices)),
            'oriented_triangles_exact_pbr_sha256':digest_json(sorted(records)),
            'role':obj['structural_role'],'storey':obj['storey'],
            'parent_role':obj.parent['static_group_role'],'static_parent_group':obj['static_parent_group']}


def exact_glb_states(raw):
    import struct
    cursor=12;doc=binary=None
    while cursor<len(raw):
        size,kind=struct.unpack_from('<I4s',raw,cursor);chunk=raw[cursor+8:cursor+8+size];cursor+=8+size
        if kind==b'JSON':doc=json.loads(chunk.rstrip(b' \0'))
        elif kind==b'BIN\0':binary=chunk
    assert doc is not None and binary is not None
    def accessor(index):
        a=doc['accessors'][index];view=doc['bufferViews'][a['bufferView']]
        n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        code={5126:'f',5125:'I',5123:'H',5121:'B'}[a['componentType']]
        stride=view.get('byteStride',struct.calcsize('<'+code)*n)
        start=view.get('byteOffset',0)+a.get('byteOffset',0)
        return [struct.unpack_from('<'+code*n,binary,start+i*stride) for i in range(a['count'])]
    parents={child:i for i,node in enumerate(doc['nodes']) for child in node.get('children',[])}
    result={}
    for index,node in enumerate(doc['nodes']):
        if 'mesh' not in node:continue
        cid=node['extras']['component_id'];assert cid not in result
        records=[]
        for primitive in doc['meshes'][node['mesh']]['primitives']:
            assert primitive.get('mode',4)==4
            positions=accessor(primitive['attributes']['POSITION'])
            normals=accessor(primitive['attributes']['NORMAL'])
            indices=[v[0] for v in accessor(primitive['indices'])]
            material=doc['materials'][primitive['material']]
            pbr={k:material.get(k) for k in ['pbrMetallicRoughness','alphaMode','alphaCutoff','doubleSided']}
            for start in range(0,len(indices),3):
                corners=[(positions[i],normals[i]) for i in indices[start:start+3]]
                records.append((min(tuple(corners[j:]+corners[:j]) for j in range(3)),digest_json(pbr)))
        chain=[];current=index
        while True:
            ancestor=doc['nodes'][current]
            chain.append({k:ancestor[k] for k in ['matrix','translation','rotation','scale'] if k in ancestor})
            if current not in parents:break
            current=parents[current]
        result[cid]={'oriented_position_normal_pbr_exact_sha256':digest_json(sorted(records)),
            'transform_chain':chain,'role':node['extras']['structural_role'],'storey':node['extras']['storey'],
            'static_parent_group':node['extras']['static_parent_group']}
    return result


def preserve_original_165(b):
    expected=b.original_baseline['native'];actual={o['component_id']:o for o in b.parts}
    assert len(expected)==165 and set(actual)==set(expected)|{'EaveClosure_Left','EaveClosure_Right'}
    for cid,state in expected.items():
        assert exact_native_state(actual[cid])==state,('Original exact native geometry/PBR/identity changed',cid)
    return {'passed':True,'original_components':165,'comparison':'unrounded actual world vertex multiset and oriented triangle/full-float PBR hashes plus identity/parent roles',
            'frozen_native_sha256':b.original_baseline['native_sha256'],'baseline_sha256':ORIGINAL_BASELINE_SHA256}


def eave_contacts(b,m):
    records=[]
    for side,deck,orientation in [('Left','L','-X'),('Right','R','+X')]:
        child=b.one('EaveClosure_'+side)
        for wall,area in [(side.lower(),.2224),('front',.0052),('rear',.0052)]:
            records.append(m.require(child,b.one('Cap_Upper_'+wall),area,'up','MANDATORY_eave_'+side+'_cap_'+wall))
        for i in range(4):
            tie=b.one('Roof_Tie_%02d'%i);rafter=b.one('Roof_Rafter_%02d_%s'%(i,deck))
            for parent,area,direction,label in [(tie,.0008,'up','tie_horizontal'),(tie,.0396,orientation,'tie_end'),
                    (rafter,.02016,orientation,'rafter_end')]:
                records.append(m.require(child,parent,area,direction,'MANDATORY_eave_%s_%02d_%s'%(side,i,label)))
        records.append(m.require(b.one('Roof_Deck_'+deck),child,.236*math.sqrt(1.49),'up','MANDATORY_eave_'+side+'_roof_slope'))
    assert len(records)==32
    return records


def convex_piece(vertices,faces):
    vv=[Vector(v) for v in vertices];axes={};edges={}
    def add(pool,vector):
        if vector.length<1e-10:return
        vector=vector.normalized()
        for c in vector:
            if abs(c)>1e-9:
                if c<0:vector=-vector
                break
        pool[tuple(round(float(c),8) for c in vector)]=vector
    for face in faces:
        a,b,c=[vv[i] for i in face[:3]];add(axes,(b-a).cross(c-a))
        for i,j in zip(face,face[1:]+face[:1]):add(edges,vv[j]-vv[i])
    return {'vertices':vv,'normals':list(axes.values()),'edges':list(edges.values())}


def convex_sat_overlap(a,b):
    axes=a['normals']+b['normals']
    axes += [x.cross(y).normalized() for x in a['edges'] for y in b['edges'] if x.cross(y).length>1e-8]
    minimum=float('inf')
    for n in axes:
        aa=[v.dot(n) for v in a['vertices']];bb=[v.dot(n) for v in b['vertices']]
        overlap=min(max(aa),max(bb))-max(min(aa),min(bb));minimum=min(minimum,overlap)
        if overlap<=2e-6:return False,overlap
    return True,minimum


def actual_eave_convex_cells(obj):
    # Derive the cell arrangement from the actual closed surface, then use its
    # actual inside classifications. AABB alone never determines occupied cells.
    triangles=triangle_records(obj);vertices=[obj.matrix_world@v.co for v in obj.data.vertices]
    xs=sorted(set(float(v.x) for v in vertices));ys=sorted(set(float(v.y) for v in vertices))
    horizontal=sorted(set(float(t['p'][0].z) for t in triangles if abs(t['n'].z)>.99999))
    roof=[t for t in triangles if .5<t['n'].z<.99999];assert roof,('No actual eave slope',obj.name)
    n=roof[0]['n'];d=n.dot(roof[0]['p'][0])
    assert all(abs(n.dot(p)-d)<2e-6 for t in roof for p in t['p']),('Eave roof planes disagree',obj.name)
    assert all(max(abs(c) for c in t['n'])>.99999 or t in roof for t in triangles),('Unpartitioned eave surface plane',obj.name)
    assert len(xs)==3 and len(horizontal)==2,('Unexpected actual eave arrangement',obj.name,xs,horizontal)
    tree=actual_tree(obj);cells=[];volume=0
    faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            for iz,z0 in enumerate(horizontal):
                z1=horizontal[iz+1] if iz+1<len(horizontal) else None
                top=[z1 if z1 is not None else (d-n.x*x-n.y*y)/n.z for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]]
                centre=Vector(((x0+x1)/2,(y0+y1)/2,(z0+sum(top)/4)/2))
                classifications=[inside(tree,centre,direction) for direction in RAY_DIRS]
                assert all(classifications) or not any(classifications),('Ambiguous actual eave cell',obj.name,rounded(centre),classifications)
                if not any(classifications):continue
                vv=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)]+[(x,y,z) for (x,y),z in zip([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],top)]
                cells.append(convex_piece(vv,faces));volume+=(x1-x0)*(y1-y0)*(sum(top)/4-z0)
    measured=topology(obj)['positive_volume_m3']
    assert abs(volume-measured)<1e-7,('Actual eave convex partition volume mismatch',obj.name,volume,measured)
    # Float32 coordinates at X2m/Z6m bound this new small solid's expected-volume
    # error; this does not relax any contact, collision, old topology or ledger gate.
    assert abs(measured-.0851216)<2e-7,('Actual eave volume differs from delta',obj.name,measured)
    return cells,{'component_id':obj['component_id'],'actual_convex_cell_count':len(cells),
        'actual_mesh_volume_m3':measured,'actual_cell_sum_volume_m3':volume,'expected_volume_m3':.0851216}


def eave_zero_intersections(b):
    rows=[];partitions=[];new=[b.one('EaveClosure_'+s) for s in ['Left','Right']]
    for obj in new:
        cells,partition=actual_eave_convex_cells(obj);partitions.append(partition)
        for other in b.parts:
            if other==obj or other in new:continue
            aa,bb=bounds(obj),bounds(other)
            overlap=[min(aa[2*i+1],bb[2*i+1])-max(aa[2*i],bb[2*i]) for i in range(3)]
            if any(x<=2e-6 for x in overlap):continue
            triangles=triangle_records(other);vertices=[other.matrix_world@v.co for v in other.data.vertices]
            assert all((v-t['p'][0]).dot(t['n'])<=2e-6 for t in triangles for v in vertices),('Unresolved nonconvex eave neighbor',obj.name,other.name)
            piece=convex_piece(vertices,[tuple(p.vertices) for p in other.data.polygons])
            for index,cell in enumerate(cells):
                collision,depth=convex_sat_overlap(cell,piece)
                assert not collision,('Forbidden eave volume overlap',obj.name,other.name,index,depth)
            rows.append({'new_component':obj['component_id'],'neighbor':other['component_id'],'convex_cells_tested':len(cells),'forbidden_overlap':False})
    assert bounds(new[0])[1]<bounds(new[1])[0]
    return {'passed':True,'screened_new_old_pairs':330,'new_new_pairs':1,'actual_positive_AABB_pairs':rows,
        'actual_mesh_convex_partitions':partitions,'allowed_new_overlaps':0,'SAT_depth_numeric_bound_m':2e-6,
        'method':'actual closed eave planes + actual per-cell inside classification and volume equality; proved-convex actual neighbors; all face/edge-cross SAT axes'}


def eave_negative_fixtures(b,m):
    records=[];baseline={s:exact_native_state(b.one('EaveClosure_'+s)) for s in ['Left','Right']}
    missing=[]
    # One lift fixture type, both real boards, all three required cap seats each.
    for side in ['Left','Right']:
        obj=b.one('EaveClosure_'+side);original=[v.co.copy() for v in obj.data.vertices]
        try:
            for v in obj.data.vertices:v.co+=Vector((0,0,.01))
            obj.data.update();m.clear()
            for wall,area in [(side.lower(),.2224),('front',.0052),('rear',.0052)]:
                label='eave_Z_plus_10mm_'+side+'_required_cap_'+wall
                try:m.require(obj,b.one('Cap_Upper_'+wall),area,'up',label)
                except AssertionError as error:
                    assert 'required_contact_failed' in str(error)
                    missing.append({'board':side,'cap':wall,'failure':str(error)[:1000]})
                else:raise AssertionError(('Eave lift negative cap falsely passed',side,wall))
        finally:
            for v,co in zip(obj.data.vertices,original):v.co=co
            obj.data.update();m.clear()
    assert len(missing)==6
    records.append({'fixture':'each_eave_Z_plus_10mm_all_three_required_caps','rejected':True,'required_failed_cap_rows':missing})
    obj=b.one('EaveClosure_Left');original=[v.co.copy() for v in obj.data.vertices]
    name='eave_inward_X20mm_required_real_tie_end'
    try:
        for v in obj.data.vertices:v.co+=Vector((.02,0,0))
        obj.data.update();m.clear()
        try:m.require(obj,b.one('Roof_Tie_01'),.0396,'-X',name)
        except AssertionError as error:
            assert 'required_contact_failed' in str(error)
            records.append({'fixture':name,'rejected':True,'failure':str(error)[:1000]})
        else:raise AssertionError(('Eave inward negative fixture falsely passed',name))
    finally:
        for v,co in zip(obj.data.vertices,original):v.co=co
        obj.data.update();m.clear()
    assert all(exact_native_state(b.one('EaveClosure_'+s))==state for s,state in baseline.items()),'Eave fixture changed final mesh/PBR'
    return records


def triangle_records(obj):
    obj.data.calc_loop_triangles()
    vv=[obj.matrix_world@v.co for v in obj.data.vertices]
    out=[]
    for ti,t in enumerate(obj.data.loop_triangles):
        pts=[vv[i].copy() for i in t.vertices]
        cross=(pts[1]-pts[0]).cross(pts[2]-pts[0]);area=cross.length/2
        assert area>1e-12,('Degenerate triangle',obj.name,ti)
        n=cross.normalized()
        out.append({'p':pts,'n':n,'area':area,'index':ti,'material_index':t.material_index,
                    'lo':[min(v[i] for v in pts) for i in range(3)],
                    'hi':[max(v[i] for v in pts) for i in range(3)]})
    return out


def pbr_signature(mat):
    assert mat.use_nodes
    node=mat.node_tree.nodes.get('Principled BSDF');assert node is not None
    return tuple(round(float(v),6) for v in node.inputs['Base Color'].default_value)+(round(float(node.inputs['Roughness'].default_value),6),round(float(node.inputs['Metallic'].default_value),6))


def oriented_fingerprint(obj):
    result=[]
    for t in triangle_records(obj):
        xyz=[tuple(round(float(c),5) for c in p) for p in t['p']]
        canonical=min(tuple(xyz[i:]+xyz[:i]) for i in range(3))
        result.append((canonical,pbr_signature(obj.data.materials[t['material_index']])))
    return digest_json(sorted(result))


def topology(obj):
    # A glTF normal seam may repeat exactly equal positions. Analyze a temporary
    # per-component index quotient, never weld/move source/imported vertices.
    # Exact tuple equality only: a nonzero crack of any size remains a crack.
    positions=[];canonical={};vertex_ids=[]
    for vertex in obj.data.vertices:
        key=tuple(float(c) for c in vertex.co)
        assert len(key)==3 and all(math.isfinite(c) for c in key),('Nonfinite vertex',obj.name,key)
        if key not in canonical:
            canonical[key]=len(positions);positions.append(key)
        vertex_ids.append(canonical[key])
    edges=defaultdict(list);incident=defaultdict(set);faces=[];seen=set()
    collapsed=duplicate=degenerate=0;volume=0.0
    for polygon in obj.data.polygons:
        face=tuple(vertex_ids[i] for i in polygon.vertices);fi=len(faces);faces.append(face)
        if len(face)<3 or len(set(face))!=len(face):collapsed+=1;continue
        identity=tuple(sorted(face))
        if identity in seen:duplicate+=1
        seen.add(identity)
        for a,b in zip(face,face[1:]+face[:1]):
            edges[min(a,b),max(a,b)].append((fi,a,b));incident[a].add(fi)
        a=positions[face[0]];area=0.0
        for i in range(1,len(face)-1):
            b=positions[face[i]];c=positions[face[i+1]]
            u=tuple(b[k]-a[k] for k in range(3));v=tuple(c[k]-a[k] for k in range(3))
            cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
            area+=math.sqrt(sum(t*t for t in cross))/2
            volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        if area<1e-12:degenerate+=1
    bad=sum(len(links)!=2 for links in edges.values())
    same_direction=sum(len(links)==2 and (links[0][1],links[0][2])!=(links[1][2],links[1][1]) for links in edges.values())
    loose=sum(i not in incident for i in range(len(positions)))
    # Edge-manifold alone allows two closed shells touching at one vertex.
    # Each vertex's incident-face fan must form one connected component.
    fan_links=defaultdict(lambda:defaultdict(set))
    for (a,b),links in edges.items():
        if len(links)==2:
            f,g=links[0][0],links[1][0]
            for vertex in (a,b):fan_links[vertex][f].add(g);fan_links[vertex][g].add(f)
    bad_fans=0
    for vertex,around in incident.items():
        reached=set();pending=[next(iter(around))]
        while pending:
            face=pending.pop()
            if face in reached:continue
            reached.add(face);pending.extend(fan_links[vertex][face]-reached)
        if reached!=around:bad_fans+=1
    result={'closed':True,'nonmanifold_edges':bad,'same_direction_edges':same_direction,
            'nonmanifold_vertex_fans':bad_fans,'loose_vertices':loose,'degenerate_faces':degenerate,
            'collapsed_faces':collapsed,'duplicate_faces':duplicate,'positive_volume_m3':volume,
            'method':'per-component-exact-position-index-quotient','position_merge_distance_m':0.0,
            'input_vertices':len(vertex_ids),'exact_positions':len(positions),'faces_retained':len(faces)}
    assert bad==same_direction==bad_fans==loose==degenerate==collapsed==duplicate==0 and volume>1e-10,('Topology failed',obj.name,result)
    return result


def bounds(obj):
    vv=[obj.matrix_world@v.co for v in obj.data.vertices]
    return [q for i in range(3) for q in [min(v[i] for v in vv),max(v[i] for v in vv)]]


def polygon_clip(subject, clip):
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    orientation=1 if cross(clip[0],clip[1],clip[2])>=0 else -1
    for a,b in zip(clip,clip[1:]+clip[:1]):
        previous=subject;subject=[]
        if not previous:break
        p=previous[-1];dp=orientation*cross(a,b,p)
        for q in previous:
            dq=orientation*cross(a,b,q)
            if (dq>=-1e-10)!=(dp>=-1e-10):
                f=dp/(dp-dq);subject.append((p[0]+f*(q[0]-p[0]),p[1]+f*(q[1]-p[1])))
            if dq>=-1e-10:subject.append(q)
            p=q;dp=dq
    return subject


def overlap_area(aa,bb,normal):
    axis=max(range(3),key=lambda k:abs(normal[k]));uv=[k for k in range(3) if k!=axis]
    poly=polygon_clip([(v[uv[0]],v[uv[1]]) for v in aa],[(v[uv[0]],v[uv[1]]) for v in bb])
    if len(poly)<3:return 0
    area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
    return area/abs(normal[axis])


class Measurements:
    def __init__(self):self.cache={}
    def triangles(self,obj):
        if obj.name not in self.cache:self.cache[obj.name]=triangle_records(obj)
        return self.cache[obj.name]
    def clear(self):self.cache.clear()
    def touch(self,child,parent,orientation='up'):
        total=0;patches=[]
        for a in self.triangles(child):
            for b in self.triangles(parent):
                if orientation=='up' and b['n'].z<.5:continue
                if orientation in ['+X','-X','+Y','-Y','+Z','-Z']:
                    axis='XYZ'.index(orientation[1]);sgn=1 if orientation[0]=='+' else -1
                    if b['n'][axis]*sgn<.999:continue
                if a['n'].dot(b['n'])>-.999:continue
                if any(a['hi'][k]<b['lo'][k]-EPS or b['hi'][k]<a['lo'][k]-EPS for k in range(3)):continue
                gap=max(abs((p-a['p'][0]).dot(a['n'])) for p in b['p'])
                if gap>EPS:continue
                area=overlap_area(a['p'],b['p'],a['n'])
                if area>1e-9:
                    total+=area;patches.append({'child_triangle':a['index'],'parent_triangle':b['index'],
                                                'area_m2':area,'plane_gap_m':gap,'parent_normal':rounded(b['n'])})
        return {'child':child['component_id'],'parent':parent['component_id'],'type':'opposed-face_'+orientation,
                'area_m2':total,'plane_tolerance_m':EPS,'patches':patches}
    def require(self,child,parent,minimum,orientation='up',label=None):
        record=self.touch(child,parent,orientation);record['minimum_design_area_m2']=minimum
        record['required_at_least_m2']=minimum*AREA_FRACTION;record['label']=label or child.name+' / '+parent.name
        assert record['area_m2']>=minimum*AREA_FRACTION,('required_contact_failed',record)
        record['passed']=True;return record


def actual_tree(obj):
    vv=[obj.matrix_world@v.co for v in obj.data.vertices]
    return BVHTree.FromPolygons(vv,[list(p.vertices) for p in obj.data.polygons],all_triangles=False,epsilon=0)


def inside(tree,point,direction):
    p=Vector(point);hits=0
    for _ in range(10000):
        hit,normal,index,distance=tree.ray_cast(p,direction)
        if hit is None:return hits%2==1
        hits+=1;p=hit+direction*1e-5
    raise AssertionError('Inside ray did not terminate')


def box_proof(obj):
    bs=bounds(obj);tr=triangle_records(obj);top=topology(obj)
    assert all(max(abs(c) for c in t['n'])>.99999 for t in tr),('Not axis-aligned box',obj.name)
    expected=math.prod(bs[2*k+1]-bs[2*k] for k in range(3))
    assert abs(top['positive_volume_m3']-expected)<1e-7,('Not full closed box volume',obj.name)
    return bs


def ledger_embed(child,parent,side):
    cb,pb=box_proof(child),box_proof(parent)
    lo=[max(cb[2*i],pb[2*i]) for i in range(3)];hi=[min(cb[2*i+1],pb[2*i+1]) for i in range(3)]
    ext=[hi[i]-lo[i] for i in range(3)]
    assert all(v>0 for v in ext) and abs(ext[0]-.02)<EPS and abs(math.prod(ext)-.00448)<1e-7
    tc,tp=actual_tree(child),actual_tree(parent);anchors=[]
    for y in [-2,0,2]:
        p=Vector(((lo[0]+hi[0])/2,y,(lo[2]+hi[2])/2));checks=[]
        for tree in [tc,tp]:
            near=tree.find_nearest(p);classifications=[inside(tree,p,d) for d in RAY_DIRS]
            assert all(classifications) and near[3]>=.002,('Ledger scoped real overlap failed',side,rounded(p),classifications,near[3])
            checks.append({'all_three_rays_inside':True,'surface_clearance_m':near[3]})
        anchors.append({'world_m':rounded(p),'both_meshes':checks})
    return {'child':child['component_id'],'parent':parent['component_id'],'type':'scoped_20mm_ledger_embed',
            'actual_intersection_bounds_m':[q for i in range(3) for q in [lo[i],hi[i]]],
            'actual_box_intersection_volume_m3':math.prod(ext),'actual_depth_m':ext[0],'anchors':anchors,'passed':True}


def horizontal_face_area(obj,z,normal_sign=1,clip_rect=None):
    total=0
    for t in triangle_records(obj):
        if t['n'].z*normal_sign<.999 or max(abs(p.z-z) for p in t['p'])>EPS:continue
        if clip_rect is None:total+=t['area'];continue
        x0,x1,y0,y1=clip_rect
        poly=polygon_clip([(v.x,v.y) for v in t['p']],[(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
        if len(poly)>=3:total+=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
    return total


def foundation_domains(b):
    obj=b.one('Foundation_Entry_Union')
    main=horizontal_face_area(obj,0,-1,[-2.18,2.18,-3.18,3.18])
    total=horizontal_face_area(obj,0,-1)
    top=horizontal_face_area(obj,.30,1)
    records={'main_lower_domain_ground_m2':main,'actual_nonconvex_union_ground_m2':total,
             'actual_union_z0p30_upward_m2':top,'expected':{'main':27.7296,'union':28.8048,'union_top':28.1088}}
    assert abs(main-27.7296)<.0001 and abs(total-28.8048)<.0001 and abs(top-28.1088)<.0001,records
    bs=bounds(obj);assert abs(bs[4])<EPS,bs
    for z,expected in [(.38/3,1.28*.28),(.38*2/3,1.28*.28),(.38,1.28*.30)]:
        actual=horizontal_face_area(obj,z,1)
        assert abs(actual-expected)<.0001,('Entry tread domain',z,actual,expected)
    return records


def check_column_grid(b):
    checked=[]
    for storey,width,z0,z1 in [(1,.28,.38,2.80),(2,.24,3.28,5.70)]:
        for i,(x,y) in enumerate(b.spec['structure']['post_centres_xy_m']):
            bs=bounds(b.one('Post_S%d_%02d'%(storey,i)))
            actual=[(bs[0]+bs[1])/2,(bs[2]+bs[3])/2,bs[4],bs[5]]
            expected=[x,y,z0,z1]
            assert max(abs(a-c) for a,c in zip(actual,expected))<EPS,('column_grid_failed',storey,i,actual,expected)
            assert abs(bs[1]-bs[0]-width)<EPS and abs(bs[3]-bs[2]-width)<EPS
            checked.append({'storey':storey,'index':i,'actual_centre_xy_z_extents':actual})
    return checked


def aperture_measurements(b,additional_objects=()):
    # Filled leaf/glazing are intentionally excluded; all walls and fixed frames remain.
    pool=[o for o in b.parts if o['structural_role'] not in ['fixed_closed_panel','fixed_opaque_glazing']]+list(additional_objects)
    trees={o.name:actual_tree(o) for o in pool};reports=[]
    for op in b.openings:
        wall=op['wall'];a=op['centre_along_wall_m'];w=op['clear_width_m'];z0,z1=op['clear_z_m'];rays=[]
        for f in [.10,.50,.90]:
            for g in [.10,.50,.90]:
                along=a-w/2+w*f;z=z0+(z1-z0)*g
                if wall in ['front','rear']:
                    c=-3 if wall=='front' else 3;origin=Vector((along,c-.4,z));direction=Vector((0,1,0))
                else:
                    c=-2 if wall=='left' else 2;origin=Vector((c-.4,along,z));direction=Vector((1,0,0))
                hits=[]
                for obj in pool:
                    hit,n,idx,d=trees[obj.name].ray_cast(origin,direction,.8)
                    if hit is not None:hits.append({'component':obj.get('component_id',obj.name),'distance_m':d})
                assert not hits,('aperture_blocked',op['id'],rounded(origin),hits)
                rays.append({'start_m':rounded(origin),'direction':rounded(direction),'length_m':.8,'hits':[]})
        left=b.one(op['id']+'_Jamb_L');right=b.one(op['id']+'_Jamb_R')
        axis=0 if wall in ['front','rear'] else 1
        # Evaluate the jamb throat on the outer front/back surface, away from the real panel slot.
        lb,rb=bounds(left),bounds(right)
        clear_width=rb[2*axis]-lb[2*axis+1]
        header_bottom=bounds(b.one(op['id']+'_Header'))[4]
        sill_top=.38 if op['id']=='entry_front' else bounds(b.one(op['id']+'_Sill'))[5]
        assert abs(clear_width-w)<EPS and abs(header_bottom-sill_top-op['clear_height_m'])<EPS,('Frame throat',op['id'],clear_width,header_bottom,sill_top)
        reports.append({'opening':op['id'],'frame_minimum_width_m':clear_width,
                        'frame_height_m':header_bottom-sill_top,'fixed_fill_excluded':True,
                        'true_through_wall_rays':rays,'no_passage_claim':True})
    return reports


def require_joist_end(b,m,index,side):
    key='Ledger_'+side
    assert key in b.objects and b.objects[key] in b.parts,('required_contact_failed','Missing actual ledger',index,side)
    return m.require(b.one('Joist_%02d'%index),b.one(key),.0192,'up',
                     'MANDATORY_joist_%02d_%s_end'%(index,side))


def required_contacts(b,m):
    records=[];one=b.one
    def req(c,p,a,orientation='up',label=None):
        rec=m.require(one(c),one(p),a,orientation,label);records.append(rec);return rec
    req('Floor_Ground_Static','Foundation_Entry_Union',27.3024)
    req('Floor_Ground_Static','Foundation_Entry_Union',1.28*.08,'+Y','entry_landing_to_deck_vertical_interface')
    for storey,section,floor,cap in [(1,.28,'Floor_Ground_Static','Cap_Lower'),(2,.24,'Floor_Upper_Static','Cap_Upper')]:
        for i,(x,y) in enumerate(b.spec['structure']['post_centres_xy_m']):
            post='Post_S%d_%02d'%(storey,i)
            req(post,floor,section**2,label='MANDATORY_column_base_'+post)
            owner='front' if y==-3 else 'rear' if y==3 else 'left' if x==-2 else 'right'
            req(cap+'_'+owner,post,section**2,label='MANDATORY_column_head_'+post)
    for wall in ['front','rear','left','right']:
        area=(4.28*.28) if wall in ['front','rear'] else (5.72*.28)
        req('TransferRing_'+wall,'Cap_Lower_'+wall,area)
        req('Floor_Upper_Static','TransferRing_'+wall,area)
    for side in ['Left','Right']:
        records.append(ledger_embed(one('Ledger_'+side),one('TransferRing_'+side.lower()),side))
    for i in range(9):
        joist='Joist_%02d'%i
        for side in ['Left','Right']:
            rec=require_joist_end(b,m,i,side);records.append(rec)
        req('Floor_Upper_Static',joist,.4464,label='MANDATORY_joist_%02d_deck'%i)
    for op in b.openings:
        oid=op['id'];floor='Floor_Ground_Static' if op['storey']==1 else 'Floor_Upper_Static'
        jarea=op['jamb_section_m'][0]*op['jamb_section_m'][1]
        for side in ['L','R']:
            jamb=oid+'_Jamb_'+side
            if oid=='entry_front':jarea=.14*.28-.02*.045
            req(oid+'_Header',jamb,jarea)
            if oid in ['entry_front','display_front']:
                req(jamb,floor,jarea)
            else:
                req(jamb,oid+'_Sill',jarea)
        if oid=='entry_front':
            req('Entry_FixedPanel',floor,.0459)
            req(oid+'_Header','Entry_FixedPanel',.0459)
            for side in ['L','R']:
                req('Entry_FixedPanel',oid+'_Jamb_'+side,.09225,'+X' if side=='L' else '-X','fixed_panel_actual_slot_end_'+side)
        else:
            # Window sill must have an actual upward plaster recess seat; tested per actual shell.
            sill=one(oid+'_Sill');candidates=[o for o in b.parts if o['structural_role']=='plaster_infill' and o['storey']==op['storey']]
            actual=[m.touch(sill,o,'up') for o in candidates];actual=[r for r in actual if r['area_m2']>1e-8]
            area=sum(r['area_m2'] for r in actual);minimum=op['sill_width_m']*.22
            assert area>=minimum*.95,('required_sill_recess_failed',oid,area,minimum)
            for rec in actual:rec.update({'passed':True,'scope':'actual sill recess seat'});records.append(rec)
            glass=oid+'_FixedGlazing'  # req resolves component IDs exactly once.
            req(oid+'_Header',glass,.03*op['clear_width_m'])
            req(glass,oid+'_Sill',.03*op['clear_width_m'])
            for side in ['L','R']:
                axis='X' if op['wall'] in ['front','rear'] else 'Y'
                req(glass,oid+'_Jamb_'+side,.03*op['clear_height_m'],('+' if side=='L' else '-')+axis)
    for i,y in enumerate(b.spec['roof']['trusses_y_m']):
        tie='Roof_Tie_%02d'%i
        if y in [-3,3]:req(tie,'Cap_Upper_'+('front' if y==-3 else 'rear'),4.16*.18)
        else:
            for side in ['left','right']:req(tie,'Cap_Upper_'+side,.0378)
        for side in ['L','R']:
            rafter='Roof_Rafter_%02d_%s'%(i,side)
            req(rafter,tie,.0152,label='MANDATORY_rafter_heel_'+rafter)
            req('Roof_Deck_'+side,rafter,2.08*math.sqrt(1.49)*.14)
    for end,i in [('Front',0),('Rear',3)]:
        tie='Roof_Tie_%02d'%i
        req('Gable_'+end+'_Kingpost',tie,.0252)
        for side in ['L','R']:
            req('Gable_'+end+'_Plaster_'+side,tie,.5856/2)
            req('Roof_Rafter_%02d_%s'%(i,side),'Gable_'+end+'_Kingpost',.07*math.sqrt(1.49)*.14)
            req('Roof_Rafter_%02d_%s'%(i,side),'Gable_'+end+'_Plaster_'+side,(1.9-.07)*math.sqrt(1.49)*.14)
    for child in b.parts:
        if child['structural_role']=='clay_course':
            side='L' if child.name.startswith('Clay_L') else 'R'
            rec=m.touch(child,one('Roof_Deck_'+side),'up');assert rec['area_m2']>.1,('Unseated clay course',child.name,rec)
            rec.update({'passed':True,'scope':'clay bottom actual sloping seat'});records.append(rec)
    for side in ['L','R']:req('Roof_RidgeCap','Roof_Deck_'+side,.16*math.sqrt(1.49)*6.64)
    return records


def infill_supports(b,m):
    records=[]
    for infill in [o for o in b.parts if o['structural_role']=='plaster_infill']:
        parents=[o for o in b.parts if o!=infill and o['storey']==infill['storey'] and
                 o['structural_role'] in ['floor_deck','opening_header','opening_sill','opening_jamb','main_post']]
        found=[]
        for obj in parents:
            # Only actual opposed upward faces, never arbitrary bounding-box overlap.
            rec=m.touch(infill,obj,'up')
            if rec['area_m2']>1e-6:rec.update({'passed':True,'scope':'infill shell direct upward geometric seat'});found.append(rec)
        assert found,('Unsupported infill source shell',infill.name)
        records+=found
    return records


def check_support_graph(b,records):
    # Directed child -> support. Mandatory column bases/heads and all eighteen
    # joist-end seats were checked individually before this supplemental closure.
    # Reverse reachability is cycle-safe and cannot memoize a temporary DFS
    # back-edge failure as a permanent failure of a genuinely supported child.
    reverse=defaultdict(set)
    for record in records:
        assert record.get('passed')
        reverse[record['parent']].add(record['child'])
    root='Foundation_Entry_Union'
    reached={root};queue=deque([root])
    while queue:
        for child in sorted(reverse[queue.popleft()]):
            if child not in reached:
                reached.add(child);queue.append(child)
    missing=[o['component_id'] for o in b.parts if o['component_id'] not in reached]
    assert not missing,('No directed geometric support route',missing)
    return {'root':root,'all_component_ids_reach_ground':True,
            'algorithm':'cycle-safe ground-root reverse reachability closure',
            'mandatory_bearing_rows_cannot_be_waived':True,
            'component_count':len(b.parts),'edge_count':len(records)}


def coplanar_skin_gate(b):
    # This design has no permitted duplicate co-oriented skin, even inside a hidden contact.
    # Opposite-face intended contacts are excluded by the normal test, not a blanket exemption.
    bins=defaultdict(list)
    for obj in b.parts:
        for t in triangle_records(obj):
            key=tuple(round(float(v),4) for v in t['n'])
            bins[key].append((obj,t))
    conflicts=[]
    for items in bins.values():
        for i,(a,ta) in enumerate(items):
            for bb,tb in items[i+1:]:
                if a==bb:continue
                if any(ta['hi'][k]<tb['lo'][k]-EPS or tb['hi'][k]<ta['lo'][k]-EPS for k in range(3)):continue
                if ta['n'].dot(tb['n'])<.999:continue
                gap=max(abs((p-ta['p'][0]).dot(ta['n'])) for p in tb['p'])
                if gap>0.0001:continue
                area=overlap_area(ta['p'],tb['p'],ta['n'])
                if area>1e-7:conflicts.append({'a':a.name,'b':bb.name,'area_m2':area,'gap_m':gap})
    assert not conflicts,('Exposed or duplicate co-oriented skin',conflicts[:20])
    return {'conflicts':[],'scope':'all inter-component same-facing coplanar triangle skins; no visibility loophole',
            'plane_tolerance_m':.0001,'minimum_area_m2':1e-7}


def negative_fixtures(b,m):
    out=[];baseline={o.name:oriented_fingerprint(o) for o in b.parts}
    def must_reject(name,action,marker):
        try:action()
        except AssertionError as exc:
            assert marker in str(exc),('Unexpected failure in negative fixture',name,str(exc))
            out.append({'fixture':name,'rejected':True,'failure':str(exc)[:1000]})
        else:raise AssertionError(('Negative fixture falsely passed',name))
    def shifted(obj,delta,action):
        old=[v.co.copy() for v in obj.data.vertices]
        try:
            for v in obj.data.vertices:v.co+=Vector(delta)
            obj.data.update();m.clear();action()
        finally:
            for v,co in zip(obj.data.vertices,old):v.co=co
            obj.data.update();m.clear()
    must_reject('post_Z_plus_20mm_required_base',lambda:shifted(b.one('Post_S1_00'),(0,0,.02),
        lambda:m.require(b.one('Post_S1_00'),b.one('Floor_Ground_Static'),.28**2)), 'required_contact_failed')
    must_reject('upper_deck_Z_plus_10mm',lambda:shifted(b.one('Floor_Upper_Static'),(0,0,.01),
        lambda:m.require(b.one('Floor_Upper_Static'),b.one('TransferRing_front'),4.28*.28)), 'required_contact_failed')
    must_reject('upper_column_X_plus_20mm_exact_grid',lambda:shifted(b.one('Post_S2_00'),(.02,0,0),lambda:check_column_grid(b)), 'column_grid_failed')
    # Remove the real source ledger from the scene and exact validator lookup.
    # Invoke the same necessary-end validator used by the positive geometry gate.
    ledger=b.one('Ledger_Left');position=b.parts.index(ledger);missing=[]
    b.parts.remove(ledger);del b.objects['Ledger_Left'];b.scene.collection.objects.unlink(ledger)
    try:
        for i in range(9):
            try:require_joist_end(b,m,i,'Left')
            except AssertionError as exc:
                assert 'required_contact_failed' in str(exc);missing.append(i)
            else:raise AssertionError(('Removed ledger side endpoint falsely passed',i))
        assert len(missing)==9
        for i in range(9):require_joist_end(b,m,i,'Right')
    finally:
        b.scene.collection.objects.link(ledger);b.parts.insert(position,ledger);b.objects['Ledger_Left']=ledger
        bpy.context.view_layer.update();m.clear()
    out.append({'fixture':'delete_left_ledger_from_actual_scene_and_lookup','rejected':True,
                'required_failed_end_rows':missing,'other_side_rows_still_pass':True})
    # Actual temporary solid blocking the clear entry, excluded from published component list.
    verts,faces=box_mesh([.55,1.45,-3.02,-2.98,.45,2.35])
    mesh=bpy.data.meshes.new('Temporary negative blocker');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('QA temporary true blocker',mesh);b.scene.collection.objects.link(obj)
    try:must_reject('blocked_entry_after_fixed_panel_removal',lambda:aperture_measurements(b,[obj]),'aperture_blocked')
    finally:bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
    assert all(oriented_fingerprint(o)==baseline[o.name] for o in b.parts),'Negative fixture contaminated final geometry'
    return out


def orthogonal_intersection_volume(a,b):
    """Actual orthogonal-mesh partition, not AABB overlap as an intersection proof.
    Actual vertex planes partition the shared box; classify every cell midpoint
    against both closed actual meshes. This is limited to these axis-aligned parts.
    """
    av=[a.matrix_world@v.co for v in a.data.vertices];bv=[b.matrix_world@v.co for v in b.data.vertices]
    lo=[max(min(v[i] for v in av),min(v[i] for v in bv)) for i in range(3)]
    hi=[min(max(v[i] for v in av),max(v[i] for v in bv)) for i in range(3)]
    if any(hi[i]-lo[i]<1e-7 for i in range(3)):return 0,0
    assert all(max(abs(c) for c in t['n'])>.99999 for o in [a,b] for t in triangle_records(o)),('Nonorthogonal intersection request',a.name,b.name)
    axes=[sorted(set([lo[i],hi[i]]+[float(v[i]) for v in av+bv if lo[i]<v[i]<hi[i]])) for i in range(3)]
    ta,tb=actual_tree(a),actual_tree(b);volume=0;count=0
    for x0,x1 in zip(axes[0],axes[0][1:]):
        for y0,y1 in zip(axes[1],axes[1][1:]):
            for z0,z1 in zip(axes[2],axes[2][1:]):
                if min(x1-x0,y1-y0,z1-z0)<1e-8:continue
                p=Vector(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2));count+=1
                if all(inside(t,p,d) for t in [ta,tb] for d in RAY_DIRS):volume+=(x1-x0)*(y1-y0)*(z1-z0)
    return volume,count


def infill_cut_gate(b):
    results=[]
    wood=[o for o in b.parts if o['structural_role'] in ['main_post','opening_jamb','opening_header','opening_sill']]
    for infill in [o for o in b.parts if o['structural_role']=='plaster_infill']:
        for frame in wood:
            if infill['storey']!=frame['storey']:continue
            volume,cells=orthogonal_intersection_volume(infill,frame)
            assert volume<1e-9,('Uncut infill/timber intersection',infill.name,frame.name,volume)
            if cells:results.append({'infill':infill.name,'frame':frame.name,'actual_intersection_m3':volume,'classified_actual_mesh_cells':cells})
    panel=b.one('Entry_FixedPanel')
    for side in ['L','R']:
        volume,cells=orthogonal_intersection_volume(panel,b.one('entry_front_Jamb_'+side))
        assert volume<1e-9,('Panel overlapped uncut jamb',side,volume)
        results.append({'fixed_panel':'Entry_FixedPanel','jamb':side,'actual_intersection_m3':volume,'classified_actual_mesh_cells':cells})
    return {'passed':True,'method':'all actual orthogonal vertex planes and real closed-mesh ray classifications','pairs':results}


def verify_glb_roundtrip(b,path):
    import struct
    raw=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',raw,0)
    assert magic==b'glTF' and version==2 and length==len(raw)
    size,kind=struct.unpack_from('<I4s',raw,12);assert kind==b'JSON'
    doc=json.loads(raw[20:20+size].decode().rstrip(' \x00'))
    assert not doc.get('animations') and not doc.get('images')
    source={o['component_id']:o for o in b.parts}
    nodes=[n for n in doc.get('nodes',[]) if 'mesh' in n]
    exported={n.get('extras',{}).get('component_id') for n in nodes}
    assert exported==set(source),('GLB child identity loss',exported,set(source))
    assert len(nodes)==len(source),('Merged or duplicated GLB child mesh nodes',len(nodes),len(source))
    groups=[n for n in doc.get('nodes',[]) if n.get('extras',{}).get('static_group_role')]
    assert len(groups)==11
    for node in nodes:
        extra=node.get('extras',{})
        for field in ['component_id','structural_role','storey','static_parent_group']:assert field in extra
    prior_scene=bpy.context.window.scene;temporary=bpy.data.scenes.new('QA actual GLB roundtrip')
    old_meshes=set(bpy.data.meshes);old_materials=set(bpy.data.materials)
    bpy.context.window.scene=temporary
    try:
        bpy.ops.import_scene.gltf(filepath=str(path))
        imported=[o for o in temporary.objects if o.type=='MESH']
        byid={o.get('component_id'):o for o in imported}
        assert set(byid)==set(source) and len(imported)==len(source)
        parents=[o for o in temporary.objects if o.get('static_group_role')]
        assert {o['static_group_role'] for o in parents}==set(b.parents)
        mapping=[]
        from mathutils.kdtree import KDTree
        for cid,original in source.items():
            actual=byid[cid]
            assert actual.parent and actual.parent.get('static_group_role')==original['static_parent_group'],('Parent identity loss',cid)
            aa=[original.matrix_world@v.co for v in original.data.vertices]
            bb=[actual.matrix_world@v.co for v in actual.data.vertices]
            kd=KDTree(len(bb))
            for i,p in enumerate(bb):kd.insert(p,i)
            kd.balance();error=max(kd.find(p)[2] for p in aa)
            assert error<1e-5,('Actual GLB vertex mismatch',cid,error)
            sf,rf=oriented_fingerprint(original),oriented_fingerprint(actual)
            assert sf==rf,('Actual GLB oriented triangles/PBR changed',cid,sf,rf)
            tc=topology(actual)
            assert max(abs(a-c) for a,c in zip(bounds(original),bounds(actual)))<EPS
            mapping.append({'component_id':cid,'source_object':original.name,'glb_import_object':actual.name,
                            'parent_group':original['static_parent_group'],'max_vertex_error_m':error,
                            'oriented_triangle_pbr_sha256_at_1e5_quantization':rf,'actual_glb_topology':tc})
        return {'passed':True,'actual_glb_node_count':len(doc.get('nodes',[])),
                'static_parent_count':11,'named_child_mesh_count':len(nodes),'animation_count':0,
                'opaque_materials_only':all(x.get('alphaMode','OPAQUE')=='OPAQUE' for x in doc.get('materials',[])),
                'mapping':mapping,'no_global_weld_across_components':True}
    finally:
        for o in list(temporary.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.context.window.scene=prior_scene;bpy.data.scenes.remove(temporary)
        for mesh in set(bpy.data.meshes)-old_meshes:
            if mesh.users==0:bpy.data.meshes.remove(mesh)
        for mat in set(bpy.data.materials)-old_materials:
            if mat.users==0:bpy.data.materials.remove(mat)


def validate_geometry(b):
    m=Measurements();check_column_grid(b)
    top={o['component_id']:topology(o) for o in b.parts}
    areas=foundation_domains(b)
    infill=infill_cut_gate(b)
    apertures=aperture_measurements(b)
    contacts=required_contacts(b,m)
    contacts+=infill_supports(b,m)
    # Account for tiny corner strips that a side ring receives from front/back caps.
    ring_domains=[]
    for wall in ['front','rear','left','right']:
        child=b.one('TransferRing_'+wall);all_seats=[]
        for parent_wall in ['front','rear','left','right']:
            rec=m.touch(child,b.one('Cap_Lower_'+parent_wall),'up')
            if rec['area_m2']>1e-8:
                all_seats.append(rec)
                if parent_wall!=wall:rec.update({'passed':True,'scope':'single-owner cap corner strip'});contacts.append(rec)
        area=sum(r['area_m2'] for r in all_seats)
        expected=horizontal_face_area(child,2.98,-1)
        assert abs(area-expected)<.0001,('Ring bottom not fully seated on owned cap union',wall,area,expected)
        ring_domains.append({'ring':wall,'actual_bottom_m2':expected,'actual_all_cap_seat_m2':area})
    original_165=preserve_original_165(b)
    contacts+=eave_contacts(b,m)
    assert len(contacts)==308,('Unexpected original-plus-eave contact count',len(contacts))
    eave_collisions=eave_zero_intersections(b)
    skins=coplanar_skin_gate(b)
    graph=check_support_graph(b,contacts)
    negatives=negative_fixtures(b,m)
    negatives+=eave_negative_fixtures(b,m)
    preserve_original_165(b)
    vv=[o.matrix_world@v.co for o in b.parts for v in o.data.vertices]
    overall=[min(v[i] for v in vv) for i in range(3)]+[max(v[i] for v in vv) for i in range(3)]
    dimensions=[max(v[i] for v in vv)-min(v[i] for v in vv) for i in range(3)]
    assert max(abs(a-c) for a,c in zip(dimensions,[4.60,7.34,7.94]))<EPS,('Unexpected final bounds',dimensions)
    triangles=sum(len(o.data.loop_triangles) for o in b.parts)
    used_mats={mat.name for o in b.parts for mat in o.data.materials}
    assert triangles<=20000 and len(used_mats)<=9,(triangles,used_mats)
    for obj in b.parts:
        assert max(abs(float(v)) for v in obj.location)<1e-9
        assert max(abs(float(v)) for v in obj.rotation_euler)<1e-9
        assert max(abs(float(v)-1) for v in obj.scale)<1e-9
        obj['source_geometry_pbr_sha256']=oriented_fingerprint(obj)
    return {'status':'geometry_checks_passed_pending_independent_review','design_only_pins':{'spec':SPEC_SHA256,'design':DESIGN_SHA256},
            'all_geometry_is_new':True,'non_enterable_static_scope':True,'component_count':len(b.parts),
            'static_parent_count':11,'triangles':triangles,'materials':len(used_mats),
            'bounds_m':dimensions,'all_vertices_bounds_min_then_max_m':overall,
            'topology':top,'foundation_measurement_domains':areas,'infill_real_cut_gate':infill,
            'apertures':apertures,'mandatory_and_fixing_contacts':contacts,
            'ring_actual_owned_cap_union_seats':ring_domains,'directed_geometric_support_graph':graph,
            'same_facing_skin_gate':skins,'negative_fixtures':negatives,'construction_audit':b.component_audit,
            'original_165_exactly_preserved':original_165,'eave_closure_zero_intersections':eave_collisions,
            'eave_design_delta_sha256':EAVE_DELTA_SHA256,
            'art_passed':False,'independent_geometry_review_passed':False}


def add_presentation(scene,b):
    world=scene.world or bpy.data.worlds.new('Neutral studio world');scene.world=world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.30,.30,.30,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    focus=Vector((0,-.25,3.80))
    bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Presentation camera excluded from export'
    scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=10.8
    def point(obj,xyz):
        obj.location=xyz;obj.rotation_euler=(focus-obj.location).to_track_quat('-Z','Y').to_euler()
    for name,xyz,power,size in [('Key',(-8,-11,16),2200,9),('Fill',(10,-4,10),1000,8),('Rim',(2,10,14),1600,8)]:
        bpy.ops.object.light_add(type='AREA',location=xyz);o=bpy.context.object;o.name='Presentation '+name
        o.data.energy=power;o.data.shape='DISK';o.data.size=size;point(o,xyz)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015));ground=bpy.context.object
    ground.name='Presentation ground excluded from asset'
    mat=bpy.data.materials.new('Studio warm slate');mat.use_nodes=True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.18,.21,.22,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9;ground.data.materials.append(mat)
    return cam,ground,point


def render_phase(scene,b,out,phase,render_log):
    cam,ground,point=add_presentation(scene,b)
    scene.render.resolution_x=512;scene.render.resolution_y=512
    def render(name,xyz):
        point(cam,xyz);scene.render.filepath=str(out/name)
        assert_render_config(scene,'before_render:'+name,render_log)
        bpy.ops.render.render(write_still=True)
        assert (out/name).is_file(),('Render file missing',name)
    if phase=='gray':
        mat=bpy.data.materials.new('QA neutral gray override');mat.use_nodes=True
        node=mat.node_tree.nodes['Principled BSDF'];node.inputs['Base Color'].default_value=(.48,.48,.48,1)
        node.inputs['Roughness'].default_value=.85;scene.view_layers[0].material_override=mat
        # Review-only 1.75m reference; created after clean native/GLB, never an asset child.
        markers=[]
        def marker_box(name,loc,size):
            bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name='QA 1.75m reference '+name
            o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
            markers.append(o)
        for dx in [-.075,.075]:marker_box('leg',(3.15+dx,-2,.40),(.10,.13,.80))
        marker_box('torso',(3.15,-2,1.12),(.34,.18,.64))
        marker_box('neck',(3.15,-2,1.49),(.10,.10,.12))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.10,location=(3.15,-2,1.65))
        bpy.context.object.name='QA reference head top exactly1.75m';markers.append(bpy.context.object)
        render('gray-front-3q.png',(12,-16,11))
        render('gray-rear-side.png',(13,12,9))
        black=bpy.data.materials.new('QA silhouette');black.use_nodes=True;nodes=black.node_tree.nodes;nodes.clear()
        output=nodes.new('ShaderNodeOutputMaterial');emission=nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value=(0,0,0,1);emission.inputs['Strength'].default_value=1
        black.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
        scene.view_layers[0].material_override=black;ground.hide_render=True
        for o in markers:o.hide_render=True
        scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
        scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
        scene.view_settings.view_transform='Standard';scene.render.resolution_x=128;scene.render.resolution_y=128
        render('silhouette-128-front.png',(0,-20,3.8))
        render('silhouette-128-side.png',(20,0,3.8))
        scene.view_layers[0].material_override=None
    elif phase=='pbr':
        render('pbr-preview.png',(12,-16,11))
    elif phase=='formal':
        views=[('thumbnail.png',(12,-16,11)),('qa-front.png',(0,-20,3.8)),('qa-back.png',(0,20,3.8)),
               ('qa-side.png',(20,0,3.8)),('qa-top.png',(0,0,20))]
        for name,xyz in views:render(name,xyz)
        wiremat=bpy.data.materials.new('QA topology dark edges');wiremat.use_nodes=True
        wiremat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.012,.018,.022,1)
        for original in b.parts:
            o=original.copy();o.data=original.data.copy();scene.collection.objects.link(o)
            o.name='QA wire overlay '+original.name;o.data.materials.clear();o.data.materials.append(wiremat)
            for polygon in o.data.polygons:polygon.material_index=0
            wire=o.modifiers.new('Actual source triangle edges','WIREFRAME');wire.thickness=.004
            wire.use_replace=True;wire.use_even_offset=False;wire.offset=1
        render('qa-wireframe.png',(12,-16,11))
    else:raise AssertionError(('Unexpected render phase',phase))


def save_metadata(out,geometry):
    records={}
    for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
        p=out/name;assert p.is_file(),('Formal primary file missing',name)
        records[role]={'path':f'assets/village/{ASSET}/v{VERSION}/{name}',
                       'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    metadata={'id':ASSET,'version':VERSION,'category':'architecture','assetKind':'modular','theme':'village',
              'style':'warm-handcrafted-village','title':TITLE,'description':DESCRIPTION,
              'bounds':dict(zip(['x','y','z'],[round(v,5) for v in geometry['bounds_m']]),unit='m'),
              'triangles':geometry['triangles'],'materials':geometry['materials'],'files':records,
              'status':'review','license':'All rights reserved'}
    write_json(out/'metadata.json',metadata)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['geometry','gray','pbr','formal'],default='geometry')
    parser.add_argument('--no-render',action='store_true',help='Only valid with geometry; asserts no rendering.')
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    args=parser.parse_args(argv)
    assert not args.no_render or args.phase=='geometry','--no-render cannot be combined with a render phase'
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    self_path=Path(__file__).resolve()
    unexpected=[p.name for p in out.iterdir() if not (p.name=='generate.py' and p.is_file() and p.read_bytes()==self_path.read_bytes())]
    assert not unexpected,('Fresh output directory required; no overwrite/resume',str(out),unexpected)
    raw_spec=zlib.decompress(base64.b85decode(_SPEC_B85))
    assert hashlib.sha256(raw_spec).hexdigest()==SPEC_SHA256,'Embedded approved design changed'
    spec=json.loads(raw_spec);started=time.time();render_log=[]
    # Clearing a fresh Blender process is local to this new output build.
    for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
    for material in list(bpy.data.materials):bpy.data.materials.remove(material)
    scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
    configure_render(scene)
    build=build_asset(scene,spec)
    raw_delta=zlib.decompress(base64.b85decode(_EAVE_DELTA_B85))
    raw_baseline=zlib.decompress(base64.b85decode(_ORIGINAL_BASELINE_B85))
    assert hashlib.sha256(raw_delta).hexdigest()==EAVE_DELTA_SHA256
    assert hashlib.sha256(raw_baseline).hexdigest()==ORIGINAL_BASELINE_SHA256
    build_eave_closures(build,json.loads(raw_delta),json.loads(raw_baseline))
    geometry=validate_geometry(build)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in list(build.parents.values())+build.parts:obj.select_set(True)
    bpy.context.view_layer.objects.active=build.parts[0]
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,
                              export_yup=True,export_apply=True,export_extras=True)
    assert (out/'model.glb').stat().st_size<=3000000,'GLB design budget exceeded'
    states=exact_glb_states((out/'model.glb').read_bytes())
    assert set(states)==set(build.original_baseline['glb'])|{'EaveClosure_Left','EaveClosure_Right'}
    for cid,state in build.original_baseline['glb'].items():
        assert states[cid]==state,('Original exact GLB geometry/PBR/identity changed',cid)
    geometry['original_165_exactly_preserved']['actual_glb_exact_original_states_passed']=True
    geometry['actual_glb_roundtrip']=verify_glb_roundtrip(build,out/'model.glb')
    assert geometry['actual_glb_roundtrip']['opaque_materials_only'],'Unexpected alpha material'
    assert_render_config(scene,'before_clean_native_save',render_log)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
    if self_path != out/'generate.py':shutil.copyfile(self_path,out/'generate.py')
    write_json(out/'qa'/'geometry-report.json',geometry)
    write_json(out/'qa'/'approved-design-embedded.json',spec)
    write_json(out/'qa'/'approved-eave-delta.json',json.loads(raw_delta))
    write_json(out/'qa'/'original-165-exact-baseline.json',json.loads(raw_baseline))
    write_json(out/'candidate-description.json',{'asset':ASSET,'description':DESCRIPTION,
       'scope':'fixed closed non-enterable exterior shell','design_only_spec_sha256':SPEC_SHA256,
       'design_only_document_sha256':DESIGN_SHA256,'phase':args.phase,'independent_geometry_pass':False,
       'art_passed':False,'no_old_approval_reused':True})
    if args.phase!='geometry':render_phase(scene,build,out,args.phase,render_log)
    else:assert len(render_log)==1,'Geometry phase unexpectedly rendered'
    write_json(out/'qa'/'actual-render-config-events.json',render_log)
    if args.phase=='formal':save_metadata(out,geometry)
    manifest={}
    for p in sorted(out.rglob('*')):
        if p.is_file():manifest[str(p.relative_to(out))]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    write_json(out/'qa'/'output-hashes.json',manifest)
    print('SHOP_HOUSE_STAGE_COMPLETE',json.dumps({'asset':ASSET,'phase':args.phase,
      'triangles':geometry['triangles'],'named_child_meshes':geometry['component_count'],
      'static_parents':11,'render_count':len(render_log)-1,'elapsed_seconds':round(time.time()-started,2),
      'out':str(out),'independent_geometry_or_art_approval':False}))


# Embedded exact approved r2c JSON. This payload makes the generator recoverable alone.
_SPEC_B85 = (
    'c-rk<?T_QOng5=@f-'
    'rEvwY5ExEPL$ErNH%)v;p>jUeW`yDGEWhXj@rX(uwlSc!T`!_q>o4Dao_m?6&<fL6D3kzCL{3N&fWn7eY)_o3>{)`MsEAQsswoR+'
    'Yu&LDaI$^70_^GL!hXEL)-'
    '4=DcgqjTDEpl_D)OQKt>QsbzD@mCCE~L6ns^$Wk_GTQvgyJxO&G@;O(nnoP0B9aPLSXaPF?86Lo+Ji`Gz=0%Yn<g9(FW(sP{%S;`'
    'sdUmYNO3s3iszd2V*<e>#C7cKIK-'
    '5iDS4w84K%2J(wm$i5e%i`Ld=IUNKVvK6DQ}PBe`^@9`07a(1<cXbI?9uD#$leT_QI__rOjz}gwgMsbl=KsrVENY@qMr`#rNqcFD'
    '_Uf9?ri1a}YlVtJ$L+{jNxXQu}<Dwt5m(DMbeK$;(|U8hKXfwvYlBCf|weIWKS}kg%;th1vmer(##NEq2|=Q~C~mpQ`K(mEPqo(j'
    '4nb@t8JwTDG?1>Rh%-'
    'zE9E`2=*wE<{`ZLg;quFs@ho*?mdyut!(nDNz@UD1+Rexq?u^`EVE=+Amx)nrqFPiC5Iw?k3{u~0z;hhQYKGnQ9$>yK`v5$nG{$n'
    'Es{e6!_26uGcHrIFRH5Xi^AaYW|t})?>;S*9T65y=xqYCDR~@j31C*>OdxMk>6VkW(tp&jF1YM|jRuI8pCk+@KhcU|%_FqjFSx6K'
    'n~*P)GJVVsTsGb9B&_x}FY@++HO+D+D&0$X1l*9HdM)LpCi*^at8?3XTNPP?G9?wZ2kR~il_1y9f>KGls5_V!^ybOhxy)OV_mga4'
    '5gtT(ZjT^rnfOth>!~;tfBgm-sLawP6K~;}VW6tX4|$p3aQ{Y6gb1dCKj{B|?^ThhUW~~p%}cSzH6{uP_yff`lL8nU1|;CwzDQfa'
    'j9{gzsepO2ypcOCHiIF|!tpVvT}tw6D%fJ(A6|K4QXWjA>eQcbZ0fA8)d7_POY`j2nnk8s^m4U}Uu|KkExc-Fb%I4Ll5KhcdC4=X'
    '6xme=%AQY(9_lsMwEVpx7Og_ktpW%^jc@0Rsaqk*<nCRv1yxg>#$NC9G6zP?v;d*ZW+YNaV5}oBDpy+TT1E8)@|>6Z9JK%x2BqEV'
    'uA{kMYM0jb&BnZHo3vDWc-x=^*>PPh!3`|tn)(w~DE_4SZ~ZxOfwfm+d;-'
    'h)y;n+4fQmI$wFgNBO+p3NragMz=CT{j*h||A8XeF*QWlAlDYmtmhi++_8SulwY4P5Ut6zl2eLr8vrT{(eD1SfS#DlsreRNu1&4b'
    'N&5pH5Nj~13M4coF6P)eS*#RcY*AC4`v@O(uDdx}}FF~71r+i^EBvtGTbYHL{g))(4&C${t06D6w4)45uCvFd6se7V=mTAdpullN'
    'Ct<2+n?l{ABlR)Vr!y~S{-TJq|&-'
    '5nEfzS86rA$ee#qs=O?|13R0KLf#ujk*f!dFT`mg1EDg%|+W#FcqL1&}B+`3d6U@Tn_BXvC0y(Uc~4Vb`8KEf#-'
    '(`R$i#8$TP8}W||9nD&UJ0ITVu5VE+X*^dQIpV)^V0Z+Ga+>{BqL=<Sf>;*FKpKobV-L-Ks-'
    '5w%;vaK5s<FpKAbRm`&m5M)U24>mrF=Hc3Ecjs?x(Eh-'
    '`y~cUyx?S|LN^%{*+@mdIa(Al*Ztndu@~GWbZRafw*kL_i2l4va>h6Guq#&uA_d&e~oXX%)FGIgGE&^Uc{vOOQ^n32}Qm}S<i>@='
    'DaWf}%BWKjOAdi5f4$^SU1yey|g(a^GT6-'
    'SWDH7FQfCnSG(TE?voG$`_8ppR!OqR#A$Sv1`*OMv?Vc6Z&UIs8Tc*=(Yy4e*uh$lR$cwkvY|5Fk|9biNprD*~s0KD>YSCx<QnTI'
    'WCUBFqFKw_ca9DxML?7QlO0h2(I*y7xce6E4HpkJiYq%-B9PnG4ipEWm4%9JCOZ%9A>iD&ygx$G0eauX6W<uNO>s}%-'
    'fSmzhXK=;%CWv##dvDQESZaZv``R*NfG2ADtmu3G62|norSh2i3Lo6n=dT2RD!<lk)R@Jyxur~kkWpp|Tbp&%!Jqgm9pgYhjMR!T'
    '=Db_?kUjU1g?;t9zl{0;rHrnUZ^fr#B;W>ygA@b_jrmN&@)<qD-'
    '4s%o4U#2gu2nCq8FG%byNbE02>@A4*EAoE)0~X}LhzS{DBLtWi0F!wX9Hfua+<0OFA5g9UA^?;bc#HwO6hBp%6X3WOI;*hdN7VFc'
    'm#1Bu?CTBIWjXiES74p_3AO9jkSXW^t=!^x#V)`vUuas98?HKk0=P-'
    'FWT7Df=+iKYY`oW$P^fx>{}Pj7ghCUA9vi`4q9E0tvBdxIAc+6;E1+Jj1VlP5xIkEeUcO~hN4yOsKq%hKxGQmXQXCu)VNVchP$%u'
    'cEQO9)@<SZ5F_$a#)|;;0dNbngXa~6OxhxzrxE^tMMyqw+wLllzs|FDSB?-'
    'W_JRgoiNAyb6$BP25peQcJApjC`8Pu?a1b+b+>LhRlAH+}TX?u5+DaikwLds`ykG!}maG`Xw4-'
    'oi*Pl{?9a~Y1phd&F@&6qWqxN#eEc-'
    '5SgGoPQWM8c>!ZA42o=|q)9qu{{HR|byP=*NFuRO?AN_0n=n@4@*#G?FN0ivBXaJ}l&&Up1;<JE(Ad%diT$znNIGXnJjsA2F`YP1'
    'M35<<@b1mSN4harr3~=GUal?Ih%8l*Yp$e!C+jlok~z->#&{m3XR}B12t-'
    'l)j^Rb&uapy^JroS|u<z7yvUw)%hki9qedMjE6a&q56)pYw}zR*SA_-'
    'x!|^9H@4>XdRwQr^?75Lv+%ZZ;cXMWt(Yw}qQz;g6sOaAn!HoVfpIHF>VB;Lf2qUR=`g-'
    'l_jb#{m7K8xFIM}#l5FgPeyYiGFzWU^!+6)tcfr&5Jt4RGD*mw<I$w^3rVwb<OtYb0dj8*X(A0Hv%?8`6zg~Ka{>xZq?Am-'
    'gijGWpv-aH0PnmGf;r-'
    '|ddlAffH9BFNhPyi1)z!(`WFG%mf70qMyvZ&;db0Q4Wba2O>xAYX@JoRpcjS_TgM0#a=cxoMQD8<M<5R4vw42HW(0iri3^+pR0m3'
    'Fl4(o}7FYx4xw63weE?0w9sIqaF*wc5{VW*R!*43O`tlbz;z>QGD`DW?;bf`NE<}2rA;D)R23$K#jAapiZpKD7SdVCl<eAq3m)^?'
    'XZg9Y<2a)%cV>-'
    'MWG=0Q9vfF2_hGCRN$y0kXq?^D+Eq(Yl`wh!*dd=<A+=t>DuVBJ+2%;yCT_Za*ZLQFlX3~E3$SwP&E@h*Uba5gg$a5M<@K{~30V@'
    '8`IfLM`ZM#;M-^B~+reniTxK32u~1jQFroQno=ytV-'
    '*yGkZ>8D?@g2<Nn%A1F*Xx<<#@KEk+T7*b61W)*pRoLxV8)hN(OT;12{a{Y41pbKwV;-TK+ieCCYSaw9hc+BZDbU0qW{7|3Efs-'
    '@AP;S(RAR&rfks8T|a15vi1zs-'
    'v*BSob#uY>_?=>Q+y4j({j6K!A+zhP<ZK2cNxys+m!7u_(Nd&Q{se<K8?dd%YOuT;d%2ES|w04~(zje)V?BRD|s$1lW+6?CL#?_i'
    '5i|jOVO=*DGN0Dm?z&*LYUyk$3ujXwNYT2aqDKGQW`6TvDdXkiMNL!t>rc49`N)R&9_(h$TvM_mV&Z3!<528sg%A}DqH{!y=U|01'
    '~1i_~R#s~uni#J&)30>86{$+-#BY}H^e00b3i&PM*s9H7EnLKm{m~E-QbGbXWdUr<K^hr<Vpms8v!1VG2-'
    's0l#W#}g~dh2Fa&abubY>~4<FW4f#=kOoU^SGSYZA#3f0>S;Alz6$`xc{sMm9_Txm9@!A(c%CDjW@E1qS$Gp)BI(XnA0tW(_tFS$'
    'aqAC_VUdE738zg%r{%GELU}res&u+yKcn7Zd3QF4coY49(~w?If{S8fGt04z}8-'
    '5Gh%{BnDksZA{{uq!TjFacDY}Dq#2ApU<PkeiqR)n&-'
    '>`Q`CQ*_J|lNLBl}Him`<iOaQoYg*W%%`FBJFmt3JUt$ovN#Z=C7q*#u7~3eEW@k38*;@&SjRaQ{#$JjnM1YQB1!_~RI7XL{wvaq'
    '5`Y)FJH~fMrn-V6{(DmaN<J688t3jRPn*qc`lJUQz0r@{RnzbB^wEPklH(?PB5Ywk-XzlH*)lkZL;1KiseZMhMm~Xb^pXgW_s03E'
    'U}>=(8)48$99I$%<eyU__vXdgN2w;MisSr8#l(E4|>wt>U)qO*4*flegI0B#y_(GmyCMIL7TFH>$L5Set>EEuv432R;<KlY4kwfV'
    'UF&vq?PnQnpj=iHURzV#?3)i5jF>^gbYO(DofPb0*D|?CSy@M>mS1zwz<OviK^BucG)WiXSVAXb+R%CMony=M{q(y-'
    'MM$6uwH~uaUy=vq|Br5WWiGs}O#y5RyN7qb=<DuCK=MRSsX}@UzNc`1$1URSaLn@Kp?N7ejr=Makwd-'
    '^r_an($vBjbU#uVeyZaMsMw-dHm0j#;AW@;YMi;oug+=tbd|3-'
    'mo^W()g>5qI;(PMT_VaeBHKqwTQ1W_%SkQuWq5_q$Sut)ymqr!{w6B-'
    'rs*VJMRv&>yx}~#fNz>$rk?q&fk>pUlhKNogeY)`W0ezZg5j}c*#3jdH=ZQ?UxJhANM-Af2zL8RqwRyiw%FwE3Y3QSemI9uLxYbv'
    'W}<Eij<IqkivMSkN|J+xKfS?HL_{(CKqj8PsQa+zJV%oJPSoHpat>%OPKnDcrTku;H1s5Vgeh$W<AV_1dDjb{E;<WunW3*>)&86t'
    '2V*9RFtuFx-&0)h7<7(I{qr<Q_@|XOf2Y+(<T8v=%sgY9SCJ1ea`7>+uO+q>d3CCK$lqT5p#LF&ha`kUX!dy8t%R4-'
    'OZszJl|}hAPU0GdbwP$R+jw<nPL3a-=e#`;jiK4daZ?{Q}FMrFe<P}MT*Ef1vloSiS$Yy=<tzSF0!kXM5m-'
    'huqnimsH>*+&L_EiQB=S_Kz$2UF$w4ENX(FKzfHI5-'
    '=BXo87t4Y6;ODyx?b4u?LhN~Lo5w$*qp<R=E2I!)mf<*Fkfavpqid^<?`y~&%n8i6RZc-E}mfv*Ul?Lh$~nYk-'
    'y3sl%&^QM+LM>x{R^>&+o6?3kzJQcy;}P6RgdB7)R@+`LB24CyHLU8s*UCW6Lg9v3KA2rYmH~bK`fga4&%g!v{;7rfTq3UL#w)n~'
    'soX`bZC*9CC2V2ml5ll3uWr;WG5j4KDrVA|}3Cd$C-'
    '`%Xq!nEEhqzS{eg4p;JZ#NrQYnR=qnfzqmI%#o|1Ez2h3d5!dlpYURB$yu{3Um80;w$gS)B2}SR{vr$oeBWt|C;<H=37$KW;37;M'
    'aR)KUbSRwcU-p_$mMBDm+$AZa8LqmH4w@$f0341EbOap!$!X@AXZWcU5C2-a8nZ1`z@JVzq84NP?-'
    'Bf9YaAJpp#Iw#jJSxY~Hws|`seds2*z~SCN`ez4<%u_y$d%l|0HG$@Ujh@Hc(Z*6gU2g=W4DVsmznwGiU#Ukg#qrp_YVbIUbuSv_'
    ';b_==SzDS{(2?9#_B`mXCLTg<eJXFrgfpFK}JyLEx6r?SK?V-'
    'yj7DbGUB8q#!e$g&M8_nil)$ofP)%0JamIXDyw;QT=gKwYULMhR#6<q%U}_Qn_v;%)Cd8$=rJxfQM`^fL9kjc*1@U^=bjLgAUVhi'
    '!SnK+3#v32#S*GUt01^vuA?|!twyJ9uNJV73DS82CN3;F6eHt-GYpSUD3pfhZRxeWVo;|!i5WLfXfh(p_j_oH&!Z9&#Zy&fB=PwE'
    'L2Q=)CRz#YX@DAKZ~B>=RMf6;S7=JO9Yham$%1E1y!&XLN=g_^M=>*4ajhG<JGY5pE<{-'
    '(Fdm}gDj2e#MtuOEzH#LrS1$65v=fMHcu6ekbVjw7>t(k%roF@fKqR`R1B2%=v3_mw%sM_=g)ZQVS!ld%nYN_PW~7!7z9@<wx>bE'
    'EtO(-'
    'TiW9;Z!J?qfwktk0QT7pNH5dP_F^TlN1Wk&rdC*$ZkR42m`D8d@6j?nP%|3Rrz3XfUw^QQvI(>VftTNf%ZJT`4g<4<J#WoKJ=LOK'
    'B$@d0QAbCSqv;DW<^3me4SJY-#djx;yIx^4X<$Ai;u~*+A<emTME9m46-p%-iGDQB%Kk0mt_s*s=3^h$eGYLZj0^1>w05kjqjv^-'
    'iYs|DTW{v`b3XbCLm=_sXP$9FNN|XIe8(<)q-Bef%(<z=-'
    'r$7>Mmg@YmY7tUa1DKNbXyBJ50AB|Qg$yfbgAQ$$A${w#kS&NxbJ(T>933xj(5XR?yM>cCxE}}O1eJ11frWJP$V)*u)x*HalLT=*'
    '-WaH^ije0L6pAYdaY2{I#LF|wD@`GGl;46=E!s>+unk69NDA7FaodTb=?J6({Cx$k6g{e|Q*p-c-'
    '5(q_F*XvXp)htE>XJu(Lta|cPfSfm5e~yE%bqu&JTeT03a^>q-W!JdW7(gaRag5n33r26>?pao&pQN!i7XE}E#>6D-'
    'u~B{ufMmj&nZF)5pYch01D1cnx!=gT|xzh5W`p|lVt^>G<b(TG3C;#jM2ir{o(7cCjLt&;e$4%K`5&|B2lrdL${BTGNy<ychR%*6'
    'Ch~DF~L?fS4ToH(g}{$DDUB0O)xBES{yc{$7l_Q?U~w5jyT$~(&Lal$Y-'
    'wmn9HXGSWq&A?C!Dyx_2W_vYZgHv(d^$b<mXP)5oJsXS<r}&`4zf#2NJ51HB<|^VuH^wmHKi=kFP=7@mVN-'
    'p|NF0^ejt_x=tdcfwV?h#$ZGi&OtizHJcfa+~hnooh^a=6j51pafnHrO2nOW;|M<UCRq501!GFi)q)6fYkrzKk-TXRDlVAND4`(#'
    'P5JZ>u1DwAk20s;LQgMnn_`AfBEBg(7eRD{jzD(&0pouV$bM5+zmbhcW>6gyW<X03H=hP^_@0gcM80fQ+jtyVZ2>8#*B#iye$x7m'
    '$w2a^(vpy1C*Ug#{6mrBR}b&uZIu+SnxWVtSiIKV{WiRgG>=A%q``Rz(%eb=*TPgryP9TCU0%dnFg<++pXoci1x|$43TRWi%u-'
    'AWO7QMF(O5$)Cd_~w@vD81Md*<8-z-iGLX85Vw-F)t*yOar?!Voj-Gp>T69v(O|C)i8fI!ZzKM3f7frOq`QzaMnL+T783b1Ago00'
    'hr(=@0GrgN*!wT)kPi*5Lz}<%g#=afUM8f&LfM$#Fj|Fh6`W~6tlPW3Rbn)qtmkxxpujNC-'
    '>VX)7+}z=XW>``|x`FW?X<q0O^9AibESyd@G;*d95dFJz5bFRR0Owl1B6w4VydsqL2?bb`5kYiQ908`bsZC)*W<4Ny2IQ|Rrj!ZZ'
    'aDaRZ8<8+!$Ov?b5G_Bv?E);C0<RWT_)#>#W739zOouyq$FRAW*D=_dbWvQRdQnP8t028eN3}37^TXQ?YLJ$Ir)a0)TrKyo^=SAy'
    '*7PT-*C$m1KfHkd$5?d65e>ulnG5m{0=h%iqo@ht$=YM;M5FqyB~gOj5S{gxD>PdR#-'
    '7K`CAzK81GAfxh_|4%2{_m|I}ak)UV0}6%fO!|Um1PiGXda`4n}T3%vKY7<Bfm1XOE$B#UPp35_GFy>bv=;Gmv@PySPuP%ZL~)7j'
    '1csUg4Y=g#Lu@mGXe!+s#@G$zcR~i&kd<HIC1Nf%w#TKbQr;93GEi3zRpbun0cpdN;OBpTfZHRRP)tm<X?~o-'
    '~*u?pfKZsSdQLCIasx^I+y{%0&_%d!kE3qVSgXlza0YWc?;a>De@i<zbl9RB(*_gZLe%!urwm)Qsmxf!LlLm#bsS7{E0I=iz)6%='
    'A9c55KWuW+VZ<0^;_0xH{?7sE&MS5*TXSnXr7Yh#Yx>=cJKjbb+K(HdnDFRS$J=@`kW~k~cnrBE0yk#{T*ay(xM<3PU&w?=X%H<R'
    'TySF?@R9Xg$Cl53<Mae;lX>Klox$c6tCi*C89P(dN4zjANfT{QhI8)2GFNSpPcOco7xuv4T2sPFK)}Xc%A>{3Y;e@Y^x2K5DBom@'
    '+>DkX1YAj*<XnRd)P~HkHqMP~#va%{Fhz@g=q9rVa)8OPD;=mS5smZO%1%YywxwD&l7v3yc@@O=**;cj$9a3hfC2R2umcVP-pk@t'
    '~a5os}Jp!VTW#scwaCPe9xzae_W*88&Xelye4`^brps>=>&YPr2;(4A4zU7M_&etFwm2fwxyvqbIZ_`}Qk%1g7a+kO7d7X>m@my$'
    '*UDtr=@8Ish=!<O01($yq-CAkpjS%;_Da_dMz{M|3!y#!uu!75L4Wfj7mW3WaQm**r1u!RBRq;ryjeNqr3@z1&eAN^l5ih==r{FV'
    'rO36pwr{AgdDe`w_*4i<;C`?+69G(gQMn9ztzrUdoH}Qd5e+nhajjVFN~%4nvop@W23=-'
    's+U_25XyxbDb*OL~qjG2Z<~!f+m11^EaFNRfs5=XAVLSp967@0Mciah)fA#$@;tJ7I}e)Htd1o=@NT)dvVMLwb?&$*zaCXfJWgDf'
    'T@^ZpmE~UTIPdPJ^Jcl02_lZT`Tl0u$1O4T@3l)!G|;Ac=zJ)I|I#v%&-=*>_4Tr6hj2cR<byB7|RcOb-M_8j~`)b$R$?nF0l{N0'
    '!iphm}N<u_f*cQAUwgt3urmsiI?=cn2n2}$e=jzXVd7LM9!W|Q$5jWAr46S!%yhIqJ}FZs!jxgf~jdG_>^J-'
    'Hx=~#H1rJ7t%GH}kQ>x}y9;ExOlWsa@6*#pLKp}FF=d|zU(*h+{;C0C>SJHJC`0J`Mfn+*Y!I6~%R%#<$<?)E=?w$7|3^nL+SjbD'
    'W>7;AWR?0r58Wqv_^5hkQoyMKM-p2nAbCRUo1uqheAN%M%n*OhDTT>KL(q$77YmsY6vdac@nY8ETtDG=2Q)j-'
    '5>GkO`@@%v4*1((zFD5Yfu!9UC#ZwYYMl9$fmt%CQM%4sh}qk7ms+3?=(uEE3q0zf_wA9iYrPeJN6U5Nyi0lD#28p;^Vzi#kJ5a='
    'ph@xg9Hpi$eC`1E8YL1Isc6%ep~C$i^B@|Bzc$jgPxFHDq$d>B5%(acYWmL{`U@=VfT%^m3BB+7fif2qavR3+BrUh@-'
    'I(v_Q^8@z&qaaoW(wHvCJ>WSEHb2mA~JMT2sIUMnj`I^@=_DePd+drk~^cPxN~q0X{EH#AbURuax*R8t2<8>>cv2WyITgi1&8RJg'
    '(u_FOM6ar5#HX1#;k=9^8+*UkpLftkG)7tfdT!fJD|i3BU8tG-xBp4i0bFdM{$bh%HIYRKQc#-'
    'p;<T2@OyA~X#r*wZH?g!`kN)@4;Uo`(MbbW?dTn)MJTP$n1j5k#w({&1eCIPOzC)!A7P-`{Nk4{{vRxre0~'
)


# Exact approved minimal eave delta and immutable actual stage05 baseline.
EAVE_DELTA_SHA256 = '3054e42208d93403e6e2e4478f7db26edd06725acdb1553c9a6c4ae203ce6fe3'
ORIGINAL_BASELINE_SHA256 = '7a8d58d5d0e38a4a2d34ebe88953df35fce8ccb84159dca53aa76e09c5fb0d55'
_EAVE_DELTA_B85 = (
    'c-rk+OOM+|62ALaH0G3SM2Qbkq&&#M$tKwaf+VmFtm7acnq*UAOtG16YBX|?|Gr=KgQ7H(O-'
    '_4?4;qQ=M?Jo(`l{Q%y<qI_L)+JPFWKFp?b`$I0<Okjr}#Mtqd@Qn5mcSjM<s$<=yuoRPdD<r1x;1rq1CPIX}XH+vq}j*in=(C6+'
    'Mo_coRfn5M^(p<Yk(_Ot;Hy9jEd7voL%ahISIyT8u?&<alVij_*V;o@Ag$sl++ZdpQJqdDH?z*%=K#wB5Nl_SK&EJ7H$N36tQ>zr'
    'yunxCtKIxL%wJyLu&${fJ?qd0uiYilOZ_p8SRfc%%nW6?)I(bVI9cc+&{6U2isZR0<x)%{I;BP2HqrQ<pprH+d81A#d_LZ|Yj`v='
    'U8RN82<>QXVH}e=KXwHd{DJvt%8Km?xVo4<iiU@Nm6On>rFvjHN}BM7+teCJxI@QbzeY7ukkK+ih5fRqPkm@~A3NsP$~^D9krPY~'
    'pR5=1G<DG~8C1h<Ms0d6?wuZPS$7I)_G4SXbG)UN<q%HrqH$qB7=Nzc#PNBku}hrCnFfcF6J?3zt>2DKRnLz!uwWCc-'
    '$5!X#_fq2Og5i>Qg3rm6EdX|lY@x7&Clk`ih^w?ogz_Cd@xshddTS-44?D$KTGn^$Dxbrkb7&!QyVLb+(OZIX-'
    '(wyhfYrjF}mo#!#%l#}fNZ7~RZ^kcCT@*qZaE|jQ5JB+jK%2ZV08b09Lc$==*jW9kh<2r{i*BenM<u=ZvI&ad1*I8OdWeQo=d0AC'
    ';$S0lDSTwxtp4lSKHdU4<yb8m0RYR*Z$wi)Sl1<E`FfGdn7zpz?<{?i-'
    '(?mJU$wjrzN|A<jc848)w*h7Vk1e>ik@xEL+u)nmuYN>qykvOXv2m~Dakmdj-q)-'
    'YojkEl_B%%5tXahoNSZaBgxT>_N!hUWFesrZnD5!3<RI0E@2dlE``~~8V!A>oMyq6L;|f0qVRo-'
    ';hEQcY(I4AhbZ6||Rv%a|$7(NX*0hiKJV^;B7y+2eC#;lQ)tbq^J1^OHl1bI>+8*Lp@-'
    'WCAK4aczt3m442{a1T@@_%$OSOU&J(O5sv^p=WE<=m0SK@KR!v!O~@P*TKhAprU)AX}~jD3JtLh-T_%&5eyd9_p1$_PDwG9I>>f}'
    'G$*bV=(gDE6h*tN2zlqeBEnJ{BbsPpyl?v<m$T;$^g${|Yzm*U!_`^B+u2mf`j?mwr8&TFP;hhvK7|nlAHvdNazQ7&_h?=Y9M<TV'
    '`Pp;^QB@)So<ldJ(+sd!Y&%ZdchX<MgtOJdU?-'
    'lj&tI6)H(#fY1X~#iJP$F2nUS#*~}m0XQa%!G%cBJ@9x$nlG@rvHWvO#Fr%;7K#tzOxg?z1q=Z`wue%vizWkCCIKKQ1{(JoASvD$'
    '2wVo~Q5}(z6qZx6GuAQCEeNxP!|Z%GRVIwOhy(fUBCaB8C<R#IaW5*AL<4;M(Xwl6HVDA5t;IdV9Kps`Fp5^i8z|+XM=$V&$p@i2'
    'jw!|@cZ;VO1k@GRS0K4Y=mjlL^t^gybh>&%Mk=lh_ylW;pNa?B9S@>7B-'
    'TgB_jx$S+(>YMo<(&WZwH6#Jl$T*=nBK_ifI%_Hbj13{PkFT-R|~(9*h)yi`lQ}?@;_Z6#ovzzYvNq-'
    '0pYIN*6YbEdZ7CRlo!jE`zD~O<$51GhOZmg0xwJ7!7bFik2$17T&2-{3BW%B>y;~!~B_$R-'
    '&`S^CqantDp{_3+j(IbLMf)5P?rK$gQQpYvXx3yVcmD@BgZFcBORozcbn9!e5?EWY6WXCpK8e=%8l*k}HdVlXl|ZxmzKAJ+=?L6M'
    'bd&`Cg5CxsyZ~0ee<<608%FnB>Ti(~jDNGT5(Bfx+iItd9c>9(bl~Uf;6=9}FL5$S@D>gJH*58><FJKZf{66oNgEl08v$$^O$KOZ'
    'E&u-~D8~K~DI2!Ng;$E!Vc2?}g}?H79E|UL(@FGfWy95!;bA7-'
    'p|Ps`=>HEeWz@Z}(#2`G{m%m6ym*cnB)nfy&lq4J36*tRLCS<R;r8SWhf{<I>B*i)cbkDv!T|tlOqF{WT>G-'
    '{^E*VJSI)<h(jZsxItoN-'
    '^SbFge$`{kr{gySQlu+)%uF^~D$0ySYKNr1De@WCa2MS%44t`2baoMWJ4A`vfu_c_CVEvuGXX>GXMT3<OZM>e7nXyguAIj#eqfS;'
    '8g8{+IQQ{gr5trI}U5yVk&sHM|lu+Y};>PUijOTm!smfcNivk0la;0Yd;1HYd^n?X2oc_N8_7EE329T`O!GMW{6M?070!qkSe=bL'
    '=J=$;8W9M~P|=DRe<8$X2!~jaPgqs5TZZ_z$s(-'
    '8haNe=s8&g(Yr=gkc)bh5&Zzk4F%o{E2`aGs*(f^t53T=T8zPL3NL|@gphF6()#*B|ctu2%n#2;}~;9Ul-(yX-'
    '2Z$JWa?JfPXwG4kJH{&{@=?`cRl4ESzx(w!gSI@EZNu6lV}WKF`B!okek)L`jr-'
    '^B;gI4z_?wD>#9<2AMcfA)Z7c<I*#PXpN*+)1rH#bUUy%eI09_3xZ~FxRv|D6E3%@w+kg8_@_hP+*iVr!7z+(5mnR(G8@_I*v;92'
    'qm<6aP{DYGTt|cMz-<;c1L-}DbH0EJ%t%A<nPo-nvv+L8sQva2f_HaMY>c(+qQ=;EH};7f2EzzVJlg!pEO*xTezo`R$>-'
    '5Z|Ek7lx!!(yi6V`_mWrquANIBnLB%m!u|3z6tOY`Task3sQ6MX#qkITlIWRUbiK3B5Wh$7hUFOAt(s#9|QZm&Pn@}MBs8{wo>AC'
    'tvw)CVE^$vM?W%E+CM_yPplvcRSW5mFNQ3h5}su(^UFlfz4D_4Zo`JO@S%Q=m5Q>{x@B&wC(HWF-trctNjJ*A^kuoFkwsND%mCA-'
    'cXA{Y7tvb)V(Go;V~?t{LRr-'
    '@9{m?ZJ_#0{fA18<eV|Lhg4a%e}2K3A<=#@DlwL>aX3$`#NQ7OUq2@93OsGP^bGO3`;>&g=Y;Fmld<T~4KEBFrIg(Co_^oJEU!1Z'
    'spP{+Mz~Nyeu3g+r#P-'
    't(43^MeR5j>M>ss09@rzXP(Ck2?WSglTb;wTvpht+RB(6h8F5;XNv&d#2fspRG)Tdk<mkU@H$?d+cRZ9S0BtR`Rp9z(BR1i%sxp`'
    'xEA^oNl%t(ZQT*rE*pGJP8TlRs2FIAiuQ?EJRM%Q>pc5i&iLXX-nJ$%v~o-6JXAk?^Zvq-'
    'm`gA$STowFyIM<&6m#M!tS~=nG?gD(I?(@PpdqLM>C&YQ64&1oC@>kMLh_;#|NmY)1GQ?V0QfB)tfgn0ya61*q2$EU`PyVa@tqGu'
    ';l~@Ms@)QQiU=WF#W5yj%jZ12_s632r5C`_Y}-'
    'M=?J7FiM6*1rZ`Gz#D~8Dm*F@*0UUXp!d5TY_YS@d3dksY5^?*KVmt}aBRwFMLPdxy>UK28uE=Ixjr{8HLWj1kVfDVA%`jz6=-'
    'HZh6o<jsenw_mI_z)9vndu+Aex#=)$Ed3rbzFh5C%9gOyNvtar@-'
    '8=Pb6Ber9&&FKDh>c7OjA`Mfj<fc<=}KS|Zqg+J}ql#b|t8hJytoX#+8u^dV;^P>jOp)fDXb8&MBHmm4U=FAFzN~5pt&1Pe5o-'
    'zkr<mQ5FdqFer71ztD$;_6?`tp6dzUts7^(K1hVMsR2CUR2O&OJmJ9Cb<JOWv}i$r}51*u?Ip&FuM$HIlVE9j!c7c)|;>Dlv@QHk'
    'H3!H7AtJUD|&32*mCEQ7CB&&vgfMNG=@7unaxRP_v6E)?;NwywZlYjX!GB>EeV~gWk(-R!VlZe{b5y5#cdEYr5-'
    'Na36u3My1~MHt#=+!o%UEZ7K~1nbQv6g_1=XL5k4@)}>{)nc;R#@O?}n`LT@6W_8PVJvc~Pu?J3I9jU$f?)$flA4fydv0*Py_vl1'
    'OZZ^;dwHDwB`h&Uj!90zmYs66Efl3`TXQw?fioMM8jZH00CLo)3!~iK7p$hD2xpsEo>#gO}vFYGCdlzJD6MGlKJa$iWGsZZj)3UA'
    'U!U}bI<(ej+b&zVgF_K}67M?^H#}(`m5CL*hn$&C9AS=%U*ZS@%KIo3!T%g%gMsb>MyGZv|oK_{TK7gBg`x&VhCjVM)SmB%ED_{W'
    'VG`C~k7SlCZKvFBR3av<K8um0szq%uY%<X~ign>bl1xaoV0tM*ekUX!X*0yz~J3QTXdwCS75k|`&zIY8vFt*pgCJh-'
    'WKAkgI$jp=RT@>dlUh{#x^fgkGSYa-xtNZcwzu$fJ&-'
    'Ka@fEHxZJhpXPLy{F>qRxR`*n62S{FN=rPpH@|s8RA|CwImR_CR>S{HX@>K@L)9gMYyci=pCX+ZyseD4+o$8Bx0PA+UpnTkm%gt1'
    'cLETu?|_zZN^u3#x$xq^aiHI(hH-hR^@(*P|S%0GKL&b93&><H6)O7tsb!ASM$oK}L>_id_;N1DD^4(O<p3wv(@1=M4GHw_mL6<-'
    '8{{)1C~Jh-~RA{en>*G&r74Q(%-iTQE$)a1~;Uy#QECY4|gGgSxG$8@=~^0<j~TXC`Hk9>zT)q^)N49wY!PM9hvX-'
    '2aQ1om@498Q)NL7K13xYJBpRv@FVF+l@Cbe6sV8FZIJjXK|6u^43`gGZlVc)F>pb3ek(-U;G!fdq{}'
)
_ORIGINAL_BASELINE_B85 = (
    'c-q{(TeF<GaV7dbzrvwsI|4u=k;wDv8GFV@4~~}oG;xBFxV320WDmP#kH<0p{j61_CALJh>MOR?yCm98?!D`>D-'
    '+1I7Lb?!_%DC)7eD*w*KgO){-3}2*?Ir&|LnJa74y4a#hbtS_Ph9cC;h8;?_YoY`YpbZoBq}Q-}oti^xgie5#R1Nuix&U{Uu-'
    'IZG89oU-zr^tAF|C)wjQlqKz-PW}o6#SB`V6MjLyb(wi+?-'
    'CERa$4abv@=mtaS!af%6c(mh`uAS@lb6NAyQQXQCiCrm_I_5)CA3=>^)53vKVrG8;qx5VRhHD=3w{Ur@UmaO8K1nS^(E5=o;Si;X'
    '$Mbq+o_bC#7<2+#wt6Xe9l?D$gzI9dudxn%^%J1?Ym#SpZnGO`pGNj)Z5;z_)`2{7Mgt8&Y?$ol3x9s;j6Daa#|C{s;A&r@M4lj3'
    'IEgxc)kC?SNQs`<C|AMfA??u{VVwG?RUTa0e<wa`~7#X=l=H9&0U}TCSujnz`M5D>#*XZ?xFi6IX#D$dRlUPM7X5)u6vi3&Gs~SX'
    'YX@vzsc<_uqyW3@Ai82-TT+^_UkvlezR}J`%m967cc77>pHtti;~-'
    '_c=d$Wv=t*tEp{TOveT(mR^6wMJWEPvHu=pPzJK?IAO2_m7H{6Xn(@tVe)8>i@80i!$ItSwzx7SL$8Y!QKcDl9@816ki~9ZkXs};'
    'k{l1=`z5>5~_3>F>zkm0uZ+_ruw`cv|zx-'
    '`4yxHeICukAxC+$;~wlYfBlxLXqK2}b1*WCBkmd>u8_EKpj*D?l{@{U}tJE1IWz9v}TwN<w^niYvT&8L_~@v{Vba{6AmCe8g6-'
    '%YlJxVL6c<b?M--rwbftzw8YwZ|?as)|po)l6(_QInd7Bt#;ySf?LZFvP@?oC{IQWL<W`MpW@6tI0V<M#^|GO~t%Kq?#IniNM)8?'
    '*rd-'
    '{6;#t16##Amhx0ic>VP+@7oG3u=>3%9UCFABRu#Tc0?xDAHqXkvf+fKu@wF}p7O5AOU?(*3Aw%%W;>2}J%ATBrJRPB_0?)lz9eg('
    'r|vZsF|f?i`$}4Ss#6V%U`u`qFZ|;--'
    '&{h44M=P4=qZ5TRI3ZjTUtrStH9WbP_$w<1^yv6bZnM<W}YySx%Yb63u&89$<e~A3EmjE*x-W>u;t%-'
    '?0H%jtP4b@VSD$T%LYK<m&!gad7=DaFMKfAWiNd1X}`w{ccTJOGS4|>jWKQ2*m+MGn*^ZXYnyXe9xwq`uk`{Nqn+L;SflWsUv@%X'
    'yTkgqgAObh94lW%c3m5RZUcbvWz*sbPKkmQkikp#Y3tOiuK9_aa6c+kRWQhj&kQy?PHjtom%Fb%PS^w!s%`g}QRXb9fh|D(;G2<Z'
    'Y1iYC<v!PdYrB*xaO+^S0{~gA;ECn<916mOsAPzJI?mW~+8~yn)%r6z;cirjHPm4IoLbLbO6r@)xn0j%K*Y2>=0ccGV>De6vbvii'
    'emDTauX_Q3Mxh!IkG2<(QNWNatbjgqu2Lt6_^4J!4NxaIEK9Ooz{S*uLtwmoFT9C=fA#ZM=~cRK8+1hBF{>-Zih%lChfc6?M2XG-'
    '1rS|nVa+4-'
    'WSLc>L>itwofGY{0~RELB|D`;!&Ol=5MFbryNun@w@!!wt2)FyGWTF>9ZLj%z#vNcT?b5l;t4VK?Y`oJuim{o_Zt4w$9~@0`7Ub%'
    'auHe6cEl3xpnHilz0KpX2dGbpN>vJJith`MPzP*Pur=c3+^<_3Y7BA=vhF}yv{|QAaH|8E8VU(mK}12k=8S+?NCB*O5Mp2tpm`=8'
    'FVx!QE^B+L*uFj+6ew1&!LFyb>@FKi3j)6g!tvaY{Mg+AagYGJSo9$6G4^$9dvsGveQq-cpInd`h%y>k>Pi!K-'
    'GGz5v6sd<2B^^vCY(Dss)Gc-P;1M51b>(`#LiP~2y9yspMjR=4EzlPmsSIkbm;<@<Yu-'
    '6VXR=@Cu%$Zs9;g0kD5m7YTjh7mUhGfbOKD5L&I%_hM+4OoUT~uty%^bQh<xSNNeXi<8~@@rxr(!MN738eC$YIZ?0803=X*ukF>o'
    '&8mBe{5qx+=ZfF}Yo^jdQ$21QO@N+D0hj;=(R8O0L43q?h0}!$pNX@2*#@j;AWrUeM81Y}IweO4DF*EhbHc-'
    'G&Am%RKQiBUXS0aWqgwi}c?^b$~wn4AKCb=XbLPxnSoA7qvKRLFQ<|h<k8LNBtG|T|MM<84aqV|G#nhks@!MhzxUAzy|7i#VM;`Z'
    'Xn3)RSUP(NtUiVcj93zcX|qG2(&HM%57nFKE!v$JjcT6U7@^;5HDIWmuI*POd&Xk+sMRZt4Z2zLww69AdS5p+p%UdCSubTlK7=kY'
    '?VeP7&Oz&w1A;o}roe&Fk+Jc^nwv#-E5Z(w94V>#*$i(Mx~{5}w;Iqh`W+HJvU2n}N|NFAbI5iQFVL<Jx?6GAw!5h0q3-W!h!xc'
    '--doaE&%)Y|nfYv-D6!I+_-0@%2c6`vWAbWI;~YQ?G(n*u>}PC^V>Q*<vxf|^Xub?rZVV=;FS$vQwgyXRg4BJ_~)AVdv^9-'
    'YAK1sCjnyw`~(J`#vG9Q86eNx2gx5jb1QSl$~tvnt}F0~~kVQtJUOZK!aNgr=PbEeaknT7aNSp8_d*J#Ooi1Cdgz&tAnRlsn#HY5'
    ')XIE3#&u0PPI@U$?GitDTuU9+ZZFtG-Zc--'
    'nXBoV>xF_a0o+c@*1Z#FMul3(_JDXo{&5i)(;740r@CfCQQ1>4C#V?L12^B_l$2$j1(mG@&b}E4EStA1p&aE_-'
    'pW2|5eF0-PpAESfC8P;1|Zk};Imp1fW2+If-z#SEQO20mRRfl)yoR>cDVW{&06Vl?QRNd-FlWovhcrdi<FE@O|4V9h&Dykf2pF)a'
    '+<1TNy;B~|zo40WDt0;sT2e7sO=--'
    'nXZyHCw60|0aKd`L)Y>J8>!k{j>}E9}e;Gs~<6@f7Rtc8%OY(64LB=}_cc$O>alhd^p|j8Rt|2ecmVmCLA*wgFiWNDhe4Gs{Mx*$'
    '8g(0<Hbk-KSDmpSdJh)gT&MLxfB@<r1y;J#5L!nHS5o_i-GY4_jf0*;enWwy$f+Gp*%XA)OA70052*NP|*R#_b6B06^myKpXt1Ae'
    '?}VKwx^fWbZH3+IPn73TVO_ik&Kg=`xKKr!XdCj~g!}f`q#+tpAOW+VP1sadCnbM_i92c^l#gDaY<351s@<SOPjI;74;r4v2f1*g'
    'pbjULCSVcr6H~?vY-oweO4DSV-cdoh8+8N1>U@yzbH4KtN&WM!W<a-ZnrC76>uvua1#`p67bpF6JQ7JegUxyVazGf>t42gfS+a-'
    'pYVuNeU(J6TPKS$v_G@`K7My`{Fiq_)7RpyDaf2!$zir_hyif4QhSc!OC)wZ&N*BEj?F<q%J3<)O=mJmj=QknpTgFSdzg}5W?pY&'
    '`JSDR;fCm*bUpR=X2UA&^A0mz?PaXGj88|DkTyLD%p)GS;CW6Z1TP|E5tmv`iuY(Ota=JvlQB9@CL%AgR9u}6IXaHr&QB!JJ*;3!'
    'I~BcD8fjCK^v30w2fRfYC(V*pg%Fyc+FSm3$^y0w+W)mT9Xh99jSQS>>7bU4IdoFl3dn7)HF!B11RlN5kiwLL8QGNw|NS{SHMDDs'
    'Z}O5CC299Djrz$8T%%wgDUY>?^vl`r;1{kr}0wP_MLGXwzN@4S_q4|4&GgX3wP{d#VS6z#iG<4sd^qz8jzM_p46cI_V(*>yF#ZF='
    '`eFXAen{Yow)+uN0R{mbgb`lOI|E(Y{YfMoHg(Vkn%E>`&W0LN~H_}kbCP0!@GK0%mf04^+*X3Ix<y7T0A@gZNr9cQ1u$qq2{Zf>'
    'wLQ>DE?IuAhNY42pI(g2TH~_eurf}=ZZC*PgKiLHCWcZsscT10aW%2wf23dQqjig6KiN;4<7;F^}PUxmUOQ<E03WeDsAm^Anllzv'
    'QA`Gs7~H3KEg@5Xc&we30kTao`fBy=54hM4xeJ<O{b?eu*cRps|K8~5Ong%FVfogo=UBw2#3Y@grHtYh+Cisu<{57R_yUOv#kxfA'
    'n;2q654eoBcyeIAob*&Q$Xy%^r9hJU<E@|s`U<*GHvPrNxCKb)CSt;CcA+17bZlsnqH{2??XvFptcQxGmaK(M8d?2_A`2Jdq;<~S'
    'j@nNVmAUD;B+4F-'
    '+peH$=8)T2sF={QnuJF3KS$WtAWdqi!1r8ws>7xM~O31%q`G8dshRPt{2L;?>&_QSk)$d2egeJNI8+*D%fBpyB;kmMBJ%$A!K&R!'
    '(bTzm$xzx=;8zCB!)=Q3LK}a!POAzx?@N_Jmq8Bxpzog=y@i-rJ4^OA)+$8Y3cGpt$pXIRQPHMMlKuB)stzht=E)nV6o|t<-'
    'kbuY0UwP&I@5slZl^}rLnKyCKUaU3AEOp6~GA2F>*MFU!z91KFR$vqE-WVGPD;<o}mD0&7U6ez65Lkx3}ND|Mypa^ZI}9_4o01zq'
    'v1~M0UW+1DtO+Af%-YZG&B0z;gS}*3Dd@=dt3>?xjKRLCg25&8j?dUsiO~f+gMIK?LPm3L?l<=qf0H?9svMXM*M-'
    'HR=OWe+HsY$70`}%J16z@Dsn9Z{B^2zrMMB@(U@=|MlIw_df?heK6d;PWb$@zUPj=d4tEi`dd8X?XMqjk4J1Y?M$VQC_Q+plAvx7'
    'V>?fbCStwtWb_;$>)NSQNpqC5nGOWFEf3saI<}U;5qK*i_1N$=LK%;ME8L$$u=Fb<k+wV>k$v`!w+8f=^%*=pw~vlJ_0Ly4@i~M2'
    'AwPWXIiK;u_Yw^6g4s2bg@Z!Q+l`jgv?`M{7b~0s^4l#T-p-EY+nFjcNvZ+NrGWQbud?X1dKkb|<M_w|Z2-'
    'BY5cefDD1kf&wg7MHp$ULJVM%V+5qVlEqg-@C`C%tq%H#aZQ@-'
    'y4ItSl=_x9C?5cQ95@$dVX{8lXK+I!1_5P#On%+!okM8Go;7piw423-M-$O@G?h8E@+V)I--6F}?-'
    'j2@=AVe84jdtjqw8<xp{n8iF+fowVp@3aai?qY@vXjZ^IpV<pve^{IE-'
    '@W_pGk!?F*AKsKw0oWLd!F|_kNj<nH~ZD!u+HMu|NHvw*WbMR_PzvX)<Nc-L2p?96={HKLr|Kv)2pS-JBEYk1=<v<PQ@8zfDZO7I'
    '^{aocl-'
    '^r!zCKREr|#P?5I2sf>5S(J!1i~1D@g{*k`h0PpV9@^O<e&_3g9&^M8KoKQ%~yYWlx_6W@M^P4n~naxD(?dO$`uB2ell2U9^ug+0'
    'JSQ?wA?LI)Jk(msPWIIZ}U&U3`;XTR_>G;3L7O=(BKz-'
    'DwSBkN#g>SAKA*A5aUEICSTr&bp4mMU{w`tP&-Hy=Lsi!l9H_Z<Y+dOJYqV;FV-7<yNjA-NV<Hx>)zc<`Gw0*_OJM#9PrCJz8M?1'
    '2)OsfZ`QeT1X%+$Kw$Hlh-'
    '%zmf`bY*L$1S8ucNR|1HyAzDw7wqB;`zuNKsTD(~@io>vNX`8Gcs;vT(s{{N__gZpYr6@uWR$RB~4az@5t3{I5^8+yKP}dU#DEa{'
    'DN(q?X+ANbLmkZoDFP*$ka;x4v7jL#f!KOiG51B7C-rOvIE!=GI8-'
    'qI1#0tZ`x^ZnM$l62NernsKq@~ZiI;abfdGPehd62&5bulL0gh_~n3b0Nlf&yh@C{(~=KEOT;YzKSLL3}`u=ZP55W`)JBzdzK!fH'
    'i+H+JIm9NC%{*V|6XT?w<w!i(D2{-'
    '*hyGG@Ic3hqdO5SriBfV}rA=2P%96Dx!CVyQQ&S0$XUWH8U3U*cm(s>Uf_X8Gyc|ml>A9v8q59>|-'
    'y@^8e%QdHv?it6$^~rKGQZ@yq?@O-'
    'gs3`0yTLmex+{eelRUyM*7$0UB)&98BH0NGDGM5Q~7XUWzEx()AM`uvR(N8e$m&$ymXod&gQo3Jxl1fd9h9shLgi8^G^8xvKS4SZ'
    'e$k<9{^!tJgO(Tv1>j4R@)w_jAv=!yEUVcD8+-Nr%-&&AO9RR{hM8I)DzkAj22d>g~L-'
    'WL1{@AX1NR8%ufU^;;^1oXWNbw!=7iM~PlX3+o_PrObtRM{F<_n6l*n9>R*g8cc|+&+3i)PD7bazKb73VIcBkc4!4Cq_&`n@!>6j'
    'kIq|;A^^d$fowF9(K@v8u<K{fDSYNSE9vV32n&E^%p8ytUbA4ELjOAN-'
    'z8GstaAeUnW_ZkH1$cnao=fahA9lO2}^%Yo2_;iF`#4vZ-iWBc`kFMy%o?W2nJnM>)Ke>tdyS*G=g9XtTMl2sjK(3Kyd@0eLI!T$'
    '+oN(PyoVX)mv=?O8_fkSdmZLe>{~p?z?lG=OjQg)0!$m4|7FDt@P2?41|k(fFa_`szvfHP|-'
    '!_p0dh;s7eoH=IrW<0JWIov;}|^%StdU9?@umqKYLMTQV;uA(yAm<V<M})?`1CH`t2c5{QGA02z9QKiD7!xC!Nua@n$5urX3w4eP'
    'QpU!E04dn2;+0#78e%j?{=^c_GU#KtPnf)(!uz^-'
    'L<KzI)USsjB{o(i3UO>+$VuAIR{#AU~y(;4?+I0Z6Dj5wl4<KZRyM&$r>VlBd6voL#V0WVsCTej<%X<`Qjcx@{W)b=6hl!$0_Yo!'
    'd&-'
    'oX_rcvP}m6Q_o#nOk?CkTI(!Xt&JHSdB@W&*_Z&AiS_Q3W$_0#RrCl9ddjDMWEYKhFvC9Ro*}ok3j=UfM&K*7B68QNV3`uvJm0|`'
    'T<g=LX>Cb$$>=lTjeZokOeTNAauLgf&GEr2fs@P2mjo;_KS4}n{`|YQy~mWW-'
    '5EN*_=hz!keEH2Ua_C%?gIqYi0`f)I2pUFkWz7uI~r#@|h$GrsTkZ)kaRr+YHcZfRvTS{I(1+&1^Vm?oRY>8*l5Nb4=%bPG{T~rn'
    '+u%TdX_XBN0TGfLLmSn()r6_5q)?l8aAYOaM^GKTTP?*WJzo7ok>;Ldn}<DwrOo$;7IYcW!uB4OTMBOug3Gj6HQ`2IGqD%`HEZ)V'
    'Os}xwJJ3k9i>HjCF(oY6<?7A+!?WNYa$jpr0l?oal+0fQBk5Af{lS-'
    'L9Xw)?pA2WwEK<#;d!X$>UsO87JgE_QsBY?z~mYR=kHFEC2+|1`vt-'
    'q~5r1Z&>C^t;~`@d<K;~ER@*N8WftWG!d^43y2!PzE=rG`OMx+x?TMGp-5rX09(lg-'
    'j^3gg?ZQjqMew#*P%oK5FK=_Lg+yQ=Co1<!&0VUf3Af2DZFtfh6jYi*(ax*6EwE=miP8Z4NMo29YUajbD1yRy`@ot8F3{x<H&dbH'
    'Y$kmZVUTk$*ri_AZd0zIzicZ-I~r}Nh(`Y04vyID;i-Q6fePpPved9z=5H6?dmQ`L6pE?EKTj>K$QVhu|ala-'
    '_RpPD7(C$g9XZtbt+3wy`HX-yLe=XdT+fBIA&;HaoC};fJpc`mP%;2`^d+wR$WX^t?dA^#v^;9`~h!VN*DOtbMElQeUU0N8bMV-W'
    'FTVX*q}>l6_FuehX%>jYFcbQWbhEX_zfQRGCy+l^gzM@1>_lvDLZqzLQs~SXN9uq%t2_%o&c4#Az*c25qKn^olRmYG>^?E^2TKuU'
    'WCn=4woxvl*Ph=1%ys$;EHI1wYZ8*hhg^Iz>S(?3Vyn4Hqg=Qfl7)=?TI}e^D2prrXclGjaGB*6-'
    'XTcE?wDA)(2Ka3LOYqmB$1&_H#PpzMTPRgw|l=08p2?E$c|EKHV_+(uJQi%Z&*g+%X9FY+eecbD+*a#vYL2lV==oBy*@10jaiJZ%'
    '4$1Da*=@B86?Rw=cXASlwa;Aw-athh+E*aK?QQE<=FJ(mNJA8`4QSAeSuLD=RG-Ub=|DH7Ujcq;t`p4fx){rsMm8`s)Po$1ulI$='
    'N{`PL&4A1_B*@GjC%FNZhSL!K@pb<Q>USfoVT<cKcH~<FX7tKKocOa4)@JEe_w<Bi$A-(<-c>P=i|sRG-'
    '*@KB%%bHjx_`S3J<x8U~)aC$#)x`dBd4FQlv*5HBEiMRmh3OmH(6SqAIzt);mO7R!j|bjF=hgN37sZIpLudqZy5g-D_7)p$}{tX-'
    '!X8-P}31l*eKVxwesnHdlCrUGQlnH0~5tY_c)%s!1?szcO(M~{m4JuOL@iK+I-Mo5~|pmGMD`b^HaEW^Xw?j-=^1#!m#lSgBD-zL'
    'mCNC;2|1`{1neS5aT3y{nTZGkV!^(sL(#3#|k@;A_f2+yV&+GCf3K<JbkV!-'
    'k=;3V643>ddLHmL>}_mg_#&e|Wuf~C1{uM>)oP3f}rfF@>*N-'
    '7Pq3$R@|2O(|gspDJ4%dBB%)a!>LoxR_DbT+kNbD_yjS3M_Y|J7QuFc&R$gEPQwhfe$sfk3*L2$YXKsW<M!@UgX)HWCxF&)5@Mdl'
    'qUsXuXlvp!8zx0tZqw38rqGToLA3THEsVT-bh?9%UX)XRs(}G&a-'
    'r(}`27>~m`|ya7!3K69n3*@hg)uMm>+i}%Lgy?g!bcdzaZO*?5_Yi{jgoYIn+9R(r5#)VMZhXMn77|f?AM6$3TEp9r@KxwZ71-'
    'JnSbnmiz&Vx-B95G2c_=3Q>6>^*nvGW|OyC3b?8M=I6OR~KBGko@+_<1iU=ReqO`G=nSIWOF)x4ShrJ?waWvX3-4-'
    '6s3tB$x~@ECX(q?3%}vCcH~>H5YIx;KcO=9i@ONy4ceVe*u_h=b#q6Q8wukaFRgrRq>_6PT^P_#7bcs&+htUUbrt5bp-jGHbQT$d'
    '!O8^?gCwRTo9z@mO8+uMs<9DEB6Q%B(ypHX06@zjKRaq=3oPx&I(-M%uW-'
    '+q6a9_sclR(Wm*c$y2fFfe_<Oh2n&_g%aeKG&LaO&GK`y3XR4sHeQ<_p;Es|{vSUq*E&K*6l)+(mYR<E4UA$vB*CWyZQ)Y^8G{}<'
    'XhbO_c@#b6lIcdNlkagatb0*GESDgren`t``8|%rua9<)0D;_%ZLS<{u0eoDEle^}?13dPDfF3&l!9H?f3pg-'
    '&?|7EYmQ=2v0D|e@oj|=nc*WRCm#jD{ha)9jtpKGrTjYoZCnH4#j5}*%SaA1g#^_UcLGPogo5?Mn4wWndjt9im%soevG`J`=@@gv'
    '$R@3<eNoAIKTE<(W{lFbX9B|#>8Pbd~mndk_1m^RA$x|O3Tm=NmYq_#i2%FAh!WpbzpXbTE(C*s{P^exv$3PVJ2@p000Eb@)-'
    'YauvP6SNOCb{EG7C9FW#0=;K5~cD$Cb<DmCKIh(&lXlRGV(9ru`GB6uf2MbTpA*gf|z-=2C`cBDtY!N^Mc)n&Iw{|Y8HYqZ-'
    'n}^#I~UwdaBjg6Sz7DL#XUss3tlX`+#+NQhOk?fZa+1+62N6%(RwKp_)OEDr_$b*F(f@5ah%}oW0mqN>?m)aqCf2Jee2zeR{zX3('
    '6r>HPj4SfCapE7CY!71aPV$P?KQ-'
    '%YQNt5ISmgFcxJ+>Gk{$_E%((kBm29BiWRM1=R_=tZ#_vqa)=3nGXM_BfLjs$N8Mtp#5p|!q4~mnpH*j&Wj>tEbI^n1PtL|4ge-'
    'N5>}*XX?1W~pt31^pLymAr|BNXrgs_A`Fb(|Ox{{_Zh(?JA>2h_?+86iZtA1lTE}p-VB+9`0vJ!>!16Y2#s16*-'
    '<#V<eyN`L>h5_(DNSb0CyszR!?74`6EkOr*_&5iT)TRp*P3<K{SsV(=Lp!E({<gD)lT9>!e(CT$m}+eijgG)4G^rF;M+i~+o9ru('
    'mN}6honJliqBm`yiiyC{X0aaU*vlaGwOk22q{_-b7TV=Al`0wVvDusYq8dmIUI&{+y`veCCgw_bGC-Lo;}_-'
    's6kEwWysb|X~EKoy_107xv`sOP7sKYFoy?<#bvVh!_-'
    '^R_vfmP{v}?&ef4`v9Dj;=g1`2_eFqtc(4N3mu*Cha_3><wae77*m7YLSByF3{VR8cD%yU>4%L()@)^vNI_Y8cB-PF`Qcivlr4Qu'
    '8Q0qKLQfA=~S0nbA4o!$~h+O~Sj<}dS!JaA_R@I0NJyxCB;)aY#NfF;fjbvHf=1p(p+B2zhK?QAf5udAj3O~*@|>)8Ueu^DZ0pij'
    'b5AEN<fwA*6)Wl@-Yl#mSk=e>3JtR(@Ym7CT5nf8F(+3{ZZk?VA(!H29-'
    'YsLrWU1YR<*xf`t0VE1!6atbrHZQc?l})i8=yt{2kjf#lOR*n%X-W3NTVlb(-'
    'BbOX=(01b{kqgTdCb()9?JwidLj?hJFlXHQ^$$LiTS0yGa<P5%tQ*7oPv+e+idMK7O(8V;X9A@oV9T6fo{qxC5{UBxg!UlmW7NE0'
    '|;^01kmbCg3YWIkhycoZ3i>Y$q%NUT%O1S_Z?h75>@8NOIbxDox{H1ORb)gO9DA!FS5lWrZd@nY=a-'
    'ob6A{OeLhg*IE<~?1BwK^n1^*RYfYJ1g~tyf)Xbb|&9T9rK!mXu3=#p$WK}xqi9FEm?B02rE(x*?L|=fSrV87GlgI);g<M#`MCgR'
    'ge!ZPNANoyfAy_;Tg-UjI+*dV)a^4OpW*L}+=oFqN{z_eU?`fU@J@Z6AgN?FhtxL~O<bnGREVT8;;~(j3A2z~j5j<8FrUey?!%Sd'
    'Uq?itA$xiKy^}y#Gwt?^mhFc@(xi^@-Fz>!hY&85S;n;VJlgycG4=sSOzqeYjLq|<T3Peh8Pvn974l4%Ji-sRw4EO}k7qC9)(w--'
    '`!I>qr@8%_++dQjVaw!0VC3Xn`>H1*>m}q6@{(|qV^-@pA9%L_wxp}XTT?sPE3xxztGB{>)gS#GH{=o-'
    'N<N?3W13Z(<>)`*`3as*QD9Fhj|Bf+aN*fcx>~Ny)S{zrh*oGFUfk^Uz2Y6kO6qJ@tve{yPmqh)=fs?U0tC`&w2ZvsJV-'
    '=}wZ^MH<i({W>@j$uzg1;mmIS=v<9v_2iHsOiP8EHWkDO8s(#DG3F)G;suLAkfn<<L9VqtHh1hvs146;Pg895F68z%meK5tTr*0x'
    'p5xHrb|NW&sUhq41FEMGyQG)0BVhfje{Y&cH_-'
    '2s)6uE;dWzM6r`^)7OBvb3;09h93h6VCh01uc$L+X4Q`evcC*r$2Uj0arWmlEbMM$L-'
    'J1FP=?b0JCqH~e{oHlMJDMeXHN8ZA`jfBi8Hxo@7vM{1f4ntFR{h}^c|YN^5!OhyNEoe9R+&_Img0Xfd}>L8DEgY9r)|VawFY`Fw'
    'PF13)%xNh6iE0B~BG*a%?#%2eXir-HAYrKX;}4Vm)x@#FZR#mC;)BQ3?mKk$tFm4@$ALmLeLoT|M(mKQ>}U-'
    'b>j*_|$U!h?ITQB{PgwX_ak3A@DdTsDoKSm$gL=l2}Y~*m|zi46(4I7GtYic_I(o+09=})7ap8sZ>_r!VM=$U<>Tgg_j5j5K>e|E'
    '(NNA!wJQ~DJ!q|*8^9{+q3Wl4uPyNwnXdfunX2@erhEd+l~DfIhBPKJ!=AZ%E_%RPfz3ly|Y?jS(|#x^&N|&A6sx_Sc3fG&_myx0'
    'fkVpQ%CG>QfB9YX<Z4b`GGEcZkq|&sdFH7@|@V%FebwPM&uXpptud);f&RNKC~T$ex9v1w<hh0JaFelzF^C9l4og5zby#vt=H9^j'
    'nX|z2O*5z*3NzLqERcS6X}>$A(9`^#Cmq=3*n`C4Ml9pOqy}111N-'
    'Zz`pk3;e_@c#0x|qo{UF6P>Olk6M5i1P28}mV*w2++c6|^({8NJVClIdB%hPmv2C>!AdNuCcALnc4$4#?NH^u}OIqxI&aN@+TQiI'
    '^a}5i>aV!)>Ae2ZXKP==z*b5E?VDk>!0Hi1KK)<sy-'
    '#mrqVFSdU4Vjl=HzWjnVIDg6gaMP|Z02RBGt)@ZSw#boU^edcJ2DOy5SEzKd7M<tfcUUH=U0xn&BN@DKMmr9Bfb?8DRJO%?HStPi'
    '9B$hChq5`D${%BO5mA@2UaGh8<yfT69K_qau;?fKL+87?E%2%sAhj?{;&;t6lN~B%jv>)w-'
    'Cqb12TL#&p(P)S1b!G0YC)EQbnMe9A^2sQs<ZEfm;vD|GMWt-'
    '`SNFYuY$E8%*>#J8ZAiZbK|eV$WeRA!aZPY5_!T;4cghGyo^!q`>P#iE~RuZLg#g6pSepDwD+^ELU7><fG^CEL^hnd>U_w%LHRhv'
    'yWz<5ykKMk*~I;|55sa{>Io}-8pNABCD=jj$oPIAhNuze#}Sftl{qD>Kt=ai+IMS039{n-'
    '22)OOzqmN02MY{0D>#TbS;CW1Hn{LIny1{e)r_U<hsGj;T@etojeWsTrJv9Z0xV%u)ZXvdzUxoghJXQw6L{!#-'
    'A8<DU%Lr4%lNkHPM&|xGPo3+7WS!Lm9(J*C%(0ahd|?RK>~#&H`%}TZHw_VPL0D!~a9jA?)BOl!7M#mGyuHIH3457QcPupW58_Ep'
    'X@1NS_>F0FrH3R;f&gNFFSfEdq9#lN?B|Jv(4l`w;fy2FXk<`Xe<oOA9D{my{hQU%?_NM2*<7AfJGy(Q-'
    'A}9xD3`{1O0E31AN5j=W5B=Q~$-zs(pfo0q4i;F4*uRVKt^N(mfd?CQ{$Ge9<3R>b<swvTBuXNluwbFY9d(org#_-'
    'FDM>62A~bH_OWiJX9&t*y!$*iMl>I#bpa-(4@)-'
    '1n{SMdsbX8B7$^xO9`W(`_IcJH=Btv085O;NEzz*H2azUU@(|Jy1%_pbseEBrf3u)4D5rTClBw^X#<b?uT=f*x>-'
    '{+59%3untuwM7Eb{?sDhqo(8GT_F2#*>DIQ{SQ}=0sGkBF=M9R{I=*I0NY*ZL@~6y}Kqlop&^bGSkTlk|9w?!`Ah?W!8oD)(D}@R'
    'wEbH#BtdGn`SVp{3$~;FH@>0!x-|9Z?#BJ`|ObFhm3j2?C9>I$-iDn3x;H~1Mb?O$$usG|pIraT}N#1u0(hk<A)j45=OIox}4t-'
    '7=cx;^81qa8F$wcPOYJ;_QaH0-;?&D>eTkc%l9CWf1ux~AGtgK}({K9j=I@4_|9Sa(m#<a~~C`i-'
    '{J=j;Ttqr@rx@Sk2lIkEp(|NM!2vzHr9>Vg06QC_+B*_`UtIyNYW(!qYyhl%;8;9^R%zft!1ZzyQU^^wY-'
    'RDe1knKK3OADHiyI5~(WJak6aswoh?J_M@Zu;v-ju5K^gkXxn%!o<QkB!~Mc@dl-r-bL5WiTTmGOH~?zK2egNHWh$i`}o+*ZZ&Io'
    'BNhFFV=1uc3Vq_jA5rFQ)gz))aJR*o6alju}ISZG`q8|ce9t$10xRr#Ia^m<H(BM3L^5^JlEn?qphf8118y{H!BD!Hde#$*5KZ~P'
    'Wnv3&3k^{R}&xjCo%Uwyxw=;YGdne1Id8oKmez<5M9jo(BaI%6Xv(LAb|Qg9>!UpTR3J0`Y-'
    '24$`jLBEGcRn5qMa1*c#l3XkiC|3>4dVxH#c)4wSO0qm`yUDk#hTJ(}{n*ZU{5^_>&tcR;x3H9!PF4IDb1_eGg3?-'
    'aJqa2sjl#U_&njAS8_Xa#qJ_%M6G*1*0s5sB~yBH%!+0GgAO3U@CbRsuwXxl9P@h#x63;|g=X4~NgcNL$~Ty*;5@3K1yRnv_BYA9'
    'By)Sau5Tw<o)FhP5`?5o2nA3y%P42^KUwQ2Z=j^J?JlOoUpjO*ouRYy}!V4~-%MF1Vm}dg>ZY5ve!0DX3A5m$|Ox&L-'
    'X)N=7U}xn*$c*c+r{a^OJE4Z^NX4zbx4x)PytV!;)LR4nwBOS*m%-'
    'juaEM>F1zd4Lj?BA)Y55LFt&20)Xy9Tn_<aa1E*k_>SSkX)v}AY1>#`*{29+3&x4{r2k*{Uz^Q-'
    'pZ6ytgD(KmbV|K1UFrk)2{$qo2?E(*$UP*Bw!vB8gOz*+p48K(2qEJ-'
    'Y{JS>)3|~Fj*v`KJys8d+{=0>NaN9Hn607L%4yQ1pnuFy5BYVcOO6btM~ZmFRozfdwzLyZ!ID0kZ#h$v?uliyR}{b%yE)1+aZunV'
    '8ag?MRKoEI#6w=(<gAXUOz9)^~{qfYJtz0W#m$Mh{9SzzPfUk9N*>48kN(`xJnMMtXbJJp4u&J=62`oIAwh+f)r==)KQ@W6Bgw<8'
    '}2&ndI;5i&Z>5#E@6tJE95N5zDT{Ey2nfqfWTQ02#p&68x&pvNd<k?-N!9g(%L=<PW$xM0s9+T30(J-'
    '70>OKyX!q=r<x5R0z0E<w>}a=JK`1l)m9crgRHPYu7M5;%TR#K?uh%b#+eTc`{n`9s&MH}ur^RX)xn;YVVemZz3JX<3g84%!hq&='
    '$La*|)N`)S=9l&Q+iy4l{zK#9+idW^eG~tOzv^8{22cT<+d4XrVR^&cut9+G9l_om<h2<y9Zf=GaA3x0%uI!RSjX}M{Tg(d`-'
    'JGgPGK_T=%+Z~WOKkN!sb%KO)XdwCou&yJIGr|uB!1lVE-_T{oOb5zkan}ef{yXU&ufHXs&D1*gyNEA8^cn$0FPJg|ZU}ETB9MvW'
    'S-<!I5yILN@6<lMNdRu?6&}speTYs>7io4s#FsdSLV`Hc5s@Wlb2I^+$~}eR=!T5xW{74-'
    'D6}CHAqwZi2iMNQ|<IwY5K!dGqd@{g&4G<%duGGLpf+?~uQXe;N1AC1vMaD258&4?-'
    '{OwRSkE{Ty}|n=<M+JPtC!!x~e^6yD*)%C+m*k2nN7u7lxC#eajdCywVb_s)GVH*Nq>IC8nMUf6P55{LJdHL=;v?{~;Q;Zwg{cYJ'
    'kcR!&L~8zTyWkc`7&-'
    'N7Exz!GV(AxdtuDxu9ljY{OTJ4`qy@BDJPuCYV)Y}QBIx)IED>(B}xWy&Gv+;R3>0VBjeu@`4;<JhSj9*MP(^$Fea3pQuGYj1eP|'
    'ITC^FsQz^AodVH%7Rvdo$#;~9YXz(HN$EgE-kAsm<Yn6?FSMy(>X4jBxIYjbC{E>Z0y&|<X8xHa>vHY$Cg&@p~Z9e22vh-'
    '%^z^aw-'
    '@I^{1KgjC%k_EIUo?RJ~=QY#booV43(Y>E2uKoBWb8ghaYllY$AaFFtZAznWL~qeV~3N&Pp>uE(RjsL5T8`wcJ2s^x!CKP6C-'
    '^a}cq@9P?2;ARZxK&XXX=r|!6b8({v4y+?Qe$f*Qv8f?^eD+TKo<n+){a7~oNTeQtqaqL2!p(L|kzrcZcSI^b>Y^b4`c`BGkfz!c'
    'y58&Jshz-ZEo}Tm0)`ZV?O88!1>nQ@&?>OVDJ6mEEP^7hs-'
    'Bj2F2kq?0gq5G!M30tF93RT!ueI0$psjoxc&s(jbs+*rL$dScpBEUBOXai<S+dV<hV8kf&31f?Q@43?n4RrHRS-'
    'tE##1<h4}QB|eY@ZPE3E#prSWAEvh^e$V(sb(Ols!a6X^aN-XRY?t-@i<OMHO+x-'
    'X8sE;$<Z5A^+Y5t8)eJeh5k_kvunpija&;4=G$@L{Dln}F=bF+;nbfan3az;h6{T6r1~@>%~}K$Nu*#s?e#?5^F|vOzOj?5-'
    'vap0F`v&fx5_v}WaC;8K0G0*<P?<_Bt0caC0|JX+EioH}m!nz#A4YZW`0%@i9*M58cd_pUK=8yw2L^L!FS`K({ANRpf(IU?B-'
    '{1*m@t({Q>I-%O>z3l|-%^X`@06=g>jm43hwXd?SpT|2V9_%w0u*6pamT9q=!ZE|8f(3)rZNxNF1T-'
    'pj&ur&4fPR4d{lwAi0>+2|OCttChNW&PPTXc+cWfEO#sC`Rxs4~p4bssKN`;MpKw&xfLm!wV0X6~hwihIdU^CWq>ond=VrMxJzy`'
    'HcK(vz#ED<m>(SA5+-'
    'oQTOdA)MCKnd7)uyJ$(%pPVi^Waa{LBJ>+xzan^5IC@(b7|Bo@3+{y9c<MfNMC23Jj4(u5P^bCZKDPhVJkqHp23rOLkSQ`6J85!q'
    'ucP|u*19Zy82THlwaM>BR`O^+bE*Tn7_2FQ4o}t0#rmM1j$)zC#>Pp*cSy`<*+3pSehRM85`Bvk%=7}>-'
    '9?SGQj+D)w$|oMd9X&B3Ky~L-'
    'mrPPJtYPvJ}}>qn^SOO6aCCS4*F}y}c9j%bytYf5$f$@ZJ);B6HA;LTJ}j;G79r*#mJyqEwcjMQ*%w1w<#0#H$Tu4};-$-'
    '78=f3Hs=O)a?%qA(^lMOu;5n1TB{Jj9?E_Lrkqa0F{|r;G5V|J3oN;KSj~a@A%{b)^l9l)U*5S3bJZ>1;m;eGtaziZ<{q^&P!ncz'
    'C+Y+MRci5HMTUb`y^&#qRPRm!l_Hd!L*u=-'
    'sTb}$K}2eI9VEj9Si86H*fW^0C)Pi3WYy_Dlf+)cWTKzrE&7C7aAuklUy4ULbg|#*38Dvrw@d&!UkGCq@9)6Wpow4-'
    'ZO1O8o{gJ7EF}~u`6r<Fn#2d7x+bC|3EJcQ<bv-_9|>)*e0jhLq$EONAAY>b6W50-jVIFC;KSusD)S#sTKiDwX-TycMwhhBP^VP<'
    'QzcX7M!PZT|f5Y37}C(?}`>L9gvm5{7yOvi{NxbF!$Y8!nW)Uq13S+n&ts8S(h>Xr}oE#!d}@ZGq28!iPSp8N+|_O1Tljn@Tg8iV'
    '`c0b(Zzu}8HhU#TLseMfz-noz9l%W$oMj&vvH^At`qML2GC1ZHjv>y!j1`vaX2$zcsFmK%kz8!kiV?zQ!$RD#R~R~%@GJBp`fF#9'
    'P*Wc@0ESxA;4EI%)E!XNYs@Lx@FJnZW)vP3yZJ}B?4e?CdpE65J4r+1bMUsdQl6OMXuO5K%N8yt4)vUctVuFEa^d`sv5MQ*v1-'
    '$eojT9RRlI`6`{;5tH)|q=&;1r;>I%)W`9EeKhSVNuovO&VLQRq);WgKy2owYTN%BBA`kX=U}KWVEHz>}Ko;-{*-r;5m-'
    'T#W!qk5sZCD)Bs!)=f9U)8A4WYsbVDQksO(GP|;o8_$t8Z~E>GMGKIdEw+^&i^-'
    '#13X}1@FLwbe|LQXbaVAosIR9p2yKF9CyMbrnH{aC3gcoV-Xwjx|Gfyd3lM&=+FY04J)d4{BQ=eW$!L~ti;y6DY1bqg3kkUQ}OJz'
    'CI}peEoXCzF9)FW^q!zEUV&<4y$zZqNRm58I_ws1KJAHs{zkdd143RZ^kDETGWJGXch37Q6M^e!2T?9O5ahu6UcsBAx*&?2&M734'
    '<9g;DCr~0rL3t$5DZDQ$Mn>OxaQ@xEI~Rn>G<xZ)^7aL2w~Yl<T9bBrGK~M|mn-nzdcht@BkJb;1{1nUWfQxRc?t=d9P0#pm6^>7'
    '1OdWlgq@`=e=h~@-lAU?$AegN{8&c_<N(OSS*_(JQ}^V2wjuak7%^Sj<~cQ+EHPt7(^J9wM}J&Eb_hj~DMkmL`D$7TTEL-'
    '3@*dDBb%X98uz9Ue*l}iX73UH%2YB%VDZ|F0oq^YpLl?(UDnkcl7^5<iX(gs}vD<%GQz)WSfhz(^SXO%Au>NIu<33QIlU?{vHpK7'
    'F?x`TbP-'
    'h@ndshgx%^V_Sm(?~oFs2q^MMD`Jy;{a~@@qVZfyM#JzExqhlWHFmS_FYJLp16ES^;Ak)JO*z293b>YzI785!Ig08}|$Mi5<{3WY'
    '`9)T&+Tbtw^V=25Bwp@ZJPcP=+`YTXYP7yz>4W-'
    '+thFQ9jJm$eDx99prZ~k2|)ETC3xg@s_;qj9!DSl{g)P$$px^EK<$ShUfV@p63a!#If@muo{`|1XjxDti)43g!cxHlK`=ub6jkIV'
    '8MpgGU6D7$@MnGYZjddJ6i!ytF;8*GfF8#W3qj++T5U9Q1bw`)&~^g$+McLiJ19}c%HA|`R+jhGP|<V;N*l5qZs7)u55_mUX?@SM'
    '+oqi@g3`U1Up2RGRJlNh{{$&JGI4plrll+CetZf%1L_P%2WE5qEz-<l6lJRoDE^DicUY2y7E%-'
    'JYT`{)W)rM{BaHT<tv@j;S++{f<hdLvV=Dx<*3dCNicL#Fyh;5jNTsTgMbZYh<t$;c1lbTXF29k6~MAiO1osmCLL|!w;Q#Ad;`q|'
    'D%IxG;d#Dv>Ar5Qv$b<dy}{5!Ih;O0g=3RshcXioe*}2nAe$S}9FHzza0;J1PzDM|kU)!;lrvMa!(rtnc;nSpfj=Prgf06LBI01K'
    'vLljZ=yry(`h4EF8_)aLbA=%YU?bGjBb1}0iW-~fP3Xivr)Lh_0kW`PN3H;4c4w*89!P-'
    'T%bzi9wcHYz72B18CfKr+L3+WZR%sA^?8@t_K!bo{xj1hR=bq__@SLS^*U@}9bK_5T8KocIKX9gqs(NEh&1TIm^Q@v^Pt?KIMO_A'
    '-rHhRwu3uH<+x#SUipHz6Nyx1Mj!MZ10SpKMM9<sC$UqWppjW-'
    '9W*KYR_>%gbp9aluUb%qfb<L5_o?ZHsISUJFA=7(hb*JrB47NXDJ5hLe;l%akot;)@&)Xj8G6FP!&nuJgA-ES06*>2hXPLcbaX2W'
    'GYOyg`SiRl-@&sN-c&|@|<u`9!Kyq04#yum0DRG2-'
    'N6bQSx9&W_L#UelaI7ucePYvS*}}FN>0~y6eq`jv>Rm#|iNx#2!O2g{&AMsJz@&6)$EuhWl02CI$_~55636n6mY)bae&dV#a2)#p'
    'Zot0iWxy+keM#7bWg&)R)goy1;{%j5*;x%*T5CO24Gppy8|M1XKs4+QwzR12KyYVbasy|L&gKeoXTw160Q3$&O~K~a(~U`8puF|j'
    'd~v@jmo35x()g@Bk`)AyhL~=19af?PO3TFNH^>dnj%JGIxOIeL|4>N}3?!S1t+=4(M8`aM2S5}r2|*XyT7@3UqhMRk-TcfJ=hVh('
    'IH~w8o(aWo7ak8Bvv2S!9tOs=8`sZk=48Ny?uY#y=UiQ7bO`nufO6_(3TMu0g|n_7>dI)*c=NHKA#=U8UWO_>9n@(6C|E^ZHs?UG'
    'BY8PdIl{nM3YN^5J{ypKbj+1=_5*-'
    '~qJS6<U?!I1Dz_Gd#Sl$^7#wtNdVnWmYRPOAQO~M{BC*(Ym$XtjBoGQbQ^TAP<}GM7b_y?}1IO61mt|NBOnh+4;;o8T+4jJm>l*z'
    '(9dZHA7vy$bi`}J4jl9~nOkHsbEyJS;h(0hMr63=5Yw8_F8xkC=XV)RbYKF#R4KB8tOxC@D8WhkqJc2U{*e;xh1lT|e{6aSSb;`i'
    '@<@o9OOc3&^JMQck3AHgR)Wi}{TdYG)-'
    '9|tfwJQW7GjS@Q)fJ$^eyNKc^n0Da_BpVV9vCsrqsz`366g4$Z5xzooGK#hG(0&*j^)_`EeOW|zSx5`8q4vD)F*Vu-JlK;$TD`Th'
    'ohu7!~lYm;_HAkge4|+LF`&cc??L~$KYV}Ie;$UU)K*2Q<Jk14xw#=Q$s=0`rzQkv{EWHaoSnq3_Ea)o;k+F`<4bZpAD*UJ{_n(a'
    'Mo@cF4$p7IZCdJk=c|$h^Xwk!Pbx(F+w+w0Pz<K)-ps(+m$Jv*Uw9K;xMNKaX%}FUB-)^Zde$%ngo-'
    '?foo^o?q{3NVc3we6P#!+?KwgH(qa4PgBKF)jyynU*xHA^!3B8Qa+^!BUv?dU*#UON1J}l)#nnAhs(!u6Ej%%p`G%;pca_Tgm4f$'
    '-GA4xI#IC8FK*|=!nOTb;x(FKQf~8gR6N37s({_AJ0JW^Kb^uakuvi4~3nFC8tn5czCc_Fe`R4Z6b4rp^Z%v>c=omjzf>Y}RE*+g'
    'B1tR3ult%CXtt+u9F5n$ul<5mSiylr6UZX_mW>1GAmyX*J!`UxL*!m3NI~jXu>Gs8R>NO{aNMN0UczT=rWZ=g*ZGjlstrNrp^TIi'
    '<npxd75T*)1qJr;wNQ;_G8z}KCEZWHp&c}wt!eDws#*XyyjPAG_)SE+pCmz=2&hD+1Rc?j-9hg_kRO&<-'
    'o#B?G2h>ZjnGPbzsJ7MvH&MM64lAuh^JBUjJiDgXp-'
    '0X8%7}${mt3JkR+4c%$;@>pULofE!a@DNe00dqzJ4=)ZU3MB4a*PlsCRE){kL21fq#69e}C$qUmNe6ci+CgJ@D<j_x}=aZpQoFZb'
    'GVyo;m@boozVtZVZdnGQ5Rwhn2h8YH4_l*<fu@RP3ytpd3EE%=^%o4Da-'
    '6{xV+kH~OC+fAklB@gM*9FF*PB$AA8RzhnK6wUzJRz5CpFqVxy5l>N48KDV}St;}Bi?T2^z_<%=^7p%+NNoS1VgCj%FJbM@3Hq-'
    '`2JG;4cs}6Z(y;=GI7~z}(;`K*0-no6S-!tka-__ymx6JZAyZv>1^RWW+cbbM?vKfdy=pqLyHs*i<yaskALNVxfN*yq_wM;gu^3|'
    'C^o2+7urkuR9@9K|gvww>>Z+=hL?EGUCrvAogzunRE+B$<$^m%xG*80qwt%JkaR9RK6Whvf(c#_U7rK^}>KUZe$7Yhi@C$-'
    'scx7)mAvr~XD;AqS;1a%@Y0DZ2fG4)WPaadBCbJhCso|d)pfsn^>G3(P-P|szv-'
    '|mHZ$!M!2aMcakvfN9`b%8MPnzU~faR<CdTHw8F0YKSKp{nx?HmZ%?*Hano54A+RWVuo}cFsuonYicqY^LD5&b~$i^%#g`&C?!9J'
    '6q)POjH4<XF^4MIy3i2u-'
    't_vBY(sWhL`MDi(sFY(#SU?dOxM{V0p2E?wnm_#KeN*!32aTE9Hkk@A?keW3NAo{r+Ivi9ce)!AsV&j+mwe0%R%nVZwHttPlYk7)'
    'MxX$dWhkJLgz#?DDC0j7dXYOZhY>?<uYK+Y059?J^HH{BVN`<ic*?W&sJ;Vs5M5c@U=E*pFA&ZP1~e%4Rpv+Su&=N3q=>Y_9P~Yv'
    '*^#cAX{t(+Xf>H1%B*V04e$D1;L{%?*~QVFM3nun3plPVL90^aK(9gi-'
    'H@yYF3#c~W*!FV1eRfnCWS7AKbFjTIO}98B15ZSHSlc2liOa~w`N9pU@wcI^*0%e#iRfZ5ToN85@mMfU=IV@c0s6fEWqB21yiKxo'
    'PoHXvjIL2k_SiZY(gc6atpyJSR!HH(}9ui6az6>DqOlpAMw>l_&r*-yb92GJ|^Hd)?z96X9tpVOak``+2=?3x+fuqCmHz2|17YD-'
    'yb)&`=d3BX)I4mpjF$!_Yan)hb2ahg|!Wc%}2i(k5-EfC#WXN!_xh4-4J6e(6q<?Pdn-CU(Y(2cZ9t#}lNp0`w!H?jTaVZ<+DGMg'
    'Q8>V!4qHh|KG0FPM@FpB2NOj=F>$t>AlHP{=E<=yPfJ1su#Ui2hP=EL~*{9B{Pt{q23tHFMr2OI@akaui(xH3av`m(l3mM1%<h4A'
    'XJh=wQc>u_k*`B825L&MpBT!ZDu&s8L!wtTql?4ZR(p~E!!%$wsFGL~3J;43sNR-NhLIGA~AEy2^hCpB1kd{-'
    'LQR&fuuX;7Bhrm`9{=j0rNT*H=S@iD}&wG74_=J;1|T-sS7PiioET+GH`0gaTN5Zu|VdsL_iP6X^!vX<%wsB-SAu%V<5&QM{|#i+'
    'Y{Iz{-Y3|1dDn5e@#U~k}To0RxO%c+jie0h|7V|Gj)Pt`QV8BP(A>sXuwRi1TA>ca+ORd2vt=4=(fsbV8`-'
    '<zEnR~gI?k|}EyIm`(Yb~$UMv!O$^b@r1QtUaz&GpmwyneCK)?2PzS*?Ms&$(mYXU#2=a2*jj}(UlQD77vfvujfe(W{=Yf&CW3f%'
    '*QM<N#}l>ocWp@hVs$ZWGDRHOO%y$MpmXQ&ptZX$g^(A{smi-'
    '9XIPXFsu|cII=R?WG>*^riIfMu|bCng97awsczMxA8Un4NKa}oe_SuI#Ueu#cxj0fQ%JWE$@1Bm^NjnM0LZ$eEnq;U=~n9nD{-'
    'Fa{kaVGKi(eb2%7BUiSIA>n>SxT`*|4TYZrtl<{O?ou-bgiy;%xa*m^8skJ5k$Y5|_X!k!kSa4p%7dvN*9oA{Q)!C&7#<Rd2hXr8'
    'O~`vMh^cD_{wrmkK$cq>$8u~8R-8(7Fx7_yh9gOtQ_?l7oLNG8B(^Y-'
    'UqzsE&^o>s!T^u&4gx|TpRSu^mFp{(*lm}^~FK_NLU=TMuImT;gJ^DO^7>?dDvyU(m7$j)1be@U`=8>r$8fy=?+IC!hyI)U{jYgZ'
    '3-Vb2Z-'
    '`ycss|0lEG<B~yvoa$_4jV%kcnbJBsx<g1ca6OKUR%J#+G3YK$dzEs0<b`;7+Ud`0zYo29zYsoPgw(}nv|E3ZdSZ39q{&49!)BiA'
    '(Uq&u%^otgWfwfG<|eYUmp=>hJ&qoIhz-uv@zWODhv=<?H0NsPGg%?VgfJ;GHc+|T?s3)vjrO%-'
    'tnp`IzQ@5sI7hz842fPzOrR{Z<|C8mB?Bu{N7;uRIjLCXkT4rt^5~Xc=JT5GL*?+7ZeGh>n=88;APPo{-'
    '0R>BIBkthS!PjPdP)VCmNeXD-^QY`wGE=*pN07z-@H6zLU?0mC&4b|u}EzuwL);{7(T&Vlmn{9D%jJ$LUTjB9Bh7>(-'
    'Uvrk5@Ebxcr*ra_scox2J>%IH!OFu979q#>5jAk~dS{Kx~A+T`CI@btI7Osec~!dwl)1y`+XfOvF;i+kUX-'
    '!c!a3)?DoS=C#G(L}En7a(HT><t$ccwBdgq_A6h&UD_(Vjmd0;Tbx4*B9>_`998OTx|~`HOr;4T*sE=<L6(+<7kxVJ@^|lEfBW5+'
    'ToD=;&@N>wJ3H^%L@iQ4$x0c!vq4c_d1F0V17sXqoh=Eh7zb;1`*8!_Kk?K2U}egej&T2Iug5p2bFP(x;5DrXSYZHEv+xN)k<;8-'
    '*nN3I^<sgo##;%_$*@~fjnT_<+UxNRY121o1*Z<B!(NGv?HD+69=osQFs!}<`P#>_2`N^}m@19^k!q@?KBv7N*Z$K+YEWG4{yEAr'
    'jx@`>F%8uLeQ>Z<5BNutk`H?&HT-Ms+)f3D%j-Gq^|;oL<7XD=)6r{LQ4Ra9a0*cV5YAX73h0C|ojN%<sbC?-'
    'G&6zN>gPG__4w^zUWim|GrL<p38oo45ZZOJE`7DMN6y{WUZ)*{v_F-XVt~rhGYi3<(_W8X4(e7mOsKsnq^3_!Q;*hqX{-'
    'btDfclHfhu|OIN)wgEJqdRHNI7OPJ2CmH;CAj0eFb$oLh$=UI#l($x_~I-'
    'IC8|g1v??ut9z%(2A~|{U{jdp3`2BUkzG4J~(A;8r#`$WTJs^`6wC{yh{p)jY#6vLOpvc>_u^k{dziB*pu1o=X-'
    'sPAN~AG3I_KsVv@B&lFw8-_E`sGO|i#P*3htl-'
    '7FhhHBDWJW)5m$xo4Kf*B`g4_s#7C{V8nr)fW}N@nFNGLOj|q$nfs$o68c1G1>5<A#OP~>S4PW*fnTT4hcQG?x^G0jP?(=-'
    '*UhIifNi(R@BQBNjr&$6vAO$5SMwWc;=1%tzAj9!_H*q<T`nAC>pI~ZP>~)e%#E{?>>Gm=;c4q{N+cr;1^Z+=F|);FT|n8mC2PNo'
    'eiNUvv<K@TVrRi!|t_b3wuO$IUsSlE;e)fb1>i+mHSS%V9XHQ?DjEc9p#*YZ&_@>E983N+$A5%xtD$U9(CkKhSH+vA2}W3r!wFdg'
    '})4oWeqRExgWva$T5MdoJca0S<*dsbdK-obp<plHZ{jsx8Cs*>q#y6q4B}@e*SP21Pfkl$(kKR?Re#|FXy1`jo|20n*w?>;C51Bk'
    '^Hv2mcybe*B?1c?g!gJ+-JTYuo?@_|M54I(;h#}?Gq-G+_A{Iiq>JP6Np7@um`bhog1Jm&e;Z;BbcG#=cu;BTl-'
    'TLoR=S?t<G<Z_C;6$v8mD%_{qp(%{iJxb998aC14@~$)F`+A?D0kS7mWxV8>pbBjiWUUHa46?91R`CFs$pz5%kZTkENhmYgF3Du-'
    'Jd^g@%<x`5z8$uBXssfX4mL(6<tn|%=?jBcBy3z_|=J+X_{z(#DRQobt`Myn;8<=de+Q*uOCmNhc?T}$PujP@ZVvwX=#!8DZ;Y`w'
    'Z$XFCi8eKx0xedd_SC3vAyiiF>kt9gQ=-JrxwI#2N@OUe9k4fgm=!Ax`Us<^`-'
    'r&hNDy}CC{$H9HdK?G;ULBKogtnCY5_L@s|h>2RC)nH$6Re&J27S@xE-p1irtnO@2P!Xm!=l+0R#F514RwL!&h-'
    'h6ca*wF?qy~HZt{@9yc*_RXP}Z^p0t<=YSV5_%PtH-(+RIooOP6in9;>J0Y-frk=1*#{$1e-'
    '2_BID>vOr+1vp?=U&2RY}?I_bz>xPM-'
    'P$x$;o;;@O8n<5fI?|IG?D5+I&pT(sXO|v4sGW0ir0mYUr94{4;%jY4E;FaqnFP&QCN{=8ePpXoYOu$z3rZ`A19t}&j-'
    '{6Mz<ld0HhNPC^OB0->)X)caoD`8uf;)01zh*Yvj%<pg2P-'
    'URTWN#EVnzS)BEJ8X*q>Cs3jw$f%C^GjnWdpkU5esou!h`vj+YC1<Ca}?`=AhZDR_WBa&P4#`2;uZnKA$YRCf7NM3|(d}dk7W24='
    'kbxS^8ON40ddmM24Jk={Z-%qF|>`vZ-_FUUo_^z#Uu%0-'
    'P)C*{C=mLiNda@Pv>BRS2KJFKGQ32_)z5oC2uC7PV+qmBQS1fYfrko*%AGb*wU(_fJHN6&w!=bu}vg=54PzUIL@0rJIpg=0u+UH%'
    'Rj||JgO6!mJn4CF>9G;W36UD4|Pmz_Cqe~76tJ^sVJyW_v9!VY`W|ksDR%SKmrS^GUR9*(clMX7jA<wm-v`NhtM?3-'
    'v)gqjs4TD_Ypl)RBse0L((_Gqk1_yzNy73F<Uu?*Ha{!<3p3<d9hJ8~gZ$^Q`hQ`l@!fcs1rb`=j(@dHoRX9>VcFiCw5MQJ>e$Vl'
    'D0q~r2N|B0vyEX7>86=IdRrBF$kM=Ox1mrG*y<rh<BVcLN7~6gKn5F!j&M7yC?<Q7KXdIKqKvSg#+EMo?xvV7{Yb{pUOo<0Yrs9m'
    ';E|ft^g*I!?+a=q@i{MRsq?R#7@*$P*_)S_j4Xuu5QA&lJU-'
    '7VaQY5uAl*aUUuZn6JZ$QfI*WSc8F_E$nu9lQp5_oXZIa^^0>vtMGqXXA9WVA9^mojK_u138l@|i1d{sIs@RR_7!5QzIywlB>b1E'
    '_767Ct{mW^kb~Tk2Se*t+3m4(<aT=aD5<>$+$iJQ_$kTLRZAF&o%@L3e1%kr=tMhXdwL5V9(i9ZYferY+(HD>%*?jp~de^?unB_y'
    'pg{>c^ro6blKGwxyO^w<__#Bd@io4HUVt%PbTN5InkBL}zPwkF31aF1mOBCwR{<d?;lMf~*Qf7D@xm&m+FKbBJ8;wy4@nk<Pv&c{'
    'fhk<BjT|ZKE+?8@y9BZ=hjB%F@o^;h0JpBdT2%M`ztBr&{9~Z;s(!iJSad>XHtUvqtSqSFU+<w&vML6wk&XG#Vs`LT;>;(oUtR#W'
    '2nhpo{(>ZE<Q93(-'
    '~r!)eM3Tm0HJk4`&>LfZ~b%B6{R7YZ|=n)Wc7GofKv*y%0S$sl?q0)bmQCc(<GyyeQ<md@6^oTjl)ca1nMls{r@(Cyyif^}*FxSr'
    'yLevPy)2J!3YE~tAlw$62J@J`h{aF0elQm(QsZR;`{x&$}uTXcj8R#KDI*(x|pGA-dJPaEn@VmzW<wB{Y}pHEgiDE_v6N2u2-'
    'Tsn1tmiI!p7`+w?FVU63p_7Q^$i3nSVq0-h#+vqJE8a)a>_4s7rgEeRc2Jcq3J7bL;qGykyr|hA(y^>J?-G$Bsp6}-'
    'QjMYEIxo6qKN3FwY3gEtom6c*N4%7D@ZP<rW$wGre&jh|?E%%62Gx!4PFQn^*;7$|A#>l)1l_4x*D1%s;>mMPkMQM~1gNAoG{ONV'
    'm<bvMs4#l$n1NTg$6HInY*VjV>pq$w{)t9u5&bhfd#>5YXqViE&bY<y)8aV^mK*S0y`a#wIv_22UC~JrFTQTM`)J_zC#H+^UPqG%'
    'Alx;1%bfe_y{#OVY8<!RYwl<dtu}Dy3B^%>cU`lMd{tHZ@qF%2n|A_aOE~cHRZ1T-'
    'CQhI?xEz5%>M{)^&uYS+rC4&E!!I%^`0)$ni+n!xPSw2_1F(VyVYQb!Sj(d6qiWfqb;Z-*9viw3v|GovUffo^IdP{-'
    'e(Ab*TG*n@RT+gx0Y020*4ipFS<#))CDbC8nuntl>WuWvIkaRmHRD~{#p~W_WeY_HofR|uJl7tz^weZwvto6HHISgzImI0NjzeY;'
    'nxr;!FPRBKw_keao|d)(I=4#NjMW#GnGyTg_CVz$+e1cbErUi=`0kt5J!?rt3f89YH7<Lc_p!v`PtzFAn%(BG#Le=ojKx)iYAI_J'
    'EW$3e#JE{J3ggv5{erAG?}a5P*So{`$smYt<c*u-'
    '1xX5veRPLvg<=i}8a6B=nNw;I7FnTqXRUS6VR$3bnTT?f#m{RH#J|uW=u`1~{!}~q0>!(yzGP<_QO|mz@H(s+8yb7{c&0c6&7@9E'
    'nh3i#d?nH-<n6ln-Nai{(_(V4IFCIkOKh8h7MGr_<v}#U6SuMqP1`|g2IrU)s<Y+|_4Y-'
    ';cfua6jFbnD?RAVA6OA_Fv>o(hQ{FYN(XG$q=oZpzbM)S-'
    '0&bI6t*T!He9wPjF{GfEj+`eX7)O9%jd|{+g&;yA*s$65Ry=oVK+@{$5~uZ&Yn`QD7rvW#Yfeg(y>Mz}_E>Lmd%GG`S!BAleGEco'
    '6|@r)FY!hZG{<%`?Y4ILBH*JFR$y&V!(I&ozRh(2s0}R^H)pL&N5=(tkyf=DE#9;Bks;TxdD~8zE)3sIyfx7ba-'
    '7*|Tni;szn0K<84Vb^RyUR&R%H?tK~}Wsn3K<A9KjM)RvuplekUH}6<ZzcHiwOMj72r@J^V^MRh(WT^(CUvHkhI0k|=WK@f~x3L{'
    'F#uW#D(h)_?U{OT*SJT}vGMwFm=;(5;!K#GiFEY-9W-^@+cNRxjw14W%qPuZG`mBZK*y*Xi{MwNW&S)z%j(-'
    'I&=3dSVQZrx_gc@pDaGVO~dhK-'
    '|V%uKSpyb6?YLt2Qh?k3D|>?!7+;uUC(c`{!|b{?^petAo|;&FHBq@2+!UM_Px3onbbgy~Uf)8aZ<9$P-'
    'rW!{WxHce@r&CkWh{(%86{czd1Z_Qfbo;saYUPEpd9h&I>-tEo<t?U`Gi8GJbgfUbqpiIhF==z81-'
    'v)6E=Znhf!m_6LPN7}KfJm+EY2oK_PbO?%2`GBgETnQ&SQJ*BU#J#jwgqx{TO$6-;J&*0TDg0Q87inSXPCNAqNy=-'
    'K7@IArT??n@*QYX}G&R#k2h2U@z0v?$ZD-'
    '|VSy}}hTLY4cyf#@iatV8``1@PAweEazoK8@LYBaWl3wKX(RZq!8p($%aW9wKo8kXjgg+aMc+rbMA%ZcKkTyE_4`{FpAaQRKSM6|'
    'O)1I5t8k>MURYK(Z*%Cqjl-IC<)Agg@%$OWEtSRFUMcz$u5p8sIq6R3BZ?19$qwpZGV484Cr(99P1_APP-'
    '3XvXB3<bNfupd$6=~BFaPt<X+$eG&qn6}rQmrJDE3rjr4N6({hg#d3*OO-'
    '&QIxrgX#49mZpZi)kok(_TxwaPRMx$e+S@8)174FA1R!_~o!7kg(w6;$U=Qk}-*D<OO>dDu_>G^fMqKGHZa3jO^vIZ^=wi#(-'
    'pqd@!Nbyrj9R-'
    'SJ51$_oV*{@RTz#~4Eu2o&aViB=8x%Z_uHx<FD!R#rqmYZoC0*W!%A4Q^v*g&Q=zXI!Q%x6IPp?ktU>C3?FmA<C(zw(OW57{`nPd'
    'rSSNF!E3)+usiCNtqmzi8vNwX}u7EUL4X3D*y|Bt1q6*8<9NSC>>q^N1tG{jp+T}qT(_n3xtw7Nxr!cOaA>xob7J7eym%2*;E7eG'
    'tmX+}8jPK(%_);ku^){-'
    'YS=HT2RT1JhN(Q)Hzv=_%IpWx#XlRGAHH0PTaST=}}PD<#4Zjw>9iYm%|Ppol_kV;1dM{(NJ+LdrRqk~txgfG%kh2T|Z?>+5EPLH'
    'RIk&O^z+L^R%P)l9Ia@uTZ&rx@s+OLJv3I60Z1RS%Vl&3hX?Blp$<(e~<@D;$iD)FwnHCiZN+0gYY9<wy;y>cy_PJ|d*JT-'
    'w7MxU>Br`C1!2*FLDN|mYavBFXyQ+FC&0q3e%Z}`CrKV1u_=hvsg&C%^CFk(lSgFp$J&6ZGnR&g%SD`{Yr&5>p=vv4Zghk&L_@{8'
    'g0d>uT69OW6T2+ho+4uNT6=}d6+oj^asz$3|=(q;_3=0zOF2{PjvwfU8BI-`S|hj59&k-'
    '2+`F*sq0>r#T)!|v;BU{ug4=DDJjq1A2d$YfS|2#ssubRwhHc9EoE;_WHV$Ukl+D;8F^yvy`TadzP09!aYXox71?{W&EqJzoo_Gv'
    '}GQXGthEBi9zm4y(<WoAI2hSRZ|6RPq`LXO=V)lDu#ja7g1Z%e8Piql1HB@0lAUuwWNXS#H)L-'
    'k^Q!UK(?i=!V?T7{$OwL8@v;Q3qp~*U&9r>wN34e}9Zo{>%Nto5RNK`LjgBYauKitQ#-'
    '3dzVP4T&a$}gIGZn(`tl@5Bk9PYAhO7W%!!wwv6-'
    '5@yY)9(`R}q(7t`Tvp@0R$oDn|OLrgUGoy?Xiuqm~H!;w{iEHdxDG`ZUbjB074Z@yK*3yk%MgNG}(;&i&gLc9`L(%j`Fwb3jFKsr'
    '^tw?9s+#~FV!>e!Pt=gC*V#(u%Jq_V7y>0tapuLJowbQ$E%ZM=Sc!~fZRs(fttr+B9Fou@Jyv_}6GX@&LU~v7zC%1>Uce=63=8Ny'
    'n1GDp+v#c!(IwyHpCR^B<=N03mZ8b$RM3*$@zH0Ghi|iQRov46&2}Du9-a5O%-jr}NTr=z(a%os(oxs_b8pP1-'
    ';zjq+ScgzSH73@eiKxzL!P{6bg4yvKzjOQJiRBgMAPTxJ3A;_YK{(1z<Y9P`!*k`Jv^`z|4v-I!w3c^A6*DZyy>DB_-'
    'o*!cZvM<Kfa%1m(yVJ)oSN537NP5e*4PyqTUHuHa&Mrq%oK4)V6+oIEK|&TV4JS1!1PLYY`v6DEU6rR(o$EB=|#eZLt!6rgq#Nr5'
    'LbM)C>EEjf?7|BrZq7s=DK;^cK5wIKF~`7bz)I93ahfsnV0l|8b9kS;8%qgO4ia;g(9`0VfT5IbsA;abjZlQWnT&?I^**eu>$Nl&'
    'im@fXo<Av@s_bw>TyU)87x(*#35i&>v1oJ-3bzwdZCK}b;jQ)Muk=fEw6Je2P;USYZ^8nv?6t%;8T0WDjKtjlA-paruWtIxbZOYO'
    '9RCxR@7AKGG_|oEYDy7kjr7QK)DtJ=LCUR8o3pLn}BS2Rzi0K)!N%lE(X-'
    'A6G;NKhyf(f(0ItCS$B+mqW|&8R7>VYg3VU6Lk}J<ZfO{M1n#6&F9lRSv7$EUBPnQiFNY^g8~_fL)f1?}p2ko#Wsn<~L|P-'
    '7A~t152LN_7_r-uZ;YzeEmq@|&32MGsHPWnd>(n4$x^+?PvE8Aoci8GcHOKq8G--'
    '|vWUm3#{d(iS)$g9)@~CTf&og3~9Us35sSa8zgBh5iL~TfD=7b+Kl}4g0E*fdzrQEnc#ix00lG@J$^@n>ulb^P-'
    '&t+kFAVPwj6y`#y>&_;bCr9#Q+d!q~@Tm(6iKLdn;`_8wUO>Klxc3)A>G>BE-o4htTWO_4EzG{StyCjE6XiSa-'
    '82sgBQ^XMs&>R3HeW?!P)77hD4iI8@uaiH)#zfB=U7F1GWQvw62MMmf(^`wlk+u7?;xZZ>REi{eQOhg7e?v%mlCMnIVL({;C$sU^'
    '4dvVC-g7Ah(vgaB)(L@7oeDXmx!~PEsA|ZbNv60(my|Zc=yBW-'
    '{1eIuW$9iPuPmgQF5HmRfEDi{Nmjx?UD!AT8`tEIwQn3>nIYoxG~r7)+Y#6yK%U0e4f|#_VIoE*B_tjZ$YE~3$))oKEC?~GW|z*{'
    '#W?c{rm6YuINW+jN|*heye|tQ0C{`iwvh#RoNN}dkAAg<u~`ilnj!2#9a=@)3$K`_9O0qpnp<K{f`#_^6@+U^Y{Mx&C@4)29!^r{'
    '0x%utq<$<dw=(rd-JFFrZ)l9W(_7fKrn{X2;tk<!H!-z8Vl%{#zZp6t1kSC4qH`{jO9d~QTQ$j=-'
    '(v3+yu<DQ{P3v>meKS6s%FQB|xw>1tH0K*5x@f1X6@9Lt7TtQlY=mPO|(xz~tM4dBdf-K;7yjFuI*-hM@~b2uFbg50a7-'
    'bks&YXk2)NjkuK!k*Zs3Lr1QcM)S#>{x*Bu!enGeK+#gdPH(eil*fhUd_1zluSg6RdhZn8E)==n;DoJsn?lzIl5PW}f)BTYz=T7t'
    'FdEOMPGj!c*jprY0LI+VigIbvcp2nto;^eP%d|@ad3coE1V*Mxv{$l9`w+E_>t1U{$B|`09Z?^9Pi*Qnukfy4C4n1RjW-'
    'L|hVjXs^Cn1+R=~g`;#zl0siO|2Cc`A|>sIrfBYPK}Ci%pAY<<{7hj&VG*wX9^K=MXgyM$$(psQpnvXZh+^zoWT!&kg#8R0n|6U4'
    'M55gS-`;f@yM;(K3iO@8%+=CA(bAO7QU#drVv!@)9r-R-xJ`r+;``u2N&{||TegT1}Ce|&s+`@`K&nBIMOcdrj`-'
    'uj*C!{fuf>D&9iYJiOIfBe&TZ~cScefyhNPydiReOPy2fAgEWAO8=$|EE8^`nS6So?qYn>*L)Uf5d;ryL-'
    'F)^Y{Aj;pv}*f7#s|{qF7qPywdqzy8%%|Mk^>1D&bO>H'
)

if __name__ == '__main__':
    main()
