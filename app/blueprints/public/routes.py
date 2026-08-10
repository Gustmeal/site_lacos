"""
Rotas públicas do Site Laços.

Todas as páginas acessíveis sem login ficam aqui.
"""

from datetime import datetime
from flask import render_template, abort, flash, redirect, url_for
from app.blueprints.public import public_bp
from app.data.clubes_data import (
    get_clubes_destaque,
    get_clubes_por_categoria,
    get_estatisticas,
    get_clube_por_slug,
    get_outros_clubes,
    get_fotos_clube,
    get_foto_capa,
    get_imagem_capa,
)
from app.forms import IntencaoClubeForm
from app.models.intencao import IntencaoClube
from app.extensions import db
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


@public_bp.route("/clubes/<slug>", methods=["GET", "POST"])
def clube_detalhe(slug):
    """Página individual de um clube."""

    clube = get_clube_por_slug(slug)
    if not clube:
        abort(404)

    # Carrega capa (foto OU logo) e galeria
    imagem_capa = get_imagem_capa(slug)
    fotos = get_fotos_clube(slug)
    # Se a capa é uma foto, a galeria é o resto. Se é logo, mostra todas as fotos.
    if imagem_capa and imagem_capa["tipo"] == "foto":
        fotos_galeria = fotos[1:] if len(fotos) > 1 else []
    else:
        fotos_galeria = fotos  # Logo de capa, fotos são extras na galeria

    # Outros clubes da mesma categoria
    outros_clubes = get_outros_clubes(slug, mesma_categoria=True, quantidade=3)

    # Formulário de intenção
    form = IntencaoClubeForm()
    form.clube_slug.data = clube["slug"]
    form.clube_nome.data = clube["nome"]

    if form.validate_on_submit():
        intencao = IntencaoClube(
            clube_slug=form.clube_slug.data,
            clube_nome=form.clube_nome.data,
            nome_responsavel=form.nome_responsavel.data.strip(),
            email=form.email.data.lower().strip(),
            telefone=form.telefone.data.strip(),
            nome_candidata=form.nome_candidata.data.strip(),
            idade_candidata=form.idade_candidata.data,
            mensagem=form.mensagem.data.strip() if form.mensagem.data else None,
        )

        db.session.add(intencao)
        db.session.commit()

        flash(
            f'Sua intenção de inscrição para o Clube {clube["nome"]} foi enviada com sucesso! '
            f'A equipe da Laços entrará em contato em breve.',
            "sucesso",
        )
        return redirect(url_for("public.clube_detalhe", slug=slug) + "#intencao-enviada")

    return render_template(
        "pages/clube_detalhe.html",
        clube=clube,
        imagem_capa=imagem_capa,
        fotos_galeria=fotos_galeria,
        outros_clubes=outros_clubes,
        form=form,
    )

@public_bp.route("/termos-de-uso")
def termos_de_uso():
    return render_template("pages/termos_de_uso.html")


@public_bp.route("/politica-de-privacidade")
def politica_privacidade():
    return render_template("pages/politica_privacidade.html")

@public_bp.route("/contato")
def contato():
    return render_template("pages/contato.html")