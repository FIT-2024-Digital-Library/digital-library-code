from sqlalchemy import select

from app.db.database import async_session_maker
from app.db.models import author_table


async def get_author_from_db(id: int):
    async with async_session_maker() as session:
        query = select(author_table).where(author_table.c.id == id)
        result = await session.execute(query)
        return result.mappings().first()


async def get_authors_from_db():
    async with async_session_maker() as session:
        query = select(author_table)
        result = await session.execute(query)
        return result.mappings().all()
