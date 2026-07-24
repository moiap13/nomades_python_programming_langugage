import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
EMPLOYEE_CSV_FILE: str = os.path.join(os.path.dirname(CURR_DIR), "employee.csv")


st.set_page_config(
    page_title="Employee analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_data() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(EMPLOYEE_CSV_FILE)
    df.Salary = pd.to_numeric(df["Salary"])
    return df


def employee_analysis() -> None:
    df = load_data()
    df_filtered = df.copy()

    st.title("Employee analysis")
    st.markdown("## Build with streamlit")

    st.sidebar.title("Filters")

    select_name: tuple[str] = st.sidebar.multiselect(
        "Employee filter", df.Name.unique(), df.Name.unique()
    )

    select_department: tuple[str] = st.sidebar.multiselect(
        "Department filter", df.Department.unique(), df.Department.unique()
    )

    df_filtered = df_filtered.loc[df_filtered.Nsme.isin(select_name)]
    df_filtered = df_filtered.loc[df_filtered.Department.isin(select_department)]

    st.dataframe(df_filtered)
    st.write(df_filtered.shape)

    tabs = st.tabs(["Employee", "Department"])
    with tabs[0]:
        name_salary = df_filtered.groupby("Name")["Salary"].sum()
        bar_chart = plt.bar(name_salary.index, name_salary.values)
        st.pyplot(bar_chart)
    with tabs[1]:
        department_salary = df_filtered.groupby("Department")["Salary"].sum()
        bar_chart = plt.bar(department_salary.index, department_salary.values)
        st.pyplot(bar_chart)

    # post_per_authors = df_filtered.groupby("author").size()
    # post_per_authors_pie = px.pie(
    #     post_per_authors, values=post_per_authors.values, names=post_per_authors.index
    # )
    # st.plotly_chart(post_per_authors_pie, key="post_per_authors_pie")


employee_analysis()
