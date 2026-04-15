from fastapi import APIRouter
from sqlalchemy import text
from pyaigress.database.database import engine
import ollama
import redis
import os

router = APIRouter(prefix="")


@router.get("/")
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

    try:
        r = redis.from_url(os.getenv("REDIS_URL"))
        r.ping()
        redis_status = True;
    except Exception as e:
        print(f"Redis error: {e}")
        redis_status = False;

    return {
        "db": "connected",
        "redis": "connected" if redis_status else "disconnected",
        "ollama": ollama_status,
        "available_models": available_models,
    }
