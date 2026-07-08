"""Blueprint da área restrita das famílias."""

from flask import Blueprint

familia_bp = Blueprint(
    "familia",
    __name__,
    url_prefix="/familia",
)

from app.blueprints.familia import routes