import datetime


import streamlit as st

# Métriques simples
st.metric(label='Ventes totales', value='1,234,567 CHF', delta='-0%')
st.metric(label='Utilisateurs actifs', value='8,432', delta='-2.3%', delta_color='inverse')
st.metric(label='Taux de conversion', value='4.2%', delta='-0.5%')

min_date = datetime.datetime.now() - datetime.timedelta(days=7)
max_date = datetime.datetime.now() + datetime.timedelta(days=7)

dates: tuple = st.date_input(
    "Select dates", [min_date, max_date], min_date, max_date
)

print(dates)