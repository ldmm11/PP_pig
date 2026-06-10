from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.schemas import LoginRequest, TokenResponse, UserInfo
from app.services.auth_service import verify_password, create_access_token, get_user_by_username, decode_access_token
from app.api.deps import get_current_user
from app.db.database import User

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, body.username)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return TokenResponse(access_token=token, username=user.username, is_admin=bool(user.is_admin))


@router.get("/me", response_model=UserInfo)
async def get_me(user: User = Depends(get_current_user)):
    return UserInfo(id=user.id, username=user.username, nickname=user.nickname, is_admin=bool(user.is_admin))
