from enum import Enum

from pydantic import Field, EmailStr
from .base import CamelCaseBaseModel

__all__ = ["User", "UserLogin", "UserRegister", "UserLogined"]


class PrivilegesEnum(str, Enum):
    BASIC = "basic"
    MODERATOR = "moderator"
    ADMIN = "admin"

    _role_hierarchy = {
        BASIC: 1,
        MODERATOR: 2,
        ADMIN: 3,
    }

    def __lt__(self, other):
        if isinstance(other, PrivilegesEnum):
            return self._role_hierarchy[self] < self._role_hierarchy[other]
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, PrivilegesEnum):
            return self._role_hierarchy[self] <= self._role_hierarchy[other]
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PrivilegesEnum):
            return self._role_hierarchy[self] > self._role_hierarchy[other]
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PrivilegesEnum):
            return self._role_hierarchy[self] >= self._role_hierarchy[other]
        return NotImplemented


class UserRegister(CamelCaseBaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")


class UserLogin(CamelCaseBaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class User(CamelCaseBaseModel):
    id: int
    email: EmailStr = Field(description="Электронная почта")
    name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    privileges: PrivilegesEnum


class UserLogined(CamelCaseBaseModel):
    email: EmailStr = Field(description="Электронная почта")
    name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    privileges: PrivilegesEnum
