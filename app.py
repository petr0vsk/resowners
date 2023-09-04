from flask import Flask, render_template, request
from resowners.database_helper import get_total_records, get_records, get_servers

app = Flask(__name__)

LIMIT = 30  # количество записей на одной странице

@app.route('/', methods=['POST', 'GET'])
def index():

    page = request.args.get('page', 1, type=int) # к-во страниц
    offset = (page - 1) * LIMIT # смещение
    servers = get_servers()
    print(servers)
    selected_server = request.args.get('server')
    if selected_server == "ALL": # обработаем п.меню для возврата к выбору всех серверов
        selected_server = None
    total = get_total_records(selected_server)
    if selected_server:  # Если сервер выбран
        data = get_records(selected_server, LIMIT, offset)
    else:  # Если сервер не выбран, выводим все данные
        data = get_records(None, LIMIT, offset)

    pages = range(1, total // LIMIT + 2)
    return render_template('home.html', data=data, pages=pages, current_page=page, servers=servers,
                           selected_server=selected_server)




if __name__ == '__main__':
    app.run(debug=True)
