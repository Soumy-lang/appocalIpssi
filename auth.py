import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from utils import DatabaseManager
from config import Config

class AuthManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.session_timeout = timedelta(hours=24)
    
    def hash_password(self, password: str) -> str:
        """Hash un mot de passe avec salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Vérifie un mot de passe contre son hash"""
        try:
            salt, hash_value = hashed_password.split('$')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Inscrit un nouvel utilisateur"""
        try:
            # Vérifier si l'utilisateur existe déjà
            if self.db.db is not None:
                existing_user = self.db.db.users.find_one({
                    "$or": [
                        {"username": username},
                        {"email": email}
                    ]
                })
                
                if existing_user:
                    return {
                        "success": False,
                        "message": "Un utilisateur avec ce nom d'utilisateur ou cet email existe déjà."
                    }
                
                # Créer le nouvel utilisateur
                hashed_password = self.hash_password(password)
                user_data = {
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                    "created_at": datetime.now(),
                    "last_login": None,
                    "is_active": True
                }
                
                result = self.db.db.users.insert_one(user_data)
                
                if result.inserted_id:
                    return {
                        "success": True,
                        "message": "Inscription réussie ! Vous pouvez maintenant vous connecter.",
                        "user_id": str(result.inserted_id)
                    }
                else:
                    return {
                        "success": False,
                        "message": "Erreur lors de l'inscription. Veuillez réessayer."
                    }
            else:
                return {
                    "success": False,
                    "message": "Erreur de connexion à la base de données."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'inscription : {str(e)}"
            }
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Connecte un utilisateur"""
        try:
            if self.db.db is not None:
                # Rechercher l'utilisateur
                user = self.db.db.users.find_one({"username": username})
                
                if not user:
                    return {
                        "success": False,
                        "message": "Nom d'utilisateur ou mot de passe incorrect."
                    }
                
                # Vérifier le mot de passe
                if not self.verify_password(password, user["password"]):
                    return {
                        "success": False,
                        "message": "Nom d'utilisateur ou mot de passe incorrect."
                    }
                
                # Vérifier si le compte est actif
                if not user.get("is_active", True):
                    return {
                        "success": False,
                        "message": "Ce compte a été désactivé."
                    }
                
                # Mettre à jour la dernière connexion
                self.db.db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"last_login": datetime.now()}}
                )
                
                return {
                    "success": True,
                    "message": "Connexion réussie !",
                    "user": {
                        "id": str(user["_id"]),
                        "username": user["username"],
                        "email": user["email"],
                        "created_at": user["created_at"]
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "Erreur de connexion à la base de données."
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la connexion : {str(e)}"
            }
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un utilisateur par son ID"""
        try:
            if self.db.db is not None:
                from bson import ObjectId
                user = self.db.db.users.find_one({"_id": ObjectId(user_id)})
                if user:
                    return {
                        "id": str(user["_id"]),
                        "username": user["username"],
                        "email": user["email"],
                        "created_at": user["created_at"],
                        "last_login": user.get("last_login")
                    }
            return None
        except:
            return None
    
    def logout_user(self):
        """Déconnecte l'utilisateur actuel"""
        if "user" in st.session_state:
            del st.session_state["user"]
        if "user_id" in st.session_state:
            del st.session_state["user_id"]
        if "authenticated" in st.session_state:
            st.session_state["authenticated"] = False

def show_login_form(auth_manager: AuthManager):
    """Affiche le formulaire de connexion"""
    st.subheader("🔐 Connexion")
    
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur", key="login_username")
        password = st.text_input("Mot de passe", type="password", key="login_password")
        submit_button = st.form_submit_button("Se connecter")
        
        if submit_button:
            if username and password:
                result = auth_manager.login_user(username, password)
                if result["success"]:
                    st.session_state["user"] = result["user"]
                    st.session_state["user_id"] = result["user"]["id"]
                    st.session_state["authenticated"] = True
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("Veuillez remplir tous les champs.")
    
    # Lien vers l'inscription
    st.markdown("---")
    if st.button("📝 Créer un compte", key="go_to_register"):
        st.session_state["show_register"] = True
        st.rerun()

def show_register_form(auth_manager: AuthManager):
    """Affiche le formulaire d'inscription"""
    st.subheader("📝 Inscription")
    
    with st.form("register_form"):
        username = st.text_input("Nom d'utilisateur", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Mot de passe", type="password", key="register_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="confirm_password")
        submit_button = st.form_submit_button("S'inscrire")
        
        if submit_button:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas.")
                elif len(password) < Config.MIN_PASSWORD_LENGTH:
                    st.error(f"Le mot de passe doit contenir au moins {Config.MIN_PASSWORD_LENGTH} caractères.")
                else:
                    result = auth_manager.register_user(username, email, password)
                    if result["success"]:
                        st.success(result["message"])
                        # Rediriger vers la connexion
                        st.session_state["show_login"] = True
                        st.rerun()
                    else:
                        st.error(result["message"])
            else:
                st.error("Veuillez remplir tous les champs.")
    
    # Lien vers la connexion
    st.markdown("---")
    if st.button("🔐 Se connecter", key="go_to_login"):
        st.session_state["show_register"] = False
        st.rerun()

def show_auth_page(auth_manager: AuthManager):
    """Affiche la page d'authentification"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h1>🔐 Authentification</h1>', unsafe_allow_html=True)
    
    # Gestion de l'affichage des formulaires
    show_register = st.session_state.get("show_register", False)
    
    if show_register:
        show_register_form(auth_manager)
    else:
        show_login_form(auth_manager)
    
    st.markdown('</div>', unsafe_allow_html=True) 