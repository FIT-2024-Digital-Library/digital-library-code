from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update

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
        if result.inserted_primary_key:
            user_dict.pop("password_hash")
            return user_dict


async def login_user(user_data: UserLogin):
    async with async_session_maker() as session:
        query = select(user_table).where(
            user_table.c.email == user_data.email)
        result = await session.execute(query)
        user = result.mappings().first()
        if not user or verify_password(plain_password=user_data.password,
                                       hashed_password=user["password_hash"]) is False:
            return None
        return user


async def find_user_by_id(user_id: int):
    async with async_session_maker() as session:
        query = select(
            user_table.c.id,
            user_table.c.email,
            user_table.c.name,
            user_table.c.privileges
        ).where(user_table.c.id == user_id)

        result = await session.execute(query)
        user = result.mappings().first()
        return user


async def delete_user_from_db(user_id: int):
    async with async_session_maker() as session:
        user = await find_user_by_id(user_id)
        if user:
            query = delete(user_table).where(user_table.c.id == user_id)
            await session.execute(query)
            await session.commit()
        return user


async def update_user_in_db(user_id: int, user_data: UserRegister):
    async with async_session_maker() as session:
        user = await find_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")
        user_dict = user_data.model_dump()

        user_dict["password_hash"] = get_password_hash(user_data.password)
        user_dict['privileges'] = "basic"
        user_dict.pop("password")
        query = update(user_table).where(user_table.c.id == user_id).values(**user_dict)
        result = await session.execute(query)
        await session.commit()
        if result.inserted_primary_key:
            user_dict.pop("password_hash")
            return user_dict


async def set_admin_role_for_user(user_id: int):
    async with async_session_maker() as session:
        user = await find_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")

        query = update(user_table).where(user_table.c.id == user_id).values(**{'privileges': 'admin'})
        await session.execute(query)
        await session.commit()
        user = await find_user_by_id(user_id)
        return user
