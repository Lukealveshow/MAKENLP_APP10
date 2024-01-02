import streamlit as st
import mysql.connector
from deep_translator import GoogleTranslator
from summarization import summarize_text
from generation import generate_answer

def my_hash_func(conn_config):
    host = conn_config.get("host", None)
    user = conn_config.get("user", None)
    database = conn_config.get("database", None)
    port = conn_config.get("port", None)
    
    return hash((host, user, database, port))

@st.cache(hash_funcs={mysql.connector.connection.MySQLConnection: id, dict: my_hash_func})
def init_connection():
    connection_config = {
        "host": st.secrets["connections.mysql"]["host"],
        "user": st.secrets["connections.mysql"]["username"],
        "password": st.secrets["connections.mysql"]["password"],
        "database": st.secrets["connections.mysql"]["database"],
        "port": st.secrets["connections.mysql"]["port"],
    }
    return mysql.connector.connect(**connection_config)

# Executa uma consulta SQL.
@st.cache(allow_output_mutation=True, hash_funcs={mysql.connector.connection.MySQLConnection: id})
def run_query(query):
    connection = init_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    connection.close()
    return result

def insert_data(connection_config, name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)

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

        insert_data(init_connection(), name, age, gender, text_summarization, summarized_text, text_generation,
                    question, answer, text_translation, language, translated_text)

        st.success(translator.translate("Dados inseridos com sucesso!"))

        query = "SELECT * app_dados;"
        data = run_query(query)

        for row in data:
            st.write(f"Nome: {row['name']}, Idade: {row['age']}, Gênero: {row['gender']}")
            st.write(f"Texto Sumarizado: {row['text_summarization']}")
            st.write(f"Resposta Gerada: {row['answer']}")
            st.write("---")

if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    translate_page(translation_language)
