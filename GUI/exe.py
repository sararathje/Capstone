import sys
from cx_Freeze import setup, Executable
packages = ['tkinter', 'pyfirmata', 'threading', 'warnings', 'serial', 'sys', 'cv2', 'numpy', 'datetime', 'os', 'platform']
import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"
setup(
    name = "test",
    version = "0.1",
    desciption = "Sarps Lighting GUI",
    options = {'build_exe': {'packages':packages}},
    executables = [Executable("lighting_gui.py", base = None)])
