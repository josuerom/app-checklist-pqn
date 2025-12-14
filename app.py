"""
@author: Josué Romero
@date:   12/12/2025
"""

import os
from app import create_app

# Crear la aplicación
app = create_app()

if __name__ == "__main__":
    # Obtener configuración del entorno
    host = app.config.get("HOST", "0.0.0.0")
    port = app.config.get("PORT", 9015)
    debug = app.config.get("DEBUG", False)

    # Ejecutar aplicación
    app.run(host=host, port=port, debug=debug)
