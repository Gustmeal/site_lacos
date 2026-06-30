"""
Blueprint administrativo do Site Laços.
"""

from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)

# Importa rotas após criar o blueprint
from app.blueprints.admin import (
    auth_routes,
    dashboard_routes,
    eventos_routes,
    usuarios_routes,
    admin_clubes_routes,
)