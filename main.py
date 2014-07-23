import numpy
import matplotlib.pyplot as plt
import os
import mlpy
import sys

def clustering (matrix, k=8):
  cls, means, steps = mlpy.kmeans(matrix, k=k, plus=True)
  print cls
  group=0
  for i in range (0,k):
    for j in cls:
      if (j==i):
        group+=1
    print "In cluster %s are %s users" % (i,group)
    group=0

  #drawplot(matrix, cls, means)


def drawplot(matrix, cls,means):
  fig = plt.figure(1)
  plot1 = plt.scatter(matrix[:,0], matrix[:,1], c=cls, alpha=0.75)
  plot2 = plt.scatter(means[:,0], means[:,1], c=numpy.unique(cls), s=128, marker='d') # plot the means
  plt.show()

def getsample(path, filename):
  if os.path.exists(path):
    return numpy.load(path+filename)

if __name__ == '__main__':

  path = sys.argv[1]
  filename = sys.argv[2]
  array = getsample(path,filename)
  print len(array[0])
  clustering(array)
