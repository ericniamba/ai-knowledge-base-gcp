from google.cloud import aiplatform
from app.core.config import settings
from pypdf import PdfReader
import io

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        raise e

def chunk_text(text: str, chunk_size: int = 1000) -> list:
    """Split text into chunks for embedding"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        current_chunk.append(word)
        current_size += len(word)
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

async def process_document(filename: str, file_content: bytes):
    """Process document and create embeddings"""
    try:
        # Initialize Vertex AI
        aiplatform.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.VERTEX_AI_LOCATION
        )

        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
        else:
            text = file_content.decode('utf-8')

        # Chunk the text
        chunks = chunk_text(text)
        print(f"Document processed into {len(chunks)} chunks")

        return chunks

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        raise e
