from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone
from app.src.models.model import User, Session


# Handler untuk mendapatkan user berdasarkan session_id
async def get_user_by_session(session_id: str, db: AsyncSession):
    try:
        # Query session berdasarkan session_id
        db_session = await db.execute(select(Session).filter(Session.session_id == session_id))
        session = db_session.scalars().first()

        # Jika session tidak ditemukan atau sudah kedaluwarsa
        if not session:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Session not found or expired",
                    "time": datetime.now(timezone.utc).isoformat()
                }
            )

        # Query user berdasarkan user_id dari session
        db_user = await db.execute(select(User).filter(User.id == session.user_id))
        user = db_user.scalars().first()

        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "User not found",
                    "time": datetime.now(timezone.utc).isoformat()
                }
            )

        # Return data user
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "time": datetime.now(timezone.utc).isoformat()
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "time": datetime.now(timezone.utc).isoformat()
            }
        )


# Handler untuk mendapatkan semua user
async def get_all_users(db: AsyncSession):
    try:
        # Query semua user
        db_users = await db.execute(select(User))
        users = db_users.scalars().all()

        if not users:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No users found",
                    "time": datetime.now(timezone.utc).isoformat()
                }
            )

        # return data user
        user_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            for user in users
        ]

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": user_list,
                "time": datetime.now(timezone.utc).isoformat()
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "time": datetime.now(timezone.utc).isoformat()
            }
        )
