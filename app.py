from flask import Flask, render_template, request
from resowners.database_helper import get_total_records, get_records

app = Flask(__name__)

LIMIT = 30  # количество записей на одной странице

@app.route('/', methods=['POST', 'GET'])
def index():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * LIMIT

    total = get_total_records()
    data = get_records(LIMIT, offset)

    pages = range(1, total // LIMIT + 2)
    return render_template('home.html', data=data, pages=pages, current_page=page)


if __name__ == '__main__':
    app.run(debug=True)
