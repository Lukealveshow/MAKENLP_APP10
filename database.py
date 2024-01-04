import toml
import pymysql
import streamlit as st

credentials = toml.load("secrets.toml")["mysql"]

db_config = {
    'host': credentials['host'],
    'port': credentials.get('port', 3306)
    'password': credentials['password'],
    'database': credentials['database'],
    'port': credentials.get('port', 3306)  # Use 3306 se a porta não estiver definida no arquivo secrets.toml
}

def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO info(name, age, gender, text_summarization, summarized_text,
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
