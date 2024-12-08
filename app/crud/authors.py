from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from app.settings import async_session_maker
from app.models import author_table
from app.schemas import AuthorCreate
from app.utils import CrudException


async def get_author_from_db(author_id):
    async with async_session_maker() as session:
        query = select(author_table).where(author_table.c.id == author_id)
        result = await session.execute(query)
        return result.mappings().first()


async def get_authors_from_db(name: str = None):
    async with async_session_maker() as session:
        if name is not None:
            query = select(author_table).where(author_table.c.name.ilike(f"%{name}%"))
        else:
            query = select(author_table)
        result = await session.execute(query)
        return result.mappings().all()


async def create_author_in_db(author: AuthorCreate):
    async with async_session_maker() as session:
        query = insert(author_table).values(**author.model_dump())
        result = await session.execute(query)
        await session.commit()
        author_id = result.inserted_primary_key[0]
        return author_id


async def get_existent_or_create_author_in_db(author: AuthorCreate):
    async with async_session_maker() as session:
        authors_in_db = await get_authors_from_db(name=author.name)
        if authors_in_db is None:
            query = insert(author_table).values(**author.model_dump())
            result = await session.execute(query)
            await session.commit()
            author_id = result.inserted_primary_key[0]
        else:
            author_id = authors_in_db[0]["author_id"]
        return author_id


async def delete_author_from_db(author_id: int):
    async with async_session_maker() as session:
        try:
            author = await get_author_from_db(author_id)
            if author is not None:
                query = delete(author_table).where(author_table.c.id == author_id)
                await session.execute(query)
                await session.commit()
            return author
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")


async def update_author_in_db(author_id: int, author: AuthorCreate):
    async with async_session_maker() as session:
        try:
            author_in_db = await get_author_from_db(author_id)
            if author_in_db is not None:
                query = update(author_table).where(author_table.c.id == author_id).values(**author.model_dump())
                await session.execute(query)
                await session.commit()
                author_in_db = await get_author_from_db(author_id)
            return author_in_db
        except IntegrityError as e:
            raise CrudException("Update or delete on table violates foreign key constraint")
