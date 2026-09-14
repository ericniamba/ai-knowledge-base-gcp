import sqlalchemy
from app.services.compliance_score_service import get_compliance_trend


def _insert_drift_event(db_engine, filename, risk_level, created_at):
    with db_engine.connect() as conn:
        conn.execute(sqlalchemy.text(
            "INSERT INTO drift_analysis (filename, risk_level, created_at) VALUES (:fn, :r, :d)"
        ), {"fn": filename, "r": risk_level, "d": created_at})
        conn.commit()


def test_cumulative_score_increases_with_each_event(db_engine):
    _insert_drift_event(db_engine, "policy1.txt", "LOW", "2025-01-01")
    _insert_drift_event(db_engine, "policy2.txt", "HIGH", "2025-06-01")

    trend = get_compliance_trend()

    assert len(trend) == 2
    assert trend[0]["cumulative_risk_score"] == 1
    assert trend[1]["cumulative_risk_score"] == 11


def test_empty_when_no_drift_events(db_engine):
    trend = get_compliance_trend()
    assert trend == []


def test_high_risk_weighted_more_than_low_risk(db_engine):
    _insert_drift_event(db_engine, "a.txt", "LOW", "2025-01-01")
    _insert_drift_event(db_engine, "b.txt", "HIGH", "2025-02-01")

    trend = get_compliance_trend()

    low_event = trend[0]
    high_event = trend[1]
    assert high_event["event_score"] > low_event["event_score"]
