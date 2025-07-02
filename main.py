import streamlit as st
import PyPDF2
import requests
from utils import DatabaseManager, format_log_entry
from config import Config
import uuid
import hashlib
import re

st.markdown(r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

HF_API_KEY = Config.get_huggingface_api_key()

# Initialiser la connexion à la base de données
@st.cache_resource
def get_database():
    return DatabaseManager()

db = get_database()

# Initialiser les états d'authentification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "show_register" not in st.session_state:
    st.session_state.show_register = False

def hash_password(password):
    """Hash le mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Valide la force du mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, "Mot de passe valide"

def register_user(email, password, confirm_password, full_name):
    """Enregistre un nouvel utilisateur"""
    try:
        # Validation des champs
        if not email or not password or not confirm_password or not full_name:
            return False, "Tous les champs sont obligatoires"
        
        if not validate_email(email):
            return False, "Format d'email invalide"
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return False, message
        
        if password != confirm_password:
            return False, "Les mots de passe ne correspondent pas"
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return False, "Un utilisateur avec cet email existe déjà"
        
        # Créer le nouvel utilisateur
        hashed_password = hash_password(password)
        user_data = {
            "email": email,
            "password": hashed_password,
            "full_name": full_name,
            "created_at": db.get_current_timestamp(),
            "last_login": None
        }
        
        success = db.create_user(user_data)
        if success:
            return True, "Inscription réussie ! Vous pouvez maintenant vous connecter."
        else:
            return False, "Erreur lors de l'inscription. Veuillez réessayer."
            
    except Exception as e:
        return False, f"Erreur lors de l'inscription : {str(e)}"

def login_user(email, password):
    """Connecte un utilisateur"""
    try:
        if not email or not password:
            return False, "Email et mot de passe requis"
        
        # Récupérer l'utilisateur
        user = db.get_user_by_email(email)
        if not user:
            return False, "Email ou mot de passe incorrect"
        
        # Vérifier le mot de passe
        hashed_password = hash_password(password)
        if user["password"] != hashed_password:
            return False, "Email ou mot de passe incorrect"
        
        # Mettre à jour la dernière connexion
        db.update_last_login(user["_id"])
        
        return True, "Connexion réussie !"
        
    except Exception as e:
        return False, f"Erreur lors de la connexion : {str(e)}"

def show_auth_page():
    """Affiche la page d'authentification"""
    # CSS pour améliorer l'apparence
    st.markdown("""
    <style>
    .auth-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
    }
    .auth-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">🔐 Authentification APOCALIPSSI</h1>', unsafe_allow_html=True)
    
    # Onglets pour connexion/inscription
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        st.subheader("Se connecter")
        with st.form("login_form"):
            login_email = st.text_input("📧 Email", key="login_email", placeholder="votre@email.com")
            login_password = st.text_input("🔒 Mot de passe", type="password", key="login_password", placeholder="Votre mot de passe")
            login_submitted = st.form_submit_button("🚀 Se connecter", use_container_width=True)
            
            if login_submitted:
                success, message = login_user(login_email, login_password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.current_user = db.get_user_by_email(login_email)
                    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    with tab2:
        st.subheader("S'inscrire")
        with st.form("register_form"):
            reg_full_name = st.text_input("👤 Nom complet", key="reg_full_name", placeholder="Votre nom complet")
            reg_email = st.text_input("📧 Email", key="reg_email", placeholder="votre@email.com")
            reg_password = st.text_input("🔒 Mot de passe", type="password", key="reg_password", placeholder="Min. 8 caractères, majuscule, minuscule, chiffre")
            reg_confirm_password = st.text_input("🔒 Confirmer le mot de passe", type="password", key="reg_confirm_password", placeholder="Confirmez votre mot de passe")
            
            # Afficher les exigences du mot de passe
            st.info("💡 Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre.")
            
            reg_submitted = st.form_submit_button("📝 S'inscrire", use_container_width=True)
            
            if reg_submitted:
                success, message = register_user(reg_email, reg_password, reg_confirm_password, reg_full_name)
                if success:
                    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                    st.balloons()
                    # Redirection automatique vers l'onglet connexion après 3 secondes
                    st.info("🔄 Redirection automatique vers la page de connexion dans 3 secondes...")
                    import time
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_logout_button():
    """Affiche le bouton de déconnexion dans la sidebar"""
    with st.sidebar:
        st.divider()
        if st.button("🚪 Se déconnecter"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.file_texts = {}
            st.session_state.summaries = []
            st.session_state.current_summaries = ""
            st.session_state.messages = []
            st.rerun()

# Vérifier l'authentification
if not st.session_state.authenticated:
    show_auth_page()
    st.stop()

# Afficher les informations de l'utilisateur connecté
st.sidebar.success(f"👤 Connecté : {st.session_state.current_user['full_name']}")
show_logout_button()

# Générer un ID de session unique
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialiser la connexion à la base de données
@st.cache_resource
def get_database():
    return DatabaseManager()

db = get_database()

# Générer un ID de session unique
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

def summarize_with_huggingface(text):
    import time

    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    short_text = text[:1300]

    try:
        response = requests.post(api_url, headers=headers, json={"inputs": short_text})
        
        # Si le modèle est en train de se charger (503)
        if response.status_code == 503:
            st.warning("Le modèle se réveille... Réessaye dans quelques secondes.")
            time.sleep(10) 
            return "Le modèle n'est pas encore prêt. Réessaie dans quelques secondes."

        # Gestion spécifique de l'erreur 504 (Gateway Timeout)
        if response.status_code == 504:
            return "Le service Hugging Face est temporairement surchargé. Veuillez réessayer dans quelques minutes."

        if response.status_code != 200:
            return f"Erreur Hugging Face : {response.status_code} - Service temporairement indisponible"

        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        else:
            return f"Réponse inattendue du service"

    except Exception as e:
        return f"Erreur lors du résumé : {e}"

def ask_question_with_huggingface(question, context):
    import time
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    context = context[:2000]

    prompt = f"""
    Tu es un assistant intelligent. Utilise les informations suivantes pour répondre :

    Contexte :
    {context}

    Question : {question}

    Réponse :
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Gestion spécifique de l'erreur 504 (Gateway Timeout)
        if response.status_code == 504:
            return "Le service Hugging Face est temporairement surchargé. Veuillez réessayer dans quelques minutes."

        if response.status_code == 503:
            return "Le modèle est en train de se charger. Réessaye dans quelques secondes."

        if response.status_code != 200:
            return f"Erreur API Hugging Face : {response.status_code} - Service temporairement indisponible"

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"Réponse inattendue du service"

    except Exception as e:
        return f"Erreur lors de la réponse : {e}"

# Initialiser les états de session
if "summaries" not in st.session_state:
    st.session_state["summaries"] = []
if "file_texts" not in st.session_state:
    st.session_state["file_texts"] = {}

# Charger les données de session depuis la base de données
if "session_loaded" not in st.session_state:
    saved_data = db.load_session_data(st.session_state.session_id)
    if saved_data:
        st.session_state["file_texts"] = saved_data.get("file_texts", {})
        st.session_state["summaries"] = saved_data.get("summaries", [])
        st.session_state["current_summaries"] = saved_data.get("current_summaries", "")
        st.session_state["messages"] = saved_data.get("messages", [])
        st.session_state["session_loaded"] = True
        db.log_activity("session_restored", {
            "session_id": st.session_state.session_id,
            "files_count": len(st.session_state["file_texts"])
        }, st.session_state.current_user["email"])
    else:
        st.session_state["session_loaded"] = True

st.title("Analyse des fichiers")

# Sidebar pour les logs et la gestion de session
with st.sidebar:
    st.header("📊 Logs et Session")
    
    # Bouton pour afficher les logs
    if st.button("📋 Afficher les logs récents"):

        logs = db.get_recent_logs(20)
        # logs = db.get_recent_logs(Config.LOG_DISPLAY_LIMIT)

        if logs:
            st.subheader("Logs récents:")
            for log in logs:
                st.text(format_log_entry(log))
        else:
            st.info("Aucun log disponible")
    
    # Informations de session
    st.subheader("Session actuelle:")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    st.text(f"Fichiers: {len(st.session_state['file_texts'])}")
    
    # Bouton pour sauvegarder manuellement
    if st.button("💾 Sauvegarder session"):
        session_data = {
            "file_texts": st.session_state["file_texts"],
            "summaries": st.session_state["summaries"],
            "current_summaries": st.session_state.get("current_summaries", ""),
            "messages": st.session_state.get("messages", [])
        }
        db.save_session_data(st.session_state.session_id, session_data)
        db.log_activity("manual_save", {
            "session_id": st.session_state.session_id,
            "files_count": len(st.session_state["file_texts"])
        }, st.session_state.current_user["email"])
        st.success("Session sauvegardée!")
    
    # Bouton pour effacer la session
    if st.button("🗑️ Effacer session"):
        st.session_state["file_texts"] = {}
        st.session_state["summaries"] = []
        st.session_state["current_summaries"] = ""
        st.session_state["messages"] = []
        db.log_activity("session_cleared", {
            "session_id": st.session_state.session_id
        }, st.session_state.current_user["email"])
        st.success("Session effacée!")
        st.rerun()

uploaded_files = st.file_uploader("Télécharger vos fichiers PDF", type="pdf", accept_multiple_files=True)
# uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)


if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state["file_texts"]:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Stocker le contenu extrait pour chaque fichier
            st.session_state["file_texts"][uploaded_file.name] = {
                "text": text,
                "num_pages": len(pdf_reader.pages),
                "num_words": len(text.split())
            }
            
            # Logger l'ajout du fichier
            db.log_activity("file_uploaded", {
                "filename": uploaded_file.name,
                "pages": len(pdf_reader.pages),
                "words": len(text.split()),
                "session_id": st.session_state.session_id
            }, st.session_state.current_user["email"])
            
            # Sauvegarder automatiquement la session
            session_data = {
                "file_texts": st.session_state["file_texts"],
                "summaries": st.session_state["summaries"],
                "current_summaries": st.session_state.get("current_summaries", ""),
                "messages": st.session_state.get("messages", [])
            }
            db.save_session_data(st.session_state.session_id, session_data)

    # Affichage des analyses
    for file_name, data in st.session_state["file_texts"].items():
        with st.expander(f"{file_name}"):
            st.write(f"**Nombre de pages :** {data['num_pages']}")
            st.write(f"**Nombre total de mots :** {data['num_words']}")
            st.text_area(f"Contenu brut de {file_name}", data['text'], height=200)

    # Initialiser les résumés actifs dans l'état de session
    if "current_summaries" not in st.session_state:
        st.session_state["current_summaries"] = ""

    # Bouton pour générer un résumé pour tous les fichiers
    if st.button("Résumer les documents"):
        with st.spinner("Génération des résumés en cours..."):
            summaries = []
            for file_name, data in st.session_state["file_texts"].items():
                summary = summarize_with_huggingface(data["text"][:Config.MAX_TEXT_LENGTH])
                summaries.append(f"**{file_name}** : {summary}")
            st.session_state["current_summaries"] = "\n\n".join(summaries)
            
            # Logger la génération de résumés
            db.log_activity("summaries_generated", {
                "files_count": len(st.session_state["file_texts"]),
                "session_id": st.session_state.session_id
            }, st.session_state.current_user["email"])
            
            # Sauvegarder la session
            session_data = {
                "file_texts": st.session_state["file_texts"],
                "summaries": st.session_state["summaries"],
                "current_summaries": st.session_state["current_summaries"],
                "messages": st.session_state.get("messages", [])
            }
            db.save_session_data(st.session_state.session_id, session_data)

    if st.session_state["current_summaries"]:
        st.subheader("Résumé :")
        st.write(st.session_state["current_summaries"])

# Posez des questions sur les fichiers PDF
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Votre question")
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.spinner("L'IA réfléchit à votre question..."):
        try:
            combined_texts = "\n\n".join(
                [f"Contenu de {file_name} : {data['text'][:1000]}" for file_name, data in st.session_state["file_texts"].items()]
            )
            answer = ask_question_with_huggingface(user_question, combined_texts)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            # Logger la question posée
            db.log_activity("question_asked", {
                "question": user_question[:100],  # Limiter la longueur
                # "question": user_question[:Config.MAX_QUESTION_LENGTH],  # Limiter la longueur
                "files_count": len(st.session_state["file_texts"]),
                "session_id": st.session_state.session_id
            }, st.session_state.current_user["email"])
            
            # Sauvegarder la session avec les nouveaux messages
            session_data = {
                "file_texts": st.session_state["file_texts"],
                "summaries": st.session_state["summaries"],
                "current_summaries": st.session_state.get("current_summaries", ""),
                "messages": st.session_state.messages
            }
            db.save_session_data(st.session_state.session_id, session_data)
            
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")
            db.log_activity("error_occurred", {
                "error": str(e),
                "session_id": st.session_state.session_id
            }, st.session_state.current_user["email"])

# Nettoyage à la fin de l'application
import atexit
atexit.register(db.close_connection)
