from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class CrudInterface(ABC):
    @abstractmethod
    async def get(cls, session: AsyncSession, element_id: int):
        pass

    @abstractmethod
    async def get_multiple(cls, session: AsyncSession):
        pass

    @abstractmethod
    async def create(cls, session: AsyncSession, model: BaseModel):
        pass

    @abstractmethod
    async def delete(cls, session: AsyncSession, element_id: int):
        pass

    @abstractmethod
    async def update(cls, session: AsyncSession, element_id: int, model: BaseModel):
        pass
