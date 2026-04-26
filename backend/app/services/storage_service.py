from google.cloud import storage
from app.core.config import settings
import uuid

async def upload_document(file_content: bytes, filename: str) -> str:
    """Upload document to Google Cloud Storage"""
    try:
        client = storage.Client(project=settings.GCP_PROJECT_ID)
        bucket = client.bucket(settings.GCS_BUCKET_NAME)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}-{filename}"
        blob = bucket.blob(f"documents/{unique_filename}")
        
        # Upload file
        blob.upload_from_string(
            file_content,
            content_type="application/octet-stream"
        )
        
        storage_url = f"gs://{settings.GCS_BUCKET_NAME}/documents/{unique_filename}"
        print(f"Document uploaded successfully: {storage_url}")
        return storage_url

    except Exception as e:
        print(f"Error uploading document: {str(e)}")
        raise e

async def download_document(filename: str) -> bytes:
    """Download document from Google Cloud Storage"""
    try:
        client = storage.Client(project=settings.GCP_PROJECT_ID)
        bucket = client.bucket(settings.GCS_BUCKET_NAME)
        blob = bucket.blob(f"documents/{filename}")
        return blob.download_as_bytes()

    except Exception as e:
        print(f"Error downloading document: {str(e)}")
        raise e
