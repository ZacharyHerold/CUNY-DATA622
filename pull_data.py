'''
pull_data.py (5 points)
When this is called using python pull_data.py in the command line, this will go to the 2 Kaggle urls provided below, authenticate using your own Kaggle sign on, 
pull the two datasets, and save as .csv files in the current local directory. The authentication login details (aka secrets) need to be in a hidden folder (hint: use .gitignore). 
There must be a data check step to ensure the data has been pulled correctly and clear commenting and documentation for each step inside the .py file.
Training dataset url: https://www.kaggle.com/c/titanic/download/train.csv
Scoring dataset url: https://www.kaggle.com/c/titanic/download/test.csv
'''

import requests
import peekaboo

# The direct link to the Kaggle data set
url_train = 'https://www.kaggle.com/c/titanic/download/train.csv'
url_test = 'https://www.kaggle.com/c/titanic/download/test.csv'

# The local path where the data set is saved.
local_filename_train = "titanic_train.csv"
local_filename_test = "titanic_test.csv"

# Kaggle Username and Password
kaggle_info = {'UserName': peekaboo.UserName, 'Password': peekaboo.Password}


def local_write(url, local_filename): 
# Attempts to download the CSV file. Gets rejected because we are not logged in.
    r = requests.get(url)

    # Login to Kaggle and retrieve the data.
    r = requests.post(r.url, data = kaggle_info)
    #r = requests.post(r.url, data = kaggle_info, prefetch = False)

    # Writes the data to a local file one chunk at a time.
    f = open(local_filename, 'w')
    for chunk in r.iter_content(chunk_size = 512 * 1024): # Reads 512KB at a time into memory
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

local_write(url_train, local_filename_train)
local_write(url_test, local_filename_train)

# Source: https://ramhiser.com/2012/11/23/how-to-download-kaggle-data-with-python-and-requests-dot-py/
