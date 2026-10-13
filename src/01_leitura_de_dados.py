import pandas as pd
from sqlalchemy import inspect, text
from funcoes_auxiliares import RAIZ_PROJETO, criar_engine

engine = criar_engine()

# Permite executar este arquivo diretamente no console. Se a tabela não existir
# ou estiver com uma estrutura antiga, ela é recriada a partir do CSV.
caminho_csv = RAIZ_PROJETO / "data" / "raw" / "archive" / "raw.csv"
inspetor = inspect(engine)
colunas_raw = {
    coluna["name"] for coluna in inspetor.get_columns("raw")
} if inspetor.has_table("raw") else set()
if "City" not in colunas_raw:
    dados = pd.read_csv(caminho_csv, encoding="utf-8-sig")
    dados.to_sql("raw", con=engine, if_exists="replace", index=False)
    print(f"Tabela raw criada automaticamente com {len(dados)} registros.")

# A coluna foi criada pelo pandas com o nome "City" (C maiúsculo).
SQL_CONTAGEM = 'SELECT COUNT(*) AS total_linhas FROM raw'
SQL_CIDADES = """
    SELECT raw."City" AS city, COUNT(*) AS total_vendas
    FROM raw
    GROUP BY raw."City"
    ORDER BY raw."City" ASC
"""

with engine.connect() as conexao:
    total = conexao.execute(text(SQL_CONTAGEM)).scalar_one()
    cidades = pd.read_sql(text(SQL_CIDADES), conexao)

print("\n=== Total de registros por City ===")
print(total)
print("\n=== Registros agrupados por cidade ===")
print(cidades.to_string(index=False))

# O resultado também fica disponível como DataFrame para análises posteriores.
print("\n=== DataFrame pandas ===")
print(cidades)

# Salva um gráfico que pode ser aberto no Explorer/VS Code.
try:
    import matplotlib.pyplot as plt

    pasta_saida = RAIZ_PROJETO / "data" / "processed"
    pasta_saida.mkdir(parents=True, exist_ok=True)
    caminho_grafico = pasta_saida / "vendas_por_cidade.png"

    ax = cidades.plot.bar(
        x="city",
        y="total_vendas",
        legend=False,
        title="Quantidade de vendas por cidade",
        ylabel="Quantidade de vendas",
        rot=0,
    )
    ax.figure.tight_layout()
    ax.figure.savefig(caminho_grafico, dpi=150)
    print(f"\nGráfico salvo em: {caminho_grafico}")

    # Em Jupyter/VS Code interativo, exibe o gráfico inline.
    try:
        from IPython.display import display

        display(ax.figure)
    except ImportError:
        pass
finally:
    engine.dispose()
