import streamlit as st

st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="expanded")

st.title("Sales analysis tool")

st.page_link("pages/employee.py", label="Employee Analysis")
st.page_link("pages/sales.py", label="Sales analysis")
