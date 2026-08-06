"""
Rotas admin para visualizar inscrições (matrículas) das candidatas.

- admin_geral: vê todas as inscrições
- admin_clube: vê apenas inscrições cujo clube_slug bate com o seu

Admin não edita inscrições (só a família edita a própria).
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.models import Inscricao, Candidata, Usuario, ROLE_FAMILIA
from app.data.clubes_data import get_todos_clubes, get_clube_por_slug
from app.utils.decorators import admin_required



def _pode_ver_inscricao(inscricao):
    """
    admin_geral vê qualquer inscrição.
    admin_clube só vê inscrições do seu clube.
    """
    if current_user.is_admin_geral():
        return True
    if current_user.is_admin_clube():
        return inscricao.clube_slug == current_user.clube_slug
    return False


@admin_bp.route("/inscricoes")
@login_required
@admin_required
def inscricoes_listar():
    """Lista inscrições filtradas por permissão + filtro opcional de clube."""

    filtro_clube = request.args.get("clube", "").strip()

    if current_user.is_admin_geral():
        query = Inscricao.query

        # Filtro opcional por clube (só admin geral)
        if filtro_clube:
            query = query.filter_by(clube_slug=filtro_clube)

    elif current_user.is_admin_clube():
        # Admin de clube: sempre filtra pelo próprio clube
        query = Inscricao.query.filter_by(clube_slug=current_user.clube_slug)
    else:
        query = Inscricao.query.filter(False)  # nenhuma

    inscricoes = query.order_by(Inscricao.criada_em.desc()).all()

    # Enriquece com dados do clube
    for i in inscricoes:
        i.clube_info = get_clube_por_slug(i.clube_slug)

    # Lista de clubes para o dropdown (só admin geral)
    clubes_disponiveis = get_todos_clubes() if current_user.is_admin_geral() else []

    clube_filtrado_info = None
    if filtro_clube:
        clube_filtrado_info = get_clube_por_slug(filtro_clube)

    estatisticas = {
        "total": len(inscricoes),
    }

    return render_template(
        "admin/inscricoes/listar.html",
        inscricoes=inscricoes,
        estatisticas=estatisticas,
        clubes_disponiveis=clubes_disponiveis,
        filtro_clube=filtro_clube,
        clube_filtrado_info=clube_filtrado_info,
    )


@admin_bp.route("/inscricoes/<int:inscricao_id>")
@login_required
@admin_required
def inscricoes_ver(inscricao_id):
    """Visualiza os dados completos de uma inscrição."""

    inscricao = Inscricao.query.get_or_404(inscricao_id)

    if not _pode_ver_inscricao(inscricao):
        flash("Você não tem permissão para ver essa inscrição.", "erro")
        return redirect(url_for("admin.inscricoes_listar"))

    candidata = inscricao.candidata
    familia = inscricao.familia
    clube_info = inscricao.get_clube()

    return render_template(
        "admin/inscricoes/ver.html",
        inscricao=inscricao,
        candidata=candidata,
        familia=familia,
        clube_info=clube_info,
    )