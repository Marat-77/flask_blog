import os

from flask import Flask
from dotenv import load_dotenv

from flask_blog.models.database import db
from flask_blog.users.auth import login_manager, auth_app
# from flask import request, __version__
# from werkzeug.exceptions import NotFound

from flask_blog.users.views import user
from flask_blog.articles.views import article
from flask_blog.index.views import index
from flask_blog.error_handlers.err_handler import error_


def create_app() -> Flask:
    app = Flask(__name__)
    load_dotenv()
    # app.config['SECRET_KEY'] = 'BWdOngZKV-iKp3QJIc79_g'
    app.config['SECRET_KEY'] = os.getenv('sk')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(index)
    app.register_blueprint(error_)
    app.register_blueprint(auth_app, url_prefix="/auth")


def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)


# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return 'Hello, Flask'
#
#
# @app.route('/flask/')
# def flask_version():
#     return f'Flask {__version__}'
#
#
# @app.route('/sum/')
# def sum_():
#     print(request.base_url)
#     return f'Чтобы найти сумму двух целых чисел (например 5 и 3): <br>' \
#            f'в адресной строке наберите' \
#            f' <a href="{request.base_url}5/3">{request.base_url}5/3</a>'
#
#
# @app.route('/sum/<int:x>/<int:y>')
# def sum_num(x: int, y: int):
#     return f'Сумма: <br> {x} + {y} = {x + y}'
#
#
# @app.errorhandler(NotFound)
# def handle_error(err):
#     print(request.base_url)
#     return f'<h1> Ошибка {err.code}.</h1>' \
#            f' Запрашиваемый URL-адрес ({request.base_url}) не найден.'

