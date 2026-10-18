"""Original fixed slightly-open tailoring shears. Static visual geometry only."""
import math,json,hashlib,sys,time
from pathlib import Path
START=time.time();OUT=Path(__file__).resolve().parent
ASSET='tailoring-open-blade-shears-01';VERSION='1.0.0';TITLE='Slightly Open Tailoring Shears'
DESCRIPTION=('One original static low-poly tailoring shears prop in a fixed slightly open flat pose. Two continuous thick blade-to-handle halves have separate genuine through handle openings, one long oval and one smaller oval, and actual coaxial pivot bores. Each blade has an integral geometric bevel with a finite blunt edge and tip. The halves occupy separate thickness layers with positive surface clearance. One continuous fixed pin with integral lower and upper retaining heads and one genuinely bored center spacer make four finite opposed pivot contact faces without penetrating the blade bodies. Thickened handle rims and the pin base have real finite ground patches. '
 'Four named editable closed meshes and three opaque constant PBR materials. Metres, native Z up, blades/front -Y, pivot X=Y=0 and ground Z=0. No cloth, workbench, tools, labels, texture or animation. '
 'Static visual geometry only: no cutting performance, sharpness, opening or closing motion, assembly path, moving bearing, ergonomic or finger fit, stability, load capacity, manufacturing tolerance, quality, textile-process or safety certification. No fit or compatibility with earlier sewing, ironing or tool-rack assets.')
G={};LINKS=[];CONTACTS=[];FEET=[];BORES=[];GAPS=[];VOID_VOLUMES={}
PALETTE=[('Blades_SatinSteel',(.57,.65,.68,1),.32,.78),('Handles_DeepPetrol',(.025,.105,.125,1),.42,.20),('Pivot_WarmBrass',(.67,.42,.16,1),.38,.73)]
MATERIAL_CONTRACT={'alphaMode':'OPAQUE','alpha':1.0,'transmission':0.0,'texture_count':0,'single_prop_count':1,'static_pose_only':True,'no_cutting_motion_fit_or_safety_claim':True}
FOCUS=(0,-.026,.006);ORTHO=.335
CAMERAS={'gray-front3q':(.29,-.40,.61),'gray-back3q':(-.29,.40,.61),'thumbnail':(.29,-.40,.61),'qa-front':(0,-.90,.55),'qa-side':(.90,-.026,.48),'qa-top':(0,-.026,.95),'qa-back':(0,.90,.55),'qa-wireframe':(.29,-.40,.61),'silhouette-128-front':(0,-.90,.55),'silhouette-128-side':(.90,-.026,.48)}
CAMERA_SCALES={};WIRE_THICKNESS=ORTHO/640

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return mul(a,1/math.sqrt(dot(a,a)))
def mesh(name,vs,fs,material,role,fm=None):
 assert name not in G
 G[name]={'vertices':[tuple(0.0 if abs(c)<1e-10 else round(float(c),7) for c in v) for v in vs],'faces':[tuple(f) for f in fs],'material':material,'role':role}
 if fm is not None:G[name]['face_materials']=fm
 return name
BOX_FACES=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
def cuboid(lo,hi):return [tuple(hi[i] if bits[i] else lo[i] for i in range(3)) for bits in [(a,b,c)for c in[0,1]for b in[0,1]for a in[0,1]]]
def voidbox(name,lo,hi,role):VOID_VOLUMES[name]={'vertices':cuboid(lo,hi),'faces':BOX_FACES,'role':role}
def ring_geometry(cx,cy,rx,ry,ix,iy,z0,z1,n=24):
 v=[(cx+a*math.cos(math.tau*j/n),cy+b*math.sin(math.tau*j/n),z) for a,b,z in[(rx,ry,z0),(rx,ry,z1),(ix,iy,z0),(ix,iy,z1)]for j in range(n)];f=[]
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return v,f

def ellipse_volume(name,cx,cy,rx,ry,z0,z1,role,n=24):
 v=[(cx+rx*math.cos(math.tau*j/n),cy+ry*math.sin(math.tau*j/n),z)for z in[z0,z1]for j in range(n)]
 f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n)for j in range(n)]
 VOID_VOLUMES[name]={'vertices':v,'faces':f,'role':role}
# Fixed original constrained planar tessellations, generated once from authored
# contour + two holes + two blade-ridge points. No scipy, external source or
# external tessellation library is needed to reproduce this delivered source.
PROFILES={'large': {'points': [[-0.019, -0.165], [-0.023, -0.143], [-0.026, -0.043], [-0.014, -0.008], [-0.014, 0.0], [-0.01, 0.011], [0.005, 0.046], [0.0092486, 0.0583631], [0.0073646, 0.067575], [0.0070913, 0.0772248], [0.0084474, 0.0866547], [0.0113404, 0.0952223], [0.0155731, 0.1023436], [0.0208572, 0.1075334], [0.0268324, 0.1104379], [0.0330917, 0.1108592], [0.0392085, 0.1087686], [0.0447658, 0.1043086], [0.0493851, 0.0977831], [0.0527514, 0.0896369], [0.0546354, 0.080425], [0.0549087, 0.0707752], [0.0535526, 0.0613453], [0.0506596, 0.0527777], [0.0464269, 0.0456564], [0.0411428, 0.0404666], [0.015, 0.015], [0.013, 0.005], [0.014, -0.005], [-0.005, -0.03], [-0.014, -0.15], [-0.017, -0.165], [0.047, 0.074], [0.0464548, 0.0812469], [0.0448564, 0.088], [0.0423137, 0.093799], [0.039, 0.0982487], [0.0351411, 0.1010459], [0.031, 0.102], [0.0268589, 0.1010459], [0.023, 0.0982487], [0.0196863, 0.093799], [0.0171436, 0.088], [0.0155452, 0.0812469], [0.015, 0.074], [0.0155452, 0.0667531], [0.0171436, 0.06], [0.0196863, 0.054201], [0.023, 0.0497513], [0.0268589, 0.0469541], [0.031, 0.046], [0.0351411, 0.0469541], [0.039, 0.0497513], [0.0423137, 0.054201], [0.0448564, 0.06], [0.0464548, 0.0667531], [0.0036, 0.0], [0.0034773, 0.0009317], [0.0031177, 0.0018], [0.0025456, 0.0025456], [0.0018, 0.0031177], [0.0009317, 0.0034773], [0.0, 0.0036], [-0.0009317, 0.0034773], [-0.0018, 0.0031177], [-0.0025456, 0.0025456], [-0.0031177, 0.0018], [-0.0034773, 0.0009317], [-0.0036, 0.0], [-0.0034773, -0.0009317], [-0.0031177, -0.0018], [-0.0025456, -0.0025456], [-0.0018, -0.0031177], [-0.0009317, -0.0034773], [-0.0, -0.0036], [0.0009317, -0.0034773], [0.0018, -0.0031177], [0.0025456, -0.0025456], [0.0031177, -0.0018], [0.0034773, -0.0009317], [-0.009, -0.036], [-0.018, -0.14], [0.009, 0.0], [0.0086933, 0.0023294], [0.0077942, 0.0045], [0.006364, 0.006364], [0.0045, 0.0077942], [0.0023294, 0.0086933], [0.0, 0.009], [-0.0023294, 0.0086933], [-0.0045, 0.0077942], [-0.006364, 0.006364], [-0.0077942, 0.0045], [-0.0086933, 0.0023294], [-0.009, 0.0], [-0.0086933, -0.0023294], [-0.0077942, -0.0045], [-0.006364, -0.006364], [-0.0045, -0.0077942], [-0.0023294, -0.0086933], [-0.0, -0.009], [0.0023294, -0.0086933], [0.0045, -0.0077942], [0.006364, -0.006364], [0.0077942, -0.0045], [0.0086933, -0.0023294], [0.0224225, 0.035], [0.0085484, 0.035], [0.0253226, 0.035], [0.035531, 0.035], [0.0035135, 0.035], [0.0002857, 0.035], [0.044336, 0.05], [0.0490086, 0.05], [0.0391852, 0.05], [0.0228148, 0.05], [0.0121632, 0.05], [0.0063746, 0.05]], 'loops': [[0, 1, 2, 3, 4, 5, 111, 6, 117, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 113, 24, 25, 109, 26, 27, 28, 29, 30, 31], [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 115, 48, 49, 50, 51, 52, 114, 53, 54, 55], [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]], 'triangles': [[1, 81, 2], [81, 80, 2], [80, 3, 2], [29, 80, 81], [80, 29, 3], [55, 22, 21], [1, 30, 81], [30, 29, 81], [30, 1, 0], [31, 30, 0], [32, 55, 21], [20, 32, 21], [29, 98, 3], [52, 25, 24], [26, 106, 107], [106, 49, 6], [106, 6, 107], [10, 9, 43], [10, 42, 11], [42, 10, 43], [17, 36, 18], [100, 99, 29], [99, 98, 29], [98, 97, 3], [112, 24, 113], [23, 53, 112], [23, 112, 113], [114, 52, 24], [114, 24, 112], [53, 114, 112], [48, 115, 116], [48, 116, 6], [115, 47, 116], [49, 48, 6], [108, 26, 109], [50, 108, 109], [50, 109, 25], [106, 26, 108], [50, 49, 106], [50, 106, 108], [9, 44, 43], [44, 8, 45], [8, 44, 9], [37, 17, 16], [37, 36, 17], [15, 37, 16], [34, 19, 18], [102, 29, 28], [88, 26, 107], [88, 107, 110], [107, 6, 110], [88, 87, 26], [5, 88, 110], [5, 110, 111], [110, 6, 111], [88, 5, 89], [87, 86, 26], [86, 85, 26], [54, 22, 55], [54, 23, 22], [54, 53, 23], [52, 51, 25], [51, 50, 25], [117, 6, 116], [47, 7, 117], [47, 117, 116], [8, 7, 45], [38, 15, 14], [38, 37, 15], [36, 35, 18], [35, 34, 18], [33, 20, 19], [34, 33, 19], [33, 32, 20], [97, 96, 3], [104, 103, 28], [103, 102, 28], [101, 100, 29], [102, 101, 29], [105, 104, 28], [82, 105, 28], [85, 27, 26], [27, 82, 28], [82, 27, 83], [27, 84, 83], [84, 27, 85], [46, 7, 47], [7, 46, 45], [13, 39, 14], [39, 38, 14], [94, 93, 4], [5, 90, 89], [91, 90, 5], [40, 13, 12], [40, 39, 13], [95, 94, 4], [95, 4, 3], [96, 95, 3], [92, 91, 5], [4, 92, 5], [93, 92, 4], [11, 41, 12], [41, 40, 12], [42, 41, 11], [77, 103, 104], [103, 77, 102], [105, 78, 104], [78, 77, 104], [76, 101, 102], [77, 76, 102], [56, 105, 82], [56, 82, 83], [101, 74, 100], [74, 99, 100], [79, 78, 105], [56, 79, 105], [84, 58, 83], [76, 75, 101], [75, 74, 101], [99, 72, 98], [57, 56, 83], [58, 57, 83], [59, 84, 85], [59, 58, 84], [86, 59, 85], [74, 73, 99], [73, 72, 99], [71, 97, 98], [72, 71, 98], [71, 96, 97], [60, 86, 87], [60, 59, 86], [70, 95, 96], [71, 70, 96], [88, 62, 87], [62, 88, 89], [95, 68, 94], [94, 68, 93], [68, 67, 93], [61, 60, 87], [62, 61, 87], [90, 64, 89], [70, 69, 95], [69, 68, 95], [63, 62, 89], [64, 63, 89], [65, 90, 91], [65, 64, 90], [92, 65, 91], [66, 65, 92], [66, 92, 93], [67, 66, 93]], 'bevel_edge_indices': [0, 31, 30, 29], 'ridge_indices': [80, 81]}, 'small': {'points': [[-0.019, -0.165], [-0.023, -0.143], [-0.026, -0.043], [-0.014, -0.008], [-0.014, 0.0], [-0.01, 0.011], [0.005, 0.038], [0.0119675, 0.0541667], [0.010319, 0.0611379], [0.0100799, 0.0684404], [0.0112665, 0.0755766], [0.0137978, 0.0820601], [0.0175015, 0.0874492], [0.022125, 0.0913766], [0.0273534, 0.0935746], [0.0328303, 0.0938935], [0.0381824, 0.0923114], [0.0430451, 0.0889363], [0.0470869, 0.0839981], [0.0500325, 0.0778333], [0.051681, 0.0708621], [0.0519201, 0.0635596], [0.0507335, 0.0564234], [0.0482022, 0.0499399], [0.0444985, 0.0445508], [0.039875, 0.0406234], [0.015, 0.015], [0.013, 0.005], [0.014, -0.005], [-0.005, -0.03], [-0.014, -0.15], [-0.017, -0.165], [0.044, 0.066], [0.043557, 0.0709176], [0.0422583, 0.0755], [0.0401924, 0.079435], [0.0375, 0.0824545], [0.0343646, 0.0843526], [0.031, 0.085], [0.0276354, 0.0843526], [0.0245, 0.0824545], [0.0218076, 0.079435], [0.0197417, 0.0755], [0.018443, 0.0709176], [0.018, 0.066], [0.018443, 0.0610824], [0.0197417, 0.0565], [0.0218076, 0.052565], [0.0245, 0.0495455], [0.0276354, 0.0476474], [0.031, 0.047], [0.0343646, 0.0476474], [0.0375, 0.0495455], [0.0401924, 0.052565], [0.0422583, 0.0565], [0.043557, 0.0610824], [0.0036, 0.0], [0.0034773, 0.0009317], [0.0031177, 0.0018], [0.0025456, 0.0025456], [0.0018, 0.0031177], [0.0009317, 0.0034773], [0.0, 0.0036], [-0.0009317, 0.0034773], [-0.0018, 0.0031177], [-0.0025456, 0.0025456], [-0.0031177, 0.0018], [-0.0034773, 0.0009317], [-0.0036, 0.0], [-0.0034773, -0.0009317], [-0.0031177, -0.0018], [-0.0025456, -0.0025456], [-0.0018, -0.0031177], [-0.0009317, -0.0034773], [-0.0, -0.0036], [0.0009317, -0.0034773], [0.0018, -0.0031177], [0.0025456, -0.0025456], [0.0031177, -0.0018], [0.0034773, -0.0009317], [-0.009, -0.036], [-0.018, -0.14], [0.009, 0.0], [0.0086933, 0.0023294], [0.0077942, 0.0045], [0.006364, 0.006364], [0.0045, 0.0077942], [0.0023294, 0.0086933], [0.0, 0.009], [-0.0023294, 0.0086933], [-0.0045, 0.0077942], [-0.006364, 0.006364], [-0.0077942, 0.0045], [-0.0086933, 0.0023294], [-0.009, 0.0], [-0.0086933, -0.0023294], [-0.0077942, -0.0045], [-0.006364, -0.006364], [-0.0045, -0.0077942], [-0.0023294, -0.0086933], [-0.0, -0.009], [0.0023294, -0.0086933], [0.0045, -0.0077942], [0.006364, -0.006364], [0.0077942, -0.0045], [0.0086933, -0.0023294], [0.0044828, 0.035], [0.0033333, 0.035], [0.0063043, 0.035], [0.0227405, 0.035], [0.0344158, 0.035], [0.0415706, 0.05], [0.0480188, 0.05], [0.0481477, 0.05], [0.0482257, 0.05], [0.0232674, 0.05], [0.0101717, 0.05], [0.0240947, 0.05], [0.0379053, 0.05]], 'loops': [[0, 1, 2, 3, 4, 5, 107, 6, 116, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 114, 23, 24, 25, 110, 26, 27, 28, 29, 30, 31], [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 117, 48, 49, 50, 51, 52, 118, 53, 54, 55], [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]], 'triangles': [[31, 30, 0], [81, 80, 2], [81, 29, 80], [29, 81, 30], [1, 81, 2], [30, 1, 0], [81, 1, 30], [80, 3, 2], [29, 3, 80], [5, 88, 106], [5, 106, 107], [106, 6, 107], [88, 26, 108], [88, 108, 106], [108, 6, 106], [26, 88, 87], [17, 36, 18], [36, 17, 16], [99, 98, 29], [98, 3, 29], [34, 19, 18], [15, 37, 16], [37, 36, 16], [13, 12, 40], [111, 24, 23], [111, 23, 112], [53, 111, 112], [26, 109, 108], [109, 49, 6], [109, 6, 108], [109, 26, 110], [25, 49, 109], [25, 109, 110], [72, 98, 99], [94, 93, 4], [86, 26, 87], [60, 86, 87], [36, 35, 18], [35, 34, 18], [33, 20, 19], [34, 33, 19], [38, 15, 14], [38, 37, 15], [113, 23, 114], [22, 54, 113], [22, 113, 114], [112, 23, 113], [54, 53, 112], [54, 112, 113], [7, 47, 46], [100, 99, 29], [101, 100, 29], [105, 104, 28], [104, 103, 28], [57, 83, 58], [93, 68, 67], [94, 68, 93], [92, 5, 4], [93, 92, 4], [83, 84, 58], [84, 83, 27], [88, 62, 87], [43, 10, 9], [39, 13, 40], [13, 39, 14], [39, 38, 14], [55, 22, 21], [55, 54, 22], [50, 49, 25], [51, 50, 25], [49, 48, 6], [48, 115, 116], [48, 116, 6], [115, 7, 116], [48, 117, 115], [117, 47, 7], [117, 7, 115], [83, 82, 27], [82, 105, 28], [27, 82, 28], [102, 76, 101], [103, 102, 28], [102, 29, 28], [102, 101, 29], [74, 100, 101], [100, 74, 99], [104, 77, 103], [77, 102, 103], [102, 77, 76], [85, 84, 27], [85, 27, 26], [86, 85, 26], [61, 60, 87], [62, 61, 87], [89, 62, 88], [89, 88, 5], [90, 89, 5], [10, 42, 11], [43, 42, 10], [8, 44, 9], [44, 43, 9], [32, 55, 21], [20, 32, 21], [33, 32, 20], [118, 52, 24], [118, 24, 111], [53, 118, 111], [52, 25, 24], [52, 51, 25], [76, 75, 101], [75, 74, 101], [73, 72, 99], [74, 73, 99], [78, 104, 105], [78, 77, 104], [95, 68, 94], [95, 69, 68], [95, 70, 69], [3, 95, 4], [95, 94, 4], [66, 65, 92], [66, 93, 67], [66, 92, 93], [91, 65, 90], [65, 91, 92], [91, 90, 5], [92, 91, 5], [84, 59, 58], [85, 59, 84], [60, 59, 86], [59, 85, 86], [89, 63, 62], [42, 41, 11], [41, 12, 11], [12, 41, 40], [45, 44, 8], [45, 7, 46], [45, 8, 7], [82, 56, 105], [57, 56, 83], [56, 82, 83], [79, 78, 105], [56, 79, 105], [98, 97, 3], [72, 71, 98], [71, 97, 98], [65, 64, 90], [64, 89, 90], [64, 63, 89], [95, 96, 70], [96, 71, 70], [71, 96, 97], [96, 95, 3], [97, 96, 3]], 'bevel_edge_indices': [0, 31, 30, 29], 'ridge_indices': [80, 81]}}
HALVES=[];HANDLE_SPECS=[];BEVEL_SPECS=[]
def half(key,sign,z0,z1):
 p=PROFILES[key];xy=p['points'];n=len(xy);outer=p['loops'][0];inner_edge=set(p['bevel_edge_indices'])
 def height(i,top):
  x,y=xy[i];handle=max(0,min(1,(y-.035)/.015))
  if top:
   h=z1+handle*.004
   if i in inner_edge and y<-.025:h=z0+.0006
   return h
  return z0*(1-handle)
 vs=[(sign*x,y,height(i,top))for top in[False,True]for i,(x,y)in enumerate(xy)]
 fs=[];fm=[]
 for tri in p['triangles']:
  material=1 if min(xy[i][1]for i in tri)>.034999 else 0
  fs.append(tuple(reversed(tri)));fm.append(material);fs.append(tuple(i+n for i in tri));fm.append(material)
 for loop in p['loops']:
  for a,b in zip(loop,loop[1:]+loop[:1]):fs.append((a,a+n,b+n,b));fm.append(1 if min(xy[i][1]for i in[a,b])>.034999 else 0)
 if sign<0:fs=[tuple(reversed(f))for f in fs]
 name=mesh('Half_'+('LowerLargeOval' if key=='large' else 'UpperThumbOval'),vs,fs,0,'one continuous blade, neck and thickened true oval handle shell with actual separate coaxial pivot through bore; integral geometric blade bevel and finite blunt edge',fm)
 HALVES.append(name);FEET.append(name)
 cx=sign*.031;cy=.074 if key=='large'else .066;rx=.016 if key=='large'else .013;ry=.028 if key=='large'else .019
 HANDLE_SPECS.append({'mesh':name,'center_xy_m':[cx,cy],'inner_radii_m':[rx,ry],'polygon_sides':24,'z_bottom_m':0,'z_top_m':z1+.004})
 BEVEL_SPECS.append({'mesh':name,'full_blade_plane_z_m':z1,'edge_bottom_z_m':z0,'edge_top_z_m':z0+.0006,'finite_edge_thickness_m':.0006,'ridge_vertex_indices':p['ridge_indices']})
 ellipse_volume('FullHandleOpening_'+key,cx,cy,rx-.0008,ry-.0008,-.004,.024,'complete finite polygonal handle opening throughout and beyond both faces')
 for dx in[-.004,0,.004]:GAPS.append({'label':'Handle_'+key+'_'+str(dx),'origin_m':(cx+dx,cy,-.003),'direction':(0,0,1),'length_m':.026})
 BORES.extend([{'mesh':name,'origin_m':(cx,cy,-.003),'direction':(0,0,1),'length_m':.026},{'mesh':name,'origin_m':(0,0,-.003),'direction':(0,0,1),'length_m':.026}])
half('large',1,.003,.006);half('small',-1,.007,.010)
# A single closed revolved pin has integral lower and upper fixed heads.
# Its 2.8 mm shaft radius remains clear of all 3.6 mm pivot-hole walls.
PIN_PROFILE=[(0,.0075),(.0007,.008),(.003,.008),(.003,.0028),(.010,.0028),(.010,.008),(.0123,.008),(.013,.0075)]
n=24;vs=[(r*math.cos(math.tau*j/n),r*math.sin(math.tau*j/n),z)for z,r in PIN_PROFILE for j in range(n)]
fs=[tuple(reversed(range(n))),tuple((len(PIN_PROFILE)-1)*n+j for j in range(n))]+[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j)for k in range(len(PIN_PROFILE)-1)for j in range(n)]
PIN=mesh('FixedPivot_PinWithIntegralRetainingHeads',vs,fs,2,'continuous solid fixed coaxial pin and integral opposing retaining heads; no assembly-path, bearing or motion claim');FEET.append(PIN)
v,f=ring_geometry(0,0,.008,.008,.0036,.0036,.006,.007)
SPACER=mesh('Pivot_TrueBoredCenterSpacer',v,f,2,'actual thick annular spacer with continuous full pivot-hole wall, finite opposed faces and positive radial shaft clearance')
BORES.append({'mesh':SPACER,'origin_m':(0,0,-.003),'direction':(0,0,1),'length_m':.026})
for a,b,z in[(PIN,HALVES[0],.003),(HALVES[0],SPACER,.006),(SPACER,HALVES[1],.007),(HALVES[1],PIN,.010)]:
 CONTACTS.append({'a':a,'b':b,'lower_mesh':a,'upper_mesh':b,'axis':'Z','plane_m':z,'normal':(0,0,1),'minimum_patch_area_m2':.000145,'points':[(.0056*math.cos(math.tau*j/8),.0056*math.sin(math.tau*j/8),z)for j in range(8)],'interior_probe_offset_m':.00005,'expected_contact_annulus_outer_radius_m':.008,'expected_contact_annulus_inner_radius_m':.0036})
v,f=ring_geometry(0,0,.0034,.0034,.0030,.0030,.0032,.0098)
VOID_VOLUMES['CompletePivotRadialClearance']={'vertices':v,'faces':f,'role':'full closed annular clearance between shaft and both bore walls, including the spacer; independent full volume test, not only a center ray'}
voidbox('OpenAirBetweenBladeTips',(-.012,-.159,.002),(.012,-.151,.012),'finite open space between diverged fixed blade tips')
voidbox('LayerGapNearPivot',(-.004,-.012,.0062),(.004,-.009,.0068),'finite fixed interlayer gap ahead of and clear of the pivot spacer')
SHEARS_CONTRACT={'single_prop_count':1,'continuous_blade_handle_halves':HALVES,'handle_openings':HANDLE_SPECS,'geometric_blade_bevels':BEVEL_SPECS,'pivot_pin':PIN,'center_spacer':SPACER,'pivot_bore_radius_m':.0036,'pin_shaft_radius_m':.0028,'minimum_nominal_blade_layer_gap_m':.001,'finite_pivot_contact_count':4,'ground_meshes':FEET,'static_pose_only':True,'cutting_motion_ergonomic_fit_safety_or_manufacturing_claim':False}
def measure_shears_geometry(vertices):
 assert set(vertices)==set(G)
 rows=[]
 for name,g in G.items():
  assert len(vertices[name])==len(g['vertices']);d=max(math.dist(a,b)for a,b in zip(vertices[name],g['vertices']));assert d<1.5e-6,(name,d)
  rows.append({'mesh':name,'actual_vertex_count':len(vertices[name]),'maximum_original_profile_deviation_m':d})
 for name in FEET:assert abs(min(p[2]for p in vertices[name]))<1e-7,(name,'ground lifted')
 return dict(SHEARS_CONTRACT,all_actual_profile_vertices=rows)

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
root=bpy.data.objects.new('OneFixedTailoringShears',None);scene.collection.objects.link(root);root['asset_id']=ASSET;root['front_direction']='-Y';root['static_visual_only']=True;root['origin_datum']='Ground origin X=Y=Z=0, blades/front -Y';root['render_contract']=json.dumps(guard(),sort_keys=True)
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
adj={o.name:set() for o in parts}
for j in joints+CONTACTS:adj[j['a']].add(j['b']);adj[j['b']].add(j['a'])
seen=set(FEET);todo=list(seen)
while todo:
 for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
assert seen==set(byname),('Unsupported meshes',set(byname)-seen)
supports=[]
for name in FEET:
 patch=horizontal_triangles(name,0,-1);area=sum(t['area_m2'] for t in patch);assert area>.00015,(name,area);supports.append({'name':name,'area_m2':area,'triangles':patch})
def triangle_surface_distance(vertices,point):
 a,b,c=vertices;p=tuple(float(x) for x in point);n=unit(cross(sub(b,a),sub(c,a)));signed=dot(sub(p,a),n);projected=sub(p,mul(n,signed))
 sides=[dot(cross(sub(y,x),sub(projected,x)),n) for x,y in [(a,b),(b,c),(c,a)]]
 best=abs(signed) if min(sides)>=-1e-15 or max(sides)<=1e-15 else float('inf')
 for x,y in [(a,b),(b,c),(c,a)]:
  edge=sub(y,x);u=max(0.,min(1.,dot(sub(p,x),edge)/dot(edge,edge)));delta=sub(p,add(x,mul(edge,u)));best=min(best,math.sqrt(dot(delta,delta)))
 return best
def actual_loop_triangles(name):
 o=byname[name];o.data.calc_loop_triangles();v=[tuple(float(c) for c in o.matrix_world@p.co) for p in o.data.vertices]
 return [tuple(v[i] for i in t.vertices) for t in o.data.loop_triangles]
def actual_surface_distance(name,point):return min(triangle_surface_distance(t,point) for t in actual_loop_triangles(name))
face_contacts=[]
for r in CONTACTS:
 points=[]
 for p in r['points']:
  point=Vector(p);eps=r['interior_probe_offset_m'];up=Vector(r['normal']);ta=trees[r['lower_mesh']];tb=trees[r['upper_mesh']]
  da=actual_surface_distance(r['lower_mesh'],point);db=actual_surface_distance(r['upper_mesh'],point);bvh_da=ta.find_nearest(point)[3];bvh_db=tb.find_nearest(point)[3]
  valid=da<1e-6 and db<1e-6 and inside(ta,point-up*eps) and inside(tb,point+up*eps) and not inside(ta,point+up*eps) and not inside(tb,point-up*eps)
  assert valid,('True face contact failed',r['a'],r['b'],p,da,db)
  points.append({'point_m':list(p),'lower_surface_distance_m':da,'upper_surface_distance_m':db,'distance_method':'all_actual_loop_triangles_float64','bvh_lower_surface_distance_m':bvh_da,'bvh_upper_surface_distance_m':bvh_db,'opposed_interior_sides_verified':True})
 face_contacts.append(dict(r,actual_surface_point_checks=points))
bore_checks=[]
for r in BORES:
 hit=trees[r['mesh']].ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0]
 assert hit is None,('Isolated opening capped',r)
 bore_checks.append(dict(r,actual_isolated_opening_ray_clear=True))
gap_checks=[]
for r in GAPS:
 blockers=[name for name,t in trees.items() if t.ray_cast(Vector(r['origin_m']),Vector(r['direction']),r['length_m'])[0] is not None]
 assert not blockers,('Actual assembled opening blocked',r,blockers)
 gap_checks.append(dict(r,actual_full_assembly_blockers=blockers))
void_volume_checks=[];probe_inside_selftests=[]
for name,probe in VOID_VOLUMES.items():
 pv=[Vector(v) for v in probe['vertices']];pt=BVHTree.FromPolygons(pv,probe['faces'],all_triangles=False)
 actual_triangles[id(pt)]=[[tuple(float(c) for c in pv[i]) for i in (face[0],face[j],face[j+1])] for face in probe['faces'] for j in range(1,len(face)-1)]
 center=tuple(sum(float(v[k]) for v in pv)/len(pv) for k in range(3))
 if name=='CompletePivotRadialClearance':center=(.0032,0,.0065)
 outside=(max(float(v[0]) for v in pv)+.05,center[1],center[2])
 assert inside(pt,center) is True and inside(pt,outside) is False,('Actual probe inside/outside control failed',name)
 probe_inside_selftests.append({'probe':name,'actual_center_m':center,'actual_outside_point_m':outside,'center_inside':True,'outside_is_outside':True})
 per_part=[]
 for obj in parts:
  model_tree=trees[obj.name];crossing=model_tree.overlap(pt)
  model_inside=[i for i,v in enumerate(obj.data.vertices) if inside(pt,obj.matrix_world@v.co)]
  probe_inside=[i for i,v in enumerate(pv) if inside(model_tree,v)]
  assert not crossing and not model_inside and not probe_inside,('Finite cavity obstruction',name,obj.name,len(crossing),model_inside,probe_inside)
  per_part.append({'part':obj.name,'triangle_crossings':len(crossing),'model_vertices_inside_probe':len(model_inside),'probe_vertices_inside_model':len(probe_inside)})
 void_volume_checks.append({'probe':name,'role':probe['role'],'part_checks':per_part,'finite_volume_empty':True})
shears_evidence=dict(measure_shears_geometry({o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in parts}),finite_external_air_volume_checks=void_volume_checks,actual_probe_inside_outside_selftests=probe_inside_selftests,material_contract=MATERIAL_CONTRACT)
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
 'single_prop_count':1,'shears_geometry':shears_evidence,'finite_opposed_face_contacts':face_contacts,'actual_opening_rays':gap_checks,'actual_isolated_bores':bore_checks,
 'finite_ground_patches':supports,'world_oriented_triangle_full_solid_pbr_sha256':source_fp,
 'actual_glb_sha256':hashlib.sha256((OUT/'model.glb').read_bytes()).hexdigest(),'native_saved_render_config':guard(),
 'status':'producer geometry only; independent gates pending'}
def saveqa():(OUT/'qa-report.json').write_text(json.dumps(qa,indent=2)+'\n')
def metadata():
 files={}
 for role,name in [('glb','model.glb'),('blend','source.blend'),('generator','generate.py'),('render','thumbnail.png')]:
  p=OUT/name
  if not p.exists():return
  files[role]={'path':f'assets/tailoring/{ASSET}/v{VERSION}/{name}','size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 d={'id':ASSET,'version':VERSION,'category':'props','assetKind':'prop','theme':'tailoring','style':'S01-clean-geometric','title':TITLE,'description':DESCRIPTION,
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
for name,pos,power,size in [('Key',(-.4,-.6,.7),12,.5),('Fill',(.5,-.1,.4),6,.4),('Rim',(.1,.5,.6),8.5,.4)]:
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
