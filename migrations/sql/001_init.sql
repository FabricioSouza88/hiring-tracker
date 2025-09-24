-- 001_init.sql: schema inicial para Hiring Tracker
CREATE TYPE application_status AS ENUM ('APPLIED','TRIAGE','TECH_EVAL','HUMAN_INPUT','FINAL_DECISION');
CREATE TYPE stage_type AS ENUM ('TRIAGE','TECH_EVAL','HUMAN_INPUT','FINAL_DECISION');
CREATE TYPE stage_status AS ENUM ('NOT_STARTED','IN_PROGRESS','WAITING','COMPLETED','FAILED');
CREATE TYPE agent_type AS ENUM ('TRIAGE','CODE_EVALUATOR','JUDGE');
CREATE TYPE run_status AS ENUM ('PENDING','RUNNING','SUCCEEDED','FAILED');
CREATE TYPE decision_type AS ENUM ('APPROVE','REJECT','NEUTRAL');

CREATE TABLE IF NOT EXISTS files (
  id UUID PRIMARY KEY,
  bucket TEXT NOT NULL,
  path TEXT NOT NULL,
  content_type TEXT NOT NULL,
  size_bytes BIGINT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS companies (
  id UUID PRIMARY KEY,
  trade_name TEXT NOT NULL,
  legal_name TEXT NOT NULL,
  cnpj VARCHAR(18) UNIQUE,
  website TEXT,
  phone TEXT,
  address JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  title TEXT NOT NULL,
  description TEXT,
  test_description TEXT,
  seniority TEXT,
  location_type TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS candidates (
  id UUID PRIMARY KEY,
  full_name TEXT NOT NULL,
  cpf VARCHAR(14) UNIQUE,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  address JSONB,
  profile_summary TEXT,
  presentation_text TEXT,
  linkedin_url TEXT,
  github_url TEXT,
  resume_file_id UUID REFERENCES files(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS applications (
  id UUID PRIMARY KEY,
  candidate_id UUID NOT NULL REFERENCES candidates(id),
  job_id UUID NOT NULL REFERENCES jobs(id),
  status application_status NOT NULL DEFAULT 'APPLIED',
  applied_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(candidate_id, job_id)
);

CREATE TABLE IF NOT EXISTS application_stages (
  id UUID PRIMARY KEY,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  stage stage_type NOT NULL,
  status stage_status NOT NULL DEFAULT 'NOT_STARTED',
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  result_summary TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(application_id, stage)
);

CREATE TABLE IF NOT EXISTS test_submissions (
  id UUID PRIMARY KEY,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  repository_url TEXT NOT NULL,
  submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS interview_reports (
  id UUID PRIMARY KEY,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  interviewer_name TEXT NOT NULL,
  interview_date DATE NOT NULL,
  report_markdown TEXT NOT NULL,
  rating NUMERIC(3,1),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_runs (
  id UUID PRIMARY KEY,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  agent_type agent_type NOT NULL,
  trigger_event TEXT NOT NULL,
  input_snapshot JSONB,
  output_snapshot JSONB,
  status run_status NOT NULL DEFAULT 'PENDING',
  score NUMERIC(5,2),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_reports (
  id UUID PRIMARY KEY,
  application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  agent_type agent_type NOT NULL,
  report_markdown TEXT NOT NULL,
  decision decision_type NOT NULL,
  score NUMERIC(5,2),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(application_id, agent_type)
);

CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id);
CREATE INDEX IF NOT EXISTS idx_applications_candidate ON applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_application_stages_app ON application_stages(application_id);
CREATE INDEX IF NOT EXISTS idx_agent_runs_app ON agent_runs(application_id);
CREATE INDEX IF NOT EXISTS idx_agent_reports_app ON agent_reports(application_id);
