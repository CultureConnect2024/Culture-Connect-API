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
    db: AsyncSession  
):
    hashed_password = hash_password(password)
    
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(username=username, email=email, password=hashed_password)
    db.add(user)

    try:

        await db.commit()

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

        return {
            "message": "User successfully registered",
            "session_id": session_id,
            "expires_at": expires_at_naive.isoformat()
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")



async def login_user(username: str, password: str, db: AsyncSession):

    # Query user based on username
    db_user = await db.execute(select(User).filter(User.username == username))
    user = db_user.scalars().first()

    # Validate username and password
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate session ID (UUID)
    session_id = str(uuid.uuid4())



    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    expires_at_naive = expires_at.replace(tzinfo=None)

    # Check if there is already an active session for the user
    db_session = await db.execute(select(Session).filter(Session.user_id == user.id))
    existing_session = db_session.scalars().first()

    if existing_session:
        # Update the existing session's expiration time
        existing_session.expires_at = expires_at_naive
        db.add(existing_session)
        await db.commit()

        # Return updated session info
        return {
            "status": "success",
            "message": "Login successfully",
            "session_id": existing_session.session_id,
            "expires_at": expires_at_naive.isoformat()
        }
    else:
        # If no existing session, create a new one
        session = Session(
            session_id=session_id,
            user_id=user.id,
            expires_at=expires_at_naive
        )
        db.add(session)
        await db.commit()

        # Return new session info
        return {
            "status": "success",
            "message": "Login successful",
            "session_id": session_id,
            "expires_at": expires_at_naive.isoformat()
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