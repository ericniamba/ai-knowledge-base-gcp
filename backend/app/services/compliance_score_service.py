from app.core.config import settings
import sqlalchemy

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

RISK_WEIGHTS = {"LOW": 1, "MEDIUM": 5, "HIGH": 10}

def get_compliance_trend():
    sql = "SELECT filename, risk_level, created_at FROM drift_analysis ORDER BY created_at ASC"
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))
        rows = result.fetchall()

    trend = []
    running_total = 0
    for filename, risk_level, created_at in rows:
        weight = RISK_WEIGHTS.get(risk_level, 0)
        running_total += weight
        trend.append({
            "date": str(created_at),
            "filename": filename,
            "risk_level": risk_level,
            "event_score": weight,
            "cumulative_risk_score": running_total
        })
    return trend
