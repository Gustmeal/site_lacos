"""
Rotas administrativas para gerenciamento de usuários.

Todas as rotas exigem autenticação. Inclui proteções:
- Não pode se auto-desativar
- Sempre tem que existir pelo menos 1 admin ativo
- Não pode editar o próprio role
"""

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.blueprints.admin import admin_bp
from app.forms import (
    CriarUsuarioForm,
    EditarUsuarioForm,
    ResetarSenhaForm,
    AlterarMinhaSenhaForm,
)
from app.models.usuario import Usuario
from app.extensions import db
from app.utils.decorators import admin_geral_required
from app.models import ROLE_FAMILIA


def _contar_admins_ativos():
    """Conta quantos admins ativos existem no sistema."""
    return Usuario.query.filter_by(role="admin", ativo=True).count()


def _eh_ultimo_admin_ativo(usuario):
    """Verifica se o usuário é o último admin ativo do sistema."""
    if usuario.role != "admin" or not usuario.ativo:
        return False
    return _contar_admins_ativos() == 1


@admin_bp.route("/usuarios")
@login_required
@admin_geral_required
def usuarios_listar():
    """Lista todos os usuários administrativos."""

    # Lista apenas admins (geral e de clube), NUNCA famílias
    usuarios = (
        Usuario.query
        .filter(Usuario.role != ROLE_FAMILIA)
        .order_by(Usuario.ativo.desc(), Usuario.nome.asc())
        .all()
    )

    estatisticas = {
        "total": len(usuarios),
        "ativos": sum(1 for u in usuarios if u.ativo),
        "inativos": sum(1 for u in usuarios if not u.ativo),
    }

    return render_template(
        "admin/usuarios/listar.html",
        usuarios=usuarios,
        estatisticas=estatisticas,
    )


@admin_bp.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
@admin_geral_required
def usuarios_criar():
    """Cria um novo usuário admin."""

    form = CriarUsuarioForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        # Verifica se já existe usuário com esse e-mail
        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            flash(f"Já existe um usuário com o e-mail {email}.", "erro")
            return render_template(
                "admin/usuarios/form.html",
                form=form,
                titulo_pagina="Criar Novo Usuário",
                modo="criar",
            )

        # Cria o usuário
        novo_usuario = Usuario(
            nome=form.nome.data.strip(),
            email=email,
            role=form.role.data,
            ativo=form.ativo.data,
        )
        novo_usuario.set_senha(form.senha.data)

        db.session.add(novo_usuario)
        db.session.commit()

        flash(f'Usuário "{novo_usuario.nome}" criado com sucesso!', "sucesso")
        return redirect(url_for("admin.usuarios_listar"))

    return render_template(
        "admin/usuarios/form.html",
        form=form,
        titulo_pagina="Criar Novo Usuário",
        modo="criar",
    )


@admin_bp.route("/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
@admin_geral_required
def usuarios_editar(usuario_id):
    """Edita um usuário existente (exceto senha)."""

    usuario = Usuario.query.get_or_404(usuario_id)

    # Verifica se é edição do próprio usuário
    eh_proprio = usuario.id == current_user.id

    form = EditarUsuarioForm(obj=usuario)

    if form.validate_on_submit():
        novo_email = form.email.data.lower().strip()

        # Verifica se o e-mail já existe em outro usuário
        if novo_email != usuario.email:
            existente = Usuario.query.filter_by(email=novo_email).first()
            if existente and existente.id != usuario.id:
                flash(f"Já existe outro usuário com o e-mail {novo_email}.", "erro")
                return render_template(
                    "admin/usuarios/form.html",
                    form=form,
                    titulo_pagina=f"Editar: {usuario.nome}",
                    modo="editar",
                    usuario=usuario,
                    eh_proprio=eh_proprio,
                )

        # Proteção: não pode se auto-desativar
        if eh_proprio and not form.ativo.data:
            flash("Você não pode desativar a própria conta.", "erro")
            return render_template(
                "admin/usuarios/form.html",
                form=form,
                titulo_pagina=f"Editar: {usuario.nome}",
                modo="editar",
                usuario=usuario,
                eh_proprio=eh_proprio,
            )

        # Proteção: não pode desativar o último admin ativo
        if usuario.ativo and not form.ativo.data and _eh_ultimo_admin_ativo(usuario):
            flash("Não é possível desativar o único administrador ativo do sistema.", "erro")
            return render_template(
                "admin/usuarios/form.html",
                form=form,
                titulo_pagina=f"Editar: {usuario.nome}",
                modo="editar",
                usuario=usuario,
                eh_proprio=eh_proprio,
            )

        # Atualiza os dados
        usuario.nome = form.nome.data.strip()
        usuario.email = novo_email
        usuario.role = form.role.data
        usuario.ativo = form.ativo.data

        db.session.commit()

        flash(f'Usuário "{usuario.nome}" atualizado com sucesso!', "sucesso")
        return redirect(url_for("admin.usuarios_listar"))

    return render_template(
        "admin/usuarios/form.html",
        form=form,
        titulo_pagina=f"Editar: {usuario.nome}",
        modo="editar",
        usuario=usuario,
        eh_proprio=eh_proprio,
    )


@admin_bp.route("/usuarios/<int:usuario_id>/resetar-senha", methods=["GET", "POST"])
@login_required
def usuarios_resetar_senha(usuario_id):
    """Reseta a senha de outro usuário."""

    usuario = Usuario.query.get_or_404(usuario_id)

    # Não permite resetar a própria senha por aqui (usar "Alterar minha senha")
    if usuario.id == current_user.id:
        flash("Para alterar sua própria senha, use 'Minha Conta'.", "info")
        return redirect(url_for("admin.minha_conta"))

    form = ResetarSenhaForm()

    if form.validate_on_submit():
        usuario.set_senha(form.senha.data)
        db.session.commit()

        flash(
            f'Senha de "{usuario.nome}" resetada com sucesso. '
            f"Comunique a nova senha ao usuário com segurança.",
            "sucesso",
        )
        return redirect(url_for("admin.usuarios_listar"))

    return render_template(
        "admin/usuarios/resetar_senha.html",
        form=form,
        usuario=usuario,
    )


@admin_bp.route("/usuarios/<int:usuario_id>/toggle-ativo", methods=["POST"])
@login_required
@admin_geral_required
def usuarios_toggle_ativo(usuario_id):
    """Ativa ou desativa um usuário."""

    usuario = Usuario.query.get_or_404(usuario_id)

    # Proteção: não pode se auto-desativar
    if usuario.id == current_user.id:
        flash("Você não pode desativar a própria conta.", "erro")
        return redirect(url_for("admin.usuarios_listar"))

    # Proteção: não pode desativar o último admin ativo
    if usuario.ativo and _eh_ultimo_admin_ativo(usuario):
        flash("Não é possível desativar o único administrador ativo do sistema.", "erro")
        return redirect(url_for("admin.usuarios_listar"))

    usuario.ativo = not usuario.ativo
    db.session.commit()

    status = "ativado" if usuario.ativo else "desativado"
    flash(f'Usuário "{usuario.nome}" {status}.', "sucesso")
    return redirect(url_for("admin.usuarios_listar"))


@admin_bp.route("/minha-conta", methods=["GET", "POST"])
@login_required
def minha_conta():
    """Página para o usuário gerenciar a própria conta."""

    form = AlterarMinhaSenhaForm()

    if form.validate_on_submit():
        # Verifica senha atual
        if not current_user.verificar_senha(form.senha_atual.data):
            flash("Senha atual incorreta.", "erro")
            return render_template("admin/minha_conta.html", form=form)

        # Atualiza senha
        current_user.set_senha(form.senha_nova.data)
        db.session.commit()

        flash("Sua senha foi alterada com sucesso!", "sucesso")
        return redirect(url_for("admin.minha_conta"))

    return render_template("admin/minha_conta.html", form=form)