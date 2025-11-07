from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os

# Separate connection for auth database
AUTH_DATABASE_URL = os.getenv(
    "AUTH_DATABASE_URL",
    "postgresql+asyncpg://farout:TorOve78!@db:5432/farout_auth"
)

auth_engine = create_async_engine(
    AUTH_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    future=True
)

AuthSessionLocal = async_sessionmaker(
    auth_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_auth_db():
    """Dependency to get auth database session"""
    async with AuthSessionLocal() as session:
        yield session
