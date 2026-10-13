import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
import os
import re

raiz_projeto = Path(__file__).resolve().parents[1]
load_dotenv(raiz_projeto / ".env")

# 1. Configurar as credenciais do banco de dados
USUARIO = os.getenv("POSTGRES_USER", "root")
SENHA = os.getenv("POSTGRES_PASSWORD", "admin123")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORTA = os.getenv("POSTGRES_PORT", "5432")
BANCO = os.getenv("POSTGRES_DB", "loja")

if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", BANCO):
    raise ValueError("POSTGRES_DB contém um nome de banco inválido")

def url(banco):
    return f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{banco}"

# Cria o banco de destino se ele ainda não existir.
engine_admin = create_engine(url("postgres"), isolation_level="AUTOCOMMIT")
with engine_admin.connect() as conexao:
    existe = conexao.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :banco"),
        {"banco": BANCO},
    ).scalar()
    if not existe:
        conexao.execute(text(f'CREATE DATABASE "{BANCO}"'))
engine_admin.dispose()

# 2. Criar o motor de conexão (Engine) do SQLAlchemy
# Para psycopg2, a URL começa com: postgresql+psycopg2://
# Para psycopg3, use: postgresql+psycopg://
engine = create_engine(
    url(BANCO),
    connect_args={"options": "-c client_encoding=utf8"}
)
# 3. Ler o arquivo CSV usando o Pandas.
# O caminho é relativo ao projeto, evitando depender do usuário/computador
# onde o script foi originalmente criado.
caminho_csv = raiz_projeto / "data" / "raw" / "archive" / "raw.csv"
# O pandas detecta automaticamente o delimitador, mas você pode forçar com sep=',' ou sep=';'
df = pd.read_csv(caminho_csv, encoding="utf-8-sig")

# 4. Enviar os dados e criar a tabela automaticamente
nome_da_tabela = "raw"

df.to_sql(
    name=nome_da_tabela, 
    con=engine, 
    if_exists="replace",   # Opções: 'fail' (erro se já existir), 'replace' (recria), 'append' (adiciona)
    index=False         # Define se o índice do Pandas deve virar uma coluna na tabela
)

print(f"Tabela '{nome_da_tabela}' criada e CSV importado com sucesso!")
