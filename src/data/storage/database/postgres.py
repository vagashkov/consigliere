from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)


from src.config import settings
from src.data.storage.database.models import Base

# Create an async engine
engine = create_async_engine(settings.DATABASE_URL)

# Create a session factory
AsyncLocalSession = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autocommit=False,
         )


# Function to create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
