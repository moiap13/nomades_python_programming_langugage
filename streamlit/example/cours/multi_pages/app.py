# app.py
import streamlit as st
st.title("Mon Application Streamlit")
st.write("Ceci est une application Streamlit avec une configuration personnalisée.")
st.page_link("./pages/page1.py", label="Page 1")
st.page_link("./pages/page2.py", label="Page 2")