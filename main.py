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

  """
  numpy.random.seed(0)
  mean1, cov1, n1 = [1, 5], [[1,1],[1,2]], 200 # 200 points, mean=(1,5)
  x1 = numpy.random.multivariate_normal(mean1, cov1, n1)
  mean2, cov2, n2 = [2.5, 2.5], [[1,0],[0,1]], 300 # 300 points, mean=(2.5,2.5)
  x2 = numpy.random.multivariate_normal(mean2, cov2, n2)
  mean3, cov3, n3 = [5, 8], [[0.5,0],[0,0.5]], 200 # 200 points, mean=(5,8)
  x3 = numpy.random.multivariate_normal(mean3, cov3, n3)
  x = numpy.concatenate((x1, x2, x3), axis=0) # concatenate the samples
  clustering(x)
  """
