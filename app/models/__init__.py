"""Modelos da aplicação."""

from app.models.usuario import (
    Usuario,
    ROLE_ADMIN_GERAL,
    ROLE_ADMIN_CLUBE,
    ROLE_FAMILIA,
    ROLES_VALIDOS,
)
from app.models.evento import Evento
from app.models.intencao import IntencaoClube
from app.models.candidata import Candidata

__all__ = [
    "Usuario",
    "Evento",
    "IntencaoClube",
    "Candidata",
    "ROLE_ADMIN_GERAL",
    "ROLE_ADMIN_CLUBE",
    "ROLE_FAMILIA",
    "ROLES_VALIDOS",
]