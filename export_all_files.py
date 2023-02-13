import os
import subprocess
import sys
import pygame
import psutil
def  isProcessRunnin(p):
    return p.poll() == None





blender_base_path = os.path.join(os.environ.get("ProgramW6432", "") ,"Blender Foundation")
blender_instalations = []
for root, dirs, files in os.walk(blender_base_path):
    for file in files:
        if file == "blender.exe":
            blender_instalations.append(os.path.join(root, file))

if len(blender_instalations) == 0:
    print("Not blender installation found")
    print(os.environ.get("ProgramW6432", ""))
    print(blender_base_path)
    exit(1)
blender_path=blender_instalations[0]
if len(blender_instalations)>1:
    print ("Choose blender installation")
    for index,instalation in enumerate(blender_instalations)  :
            print(index,".",blender_instalations)

    choice = int(input("Choose an option: "))
    blender_path=blender_instalations[index]
# Replace the path with the path where the files with .blend extension are stored


#base_path = sys.argv[1]

base_path="C:/dev/sanuma/nature/res/"
files_to_process=[]
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".blend"):
            # Replace the path with the path of the plugin to be executed
            files_to_process.append( (root,file) )
total_files=len(files_to_process)

pygame.init()

# Create a window
window = pygame.display.set_mode((400, 400))

# Set window title
pygame.display.set_caption("Progress Bar")

# Create a progress bar
bar = pygame.Surface((400, 40))
progress = 0

font = pygame.font.Font("C:/windows/fonts/arial.ttf",12) # Create a Font object

processes = []
max_processes=12
finished = False
index=0
exported_count=0
map_pid={}
while not finished:
    pygame.event.pump()
    pygame.draw.rect(bar, (0, 90, 0), (0, 0, 400*progress, 40))
    text = font.render(str(exported_count)+ " of " + str(total_files), True, (255, 255, 255))  # Render the text

    # Update the progress bar
    progress = exported_count/total_files
    window.fill((255, 255, 255))

    window.blit(bar, (0, 0))
    window.blit(text, (0, 0))  # Draw the text to the screen

    pygame.display.update()
    if index < len(files_to_process):
        root,file = files_to_process[index]
        if len(processes)<max_processes:
            p=subprocess.Popen([blender_path, os.path.join(root, file), "--background", "--python", "./export.py", root],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processes.append(p)
            index += 1
    remove_list=[]
    for process in processes:
        result=process.poll()
        if  result is not None:
            exported_count+=1
            remove_list.append(process)
            if result != 0:
                print("Error exporting file ", process.args[len(process.args)-1])
                print("**********************")
                print(process.stdout)
                print(process.stderr)
                print("**********************")
                print("\n\n")
            else:
                print("Finished  exporting  ", process.args[len(process.args) - 1])
        else:
            if process.pid not in map_pid:
                uprocess=psutil.Process(process.pid)
                map_pid[process.pid]=uprocess
                uprocess.cpu_percent(0)
            else:
                uprocess=map_pid[process.pid]
                try:
                    if uprocess.cpu_percent(0)==0 :
                        print ("Process Stalled ? : ", process.args[len(process.args) - 1])
                except psutil.NoSuchProcess:
                    del map_pid[process.pid]



    for remove_process in remove_list:
        processes.remove(remove_process)
    finished= len(processes) == 0
pygame.quit()