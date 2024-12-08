from .base import CamelCaseBaseModel

__all__ = ["Author", "AuthorCreate"]


class Author(CamelCaseBaseModel):
    id: int
    name: str


class AuthorCreate(CamelCaseBaseModel):
    name: str
