Groups series of images taken with Canon's focus bracketing function into distinct folders to help stacking and / or post-process the images. Supports Canon CR3 files.

# Based on
 - PyExifTool - A Python wrapper for Phil Harvey's ExifTool (https://github.com/sylikc/pyexiftool)
 - ExifTool by Phil Harvey (https://exiftool.org/)

# Dev Requirements
Don't know yet how to properly define requirements for a python project.
Here's a summary what I did on dev machine:
 - pip install pyexiftool
 - Python 3.10+ (3.6 or above for PyExifTool, 3.10.0 or above for match)
 - GUI (https://github.com/chriskiehl/Gooey):
    - Gooey requires wxPython. Here it is installed from pre-compiled package (for Ubuntu):
   ```
   sudo apt update && sudo apt install libgtk-3-dev
   pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython
   pip install Gooey
   ```
 - For running the program, ExifTool(.exe) must be placed on working directory or PATH


# Installer
Based on Gooey's help & spec: https://github.com/chriskiehl/Gooey/blob/master/docs/packaging/Packaging-Gooey.md
Notes how I did it the last time:
 - Rename / copy build-win.spec.template to build-win.spec (not sure of necessary though)
 - Run at the root of the repo: `pyinstaller build-win.spec`
   - Options adivised in Gooey's instructions do not work with pyinstaller >5.0

Icon by <a href="https://freeicons.io/profile/5790">ColourCreatype</a> on <a href="https://freeicons.io">freeicons.io</a>
