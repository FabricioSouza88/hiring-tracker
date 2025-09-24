# Hiring Tracker (MVP)

Sistema para gestão de processos seletivos com API (FastAPI), ecosistema de agentes (RabbitMQ) e frontend Streamlit.

## Como executar (dev)

### 1) Infra local
Suba apenas infraestrutura (PostgreSQL, RabbitMQ, Azurite):
```bash
docker compose -f docker-compose.infra.local.yaml up -d
```

### 2) Serviços (API, Agents, Frontend)
Com a infra rodando, suba os serviços da aplicação:
```bash
docker compose up -d --build
```

A API ficará em `http://localhost:8080` e o Streamlit em `http://localhost:8501`. 
O RabbitMQ Management em `http://localhost:15672` (guest/guest) e o Azurite Blob em `http://localhost:10000`.

### 3) Migrations (DDL inicial)
Se ainda não rodou migrations, execute o migrator:
```bash
docker compose run --rm migrator
```
Esse serviço aplica todos os arquivos `.sql` em `migrations/sql` em ordem (001_, 002_, ...).

## Como usar as migrations
- Adicione novos arquivos em `migrations/sql` com o prefixo incremental (`002_add_table_x.sql`).
- Rode novamente `docker compose run --rm migrator`.
- Em produção, recomendamos evoluir para Alembic/EF Core; no MVP usamos SQL + runner Python.

## Estrutura
```
frontend/   # Streamlit (MVP UI) - código na próxima etapa
api/        # FastAPI (REST)     - código na próxima etapa
agents/     # Serviços de agentes - código na próxima etapa
migrations/ # SQL + runner Python (migrator)
.vscode/    # launch.json para debug
```

## Variáveis de ambiente (.env)
Copie `.env.example` para `.env` e ajuste se necessário.

## Testes e Qualidade
- Planejado: pytest, ruff, black, mypy (adicionados nos requirements quando formos codar).
