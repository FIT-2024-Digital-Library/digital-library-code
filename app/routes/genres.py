from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query

from app.crud.genres import get_genre_from_db, get_genres_from_db, create_genre_in_db, \
    delete_genre_from_db, update_genre_in_db
from app.schemas import Genre, GenreCreate
from app.utils import CrudException
from app.utils.auth import get_current_user


router = APIRouter(
    prefix='/genres',
    tags=['genres']
)


@router.get('/', response_model=List[Genre], summary='Returns genres')
async def get_genres(name: Optional[str] = Query(None, description="Find by genre name")):
    genres = await get_genres_from_db(name)
    if genres is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genres


@router.get('/{genre_id}', response_model=Genre, summary='Returns genre')
async def get_genre(genre_id: int):
    genre = await get_genre_from_db(genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.post('/create', response_model=int, summary='Creates genres')
async def create_genre(genre: GenreCreate, user_data=Depends(get_current_user)):
    key = await get_genres_from_db(name=genre.name)
    if len(key) == 0:
        key = await create_genre_in_db(genre)
    else:
        raise HTTPException(status_code=409, detail="Genre already exists")
    return key


@router.delete('/{genre_id}/delete', response_model=Genre, summary='Deletes genres')
async def delete_genre(genre_id: int, user_data=Depends(get_current_user)):
    try:
        genre = await delete_genre_from_db(genre_id)
        if genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return genre
    except CrudException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/{genre_id}/update', response_model=Genre, summary='Updates genres')
async def update_genre(genre_id: int, genre: GenreCreate, user_data=Depends(get_current_user)):
    try:
        genre = await update_genre_in_db(genre_id, genre)
        if genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return genre
    except CrudException as e:
        raise HTTPException(status_code=404, detail=str(e))
