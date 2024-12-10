import datetime

from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import review_table
from app.schemas import Review, ReviewCreate
from app.utils import CrudException


async def get_review_by_id(session: AsyncSession, review_id: int) -> Review:
    result = await session.execute((
        select(review_table.c[*Review.model_fields])
        .where(review_table.c.id == review_id)
    ))
    return Review(**result.mappings().first())


async def create_review_in_db(session: AsyncSession, user_id: int, review_data: ReviewCreate) -> Review:
    result = await session.execute(
        insert(review_table)
        .values(author_id=user_id, last_edit_date=datetime.date.today(), **review_data.model_dump())
        .returning(review_table.c[*Review.model_fields])
    )
    await session.commit()
    return Review(**result.mappings().first())
