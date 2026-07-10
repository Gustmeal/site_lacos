"""
Rotas de autenticação do painel admin.

Inclui login, logout e proteção contra brute force via rate limiting.
"""

from datetime import datetime
from urllib.parse import urlparse
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.blueprints.admin import admin_bp
from app.forms import LoginForm
from app.models.usuario import Usuario
from app.extensions import db, limiter


@admin_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    """Página de login do painel admin."""

    # Se já estiver logado, redireciona direto para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        # Busca usuário pelo e-mail (case insensitive)
        usuario = Usuario.query.filter_by(email=form.email.data.lower()).first()

        # Verifica usuário e senha
        if usuario is None or not usuario.verificar_senha(form.senha.data):
            flash("E-mail ou senha incorretos.", "erro")
            return redirect(url_for("admin.login"))

        # Verifica se conta está ativa
        if not usuario.ativo:
            flash("Esta conta está desativada. Entre em contato com o administrador.", "erro")
            return redirect(url_for("admin.login"))

        # Faz login
        login_user(usuario, remember=form.lembrar_me.data)

        # Atualiza último login
        usuario.ultimo_login = datetime.utcnow()
        db.session.commit()

        # Redireciona para a página solicitada (ou dashboard)
        next_page = request.args.get("next")
        # Validação de segurança: só redireciona para URLs internas
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("admin.dashboard")

        flash(f"Bem-vindo(a), {usuario.nome}!", "sucesso")
        return redirect(next_page)

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    """Encerra a sessão do usuário."""
    nome = current_user.nome
    logout_user()
    flash(f"Sessão encerrada. Até logo, {nome}!", "info")
    return redirect(url_for("public.home"))