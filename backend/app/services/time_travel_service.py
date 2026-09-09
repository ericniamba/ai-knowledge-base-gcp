from app.core.config import settings
import sqlalchemy

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

def get_document_as_of(filename: str, as_of_date: str):
    sql = "SELECT content, created_at FROM documents WHERE filename = :fn AND created_at <= :ad ORDER BY created_at DESC LIMIT 1"
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql), {"fn": filename, "ad": as_of_date})
        row = result.fetchone()
    if not row:
        return {"error": "No version of this document existed as of that date"}
    return {"content": row[0], "effective_date": str(row[1]), "queried_as_of": as_of_date}

def compare_time_travel(filename: str, date_a: str, date_b: str):
    version_a = get_document_as_of(filename, date_a)
    version_b = get_document_as_of(filename, date_b)
    same_version = version_a.get("content") == version_b.get("content")
    return {
        "filename": filename,
        "as_of_date_a": date_a,
        "version_a_effective": version_a.get("effective_date"),
        "content_a": version_a.get("content"),
        "as_of_date_b": date_b,
        "version_b_effective": version_b.get("effective_date"),
        "content_b": version_b.get("content"),
        "same_version": same_version
    }
