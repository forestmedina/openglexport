#/usr/bin/python
import sys
import bpy

filedir=sys.argv[len(sys.argv)-1]
print ("Exportando a: ",filedir)
bpy.ops.export_opengl.gpb(directory=filedir);
exit(0);
