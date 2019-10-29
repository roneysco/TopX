import taggerManager
import tokensManager
import correctnessManager
import patternsManager
import annManager
from typing import List

# modify this method accordingly to the base used for training
def parse_text(filename):
    ''' Parses the file data to extract the reviews and the corresponding classification. '''
    classifications = {'IF' : 0, 'SF' : 1, 'BM' : 2, 'PL' : 3}

    parsed_data = []

    with open(filename, 'r') as f:
        data = f.read().split('\n')[1:-1] #removes header and last empty position

        for entry in data:
            temp = entry.split('\t')
            parsed_data.append([temp[1], classifications[temp[-1]]])
    return parsed_data

def train_model(parsed_data : List,  metric : int):
    ''' Trains the model using the specified metric(1 or 2) or input 0 to train both. '''
    
    input_text = []
    output_text = []

    for entry in parsed_data:
        
        text_features = []

        # enter author's reputation
        text_features.append(1)
        
        # finding patterns
        tokens = tokensManager.GetTokens(entry[0], 0)
        tagsTokens = taggerManager.TaggerComment(entry[0])
        tags = taggerManager.TagsDict(tagsTokens)
        patt1, patt3, patt4, patt5 = patternsManager.GetPatternsDict(tags)
        
        number_tuples = len(patt1[1])+len(patt3[1])+len(patt3[1])+len(patt3[1])
        text_features.append(number_tuples)
            
        # correctness
        correctness = correctnessManager.Correctness(entry[0])
        text_features.append(correctness)
        
        # enter features 
        input_text.append(text_features)
        
        # enter classification
        output_text.append(entry[1])
        
    print("The features vector (input) is", input_text, "and the expected value (output) is", output_text, "\n")
    annManager.AnnTraining(input_text, output_text, metric) 
    
if __name__ == '__main__':
    
    parsed_data = parse_text('corpus_buscape_conceitos.txt')
    print('Treinando modelos ...')
    train_model(parsed_data, 0)
    


