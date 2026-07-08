"""
Rotas para gerenciamento de Famílias pelo admin.

- admin_geral: gerencia famílias de QUALQUER clube
- admin_clube: gerencia famílias APENAS do próprio clube
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.forms import (
    CriarFamiliaForm,
    EditarFamiliaForm,
    ResetarSenhaForm,
)
from app.models import Usuario, ROLE_FAMILIA
from app.data.clubes_data import get_todos_clubes, get_clube_por_slug
from app.utils.decorators import admin_required
from app.models import Usuario, Candidata, ROLE_FAMILIA


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


def _familia_permitida(familia):
    """
    Verifica se o usuário atual pode gerenciar essa família.
    - admin_geral: qualquer
    - admin_clube: se tem candidata no clube dele OU se família ainda não tem candidatas
    """
    if current_user.is_admin_geral():
        return True

    if current_user.is_admin_clube():
        total_candidatas = familia.candidatas.count()
        if total_candidatas == 0:
            return True

        return familia.candidatas.filter_by(
            clube_slug=current_user.clube_slug,
            ativa=True,
        ).count() > 0

    return False

@admin_bp.route("/familias")
@login_required
@admin_required
def familias_listar():
    """Lista famílias filtradas por permissão + filtro opcional de clube."""

    # Filtro de clube (só admin geral tem essa opção)
    filtro_clube = request.args.get("clube", "").strip()

    if current_user.is_admin_geral():
        query = Usuario.query.filter_by(role=ROLE_FAMILIA)

        # Aplicar filtro de clube se selecionado
        if filtro_clube == "sem_candidatas":
            # Famílias sem NENHUMA candidata cadastrada
            familia_ids_com_candidata = (
                db.session.query(Candidata.familia_id)
                .distinct()
                .subquery()
            )
            query = query.filter(~Usuario.id.in_(familia_ids_com_candidata))
        elif filtro_clube:
            # Famílias que têm candidata no clube específico
            familia_ids = (
                db.session.query(Candidata.familia_id)
                .filter_by(clube_slug=filtro_clube, ativa=True)
                .distinct()
                .subquery()
            )
            query = query.filter(Usuario.id.in_(familia_ids))

        familias = query.order_by(Usuario.ativo.desc(), Usuario.nome.asc()).all()


    elif current_user.is_admin_clube():

        # Admin de clube: vê famílias com candidata no clube dele

        # + famílias sem NENHUMA candidata ainda (recém-criadas)

        familia_ids_com_candidata_no_clube = (

            db.session.query(Candidata.familia_id)

            .filter_by(clube_slug=current_user.clube_slug, ativa=True)

            .distinct()

            .subquery()

        )

        familia_ids_com_candidatas = (

            db.session.query(Candidata.familia_id)

            .distinct()

            .subquery()

        )

        familias = (

            Usuario.query

            .filter(

                Usuario.role == ROLE_FAMILIA,

                db.or_(

                    Usuario.id.in_(familia_ids_com_candidata_no_clube),

                    ~Usuario.id.in_(familia_ids_com_candidatas),

                ),

            )

            .order_by(Usuario.ativo.desc(), Usuario.nome.asc())

            .all()

        )
    else:
        familias = []

    # Enriquece com dados das candidatas (filtradas por permissão)
    for f in familias:
        if current_user.is_admin_clube():
            f.candidatas_visiveis = f.candidatas.filter_by(
                clube_slug=current_user.clube_slug,
                ativa=True,
            ).all()
        else:
            f.candidatas_visiveis = f.candidatas.filter_by(ativa=True).all()

    # Lista de clubes para o dropdown de filtro (só admin geral usa)
    clubes_disponiveis = get_todos_clubes() if current_user.is_admin_geral() else []

    # Info do clube filtrado (para o header)
    clube_filtrado_info = None
    if filtro_clube and filtro_clube != "sem_candidatas":
        clube_filtrado_info = get_clube_por_slug(filtro_clube)

    estatisticas = {
        "total": len(familias),
        "ativos": sum(1 for f in familias if f.ativo),
        "inativos": sum(1 for f in familias if not f.ativo),
    }

    return render_template(
        "admin/familias/listar.html",
        familias=familias,
        estatisticas=estatisticas,
        clubes_disponiveis=clubes_disponiveis,
        filtro_clube=filtro_clube,
        clube_filtrado_info=clube_filtrado_info,
    )

@admin_bp.route("/familias/nova", methods=["GET", "POST"])
@login_required
@admin_required
def familias_criar():
    """
    Cria uma nova família (só dados do responsável).
    Após criar, redireciona para adicionar candidatas.
    """

    form = CriarFamiliaForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        # E-mail duplicado?
        if Usuario.query.filter_by(email=email).first():
            flash(f"Já existe um usuário com o e-mail {email}.", "erro")
            return render_template(
                "admin/familias/form.html",
                form=form,
                titulo_pagina="Cadastrar Família",
                modo="criar",
            )

        nova = Usuario(
            nome=form.nome.data.strip(),
            email=email,
            role=ROLE_FAMILIA,
            telefone=form.telefone.data.strip(),
            endereco=(form.endereco.data or "").strip() or None,
            ativo=form.ativo.data,
        )
        nova.set_senha(form.senha.data)

        db.session.add(nova)
        db.session.commit()

        flash(
            f'Família "{nova.nome}" cadastrada! Agora adicione as candidatas.',
            "sucesso",
        )
        return redirect(url_for("admin.candidatas_listar", familia_id=nova.id))

    return render_template(
        "admin/familias/form.html",
        form=form,
        titulo_pagina="Cadastrar Família",
        modo="criar",
    )


@admin_bp.route("/familias/<int:familia_id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def familias_editar(familia_id):
    """Edita dados do responsável (sem candidatas)."""

    familia = Usuario.query.get_or_404(familia_id)

    if familia.role != ROLE_FAMILIA:
        flash("Usuário não é uma família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    if not _familia_permitida(familia):
        flash("Você não tem permissão para editar essa família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    form = EditarFamiliaForm(obj=familia)

    if form.validate_on_submit():
        novo_email = form.email.data.lower().strip()

        if novo_email != familia.email:
            existente = Usuario.query.filter_by(email=novo_email).first()
            if existente and existente.id != familia.id:
                flash(f"Já existe outro usuário com o e-mail {novo_email}.", "erro")
                return render_template(
                    "admin/familias/form.html",
                    form=form,
                    titulo_pagina=f"Editar: {familia.nome}",
                    modo="editar",
                    familia=familia,
                )

        familia.nome = form.nome.data.strip()
        familia.email = novo_email
        familia.telefone = form.telefone.data.strip()
        familia.endereco = (form.endereco.data or "").strip() or None
        familia.ativo = form.ativo.data

        db.session.commit()

        flash(f'Família "{familia.nome}" atualizada!', "sucesso")
        return redirect(url_for("admin.familias_listar"))

    return render_template(
        "admin/familias/form.html",
        form=form,
        titulo_pagina=f"Editar: {familia.nome}",
        modo="editar",
        familia=familia,
    )


@admin_bp.route("/familias/<int:familia_id>/resetar-senha", methods=["GET", "POST"])
@login_required
@admin_required
def familias_resetar_senha(familia_id):
    """Reseta a senha de uma família."""

    familia = Usuario.query.get_or_404(familia_id)

    if familia.role != ROLE_FAMILIA:
        flash("Usuário não é uma família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    if not _familia_permitida(familia):
        flash("Você não tem permissão para resetar essa senha.", "erro")
        return redirect(url_for("admin.familias_listar"))

    form = ResetarSenhaForm()

    if form.validate_on_submit():
        familia.set_senha(form.senha.data)
        db.session.commit()

        flash(
            f'Senha de "{familia.nome}" resetada. '
            f"Comunique a nova senha ao responsável de forma segura.",
            "sucesso",
        )
        return redirect(url_for("admin.familias_listar"))

    return render_template(
        "admin/familias/resetar_senha.html",
        form=form,
        familia=familia,
    )


@admin_bp.route("/familias/<int:familia_id>/toggle-ativo", methods=["POST"])
@login_required
@admin_required
def familias_toggle_ativo(familia_id):
    """Ativa/desativa uma família."""

    familia = Usuario.query.get_or_404(familia_id)

    if familia.role != ROLE_FAMILIA:
        flash("Usuário não é uma família.", "erro")
        return redirect(url_for("admin.familias_listar"))

    if not _familia_permitida(familia):
        flash("Você não tem permissão.", "erro")
        return redirect(url_for("admin.familias_listar"))

    familia.ativo = not familia.ativo
    db.session.commit()

    status = "ativada" if familia.ativo else "desativada"
    flash(f'Família "{familia.nome}" {status}.', "sucesso")
    return redirect(url_for("admin.familias_listar"))