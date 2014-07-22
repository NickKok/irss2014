import sys
import cPickle
import helpfunction
import os
from nltk import PorterStemmer
import nltk.tokenize
from gensim import corpora, models, similarities
import gensim
from os.path import basename
import tf_idf
import numpy, csv


reload(sys)
sys.setdefaultencoding("utf-8")

import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

modellsi = "movielsi"
folderlsi = "lsi/"


stopList = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
            "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
            "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as",
            "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
            "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by",
            "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do",
            "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty",
            "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few",
            "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found",
            "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
            "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
            "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it",
            "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
            "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my",
            "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none",
            "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
            "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part",
            "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
            "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
            "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
            "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter",
            "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those",
            "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward",
            "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was",
            "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas",
            "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever",
            "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your",
            "yours", "yourself", "yourselves", "the"]


def readTextFile(fileName):
  #print fileName
  with open(fileName, "r") as myfile:
    data = myfile.read().replace('\n', ' ').decode('utf-8')
  return data


def readTextDir(dirName):
  texts = []
  fileNames = []
  for subdir, dirs, files in os.walk(dirName):
    files.sort()
    for f in files:  # for each file in the given directory:
      if f.endswith(".txt"):
        fi = dirName + os.sep + f  # update the list of files analyzed:
        fileNames.append(fi)
        texts.append(readTextFile(fi))

  return texts, fileNames


def readTextDirWithBounds(dirName):
  texts = []
  fileNames = []
  for subdir, dirs, files in os.walk(dirName):
    files.sort()
    for f in files:  # for each file in the given directory:
      if f.endswith(".txt"):
        with open(dirName + os.sep + f, "r") as testfile:
          num_lines = sum(1 for line in testfile)
        if num_lines > 3:
          fi = dirName + os.sep + f  # update the list of files analyzed:
          fileNames.append(fi)
          texts.append(readTextFile(fi))

  return texts, fileNames


def postProcessTexts(texts):
  # tokenization
  # stop-word removal
  # stemming
  newTexts = []
  for text in texts:
    curT = []
    tokenizer = nltk.tokenize.RegexpTokenizer('[\d\.]+|\w+|\$[\d\.]+')  # initialize tokenizer
    tokens = tokenizer.tokenize(text.lower())
    for word in tokens:
      if len(word) > 1 and word not in stopList:
        curT.append(PorterStemmer().stem_word((word)))
    newTexts.append(curT)
  return newTexts


def LSI(T2, folderName, modelName, fileNames):
  folderName = folderName + folderlsi
  helpfunction.ensure_dir(folderName)
  dictionary = corpora.Dictionary(T2)
  corpus = [dictionary.doc2bow(text) for text in T2]
  corpora.MmCorpus.serialize(folderName + modelName + '.mm', corpus)
  corpus = corpora.MmCorpus(folderName + modelName + '.mm')
  tfidf = models.TfidfModel(corpus)

  lsi = models.LsiModel(tfidf[corpus], num_topics=len(fileNames), id2word=dictionary, chunksize=100, onepass=True,
                        power_iters=2, extra_samples=100)
  indexLSI = similarities.MatrixSimilarity(lsi[tfidf[corpus]])
  index = similarities.MatrixSimilarity(tfidf[corpus])

  dictionary.save(folderName + modelName + '.dict')
  index.save(folderName + modelName + '.index')
  indexLSI.save(folderName + modelName + '.indexLSI')
  cPickle.dump(fileNames, open(folderName + modelName + '.filenames', 'wb'))
  tfidf.save(folderName + modelName + '.tfidf')
  lsi.save(folderName + modelName + '.lsi')

def similarityLSI(folderName,text):
  folderName = folderName + folderlsi
  modelName = modellsi
  dictionary = corpora.Dictionary.load(folderName + modelName + '.dict')
  index = similarities.MatrixSimilarity.load(folderName + modelName + '.index')
  indexLSI = similarities.MatrixSimilarity.load(folderName + modelName + '.indexLSI')
  fileNames = cPickle.load(open(folderName + modelName + '.filenames', 'rb'))
  tfidf = gensim.models.tfidfmodel.TfidfModel.load(folderName + modelName + '.tfidf');
  lsi = gensim.models.lsimodel.LsiModel.load(folderName + modelName + '.lsi')

  names = []
  Similarity = numpy.zeros((len(index), len(index)))
  for i, s in enumerate(index):
    curArray = numpy.array(s);
    curArray[i] = 0.0;
    #Similarity[i, :] = curArray / numpy.max(curArray)
    Similarity[i, :] = curArray
    names.append(basename(fileNames[i]))

  with open(folderName + modellsi + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in Similarity.tolist()]
  numpy.save(folderName + modellsi + '.npy', Similarity)
  """
  tfidf = tf_idf.tfidf()
  for i in range(0,len(fileNames)):
    tfidf.addDocument(fileNames[i],text[i])

  for j in range(0,len(fileNames)):
    print str((tfidf.similarities(text[7]))[j][1]) + " ----- " + str((Similarity[7])[j])

  print fileNames[7]
  """
  
def buildSearchIndex(folderName):
  T, fileNames = readTextDir(folderName)
  T2 = postProcessTexts(T)
  LSI(T2, folderName, modellsi, fileNames)
  similarityLSI(folderName,T2)

if __name__ == '__main__':

  if sys.argv[1] == "-train":
    buildSearchIndex(sys.argv[2])

  if sys.argv[1] == "-similarity":
    folderName = sys.argv[2]
    similarityLSI(folderName)
