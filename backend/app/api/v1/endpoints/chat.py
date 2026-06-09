from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.schemas import ChatRequest, ChatResponse, ConversationItem, MessageItem
from app.services.chat_service import (
    create_conversation,
    get_device_conversations,
    save_message,
    save_emotion_record,
    get_conversation_messages,
)
from app.services.llm_service import deepseek_client

router = APIRouter(prefix="/chat", tags=["??"])


@router.post("/send", response_model=ChatResponse)
async def send_message(body: ChatRequest, db: AsyncSession = Depends(get_db)):
    conv_id = body.conversation_id
    if conv_id is None:
        conv = await create_conversation(db, body.device_id, body.message[:30])
        conv_id = conv.id

    msgs = await get_conversation_messages(db, conv_id)
    history = [{"role": m.role, "content": m.content} for m in msgs]

    reply_text, detected_label, detected_score = await deepseek_client.generate_reply(body.message, history)

    msg = await save_message(db, conv_id, "user", body.message, detected_label, detected_score)
    await save_emotion_record(db, body.device_id, msg.id, detected_label, detected_score)
    await save_message(db, conv_id, "assistant", reply_text)

    return ChatResponse(
        conversation_id=conv_id,
        reply=reply_text,
        emotion_label=detected_label,
        emotion_score=detected_score,
    )

@router.get("/conversations", response_model=list[ConversationItem])
async def list_conversations(device_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    convs = await get_device_conversations(db, device_id)
    return [
        ConversationItem(
            id=c.id,
            title=c.title,
            created_at=c.created_at.isoformat() if c.created_at else "",
            updated_at=c.updated_at.isoformat() if c.updated_at else "",
        )
        for c in convs
    ]


@router.get("/conversations/{conv_id}/messages", response_model=list[MessageItem])
async def list_messages(conv_id: int, db: AsyncSession = Depends(get_db)):
    msgs = await get_conversation_messages(db, conv_id)
    return [
        MessageItem(
            id=m.id,
            role=m.role,
            content=m.content,
            emotion_label=m.emotion_label,
            emotion_score=m.emotion_score,
            created_at=m.created_at.isoformat() if m.created_at else "",
        )
        for m in msgs
    ]
