"""
Blueprint de autenticação pública.

Login único inteligente em /login que aceita todos os tipos de usuário
(admin_geral, admin_clube, familia) e redireciona para o lugar certo.
"""

from flask import Blueprint

auth_bp = Blueprint(
    "auth",
    __name__,
)

from app.blueprints.auth import routes