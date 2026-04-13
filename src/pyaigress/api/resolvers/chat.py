from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pyaigress.ai.ai import chat, chat_stream
from pyaigress.api.models import AiTest
from typing import AsyncGenerator


router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
def chat_endpoint(req: AiTest):
    reply = chat(req.text, model=req.model)
    return {"chat_reply": reply}



async def event_generator(message: str, model: str):
    for chunk in chat_stream(message, model=model):
        yield f"data: {chunk}\n\n"


@router.post("/stream")
def chat_stream_endpoint(req: AiTest):
    return StreamingResponse(
        event_generator(req.text, model=req.model),
        media_type="text/plain"
    )