import mysql.connector
import streamlit as st
db_secrets = st.secrets.get("connections.mysql", {})


# Utilize os segredos conforme necessário
db_username = db_secrets.get("username", "")
db_password = db_secrets.get("password", "")
db_config = {
    'host': 'localhost',
    'user': db_username,
    'password': db_password,
    'database': 'app'
}
def insert_data(name, age, gender, text_summarization, summarized_text, text_generation, question,
                answer, text_translation, language, translated_text):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO apps(name, age, gender, text_summarization, summarized_text,
          text_generation, question, answer, text_translation, language, translated_text)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (name, age, gender, text_summarization, summarized_text, text_generation,
                                      question, answer, text_translation, language, translated_text))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print("MySQL Error during insertion:", err)  
