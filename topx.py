from django.db.models.base import ObjectDoesNotExist
import json
import matplotlib.pyplot as pyplot
from topXProject.core.models import Adverblist, Caractlist, SentilexFlexPt02
import nltk
from nltk.chunk import RegexpParser
from nltk.tree import *
from nltk.tokenize import RegexpTokenizer
import random

#The list of adjectives' polarity will be stored here. Each polarity adjective will be saved in second list's values inside each key. 
def adjectives(dictAdjectives):
	for key in dictAdjectives.keys():
		for adj in dictAdjectives[key][0]:
			if ' ' in adj:
				polExpr = getOverallPolarity(adj)
				dictAdjectives[key][1].append(polExpr)
			else:
				pol = sentilex(adj)
				dictAdjectives[key][1].append(pol)

	res = [[],[],[]]
	for caract, adjPol in dictAdjectives.items():
		if sum(adjPol[1]) > 0:
			#print(caract+" is POSITIVE with polarity "+str(sum(adjPol[1])))
			res[0].append(caract)
		elif sum(adjPol[1]) < 0:
			#print(caract+" is NEGATIVE with polarity "+str(sum(adjPol[1])))
			res[1].append(caract)
		else:
			#print(caract+" is NEUTRAL with polarity "+str(sum(adjPol[1])))
			res[2].append(caract)

	return res

def adjectivesGraphic(result2):
	numbers = [len(result2[0]), len(result2[2]), len(result2[1])]
	labelsList = ['Positiva', 'Neutra', 'Negativa']
	expl = (0, 0.05, 0)
	pyplot.pie(numbers, explode=expl, labels=labelsList, autopct='%1.1f%%', shadow=True)
	pyplot.title('Polaridade das características')
	pyplot.legend()

	n = random.randint(0,100000)
	name = "graphic"+str(n)+".png"

	pyplot.savefig('/home/easiiserver/www/topx/static/img/'+name)

	return name

#Returns the weight of an adverb according a weight table [Sousa et al. 2015, modified]
def adverbWeight(adv):
	#cur.execute("SELECT pol FROM adverblist WHERE adverb LIKE "+"'"+adv+"%'")
	try:
		ret = Adverblist.objects.get(adverb__startswith=adv)
		retstr = ret.pol
		return retstr
	except ObjectDoesNotExist:
		return 0

def correctness(tokens):
	corr = 0		
	with open('/home/easiiserver/www/topx/project/topXProject/core/UserDictionary_pt.txt', encoding="utf8") as list1:
		dict1 = list1.read().split("\n")
		for w in tokens:
			if w in dict1:
				corr+=1
			else:
				pass
		acc = (corr/len(tokens))*100
		return acc

#Return, if exists, one of the feature stored in database.
def existCaract(word, flag):
	if flag == 0:
		#cur.execute("SELECT caract FROM caractlist WHERE caract = '"+word+"'")
		try:
			ret = Caractlist.objects.get(caract=word)
			retstr = ret.caract
			return retstr
		except ObjectDoesNotExist:
			return None
	if flag == 1:
		#cur.execute("SELECT caract FROM caractlist WHERE stem = '"+word+"'")
		try:
			ret = Caractlist.objects.get(stem=word)
			retstr = ret.caract
			return retstr
		except ObjectDoesNotExist:
			return None

#Extract patterns which was previously definited.
def extractPhrases(myTree, phrase):
	myPhrases = []
	if (myTree.label() == phrase):
		treeTmp = myTree.copy(True)
		word=""
		for w in treeTmp.leaves():
			if (len(word)==0):
				word = w
			else:
				word = word+w
		myPhrases.append(word)
	for child in myTree:
		if (type(child) is Tree):
			list_of_phrases = extractPhrases(child, phrase)
			if (len(list_of_phrases) > 0):
				myPhrases.extend(list_of_phrases)
	return myPhrases

#Return the feature inside tuple, using the pattern definited.
def getName(t):
	try:
		name = t[t.index('N')-1]
	except ValueError:
		name = t[t.index('NPROP')-1]
	try:
		if t[t.index('PREP')]:
			name = t[t.index('N')-1]+' '+t[t.index('PREP')-1]+' '+t[t.index('PREP')+1]
	except ValueError:
		pass

	return name

#Used when get ADV+ADJ. adj = ADV+ADJ
def getOverallPolarity(adj):
	adv = adj.split()[0]
	adj = adj.split()[1]
	polAdv = adverbWeight(adv)
	polAdj = sentilex(adj)
	if polAdj < 0:
		polAdv = polAdv*(-1)
		polExpr = polAdv + polAdj
		return polExpr
	else:
		if polAdv == -1:
			if polAdj == 0:
				polExpr = polAdv
				return polExpr
			else:
				pass
		if polAdv < 0:
			polExpr = polAdv + polAdj
			polExpr = polExpr*(-1) #inversor
			return polExpr
		else:
			polExpr = polAdv + polAdj
			return polExpr

#Return the pattern tree which will be analysed to extract patterns
def getPatternsTree(tagsList, pattern, patternName):
	gramaticalAnalyse = RegexpParser(pattern)
	tree = gramaticalAnalyse.parse(tagsList)
	patt = extractPhrases(tree, patternName)
	return patt

def getTokens(textOverall, flag):
	if flag == 0:
		tokens = nltk.word_tokenize(textOverall.lower())
		#newTokens = ReplacePrepositions(tokens)
		return tokens
	if flag == 1:
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(textOverall.lower())
		return tokens

'''Insert an adjective from a multiword. A multiword has two parts to analyse. Depending of context, the adjective can be stored in first or last split of multiword.
So, if the multiword is an feature, the adjective will be stored in a key with its name (e.g. 'café da manhã');
If the first split of multiword is a feature and the last is not, the adjective will be stored in a key with first split name (e.g. 'vista do mar')
If the last split of multiword is a feature and the first is not, the adjective will be stored in a key with last split name (e.g. 'colchão da cama')
But if both splits of multiword are features, the adjective will be stored in both keys (e.g. 'localização do hotel').'''
def insertMultiwordNewAdjective(dictAdjectives, name, adj):
	stemmer = nltk.stem.RSLPStemmer()
	first = stemmer.stem(name.split()[0])
	last = stemmer.stem(name.split()[2])

	caract = existCaract(name, 0)
	first = existCaract(first, 1)
	last = existCaract(last, 1)

	if caract:
		insertNewAdjective(dictAdjectives, caract, adj)
	elif first and last:
		insertNewAdjective(dictAdjectives, first, adj)
		insertNewAdjective(dictAdjectives, last, adj)
	elif first:
		insertNewAdjective(dictAdjectives, first, adj)
	elif last:
		insertNewAdjective(dictAdjectives, last, adj)
	else:
		pass

#Insert an adjective in dictAdjectives dictionary.
def insertNewAdjective(dictAdjectives, caract, adj):
	if caract in dictAdjectives.keys():
		dictAdjectives[caract][0].append(adj)
	else:
		dictAdjectives[caract] = [[],[]]
		dictAdjectives[caract][0].append(adj)

#Sentiment Lexicon. Return the polarity of a given adjective.
def sentilex(word):
	#cur.execute("SELECT pol FROM sentilex_flex_pt02 WHERE palavra LIKE "+"'"+word+"%'")
	try:
		ret = SentilexFlexPt02.objects.filter(palavra__startswith=word)[0:1].get()
		polSent = ret.pol.split('=')[1]
		return int(polSent)
	except ObjectDoesNotExist:
		return 0

def tagger(tokens):
	with open('/home/easiiserver/www/topx/project/topXProject/core/mac_morpho_backup.json', 'r') as tags_macmorpho:
		etiq2 = json.load(tags_macmorpho)

		tagsT = []
		for token in tokens:
			if token in etiq2.keys():
				t = (token, etiq2[token])
				tagsT.append(t)
			else:
				t = (token, 'N')
				tagsT.append(t)

		return tagsT