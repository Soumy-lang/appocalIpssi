import streamlit as st

# Configuration de l'application
class Config:
    # Paramètres MongoDB
    MONGODB_DB_NAME = "apocalipssi_db"
    MONGODB_LOGS_COLLECTION = "activity_logs"
    MONGODB_SESSIONS_COLLECTION = "sessions"
    
    # Paramètres de logging
    MAX_LOG_ENTRIES = 50
    LOG_DISPLAY_LIMIT = 20
    
    # Paramètres de session
    SESSION_TIMEOUT_HOURS = 24
    
    # Paramètres d'API
    MAX_TEXT_LENGTH = 3000
    MAX_QUESTION_LENGTH = 100
    
    # Paramètres d'interface
    SIDEBAR_TITLE = "📊 Logs et Session"
    MAIN_TITLE = "Analyse des fichiers"
    
    @staticmethod
    def get_mongodb_connection_string():
        """Récupère la chaîne de connexion MongoDB depuis les secrets"""
        return st.secrets["mongodb"]["connection_string"]
    
    @staticmethod
    def get_huggingface_api_key():
        """Récupère la clé API Hugging Face depuis les secrets"""
        return st.secrets["huggingface"]["api_key"] 