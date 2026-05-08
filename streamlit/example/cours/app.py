import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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