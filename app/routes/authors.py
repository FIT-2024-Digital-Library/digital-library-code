from typing import Optional, List

import sqlalchemy
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select, MappingResult

from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from app.crud.authors import get_author_from_db, get_authors_from_db
from app.db.database import async_session_maker
from app.db.models import author_table
from app.schemas import Author

router = APIRouter(
    prefix='/authors',
    tags=['authors']
)


@router.get('/{id}', response_model=Author, summary='Returns Authors Data')
async def get_author(id: int):
    author = await get_author_from_db(id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get('/', response_model=List[Author], summary='Returns Authors Data')
async def get_authors():
    authors = await get_authors_from_db()
    if len(authors) == 0:
        raise HTTPException(status_code=404, detail="No authors in db")
    return authors
