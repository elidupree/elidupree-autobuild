#!/usr/bin/python3

# A simple script to watch a file and automatically run a build script whenever the file changes.
# If the build script is still running when the change happens, terminate it and started again.
# I use this in conjunction with using hilarious-text-editor's on-save feature to automatically touch a file whenever I've modified any part of a project.

import time
import os
import os.path
import sys
import signal
import subprocess

if len(sys.argv) < 3:
  print("usage: watch.py watchpath buildpath [memory limit, default 1000000 (kB)]")
  sys.exit(0)

watch_path = sys.argv[1]
build_path = sys.argv[2]
memory_limit = 1000000
if 3 in sys.argv:
  memory_limit = int(sys.argv[3])

on_change_commands = [build_path]
running_processes = []

def on_change ():
  for (command, process) in running_processes:
    sys.stderr.write('\nAbout to terminate: ' + command + '\n')
    try:
      os.killpg (os.getpgid(process.pid), signal.SIGTERM)
    except OSError:
      sys.stderr.write('\nOld process already exited with status ' + str(process.returncode) + '\n')      
    sys.stderr.write('\nDone terminating: ' + command + '\n')
    
  # Reset the color, in case a terminated process left a color lying around
  print('\x1b[0m', end='')
    
  running_processes[:] = []
    
  for command in on_change_commands:
    exact = 'ulimit -v 10000000; nice -n 15 '+command
    sys.stderr.write('Running: ' + command + '\n')
    running_processes.append ((command, subprocess.Popen (exact, shell=True, start_new_session = True)))

last_modified_time = None
while True:
  modified_time = None
  try:
    modified_time = os.path.getmtime (watch_path)
  except OSError:
    pass
  #print ("Saw time: "+str(modified_time))
  if modified_time is not None:
    if last_modified_time is not None and modified_time > last_modified_time:
      on_change()
    last_modified_time = modified_time
  
  time.sleep(1)
