import streamlit as st

st.set_page_config(page_title="Home", layout="centered")

st.title("Welcome to the FlaskBlog analysis")

st.page_link("pages/posts.py", label="My post analysis")
st.page_link("pages/users.py", label="My post analysis")