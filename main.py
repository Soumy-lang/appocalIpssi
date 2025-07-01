import streamlit as st
import PyPDF2
import requests

st.markdown(r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

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
            st.session_state["file_texts"][uploaded_file.name] = {
                "text": text,
                "num_pages": len(pdf_reader.pages),
                "num_words": len(text.split())
            }

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
                summary = summarize_with_huggingface(data["text"][:3000])
                summaries.append(f"**{file_name}** : {summary}")
            st.session_state["current_summaries"] = "\n\n".join(summaries)

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
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")
