"""
Blueprint de setup inicial.

Contém rotas especiais usadas APENAS uma vez para configuração
inicial em produção (criar primeiro admin).

Estas rotas se auto-desativam quando já existem usuários no banco.
"""

from flask import Blueprint

setup_bp = Blueprint(
    "setup",
    __name__,
    url_prefix="/setup",
)

# Importa rotas após criar o blueprint
from app.blueprints.setup import routes