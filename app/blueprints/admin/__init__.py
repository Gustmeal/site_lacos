"""
Blueprint administrativo do Site Laços.

Agrupa todas as rotas protegidas por autenticação:
- Login/logout
- Dashboard
- CRUD de eventos
- Gerenciamento de usuários
"""

from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)

# Importa rotas após criar o blueprint para evitar imports circulares
from app.blueprints.admin import (
    auth_routes,
    dashboard_routes,
    eventos_routes,
    usuarios_routes,
)