from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_interface import CrudInterface
from app.models import genre_table
from app.schemas import GenreCreate
from app.utils import CrudException


class GenresCrud(CrudInterface):
    @classmethod
    async def get(cls, session: AsyncSession, genre_id: int):
        query = select(genre_table).where(genre_table.c.id == genre_id)
        result = await session.execute(query)
        return result.mappings().first()

    @classmethod
    async def get_multiple(cls, session: AsyncSession, name: str | None = None):
        if name is not None:
            query = select(genre_table).where(genre_table.c.name.ilike(f"%{name}%"))
        else:
            query = select(genre_table)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def create(cls, session: AsyncSession, genre: GenreCreate):
        query = insert(genre_table).values(**genre.model_dump())
        result = await session.execute(query)
        genre_id = result.inserted_primary_key[0]
        return genre_id

    @classmethod
    async def get_existent_or_create(cls, session: AsyncSession, genre: GenreCreate):
        genres_in_db = await cls.get_multiple(session, name=genre.name)
        if genres_in_db is None or len(genres_in_db) == 0:
            query = insert(genre_table).values(**genre.model_dump())
            result = await session.execute(query)
            genre_id = result.inserted_primary_key[0]
        else:
            genre_id = genres_in_db[0]["id"]
        return genre_id

    @classmethod
    async def delete(cls, session: AsyncSession, genre_id: int):
        try:
            genre = await cls.get(session, genre_id)
            if genre is not None:
                query = delete(genre_table).where(genre_table.c.id == genre_id)
                await session.execute(query)
            return genre
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")

    @classmethod
    async def update(cls, session: AsyncSession, genre_id: int, genre: GenreCreate):
        try:
            genre_in_db = await cls.get(session, genre_id)
            if genre_in_db is not None:
                query = update(genre_table).where(genre_table.c.id == genre_id).values(**genre.model_dump())
                await session.execute(query)
                genre_in_db = await cls.get(session, genre_id)
            return genre_in_db
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")
