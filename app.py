from flask import Flask, render_template, g, request
from decouple import config
import psycopg2

app = Flask(__name__)

# Параметры подключения к PostgreSQL
DATABASE_CONFIG = {
    'dbname': config('DB_NAME'),
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'port': config('DB_PORT')
}

@app.route('/', methods=['POST', 'GET'])
def index():
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Выполняем запрос к представлению vw_tmp_import
    cursor.execute("SELECT * FROM vw_tmp_import")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('home.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
