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
    # Em desenvolvimento usa SQLite local com caminho absoluto.
    # Em produção (Railway), usa DATABASE_URL fornecido pelo PostgreSQL.
    _instance_db_path = basedir / "instance" / "site_lacos.db"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{_instance_db_path.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento local."""

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False  # True para ver todas as queries SQL


class ProductionConfig(Config):
    """Configuração para produção (Railway)."""

    DEBUG = False
    TESTING = False

    # === COOKIES DE SESSÃO ===
    # Força HTTPS e cookies seguros (Railway serve via HTTPS)
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Força url_for a gerar URLs com https://
    PREFERRED_URL_SCHEME = "https"

    # === BANCO DE DADOS ===
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