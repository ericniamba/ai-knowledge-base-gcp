import sqlalchemy
from app.services.drift_service import analyze_drift


def _insert_document(db_engine, filename, content, created_at):
    with db_engine.connect() as conn:
        conn.execute(sqlalchemy.text(
            "INSERT INTO documents (filename, content, created_at) VALUES (:fn, :c, :d)"
        ), {"fn": filename, "c": content, "d": created_at})
        conn.commit()


def test_flags_high_risk_when_regulatory_keyword_added(db_engine):
    _insert_document(db_engine, "policy.txt", "Report transactions over 10000 dollars.", "2025-01-01")
    _insert_document(db_engine, "policy.txt", "Report transactions over 5000 dollars and undergo enhanced review.", "2026-01-01")

    result = analyze_drift("policy.txt")
    assert result["risk_level"] == "HIGH"
    assert "enhanced" in result["changes_summary"]


def test_low_risk_when_no_keywords_changed(db_engine):
    _insert_document(db_engine, "policy2.txt", "The office is open Monday through Friday.", "2025-01-01")
    _insert_document(db_engine, "policy2.txt", "The office is open Monday through Saturday.", "2026-01-01")

    result = analyze_drift("policy2.txt")
    assert result["risk_level"] in ("LOW", "MEDIUM")


def test_error_when_only_one_version_exists(db_engine):
    _insert_document(db_engine, "onlyone.txt", "Just one version.", "2025-01-01")
    result = analyze_drift("onlyone.txt")
    assert "error" in result
