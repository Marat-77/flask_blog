import os

from flask import Flask

from flask_blog.api.extensions import api, jwt
from flask_blog.api.resources import ns
from flask_blog.models.database import db


def create_app() -> Flask:
    app = Flask(__name__)

    cfg_name = os.environ.get('CONFIG_NAME', 'DevConfig')
    print(cfg_name)
    app.config.from_object(f'flask_blog.config.{cfg_name}')
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.add_namespace(ns)
    return app
