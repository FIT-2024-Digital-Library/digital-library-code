from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends

from app.crud.reviews import get_review_by_id, create_review_in_db
from app.schemas import Review, ReviewCreate, User
from app.settings import async_session_maker
from app.utils.auth import get_current_user, get_current_admin_user

router = APIRouter(
    prefix='/reviews',
    tags=['review']
)


@router.get('/{review_id}', response_model=Review, summary='Returns review')
async def get_review(review_id: int):
    async with async_session_maker() as session:
        result = await get_review_by_id(session, review_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return result


@router.post('/create', response_model=Review, summary='Creates new book. Only for authorized users. One review from one user for one book')
async def create_review(review: ReviewCreate, user_data: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        try:
            return await create_review_in_db(session, user_data.id, review)
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e))



# @router.put('/{book_id}/update', response_model=Review,
#             summary='Updates book data. Only for authorized user with admin privilege')
# async def update_review(book_id: int, book: ReviewCreate, user_data: User = Depends(get_current_user)):
#     async with async_session_maker() as session:
#         book = await update_book_in_db(session, book_id, book)
#         if book is None:
#             raise HTTPException(status_code=404, detail="Book not found")
#         await session.commit()
#         return book
#
#
# @router.delete('/{book_id}/delete', response_model=Review,
#                summary='Deletes book. Only for authorized user with admin privilege')
# async def delete_review(book_id: int, user_data: User = Depends(get_current_user)):
#     async with async_session_maker() as session:
#         book = await delete_book_from_db(session, book_id)
#         if book is None:
#             raise HTTPException(status_code=404, detail="Book not found")
#         await session.commit()
#         return book
