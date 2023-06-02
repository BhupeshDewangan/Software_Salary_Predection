import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt


def shorten_catagories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]

        else:
            categorical_map[categories.index[i]] = 'Other'

    return categorical_map


def clean_experi(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5

    return float(x)


def clean_edu(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"

    if "Master's degree" in x:
        return "Master’s degree"

    if "Professional degree" or "Other doctoral" in x:
        return "Post Grad"

    return "Less than a Bachelors"

@st.cache

def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]

    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    # df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_catagories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)

    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != 'Others']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experi)
    df["EdLevel"] = df['EdLevel'].apply(clean_edu)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engg Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2021
        """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels= data.index, autopct="%1.1f%%", shadow=True, startangle=90)

    ax1.axis("equal")

    st.write("""#### No. of data from diff countries""")

    fig1.set_size_inches(15, 10)

    st.pyplot(fig1)




    st.write("""#### Mean Salary Based On Country""")

    data = df.groupby(['Country'])["Salary"].mean().sort_values(ascending=True)
    
    st.bar_chart(data)

    st.write("""#### Mean Salary Based On Experience""")

    # data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    # st.line_chart(data)

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    fig, ax = plt.subplots()
    ax.plot(data.index, data.values)
    fig.set_size_inches(50, 20)  # Set figure size to (8, 6)

    st.pyplot(fig)