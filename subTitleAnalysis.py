import re, os, glob, codecs, sys, numpy
from os.path import basename
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pysrt import SubRipFile
from nltk import PorterStemmer
import nltk.tokenize
from gensim import corpora, models, similarities
import gensim
from itertools import izip
import cPickle
import pydot
# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

reload(sys)
sys.setdefaultencoding("utf-8")

import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

stopList = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

def drawGraphFromSM2(SM, names, outFile):
	graph = pydot.Dot(graph_type='graph')

	# THRESHOLD SM:
	numberOfTotalConnections = numpy.sum(SM)

	#T = int(numberOfTotalConnections / 1500.0)
	T = 0.5;

	for i in range(SM.shape[0]):
		for j in range(SM.shape[0]):
			if SM[i,j] <= T:
				SM[i,j] = 0.0
			else:
				SM[i,j] = 1.0

	numOfConnections = numpy.sum(SM, axis = 0)
	fig = plt.figure(1)
	plot1 = plt.imshow(SM, origin='upper', cmap=cm.gray, interpolation='nearest')
	plt.show()

	numOfConnections = 9*numOfConnections / max(numOfConnections)

	for i,f in enumerate(names):	
		if numpy.sum(SM[i,:])>0:
			fillColorCurrent = "{0:d}".format(int(numpy.ceil(numOfConnections[i])))
			print fillColorCurrent
			# NOTE: SEE http://www.graphviz.org/doc/info/colors.html for color schemes
			node = pydot.Node(f, style="filled", fontsize="8", shape="egg", fillcolor=fillColorCurrent, colorscheme = "reds9")
			graph.add_node(node)
			
	for i in range(len(names)):
		for j in range(len(names)):
			if i<j:
				if SM[i][j] > 0:
					#gr.add_edge((names[i], names[j]))				
					edge = pydot.Edge(names[i], names[j])	
					graph.add_edge(edge)
	graph.write_png(outFile)


def readTextFile(fileName):
	print fileName
	with open (fileName, "r") as myfile:
		data=myfile.read().replace('\n', ' ').decode('utf-8')
	return data

def readTextDir(dirName):
	texts = []
	fileNames = []
	for subdir, dirs, files in os.walk(dirName):
		files.sort()
		for f in files:  							# for each file in the given directory:
			fi = dirName + os.sep + f					# update the list of files analyzed:
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
		tokenizer = nltk.tokenize.RegexpTokenizer('[\d\.]+|\w+|\$[\d\.]+')		# initialize tokenizer
		tokens = tokenizer.tokenize(text.lower())
		for word in tokens:
			if len(word)>1 and word not in stopList:
				curT.append(PorterStemmer().stem_word((word)))
		newTexts.append(curT)
	# TODO:
	# 2_GRAMS IN gensim????
	return newTexts

def buildSearchIndex(folderName, modelName):
	T, fileNames = readTextDir(folderName)
	T2 = postProcessTexts(T)
	print T2
	dictionary = corpora.Dictionary(T2)
	corpus = [dictionary.doc2bow(text) for text in T2]

	tfidf = gensim.models.tfidfmodel.TfidfModel(corpus)

	lsi = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=500)
	indexLSI = similarities.MatrixSimilarity(lsi[tfidf[corpus]])
	index    = similarities.MatrixSimilarity(tfidf[corpus])

	dictionary.save(modelName + '.dict')
	corpora.MmCorpus.serialize(modelName + '.corpus', corpus)
	index.save(modelName + '.index')
	indexLSI.save(modelName + '.indexLSI')
	cPickle.dump(fileNames, open(modelName + '.filenames', 'wb'))	
	tfidf.save(modelName + '.tfidf')
	lsi.save(modelName + '.lsi')

def query(queryStr, index, dictionary, fileNames, tfidf, MAX_RESULTS):
	queryStr = postProcessTexts([queryStr])
	vec_bow = tfidf[dictionary.doc2bow(queryStr[0])]
	sims = index[vec_bow]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	for i in range(len(sims)):
		if sims[i][1]<0.20 or i>MAX_RESULTS :
			break
		print fileNames[sims[i][0]], readTextFile(fileNames[sims[i][0]]), sims[i][1]

def srtToTxt(dirName):
	iDoc = 0
	for infile in glob.glob( os.path.join(dirName, '*.srt') ):
		#infile2 = infile.replace(".srt","_n.srt")
		#os.system("iconv --from-code=ISO-8859-1 --to-code=UTF-8 \"" + infile + "\" > \"" + infile2 + "\"")
		print infile
		subs = SubRipFile.open(infile)	
		outfile = infile[:-4]
		f = codecs.open(outfile, "w", "utf-8")
		# f = open(outfile, 'w')
		for i in range(len(subs)):
			f.write(subs[i].text)
		f.close()
		iDoc = iDoc + 1

def queryLSI(queryStr, index, lsi, dictionary, fileNames, tfidf, MAX_RESULTS):
	queryStr = postProcessTexts([queryStr])
#	vec_bow = dictionary.doc2bow(queryStr[0])
	vec_bow = tfidf[dictionary.doc2bow(queryStr[0])]
	print vec_bow
	vec_lsi = lsi[vec_bow] # convert the query to LSI space
	sims = index[vec_lsi]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	for i in range(len(sims)):
		if sims[i][1]<0.10 or i>MAX_RESULTS:
			break
		#print fileNames[sims[i][0]], readTextFile(fileNames[sims[i][0]]), sims[i][1]
		print fileNames[sims[i][0]]

def splitSingle(fileName, newFileName, Hs, Ms, Ss, He, Me, Se):
	subs = SubRipFile.open(fileName)
	A = {'hour': Hs, 'minutes': Ms, 'seconds': Ss}
	B = {'hour': He, 'minutes': Me, 'seconds': Se}
 	part = subs.slice(starts_after={'hours': Hs, 'minutes': Ms, 'seconds': Ss}, ends_before={'hours': He, 'minutes': Me, 'seconds': Se})
	part.shift(hours = -Hs, minutes=-Ms, seconds=-Ss)
	part.save(newFileName)

# TODO:
# run os.system() with ffmpeg
# ffmpeg -i <originalMovieFileName> -ss 100 -t 50 <segmentFileName>
# 100 and 50 are the starting points (in seconds) and the duration (in seconds) respectively


if __name__ == '__main__':

	if (len(sys.argv) > 2):
		if sys.argv[1]=="-srt2txt":
			dirName = sys.argv[2]
			srtToTxt(dirName)
		if sys.argv[1]=="-train":
			buildSearchIndex(sys.argv[2], sys.argv[3])
		if sys.argv[1]=="-similarity":
			modelName = sys.argv[2]
			dictionary = corpora.Dictionary.load(modelName + '.dict')
			index = similarities.MatrixSimilarity.load(modelName + '.index')
			indexLSI = similarities.MatrixSimilarity.load(modelName + '.indexLSI')
			fileNames = cPickle.load(open(modelName + '.filenames', 'rb'))			
			tfidf = gensim.models.tfidfmodel.TfidfModel.load(modelName + '.tfidf');	
			lsi = gensim.models.lsimodel.LsiModel.load(modelName + '.lsi')
			topics = lsi.show_topics()
	
			topicsList = []	
			names = []
			Similarity = numpy.zeros((len(index), len(index)))
			for i,s in enumerate(index):
				curArray = numpy.array(s);
				curArray[i] = 0.0;
				Similarity[i,:] = curArray / numpy.max(curArray)
				names.append(basename(fileNames[i]))
			print Similarity
			drawGraphFromSM2(Similarity, names, sys.argv[3])
			#for x in topics:
			#	A = [j.split("*")[1].strip('"') for j in [i for i in x.strip().split(" + ")]]
			#	B = [float(j.split("*")[0]) for j in [i for i in x.strip().split(" + ")]]
			#	D = dict()
			#	for i in range(len(A)):
			#		D[A[i]] = B[i] 
			#	topicsList.append(D)
				

			



