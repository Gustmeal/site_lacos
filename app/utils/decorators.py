"""
Decorators de permissão para rotas administrativas.

Uso:
    @admin_geral_required
    def rota_que_so_admin_geral_acessa():
        ...

    @admin_required  # admin_geral OU admin_clube
    def rota_de_admin():
        ...
"""

from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def admin_geral_required(f):
    """
    Bloqueia acesso a quem não é admin_geral.

    Admin de clube e família NÃO passam.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login"))

        if not current_user.is_admin_geral():
            flash("Você não tem permissão para acessar esta página.", "erro")
            return redirect(url_for("admin.dashboard"))

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Permite acesso a admin_geral OU admin_clube.

    Famílias NÃO passam.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login"))

        if not (current_user.is_admin_geral() or current_user.is_admin_clube()):
            flash("Você não tem permissão para acessar esta página.", "erro")
            return redirect(url_for("admin.dashboard"))

        return f(*args, **kwargs)

    return decorated_function


def clube_required(slug_param="slug"):
    """
    Para rotas que recebem um clube como parâmetro.
    Garante que o usuário tem permissão para gerenciar AQUELE clube.

    Admin geral acessa qualquer clube.
    Admin de clube só acessa o próprio.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("admin.login"))

            slug_solicitado = kwargs.get(slug_param)

            if not current_user.pode_gerenciar_clube(slug_solicitado):
                flash("Você não tem permissão para acessar este clube.", "erro")
                return redirect(url_for("admin.dashboard"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator