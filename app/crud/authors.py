from sqlalchemy import select, insert, delete, update

from app.db.database import async_session_maker
from app.db.models import author_table
from app.schemas import AuthorCreate


async def get_author_from_db(id: int = None, name: str = None):
    async with async_session_maker() as session:
        if id is not None:
            query = select(author_table).where(author_table.c.id == id)
        elif name is not None:
            query = select(author_table).where(author_table.c.name == name)
        else:
            return None
        result = await session.execute(query)
        return result.mappings().first()


async def get_authors_from_db():
    async with async_session_maker() as session:
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
        author_in_db = await get_author_from_db(name=author.name)
        if author_in_db is None:
            query = insert(author_table).values(**author.model_dump())
            result = await session.execute(query)
            await session.commit()
            author_id = result.inserted_primary_key[0]
        else:
            author_id = author_in_db["id"]
        return author_id


async def delete_author_from_db(id: int):
    async with async_session_maker() as session:
        author = await get_author_from_db(id)
        if author is not None:
            query = delete(author_table).where(author_table.c.id == id)
            await session.execute(query)
            await session.commit()
        return author


async def update_author_in_db(id: int, author: AuthorCreate):
    async with async_session_maker() as session:
        author_in_db = await get_author_from_db(id)
        if author_in_db is not None:
            query = update(author_table).where(author_table.c.id == id).values(**author.model_dump())
            await session.execute(query)
            await session.commit()
            author_in_db = await get_author_from_db(id)
        return author_in_db
