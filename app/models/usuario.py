"""
Modelo de Usuário do sistema.

Tipos de usuário (campo role):
- 'admin_geral': controle total do sistema (equipe central da Laços)
- 'admin_clube': gestão limitada a um clube específico (vinculado pelo campo clube_slug)
- 'familia': RESERVADO para fase futura (pais/responsáveis das associadas)
"""

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


# Constantes para roles (evita strings soltas no código)
ROLE_ADMIN_GERAL = "admin_geral"
ROLE_ADMIN_CLUBE = "admin_clube"
ROLE_FAMILIA = "familia"  # Reservado para futuro

ROLES_VALIDOS = [ROLE_ADMIN_GERAL, ROLE_ADMIN_CLUBE, ROLE_FAMILIA]


class Usuario(db.Model, UserMixin):
    """Modelo de usuário do sistema."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)

    # Tipo de usuário
    role = db.Column(db.String(32), nullable=False, default=ROLE_ADMIN_GERAL)

    # Vínculo a um clube específico (preenchido apenas para admin_clube e familia)
    clube_slug = db.Column(db.String(64), nullable=True, index=True)

    ativo = db.Column(db.Boolean, default=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=True)

    def set_senha(self, senha_plana):
        """Define a senha do usuário, gerando um hash bcrypt seguro."""
        self.senha_hash = bcrypt.generate_password_hash(senha_plana).decode("utf-8")

    def verificar_senha(self, senha_plana):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.check_password_hash(self.senha_hash, senha_plana)

    # === MÉTODOS DE PERMISSÃO (úteis em templates e views) ===

    def is_admin_geral(self):
        """Verifica se é admin geral (acesso total)."""
        return self.role == ROLE_ADMIN_GERAL

    def is_admin_clube(self):
        """Verifica se é admin de um clube específico."""
        return self.role == ROLE_ADMIN_CLUBE

    def is_familia(self):
        """Verifica se é uma família (uso futuro)."""
        return self.role == ROLE_FAMILIA

    def pode_gerenciar_clube(self, slug_clube):
        """Verifica se o usuário pode gerenciar o clube especificado."""
        if self.is_admin_geral():
            return True
        if self.is_admin_clube() and self.clube_slug == slug_clube:
            return True
        return False

    def get_clube(self):
        """Retorna o dicionário do clube vinculado (se houver)."""
        if not self.clube_slug:
            return None
        from app.data.clubes_data import get_clube_por_slug
        return get_clube_por_slug(self.clube_slug)

    def __repr__(self):
        return f"<Usuario {self.email} ({self.role})>"