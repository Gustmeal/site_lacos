"""
Rotas de autenticação única.

- /login: aceita qualquer role e roteia para o lugar correto
- /logout: encerra sessão de qualquer tipo de usuário
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app.blueprints.auth import auth_bp
from app.extensions import db, limiter
from app.forms import LoginForm
from app.models import Usuario


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    """
    Login único inteligente.

    Aceita qualquer role (admin_geral, admin_clube, familia)
    e redireciona baseado no tipo de usuário.
    """

    # Se já está logado, redireciona para o painel correto
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.verificar_senha(form.senha.data):
            flash("E-mail ou senha inválidos.", "erro")
            return render_template("auth/login.html", form=form)

        if not usuario.ativo:
            flash("Sua conta está desativada. Entre em contato com o clube ou com a Laços.", "erro")
            return render_template("auth/login.html", form=form)

        # Login OK
        login_user(usuario)
        usuario.ultimo_login = datetime.utcnow()
        db.session.commit()

        flash(f"Bem-vinda, {usuario.nome}!", "sucesso")
        return _redirect_by_role(usuario)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """Encerra a sessão de qualquer tipo de usuário."""
    if current_user.is_authenticated:
        logout_user()
        flash("Você saiu com sucesso.", "sucesso")
    return redirect(url_for("public.home"))


def _redirect_by_role(usuario):
    """Redireciona o usuário baseado no seu role."""
    if usuario.is_admin_geral() or usuario.is_admin_clube():
        return redirect(url_for("admin.dashboard"))
    elif usuario.is_familia():
        return redirect(url_for("familia.painel"))
    else:
        # Fallback improvável
        flash("Tipo de conta desconhecido. Contate o suporte.", "erro")
        logout_user()
        return redirect(url_for("public.home"))