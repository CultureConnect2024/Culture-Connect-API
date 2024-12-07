from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import Config

# Inisialisasi engine untuk berinteraksi dengan database menggunakan asyncpg
engine = create_async_engine(
    f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
    echo=True,
)

# Membuat SessionFactory untuk menghasilkan sesi asinkronus
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base digunakan untuk deklarasi model ORM
Base = declarative_base()

# Dependency untuk mengelola sesi database asinkronus
async def get_db():
    """
    Menghasilkan sesi database asinkronus dan menutupnya setelah digunakan.
    """
    async with AsyncSessionLocal() as db:
        yield db  # Make sure this returns an AsyncSession

