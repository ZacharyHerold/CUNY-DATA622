'''
score_model.py (2 points)
When this is called using python score_model.py in the command line, 
this will ingest the .pkl random forest file and apply the model to the locally saved scoring dataset csv. 
There must be data check steps and clear commenting for each step inside the .py file. 
The output for running this file is a csv file with the predicted score, 
as well as a png or text file output that contains the model accuracy report 
(e.g. sklearn's classification report or any other way of model evaluation).
'''
# To troubleshoot, file runs from within IDE, but not from command line. 
# GIves NameError: name 'y_predict' is not defined

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

with open(random_forest_pkl_filename, 'rb') as fp:
    random_forest_model = pickle.load(fp)
    print("Loaded Random Forest model :: ", random_forest_model)
fp.close()

#Exporting predictions to csv file in current working directory
prediction = pd.DataFrame(y_predict, columns=['predictions']).to_csv('prediction.csv')

print("Train Accuracy :{}".format(random_forest_model.score(X_train, y_predict_train)))
#Train Accuracy :0.9823434991974318

print("Test Accuracy: {}".format(random_forest_model.score(X_test, y_test)))
#Test Accuracy: 0.8134328358208955

# creating an accuracy report, writing to cwd

cm = confusion_matrix(y_test, y_predict)
cr = classification_report(y_test, y_predict)

print("Confusion Matrix : \n {}".format(cm))
print(" ")
print("Classification Report : \n {}".format(cr))

cm = np.array2string(cm)
score_train = random_forest_model.score(X_train, y_predict_train)
score_test = random_forest_model.score(X_test, y_test)

with open('accuracy_report.txt', 'w') as f:
    f.write("Titanic Random Forest Classification Accuracy Report \n")
    f.write("DATA622 Zachary Herold - HW2 \n\n")
    f.write("Train Accuracy :{} \n".format(score_train))
    f.write("Test Accuracy: {} \n".format(score_test))
    f.write("Classification Report\n\n{}\n\nConfusion Matrix\n\n{}\n".format(cr, cm))
f.close()


