# import streamlit as st

# st.title("Welcome to the streamlit chapter")
# st.write("This part is about creating interractive website using streamlit")

# if st.button("Cliquez-moi"):
#     st.write("Bouton cliqué!")

# age = st.slider("Âge", 0, 100, 25)
# st.write(f"Vous avez {age} ans")

# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np

# st.title("Graphique interactif")

# # 1. Le widget crée une variable qui change à chaque interaction
# amplitude = st.slider("Amplitude", 0.1, 5.0, 1.0)

# # 2. On utilise cette variable pour générer les données
# x = np.linspace(0, 10, 100)
# y = amplitude * np.sin(x)

# # 3. Le graphique est recréé à chaque modification du slider
# fig, ax = plt.subplots()
# ax.plot(x, y)
# ax.set_ylim(-5, 5)
# st.pyplot(fig)

# Demonstration des éléments textuels
# import streamlit as st

# st.title("Titre principal - st.title()")
# st.header("En-tête - st.header()")
# st.subheader("Sous-en-tête - st.subheader()")
# st.text("Texte simple - st.text()")
# st.markdown("**Gras** et *italique* avec `st.markdown()`")
# st.caption("Légende - st.caption()")
# st.code("print('Hello World')", language="python")

# import streamlit as st

# # Compteur qui s'incrémente à chaque clic
# if 'clicks' not in st.session_state:
#     st.session_state.clicks = 0

# def increment():
#     st.session_state.clicks += 1

# # Bouton avec callback (fonction appelée au clic)
# st.button('Cliquez-moi', on_click=increment)
# st.write(f'Nombre de clics: {st.session_state.clicks}')

# # Case à cocher
# show_secret = st.checkbox('Afficher le secret')
# if show_secret:
#     st.write('🎉 Le secret: Streamlit ré-exécute tout le script à chaque interaction!')

# import streamlit as st

# # Radio - boutons radio
# option_radio = st.radio(
#     'Choisissez une option:',
#     ('Option A', 'Option B', 'Option C'), index=1
# )
# print(option_radio)
# st.write(f'Vous avez choisi: {option_radio}')

# # Selectbox - liste déroulante
# option_select = st.selectbox(
#     'Choisissez une option:',
#     ['Option X', 'Option Y', 'Option Z'], index=2
# )
# if option_select == "Option X":
#   st.write("X selected")
# st.write(f'Vous avez choisi: {option_select}')

# # Curseur avec intervalle
# range_values = st.slider(
#     'Sélectionnez un intervalle:',
#     0, 100, (25, 75)
# )
# st.write(f'Intervalle: {type(range_values)}')

# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title("Affichage conditionnel")

# # Checkbox pour afficher/masquer les données
# show_data = st.checkbox("Afficher les données détaillées")

# # Checkbox pour afficher/masquer le graphique
# show_chart = st.checkbox("Afficher le graphique")

# # Générer des données
# df = pd.DataFrame({
#     'x': range(50),
#     'y': np.random.randn(50).cumsum()
# })

# # Afficher selon l'état des checkboxes
# if show_data:
#     st.subheader("Données")
#     st.dataframe(df)

# if show_chart:
#     st.subheader("Graphique")
#     st.line_chart(df.set_index('x')['y'])

# st.write("---")
# st.write(f"Données affichées: {show_data}, Graphique affiché: {show_chart}")

# import streamlit as st

# # Champ de texte
# nom = st.text_input('Entrez votre nom:', 'John Doe')
# st.write(f'Bonjour, {nom}!')

# # Champ numérique
# nombre = st.number_input('Entrez un nombre:', min_value=0, max_value=100, value=50, step=5)
# st.write(f'Nombre sélectionné: {nombre}')

# # Champ numérique décimal
# prix = st.number_input('Entrez un prix (€):', min_value=0.0, max_value=1000.0, value=10.0, step=0.005, format="%.2f")
# st.write(f'Prix: {prix} €')

# import streamlit as st

# # Sélection multiple
# options = st.multiselect(
#     'Quels fruits aimez-vous?',
#     ['Pomme', 'Banane', 'Orange', 'Fraise', 'Raisin'],
#     default=['Pomme', 'Banane']
# )
# for fruit in options:
#   st.write(f'Vous avez choisi: {fruit}')

# # Sélecteur de couleur
# couleur = st.color_picker('Choisissez une couleur:', '#00f900')
# st.write(f'Couleur sélectionnée: {couleur}')

# import streamlit as st

# # Ajouter des widgets dans la sidebar
# st.sidebar.title('Navigation')
# st.sidebar.markdown('---')

# page = st.sidebar.radio(
#     'Aller à:',
#     ['Accueil', 'Analyse', 'Paramètres']
# )

# # Sélection multiple
# options = st.sidebar.multiselect( 
#     'Quels fruits aimez-vous?',
#     ['Pomme', 'Banane', 'Orange', 'Fraise', 'Raisin'],
#     default=['Pomme', 'Banane']
# )

# st.sidebar.markdown('---')
# st.sidebar.write('Version 1.0.0')

# # Contenu principal
# st.title(f'Page: {page}')
# st.write(f'Vous êtes sur la page {page}')
# for fruit in options:
#   st.write(f'Vous avez choisi: {fruit}')

# import streamlit as st

# # Créer 3 colonnes
# col1, col2, col3 = st.columns([0.5, 0.25, 0.25])

# with col1:
#     st.header('Colonne 1')
#     st.write('Contenu de la colonne 1')
#     st.button('Bouton 1')

# with col2:
#     st.header('Colonne 2')
#     st.write('Contenu de la colonne 2')
#     st.button('Bouton 2')

# with col3:
#     st.header('Colonne 3')
#     st.write('Contenu de la colonne 3')
#     st.button('Bouton 3')

# import streamlit as st

# # Expander simple
# with st.expander('Cliquez pour expand'):
#     st.write('Contenu hidden!')
#     st.write('Plus de contenu...')

# # Plusieurs expanders
# with st.expander('Section A'):
#     st.write('Contenu de la section A')

# with st.expander('Section B'):
#     st.write('Contenu de la section B')

# with st.expander('Section C'):
#     st.write('Contenu de la section C')

# import streamlit as st

# # Créer des onglets
# tab1, tab2, tab3 = st.tabs(['Accueil', 'Analyse', 'Statistiques'])

# with tab1:
#     st.header('Accueil')
#     st.write('Bienvenue sur la page d\'accueil!')

# with tab2:
#     st.header('Analyse')
#     st.write('Page danalyse des données')

# with tab3:
#     st.header('Statistiques')
#     st.write('Quelques statistiques...')

# import streamlit as st
# import pandas as pd

# # Créer un DataFrame d'exemple
# data = pd.DataFrame({
#     'Nom': ['Alice', 'Bob', 'Charlie'],
#     'Âge': [25, 30, 35],
#     'Ville': ['Paris', 'Lyon', 'Marseille']
# })

# st.dataframe(data)
# st.table(data)

# import streamlit as st

# # Métriques simples
# st.metric(label='Ventes totales', value='1,234,567 €', delta='+12.5%')
# st.metric(label='Utilisateurs actifs', value='8,432', delta='-2.3%', delta_color='inverse')
# st.metric(label='Taux de conversion', value='4.2%', delta='+0.5%', delta_color="inverse")

# import streamlit as st
# import requests

# if st.button("Fetch Data"):
#     users = requests.get("https://jsonplaceholder.typicode.com/users").json()
#     st.json(users)

# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np

# st.write("**Modifiez les valeurs ci-dessous et observez le graphique se mettre à jour!**")

# # Ces variables prennent les valeurs des widgets
# amplitude = st.slider('Amplitude du sinus', 0.1, 3.0, 1.0, 0.1)
# frequence = st.slider('Fréquence', 1, 10, 1)
# phase = st.slider('Phase (degrés)', 0, 360, 0)

# # Génération des données basée sur les valeurs des widgets
# x = np.linspace(0, 4 * np.pi, 200)
# y = amplitude * np.sin(frequence * x + np.radians(phase))

# # Création et affichage du graphique
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(x, y, 'b-', linewidth=2)
# ax.axhline(y=0, color='k', linewidth=0.5)
# ax.set_xlim(0, 4 * np.pi)
# ax.set_ylim(-4, 4)
# ax.set_xlabel('x')
# ax.set_ylabel('sin(x)')
# ax.set_title(f'sin(x) avec amplitude={amplitude}, fréquence={frequence}, phase={phase}°')
# ax.grid(True, alpha=0.3)

# st.pyplot(fig)

# import streamlit as st
# import plotly.express as px

# # Données d'exemple
# df = px.data.iris()

# # Créer un scatter plot
# fig = px.scatter(
#     df,
#     x='sepal_width',
#     y='sepal_length',
#     color='species',
#     title='Iris Dataset'
# )

# # Afficher dans Streamlit
# st.plotly_chart(fig)

# import streamlit as st
# import plotly.express as px

# # Graphique en barres
# df = px.data.tips()

# fig = px.bar(
#     df,
#     x='day',
#     y='total_bill',
#     color='sex',
#     title='Total des factures par jour'
# )

# st.plotly_chart(fig)

# import streamlit as st
# import time

# @st.cache_data
# def fonction_lente():
#     time.sleep(2)  # Simule un calcul long
#     return 'Résultat'

# if st.button('Exécuter'):
#     result = fonction_lente()
#     st.write(f'Résultat: {result}')

# import streamlit as st
# import pandas as pd

# # Upload de fichier CSV
# uploaded_file = st.file_uploader('Choisissez un fichier CSV', type=['csv'])

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     st.dataframe(df)
#     st.write(f'Nombre de lignes: {df.shape[0]}')
#     st.write(f'Nombre de colonnes: {df.shape[1]}')

# import streamlit as st

# # Créer un formulaire
# with st.form(key='my_form'):
#     name = st.text_input('Nom')
#     email = st.text_input('Email')
#     submit = st.form_submit_button('Soumettre')

# if submit:
#     st.success(f"Merci {name}! Votre email: {email}")

# import streamlit as st

# st.success('Opération réussie!')
# st.info('Information importante')
# st.warning('Attention: quelque chose ne va pas')
# st.error('Une erreur est survenue!')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

import streamlit as st

# Configuration de la page (DOIT ÊTRE EN PREMIER)
st.set_page_config(
    page_title='Mon Application',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("Application d'Analyse de Données")

# ============================================
# SECTION 1: Sidebar pour les contrôles
# ============================================
st.sidebar.title("Paramètres")
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier CSV", type=['csv'])

# ============================================
# SECTION 2: Contenu principal
# ============================================
if uploaded_file is not None:
    # Lire les données
    df = pd.read_csv(uploaded_file)
    
    # Afficher les données
    st.header("Données")
    st.dataframe(df.head(100))
    
    # Statistiques avec colonnes
    st.header("Statistiques")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", df.shape[0])
    col2.metric("Colonnes", df.shape[1])
    col3.metric("Valeurs manquantes", df.isnull().sum().sum())
    
    # Sélection de colonne pour le graphique
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        # Le selectbox retourne la colonne choisie
        col_select = st.selectbox("Sélectionnez une colonne numérique:", numeric_cols)
        
        # Le slider contrôle le nombre de bins
        bins = st.slider("Nombre de bins", 5, 100, 30)
        
        # Le graphique se met à jour automatiquement
        st.header(f"Distribution de {col_select}")
        
        fig, ax = plt.subplots()
        ax.hist(df[col_select].dropna(), bins=bins, edgecolor='black')
        ax.set_xlabel(col_select)
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)
else:
    st.info("Téléchargez un fichier CSV pour commencer.")

# ============================================
# L'application se ré-exécute entièrement à chaque modification
# ============================================