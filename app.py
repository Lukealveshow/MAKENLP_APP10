import streamlit as st
#from translation import translate_text
from deep_translator.exceptions import TooManyRequests

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
        "insert_error": "Erro durante a inserção:",

        "empty_translation": "Digite um texto para traduzir.",
        "translation_limit": (
            "O serviço de tradução atingiu o limite de requisições. "
            "Aguarde alguns instantes e tente novamente."
        ),
        "translation_error": (
            "Não foi possível realizar a tradução. "
            "Tente novamente mais tarde."
        )
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
        "insert_error": "Error during insertion:",

        "empty_translation": "Enter a text to translate.",
        "translation_limit": (
            "The translation service has reached its request limit. "
            "Please wait a few moments and try again."
        ),
        "translation_error": (
            "The translation could not be completed. "
            "Please try again later."
        )
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
        "insert_error": "Erreur lors de l'insertion :",

        "empty_translation": "Saisissez un texte à traduire.",
        "translation_limit": (
            "Le service de traduction a atteint sa limite de requêtes. "
            "Veuillez patienter quelques instants et réessayer."
        ),
        "translation_error": (
            "La traduction n'a pas pu être effectuée. "
            "Veuillez réessayer plus tard."
        )
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
        "insert_error": "Error durante la inserción:",

        "empty_translation": "Ingrese un texto para traducir.",
        "translation_limit": (
            "El servicio de traducción ha alcanzado el límite de solicitudes. "
            "Espere unos momentos y vuelva a intentarlo."
        ),
        "translation_error": (
            "No se pudo realizar la traducción. "
            "Inténtelo nuevamente más tarde."
        )
    }
}

@st.cache_data
def cache_summarize_text(text_summarization):

    return summarize_text(
        text_summarization
    )

@st.cache_data
def cache_generate_answer(question, text_generation):

    return generate_answer(
        question,
        text_generation
    )

def translate_text(text, target_language):

    if not text or not text.strip():

        return None

    try:

        translator = GoogleTranslator(
            source="auto",
            target=target_language
        )

        return translator.translate(
            text
        )

    except TooManyRequests:

        return "TOO_MANY_REQUESTS"

    except Exception:

        return "TRANSLATION_ERROR"


def translate_page(page_language):
    t = UI_TRANSLATIONS[page_language]

    if "translated_text" not in st.session_state:

        st.session_state.translated_text = ""

    if "translated_source_text" not in st.session_state:

        st.session_state.translated_source_text = ""

    if "translated_target_language" not in st.session_state:

        st.session_state.translated_target_language = ""

    st.title(
        t["welcome"]
    )

    name = st.text_input(
        t["name"]
    )

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

    st.subheader(
        t["summarize_input"]
    )

    text_summarization = st.text_area(
        "",
        height=150,
        key="text_summarization"
    )


    if st.button(
        t["summarize"]
    ):

        if not text_summarization.strip():

            if page_language == "pt":
                st.warning(
                    "Digite um texto para resumir."
                )

            elif page_language == "en":
                st.warning(
                    "Enter a text to summarize."
                )

            elif page_language == "fr":
                st.warning(
                    "Saisissez un texte à résumer."
                )

            else:
                st.warning(
                    "Ingrese un texto para resumir."
                )

        else:

            summarized_text = cache_summarize_text(
                text_summarization
            )

            st.subheader(
                t["summary"]
            )

            st.write(
                summarized_text
            )

    st.subheader(
        t["generation_input"]
    )

    text_generation = st.text_area(
        "",
        height=150,
        key="text_generation"
    )

    question = st.text_input(
        t["question"],
        key="question"
    )


    if st.button(
        t["generate"]
    ):

        if not text_generation.strip():

            if page_language == "pt":
                st.warning(
                    "Digite um texto para gerar uma resposta."
                )

            elif page_language == "en":
                st.warning(
                    "Enter a text to generate an answer."
                )

            elif page_language == "fr":
                st.warning(
                    "Saisissez un texte pour générer une réponse."
                )

            else:
                st.warning(
                    "Ingrese un texto para generar una respuesta."
                )

        elif not question.strip():

            if page_language == "pt":
                st.warning(
                    "Digite uma pergunta."
                )

            elif page_language == "en":
                st.warning(
                    "Enter a question."
                )

            elif page_language == "fr":
                st.warning(
                    "Saisissez une question."
                )

            else:
                st.warning(
                    "Ingrese una pregunta."
                )

        else:

            answer = cache_generate_answer(
                question,
                text_generation
            )

            st.subheader(
                t["answer"]
            )

            st.write(
                answer
            )

    st.subheader(
        t["translation_input"]
    )

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

    if (
        text_translation
        != st.session_state.translated_source_text
        or
        target_language
        != st.session_state.translated_target_language
    ):

        st.session_state.translated_text = ""


    if st.button(
        t["translate"]
    ):

        if not text_translation.strip():

            st.warning(
                t["empty_translation"]
            )

        else:

            result = translate_text(
                text_translation,
                target_language
            )

            if result == "TOO_MANY_REQUESTS":

                st.error(
                    t["translation_limit"]
                )


            elif result == "TRANSLATION_ERROR":

                st.error(
                    t["translation_error"]
                )


            else:

                st.session_state.translated_text = result

                st.session_state.translated_source_text = (
                    text_translation
                )

                st.session_state.translated_target_language = (
                    target_language
                )

                st.subheader(
                    t["translated_text"]
                )

                st.write(
                    result
                )


    if (
        st.session_state.translated_text
        and
        st.session_state.translated_source_text
        == text_translation
        and
        st.session_state.translated_target_language
        == target_language
    ):

        st.subheader(
            t["translated_text"]
        )

        st.write(
            st.session_state.translated_text
        )


    if st.button(
        t["send"]
    ):

        try:

            summarized_text = cache_summarize_text(
                text_summarization
            )

            answer = cache_generate_answer(
                question,
                text_generation
            )


            translated_text = ""


            if text_translation.strip():

                # Se já temos uma tradução válida armazenada,
                # reutiliza ela e NÃO chama o Google novamente.

                if (
                    st.session_state.translated_text
                    and
                    st.session_state.translated_source_text
                    == text_translation
                    and
                    st.session_state.translated_target_language
                    == target_language
                ):

                    translated_text = (
                        st.session_state.translated_text
                    )

                else:

                    result = translate_text(
                        text_translation,
                        target_language
                    )


                    if result == "TOO_MANY_REQUESTS":

                        st.error(
                            t["translation_limit"]
                        )

                        st.stop()


                    elif result == "TRANSLATION_ERROR":

                        st.error(
                            t["translation_error"]
                        )

                        st.stop()


                    else:

                        translated_text = result

                        # Guarda a tradução para reutilização
                        st.session_state.translated_text = (
                            translated_text
                        )

                        st.session_state.translated_source_text = (
                            text_translation
                        )

                        st.session_state.translated_target_language = (
                            target_language
                        )


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

            st.success(
                t["success"]
            )


        except Exception as e:

            st.error(
                f"{t['insert_error']} {e}"
            )


if __name__ == "__main__":

    st.set_page_config(
        page_title="MAKENLP",
        page_icon=":speech_balloon:"
    )


    page_language = st.selectbox(
        "Selecione o idioma de tradução:",
        options=[
            "pt",
            "en",
            "fr",
            "es"
        ]
    )


    translate_page(
        page_language
    )
