from app.services.pii_redaction_service import redact_pii


def test_detects_and_redacts_ssn(db_engine):
    result = redact_pii("My SSN is 123-45-6789, please help.")
    assert result["was_redacted"] is True
    assert "SSN" in result["pii_detected"]
    assert "123-45-6789" not in result["redacted"]
    assert "[SSN_REDACTED]" in result["redacted"]


def test_detects_and_redacts_email(db_engine):
    result = redact_pii("Contact me at john.doe@bank.com please.")
    assert "EMAIL" in result["pii_detected"]
    assert "john.doe@bank.com" not in result["redacted"]


def test_detects_multiple_pii_types_in_one_message(db_engine):
    text = "SSN 123-45-6789 and card 4111 1111 1111 1111, email me at a@b.com"
    result = redact_pii(text)
    assert "SSN" in result["pii_detected"]
    assert "CREDIT_CARD" in result["pii_detected"]
    assert "EMAIL" in result["pii_detected"]


def test_clean_text_is_not_flagged(db_engine):
    result = redact_pii("What is our compliance policy on reporting thresholds?")
    assert result["was_redacted"] is False
    assert result["pii_detected"] == []
    assert result["redacted"] == result["original"]


def test_redaction_event_is_logged_to_database(db_engine):
    redact_pii("My SSN is 987-65-4321")
    with db_engine.connect() as conn:
        import sqlalchemy
        rows = conn.execute(sqlalchemy.text(
            "SELECT pii_type FROM pii_redaction_events"
        )).fetchall()
    assert len(rows) >= 1
    assert rows[0][0] == "SSN"
