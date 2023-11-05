#!/n/HOME/miniconda3/bin/python

# A simple script to watch a file and automatically run a build script whenever the file changes.
# If the build script is still running when the change happens, terminate it and started again.
# I use this in conjunction with using hilarious-text-editor's on-save feature to automatically touch a file whenever I've modified any part of a project.

import time
import os
import os.path
import sys
import signal
import subprocess
import psutil
from datetime import datetime

if len(sys.argv) < 3:
  print("usage: watch.py watchpath buildpath [memory limit, default 1000000 (kB)]")
  sys.exit(0)

watch_path = sys.argv[1]
build_path = sys.argv[2]
memory_limit = 1000000
if len(sys.argv) >= 4:
  memory_limit = int(sys.argv[3])

on_change_commands = [build_path]
running_processes = []

def stop_all_commands():
  all_procs = []
  for (command, process) in running_processes:
    root = psutil.Process(process.pid)
    children = root.children(recursive=True)
    tree = [root]+children
    sys.stderr.write('\nAbout to terminate: ' + command + '\n')
    try:
      os.killpg (os.getpgid(process.pid), signal.SIGTERM)
      sys.stderr.write('\nSent SIGTERM to: ' + command + '\n')
    except OSError:
      sys.stderr.write('\nOld process already exited with status ' + str(process.returncode) + '\n')
      
    #sys.stderr.write(f'\nDouble terminating all of: {[p.name() for p in tree]}\n')
    #for p in tree:
    #  p.terminate()
    all_procs.extend(tree)
    
  sys.stderr.write(f'\nWaiting on all of: {[p.name() for p in all_procs]}')
  gone, alive = psutil.wait_procs(all_procs, timeout=3)
  if alive:
    sys.stderr.write(f'\nThese processes didn\'t quit after 3 seconds and will be killed: {[p.name() for p in alive]}')
    for p in alive:
      p.kill()
  sys.stderr.write('\nFinished terminating old processes\n')
    
  # Reset the color, in case a terminated process left a color lying around
  print('\x1b[0m', end='')
  
  running_processes[:] = []
    

def on_change():
  stop_all_commands()
  
  for command in on_change_commands:
    exact = f'ulimit -v {memory_limit}; nice -n 15 '+command
    sys.stderr.write('Running at '+str(datetime.now())+': ' + exact + '\n')
    running_processes.append ((command, subprocess.Popen (exact, shell=True, start_new_session = True)))

try:
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
except KeyboardInterrupt:
  stop_all_commands()
