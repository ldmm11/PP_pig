from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.database import get_db, User
from app.schemas.schemas import EmotionAnalysisRequest, EmotionAnalysisResponse
from app.services.llm_service import deepseek_client
from app.services.chat_service import save_emotion_record, get_user_emotion_trends

router = APIRouter(prefix="/emotion", tags=["情绪分析"])


@router.post("/analyze", response_model=EmotionAnalysisResponse)
async def analyze_emotion(
    body: EmotionAnalysisRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    emotion = await deepseek_client.analyze_emotion(body.text)
    return EmotionAnalysisResponse(
        label=emotion["label"],
        score=emotion["score"],
        explanation=emotion["explanation"],
    )


@router.get("/trends")
async def emotion_trends(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    records = await get_user_emotion_trends(db, user.id)
    return [
        {
            "id": r.id,
            "label": r.label,
            "score": r.score,
            "created_at": r.created_at.isoformat() if r.created_at else "",
        }
        for r in records
    ]
