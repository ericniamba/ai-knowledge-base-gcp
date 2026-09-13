import sqlalchemy
from app.services.chat_service import _log_to_ledger, _get_last_hash, _extract_confidence


def test_first_ledger_entry_chains_to_genesis(db_engine):
    assert _get_last_hash() == "GENESIS"
    _log_to_ledger("q1", "context", "answer1", confidence=8, escalated=False)
    with db_engine.connect() as conn:
        row = conn.execute(sqlalchemy.text(
            "SELECT prev_hash FROM query_ledger ORDER BY created_at DESC LIMIT 1"
        )).fetchone()
    assert row[0] == "GENESIS"


def test_second_entry_chains_to_first_entrys_hash(db_engine):
    _log_to_ledger("q1", "context", "answer1")
    with db_engine.connect() as conn:
        first_hash = conn.execute(sqlalchemy.text(
            "SELECT record_hash FROM query_ledger ORDER BY created_at DESC LIMIT 1"
        )).fetchone()[0]

    _log_to_ledger("q2", "context", "answer2")
    with db_engine.connect() as conn:
        second_prev_hash = conn.execute(sqlalchemy.text(
            "SELECT prev_hash FROM query_ledger ORDER BY created_at DESC LIMIT 1"
        )).fetchone()[0]

    assert second_prev_hash == first_hash


def test_extract_confidence_parses_number_from_model_output():
    confidence, cleaned = _extract_confidence("ANSWER: Something.\nCONFIDENCE: 7")
    assert confidence == 7.0
    assert "CONFIDENCE" not in cleaned


def test_extract_confidence_defaults_when_missing():
    confidence, cleaned = _extract_confidence("ANSWER: No confidence line here.")
    assert confidence == 5.0
