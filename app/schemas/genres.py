from pydantic import BaseModel

__all__ = ["Genre", "GenreCreate"]


class Genre(BaseModel):
    id: int
    name: str


class GenreCreate(BaseModel):
    name: str
