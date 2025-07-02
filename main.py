import streamlit as st
import PyPDF2
import requests
from utils import DatabaseManager, format_log_entry
from config import Config
import uuid

st.markdown(r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

HF_API_KEY = Config.get_huggingface_api_key()

# Initialiser la connexion à la base de données
@st.cache_resource
def get_database():
    return DatabaseManager()

db = get_database()

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
        })
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
        })
        st.success("Session sauvegardée!")
    
    # Bouton pour effacer la session
    if st.button("🗑️ Effacer session"):
        st.session_state["file_texts"] = {}
        st.session_state["summaries"] = []
        st.session_state["current_summaries"] = ""
        st.session_state["messages"] = []
        db.log_activity("session_cleared", {
            "session_id": st.session_state.session_id
        })
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
            })
            
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
            })
            
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
            })
            
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
            })

# Nettoyage à la fin de l'application
import atexit
atexit.register(db.close_connection)
