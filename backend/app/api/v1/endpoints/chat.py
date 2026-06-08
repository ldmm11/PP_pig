from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import decode_access_token
from app.db.database import get_db, User
from app.schemas.schemas import ChatRequest, ChatResponse, ConversationItem, MessageItem
from app.services.chat_service import (
    create_conversation,
    get_user_conversations,
    save_message,
    get_conversation_messages,
)
from app.services.llm_service import deepseek_client
from app.ws.manager import ConnectionManager

router = APIRouter(prefix="/chat", tags=["对话"])
ws_manager = ConnectionManager()


@router.post("/send", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv_id = body.conversation_id
    if conv_id is None:
        conv = await create_conversation(db, user.id, body.message[:30])
        conv_id = conv.id

    # 1. 情绪分析
    emotion = await deepseek_client.analyze_emotion(body.message)

    # 2. 保存用户消息
    await save_message(db, conv_id, "user", body.message, emotion["label"], emotion["score"])

    # 3. 获取历史消息
    msgs = await get_conversation_messages(db, conv_id)
    history = [{"role": m.role, "content": m.content} for m in msgs[:-1]]  # 除去刚保存的最后一条用于构建上下文

    # 4. 生成回复
    reply_text = await deepseek_client.generate_reply(
        body.message, emotion["label"], emotion["score"], history
    )

    # 5. 保存回复
    reply_msg = await save_message(db, conv_id, "assistant", reply_text)

    return ChatResponse(
        conversation_id=conv_id,
        reply=reply_text,
        emotion_label=emotion["label"],
        emotion_score=emotion["score"],
    )


@router.get("/conversations", response_model=list[ConversationItem])
async def list_conversations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    convs = await get_user_conversations(db, user.id)
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
async def list_messages(
    conv_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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


@router.websocket("/ws/{token}")
async def chat_websocket(websocket: WebSocket, token: str):
    payload = decode_access_token(token)
    if payload is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user_id = int(payload["sub"])
    await ws_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            # 简化处理：WebSocket 只做推送，具体消息走 REST
            pass
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)
