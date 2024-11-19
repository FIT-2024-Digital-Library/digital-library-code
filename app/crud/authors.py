from sqlalchemy import select

from app.db.database import async_session_maker
from app.db.models import author_table


async def get_author_from_db_by_id(id: int):
    async with async_session_maker() as session:
        query = select(author_table).where(author_table.c.id == id)
        result = await session.execute(query)
        return result.mappings().first()


async def get_author_from_db_by_name(name: str):
    async with async_session_maker() as session:
        author_id = await session.execute(select(author_table.c.id).where(author_table.c.name == name))
        return author_id.scalar()


async def get_authors_from_db():
    async with async_session_maker() as session:
        query = select(author_table)
        result = await session.execute(query)
        return result.mappings().all()
