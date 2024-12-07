from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException

async def test_db_connection(db: AsyncSession):
    try:
        # Menjalankan query untuk mendapatkan versi PostgreSQL menggunakan text()
        result = await db.execute(text("SELECT version()"))
        version = result.scalar()  # Ambil hasil pertama dari query (versi PostgreSQL)
        return {
            "status": "success",
            "message": "Database connection successful",
            "database_version": version  # Menampilkan versi PostgreSQL
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
