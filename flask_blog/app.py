from flask import Flask, request, __version__
from werkzeug.exceptions import NotFound

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Flask'


@app.route('/flask/')
def flask_version():
    return f'Flask {__version__}'


@app.route('/sum/')
def sum_():
    print(request.base_url)
    return f'Чтобы найти сумму двух целых чисел (например 5 и 3): <br>' \
           f'в адресной строке наберите' \
           f' <a href="{request.base_url}5/3">{request.base_url}5/3</a>'


@app.route('/sum/<int:x>/<int:y>')
def sum_num(x: int, y: int):
    return f'Сумма: <br> {x} + {y} = {x + y}'


@app.errorhandler(NotFound)
def handle_error(err):
    print(request.base_url)
    return f'<h1> Ошибка {err.code}.</h1>' \
           f' Запрашиваемый URL-адрес ({request.base_url}) не найден.'

