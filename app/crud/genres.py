from sqlalchemy import select

from app.db.database import async_session_maker
from app.db.models import genre_table


async def get_genre_from_db(id: int):
    async with async_session_maker() as session:
        query = select(genre_table).where(genre_table.c.id == id)
        result = await session.execute(query)
        return result.mappings().first()


async def get_genres_from_db():
    async with async_session_maker() as session:
        query = select(genre_table)
        result = await session.execute(query)
        return result.mappings().all()
