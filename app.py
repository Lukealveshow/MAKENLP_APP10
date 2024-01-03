import streamlit as st
from deep_translator import GoogleTranslator
from summarization import summarize_text
from generation import generate_answer
from database import insert_data

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

    # Button to execute all functions and insert into the database
    if st.button(translator.translate("Enviar")):
        try:
            summarized_text = summarize_text(text_summarization)
            answer = generate_answer(question, text_generation)
            translated_text = GoogleTranslator(source='auto', target=language).translate(text_translation)

            # Exibição dos dados antes da inserção
            st.subheader("Dados para Inserção:")
            st.write(f"Nome: {name}")
            st.write(f"Idade: {age}")
            st.write(f"Gênero: {gender}")
            st.write(f"Texto para Resumo: {text_summarization}")
            st.write(f"Texto Resumido: {summarized_text}")
            st.write(f"Texto para Geração: {text_generation}")
            st.write(f"Pergunta: {question}")
            st.write(f"Resposta Gerada: {answer}")
            st.write(f"Texto para Tradução: {text_translation}")
            st.write(f"Idioma de Destino: {language}")
            st.write(f"Texto Traduzido: {translated_text}")

            # Utilize a função insert_data do database.py
            st.success("Processando... Por favor, aguarde.")

            # Chame a função insert_data depois desta linha
            insert_data(name, age, gender, text_summarization, summarized_text, text_generation,
                        question, answer, text_translation, language, translated_text)

            st.success("Dados inseridos com sucesso!")
        except Exception as e:
            st.error(f"Erro durante a inserção: {e}")


# Run the Streamlit app
if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    translate_page(translation_language)
