from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

# Return the classification report of the chosen topology
def AnnTraining(inputs, outputs, topology):

	input_train, input_test, output_train, output_test = train_test_split(inputs, outputs)

	scaler = StandardScaler()
	scaler.fit(input_train)
	input_train = scaler.transform(input_train)
	input_test = scaler.transform(input_test)

	#Paper Topology 1
	mlp_top1 = MLPClassifier(activation='logistic', learning_rate_init=0.1, alpha=0.0001, hidden_layer_sizes=(3), max_iter=1000000)

	#Paper Topology 2
	mlp_top2 = MLPClassifier(activation='logistic', learning_rate_init=0.1, alpha=0.000001, hidden_layer_sizes=(6), max_iter=100000)

	mlp_top1.fit(input_train,output_train)
	mlp_top2.fit(input_train,output_train)

	if topology == 1:
		predictions = mlp_top1.predict(input_test)
		print(classification_report(output_test, predictions))
	if topology == 2:
		predictions = mlp_top2.predict(input_test)
		print(classification_report(output_test, predictions))

	









