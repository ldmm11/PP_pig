from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.db.database import get_db, User
from app.schemas.schemas import (
    LoginRequest,
    RegisterRequest,
    Token,
    UserInfo,
)

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=Token)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == body.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user = User(
        username=body.username,
        hashed_password=hash_password(body.password),
        nickname=body.nickname or body.username,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == body.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserInfo)
async def get_me(user: User = Depends(get_current_user)):
    return UserInfo(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
    )
