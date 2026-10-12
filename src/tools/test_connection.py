from sqlalchemy import create_engine, text

USUARIO = "root"
SENHA = "admin123"
HOST = "localhost"
PORTA = "5432"
BANCO = "loja"

engine = create_engine(
    f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
)

with engine.connect() as conexao:
    resultado = conexao.execute(text("SELECT 1")).scalar_one()

print(f"Conexão com o PostgreSQL realizada com sucesso (SELECT {resultado}).")
