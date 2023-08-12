import os

from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT', default=5050)
API_TIMEOUT = int(os.getenv('API_TIMEOUT', default=15))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('sk')
    static_folder = 'static'
    WTF_CSRF_ENABLED = True


class DevConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
