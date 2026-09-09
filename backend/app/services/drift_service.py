from app.core.config import settings
import sqlalchemy

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

def get_document_versions(filename: str):
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT content, created_at FROM documents WHERE filename = :fn ORDER BY created_at ASC"), {"fn": filename})
        rows = result.fetchall()
    return rows

def analyze_drift(filename: str):
    versions = get_document_versions(filename)
    if len(versions) < 2:
        return {"error": "Need at least 2 versions of this document to compare"}

    old_content, old_date = versions[0]
    new_content, new_date = versions[-1]

    old_words = set(old_content.lower().split())
    new_words = set(new_content.lower().split())
    added = new_words - old_words
    removed = old_words - new_words

    changes_summary = "Added terms: " + ", ".join(sorted(added)) + " | Removed terms: " + ", ".join(sorted(removed))

    risk_level = "LOW"
    risk_keywords = {"must", "required", "prohibited", "penalty", "deadline", "due", "enhanced"}
    if added & risk_keywords:
        risk_level = "HIGH"
    elif added or removed:
        risk_level = "MEDIUM"

    insert_sql = "INSERT INTO drift_analysis (filename, old_version_date, new_version_date, changes_summary, risk_level) VALUES (:fn, :od, :nd, :cs, :rl)"
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(insert_sql), {"fn": filename, "od": old_date, "nd": new_date, "cs": changes_summary, "rl": risk_level})
        conn.commit()

    return {
        "filename": filename,
        "old_date": str(old_date),
        "new_date": str(new_date),
        "changes_summary": changes_summary,
        "risk_level": risk_level
    }
