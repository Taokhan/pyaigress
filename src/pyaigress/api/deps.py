from contextlib import asynccontextmanager
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pyaigress.database.models.models import Document
import os
import uuid
import aiofiles

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def document_upload_context(
    db: AsyncSession,
    session_id: str,
    original_filename: str,
    file_content: bytes
):
    # create DB record first
    unique_filename = f"{uuid.uuid4()}_{original_filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    document = Document(
        session_id=session_id,
        filename=unique_filename,
        status="pending"
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    try:
        # save file to disk
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_content)

        yield document  # success — caller gets the document

    except Exception as e:
        # rollback — delete DB record and file if it was saved
        await db.delete(document)
        await db.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")