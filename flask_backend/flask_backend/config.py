import os

# from dotenv import load_dotenv

# load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('sk')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # static_folder = 'flask_front/static'
    static_folder = 'static'
    WTF_CSRF_ENABLED = True
    JWT_SECRET_KEY = os.getenv('api_sk')


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
