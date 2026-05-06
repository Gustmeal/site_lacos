"""
Rotas administrativas para gerenciamento de eventos.

Todas as rotas aqui exigem autenticação (login).
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.blueprints.admin import admin_bp
from app.forms import EventoForm
from app.models.evento import Evento
from app.extensions import db


@admin_bp.route("/eventos")
@login_required
def eventos_listar():
    """Lista todos os eventos cadastrados."""

    # Filtros opcionais
    filtro = request.args.get("filtro", "todos")

    query = Evento.query

    if filtro == "futuros":
        query = query.filter(Evento.data_evento >= datetime.utcnow().date())
    elif filtro == "passados":
        query = query.filter(Evento.data_evento < datetime.utcnow().date())
    elif filtro == "publicados":
        query = query.filter(Evento.publicado == True)
    elif filtro == "rascunhos":
        query = query.filter(Evento.publicado == False)

    # Ordena: futuros primeiro, depois passados (mais recentes no topo)
    eventos = query.order_by(Evento.data_evento.desc()).all()

    # Estatísticas para mostrar nos filtros
    estatisticas = {
        "total": Evento.query.count(),
        "futuros": Evento.query.filter(Evento.data_evento >= datetime.utcnow().date()).count(),
        "passados": Evento.query.filter(Evento.data_evento < datetime.utcnow().date()).count(),
        "publicados": Evento.query.filter(Evento.publicado == True).count(),
        "rascunhos": Evento.query.filter(Evento.publicado == False).count(),
    }

    return render_template(
        "admin/eventos/listar.html",
        eventos=eventos,
        estatisticas=estatisticas,
        filtro_atual=filtro,
    )


@admin_bp.route("/eventos/novo", methods=["GET", "POST"])
@login_required
def eventos_criar():
    """Cria um novo evento."""

    form = EventoForm()

    if form.validate_on_submit():
        novo_evento = Evento(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            data_evento=form.data_evento.data,
            horario=form.horario.data,
            local=form.local.data or None,
            publicado=form.publicado.data,
            autor_id=current_user.id,
        )
        novo_evento.gerar_slug()

        db.session.add(novo_evento)
        db.session.commit()

        flash(f'Evento "{novo_evento.titulo}" criado com sucesso!', "sucesso")
        return redirect(url_for("admin.eventos_listar"))

    return render_template(
        "admin/eventos/form.html",
        form=form,
        titulo_pagina="Criar Novo Evento",
        modo="criar",
    )


@admin_bp.route("/eventos/<int:evento_id>/editar", methods=["GET", "POST"])
@login_required
def eventos_editar(evento_id):
    """Edita um evento existente."""

    evento = Evento.query.get_or_404(evento_id)
    form = EventoForm(obj=evento)

    if form.validate_on_submit():
        # Verifica se o título mudou (precisa regenerar slug)
        titulo_mudou = evento.titulo != form.titulo.data

        evento.titulo = form.titulo.data
        evento.descricao = form.descricao.data
        evento.data_evento = form.data_evento.data
        evento.horario = form.horario.data
        evento.local = form.local.data or None
        evento.publicado = form.publicado.data

        if titulo_mudou:
            evento.gerar_slug()

        db.session.commit()

        flash(f'Evento "{evento.titulo}" atualizado com sucesso!', "sucesso")
        return redirect(url_for("admin.eventos_listar"))

    return render_template(
        "admin/eventos/form.html",
        form=form,
        titulo_pagina=f"Editar: {evento.titulo}",
        modo="editar",
        evento=evento,
    )


@admin_bp.route("/eventos/<int:evento_id>/excluir", methods=["POST"])
@login_required
def eventos_excluir(evento_id):
    """Exclui um evento."""

    evento = Evento.query.get_or_404(evento_id)
    titulo = evento.titulo

    db.session.delete(evento)
    db.session.commit()

    flash(f'Evento "{titulo}" excluído com sucesso.', "sucesso")
    return redirect(url_for("admin.eventos_listar"))


@admin_bp.route("/eventos/<int:evento_id>/toggle-publicado", methods=["POST"])
@login_required
def eventos_toggle_publicado(evento_id):
    """Alterna o status de publicação do evento."""

    evento = Evento.query.get_or_404(evento_id)
    evento.publicado = not evento.publicado

    db.session.commit()

    status = "publicado" if evento.publicado else "despublicado"
    flash(f'Evento "{evento.titulo}" {status}.', "sucesso")
    return redirect(url_for("admin.eventos_listar"))