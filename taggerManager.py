# -*- coding: utf-8 -*-
'''Tagger MODULE'''

import nltk
import json
import tokensManager

from nltk.corpus import mac_morpho
from nltk.tag import UnigramTagger
from nltk.tag import DefaultTagger
from nltk.chunk import RegexpParser
from nltk.tree import *


def TaggerOnline(tokens):
	etiq1 = DefaultTagger('N')
	sentencas_treinadoras = mac_morpho.tagged_sents()[::]
	etiq2 = UnigramTagger(sentencas_treinadoras, backoff=etiq1)
	tagsTokens = etiq2.tag(tokens)
	return tagsTokens

def TaggerOffline(tokens):
	with open('mac_morpho_backup.json', 'r') as tags_macmorpho:
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

def TaggerComment(comment):
	tokens = tokensManager.GetTokens(comment, 0)
	tags = TaggerOffline(tokens)
	#tags = TaggerOnline(tokens)
	return tags

def TagsDict(tagsTokens):
	tags = {}
	tags[1] = []
	for tupleTag in tagsTokens:
		tags[1].append(tupleTag)

	return tags