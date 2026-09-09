from app.core.config import settings
import sqlalchemy
import re

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

PII_PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
    "BANK_ACCOUNT": re.compile(r"\b\d{8,17}\b"),
    "ROUTING_NUMBER": re.compile(r"\b\d{9}\b"),
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
}

def _log_redaction(pii_type: str, original_snippet: str, redacted_text: str):
    sql = "INSERT INTO pii_redaction_events (pii_type, original_query_snippet, redacted_query) VALUES (:pt, :os, :rt)"
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(sql), {"pt": pii_type, "os": original_snippet, "rt": redacted_text})
        conn.commit()

def redact_pii(text: str):
    redacted_text = text
    detected_types = []

    for pii_type, pattern in PII_PATTERNS.items():
        matches = pattern.findall(redacted_text)
        if matches:
            detected_types.append(pii_type)
            redacted_text = pattern.sub("[" + pii_type + "_REDACTED]", redacted_text)

    if detected_types:
        for pii_type in detected_types:
            _log_redaction(pii_type, text[:50], redacted_text[:50])

    return {
        "original": text,
        "redacted": redacted_text,
        "pii_detected": detected_types,
        "was_redacted": len(detected_types) > 0
    }
