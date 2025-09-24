# Documento de Requisitos – Hiring Tracker (MVP)

## 1. Visão Geral

O **Hiring Tracker** é um sistema para gestão de processos seletivos de candidatos em uma empresa. Ele permite cadastrar empresas, vagas, candidatos e acompanhar as etapas de seleção de forma estruturada, com apoio de agentes de IA para triagem, avaliação técnica e decisão final.

---

## 2. Objetivos do Sistema

* Centralizar o cadastro de **empresas**, **vagas** e **candidatos**.
* Automatizar parte do processo seletivo por meio de **agents de IA**.
* Disponibilizar uma **API** para integração com outros sistemas da empresa.
* Facilitar a **orquestração de etapas** do processo seletivo via eventos.

---

## 3. Entidades Principais

### 3.1. Empresa

* **id** (uuid)
* **nome\_fantasia** (string)
* **razao\_social** (string)
* **cnpj** (string, único)
* **website** (string, opcional)
* **telefone** (string, opcional)
* **endereco** (rua, número, bairro, cidade, estado, CEP, país)
* **created\_at**, **updated\_at** (timestamps)

### 3.2. Vaga

* **id** (uuid)
* **empresa\_id** (fk → Empresa)
* **titulo** (string)
* **descricao** (text)
* **descricao\_teste** (text)
* **senioridade** (enum: ESTAGIARIO, JR, PLENO, SENIOR, LIDER – opcional)
* **localizacao\_tipo** (enum: PRESENCIAL, REMOTO, HIBRIDO – opcional)
* **ativo** (boolean, default: true)
* **created\_at**, **updated\_at**

### 3.3. Candidato

* **id** (uuid)
* **nome\_completo** (string)
* **cpf** (string, único, opcional se estrangeiro)
* **email** (string, único)
* **telefone** (string, opcional)
* **endereco** (rua, número, bairro, cidade, estado, CEP, país)
* **perfil\_resumido** (text)
* **texto\_apresentacao** (text, opcional)
* **linkedin\_url** (string, opcional)
* **github\_url** (string, opcional)
* **curriculo\_file\_id** (fk → FileStorage)
* **created\_at**, **updated\_at**

### 3.4. Candidatura (Application)

* **id** (uuid)
* **candidato\_id** (fk → Candidato)
* **vaga\_id** (fk → Vaga)
* **status** (enum ApplicationStatus: APPLIED, TRIAGE, TECH\_EVAL, HUMAN\_INPUT, FINAL\_DECISION)
* **applied\_at** (timestamp)
* **metadata** (jsonb)
* **created\_at**, **updated\_at**
* **constraint**: (candidato\_id, vaga\_id) deve ser único

### 3.5. Etapas da Candidatura (ApplicationStage)

* **id** (uuid)
* **application\_id** (fk → Application)
* **stage** (enum StageType: TRIAGE, TECH\_EVAL, HUMAN\_INPUT, FINAL\_DECISION)
* **status** (enum StageStatus: NOT\_STARTED, IN\_PROGRESS, WAITING, COMPLETED, FAILED)
* **started\_at**, **finished\_at** (timestamps)
* **result\_summary** (text)
* **created\_at**, **updated\_at**

### 3.6. Submissão de Teste (TestSubmission)

* **id** (uuid)
* **application\_id** (fk → Application)
* **repository\_url** (string)
* **submitted\_at** (timestamp)
* **created\_at**, **updated\_at**

### 3.7. Relatório de Entrevista (InterviewReport)

* **id** (uuid)
* **application\_id** (fk → Application)
* **entrevistador\_nome** (string)
* **data\_entrevista** (date)
* **relatorio\_markdown** (text)
* **nota** (numeric, opcional)
* **created\_at**, **updated\_at**

### 3.8. Execução de Agent (AgentRun)

* **id** (uuid)
* **application\_id** (fk → Application)
* **agent\_type** (enum AgentType: TRIAGE, CODE\_EVALUATOR, JUDGE)
* **trigger\_event** (string)
* **input\_snapshot** (jsonb)
* **output\_snapshot** (jsonb)
* **status** (enum RunStatus: PENDING, RUNNING, SUCCEEDED, FAILED)
* **score** (numeric, opcional)
* **created\_at**, **updated\_at**

### 3.9. Relatório de Agent (AgentReport)

* **id** (uuid)
* **application\_id** (fk → Application)
* **agent\_type** (enum AgentType)
* **report\_markdown** (text)
* **decision** (enum: APPROVE, REJECT, NEUTRAL)
* **score** (numeric, opcional)
* **created\_at**, **updated\_at**
* **constraint**: (application\_id, agent\_type) deve ser único

### 3.10. Armazenamento de Arquivos (FileStorage)

* **id** (uuid)
* **bucket** (string)
* **path** (string)
* **content\_type** (string)
* **size\_bytes** (bigint)
* **created\_at** (timestamp)

---

## 4. Processo Seletivo (Etapas)

1. **Aplicação**

   * O candidato se inscreve em uma vaga.
   * É criada uma `Application` com status `APPLIED`.
   * Sistema cria automaticamente um `ApplicationStage` de tipo `TRIAGE`.

2. **Triagem (Agent de Triagem)**

   * Iniciada automaticamente após a criação da candidatura.
   * O agent consome dados do candidato e da vaga.
   * Gera um relatório (`AgentReport` do tipo TRIAGE) e uma decisão prévia (APPROVE/REJECT).
   * Ao concluir, atualiza a etapa `TRIAGE` como COMPLETED.

3. **Avaliação Técnica (Agent de Teste)**

   * O candidato envia link público de repositório GitHub (`TestSubmission`).
   * O sistema inicia a etapa `TECH_EVAL`.
   * O agent executa a avaliação do código com base na `descricao_teste` da vaga e gera relatório + nota (`AgentReport` CODE\_EVALUATOR).

4. **Input Humano (Entrevista)**

   * Entrevistador cadastra `InterviewReport` vinculado à candidatura.
   * Ao salvar, atualiza `ApplicationStage(HUMAN_INPUT)` para COMPLETED.

5. **Resultado Final (Agent Juiz)**

   * Quando TRIAGE, TECH\_EVAL e HUMAN\_INPUT estiverem concluídos, o sistema dispara evento `all.inputs.ready`.
   * O Agent Juiz processa todos os dados (perfil, relatórios de agents, avaliação humana, descrição da vaga).
   * Gera relatório final (`AgentReport` JUDGE) e decisão (APPROVE, REJECT, NEUTRAL).
   * Atualiza `ApplicationStatus=FINAL_DECISION`.

---

## 5. Requisitos Funcionais

* **RF001** – O sistema deverá permitir cadastrar empresas.
* **RF002** – O sistema deverá permitir cadastrar vagas vinculadas a empresas.
* **RF003** – O sistema deverá permitir cadastrar candidatos.
* **RF004** – O candidato deverá poder se inscrever em uma vaga.
* **RF005** – O sistema deverá iniciar automaticamente a etapa de triagem após nova inscrição.
* **RF006** – O Agent de Triagem deverá gerar relatório e decisão prévia.
* **RF007** – O candidato aprovado na triagem deverá poder submeter o link do repositório do teste.
* **RF008** – O Agent de Avaliação Técnica deverá avaliar o repositório, gerar nota e relatório.
* **RF009** – O entrevistador deverá poder cadastrar relatório de entrevista e nota.
* **RF010** – Após todas as etapas concluídas, o Agent Juiz deverá gerar relatório final e decisão.
* **RF011** – O sistema deverá fornecer uma API (REST) para integração com outros sistemas.
* **RF012** – O sistema deverá gerenciar upload e armazenamento de currículos (PDF) de forma segura.

---

## 6. Requisitos Não Funcionais

* **RNF001** – Utilizar arquitetura **baseada em microserviços**.
* **RNF002** – Comunicação assíncrona entre serviços via **fila de mensagens** (RabbitMQ ou Kafka).
* **RNF003** – Persistência em **PostgreSQL**.
* **RNF004** – Deploy em **cloud** (ex.: Azure ou GCP), preferencialmente usando **containers** (Docker, Cloud Run, ou Kubernetes).
* **RNF005** – Implementar **segurança e privacidade**: criptografia de dados sensíveis (CPF, e‑mail), mascaramento em logs, armazenamento seguro para PDFs.
* **RNF006** – Estrutura modular (ex.: `CoreKit.*` + microserviços em **.NET** e **Python FastAPI**).
* **RNF007** – Disponibilizar logs e métricas por **cenário de processo seletivo** (ex.: por `application_id`).

---

## 7. Tecnologias Sugeridas

* **Backend Services**: .NET 8 (API), Python (FastAPI para agents de IA/integração com modelos)
* **Mensageria**: RabbitMQ (ou Kafka em escala maior)
* **Banco de Dados**: PostgreSQL (com schemas por tenant se necessário)
* **Infraestrutura**: Docker + Kubernetes ou Google Cloud Run
* **Autenticação**: OIDC (ex.: Azure AD, Auth0, Keycloak)
* **Front‑end**: React ou Streamlit (para dashboards internos)
* **Gerenciamento de dependências**:

  * .NET: NuGet
  * Python: Poetry
* **CI/CD**: GitHub Actions + Azure DevOps pipelines
* **Observabilidade**: Logging centralizado, métricas de CPU/memória e monitoramento de jobs

---

## 8. Premissas de Projeto

1. O cliente deverá fornecer acesso ao ambiente **SAP S/4HANA, VIM e sistemas legados**.
2. O cliente deverá disponibilizar **contas e credenciais de autenticação (OIDC/AD)** previamente.
3. O cliente deverá prover **infraestrutura em nuvem (Azure ou GCP)** já configurada para deploy dos serviços.
4. O MVP não contemplará:

   * Relatórios customizados além dos descritos.
   * Automação completa de onboarding de candidatos (apenas as etapas definidas).
   * Integrações adicionais além do **MCP DRP** e **SAP**.
5. A integração com o **Tool MCP DRP** deverá ter documentação clara e endpoints definidos pelo cliente.
6. A avaliação técnica dependerá de **repositórios públicos no GitHub** fornecidos pelo candidato.
7. O escopo inicial foca apenas em **um fluxo básico de candidatura** (sem suporte a múltiplas vagas simultâneas por candidato na mesma empresa).
8. O escopo inicial não contempla funcionalidades avançadas de analytics, relatórios customizáveis ou integração com sistemas de terceiros além dos citados.
9. O cliente deverá garantir a **qualidade e disponibilidade dos dados** enviados (ex.: currículos legíveis, links válidos).
10. A escalabilidade para alto volume será tratada em fases futuras, utilizando **Kubernetes** ou **Cloud Run** com autoescalonamento.

---

## 9. Roadmap (alto nível)

* **Fase 1 – MVP**

  * Cadastros básicos (Empresa, Vaga, Candidato)
  * Aplicação de candidatos
  * Execução automática do Agent de Triagem
  * Submissão de testes + Avaliador de Testes
  * Input humano (entrevista)
  * Relatório final (Agent Juiz)
  * API exposta (REST)
  * Armazenamento de currículos em GCS ou Azure Blob
  * Logging e auditoria básica

* **Fase 2 – Evolução**

  * Integração com sistemas de CRM do cliente
  * Portal web (React / Next.js)
  * Melhorias em UX
  * Painéis de analytics
  * Processamento distribuído com múltiplos nós (Kubernetes)

* **Fase 3 – Expansão**

  * Suporte multi‑tenant (isolamento por cliente)
  * Workflows customizáveis por empresa
  * Integrações adicionais (Slack, Teams, etc.)
  * Módulo de recomendação (matching avançado via IA)

---

## 10. Próximos Passos

* Definir prompts e fluxos de cada **Agent** (Triagem, Avaliação Técnica, Juiz)
* Criar esqueleto de projeto em **.NET + FastAPI** com suporte a mensageria e storage
* Estruturar **banco PostgreSQL** com migrations (Alembic / EF Core)
* Montar pasta `docs/` com este documento
* Iniciar desenvolvimento da **Aba Estimativas** (cronograma e esforço por grupo de tarefas)

---
