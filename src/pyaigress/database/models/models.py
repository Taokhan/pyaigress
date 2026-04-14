from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from pyaigress.database.database import Base

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list] = mapped_column(Vector(768))

class Message(Base):
    __tablename__="messages"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64),index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list] = mapped_column(Vector(768))
    created_at: Mapped[DateTime] = mapped_column(DateTime,server_default=func.now())