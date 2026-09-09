from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GCP_PROJECT_ID: str = "handsonproject-485816"
    GCP_REGION: str = "us-central1"
    GCS_BUCKET_NAME: str = "ai-knowledge-base-gcp-documents"
    DATABASE_URL: str
    VERTEX_AI_LOCATION: str = "us-central1"
    EMBEDDING_MODEL: str = "text-embedding-004"
    LLM_MODEL: str = "gemini-1.5-flash"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Knowledge Base"

    class Config:
        env_file = ".env"

settings = Settings()
