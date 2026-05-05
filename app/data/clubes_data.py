"""
Dados dos clubes da Associação Laços.

Por enquanto está em formato estático (lista Python).
Quando criarmos o modelo Clube no banco (Sprint 3), os dados
migrarão para lá e este arquivo será removido.

Dados extraídos do backlog oficial fornecido pela cliente.
"""

# Lista completa dos 10 clubes da Associação Laços
CLUBES = [
    # ===== CLUBES INFANTIS (7) =====
    {
        "slug": "caliandra",
        "nome": "Caliandra",
        "categoria": "infantil",
        "regiao": "Lago Sul",
        "logo": "img/clubes/caliandra.png",  # Ajustar se for .png
        "descricao_breve": "Um espaço acolhedor para o desenvolvimento integral de crianças no Lago Sul.",
        "ordem": 1,
    },
    {
        "slug": "camelia",
        "nome": "Camélia",
        "categoria": "infantil",
        "regiao": "Lago Norte",
        "logo": "img/clubes/camelia.png",
        "descricao_breve": "Formação, comunidade e crescimento para crianças do Lago Norte.",
        "ordem": 2,
    },
    {
        "slug": "flor-de-lis",
        "nome": "Flor de Lis",
        "categoria": "infantil",
        "regiao": "Guará",
        "logo": "img/clubes/flor-de-lis.png",
        "descricao_breve": "Atividades formativas e recreativas para crianças no Guará.",
        "ordem": 3,
    },
    {
        "slug": "girassol",
        "nome": "Girassol",
        "categoria": "infantil",
        "regiao": "Grande Colorado",
        "logo": "img/clubes/girassol.png",
        "descricao_breve": "Espaço de aprendizado e amizade no Grande Colorado.",
        "ordem": 4,
    },
    {
        "slug": "ipe-rosa",
        "nome": "Ipê Rosa",
        "categoria": "infantil",
        "regiao": "Águas Claras",
        "logo": "img/clubes/ipe-rosa.png",
        "descricao_breve": "Construindo laços de comunidade em Águas Claras.",
        "ordem": 5,
    },
    {
        "slug": "jacaranda",
        "nome": "Jacarandá",
        "categoria": "infantil",
        "regiao": "Taguatinga",
        "logo": "img/clubes/jacaranda.png",
        "descricao_breve": "Formação humana e cristã para crianças de Taguatinga.",
        "ordem": 6,
    },
    {
        "slug": "margarida",
        "nome": "Margarida",
        "categoria": "infantil",
        "regiao": "Lago Sul",
        "logo": "img/clubes/margarida.png",
        "descricao_breve": "Atividades enriquecedoras para crianças no Lago Sul.",
        "ordem": 7,
    },
    # ===== CLUBES JUVENIS (3) =====
    {
        "slug": "andorinha",
        "nome": "Andorinha",
        "categoria": "juvenil",
        "regiao": "Asa Sul",
        "logo": "img/clubes/andorinha.png",
        "descricao_breve": "Espaço de formação para jovens na Asa Sul.",
        "ordem": 8,
    },
    {
        "slug": "magnolia",
        "nome": "Magnólia",
        "categoria": "juvenil",
        "regiao": "Park Way",
        "logo": "img/clubes/magnolia.png",
        "descricao_breve": "Comunidade jovem com formação integral no Park Way.",
        "ordem": 9,
    },
    {
        "slug": "orquidea",
        "nome": "Orquídea",
        "categoria": "juvenil",
        "regiao": "Lago Sul",
        "logo": "img/clubes/orquidea.png",
        "descricao_breve": "Crescimento e formação para jovens no Lago Sul.",
        "ordem": 10,
    },
]


def get_clubes_destaque(quantidade=6):
    """
    Retorna clubes em destaque para a home (limitado).

    Args:
        quantidade: Número de clubes a retornar (padrão 6).

    Returns:
        Lista com os primeiros N clubes ordenados.
    """
    return sorted(CLUBES, key=lambda c: c["ordem"])[:quantidade]


def get_clubes_por_categoria(categoria=None):
    """
    Retorna clubes filtrados por categoria.

    Args:
        categoria: 'infantil', 'juvenil' ou None (retorna todos).

    Returns:
        Lista de clubes da categoria especificada.
    """
    if categoria is None:
        return sorted(CLUBES, key=lambda c: c["ordem"])
    return [c for c in CLUBES if c["categoria"] == categoria]


def get_clube_por_slug(slug):
    """
    Busca um clube pelo seu slug (URL amigável).

    Args:
        slug: Identificador único do clube (ex: 'caliandra').

    Returns:
        Dict do clube ou None se não encontrado.
    """
    for clube in CLUBES:
        if clube["slug"] == slug:
            return clube
    return None


def get_estatisticas():
    """
    Retorna estatísticas gerais dos clubes.

    Returns:
        Dict com totais por categoria.
    """
    return {
        "total": len(CLUBES),
        "infantis": len([c for c in CLUBES if c["categoria"] == "infantil"]),
        "juvenis": len([c for c in CLUBES if c["categoria"] == "juvenil"]),
        "regioes": len(set(c["regiao"] for c in CLUBES)),
    }