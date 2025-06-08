import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import time

st.set_page_config(page_title="Titanic Survival Predictor", layout="centered", page_icon="🚢")

@st.cache_data
def load_model():
    df1 = pd.read_csv("titanic.csv")
    df1 = df1.drop(df1.columns[0], axis = 1)
    X = df1.drop("Survived", axis=1)
    y = df1["Survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, lr.predict(X_test))
    return lr, accuracy

model, model_accuracy = load_model()

def predict_survival(pclass, age, fare, alone, sex, embarked, sharedt, title):
    # Mapping input to numeric values
    pclass_map = {"1st class": 1, "2nd class": 2, "3rd class": 3}
    sex_map = {"Male": 0, "Female": 1}
    embarked_map = {"Southhampton": 0, "Queenstown": 1, "Cherbourg": 2}
    title_map = {"Mr": 0, "Master": 1, "Mrs": 2, "Ms": 3, "Other": 4}

    pclass_num = pclass_map[pclass]
    sex_num = sex_map[sex]
    embarked_num = embarked_map[embarked]
    title_num = title_map[title]
    alone_num = 1 if not alone else 0

    # Age and fare bins
    age_num = min(age // 16, 4)
    if fare <= 8:
        fare_num = 0
    elif fare <= 14:
        fare_num = 1
    elif fare <= 31:
        fare_num = 2
    else:
        fare_num = 3

    # Prediction
    features = [[pclass_num, sex_num, fare_num, embarked_num, title_num, alone_num, sharedt, age_num]]
    result = model.predict(features)

    if result[0] == 1:
        st.success("🎉 You survived! Redirecting...")
        time.sleep(2)
        st.switch_page("pages/survived.py")
    else:
        st.error("💀 You did not survive. Redirecting...")
        time.sleep(2)
        st.switch_page("pages/died.py")

def main():
    st.title("🚢 Titanic Survival Predictor")
    st.markdown("Please enter your details to predict survival on the Titanic.")

    st.info(f"📊 Model Accuracy on Test Data: **{model_accuracy:.2%}**")

    # Layout in two columns
    col1, col2 = st.columns(2)
    with col1:
        pclass = st.selectbox('🎟️ Ticket Class', ['1st class', '2nd class', '3rd class'])
        age = st.slider('🎂 Age', 0, 80, 25)
        fare = st.number_input("💰 Fare Paid", min_value=0, max_value=512, value=50, step=1)
        title = st.selectbox("🧑 Title", ["Mr", "Master", "Mrs", "Ms", "Other"])

    with col2:
        sex = st.selectbox('🧬 Gender', ['Female', 'Male'])
        embarked = st.radio("🛳️ Port of Embarkation", ["Southhampton", "Queenstown", "Cherbourg"])
        alone = st.toggle('🧍 Are you traveling alone?')

        sharedt = 0
        if not alone:
            sharedt = st.slider('🧑‍🤝‍🧑 Number of companions', 1, 7, 4)

    # Show user input summary
    with st.expander("📄 See your inputs"):
        st.write({
            "Class": pclass,
            "Age": age,
            "Fare": fare,
            "Title": title,
            "Sex": sex,
            "Embarked": embarked,
            "Alone": alone,
            "Traveling Companions": sharedt
        })
    # Gender-Title validation
    invalid_female_titles = ["Mr", "Master"]
    invalid_male_titles = ["Mrs", "Ms"]

    if (sex == "Female" and title in invalid_female_titles) or (sex == "Male" and title in invalid_male_titles):
        st.error("⚠️ Inconsistent input: Selected title does not match selected gender.")
    else:
        # Button logic
        if st.button("Submit", type="primary"):
            predict_survival(pclass, age, fare, alone, sex, embarked, sharedt, title)

    # Button
    if st.button("🔍 Submit for Prediction", type="primary"):
        with st.spinner("Processing your result..."):
            predict_survival(pclass, age, fare, alone, sex, embarked, sharedt, title)

main()
