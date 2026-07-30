import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _build_database_uri():
    # Railway (u otros PaaS) exponen una URL de conexión completa via DATABASE_URL.
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        return database_url

    # Desarrollo local: variables sueltas en .env
    safe_password = quote_plus(os.getenv('DB_PASSWORD', ''))
    return (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{safe_password}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')

    # Configuracion de la DB
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Subida de imagenes de productos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'img')
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'webp'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB

    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
