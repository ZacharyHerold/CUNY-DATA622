DATA 622 # hw2 = Zachary Herold

	Assigned on September 15, 2018
	Due on October 6, 2019 11:59 PM EST
	17 points possible, worth 17% of your final grade
	
--------------------------------------------------------------------------------------------------------	
3. CRITICAL THINKING (3 points total)

Modify this ReadMe file to answer the following questions directly in place.
	1) Kaggle changes links/ file locations/login process/ file content
	
	
	
	2) We run out of space on HD / local permissions issue - can't save files
	
Before we can actually work with the data, we need to do something with it so we can begin to filter it to work with subsets of the data. This is usually what I would use pandas’ dataframe for but with large data files, we need to store the data somewhere else. In this case, we’ll set up a local sqllite database, read the csv file in chunks and then write those chunks to sqllite.

To do this, we’ll first need to create the sqllite database using the following command.

csv_database = create_engine('sqlite:///csv_database.db')
Next, we need to iterate through the CSV file in chunks and store the data into sqllite.


chunksize = 100000
i = 0
j = 1
for df in pd.read_csv(file, chunksize=chunksize, iterator=True):
      df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) 
      df.index += j
      i+=1
      df.to_sql('table', csv_database, if_exists='append')
      j = df.index[-1] + 1
	
	
https://pythondata.com/working-large-csv-files-python/

if you do not specify the buffering parameter upon calling Python's open(), a (small) buffer is usually applied, according to the "system default". The size of this buffer is not documented. For some version of glibc, here someone determined it to be 8 kB: stackoverflow.com/a/18194856/145400. For certain applications it makes sense to increase that buffer size with the buffering parameter. No general statement possible, but benchmarks help. Sometimes it makes sense to explicitly collect data in memory first, via docs.python.org/2/library/stringio.html 

	3) Someone updated python packages and there is unintended effect (functions retired or act differently)

Make use of virtual environments
Revert back to prior version (indicated on requirements.txt?)
	
	
	4) Docker issues - lost internet within docker due to some ip binding to vm or local routing issues( I guess this falls under lost internet, but I am talking more if docker is the cause rather then ISP)	
	
Check:
ip route list // there may be some network powersave options on your host that messes with the virtual network interfaces that docker needs.
ip addr show 
iptables -t nat -L -n -v  //  where docker puts all the rules to actually allow the containers to talk to different parts of then network (between them or out). Maybe the problem is a firewall tool/helper that wants full control over the iptables rules, and is therefor flushing the docker rules from time to time.
	
Source: https://stackoverflow.com/questions/24754984/docker-containers-keep-losing-internet
	
One workaround is by passing --net=host to your run command. This will cause your containers to use their hosts network stack and will disable linking of containers, however (as docker can't/shouldn't update the /etc/hosts of the host machine)

https://github.com/moby/moby/issues/14073

--------------------------------------------------------------------------------------------------------

1. Required Reading

  Read Chapter 4 of the Deep Learning Book
	Read Chapter 5 of the Deep Learning Book
	Read Chapter 1 of the Agile Data Science 2.0 textbook

2. Data Pipeline using Python (13 points total)

	Build a data pipeline in Python that downloads data using the urls given below, trains a random forest model on the training dataset using sklearn and scores the model on the test dataset.

	Scoring Rubric

	The homework will be scored based on code efficiency (hint: use functions, not stream of consciousness coding), code cleaniless, code reproducibility, and critical thinking (hint: commenting lets me know what you are thinking!)
Instructions:

	Submit the following 5 items on github.
	ReadMe.md (see "Critical Thinking")
	requirements.txt
	pull_data.py
	train_model.py
	score_model.py

More details:

requirements.txt (2 point)
This file documents all dependencies needed on top of the existing packages in the Docker Dataquest image from HW1. When called upon using pip install -r requirements.txt , this will install all python packages needed to run the .py files. (hint: use pip freeze to generate the .txt file)

pull_data.py (5 points)
When this is called using python pull_data.py in the command line, this will go to the 2 Kaggle urls provided below, authenticate using your own Kaggle sign on, pull the two datasets, and save as .csv files in the current local directory. The authentication login details (aka secrets) need to be in a hidden folder (hint: use .gitignore). There must be a data check step to ensure the data has been pulled correctly and clear commenting and documentation for each step inside the .py file.
	Training dataset url: https://www.kaggle.com/c/titanic/download/train.csv
	Scoring dataset url: https://www.kaggle.com/c/titanic/download/test.csv

train_model.py (5 points)
When this is called using python train_model.py in the command line, this will take in the training dataset csv, perform the necessary data cleaning and imputation, and fit a classification model to the dependent Y. There must be data check steps and clear commenting for each step inside the .py file. The output for running this file is the random forest model saved as a .pkl file in the local directory. Remember that the thought process and decision for why you chose the final model must be clearly documented in this section.
eda.ipynb (0 points)

[Optional] This supplements the commenting inside train_model.py. This is the place to provide scratch work and plots to convince me why you did certain data imputations and manipulations inside the train_model.py file.

score_model.py (2 points)
When this is called using python score_model.py in the command line, this will ingest the .pkl random forest file and apply the model to the locally saved scoring dataset csv. There must be data check steps and clear commenting for each step inside the .py file. The output for running this file is a csv file with the predicted score, as well as a png or text file output that contains the model accuracy report (e.g. sklearn's classification report or any other way of model evaluation).


