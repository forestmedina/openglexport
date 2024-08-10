SET mypath=%~dp0
python %mypath%\convert_fbx.py  %1
echo  %mypath%\convert_fbx.py  %1
pause