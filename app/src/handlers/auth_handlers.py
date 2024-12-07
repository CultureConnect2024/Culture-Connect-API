from fastapi import HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.database import get_db
from app.src.models.model import User, Session
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import uuid
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify the user's password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Function to hash a new password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Handler for user registration

async def register_user(
    username: str,
    email: str,
    password: str,
    db: AsyncSession  # Directly inject AsyncSession
):
    hashed_password = hash_password(password)
    
    # Check if the user already exists
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create and add the new user
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)
    await db.commit()

    # Generate session ID (UUID)
    session_id = str(uuid.uuid4())

    # Tentukan waktu kadaluarsa sesi (misalnya 1 jam)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    # Simpan session baru ke tabel sessions
    session = Session(
        session_id=session_id,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(session)
    await db.commit()

    # Return response dengan session_id
    return {
        "message": "User successfully registered",
        "session_id": session_id,
        "expires_at": expires_at.isoformat()
    }



async def login_user(username: str, password: str, db: AsyncSession):
    """
    Endpoint untuk login pengguna.
    Menerima username dan password sebagai input, lalu mengembalikan session ID.
    """
    # Query user berdasarkan username
    db_user = await db.execute(select(User).filter(User.username == username))
    user = db_user.scalars().first()

    # Validasi username dan password
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

  
    session_id = str(uuid.uuid4())

      
    now_utc = datetime.now(ZoneInfo("UTC"))

    # Convert to Jakarta time (UTC+7)
    now_jakarta = now_utc.astimezone(ZoneInfo("Asia/Jakarta"))

    
    expires_at = now_jakarta + timedelta(hours=24)


    # Simpan session baru ke tabel sessions
    session = Session(
        session_id=session_id,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(session)
    await db.commit()

    # Return session ID dan waktu kadaluarsa sesi ke aplikasi
    return {
        "status" : "success",
        "message": "Login successful",
        "session_id": session_id,
        "expires_at": expires_at.isoformat()
    }

# Handler for user logout
async def logout_user(session_id: str, db: AsyncSession):
    """
    Endpoint to log out the user.
    It will remove the session from the database using the session_id.
    """
    # Query the session based on the session_id
    db_session = await db.execute(select(Session).filter(Session.session_id == session_id))
    session = db_session.scalars().first()

    # If session does not exist or session ID is invalid, raise error
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Remove the session from the database
    await db.delete(session)
    await db.commit()

    return {"message": "Logged out successfully"}