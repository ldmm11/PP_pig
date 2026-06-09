from pydantic import BaseModel, Field


# ===== Chat =====
class ChatRequest(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=100, description="??????")
    conversation_id: int | None = None
    message: str = Field(..., max_length=5000)


class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    emotion_label: str
    emotion_score: float


class ConversationItem(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str


class MessageItem(BaseModel):
    id: int
    role: str
    content: str
    emotion_label: str = ""
    emotion_score: float = 0.0
    created_at: str


# ===== Emotion =====
class EmotionAnalysisRequest(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., max_length=5000)


class EmotionAnalysisResponse(BaseModel):
    label: str
    score: float
    explanation: str
