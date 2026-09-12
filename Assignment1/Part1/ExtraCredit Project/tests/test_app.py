import pandas as pd

from app import build_passenger_row, clean_data, predict_survival, train_model


def sample_data():
    return pd.DataFrame({
        'Survived': [0, 1, 1, 0],
        'Pclass': [3, 1, 2, 3],
        'Sex': ['male', 'female', 'female', 'male'],
        'Age': [22, 38, None, 35],
        'SibSp': [1, 1, 0, 0],
        'Parch': [0, 0, 0, 0],
        'Fare': [7.25, 71.28, 13.0, 8.05],
        'Embarked': ['S', 'C', None, 'S'],
        'Cabin': [None, 'C85', None, None],
    })


def test_clean_data_removes_cabin_and_fills_missing_values():
    cleaned = clean_data(sample_data())
    assert 'Cabin' not in cleaned.columns
    assert cleaned[['Age', 'Embarked']].isnull().sum().sum() == 0


def test_clean_data_replaces_missing_age_and_embarked_with_expected_values():
    df = pd.DataFrame({
        'Survived': [0, 1, 1, 0],
        'Pclass': [3, 1, 2, 3],
        'Sex': ['male', 'female', 'female', 'male'],
        'Age': [22, None, 30, 35],
        'SibSp': [1, 1, 0, 0],
        'Parch': [0, 0, 0, 0],
        'Fare': [7.25, 71.28, 13.0, 8.05],
        'Embarked': ['S', None, 'C', 'S'],
        'Cabin': [None, 'C85', None, None],
    })

    cleaned = clean_data(df)

    assert cleaned.loc[1, 'Age'] == 30.0
    assert cleaned.loc[1, 'Embarked'] == 'S'
    assert cleaned['Age'].isnull().sum() == 0
    assert cleaned['Embarked'].isnull().sum() == 0
    assert 'Cabin' not in cleaned.columns


def test_train_model_trains_successfully():
    model, columns = train_model(sample_data())

    assert model is not None
    assert len(columns) > 0
    assert set(model.classes_) == {0, 1}


def test_model_can_predict_a_passenger():
    model, columns = train_model(sample_data())
    passenger = {
        'Pclass': 1,
        'Sex': 'female',
        'Age': 30,
        'SibSp': 0,
        'Parch': 0,
        'Fare': 50,
        'Embarked': 'C',
    }
    prediction = predict_survival(model, columns, passenger)
    assert prediction in (0, 1)


def test_predict_survival_returns_binary_output_for_multiple_passengers():
    model, columns = train_model(sample_data())
    passengers = [
        {
            'Pclass': 1,
            'Sex': 'female',
            'Age': 30,
            'SibSp': 0,
            'Parch': 0,
            'Fare': 50,
            'Embarked': 'C',
        },
        {
            'Pclass': 3,
            'Sex': 'male',
            'Age': 22,
            'SibSp': 1,
            'Parch': 0,
            'Fare': 7.25,
            'Embarked': 'S',
        },
    ]

    predictions = [predict_survival(model, columns, passenger) for passenger in passengers]

    assert all(prediction in (0, 1) for prediction in predictions)


def test_predict_survival_for_third_class_male_passenger_matches_training_encoding():
    model, columns = train_model(sample_data())
    passenger = {
        'Pclass': 3,
        'Sex': 'male',
        'Age': 22,
        'SibSp': 1,
        'Parch': 0,
        'Fare': 7.25,
        'Embarked': 'S',
    }

    prediction = predict_survival(model, columns, passenger)
    encoded_row = build_passenger_row(passenger, columns)

    assert prediction in (0, 1)
    assert encoded_row.loc[0, 'Sex_male'] == 1
    assert encoded_row.loc[0, 'Embarked_S'] == 1
    if 'Embarked_Q' in encoded_row.columns:
        assert encoded_row.loc[0, 'Embarked_Q'] == 0
    assert set(encoded_row.columns) == set(columns)
