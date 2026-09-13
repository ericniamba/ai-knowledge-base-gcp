import os
import sys
import pytest
import sqlalchemy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS query_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    context_used TEXT,
    answer_text TEXT NOT NULL,
    record_hash VARCHAR(64) NOT NULL,
    prev_hash VARCHAR(64),
    confidence_score FLOAT,
    escalated BOOLEAN DEFAULT FALSE,
    tenant_id TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    tenant_id TEXT NOT NULL DEFAULT 'default_tenant',
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS drift_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    old_version_date TIMESTAMPTZ,
    new_version_date TIMESTAMPTZ,
    changes_summary TEXT,
    risk_level TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS pii_redaction_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pii_type TEXT NOT NULL,
    original_query_snippet TEXT,
    redacted_query TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
"""


@pytest.fixture(scope="session", autouse=True)
def _set_database_url_env():
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    os.environ.setdefault("GCP_PROJECT_ID", "test-project")
    os.environ.setdefault("VERTEX_AI_LOCATION", "us-central1")


@pytest.fixture(scope="session")
def db_engine(_set_database_url_env):
    engine = sqlalchemy.create_engine(TEST_DATABASE_URL)
    with engine.connect() as conn:
        for statement in SCHEMA_SQL.strip().split(";"):
            if statement.strip():
                conn.execute(sqlalchemy.text(statement))
        conn.commit()
    yield engine


@pytest.fixture(autouse=True)
def _clean_tables(db_engine):
    with db_engine.connect() as conn:
        for table in ["query_ledger", "documents", "drift_analysis", "pii_redaction_events"]:
            conn.execute(sqlalchemy.text(f"DELETE FROM {table}"))
        conn.commit()
    yield
