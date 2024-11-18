from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select, MappingResult

from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from app.crud.books import get_books_from_db, get_book_from_db
from app.db.database import async_session_maker
from app.db.models import book_table, author_table, genre_table
from app.schemas import Book

router = APIRouter(
    prefix='/books',
    tags=['book']
)


@router.get('/', response_model=List[Book], summary='Returns books using search parameters (all of them otherwise)')
async def get_books(
        id: Optional[int] = Query(None, description="Filter by book ID"),
        title: Optional[str] = Query(None, description="Filter by book title"),
        author: Optional[str] = Query(None, description="Filter by author"),
        genre: Optional[str] = Query(None, description="Filter by name"),
        published_date: Optional[date] = Query(None, description="Filter by publication date"),
        description: Optional[str] = Query(None, description="Filter by description keyword"),
        pdf_url: Optional[str] = Query(None, description="Filter by PDF URL")
):
    books = await get_books_from_db(id, title, author, genre, published_date, description, pdf_url)
    if len(books) == 0:
        raise HTTPException(status_code=404, detail="No books found matching the criteria")
    return books


@router.get('/{id}', response_model=Book, summary='Returns book data')
async def get_book(id: int):
    result = await get_book_from_db(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


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
