"""
Script utilitário para criar as tabelas do banco de dados manualmente.

Use quando o Flask-Migrate não detectar automaticamente os modelos.

Uso:
    python -m app.utils.criar_tabelas
"""

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from app.models.evento import Evento


def criar_tabelas():
    """Cria todas as tabelas registradas nos modelos."""
    app = create_app()

    with app.app_context():
        print("\n" + "=" * 60)
        print("CRIANDO TABELAS DO BANCO DE DADOS")
        print("=" * 60)

        # Lista os modelos que serão criados
        print("\nModelos detectados:")
        print(f"  - {Usuario.__tablename__} ({Usuario.__name__})")
        print(f"  - {Evento.__tablename__} ({Evento.__name__})")

        # Cria as tabelas
        db.create_all()

        # Verifica se foram criadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tabelas = inspector.get_table_names()

        print(f"\nTabelas no banco após criação:")
        for tabela in tabelas:
            print(f"  - {tabela}")

        print("\n" + "=" * 60)
        print("TABELAS CRIADAS COM SUCESSO!")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    criar_tabelas()