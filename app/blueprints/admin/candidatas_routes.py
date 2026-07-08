"""
Rotas para gerenciamento de Candidatas (filhas) de cada família.
"""

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.forms.familia_forms import CandidataForm
from app.models import Usuario, Candidata, ROLE_FAMILIA
from app.data.clubes_data import get_todos_clubes, get_clube_por_slug
from app.utils.decorators import admin_required


def _get_choices_clubes_permitidos():
    """
    Retorna choices de clubes que o usuário atual pode gerenciar.
    - admin_geral: todos
    - admin_clube: apenas o dele
    """
    if current_user.is_admin_geral():
        clubes = get_todos_clubes()
    elif current_user.is_admin_clube():
        clube = get_clube_por_slug(current_user.clube_slug)
        clubes = [clube] if clube else []
    else:
        clubes = []

    return [(c["slug"], f"{c['nome']} — {c['regiao']}") for c in clubes]


def _pode_ver_familia(familia):
    """
    admin_geral vê qualquer família.
    admin_clube vê família se:
      - Tem candidata no clube dele (regra padrão), OU
      - A família ainda não tem NENHUMA candidata (para poder adicionar a primeira)
    """
    if current_user.is_admin_geral():
        return True

    if current_user.is_admin_clube():
        # Se família não tem nenhuma candidata, qualquer admin de clube pode acessá-la
        # (para adicionar a primeira candidata do clube dele)
        total_candidatas = familia.candidatas.count()
        if total_candidatas == 0:
            return True

        # Se já tem candidatas, admin de clube só vê se alguma for do clube dele
        return familia.candidatas.filter_by(
            clube_slug=current_user.clube_slug,
            ativa=True,
        ).count() > 0

    return False


def _pode_mexer_candidata(candidata):
    """
    admin_geral mexe em qualquer candidata.
    admin_clube só mexe em candidata do próprio clube.
    """
    if current_user.is_admin_geral():
        return True
    if current_user.is_admin_clube():
        return candidata.clube_slug == current_user.clube_slug
    return False


@admin_bp.route("/familias/<int:familia_id>/candidatas")
@login_required
@admin_required
def candidatas_listar(familia_id):
    """Lista candidatas de uma família."""

    familia = Usuario.query.get_or_404(familia_id)

    if familia.role != ROLE_FAMILIA:
        flash("Usuário não é uma família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    if not _pode_ver_familia(familia):
        flash("Você não tem permissão para ver essa família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    # Admin de clube só vê candidatas do próprio clube
    if current_user.is_admin_clube():
        candidatas = familia.candidatas.filter_by(
            clube_slug=current_user.clube_slug,
        ).order_by(Candidata.criada_em.desc()).all()
    else:
        candidatas = familia.candidatas.order_by(Candidata.criada_em.desc()).all()

    # Enriquece com dados do clube
    for c in candidatas:
        c.clube_info = get_clube_por_slug(c.clube_slug)

    return render_template(
        "admin/candidatas/listar.html",
        familia=familia,
        candidatas=candidatas,
    )


@admin_bp.route("/familias/<int:familia_id>/candidatas/nova", methods=["GET", "POST"])
@login_required
@admin_required
def candidatas_criar(familia_id):
    """Adiciona uma candidata à família."""

    familia = Usuario.query.get_or_404(familia_id)

    if familia.role != ROLE_FAMILIA:
        flash("Usuário não é uma família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    if not _pode_ver_familia(familia):
        flash("Você não tem permissão para adicionar candidatas nessa família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    form = CandidataForm()
    form.clube_slug.choices = _get_choices_clubes_permitidos()

    # Admin de clube: pré-seleciona seu clube (já é a única opção)
    if current_user.is_admin_clube():
        form.clube_slug.data = current_user.clube_slug

    if form.validate_on_submit():
        # Admin de clube só pode adicionar candidata no próprio clube
        if current_user.is_admin_clube() and form.clube_slug.data != current_user.clube_slug:
            flash("Você só pode adicionar candidatas no seu clube.", "erro")
            return render_template(
                "admin/candidatas/form.html",
                form=form,
                familia=familia,
                titulo_pagina="Adicionar Candidata",
                modo="criar",
            )

        nova = Candidata(
            familia_id=familia.id,
            clube_slug=form.clube_slug.data,
            nome=form.nome.data.strip(),
            idade=form.idade.data,
            observacoes=(form.observacoes.data or "").strip() or None,
            ativa=form.ativa.data,
        )

        db.session.add(nova)
        db.session.commit()

        clube_info = get_clube_por_slug(nova.clube_slug)
        flash(
            f'Candidata "{nova.nome}" adicionada ao Clube {clube_info["nome"]}!',
            "sucesso",
        )
        return redirect(url_for("admin.candidatas_listar", familia_id=familia.id))

    return render_template(
        "admin/candidatas/form.html",
        form=form,
        familia=familia,
        titulo_pagina="Adicionar Candidata",
        modo="criar",
    )


@admin_bp.route("/candidatas/<int:candidata_id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def candidatas_editar(candidata_id):
    """Edita uma candidata."""

    candidata = Candidata.query.get_or_404(candidata_id)

    if not _pode_mexer_candidata(candidata):
        flash("Você não tem permissão para editar essa candidata.", "erro")
        return redirect(url_for("admin.familias_listar"))

    familia = candidata.familia
    form = CandidataForm(obj=candidata)
    form.clube_slug.choices = _get_choices_clubes_permitidos()

    if form.validate_on_submit():
        # Admin de clube não pode mudar o clube da candidata para outro
        if current_user.is_admin_clube() and form.clube_slug.data != current_user.clube_slug:
            flash("Você não pode mover candidata para outro clube.", "erro")
            return render_template(
                "admin/candidatas/form.html",
                form=form,
                familia=familia,
                titulo_pagina=f"Editar: {candidata.nome}",
                modo="editar",
            )

        candidata.nome = form.nome.data.strip()
        candidata.idade = form.idade.data
        candidata.clube_slug = form.clube_slug.data
        candidata.observacoes = (form.observacoes.data or "").strip() or None
        candidata.ativa = form.ativa.data

        db.session.commit()

        flash(f'Candidata "{candidata.nome}" atualizada!', "sucesso")
        return redirect(url_for("admin.candidatas_listar", familia_id=familia.id))

    return render_template(
        "admin/candidatas/form.html",
        form=form,
        familia=familia,
        titulo_pagina=f"Editar: {candidata.nome}",
        modo="editar",
    )


@admin_bp.route("/candidatas/<int:candidata_id>/excluir", methods=["POST"])
@login_required
@admin_required
def candidatas_excluir(candidata_id):
    """Exclui uma candidata."""

    candidata = Candidata.query.get_or_404(candidata_id)

    if not _pode_mexer_candidata(candidata):
        flash("Você não tem permissão para excluir essa candidata.", "erro")
        return redirect(url_for("admin.familias_listar"))

    familia_id = candidata.familia_id
    nome = candidata.nome

    db.session.delete(candidata)
    db.session.commit()

    flash(f'Candidata "{nome}" excluída.', "sucesso")
    return redirect(url_for("admin.candidatas_listar", familia_id=familia_id))