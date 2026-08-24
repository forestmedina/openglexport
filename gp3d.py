'''
Created on 10/05/2013

@author: forestmedina
'''
import shutil
import bpy
import sys
import os
import struct
import math
import mathutils
from bpy_extras.io_utils import ExportHelper

from bpy.utils import (
        register_class,
        unregister_class,
        )

def register():
    register_class(Exporter)
    register_class(FileHeader)
    register_class(FileBody)
    register_class(PanelOpciones)


def unregister():
    unregister_class(Exporter)
    unregister_class(FileHeader)
    unregister_class(FileBody)
    unregister_class(PanelOpciones)

class PanelOpciones(bpy.types.Panel):
    bl_label = "exportadorOpengl"
#    bl_idname = "OBJECT_exportadorOpengl"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.active_object
        self.layout.prop(obj, "colisionador","Colisionador")


        
class Vertice():
    def __init__(self):
        self.co=[0.0]*3
        self.normal=[0.3]*3
        self.color=[1.0]*3
        self.uv0 = [0.0] * 2
        self.uv1 = [0.0] * 2
        return

class Cara():
    def __init__(self):
        self.vertices=[0]*3
        return

class Grupo():
    def __init__(self,group,weight):
        self.group=group
        self.weight=weight
        return
        
        
def group_sort_weight(value):
    return value.weight

class Mesh():
    vertexFormat =""
    vertices    =[]
    boundingBox =""
    boundingSphere=""
    parts=""
    def __init__(self):
        return


    def writeData(self,f):
        f.write(struct.pack("<I",len(self.vertices)))
        for v in self.vertices:
            f.write(struct.pack("<f",v.co[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.co[1]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.co[2]))#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.normal[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.normal[1]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.normal[2]))#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.color[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[1]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[2]))#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f", v.uv0[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f", v.uv0[1]))#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f", v.uv1[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f", v.uv1[1]))#VextexSize 3 (x,y,z)
        # print("Group Exporting")
        for v in self.vertices:
          #  print(v.co)
            if len(v.groups)>0:
                v.groups.sort(reverse=True, key=group_sort_weight)
            if (len(v.groups)>4):
                # print("more than 4 groups",len(v.groups))
                total=0
                for j in range(len(v.groups)):
                    if j >=4:
                       total+=v.groups[j].weight
                # print("total weight loss: ",total)
                # if total> 0.2:
                #     print ("huge total loss")
            for i in range(4):
                if i>=len(v.groups):                    
                    f.write(struct.pack("<f",0))
                else:
                    # print(v.groups[i].group,v.groups[i].weight)
                    f.write(struct.pack("<f",v.groups[i].group))
        for v in self.vertices:
            for i in range(4):
                if i>=len(v.groups):                    
                    f.write(struct.pack("<f",0))
                else:
                    f.write(struct.pack("<f",v.groups[i].weight))

        f.write(struct.pack("<I",len(self.caras)))
        for c in self.caras:
            f.write(struct.pack("<I",c.vertices[0]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<I",c.vertices[1]))#VextexSize 3 (x,y,z)
            f.write(struct.pack("<I",c.vertices[2]))#VextexSize 3 (x,y,z)
        print ("Importado")
        return 
        
        
class Esqueleto():
    huesos =[]
    
    def __init__(self):
        self.huesos=[]
        self.mapHuesos={}
        return
    def trimHuesos(self):
        huesosAux=[]

        for h in self.huesos:
            if h.use_deform:
                huesosAux.append(h)

        i=0
        self.huesos=huesosAux
        for h in self.huesos:
            # print("agregando:",h.name,":",i)
            self.mapHuesos[h.name]=i
            i+=1
        



    def writeData(self,f):

        nhuesos=0
        for h in self.huesos:
            if h.use_deform:
                nhuesos=nhuesos+1
        f.write(struct.pack("<I",nhuesos))
        for h in self.huesos:
            if h.use_deform:
                f.write(bytearray(h.name+"\00","ascii"))
                if h.parent is None:
                    f.write(struct.pack("<I",0))
                else:
                    f.write(struct.pack("<I",1))
                    f.write(bytearray(h.parent.name+"\00","ascii"))
                f.write(struct.pack("<f",h.head_local.x))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.head_local.y))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.head_local.z))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.x))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.y))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.z))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][0]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][0]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][0]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][0]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][1]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][1]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][1]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][1]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][2]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][2]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][2]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][2]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][3]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][3]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][3]))#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][3]))#VextexSize 3 (x,y,z)
                if(h.name=="espada" or h.name=="arma"):
                    f.write(struct.pack("<i",4))#VextexSize 3 (x,y,z)
                elif h.name=="cuerpo":
                    f.write(struct.pack("<i",1))#VextexSize 3 (x,y,z)
                elif h.name=="brazo.L":
                    f.write(struct.pack("<i",3))#VextexSize 3 (x,y,z)
                elif h.name=="brazo.R":
                    f.write(struct.pack("<i",3))#VextexSize 3 (x,y,z)
                elif h.name=="pierna.L":
                    f.write(struct.pack("<i",3))#VextexSize 3 (x,y,z)
                elif h.name=="pierna.R":
                    f.write(struct.pack("<i",3))#VextexSize 3 (x,y,z)
                else:
                    f.write(struct.pack("<i",3))#VextexSize 3 (x,y,z)


class Exporter(bpy.types.Operator):
    bl_idname       = "export_opengl.gpb"
    bl_label        = "Exportador OPENGL personalizado"
    bl_options      = {'PRESET'}
    directory  : bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for exporting the file",
        maxlen=1024
    )
    objetos=[]
    def printvert(self,v):
        sys.stdout.write("vert ")
        sys.stdout.write("co(")
        sys.stdout.write(str(v.co[0]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.co[1]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.co[2]))
        sys.stdout.write(")")
        sys.stdout.write("uv(")
        sys.stdout.write(str(v.uv0[0]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.uv0[1]))
        sys.stdout.write("uv1(")
        sys.stdout.write(str(v.uv1[0]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.uv1[1]))
        sys.stdout.write(")\n")

    def getvertid(self,varray,v):
        for i in range(0,len(varray)):
            v2=varray[i]
            if(v.co[0]==v2.co[0] and v.co[1]==v2.co[1] and v.co[2]==v2.co[2] and v.uv0[0]==v2.uv0[0] and v.uv0[1]==v2.uv0[1] and v.uv1[0]==v2.uv1[0] and v.uv1[1]==v2.uv1[1]):
                return i
        return -1
              
    def procesarMesh(self, p_bobject,depsgraph):
        for mod in p_bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=False
        dg = bpy.context.evaluated_depsgraph_get()
        bobject = p_bobject.evaluated_get(dg)
        mesh = bobject.to_mesh(preserve_all_data_layers =True,depsgraph=depsgraph)
        for mod in bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=True 
        meshes_to_clear.append(bobject)
        mesh.calc_tangents()
        omesh=Mesh()
        omesh.vertices=[]
        omesh.caras=[]
        if not bobject.parent is None and bobject.parent.type=='ARMATURE':
            esq=self.procesarArmadura(bobject.parent)
        for p in mesh.polygons:
            cara= Cara()
            for vi in range(0,3):
                vert=Vertice()
                meshvid=p.vertices[vi]
                bvert=mesh.vertices[meshvid]
                vert.co=bvert.co
                if not bobject.parent is None and bobject.parent.type=='ARMATURE':
                    vert.groups=[]
                    for g in bvert.groups:
                        if not bobject.vertex_groups[g.group].name in bobject.parent.data.bones:
                            continue
                        huesoAux=bobject.parent.data.bones[bobject.vertex_groups[g.group].name]
                        if huesoAux.use_deform :
                            indiceHueso=esq.mapHuesos[huesoAux.name]
                            ngrupo=Grupo(indiceHueso,g.weight)

                            if g.group!=indiceHueso:
                                pass
                                #print ("Diferentes:"+huesoAux.name+"!="+esq.huesos[indiceHueso].name)
                                #print("grupo (i,w):(",huesoAux.name,"(",ngrupo.group,")",ngrupo.weight,")")
                            vert.groups.append(ngrupo)
                else:
                    vert.groups=[]
                vert.normal=bvert.normal
                for li in p.loop_indices:
                    if meshvid==mesh.loops[li].vertex_index:
                        #little hack we will be using the color buffer for the tangent data 
                        #i need to rename it to tangent in the future 
                        vert.color=mesh.loops[li].tangent
                        #if len(mesh.vertex_colors)>0:
                        #    vert.color=mesh.vertex_colors[0].data[li].color
                        if len(mesh.uv_layers)>0:
                            vert.uv0= mesh.uv_layers[0].data[li].uv
                        if len(mesh.uv_layers) > 1:
                            vert.uv1 = mesh.uv_layers[1].data[li].uv
                #vertid= self.getvertid(omesh.vertices,vert)
                vertid=-1
                if vertid==-1:
                    cara.vertices[vi]=len(omesh.vertices)
                    omesh.vertices.append(vert)
        #            self.printvert(vert)
                else:
                    cara.vertices[vi]=vertid

            omesh.caras.append(cara)
        # print(len(omesh.vertices))
        return omesh
        
    def procesarObjetoMapa(self, bobject,f):
        ob= bobject
        f.write(ob.name)
        f.write(" ")
        for y in range(0,4):
            for x in range(0,4):
                f.write(str(ob.matrix_local[x][y])+" ")
        f.write('\n')

    def procesarArmadura(self, bobject):
        arm = bobject.data
        esq=Esqueleto()
        esq.huesos=arm.bones
        esq.trimHuesos()
        return esq

    def escribirAnimacion(self, bobject, esq, a, f):
        # Writes a single action as a standalone .anim record:
        #   name\0, frameCount, per-frame (time + per-deform-bone loc+quat),
        #   eventCount, per-event (name\0 + time).
        # Byte layout matches the per-animation block the engine's load_animation()
        # reads; the frame stride is the skeleton's deform-bone order.
        inicio, fin = [int(x) for x in a.frame_range]
        fps = bpy.context.scene.render.fps
        total = fin - inicio
        f.write(bytearray(a.name + "\00", "ascii"))
        f.write(struct.pack("<I", total))  # Cantidad de frames
        for frame in range(inicio, fin):
            f.write(struct.pack("<f", float(frame) / float(fps)))
            bpy.context.scene.frame_set(frame)
            for huesoId in esq.huesos:
                if huesoId.use_deform:
                    h = bobject.pose.bones[huesoId.name]
                    matfix = mathutils.Matrix.Rotation(math.radians(-90), 4, "X")
                    matorig = h.bone.matrix_local @ matfix
                    matpose = h.matrix @ matfix
                    mat = matpose @ matorig.inverted()
                    q = mat.to_quaternion()
                    loc = h.matrix.translation - h.bone.matrix_local.translation
                    f.write(struct.pack("<f", loc.x))
                    f.write(struct.pack("<f", loc.y))
                    f.write(struct.pack("<f", loc.z))
                    f.write(struct.pack("<f", q.x))
                    f.write(struct.pack("<f", q.y))
                    f.write(struct.pack("<f", q.z))
                    f.write(struct.pack("<f", q.w))
        f.write(struct.pack("<I", len(a.pose_markers)))
        for marker in a.pose_markers:
            f.write(bytearray(marker.name + "\00", "ascii"))
            f.write(struct.pack("<f", float(marker.frame) / float(fps)))

    def exportarAnimaciones(self, bobject, dirname):
        # One .anim file per action under <dirname>/animations/. Works whether the
        # .blend holds every action (body.blend) or a single action (per-animation
        # editing file). The filename sanitizes '.', but the real action name is
        # stored inside the file so the engine keys animations by their true name.
        anim_dir = dirname + '/animations'
        os.makedirs(anim_dir, exist_ok=True)
        esq = self.procesarArmadura(bobject)
        original_action = bobject.animation_data.action
        for a in bpy.data.actions:
            bobject.animation_data.action = a
            safe_name = a.name.replace(".", "_")
            anim_file = anim_dir + '/' + safe_name + '.anim'
            anim_file_temp = anim_file + '.tmp'
            file = open(anim_file_temp, 'bw')
            try:
                print("procesando animacion: " + a.name)
                self.escribirAnimacion(bobject, esq, a, file)
            finally:
                file.close()
            try:
                if os.path.exists(anim_file):
                    os.remove(anim_file)
                os.rename(anim_file_temp, anim_file)
            except Exception as ex:
                print(ex)
        bobject.animation_data.action = original_action

    def invoke(self, context, _event):
        import os
        if not self.directory:
            blend_filepath = context.blend_data.filepath
            print("blend_filepath 1: ", blend_filepath)
            if not blend_filepath:
                blend_filepath = "untitled"
            else:
                blend_filepath = os.path.dirname(blend_filepath)
            print("blend_filepath 2: ", blend_filepath)
            self.directory = blend_filepath
        self.execute(context)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        print ( "Executing ")
        global meshes_to_clear
        meshes_to_clear=[]
#        bpy.ops.object.mode_set(mode='OBJECT')
        result = {'FINISHED'}
        depsgraph = context.evaluated_depsgraph_get()
        dirname =self.directory
        print(self.directory)
        if self.directory.endswith(".mesh"):
            dirname=os.path.splitext(os.path.basename(self.directory))[0]

        # Remove stale .mesh files before a full-model export. Skip this for
        # per-animation editing files: those library-link their rig (so
        # bpy.data.libraries is non-empty) and cannot fully regenerate the mesh,
        # so wiping here would destroy the model's real geometry.
        if os.path.isdir(dirname) and not bpy.data.libraries:
            for f in os.listdir(dirname):
                if f.endswith('.mesh'):
                    os.remove(os.path.join(dirname, f))

        for ob in bpy.data.objects:
            if ob.type == 'MESH' and ob.visible_get():
                mesh_file_name=dirname + '/' + ob.name + '.mesh'
                mesh_temp_file_name=dirname + '/' + ob.name + '.mesh.tmp'
                # A single problematic mesh (missing UV map, non-tri/quad bone-widget
                # shape, etc.) must not abort the whole export — otherwise the armature
                # animations that come after it are never written. Skip it with a
                # warning instead. Real geometry meshes are unaffected.
                try:
                    file = open(mesh_temp_file_name, 'bw')
                    try:
                        print("procesando mesh")
                        self.procesarMesh(ob,depsgraph).writeData(file)
                    finally:
                        file.close()
                    if os.path.exists(mesh_file_name):
                        os.remove(mesh_file_name)
                    os.rename(mesh_temp_file_name,mesh_file_name)
                except Exception as ex:
                    print("WARNING: skipping mesh", ob.name, ":", ex)
                    try:
                        os.remove(mesh_temp_file_name)
                    except Exception:
                        pass
            # Only the animated deform rig carries animation_data; helper armatures
            # (e.g. Auto-Rig-Pro's "rig_add") have none and must be skipped, else
            # they would overwrite the real skeleton .esq with an empty one.
            if ob.type == 'ARMATURE' and ob.animation_data is not None:
                esq_file_name=dirname+ '/' + os.path.basename(dirname) +".mesh.esq"
                esq_file_name_temp=dirname+ '/' + os.path.basename(dirname) +".mesh.esq.tmp"
                # Skeleton-only .esq: bone block followed by an animation count of 0.
                # Animations are now written as individual .anim files (see below);
                # the trailing 0 keeps the engine loader's animation-count read valid.
                file = open(esq_file_name_temp, 'bw')
                try:
                    print("procesando armadura")
                    self.procesarArmadura(ob).writeData(file)
                    file.write(struct.pack("<I", 0))
                finally:
                    file.close()
                try:
                    if os.path.exists(esq_file_name):
                        os.remove(esq_file_name)
                    os.rename(esq_file_name_temp, esq_file_name)
                except Exception as ex:
                    print(ex)
                # Per-animation .anim files (only when the .blend carries actions).
                if len(bpy.data.actions) > 0:
                    print("procesando animaciones")
                    self.exportarAnimaciones(ob, dirname)
        for m in meshes_to_clear:
            m.to_mesh_clear()
        return result

