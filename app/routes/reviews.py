from typing import List, Annotated
from fastapi import APIRouter, Query, HTTPException, Depends

from app.crud.reviews import ReviewsCrud
from app.schemas import User, ReviewsFiltersScheme, Review, ReviewCreate, ReviewUpdate
from app.settings import async_session_maker
from app.utils.auth import get_current_user

router = APIRouter(
    prefix='/reviews',
    tags=['review']
)


@router.get('/', response_model=List[int], summary="Returns reviews's ids maybe filtered by book and user")
async def get_reviews(filters: Annotated[ReviewsFiltersScheme, Query()]) -> List[int]:
    async with async_session_maker() as session:
        try:
            return await ReviewsCrud.get_multiple(session, filters)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.get('/{review_id}', response_model=Review, summary='Returns review')
async def get_review(review_id: int) -> Review:
    async with async_session_maker() as session:
        result = await ReviewsCrud.get(session, review_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return result


@router.get('/average/{book_id}', response_model=float, summary='Returns average mark for book')
async def get_average_mark(book_id: int) -> float:
    async with async_session_maker() as session:
        avg_mark = await get_average_mark(session, book_id)
        if avg_mark is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return avg_mark


@router.get('/count/{book_id}', response_model=int, summary='Returns marks count for book')
async def get_marks_count(book_id: int) -> int:
    async with async_session_maker() as session:
        reviews_count = await ReviewsCrud.get_reviews_count(session, book_id)
        if reviews_count is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return reviews_count


@router.post('/create', response_model=Review,
             summary='Creates new review. Only for authorized users. One review from one user for one book')
async def create_review(review: ReviewCreate, user_creds: User = Depends(get_current_user)) -> Review:
    async with async_session_maker() as session:
        try:
            return await ReviewsCrud.create(session, review, user_creds.id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.put('/{review_id}/update', response_model=Review, summary="Updates existing review. Only for reviews' owners")
async def update_review(review_id: int, review: ReviewUpdate, user_creds: User = Depends(get_current_user)) -> Review:
    async with async_session_maker() as session:
        try:
            return await ReviewsCrud.update(session, review_id, user_creds.id, review)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{review_id}/delete', response_model=Review,
               summary="Deletes existing review. Only for reviews' owners")
async def delete_review(review_id: int, user_creds: User = Depends(get_current_user)) -> Review:
    async with async_session_maker() as session:
        try:
            return await ReviewsCrud.delete(session, review_id, user_creds.id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
