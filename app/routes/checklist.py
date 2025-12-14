from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
)
from app.models.checklist_data import get_checklist, checklist_exists
from app.services.excel_service import ExcelService
from app.services.file_service import FileService
from app.utils.helpers import session_required

checklist_bp = Blueprint("checklist", __name__, url_prefix="/checklist")


@checklist_bp.route("/formulario/<tipo>", methods=["GET", "POST"])
def formulario(tipo):
    """Formulario para capturar datos iniciales del checklist"""
    if not checklist_exists(tipo):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        # Guardar datos en sesión
        session["activo_fijo"] = request.form.get("activo_fijo", "").strip()
        session["propietario"] = request.form.get("propietario", "").strip()
        session["cargo"] = request.form.get("cargo", "").strip()
        session["tecnico"] = request.form.get("tecnico", "").strip()
        session["tipo_checklist"] = tipo

        current_app.logger.info(
            f"Formulario completado - Tipo: {tipo}, "
            f"Activo: {session['activo_fijo']}"
        )

        return redirect(url_for("checklist.mostrar_checklist", tipo=tipo))

    config = get_checklist(tipo)
    return render_template("pages/checklist_form.html", checklist=config, tipo=tipo)


@checklist_bp.route("/<tipo>", methods=["GET"])
@session_required
def mostrar_checklist(tipo):
    """Mostrar el checklist interactivo"""
    if not checklist_exists(tipo):
        return redirect(url_for("main.index"))

    config = get_checklist(tipo)

    # Leer parámetros de mensaje de éxito
    mensaje = request.args.get("mensaje")
    archivo = request.args.get("archivo")

    # Enumerar preguntas
    preguntas_enumeradas = list(enumerate(config["preguntas"], 1))

    return render_template(
        "pages/checklist.html",
        checklist=config,
        tipo=tipo,
        preguntas=preguntas_enumeradas,
        session=session,
        mensaje=mensaje,
        archivo=archivo,
    )


@checklist_bp.route("/guardar/<tipo>", methods=["POST"])
@session_required
def guardar_checklist(tipo):
    """Guardar checklist y generar archivo Excel"""
    if not checklist_exists(tipo):
        return redirect(url_for("main.index"))

    try:
        config = get_checklist(tipo)

        # Recopilar respuestas del formulario
        respuestas = {}
        for i in range(len(config["preguntas"])):
            respuestas[i + 1] = request.form.get(f"pregunta_{i + 1}", "N/A")

        # Datos de sesión
        session_data = {
            "activo_fijo": session.get("activo_fijo"),
            "propietario": session.get("propietario"),
            "cargo": session.get("cargo"),
            "tecnico": session.get("tecnico"),
        }

        # Generar Excel
        archivo_local, nombre_archivo = ExcelService.generar_excel(
            tipo, respuestas, session_data
        )

        # Intentar copiar a carpeta compartida
        copia_exitosa = FileService.copiar_a_red(archivo_local, nombre_archivo)

        # Redirigir con mensaje
        mensaje_status = "1" if copia_exitosa else "0"

        return redirect(
            url_for(
                "checklist.mostrar_checklist",
                tipo=tipo,
                mensaje=mensaje_status,
                archivo=nombre_archivo,
            )
        )

    except Exception as e:
        current_app.logger.error(f"Error al guardar checklist: {e}")
        return redirect(
            url_for("checklist.mostrar_checklist", tipo=tipo, mensaje="error")
        )
