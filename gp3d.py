'''
Created on 10/05/2013

@author: forestmedina
'''

import bpy;
import sys;
import os;
import struct;
import math;
import mathutils;
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
        self.layout.prop(obj, "colisionador","Colisionador");


        
class Vertice():
    def __init__(self):
        self.co=[0.0]*3;
        self.normal=[0.3]*3;
        self.color=[1.0]*3;
        self.uv=[0.0]*2;
        return;

class Cara():
    def __init__(self):
        self.vertices=[0]*3;
        return;

class Grupo():
    def __init__(self,group,weight):
        self.group=group;
        self.weight=weight
        return;
        
        
def group_sort_weight(value):
    return value.weight

class Mesh():
    vertexFormat ="";
    vertices    =[];
    boundingBox ="";
    boundingSphere="";
    parts="";
    def __init__(self):
        return;


    def writeData(self,f):
        f.write(struct.pack("<I",len(self.vertices)));
        for v in self.vertices:
            f.write(struct.pack("<f",v.co[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.co[1]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.co[2]));#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.normal[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.normal[1]));#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.color[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[1]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[2]));#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.uv[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.uv[1]));#VextexSize 3 (x,y,z)
        print("Group Exporting")
        for v in self.vertices:
          #  print(v.co)
            if len(v.groups)>0:
                v.groups.sort(reverse=True, key=group_sort_weight)
            if (len(v.groups)>4):
                print("more than 4 groups",len(v.groups))
                total=0
                for j in range(len(v.groups)):
                    if j >=4:
                       total+=v.groups[j].weight
                print("total weight loss: ",total)
                if total> 0.2:
                    print ("huge total loss")
            for i in range(4):
                if i>=len(v.groups):                    
                    f.write(struct.pack("<f",0));
                else:
                    print(v.groups[i].group,v.groups[i].weight)
                    f.write(struct.pack("<f",v.groups[i].group));
        for v in self.vertices:
            for i in range(4):
                if i>=len(v.groups):                    
                    f.write(struct.pack("<f",0));
                else:
                    f.write(struct.pack("<f",v.groups[i].weight));

        f.write(struct.pack("<I",len(self.caras)));
        for c in self.caras:
            f.write(struct.pack("<I",c.vertices[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<I",c.vertices[1]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<I",c.vertices[2]));#VextexSize 3 (x,y,z)
        print ("Importado")
        return ;
        
        
class Esqueleto():
    huesos =[];
    
    def __init__(self):
        self.huesos=[];
        self.mapHuesos={};
        return;
    def trimHuesos(self):
        huesosAux=[];

        for h in self.huesos:
            if h.use_deform:
                huesosAux.append(h);

        i=0;
        self.huesos=huesosAux;
        for h in self.huesos:
            print("agregando:",h.name,":",i);
            self.mapHuesos[h.name]=i;
            i+=1;
        



    def writeData(self,f):

        nhuesos=0;
        for h in self.huesos:
            if h.use_deform:
                nhuesos=nhuesos+1
        f.write(struct.pack("<I",nhuesos));
        for h in self.huesos:
            if h.use_deform:
                f.write(bytearray(h.name+"\00","ascii"));
                if h.parent is None:
                    f.write(struct.pack("<I",0));
                else:
                    f.write(struct.pack("<I",1));
                    f.write(bytearray(h.parent.name+"\00","ascii"));
                f.write(struct.pack("<f",h.head_local.x));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.head_local.y));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.head_local.z));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.x));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.y));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.tail_local.z));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][0]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][0]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][0]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][0]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][1]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][1]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][1]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][1]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][2]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][2]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][2]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][2]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[0][3]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[1][3]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[2][3]));#VextexSize 3 (x,y,z)
                f.write(struct.pack("<f",h.matrix_local[3][3]));#VextexSize 3 (x,y,z)
                if(h.name=="espada" or h.name=="arma"):
                    f.write(struct.pack("<i",4));#VextexSize 3 (x,y,z)
                elif h.name=="cuerpo":
                    f.write(struct.pack("<i",1));#VextexSize 3 (x,y,z)
                elif h.name=="brazo.L":
                    f.write(struct.pack("<i",3));#VextexSize 3 (x,y,z)
                elif h.name=="brazo.R":
                    f.write(struct.pack("<i",3));#VextexSize 3 (x,y,z)
                elif h.name=="pierna.L":
                    f.write(struct.pack("<i",3));#VextexSize 3 (x,y,z)
                elif h.name=="pierna.R":
                    f.write(struct.pack("<i",3));#VextexSize 3 (x,y,z)
                else:
                    f.write(struct.pack("<i",3));#VextexSize 3 (x,y,z)


class Exporter(bpy.types.Operator, ExportHelper):
    bl_idname       = "export_opengl.gpb";
    bl_label        = "Exportador OPENGL personalizado";
    bl_options      = {'PRESET'};
    filename_ext    = ".mesh";
    objetos=[];
    expmapa = bpy.props.BoolProperty(
            name="Exportar como mapa",
            description="Exporta todos los objetos como un Mapa",
            default=False,
            )
    
    def printvert(self,v):
        sys.stdout.write("vert ")
        sys.stdout.write("co(")
        sys.stdout.write(str(v.co[0]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.co[1]))
        sys.stdout.write(",")


class Exporter(bpy.types.Operator, ExportHelper):
    bl_idname       = "export_opengl.gpb";
    bl_label        = "Exportador OPENGL personalizado";
    bl_options      = {'PRESET'};
    filename_ext    = ".mesh";
    objetos=[];
    expmapa = bpy.props.BoolProperty(
            name="Exportar como mapa",
            description="Exporta todos los objetos como un Mapa",
            default=False,
            )
    
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
        sys.stdout.write(str(v.uv[0]))
        sys.stdout.write(",")
        sys.stdout.write(str(v.uv[1]))
        sys.stdout.write(")\n")

    def getvertid(self,varray,v):
        for i in range(0,len(varray)):
            v2=varray[i];
            if(v.co[0]==v2.co[0] and v.co[1]==v2.co[1] and v.co[2]==v2.co[2] and v.uv[0]==v2.uv[0] and v.uv[1]==v2.uv[1]):
                return i
        return -1;
              
    def procesarMesh(self, p_bobject,depsgraph):
        for mod in p_bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=False;
        dg = bpy.context.evaluated_depsgraph_get()
        bobject = p_bobject.evaluated_get(dg)
        mesh = bobject.to_mesh(preserve_all_data_layers =True,depsgraph=depsgraph);
        for mod in bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=True; 
        meshes_to_clear.append(bobject);
        mesh.calc_tangents();
        omesh=Mesh();
        omesh.vertices=[]
        omesh.caras=[];
        if not bobject.parent is None and bobject.parent.type=='ARMATURE':
            esq=self.procesarArmadura(bobject.parent);
        for p in mesh.polygons:
            cara= Cara();
            for vi in range(0,3):
                vert=Vertice();
                meshvid=p.vertices[vi]
                bvert=mesh.vertices[meshvid]
                vert.co=bvert.co;
                if not bobject.parent is None and bobject.parent.type=='ARMATURE':
                    vert.groups=[]
                    for g in bvert.groups:
                        if not bobject.vertex_groups[g.group].name in bobject.parent.data.bones:
                            continue;
                        huesoAux=bobject.parent.data.bones[bobject.vertex_groups[g.group].name];
                        if huesoAux.use_deform :
                            indiceHueso=esq.mapHuesos[huesoAux.name];
                            ngrupo=Grupo(indiceHueso,g.weight);

                            if g.group!=indiceHueso:
                                pass
                                #print ("Diferentes:"+huesoAux.name+"!="+esq.huesos[indiceHueso].name)
                                #print("grupo (i,w):(",huesoAux.name,"(",ngrupo.group,")",ngrupo.weight,")")
                            vert.groups.append(ngrupo);
                else:
                    vert.groups=bvert.groups;
                vert.normal=bvert.normal;
                for li in p.loop_indices:
                    if meshvid==mesh.loops[li].vertex_index:
                        #little hack we will be using the color buffer for the tangent data 
                        #i need to rename it to tangent in the future 
                        vert.color=mesh.loops[li].tangent;
                        #if len(mesh.vertex_colors)>0:
                        #    vert.color=mesh.vertex_colors[0].data[li].color;
                        if len(mesh.uv_layers)>0:
                            vert.uv= mesh.uv_layers[0].data[li].uv;
                #vertid= self.getvertid(omesh.vertices,vert);
                vertid=-1
                if vertid==-1:
                    cara.vertices[vi]=len(omesh.vertices);
                    omesh.vertices.append(vert)
        #            self.printvert(vert);
                else:
                    cara.vertices[vi]=vertid;

            omesh.caras.append(cara);
        print(len(omesh.vertices))
        return omesh;
        
    def procesarObjetoMapa(self, bobject,f):
        ob= bobject;
        f.write(ob.name);
        f.write(" ");
        for y in range(0,4):
            for x in range(0,4):
                f.write(str(ob.matrix_local[x][y])+" ");
        f.write('\n');

    def procesarArmadura(self, bobject):
        arm = bobject.data;
        esq=Esqueleto();
        esq.huesos=arm.bones;
        esq.trimHuesos();
        return esq;

    def procesarAnimaciones(self, bobject,f):
        f.write(struct.pack("<I",len(bpy.data.actions))); 
        esq=self.procesarArmadura(bobject);
        print("writing acciones:",f.tell());
        for a in bpy.data.actions:
            print("Accion:"+a.name);
            
            bobject.animation_data.action=a;
            inicio, fin = [int(x) for x in a.frame_range]
            fps=bpy.context.scene.render.fps;
            total=fin-inicio;
            print("acciones:"+str(len(bpy.data.actions)));
#            f.write(struct.pack("<I",len(a.name))); 
#            if len(a.name)>0:
            f.write(bytearray(a.name+"\00","ascii"));
            f.write(struct.pack("<I",total)); #Cantidad de frames
            i=0;
            for frame in range(inicio,fin):
                f.write(struct.pack("<f",float(frame)/float(fps)));
                bpy.context.scene.frame_set(frame);
                i=i+1;
                for huesoId in esq.huesos:
                    if huesoId.use_deform:
                        h=bobject.pose.bones[huesoId.name]
                        matfix =mathutils.Matrix.Rotation(math.radians(-90), 4, "X");
                        matorig =h.bone.matrix_local @ matfix;
                        matpose=h.matrix @ matfix;
                        mat=matpose @ matorig.inverted();
                        q=mat.to_quaternion();
                        loc=h.matrix.translation-h.bone.matrix_local.translation;
#                    q=h.rotation_quaternion;
                        f.write(struct.pack("<f",loc.x));
                        f.write(struct.pack("<f",loc.y));
                        f.write(struct.pack("<f",loc.z));
                        f.write(struct.pack("<f",q.x));
                        f.write(struct.pack("<f",q.y));
                        f.write(struct.pack("<f",q.z));
                        f.write(struct.pack("<f",q.w));
            f.write(struct.pack("<I",len(a.pose_markers))) 
            for marker in a.pose_markers:
                f.write(bytearray(marker.name+"\00","ascii"));
                f.write(struct.pack("<f",float(marker.frame)/float(fps))) 
                
            print("cuadros:"+str(i)); 


    def execute(self, context):
        global meshes_to_clear;
        meshes_to_clear=[];
#        bpy.ops.object.mode_set(mode='OBJECT');
        result = {'FINISHED'};
        dirname =os.path.dirname(self.filepath);
        depsgraph = context.evaluated_depsgraph_get()
        filename=os.path.splitext(os.path.basename(self.filepath))[0];
        if(self.expmapa):
            filemapa=open(dirname+"/"+filename+".map","w");
        for ob in bpy.data.objects:
            if ob.type == 'MESH' and ob.visible_get():
                if(self.expmapa):
                    self.procesarObjetoMapa(ob,filemapa);
                    file = open(dirname+'/'+ob.name+'.mesh', 'bw');
                else:
                    file = open(self.filepath, 'bw');
                print("procesando mesh");
                self.procesarMesh(ob,depsgraph).writeData(file);
                file.close();
            if ob.type == 'ARMATURE':
                if ob.animation_data is not None:
                    file = open(self.filepath+".esq", 'bw');
                    print("procesando armadura");
                    self.procesarArmadura(ob).writeData(file);
                    print("procesando animaciones");
                    self.procesarAnimaciones(ob,file);
                    file.close();
        if(self.expmapa):
            filemapa.close();
        for m in meshes_to_clear:
            m.to_mesh_clear();
        return result;

