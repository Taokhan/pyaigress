from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pyaigress.api.deps import document_upload_context
from pyaigress.database.database import get_db
from pyaigress.database.models.models import Document, Session
from arq import create_pool
from arq.connections import RedisSettings
import os

router = APIRouter(prefix="/sessions/{session_id}/documents", tags=["documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_redis():
    return await create_pool(RedisSettings.from_dsn(os.environ["REDIS_URL"]))

@router.post("")
async def upload_document(
    session_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # verify session exists
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")

    content = await file.read()

    async with document_upload_context(db, session_id, file.filename, content) as document:
        # only runs if file saved and DB record created successfully
        redis = await get_redis()
        await redis.enqueue_job("process_document", document.id)
        await redis.aclose()

    return {
        "document_id": document.id,
        "filename": file.filename,
        "status": "pending",
        "message": "Document uploaded and queued for processing"
    }

@router.get("")
async def list_documents(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).where(Document.session_id == session_id)
    )
    documents = result.scalars().all()
    return {"documents": [
        {
            "document_id": d.id,
            "filename": d.filename,
            "status": d.status,
            "created_at": d.created_at
        } for d in documents
    ]}

@router.get("/{document_id}/status")
async def document_status(session_id: str, document_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.session_id == session_id
        )
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document_id": document.id, "status": document.status}