"""
Formulários para gerenciamento de usuários administrativos.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class CriarUsuarioForm(FlaskForm):
    """Formulário para criar um novo usuário admin."""

    nome = StringField(
        "Nome completo",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120, message="O nome deve ter entre 3 e 120 caracteres."),
        ],
        render_kw={
            "placeholder": "Ex: Maria Silva",
            "autocomplete": "name",
            "autofocus": True,
        },
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={
            "placeholder": "maria@lacos.com.br",
            "autocomplete": "email",
        },
    )

    role = SelectField(
        "Tipo de usuário",
        choices=[
            ("admin", "Administrador (acesso completo)"),
        ],
        default="admin",
        validators=[DataRequired()],
    )

    senha = PasswordField(
        "Senha (mínimo 8 caracteres)",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
        render_kw={
            "placeholder": "Mínimo 8 caracteres",
            "autocomplete": "new-password",
        },
    )

    senha_confirma = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message="Confirme a senha."),
            EqualTo("senha", message="As senhas não conferem."),
        ],
        render_kw={
            "placeholder": "Digite a senha novamente",
            "autocomplete": "new-password",
        },
    )

    ativo = BooleanField(
        "Conta ativa",
        default=True,
    )

    submit = SubmitField("Criar usuário")


class EditarUsuarioForm(FlaskForm):
    """Formulário para editar dados de um usuário (sem alterar senha)."""

    nome = StringField(
        "Nome completo",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
    )

    role = SelectField(
        "Tipo de usuário",
        choices=[
            ("admin", "Administrador (acesso completo)"),
        ],
        validators=[DataRequired()],
    )

    ativo = BooleanField("Conta ativa")

    submit = SubmitField("Salvar alterações")


class ResetarSenhaForm(FlaskForm):
    """Formulário para resetar a senha de um usuário."""

    senha = PasswordField(
        "Nova senha (mínimo 8 caracteres)",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
        render_kw={
            "placeholder": "Mínimo 8 caracteres",
            "autocomplete": "new-password",
            "autofocus": True,
        },
    )

    senha_confirma = PasswordField(
        "Confirmar nova senha",
        validators=[
            DataRequired(message="Confirme a senha."),
            EqualTo("senha", message="As senhas não conferem."),
        ],
        render_kw={
            "placeholder": "Digite a senha novamente",
            "autocomplete": "new-password",
        },
    )

    submit = SubmitField("Resetar senha")


class AlterarMinhaSenhaForm(FlaskForm):
    """Formulário para o usuário alterar a própria senha."""

    senha_atual = PasswordField(
        "Senha atual",
        validators=[
            DataRequired(message="A senha atual é obrigatória."),
        ],
        render_kw={
            "placeholder": "Sua senha atual",
            "autocomplete": "current-password",
            "autofocus": True,
        },
    )

    senha_nova = PasswordField(
        "Nova senha (mínimo 8 caracteres)",
        validators=[
            DataRequired(message="A nova senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
        render_kw={
            "placeholder": "Mínimo 8 caracteres",
            "autocomplete": "new-password",
        },
    )

    senha_confirma = PasswordField(
        "Confirmar nova senha",
        validators=[
            DataRequired(message="Confirme a senha."),
            EqualTo("senha_nova", message="As senhas não conferem."),
        ],
        render_kw={
            "placeholder": "Digite a nova senha novamente",
            "autocomplete": "new-password",
        },
    )

    submit = SubmitField("Alterar senha")