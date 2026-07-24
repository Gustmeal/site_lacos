"""
Modelo de Inscrição (Matrícula) — dados completos preenchidos pela família.

Cada Candidata pode ter uma Inscrição vinculada.
A família preenche todos os campos ao formalizar a matrícula.
"""

from datetime import datetime
from app.extensions import db


class Inscricao(db.Model):
    """Ficha completa de inscrição de uma candidata em um clube."""

    __tablename__ = "inscricoes"

    id = db.Column(db.Integer, primary_key=True)

    # === RELACIONAMENTOS ===
    candidata_id = db.Column(
        db.Integer,
        db.ForeignKey("candidatas.id"),
        nullable=False,
        unique=True,  # Uma candidata só tem UMA inscrição
        index=True,
    )
    candidata = db.relationship(
        "Candidata",
        backref=db.backref("inscricao", uselist=False, cascade="all, delete-orphan"),
    )

    familia_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    familia = db.relationship("Usuario", backref="inscricoes_criadas")

    # Clube escolhido no formulário (pode ser diferente do slug da candidata)
    clube_slug = db.Column(db.String(64), nullable=False, index=True)

    # === DADOS DA ASSOCIADA (CANDIDATA) ===
    email = db.Column(db.String(120), nullable=False)
    nome_associada = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    cpf_associada = db.Column(db.String(20), nullable=True)  # Opcional
    endereco = db.Column(db.Text, nullable=False)

    # === ESCOLARIDADE ===
    tipo_ensino = db.Column(db.String(20), nullable=False)  # 'homeschooling' ou 'escola'
    nome_escola = db.Column(db.String(200), nullable=True)  # Só se tipo_ensino = 'escola'

    # === DADOS DA MÃE ===
    nome_mae = db.Column(db.String(120), nullable=False)
    data_nascimento_mae = db.Column(db.Date, nullable=False)
    profissao_mae = db.Column(db.String(120), nullable=False)
    celular_mae = db.Column(db.String(32), nullable=False)
    email_mae = db.Column(db.String(120), nullable=False)

    # === DADOS DO PAI ===
    nome_pai = db.Column(db.String(120), nullable=False)
    data_nascimento_pai = db.Column(db.Date, nullable=False)
    profissao_pai = db.Column(db.String(120), nullable=False)
    celular_pai = db.Column(db.String(32), nullable=False)
    email_pai = db.Column(db.String(120), nullable=False)

    # === RESPONSÁVEL FINANCEIRO ===
    responsavel_financeiro = db.Column(db.String(20), nullable=False)  # 'mae', 'pai', 'outro'
    cpf_responsavel_financeiro = db.Column(db.Text, nullable=False)
    # Se for 'outro', instrução do form pede colocar CPF + nome + email nesse campo

    # === CONTEXTO FAMILIAR ===
    como_conheceu = db.Column(db.Text, nullable=False)
    esportes_hobbies = db.Column(db.Text, nullable=False)
    situacao_pais = db.Column(db.Text, nullable=False)  # Mora com quem
    irmaos = db.Column(db.Text, nullable=False)  # Descrição de irmãos

    # === PERSONALIDADE ===
    caracteristicas = db.Column(db.Text, nullable=False)
    pontos_a_trabalhar = db.Column(db.Text, nullable=False)

    # === SAÚDE ===
    alergias = db.Column(db.Text, nullable=False)
    medicamento_administrado = db.Column(db.Text, nullable=False)

    # === AUTORIZAÇÕES (booleanos) ===
    interesse_doutrina = db.Column(db.Boolean, nullable=False)
    ciente_regimento = db.Column(db.Boolean, nullable=False)
    autoriza_imagem = db.Column(db.Boolean, nullable=False)

    # === CONTROLE ===
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def get_clube(self):
        """Retorna o dicionário do clube escolhido."""
        from app.data.clubes_data import get_clube_por_slug
        return get_clube_por_slug(self.clube_slug)

    def __repr__(self):
        return f"<Inscricao {self.nome_associada} - {self.clube_slug}>"