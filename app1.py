import streamlit as st
import os
import sqlite3
from deep_translator import GoogleTranslator
from summarization import summarize_text
from generation import generate_answer
import _thread
import weakref

# Caminho absoluto para o banco de dados SQLite
db_path = "sqlite:///data.db"

# Verificar se o arquivo do banco de dados existe
if os.path.exists(db_path[10:]):  # Remova o prefixo "sqlite:///"
    print("O arquivo do banco de dados existe.")
else:
    print("O arquivo do banco de dados não foi encontrado.")

# Configuração de conexão
connection_config = {
    "url": db_path
}

# Função para calcular o hash de objetos _thread.RLock
def my_hash_func(obj):
    if isinstance(obj, (_thread.RLock, weakref.ReferenceType)):
        return hash(obj)  # ou qualquer outra lógica de hash que você deseje aplicar
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not hashable.")

@st.cache(hash_funcs={_thread.RLock: my_hash_func, weakref.ReferenceType: my_hash_func})
def init_connection():
    return sqlite3.connect(connection_config["url"])

@st.cache(allow_output_mutation=True, hash_funcs={_thread.RLock: my_hash_func, weakref.ReferenceType: my_hash_func})
def run_query(query):
    connection = init_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    connection.close()
    return result

def insert_data(connection_config, name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = sqlite3.connect(connection_config["url"])
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print("SQLite Error:", err)

# Função para traduzir a página.
def translate_page(language):
    # Using deep_translator for page translation
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
        summarized_text = summarize_text(text_summarization)
        st.subheader(translator.translate("Texto Resumido"))
        st.write(summarized_text)
    translated_text_gen = translator.translate("Digite o texto:")
    st.subheader(translated_text_gen)
    text_generation = st.text_area("", height=150, key='text_generation')
    translated_question = translator.translate("Faça uma pergunta sobre o texto:")
    question = st.text_input(translated_question, key='question')

    # Button to generate answer
    if st.button(translator.translate("Gerar Resposta")):
        answer = generate_answer(question, text_generation)
        st.subheader(translator.translate("Resposta Gerada"))
        st.write(answer)

    # Section for text input and language selection
    translated_text_trans = translator.translate("Digite o texto para traduzir:")
    st.subheader(translated_text_trans)
    text_translation = st.text_area("", height=150, key='text_translation')
    translated_lang = translator.translate("Selecione o idioma de destino:")
    language_options = ['en', 'es', 'fr', 'pt']
    language = st.selectbox(translated_lang, options=language_options, key='language')

    # Button to translate text
    if st.button(translator.translate("Traduzir Texto")):
        translated_text = GoogleTranslator(source='auto', target=language).translate(text_translation)
        st.subheader(translator.translate("Texto Traduzido"))
        st.write(translated_text)

    if st.button(translator.translate("Enviar")):
        summarized_text = summarize_text(text_summarization)
        answer = generate_answer(question, text_generation)
        translated_text = GoogleTranslator(source='auto', target=language).translate(text_translation)

        insert_data({"url": "sqlite:///data.db"}, name, age, gender, text_summarization, summarized_text, text_generation,
                    question, answer, text_translation, language, translated_text)

        st.success(translator.translate("Dados inseridos com sucesso!"))

        query = "SELECT * FROM app_dados;"
        data = run_query(query)

        for row in data:
            st.write(f"Nome: {row[1]}, Idade: {row[2]}, Gênero: {row[3]}")
            st.write(f"Texto Sumarizado: {row[4]}")
            st.write(f"Resposta Gerada: {row[8]}")
            st.write("---")

if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    translate_page(translation_language)
