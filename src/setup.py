# This script is used to build an executable application from the code
#  as well as an .msi installer that can be used for releases.

import cx_Freeze
import sys
import os

base = None
if sys.platform == "win32":
    base = "Win32GUI"

path = os.path.join(os.environ['LOCALAPPDATA'], f"AssettoTrafficServerCarTool")

executables = [cx_Freeze.Executable("main.py", base=base, target_name="AssettoTrafficServerCarTool.exe")]

cx_Freeze.setup(
    name="AssettoTrafficServerCarTool",
    options={"build_exe": {"packages":["pygame", "datetime", "tkinter", "os", "shutil", "sys", "re"],
                           "include_files":["util.py"]},
            "bdist_msi": {'initial_target_dir': path}},
    executables = executables

)