from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # GCP Settings
    GCP_PROJECT_ID: str = "project-35d5c8cd-c2c7-40ef-9e5"
    GCP_REGION: str = "us-central1"
    GCS_BUCKET_NAME: str = "ai-knowledge-base-gcp-documents"
    
    # Database Settings
    DATABASE_URL: str = ""
    
    # Vertex AI Settings
    VERTEX_AI_LOCATION: str = "us-central1"
    EMBEDDING_MODEL: str = "textembedding-gecko@003"
    LLM_MODEL: str = "gemini-1.0-pro"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Knowledge Base"

    class Config:
        env_file = ".env"

settings = Settings()
