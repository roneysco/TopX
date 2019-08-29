# -*- coding: utf-8 -*-
'''Tokens MODULE'''

import nltk

from nltk.tokenize import RegexpTokenizer

def GetTokens(textOverall, flag):
	if flag == 0:
		tokens = nltk.word_tokenize(textOverall.lower())
		#newTokens = ReplacePrepositions(tokens)
		return tokens
	if flag == 1:
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(textOverall.lower())
		return tokens