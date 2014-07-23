import csv, sys
import json as simplejson
import numpy as np
from urllib2 import urlopen
import re
import StringIO
import json
from tempfile import TemporaryFile
import random
import mlpy
import sys
import matplotlib.pyplot as plt


def clustering (depth,matrix, numCL):
  groupsOfUsers=[]

  cls, means, steps = mlpy.kmeans(matrix, k=numCL, plus=True)
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



#read files
f = open('Scenes.csv')
file = open('Scenes.csv')
minNumOfAnnotators=3
MinnnotationPerUser=5
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
for row in reader:    # generate user-speficic similarity matrices:
         depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[3])]+=1
         depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[2])]+=1
         depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[4])]-=1
         depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[3])]-=1
         depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[4])]-=1
         depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[2])]-=1


groupAnnotation= np.zeros((len(users),len(users)))
for k in range(len(users)):
    for x in range(len(users)):
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
              groupAnnotation[k][x]=((Nuv/2)*(Muv/2))/float((min(Nv/2,Nu/2)**2))


np.save("GroupAnnotation.npy"  ,  groupAnnotation)
with open("GroupAnnotation.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in   groupAnnotation.tolist()]


clustering(depth,groupAnnotation,3)

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

color=['#00FF00','#0000FF','#00FFFF','#888888','#CC6633','#990099','#00FF99','#CC0033','#CC3300','#3333FF','#6600FF','#FF99FF','#FF3399','#CC9999','#FFFF33','#66FF00','#00FF00','#009999','#CC33FF','#FF3333','#CCFF66',]


nameswithcolor = [[] for _ in range(len(Scenes))]


for i in range(len(Scenes)):
    nameswithcolor[i].append(Scenes[i])
    nameswithcolor[i].append(random.choice(color))




np.save("SceneNames.npy"  , Scenes)
with open('SceneNames.csv', 'w') as csvfile:
          writer = csv.writer(csvfile)
          [writer.writerow(r) for r in nameswithcolor]


for i in range(len(Scenes)):
    for j in range(len(Scenes)):
        if( SumofAnnotation[i][j]<0):
            SumofAnnotation[i][j]=0



json=json.dumps(SumofAnnotation.tolist())
jsonfile=open("AverageAnnotationNormalized.json","w")
jsonfile.write(json)
jsonfile.close()



np.save('Agreement.npy', Agreement)
with open('Agreement.csv', 'w') as csvfile:
          writer = csv.writer(csvfile)
          [writer.writerow(r) for r in Agreement.tolist()]





Agr = np.load("Agreement.npy");
print "coverage = {0:.1f}%\t agreement = {1:.2f}%".format(100.0 * np.count_nonzero(Agr) / (Agr.shape[0]*Agr.shape[1]), 100.0*Agr[Agr.nonzero()].mean())




