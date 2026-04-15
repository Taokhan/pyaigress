from pyaigress.database.database import AsyncSessionLocal
from pyaigress.database.models.models import Document, DocumentChunk
from pyaigress.ai.ai import embed
from sqlalchemy import select
import PyPDF2
import os

UPLOAD_DIR = "uploads"


async def process_document(ctx, document_id: int):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Document).where(Document.id == document_id))
        document = result.scalar_one_or_none()

        if not document:
            return

        try:
            document.status = "processing"
            await db.commit()

            file_path = os.path.join(UPLOAD_DIR, document.filename)
            text = ""

            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            chunks = chunk_text(text, chunk_size=500, overlap=50)

            for chunk in chunks:
                embeddings = embed(chunk)
                documentChunk = DocumentChunk(
                    document_id=document.id,
                    session_id=document.session_id,
                    content=chunk,
                    embeddings=embeddings,
                )
                db.add(documentChunk)

            document.status = "ready"
            await db.commit()
            print(f"✅ Document {document_id} processed — {len(chunks)} chunks")
        except Exception as e:
            document.status = "failed"
            await db.commit()
            print(f"❌ Document {document_id} failed: {e}")
            raise


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]
