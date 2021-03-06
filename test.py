import taggerManager
import tokensManager
import correctnessManager
import patternsManager
import annManager


# list with ALL features input, which will be used in the MLP.
input_text = []

# list with the value of the text (insufficient - 0, sufficient - 1, good - 2 or excelent - 3), for training purposes
output_text = []

# from here, you must have load your texts, to extract their features. It can be by SQL file, txt files, csv... anyway, feel free, it is important the plain text!
file_examples = open("examples.txt", encoding="utf8")
for text in file_examples.readlines():

	# list with the text features.
	text_features = []

	# author reputation
	author = 1
	print("Author Reputation:", author)
	text_features.append(author)

	# number of tuples
	tokens = tokensManager.GetTokens(text, 0)
	tagsTokens = taggerManager.TaggerComment(text)
	tags = taggerManager.TagsDict(tagsTokens)
	patt1, patt3, patt4, patt5 = patternsManager.GetPatternsDict(tags)

	number_tuples = len(patt1[1])+len(patt3[1])+len(patt3[1])+len(patt3[1])
	print("Number of Tuples:", number_tuples)
	text_features.append(number_tuples)

	# correctness
	correctness = correctnessManager.Correctness(text)
	print("Correctness: ", correctness, "\n-----\n")
	text_features.append(correctness)

	# in the end, add this list in the input text list, to the training purposes.
	input_text.append(text_features)

	# update the output with the desired value.
	output_text.append(3)

	# bonus: polarity of the text, using the Sentilex. To values greater than 0, the comment is positive; otherside, is negative.
	#dictF, pol = patternsManager.GetDictFeatures(tags)

print("The features vector (input) is", input_text, "and the expected value (output) is", output_text, "\n")

# So, when you finish to extract the features from your database, just apply the features vector and the expected vector to the MLP classifier
# You have to choose what topology you want to use. 1 for topology 1 and 2 for topology 2
# The return is a printed classification report with precision, recall and f-measure. If you wish more information, please see the scikit-learn documentation

annManager.AnnTraining(input_text, output_text, 1)


