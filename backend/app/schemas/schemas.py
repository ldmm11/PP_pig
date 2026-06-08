from pydantic import BaseModel, Field


# ===== Auth =====
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    nickname: str = ""


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str


# ===== Chat =====
class ChatRequest(BaseModel):
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
    text: str = Field(..., max_length=5000)


class EmotionAnalysisResponse(BaseModel):
    label: str
    score: float
    explanation: str
