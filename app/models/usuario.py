"""
Modelo Usuário do Site Laços.

Representa os usuários administrativos que podem
publicar e gerenciar eventos.

Senhas são SEMPRE armazenadas como hash bcrypt — nunca em texto puro.
"""

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


class Usuario(UserMixin, db.Model):
    """Usuário administrativo do sistema."""

    __tablename__ = "usuarios"

    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(200), nullable=False)

    # Permissões e status
    role = db.Column(db.String(20), default="admin", nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Auditoria
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=True)

    # Relacionamento: 1 usuário pode criar muitos eventos
    eventos = db.relationship("Evento", backref="autor", lazy=True)

    def set_senha(self, senha):
        """
        Define a senha do usuário, gerando o hash bcrypt automaticamente.

        Args:
            senha: Senha em texto puro (será descartada após hash).
        """
        self.senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

    def verificar_senha(self, senha):
        """
        Verifica se uma senha bate com o hash armazenado.

        Args:
            senha: Senha em texto puro para verificar.

        Returns:
            True se a senha estiver correta, False caso contrário.
        """
        return bcrypt.check_password_hash(self.senha_hash, senha)

    @property
    def is_active(self):
        """Flask-Login usa para verificar se a conta está ativa."""
        return self.ativo

    def __repr__(self):
        return f"<Usuario {self.email}>"