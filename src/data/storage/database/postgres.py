from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

from src.config import settings

# Create an async engine
engine = create_async_engine(settings.DATABASE_URL)

# Create a session factory
AsyncLocalSession = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autocommit=False,
            expire_on_commit=False
         )
