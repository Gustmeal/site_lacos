"""
Pacote de modelos do Site Laços.

Importa todos os modelos para facilitar o uso no resto da aplicação
e para que o Flask-Migrate detecte automaticamente.
"""

from app.models.usuario import Usuario
from app.models.evento import Evento

# Lista pública de modelos
__all__ = ["Usuario", "Evento"]