from datetime import date
from sqlalchemy import select, insert, update, delete

from app.crud.authors import get_existent_or_create_author_in_db, get_author_from_db
from app.crud.genres import get_genre_from_db, get_existent_or_create_genre_in_db
from app.settings import async_session_maker
from app.models import book_table
from app.schemas import BookCreate, GenreCreate, AuthorCreate


async def get_books_from_db(
        title: str = None,
        author: str = None,
        genre: str = None,
        published_date: date = None,
        description: str = None,
        image_url: str = None,
        pdf_url: str = None):
    async with async_session_maker() as session:
        query = select(book_table)
        if title is not None:
            query = query.where(book_table.c.title.ilike(f"%{title}%"))
        if author is not None:
            author_id = await get_author_from_db(name=author)
            query = query.where(book_table.c.author == author_id)
        if genre is not None:
            genre_id = get_genre_from_db(name=genre)
            query = query.where(book_table.c.name == genre_id)
        if published_date is not None:
            query = query.where(book_table.c.published_date == published_date)
        if description is not None:
            query = query.where(book_table.c.description.ilike(f"%{description}%"))
        if pdf_url is not None:
            query = query.where(book_table.c.pdf_url == pdf_url)

        if image_url is not None:
            query = query.where(book_table.c.image_url == image_url)

        result = await session.execute(query)
        books = result.mappings().all()
        return books


async def get_book_from_db(book_id: int):
    async with async_session_maker() as session:
        query = select(book_table).where(book_table.c.id == book_id)
        result = await session.execute(query)
        return result.mappings().first()


async def create_book_in_db(book: BookCreate):
    async with async_session_maker() as session:
        book_dict = book.model_dump()
        genre_creation_model = GenreCreate(name=book_dict['genre'])
        genre_id = await get_existent_or_create_genre_in_db(genre_creation_model)
        book_dict['genre'] = genre_id

        author_creation_model = AuthorCreate(name=book_dict['author'])
        author_id = await get_existent_or_create_author_in_db(author_creation_model)
        book_dict['author'] = author_id

        query = insert(book_table).values(**book_dict)
        result = await session.execute(query)
        await session.commit()
        return result.inserted_primary_key[0]


async def update_book_in_db(book_id: int, book: BookCreate):
    async with async_session_maker() as session:
        book_dict = book.model_dump()
        genre_creation_model = GenreCreate(name=book_dict['genre'])
        genre_id = await get_existent_or_create_genre_in_db(genre_creation_model)
        book_dict['genre'] = genre_id

        author_creation_model = AuthorCreate(name=book_dict['author'])
        author_id = await get_existent_or_create_author_in_db(author_creation_model)
        book_dict['author'] = author_id

        query = update(book_table).where(book_table.c.id == book_id).values(**book_dict)
        await session.execute(query)
        await session.commit()
        book = await get_book_from_db(book_id)
        return book


async def delete_book_from_db(book_id: int):
    async with async_session_maker() as session:
        book = await get_book_from_db(book_id)
        if book:
            query = delete(book_table).where(book_table.c.id == book_id)
            await session.execute(query)
            await session.commit()
        return book
