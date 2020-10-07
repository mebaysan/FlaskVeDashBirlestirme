"""Flask uygulamamıza ait ayarların tutulduğu dosya"""
from os import environ, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))


class Config:
    """Genel Flask Ayarları"""
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')

    """Static Dosya Ayarları"""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')
