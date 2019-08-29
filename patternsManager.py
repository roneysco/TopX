# -*- coding: utf-8 -*-
'''Patterns MODULE'''

import nltk
import MySQLdb as mdb

from nltk.tree import *
from nltk.chunk import RegexpParser

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

#Return the pattern tree which will be analysed to extract patterns
def GetPatternsTree(tagsList, pattern, patternName):
	gramaticalAnalyse = RegexpParser(pattern)
	tree = gramaticalAnalyse.parse(tagsList)
	patt = ExtractPhrases(tree, patternName)
	return patt

def ExistCaract(word, flag):
	db = mdb.connect('localhost', 'root', 'root', 'comments_booking')
	db.set_character_set("utf8")
	
	cur = db.cursor()
	if flag == 0:
		cur.execute("SELECT caract FROM caractlist WHERE caract = '"+word+"'")
	if flag == 1:
		cur.execute("SELECT caract FROM caractlist WHERE stem = '"+word+"'")

	return cur.fetchone()

def InsertMultiwordNewAdjective(dictAdjectives, name, adj):
	stemmer = nltk.stem.RSLPStemmer()
	first = stemmer.stem(name.split()[0])
	last = stemmer.stem(name.split()[2])

	caract = ExistCaract(name, 0)
	first = ExistCaract(first, 1)
	last = ExistCaract(last, 1)

	if caract:
		dictAdjectives = InsertNewAdjective(dictAdjectives, caract, adj)
	elif first and last:
		dictAdjectives = InsertNewAdjective(dictAdjectives, first, adj)
		dictAdjectives = InsertNewAdjective(dictAdjectives, last, adj)
	elif first:
		dictAdjectives = InsertNewAdjective(dictAdjectives, first, adj)
	elif last:
		dictAdjectives = InsertNewAdjective(dictAdjectives, last, adj)
	else:
		pass

	return dictAdjectives

#Insert an adjective in dictAdjectives dictionary.
def InsertNewAdjective(dictAdjectives, caract, adj):
	if caract in dictAdjectives.keys():
		dictAdjectives[caract][0].append(adj)
	else:
		dictAdjectives[caract] = [[],[]]
		dictAdjectives[caract][0].append(adj)

	return dictAdjectives

#Sentiment Lexicon. Return the polarity of a given adjective.
def Sentilex(word):
	db = mdb.connect('localhost', 'root', 'root', 'comments_booking')
	db.set_character_set("utf8")

	cur = db.cursor()
	cur.execute("SELECT pol FROM sentilex_flex_pt02 WHERE palavra LIKE "+"'"+word+"%'")
	pol = cur.fetchone()
	if pol:
		polSent = pol[0].split('=')[1]
		return int(polSent)
	else:
		polSent = 0
		return int(polSent)

#Returns the weight of an adverb according a weight table [Sousa et al. 2015, modified]
def AdverbWeight(adv):
	db = mdb.connect('localhost', 'root', 'root', 'comments_booking')
	db.set_character_set("utf8")

	try:
		cur = db.cursor()
		cur.execute("SELECT pol FROM adverblist WHERE adverb LIKE "+"'"+adv+"%'")
		pol = cur.fetchone()
		return pol[0]
	except TypeError:
		return 0

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

def GetPatternsDict(tags):
	patt1Dict = {}
	patt3Dict = {}
	patt4Dict = {}
	patt5Dict = {}

	pattern1 = r"""PADRAO1: {(<N>|<NPROP>|((<N>|<NPROP>)(<PREP>|<PREP><ART>)(<N>|<NPROP>)))<ADV>?(<V>|<VAUX>)?<ADV>?<ADJ>}"""
	pattern3 = r"""PADRAO3: {(<N>|<NPROP>|(<NPROP><PREP><NPROP>)|(<N><PREP><NPROP>))<V>?(<ADV>?<ADJ><,>)*<ADV>?<ADJ><KC><ADV>?<ADJ>}"""
	pattern4 = r"""PADRAO4: {<ADJ>(<N>|<NPROP>|((<N>|<NPROP>)(<PREP>|<PREP><ART>)(<N>|<NPROP>)))}"""
	pattern5 = r"""PADRAO5: {<ADV><V><PREP>(<N>|<NPROP>|((<N>|<NPROP>)<PREP>(<N>|<NPROP>)))(<KC><PREP>(<N>|<NPROP>|((<N>|<NPROP>)<PREP>(<N>|<NPROP>))))*}"""	

	patt1 = GetPatternsTree(tags[1], pattern1, "PADRAO1")
	patt1Dict[1] = []
	for p1 in patt1:
		patt1Dict[1].append(p1)

	patt3 = GetPatternsTree(tags[1], pattern3, "PADRAO3") 
	patt3Dict[1] = []
	for p3 in patt3:
		patt3Dict[1].append(p3)

	patt4 = GetPatternsTree(tags[1], pattern4, "PADRAO4") 
	patt4Dict[1] = []
	for p4 in patt4:
		patt3Dict[1].append(p4)

	patt5 = GetPatternsTree(tags[1], pattern5, "PADRAO5")
	patt5Dict[1] = []
	for p5 in patt5:
		patt5Dict[1].append(p5)

	return (patt1Dict, patt3Dict, patt4Dict, patt5Dict)

def GetDictFeatures(tags):
	dictAdjectives = {}
	listAdj=[]
	stemmer = nltk.stem.RSLPStemmer()
	polarityComment=0

	patt1Dict, patt3Dict, patt4Dict, patt5Dict = GetPatternsDict(tags)

	#Pattern 1
	for tuplePattern1 in patt1Dict[1]:
		name1 = GetName(tuplePattern1)
		adj1 = tuplePattern1[tuplePattern1.index('ADJ')-1]
		try:
			if tuplePattern1[tuplePattern1.index('ADV')]:
				adj1 = tuplePattern1[tuplePattern1.index('ADV')-1]+' '+adj1
		except ValueError:
			pass

		if ' ' in name1:
			dictAdjectives = InsertMultiwordNewAdjective(dictAdjectives, name1, adj1)
		else:
			caract1 = ExistCaract(stemmer.stem(name1), 1)
			if caract1:
				dictAdjectives = InsertNewAdjective(dictAdjectives, name1, adj1)

		if ' ' in adj1:
			pol1 = GetOverallPolarity(adj1)
			polarityComment+=pol1
		else:
			pol1 = Sentilex(adj1)
			polarityComment+=pol1

	for tuplePattern5 in patt5Dict[1]:
		#expr means ADV + VERB
		expr = tuplePattern5[tuplePattern5.index('ADV')-1]+' '+tuplePattern5[tuplePattern5.index('V')-1]
		indexes = [i for i,val in enumerate(tuplePattern5) if val == 'N']
		for k in indexes:
			try:
				name5 = tuplePattern5[k-1]
				if tuplePattern5[tuplePattern5.index(name5)+3] == 'PREP' and tuplePattern5[tuplePattern5.index(name5)+5] == 'N':
					name5 = name5+' '+tuplePattern5[tuplePattern5.index(name5)+2]+' '+tuplePattern5[tuplePattern5.index(name5)+4]
					for k1 in indexes:
						name5aux = tuplePattern5[k1-1]
						n2 = tuplePattern5[k-1]
						if n2 == name5aux:
							indexes.remove(k1)
			except IndexError:
				name5 = tuplePattern5[k-1]

		if ' ' in name5:
			InsertMultiwordNewAdjective(dictAdjectives, name5, expr)
		else:
			caract5 = ExistCaract(stemmer.stem(name5), 1)
			if caract5:
				InsertNewAdjective(dictAdjectives, caract5, expr)

		pol5 = GetOverallPolarity(expr)
		polarityComment+=pol5

	return (dictAdjectives, polarityComment)