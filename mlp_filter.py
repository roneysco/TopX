from typing import Tuple
import quality_predictor

def run_mlp_filter(parser_params : Tuple, num_reviews, grade, metric):
    '''
        This is an example usage of TopX approach to filter reviews by their quality.
        parser_params: is a tuple with two entries. The first is a list of dictionaries (each 
                        dictionary contains data of a review) and the second is the dictionary
                        key to use to get the review body of each review.
        num_reviews: the amount of dictionaries in the list
        grade: the desired grade
        metric: 1 or 2
        
    '''
    predictions = quality_predictor.predict(parser_params, metric)
    
    classifications = {'insufficient' : 0, 'sufficient' : 1, 'good' : 2, 'excellent' : 3}
    target = classifications[grade]

    for i in range(num_reviews):
        parser_params[0][i]['qualidade'] = str(predictions[i])
        if predictions[i] < target:
            parser_params[0][i]['removido'] = parser_params[0][i][parser_params[1]]
            parser_params[0][i][parser_params[1]] = ''
        else:
            parser_params[0][i]['removido'] = ''

    return parser_params[0]

    
    
