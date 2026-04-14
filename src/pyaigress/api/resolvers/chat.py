from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pyaigress.ai.ai import chat, chat_stream
from pyaigress.api.models import AiTest
from typing import AsyncGenerator
from pyaigress.database.database import get_db
from pyaigress.database.memory import clear_session, get_recent_messages, save_message
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat_endpoint(req: AiTest, db: AsyncSession = Depends(get_db)):
    history = await get_recent_messages(db, req.session_id)
    messages = [{"role": m.role, "content": m.content} for m in history]

    await save_message(db, req.session_id, "user", req.text)

    reply = chat(req.text, model=req.model, history=messages)

    await save_message(db, req.session_id, "assistant", reply)
    return {"chat_reply": reply, "session_id": req.session_id}


@router.post("/stream")
async def chat_stream_endpoint(req: AiTest, db: AsyncSession = Depends(get_db)):
    history = await get_recent_messages(db, req.session_id)
    messages = [{"role": m.role, "content": m.content} for m in history]
    await save_message(db, req.session_id, "user", req.text)

    async def stream_and_save():
        full_reply = ""
        for chunk in chat_stream(req.text, model=req.model, history=messages):
            full_reply += chunk
            yield chunk
        await save_message(db, req.session_id, "assistant", full_reply)
    return StreamingResponse(stream_and_save(), media_type="text/plain")


@router.delete("/session/{session_id}")
async def clear_session_endpoint(session_id: str, db: AsyncSession = Depends(get_db)):
    await clear_session(db, session_id)
    return {"cleared": session_id}
