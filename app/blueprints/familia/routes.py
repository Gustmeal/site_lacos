"""
Rotas da área restrita das famílias.

Todas as rotas requerem role 'familia'.
"""

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.blueprints.familia import familia_bp
from app.extensions import db
from app.forms import AlterarMinhaSenhaForm
from app.utils.decorators import familia_required

# Link único do formulário de matrícula (Google Forms)
FORMULARIO_MATRICULA_URL = "https://forms.gle/RQTrZUvm8LwDsXjq9"


@familia_bp.route("/painel")
@login_required
@familia_required
def painel():
    """Painel principal da família com todas as candidatas."""

    from app.models import Candidata

    candidatas = current_user.candidatas.filter_by(ativa=True).all()

    # Enriquece com dados do clube
    for c in candidatas:
        c.clube_info = c.get_clube()

    return render_template(
        "familia/painel.html",
        candidatas=candidatas,
        formulario_matricula_url=FORMULARIO_MATRICULA_URL,
    )


@familia_bp.route("/minha-conta", methods=["GET", "POST"])
@login_required
@familia_required
def minha_conta():
    """Página de alteração de senha da família."""

    form = AlterarMinhaSenhaForm()

    if form.validate_on_submit():
        # Verifica senha atual
        if not current_user.verificar_senha(form.senha_atual.data):
            flash("Senha atual incorreta.", "erro")
            return render_template("familia/minha_conta.html", form=form)

        current_user.set_senha(form.senha_nova.data)
        db.session.commit()

        flash("Senha alterada com sucesso!", "sucesso")
        return redirect(url_for("familia.painel"))

    return render_template("familia/minha_conta.html", form=form)