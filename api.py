# api.py
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Luc@s1717##@@'
app.config['MYSQL_DB'] = 'data'
mysql = MySQL(app)

@app.route('/enviar-dados', methods=['POST'])
def receber_e_salvar_dados():
    try:
        data = request.get_json()
        conn = mysql.connection
        cursor = conn.cursor()
        insert_query = '''INSERT INTO app_dados(name, age, gender, text_summarization, summarized_text,
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
        return jsonify({"message": "Dados inseridos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
