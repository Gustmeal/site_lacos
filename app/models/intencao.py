"""
Modelo de intenção de inscrição em clube.

Esse modelo guarda as "intenções" enviadas pelo formulário público
nas páginas individuais dos clubes. Não é uma inscrição formal,
apenas demonstração de interesse.
"""

from datetime import datetime
from app.extensions import db


class IntencaoClube(db.Model):
    """Intenção de inscrição em um clube específico."""

    __tablename__ = "intencoes_clube"

    id = db.Column(db.Integer, primary_key=True)

    # Dados do clube (slug em vez de FK, pois clubes são hardcoded)
    clube_slug = db.Column(db.String(64), nullable=False, index=True)
    clube_nome = db.Column(db.String(120), nullable=False)

    # Dados do responsável
    nome_responsavel = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(32), nullable=False)

    # Dados da candidata
    nome_candidata = db.Column(db.String(120), nullable=False)
    idade_candidata = db.Column(db.Integer, nullable=True)

    # Mensagem opcional
    mensagem = db.Column(db.Text, nullable=True)

    # Controle
    enviada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lida = db.Column(db.Boolean, default=False, nullable=False)
    respondida = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<IntencaoClube {self.nome_candidata} - {self.clube_nome}>"