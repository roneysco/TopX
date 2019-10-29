import taggerManager
import tokensManager
import correctnessManager
import patternsManager
import annManager

# Text example. I think that you will use a lot of this, being from a SQL database (in my case) or file.
text = "o hotel é muito bom, bela vista da varanda, a localização é perfeita e o estacionamento é caro e sujo."

# list with ALL features input, which will be used in the MLP.
input_text = []

# list with the value of the text (insufficient - 0, sufficient - 1, good - 2 or excelent - 3), for training purposes
output_text = []

# list with the text features.
text_features = []

# author reputation
author = 1
print("Author Reputation:", author)
text_features.append(author)

# number of tuples
tokens = tokensManager.GetTokens(text, 0)
print(tokens)
tagsTokens = taggerManager.TaggerComment(text)
print(tagsTokens)
tags = taggerManager.TagsDict(tagsTokens)
print(tags)
patt1, patt3, patt4, patt5 = patternsManager.GetPatternsDict(tags)

number_tuples = len(patt1[1])+len(patt3[1])+len(patt3[1])+len(patt3[1])
print("Number of Tuples:", number_tuples)
text_features.append(number_tuples)

# correctness
correctness = correctnessManager.Correctness(text)
print("Correctness: ", correctness)
text_features.append(correctness)

# in the end, add this list in the input text list, to the training purposes.
input_text.append(text_features)

output_text = [2]

# bonus: polarity of the text, using the Sentilex. To values greater than 0, the comment is positive; otherside, is negative.
#dictF, pol = patternsManager.GetDictFeatures(tags)

print("The features vector (input) is", input_text, "and the expected value (output) is", output_text)

# So, when you finish to extract the features from your database, just apply the features vector and the expected vector to the MLP classifier
# You have to choose what topology you want to use. 1 for topology 1 and 2 for topology 2
# The return is a printed classification report with precision, recall and f-measure. If you wish more information, please see the scikit-learn documentation
# IMPORTANT: This test will not work because we have only one text example. Please, extract the features for other texts and run the code!!
annManager.AnnTraining(input_text+input_text, output_text+output_text, 2)


