import streamlit as st

st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Welcome to the Streamlit app")

st.page_link("pages/posts.py", "Posts analysis")
st.page_link("pages/authors.py", "Authors analysis")
