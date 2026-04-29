from app.core.config import settings
from google import genai
import sqlalchemy

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

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
        return response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"I encountered an error: {str(e)}"
