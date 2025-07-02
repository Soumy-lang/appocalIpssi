import pymongo
from datetime import datetime
import streamlit as st
from typing import Dict, Any, List

class DatabaseManager:
    def __init__(self):
        self.connection_string = st.secrets["mongodb"]["connection_string"]
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Établit la connexion à MongoDB"""
        try:
            self.client = pymongo.MongoClient(self.connection_string)

            self.db = self.client.apocalipssi_db
            # Test de connexion
            self.client.admin.command('ping')
            print("Connexion MongoDB réussie")
        except Exception as e:
            print(f"Erreur de connexion MongoDB: {e}")
            st.error(f"Erreur de connexion à la base de données: {e}")
    
    def get_current_timestamp(self):
        """Retourne le timestamp actuel"""
        return datetime.now()
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Crée un nouvel utilisateur"""
        try:
            if self.db is not None:
                result = self.db.users.insert_one(user_data)
                print(f"Utilisateur créé avec l'ID: {result.inserted_id}")
                return True
            else:
                print("Base de données non connectée")
                return False
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur: {e}")
            return False
    
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """Récupère un utilisateur par son email"""
        try:
            if self.db is not None:
                user = self.db.users.find_one({"email": email})
                return user
            else:
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None
    
    def update_last_login(self, user_id) -> bool:
        """Met à jour la dernière connexion d'un utilisateur"""
        try:
            if self.db is not None:
                result = self.db.users.update_one(
                    {"_id": user_id},
                    {"$set": {"last_login": self.get_current_timestamp()}}
                )
                return result.modified_count > 0
            else:
                return False
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la dernière connexion: {e}")
            return False
    
    def log_activity(self, activity_type: str, details: Dict[str, Any], user_id: str = "default"):
        """Enregistre une activité dans la base de données"""
        try:
            log_entry = {
                "timestamp": datetime.now(),
                "activity_type": activity_type,
                "user_id": user_id,
                "details": details
            }
            
            if self.db is not None:
                self.db.activity_logs.insert_one(log_entry)
                print(f"Log enregistré: {activity_type}")
            else:
                print("Base de données non connectée")
                
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du log: {e}")
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Récupère les logs récents"""
        try:
            if self.db is not None:
                logs = list(self.db.activity_logs.find().sort("timestamp", -1).limit(limit))

                return logs
            else:
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des logs: {e}")
            return []
    
    def save_session_data(self, session_id: str, data: Dict[str, Any]):
        """Sauvegarde les données de session"""
        try:
            if self.db is not None:
                self.db.sessions.update_one(
                    {"session_id": session_id},
                    {"$set": {"data": data, "last_updated": datetime.now()}},
                    upsert=True
                )
                print(f"Session sauvegardée: {session_id}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de session: {e}")
    
    def load_session_data(self, session_id: str) -> Dict[str, Any]:
        """Charge les données de session"""
        try:
            if self.db is not None:
                session = self.db.sessions.find_one({"session_id": session_id})
                if session:
                    return session.get("data", {})
            return {}
        except Exception as e:
            print(f"Erreur lors du chargement de session: {e}")
            return {}
    
    def close_connection(self):
        """Ferme la connexion MongoDB"""

        if self.client is not None:
            self.client.close()
            print("Connexion MongoDB fermée")

def format_log_entry(log_entry: Dict) -> str:
    """Formate une entrée de log pour l'affichage"""
    timestamp = log_entry.get("timestamp", "")
    if isinstance(timestamp, datetime):
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    activity_type = log_entry.get("activity_type", "")
    details = log_entry.get("details", {})
    
    return f"**{timestamp}** - {activity_type}: {details}" 