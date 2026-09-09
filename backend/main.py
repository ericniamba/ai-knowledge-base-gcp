from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, chat, health

app = FastAPI(
    title="FinGuard AI",
    description="AI-powered compliance intelligence for banks: audit trails, PII redaction, drift detection, and tenant isolation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "FinGuard AI - Compliance Intelligence Platform",
        "version": "1.0.0",
        "status": "running"
    }
