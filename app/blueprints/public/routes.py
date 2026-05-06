"""
Rotas públicas do Site Laços.

Todas as páginas acessíveis sem login ficam aqui.
"""

from datetime import datetime
from flask import render_template, abort
from app.blueprints.public import public_bp
from app.data.clubes_data import (
    get_clubes_destaque,
    get_clubes_por_categoria,
    get_estatisticas,
)
from app.data.atividades_data import (
    get_todas_atividades,
    get_atividades_destaque,
    get_total_atividades,
)
from app.models.evento import Evento


@public_bp.route("/")
def home():
    """Página inicial do site."""
    clubes_destaque = get_clubes_destaque(quantidade=6)
    estatisticas = get_estatisticas()
    atividades_destaque = get_atividades_destaque(quantidade=4)

    # Pega os 3 próximos eventos publicados (futuros)
    eventos_proximos = (
        Evento.query
        .filter(Evento.publicado == True)
        .filter(Evento.data_evento >= datetime.utcnow().date())
        .order_by(Evento.data_evento.asc())
        .limit(3)
        .all()
    )

    return render_template(
        "pages/home.html",
        clubes_destaque=clubes_destaque,
        estatisticas=estatisticas,
        atividades_destaque=atividades_destaque,
        total_atividades=get_total_atividades(),
        eventos_proximos=eventos_proximos,
    )


@public_bp.route("/quem-somos")
def quem_somos():
    """Página Quem Somos (institucional)."""
    return render_template("pages/quem_somos.html")


@public_bp.route("/atividades")
def atividades():
    """Página com as 10 atividades oferecidas."""
    todas_atividades = get_todas_atividades()
    return render_template(
        "pages/atividades.html",
        atividades=todas_atividades,
        total=get_total_atividades(),
    )


@public_bp.route("/clubes")
def clubes_lista():
    """Página de listagem dos clubes (categorias)."""
    clubes_infantis = get_clubes_por_categoria("infantil")
    clubes_juvenis = get_clubes_por_categoria("juvenil")
    estatisticas = get_estatisticas()
    return render_template(
        "pages/clubes_lista.html",
        clubes_infantis=clubes_infantis,
        clubes_juvenis=clubes_juvenis,
        estatisticas=estatisticas,
    )


@public_bp.route("/eventos")
def eventos_lista():
    """Página com a lista de eventos publicados."""

    # Pega o filtro da URL (futuros, passados, todos)
    from flask import request
    filtro = request.args.get("filtro", "futuros")

    # Base: só eventos publicados
    query = Evento.query.filter(Evento.publicado == True)

    if filtro == "futuros":
        query = query.filter(Evento.data_evento >= datetime.utcnow().date())
        eventos = query.order_by(Evento.data_evento.asc()).all()
    elif filtro == "passados":
        query = query.filter(Evento.data_evento < datetime.utcnow().date())
        eventos = query.order_by(Evento.data_evento.desc()).all()
    else:  # todos
        eventos = query.order_by(Evento.data_evento.desc()).all()

    # Estatísticas para mostrar nos filtros
    publicados = Evento.query.filter(Evento.publicado == True)
    estatisticas = {
        "total": publicados.count(),
        "futuros": publicados.filter(Evento.data_evento >= datetime.utcnow().date()).count(),
        "passados": publicados.filter(Evento.data_evento < datetime.utcnow().date()).count(),
    }

    return render_template(
        "pages/eventos_lista.html",
        eventos=eventos,
        estatisticas=estatisticas,
        filtro_atual=filtro,
    )


@public_bp.route("/eventos/<slug>")
def evento_detalhe(slug):
    """Página de detalhes de um evento específico."""

    evento = Evento.query.filter_by(slug=slug, publicado=True).first()

    # Se não encontrou ou não está publicado, retorna 404
    if evento is None:
        abort(404)

    # Pega outros eventos próximos para mostrar na lateral
    outros_eventos = (
        Evento.query
        .filter(Evento.publicado == True)
        .filter(Evento.id != evento.id)
        .filter(Evento.data_evento >= datetime.utcnow().date())
        .order_by(Evento.data_evento.asc())
        .limit(3)
        .all()
    )

    return render_template(
        "pages/evento_detalhe.html",
        evento=evento,
        outros_eventos=outros_eventos,
    )