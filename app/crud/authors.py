from sqlalchemy import select, insert

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
        author = await get_author_from_db(name=author.name)
        author_id = author["id"]
        if author_id is None:
            query = insert(author_table).values(**author.model_dump())
            result = await session.execute(query)
            await session.commit()
            author_id = result.inserted_primary_key[0]
        return author_id
