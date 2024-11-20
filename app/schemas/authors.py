from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class Author(BaseModel):
    id: int
    name: str


class AuthorCreate(BaseModel):
    name: str
