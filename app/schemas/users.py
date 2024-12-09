from enum import Enum

from pydantic import Field, EmailStr
from .base import CamelCaseBaseModel

__all__ = ["User", "UserLogin", "UserLogined", "UserRegister"]


class PrivilegesEnum(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"
    MODERATOR = "moderator"


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
