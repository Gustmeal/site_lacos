"""Formulários WTForms da aplicação Site Laços."""

from app.forms.auth_forms import LoginForm
from app.forms.evento_forms import EventoForm
from app.forms.usuario_forms import (
    CriarUsuarioForm,
    EditarUsuarioForm,
    ResetarSenhaForm,
    AlterarMinhaSenhaForm,
)
from app.forms.intencao_forms import IntencaoClubeForm

__all__ = [
    "LoginForm",
    "EventoForm",
    "CriarUsuarioForm",
    "EditarUsuarioForm",
    "ResetarSenhaForm",
    "AlterarMinhaSenhaForm",
    "IntencaoClubeForm",
]