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
        "link_inscricao": "#",  # Vai virar admin de pais depois
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
        "total_associadas": None,
        "descricao_curta": "Clube infantil do Lago Norte com atividades formativas e culturais.",
        "descricao": (
            "O Clube Camélia, localizado no Lago Norte, oferece atividades formativas para "
            "meninas de 5 a 10 anos, com foco na vivência das virtudes e desenvolvimento integral."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "flor-de-lis",
        "nome": "Flor de Lis",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Guará",
        "regiao_completa": "Guará — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-verde",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": None,
        "descricao_curta": "Clube do Guará com atividades dinâmicas e formação de virtudes.",
        "descricao": (
            "O Clube Flor de Lis, localizado no Guará, acolhe meninas de 5 a 10 anos em um "
            "ambiente de formação humana e cristã, com atividades variadas e dinâmicas."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
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
        "descricao_curta": "Clube do Grande Colorado com proposta vibrante e acolhedora.",
        "descricao": (
            "O Clube Girassol, localizado no Grande Colorado, oferece formação para meninas "
            "de 5 a 10 anos em um ambiente alegre e acolhedor."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "ipe-rosa",
        "nome": "Ipê Rosa",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Águas Claras",
        "regiao_completa": "Águas Claras — Brasília/DF",
        "destaque": True,
        "cor_tema": "lacos-vermelho",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": None,
        "descricao_curta": "Clube de Águas Claras com forte ênfase em virtudes e amizades.",
        "descricao": (
            "O Clube Ipê Rosa, localizado em Águas Claras, é um espaço de formação e amizade "
            "para meninas de 5 a 10 anos, com atividades semanais ricas e variadas."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "jacaranda",
        "nome": "Jacarandá",
        "categoria": "infantil",
        "categoria_label": "Infantil",
        "regiao": "Taguatinga",
        "regiao_completa": "Taguatinga — Brasília/DF",
        "destaque": False,
        "cor_tema": "lacos-azul",
        "fundado_em": None,
        "idades": "5 a 10 anos",
        "total_associadas": None,
        "descricao_curta": "Clube de Taguatinga, ambiente acolhedor para crescer com alegria.",
        "descricao": (
            "O Clube Jacarandá, localizado em Taguatinga, oferece atividades formativas para "
            "meninas de 5 a 10 anos, em um ambiente que combina alegria e formação."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
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
        "total_associadas": None,
        "descricao_curta": "Clube do Lago Sul, espaço seguro para meninas crescerem.",
        "descricao": (
            "O Clube Margarida, localizado no Lago Sul, é um espaço seguro e formativo para "
            "meninas de 5 a 10 anos, com atividades semanais."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
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
        "total_associadas": None,
        "descricao_curta": "Clube juvenil da Asa Sul, formação aprofundada para jovens.",
        "descricao": (
            "O Clube Andorinha, localizado na Asa Sul, oferece formação aprofundada para "
            "jovens de 11 a 17 anos, com atividades adaptadas à fase da adolescência."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
        "link_inscricao": "#",
        "ativo": True,
    },
    {
        "slug": "magnolia",
        "nome": "Magnólia",
        "categoria": "juvenil",
        "categoria_label": "Juvenil",
        "regiao": "Park Way",
        "regiao_completa": "Park Way — Brasília/DF",
        "destaque": False,
        "cor_tema": "lacos-marinho",
        "fundado_em": None,
        "idades": "11 a 17 anos",
        "total_associadas": None,
        "descricao_curta": "Clube juvenil do Park Way, jovens em formação e amizade.",
        "descricao": (
            "O Clube Magnólia, localizado no Park Way, é um espaço de formação para jovens "
            "de 11 a 17 anos, com foco em amizade e crescimento integral."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
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
        "total_associadas": None,
        "descricao_curta": "Clube juvenil do Lago Sul, atividades para jovens em formação.",
        "descricao": (
            "O Clube Orquídea, localizado no Lago Sul, atende jovens de 11 a 17 anos em "
            "um ambiente formativo e desafiador."
        ),
        "diretora": None,
        "vice_diretora": None,
        "secretaria": None,
        "monitora": None,
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