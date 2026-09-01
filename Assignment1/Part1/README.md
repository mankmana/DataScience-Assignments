# Explain what you did in assignment 1 part 1

Objective
The objective of this project is to analyze the Titanic passenger data and build a machine learning model that can predict whether a passenger survived based on features such as age, gender, passenger class, fare, and family information.

Step 1: Identifying and choosing a kaggle DataSet
- I am choosing Titanic Survival Prediction Dataset

- Google collab link :

- https://colab.research.google.com/drive/1fPkGpGySCqBkFd8GbqN2yzIF-WXF6jBS?usp=sharing

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
train_df.isnull().sum()
```
 and now there are no missing values in any columns.

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

In this graph:

- `0` represents passengers who did not survive.
- `1` represents passengers who survived.

The purpose of this graph is to quickly compare the number of survivors and non-survivors in the dataset.

#### Survival Rate by Gender

The next EDA step was to compare survival rates between male and female passengers.

The survival rate was calculated as a percentage for each gender.

The result showed:

- Female survival rate: approximately **74.2%**
- Male survival rate: approximately **18.9%**

This shows a very strong difference in survival based on gender. Female passengers had a much higher survival rate than male passengers.

#### Survival Rate by Passenger Class

The next EDA step was to compare survival rates across the three passenger classes.

The Titanic dataset uses:

- `1` = First Class
- `2` = Second Class
- `3` = Third Class

The graph shows:

- First Class survival rate: approximately **63%**
- Second Class survival rate: approximately **47%**
- Third Class survival rate: approximately **24%**

This shows a clear relationship between passenger class and survival. Passengers in First Class had the highest survival rate, while passengers in Third Class had the lowest survival rate.

#### Age Distribution

The next EDA step was to analyze the age distribution of Titanic passengers.

A **histogram** was used because age is a continuous numerical value rather than a category.

The histogram uses `bins=20`, which means the complete age range is divided into 20 intervals. Matplotlib automatically identifies the minimum and maximum values in the `Age` column and divides that range into equal-sized groups.

From the graph:

- Most passengers were approximately between 20 and 40 years old.
- The number of passengers generally decreases as age increases.
- There were fewer elderly passengers compared with younger and middle-aged passengers.
- A noticeable spike appears around the late 20s.

The spike around the late 20s is partly because missing `Age` values were earlier replaced with the median age. This caused many passengers to have the same age value after data cleaning.

#### Average Age by Survival Status

The next EDA step compared the average age of passengers who survived with those who did not.

The results showed:

- Average age of passengers who did not survive: approximately **30.0 years**
- Average age of passengers who survived: approximately **28.3 years**

Survivors were slightly younger on average, but the difference was small. This suggests that age alone may not have been as strong a factor as gender or passenger class.

#### Survival Rate by Age Group

To understand the effect of age more clearly, passengers were grouped into age ranges:

- Child: 0–12 years
- Teen: 13–17 years
- Adult: 18–59 years
- Senior: 60+ years

The survival rates were approximately:

- Child: **58%**
- Teen: **48%**
- Adult: **36%**
- Senior: **27%**

This shows that younger passengers had a higher survival rate, while survival generally decreased as age increased.

This age-group analysis was more useful than comparing only the average age of survivors and non-survivors, because it revealed differences between specific age ranges.

## Calculate average fare for survivors and non-survivors
average_fare_by_survival = train_df.groupby('Survived')['Fare'].mean()

print(average_fare_by_survival)

#### Average Fare by Survival Status

The next EDA step compared the average fare paid by passengers who survived with those who did not.

The results showed:

- Average fare for passengers who did not survive: approximately **22.1**
- Average fare for passengers who survived: approximately **48.4**

Passengers who survived had paid a much higher average fare.

This suggests that higher fare was associated with a better chance of survival. However, fare is also closely related to passenger class, so this result may partly reflect the higher survival rate already observed among First Class passengers.


## Feature Preparation

Before building the machine learning model, the dataset needs to be converted into a form the model can understand.

A list called `features` is used to select only the useful columns for prediction:

- `Pclass`
- `Sex`
- `Age`
- `SibSp`
- `Parch`
- `Fare`
- `Embarked`

Columns such as `PassengerId`, `Name`, and `Ticket` are not used in this basic model because they are either identifiers or contain values that are too unique to be useful directly.

The selected input columns are stored in `X`, while the value we want to predict, `Survived`, is stored in `y`.

The columns `Sex` and `Embarked` contain text categories, so they need to be converted into numerical form.

For this, Pandas provides the `get_dummies()` function.

`pd.get_dummies()` converts categorical values into separate 0/1 columns so that a machine learning model can use them.

For example, instead of storing `male` and `female` as text, the data can be represented using a numeric column containing 0 and 1.

The option `drop_first=True` removes one category because it can already be inferred from the remaining columns. This avoids adding unnecessary duplicate information.

A few things to notice:

Sex is now represented by Sex_male
True = male
False = female
Embarked became:
Embarked_Q
Embarked_S
The missing category is C, because drop_first=True removed one category as the reference.

So for example:

Embarked_Q=False
Embarked_S=False

means that passenger embarked from C.

Also, True/False is fine for machine learning. In practice, these behave like 1/0.

## Training and Testing Data Split

The prepared dataset was divided into training and testing sets so the model can be evaluated fairly.

The result was:

- Training rows: **712**
- Testing rows: **179**

This means approximately 80% of the Titanic data will be used to train the model, while the remaining 20% will be used to test how well the model performs on unseen passengers.

This step is now complete, and the next step is to train the machine learning model.

## Model Training - Logistic Regression

For the first machine learning model, I used **Logistic Regression**.

```from sklearn.linear_model import LogisticRegression

# Create the model
model = LogisticRegression(max_iter=1000)

# Train the model using the training data
model.fit(X_train, y_train)

print("Model training complete")
```

Logistic Regression is commonly used for classification problems where the output has two possible values. In this project:

- `0` = Did not survive
- `1` = Survived

The model learns patterns from features such as passenger class, gender, age, fare, and embarkation port, and then estimates the probability of survival.

I used:

`max_iter=1000`

This gives the model up to 1000 internal optimization steps to find a stable solution while training. It may stop earlier if it converges before reaching that limit.

Logistic Regression was selected because it is simple, widely used, and suitable for a binary prediction problem like Titanic survival.

## Making Predictions

After training the Logistic Regression model, I used it to predict survival for the testing data.

The model used the passenger features in `X_test`, such as:

- Passenger class
- Gender
- Age
- Number of siblings/spouse
- Number of parents/children
- Fare
- Embarkation port

For each passenger, the model combined these features with the patterns it had learned from the training data and estimated the probability of survival.

The prediction output uses:

- `0` = Predicted not to survive
- `1` = Predicted to survive

For example, the first 20 predictions were:

`[0 0 0 1 1 1 1 0 1 1 0 0 0 0 0 1 0 1 0 0]`

This means the model predicted survival individually for each passenger based on that passenger's combination of features.

At this stage, these are only predictions. We still need to compare them with the actual survival values from the testing set to measure how accurate the model is.


## Model Evaluation - Accuracy

After making predictions on the testing data, I compared the predicted survival values with the actual values using `accuracy_score()` from Scikit-learn.

The Logistic Regression model achieved an accuracy of approximately **81%**.

This means the model correctly predicted the survival outcome for about **81 out of every 100 passengers** in the testing set.

Since the testing set contained 179 passengers, the model made roughly **145 correct predictions** and about **34 incorrect predictions**.

Accuracy gives an overall idea of model performance, but it does not show what type of mistakes the model made. The next step is to use a confusion matrix to understand those errors in more detail.


## Confusion Matrix

To understand the model's predictions in more detail, I used a confusion matrix.

The result was:

```text
[[90 15]
 [19 55]]

This means:

90 passengers did not survive, and the model predicted this correctly.
15 passengers did not survive, but the model predicted that they survived.
19 passengers survived, but the model predicted that they did not survive.
55 passengers survived, and the model predicted this correctly.

# Final Model Interpretation

The Logistic Regression model achieved an accuracy of approximately **81%** on the testing data.

The model used passenger information such as:

- Passenger class
- Gender
- Age
- Family information
- Fare
- Embarkation port

to predict whether a passenger survived.

The exploratory analysis showed that gender and passenger class had strong relationships with survival. Age also showed a clearer pattern when passengers were grouped into age ranges.

Overall, the model performed reasonably well for a simple binary classification model, although some predictions were still incorrect.

Overall:

Correct predictions: 145
Incorrect predictions: 34
