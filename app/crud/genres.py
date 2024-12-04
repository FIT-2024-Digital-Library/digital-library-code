import asyncpg
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from app.crud.crud_exception import CrudException
from app.db.database import async_session_maker
from app.db.models import genre_table
from app.schemas import GenreCreate


async def get_genre_from_db(id: int = None, name: str = None):
    async with async_session_maker() as session:
        if id is not None:
            query = select(genre_table).where(genre_table.c.id == id)
        elif name is not None:
            query = select(genre_table).where(genre_table.c.name.ilike(f"%{name}%"))
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
        genre_in_db = await get_genre_from_db(name=genre.name)
        if genre_in_db is None:
            query = insert(genre_table).values(**genre.model_dump())
            result = await session.execute(query)
            await session.commit()
            genre_id = result.inserted_primary_key[0]
        else:
            genre_id = genre_in_db["id"]
        return genre_id


async def delete_genre_from_db(id: int):
    async with async_session_maker() as session:
        try:
            genre = await get_genre_from_db(id)
            if genre is not None:
                query = delete(genre_table).where(genre_table.c.id == id)
                await session.execute(query)
                await session.commit()
            return genre
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")


async def update_genre_in_db(id: int, genre: GenreCreate):
    async with async_session_maker() as session:
        try:
            genre_in_db = await get_genre_from_db(id)
            if genre_in_db is not None:
                query = update(genre_table).where(genre_table.c.id == id).values(**genre.model_dump())
                await session.execute(query)
                await session.commit()
                genre_in_db = await get_genre_from_db(id)
            return genre_in_db
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")
