import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('sk')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # static_folder = 'flask_blog/static'
    static_folder = 'static'
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cosmo'
    JWT_SECRET_KEY = os.getenv('api_sk')


class DevConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    # postgres
    # SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# app.config['SECRET_KEY'] = os.getenv('sk')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
