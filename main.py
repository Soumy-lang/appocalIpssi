import streamlit as st
import PyPDF2
from openai import OpenAI

st.markdown(r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True)

hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)


# openai.api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

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

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

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
                [f"Contenu de {file_name} : {data['text']}" for file_name, data in st.session_state["file_texts"].items()]
            )
            response = client.chat.completions.create(
                # model="gpt-4o",
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui répond aux questions basées sur plusieurs documents PDF."},
                    {"role": "user", "content": f"Voici les contenus des fichiers : {combined_texts}. Réponds à cette question : {user_question}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            with st.chat_message("assistant"):
                st.markdown(answer)
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")
