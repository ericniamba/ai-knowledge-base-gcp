from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.storage_service import upload_document
from app.services.embedding_service import process_document

router = APIRouter()

@router.post("/documents/upload")
async def upload_document_endpoint(file: UploadFile = File(...)):
    """Upload a document to the knowledge base"""
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT and DOCX files are supported"
            )

        # Upload to Cloud Storage
        file_content = await file.read()
        storage_url = await upload_document(
            file_content=file_content,
            filename=file.filename
        )

        # Process document and create embeddings
        await process_document(
            filename=file.filename,
            file_content=file_content
        )

        return JSONResponse(content={
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "storage_url": storage_url,
            "status": "processed"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    return {
        "documents": [],
        "total": 0,
        "message": "Knowledge base is ready"
    }
