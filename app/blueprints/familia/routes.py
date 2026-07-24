"""
Rotas da área restrita das famílias.

Todas as rotas requerem role 'familia'.
"""

from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required

from app.blueprints.familia import familia_bp
from app.extensions import db
from app.forms import AlterarMinhaSenhaForm, InscricaoForm
from app.models import Candidata, Inscricao
from app.data.clubes_data import get_todos_clubes, get_clube_por_slug
from app.utils.decorators import familia_required


@familia_bp.route("/painel")
@login_required
@familia_required
def painel():
    """Painel principal da família com todas as candidatas."""

    candidatas = current_user.candidatas.filter_by(ativa=True).all()

    # Enriquece com dados do clube e status da inscrição
    for c in candidatas:
        c.clube_info = c.get_clube()
        c.tem_inscricao = c.inscricao is not None

    return render_template(
        "familia/painel.html",
        candidatas=candidatas,
    )


@familia_bp.route("/minha-conta", methods=["GET", "POST"])
@login_required
@familia_required
def minha_conta():
    """Página de alteração de senha da família."""

    form = AlterarMinhaSenhaForm()

    if form.validate_on_submit():
        if not current_user.verificar_senha(form.senha_atual.data):
            flash("Senha atual incorreta.", "erro")
            return render_template("familia/minha_conta.html", form=form)

        current_user.set_senha(form.senha_nova.data)
        db.session.commit()

        flash("Senha alterada com sucesso!", "sucesso")
        return redirect(url_for("familia.painel"))

    return render_template("familia/minha_conta.html", form=form)


# ==========================================
# INSCRIÇÕES (MATRÍCULAS)
# ==========================================


def _candidata_da_familia(candidata_id):
    """
    Busca uma candidata garantindo que pertence à família logada.
    Retorna 404 se não pertencer.
    """
    candidata = Candidata.query.get_or_404(candidata_id)

    if candidata.familia_id != current_user.id:
        abort(404)  # 404 em vez de 403 para não vazar existência

    return candidata


@familia_bp.route("/inscricao/nova/<int:candidata_id>", methods=["GET", "POST"])
@login_required
@familia_required
def inscricao_criar(candidata_id):
    """Cria uma nova inscrição para uma candidata."""

    candidata = _candidata_da_familia(candidata_id)

    # Se já tem inscrição, redireciona para visualização
    if candidata.inscricao:
        flash("Esta candidata já possui inscrição preenchida.", "info")
        return redirect(url_for("familia.inscricao_ver", candidata_id=candidata.id))

    form = InscricaoForm()

    # Popula choices do dropdown de clubes
    clubes = get_todos_clubes()
    form.clube_slug.choices = [
        (c["slug"], f"{c['nome']} — {c['regiao']}") for c in clubes
    ]

    # Pré-preenche alguns campos com dados que já temos
    if not form.is_submitted():
        form.nome_associada.data = candidata.nome
        form.clube_slug.data = candidata.clube_slug

    if form.validate_on_submit():
        # Validação condicional: se tipo_ensino='escola', nome_escola é obrigatório
        if form.tipo_ensino.data == "escola" and not form.nome_escola.data:
            flash("Se a candidata frequenta escola, informe o nome da escola.", "erro")
            return render_template(
                "familia/inscricao_form.html",
                form=form,
                candidata=candidata,
                modo="criar",
            )

        # Cria a inscrição
        inscricao = Inscricao(
            candidata_id=candidata.id,
            familia_id=current_user.id,
            clube_slug=form.clube_slug.data,

            # Dados da associada
            email=form.email.data.lower().strip(),
            nome_associada=form.nome_associada.data.strip(),
            data_nascimento=form.data_nascimento.data,
            cpf_associada=(form.cpf_associada.data or "").strip() or None,
            endereco=form.endereco.data.strip(),

            # Escolaridade
            tipo_ensino=form.tipo_ensino.data,
            nome_escola=(form.nome_escola.data or "").strip() or None,

            # Dados da mãe
            nome_mae=form.nome_mae.data.strip(),
            data_nascimento_mae=form.data_nascimento_mae.data,
            profissao_mae=form.profissao_mae.data.strip(),
            celular_mae=form.celular_mae.data.strip(),
            email_mae=form.email_mae.data.lower().strip(),

            # Dados do pai
            nome_pai=form.nome_pai.data.strip(),
            data_nascimento_pai=form.data_nascimento_pai.data,
            profissao_pai=form.profissao_pai.data.strip(),
            celular_pai=form.celular_pai.data.strip(),
            email_pai=form.email_pai.data.lower().strip(),

            # Responsável financeiro
            responsavel_financeiro=form.responsavel_financeiro.data,
            cpf_responsavel_financeiro=form.cpf_responsavel_financeiro.data.strip(),

            # Contexto familiar
            como_conheceu=form.como_conheceu.data.strip(),
            esportes_hobbies=form.esportes_hobbies.data.strip(),
            situacao_pais=form.situacao_pais.data.strip(),
            irmaos=form.irmaos.data.strip(),

            # Personalidade
            caracteristicas=form.caracteristicas.data.strip(),
            pontos_a_trabalhar=form.pontos_a_trabalhar.data.strip(),

            # Saúde
            alergias=form.alergias.data.strip(),
            medicamento_administrado=form.medicamento_administrado.data.strip(),

            # Autorizações
            interesse_doutrina=(form.interesse_doutrina.data == "sim"),
            ciente_regimento=(form.ciente_regimento.data == "sim"),
            autoriza_imagem=(form.autoriza_imagem.data == "sim"),
        )

        db.session.add(inscricao)

        # Atualiza o clube_slug da candidata caso a família tenha mudado
        if candidata.clube_slug != form.clube_slug.data:
            candidata.clube_slug = form.clube_slug.data

        db.session.commit()

        flash(
            f"Inscrição de {candidata.nome} enviada com sucesso!",
            "sucesso",
        )
        return redirect(url_for("familia.inscricao_ver", candidata_id=candidata.id))

    return render_template(
        "familia/inscricao_form.html",
        form=form,
        candidata=candidata,
        modo="criar",
    )


@familia_bp.route("/inscricao/<int:candidata_id>")
@login_required
@familia_required
def inscricao_ver(candidata_id):
    """Visualiza os dados da inscrição de uma candidata."""

    candidata = _candidata_da_familia(candidata_id)

    if not candidata.inscricao:
        flash("Esta candidata ainda não possui inscrição preenchida.", "info")
        return redirect(url_for("familia.inscricao_criar", candidata_id=candidata.id))

    inscricao = candidata.inscricao
    clube_info = inscricao.get_clube()

    return render_template(
        "familia/inscricao_ver.html",
        candidata=candidata,
        inscricao=inscricao,
        clube_info=clube_info,
    )


@familia_bp.route("/inscricao/<int:candidata_id>/editar", methods=["GET", "POST"])
@login_required
@familia_required
def inscricao_editar(candidata_id):
    """Edita uma inscrição já preenchida."""

    candidata = _candidata_da_familia(candidata_id)

    if not candidata.inscricao:
        flash("Esta candidata ainda não possui inscrição para editar.", "info")
        return redirect(url_for("familia.inscricao_criar", candidata_id=candidata.id))

    inscricao = candidata.inscricao
    form = InscricaoForm(obj=inscricao)

    # Popula choices do dropdown de clubes
    clubes = get_todos_clubes()
    form.clube_slug.choices = [
        (c["slug"], f"{c['nome']} — {c['regiao']}") for c in clubes
    ]

    # No GET, converte os booleanos para radio values ('sim'/'nao')
    if not form.is_submitted():
        form.interesse_doutrina.data = "sim" if inscricao.interesse_doutrina else "nao"
        form.ciente_regimento.data = "sim" if inscricao.ciente_regimento else "nao"
        form.autoriza_imagem.data = "sim" if inscricao.autoriza_imagem else "nao"

    if form.validate_on_submit():
        # Validação condicional
        if form.tipo_ensino.data == "escola" and not form.nome_escola.data:
            flash("Se a candidata frequenta escola, informe o nome da escola.", "erro")
            return render_template(
                "familia/inscricao_form.html",
                form=form,
                candidata=candidata,
                modo="editar",
            )

        # Atualiza os campos
        inscricao.clube_slug = form.clube_slug.data
        inscricao.email = form.email.data.lower().strip()
        inscricao.nome_associada = form.nome_associada.data.strip()
        inscricao.data_nascimento = form.data_nascimento.data
        inscricao.cpf_associada = (form.cpf_associada.data or "").strip() or None
        inscricao.endereco = form.endereco.data.strip()

        inscricao.tipo_ensino = form.tipo_ensino.data
        inscricao.nome_escola = (form.nome_escola.data or "").strip() or None

        inscricao.nome_mae = form.nome_mae.data.strip()
        inscricao.data_nascimento_mae = form.data_nascimento_mae.data
        inscricao.profissao_mae = form.profissao_mae.data.strip()
        inscricao.celular_mae = form.celular_mae.data.strip()
        inscricao.email_mae = form.email_mae.data.lower().strip()

        inscricao.nome_pai = form.nome_pai.data.strip()
        inscricao.data_nascimento_pai = form.data_nascimento_pai.data
        inscricao.profissao_pai = form.profissao_pai.data.strip()
        inscricao.celular_pai = form.celular_pai.data.strip()
        inscricao.email_pai = form.email_pai.data.lower().strip()

        inscricao.responsavel_financeiro = form.responsavel_financeiro.data
        inscricao.cpf_responsavel_financeiro = form.cpf_responsavel_financeiro.data.strip()

        inscricao.como_conheceu = form.como_conheceu.data.strip()
        inscricao.esportes_hobbies = form.esportes_hobbies.data.strip()
        inscricao.situacao_pais = form.situacao_pais.data.strip()
        inscricao.irmaos = form.irmaos.data.strip()

        inscricao.caracteristicas = form.caracteristicas.data.strip()
        inscricao.pontos_a_trabalhar = form.pontos_a_trabalhar.data.strip()

        inscricao.alergias = form.alergias.data.strip()
        inscricao.medicamento_administrado = form.medicamento_administrado.data.strip()

        inscricao.interesse_doutrina = (form.interesse_doutrina.data == "sim")
        inscricao.ciente_regimento = (form.ciente_regimento.data == "sim")
        inscricao.autoriza_imagem = (form.autoriza_imagem.data == "sim")

        # Atualiza clube da candidata se mudou
        if candidata.clube_slug != form.clube_slug.data:
            candidata.clube_slug = form.clube_slug.data

        db.session.commit()

        flash("Inscrição atualizada com sucesso!", "sucesso")
        return redirect(url_for("familia.inscricao_ver", candidata_id=candidata.id))

    return render_template(
        "familia/inscricao_form.html",
        form=form,
        candidata=candidata,
        modo="editar",
    )