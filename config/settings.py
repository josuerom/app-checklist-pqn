import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise RuntimeError(f"Variable de entorno requerida no definida: {key}")
    return value


class Config:
    # Flask
    SECRET_KEY = env("SECRET_KEY")
    DEBUG = env("DEBUG") == "True"

    # Server
    HOST = env("HOST")
    PORT = int(env("PORT"))

    # Session
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(env("SESSION_TIMEOUT")))

    # Paths
    OUTPUT_DIR = BASE_DIR / env("OUTPUT_DIR")
    TEMPLATES_DIR = BASE_DIR / env("TEMPLATES_DIR")
    SHARED_NETWORK_PATH = env("SHARED_NETWORK_PATH")
    LOGS_DIR = BASE_DIR / env("LOG_DIR")
    LOG_FILE = BASE_DIR / env("LOG_FILE")

    # Empresa
    DEFAULT_VALIDATOR = env("DEFAULT_VALIDATOR")
    COMPANY_NAME = env("COMPANY_NAME")
    SUPPORT_EMAIL = env("SUPPORT_EMAIL")
    SUPPORT_PHONE = env("SUPPORT_PHONE")
    GITHUB = env("GITHUB")

    # Red
    FILE_SERVER_IP = env("FILE_SERVER_IP")
    CORPORATE_DOMAIN = env("CORPORATE_DOMAIN")
    USER_DOMAIN = env("USER_DOMAIN")
    PASSWD_DOMAIN = env("PASSWD_DOMAIN")

    # Logs
    LOG_LEVEL = env("LOG_LEVEL")

    # CORS
    ENABLE_CORS = env("ENABLE_CORS").lower() == "true"

    @staticmethod
    def init_app(app):
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        Config.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción"""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuración para testing"""

    TESTING = True
    DEBUG = True


# Diccionario de configuraciones
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Obtener configuración según el entorno"""
    env = os.getenv("FLASK_ENV", "development")
    return config.get(env, config["default"])
