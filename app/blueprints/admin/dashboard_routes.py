"""
Rotas do dashboard administrativo.

Dashboard adaptativo por role:
- admin_geral: estatísticas globais + contadores por clube + atalhos
- admin_clube: estatísticas do próprio clube + atalhos
"""

from datetime import datetime, date
from flask import render_template
from flask_login import login_required, current_user

from app.blueprints.admin import admin_bp
from app.extensions import db
from app.models import (
    Usuario,
    Evento,
    Candidata,
    Inscricao,
    ROLE_FAMILIA,
    ROLE_ADMIN_CLUBE,
)
from app.data.clubes_data import (
    get_todos_clubes,
    get_clube_por_slug,
    get_estatisticas as get_estatisticas_clubes,
)
from app.utils.decorators import admin_required


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    """Dashboard com números reais e ações rápidas."""

    hoje = datetime.utcnow()

    if current_user.is_admin_geral():
        estatisticas = _get_stats_admin_geral()
        proximos_eventos = _get_proximos_eventos(limit=3)
        inscricoes_por_clube = _get_inscricoes_por_clube()
        clube_info = None
    else:
        # admin_clube
        estatisticas = _get_stats_admin_clube(current_user.clube_slug)
        proximos_eventos = _get_proximos_eventos_do_clube(current_user.clube_slug, limit=3)
        inscricoes_por_clube = None  # admin de clube não vê visão global
        clube_info = get_clube_por_slug(current_user.clube_slug)

    return render_template(
        "admin/dashboard.html",
        estatisticas=estatisticas,
        proximos_eventos=proximos_eventos,
        inscricoes_por_clube=inscricoes_por_clube,
        clube_info=clube_info,
        hoje=hoje,
    )


def _get_stats_admin_geral():
    """Estatísticas para admin geral (visão global)."""

    hoje_date = date.today()

    total_familias = Usuario.query.filter_by(role=ROLE_FAMILIA, ativo=True).count()
    total_candidatas = Candidata.query.filter_by(ativa=True).count()
    total_inscricoes = Inscricao.query.count()
    total_eventos_futuros = Evento.query.filter(
        Evento.data_evento >= hoje_date,
        Evento.publicado == True,
    ).count()
    total_admins_clube = Usuario.query.filter_by(role=ROLE_ADMIN_CLUBE, ativo=True).count()
    stats_clubes = get_estatisticas_clubes()
    total_clubes = stats_clubes.get("total_clubes", 0)

    return {
        "familias": total_familias,
        "candidatas": total_candidatas,
        "inscricoes": total_inscricoes,
        "eventos_proximos": total_eventos_futuros,
        "admins_clube": total_admins_clube,
        "total_clubes": total_clubes,
    }


def _get_stats_admin_clube(clube_slug):
    """Estatísticas para admin de clube (visão do próprio clube)."""

    hoje_date = date.today()

    # Famílias que têm candidata no clube dele
    familia_ids = (
        db.session.query(Candidata.familia_id)
        .filter_by(clube_slug=clube_slug, ativa=True)
        .distinct()
        .subquery()
    )
    total_familias_do_clube = (
        Usuario.query
        .filter(Usuario.role == ROLE_FAMILIA, Usuario.id.in_(familia_ids))
        .count()
    )

    # Candidatas do clube
    total_candidatas_do_clube = Candidata.query.filter_by(
        clube_slug=clube_slug,
        ativa=True,
    ).count()

    # Inscrições do clube
    total_inscricoes_do_clube = Inscricao.query.filter_by(clube_slug=clube_slug).count()

    # Eventos futuros criados por esse admin
    total_eventos_criados = Evento.query.filter(
        Evento.autor_id == current_user.id,
        Evento.data_evento >= hoje_date,
        Evento.publicado == True,
    ).count()

    return {
        "familias": total_familias_do_clube,
        "candidatas": total_candidatas_do_clube,
        "inscricoes": total_inscricoes_do_clube,
        "eventos_proximos": total_eventos_criados,
    }


def _get_inscricoes_por_clube():
    """
    Retorna uma lista de dicionários com contagem de inscrições por clube.
    Ordenado por total decrescente.
    """
    # Query agregada: agrupa por clube_slug e conta
    resultados = (
        db.session.query(
            Inscricao.clube_slug,
            db.func.count(Inscricao.id).label("total"),
        )
        .group_by(Inscricao.clube_slug)
        .all()
    )

    # Converte para dicionário { slug: total }
    contagens = {slug: total for slug, total in resultados}

    # Monta lista com TODOS os clubes (mesmo os com 0 inscrições)
    clubes = get_todos_clubes()
    lista = []
    for clube in clubes:
        lista.append({
            "slug": clube["slug"],
            "nome": clube["nome"],
            "regiao": clube["regiao"],
            "total": contagens.get(clube["slug"], 0),
        })

    # Ordena por total decrescente
    lista.sort(key=lambda x: x["total"], reverse=True)

    return lista


def _get_proximos_eventos(limit=3):
    """Retorna os próximos eventos publicados (para admin geral)."""
    hoje_date = date.today()
    return (
        Evento.query
        .filter(
            Evento.data_evento >= hoje_date,
            Evento.publicado == True,
        )
        .order_by(Evento.data_evento.asc())
        .limit(limit)
        .all()
    )


def _get_proximos_eventos_do_clube(clube_slug, limit=3):
    """Retorna próximos eventos criados pelo admin do clube."""
    hoje_date = date.today()
    return (
        Evento.query
        .filter(
            Evento.autor_id == current_user.id,
            Evento.data_evento >= hoje_date,
            Evento.publicado == True,
        )
        .order_by(Evento.data_evento.asc())
        .limit(limit)
        .all()
    )