from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'roottupa2023',
    'database': 'data'
}

def insert_data_into_database(data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_data(name, age, gender, text_summarization, summarized_text,
                          text_generation, question, answer, text_translation, language, translated_text)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (
            data['name'], data['age'], data['gender'], data['text_summarization'],
            data['summarized_text'], data['text_generation'], data['question'],
            data['answer'], data['text_translation'], data['language'], data['translated_text']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return False

@app.route('/enviar-dados', methods=['POST'])
def receber_dados():
    data = request.get_json()
    success = insert_data_into_database(data)
    if success:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
