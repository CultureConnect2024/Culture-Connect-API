from fastapi import APIRouter, Depends
from app.src.handlers.check_handlers import test_db_connection
from app.database import get_db
from sqlalchemy.orm import Session
router = APIRouter()

@router.get("/")
async def healthcheck_route(db: Session = Depends(get_db)):
    return await test_db_connection(db)
