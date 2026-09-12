import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression

FEATURES = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean the Titanic training data using the Assignment 1 decisions."""
    data = dataframe.copy()
    data['Age'] = data['Age'].fillna(data['Age'].median())
    data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])
    return data.drop(columns=['Cabin'], errors='ignore')


def build_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepare the Titanic model features using the existing schema."""
    return pd.get_dummies(dataframe[FEATURES], columns=['Sex', 'Embarked'], drop_first=True)


def build_passenger_row(passenger: dict, feature_columns) -> pd.DataFrame:
    """Convert a single passenger into the exact feature layout learned during training."""
    row = pd.DataFrame([passenger])
    row['Sex_male'] = (row['Sex'] == 'male').astype(int)
    row['Embarked_Q'] = (row['Embarked'] == 'Q').astype(int)
    row['Embarked_S'] = (row['Embarked'] == 'S').astype(int)
    row = row.drop(columns=['Sex', 'Embarked'])
    return row.reindex(columns=feature_columns, fill_value=0)


def train_model(dataframe: pd.DataFrame):
    """Prepare features and train a Logistic Regression model."""
    data = clean_data(dataframe)
    X = build_features(data)
    y = data['Survived']
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, X.columns


def predict_survival(model, feature_columns, passenger: dict) -> int:
    """Predict survival for one passenger using the trained feature layout."""
    row = build_passenger_row(passenger, feature_columns)
    return int(model.predict(row)[0])


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_resource
def get_model(dataframe: pd.DataFrame):
    return train_model(dataframe)


st.set_page_config(page_title='Titanic Survival Dashboard', page_icon='🚢')
st.title('Titanic Survival Prediction Dashboard')
st.write('Enter passenger details to receive a Logistic Regression survival prediction.')

try:
    train_df = load_data('data/train.csv')
    model, feature_columns = get_model(train_df)

    with st.sidebar:
        st.header('Passenger details')
        pclass = st.selectbox('Passenger class', [1, 2, 3], index=2)
        sex = st.selectbox('Sex', ['female', 'male'])
        age = st.number_input('Age', min_value=0.0, max_value=100.0, value=30.0)
        sibsp = st.number_input('Siblings/spouses aboard', min_value=0, max_value=8, value=0)
        parch = st.number_input('Parents/children aboard', min_value=0, max_value=6, value=0)
        fare = st.number_input('Fare', min_value=0.0, value=32.0)
        embarked = st.selectbox('Embarkation port', ['C', 'Q', 'S'], index=2)

    passenger = {
        'Pclass': pclass,
        'Sex': sex,
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Fare': fare,
        'Embarked': embarked,
    }

    if st.button('Predict survival'):
        prediction = predict_survival(model, feature_columns, passenger)
        if prediction == 1:
            st.success('Prediction: This passenger is predicted to survive.')
        else:
            st.error('Prediction: This passenger is predicted not to survive.')

    st.subheader('Dataset overview')
    col1, col2 = st.columns(2)
    col1.metric('Passengers', len(train_df))
    col2.metric('Observed survival rate', f"{train_df['Survived'].mean() * 100:.1f}%")

    st.subheader('Survival rate by gender')
    st.bar_chart(train_df.groupby('Sex')['Survived'].mean() * 100)

except FileNotFoundError:
    st.warning('Add the Kaggle file at data/train.csv before running the dashboard.')
