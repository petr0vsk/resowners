from flask import Flask, render_template_string
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

@app.route('/')
def index():
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    # Выполняем запрос к представлению vw_tmp_import
    cursor.execute("SELECT * FROM vw_tmp_import")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template_string("""
        <table>
            <tr>
                <th>Server Name</th>
                <th>Drive Path</th>
                <th>Path</th>
                <th>Owner</th>
                <th>Second Owner</th>
                <th>Note</th>
            </tr>
            {% for item in data %}
            <tr>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>{{ item[2] }}</td>
                <td>{{ item[3] }}</td>
                <td>{{ item[4] }}</td>
                <td>{{ item[5] }}</td>
            </tr>
            {% endfor %}
        </table>
    """, data=data)

if __name__ == '__main__':
    app.run(debug=True)
