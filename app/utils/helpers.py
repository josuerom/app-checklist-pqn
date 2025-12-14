from functools import wraps
from flask import session, redirect, url_for, flash


def session_required(f):
    """
    Decorador para verificar que existan datos en sesión
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        required_keys = ["activo_fijo", "propietario", "cargo", "tecnico"]

        for key in required_keys:
            if key not in session:
                flash("Por favor, completa el formulario de datos iniciales", "warning")
                return redirect(
                    url_for("checklist.formulario", tipo=kwargs.get("tipo", "pc"))
                )

        return f(*args, **kwargs)

    return decorated_function


def sanitize_filename(filename: str) -> str:
    """
    Sanitizar nombre de archivo eliminando caracteres no permitidos

    Args:
        filename: Nombre de archivo original

    Returns:
        str: Nombre de archivo sanitizado
    """
    caracteres_invalidos = r'\/:*?"<>|'
    for char in caracteres_invalidos:
        filename = filename.replace(char, "_")

    return filename


def format_date(date_obj, format_str: str = "%d/%m/%Y") -> str:
    """
    Formatear fecha a string

    Args:
        date_obj: Objeto datetime
        format_str: Formato de salida

    Returns:
        str: Fecha formateada
    """
    return date_obj.strftime(format_str)


def get_client_ip(request):
    """
    Obtener IP del cliente

    Args:
        request: Objeto request de Flask

    Returns:
        str: IP del cliente
    """
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        return request.environ["REMOTE_ADDR"]
    else:
        return request.environ["HTTP_X_FORWARDED_FOR"]


def create_response_data(success: bool, message: str, data=None) -> dict:
    """
    Crear estructura estándar de respuesta

    Args:
        success: Indica si la operación fue exitosa
        message: Mensaje descriptivo
        data: Datos adicionales (opcional)

    Returns:
        dict: Respuesta estructurada
    """
    response = {"success": success, "message": message}

    if data is not None:
        response["data"] = data

    return response
