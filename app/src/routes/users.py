from app.src.handlers.user_handlers import get_user_by_session, get_all_users
from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/{session_id}")
async def get_user(session_id: str, db: AsyncSession = Depends(get_db)):
    return await get_user_by_session(session_id, db)

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)