import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
CSV_FILE: str = os.path.join(CURR_DIR, "posts.csv")


def main():
    df = pd.read_csv(CSV_FILE)
    df.created_at = pd.to_datetime(df["created_at"]).dt.date

    st.title("Posts analysis")
    st.subheader("Post made by PPL_2025_0708 students")

    st.sidebar.title("Filters")
    authors = df.author.unique()
    selected_authors = st.sidebar.multiselect("Select Authors", authors, authors)

    df_filtered = df.loc[df.author.isin(selected_authors)]
    nb_rows = df_filtered.shape[0]

    st.sidebar.text(f"DF rows: {nb_rows}")

    st.dataframe(df_filtered)

    post_per_date = df_filtered.groupby("created_at").size()

    fig, ax = plt.subplots()

    ax.bar(post_per_date.index, post_per_date.values)
    ax.set_xticks(post_per_date.index)
    ax.set_xticklabels(post_per_date.index, rotation=90)
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of posts")

    st.pyplot(fig)


main()
