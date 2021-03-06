import csv, sys
import json as simplejson
import numpy as np
from urllib2 import urlopen
import re
import StringIO
import json
from tempfile import TemporaryFile
import random
import matplotlib.pyplot as plt
import mlpy
import heapq



def clustering (depth,numCL):
  matrix = np.load("GroupAnnotation.npy");
  groupsOfUsers=[]
  cls, means, steps = mlpy.kmeans(matrix, k=numCL)
  print cls
  for i in range(numCL):
      groupsOfUsers.append(np.zeros((27,27)))
  for i in range(len(cls)):
        groupsOfUsers[cls[i]]+=depth[i]
  for i in range(numCL):
        np.save("groupOfUsers%02d.npy" % i , groupsOfUsers[i])
        with open("groupOfUsers%02d.csv" % i, 'w') as csvfile:
            writer = csv.writer(csvfile)
            [writer.writerow(r) for r in   groupsOfUsers[i].tolist()]
  drawplot(matrix, cls, means)




def drawplot(matrix, cls,means):
  fig = plt.figure(1)
  plot1 = plt.scatter(matrix[:,0], matrix[:,1], c=cls, alpha=0.75)
  plot2 = plt.scatter(means[:,0], means[:,1], c=np.unique(cls), s=128, marker='d') # plot the means
  plt.show()



def readDataSimilarities(minNumOfAnnotators,path):

	#read files
	f = open('Scenes.csv')
	file = open('Scenes.csv')

	#create lists to read the names of the Scenes
	Allusers=[]
	all=[]
	b=[]
	c=[]
	d=[]
	depth=[]

	#read the names  of the Scenes and the users names
	reader = csv.reader(f, delimiter=';')
	for row in reader:
	    Allusers.append(row[1])
	    b.append(row[2])
	    c.append(row[3])
	    d.append(row[4])


	#concate the lists
	all= b+c+d
	Scenes=list(set(all))
	Scenes.sort()
	users=list(set(Allusers))
	users.sort()

	#create 3 lists numpy
	SumofAnnotation = np.zeros((len(Scenes),len(Scenes)))
	CountPlus=np.zeros((len(Scenes),len(Scenes)))
	CountMin=np.zeros((len(Scenes),len(Scenes)))


	#create array that take the size of the user length
	for i in range(len(users)):
	    depth.append(np.zeros((27,27)))




	#read again the file of annotations and put the values at depth array
	reader = csv.reader(file, delimiter=';')
	for row in reader:	# generate user-speficic similarity matrices:
	     depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[3])]+=1
	     depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[2])]+=1
	     depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[4])]-=1
	     depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[3])]-=1
	     depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[4])]-=1
	     depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[2])]-=1

	groupAnnotation= np.zeros((len(users),len(users)))
    similarUsers= {}
    MaxSimilarUsers=5
	for k in range(len(users)):
	    for x in range(len(users)):
	            print "k,x", k, x
	            if(k!=x):
	              Nv=0
	              Nu=0
	              Nuv=0
	              Muv=0
	              for i in range(len(Scenes)):
	                  for j in range(len(Scenes)):
	                      if(i!=j):
	                        if(depth[k][i][j]!=0):
	                              Nu+=1
	                        if(depth[x][i][j]!=0):
	                            Nv+=1
	                        if(depth[k][i][j]!=0  and depth[x][i][j]!=0):
	                          Nuv+=1
	                        if((depth[k][i][j]>0  and depth[x][i][j]>0) or (depth[k][i][j]<0  and depth[x][i][j]<0)):
	                          Muv+=1
	              if(Nuv/2!=0):
                      groupAnnotation[k][x]=(Muv/2)/float(Nuv/2)
                  else:
                      groupAnnotation[k][x]=0
                  Names=users[k]+'-'+ users[x]
                  Name=users[x]+'-'+ users[k]
                  if Names not in similarUsers:
                        if Name not in similarUsers:
                            similarUsers[Names]= groupAnnotation[k][x]


    similars=heapq.nlargest(MaxSimilarUsers, similarUsers, key=similarUsers.get)
    for i in range(MaxSimilarUsers):
        print similars[i],similarUsers[similars[i]]

    dissimilar=heapq.nsmallest(MaxSimilarUsers, similarUsers, key=similarUsers.get)
    for i in range(MaxSimilarUsers):
        print dissimilar[i],similarUsers[dissimilar[i]]




	np.save("GroupAnnotation.npy"  ,  groupAnnotation)
	with open("GroupAnnotation.csv", 'w') as csvfile:
	        writer = csv.writer(csvfile)
	        [writer.writerow(r) for r in   groupAnnotation.tolist()]


	#count the positive and the negative values
	for i in range(len(users)):
	     for j in range(len(Scenes)):
		 	   for x in range(len(Scenes)):
		 	   	if (depth[i][j][x]>0):
		 	   		CountPlus[j][x]+=depth[i][j][x]
		 	   	if(depth[i][j][x]<0):
		 	   		CountMin[j][x]+=depth[i][j][x]
	     #create annotation of each user
	     SumofAnnotation+=depth[i]
	     np.save("annotations%02d.npy" % i , depth[i])
	     with open("annotations%02d.csv" % i, 'w') as csvfile:
		      writer = csv.writer(csvfile)
		      [writer.writerow(r) for r in   depth[i].tolist()]


	#make Agreement similarity matrix and save it
	Agreement=np.zeros((len(Scenes),len(Scenes)))
	for i in range(len(Scenes)):
	    for j in range(len(Scenes)):
			if abs(CountMin[i][j]) + abs(CountPlus[i][j]) >= minNumOfAnnotators :
			   SumofAnnotation[i][j] /= float((abs(CountMin[i][j])+abs(CountPlus[i][j])))
			   if(abs(CountMin[i][j]) > abs(CountPlus[i][j])):
			    	Agreement[i][j]=abs(CountMin[i][j])/(abs(CountMin[i][j])+abs(CountPlus[i][j]))
			   else:
			    	Agreement[i][j]=CountPlus[i][j]/(abs(CountMin[i][j])+abs(CountPlus[i][j]))
			else:
				Agreement[i][j]=0
				SumofAnnotation[i][j] = 0



	#concate all the annotations of the users and save it
	np.save("AverageAnnotation.npy"  , SumofAnnotation)
	with open('AverageAnnotation.csv', 'w') as csvfile:
	      writer = csv.writer(csvfile)
	      [writer.writerow(r) for r in SumofAnnotation.tolist()]

	np.save("SceneNames.npy"  , Scenes)
	color=['#FF0000','#00FF00','#0000FF','#FFFF00','#00FFFF','#888888','#CC6633','#990099','#00FF99','#CC0033','#CC3300','#3333FF','#6600FF','#FF99FF','#FF3399','#CC9999','#FFFF33','#66FF00','#00FF00','#009999','#CC33FF','#FF3333','#CCFF66',]

	nameswithcolor = [[] for _ in range(len(Scenes))]


	for i in range(len(Scenes)):
	    nameswithcolor[i].append(Scenes[i])
	    nameswithcolor[i].append(random.choice(color))



	np.save("SceneNames.npy"  , Scenes)
	with open(path+'SceneNames.csv', 'w') as csvfile:
	          writer = csv.writer(csvfile)
	          [writer.writerow(r) for r in nameswithcolor]

	for i in range(len(Scenes)):
		for j in range(len(Scenes)):
			if( SumofAnnotation[i][j]<0):
				SumofAnnotation[i][j]=0

	json=json.dumps(SumofAnnotation.tolist())
	jsonfile=open(path+"AverageAnnotationNormalized.json","w")
	jsonfile.write(json)
	jsonfile.close()

    clustering(depth,3)
	np.save('Agreement.npy', Agreement)
	with open('Agreement.csv', 'w') as csvfile:
	      writer = csv.writer(csvfile)
	      [writer.writerow(r) for r in Agreement.tolist()]



def statistics():
	Agr = np.load("Agreement.npy");
	print "coverage = {0:.1f}%\t agreement = {1:.2f}%".format(100.0 * np.count_nonzero(Agr) / (Agr.shape[0]*Agr.shape[1]), 100.0*Agr[Agr.nonzero()].mean())

def main(argv):
	if (len(argv)==2):
		readDataSimilarities(int(argv[1]),"")
		statistics()

	if (len(argv)==3):
		readDataSimilarities(int(argv[1]),argv[2])
		statistics()


if __name__ == '__main__':
	main(sys.argv)
