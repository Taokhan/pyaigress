from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pyaigress.database.models.models import Message
from pyaigress.ai.ai import embed


async def save_message(db: AsyncSession,session_id: str,role:str,content:str):
    embedding = embed(content)
    msg = Message(
        session_id=session_id,
        role=role,
        content=content,
        embedding=embedding
    )
    db.add(msg)
    await db.commit()

async def get_recent_messages(db: AsyncSession,session_id: str,limit: int = 10):
    result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()

    return list(reversed(messages))

async def get_similar_messages(db: AsyncSession, session_id: str, query: str, limit: int = 5):
    query_embedding = embed(query)
    result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    return result.scalars().all()

async def clear_session(db: AsyncSession, session_id: str):
    await db.execute(delete(Message).where(Message.session_id == session_id))
    await db.commit()