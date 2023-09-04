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
LIMIT = 30  # количество записей на одной странице

@app.route('/', methods=['POST', 'GET'])
def index():
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * LIMIT

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vw_tmp_import")
    total = cursor.fetchone()[0]

    cursor.execute(f"SELECT * FROM vw_tmp_import LIMIT {LIMIT} OFFSET {offset}")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    pages = range(1, total // LIMIT + 2)
    return render_template('home.html', data=data, pages=pages, current_page=page)


if __name__ == '__main__':
    app.run(debug=True)
