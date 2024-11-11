from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select

from app.schemas import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from app.db.database import *

router = APIRouter(
    prefix='/authors',
    tags=['authors']
)


@router.get('/{id}', response_model=Author, summary='Returns Authors Data')
async def get_author(id: int):
    async with async_session_maker() as session:
        query = select(author_table).where(author_table.c.id == id)
        result = await session.execute(query)
        result = result.first()

        if result is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return Author(**result._mapping)


@router.get('/', response_model=List[Author], summary='Returns Authors Data')
async def get_author():
    async with async_session_maker() as session:
        query = select(author_table)
        result = await session.execute(query)
        authors = result.all()
        if not authors:
            raise HTTPException(status_code=404, detail="No author found matching the criteria")
        return [Author(**author._mapping) for author in authors]
