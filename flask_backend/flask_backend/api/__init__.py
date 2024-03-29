import os

from flask import Flask

from flask_backend.api.extensions import api, jwt
from flask_backend.api.resources import ns
# from flask_backend.models import User
from flask_backend.models.database import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)

    cfg_name = os.environ.get('CONFIG_NAME', default='DevConfig')
    print(cfg_name)
    app.config.from_object(f'flask_backend.config.{cfg_name}')
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    jwt.init_app(app)
    api.add_namespace(ns)
    return app
