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