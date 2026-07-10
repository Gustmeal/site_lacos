"""
Rotas de setup inicial (uso único em produção).

Para criar o primeiro admin em produção, use:
    GET  /setup/status          → verifica se setup é necessário
    POST /setup/criar-admin     → cria o primeiro admin

A rota só funciona se NÃO existir nenhum ADMIN GERAL no banco
e se a SETUP_SECRET_KEY for fornecida corretamente.
"""

import os
from flask import render_template, request, flash, redirect, url_for, abort

from app.blueprints.setup import setup_bp
from app.extensions import db, limiter
from app.models.usuario import Usuario, ROLE_ADMIN_GERAL


def _setup_disponivel():
    """
    Verifica se o setup ainda é necessário.
    Setup fica disponível se NÃO existe nenhum admin geral no banco.
    """
    return Usuario.query.filter_by(role=ROLE_ADMIN_GERAL).count() == 0


def _validar_secret_key(chave_fornecida):
    """Valida a chave secreta de setup."""
    chave_correta = os.environ.get("SETUP_SECRET_KEY")

    # Se não tem chave configurada no ambiente, bloqueia setup
    if not chave_correta:
        return False

    # Comparação direta (chaves longas tornam a comparação simples segura)
    return chave_fornecida == chave_correta


@setup_bp.route("/")
@setup_bp.route("/status")
def status():
    """Página inicial de status do setup."""

    if not _setup_disponivel():
        # Já tem admin geral, setup não é mais necessário
        return render_template("setup/desativado.html")

    return render_template("setup/status.html")


@setup_bp.route("/criar-admin", methods=["GET", "POST"])
@limiter.limit("3 per minute")
def criar_admin():
    """Cria o primeiro admin geral do sistema (só funciona se não existir admin geral)."""

    # Bloqueia se já tem admin geral no banco
    if not _setup_disponivel():
        return render_template("setup/desativado.html")

    if request.method == "POST":
        # Validações de campos
        chave = request.form.get("chave_setup", "").strip()
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        senha_confirma = request.form.get("senha_confirma", "")

        erros = []

        # Valida chave
        if not _validar_secret_key(chave):
            erros.append("Chave de setup inválida.")

        # Valida nome
        if len(nome) < 3:
            erros.append("Nome deve ter no mínimo 3 caracteres.")

        # Valida e-mail
        if "@" not in email or len(email) < 5:
            erros.append("E-mail inválido.")

        # Valida senha
        if len(senha) < 8:
            erros.append("Senha deve ter no mínimo 8 caracteres.")

        if senha != senha_confirma:
            erros.append("As senhas não conferem.")

        # Verifica se já existe usuário com esse email
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            erros.append(f"Já existe um usuário com o e-mail {email}.")

        # Se tem erros, mostra a página com mensagens
        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template(
                "setup/criar_admin.html",
                nome=nome,
                email=email,
            )

        # Cria o usuário admin geral
        try:
            novo_admin = Usuario(
                nome=nome,
                email=email,
                role=ROLE_ADMIN_GERAL,   # ← CORRIGIDO
                ativo=True,
            )
            novo_admin.set_senha(senha)

            db.session.add(novo_admin)
            db.session.commit()

            return render_template(
                "setup/sucesso.html",
                admin=novo_admin,
            )
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar admin: {str(e)}", "erro")
            return render_template(
                "setup/criar_admin.html",
                nome=nome,
                email=email,
            )

    return render_template("setup/criar_admin.html")