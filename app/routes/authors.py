from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.crud.authors import AuthorsCrud
from app.schemas import Author, AuthorCreate, PrivilegesEnum, User
from app.settings import async_session_maker
from app.utils import CrudException
from app.utils.auth import user_has_permissions

router = APIRouter(
    prefix='/authors',
    tags=['authors']
)


@router.get('/', response_model=List[Author], summary='Returns authors')
async def get_authors(name: Optional[str] = Query(None, description="Find by author name")):
    async with async_session_maker() as session:
        authors = await AuthorsCrud.get_multiple(session, name)
        if authors is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return authors


@router.get('/{author_id}', response_model=Author, summary='Returns author')
async def get_author(author_id: int):
    async with async_session_maker() as session:
        author = await AuthorsCrud.get(session, author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author


@router.post('/create', response_model=int, summary='Creates authors')
async def create_author(author: AuthorCreate,
                        user_creds: User = user_has_permissions(PrivilegesEnum.MODERATOR)):
    async with async_session_maker() as session:
        key = await AuthorsCrud.get_multiple(session, name=author.name)
        if len(key) == 0:
            key = await AuthorsCrud.create(session, author)
        else:
            raise HTTPException(status_code=409, detail="Author already exists")
        await session.commit()
        return key


@router.delete('/{author_id}/delete', response_model=Author, summary='Deletes authors')
async def delete_author(author_id: int,
                        user_creds: User = user_has_permissions(PrivilegesEnum.MODERATOR)):
    async with async_session_maker() as session:
        try:
            author = await AuthorsCrud.delete(session, author_id)
            if author is None:
                raise HTTPException(status_code=404, detail="Author not found")
            await session.commit()
            return author
        except CrudException as e:
            raise HTTPException(status_code=404, detail=str(e))


@router.put('/{author_id}/update', response_model=Author, summary='Updates authors')
async def update_author(author_id: int, author: AuthorCreate,
                        user_creds: User = user_has_permissions(PrivilegesEnum.MODERATOR)):
    async with async_session_maker() as session:
        try:
            author = await AuthorsCrud.update(session, author_id, author)
            if author is None:
                raise HTTPException(status_code=404, detail="Author not found")
            await session.commit()
            return author
        except CrudException as e:
            raise HTTPException(status_code=404, detail=str(e))
