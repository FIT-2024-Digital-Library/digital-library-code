from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select

from app.schemas import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from app.db.database import *

router = APIRouter(
    prefix='/books',
    tags=['book']
)


@router.get('/', response_model=List[Book], summary='Returns books using search parameters (all of them otherwise)')
async def get_books(
        id: Optional[int] = Query(None, description="Filter by book ID"),
        title: Optional[str] = Query(None, description="Filter by book title"),
        author: Optional[str] = Query(None, description="Filter by author"),
        genre: Optional[int] = Query(None, description="Filter by genre ID"),
        published_date: Optional[date] = Query(None, description="Filter by publication date"),
        description: Optional[str] = Query(None, description="Filter by description keyword"),
        pdf_url: Optional[str] = Query(None, description="Filter by PDF URL")
):
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
            query = query.where(book_table.c.genre == res)
        if published_date is not None:
            query = query.where(book_table.c.published_date == published_date)
        if description is not None:
            query = query.where(book_table.c.description.ilike(f"%{description}%"))
        if pdf_url is not None:
            query = query.where(book_table.c.pdf_url == pdf_url)

        result = await session.execute(query)
        books = result.all()

        if not books:
            raise HTTPException(status_code=404, detail="No books found matching the criteria")
        return [Book(**book._mapping) for book in books]


@router.get('/{id}', response_model=Book, summary='Returns book data')
async def get_book(id: int):
    async with async_session_maker() as session:
        query = select(book_table).where(book_table.c.id == id)
        result = await session.execute(query)
        result = result.first()
        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return Book(**result._mapping)


@router.post('/create', response_model=None, summary='Creates new book. Only for authorized user with admin previlegy')
async def create_book():
    raise NotImplemented
    return {}  # Here will be pydantic scheme's object


@router.put('/{id}/update', response_model=None,
            summary='Updates book data. Only for authorized user with admin previlegy')
async def update_book(id: int):
    raise NotImplemented
    return {}  # Here will be pydantic scheme's object


@router.delete('/{id}/delete', response_model=None,
               summary='Deletes book. Only for authorized user with admin previlegy')
async def delete_book(id: int):
    raise NotImplemented
    return {}  # Here will be OK empty response
