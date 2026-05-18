import streamlit as st

# =========================
# VERIFICATION PASSWORD
# =========================

def check_password(password):
    """Vérifie le mot de passe contre le secret configuré."""
    try:
        return password == st.secrets["APP_PASSWORD"]
    except KeyError:
        st.error("Clé APP_PASSWORD absente dans .streamlit/secrets.toml")
        return False

# =========================
# PROTECTION PAGE
# =========================

def require_auth():
    """
    À appeler en haut de chaque page protégée.
    Redirige vers index.py si l'utilisateur n'est pas authentifié.
    """
    # Vérifie si l'utilisateur est authentifié dans la session Streamlit
    # st.session_state.get("authenticated", False)
    # → récupère la valeur de "authenticated"
    # → si la clé n'existe pas, retourne False par défaut
    if not st.session_state.get("authenticated", False):

        # Affiche un message d'avertissement dans l'application
        # pour informer que l'accès est refusé
        st.warning("🔒 Accès non autorisé. Veuillez vous connecter.")

        # Redirige automatiquement l'utilisateur
        # vers la page de connexion principale "index.py"
        st.switch_page("index.py")

        # Arrête immédiatement l'exécution du script actuel
        # afin d'empêcher l'accès au contenu protégé
        st.stop()
    

# =========================
# LOGIN
# =========================

def login():

    st.subheader("Connexion")

    password = st.text_input(
        "Mot de passe",
        type="password"
    )

    if st.button("Se connecter"):

        if check_password(password):

            st.session_state.authenticated = True

            st.success("Connexion réussie ✅")

            st.switch_page("pages/tableau_de_bord.py")

        else:

            st.error("Mot de passe incorrect ❌")
