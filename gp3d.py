'''
Created on 10/05/2013

@author: forestmedina
'''

import bpy;
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
    register_class(VoxelizarOP)
    register_class(FileHeader)
    register_class(FileBody)
    register_class(PanelOpciones)


def unregister():
    unregister_class(Exporter)
    unregister_class(VoxelizarOP)
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

class VoxelizarOP(bpy.types.Operator):
    bl_idname = "export_opengl.voxelizar"
    bl_label = "Minimal Operator"

    def execute(self, context):
        voxelizar()
        return {'FINISHED'}

class Vertice():
    def __init__(self):
        self.co=[0.0]*3;
        self.normal=[0.3]*3;
        self.color=[0.0]*3;
        return;
def pointInsideMesh(ob, pt):
        Vector = mathutils.Vector
        def ptInFaceXYBounds(mesh,f,_pt):
               # print("intersecta xy")
                v1=mesh.vertices[f.vertices[0]]
                v2=mesh.vertices[f.vertices[1]]
                v3=mesh.vertices[f.vertices[2]]
                xmax= xmin= v1.co.x
                ymax= ymin= v1.co.y

                xmax= max(xmax, v2.co.x)
                xmin= min(xmin, v2.co.x)

                ymax= max(ymax, v2.co.y)
                ymin= min(ymin, v2.co.y)

                xmax= max(xmax, v3.co.x)
                xmin= min(xmin, v3.co.x)

                ymax= max(ymax, v3.co.y)
                ymin= min(ymin, v3.co.y)
 
		# Now we have the bounds, see if the point is in it.
                return (xmin <= _pt.x <= xmax) and (ymin <= _pt.y <= ymax)
 
        def faceIntersect(mesh,f,_ray,_pt):
                #print("intersecta tirangulo")
                v1=mesh.vertices[f.vertices[0]]
                v2=mesh.vertices[f.vertices[1]]
                v3=mesh.vertices[f.vertices[2]]
                if len(f.vertices)==4:
                    v4=mesh.vertices[f.vertices[3]]
                #print("rayo:");
                #print(ray);
                #print("obSpacept:");
                #print(obSpacePt);
                isect = mathutils.geometry.intersect_ray_tri(v1.co, v2.co, v3.co, _ray, _pt, True) # Clipped.
                #if isect is None:
                    # print("isect")
                    #print(_pt)
                    #print("--")
                    #print(v1.co)
                    #print(v2.co)
                    #print(v3.co)
        #            print (isect.z);
        #            print (obSpacePt.z);
               # if not isect and len(f.vertices) == 4:
               #     isect = mathutils.geometry.intersect_ray_tri(v2.co, v3.co, v4.co, ray, pt, True) # Clipped.
                return bool(isect is not None ) # This is so the ray only counts if its above the point. 
        obImvMat = mathutils.Matrix(ob.matrix_world)
        obImvMat.invert()
        pt.resize_4d()
        obSpacePt = pt* obImvMat
        pt.resize_3d()
        obSpacePt.resize_3d()

        me= ob.data
        niz=0;
        nix=0;
        niy=0;
        niw=0;
        niv=0;
        ptOr=pt;
        ray = Vector((0.0,0.0,-1.0))
        for f in me.polygons:
            if ptInFaceXYBounds(me,f,pt) or False:

                pt=ptOr
                #print("***")
                if  faceIntersect(me,f,ray,pt):
                    niz=niz+1;
#            ray = Vector((-1,0,0))
             #pt=ptOr+Vector((0.38,0.45,0.0));
#        print("ni")
#        print(niz)
#        print(nix)
#        print(niy)
#        print(niw)
#        print(niv)

        #return  niz%2!=0 or nix%2!=0 or niy%2!=0 or niw%2!=0 or niv%2!=0
        #return  ((niz%2)+(nix%2)+(niy%2)+(niw%2)+(niv%2))>2
        return  (niz%2)!=0


def voxelizar():
    ob= bpy.context.active_object
    p1=ob.bound_box[0];
    p2=ob.bound_box[6];
#    f.write(struct.pack("<I",round(p1[0])-round(p2[0])));
#    f.write(struct.pack("<I",round(p1[1])-round(p2[1])));
#    f.write(struct.pack("<I",round(p1[2])-round(p2[2])));
    for z in range(round(p1[2]),round(p2[2])):
        for y in range(round(p1[1]),round(p2[1])):
            for x in range(round(p1[0]),round(p2[0])):
                p=mathutils.Vector((float(x),float(y),float(z)));
              #  print("Revisando Punto");
               # print(p);
                if pointInsideMesh(ob,p):
            #        bpy.ops.mesh.primitive_cube_add(radius=0.5,location=p)
 #                   f.write(struct.pack("<B",1));
                     bpy.ops.object.add(radius=0.5,location=p)
                #    print("si")
                     a=True;

    p=mathutils.Vector((9.0,-12.0,5.0));
    print("Revisando Punto");
    print(p);
    if pointInsideMesh(ob,p):
         print("si")


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
            f.write(struct.pack("<f",v.normal[2]));#VextexSize 3 (x,y,z)
        for v in self.vertices:
            f.write(struct.pack("<f",v.color[0]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[1]));#VextexSize 3 (x,y,z)
            f.write(struct.pack("<f",v.color[2]));#VextexSize 3 (x,y,z)
        for v in self.vertices:
            if len(v.groups)>0:
                f.write(struct.pack("f",v.groups[0].group));
            else:
                f.write(struct.pack("f",0));
        for v in self.vertices:
            if len(v.groups)>0:
                f.write(struct.pack("f",v.groups[0].weight));
            else:
                f.write(struct.pack("f",0));
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
        return;

    def writeData(self,f):
        f.write(struct.pack("<I",len(self.huesos)));
        for h in self.huesos:
            if h.parent is None:
                f.write(struct.pack("<i",-1));
            else:
                f.write(struct.pack("<i",self.huesos.find(h.parent.name)));
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
    
        
    def procesarMesh(self, bobject):
        for mod in bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=False; 
        mesh = bobject.to_mesh(bpy.context.scene,True,'PREVIEW',True,False);
        for mod in bobject.modifiers:
            if mod.type=='ARMATURE':
                mod.show_viewport=True; 
        meshes_to_clear.append(mesh);
        omesh=Mesh();

        omesh.vertices=[0]*len(mesh.vertices)
        for i in range(0,len(mesh.vertices)):
            v=Vertice();
            v.co=mesh.vertices[i].co;
            v.normal=mesh.vertices[i].normal;
            v.groups=mesh.vertices[i].groups;
            omesh.vertices[i]=v;
        omesh.caras=mesh.polygons;
        colores=[0]*10;
        for p in mesh.polygons:
            for li in p.loop_indices:
                vi=mesh.loops[li].vertex_index;
                omesh.vertices[vi].color= mesh.vertex_colors[0].data[li].color; 
        omesh.colores=colores;
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
        return esq;

    def procesarAnimaciones(self, bobject,f):
        f.write(struct.pack("<I",len(bpy.data.actions))); 
        for a in bpy.data.actions:
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
                for h in bobject.pose.bones:
                    matfix =mathutils.Matrix.Rotation(math.radians(-90), 4, "X");
                    matorig =h.bone.matrix_local*matfix;
                    matpose=h.matrix*matfix;
                    mat=matpose*matorig.inverted();
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
            print("cuadros:"+str(i)); 


    def execute(self, context):
        global meshes_to_clear;
        meshes_to_clear=[];
#        bpy.ops.object.mode_set(mode='OBJECT');
        result = {'FINISHED'};
        dirname =os.path.dirname(self.filepath);
        filename=os.path.splitext(os.path.basename(self.filepath))[0];
        if(self.expmapa):
            filemapa=open(dirname+"/"+filename+".map","w");
        for ob in bpy.data.objects:
            if ob.type == 'MESH' and ob.is_visible(bpy.context.scene):
                if(self.expmapa):
                    self.procesarObjetoMapa(ob,filemapa);
                    file = open(dirname+'/'+ob.name+'.mesh', 'bw');
                else:
                    file = open(self.filepath, 'bw');
                self.procesarMesh(ob).writeData(file);
                file.close();
            if ob.type == 'ARMATURE':
                file = open(self.filepath+".esq", 'bw');
                self.procesarArmadura(ob).writeData(file);
                self.procesarAnimaciones(ob,file);
                file.close();
        if(self.expmapa):
            filemapa.close();
        for m in meshes_to_clear:
            bpy.data.meshes.remove(m);
        return result;

