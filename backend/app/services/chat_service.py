from google.cloud import aiplatform
from app.core.config import settings
import vertexai
from vertexai.generative_models import GenerativeModel

async def get_answer(question: str, document_id: str = None) -> str:
    """Get AI answer for a question using Vertex AI"""
    try:
        # Initialize Vertex AI
        vertexai.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION
        )

        # Load Gemini model
        model = GenerativeModel("gemini-1.0-pro")

        # Create prompt
        prompt = f"""You are a helpful AI assistant for a knowledge base.
        Answer the following question based on the documents in the knowledge base.
        If you don't know the answer, say so clearly.
        
        Question: {question}
        
        Answer:"""

        # Generate response
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        return f"I encountered an error answering your question: {str(e)}"
