from sqlalchemy import select, insert

from app.db.database import async_session_maker
from app.db.models import genre_table
from app.schemas import GenreCreate


async def get_genre_from_db(id: int = None, name: str = None):
    async with async_session_maker() as session:
        if id is not None:
            query = select(genre_table).where(genre_table.c.id == id)
        elif name is not None:
            query = select(genre_table).where(genre_table.c.name == name)
        else:
            return None
        result = await session.execute(query)
        return result.mappings().first()


async def get_genres_from_db():
    async with async_session_maker() as session:
        query = select(genre_table)
        result = await session.execute(query)
        return result.mappings().all()


async def create_genre_in_db(genre: GenreCreate):
    async with async_session_maker() as session:
        query = insert(genre_table).values(**genre.model_dump())
        result = await session.execute(query)
        await session.commit()
        genre_id = result.inserted_primary_key[0]
        return genre_id


async def get_existent_or_create_genre_in_db(genre: GenreCreate):
    async with async_session_maker() as session:
        genre = await get_genre_from_db(name=genre.name)
        genre_id = genre['id']
        if genre_id is None:
            query = insert(genre_table).values(**genre.model_dump())
            result = await session.execute(query)
            await session.commit()
            genre_id = result.inserted_primary_key[0]
        return genre_id
