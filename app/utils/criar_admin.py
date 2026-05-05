"""
Script utilitário para criar o primeiro usuário administrador.

Uso:
    python -m app.utils.criar_admin

Solicitará nome, email e senha interativamente.
"""

import getpass
from app import create_app
from app.extensions import db
from app.models.usuario import Usuario


def criar_admin():
    """Cria interativamente o primeiro usuário admin."""
    app = create_app()

    with app.app_context():
        print("\n" + "=" * 50)
        print("CRIAR USUÁRIO ADMINISTRADOR - SITE LAÇOS")
        print("=" * 50 + "\n")

        # Coleta dados
        nome = input("Nome completo: ").strip()
        if not nome:
            print("ERRO: Nome é obrigatório.")
            return

        email = input("E-mail: ").strip().lower()
        if not email or "@" not in email:
            print("ERRO: E-mail inválido.")
            return

        # Verifica se já existe
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            print(f"ERRO: Já existe usuário com o e-mail {email}.")
            return

        # Senha (sem mostrar na tela)
        senha = getpass.getpass("Senha (mínimo 8 caracteres): ")
        if len(senha) < 8:
            print("ERRO: Senha deve ter no mínimo 8 caracteres.")
            return

        senha_confirma = getpass.getpass("Confirme a senha: ")
        if senha != senha_confirma:
            print("ERRO: Senhas não conferem.")
            return

        # Cria o usuário
        novo_admin = Usuario(
            nome=nome,
            email=email,
            role="admin",
            ativo=True,
        )
        novo_admin.set_senha(senha)

        db.session.add(novo_admin)
        db.session.commit()

        print("\n" + "=" * 50)
        print("USUÁRIO ADMIN CRIADO COM SUCESSO!")
        print("=" * 50)
        print(f"Nome: {novo_admin.nome}")
        print(f"E-mail: {novo_admin.email}")
        print(f"ID: {novo_admin.id}")
        print(f"Acesse: http://localhost:5000/admin/login")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    criar_admin()