from fastapi import HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.database import get_db
from app.src.models.model import User, Session
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
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
    db: AsyncSession  
):
    hashed_password = hash_password(password)

    # Cek apakah username sudah terdaftar
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if user:
      
        return JSONResponse(
            status_code=400,  
            content={
                "status": "error",
                "message": "Username already registered",
                "time": datetime.now(timezone.utc).isoformat()
            }
        )

    # Membuat user baru
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)

    try:
        # Menyimpan user baru
        await db.commit()

        # Membuat session baru
        session_id = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        expires_at_naive = expires_at.replace(tzinfo=None)

        session = Session(
            session_id=session_id,
            user_id=user.id,
            expires_at=expires_at_naive  
        )
        
        db.add(session)
        await db.commit()

        return JSONResponse(
            status_code=200,  
            content={
                "status": "success",
                "message": "User successfully registered",
                "session_id": session_id,
                "expires_at": expires_at_naive.isoformat(),
            }
        )

    except Exception as e:
        # Rollback jika terjadi error
        await db.rollback()
        return JSONResponse(
            status_code=500,  
            content={
                "status": "error",
                "message": f"An error occurred while registering the user: {str(e)}",
                "time": datetime.now(timezone.utc).isoformat()
            }
        )



async def login_user(username: str, password: str, db: AsyncSession):
    try:
        # Query user berdasarkan username
        db_user = await db.execute(select(User).filter(User.username == username))
        user = db_user.scalars().first()

        # Validasi apakah user ditemukan
        if not user:
            # Jika username tidak ditemukan, kembalikan response error 401
            return JSONResponse(
                status_code=401, 
                content={
                    "status": "error",
                    "message": "Username not found",
                    "time": datetime.now(timezone.utc).isoformat()
                }
            )

        # Validasi password
        if not verify_password(password, user.password):
            # Jika password salah, kembalikan response error 401
            return JSONResponse(
                status_code=401,  
                content={
                    "status": "error",
                    "message": "Incorrect password",
                    "time": datetime.now(timezone.utc).isoformat()
                }
            )

        # Generate session ID (UUID)
        session_id = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        expires_at_naive = expires_at.replace(tzinfo=None)

        # Cek jika ada session aktif untuk user
        db_session = await db.execute(select(Session).filter(Session.user_id == user.id))
        existing_session = db_session.scalars().first()

        if existing_session:
            # Jika session sudah ada, update waktu kedaluwarsa
            existing_session.expires_at = expires_at_naive
            db.add(existing_session)
            await db.commit()

            # Return session yang diperbarui
            return JSONResponse(
                status_code=200, 
                content={
                    "status": "success",
                    "message": "Login successfully",
                    "session_id": existing_session.session_id,
                    "expires_at": expires_at_naive.isoformat(),
                   
                }
            )
        else:
            # Jika tidak ada session, buat session baru
            session = Session(
                session_id=session_id,
                user_id=user.id,
                expires_at=expires_at_naive
            )
            db.add(session)
            await db.commit()

            # Return session baru
            return JSONResponse(
                status_code=200,  
                content={
                    "status": "success",
                    "message": "Login successful",
                    "session_id": session_id,
                    "expires_at": expires_at_naive.isoformat(),
                   
                }
            )

    except Exception as e:
        # Menangani error jika terjadi masalah selama login atau operasi database
        return JSONResponse(
            status_code=500,  # Status 500 Internal Server Error
            content={
                "status": "error",
                "message": f"An error occurred during login: {str(e)}",
                "time": datetime.now(timezone.utc).isoformat()
            }
        )
    
# Handler for user logout
async def logout_user(session_id: str, db: AsyncSession):
    """
    Endpoint to log out the user.
    It will remove the session from the database using the session_id.
    """
    try:
        # Query session berdasarkan session_id
        db_session = await db.execute(select(Session).filter(Session.session_id == session_id))
        session = db_session.scalars().first()

        # Jika session tidak ditemukan atau session_id tidak valid
        if not session:
            return JSONResponse(
                status_code=404,  
                content={
                    "status": "error",
                    "message": "Session not found",
                    "time": datetime.now().isoformat()
                }
            )

      
        await db.delete(session)
        await db.commit()

        return JSONResponse(
            status_code=200, 
            content={
                "status": "success",
                "message": "Logged out successfully",
                "time": datetime.now().isoformat()
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "status": "error",
                "message": f"An error occurred during logout: {str(e)}",
                "time": datetime.now().isoformat()
            }
        )