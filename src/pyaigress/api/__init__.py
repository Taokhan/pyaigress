from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from sqlalchemy import text
from pyaigress.database.database import engine, Base
import pyaigress.database.models.models
from pyaigress.api.resolvers import chat, document, health, sessions



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        result = await conn.execute(text(
            "SELECT 1 FROM pg_extension WHERE extname = 'vector'"
        ))
        if not result.fetchone():
            raise RuntimeError("pgvector extension is not enabled. Run: CREATE EXTENSION vector;")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables ready")
    yield

    await engine.dispose()
    print("🛑 Shutdown complete")


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(sessions.router)
api_router.include_router(document.router)