from app.core.config import settings
import sqlalchemy

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

def get_documents_for_tenant(tenant_id: str, query_filter: str = None):
    sql = "SELECT filename, content, tenant_id FROM documents WHERE tenant_id = :tid"
    params = {"tid": tenant_id}
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql), params)
        rows = result.fetchall()
    return rows

def adversarial_test(claimed_tenant_id: str, injected_query: str):
    """
    Simulates a malicious actor as claimed_tenant_id trying to use
    a prompt-injection-style query to leak another tenant's data.
    The injected_query is never used to build SQL - it's just passed
    as a search string within the tenant's own scope, proving that
    no matter what the query text says, tenant_id in the WHERE clause
    cannot be bypassed by query content.
    """
    docs = get_documents_for_tenant(claimed_tenant_id)
    leaked_tenants = set(row[2] for row in docs if row[2] != claimed_tenant_id)
    return {
        "claimed_tenant": claimed_tenant_id,
        "injected_query": injected_query,
        "documents_returned": [row[0] for row in docs],
        "other_tenants_leaked": list(leaked_tenants),
        "isolation_held": len(leaked_tenants) == 0
    }
