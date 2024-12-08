from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query

from app.crud.authors import get_author_from_db, get_authors_from_db, create_author_in_db, \
    delete_author_from_db, update_author_in_db
from app.schemas import Author, AuthorCreate
from app.utils import CrudException, get_current_user


router = APIRouter(
    prefix='/authors',
    tags=['authors']
)


@router.get('/', response_model=List[Author], summary='Returns authors')
async def get_authors(name: Optional[str] = Query(None, description="Find by author name")):
    authors = await get_authors_from_db(name)
    if authors is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return authors


@router.get('/{author_id}', response_model=Author, summary='Returns author')
async def get_author(author_id: int):
    author = await get_author_from_db(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post('/create', response_model=int, summary='Creates authors')
async def create_author(author: AuthorCreate, user_data=Depends(get_current_user)):
    key = await get_authors_from_db(name=author.name)
    if len(key) == 0:
        key = await create_author_in_db(author)
    else:
        raise HTTPException(status_code=409, detail="Author already exists")
    return key


@router.delete('/delete/{author_id}', response_model=Author, summary='Deletes authors')
async def delete_author(author_id: int, user_data=Depends(get_current_user)):
    try:
        author = await delete_author_from_db(author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author
    except CrudException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/update/{author_id}', response_model=Author, summary='Updates authors')
async def update_author(author_id: int, author: AuthorCreate, user_data=Depends(get_current_user)):
    try:
        author = await update_author_in_db(author_id, author)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author
    except CrudException as e:
        raise HTTPException(status_code=404, detail=str(e))
