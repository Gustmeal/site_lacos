"""
Blueprint público do Site Laços.

Agrupa todas as rotas acessíveis sem autenticação:
- Página inicial
- Quem somos
- Atividades
- Listagem de clubes
- Contato (formulário)
"""

from flask import Blueprint

# Cria o blueprint
# - 'public' é o nome interno (usado em url_for)
# - template_folder e static_folder usam os defaults da app
public_bp = Blueprint("public", __name__)

# Importa as rotas DEPOIS de criar o blueprint
# (evita imports circulares)
from app.blueprints.public import routes