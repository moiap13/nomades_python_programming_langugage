from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px

def load_data() -> pd.DataFrame:
  df = pd.read_csv("data/authors_posts.csv")
  df["date"] = pd.to_datetime(df.date).dt.date
  df.drop(columns=["Unnamed: 0", "authors", "created_at"], inplace=True)
  return df

def post_analysis() -> None:
  df = load_data()

  min_date: datetime = df.date.min()
  max_date: datetime = df.date.max()
  
  st.sidebar.header("Filter by date")
  selected_dates: tuple[datetime, datetime] = st.sidebar.date_input("Select dates", [min_date, max_date], min_value=min_date, max_value=max_date)

  try:
    filtered_df = df[df.date.between(selected_dates[0], selected_dates[1])]
  except:
    st.error("Please select a date range")
    filtered_df = df

  authors: list[str] = list(df.iloc[0, 3:].index)
  selected_authors: list[str] = st.sidebar.multiselect("Select authors", options=authors, default=authors)

  filtered_df = filtered_df.loc[:, ["date"]+selected_authors]

  st.dataframe(filtered_df)

  posts_per_date = filtered_df.set_index("date").sum(axis=1).map(lambda v: 1 if v > 0 else 0).groupby("date").sum().reset_index(name="count")

  post_per_date_line = px.line(
    posts_per_date, x="date", y="count"
  )

  post_per_date_bar = px.bar(
    posts_per_date, x="date", y="count" 
  )

  df_authors = filtered_df.set_index("date")
  df_authors = df_authors.groupby("date").sum().cumsum()

  post_per_user_cumulative = px.area(
    df_authors, x=df_authors.index, y=df_authors.columns
  )

  st.plotly_chart(post_per_date_line)
  st.plotly_chart(post_per_date_bar)
  st.plotly_chart(post_per_user_cumulative)


############################## MAIN ###############################
st.set_page_config(page_title="Posts Analysis", layout="wide")

st.title("Post Analysis")
st.write("Welcome to this post analysis")
st.markdown("""
## SubTitle
            
- `Date`: the date for a post
> All the users are column in the dataset and we store 1 or 0 if the posted for that posts

""")
st.image("imgs/cumsum_result.png")

post_analysis()
