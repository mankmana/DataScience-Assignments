# explain what you did in assignment 1 part 1

Objective
The objective of this project is to analyze the Titanic passenger data and build a machine learning model that can predict whether a passenger survived based on features such as age, gender, passenger class, fare, and family information.

Step 1: Identifying and choosing a kaggle DataSet
- I am choosing Titanic Survival Prediction Dataset

# Dataset (Load Data)
For this assignment, I am using the Titanic - Machine Learning from Disaster dataset from Kaggle.

The dataset contains passenger information from the Titanic disaster and is provided in CSV format. Since the data is organized into rows and columns, it is considered structured tabular data.

Two main files are used:

train.csv - Contains passenger information along with the Survived column. This file is used to train the machine learning model.
test.csv - Contains similar passenger information but does not contain the Survived column. This file is used to make predictions after the model has been trained.
Some important columns in the dataset are:

PassengerId - Unique ID for each passenger
Pclass - Passenger class
Sex - Gender
Age - Age of the passenger
SibSp - Number of siblings or spouses aboard
Parch - Number of parents or children aboard
Fare - Ticket fare
Embarked - Port where the passenger boarded
Survived - Survival status, where 0 means did not survive and 1 means survived


# Initial Data Check (Understand data)
I checked the dataset before making any changes.

train_df.head()
train_df.info()
train_df.isnull().sum()
This helped me see the columns, data types, and missing values in the data.


# Finding and analyzing the data for cleanup

train_df.isnull().sum() - this will give me the number of missing value for each column so it becomes easier to identify which columns would need a data cleanup

