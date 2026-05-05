"""
Rotas públicas do Site Laços.

Todas as páginas acessíveis sem login ficam aqui.
"""

from flask import render_template
from app.blueprints.public import public_bp
from app.data.clubes_data import (
    get_clubes_destaque,
    get_clubes_por_categoria,
    get_estatisticas,
)


@public_bp.route("/")
def home():
    """Página inicial do site."""
    # Pega os 6 primeiros clubes para destaque na home
    clubes_destaque = get_clubes_destaque(quantidade=6)
    estatisticas = get_estatisticas()
    return render_template(
        "pages/home.html",
        clubes_destaque=clubes_destaque,
        estatisticas=estatisticas,
    )


@public_bp.route("/quem-somos")
def quem_somos():
    """Página Quem Somos (institucional)."""
    return render_template("pages/quem_somos.html")


@public_bp.route("/atividades")
def atividades():
    """Página com as 10 atividades oferecidas."""
    return render_template("pages/atividades.html")


@public_bp.route("/clubes")
def clubes_lista():
    """Página de listagem dos clubes (categorias)."""
    clubes_infantis = get_clubes_por_categoria("infantil")
    clubes_juvenis = get_clubes_por_categoria("juvenil")
    estatisticas = get_estatisticas()
    return render_template(
        "pages/clubes_lista.html",
        clubes_infantis=clubes_infantis,
        clubes_juvenis=clubes_juvenis,
        estatisticas=estatisticas,
    )