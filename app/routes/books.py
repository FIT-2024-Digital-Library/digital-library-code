from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException, Depends

from app.crud.books import get_books_from_db, get_book_from_db, create_book_in_db, \
    update_book_in_db, delete_book_from_db
from app.schemas import Book, CreateBook, User
from app.utils import get_current_user


router = APIRouter(
    prefix='/books',
    tags=['book']
)


@router.get('/', response_model=List[Book], summary='Returns books using search parameters (all of them otherwise)')
async def get_books(
        title: Optional[str] = Query(None, description="Filter by book title"),
        author: Optional[str] = Query(None, description="Filter by author"),
        genre: Optional[str] = Query(None, description="Filter by name"),
        published_date: Optional[date] = Query(None, description="Filter by publication date"),
        description: Optional[str] = Query(None, description="Filter by description keyword"),
        image: Optional[str] = Query(None, description="Filter by image\'s path"),
        pdf_url: Optional[str] = Query(None, description="Filter by PDF URL")
):
    books = await get_books_from_db(title, author, genre, published_date, description, image, pdf_url)
    return books


@router.get('/{author_id}', response_model=Book, summary='Returns book data')
async def get_book(id: int):
    result = await get_book_from_db(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result


@router.post('/create', response_model=int, summary='Creates new book. Only for authorized user with admin previlegy')
async def create_book(book: CreateBook, user_data: User = Depends(get_current_user)):
    id = await create_book_in_db(book)
    return id


@router.put('/{author_id}/update', response_model=Book,
            summary='Updates book data. Only for authorized user with admin previlegy')
async def update_book(id: int, book: CreateBook, user_data: User = Depends(get_current_user)):
    book = await update_book_in_db(id, book)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete('/{author_id}/delete', response_model=Book,
               summary='Deletes book. Only for authorized user with admin previlegy')
async def delete_book(id: int, user_data: User = Depends(get_current_user)):
    book = await delete_book_from_db(id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
