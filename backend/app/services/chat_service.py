from __future__ import annotations

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Conversation, Message, EmotionRecord


async def create_conversation(db: AsyncSession, user_id: int, title: str = "新对话") -> Conversation:
    conv = Conversation(user_id=user_id, title=title)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def get_user_conversations(db: AsyncSession, user_id: int) -> list[Conversation]:
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.updated_at))
    )
    return list(result.scalars().all())


async def save_message(
    db: AsyncSession,
    conversation_id: int,
    role: str,
    content: str,
    emotion_label: str = "",
    emotion_score: float = 0.0,
) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        emotion_label=emotion_label,
        emotion_score=emotion_score,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_conversation_messages(db: AsyncSession, conversation_id: int) -> list[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id)
    )
    return list(result.scalars().all())


async def save_emotion_record(
    db: AsyncSession, user_id: int, message_id: int, label: str, score: float
) -> EmotionRecord:
    record = EmotionRecord(user_id=user_id, message_id=message_id, label=label, score=score)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_user_emotion_trends(db: AsyncSession, user_id: int, limit: int = 50) -> list[EmotionRecord]:
    result = await db.execute(
        select(EmotionRecord)
        .where(EmotionRecord.user_id == user_id)
        .order_by(desc(EmotionRecord.created_at))
        .limit(limit)
    )
    return list(result.scalars().all())
