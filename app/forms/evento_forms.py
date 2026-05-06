"""
Formulários relacionados a eventos do Site Laços.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class EventoForm(FlaskForm):
    """Formulário para criar e editar eventos."""

    titulo = StringField(
        "Título do evento",
        validators=[
            DataRequired(message="O título é obrigatório."),
            Length(min=3, max=200, message="O título deve ter entre 3 e 200 caracteres."),
        ],
        render_kw={
            "placeholder": "Ex: Encontro de Famílias 2026",
            "autofocus": True,
        },
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[
            DataRequired(message="A descrição é obrigatória."),
            Length(min=10, max=5000, message="A descrição deve ter entre 10 e 5000 caracteres."),
        ],
        render_kw={
            "placeholder": "Descreva os detalhes do evento, programação, público-alvo...",
            "rows": 6,
        },
    )

    data_evento = DateField(
        "Data",
        validators=[DataRequired(message="A data é obrigatória.")],
    )

    horario = TimeField(
        "Horário",
        validators=[Optional()],
    )

    local = StringField(
        "Local (opcional)",
        validators=[
            Optional(),
            Length(max=200, message="O local deve ter no máximo 200 caracteres."),
        ],
        render_kw={
            "placeholder": "Ex: Clube Caliandra - Lago Sul",
        },
    )

    publicado = BooleanField(
        "Publicar no site (visível para visitantes)",
        default=True,
    )

    submit = SubmitField("Salvar evento")