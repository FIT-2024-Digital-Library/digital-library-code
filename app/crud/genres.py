from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from app.settings import async_session_maker
from app.models import genre_table
from app.schemas import GenreCreate
from app.utils import CrudException


async def get_genre_from_db(genre_id):
    async with async_session_maker() as session:
        query = select(genre_table).where(genre_table.c.id == genre_id)
        result = await session.execute(query)
        return result.mappings().first()


async def get_genres_from_db(name: str = None):
    async with async_session_maker() as session:
        if name is not None:
            query = select(genre_table).where(genre_table.c.name.ilike(f"%{name}%"))
        else:
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
        genres_in_db = await get_genres_from_db(name=genre.name)
        if genres_in_db is None or len(genres_in_db) is 0:
            query = insert(genre_table).values(**genre.model_dump())
            result = await session.execute(query)
            await session.commit()
            genre_id = result.inserted_primary_key[0]
        else:
            genre_id = genres_in_db[0]["genre_id"]
        return genre_id


async def delete_genre_from_db(genre_id: int):
    async with async_session_maker() as session:
        try:
            genre = await get_genre_from_db(genre_id)
            if genre is not None:
                query = delete(genre_table).where(genre_table.c.id == genre_id)
                await session.execute(query)
                await session.commit()
            return genre
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")


async def update_genre_in_db(genre_id: int, genre: GenreCreate):
    async with async_session_maker() as session:
        try:
            genre_in_db = await get_genre_from_db(genre_id)
            if genre_in_db is not None:
                query = update(genre_table).where(genre_table.c.id == genre_id).values(**genre.model_dump())
                await session.execute(query)
                await session.commit()
                genre_in_db = await get_genre_from_db(genre_id)
            return genre_in_db
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")
