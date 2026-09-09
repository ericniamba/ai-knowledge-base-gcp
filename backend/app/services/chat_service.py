from app.core.config import settings
from google import genai
import sqlalchemy
import hashlib
import re

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

def _get_last_hash() -> str:
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(
            "SELECT record_hash FROM query_ledger ORDER BY created_at DESC LIMIT 1"
        ))
        row = result.fetchone()
        return row[0] if row else "GENESIS"

def _log_to_ledger(question: str, context: str, answer: str, confidence: float = None, escalated: bool = False):
    prev_hash = _get_last_hash()
    raw = f"{question}|{context}|{answer}|{prev_hash}"
    record_hash = hashlib.sha256(raw.encode()).hexdigest()
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("""
            INSERT INTO query_ledger (query_text, context_used, answer_text, record_hash, prev_hash, confidence_score, escalated)
            VALUES (:q, :c, :a, :rh, :ph, :conf, :esc)
        """), {"q": question, "c": context, "a": answer, "rh": record_hash, "ph": prev_hash, "conf": confidence, "esc": escalated})
        conn.commit()

def _extract_confidence(text: str):
    match = re.search(r"CONFIDENCE:\s*(\d+)", text)
    confidence = float(match.group(1)) if match else 5.0
    cleaned = re.sub(r"CONFIDENCE:\s*\d+", "", text).strip()
    return confidence, cleaned

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
            prompt = "You are a compliance-focused AI assistant. You have access to these documents: " + context + "\n\nAnswer the question using ONLY the documents above. If the documents don't contain enough information to answer confidently, say so explicitly.\n\nQuestion: " + question + "\n\nRespond in this exact format:\nANSWER: <your answer>\nCONFIDENCE: <a number from 1-10>"
        else:
            prompt = "No documents were found for this query.\n\nQuestion: " + question + "\n\nRespond in this exact format:\nANSWER: I don't have relevant documents to answer this question confidently.\nCONFIDENCE: 1"

        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_text = response.text
        confidence, answer = _extract_confidence(raw_text)

        ESCALATION_THRESHOLD = 5.0
        escalated = confidence < ESCALATION_THRESHOLD

        if escalated:
            final_answer = "Low confidence (" + str(confidence) + "/10) - flagging for human compliance review rather than guessing.\n\nPreliminary answer: " + answer
        else:
            final_answer = answer

        _log_to_ledger(question, context, final_answer, confidence, escalated)
        return final_answer
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"I encountered an error: {str(e)}"
