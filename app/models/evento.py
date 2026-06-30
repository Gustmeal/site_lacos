"""
Modelo Evento do Site Laços.

Representa os eventos publicados pela equipe administrativa.
"""

from datetime import datetime
from slugify import slugify
from app.extensions import db


class Evento(db.Model):
    """Evento publicado pela administração."""

    __tablename__ = "eventos"

    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    descricao = db.Column(db.Text, nullable=False)

    # Data e hora
    data_evento = db.Column(db.Date, nullable=False, index=True)
    horario = db.Column(db.Time, nullable=True)

    # Local (opcional)
    local = db.Column(db.String(200), nullable=True)

    # Status
    publicado = db.Column(db.Boolean, default=True, nullable=False)

    # Imagem (caminho relativo, opcional)
    imagem = db.Column(db.String(255), nullable=True)

    # Relacionamento
    # Adicionar dentro da classe Evento, junto com os outros campos:
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True,
    )

    autor = db.relationship("Usuario", backref="eventos_criados")

    # Auditoria
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def gerar_slug(self):
        """Gera um slug único baseado no título."""
        base_slug = slugify(self.titulo)
        slug = base_slug
        contador = 1

        # Garante unicidade do slug
        while Evento.query.filter_by(slug=slug).filter(Evento.id != self.id).first():
            slug = f"{base_slug}-{contador}"
            contador += 1

        self.slug = slug

    @property
    def is_futuro(self):
        """Retorna True se o evento é no futuro ou hoje."""
        return self.data_evento >= datetime.utcnow().date()

    @property
    def is_passado(self):
        """Retorna True se o evento já passou."""
        return self.data_evento < datetime.utcnow().date()

    def __repr__(self):
        return f"<Evento {self.titulo}>"