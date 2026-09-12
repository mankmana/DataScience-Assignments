# Assignment 2 — Titanic Survival Prediction Dashboard

This extra-credit project demonstrates AI-assisted software development using the Titanic machine-learning project from Assignment 1.

## Purpose

The dashboard allows a user to enter passenger information and receive a Logistic Regression survival prediction. It also displays dataset metrics and a survival-rate chart.

## Features

- Data cleaning for missing `Age` and `Embarked` values
- Removal of `Cabin`, consistent with Assignment 1
- Logistic Regression with `max_iter=1000`
- Interactive Streamlit prediction form
- Dataset overview metrics
- Survival-rate visualization
- Automated pytest tests

## Setup

Place the Kaggle Titanic file here:

```text
Assignment 2/data/train.csv
```

Install dependencies and run the dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest
```

## AI-assisted development demonstration

The screencast should demonstrate:

1. Generating the application structure with an AI coding assistant.
2. Writing the data-cleaning and prediction functions.
3. Refactoring repeated logic into reusable functions.
4. Generating and running unit tests.
5. Running the Streamlit application.

## Deliverables

- Source code: `app.py`
- Tests: `tests/test_app.py`
- Dependencies: `requirements.txt`
- Screencast/video link: **Add link here**
