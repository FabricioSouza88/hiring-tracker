# Makefile - Hiring Tracker

# Variáveis
COMPOSE = docker-compose
INFRA_FILE = -f docker-compose.infra.local.yaml
APP_FILE = -f docker-compose.yaml

# ---------------------
# Infraestrutura
# ---------------------

infra-up:
	$(COMPOSE) $(INFRA_FILE) up -d

infra-down:
	$(COMPOSE) $(INFRA_FILE) down -v

infra-logs:
	$(COMPOSE) $(INFRA_FILE) logs -f --tail=200

# ---------------------
# Aplicação (API, Agents, Frontend)
# ---------------------

app-up:
	$(COMPOSE) $(APP_FILE) up -d --build

app-down:
	$(COMPOSE) $(APP_FILE) down -v

app-logs:
	$(COMPOSE) $(APP_FILE) logs -f --tail=200

# ---------------------
# Banco & Migrations
# ---------------------

migrate:
	$(COMPOSE) $(APP_FILE) run --rm migrator

psql:
	$(COMPOSE) $(INFRA_FILE) exec db psql -U app -d hiring

# ---------------------
# API
# ---------------------

api-shell:
	$(COMPOSE) $(APP_FILE) exec api bash

api-logs:
	$(COMPOSE) $(APP_FILE) logs -f api

api-test:
	$(COMPOSE) $(APP_FILE) run --rm api pytest -q --disable-warnings

api-lint:
	$(COMPOSE) $(APP_FILE) run --rm api ruff check app
	$(COMPOSE) $(APP_FILE) run --rm api mypy app

# ---------------------
# Agents
# ---------------------

agents-shell:
	$(COMPOSE) $(APP_FILE) exec agents bash

agents-logs:
	$(COMPOSE) $(APP_FILE) logs -f agents

# ---------------------
# Frontend (Streamlit)
# ---------------------

frontend-logs:
	$(COMPOSE) $(APP_FILE) logs -f frontend

# ---------------------
# Conveniências
# ---------------------

logs: infra-logs app-logs
up: infra-up app-up
down: infra-down app-down
