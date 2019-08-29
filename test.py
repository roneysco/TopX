# -*- coding: utf-8 -*-
'''test file'''

import taggerManager
import tokensManager
import correctnessManager
import patternsManager

text = "o hotel é muito bom, bela vista da varanda, a localização é perfeita e o estacionamento é caro e sujo."

tokens = tokensManager.GetTokens(text, 0)
#print(tokens)
print("-----------------------------------------------------")
tagsTokens = taggerManager.TaggerComment(text)
#print(tagsTokens)
print("-----------------------------------------------------")
tags = taggerManager.TagsDict(tagsTokens)
#print(tags)
print("-----------------------------------------------------")
patt1, patt3, patt4, patt5 = patternsManager.GetPatternsDict(tags)
print(patt1)
print(patt3)
print(patt4)
print(patt5)
print("-----------------------------------------------------")
dictF, pol = patternsManager.GetDictFeatures(tags)
print(dictF)
print(pol)
print("-----------------------------------------------------")
acc = correctnessManager.Correctness(text)
print("Accuracy: ", acc)


