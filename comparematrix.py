import cPickle
import os, sys , numpy

modellsi = "movielsi"
modellda = "movielda"
folderlsi= "lsi/"
folderlda= "lda/"


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
  if (len(fileNameText) != len(fileNameGrund)):
    for i in range (len(fileNameText)):
      cuttedFileName = os.path.basename(fileNameText[i]).split('.',1)[0]
      for j in range(0,len(fileNameGrund)):
        cuttedFileNameGTM =(fileNameGrund[j].split('/'))[4].split('.',1)[0]
        if (cuttedFileName == cuttedFileNameGTM):
          newGrundTrustMatrix.append(grundMatrix[j])
    return numpy.array(newGrundTrustMatrix)
  else:
    return grundMatrix

def comparematrix(folderName,coefficient =1.2):
  fileNames = cPickle.load(open(folderName+folderlsi + modellsi + '.filenames', 'rb'))
  SimilarityLSI = numpy.load(folderName + folderlsi+modellsi+'.npy')
  grundTrustMatrix = numpy.load(folderName + "gtm/AverageAnnotation.npy")
  filesGTM = numpy.load(folderName + "gtm/SceneNames.npy")
  lenTextinFiles = lenTextInFiles(folderName)
  grundTrustMatrix = transforMatrix(fileNames,filesGTM,grundTrustMatrix)
  recall = []
  precision = []
  for i in range(0,len(fileNames)):
    gtm=evaluateGTM(grundTrustMatrix[i],coefficient)
    sm=evaluateSM(SimilarityLSI[i],coefficient)
    similarity = numpy.intersect1d(gtm,sm)
    if len(gtm)!= 0 :
      recall.append(float(len(similarity))/float(len(gtm)))
    else :
      recall.append(0)
    if len(sm)!= 0 :
      precision.append(float(len(similarity))/float(len(sm)))
    else :
      precision.append(0)
    debugprint(gtm,sm,similarity,lenTextinFiles, recall[i],precision[i],fileNames[i],SimilarityLSI[i],grundTrustMatrix[i],filesGTM[i])

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


def evaluateSMRandom(row,coef):
  random_index = numpy.random.permutation(len(row))
  T_value = 5
  result =[]
  """
  for val in range(0,len(row)):
    T_value += row[val]
  """
  for i in range(0,int(T_value)):
    result.append(random_index[i])
  return numpy.array(result)

if __name__ == '__main__':

  if sys.argv[1] == "-compareMatrix":
    folderName = sys.argv[2]
    comparematrix(folderName)
