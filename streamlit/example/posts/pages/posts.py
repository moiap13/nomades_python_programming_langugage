import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
CSV_FILE: str = os.path.join(os.path.dirname(CURR_DIR), "posts.csv")


def load_data() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_FILE)
    df.created_at = pd.to_datetime(df["created_at"]).dt.date
    return df


def posts_analysis() -> None:
    df = load_data()
    df_filtered = df.copy()

    st.title("Posts analysis")
    st.html('<h2 style="color: red;">Build with streamlit</h2>')
    st.markdown(
        """
- item 1
- item 2
                
$$a^2$$
"""
    )

    min_date = df.created_at.min()
    max_date = df.created_at.max()

    st.sidebar.title("Filters")

    dates: tuple = st.sidebar.date_input(
        "Date filter", [min_date, max_date], min_value=min_date, max_value=max_date
    )
    selected_authors: tuple[str] = st.sidebar.multiselect(
        "Author filter", df.author.unique(), df.author.unique()
    )

    df_filtered = df_filtered.loc[df_filtered.created_at.between(dates[0], dates[1])]
    df_filtered = df_filtered.loc[df_filtered.author.isin(selected_authors)]

    st.dataframe(df_filtered)
    st.write(df_filtered.shape)

    post_per_date: pd.DataFrame = df_filtered.groupby("created_at").size()
    post_per_date_bar: px.bar = px.bar(post_per_date)
    st.plotly_chart(post_per_date_bar, key="post_per_date_bar")

    post_per_authors_and_date = df_filtered.groupby(["created_at", "author"]).size()
    post_per_authors_date_bar = px.bar(
        post_per_authors_and_date,
        x=post_per_authors_and_date.index.get_level_values(0),
        y=post_per_authors_and_date.values,
        color=post_per_authors_and_date.index.get_level_values(1),
    )
    st.plotly_chart(post_per_authors_date_bar, key="post_per_authors_date_bar")

    st.sidebar.html('<a href="http://google.com">Google</a>')


posts_analysis()
