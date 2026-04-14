from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pyaigress.database.database import get_db
from pyaigress.database.models.models import Session
import uuid



router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("")
async def create_session(db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())
    session = Session(session_id=session_id)
    db.add(session)
    await db.commit
    return {"session_id": session_id}

@router.get("")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).order_by(Session.created_at.desc()))
    sessions = result.scalars().all()
    return {
        "sessions": [
            {"session_id": s.session_id , "created_at": s.created_at} for s in sessions
        ]
    }

@router.delete("/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await db.execute(delete(Session).where(Session.session_id == session_id))
    await db.commit()
    return {"deleted": session_id}