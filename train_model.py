'''
train_model.py (5 points) When this is called using python train_model.py in the command line, 
this will take in the training dataset csv, perform the necessary data cleaning and imputation, 
and fit a classification model to the dependent Y. 

There must be data check steps and clear commenting for each step inside the .py file. 
The output for running this file is the random forest model saved as a .pkl file in the local directory. 
Remember that the thought process and decision for why you chose the final model must be clearly documented in this section. eda.ipynb (0 points)
'''

# In this exercise we seek to construct a highly parsimonious model based on 
# the well-known fact that females not in third class had the highest survival rates on the Titanic. 

# Import the necessary modules
import pandas as pd
import re 
from sklearn.model_selection import train_test_split
import pickle
from sklearn.pipeline import Pipeline 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import warnings 
warnings.filterwarnings("ignore")

df = pd.DataFrame(pd.read_csv('train.csv'))
#df.info()

model_cols = ['Name', 'Pclass', 'Cabin', 'Embarked', 'Fare']

X = df[model_cols]
# Model does not include these fields:
#       'PassengerID' (no predictive value), 
#       'Sex' (collinear with constructed 'Title' feature),
#       'Age' (majority of null values, if later included, suggested imputation method is regression prediction)
#       'SibSp' (research shows low predictive power),
#       'Parch' (research shows low predictive power), 
#       'Ticket' (little of value from decomposition),  

#Separating out the target variable
y = df['Survived']

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42) # 70% training and 30% test
#X_train.info()

def categorization(data): 
    data = [data]
    titles = {"Mr": 1, "Mrs": 2, "Miss": 3, "Master": 4, "Rare": 5}

    for dataset in data:
        # extract titles
        dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
        # replace titles with a more common title or as Rare
        dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr',\
                                                'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
        dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
        dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
        # convert titles into numbers
        dataset['Title'] = dataset['Title'].map(titles)
        # filling NaN with 0, to get safe
        dataset['Title'] = dataset['Title'].fillna(0)
    
    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
    for dataset in data:
        dataset['Cabin'] = dataset['Cabin'].fillna("U0")
        dataset['Cabin'] = dataset['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
        # converting cabins into deck numbers, with null values equaling 8
        dataset['Cabin'] = dataset['Cabin'].map(deck)
         # filling NaN with 8, to get safe
        dataset['Cabin'] = dataset['Cabin'].fillna(8)

    ports = {"S": 0, "C": 1, "Q": 2}
    for dataset in data:
        # convert ports into numbers
        dataset['Embarked'] = dataset['Embarked'].map(ports)
        # filling NaN with 0 (most common port, Southampton), to get safe
        dataset['Embarked'] = dataset['Embarked'].fillna(0)

categorization(X_train)

X_train = X_train.drop(['Name'], axis=1)
X_train.head()
X_train.describe()

#Checking for null values (in X_train)
total = X_train.isnull().sum().sort_values(ascending=False)
percent_1 = X_train.isnull().sum()/X_train.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
missing_data.head(5)

X_train.info()

''' 
CODE for hyperparameter tuning: 
Tuned Logistic Regression Parameters: {'n_estimators': 35}
Best score is 0.8346709470304976

# Setup the hyperparameter grid
k = np.linspace(5, 100, 20).astype(int)
param_grid = {'n_estimators': k}

# Instantiate a logistic regression classifier: logreg
decision_tree_model = RandomForestClassifier()

# Instantiate the GridSearchCV object: logreg_cv
decision_tree_model_cv = GridSearchCV(decision_tree_model, param_grid, cv=5)

# Fit it to the data
decision_tree_model_cv.fit(X_train, y_train)

# Print the tuned parameters and score
print("Tuned Logistic Regression Parameters: {}".format(decision_tree_model_cv.best_params_)) 
print("Best score is {}".format(decision_tree_model_cv.best_score_))

'''
# Test data handling
categorization(X_test)
X_test = X_test.drop(['Name'], axis=1)

# Our random forest, based on only five features - Plcass, Cabin, Embarked, Fare and Title

random_forest_model = RandomForestClassifier(n_estimators=35)
random_forest_model.fit(X_train, y_train)
y_predict_train = random_forest_model.predict(X_train)
y_predict_test = random_forest_model.predict(X_test)

# Appears in score_model.py
# print("Train Accuracy :{}".format(random_forest_model.score(X_train, y_predict_train)))
# print("Test Accuracy: {}".format(random_forest_model.score(X_test, y_test)))
# print(confusion_matrix(y_test, y_predict))
# print(classification_report(y_test, y_predict))


# Dump the trained decision tree classifier with Pickle
random_forest_pkl_filename = 'random_forest_titanic.pkl'
# Open the file to save as pkl file
random_forest_model_pkl = open(random_forest_pkl_filename, 'wb')
pickle.dump(random_forest_model, random_forest_model_pkl)
# Close the pickle instances
random_forest_model_pkl.close()


# ''' Resources
# https://www.datacamp.com/community/tutorials/random-forests-classifier-python
# https://towardsdatascience.com%2Fpredicting-the-survival-of-titanic-passengers-30870ccc7e8
# https://dataaspirant.com/2017/02/13/save-scikit-learn-models-with-python-pickle/
# https://thatdatatho.com/2018/09/18/titanic-data-set-increased-prediction-scores-82/
# '''


