import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Users Analysis", layout="wide")

st.title("User Analysis")
st.write("Welcome to this user analysis")

def load_data() -> pd.DataFrame:
  df = pd.read_csv("data/users.csv")
  df["date_of_birth"] = pd.to_datetime(df.date_of_birth).dt.date
  return df

def user_analysis() -> None:
  df = load_data()

  st.sidebar.header("Filters")
  users_options: list[str] = list(df["firstname"] + " " + df.lastname)
  users_default: list[str] = list(df.loc[df.gender == "female"]["firstname"] + " " + df.loc[df.gender == "female"].lastname) 
  users: list[str] = st.sidebar.multiselect("Select users", options=users_options, default=users_default)
  
  users_firstnames: list[str] = [user_full_name.split(" ")[0] for user_full_name in users]
  users_lastnames: list[str] = [user_full_name.split(" ")[1] for user_full_name in users]
  filtered_df = df.loc[df.firstname.isin(users_firstnames) & df.lastname.isin(users_lastnames)]


  st.dataframe(filtered_df)

  gender = filtered_df['gender'].value_counts()

  gender_pie = px.pie(
    gender, values=gender.values, names=gender.index
  )

  st.plotly_chart(gender_pie)

user_analysis()