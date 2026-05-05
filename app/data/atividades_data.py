"""
Dados das atividades oferecidas pela Associação Laços.

As 10 atividades vêm do backlog oficial (US10).
Cada atividade tem associada uma cor da paleta da marca
e um ícone SVG (referenciado por nome no template).

Quando criarmos o modelo Atividade no banco (futuro), os dados
migrarão para lá. Este arquivo será removido posteriormente.
"""

# Lista das 10 atividades oferecidas pelos clubes Laços
ATIVIDADES = [
    {
        "slug": "artesanato",
        "nome": "Artesanato e Arte Floral",
        "descricao": "Trabalhos manuais que despertam a sensibilidade estética, a paciência e o cuidado com os detalhes através de técnicas variadas.",
        "icone": "scissors",  # Ícone SVG - referenciado no template
        "cor": "vermelho",  # Cor da paleta institucional
        "ordem": 1,
    },
    {
        "slug": "comemoracoes",
        "nome": "Comemorações",
        "descricao": "Momentos de celebração que fortalecem laços de amizade e marcam datas especiais com alegria e propósito.",
        "icone": "cake",
        "cor": "amarelo",
        "ordem": 2,
    },
    {
        "slug": "corte-costura",
        "nome": "Corte e Costura",
        "descricao": "Aprendizado de técnicas tradicionais que estimulam a autonomia, criatividade e o senso prático.",
        "icone": "needle",
        "cor": "azul",
        "ordem": 3,
    },
    {
        "slug": "culinaria",
        "nome": "Culinária",
        "descricao": "Da preparação ao prato finalizado, descobrindo sabores, técnicas e o prazer de cozinhar para quem se ama.",
        "icone": "utensils",
        "cor": "vermelho",
        "ordem": 4,
    },
    {
        "slug": "educacao",
        "nome": "Educação",
        "descricao": "Atividades formativas que estimulam o aprendizado, a curiosidade e o desenvolvimento intelectual de cada associada.",
        "icone": "book",
        "cor": "marinho",
        "ordem": 5,
    },
    {
        "slug": "esporte",
        "nome": "Esporte",
        "descricao": "Atividades físicas que promovem saúde, disciplina, espírito de equipe e o desenvolvimento integral do corpo.",
        "icone": "trophy",
        "cor": "verde",
        "ordem": 6,
    },
    {
        "slug": "formacoes",
        "nome": "Formações",
        "descricao": "Encontros formativos com temas de virtudes, valores humanos e cristãos, fundamentais para o crescimento pessoal.",
        "icone": "academic",
        "cor": "marinho",
        "ordem": 7,
    },
    {
        "slug": "moda",
        "nome": "Moda",
        "descricao": "Estilo, elegância e expressão pessoal — descobrindo como a moda pode ser uma forma de cuidado e arte.",
        "icone": "sparkles",
        "cor": "amarelo",
        "ordem": 8,
    },
    {
        "slug": "oficinas",
        "nome": "Oficinas",
        "descricao": "Espaços práticos de descoberta, onde habilidades novas são apresentadas em ambiente colaborativo e criativo.",
        "icone": "hammer",
        "cor": "azul",
        "ordem": 9,
    },
    {
        "slug": "passeios",
        "nome": "Passeios",
        "descricao": "Saídas culturais, recreativas e formativas que ampliam horizontes e fortalecem os laços de amizade entre as associadas.",
        "icone": "map",
        "cor": "verde",
        "ordem": 10,
    },
]


def get_todas_atividades():
    """
    Retorna todas as atividades ordenadas.

    Returns:
        Lista completa de atividades.
    """
    return sorted(ATIVIDADES, key=lambda a: a["ordem"])


def get_atividades_destaque(quantidade=4):
    """
    Retorna atividades em destaque (para usar na home).

    Args:
        quantidade: Número de atividades a retornar (padrão 4).

    Returns:
        Lista com as primeiras N atividades.
    """
    return sorted(ATIVIDADES, key=lambda a: a["ordem"])[:quantidade]


def get_atividade_por_slug(slug):
    """
    Busca uma atividade pelo seu slug.

    Args:
        slug: Identificador único (ex: 'culinaria').

    Returns:
        Dict da atividade ou None se não encontrada.
    """
    for atividade in ATIVIDADES:
        if atividade["slug"] == slug:
            return atividade
    return None


def get_total_atividades():
    """Retorna o número total de atividades."""
    return len(ATIVIDADES)