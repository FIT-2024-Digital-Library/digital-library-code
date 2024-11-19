from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select, insert

from app.db.database import async_session_maker
from app.db.models import user_table
from app.schemas.users import UserRegister, UserLogin
from app.users.auth import get_password_hash, verify_password


async def register_user(user_data: UserRegister):
    async with async_session_maker() as session:
        query = select(user_table).where(user_table.c.email == user_data.email)
        result = await session.execute(query)
        result = result.first()
        if result:
            raise HTTPException(status_code=409, detail="User already exists")
        user_dict = user_data.model_dump()

        user_dict["password_hash"] = get_password_hash(user_data.password)
        user_dict['privileges'] = "basic"
        user_dict.pop("password")
        query = insert(user_table).values(**user_dict)
        result = await session.execute(query)
        await session.commit()
        return result.inserted_primary_key[0]


async def login_user(user_data: UserLogin):
    async with async_session_maker() as session:
        query = select(user_table).where(user_table.c.email == user_data.email)
        result = await session.execute(query)
        user = result.mappings().first()
        if not user or verify_password(plain_password=user_data.password,
                                       hashed_password=user["password_hash"]) is False:
            return None
        return user


async def find_user_by_id(id: int):
    async with async_session_maker() as session:
        query = select(
            user_table.c.id,
            user_table.c.email,
            user_table.c.name,
            user_table.c.privileges
        ).where(user_table.c.id == id)

        result = await session.execute(query)
        user = result.mappings().first()
        return user
