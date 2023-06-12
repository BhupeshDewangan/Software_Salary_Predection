import streamlit as st
import pickle
import numpy as np

def load_model():
    with open("saved_steps.pkl", 'rb') as file:
        data = pickle.load(file)

    return data

data = load_model()

reg_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


def show_predict_page():
    st.title("Software Developer Salary Predication")

    st.write("### We need some info to predict the salary")

    countries = (
        "United States of America",
        "Germany",
        "India",
        "Canada",
        "Brazil",
        "Russian Federation",
        "Israel",
        "Netherlands",
        "Switzerland",
        "Italy",
        "Spain"
    )

    education = (
        # "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post Grad"
    )

    country = st.selectbox("Country", countries)

    education = st.selectbox("Education Level", education)

    experi = st.slider("Year Of Experiece", 0, 50, 3)

    ok = st.button("Calculate Salary")

    if ok:

        x = np.array([[country, education, experi]])
        # x = np.array([["United States of America", "Master’s degree", 18]])
        
        x[:, 0] = le_country.transform(x[:, 0])
        x[:, 1] = le_education.transform(x[:, 1])
        x = x.astype(float)
        
        salary = reg_loaded.predict(x)
        # st.title(f"The estimated salary is ${salary[0]:.2f}")
        st.subheader(f"The estimated salary is")
        st.title(f"${salary[0]:.2f}")

        