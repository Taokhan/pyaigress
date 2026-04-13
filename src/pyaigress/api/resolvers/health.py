from fastapi import APIRouter
from sqlalchemy import text
from pyaigress.database.database import engine
import ollama

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    try:
        models = ollama.list()
        ollama_status = "connected"
        available_models = [m.model for m in models.models]
    except Exception as e:
        ollama_status = f"unreachable: {str(e)}"
        available_models = []

    return {
        "db": "connected",
        "ollama": ollama_status,
        "available_models": available_models,
    }
