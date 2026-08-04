import streamlit as st

st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="expanded")

st.title("Welcome to the Blog analysis tool")

# st.page_link("pages/authors.py", label="Authors analysis")
# st.page_link("pages/posts.py", label="Post analysis")
st.link_button("google", "https://google.com")