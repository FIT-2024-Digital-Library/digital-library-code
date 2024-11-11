from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select

from app.schemas import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from app.db.database import *

router = APIRouter(
    prefix='/genres',
    tags=['genres']
)


@router.get('/{id}', response_model=Genre, summary='Returns Genres Data')
async def get_genre(id: int):
    async with async_session_maker() as session:
        query = select(genre_table).where(genre_table.c.id == id)
        result = await session.execute(query)
        result = result.first()
        if result is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return Genre(**result._mapping)


@router.get('/', response_model=List[Genre], summary='Returns Genres Data')
async def get_genre():
    async with async_session_maker() as session:
        query = select(author_table)
        result = await session.execute(query)
        genres = result.all()
        if not genres:
            raise HTTPException(status_code=404, detail="No genres found matching the criteria")
        return [Genre(**genre._mapping) for genre in genres]
