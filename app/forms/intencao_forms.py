"""Formulário público de intenção de inscrição em clube."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class IntencaoClubeForm(FlaskForm):
    """Formulário para demonstrar interesse em um clube."""

    # Campos ocultos (preenchidos pelo template)
    clube_slug = HiddenField(validators=[DataRequired()])
    clube_nome = HiddenField(validators=[DataRequired()])

    nome_responsavel = StringField(
        "Seu nome completo (responsável)",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
        render_kw={
            "placeholder": "Ex: Maria da Silva",
            "autocomplete": "name",
        },
    )

    email = StringField(
        "Seu e-mail",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "seu@email.com",
            "autocomplete": "email",
        },
    )

    telefone = StringField(
        "Telefone com DDD",
        validators=[
            DataRequired(message="O telefone é obrigatório."),
            Length(min=10, max=32),
        ],
        render_kw={
            "placeholder": "(61) 99999-9999",
            "autocomplete": "tel",
        },
    )

    nome_candidata = StringField(
        "Nome da candidata",
        validators=[
            DataRequired(message="O nome da candidata é obrigatório."),
            Length(min=2, max=120),
        ],
        render_kw={
            "placeholder": "Nome completo da menina",
        },
    )

    idade_candidata = IntegerField(
        "Idade da candidata",
        validators=[
            Optional(),
            NumberRange(min=4, max=18, message="Idade deve estar entre 4 e 18 anos."),
        ],
        render_kw={
            "placeholder": "Ex: 7",
            "min": "4",
            "max": "18",
        },
    )

    mensagem = TextAreaField(
        "Mensagem (opcional)",
        validators=[
            Optional(),
            Length(max=1000),
        ],
        render_kw={
            "placeholder": "Conte-nos um pouco mais ou faça uma pergunta...",
            "rows": "4",
        },
    )

    submit = SubmitField("Enviar intenção de inscrição")