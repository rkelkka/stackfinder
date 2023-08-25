Groups series of images taken with Canon's focus bracketing function into distinct folders to help stacking and / or post-process the images. Supports Canon CR3 files.

Based on
 - PyExifTool - A Python wrapper for Phil Harvey's ExifTool (https://smarnach.github.io/pyexiftool/)
 - ExifTool by Phil Harvey (https://exiftool.org/)
 
Requirements
 - pip install pyexiftool
 - ExifTool placed on working directory or PATH
 - Python 3.5+
 - GUI (on github codespace):
   ```
   sudo apt update && sudo apt install libgtk-3-dev
   pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython
   pip install Gooey
   ```
   - here wxpython is installed from pre-compiled package