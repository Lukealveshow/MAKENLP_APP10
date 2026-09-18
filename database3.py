import toml
import mysql.connector
import streamlit as st



db_config = {
    'host': 'mysql-b2a9c61-lucasalvesmartins10-3bb6.i.aivencloud.com',
    'port': 21742,
    'database': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_CjPHvwsnx0cY245d8Wz'
}

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        values = (name, age, gender, text_summarization, summarized_text, text_generation,
                  question, answer, text_translation, language, translated_text)
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as err:
        print("Error during insertion:", err)
