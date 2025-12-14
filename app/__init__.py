import os
import logging
from flask import Flask
from config.settings import get_config


def create_app():
    """Factory para crear la aplicación Flask"""

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )

    # Cargar configuración
    config_class = get_config()
    app.config.from_object(config_class)
    config_class.init_app(app)

    # Configurar logging
    setup_logging(app)

    # Registrar blueprints
    register_blueprints(app)

    # Registrar filtros de templates
    register_template_filters(app)

    app.logger.info("Aplicación iniciada correctamente")

    return app


def setup_logging(app):
    """Configurar sistema de logs"""
    import os

    log_level = getattr(logging, app.config["LOG_LEVEL"])

    # Asegurar que el directorio de logs existe
    log_file_path = app.config["LOG_FILE"]
    log_dir = os.path.dirname(log_file_path)

    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Formato de logs
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Handler para archivo
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Agregar handlers
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)


def register_blueprints(app):
    """Registrar blueprints de la aplicación"""
    from app.routes.main import main_bp
    from app.routes.checklist import checklist_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(checklist_bp)


def register_template_filters(app):
    """Registrar filtros personalizados para templates"""

    @app.template_filter("format_date")
    def format_date_filter(date, format_str="%d/%m/%Y"):
        """Filtro para formatear fechas"""
        if date is None:
            return ""
        return date.strftime(format_str)
