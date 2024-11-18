from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from app.db.database import async_session_maker
from app.db.models import book_table, author_table, genre_table


async def get_books_from_db(id: int = None,
                            title: str = None,
                            author: str = None,
                            genre: str = None,
                            published_date: date = None,
                            description: str = None,
                            pdf_url: str = None):
    async with async_session_maker() as session:
        query = select(book_table)
        if id is not None:
            query = query.where(book_table.c.id == id)
        if title is not None:
            query = query.where(book_table.c.title.ilike(f"%{title}%"))
        if author is not None:
            author_id = await session.execute(select(author_table.c.id).where(author_table.c.name == author))
            res = author_id.scalar()
            query = query.where(book_table.c.author == res)
        if genre is not None:
            genre_id = await session.execute(select(genre_table.c.id).where(genre_table.c.name == genre))
            res = genre_id.scalar()
            query = query.where(book_table.c.name == res)
        if published_date is not None:
            query = query.where(book_table.c.published_date == published_date)
        if description is not None:
            query = query.where(book_table.c.description.ilike(f"%{description}%"))
        if pdf_url is not None:
            query = query.where(book_table.c.pdf_url == pdf_url)

        result = await session.execute(query)
        books = result.mappings().all()
        return books


async def get_book_from_db(id: int):
    async with async_session_maker() as session:
        query = select(book_table).where(book_table.c.id == id)
        result = await session.execute(query)
        return result.mappings().first()
