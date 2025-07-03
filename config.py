import streamlit as st

# Configuration de l'application
class Config:
    # Paramètres MongoDB
    MONGODB_DB_NAME = "apocalipssi_db"
    MONGODB_LOGS_COLLECTION = "activity_logs"
    MONGODB_SESSIONS_COLLECTION = "sessions"
    MONGODB_USERS_COLLECTION = "users"
    
    # Paramètres de logging
    MAX_LOG_ENTRIES = 50
    LOG_DISPLAY_LIMIT = 20
    
    # Paramètres de session
    SESSION_TIMEOUT_HOURS = 24
    
    # Paramètres d'API
    MAX_TEXT_LENGTH = 3000
    MAX_QUESTION_LENGTH = 100
    
    # Paramètres d'authentification
    MIN_PASSWORD_LENGTH = 6
    SESSION_TIMEOUT = 24  # heures
    
    # Paramètres d'interface
    SIDEBAR_TITLE = "📊 Logs et Session"
    MAIN_TITLE = "Analyse des fichiers"
    
    # Paramètres d'authentification
    MIN_PASSWORD_LENGTH = 8
    PASSWORD_REQUIREMENTS = {
        "min_length": 8,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digit": True
    }
    
    @staticmethod
    def get_mongodb_connection_string():
        """Récupère la chaîne de connexion MongoDB depuis les secrets"""
        return st.secrets["mongodb"]["connection_string"]
    
    @staticmethod
    def get_huggingface_api_key():
        """Récupère la clé API Hugging Face depuis les secrets"""
        return st.secrets["huggingface"]["api_key"] 