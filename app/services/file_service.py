import os
import shutil
from flask import current_app


class FileService:
    """Servicio para manejar operaciones con archivos"""

    @staticmethod
    def copiar_a_red(archivo_local: str, nombre_archivo: str) -> bool:
        """
        Copiar archivo a carpeta compartida de red

        Args:
            archivo_local: Ruta del archivo local
            nombre_archivo: Nombre del archivo

        Returns:
            bool: True si se copió exitosamente, False si falló
        """
        try:
            shared_path = current_app.config["SHARED_NETWORK_PATH"]

            # Crear directorio si no existe
            os.makedirs(shared_path, exist_ok=True)

            destino = os.path.join(shared_path, nombre_archivo)
            shutil.copy(archivo_local, destino)

            current_app.logger.info(f"Archivo copiado a red: {destino}")
            return True

        except Exception as e:
            current_app.logger.error(f"Error al copiar archivo a red: {e}")
            return False

    @staticmethod
    def limpiar_archivos_antiguos(dias: int = 7):
        """
        Limpiar archivos antiguos del directorio de salida

        Args:
            dias: Días de antigüedad para eliminar archivos
        """
        import time

        try:
            output_dir = current_app.config["OUTPUT_DIR"]
            now = time.time()
            cutoff = now - (dias * 86400)  # días en segundos

            for filename in os.listdir(output_dir):
                filepath = os.path.join(output_dir, filename)

                if os.path.isfile(filepath):
                    file_modified = os.path.getmtime(filepath)

                    if file_modified < cutoff:
                        os.remove(filepath)
                        current_app.logger.info(f"Archivo eliminado: {filepath}")

        except Exception as e:
            current_app.logger.error(f"Error al limpiar archivos: {e}")

    @staticmethod
    def validar_plantilla(tipo: str) -> bool:
        """
        Validar que existe la plantilla para el tipo de checklist

        Args:
            tipo: Tipo de checklist

        Returns:
            bool: True si existe la plantilla
        """
        from app.models.checklist_data import get_checklist

        config = get_checklist(tipo)
        if not config:
            return False

        plantilla_path = os.path.join(
            current_app.config["TEMPLATES_DIR"], config["plantilla"]
        )

        return os.path.exists(plantilla_path)
