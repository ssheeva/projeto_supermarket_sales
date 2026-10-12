# PostgreSQL local

O banco de dados local roda em PostgreSQL 18 usando Docker Compose.

Para iniciar o banco na raiz do projeto:

```sh
docker compose up -d
```

Conexão:

- Host: `localhost`
- Porta: `5432`
- Usuário: `root`
- Senha: `admin123`
- Banco: `loja`

Para parar o contêiner sem apagar os dados:

```sh
docker compose down
```

Os dados ficam no volume `postgres_loja_data` e são preservados ao parar ou
remover o contêiner. As credenciais deste arquivo são adequadas apenas para
desenvolvimento local.