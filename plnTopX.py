import nltk
from nltk.corpus import mac_morpho
from nltk.tag import UnigramTagger
from nltk.tag import DefaultTagger
from nltk.chunk import RegexpParser
from nltk.tree import *
from nltk.tokenize import RegexpTokenizer

from decimal import Decimal

from .models import Adverblist, Caractlist, Comments, Dictwords, SentilexFlexPt02

def GetTokens(textOverall, flag):
	if flag == 0:
		tokens = nltk.word_tokenize(textOverall.lower())
		newTokens = ReplacePrepositions(tokens)
		return newTokens
	if flag == 1:
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(textOverall.lower())
		return tokens


#Replace prepositions which tagger doesn't recognize as 'da', 'do', 'das', 'dos'
def ReplacePrepositions(tokens):
	for token in tokens:
		if token == 'da':
			tokens.insert(tokens.index(token), 'de')
			tokens.insert(tokens.index(token), 'a')
			tokens.remove('da')
		if token == 'do':
			tokens.insert(tokens.index(token), 'de')
			tokens.insert(tokens.index(token), 'o')
			tokens.remove('do')
		if token == 'das':
			tokens.insert(tokens.index(token), 'de')
			tokens.insert(tokens.index(token), 'as')
			tokens.remove('das')
		if token == 'dos':
			tokens.insert(tokens.index(token), 'de')
			tokens.insert(tokens.index(token), 'os')
			tokens.remove('dos')
	return tokens

#Extract patterns which was previously definited.
def ExtractPhrases(myTree, phrase):
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
			list_of_phrases = ExtractPhrases(child, phrase)
			if (len(list_of_phrases) > 0):
				myPhrases.extend(list_of_phrases)
	return myPhrases

#Return the pattern tree which will be analysed to extract patterns
def GetPatternsTree(tagsList, pattern, patternName):
	gramaticalAnalyse = RegexpParser(pattern)
	tree = gramaticalAnalyse.parse(tagsList)
	patt = ExtractPhrases(tree, patternName)
	return patt

def Tagger():
	#Tagger
	etiq1 = DefaultTagger('N')
	sentencas_treinadoras = mac_morpho.tagged_sents()[::]
	etiq2 = UnigramTagger(sentencas_treinadoras, backoff=etiq1)
	return etiq2

def Correctness(tokens):
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

#Return the feature inside tuple, using the pattern definited.
def GetName(t):
	try:
		name = t[t.index('N')-1]
	except ValueError:
		name = t[t.index('NPROP')-1]
	try:
		if t[t.index('PREP')] and t[t.index('ART')]:
			if PlacePrepositions(t[t.index('PREP')-1], t[t.index('ART')-1]) == '':
				pass
			else:
				name = t[t.index('N')-1]+' '+PlacePrepositions(t[t.index('PREP')-1], t[t.index('ART')-1])+' '+t[t.index('ART')+1]
	except ValueError:
		pass

	return name

#Place the preposition to right writing.
def PlacePrepositions(prep, art):
	if prep == 'de':
		if art == 'a':
			return 'da'
		elif art == 'o':
			return 'do'
		elif art == 'as':
			return 'das'
		elif art == 'os':
			return 'dos'
		else:
			return ''
	else:
		return ''

'''Insert an adjective from a multiword. A multiword has two parts to analyse. Depending of context, the adjective can be stored in first or last split of multiword.
So, if the multiword is an feature, the adjective will be stored in a key with its name (e.g. 'café da manhã');
If the first split of multiword is a feature and the last is not, the adjective will be stored in a key with first split name (e.g. 'vista do mar')
If the last split of multiword is a feature and the first is not, the adjective will be stored in a key with last split name (e.g. 'colchão da cama')
But if both splits of multiword are features, the adjective will be stored in both keys (e.g. 'localização do hotel').'''
def InsertMultiwordNewAdjective(dictAdjectives, name, adj):
	stemmer = nltk.stem.RSLPStemmer()
	first = stemmer.stem(name.split()[0])
	last = stemmer.stem(name.split()[2])

	caract = ExistCaract(name, 0)
	first = ExistCaract(first, 1)
	last = ExistCaract(last, 1)

	if caract:
		InsertNewAdjective(db, dictAdjectives, caract, adj)
	elif first and last:
		InsertNewAdjective(db, dictAdjectives, first, adj)
		InsertNewAdjective(db, dictAdjectives, last, adj)
	elif first:
		InsertNewAdjective(db, dictAdjectives, first, adj)
	elif last:
		InsertNewAdjective(db, dictAdjectives, last, adj)
	else:
		pass

#Insert an adjective in dictAdjectives dictionary.
def InsertNewAdjective(dictAdjectives, caract, adj):
	if caract[0] in dictAdjectives.keys():
		dictAdjectives[caract[0]][0].append(adj)
	else:
		dictAdjectives[caract[0]] = [[],[]]
		dictAdjectives[caract[0]][0].append(adj)

#Return, if exists, one of the feature stored in database.
def ExistCaract(word, flag):
	if flag == 0:
		#cur.execute("SELECT caract FROM caractlist WHERE caract = '"+word+"'")
		ret = Caractlist.objects.filter(caract='"+word+"')
		if ret:
			retstr = str(ret).split()[0]
			return retstr
		else:
			return ret
	if flag == 1:
		#cur.execute("SELECT caract FROM caractlist WHERE stem = '"+word+"'")
		ret = Caractlist.objects.filter(stem='"+word+"')
		if ret:
			retstr = str(ret).split()[1]
			return retstr
		else:
			return ret

#Used when get ADV+ADJ. adj = ADV+ADJ
def GetOverallPolarity(adj):
	adv = adj.split()[0]
	adj = adj.split()[1]
	polAdv = AdverbWeight(adv)
	polAdj = Sentilex(adj)
	if polAdj < 0:
		polAdv = polAdv*(-1)
		polExpr = polAdv + polAdj
		return polExpr
	else:
		if polAdv < 0:
			polExpr = polAdv + polAdj
			polExpr = polExpr*(-1) #inversor
			return polExpr
		else:
			polExpr = polAdv + polAdj
			return polExpr

#Returns the weight of an adverb according a weight table [Sousa et al. 2015, modified]
def AdverbWeight(adv):
	#cur.execute("SELECT pol FROM adverblist WHERE adverb LIKE "+"'"+adv+"%'")
	ret = Adverblist.objects.filter(adverb__startswith='"+adv+"')
	if ret:
		retstr = str(ret).split()[1]
		retstr = ret.pol
		return Decimal(retstr)
	else:
		return 0

#Sentiment Lexicon. Return the polarity of a given adjective.
def Sentilex(word):
	#cur.execute("SELECT pol FROM sentilex_flex_pt02 WHERE palavra LIKE "+"'"+word+"%'")
	pol = SentilexFlexPt02.objects.filter(palavra__contains='"+word+"')
	if pol:
		polSent = str(pol).split('=')[1]
		return int(polSent)
	else:
		polSent = 0
		return int(polSent)

