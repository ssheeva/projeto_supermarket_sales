import pandas as pd
from sqlalchemy import create_engine

# 1. Configurar as credenciais do banco de dados
USUARIO = "root"
SENHA = "admin123"
HOST = "localhost"
PORTA = "5432"  # Porta padrão do PostgreSQL
BANCO = "loja"

# 2. Criar o motor de conexão (Engine) do SQLAlchemy
# Para psycopg2, a URL começa com: postgresql+psycopg2://
# Para psycopg3, use: postgresql+psycopg://
engine = create_engine(
    f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}",
    connect_args={"options": "-c client_encoding=utf8"}
)
# 3. Ler o arquivo CSV usando o Pandas
caminho_csv = "C:\\Users\\nogueira\\Desktop\\projeto_supermarket\\projeto_supermarket_sales\\data\\raw\\archive\\SuperMarket Analysis.csv"
# O pandas detecta automaticamente o delimitador, mas você pode forçar com sep=',' ou sep=';'
df = pd.read_csv(caminho_csv, encoding='utf-8-sig')

# 4. Enviar os dados e criar a tabela automaticamente
nome_da_tabela = "raw"

df.to_sql(
    name=nome_da_tabela, 
    con=engine, 
    if_exists="fail",   # Opções: 'fail' (erro se já existir), 'replace' (recria), 'append' (adiciona)
    index=False         # Define se o índice do Pandas deve virar uma coluna na tabela
)

print(f"Tabela '{nome_da_tabela}' criada e CSV importado com sucesso!")
