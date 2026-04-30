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
from flask import Flask, render_template
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

    Args:
        config_name: Nome da configuração ('development', 'production',
                     'testing'). Se None, usa a variável de ambiente
                     FLASK_ENV ou 'development' como padrão.

    Returns:
        Flask app configurada.
    """
    # Define qual configuração usar
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    # Cria a aplicação
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # Garante que a pasta instance existe (para SQLite)
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

    # Rota temporária de "Hello World" (será removida na Sprint 1)
    @app.route("/")
    def hello():
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Site Laços - Em construção</title>
            <style>
                body {
                    font-family: -apple-system, sans-serif;
                    background: linear-gradient(135deg, #5BA3D0, #88C088);
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    text-align: center;
                }
                .container {
                    padding: 2rem;
                    background: rgba(255,255,255,0.1);
                    border-radius: 1rem;
                    backdrop-filter: blur(10px);
                    max-width: 500px;
                }
                h1 { font-size: 2.5rem; margin-bottom: 1rem; }
                p { font-size: 1.2rem; line-height: 1.6; }
                .badge {
                    display: inline-block;
                    background: rgba(255,255,255,0.2);
                    padding: 0.5rem 1rem;
                    border-radius: 2rem;
                    margin-top: 1rem;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Site Laços</h1>
                <p>Sprint 0 concluída com sucesso!</p>
                <p>Em breve, o site institucional da Associação de Clubes de Brasília.</p>
                <div class="badge">Em construção</div>
            </div>
        </body>
        </html>
        """

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


def _register_blueprints(app):
    """Registra os blueprints (módulos de rotas)."""
    # Blueprints serão adicionados nas próximas sprints
    # from app.blueprints.public import public_bp
    # app.register_blueprint(public_bp)
    pass


def _register_error_handlers(app):
    """Registra handlers para erros HTTP."""

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>404 - Página não encontrada</h1>", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "<h1>500 - Erro interno do servidor</h1>", 500