import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.auth import require_auth

from utils.rapport_utils import (
    generate_profile_report,
    generate_sweetviz_report,
    generate_all_reports
)

# =====================================================
# CONFIGURATION PAGE
# =====================================================

st.set_page_config(
    page_title="Tableau de Bord",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# AUTHENTIFICATION
# =====================================================

require_auth()

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "data_etudiants.csv"
)

# =====================================================
# STYLE CSS
# =====================================================

###
st.markdown("""
<style>

/* Fond principal */
.stApp {
    background-color: #f5f7fa;
}

/* Cartes */
/* Cartes */
.metric-card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    text-align: center;

    /* Correction visibilité */
    color: #0f172a;
    opacity: 1;

    transition: all 0.2s ease-in-out;
}

/* Hover cartes */
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.12);
}

/* Valeurs métriques */
.metric-card h2 {
    color: #1e293b;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* Texte métriques */
.metric-card p {
    color: #64748b;
    font-size: 15px;
    font-weight: 500;
}

/* Titres */
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #1e293b;
}

/* Sous titres */
.section-title {
    font-size: 26px;
    font-weight: bold;
    color: #334155;
    margin-top: 20px;
}

/* =====================================================
   BOUTONS (VERSION AMÉLIORÉE)
===================================================== */

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 12px;

    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;

    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;

    border: none;
    box-shadow: 0 6px 15px rgba(37, 99, 235, 0.35);

    transition: all 0.25s ease-in-out;
}

/* Hover */
.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    box-shadow: 0 10px 20px rgba(29, 78, 216, 0.45);
}

/* Click */
.stButton > button:active {
    transform: scale(0.98);
    box-shadow: 0 4px 10px rgba(29, 78, 216, 0.3);
}

/* Boutons download (spécial Streamlit) */
.stDownloadButton > button {
    width: 100%;
    height: 48px;
    border-radius: 12px;

    font-weight: 700;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;

    border: none;
    box-shadow: 0 6px 15px rgba(16, 185, 129, 0.35);

    transition: all 0.25s ease-in-out;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #059669, #047857);
}

/* Boutons danger (optionnel si tu veux plus tard) */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #ef4444, #dc2626);
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CHARGEMENT DONNEES
# =====================================================

@st.cache_data
def load_data():

    if not os.path.exists(DATA_PATH):

        st.error(
            f"Fichier introuvable : {DATA_PATH}"
        )

        st.stop()

    df = pd.read_csv(
        DATA_PATH,
        sep=",",
        encoding="utf-8",
        low_memory=False
    )

    return df


df = load_data()


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
📊 Tableau de Bord 
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
Analyse exploratoire des données étudiantes,
génération de rapports automatiques et prédictions
Machine Learning.
""")

st.divider()


# =====================================================
# METRIQUES
# =====================================================

st.markdown("""
<div class="section-title">
Vue Générale
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{df.shape[0]}</h2>
        <p>Étudiants</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{df.shape[1]}</h2>
        <p>Variables</p>
    </div>
    """, unsafe_allow_html=True)

with col3:

    missing_values = df.isnull().sum().sum()

    st.markdown(f"""
    <div class="metric-card">
        <h2>{missing_values}</h2>
        <p>Valeurs Manquantes</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# APERCU DATASET
# =====================================================

st.write("")

st.markdown("""
<div class="section-title">
Aperçu du Dataset
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df.head(5),
    use_container_width=True
)

# =====================================================
# DESCRIPTION DES VARIABLES DU DATASET
# =====================================================
st.write("")

st.markdown("""
<div class="section-title">
📘 Description des Variables
</div>
""", unsafe_allow_html=True)

dataset_info = pd.DataFrame({
    "Variable": [
        "school", "sex", "age", "address", "famsize", "Pstatus",
        "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian",
        "traveltime", "studytime", "failures", "schoolsup",
        "famsup", "paid", "activities", "nursery", "higher",
        "internet", "romantic", "famrel", "freetime", "goout",
        "Dalc", "Walc", "health", "absences", "passed"
    ],

    "Description": [
        "École fréquentée",
        "Sexe de l'étudiant",
        "Âge de l'étudiant",
        "Type d'adresse du domicile",
        "Taille de la famille",
        "Statut de cohabitation des parents",

        "Niveau d'éducation de la mère",
        "Niveau d'éducation du père",

        "Profession de la mère",
        "Profession du père",

        "Raison du choix de l'école",
        "Tuteur légal de l'étudiant",

        "Temps de trajet domicile-école",
        "Temps d'étude hebdomadaire",
        "Nombre d'échecs scolaires passés",

        "Soutien scolaire supplémentaire",
        "Soutien éducatif familial",
        "Cours particuliers payants",

        "Activités parascolaires",
        "A fréquenté une garderie",
        "Souhaite poursuivre des études supérieures",

        "Accès Internet à la maison",
        "Relation amoureuse",

        "Qualité des relations familiales",
        "Temps libre après l'école",
        "Sorties avec les amis",

        "Consommation d'alcool en semaine",
        "Consommation d'alcool le week-end",

        "État de santé actuel",
        "Nombre d'absences scolaires",

        "Réussite à l'examen final"
    ],

    "Type": [
        "Binaire", "Binaire", "Numérique", "Binaire", "Binaire", "Binaire",

        "Numérique", "Numérique",

        "Catégorielle", "Catégorielle", "Catégorielle", "Catégorielle",

        "Numérique", "Numérique", "Numérique",

        "Binaire", "Binaire", "Binaire",

        "Binaire", "Binaire", "Binaire",

        "Binaire", "Binaire",

        "Numérique", "Numérique", "Numérique",

        "Numérique", "Numérique",

        "Numérique", "Numérique",

        "Variable cible"
    ],

    "Valeurs possibles": [
        "GP, MS",
        "F, M",
        "15 à 22",

        "U = Urbain, R = Rural",

        "LE3 ≤ 3 pers., GT3 > 3 pers.",

        "T = Ensemble, A = Séparés",

        "0 à 4",
        "0 à 4",

        "teacher, health, services, at_home, other",
        "teacher, health, services, at_home, other",

        "home, reputation, course, other",

        "mother, father, other",

        "1 à 4",
        "1 à 4",
        "0 à 4",

        "yes / no",
        "yes / no",
        "yes / no",

        "yes / no",
        "yes / no",
        "yes / no",

        "yes / no",
        "yes / no",

        "1 à 5",
        "1 à 5",
        "1 à 5",

        "1 à 5",
        "1 à 5",

        "1 à 5",
        "0 à 93",

        "yes / no"
    ]
})

st.dataframe(
    dataset_info,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# STATISTIQUES
# =====================================================

st.write("")

st.markdown("""
<div class="section-title">
Statistiques Descriptives
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df.describe(),
    use_container_width=True
)

# =====================================================
# VISUALISATIONS
# =====================================================

st.write("")

st.markdown("""
<div class="section-title">
Visualisations
</div>
""", unsafe_allow_html=True)

numeric_cols = df.select_dtypes(
    include=['int64', 'float64']
).columns

selected_col = st.selectbox(
    "Choisir une variable numérique",
    numeric_cols
)

col1, col2 = st.columns(2)

# Histogramme
with col1:

    fig, ax = plt.subplots(figsize=(6,4))

    sns.histplot(
        df[selected_col],
        kde=True,
        ax=ax
    )

    ax.set_title(
        f"Distribution de {selected_col}"
    )

    st.pyplot(fig)

# Boxplot
with col2:

    fig, ax = plt.subplots(figsize=(6,4))

    sns.boxplot(
        y=df[selected_col],
        ax=ax
    )

    ax.set_title(
        f"Boxplot de {selected_col}"
    )

    st.pyplot(fig)

# =====================================================
# MATRICE CORRELATION
# =====================================================

st.write("")

st.markdown("""
<div class="section-title">
Matrice de Corrélation
</div>
""", unsafe_allow_html=True)

corr = df[numeric_cols].corr()

fig, ax = plt.subplots(
    figsize=(12,8)
)

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=True,
    ax=ax
)

ax.set_title(
    "Corrélation des Variables"
)

st.pyplot(fig)

# =====================================================
# RAPPORTS AUTOMATIQUES
# =====================================================

st.write("")

st.markdown("""
<div class="section-title">
Rapports Automatiques
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# -----------------------------------------------------
# YDATA PROFILING
# -----------------------------------------------------

with col1:

    st.subheader("YData Profiling")

    st.write("""
    Rapport exploratoire avancé :
    statistiques, corrélations,
    valeurs manquantes, distributions.
    """)

    if st.button(
        "Generer Rapport Profiling"
    ):

        with st.spinner(
            "Generation du rapport Profiling..."
        ):

            output_path = generate_profile_report(df)

        st.success(
            "Rapport Profiling genere"
        )

        with open(output_path, "rb") as file:

            st.download_button(
                label="Telecharger Rapport Profiling",
                data=file,
                file_name="rapport.html",
                mime="text/html"
            )

# -----------------------------------------------------
# SWEETVIZ
# -----------------------------------------------------

with col2:

    st.subheader("Sweetviz")

    st.write("""
    Analyse visuelle automatique
    avec graphiques interactifs
    et insights statistiques.
    """)

    if st.button(
        "Generer Rapport Sweetviz"
    ):

        with st.spinner(
            "Generation du rapport Sweetviz..."
        ):

            output_path = generate_sweetviz_report(df)

        st.success(
            "Rapport Sweetviz genere"
        )

        with open(output_path, "rb") as file:

            st.download_button(
                label="Telecharger Rapport Sweetviz",
                data=file,
                file_name="rapport_sweetviz.html",
                mime="text/html"
            )

# =====================================================
# GENERATION COMPLETE
# =====================================================

st.write("")

if st.button(
    "Generer Tous Les Rapports"
):

    with st.spinner(
        "Generation complete des rapports..."
    ):

        reports = generate_all_reports(
            DATA_PATH
        )

    st.success(
        "Tous les rapports ont ete generes"
    )

# =====================================================
# NAVIGATION
# =====================================================

st.divider()

st.markdown("""
<div class="section-title">
Prediction Machine Learning
</div>
""", unsafe_allow_html=True)

st.write("""
Acceder au modele de prediction
de la reussite etudiante.
""")

if st.button(
    "Aller a la page Prediction"
):

    st.switch_page(
        "pages/prediction.py"
    )