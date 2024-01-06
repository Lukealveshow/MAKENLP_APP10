import streamlit as st
from deep_translator import GoogleTranslator
from summarization import summarize_text
from generation import generate_answer
from database3 import insert_data
import _thread
import weakref

# Função de hash personalizada para objetos não padrão
def my_hash_func(obj):
    if isinstance(obj, (_thread.RLock, weakref.ReferenceType)):
        return hash(obj)  # ou qualquer outra lógica de hash que você deseje aplicar
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not hashable.")

# Decoradores st.cache com hash_funcs
@st.cache(hash_funcs={_thread.RLock: my_hash_func, weakref.ReferenceType: my_hash_func})
def cache_summarize_text(text_summarization):
    return summarize_text(text_summarization)

@st.cache(hash_funcs={_thread.RLock: my_hash_func, weakref.ReferenceType: my_hash_func})
def cache_generate_answer(question, text_generation):
    return generate_answer(question, text_generation)

@st.cache(allow_output_mutation=True, hash_funcs={_thread.RLock: my_hash_func, weakref.ReferenceType: my_hash_func})
def cache_insert_data(name, age, gender, text_summarization, summarized_text, text_generation,
                      question, answer, text_translation, language, translated_text):
    try:
        insert_data(name, age, gender, text_summarization, summarized_text, text_generation,
                    question, answer, text_translation, language, translated_text)
        st.success("Dados inseridos com sucesso!")
    except Exception as e:
        st.error(f"Erro durante a inserção: {e}")

# Função principal com chamadas às funções de cache
def translate_page(language):
    translator = GoogleTranslator(source='auto', target=language)
    translated_title = translator.translate("Seja Bem Vindo ao MAKENLP")
    st.title(translated_title)
    
    # Additional fields
    translated_name = translator.translate("Nome:")
    name = st.text_input(translated_name)
    
    translated_age = translator.translate("Idade:")
    age = st.number_input(translated_age, step=1)
    
    translated_gender = translator.translate("Gênero:")
    gender_options = [translator.translate('Masculino'), translator.translate('Feminino')]
    gender = st.selectbox(translated_gender, options=gender_options)
    
    # Section for text input
    translated_text_input = translator.translate("Digite o texto para resumir:")
    st.subheader(translated_text_input)
    text_summarization = st.text_area("", height=150)

    # Button to summarize text
    if st.button(translator.translate("Resumir Texto")):
        summarized_text = cache_summarize_text(text_summarization)
        st.subheader(translator.translate("Texto Resumido"))
        st.write(summarized_text)

    # Button to generate answer
    if st.button(translator.translate("Gerar Resposta")):
        answer = cache_generate_answer(question, text_generation)
        st.subheader(translator.translate("Resposta Gerada"))
        st.write(answer)

    # Button to execute all functions and insert into the database
    if st.button(translator.translate("Enviar")):
        try:
            summarized_text = cache_summarize_text(text_summarization)
            answer = cache_generate_answer(question, text_generation)
            translated_text = GoogleTranslator(source='auto', target=language).translate(text_translation)

            # Chamada à função de cache para inserção de dados
            cache_insert_data(name, age, gender, text_summarization, summarized_text, text_generation,
                              question, answer, text_translation, language, translated_text)
        except Exception as e:
            st.error(f"Erro durante a inserção: {e}")


# Run the Streamlit app
if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    translate_page(translation_language)
