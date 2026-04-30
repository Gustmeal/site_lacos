"""
Ponto de entrada da aplicação Site Laços.

Este arquivo é usado para rodar a aplicação localmente
(via `flask run` ou `python run.py`) e em produção (via gunicorn).
"""

import os
from app import create_app

# Cria a aplicação usando a configuração apropriada
app = create_app(os.environ.get("FLASK_ENV", "development"))


if __name__ == "__main__":
    # Usado quando rodar com: python run.py
    app.run(host="0.0.0.0", port=5002, debug=True)