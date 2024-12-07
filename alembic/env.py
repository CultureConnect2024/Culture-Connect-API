from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context
from app.config import Config
# Alembic Config
config = context.config

# Logging Configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import metadata dari model Anda
from app.src.models.model import Base  
target_metadata = Base.metadata

# database_url = postgresql+asyncpg://postgres:@localhost:5432/culture_connect_db


def get_url():
    user = Config.DB_USER
    password = Config.DB_PASS
    server = Config.DB_HOST
    port = Config.DB_PORT
    db = Config.DB_NAME
    print(f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}")
    return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

def run_migrations_offline() -> None:
    """Jalankan migrasi dalam mode offline."""
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Jalankan migrasi dalam mode online."""
    # Membuat AsyncEngine
    connectable: AsyncEngine = create_async_engine(
        # config.get_main_option("sqlalchemy.url"),
        get_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Konfigurasi context Alembic
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Fungsi menjalankan migrasi."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
