from app.core.config import settings
from google import genai

async def get_answer(question: str, document_id: str = None) -> str:
    """Get AI answer for a question using Gemini"""
    try:
        client = genai.Client(
            vertexai=True,
            project=settings.GCP_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION
        )

        prompt = f"""You are a helpful AI assistant for a knowledge base.
        Answer the following question clearly and concisely.
        
        Question: {question}
        
        Answer:"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        return f"I encountered an error: {str(e)}"
