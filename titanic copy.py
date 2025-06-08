import streamlit as st
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def predict_survival(pclass, age, fare, alone, sex, embarked, sharedt, title):
    # Fix class mapping
    if pclass == "1st class":
        pclass_num = 1
    elif pclass == "2nd class":
        pclass_num = 2
    else:
        pclass_num = 3

    # Fix age mapping
    if age <= 16:
        age_num = 0
    elif age <= 32:
        age_num = 1
    elif age <= 48:
        age_num = 2
    elif age <= 64:
        age_num = 3
    else:
        age_num = 4

    # Fix fare mapping
    if fare <= 8:
        fare_num = 0
    elif fare <= 14:
        fare_num = 1
    elif fare <= 31:
        fare_num = 2
    else:
        fare_num = 3

    alone_num = 1 if not alone else 0  # You had this reversed

    # Fix gender mapping
    if sex == "Male":
        sex_num = 0
    else:
        sex_num = 1

    # Fix embarked mapping
    if embarked == "Southhampton":
        embarked_num = 0
    elif embarked == "Queenstown":
        embarked_num = 1
    else:
        embarked_num = 2

    #title
    if title == "Mr":
        title_num = 0
    elif title == "Master":
        title_num = 1
    elif title == "Mrs":
        title_num = 2
    elif title == "Ms":
        title_num = 3
    else:
        title_num = 4

    # Load and prep data
    df1 = pd.read_csv("titanic.csv")
    df1 = df1.drop(df1.columns[0], axis=1)
    X = df1.drop("Survived", axis=1)
    y = df1['Survived']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 101)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.info("Model Accuracy on Test Data: **{accuracy:.2%}**")
    
    # Predict
    result = lr.predict([[pclass_num, sex_num, fare_num, embarked_num, title_num, alone_num, sharedt, age_num]])
    if result[0] == 0:
        st.switch_page("pages/died.py")
    elif result[0] == 1:
        st.switch_page("pages/survived.py")

def main():
    st.title("🚢 Prediction of Titanic Survival")
    st.text("Please fill in following information about passenger")

    pclass = st.selectbox(
        'Select your class',
        ('1st class', '2nd class', '3rd class'))

    age = st.slider('How old are you?', 0, 80, 40)

    fare = st.number_input("Enter your fare cost", min_value=0, max_value=512, value=50, step=1)

    title = st.selectbox(
        "What are you referred as?",
        ("Mr", "Master", "Mrs", "Ms", "Other"))

    alone = st.toggle('Are you alone?')

    if alone:
        st.write('You are alone!')
        sharedt = 0
    else:
        st.write('You are not alone!')
        sharedt = st.slider('How many people are coming along?', 0, 7, 4)

    sex = st.selectbox(
        'Select your gender',
        ('Female', 'Male'))

    embarked = st.radio(
        "Where did you embark from",
        ["Southhampton", "Queenstown", "Cherbourg"],
        index=0
    )

    # Button logic
    if st.button("Submit", type="primary"):
        predict_survival(pclass, age, fare, alone, sex, embarked, sharedt, title)

main()
