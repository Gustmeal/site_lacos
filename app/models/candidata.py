"""
Modelo de Candidata — as filhas cadastradas por famílias.

Cada família (Usuario com role='familia') pode ter várias candidatas,
cada uma vinculada a um clube específico.
"""

from datetime import datetime
from app.extensions import db


class Candidata(db.Model):
    """Uma candidata (filha) cadastrada por uma família."""

    __tablename__ = "candidatas"

    id = db.Column(db.Integer, primary_key=True)

    # Vínculo com a família (Usuario com role='familia')
    familia_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    familia = db.relationship(
        "Usuario",
        backref=db.backref("candidatas", lazy="dynamic", cascade="all, delete-orphan"),
    )

    # Vínculo com clube (slug hardcoded)
    clube_slug = db.Column(db.String(64), nullable=False, index=True)

    # Dados da candidata
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=True)

    # Observações opcionais (uso interno do admin)
    observacoes = db.Column(db.Text, nullable=True)

    # Controle
    ativa = db.Column(db.Boolean, default=True, nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_clube(self):
        """Retorna o dicionário do clube vinculado."""
        from app.data.clubes_data import get_clube_por_slug
        return get_clube_por_slug(self.clube_slug)

    def __repr__(self):
        return f"<Candidata {self.nome} - {self.clube_slug}>"