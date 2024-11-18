from typing import List

from fastapi import APIRouter, HTTPException

from app.crud.genres import get_genre_from_db, get_genres_from_db
from app.schemas import Genre

router = APIRouter(
    prefix='/genres',
    tags=['genres']
)


@router.get('/{id}', response_model=Genre, summary='Returns genres data')
async def get_genre(id: int):
    genre = await get_genre_from_db(id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.get('/', response_model=List[Genre], summary='Returns genres')
async def get_genres():
    genres = await get_genres_from_db()
    if len(genres) == 0:
        raise HTTPException(status_code=404, detail="No genres in db")
    return genres
