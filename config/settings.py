import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Configuración base de la aplicación"""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 9015))

    # Session
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=int(os.getenv("SESSION_TIMEOUT", 120))
    )

    # Rutas de archivos
    OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
    TEMPLATES_DIR = BASE_DIR / os.getenv("TEMPLATES_DIR", "templates_excel")
    SHARED_NETWORK_PATH = os.getenv(
        "SHARED_NETWORK_PATH", r"\\172.16.1.22\checklist$\2025"
    )
    LOG_FILE = BASE_DIR / os.getenv("LOG_FILE", "logs/app.log")

    # Empresa
    DEFAULT_VALIDATOR = os.getenv("DEFAULT_VALIDATOR", "Andrés Herrera")
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Proquinal - SpradlingGroup")
    SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "josue.romero@spradling.group")
    SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "310 864 3149")

    # Red
    FILE_SERVER_IP = os.getenv("FILE_SERVER_IP", "172.16.1.22")
    CORPORATE_DOMAIN = os.getenv("CORPORATE_DOMAIN", "proquinal.com")

    # Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    ENABLE_CORS = os.getenv("ENABLE_CORS", "False").lower() == "true"

    @staticmethod
    def init_app(app):
        """Inicializar configuraciones de la aplicación"""
        # Crear directorios necesarios
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        Config.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


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
