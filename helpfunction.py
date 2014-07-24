import os
import numpy
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

def lenTextInFiles(path):
  filesLength ={}
  for root, dirs, files in os.walk(path):
    files.sort()
    for fileread in files:
      if fileread.endswith(".txt"):
        with open(path + fileread) as a_file:
          num_lines = sum(1 for line in a_file)
          filesLength[fileread]=num_lines
          #print filesLength[a_file]=num_lines
  return filesLength


def transforMatrix(fileNameText,fileNameGrund,grundMatrix):
  newGrundTrustMatrix = []
  saveIndex = []
  if (len(fileNameText) != len(fileNameGrund)):
    for i in range (len(fileNameText)):
      cuttedFileName = os.path.basename(fileNameText[i]).split('.',1)[0]
      for j in range(0,len(fileNameGrund)):
        cuttedFileNameGTM =(fileNameGrund[j].split('/'))[4].split('.',1)[0]
        if (cuttedFileName == cuttedFileNameGTM):
          saveIndex.append(j)
    for k in range(0,len(saveIndex)):
      row = grundMatrix[saveIndex[k]]
      newrow = []
      for l in range(0,len(saveIndex)):
        newrow.append(row[saveIndex[l]])
      newGrundTrustMatrix.append(newrow)

    return numpy.array(newGrundTrustMatrix)
  else:
    return grundMatrix