"""
Inicialização de extensões do Flask.

As extensões são instanciadas aqui (sem app), e depois conectadas
à aplicação dentro do application factory (__init__.py).

Esse padrão evita imports circulares e permite múltiplas instâncias
da aplicação (útil para testes).
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ORM e migrações
db = SQLAlchemy()
migrate = Migrate()

# Autenticação
login_manager = LoginManager()
login_manager.login_view = "admin.login"  # Onde redirecionar se não logado
login_manager.login_message = "Por favor, faça login para acessar essa página."
login_manager.login_message_category = "info"


# ============================================
# USER LOADER TEMPORÁRIO
# ============================================
# Flask-Login exige uma função user_loader registrada.
# Como ainda não temos o modelo Usuario (vai ser criado na Sprint 5),
# registramos uma função stub que retorna None por enquanto.
# Quando criarmos o modelo Usuario, substituímos por busca real no banco.
@login_manager.user_loader
def load_user(user_id):
    """
    Carrega um usuário pelo ID.

    Por enquanto retorna None pois ainda não temos modelo Usuario.
    Será substituído na Sprint 5 quando criarmos autenticação.
    """
    return None


# Hash de senhas
bcrypt = Bcrypt()

# E-mail
mail = Mail()

# Proteção CSRF
csrf = CSRFProtect()

# Rate limiting (proteção contra spam/brute force)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)