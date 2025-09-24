# Stack Técnica – Hiring Tracker (MVP)

## 1) Princípios para o MVP
- **Simplicidade primeiro**: foco em entregar valor rápido; componentes fáceis de operar localmente.
- **Separação mínima por módulos**: `web` (Streamlit), `api` (FastAPI), `agents` (serviço próprio), `infra` (DB, fila, blob).
- **Reuso futuro**: a **API** será reutilizada quando o front evoluir (React/Next.js), mantendo padrões REST e versionamento.
- **Observabilidade e qualidade**: logging estruturado, testes, linters; nada de overengineering.

---

## 2) Módulos e Responsabilidades

### 2.1 Frontend (MVP) — Streamlit
- **Objetivo**: painel operacional para recrutadores validarem o fluxo rapidamente.
- **Stack**: Python 3.11, `streamlit`, `requests`, `pydantic`.
- **Entrega**: listagem de empresas, vagas, candidatos; detalhar *application* e estágios; submissão de links de teste; upload de CV.
- **Execução**: via Docker (`streamlit run app.py --server.port 8501`).

### 2.2 API — FastAPI (reutilizável pós-MVP)
- **Objetivo**: servir o front e integrar com agentes e mensageria.
- **Stack**: Python 3.11, `fastapi` (Pydantic v2), `uvicorn`, `SQLAlchemy 2.x`, `alembic`, `psycopg[binary]`, `python-multipart`, `azure-storage-blob`.
- **Padrões**:
  - Versionamento: prefixo `/api/v1`.
  - Validações fortes (Pydantic), erros padronizados (problem+json).
  - **Autenticação**: JWT (lib `pyjwt`) com OIDC plugável (Auth0/Azure AD) no futuro.
  - **Upload**: CV → Blob; apenas metadados no DB.
  - **Eventos**: publicar em RabbitMQ ao criar `application`, `test_submission`, etc.
- **Testes**: `pytest`, `httpx`, `pytest-asyncio`, `coverage`.
- **Qualidade**: `ruff` (lint), `black` (format), `mypy` (typing).

### 2.3 Ecosistema de Agentes — Serviço separado (`agents`)
- **Decisão**: **aplicação separada**. Mantém acoplamento baixo e escala independente no futuro.
- **Stack**: Python 3.11, `aio-pika` (RabbitMQ), `pydantic`, `tenacity` (retries), `httpx`.
- **LLM/Framework** (MVP): prompts *handcrafted* + chamadas diretas à API do provedor (ex.: OpenAI/Vertex). Frameworks como `langgraph`/`langchain` podem ser adicionados depois.
- **Fluxo**:
  - Consome eventos: `application.created` → **triagem**; `test.submitted` → **avaliador de teste**; `all.inputs.ready` → **juiz**.
  - Persiste resultados via **API** (endpoints `/agents/runs` e `/agents/reports`).

### 2.4 Banco de Dados
- **Tecnologia**: **PostgreSQL 16**.
- **Migrações**: `alembic` (API).
- **Índices**: em `applications`, `application_stages`, `agent_reports` (já planejados).
- **Backups**: fora do escopo do MVP (apenas dump local quando necessário).

### 2.5 Blob Storage
- **Tecnologia**: **Azure Blob** (em produção) / **Azurite** (em dev, via Docker).
- **Lib**: `azure-storage-blob` (API).
- **Política**: bucket/container privado; validação de content-type e tamanho.

### 2.6 Mensageria
- **Tecnologia**: **RabbitMQ** (fila + *fanout* simples).
- **Libs**: `aio-pika` (agents), `aio-pika` ou `pika` (API publisher).
- **Motivo**: amplamente suportado, leve e fácil em Docker; bom para *fire-and-forget* no MVP.

### 2.7 Observabilidade & Operação
- **Logs**: `structlog` ou `loguru`; correlação por `application_id`.
- **Tracing** (opcional): `opentelemetry-sdk` + `opentelemetry-instrumentation-fastapi` (exporter console no MVP).
- **Métricas** (opcional): `prometheus_client` na API; scraper pode vir depois.
- **Health-checks**: `/healthz` na API e probes simples para agents.

---

## 3) Infra local com Docker Compose (dev)

### 3.1 Serviços
- `db`: PostgreSQL 16 com volume.
- `azurite`: emulador do Azure Blob para *uploads* de CV.
- `mq`: RabbitMQ (com plugin de management).
- `api`: FastAPI + Alembic (migrations na subida).
- `agents`: consumidor de filas e integrador com API/LLM.
- `web`: Streamlit servindo o painel.
- (opcionais) `pgadmin` para DB.

### 3.2 Arquivo `docker-compose.yml` (MVP)
```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: hiring
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d hiring"]
      interval: 5s
      timeout: 5s
      retries: 10

  azurite:
    image: mcr.microsoft.com/azure-storage/azurite
    command: azurite --blobHost 0.0.0.0 --loose
    ports:
      - "10000:10000"   # Blob
    volumes:
      - azurite_data:/data

  mq:
    image: rabbitmq:3.13-management
    ports:
      - "5672:5672"
      - "15672:15672" # management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  api:
    build: ./services/api
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      mq:
        condition: service_started
      azurite:
        condition: service_started
    ports:
      - "8080:8080"
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8080"

  agents:
    build: ./services/agents
    env_file: .env
    depends_on:
      api:
        condition: service_started
      mq:
        condition: service_started
    command: ["python", "-m", "agents.runner"]

  web:
    build: ./services/web
    env_file: .env
    depends_on:
      api:
        condition: service_started
    ports:
      - "8501:8501"
    command: ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - pgadmin_data:/var/lib/pgadmin

volumes:
  db_data: { }
  azurite_data: { }
  rabbitmq_data: { }
  pgadmin_data: { }
```

### 3.3 `.env` (exemplo para dev)
```
# API
API_HOST=0.0.0.0
API_PORT=8080
API_BASE_URL=http://api:8080/api/v1
JWT_SECRET=dev-secret
JWT_ALG=HS256

# DB
DB_HOST=db
DB_PORT=5432
DB_USER=app
DB_PASS=app
DB_NAME=hiring
DATABASE_URL=postgresql+psycopg://app:app@db:5432/hiring

# RabbitMQ
AMQP_URL=amqp://guest:guest@mq:5672/

# Blob (Azurite)
AZURE_STORAGE_CONN_STR=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite:10000/devstoreaccount1;
BLOB_CONTAINER=cv

# LLM Provider (placeholder)
LLM_PROVIDER=openai
OPENAI_API_KEY=replace-me
```

---

## 4) Estrutura de Pastas sugerida
```
hiring-tracker/
  docs/
    stack-mvp.md
    requisitos.md
  services/
    api/
      app/
        api/          # routers
        core/         # settings, security, deps
        db/           # models, migrations scripts
        schemas/      # pydantic models
        services/     # business services (publishers, storage)
        main.py
      alembic/
      pyproject.toml
      Dockerfile
    agents/
      agents/
        consumers/    # triage, code_evaluator, judge
        runner.py
        client.py     # http client to API
        prompts/      # system prompts (EN)
      pyproject.toml
      Dockerfile
    web/
      app.py
      pages/          # streamlit pages
      pyproject.toml
      Dockerfile
  docker-compose.yml
  .env
  Makefile
  README.md
```

---

## 5) Bibliotecas (versões sugeridas)
- **API**: fastapi ^0.115, uvicorn ^0.30, pydantic ^2.8, sqlalchemy ^2.0, alembic ^1.13, psycopg[binary] ^3.2, azure-storage-blob ^12.20, python-multipart ^0.0.9, aio-pika ^9.4, structlog ^24.1
- **Agents**: aio-pika ^9.4, httpx ^0.27, tenacity ^8.5, pydantic ^2.8, (opcional) langchain/langgraph posteriormente
- **Web (Streamlit)**: streamlit ^1.38, requests ^2.32, pydantic ^2.8
- **Qualidade**: ruff ^0.6, black ^24.8, mypy ^1.10, pytest ^8.3, pytest-asyncio ^0.23, coverage ^7.6

> Observação: versões podem ser ajustadas conforme compatibilidade no momento do setup.

---

## 6) Endpoints-chave (API v1 – resumo)
- `POST /api/v1/companies`, `GET /companies`
- `POST /api/v1/jobs`, `GET /jobs`
- `POST /api/v1/candidates`, `GET /candidates`
- `PUT /api/v1/candidates/{id}/resume` (upload → Blob)
- `POST /api/v1/applications`
- `POST /api/v1/applications/{id}/test-submissions`
- `POST /api/v1/applications/{id}/interview-reports`
- `GET /api/v1/applications/{id}` (com stages, reports)
- `POST /api/v1/agents/runs` (cria run manual se necessário)
- `GET /api/v1/agents/reports?application_id=...`

---

## 7) Segurança (MVP)
- JWT simples (HS256) com expiração curta; migração para OIDC em fase 2.
- Sanitização de uploads (tamanho, tipo) + *scan* opcional.
- Dados pessoais: não logar PII; mascarar CPF/Email nos logs.
- CORS: restringir ao host do front (`web`).

---

## 8) Migrações e Seeds
- `alembic upgrade head` na subida da API.
- Seeds mínimos opcionais (empresas/vagas fake) via script `app/db/seed.py`.

---

## 9) Makefile (qualidade e DX)
```Makefile
.PHONY: up down logs api web agents fmt lint test

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

api-shell:
	docker compose exec api bash

fmt:
	docker compose run --rm api black . && docker compose run --rm api ruff check --fix .

lint:
	docker compose run --rm api ruff check . && docker compose run --rm api mypy app

test:
	docker compose run --rm api pytest -q --maxfail=1 --disable-warnings
```

---

## 10) Próximos Passos
1. Inicializar repositório com esta estrutura e **docker-compose**.
2. Implementar modelos/DDL + migrations (API).
3. Implementar publishers de eventos na API e consumidores no `agents`.
4. Criar páginas básicas no Streamlit.
5. Escrever prompts iniciais (EN) para **triage**, **code evaluator** e **judge** (revisáveis).
6. Adicionar testes e linters ao CI (GitHub Actions).

---

> **Resumo**: A stack acima entrega rapidez no MVP (Streamlit + FastAPI) com orquestração simples via RabbitMQ, armazenamento em PostgreSQL + Blob (Azurite em dev) e separação clara do serviço de *agents*. Ela permanece leve para o dia a dia e já prepara o terreno para evoluções (OIDC, React, escalabilidade horizontal) sem refatorações bruscas.
