import pytest
import streamlit as st

@pytest.fixture(autouse=True)
def init_session_state():
    """
    Fixture pytest automatique pour initialiser st.session_state
    avant chaque test, afin d'éviter les erreurs d'attribut manquant.
    """
    # Réinitialiser session_state pour garantir un dict vierge
    try:
        st.session_state.clear()
    except Exception:
        st.session_state = {}

    # Définir l'état d'authentification à True par défaut
    st.session_state["authenticated"] = True
    yield
    # Pas besoin de teardown spécifique

