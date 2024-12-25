from abc import ABC, abstractmethod

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from app.crud.crud_interface import CrudInterface
from app.models import user_table
from app.schemas import UserRegister, UserLogin, PrivilegesEnum, UserUpdate, UserLogined
from app.utils import get_password_hash, verify_password


class UsersCrud(CrudInterface):
    @classmethod
    async def get(cls, session: AsyncSession, element_id: int):
        query = select(
            user_table.c.id,
            user_table.c.email,
            user_table.c.name,
            user_table.c.privileges
        ).where(user_table.c.id == element_id)
        result = await session.execute(query)
        return result.mappings().first()

    @classmethod
    async def get_multiple(cls, session: AsyncSession, username=None, email=None):
        query = select(
            user_table.c.id,
            user_table.c.email,
            user_table.c.name,
            user_table.c.privileges
        )
        if username:
            query = query.where(user_table.c.name.ilike(f"%{username}%"))
        if email:
            query = query.where(user_table.c.email.ilike(f"%{email}%"))

        result = await session.execute(query)
        users = result.mappings().all()
        return [user for user in users]

    @classmethod
    async def create(cls, session: AsyncSession, model: UserRegister):
        query = select(user_table).where(user_table.c.email == model.email)
        result = await session.execute(query)
        result = result.first()
        if result:
            raise HTTPException(status_code=409, detail="User already exists")

        user_dict = model.model_dump()
        user_dict["password_hash"] = get_password_hash(model.password)
        user_dict['privileges'] = "basic"
        user_dict.pop("password")

        query = insert(user_table).values(**user_dict)
        result = await session.execute(query)
        key = result.inserted_primary_key

        if key and key[0] == 1:
            await cls.set_role_for_user(session, PrivilegesEnum.ADMIN, 1)
            user_dict['privileges'] = "admin"

        user_dict.pop("password_hash")
        return user_dict

    @classmethod
    async def delete(cls, session: AsyncSession, element_id: int):
        user = await cls.get(session, element_id)
        if user:
            query = delete(user_table).where(user_table.c.id == element_id)
            await session.execute(query)
        return user

    @classmethod
    async def update(cls, session: AsyncSession, element_id: int, model: UserUpdate):
        user_current_data = await cls.get(session, element_id)
        if user_current_data is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")

        user_new_dict = model.model_dump()

        for key, value in user_current_data.items():
            if key not in user_new_dict.keys() or user_new_dict[key] is None:
                user_new_dict[key] = value

        if model.password is not None:
            user_new_dict["password_hash"] = get_password_hash(model.password)
        user_new_dict.pop("password")

        query = update(user_table).where(user_table.c.id == element_id).values(**user_new_dict)
        await session.execute(query)

        user = await cls.get(session, element_id)
        return user

    @classmethod
    async def set_role_for_user(cls, session: AsyncSession, privilege: PrivilegesEnum, user_id: int):
        user = await cls.get(session, user_id)
        if user is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")

        query = update(user_table).where(user_table.c.id == user_id).values(privileges=privilege)
        await session.execute(query)
        return await cls.get(session, user_id)

    @classmethod
    async def login(cls, session: AsyncSession, user_data: UserLogin):
        query = select(user_table).where(user_table.c.email == user_data.email)
        result = await session.execute(query)
        user = result.mappings().first()
        if not user or not verify_password(user_data.password, user["password_hash"]):
            return None
        return user
