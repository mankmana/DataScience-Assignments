# explain what you did in assignment 1 part 1

Objective
The objective of this project is to analyze the Titanic passenger data and build a machine learning model that can predict whether a passenger survived based on features such as age, gender, passenger class, fare, and family information.

Step 1: Identifying and choosing a kaggle DataSet
- I am choosing Titanic Survival Prediction Dataset

## Dataset (Load Data)
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


## Initial Data Check (Understand data)
I checked the dataset before making any changes.

train_df.head()
train_df.info()
train_df.isnull().sum()
This helped me see the columns, data types, and missing values in the data.


## Finding and analyzing the data for cleanup

train_df.isnull().sum() - this will give me the number of missing value for each column so it becomes easier to identify which columns would need a data cleanup


### Dataset Structure

Using `train_df.info()`, I inspected the structure of the training dataset.

- Total rows: 891
- Total columns: 12
- `Age` contains 177 missing values
- `Cabin` contains 687 missing values
- `Embarked` contains 2 missing values

The dataset contains both numerical and categorical features, which will require preprocessing before building the machine learning model.


## Data Cleaning

From the analysis, dataset contained missing values in `Age`, `Cabin`, and `Embarked`.

To clean the data:

- Missing `Age` values were replaced with the median age.
- Missing `Embarked` values were replaced with the most common embarkation port.
- The `Cabin` column was removed because a large portion of its values were missing.

After this, I verified the dataset again using:

```python
train_df.isnull().sum() and now there are no missing values in any columns.

## Exploratory Data Analysis (EDA)

EDA stands for **Exploratory Data Analysis**.

In simple terms, EDA means looking at the data carefully before building a machine learning model.

The goal is to understand basic patterns in the dataset and answer questions such as:

- How many passengers survived?
- Did women survive more often than men?
- Did passenger class affect survival?
- Did age have any relationship with survival?

This helps us understand the data better before asking a model to make predictions.

For visualization, I used **Matplotlib**.

**Matplotlib** is a Python library used to create charts and graphs. It helps convert numerical data into visual form so that patterns are easier to understand.

The first EDA step is to check the overall survival distribution.


The first EDA step is to check the overall survival distribution.


