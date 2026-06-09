from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.schemas import EmotionAnalysisRequest, EmotionAnalysisResponse
from app.services.llm_service import deepseek_client
from app.services.chat_service import get_device_emotion_trends

router = APIRouter(prefix="/emotion", tags=["情绪分析"])


@router.post("/analyze", response_model=EmotionAnalysisResponse)
async def analyze_emotion(body: EmotionAnalysisRequest):
    reply_text, detected_label, detected_score = await deepseek_client.generate_reply(body.text)
    return EmotionAnalysisResponse(
        label=detected_label,
        score=detected_score,
        explanation=reply_text[:50],
    )


@router.get("/trends")
async def emotion_trends(device_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    records = await get_device_emotion_trends(db, device_id)
    return [
        {
            "id": r.id,
            "label": r.label,
            "score": r.score,
            "created_at": r.created_at.isoformat() if r.created_at else "",
        }
        for r in records
    ]
