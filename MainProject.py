import csv
import json as simplejson
import numpy as np
from urllib2 import urlopen
import re
import StringIO
from tempfile import TemporaryFile


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
for row in reader:

     depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[3])]+=1
     depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[2])]+=1
     depth[users.index(row[1])][Scenes.index(row[3])][Scenes.index(row[4])]-=1
     depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[3])]-=1
     depth[users.index(row[1])][Scenes.index(row[2])][Scenes.index(row[4])]-=1
     depth[users.index(row[1])][Scenes.index(row[4])][Scenes.index(row[2])]-=1



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

#concate all the annotations of the users and save it
np.save("AllannotationsOfUsers.npy"  , SumofAnnotation)
with open('AllannotationsOfUsers.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      [writer.writerow(r) for r in SumofAnnotation.tolist()]


np.save("AllScenes.npy"  , Scenes)


#find min and max of SumofAnnotation
smMin=SumofAnnotation.min()
smMax=SumofAnnotation.max()

#normalized the SumofAnnotation and save it
SumofAnnotation[np.diag_indices_from(SumofAnnotation)] = smMax
SumofAnnotation=(SumofAnnotation-smMax)/(smMax-smMin)


np.save("SumofAnnotationNormalized.npy"  , SumofAnnotation)
with open('SumofAnnotationNormalized.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      [writer.writerow(r) for r in SumofAnnotation.tolist()]

#make Agreement similarity matrix and save it
Agreement=np.zeros((len(Scenes),len(Scenes)))
for i in range(len(Scenes)):
    for j in range(len(Scenes)):
        if(abs(CountMin[i][j]) > abs(CountPlus[i][j])):
            Agreement[i][j]=abs(CountMin[i][j])/(abs(CountMin[i][j])+abs(CountPlus[i][j]))
        elif ( abs(CountMin[i][j]) <  abs(CountPlus[i][j])):
            Agreement[i][j]=CountPlus[i][j]/(abs(CountMin[i][j])+abs(CountPlus[i][j]))
        else:
            Agreement[i][j]=0

np.save('Agreement.npy', Agreement)
with open('Agreement.csv', 'w') as csvfile:
      writer = csv.writer(csvfile)
      [writer.writerow(r) for r in Agreement.tolist()]


