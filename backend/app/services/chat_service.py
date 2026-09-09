from app.core.config import settings
from google import genai
import sqlalchemy
import hashlib

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

def _get_last_hash() -> str:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(
            "SELECT record_hash FROM query_ledger ORDER BY created_at DESC LIMIT 1"
        ))
        row = result.fetchone()
        return row[0] if row else "GENESIS"

def _log_to_ledger(question: str, context: str, answer: str):
    prev_hash = _get_last_hash()
    raw = f"{question}|{context}|{answer}|{prev_hash}"
    record_hash = hashlib.sha256(raw.encode()).hexdigest()
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("""
            INSERT INTO query_ledger (query_text, context_used, answer_text, record_hash, prev_hash)
            VALUES (:q, :c, :a, :rh, :ph)
        """), {"q": question, "c": context, "a": answer, "rh": record_hash, "ph": prev_hash})
        conn.commit()

async def get_answer(question: str, document_id: str = None) -> str:
    try:
        client = genai.Client(
            vertexai=True,
            project=settings.GCP_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION
        )
        context = ""
        try:
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text("SELECT content FROM documents ORDER BY created_at DESC LIMIT 5"))
                chunks = [row[0] for row in result]
                if chunks:
                    context = "\n\n".join(chunks)
        except Exception as e:
            print(f"Could not fetch context: {str(e)}")
        if context:
            prompt = f"You are a helpful AI assistant. You have access to these documents: {context}\n\nUse the documents if relevant, otherwise use general knowledge.\n\nQuestion: {question}\n\nAnswer:"
        else:
            prompt = f"You are a helpful AI assistant. Answer this question clearly: {question}"
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        answer = response.text
        _log_to_ledger(question, context, answer)
        return answer
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"I encountered an error: {str(e)}"
