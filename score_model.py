'''
score_model.py (2 points)
When this is called using python score_model.py in the command line, 
this will ingest the .pkl random forest file and apply the model to the locally saved scoring dataset csv. 
There must be data check steps and clear commenting for each step inside the .py file. 
The output for running this file is a csv file with the predicted score, 
as well as a png or text file output that contains the model accuracy report 
(e.g. sklearn's classification report or any other way of model evaluation).
'''

# Import the necessary modules 
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#Set working directory as .pkl file location
import os
file = 'score_model.py'
dir_path = os.path.dirname(os.path.realpath(file))
os.chdir(dir_path)

# Loading the saved random forest model pickle
random_forest_pkl_filename = 'random_forest_titanic.pkl'

#random_forest_model_pkl = open(random_forest_pkl_filename, 'rb').readlines()

# #FileNotFound Exception
# try:
#     random_forest_model_pkl = open(random_forest_pkl_filename, 'rb').readlines()
# except FileNotFoundError:
#     print("File not found")

# with open(filename) as pkl:
#     content = pkl.readlines()

with open(random_forest_pkl_filename, 'rb') as fp:
    random_forest_model = pickle.load(fp)
    print("Loaded Random Forest model :: ", random_forest_model)
fp.close()

#Exporting predictions to csv file in current working directory
prediction = pd.DataFrame(y_predict, columns=['predictions']).to_csv('prediction.csv')

print("Train Accuracy :{}".format(random_forest_model.score(X_train, y_predict_train)))
print("Test Accuracy: {}".format(random_forest_model.score(X_test, y_test)))

cm = confusion_matrix(y_test, y_predict)
cr = classification_report(y_test, y_predict)

print("Confusion Matrix : \n {}".format(cm))
print(" ")
print("Classification Report : \n {}".format(cr))

cm = np.array2string(cm)

with open('accuracy_report.txt', 'w') as f:
    f.write("Titanic Random Forest Classification Accuracy Report")
    f.write("DATA622 Zachary Herold - HW2")
    f.write("Train Accuracy :{}".format(random_forest_model.score(X_train, y_predict_train)))
    f.write("Test Accuracy: {}".format(random_forest_model.score(X_test, y_test)))
    f.write('Title\n\nClassification Report\n\n{}\n\nConfusion Matrix\n\n{}\n'.format(cr, cm))
f.close()


