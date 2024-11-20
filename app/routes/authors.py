from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query

from app.crud.authors import get_author_from_db, get_authors_from_db, create_author_in_db
from app.schemas import Author, AuthorCreate
from app.users.dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    prefix='/authors',
    tags=['authors']
)


@router.get('/', response_model=List[Author], summary='Returns authors')
async def get_authors(
        id: Optional[int] = Query(None, description="Filter by author id"),
        name: Optional[str] = Query(None, description="Find by author name")):
    if id or name:
        author = await get_author_from_db(id=id, name=name)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        authors = [author]
    else:
        authors = await get_authors_from_db()

    return authors


@router.post('/create', response_model=int, summary='Returns authors')
async def create_author(author: AuthorCreate, user_data=Depends(get_current_admin_user)):
    key = await get_author_from_db(name=author.name)
    if key is None:
        key = await create_author_in_db(author)
    else:
        raise HTTPException(status_code=409, detail="Author already exists")
    return key
