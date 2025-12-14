from flask import Blueprint, render_template, session, redirect, url_for
from app.models.checklist_data import get_all_checklists

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Página principal con listado de checklists"""
    checklists = get_all_checklists()
    return render_template("pages/index.html", checklists=checklists)


@main_bp.route("/home")
def limpiar():
    """Limpiar sesión y redirigir al inicio"""
    session.clear()
    return redirect(url_for("main.index"))


@main_bp.errorhandler(404)
def not_found(error):
    """Página de error 404"""
    return render_template("errors/404.html"), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Página de error 500"""
    return render_template("errors/500.html"), 500
