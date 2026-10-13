"""Funções compartilhadas pelos scripts do projeto."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


RAIZ_PROJETO = Path(__file__).resolve().parents[1]
load_dotenv(RAIZ_PROJETO / ".env")


def ler_configuracao():
    """Lê as configurações do PostgreSQL no arquivo .env."""
    return {
        "usuario": os.getenv("POSTGRES_USER", "root"),
        "senha": os.getenv("POSTGRES_PASSWORD", "admin123"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "porta": os.getenv("POSTGRES_PORT", "5432"),
        "banco": os.getenv("POSTGRES_DB", "loja"),
    }


def criar_engine(banco=None, **opcoes):
    """Cria um engine SQLAlchemy usando o .env."""
    configuracao = ler_configuracao()
    banco = banco or configuracao["banco"]
    url = (
        f"postgresql+psycopg2://{configuracao['usuario']}:{configuracao['senha']}"
        f"@{configuracao['host']}:{configuracao['porta']}/{banco}"
    )
    return create_engine(
        url,
        connect_args={"options": "-c client_encoding=utf8"},
        **opcoes,
    )
