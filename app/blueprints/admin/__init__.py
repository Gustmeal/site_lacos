"""
Blueprint administrativo do Site Laços.

Agrupa todas as rotas protegidas por autenticação:
- Login/logout
- Dashboard
- CRUD de eventos
"""

from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="../../templates/admin",
)

# Importa rotas após criar o blueprint
from app.blueprints.admin import auth_routes