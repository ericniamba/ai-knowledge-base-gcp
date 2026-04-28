from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GCP_PROJECT_ID: str = "project-35d5c8cd-c2c7-40ef-9e5"
    GCP_REGION: str = "us-central1"
    GCS_BUCKET_NAME: str = "ai-knowledge-base-gcp-documents"
    DATABASE_URL: str = "postgresql://kb_user:KnowledgeBase2026!@34.41.215.11:5432/knowledge_base"
    VERTEX_AI_LOCATION: str = "us-central1"
    EMBEDDING_MODEL: str = "text-embedding-004"
    LLM_MODEL: str = "gemini-1.5-flash"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Knowledge Base"

    class Config:
        env_file = ".env"

settings = Settings()
