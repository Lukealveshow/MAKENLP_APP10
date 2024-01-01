import mysql.connector
import streamlit as st

db_config = {
    'host': 'localhost',
    'user': "root",
    'password': "Luc@s1717##@@",
    'database': 'data'
}

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = mysql.connector.connect(**db_config)
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
