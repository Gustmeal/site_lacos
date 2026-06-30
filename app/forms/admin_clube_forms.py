"""
Formulários para gerenciamento de Admins de Clube.

Apenas admin_geral pode usar estes formulários.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class CriarAdminClubeForm(FlaskForm):
    """Formulário para criar um novo admin de clube."""

    nome = StringField(
        "Nome de exibição",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
        render_kw={
            "placeholder": "Ex: Clube Caliandra",
            "autofocus": True,
        },
    )

    email = StringField(
        "E-mail institucional do clube",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "caliandra@lacos.com.br",
            "autocomplete": "email",
        },
    )

    # Choices serão preenchidas dinamicamente na rota
    clube_slug = SelectField(
        "Clube vinculado",
        validators=[DataRequired(message="Selecione um clube.")],
        choices=[],
    )

    senha = PasswordField(
        "Senha (mínimo 8 caracteres)",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
        render_kw={"placeholder": "Mínimo 8 caracteres"},
    )

    senha_confirma = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message="Confirme a senha."),
            EqualTo("senha", message="As senhas não conferem."),
        ],
        render_kw={"placeholder": "Digite a senha novamente"},
    )

    ativo = BooleanField("Conta ativa", default=True)

    submit = SubmitField("Criar admin de clube")


class EditarAdminClubeForm(FlaskForm):
    """Formulário para editar um admin de clube (sem alterar senha)."""

    nome = StringField(
        "Nome de exibição",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
    )

    email = StringField(
        "E-mail institucional do clube",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
    )

    clube_slug = SelectField(
        "Clube vinculado",
        validators=[DataRequired(message="Selecione um clube.")],
        choices=[],
    )

    ativo = BooleanField("Conta ativa")

    submit = SubmitField("Salvar alterações")