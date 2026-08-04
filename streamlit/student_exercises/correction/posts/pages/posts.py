import os

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

CURR_DIR: str = os.path.dirname(__file__)
POSTS_FILE: str = os.path.join(os.path.dirname(CURR_DIR), "posts.csv")

@st.cache_resource
def load_data() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(POSTS_FILE)
    df.created_at = pd.to_datetime(df["created_at"]).dt.date
    return df


def post_analysis() -> None:
    df: pd.DataFrame = load_data()
    df_filtered: pd.DataFrame = df.copy()

    st.title("Post analysis")
    st.link_button('Flask Example', 'http://localhost:8080/authors')
    st.html("<h2>Analysis tool for blog posts</h2>")
    st.markdown(
        """
### this tools allows you to:
- get the number of post per date
- see the authors that posts most
"""
    )

    min_date = df.created_at.min()
    max_date = df.created_at.max()

    st.sidebar.title("Filters")
    dates: tuple = st.sidebar.date_input(
        "Select dates", [min_date, max_date], min_date, max_date
    )

    authors: tuple[str] = st.sidebar.multiselect(
        "Authors", sorted(df.author.unique()), df.author.unique()
    )

    keyword: str = st.sidebar.text_input("Keyword", "")

    if len(dates) != 2:
        st.error("Please Select starting and ending date")
        return

    df_filtered = df_filtered.loc[df_filtered.created_at.between(dates[0], dates[1])]
    df_filtered = df_filtered.loc[df_filtered.author.isin(authors)]
    df_filtered = df_filtered.loc[
        df_filtered.body.map(lambda b: keyword in b if keyword != "" else True)
    ]

    st.dataframe(df_filtered)

    post_per_date: pd.Series = df_filtered.groupby("created_at").size()
    post_per_date_bar: px.bar = px.bar(post_per_date)

    st.plotly_chart(post_per_date_bar, key="post_per_date_bar")

    post_per_authors_and_date = df_filtered.groupby(["created_at", "author"]).size()
    post_per_authors_date_bar = px.bar(
        post_per_authors_and_date,
        x=post_per_authors_and_date.index.get_level_values(0),
        y=post_per_authors_and_date.values,
        color=post_per_authors_and_date.index.get_level_values(1),
    )
    st.plotly_chart(post_per_authors_date_bar)


post_analysis()
