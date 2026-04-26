from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import get_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    document_id: str = None

class ChatResponse(BaseModel):
    answer: str
    sources: list = []
    status: str = "success"

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Ask a question about your documents"""
    try:
        if not request.question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        answer = await get_answer(
            question=request.question,
            document_id=request.document_id
        )

        return ChatResponse(
            answer=answer,
            sources=[],
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
async def get_chat_history():
    """Get chat history"""
    return {
        "history": [],
        "total": 0
    }
