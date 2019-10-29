# TopX

Hi! Thank you for use our TopX approach!
This is the code for our IJCNN paper called "An experimental study based on Fuzzy Systems and Artificial Neural Networks to estimate the importance of reviews about product and services"

In this folder you have all the files that we used to run the approach. Please see that here we use a SQL database file with the reviews and the same resources (Sentilex for sentiment analysis and Mac_Morpho as POS tagger).

Feel free to make any adjustment that you want! Any further information, please, contact me!

Have fun! Thank you so much!


---------------------------------

Changes at this branch:

' model_trainer.py ' will train and save the model in the 'trained_models' folder. The method 'parse_text' can be modified to be used accordingly to the base used for training

' quality_predictor.py ' will predict the quality of a given list of reviews using the trained models. The method '_parse_text' can be modified to return a list of reviews(text) accordingly to the base of reviews.

'mlp_filter' is an example of how to use this approach to filter reviews by quality.


