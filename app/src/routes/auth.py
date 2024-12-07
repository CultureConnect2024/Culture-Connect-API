from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.src.handlers.auth_handlers import register_user, login_user, logout_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
router = APIRouter()

# Route for user registration

@router.post("/register")
async def register(request: Request, db: AsyncSession = Depends(get_db)):
    request_data = await request.json()
    username = request_data['username']
    email = request_data['email']
    password = request_data['password']
    return await register_user(username, email, password, db)


# Route for user login
@router.post("/login")
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    request_data = await request.json()
    username = request_data['username']
    password = request_data['password']
    return await login_user(username, password, db)


# Route for user logout
@router.post("/logout")
async def logout(request: Request, db: AsyncSession = Depends(get_db)):
    request_data = await request.json()
    session_id = request_data['session-id']
    return await logout_user(session_id,db)
