import sys
import subprocess
import os

# Get the file name from the first parameter
fbx_name = sys.argv[1].replace("\\", "/")
print("fbx file name", fbx_name)
blender_path = "C:/Program Files/Blender Foundation/Blender 3.2/blender.exe"
blend_name = os.path.splitext(fbx_name)[0] + '.blend'
print("blend file name", blend_name)

# Run Blender in background mode
subprocess.run([
    blender_path,
    "--background",  # Run Blender in background mode
    "--python-expr",
    f"""
import bpy
bpy.ops.import_scene.fbx(filepath='{fbx_name}')
bpy.ops.wm.save_as_mainfile(filepath='{blend_name}')
bpy.ops.wm.quit_blender()
"""
])
