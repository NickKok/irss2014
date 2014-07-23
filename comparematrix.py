import cPickle
import os, sys , numpy

modellsi = "movielsi"
folderlsi= "lsi/"


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

def readFiles(foldername):
  fileNames = cPickle.load(open(folderName+folderlsi + modellsi + '.filenames', 'rb'))
  similarityMatrix = numpy.load(folderName + folderlsi+modellsi+'.npy')
  grundTrustMatrix = numpy.load(folderName + "gtm/AverageAnnotation.npy")
  filesGTM = numpy.load(folderName + "gtm/SceneNames.npy")
  return fileNames,grundTrustMatrix,similarityMatrix,filesGTM

def comparematrix(folderName,coefficient =1.2):
  fileNames,grundTrustMatrix,similarityMatrix,filesGTM = readFiles(folderName)
  recall = []
  precision = []
  for i in range(0,len(fileNames)):
    gtm=evaluateGTM(grundTrustMatrix[i],coefficient)
    sm=evaluateSM(similarityMatrix[i],coefficient)
    similarity = numpy.intersect1d(gtm,sm)
    if len(gtm)!= 0 :
      recall.append(float(len(similarity))/float(len(gtm)))
    else :
      recall.append(0)
    if len(sm)!= 0 :
      precision.append(float(len(similarity))/float(len(sm)))
    else :
      precision.append(0)
    #debugprint(gtm,sm,similarity,lenTextInFiles(folderName), recall[i],precision[i],fileNames[i],similarityMatrix[i],grundTrustMatrix[i],filesGTM[i])
  print "Compare Matrix (the most similar values)"
  printInfo (recall,precision)
  """
    #lenTextinFiles = lenTextInFiles(folderName)
    #newgrundTrustMatrix = transforMatrix(fileNames,filesGTM,grundTrustMatrix)

    if len(gtm)!= 0 and len(sm) !=0 and len(similarity) !=0 :
      recall.append(float(len(similarity))/float(len(gtm)))
      precision.append(float(len(similarity))/float(len(sm)))
      print "Recall "
      print (float(len(similarity))/float(len(gtm)))
      print "Precision "
      print (float(len(similarity))/float(len(sm)))
      print "--"*30
  """

def debugprint (gtm,sm,similarity,fileLength,recall,precision,fileNames,similarityLSI,grundTrustMatrix,fileGMT):
  print " GTM row : "
  print grundTrustMatrix
  print "--"*30
  print "SM row: "
  print similarityLSI
  print "--"*30
  print " GTM : "
  print gtm
  print "--"*30
  print "SM : "
  print sm
  print "--"*30
  print "Similarity : "
  print similarity
  print "--"*30
  print "Recall :"
  print recall
  print "--"*30
  print "Precision :"
  print precision
  print "--"*30
  print "fileTextLength :"
  print fileLength[os.path.basename(fileNames)]
  print "FileTextName :"
  print fileNames
  print "--"*30
  print "FileGTMName :"
  print fileGMT
  print "/"*30

def evaluateGTM(row, coef):
  T_value = 0
  index = numpy.transpose(numpy.nonzero(row))
  for val in range(0,len(index)):
    T_value += row[index[val]]
  if T_value <= 0 :
    T_value = 0
  else:
    T_value /= numpy.count_nonzero(row)
  result =[]
  indexOfResult=0
  for check in (row > T_value*coef):
    if check == True :
      result.append(indexOfResult)
    indexOfResult +=1
  return numpy.array(result)

def evaluateSM(row,coef):
  T_value = 0
  for val in range(0,len(row)):
    T_value += row[val]
  T_value /= len(row)-1
  result =[]
  indexOfResult=0
  for check in (row > T_value*coef):
    if check == True :
      result.append(indexOfResult)
    indexOfResult +=1
  return numpy.array(result)


def evaluateSMRandom(row,coef,length):
  random_index = numpy.random.permutation(len(row))
  #TODO: choose the number of return values
  T_value = 5 #length
  result =[]
  for i in range(0,int(T_value)):
    result.append(random_index[i])
  return numpy.array(result)


def evaluateMetric30per(row1, row2):
  indexofMatrix = row2.argsort()[-3:]
  #indexofMatrix = evaluateSMRandom(row2,1)*
  x=int(len(row1)/3)
  indexGTM = row1.argsort()[-x:]
  similarity = numpy.intersect1d(indexofMatrix,indexGTM)
  """
  print "row 1"
  print row1
  print "index "
  print indexGTM
  print "row2"
  print row2
  print "index"
  print indexofMatrix
  print "similarity"
  print similarity
  """
  return (float(len(similarity))/3)

def comparematrixRandom30percent(folderName,coefficient =1.2):
  fileNames,grundTrustMatrix,similarityMatrix,filesGTM = readFiles(folderName)
  result = []
  for i in range(0,len(fileNames)):
    result.append(evaluateMetric30per(grundTrustMatrix[i],similarityMatrix[i]))
  print "Compare matrixes in 30 % "
  print numpy.array(result)
  print "Mean of result"
  print numpy.mean(numpy.array(result))

def printInfo(recall,precision):
  recall = numpy.array(recall)
  precision = numpy.array(precision)
  print "General recall :"
  print recall
  print "General precision :"
  print precision
  print "Mean of recall :"
  print numpy.mean(recall)
  print "Mean of precision"
  print numpy.mean(precision)

def comparematrixRandom(folderName,coefficient =1.2):
  fileNames,grundTrustMatrix,similarityMatrix,filesGTM = readFiles(folderName)
  recall = []
  precision = []
  for i in range(0,len(fileNames)):
    gtm=evaluateGTM(grundTrustMatrix[i],coefficient)
    sm=evaluateSMRandom(similarityMatrix[i],coefficient,len(gtm))
    similarity = numpy.intersect1d(gtm,sm)
    if len(gtm)!= 0 :
      recall.append(float(len(similarity))/float(len(gtm)))
    else :
      recall.append(0)
    if len(sm)!= 0 :
      precision.append(float(len(similarity))/float(len(sm)))
    else :
      precision.append(0)
    #debugprint(gtm,sm,similarity,lenTextInFiles(folderName), recall[i],precision[i],fileNames[i],similarityMatrix[i],grundTrustMatrix[i],filesGTM[i])
  print "Compare Matrix (random values from similarity text matrix)"
  printInfo (recall,precision)


if __name__ == '__main__':

  if sys.argv[1] == "-compare":
    folderName = sys.argv[2]
    comparematrix(folderName)
    comparematrixRandom(folderName)
    comparematrixRandom30percent(folderName)
  if sys.argv[1] == "-compareMatrix":
    folderName = sys.argv[2]
    comparematrix(folderName)
  if sys.argv[1] == "-compareMatrixRandom":
    folderName = sys.argv[2]
    comparematrixRandom(folderName)
  if sys.argv[1] == "-compareMatrix30percent":
    folderName = sys.argv[2]
    comparematrixRandom30percent(folderName)