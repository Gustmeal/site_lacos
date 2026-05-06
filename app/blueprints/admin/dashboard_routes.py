"""
Rotas do dashboard administrativo.

Páginas internas que exigem autenticação.
"""

from flask import render_template
from flask_login import login_required, current_user

from app.blueprints.admin import admin_bp


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    """Página inicial do painel administrativo."""
    return render_template(
        "admin/dashboard.html",
        usuario=current_user,
    )