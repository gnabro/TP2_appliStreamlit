# Importation de la bibliothèque Streamlit
# Permet de créer l'interface web interactive de l'application
import streamlit as st

# Importation de la fonction login depuis le fichier auth.py
# Cette fonction gère l'authentification des utilisateurs
from utils.auth import login 

# =====================================================
# CONFIGURATION DE LA PAGE STREAMLIT
# =====================================================

# Définition des paramètres principaux de l'application
st.set_page_config(

    # Titre affiché dans l'onglet du navigateur
    page_title="Application Étudiants",

    # Icône affichée dans l'onglet du navigateur
    page_icon="🎓",

    # Mise en page large (utilise toute la largeur de l'écran)
    layout="wide",

    # Sidebar fermée par défaut au lancement
    initial_sidebar_state="collapsed"
)

# =====================================================
# GESTION DE LA SESSION UTILISATEUR
# =====================================================

# Vérifie si la variable "authenticated"
# existe déjà dans la session Streamlit
if "authenticated" not in st.session_state:

    # Si elle n'existe pas :
    # on initialise l'état d'authentification à False
    # => utilisateur NON connecté
    st.session_state.authenticated = False

# =========================
# STYLE CSS
# =========================

st.markdown("""
<style>

/* Fond principal */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    color: white;
}

/* Titre principal */
.big-title {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
    color: white;
}

/* Sous titre */
.subtitle {
    font-size: 22px;
    text-align: center;
    color: #cbd5e1;
}

/* Carte */
.card {
    background-color: rgba(255,255,255,0.08);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(8px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

/* Boutons */
.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    background-color: #2563eb;
    color: white;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

/* Inputs */
.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.write("")
st.write("")

st.markdown("""
<div class="big-title">
🎓 Application de Prédiction de Réussite Étudiante
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="subtitle">
Analyse des données étudiantes, tableau de bord intelligent
et prédictions Machine Learning.
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")

# =========================
# DESCRIPTION
# =========================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.markdown("""
    <div class="card">

    <h3>Fonctionnalités</h3>

    <ul>
        <li>Authentification sécurisée</li>
        <li>Analyse exploratoire des données</li>
        <li>Rapports automatiques</li>
        <li>Prédictions Machine Learning</li>
        <li>Visualisations interactives</li>
        <li>Comparaison des modèles</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

# =========================
# LOGIN
# =========================

st.write("")
st.write("")

login()

# =========================
# FOOTER
# =========================

st.write("")
st.write("")
st.write("")

st.markdown("""
<hr>

<center>
Application développée avec Streamlit • Machine Learning • Data Science
</center>
""", unsafe_allow_html=True)