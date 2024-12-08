from pydantic import BaseModel

__all__ = ["Author", "AuthorCreate"]


class Author(BaseModel):
    id: int
    name: str


class AuthorCreate(BaseModel):
    name: str
