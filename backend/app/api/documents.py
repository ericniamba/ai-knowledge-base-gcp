from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.storage_service import upload_document
from app.services.embedding_service import process_document, get_embeddings
import sqlalchemy
from app.core.config import settings

router = APIRouter()

engine = sqlalchemy.create_engine(settings.DATABASE_URL)

@router.post("/documents/upload")
async def upload_document_endpoint(file: UploadFile = File(...)):
    """Upload a document to the knowledge base"""
    try:
        if not file.filename.endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT and DOCX files are supported"
            )

        file_content = await file.read()

        # Upload to Cloud Storage
        storage_url = await upload_document(
            file_content=file_content,
            filename=file.filename
        )

        # Process document into chunks
        chunks = await process_document(
            filename=file.filename,
            file_content=file_content
        )

        # Store each chunk with embeddings in database
        with engine.connect() as conn:
            for chunk in chunks:
                try:
                    embedding = await get_embeddings(chunk)
                    conn.execute(
                        sqlalchemy.text(
                            "INSERT INTO documents (filename, content, embedding) "
                            "VALUES (:filename, :content, :embedding)"
                        ),
                        {
                            "filename": file.filename,
                            "content": chunk,
                            "embedding": str(embedding)
                        }
                    )
                except Exception as e:
                    print(f"Error storing chunk: {str(e)}")
            conn.commit()

        return JSONResponse(content={
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "chunks": len(chunks),
            "storage_url": storage_url,
            "status": "processed"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                sqlalchemy.text(
                    "SELECT DISTINCT filename, COUNT(*) as chunks, "
                    "MAX(created_at) as uploaded_at "
                    "FROM documents GROUP BY filename"
                )
            )
            docs = [
                {
                    "filename": row[0],
                    "chunks": row[1],
                    "uploaded_at": str(row[2])
                }
                for row in result
            ]
        return {"documents": docs, "total": len(docs)}
    except Exception as e:
        return {"documents": [], "total": 0}
