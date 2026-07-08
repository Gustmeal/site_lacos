"""
Formulários para gerenciamento de Famílias e Candidatas pelo admin.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class CriarFamiliaForm(FlaskForm):
    """Formulário para criar uma nova conta de família (só dados do responsável)."""

    nome = StringField(
        "Nome do responsável",
        validators=[
            DataRequired(message="O nome do responsável é obrigatório."),
            Length(min=3, max=120),
        ],
        render_kw={
            "placeholder": "Ex: Maria da Silva",
            "autofocus": True,
        },
    )

    email = StringField(
        "E-mail do responsável",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "responsavel@email.com",
        },
    )

    telefone = StringField(
        "Telefone (com DDD)",
        validators=[
            DataRequired(message="O telefone é obrigatório."),
            Length(min=10, max=32),
        ],
        render_kw={
            "placeholder": "(61) 99999-9999",
        },
    )

    endereco = StringField(
        "Endereço (bairro/cidade)",
        validators=[
            Optional(),
            Length(max=255),
        ],
        render_kw={
            "placeholder": "Ex: Lago Sul, Brasília/DF",
        },
    )

    senha = PasswordField(
        "Senha inicial (mínimo 8 caracteres)",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="Mínimo 8 caracteres."),
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

    submit = SubmitField("Cadastrar família")


class EditarFamiliaForm(FlaskForm):
    """Formulário para editar uma família (sem alterar senha)."""

    nome = StringField(
        "Nome do responsável",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
    )

    email = StringField(
        "E-mail do responsável",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
    )

    telefone = StringField(
        "Telefone (com DDD)",
        validators=[
            DataRequired(message="O telefone é obrigatório."),
            Length(min=10, max=32),
        ],
    )

    endereco = StringField(
        "Endereço (bairro/cidade)",
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    ativo = BooleanField("Conta ativa")

    submit = SubmitField("Salvar alterações")


class CandidataForm(FlaskForm):
    """Formulário para adicionar/editar uma candidata (filha)."""

    nome = StringField(
        "Nome da candidata",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=2, max=120),
        ],
        render_kw={
            "placeholder": "Nome completo da menina",
            "autofocus": True,
        },
    )

    idade = IntegerField(
        "Idade",
        validators=[
            Optional(),
            NumberRange(min=4, max=18, message="Idade entre 4 e 18 anos."),
        ],
        render_kw={
            "placeholder": "Ex: 7",
            "min": "4",
            "max": "18",
        },
    )

    clube_slug = SelectField(
        "Clube",
        validators=[DataRequired(message="Selecione o clube.")],
        choices=[],
    )

    observacoes = TextAreaField(
        "Observações (uso interno)",
        validators=[Optional(), Length(max=500)],
        render_kw={
            "placeholder": "Notas internas sobre a candidata (opcional)",
            "rows": "3",
        },
    )

    ativa = BooleanField("Candidata ativa", default=True)

    submit = SubmitField("Salvar candidata")