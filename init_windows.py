#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
  print("usage: init_windows.py projectname port")
  sys.exit(0)

project = sys.argv[1]
port = sys.argv[2]
make_build_script = len(sys.argv) > 3 and sys.argv[3] == "-b"
hilarious_path = 'C:\\Users\\Eli\\Documents\\hilarious-text-editor'
project_path = 'C:\\Users\\Eli\\Documents\\' + project
build_script_path = f'{hilarious_path}\\build_{project}.cmd'

if make_build_script:
  on_save = f'''" ""{build_script_path}"" "'''
else:
  on_save = f'''"copy /b ""{project_path}\\modify_noticer"" +,, ""{project_path}\\modify_noticer"" "'''

with open (project_path + "\\modify_noticer", "w") as file:
  pass
with open ("C:\\Users\\Eli\\Documents\\hilarious-text-editor\\edit_" + project + ".cmd", "w") as file:
  file.write (f"""
python ""{hilarious_path}\\hilarious.py"" ^
  ""C:\\Users\\Eli\\Documents\\{project}"" ^
  --port {port} ^
  --on-save {on_save} ^
  --exclude-re "[\\\\/](\\.git|target|build)[\\\\/]"
pause
""")

if make_build_script:
  with open (build_script_path, "w") as file:
    file.write (f"""cd "{project_path}"
copy /b "{project_path}\\modify_noticer" +,, "{project_path}\\modify_noticer"

""")
