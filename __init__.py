bl_info = {
    "name":         "OpenglExportador",
    "author":       "forestmedina",
    "blender":      (2,80,0),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Exportar para OPENGL personalizado",
    "category":     "Import-Export"
}

# Ensure that we reload our dependencies if we ourselves are reloaded by Blender
if "bpy" in locals():
    import imp;
    if "gp3d" in locals():
        imp.reload(gp3d);
else:
    from openglexport.gp3d import (
            Exporter,
            )
        
import bpy;
classes = (
    Exporter,
)

def menu_func(self, context):
    self.layout.operator(Exporter.bl_idname, text="Opengl Personalizado(.mesh)");

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func);

    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func);

if __name__ == "__main__":
    register()
