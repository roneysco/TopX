import taggerManager
import tokensManager
import correctnessManager
import patternsManager
import annManager
import json
import numpy
from typing import List, Tuple

# modify this method accordingly to your review's base.
# The return type must be 'List[str]' a list of reviews
def _parse_file(parser_params : Tuple) -> List[str]:
    ''' Parses data to return a list of reviews. '''
    
    json_data = parser_params[0]
    review_key = parser_params[1]

    parsed_data = [ review[review_key] for review in json_data ]
    return parsed_data

def predict(parser_params,  metric : int) -> List[int]:
    '''
        Runs method to parse the review's file obtaining a List of reviews.
        Then uses this List to predict the reviews quality with the correspondent metric (1 or 2).

        :Return List[int]: the quality predicted for each review (0 - insufficient; 1 - sufficient;
        2 - good; 3 - excellent)
    '''
   
    # runs the parser 
    parsed_data = _parse_file(parser_params)
    
    if not parsed_data:
        print('Failed to parse reviews')

    input_prediction = []
    predictions = None

    for entry in parsed_data:
        
        text_features = []

        # enter author's reputation
        text_features.append(1)
        
        # finding patterns
        tokens = tokensManager.GetTokens(entry, 0)
        tagsTokens = taggerManager.TaggerComment(entry)
        tags = taggerManager.TagsDict(tagsTokens)
        patt1, patt3, patt4, patt5 = patternsManager.GetPatternsDict(tags)
        
        number_tuples = len(patt1[1])+len(patt3[1])+len(patt3[1])+len(patt3[1])
        text_features.append(number_tuples)
            
        # correctness
        correctness = correctnessManager.Correctness(entry)
        text_features.append(correctness)
        
        # enter features 
        input_prediction.append(text_features)
       
    predictions = annManager.AnnPredict(input_prediction, metric)
    
    if not predictions.any():
        print("Prediction failed. Make sure the requested model was trained and the given metric is valid(1 or 2).")
        return []
    return predictions







