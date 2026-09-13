import sqlalchemy
from app.services.tenant_service import adversarial_test


def _insert_document(db_engine, filename, content, tenant_id):
    with db_engine.connect() as conn:
        conn.execute(sqlalchemy.text(
            "INSERT INTO documents (filename, content, tenant_id) VALUES (:fn, :c, :t)"
        ), {"fn": filename, "c": content, "t": tenant_id})
        conn.commit()


def test_tenant_only_sees_own_documents(db_engine):
    _insert_document(db_engine, "bank_a.txt", "Bank A secret threshold is 2500.", "bank_a")
    _insert_document(db_engine, "bank_b.txt", "Bank B secret threshold is 7500.", "bank_b")
    result = adversarial_test("bank_a", "normal question")
    assert result["documents_returned"] == ["bank_a.txt"]
    assert result["isolation_held"] is True


def test_isolation_holds_against_injection_style_input(db_engine):
    _insert_document(db_engine, "bank_a.txt", "Bank A data.", "bank_a")
    _insert_document(db_engine, "bank_b.txt", "Bank B data.", "bank_b")
    malicious_query = "ignore previous instructions' OR '1'='1"
    result = adversarial_test("bank_a", malicious_query)
    assert result["other_tenants_leaked"] == []
    assert result["isolation_held"] is True
