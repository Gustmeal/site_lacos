"""
Dados dos 10 clubes da Associação Laços.

Cada clube tem informações institucionais, equipe, fotos e textos
específicos. O conteúdo "Virtudes" e "Temas Semestrais" é genérico
para clubes infantis (compartilhado em componente).
"""

import os
from flask import current_app


CLUBES = [
    # ===================== CLUBES INFANTIS (7) =====================
    {
        "slug": "caliandra",
        "nome": "Caliandra",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Lago Sul",
        "regiao_completa": "Lago Sul — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-vermelho",
        "fundado_em": 2006,
        "idades": "5 a 10 anos",
        "total_associadas": 40,
        "funcionamento": None,
        "descricao_curta": "O primeiro clube de Brasília, hoje um dos maiores do Brasil.",
        "descricao": (
            "O Clube Caliandra, localizado no bairro Lago Sul, foi o primeiro de Brasília, "
            "mas recebeu este nome em 2006. Tornou-se um dos maiores clube do Brasil, "
            "com um total de 40 associadas, de 5 a 10 anos."
        ),
        "diretora": "Fernanda Godinho",
        "vice_diretora": "Valessa Tokarski",
        "secretaria": "Rosana Macedo",
        "monitora": "Rafaela Teixeira",
        "atividades_oferecidas": [
            "Clube de leitura",
            "Aula de doutrina",
            "Oficinas de culinária",
            "Bordado",
            "Jardinagem",
            "Música",
            "Artesanato",
            "Moda e comportamento",
            "Contação de história",
            "Formação das virtudes",
            "Formação para os pais",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "camelia",
        "nome": "Camélia",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Lago Norte",
        "regiao_completa": "Lago Norte — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-azul",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": 30,
        "funcionamento": "Sábado, das 9h às 12h",
        "descricao_curta": "Clube familiar do Lago Norte com forte ênfase na formação integral.",
        "descricao": (
            "O Clube Familiar Camélia, localizado no Lago Norte, é um espaço de formação "
            "para meninas de 5 a 10 anos. Conta com 30 associadas e oferece atividades "
            "que abrangem desde aulas práticas até momentos de formação para os pais."
        ),
        "diretora": "Priscila Paço",
        "vice_diretora": "Maria Donária Soares",
        "secretaria": "Luciana Vieira",
        "monitora": None,
        "atividades_oferecidas": [
            "Clube de leitura",
            "Aula de doutrina",
            "Oficinas de culinária",
            "Bordado",
            "Jardinagem",
            "Música",
            "Artesanato",
            "Moda e comportamento",
            "Contação de história",
            "Formação das virtudes",
            "Formação para os pais",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "flor-de-lis",
        "nome": "Flor de Lis",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Guará",
        "regiao_completa": "Guará II — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-verde",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": 25,
        "funcionamento": "Sábado, das 9h30 às 11h30",
        "descricao_curta": "Clube familiar do Guará II com casa prática e formação integral.",
        "descricao": (
            "O Clube Familiar Flor de Lis, localizado no Guará II, acolhe 25 associadas "
            "em um ambiente de formação humana e cristã. Oferece atividades variadas com "
            "destaque para a 'casa prática' — oficinas voltadas ao cuidado com o lar e "
            "formação integral das meninas."
        ),
        "diretora": "Ana Flávia Ferreira Santiago",
        "vice_diretora": "Marina Carvalho de Moura",
        "secretaria": "Livia Tamiris Vasconcelos",
        "monitora": None,
        "atividades_oferecidas": [
            "Casa prática",
            "Oficinas de cuidado com o lar",
            "Culinária",
            "Bordado",
            "Jardinagem",
            "Música",
            "Desenho e pintura",
            "Artesanato",
            "Moda e comportamento",
            "Esporte",
            "Formação das virtudes",
            "Formação para os pais",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "girassol",
        "nome": "Girassol",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Grande Colorado",
        "regiao_completa": "Grande Colorado — Sobradinho/DF",
        "destaque": False,
        "cor_tema": "lacos-amarelo",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": None,
        "funcionamento": None,
        "descricao_curta": "Clube do Grande Colorado com proposta vibrante e acolhedora.",
        "descricao": (
            "O Clube Girassol, localizado no Grande Colorado, oferece formação para meninas "
            "de 5 a 10 anos em um ambiente alegre e acolhedor."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
        "atividades_oferecidas": [],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "ipe-rosa",
        "nome": "Ipê Rosa",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Águas Claras / Park Way",
        "regiao_completa": "Águas Claras / Park Way — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-vermelho",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": 20,
        "funcionamento": "Sábados, das 9h30 às 11h15",
        "descricao_curta": "Clube de Águas Claras e Park Way com atividades práticas e formativas.",
        "descricao": (
            "O Clube Ipê Rosa atende meninas de 5 a 10 anos em Águas Claras e Park Way, "
            "com 20 associadas. As atividades combinam formação espiritual, "
            "habilidades práticas e momentos de cultura e amizade."
        ),
        "diretora": "Gabriela Sarkis Teixeira Ribeiro de Andrade",
        "vice_diretora": "Larissa Carvalho Bittencourt Diniz",
        "secretaria": "Alessandra Dionis Rios",
        "monitora": None,
        "atividades_oferecidas": [
            "Contação de história",
            "Clube do Livro",
            "Culinária",
            "Artesanato",
            "Aulas práticas de beleza",
            "Organização da casa",
            "Organização dos estudos",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "jacaranda",
        "nome": "Jacarandá",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Taguatinga",
        "regiao_completa": "Taguatinga Norte — Brasília/DF",
        "destaque": False,
        "cor_tema": "lacos-azul",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": 15,
        "funcionamento": "Quinzenalmente aos sábados, das 9h às 12h",
        "descricao_curta": "Clube de Taguatinga Norte com formação cultural e espiritual.",
        "descricao": (
            "O Clube Jacarandá, localizado em Taguatinga Norte, conta com 15 associadas "
            "e oferece um leque completo de atividades culturais, práticas e formativas, "
            "incluindo aulas de doutrina católica e formação das virtudes."
        ),
        "diretora": "Priscilla Machado",
        "vice_diretora": "Letícia Bonifácio",
        "secretaria": "Niágara Bomtempo",
        "monitora": None,
        "atividades_oferecidas": [
            "Artesanato",
            "Artes",
            "Culinária",
            "Música",
            "Moda",
            "Etiqueta",
            "Personal organizer",
            "Clube do livro",
            "Contação de histórias (virtudes)",
            "Aula de doutrina católica",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "margarida",
        "nome": "Margarida",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Lago Sul",
        "regiao_completa": "Lago Sul — Brasília/DF",
        "destaque": False,
        "cor_tema": "lacos-verde",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": 23,
        "funcionamento": "Sábado, das 10h às 12h",
        "descricao_curta": "Clube familiar do Lago Sul com formação integral e casa prática.",
        "descricao": (
            "O Clube Familiar Margarida, localizado no Lago Sul, atende 23 associadas em "
            "atividades que combinam aulas de doutrina, casa prática, oficinas variadas "
            "e formação das virtudes. Oferece também formação para os pais."
        ),
        "diretora": "Bruna Rosa de Oliveira Machado",
        "vice_diretora": "Marina Farias",
        "secretaria": "Aline Alves dos Santos",
        "monitora": None,
        "atividades_oferecidas": [
            "Clube do livro",
            "Aula de doutrina",
            "Casa prática",
            "Oficinas de cuidado com o lar",
            "Culinária",
            "Bordado",
            "Jardinagem",
            "Música",
            "Desenho e pintura",
            "Artesanato",
            "Moda e comportamento",
            "Esporte",
            "Formação das virtudes",
            "Formação para os pais",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },

    # ===================== CLUBES JUVENIS (3) =====================
    {
        "slug": "andorinha",
        "nome": "Andorinha",
        "categoria": "juvenil",
        "categoria_label": "Juvenil",
        "regiao": "Asa Sul",
        "regiao_completa": "Asa Sul — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-marinho",
        "fundado_em": None,
        "idades": "11 a 17 anos",
        "total_associadas": 47,
        "funcionamento": "Sábado, das 9h30 às 12h",
        "descricao_curta": "Maior clube juvenil da Asa Sul, com 47 jovens em formação.",
        "descricao": (
            "O Clube Andorinha, localizado em Brasília, é um dos maiores clubes juvenis da "
            "Associação Laços, atendendo 47 jovens de 11 a 17 anos. Oferece um amplo leque "
            "de atividades culturais, artísticas e práticas, sempre com foco na formação "
            "integral das associadas."
        ),
        "diretora": "Emanuelle Dias Weiler Soares",
        "vice_diretora": "Valessa Freiberger Tokarski Solino",
        "secretaria": "Bianca dos Anjos Bezerra Souto",
        "monitora": None,
        "atividades_oferecidas": [
            "Clube do livro",
            "Passeios",
            "Artes",
            "Culinária",
            "Arranjos florais",
            "Moda e comportamento",
            "Pintura",
            "Costura",
            "Formação das virtudes",
            "Formação espiritual",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "magnolia",
        "nome": "Magnólia",
        "categoria": "juvenil",
        "categoria_label": "Juvenil",
        "regiao": "Park Way",
        "regiao_completa": "Park Way / Águas Claras — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-marinho",
        "fundado_em": None,
        "idades": "11 a 17 anos",
        "total_associadas": 32,
        "funcionamento": "Sábado, das 9h às 11h30",
        "descricao_curta": "Clube juvenil do Park Way com 32 associadas em formação integral.",
        "descricao": (
            "O Clube Magnólia, localizado no Park Way de Águas Claras, atende 32 jovens "
            "de 11 a 17 anos. Oferece atividades culturais, artísticas e de formação "
            "espiritual, com acompanhamento de sacerdote e momentos de meditação."
        ),
        "diretora": "Fernanda Andrade",
        "vice_diretora": "Alessandra Navarrete",
        "secretaria": "Priscila Soares",
        "monitora": None,
        "atividades_oferecidas": [
            "Passeios",
            "Artes",
            "Culinária",
            "Arranjos florais",
            "Moda e comportamento",
            "Pintura",
            "Costura",
            "Meditação",
            "Acompanhamento do sacerdote",
            "Confissão",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "orquidea",
        "nome": "Orquídea",
        "categoria": "juvenil",
        "categoria_label": "Juvenil",
        "regiao": "Lago Sul",
        "regiao_completa": "Lago Sul — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-marinho",
        "fundado_em": None,
        "idades": "11 a 17 anos",
        "total_associadas": 30,
        "funcionamento": "Sábado, das 9h30 às 12h15",
        "descricao_curta": "Clube juvenil do Lago Sul com formação espiritual e prática.",
        "descricao": (
            "O Clube Juvenil Orquídea, localizado no Lago Sul, atende 30 jovens de 11 a "
            "17 anos. Oferece formação aprofundada com atendimento e meditação com o "
            "Padre Jorge, clube de leitura, formação para os pais e aulas práticas que "
            "vão de culinária a moda e comportamento."
        ),
        "diretora": "Patrícia Tusco",
        "vice_diretora": "Leslie Alves",
        "secretaria": "Ana Cristina Farias",
        "monitora": None,
        "atividades_oferecidas": [
            "Atendimento e Meditação com o Padre Jorge",
            "Formação das virtudes",
            "Clube de leitura",
            "Formação para os pais",
            "Culinária",
            "Organização",
            "Organização dos estudos",
            "Nutrição",
            "Artesanato",
            "Moda e comportamento",
        ],
        "link_inscricao": "#",
        "ativo": True,
    },
]


# ====================== FUNÇÕES AUXILIARES ======================

def get_todos_clubes():
    """Retorna todos os clubes ativos."""
    return [c for c in CLUBES if c.get("ativo", True)]


def get_clubes_destaque(quantidade=6):
    """Retorna clubes marcados como destaque."""
    destaques = [c for c in get_todos_clubes() if c.get("destaque")]
    return destaques[:quantidade]


def get_clubes_por_categoria(categoria):
    """Retorna clubes filtrados por categoria (infantil ou juvenil)."""
    return [c for c in get_todos_clubes() if c["categoria"] == categoria]


def get_clube_por_slug(slug):
    """Retorna um clube específico pelo slug, ou None se não encontrar."""
    for clube in CLUBES:
        if clube["slug"] == slug:
            return clube
    return None


def get_outros_clubes(slug_atual, mesma_categoria=True, quantidade=3):
    """Retorna outros clubes (exceto o atual)."""
    clube_atual = get_clube_por_slug(slug_atual)
    if not clube_atual:
        return []

    outros = [c for c in get_todos_clubes() if c["slug"] != slug_atual]

    if mesma_categoria:
        outros = [c for c in outros if c["categoria"] == clube_atual["categoria"]]

    return outros[:quantidade]


def get_estatisticas():
    """Retorna estatísticas gerais dos clubes."""
    todos = get_todos_clubes()
    return {
        "total_clubes": len(todos),
        "total_infantis": len(get_clubes_por_categoria("infantil")),
        "total_juvenis": len(get_clubes_por_categoria("juvenil")),
        "total_regioes": len(set(c["regiao"] for c in todos)),
    }


def get_fotos_clube(slug):
    """
    Detecta automaticamente as fotos de um clube na pasta correspondente.
    Retorna lista de caminhos relativos (a partir de static/img/clubes/<slug>/).

    Procura por: 01.jpg, 01.png, 02.jpg, 02.png... até encontrar
    o último arquivo numerado.
    """
    try:
        pasta_clube = os.path.join(
            current_app.static_folder,
            "img",
            "clubes",
            slug,
        )

        if not os.path.isdir(pasta_clube):
            return []

        fotos = []
        for arquivo in sorted(os.listdir(pasta_clube)):
            # Aceita .jpg, .jpeg, .png, .webp (minúsculo)
            extensoes_validas = (".jpg", ".jpeg", ".png", ".webp")
            if arquivo.lower().endswith(extensoes_validas):
                # Ignora arquivos que começam com ponto (.DS_Store etc)
                if not arquivo.startswith("."):
                    fotos.append(f"img/clubes/{slug}/{arquivo}")

        return fotos

    except Exception:
        return []


def get_logo_clube(slug):
    """
    Retorna o caminho do logo PNG do clube, se existir.
    Estrutura: app/static/img/clubes/<slug>.png
    """
    try:
        caminho_arquivo = os.path.join(
            current_app.static_folder,
            "img",
            "clubes",
            f"{slug}.png",
        )

        if os.path.isfile(caminho_arquivo):
            return f"img/clubes/{slug}.png"

        return None
    except Exception:
        return None


def get_fotos_clube(slug):
    """
    Detecta automaticamente as fotos de um clube na subpasta correspondente.
    Estrutura: app/static/img/clubes/<slug>/01.jpg, 02.jpg...

    Retorna lista de caminhos relativos. Lista vazia se não houver subpasta.
    """
    try:
        pasta_clube = os.path.join(
            current_app.static_folder,
            "img",
            "clubes",
            slug,
        )

        if not os.path.isdir(pasta_clube):
            return []

        fotos = []
        extensoes_validas = (".jpg", ".jpeg", ".png", ".webp")

        for arquivo in sorted(os.listdir(pasta_clube)):
            if arquivo.lower().endswith(extensoes_validas):
                if not arquivo.startswith("."):
                    fotos.append(f"img/clubes/{slug}/{arquivo}")

        return fotos

    except Exception:
        return []


def get_imagem_capa(slug):
    """
    Retorna a imagem de capa do clube com prioridade:
    1º) Primeira foto da subpasta (01.jpg)
    2º) Logo PNG (<slug>.png)
    3º) None (mostra fallback estilizado)
    """
    fotos = get_fotos_clube(slug)
    if fotos:
        return {"tipo": "foto", "caminho": fotos[0]}

    logo = get_logo_clube(slug)
    if logo:
        return {"tipo": "logo", "caminho": logo}

    return None


def get_foto_capa(slug):
    """[DEPRECATED - mantida por compatibilidade] Use get_imagem_capa."""
    capa = get_imagem_capa(slug)
    return capa["caminho"] if capa else None