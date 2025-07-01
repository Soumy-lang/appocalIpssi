from pymongo import MongoClient
from datetime import datetime
import streamlit as st
from typing import Optional, Dict, List, Any
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class DatabaseManager:
    """Gestionnaire de base de données MongoDB pour l'application d'analyse de documents"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.documents_collection = None
        self.summaries_collection = None
        self.conversations_collection = None
        self._connect()
    
    def _connect(self) -> bool:
        """Établit la connexion à MongoDB Atlas"""
        try:
            # Utiliser les variables d'environnement pour la connexion MongoDB
            mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")
            if not mongo_uri:
                st.error("Variable d'environnement MONGODB_CONNECTION_STRING non définie")
                return False
                
            self.client = MongoClient(mongo_uri)
            # Test de connexion
            self.client.admin.command('ping')
            
            # Initialiser la base de données et les collections
            self.db = self.client['document_analyzer']
            self.documents_collection = self.db['documents']
            self.summaries_collection = self.db['summaries']
            self.conversations_collection = self.db['conversations']
            
            return True
        except Exception as e:
            st.error(f"Erreur de connexion MongoDB: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion à la base de données est active"""
        return self.client is not None
    
    def save_document(self, filename: str, content: str, num_pages: int, 
                     num_words: int, file_size: int) -> bool:
        """Sauvegarde un document dans la base de données"""
        if not self.is_connected():
            return False
        
        try:
            document_record = {
                "filename": filename,
                "content": content,
                "num_pages": num_pages,
                "num_words": num_words,
                "upload_date": datetime.now(),
                "file_size": file_size
            }
            
            # Vérifier si le document existe déjà
            existing_doc = self.documents_collection.find_one({"filename": filename})
            if existing_doc:
                # Mettre à jour le document existant
                self.documents_collection.update_one(
                    {"filename": filename},
                    {"$set": document_record}
                )
                st.success(f"Document {filename} mis à jour dans la base de données")
            else:
                # Insérer un nouveau document
                self.documents_collection.insert_one(document_record)
                st.success(f"Document {filename} sauvegardé dans la base de données")
            
            return True
        except Exception as e:
            st.warning(f"Erreur lors de la sauvegarde de {filename}: {e}")
            return False
    
    def save_summary(self, summaries: List[str], files_analyzed: List[str]) -> bool:
        """Sauvegarde les résumés générés"""
        if not self.is_connected():
            return False
        
        try:
            summary_record = {
                "timestamp": datetime.now(),
                "summaries": summaries,
                "files_analyzed": files_analyzed,
                "total_files": len(files_analyzed)
            }
            self.summaries_collection.insert_one(summary_record)
            st.success("Résumés sauvegardés dans la base de données")
            return True
        except Exception as e:
            st.warning(f"Erreur lors de la sauvegarde des résumés: {e}")
            return False
    
    def save_conversation(self, question: str, answer: str, 
                         files_referenced: List[str], session_id: int) -> bool:
        """Sauvegarde une conversation"""
        if not self.is_connected():
            return False
        
        try:
            conversation_record = {
                "timestamp": datetime.now(),
                "question": question,
                "answer": answer,
                "files_referenced": files_referenced,
                "session_id": session_id
            }
            self.conversations_collection.insert_one(conversation_record)
            return True
        except Exception as e:
            st.warning(f"Erreur lors de la sauvegarde de la conversation: {e}")
            return False
    
    def get_documents_count(self) -> int:
        """Retourne le nombre total de documents"""
        if not self.is_connected():
            return 0
        return self.documents_collection.count_documents({})
    
    def get_summaries_count(self) -> int:
        """Retourne le nombre total de résumés"""
        if not self.is_connected():
            return 0
        return self.summaries_collection.count_documents({})
    
    def get_conversations_count(self) -> int:
        """Retourne le nombre total de conversations"""
        if not self.is_connected():
            return 0
        return self.conversations_collection.count_documents({})
    
    def get_recent_documents(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retourne les documents les plus récents"""
        if not self.is_connected():
            return []
        return list(self.documents_collection.find().sort("upload_date", -1).limit(limit))
    
    def get_recent_conversations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retourne les conversations les plus récentes"""
        if not self.is_connected():
            return []
        return list(self.conversations_collection.find().sort("timestamp", -1).limit(limit))
    
    def get_document_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """Retourne un document par son nom de fichier"""
        if not self.is_connected():
            return None
        return self.documents_collection.find_one({"filename": filename})
    
    def delete_document(self, filename: str) -> bool:
        """Supprime un document de la base de données"""
        if not self.is_connected():
            return False
        try:
            result = self.documents_collection.delete_one({"filename": filename})
            return result.deleted_count > 0
        except Exception as e:
            st.error(f"Erreur lors de la suppression de {filename}: {e}")
            return False
    
    def close_connection(self):
        """Ferme la connexion à la base de données"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.documents_collection = None
            self.summaries_collection = None
            self.conversations_collection = None


# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager() 