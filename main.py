import streamlit as st
import PyPDF2
<<<<<<< HEAD
from openai import OpenAI
from database import db_manager
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_environment():
    """Vérifie que toutes les variables d'environnement nécessaires sont définies"""
    required_vars = ["OPENAI_API_KEY", "MONGODB_CONNECTION_STRING"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        st.error(f"Variables d'environnement manquantes : {', '.join(missing_vars)}")
        st.info("Veuillez créer un fichier .env avec les variables requises")
        st.stop()

# Vérifier la configuration au démarrage
check_environment()
=======
import requests
>>>>>>> 83b677f0b34e628928b2ed35efeada2f9a8408ee

st.markdown(r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

<<<<<<< HEAD
# La connexion MongoDB est maintenant gérée par le DatabaseManager
# importé depuis database.py

# Utiliser les variables d'environnement pour OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Variable d'environnement OPENAI_API_KEY non définie")
    st.stop()

client = OpenAI(api_key=openai_api_key)
=======
HF_API_KEY = st.secrets["huggingface"]["api_key"]

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

        if response.status_code != 200:
            return f"Erreur Hugging Face : {response.status_code} - {response.text}"

        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        else:
            return f"Réponse inattendue : {result}"

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
        
        # Log la réponse brute (utile en debug)
        print("Réponse Hugging Face brut:", response.text)

        if response.status_code == 503:
            return "Le modèle est en train de se charger. Réessaye dans quelques secondes."

        if response.status_code != 200:
            return f"Erreur API Hugging Face : {response.status_code} - {response.text}"

        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"Réponse inattendue : {result}"

    except Exception as e:
        return f"Erreur lors de la réponse : {e}"
>>>>>>> 83b677f0b34e628928b2ed35efeada2f9a8408ee

# Initialiser les états de session
if "summaries" not in st.session_state:
    st.session_state["summaries"] = []
if "file_texts" not in st.session_state:
    st.session_state["file_texts"] = {}

st.title("Analyse des fichiers")

uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state["file_texts"]:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Stocker le contenu extrait pour chaque fichier
            file_data = {
                "text": text,
                "num_pages": len(pdf_reader.pages),
                "num_words": len(text.split())
            }
            st.session_state["file_texts"][uploaded_file.name] = file_data

            # Sauvegarder dans MongoDB via le DatabaseManager
            db_manager.save_document(
                filename=uploaded_file.name,
                content=text,
                num_pages=len(pdf_reader.pages),
                num_words=len(text.split()),
                file_size=len(uploaded_file.getvalue())
            )

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
<<<<<<< HEAD
            try:
                summaries = []
                for file_name, data in st.session_state["file_texts"].items():
                    response = client.chat.completions.create(
                        # model="gpt-4o",
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Tu es un assistant qui résume des documents."},
                            {"role": "user", "content": f"Résume ce document intitulé {file_name} : {data['text']}"}
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    summary = response['choices'][0]['message']['content']
                    summaries.append(f"**{file_name}** : {summary}")

                # Stocker les résumés dans la session (remplace les anciens résumés)
                st.session_state["current_summaries"] = "\n\n".join(summaries)

                # Sauvegarder les résumés dans MongoDB via le DatabaseManager
                db_manager.save_summary(
                    summaries=summaries,
                    files_analyzed=list(st.session_state["file_texts"].keys())
                )

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
=======
            summaries = []
            for file_name, data in st.session_state["file_texts"].items():
                summary = summarize_with_huggingface(data["text"][:3000])
                summaries.append(f"**{file_name}** : {summary}")
            st.session_state["current_summaries"] = "\n\n".join(summaries)
>>>>>>> 83b677f0b34e628928b2ed35efeada2f9a8408ee

    if st.session_state["current_summaries"]:
        st.subheader("Résumé :")
        st.write(st.session_state["current_summaries"])

    # Afficher l'historique depuis MongoDB via le DatabaseManager
    if db_manager.is_connected():
        st.subheader("📊 Historique de la base de données")
        
        # Statistiques générales
        total_docs = db_manager.get_documents_count()
        total_summaries = db_manager.get_summaries_count()
        total_conversations = db_manager.get_conversations_count()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documents stockés", total_docs)
        with col2:
            st.metric("Résumés générés", total_summaries)
        with col3:
            st.metric("Conversations", total_conversations)
        
        # Afficher les derniers documents
        if total_docs > 0:
            with st.expander("📄 Derniers documents traités"):
                recent_docs = db_manager.get_recent_documents(5)
                for doc in recent_docs:
                    st.write(f"**{doc['filename']}** - {doc['upload_date'].strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"Pages: {doc['num_pages']} | Mots: {doc['num_words']}")
                    st.divider()
        
        # Afficher les dernières conversations
        if total_conversations > 0:
            with st.expander("💬 Dernières conversations"):
                recent_conversations = db_manager.get_recent_conversations(5)
                for conv in recent_conversations:
                    st.write(f"**{conv['timestamp'].strftime('%d/%m/%Y %H:%M')}**")
                    st.write(f"**Q:** {conv['question']}")
                    st.write(f"**R:** {conv['answer'][:100]}...")
                    st.divider()


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
<<<<<<< HEAD
            
            # Sauvegarder la conversation dans MongoDB via le DatabaseManager
            db_manager.save_conversation(
                question=user_question,
                answer=answer,
                files_referenced=list(st.session_state["file_texts"].keys()),
                session_id=id(st.session_state)
            )
            
=======
>>>>>>> 83b677f0b34e628928b2ed35efeada2f9a8408ee
            with st.chat_message("assistant"):
                st.markdown(answer)
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")

# Nettoyage à la fin de l'application
if st.session_state.get("_is_terminating", False):
    db_manager.close_connection()
