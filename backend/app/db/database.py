from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_size=10, max_overflow=20)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    """??? - ? device_id ??"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, index=True, comment="??????")
    title = Column(String(200), default="???")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Message(Base):
    """??? - ??????????????"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False, index=True)
    role = Column(String(20), nullable=False, comment="user / assistant")
    content = Column(Text, nullable=False)
    emotion_label = Column(String(50), default="", comment="????: happy/aggrieved/irritated/anxious/lonely/tired/angry/calm")
    emotion_score = Column(Float, default=0.0, comment="???? 0-1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmotionRecord(Base):
    """????? - ??????"""
    __tablename__ = "emotion_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, index=True)
    message_id = Column(Integer, nullable=False)
    label = Column(String(50), nullable=False)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
