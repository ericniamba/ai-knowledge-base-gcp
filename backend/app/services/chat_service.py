from app.core.config import settings
import vertexai
from vertexai.generative_models import GenerativeModel

async def get_answer(question: str, document_id: str = None) -> str:
    """Get AI answer for a question using Vertex AI"""
    try:
        vertexai.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION
        )

        model = GenerativeModel("gemini-1.5-flash-001")

        prompt = f"""You are a helpful AI assistant for a knowledge base.
        Answer the following question clearly and concisely.
        
        Question: {question}
        
        Answer:"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        return f"I encountered an error: {str(e)}"
