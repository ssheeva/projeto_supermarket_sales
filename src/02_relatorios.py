"""Executa as consultas SQL e materializa os relatórios em data/processed.

As consultas da pasta ``sql/consultas`` são a fonte única dos relatórios. Para
as consultas que criam visões, a visão é criada somente quando ainda não existe.
Os resultados agregados são exportados para CSV e, quando há uma dimensão e uma
medida numérica, também para PNG.
"""

from pathlib import Path
import re

import pandas as pd
from sqlalchemy import inspect, text

from funcoes_auxiliares import RAIZ_PROJETO, criar_engine


PASTA_CONSULTAS = RAIZ_PROJETO / "sql" / "consultas"
PASTA_SAIDA = RAIZ_PROJETO / "data" / "processed"


def nome_seguro(valor: str) -> str:
    """Converte um nome de relatório em um nome seguro para arquivo."""
    valor = valor.lower().replace(" ", "_")
    valor = re.sub(r"[^a-z0-9_]+", "", valor)
    return valor.strip("_")


def extrair_view(sql: str) -> str | None:
    """Retorna o nome da visão declarada no SQL, se houver."""
    correspondencia = re.search(r"\bcreate\s+view\s+([\w\"]+)", sql, re.IGNORECASE)
    if not correspondencia:
        return None
    return correspondencia.group(1).strip('"')


def sql_da_view(sql: str, view: str) -> str:
    """Remove o DDL da visão e retorna apenas a consulta equivalente."""
    inicio = re.search(r"\bcreate\s+view\s+[\w\"]+\s+as\s+", sql, re.IGNORECASE)
    if not inicio:
        raise ValueError(f"Não foi possível localizar o SELECT da visão {view}.")
    consulta = sql[inicio.end():].strip()
    return consulta.rstrip(";").strip()


def desenhar_grafico(dados: pd.DataFrame, caminho: Path, titulo: str) -> bool:
    """Gera gráfico para uma tabela com uma dimensão e uma medida numérica."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if dados.shape[1] < 2 or dados.empty:
        return False

    medida = next((col for col in dados.columns if pd.api.types.is_numeric_dtype(dados[col])), None)
    dimensao = next((col for col in dados.columns if col != medida), None)
    if medida is None or dimensao is None:
        return False

    serie = dados[[dimensao, medida]].dropna()
    if serie.empty:
        return False

    figura, eixo = plt.subplots(figsize=(10, 5))
    serie.plot.bar(x=dimensao, y=medida, ax=eixo, legend=False)
    eixo.set_title(titulo)
    eixo.set_xlabel(dimensao)
    eixo.set_ylabel(medida)
    eixo.tick_params(axis="x", labelrotation=30)

    # Exibe o valor no topo de cada barra para facilitar a leitura do gráfico.
    for barra in eixo.patches:
        valor = barra.get_height()
        eixo.annotate(
            f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            (barra.get_x() + barra.get_width() / 2, valor),
            ha="center",
            va="bottom",
            xytext=(0, 3),
            textcoords="offset points",
            fontsize=9,
        )

    figura.tight_layout()
    figura.savefig(caminho, dpi=150)
    plt.close(figura)
    return True


def main() -> None:
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(PASTA_CONSULTAS.glob("*.sql"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum SQL encontrado em {PASTA_CONSULTAS}")

    engine = criar_engine()
    try:
        inspetor = inspect(engine)
        views_existentes = set(inspetor.get_view_names())
        with engine.begin() as conexao:
            for arquivo in arquivos:
                sql = arquivo.read_text(encoding="utf-8-sig")
                view = extrair_view(sql)

                if view and view not in views_existentes:
                    conexao.execute(text(sql.rstrip().rstrip(";") + ";"))
                    views_existentes.add(view)
                    print(f"Visão criada: {view}")
                elif view:
                    print(f"Visão já existente: {view}")

                consulta = sql_da_view(sql, view) if view else sql.rstrip().rstrip(";")
                dados = pd.read_sql(text(consulta), conexao)

                base = nome_seguro(arquivo.stem)
                caminho_csv = PASTA_SAIDA / f"{base}.csv"
                dados.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

                caminho_png = PASTA_SAIDA / f"{base}.png"
                if desenhar_grafico(dados, caminho_png, arquivo.stem.replace("_", " ").title()):
                    print(f"Relatório e gráfico gerados: {base}")
                else:
                    print(f"Relatório gerado (sem gráfico aplicável): {base}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
