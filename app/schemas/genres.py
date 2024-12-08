from .base import CamelCaseBaseModel

__all__ = ["Genre", "GenreCreate"]


class Genre(CamelCaseBaseModel):
    id: int
    name: str


class GenreCreate(CamelCaseBaseModel):
    name: str
