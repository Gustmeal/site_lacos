"""
Rotas públicas do Site Laços.

Todas as páginas acessíveis sem login ficam aqui.
"""

from flask import render_template
from app.blueprints.public import public_bp


@public_bp.route("/")
def home():
    """Página inicial do site."""
    return render_template("pages/home.html")


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
    return render_template("pages/clubes_lista.html")