# Extra Credit Assignment 2: What it requires
The extra-credit assignment focuses on using an AI coding assistant inside Visual Studio Code, such as GitHub Copilot Chat.

- Use VS Code with an AI coding extension.
- Generate or develop an application using AI assistance.
- Demonstrate AI-assisted code generation.
- Ask the assistant to write functions.
- Refactor existing code.
- Create unit tests.
- Generate or improve an entire application.
- Submit the generated application code in GitHub.
- Record a screencast showing the complete process.
- Explain how the AI assistant helped with development.


## Purpose
The purpose is to demonstrate how AI coding tools can support the complete software-development workflow—not just answer questions.

## Expected end result
The final result should be:
1. A working application.
2. Organized source code uploaded to a public GitHub repository.
3. Unit tests demonstrating that important functions work.
4. A README explaining the project and how to run it.
5. A screencast/video showing the end-to-end AI-assisted development journey.
For our project, the planned result is a Titanic Survival Prediction Dashboard that lets a user enter passenger information and receive a survival prediction, while also displaying data visualizations and statistics.

### Step 1: Open the Project in VS Code

I opened the Assignment 2 project folder in Visual Studio Code. The project contains the main application file, requirements file, README documentation, and tests folder. VS Code will be used as the development environment for building, refactoring, and testing the application with AI coding assistance.

### Step 2: Set Up GitHub Copilot

I enabled GitHub Copilot and Copilot Chat in Visual Studio Code by signing in with my GitHub account. Copilot will be used to assist with generating application code, explaining the existing project, refactoring functions, and creating unit tests.

### Step 3: Review the Existing Project with Copilot

I asked GitHub Copilot Chat to review the Titanic Survival Prediction Dashboard before making changes. Copilot explained the project files, data-cleaning process, Logistic Regression model, prediction workflow, and possible improvements. This review helped me understand the existing code structure before modifying the application.

### Step 4: Refactor the Application with Copilot

I used GitHub Copilot Chat to refactor the Titanic dashboard without changing its behavior. Copilot separated feature preparation and passenger-input processing into reusable functions. This improved the organization and readability of the application while preserving the original Titanic features and Logistic Regression settings.

I also kept `hello.py` as a small demonstration of Copilot generating a basic integer-addition function.

### Step 5: Generate Unit Tests with Copilot

I used GitHub Copilot to create pytest unit tests for the data-cleaning, model-training, and prediction functions. The tests verify that missing values are handled, the Cabin column is removed, the model trains successfully, and predictions return valid binary results.

The current test file contains two tests:

- `test_clean_data_removes_cabin_and_fills_missing_values()` checks that the `Cabin` column is removed and missing `Age` and `Embarked` values are filled.
- `test_model_can_predict_a_passenger()` checks that the model can be trained and that a passenger prediction is a valid binary value (`0` or `1`).

Together, these tests cover the main data-cleaning path and the basic prediction path. They indirectly exercise `train_model()` through the prediction test. The Streamlit interface, `load_data()`, `get_model()`, visualization, and missing-file warning are not currently covered.

The edge cases considered are missing `Age`, missing `Embarked`, the mostly empty `Cabin` column, and the requirement that predictions remain binary. Additional edge cases that could be tested include an empty dataset, invalid passenger values, all values missing in a categorical column, and a missing `data/train.csv` file.


#### Unit-Test Results

The test suite passed successfully:

- Tests collected: 5
- Tests passed: 5
- Tests failed: 0
- Code coverage: 90%
- Total statements: 60
- Missed statements: 6

The tests cover data cleaning, missing-value handling, Cabin removal, model training, and binary survival predictions. The remaining uncovered lines belong mainly to the interactive Streamlit interface and missing-file warning path.

#### Error Handling

The application includes error handling for a missing dataset file. The Streamlit code uses a `try-except FileNotFoundError` block when loading `data/train.csv`.

If the file is missing, the application displays a warning message instead of stopping with an unhandled error:


### Package Installation and Python Path Configuration

The project dependencies were installed from `requirements.txt`:

bash
python3 -m pip install -r requirements.txt


### Step 6: Run the Streamlit Application

After completing the refactoring and unit testing, I launched the application using Streamlit. The dashboard displayed the passenger input form, dataset metrics, survival-rate visualization, and prediction button. I tested the interface by entering passenger details and generating a survival prediction.

#### What Is a Streamlit Application?

Streamlit is a Python framework used to create interactive web applications for data science and machine-learning projects. It allows Python code, input controls, charts, metrics, and model predictions to be displayed in a browser without requiring extensive HTML, CSS, or JavaScript.

#### Why Streamlit Is Used in This Project

Streamlit converts the Titanic Logistic Regression model into an interactive dashboard. Users can enter passenger information such as passenger class, gender, age, fare, family details, and embarkation port. The application then uses the trained model to predict whether the passenger is likely to survive.

The dashboard also displays dataset statistics and a survival-rate chart. This makes the machine-learning model easier to demonstrate and use than running predictions only from a Python script or notebook.

### Step 7: Test the Streamlit Dashboard

I launched the Titanic dashboard locally using Streamlit. The interface displayed passenger input controls, dataset metrics, a survival-rate chart, and a prediction button. I tested the application by entering passenger details and generating survival predictions through the browser interface.

### Step 8: Testing Survival and Non-Survival Scenarios

I tested the dashboard with both types of prediction outcomes.

For a higher-risk example, I entered a third-class male passenger with an age of 22, one sibling or spouse aboard, no parents or children aboard, a fare of 7.25, and embarkation port S. The model predicted that this passenger would not survive.

I also tested a first-class female passenger scenario. The model predicted that this passenger would survive.

Testing both outcomes confirms that the dashboard can return both possible binary predictions: survived (`1`) and did not survive (`0`).


### Debugging and Fixing Prediction-Time Encoding

During dashboard testing, a third-class male passenger with the following details was predicted as surviving:

- Passenger class: 3
- Sex: male
- Age: 22
- Siblings/spouses aboard: 1
- Parents/children aboard: 0
- Fare: 7.25
- Embarkation port: S

This result required investigation because the passenger represents a higher-risk profile in the Titanic dataset.

The suspected issue was that `pd.get_dummies()` was being applied separately to a single passenger row inside `predict_survival()`. When `drop_first=True` is applied to one row, the resulting columns may not match the columns created during model training. This can cause the passenger's gender or embarkation information to be encoded incorrectly.

The proposed fix creates the categorical columns explicitly:

- `Sex_male`
- `Embarked_Q`
- `Embarked_S`

The prediction row is then reindexed to exactly match the feature columns used during training. This ensures that training-time and prediction-time data have the same structure.

A regression test was also added to verify that this passenger scenario is processed correctly and that the prediction remains a valid binary value of `0` or `1`.

The application must be saved and restarted after applying the fix so that Streamlit uses the updated code. The prediction should then be tested again in the dashboard.

### Debugging Fix Verification

After correcting the prediction-time categorical encoding, I restarted the Streamlit application and tested the same third-class male passenger scenario.

The input was:

- Passenger class: 3
- Sex: male
- Age: 22
- Siblings/spouses aboard: 1
- Parents/children aboard: 0
- Fare: 7.25
- Embarkation port: S

The updated dashboard predicted:

```text
Prediction: This passenger is predicted not to survive.
