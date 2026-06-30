"""
Rotas para gerenciamento de Admins de Clube.

Acessível apenas para admin_geral.
"""

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.forms import (
    CriarAdminClubeForm,
    EditarAdminClubeForm,
    ResetarSenhaForm,
)
from app.models import Usuario, ROLE_ADMIN_CLUBE
from app.data.clubes_data import get_todos_clubes, get_clube_por_slug
from app.utils.decorators import admin_geral_required


def _get_choices_clubes():
    """Retorna a lista de clubes formatada para SelectField."""
    return [
        (c["slug"], f"{c['nome']} — {c['regiao']}")
        for c in get_todos_clubes()
    ]


@admin_bp.route("/admins-clube")
@login_required
@admin_geral_required
def admin_clubes_listar():
    """Lista todos os admins de clube."""
    admins = (
        Usuario.query
        .filter_by(role=ROLE_ADMIN_CLUBE)
        .order_by(Usuario.ativo.desc(), Usuario.nome.asc())
        .all()
    )

    # Enriquece com dados do clube
    for admin in admins:
        admin.clube_info = get_clube_por_slug(admin.clube_slug)

    estatisticas = {
        "total": len(admins),
        "ativos": sum(1 for a in admins if a.ativo),
        "inativos": sum(1 for a in admins if not a.ativo),
    }

    return render_template(
        "admin/admins_clube/listar.html",
        admins=admins,
        estatisticas=estatisticas,
    )


@admin_bp.route("/admins-clube/novo", methods=["GET", "POST"])
@login_required
@admin_geral_required
def admin_clubes_criar():
    """Cria um novo admin de clube."""
    form = CriarAdminClubeForm()
    form.clube_slug.choices = _get_choices_clubes()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        # Verifica e-mail duplicado
        if Usuario.query.filter_by(email=email).first():
            flash(f"Já existe um usuário com o e-mail {email}.", "erro")
            return render_template(
                "admin/admins_clube/form.html",
                form=form,
                titulo_pagina="Criar Admin de Clube",
                modo="criar",
            )

        # Verifica se já existe admin para esse clube
        existente_clube = Usuario.query.filter_by(
            role=ROLE_ADMIN_CLUBE,
            clube_slug=form.clube_slug.data,
        ).first()
        if existente_clube:
            clube_info = get_clube_por_slug(form.clube_slug.data)
            flash(
                f"O clube {clube_info['nome']} já tem um admin: {existente_clube.email}. "
                f"Edite a conta existente ou desative-a antes de criar uma nova.",
                "erro",
            )
            return render_template(
                "admin/admins_clube/form.html",
                form=form,
                titulo_pagina="Criar Admin de Clube",
                modo="criar",
            )

        novo = Usuario(
            nome=form.nome.data.strip(),
            email=email,
            role=ROLE_ADMIN_CLUBE,
            clube_slug=form.clube_slug.data,
            ativo=form.ativo.data,
        )
        novo.set_senha(form.senha.data)

        db.session.add(novo)
        db.session.commit()

        clube_info = get_clube_por_slug(novo.clube_slug)
        flash(
            f'Admin do Clube {clube_info["nome"]} criado com sucesso!',
            "sucesso",
        )
        return redirect(url_for("admin.admin_clubes_listar"))

    return render_template(
        "admin/admins_clube/form.html",
        form=form,
        titulo_pagina="Criar Admin de Clube",
        modo="criar",
    )


@admin_bp.route("/admins-clube/<int:admin_id>/editar", methods=["GET", "POST"])
@login_required
@admin_geral_required
def admin_clubes_editar(admin_id):
    """Edita um admin de clube existente."""
    admin = Usuario.query.get_or_404(admin_id)

    if not admin.is_admin_clube():
        flash("Usuário não é um admin de clube.", "erro")
        return redirect(url_for("admin.admin_clubes_listar"))

    form = EditarAdminClubeForm(obj=admin)
    form.clube_slug.choices = _get_choices_clubes()

    if form.validate_on_submit():
        novo_email = form.email.data.lower().strip()

        # Valida e-mail duplicado
        if novo_email != admin.email:
            existente = Usuario.query.filter_by(email=novo_email).first()
            if existente and existente.id != admin.id:
                flash(f"Já existe outro usuário com o e-mail {novo_email}.", "erro")
                return render_template(
                    "admin/admins_clube/form.html",
                    form=form,
                    titulo_pagina=f"Editar: {admin.nome}",
                    modo="editar",
                    admin=admin,
                )

        # Valida clube duplicado
        if form.clube_slug.data != admin.clube_slug:
            existente_clube = Usuario.query.filter_by(
                role=ROLE_ADMIN_CLUBE,
                clube_slug=form.clube_slug.data,
            ).first()
            if existente_clube and existente_clube.id != admin.id:
                clube_info = get_clube_por_slug(form.clube_slug.data)
                flash(
                    f"O clube {clube_info['nome']} já tem outro admin vinculado.",
                    "erro",
                )
                return render_template(
                    "admin/admins_clube/form.html",
                    form=form,
                    titulo_pagina=f"Editar: {admin.nome}",
                    modo="editar",
                    admin=admin,
                )

        admin.nome = form.nome.data.strip()
        admin.email = novo_email
        admin.clube_slug = form.clube_slug.data
        admin.ativo = form.ativo.data

        db.session.commit()

        flash(f'Admin "{admin.nome}" atualizado com sucesso!', "sucesso")
        return redirect(url_for("admin.admin_clubes_listar"))

    return render_template(
        "admin/admins_clube/form.html",
        form=form,
        titulo_pagina=f"Editar: {admin.nome}",
        modo="editar",
        admin=admin,
    )


@admin_bp.route("/admins-clube/<int:admin_id>/resetar-senha", methods=["GET", "POST"])
@login_required
@admin_geral_required
def admin_clubes_resetar_senha(admin_id):
    """Reseta a senha de um admin de clube."""
    admin = Usuario.query.get_or_404(admin_id)

    if not admin.is_admin_clube():
        flash("Usuário não é um admin de clube.", "erro")
        return redirect(url_for("admin.admin_clubes_listar"))

    form = ResetarSenhaForm()

    if form.validate_on_submit():
        admin.set_senha(form.senha.data)
        db.session.commit()

        flash(
            f'Senha de "{admin.nome}" resetada com sucesso. '
            f"Comunique a nova senha de forma segura.",
            "sucesso",
        )
        return redirect(url_for("admin.admin_clubes_listar"))

    return render_template(
        "admin/admins_clube/resetar_senha.html",
        form=form,
        admin=admin,
    )


@admin_bp.route("/admins-clube/<int:admin_id>/toggle-ativo", methods=["POST"])
@login_required
@admin_geral_required
def admin_clubes_toggle_ativo(admin_id):
    """Ativa ou desativa um admin de clube."""
    admin = Usuario.query.get_or_404(admin_id)

    if not admin.is_admin_clube():
        flash("Usuário não é um admin de clube.", "erro")
        return redirect(url_for("admin.admin_clubes_listar"))

    admin.ativo = not admin.ativo
    db.session.commit()

    status = "ativado" if admin.ativo else "desativado"
    flash(f'Admin "{admin.nome}" {status}.', "sucesso")
    return redirect(url_for("admin.admin_clubes_listar"))