from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert

from app.db.models import *
from app.db.database import async_session_maker
from app.schemas.users import *
from app.users.auth import get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['user']
)

@router.get('/profile', response_model=None, summary='Returns authorized user')
async def get_profile():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object


@router.post('/login', response_model=None, summary='Logs user in')
async def login():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object


@router.post('/register', response_model=None, summary='Creates new user')
async def register(user_data: UserRegister):
    async with async_session_maker() as session:
        query = select(user_table).where(user_table.c.email == user_data.email)
        result = await session.execute(query)
        result = result.first()
        if result:
            raise HTTPException(status_code=409, detail="User already exists")
        user_dict = user_data.model_dump()

        user_dict["password_hash"] = get_password_hash(user_data.password)
        user_dict.pop("password")
        query = insert(user_table).values(**user_dict)
        result = await session.execute(query)
        await session.commit()
        return {'message': str(result.inserted_primary_key)}
