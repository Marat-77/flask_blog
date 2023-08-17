import os

from dotenv import load_dotenv
from flask import Flask

from flask_front.users.auth import login_manager, auth_app
from flask_front.articles.views import article
from flask_front.authors.views import author
from flask_front.users.views import user
from flask_front.index.views import index
from flask_front.error_handlers.err_handler import error_


def create_app() -> Flask:
    app = Flask(__name__)
    load_dotenv()

    cfg_name = os.environ.get('CONFIG_NAME', 'DevConfig')
    print('CONFIG NAME:', cfg_name)
    app.config.from_object(f'flask_front.config.{cfg_name}')

    register_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(index)
    app.register_blueprint(error_)
    app.register_blueprint(auth_app, url_prefix="/auth")
    app.register_blueprint(author)


def register_extensions(app: Flask) -> None:
    login_manager.init_app(app)
