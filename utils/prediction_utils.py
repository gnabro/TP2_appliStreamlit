import os
import pickle
import numpy as np
import pandas as pd

# =========================
# CHEMINS
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "meilleur_modele_avec_selection.pkl")

# =========================
# CHARGEMENT MODELE
# =========================

def load_model():
    """
    Charge le modèle sauvegardé (dict contenant 'model')
    """
    if not os.path.exists(MODEL_PATH):
        return None

    try:
        with open(MODEL_PATH, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        print(f"Erreur chargement modèle : {e}")
        return None


model_info = load_model()

# on extrait le vrai modèle sklearn
model = model_info["model"] if model_info is not None else None


# =========================
# FEATURE ENGINEERING
# =========================

def apply_feature_engineering(row: dict) -> dict:
    """
    Reproduction EXACTE du feature engineering du notebook
    """

    row = row.copy()

    row["academic_risk"] = int(row["failures"] > 0 and row["studytime"] <= 2)

    row["family_support_score"] = (
        int(row["famsup"] == "yes") +
        int(row["paid"] == "yes") +
        int(row["activities"] == "yes")
    )

    row["alcohol_score"] = (row["Dalc"] + row["Walc"]) / 2

    row["age_failures"] = row["age"] * row["failures"]

    row["absences_capped"] = min(row["absences"], 30)

    return row


# =========================
# FEATURES ATTENDUES
# =========================

NUM_COLS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences",
    "academic_risk", "family_support_score", "alcohol_score",
    "age_failures", "absences_capped",
]

CAT_COLS = [
    "school", "sex", "address", "famsize", "Pstatus",
    "Mjob", "Fjob", "reason", "guardian",
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic",
]


# =========================
# PRÉDICTION
# =========================

def make_prediction(input_data):
    """
    Effectue une prédiction à partir des données du formulaire Streamlit.
    """

    if model is None:
        return None, None

    # feature engineering
    input_data = apply_feature_engineering(input_data)

    # dataframe
    df_input = pd.DataFrame([input_data])

    # sécurisation colonnes manquantes
    expected_cols = NUM_COLS + CAT_COLS
    for col in expected_cols:
        if col not in df_input.columns:
            df_input[col] = 0

    df_input = df_input[expected_cols]

    # prédiction
    prediction = model.predict(df_input)[0]
    probabilities = model.predict_proba(df_input)[0]

    return prediction, probabilities