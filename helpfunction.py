import os
from os.path import basename

def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)

def fileNamesCutter(filesNames):
  files = []
  for x in filesNames:
    files.append(basename(x))
  return files