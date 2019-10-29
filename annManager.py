from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from typing import List
import pickle
import json

# Return the classification report of the chosen topology
def AnnTraining(inputs : List, outputs : List, topology : int):
    ''' 
        Performs training for the chosen topology(1 or 2) or both if topology=0 was given.
        The trained model and the classification report will be saved in separeted files.
    '''

    input_train, input_test, output_train, output_test = train_test_split(inputs, outputs)
    scaler = StandardScaler()
    scaler.fit(input_train)
    input_train = scaler.transform(input_train)
    input_test = scaler.transform(input_test)

    if topology == 1 or topology == 0:
        #Paper Topology 1
        mlp_top1 = MLPClassifier(activation='logistic', learning_rate_init=0.1, alpha=0.0001, hidden_layer_sizes=(3), max_iter=1000000)
        
        mlp_top1.fit(input_train,output_train)
        
        pickle.dump(mlp_top1, open('trained_models/model_topology1.p', 'wb'))
        
        predictions = mlp_top1.predict(input_test)
        with open('trained_models/m1_report.txt', 'w') as f:
            report = classification_report(output_test, predictions, output_dict=True)
            json.dump(report, f, indent=4)
            print(report)

    if topology == 2 or topology == 0:
        #Paper Topology 2
        mlp_top2 = MLPClassifier(activation='logistic', learning_rate_init=0.1, alpha=0.000001, hidden_layer_sizes=(6), max_iter=100000)

        mlp_top2.fit(input_train,output_train)
        
        pickle.dump(mlp_top2, open('trained_models/model_topology2.p', 'wb'))
        predictions = mlp_top2.predict(input_test)
        with open('trained_models/m2_report.txt', 'w') as f:
            report = classification_report(output_test, predictions, output_dict=True)
            json.dump(report, f, indent=4)
            print(report)  
    
def AnnPredict(input_predict : List, topology : int) -> List[int]:
    '''
    Predicts the quality of the reviews in the given list 
    :Return: Numpy array of ints (0 - insufficient; 1 - sufficient; 2 - goof; 3 - excellent)
    ''' 
    model = None
    if topology < 1 or topology > 2:
        return []
    model_file = 'model_topology1.p' if topology == 1 else 'model_topology2.p'
    try:
        with open('trained_models/'+model_file, 'rb') as f:
            model = pickle.load(f)
            predictions = model.predict(input_predict)
            return predictions
    except FileNotFoundError:
        print('Trained model not found. Run "model_trainer.py" first.')
    return [] 




