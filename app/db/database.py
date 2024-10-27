from sqlalchemy.ext.asyncio import create_async_engine
from .models import db_metadata

db_engine = create_async_engine(
    "postgresql+asyncpg://backend:t0p_s3cret!@localhost:5432/digital-library", echo=True
)

async def create_tables() -> None:
    async with db_engine.begin() as connection:
        await connection.run_sync(db_metadata.drop_all)
        await connection.run_sync(db_metadata.create_all)