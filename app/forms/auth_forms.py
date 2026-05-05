"""
Formulários de autenticação do Site Laços.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """Formulário de login do painel admin."""

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "seu@email.com",
            "autocomplete": "email",
            "autofocus": True,
        },
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=1, max=200),
        ],
        render_kw={
            "placeholder": "Sua senha",
            "autocomplete": "current-password",
        },
    )

    lembrar_me = BooleanField("Lembrar-me neste dispositivo")

    submit = SubmitField("Entrar")