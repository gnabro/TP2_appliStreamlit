import os
import pandas as pd

from ydata_profiling import ProfileReport

import sweetviz as sv


# ==========================================
# CREATION DOSSIER REPORTS
# ==========================================

os.makedirs("reports", exist_ok=True)


# ==========================================
# GENERATION RAPPORT YDATA PROFILING
# ==========================================

def generate_profile_report(df):

    """
    Génère un rapport HTML avec YData Profiling
    """

    output_path = "reports/rapport.html"

    profile = ProfileReport(
        df,
        title="Rapport EDA",
        explorative=True
    )

    profile.to_file(output_path)

    return output_path


# ==========================================
# GENERATION RAPPORT SWEETVIZ
# ==========================================

def generate_sweetviz_report(df):

    """
    Génère un rapport HTML avec Sweetviz
    """

    output_path = "reports/rapport_sweetviz.html"

    report = sv.analyze(
        [df, "Dataset"]
    )

    report.show_html(
        output_path,
        open_browser=False
    )

    return output_path


# ==========================================
# GENERATION COMPLETE DES RAPPORTS
# ==========================================

def generate_all_reports(csv_path):

    """
    Charge le dataset puis génère tous les rapports
    """

    df = pd.read_csv(
        csv_path,
        encoding="utf-8",
        low_memory=False
    )

    profile_report = generate_profile_report(df)

    sweetviz_report = generate_sweetviz_report(df)

    return {
        "profile_report": profile_report,
        "sweetviz_report": sweetviz_report
    }