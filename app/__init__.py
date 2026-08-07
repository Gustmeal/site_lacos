"""
Application factory do Site Laços.

Este módulo contém a função create_app(), que monta e retorna
uma instância da aplicação Flask configurada.

Padrão Application Factory:
- Permite criar múltiplas instâncias da app (útil para testes)
- Evita problemas de import circular
- Facilita a configuração por ambiente
"""

import os
from pathlib import Path
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import config_by_name
from app.extensions import (
    db,
    migrate,
    login_manager,
    bcrypt,
    mail,
    csrf,
    limiter,
)


def create_app(config_name=None):
    """
    Cria e configura uma instância da aplicação Flask.
    """
    # Define qual configuração usar
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Cria a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # ==========================================
    # PROXY FIX — obrigatório em produção (Railway)
    # ==========================================
    # O Railway serve HTTPS através de um proxy reverso.
    # Sem essa configuração, o Flask não sabe que está atrás de HTTPS,
    # e cookies com SESSION_COOKIE_SECURE=True são rejeitados.
    if config_name == "production":
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
            x_prefix=1,
        )

    # ==========================================
    # PASTA INSTANCE (para SQLite local)
    # ==========================================
    basedir = Path(__file__).resolve().parent.parent
    instance_dir = basedir / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Inicializa extensões
    _initialize_extensions(app)

    # Registra blueprints (rotas)
    _register_blueprints(app)

    # Registra handlers de erro
    _register_error_handlers(app)

    # ==========================================
    # FUNÇÕES GLOBAIS DO JINJA
    # ==========================================
    # Disponibiliza get_logo_clube() dentro dos templates,
    # permitindo que ela decida dinamicamente entre .webp e .png
    from app.data.clubes_data import get_logo_clube
    app.jinja_env.globals["get_logo_clube"] = get_logo_clube

    @app.route("/health")
    def health():
        """Endpoint para monitoramento (verifica se a app está viva)."""
        return {"status": "ok", "service": "site-lacos"}, 200

    return app


def _initialize_extensions(app):
    """Inicializa todas as extensões com a aplicação."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # IMPORTANTE: Importa todos os modelos para que o Flask-Migrate os detecte.
    # Não chama db.create_all() — usamos migrations (flask db upgrade).
    with app.app_context():
        from app.models import (  # noqa: F401
            Usuario,
            Evento,
            Candidata,
            IntencaoClube,
            Inscricao,
        )


def _register_blueprints(app):
    """Registra os blueprints (módulos de rotas)."""
    from app.blueprints.public import public_bp
    app.register_blueprint(public_bp)

    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.blueprints.setup import setup_bp
    app.register_blueprint(setup_bp)

    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.blueprints.familia import familia_bp
    app.register_blueprint(familia_bp)


def _register_error_handlers(app):
    """Registra handlers para erros HTTP."""

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>404 - Página não encontrada</h1>", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "<h1>500 - Erro interno do servidor</h1>", 500