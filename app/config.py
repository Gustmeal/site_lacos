"""
Configurações da aplicação Site Laços.

Este módulo define as configurações para diferentes ambientes
(desenvolvimento, produção, testes), seguindo o padrão de classes
de configuração do Flask.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
basedir = Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")


class Config:
    """Configuração base, herdada por todas as outras."""

    # Chave secreta para sessões e CSRF (NUNCA hardcoded em produção)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-dev-key-mude-isso"

    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{basedir / 'instance' / 'site_lacos.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de e-mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # Pasta de uploads (para fotos dos clubes, etc)
    UPLOAD_FOLDER = basedir / "app" / "static" / "uploads"
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    # Configurações gerais
    POSTS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento local."""

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False  # True para ver todas as queries SQL


class ProductionConfig(Config):
    """Configuração para produção (Railway)."""

    DEBUG = False
    TESTING = False

    # Em produção, força HTTPS e cookies seguros
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Railway fornece DATABASE_URL automaticamente
    # Mas pode vir como "postgres://" - precisa converter para "postgresql://"
    @staticmethod
    def fix_database_url(url):
        if url and url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url

    SQLALCHEMY_DATABASE_URI = fix_database_url(
        os.environ.get("DATABASE_URL")
    ) or Config.SQLALCHEMY_DATABASE_URI


class TestingConfig(Config):
    """Configuração para testes automatizados."""

    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # Desabilita CSRF em testes


# Mapeamento de configurações por nome
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}