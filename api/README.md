# Hiring Tracker – API (FastAPI)

API REST do Hiring Tracker (MVP). Fornece endpoints de CRUD para **empresas**, **vagas**, **candidatos** e health-check.
Integra com **PostgreSQL**, **RabbitMQ** e **Azure Blob (Azurite em dev)** via serviços.

## Execução local (Docker)
Assumindo infra já no ar com `docker-compose.infra.local.yaml`:

```bash
docker compose up -d --build api
```

A API rodará em `http://localhost:8080/api/v1`.

## Variáveis (.env)
A API lê as seguintes variáveis (exemplos em `.env.example` na raiz do projeto):

- `DATABASE_URL=postgresql+asyncpg://app:app@db:5432/hiring`
- `AMQP_URL=amqp://guest:guest@mq:5672/`
- `AZURE_STORAGE_CONN_STR=...` (Azurite no dev)
- `BLOB_CONTAINER=cv`
- `API_HOST=0.0.0.0`, `API_PORT=8080`

## Estrutura
```
app/
  api/routers/      # endpoints
  core/             # config, logging, deps
  db/models/        # ORM models (SQLAlchemy)
  schemas/          # Pydantic models
  services/         # DB services, messaging, blob storage
  main.py
tests/              # testes unitários básicos
```

## Migrations
O projeto usa as migrations SQL do diretório `migrations/sql` da raiz e o serviço `migrator` do compose.
Para aplicar:
```bash
docker compose run --rm migrator
```

## Testes
```bash
pip install -r requirements.txt
pytest -q
```
Os testes unitários são focados nos **services** (padrão Repository/Service); usamos *mocks* para sessão DB e conectores.
