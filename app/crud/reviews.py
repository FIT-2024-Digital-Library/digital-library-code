import datetime
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.crud.books import BooksCrud
from app.crud.crud_interface import CrudInterface
from app.models import review_table
from app.schemas import Review, ReviewCreate, ReviewUpdate, ReviewsFiltersScheme, BookUpdate


class ReviewsCrud(CrudInterface):
    REVIEW_FIELDS = ['id', 'owner_id', 'book_id', 'mark', 'last_edit_date', 'text']

    @classmethod
    async def get(cls, session: AsyncSession, element_id: int) -> Optional[Review]:
        result = (await session.execute(
            select(*[review_table.c[field] for field in cls.REVIEW_FIELDS])
            .where(review_table.c.id == element_id)
        )).mappings().first()
        return None if result is None else Review(**result)

    @classmethod
    async def get_multiple(cls, session: AsyncSession, filters: ReviewsFiltersScheme = None) -> List[int]:
        query = select(*[review_table.c[field] for field in cls.REVIEW_FIELDS]).limit(filters.limit).offset(
            filters.offset)
        if filters.book_id is not None:
            query = query.where(review_table.c.book_id == filters.book_id)
        if filters.owner_id is not None:
            query = query.where(review_table.c.owner_id == filters.owner_id)
        result = await session.execute(query)
        return [review['id'] for review in result.mappings().all()]

    @classmethod
    async def create(cls, session: AsyncSession, model: ReviewCreate, owner_id: int = None) -> Review:
        book = await BooksCrud.get(session, model.book_id)
        if book is None:
            raise ValueError("Book for review not found")
        if await cls.check_review_by_user_and_book(session, owner_id, book['id']):
            raise ValueError("Only one review for book from one user")
        result = await session.execute(
            insert(review_table)
            .values(owner_id=owner_id, last_edit_date=datetime.date.today(), **model.model_dump())
            .returning(*[review_table.c[field] for field in cls.REVIEW_FIELDS])
        )
        current_avg = book['avg_mark']
        reviews_count_for_book = book['marks_count']
        new_reviews_count = reviews_count_for_book + 1
        new_avg = (current_avg * reviews_count_for_book + model.mark) / new_reviews_count
        print(new_avg)
        await BooksCrud.update(session, model.book_id,
                               BookUpdate(**{'avg_mark': new_avg, 'marks_count': new_reviews_count}))
        await session.commit()
        return Review(**result.mappings().first())

    @classmethod
    async def delete(cls, session: AsyncSession, review_id: int, owner_id: int = None):
        review = await cls.get(session, review_id)
        if review is None:
            raise ValueError("Review not found")
        if review.owner_id != owner_id:
            raise ValueError("It's not your review")
        book = await BooksCrud.get(session, review.book_id)
        current_avg = book['avg_mark']
        reviews_count_for_book = book['marks_count']
        new_reviews_count = reviews_count_for_book - 1
        new_avg = (
                              current_avg * reviews_count_for_book - review.mark) / new_reviews_count if new_reviews_count > 0 else 0
        await BooksCrud.update(session, review.book_id,
                                BookUpdate(**{'avg_mark': new_avg, 'marks_count': new_reviews_count}))
        await session.execute(
            delete(review_table).where(review_table.c.id == review_id)
        )
        await session.commit()
        return review

    @classmethod
    async def update(cls, session: AsyncSession, element_id: int, owner_id: int, model: ReviewUpdate = None) -> Review:
        old_review = await cls.get(session, element_id)
        if old_review is None:
            raise ValueError("Review not found")
        if old_review.owner_id != owner_id:
            raise ValueError("It's not your review")
        if model.mark is not None and model.mark != old_review.mark:
            book = await BooksCrud.get(session, old_review.book_id)
            current_avg = book['avg_mark']
            reviews_count_for_book = book['marks_count']
            new_avg = (
                              current_avg * reviews_count_for_book - old_review.mark + model.mark) / reviews_count_for_book
            await BooksCrud.update(session, old_review.book_id, BookUpdate(**{'avg_mark': new_avg}))
        result = await session.execute(
            update(review_table)
            .where(review_table.c.id == element_id)
            .values(last_edit_date=datetime.date.today(), **model.model_dump())
            .returning(*[review_table.c[field] for field in cls.REVIEW_FIELDS])
        )
        await session.commit()
        return Review(**result.mappings().first())

    @classmethod
    async def check_review_by_user_and_book(cls, session: AsyncSession, owner_id: int, book_id: int) -> bool:
        result = (await session.execute(
            select(review_table)
            .where(
                review_table.c.owner_id == owner_id,
                review_table.c.book_id == book_id
            )
        )).scalar()
        return result is not None

    @classmethod
    async def get_average_mark(cls, session: AsyncSession, book_id: int) -> Optional[float]:
        book = await BooksCrud.get(session, book_id)
        return book['avg_mark'] if book else None

    @classmethod
    async def get_reviews_count(cls, session: AsyncSession, book_id: int) -> Optional[int]:
        book = await BooksCrud.get(session, book_id)
        return book['marks_count'] if book else None
