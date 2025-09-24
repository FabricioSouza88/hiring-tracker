# Hiring Tracker – Agents

Serviço de **agents** (triagem, avaliação de teste, juiz) que consome eventos do **RabbitMQ** e publica resultados na **API** do Hiring Tracker.

## Execução local (Docker)
Assumindo a infra e a API em execução via `docker-compose.infra.local.yaml` e `docker-compose.yaml`:

```bash
docker compose up -d --build agents
```

## Variáveis (.env)
- `AMQP_URL=amqp://guest:guest@mq:5672/`
- `API_BASE_URL=http://api:8080/api/v1`
- `OPENAI_API_KEY=replace-me` (ou outro provedor)
- `AGENTS_PREFETCH=16`
- `AGENTS_CONCURRENCY=32`

## Estrutura
```
agents/
  core/
    settings.py       # Config via env
    logging.py        # structlog
    mq.py             # conexão RabbitMQ (aio-pika)
    client.py         # http client para API
  consumers/
    triage.py
    code_evaluator.py
    judge.py
  prompts/
    triage.md
    code_evaluator.md
    judge.md
  runner.py           # loop principal: conecta MQ + inicia consumers
tests/
  test_runner_smoke.py
```

## Como funciona
- O `runner` conecta no RabbitMQ, declara trocas/filas e inicia consumidores asyncio para cada agent.
- Cada consumer processa mensagens em concorrência (tasks), com `prefetch` configurável, e confirma (`ack`) apenas após sucesso.
- Em caso de exceção, aplica retentativa (tenacity) e nack (DLQ opcional).

## Próximos passos
- Implementar lógica real dos prompts e chamada ao provedor LLM.
- Implementar idempotência real (cache/DB) para evitar processamento duplo.
- Enviar relatórios finais para `POST /agents/reports` na API.
