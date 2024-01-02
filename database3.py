import pymysql
import streamlit as st



# Utilize os segredos conforme necessário

db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        # Imprime os valores antes de executar a query
        print("Valores a serem inseridos:", (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Imprime uma mensagem de sucesso após o commit
        print("Data committed successfully.")
        
        st.success("Dados inseridos com sucesso!")
    except pymysql.Error as err:
        print("MySQL Error during insertion:", err)
