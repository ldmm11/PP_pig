from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.db.database import init_db, async_session_factory
from app.services.auth_service import init_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session_factory() as db:
        await init_admin_user(db)
    yield


app = FastAPI(title="PP_pig", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
