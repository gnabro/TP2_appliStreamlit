import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.auth import require_auth
from utils.prediction_utils import make_prediction, model

# =========================
# PROTECTION
# =========================

require_auth()

# =========================
# INTERFACE
# =========================

st.title("🤖 Prédiction de Réussite Étudiante")
st.markdown(
    "Renseignez le profil complet de l'étudiant. "
    "Le modèle **Random Forest** (F1 = 0.77) prédit la probabilité de réussite."
)

if model is None:
    st.error(
        "⚠ Modèle introuvable. "
        "Vérifiez que `models/meilleur_modele_avec_selection.pkl` est bien présent."
    )
    st.stop()

st.divider()

# =========================
# FORMULAIRE
# Colonnes originales du dataset data_etudiants.csv :
# school, sex, age, address, famsize, Pstatus,
# Medu, Fedu, Mjob, Fjob, reason, guardian,
# traveltime, studytime, failures, schoolsup, famsup,
# paid, activities, nursery, higher, internet, romantic,
# famrel, freetime, goout, Dalc, Walc, health, absences
# =========================

# ---- Bloc 1 : Identité & famille ----
st.subheader("👤 Identité & famille")
c1, c2, c3 = st.columns(3)

with c1:
    school  = st.selectbox("École",           ["GP", "MS"],
                           help="GP = Gabriel Pereira · MS = Mousinho da Silveira")
    sex     = st.selectbox("Sexe",             ["M", "F"])
    age     = st.number_input("Âge",           min_value=15, max_value=22, value=17, step=1)
    address = st.selectbox("Milieu",           ["U", "R"],
                           help="U = Urbain · R = Rural")

with c2:
    famsize = st.selectbox("Taille famille",   ["GT3", "LE3"],
                           help="GT3 = >3 personnes · LE3 = ≤3 personnes")
    Pstatus = st.selectbox("Statut parental",  ["T", "A"],
                           help="T = Ensemble · A = Séparés")
    Medu    = st.selectbox("Éducation mère",   [0, 1, 2, 3, 4], index=2,
                           help="0=aucune · 1=primaire · 2=collège · 3=lycée · 4=supérieur")
    Fedu    = st.selectbox("Éducation père",   [0, 1, 2, 3, 4], index=2,
                           help="0=aucune · 1=primaire · 2=collège · 3=lycée · 4=supérieur")

with c3:
    Mjob    = st.selectbox("Emploi mère",      ["teacher", "health", "services", "at_home", "other"])
    Fjob    = st.selectbox("Emploi père",      ["teacher", "health", "services", "at_home", "other"])
    reason  = st.selectbox("Raison choix école", ["home", "reputation", "course", "other"])
    guardian = st.selectbox("Tuteur légal",    ["mother", "father", "other"])

st.divider()

# ---- Bloc 2 : Vie scolaire ----
st.subheader("📚 Vie scolaire")
c4, c5, c6 = st.columns(3)

with c4:
    traveltime = st.selectbox(
        "Temps de trajet",  [1, 2, 3, 4], index=0,
        help="1 = <15 min · 2 = 15-30 min · 3 = 30-60 min · 4 = >60 min"
    )
    studytime  = st.selectbox(
        "Heures d'étude / semaine", [1, 2, 3, 4], index=1,
        help="1 = <2h · 2 = 2-5h · 3 = 5-10h · 4 = >10h"
    )
    failures   = st.number_input(
        "Échecs passés (nb matières)", min_value=0, max_value=4, value=0, step=1
    )
    absences   = st.number_input(
        "Nombre d'absences",          min_value=0, max_value=93, value=4, step=1
    )

with c5:
    schoolsup = st.selectbox("Soutien scolaire extra",         ["yes", "no"])
    famsup    = st.selectbox("Soutien familial aux devoirs",   ["yes", "no"])
    paid      = st.selectbox("Cours particuliers payants",     ["yes", "no"])
    activities = st.selectbox("Activités parascolaires",       ["yes", "no"])

with c6:
    nursery   = st.selectbox("A fréquenté une garderie",       ["yes", "no"])
    higher    = st.selectbox("Veut faire des études supérieures", ["yes", "no"])
    internet  = st.selectbox("Accès internet à la maison",     ["yes", "no"])
    romantic  = st.selectbox("En relation amoureuse",          ["yes", "no"])

st.divider()

# ---- Bloc 3 : Mode de vie ----
st.subheader("🎯 Mode de vie")
c7, c8 = st.columns(2)

with c7:
    famrel   = st.slider("Qualité relations familiales (1–5)",   1, 5, 4)
    freetime = st.slider("Temps libre après l'école (1–5)",      1, 5, 3)
    goout    = st.slider("Sorties avec amis (1–5)",              1, 5, 3)

with c8:
    Dalc     = st.slider("Alcool en semaine (1–5)",              1, 5, 1)
    Walc     = st.slider("Alcool le weekend (1–5)",              1, 5, 1)
    health   = st.slider("État de santé général (1–5)",          1, 5, 3)

st.divider()

# =========================
# LANCEMENT PREDICTION
# =========================

if st.button("🔍 Lancer la prédiction", use_container_width=True):

    raw_input = {
        "school": school,   "sex": sex,         "age": age,
        "address": address, "famsize": famsize, "Pstatus": Pstatus,
        "Medu": Medu,       "Fedu": Fedu,
        "Mjob": Mjob,       "Fjob": Fjob,
        "reason": reason,   "guardian": guardian,
        "traveltime": traveltime, "studytime": studytime,
        "failures": failures,
        "schoolsup": schoolsup, "famsup": famsup,
        "paid": paid,       "activities": activities,
        "nursery": nursery, "higher": higher,
        "internet": internet, "romantic": romantic,
        "famrel": famrel,   "freetime": freetime,
        "goout": goout,     "Dalc": Dalc, "Walc": Walc,
        "health": health,   "absences": absences,
    }

    prediction, probabilities = make_prediction(raw_input)

    if prediction is None:
        st.error("Erreur lors de la prédiction. Vérifiez que le modèle est bien chargé.")
        st.stop()

    # ---- Résultat ----
    st.subheader("📊 Résultats")
    col_res, col_chart = st.columns([1, 2])

    with col_res:
        if prediction == 1:
            st.success("✅ **Réussite prédite**")
            label_pred = "Réussite"
        else:
            st.error("❌ **Échec prédit**")
            label_pred = "Échec"

        st.metric("Prédiction",           label_pred)
        st.metric("Confiance du modèle",  f"{max(probabilities)*100:.1f} %")

    # ---- Graphique probabilités ----
    with col_chart:
        fig = go.Figure(go.Bar(
            x=["Échec", "Réussite"],
            y=[probabilities[0] * 100, probabilities[1] * 100],
            marker_color=["#ef4444", "#22c55e"],
            text=[f"{probabilities[0]*100:.1f}%", f"{probabilities[1]*100:.1f}%"],
            textposition="outside",
            width=0.4,
        ))
        fig.update_layout(
            title="Probabilités par classe (%)",
            yaxis=dict(range=[0, 115], title="Probabilité (%)"),
            xaxis_title="Classe",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(t=50, b=30, l=20, r=20),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---- Variables calculées (feature engineering) ----
    with st.expander("🔧 Variables calculées automatiquement (feature engineering)"):
        fe_data = {
            "Variable": [
                "academic_risk",
                "family_support_score",
                "alcohol_score",
                "age_failures",
                "absences_capped",
            ],
            "Valeur": [
                int(failures > 0 and studytime <= 2),
                int(famsup == "yes") + int(paid == "yes") + int(activities == "yes"),
                round((Dalc + Walc) / 2, 2),
                age * failures,
                min(absences, 30),
            ],
            "Description": [
                "1 si échecs > 0 ET étude ≤ 2h/sem",
                "Somme soutien fam. + cours payants + activités",
                "Moyenne alcool semaine / weekend",
                "Âge × nombre d'échecs passés",
                "Absences plafonnées à 30",
            ],
        }
        st.table(pd.DataFrame(fe_data))

    # ---- Récapitulatif saisie ----
    with st.expander("📋 Récapitulatif des données saisies"):
        recap = {k: [v] for k, v in raw_input.items()}
        st.dataframe(
            pd.DataFrame(recap).T.rename(columns={0: "Valeur"}),
            use_container_width=True
        )

# =========================
# NAVIGATION
# =========================

st.divider()

if st.button("⬅️ Retour au tableau de bord"):
    st.switch_page("pages/tableau_de_bord.py")