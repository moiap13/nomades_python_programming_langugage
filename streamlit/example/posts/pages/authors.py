import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
CSV_FILE: str = os.path.join(os.path.dirname(CURR_DIR), "posts.csv")


st.set_page_config(
    page_title="Authors analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_data() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_FILE)
    df.created_at = pd.to_datetime(df["created_at"]).dt.date
    return df


def authors_analysis() -> None:
    df = load_data()
    df_filtered = df.copy()

    st.title("Authors analysis")
    st.html('<h2 style="color: red;">Build with streamlit</h2>')
    st.markdown(
        """
- item 1
- item 2
                
$$a^2$$
"""
    )

    st.sidebar.title("Filters")

    selected_authors: tuple[str] = st.sidebar.multiselect(
        "Author filter", df.author.unique(), df.author.unique()
    )

    df_filtered = df_filtered.loc[df_filtered.author.isin(selected_authors)]

    st.dataframe(df_filtered)
    st.write(df_filtered.shape)

    post_per_authors = df_filtered.groupby("author").size()
    post_per_authors_pie = px.pie(
        post_per_authors, values=post_per_authors.values, names=post_per_authors.index
    )
    st.plotly_chart(post_per_authors_pie, key="post_per_authors_pie")


authors_analysis()
