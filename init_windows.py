#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
  print("usage: init_windows.py projectname port")
  sys.exit(0)

project = sys.argv[1]
port = sys.argv[2]

with open ("C:\\Users\\Eli\\Documents\\" + project + "\\modify_noticer", "w") as file:
  pass
with open ("C:\\Users\\Eli\\Documents\\hilarious-text-editor\\edit_" + project + ".cmd", "w") as file:
  file.write ("""
C:\\Users\\Eli\\Documents\\hilarious-text-editor\\hilarious.py ^
  C:\\Users\\Eli\\Documents\\""" + project + """ ^
  --port """ + port + """ ^
  --on-save "copy /b C:\\Users\\Eli\\Documents\\""" + project + """\\modify_noticer +,, C:\\Users\\Eli\\Documents\\""" + project + """\\modify_noticer" ^
  --exclude-re "[\\\\/](\\.git|target|build)[\\\\/]"
pause
""")
