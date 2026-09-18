import streamlit as st
from deep_translator import GoogleTranslator

from summarization import summarize_text
from generation import generate_answer
from database3 import insert_data

UI_TRANSLATIONS = {
    "pt": {
        "welcome": "Seja Bem Vindo ao MAKENLP",
        "name": "Nome:",
        "age": "Idade:",
        "gender": "Gênero:",
        "male": "Masculino",
        "female": "Feminino",
        "summarize_input": "Digite o texto para resumir:",
        "summarize": "Resumir Texto",
        "summary": "Texto Resumido",
        "generation_input": "Digite o texto:",
        "question": "Faça uma pergunta sobre o texto:",
        "generate": "Gerar Resposta",
        "answer": "Resposta Gerada",
        "translation_input": "Digite o texto para traduzir:",
        "target_language": "Selecione o idioma de destino:",
        "translate": "Traduzir Texto",
        "translated_text": "Texto Traduzido",
        "send": "Enviar",
        "success": "Dados inseridos com sucesso!",
        "insert_error": "Erro durante a inserção:"
    },

    "en": {
        "welcome": "Welcome to MAKENLP",
        "name": "Name:",
        "age": "Age:",
        "gender": "Gender:",
        "male": "Male",
        "female": "Female",
        "summarize_input": "Enter the text to summarize:",
        "summarize": "Summarize Text",
        "summary": "Summarized Text",
        "generation_input": "Enter the text:",
        "question": "Ask a question about the text:",
        "generate": "Generate Answer",
        "answer": "Generated Answer",
        "translation_input": "Enter the text to translate:",
        "target_language": "Select target language:",
        "translate": "Translate Text",
        "translated_text": "Translated Text",
        "send": "Send",
        "success": "Data successfully inserted!",
        "insert_error": "Error during insertion:"
    },

    "fr": {
        "welcome": "Bienvenue sur MAKENLP",
        "name": "Nom :",
        "age": "Âge :",
        "gender": "Genre :",
        "male": "Masculin",
        "female": "Féminin",
        "summarize_input": "Saisissez le texte à résumer :",
        "summarize": "Résumer le texte",
        "summary": "Texte résumé",
        "generation_input": "Saisissez le texte :",
        "question": "Posez une question sur le texte :",
        "generate": "Générer une réponse",
        "answer": "Réponse générée",
        "translation_input": "Saisissez le texte à traduire :",
        "target_language": "Sélectionnez la langue cible :",
        "translate": "Traduire le texte",
        "translated_text": "Texte traduit",
        "send": "Envoyer",
        "success": "Données insérées avec succès !",
        "insert_error": "Erreur lors de l'insertion :"
    },

    "es": {
        "welcome": "Bienvenido a MAKENLP",
        "name": "Nombre:",
        "age": "Edad:",
        "gender": "Género:",
        "male": "Masculino",
        "female": "Femenino",
        "summarize_input": "Ingrese el texto para resumir:",
        "summarize": "Resumir Texto",
        "summary": "Texto Resumido",
        "generation_input": "Ingrese el texto:",
        "question": "Haga una pregunta sobre el texto:",
        "generate": "Generar Respuesta",
        "answer": "Respuesta Generada",
        "translation_input": "Ingrese el texto para traducir:",
        "target_language": "Seleccione el idioma de destino:",
        "translate": "Traducir Texto",
        "translated_text": "Texto Traducido",
        "send": "Enviar",
        "success": "¡Datos insertados correctamente!",
        "insert_error": "Error durante la inserción:"
    }
}

@st.cache_data
def cache_summarize_text(text_summarization):
    return summarize_text(text_summarization)


@st.cache_data
def cache_generate_answer(question, text_generation):
    return generate_answer(question, text_generation)

def translate_page(page_language):

    # Traduções da interface
    t = UI_TRANSLATIONS[page_language]

    st.title(t["welcome"])
    name = st.text_input(t["name"])

    age = st.number_input(
        t["age"],
        step=1
    )

    gender_display = st.selectbox(
        t["gender"],
        options=[
            t["male"],
            t["female"]
        ]
    )

    # Mantém um valor padronizado para o banco
    if gender_display == t["male"]:
        gender = "Masculino"
    else:
        gender = "Feminino"

    st.subheader(t["summarize_input"])

    text_summarization = st.text_area(
        "",
        height=150,
        key="text_summarization"
    )

    if st.button(t["summarize"]):

        summarized_text = cache_summarize_text(
            text_summarization
        )

        st.subheader(t["summary"])

        st.write(summarized_text)

    st.subheader(t["generation_input"])

    text_generation = st.text_area(
        "",
        height=150,
        key="text_generation"
    )

    question = st.text_input(
        t["question"],
        key="question"
    )

    if st.button(t["generate"]):

        answer = cache_generate_answer(
            question,
            text_generation
        )

        st.subheader(t["answer"])

        st.write(answer)

    st.subheader(t["translation_input"])

    text_translation = st.text_area(
        "",
        height=150,
        key="text_translation"
    )

    target_language = st.selectbox(
        t["target_language"],
        options=[
            "en",
            "es",
            "fr",
            "pt"
        ],
        key="target_language"
    )

    if st.button(t["translate"]):

        if not text_translation.strip():

            st.warning(
                "Digite um texto para traduzir."
                if page_language == "pt"
                else
                "Enter a text to translate."
                if page_language == "en"
                else
                "Saisissez un texte à traduire."
                if page_language == "fr"
                else
                "Ingrese un texto para traducir."
            )

        else:

            translated_text = GoogleTranslator(
                source="auto",
                target=target_language
            ).translate(text_translation)

            st.subheader(t["translated_text"])

            st.write(translated_text)

    if st.button(t["send"]):

        try:

            # Resumo
            summarized_text = cache_summarize_text(
                text_summarization
            )

            # Resposta
            answer = cache_generate_answer(
                question,
                text_generation
            )

            # Tradução
            translated_text = GoogleTranslator(
                source="auto",
                target=target_language
            ).translate(text_translation)

            # INSERT NO BANCO
            insert_data(
                name,
                age,
                gender,
                text_summarization,
                summarized_text,
                text_generation,
                question,
                answer,
                text_translation,
                target_language,
                translated_text
            )

            # Mensagem de sucesso usa o idioma DA INTERFACE,
            # e não o idioma da tradução do texto.
            st.success(t["success"])

        except Exception as e:

            st.error(
                f"{t['insert_error']} {e}"
            )

if __name__ == "__main__":

    st.set_page_config(
        page_title="MAKENLP",
        page_icon=":speech_balloon:"
    )

    # Idioma da INTERFACE
    page_language = st.selectbox(
        "Selecione o idioma de tradução:",
        options=[
            "pt",
            "en",
            "fr",
            "es"
        ]
    )

    translate_page(page_language)
