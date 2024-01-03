import toml
import pymysql
import streamlit as st

# Carregar credenciais do secrets.toml
credentials = toml.load("secrets.toml")["mysql"]

db_config = {
    'host': credentials['host'],
    'user': credentials['user'],
    'password': credentials['password'],
    'database': credentials['database']
}

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as err:
        print("Error during insertion:", err)
