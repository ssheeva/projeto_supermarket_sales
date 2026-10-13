import pandas as pd
from sqlalchemy import text
import re
from funcoes_auxiliares import RAIZ_PROJETO, criar_engine, ler_configuracao

# 1. Configurar as credenciais do banco de dados
configuracao = ler_configuracao()
BANCO = configuracao["banco"]

if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", BANCO):
    raise ValueError("POSTGRES_DB contém um nome de banco inválido")

# Cria o banco de destino se ele ainda não existir.
engine_admin = criar_engine("postgres", isolation_level="AUTOCOMMIT")
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
engine = criar_engine(BANCO)
# 3. Ler o arquivo CSV usando o Pandas.
# O caminho é relativo ao projeto, evitando depender do usuário/computador
# onde o script foi originalmente criado.
caminho_csv = RAIZ_PROJETO / "data" / "raw" / "archive" / "raw.csv"
# O pandas detecta automaticamente o delimitador, mas você pode forçar com sep=',' ou sep=';'
df = pd.read_csv(caminho_csv, encoding="utf-8-sig")

# 4. Enviar os dados e criar a tabela automaticamente
nome_da_tabela = "raw"

df.to_sql(
    name=nome_da_tabela, 
    con=engine, 
    if_exists="replace",  # Recria a tabela quando ela já existir.
    index=False         # Define se o índice do Pandas deve virar uma coluna na tabela
)

print(f"Tabela '{nome_da_tabela}' criada e CSV importado com sucesso!")
