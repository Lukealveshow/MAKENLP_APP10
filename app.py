import streamlit as st
import requests
from deep_translator import GoogleTranslator
from summarization import summarize_text
from generation import generate_answer
from database3 import insert_data
def send_data_to_api(data):
    api_url = "http://localhost:5000/enviar-dados"  # Substitua pela URL da sua API
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        st.success("Dados enviados com sucesso para a API.")
    else:
        st.error(f"Erro ao enviar dados para a API. Status code: {response.status_code}")
def start_api():
    # Inicie o servidor Flask da API como um processo secundário
    subprocess.Popen(["python", "api.py"])
def translate_page(language):
    # Using deep_translator for page translation
    translator = GoogleTranslator(source='auto', target=language)
    translated_title = translator.translate("Seja Bem Vindo ao MAKENLP")
    st.title(translated_title)
    
    # Additional fields
    name_key = f'name_{language}'
    translated_name = translator.translate("Nome:")
    name = st.text_input(translated_name, key=name_key)
    
    age_key = f'age_{language}'
    translated_age = translator.translate("Idade:")
    age = st.number_input(translated_age, step=1, key=age_key)
    
    gender_key = f'gender_{language}'
    translated_gender = translator.translate("Gênero:")
    gender_options = [translator.translate('Masculino'), translator.translate('Feminino')]
    gender = st.selectbox(translated_gender, options=gender_options, key=gender_key)
    
    # Section for text input
    text_summarization_key = f'text_summarization_{language}'
    translated_text_input = translator.translate("Digite o texto para resumir:")
    text_summarization = st.text_area(translated_text_input, height=150, key=text_summarization_key)
    
    # Button to summarize text
    if st.button(translator.translate("Resumir Texto")):
        summarized_text = summarize_text(text_summarization)
        st.subheader(translator.translate("Texto Resumido"))
        st.write(summarized_text)
    
    text_generation_key = f'text_generation_{language}'
    translated_text_gen = translator.translate("Digite o texto:")
    st.subheader(translated_text_gen)
    text_generation = st.text_area("", height=150, key=text_generation_key)
    
    question_key = f'question_{language}'
    translated_question = translator.translate("Faça uma pergunta sobre o texto:")
    question = st.text_input(translated_question, key=question_key)
    
    # Button to generate answer
    if st.button(translator.translate("Gerar Resposta")):
        answer = generate_answer(question, text_generation)
        st.subheader(translator.translate("Resposta Gerada"))
        st.write(answer)
    
    # Section for text input and language selection
    text_translation_key = f'text_translation_{language}'
    translated_text_trans = translator.translate("Digite o texto para traduzir:")
    st.subheader(translated_text_trans)
    text_translation = st.text_area("", height=150, key=text_translation_key)
    
    language_key = f'language_{language}'
    translated_lang = translator.translate("Selecione o idioma de destino:")
    language_options = ['en', 'es', 'fr', 'pt']
    selected_language = st.selectbox(translated_lang, options=language_options, key=language_key)
    
    # Button to translate text
    if st.button(translator.translate("Traduzir Texto")):
        translated_text = GoogleTranslator(source='auto', target=selected_language).translate(text_translation)
        st.subheader(translator.translate("Texto Traduzido"))
        st.write(translated_text)
    
    if st.button(translator.translate("Enviar")):
        summarized_text = summarize_text(text_summarization)
        answer = generate_answer(question, text_generation)
        translated_text = GoogleTranslator(source='auto', target=language).translate(text_translation)

        # Dados a serem enviados para a API
        data_to_send = {
            "name": name,
            "age": age,
            "gender": gender,
            "text_summarization": text_summarization,
            "summarized_text": summarized_text,
            "text_generation": text_generation,
            "question": question,
            "answer": answer,
            "text_translation": text_translation,
            "language": language,
            "translated_text": translated_text
        }

        # Utilize a função send_data_to_api para enviar os dados para a API
        send_data_to_api(data_to_send)
        st.success(translator.translate("Dados enviados com sucesso!"))

# Run the Streamlit app
if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    start_api()
    translate_page(translation_language)
