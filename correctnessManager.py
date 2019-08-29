# -*- coding: utf-8 -*-
'''Correctness MODULE'''

import nltk
import tokensManager
#from topXProject.core.modules import tokensManager

from nltk.tokenize import RegexpTokenizer


def Correctness(comment):
	tokens = tokensManager.GetTokens(comment, 1)

	corr = 0		
	with open('UserDictionary_pt.txt', encoding="utf8") as list1:
		dict1 = list1.read().split("\n")
		for w in tokens:
			if w in dict1:
				corr+=1
			else:
				pass
		acc = (corr/len(tokens))*100
		return acc