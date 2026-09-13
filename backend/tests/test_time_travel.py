import sqlalchemy
from app.services.time_travel_service import compare_time_travel


def _insert_document(db_engine, filename, content, created_at):
    with db_engine.connect() as conn:
        conn.execute(sqlalchemy.text(
            "INSERT INTO documents (filename, content, created_at) VALUES (:fn, :c, :d)"
        ), {"fn": filename, "c": content, "d": created_at})
        conn.commit()


def test_returns_different_versions_for_different_dates(db_engine):
    _insert_document(db_engine, "aml.txt", "Threshold is 10000 dollars.", "2025-01-01")
    _insert_document(db_engine, "aml.txt", "Threshold is 5000 dollars.", "2026-06-01")
    result = compare_time_travel("aml.txt", "2025-06-01", "2026-08-01")
    assert result["same_version"] is False
    assert "10000" in result["content_a"]
    assert "5000" in result["content_b"]
