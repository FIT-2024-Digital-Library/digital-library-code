from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_interface import CrudInterface
from app.models import author_table
from app.schemas import AuthorCreate
from app.utils import CrudException


class AuthorsCrud(CrudInterface):
    @classmethod
    async def get(cls, session: AsyncSession, author_id: int):
        query = select(author_table).where(author_table.c.id == author_id)
        result = await session.execute(query)
        return result.mappings().first()

    @classmethod
    async def get_multiple(cls, session: AsyncSession, name: str | None = None):
        if name is not None:
            query = select(author_table).where(author_table.c.name.ilike(f"%{name}%"))
        else:
            query = select(author_table)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def create(cls, session: AsyncSession, author: AuthorCreate):
        query = insert(author_table).values(**author.model_dump())
        result = await session.execute(query)
        author_id = result.inserted_primary_key[0]
        return author_id

    @classmethod
    async def get_existent_or_create(cls, session: AsyncSession, author: AuthorCreate):
        authors_in_db = await cls.get_multiple(session, name=author.name)
        if authors_in_db is None or len(authors_in_db) == 0:
            query = insert(author_table).values(**author.model_dump())
            result = await session.execute(query)
            author_id = result.inserted_primary_key[0]
        else:
            author_id = authors_in_db[0]["id"]
        return author_id

    @classmethod
    async def delete(cls, session: AsyncSession, author_id: int):
        try:
            author = await cls.get(session, author_id)
            if author is not None:
                query = delete(author_table).where(author_table.c.id == author_id)
                await session.execute(query)
            return author
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")

    @classmethod
    async def update(cls, session: AsyncSession, author_id: int, author: AuthorCreate):
        try:
            author_in_db = await cls.get(session, author_id)
            if author_in_db is not None:
                query = update(author_table).where(author_table.c.id == author_id).values(**author.model_dump())
                await session.execute(query)
                author_in_db = await cls.get(session, author_id)
            return author_in_db
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")
