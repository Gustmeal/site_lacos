"""
Formulário completo de Inscrição (Matrícula).

Coleta todos os dados necessários para efetivar a matrícula
de uma candidata em um clube da Associação Laços.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    SelectField,
    RadioField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional


class InscricaoForm(FlaskForm):
    """Formulário completo de matrícula."""

    # ==========================================
    # DADOS DA ASSOCIADA (CANDIDATA)
    # ==========================================

    email = StringField(
        "E-mail da associada",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
        render_kw={"placeholder": "email@exemplo.com"},
    )

    nome_associada = StringField(
        "Nome da associada",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=3, max=120),
        ],
        render_kw={"placeholder": "Nome completo"},
    )

    data_nascimento = DateField(
        "Data de nascimento",
        validators=[DataRequired(message="A data de nascimento é obrigatória.")],
    )

    cpf_associada = StringField(
        "CPF (caso possua)",
        validators=[Optional(), Length(max=20)],
        render_kw={"placeholder": "000.000.000-00 (opcional)"},
    )

    endereco = TextAreaField(
        "Endereço completo",
        validators=[
            DataRequired(message="O endereço é obrigatório."),
            Length(min=10),
        ],
        render_kw={
            "placeholder": "Rua, número, bairro, cidade, CEP",
            "rows": 2,
        },
    )

    # ==========================================
    # ESCOLARIDADE
    # ==========================================

    tipo_ensino = RadioField(
        "Ensino",
        validators=[DataRequired(message="Selecione o tipo de ensino.")],
        choices=[
            ("homeschooling", "Homeschooling"),
            ("escola", "Escola"),
        ],
    )

    nome_escola = StringField(
        "Caso frequente escola, qual?",
        validators=[Optional(), Length(max=200)],
        render_kw={"placeholder": "Nome da escola (se aplicável)"},
    )

    # ==========================================
    # DADOS DA MÃE
    # ==========================================

    nome_mae = StringField(
        "Nome da mãe",
        validators=[
            DataRequired(message="O nome da mãe é obrigatório."),
            Length(min=3, max=120),
        ],
    )

    data_nascimento_mae = DateField(
        "Data de nascimento da mãe",
        validators=[DataRequired(message="A data de nascimento é obrigatória.")],
    )

    profissao_mae = StringField(
        "Profissão da mãe",
        validators=[
            DataRequired(message="A profissão é obrigatória."),
            Length(max=120),
        ],
    )

    celular_mae = StringField(
        "Celular da mãe",
        validators=[
            DataRequired(message="O celular é obrigatório."),
            Length(min=10, max=32),
        ],
        render_kw={"placeholder": "(00) 00000-0000"},
    )

    email_mae = StringField(
        "E-mail da mãe",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
    )

    # ==========================================
    # DADOS DO PAI
    # ==========================================

    nome_pai = StringField(
        "Nome do pai",
        validators=[
            DataRequired(message="O nome do pai é obrigatório."),
            Length(min=3, max=120),
        ],
    )

    data_nascimento_pai = DateField(
        "Data de nascimento do pai",
        validators=[DataRequired(message="A data de nascimento é obrigatória.")],
    )

    profissao_pai = StringField(
        "Profissão do pai",
        validators=[
            DataRequired(message="A profissão é obrigatória."),
            Length(max=120),
        ],
    )

    celular_pai = StringField(
        "Celular do pai",
        validators=[
            DataRequired(message="O celular é obrigatório."),
            Length(min=10, max=32),
        ],
        render_kw={"placeholder": "(00) 00000-0000"},
    )

    email_pai = StringField(
        "E-mail do pai",
        validators=[
            DataRequired(message="O e-mail é obrigatório."),
            Email(message="Digite um e-mail válido."),
            Length(max=120),
        ],
    )

    # ==========================================
    # RESPONSÁVEL FINANCEIRO
    # ==========================================

    responsavel_financeiro = RadioField(
        "Responsável financeiro",
        validators=[DataRequired(message="Selecione o responsável financeiro.")],
        choices=[
            ("mae", "Mãe"),
            ("pai", "Pai"),
            ("outro", "Outro"),
        ],
    )

    cpf_responsavel_financeiro = TextAreaField(
        "CPF do responsável financeiro",
        validators=[
            DataRequired(message="Informe o CPF do responsável financeiro."),
            Length(min=11),
        ],
        render_kw={
            "placeholder": "Digite o CPF. Se responsável for OUTRO, informe também nome completo e e-mail.",
            "rows": 2,
        },
    )

    # ==========================================
    # CONTEXTO FAMILIAR
    # ==========================================

    como_conheceu = TextAreaField(
        "Como conheceu o clube?",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={"rows": 2},
    )

    esportes_hobbies = TextAreaField(
        "Esportes / Hobbies / Habilidades",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Música, dança, esportes, etc.",
            "rows": 3,
        },
    )

    situacao_pais = TextAreaField(
        "Situação dos pais / Associada mora com quem?",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={"rows": 2},
    )

    irmaos = TextAreaField(
        "Possui irmãos? Quantos? (nomes e idades)",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Ex: Sim, 2 irmãos - João (10) e Maria (7). Ou: Não tem irmãos.",
            "rows": 2,
        },
    )

    # ==========================================
    # PERSONALIDADE
    # ==========================================

    caracteristicas = TextAreaField(
        "Características mais marcantes",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Virtudes, pontos fracos, manias, gostos, humor, hábitos, jeito de ser, comportamento em casa e com amigos, etc.",
            "rows": 4,
        },
    )

    pontos_a_trabalhar = TextAreaField(
        "O que os pais gostariam que fosse trabalhado na associada?",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Virtudes a serem reforçadas e 'pontos de luta'.",
            "rows": 3,
        },
    )

    # ==========================================
    # SAÚDE
    # ==========================================

    alergias = TextAreaField(
        "Alergias",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Alimentares, medicamentosas, etc. Se não tiver, escreva 'Nenhuma'.",
            "rows": 2,
        },
    )

    medicamento_administrado = TextAreaField(
        "Em caso de dor, febre ou indisposição, que medicamento pode ser administrado?",
        validators=[DataRequired(message="Este campo é obrigatório.")],
        render_kw={
            "placeholder": "Ex: Paracetamol 500mg, Dipirona, etc.",
            "rows": 2,
        },
    )

    # ==========================================
    # AUTORIZAÇÕES
    # ==========================================

    interesse_doutrina = RadioField(
        "Têm interesse que a associada participe das aulas de doutrina da igreja católica?",
        validators=[DataRequired(message="Responda esta pergunta.")],
        choices=[
            ("sim", "Sim"),
            ("nao", "Não"),
        ],
    )

    ciente_regimento = RadioField(
        "Estão cientes das normas de convivência (Regimento Interno) do clube?",
        validators=[DataRequired(message="Responda esta pergunta.")],
        choices=[
            ("sim", "Sim"),
            ("nao", "Não"),
        ],
    )

    autoriza_imagem = RadioField(
        "Autorização de imagem, nome e voz (uso pelo clube em publicações, sites, vídeos, etc.)",
        validators=[DataRequired(message="Responda esta pergunta.")],
        choices=[
            ("sim", "Sim"),
            ("nao", "Não"),
        ],
    )

    # ==========================================
    # CLUBE (novo — família escolhe onde inscrever)
    # ==========================================

    clube_slug = SelectField(
        "Clube escolhido",
        validators=[DataRequired(message="Selecione o clube.")],
        choices=[],
    )

    submit = SubmitField("Enviar inscrição")